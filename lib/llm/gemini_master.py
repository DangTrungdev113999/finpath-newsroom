"""V5.1.9 Gemini Master — free-style with native automatic function calling.

Promotes Gemini 2.5 Pro from "parallel Writer" (reuses Claude data_trail) to
full Master role with tool access. SDK's automatic_function_calling handles
the tool-call loop natively; we cap at 8 remote calls. Returns the same
extended JSON shape Claude Master used to emit (title, body, data_trail,
chosen_question_idx, insight_final, key_view, etc.).

Pipeline-safe: NEVER raises. `ok=False` on missing key / SDK error / parse
failure. Caller logs and skips Step 4 — Telegram/web gracefully degrade
when both Gemini AND Grok fail (V5.1.8 publish_article_v5 already handles).
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Callable

import yaml

from lib.llm import gemini_client
from lib.llm.research_tools import ResearchTools

DEFAULT_MODEL = "gemini-2.5-pro"
MAX_REMOTE_CALLS = 8
DEFAULT_TIMEOUT = 180  # seconds; multi-turn so larger than non-Master


def _default_factory(api_key: str):
    from google import genai  # type: ignore[import-not-found]

    return genai.Client(api_key=api_key)


def _output_schema() -> dict:
    """JSON schema for final response (genai response_schema)."""
    return {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "body": {"type": "string"},
            "word_count": {"type": "integer"},
            "chosen_question_idx": {"type": "integer"},
            "chosen_pick_reason": {"type": "string"},
            "skip_reasons": {"type": "object"},
            "insight_final": {"type": "string"},
            "key_view": {"type": "string"},
            "variety_guard_angle": {"type": "string"},
            "format_id_used": {"type": "string"},
            "format_escalation_reason": {"type": "string"},
            "data_trail": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string"},
                        "fetched": {"type": "string"},
                        "purpose": {"type": "string"},
                        "supports_argument": {"type": "string"},
                    },
                    "required": ["source", "fetched"],
                },
            },
            "gates_passed": {"type": "boolean"},
        },
        "required": ["title", "body", "word_count", "chosen_question_idx", "data_trail"],
    }


def _extract_tool_history(response: Any) -> list[dict[str, Any]]:
    """Parse `response.automatic_function_calling_history` (genai SDK ground
    truth — what tools the LLM actually invoked + what payload came back) into
    a serializable list of {name, args, ok, source, summary} dicts.

    Each Content in history alternates role='model' (carrying function_calls)
    and role='user' (carrying function_responses). We pair them by order so
    the timeline reads sequentially.
    """
    history = getattr(response, "automatic_function_calling_history", None) or []
    out: list[dict[str, Any]] = []
    pending_calls: list[dict[str, Any]] = []
    for content in history:
        parts = getattr(content, "parts", None) or []
        role = getattr(content, "role", "")
        for part in parts:
            fc = getattr(part, "function_call", None)
            fr = getattr(part, "function_response", None)
            if fc is not None and role == "model":
                pending_calls.append({
                    "name": getattr(fc, "name", None),
                    "args": dict(getattr(fc, "args", None) or {}),
                })
            elif fr is not None and role == "user":
                resp = getattr(fr, "response", None) or {}
                # Tool callables return {"ok", "source", "data" or "error"}
                entry = pending_calls.pop(0) if pending_calls else {"name": getattr(fr, "name", None), "args": {}}
                entry["ok"] = bool(resp.get("ok", True))
                entry["source"] = resp.get("source")
                # Trim heavy 'data' payload for log size; keep error message intact.
                if "error" in resp:
                    entry["summary"] = f"error: {resp['error']}"
                else:
                    data = resp.get("data")
                    entry["summary"] = _summarize_tool_data(data)
                out.append(entry)
    return out


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


def _attempt(
    client: Any,
    prompt: str,
    tools: ResearchTools,
    model: str,
    timeout_s: int,
) -> tuple[str, dict[str, int], list[dict[str, Any]]]:
    """Single Gemini call with automatic function calling.
    Returns (text, usage, tool_history)."""
    from google.genai import types  # type: ignore[import-not-found]

    config = types.GenerateContentConfig(
        tools=tools.callables,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            maximum_remote_calls=MAX_REMOTE_CALLS,
        ),
        response_mime_type="application/json",
        response_schema=_output_schema(),
        http_options=types.HttpOptions(timeout=timeout_s * 1000),
    )
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    text = getattr(response, "text", None)
    if not isinstance(text, str):
        raise RuntimeError(f"unexpected response.text type: {type(text)!r}")
    usage: dict[str, int] = {}
    meta = getattr(response, "usage_metadata", None)
    if meta is not None:
        in_tok = getattr(meta, "prompt_token_count", None)
        out_tok = getattr(meta, "candidates_token_count", None)
        if isinstance(in_tok, int):
            usage["prompt_tokens"] = in_tok
        if isinstance(out_tok, int):
            usage["completion_tokens"] = out_tok
    tool_history = _extract_tool_history(response)
    return text, usage, tool_history


def generate_article(
    prompt: str,
    *,
    tools: ResearchTools,
    api_key: str | None,
    model: str = DEFAULT_MODEL,
    timeout_s: int = DEFAULT_TIMEOUT,
    _client_factory: Callable[[str], Any] | None = None,
) -> dict[str, Any]:
    """Run Gemini Master with tool access. NEVER raises.

    Result schema:
        {
          "ok": bool,
          "payload": dict | None,   # full parsed JSON output
          "model": str,
          "usage": {"prompt_tokens": int, "completion_tokens": int} | {},
          "duration_ms": int,
          "error": str | None,
        }

    `payload` mirrors the extended Master JSON output (title, body, data_trail,
    chosen_question_idx, ...). On any failure, payload=None.
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
        client = factory(api_key)
        raw_text, usage, tool_history = _attempt(client, prompt, tools, model, timeout_s)
    except Exception as exc:  # noqa: BLE001
        base["error"] = str(exc)
        base["duration_ms"] = int((time.monotonic() - started) * 1000)
        return base

    base["usage"] = usage
    base["tool_history"] = tool_history
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError:
        base["error"] = "parse_error"
        base["duration_ms"] = int((time.monotonic() - started) * 1000)
        return base

    if not isinstance(payload, dict):
        base["error"] = "parse_error"
        base["duration_ms"] = int((time.monotonic() - started) * 1000)
        return base

    # Required fields
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
    """Shared with gemini_client — re-export so callers have one import."""
    return gemini_client.load_api_key(secrets_path)
