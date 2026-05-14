"""Google Imagen 4 client wrapper for V5.1.8 Step 4.5 thumb generation.

Returns a dict result so callers stay decoupled from google-genai exceptions.
Pipeline-safe: NEVER raises; sets ok=False + error on failure. Caller skips
silent on missing api_key or generation failure — Step 4.5 must not block
the pipeline.

Imagen 4 returns PNG bytes; caller (run_image_gen.py) converts to WebP via
Pillow before persisting to output/thumbs/<public_slug>.webp.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable

import yaml

from lib.llm.pricing import compute_image_cost

DEFAULT_MODEL = "imagen-4.0-generate-001"
_PLACEHOLDER_TOKENS = ("REPLACE_", "your-", "fixme")


def _read_section(secrets_path: Path) -> dict | None:
    if not secrets_path.exists():
        return None
    raw = yaml.safe_load(secrets_path.read_text(encoding="utf-8"))
    if not raw or not isinstance(raw, dict):
        return None
    # Imagen reuses Gemini section (same Google API key works for both).
    section = raw.get("gemini")
    if not section or not isinstance(section, dict):
        return None
    return section


def load_api_key(secrets_path: Path = Path("data/secrets.yaml")) -> str | None:
    """Read `gemini.api_key` from secrets YAML — reused for Imagen 4 (same
    Google AI Studio key)."""
    section = _read_section(secrets_path)
    if section is None:
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


def _attempt(client: Any, prompt: str, model: str, aspect_ratio: str) -> bytes:
    """Single Imagen call. Returns PNG bytes for the first generated image.

    Schema reference: google-genai >=1.0 `models.generate_images`.
    """
    from google.genai import types  # type: ignore[import-not-found]

    config = types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio=aspect_ratio,
    )
    response = client.models.generate_images(
        model=model,
        prompt=prompt,
        config=config,
    )
    generated = getattr(response, "generated_images", None) or []
    if not generated:
        raise RuntimeError("imagen response missing generated_images")
    first = generated[0]
    image = getattr(first, "image", None)
    if image is None:
        raise RuntimeError("imagen response missing image field on generated_images[0]")
    image_bytes = getattr(image, "image_bytes", None)
    if not isinstance(image_bytes, (bytes, bytearray)) or len(image_bytes) == 0:
        raise RuntimeError("imagen returned empty image_bytes")
    return bytes(image_bytes)


def generate_thumb(
    prompt: str,
    *,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
    aspect_ratio: str = "16:9",
    _client_factory: Callable[[str], Any] | None = None,
) -> dict[str, Any]:
    """Generate a thumbnail image. NEVER raises. Returns result dict.

    Result schema:
        {
          "ok": bool,
          "image_bytes": bytes | None,
          "model": str,
          "cost_usd": float | None,
          "duration_ms": int,
          "error": str | None,
        }

    On success, caller persists `image_bytes` (PNG) + cost_usd. On failure,
    `image_bytes` is None and `error` describes the failure (missing key,
    SDK exception, empty response).
    """
    started = time.monotonic()
    base: dict[str, Any] = {
        "ok": False,
        "image_bytes": None,
        "model": model,
        "cost_usd": None,
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
        image_bytes = _attempt(client, prompt, model, aspect_ratio)
    except Exception as exc:  # noqa: BLE001 — all SDK errors handled the same
        base["error"] = str(exc)
        base["duration_ms"] = int((time.monotonic() - started) * 1000)
        return base

    base.update(
        ok=True,
        image_bytes=image_bytes,
        cost_usd=compute_image_cost(model, n_images=1),
        duration_ms=int((time.monotonic() - started) * 1000),
    )
    return base
