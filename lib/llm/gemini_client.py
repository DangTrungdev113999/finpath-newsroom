"""Gemini 2.5 Pro client wrapper for Step 4.3 parallel article writer.

Returns a dict result so callers stay decoupled from google-genai exceptions.
Retries once on transient failure (Timeout/RuntimeError). Caller is expected to
log + skip-silent on `ok=False` — Step 4.3 must never block the pipeline.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Callable

import yaml

DEFAULT_MODEL = "gemini-2.5-pro"
_PLACEHOLDER_TOKENS = ("REPLACE_", "your-", "fixme")


def load_api_key(secrets_path: Path = Path("data/secrets.yaml")) -> str | None:
    """Read `gemini.api_key` from secrets YAML. Returns None when missing or placeholder.

    Mirrors lib/telegram_publisher.py::load_telegram_config — same graceful-degrade pattern.
    """
    if not secrets_path.exists():
        return None
    raw = yaml.safe_load(secrets_path.read_text(encoding="utf-8"))
    if not raw or not isinstance(raw, dict):
        return None
    section = raw.get("gemini")
    if not section or not isinstance(section, dict):
        return None
    key = section.get("api_key")
    if not isinstance(key, str) or not key.strip():
        return None
    if any(token in key for token in _PLACEHOLDER_TOKENS):
        return None
    return key


def _default_factory(api_key: str):
    from google import genai  # type: ignore[import-not-found]

    return genai.Client(api_key=api_key)


def _attempt(
    client: Any,
    prompt: str,
    model: str,
    timeout_s: int,
) -> str:
    """Single Gemini call. Returns response.text or raises."""
    from google.genai import types  # type: ignore[import-not-found]

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "body": {"type": "string"},
                "word_count": {"type": "integer"},
            },
            "required": ["title", "body", "word_count"],
        },
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
    return text


def generate_article(
    prompt: str,
    *,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
    timeout_s: int = 60,
    _client_factory: Callable[[str], Any] | None = None,
) -> dict[str, Any]:
    """Generate article via Gemini. Retries once. Returns result dict.

    Result schema:
        {
          "ok": bool,
          "title": str | None,
          "body": str | None,
          "word_count": int | None,
          "model": str,
          "error": str | None,
          "duration_ms": int,
        }
    """
    started = time.monotonic()
    base = {
        "ok": False,
        "title": None,
        "body": None,
        "word_count": None,
        "model": model,
        "error": None,
        "duration_ms": 0,
    }

    if not api_key:
        base["error"] = "missing_api_key"
        base["duration_ms"] = int((time.monotonic() - started) * 1000)
        return base

    factory = _client_factory or _default_factory
    last_exc: Exception | None = None
    raw_text: str | None = None

    for attempt in range(2):  # try, retry once
        try:
            client = factory(api_key)
            raw_text = _attempt(client, prompt, model, timeout_s)
            last_exc = None
            break
        except Exception as exc:  # noqa: BLE001 — broad on purpose, all SDK errors handled the same
            last_exc = exc

    base["duration_ms"] = int((time.monotonic() - started) * 1000)

    if last_exc is not None or raw_text is None:
        base["error"] = str(last_exc) if last_exc else "no_response_text"
        return base

    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError:
        base["error"] = "parse_error"
        return base

    title = payload.get("title") if isinstance(payload, dict) else None
    body = payload.get("body") if isinstance(payload, dict) else None
    word_count = payload.get("word_count") if isinstance(payload, dict) else None
    if not isinstance(title, str) or not isinstance(body, str):
        base["error"] = "parse_error"
        return base

    if not isinstance(word_count, int):
        word_count = len(body.split())

    base.update(
        ok=True,
        title=title,
        body=body,
        word_count=word_count,
    )
    return base
