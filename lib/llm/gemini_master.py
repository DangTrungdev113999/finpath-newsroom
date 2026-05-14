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


def _attempt(
    client: Any,
    prompt: str,
    tools: ResearchTools,
    model: str,
    timeout_s: int,
) -> tuple[str, dict[str, int]]:
    """Single Gemini call with automatic function calling. Returns (text, usage)."""
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
    return text, usage


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
        raw_text, usage = _attempt(client, prompt, tools, model, timeout_s)
    except Exception as exc:  # noqa: BLE001
        base["error"] = str(exc)
        base["duration_ms"] = int((time.monotonic() - started) * 1000)
        return base

    base["usage"] = usage
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
