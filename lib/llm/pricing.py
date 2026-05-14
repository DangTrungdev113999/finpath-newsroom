"""Token + image pricing constants and cost computation for V5.1.8.

Public pricing pages (2026-05-14 snapshot):
- Anthropic Claude:      https://www.anthropic.com/pricing
- Google Gemini:         https://ai.google.dev/pricing
- xAI Grok:              https://docs.x.ai/docs/models
- Google Imagen:         https://ai.google.dev/pricing (Imagen 4 standard)

Token prices are USD per 1 million tokens (input / output). Image prices are
flat USD per image.

Cost computation is intentionally simple (linear) — caching discounts, batch
discounts, and free tier are NOT applied. Caller pays sticker price; UI shows
upper bound. This keeps the function pure and easy to test.
"""

from __future__ import annotations

# Per-1M-token prices (USD). Source: provider public pricing pages 2026-05-14.
TOKEN_PRICES: dict[str, tuple[float, float]] = {
    # (input_per_1M, output_per_1M)
    "claude-opus-4-7": (15.0, 75.0),
    "claude-opus-4-6": (15.0, 75.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-sonnet-4-5": (3.0, 15.0),
    "claude-haiku-4-5-20251001": (1.0, 5.0),
    "gemini-2.5-pro": (1.25, 5.0),
    "gemini-2.5-flash": (0.30, 2.5),
    "grok-4.3": (3.0, 15.0),
    "grok-4-0709": (3.0, 15.0),
    "grok-4-latest": (3.0, 15.0),
    "grok-4-fast-non-reasoning": (0.20, 0.50),
    "grok-4-fast-reasoning": (0.20, 0.50),
}

# Flat per-image prices (USD).
IMAGE_PRICES: dict[str, float] = {
    "imagen-4.0-generate-001": 0.04,
    "imagen-4.0-generate-preview-001": 0.04,
    "imagen-3.0-generate-002": 0.04,
    "gemini-2.5-flash-image-preview": 0.039,
}


def compute_cost(model_id: str, in_tokens: int, out_tokens: int) -> float | None:
    """USD cost for a single LLM call.

    Returns None when model_id is unknown (caller stores NULL in DB rather
    than recording a fabricated zero — easier to spot missing pricing later).

    Negative token counts coerce to zero (defensive — some SDKs return
    sentinel values on partial errors).
    """
    if not model_id:
        return None
    prices = TOKEN_PRICES.get(model_id)
    if prices is None:
        return None
    in_per_1m, out_per_1m = prices
    in_tok = max(0, int(in_tokens or 0))
    out_tok = max(0, int(out_tokens or 0))
    return round(
        (in_tok / 1_000_000.0) * in_per_1m + (out_tok / 1_000_000.0) * out_per_1m,
        6,
    )


def compute_image_cost(model_id: str, n_images: int = 1) -> float | None:
    """USD cost for image generation. None when model_id unknown."""
    if not model_id:
        return None
    price = IMAGE_PRICES.get(model_id)
    if price is None:
        return None
    n = max(0, int(n_images or 0))
    return round(price * n, 6)
