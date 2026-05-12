"""Tests for lib/stages/run_market_snapshot — Step 1.5 fetch ticker quote.

Soft-fetch by design: failure returns None, never raises.
"""
from __future__ import annotations
import json
from unittest.mock import MagicMock, patch
import pytest
from lib.stages.run_market_snapshot import fetch_market_snapshot, MarketSnapshot


def test_fetch_returns_none_when_api_unavailable():
    """Network error → return None, do not raise."""
    with patch("lib.stages.run_market_snapshot.FinpathAPI") as mock_api:
        mock_api.return_value.get_quote.side_effect = ConnectionError("network down")
        result = fetch_market_snapshot("VCB")
        assert result is None


def test_fetch_returns_none_when_no_get_quote_method():
    """If FinpathAPI doesn't expose get_quote, soft-fail returns None."""
    with patch("lib.stages.run_market_snapshot.FinpathAPI") as mock_api:
        # Simulate missing method (current API state)
        del mock_api.return_value.get_quote
        result = fetch_market_snapshot("VCB")
        assert result is None


def test_fetch_returns_snapshot_on_success():
    """Happy path: API returns dict with price + pct_change."""
    fake_quote = {"price": 92500, "pct_change": -3.2, "volume_ratio_3d": 1.4}
    with patch("lib.stages.run_market_snapshot.FinpathAPI") as mock_api:
        mock_api.return_value.get_quote.return_value = fake_quote
        result = fetch_market_snapshot("VCB")
        assert result is not None
        assert result.price_today == 92500
        assert result.pct_change_today == -3.2
        assert result.volume_ratio_3d == 1.4
        assert result.fetched_at  # ISO 8601 timestamp set


def test_fetch_returns_none_when_response_missing_price():
    """Malformed response without 'price' key → None (defensive)."""
    with patch("lib.stages.run_market_snapshot.FinpathAPI") as mock_api:
        mock_api.return_value.get_quote.return_value = {"junk": "data"}
        result = fetch_market_snapshot("VCB")
        assert result is None


def test_snapshot_to_dict():
    """MarketSnapshot serializable to brief.ticker_market_data shape."""
    snap = MarketSnapshot(price_today=100, pct_change_today=2.5, volume_ratio_3d=1.1, fetched_at="2026-05-11T14:00:00+00:00")
    d = snap.to_dict()
    assert d == {
        "price_today": 100,
        "pct_change_today": 2.5,
        "volume_ratio_3d": 1.1,
        "fetched_at": "2026-05-11T14:00:00+00:00",
    }
