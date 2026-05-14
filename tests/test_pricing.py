"""Tests for lib/llm/pricing.py."""

from __future__ import annotations

import pytest

from lib.llm import pricing


def test_claude_opus_pricing() -> None:
    cost = pricing.compute_cost("claude-opus-4-7", in_tokens=100_000, out_tokens=10_000)
    # 100k in × $15/1M + 10k out × $75/1M = 1.5 + 0.75 = 2.25
    assert cost == pytest.approx(2.25)


def test_claude_sonnet_pricing() -> None:
    cost = pricing.compute_cost("claude-sonnet-4-6", in_tokens=1_000_000, out_tokens=200_000)
    # 1M in × $3 + 200k out × $15/1M = 3.0 + 3.0 = 6.0
    assert cost == pytest.approx(6.0)


def test_gemini_pricing() -> None:
    cost = pricing.compute_cost("gemini-2.5-pro", in_tokens=80_000, out_tokens=2_000)
    # 80k × $1.25/1M + 2k × $5/1M = 0.10 + 0.01 = 0.11
    assert cost == pytest.approx(0.11)


def test_grok_pricing() -> None:
    cost = pricing.compute_cost("grok-4.3", in_tokens=50_000, out_tokens=5_000)
    # 50k × $3/1M + 5k × $15/1M = 0.15 + 0.075 = 0.225
    assert cost == pytest.approx(0.225)


def test_unknown_model_returns_none() -> None:
    assert pricing.compute_cost("gpt-5-turbo", 100, 100) is None


def test_zero_tokens_returns_zero() -> None:
    assert pricing.compute_cost("claude-sonnet-4-6", 0, 0) == 0.0


def test_negative_tokens_coerce_to_zero() -> None:
    """Defensive: SDK may emit -1 sentinel on partial error — treat as 0."""
    assert pricing.compute_cost("gemini-2.5-pro", -1, -1) == 0.0


def test_imagen_4_cost() -> None:
    assert pricing.compute_image_cost("imagen-4.0-generate-001") == pytest.approx(0.04)


def test_imagen_4_multi_image() -> None:
    assert pricing.compute_image_cost("imagen-4.0-generate-001", n_images=3) == pytest.approx(0.12)


def test_unknown_image_model_returns_none() -> None:
    assert pricing.compute_image_cost("dalle-3") is None


def test_empty_model_id_returns_none() -> None:
    assert pricing.compute_cost("", 100, 100) is None
    assert pricing.compute_image_cost("") is None
