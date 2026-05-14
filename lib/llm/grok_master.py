"""V5.1.9 Grok Master — free-style with manual OpenAI-compat tool-call loop.

xAI Grok doesn't have native automatic function calling in the openai SDK, so
we run the loop ourselves: send messages → check for tool_calls in the
response → dispatch tool, append result as 'tool' role → repeat until model
returns a final text answer or we hit MAX_TURNS.

Pipeline-safe: NEVER raises. Same `{ok, payload, usage, duration_ms, error}`
shape as gemini_master.generate_article so the orchestrator can treat them
interchangeably.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Callable

from lib.llm import grok_client
from lib.llm.research_tools import ResearchTools

DEFAULT_MODEL = grok_client.DEFAULT_MODEL  # "grok-4.3"
XAI_BASE_URL = grok_client.XAI_BASE_URL
MAX_TURNS = 8
DEFAULT_TIMEOUT = 60


def _default_factory(api_key: str, base_url: str):
    from openai import OpenAI  # type: ignore[import-not-found]

    # max_retries=0: we own the retry policy (none for Master loop; cost-bound)
    return OpenAI(api_key=api_key, base_url=base_url, max_retries=0)


def _exec_tool(tools: ResearchTools, fn_name: str, fn_args: dict) -> dict:
    """Execute one tool call. Wraps errors as {ok: False, error: ...}."""
    fn = tools.dispatch.get(fn_name)
    if fn is None:
        return {"ok": False, "error": f"unknown_tool: {fn_name}"}
    try:
        return fn(**fn_args)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}


def _summarize_tool_data(data: Any, max_len: int = 200) -> str:
    """Short string summary of a tool response payload for log emission."""
    if data is None:
        return "(no data)"
    if isinstance(data, list):
        return f"list[{len(data)}]" + (f" first={list(data)[0]}"[:max_len] if data else "")
    if isinstance(data, dict):
        keys = list(data.keys())[:6]
        return f"dict keys={keys}"
    s = str(data)
    return s[:max_len] + ("…" if len(s) > max_len else "")


def generate_article(
    prompt: str,
    *,
    tools: ResearchTools,
    api_key: str | None,
    model: str = DEFAULT_MODEL,
    timeout_s: int = DEFAULT_TIMEOUT,
    max_turns: int = MAX_TURNS,
    _client_factory: Callable[[str, str], Any] | None = None,
) -> dict[str, Any]:
    """Run Grok Master with manual tool-call loop. NEVER raises.

    Returns same result schema as gemini_master.generate_article:
        {ok, payload, model, usage, duration_ms, error}

    `usage` aggregates prompt_tokens + completion_tokens across all turns.
    """
    started = time.monotonic()
    base: dict[str, Any] = {
        "ok": False,
        "payload": None,
        "model": model,
        "usage": {},
        "tool_history": [],
        "duration_ms": 0,
        "error": None,
    }
    if not api_key:
        base["error"] = "missing_api_key"
        base["duration_ms"] = int((time.monotonic() - started) * 1000)
        return base

    factory = _client_factory or _default_factory
    try:
        client = factory(api_key, XAI_BASE_URL)
    except Exception as exc:  # noqa: BLE001
        base["error"] = f"client_init_failed: {exc}"
        base["duration_ms"] = int((time.monotonic() - started) * 1000)
        return base

    messages: list[dict] = [{"role": "user", "content": prompt}]
    total_in = 0
    total_out = 0
    final_content: str | None = None
    tool_history: list[dict[str, Any]] = []

    for turn in range(max_turns):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools.openai_schema,
                response_format={"type": "json_object"},
                timeout=timeout_s,
            )
        except Exception as exc:  # noqa: BLE001
            base["error"] = f"turn_{turn}: {exc}"
            base["usage"] = {"prompt_tokens": total_in, "completion_tokens": total_out}
            base["duration_ms"] = int((time.monotonic() - started) * 1000)
            return base

        usage = getattr(resp, "usage", None)
        if usage is not None:
            total_in += getattr(usage, "prompt_tokens", 0) or 0
            total_out += getattr(usage, "completion_tokens", 0) or 0

        choices = getattr(resp, "choices", None) or []
        if not choices:
            base["error"] = f"turn_{turn}: empty_choices"
            break
        msg = choices[0].message

        tool_calls = getattr(msg, "tool_calls", None) or []
        if not tool_calls:
            final_content = getattr(msg, "content", None)
            break

        # Append assistant message + each tool result back into context.
        messages.append({
            "role": "assistant",
            "content": getattr(msg, "content", None),
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in tool_calls
            ],
        })
        for tc in tool_calls:
            fn_name = tc.function.name
            try:
                fn_args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                fn_args = {}
            result = _exec_tool(tools, fn_name, fn_args)
            # V5.1.9.1 — capture SDK-side ground-truth tool log (mirrors
            # gemini_master._extract_tool_history shape).
            history_entry: dict[str, Any] = {
                "name": fn_name,
                "args": fn_args,
                "ok": bool(result.get("ok", True)),
                "source": result.get("source"),
            }
            if "error" in result:
                history_entry["summary"] = f"error: {result['error']}"
            else:
                history_entry["summary"] = _summarize_tool_data(result.get("data"))
            tool_history.append(history_entry)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result, ensure_ascii=False)[:8000],  # cap per-tool feedback
            })
    else:
        # Loop exhausted without final answer
        base["error"] = f"max_turns_reached ({max_turns})"
        base["usage"] = {"prompt_tokens": total_in, "completion_tokens": total_out}
        base["duration_ms"] = int((time.monotonic() - started) * 1000)
        return base

    base["usage"] = {"prompt_tokens": total_in, "completion_tokens": total_out}
    base["tool_history"] = tool_history

    if final_content is None:
        base["error"] = base["error"] or "no_final_content"
        base["duration_ms"] = int((time.monotonic() - started) * 1000)
        return base

    try:
        payload = json.loads(final_content)
    except json.JSONDecodeError:
        base["error"] = "parse_error"
        base["duration_ms"] = int((time.monotonic() - started) * 1000)
        return base

    if not isinstance(payload, dict):
        base["error"] = "parse_error"
        base["duration_ms"] = int((time.monotonic() - started) * 1000)
        return base

    if not isinstance(payload.get("title"), str) or not isinstance(payload.get("body"), str):
        base["error"] = "missing_required_fields"
        base["duration_ms"] = int((time.monotonic() - started) * 1000)
        return base

    if not isinstance(payload.get("word_count"), int):
        payload["word_count"] = len(payload["body"].split())

    base.update(ok=True, payload=payload)
    base["duration_ms"] = int((time.monotonic() - started) * 1000)
    return base


def load_api_key(secrets_path: Path = Path("data/secrets.yaml")) -> str | None:
    return grok_client.load_api_key(secrets_path)


def load_model(secrets_path: Path = Path("data/secrets.yaml")) -> str:
    return grok_client.load_model(secrets_path)
