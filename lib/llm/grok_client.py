"""xAI Grok client wrapper for Step 4.4 parallel article writer.

Returns a dict result so callers stay decoupled from openai SDK exceptions.
Retries once on transient failure. Caller is expected to log + skip-silent on
`ok=False` — Step 4.4 must never block the pipeline.

Uses the `openai` Python SDK with `base_url='https://api.x.ai/v1'` because
xAI exposes an OpenAI-compatible REST API. This avoids pulling in `xai-sdk`
(gRPC) for a single chat completions call.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Callable

import yaml

DEFAULT_MODEL = "grok-4-latest"
XAI_BASE_URL = "https://api.x.ai/v1"
_PLACEHOLDER_TOKENS = ("REPLACE_", "your-", "fixme")


def _read_section(secrets_path: Path) -> dict | None:
    if not secrets_path.exists():
        return None
    raw = yaml.safe_load(secrets_path.read_text(encoding="utf-8"))
    if not raw or not isinstance(raw, dict):
        return None
    section = raw.get("grok")
    if not section or not isinstance(section, dict):
        return None
    return section


def load_api_key(secrets_path: Path = Path("data/secrets.yaml")) -> str | None:
    """Read `grok.api_key` from secrets YAML. Returns None when missing or placeholder."""
    section = _read_section(secrets_path)
    if section is None:
        return None
    key = section.get("api_key")
    if not isinstance(key, str) or not key.strip():
        return None
    if any(token in key for token in _PLACEHOLDER_TOKENS):
        return None
    return key


def load_model(secrets_path: Path = Path("data/secrets.yaml")) -> str:
    """Read `grok.model` override or fall back to DEFAULT_MODEL."""
    section = _read_section(secrets_path)
    if section is None:
        return DEFAULT_MODEL
    model = section.get("model")
    if isinstance(model, str) and model.strip():
        return model.strip()
    return DEFAULT_MODEL


def _default_factory(api_key: str, base_url: str):
    from openai import OpenAI  # type: ignore[import-not-found]

    return OpenAI(api_key=api_key, base_url=base_url)


def _attempt(
    client: Any,
    prompt: str,
    model: str,
    timeout_s: int,
) -> str:
    """Single Grok call. Returns choices[0].message.content or raises."""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        timeout=timeout_s,
    )
    choices = getattr(response, "choices", None) or []
    if not choices:
        raise RuntimeError("empty choices in response")
    message = getattr(choices[0], "message", None)
    content = getattr(message, "content", None) if message is not None else None
    if not isinstance(content, str):
        raise RuntimeError(f"unexpected message.content type: {type(content)!r}")
    return content


def generate_article(
    prompt: str,
    *,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
    timeout_s: int = 60,
    _client_factory: Callable[[str, str], Any] | None = None,
) -> dict[str, Any]:
    """Generate article via Grok. Retries once. Returns result dict.

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
    base: dict[str, Any] = {
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
            client = factory(api_key, XAI_BASE_URL)
            raw_text = _attempt(client, prompt, model, timeout_s)
            last_exc = None
            break
        except Exception as exc:  # noqa: BLE001 — all SDK + transport errors handled the same
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
