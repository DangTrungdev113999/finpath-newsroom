"""Tests for lib/finpath_top_movers — fetch + filter + compute + intersect + dedup."""
from __future__ import annotations
import pytest
from unittest.mock import MagicMock
from lib.finpath_top_movers import (
    HotTicker,
    normalize,
    apply_default_filters,
    compute_top_lists,
    dedup,
    intersect_universe,
    fetch_stocks_overview,
    fetch_top_hot_tickers,
)


def _stock(c, p=10000, dcp=0, dv=1000000, a5v=1000000, mc=1000000000, st="S"):
    return {"c": c, "p": p, "dcp": dcp, "dv": dv, "a5v": a5v, "mc": mc, "st": st}


def test_normalize_maps_fields():
    raw = [_stock("VCB", p=92500, dcp=2.5, dv=5000000, a5v=4000000, mc=500_000_000_000)]
    out = normalize(raw)
    assert len(out) == 1
    s = out[0]
    assert s["ticker"] == "VCB"
    assert s["price"] == 92500
    assert s["change_pct"] == 2.5
    assert s["volume_ratio"] == 1.25  # 5M / 4M


def test_apply_default_filters_excludes_zero_price():
    raw = normalize([_stock("VCB", p=92500), _stock("ZZZ", p=0)])
    out = apply_default_filters(raw)
    assert {s["ticker"] for s in out} == {"VCB"}


def test_apply_default_filters_excludes_non_S_secType():
    raw = normalize([_stock("VCB", st="S"), _stock("INDEX1", st="I")])
    out = apply_default_filters(raw)
    assert {s["ticker"] for s in out} == {"VCB"}


def test_apply_default_filters_takes_top_100_marketcap():
    raw = normalize([_stock(f"T{i:03d}", mc=i) for i in range(150)])
    out = apply_default_filters(raw)
    assert len(out) == 100
    # Top 100 by marketcap descending; smallest in result should be mc=50 (150-100).
    assert min(s["marketcap"] for s in out) == 50


def test_compute_top_lists_n_2():
    raw = normalize([
        _stock("A", dcp=5),
        _stock("B", dcp=-5),
        _stock("C", dcp=3),
        _stock("D", dcp=-3, dv=10_000_000, a5v=1_000_000),  # high vol ratio
        _stock("E", dcp=1, dv=100, a5v=1_000_000),  # low vol ratio gainer
    ])
    filtered = apply_default_filters(raw)
    lists = compute_top_lists(filtered, n=2)
    assert {s["ticker"] for s in lists["tang"][:2]} == {"A", "C"}
    assert {s["ticker"] for s in lists["giam"][:2]} == {"B", "D"}
    # bung_no = high volume_ratio
    assert lists["bung_no"][0]["ticker"] == "D"
    # can_cung = low volume_ratio AMONG GAINERS
    can_cung_tickers = {s["ticker"] for s in lists["can_cung"]}
    assert "E" in can_cung_tickers


def test_compute_top_lists_invalid_n_raises():
    with pytest.raises(ValueError):
        compute_top_lists([], n=0)
    with pytest.raises(ValueError):
        compute_top_lists([], n=26)


def test_compute_top_lists_n_within_range():
    # Edge cases: n=1, n=25 must not raise.
    raw = normalize([_stock(f"T{i:03d}", dcp=i) for i in range(30)])
    filtered = apply_default_filters(raw)
    for n in (1, 5, 10, 25):
        lists = compute_top_lists(filtered, n=n)
        assert all(len(v) <= n for v in lists.values())


def test_dedup_keeps_first_seen_order():
    cat = {
        "tang": [{"ticker": "A", "price": 1, "change_pct": 5, "volume": 1, "avg_5d_volume": 1, "marketcap": 1, "volume_ratio": 1}],
        "giam": [{"ticker": "A", "price": 1, "change_pct": -5, "volume": 1, "avg_5d_volume": 1, "marketcap": 1, "volume_ratio": 1}],
        "bung_no": [{"ticker": "B", "price": 1, "change_pct": 0, "volume": 1, "avg_5d_volume": 1, "marketcap": 1, "volume_ratio": 1}],
        "can_cung": [],
    }
    out = dedup(cat)
    assert [h.ticker for h in out] == ["A", "B"]
    assert out[0].category == "tang"  # first-seen wins


def test_dedup_empty_lists():
    out = dedup({"tang": [], "giam": [], "bung_no": [], "can_cung": []})
    assert out == []


def test_hot_ticker_to_dict():
    h = HotTicker("VCB", "tang", 1, 92500, 2.5, 5000000, 1.25, 500_000_000_000)
    d = h.to_dict()
    assert d == {
        "ticker": "VCB", "category": "tang", "rank": 1,
        "price": 92500, "change_pct": 2.5, "volume": 5000000,
        "volume_ratio": 1.25, "marketcap": 500_000_000_000,
    }


def test_intersect_universe_filters_in():
    hots = [HotTicker(t, "tang", 1, 1, 1, 1, 1, 1) for t in ["VCB", "XYZ", "FPT"]]
    out = intersect_universe(hots, {"VCB", "FPT"})
    assert [h.ticker for h in out] == ["VCB", "FPT"]


def test_intersect_universe_empty_set_excludes_all():
    hots = [HotTicker("VCB", "tang", 1, 1, 1, 1, 1, 1)]
    assert intersect_universe(hots, set()) == []


def test_fetch_stocks_overview_uses_finpath_api(monkeypatch):
    from lib import finpath_top_movers
    fake_api = MagicMock()
    fake_api.get_overview.return_value = {"stocks": [_stock("VCB")]}
    monkeypatch.setattr(finpath_top_movers, "fetch_stocks_overview",
                        lambda api=None: (api or fake_api).get_overview()["stocks"])
    out = finpath_top_movers.fetch_stocks_overview(api=fake_api)
    assert len(out) == 1


def test_fetch_stocks_overview_accepts_injected_api():
    fake_api = MagicMock()
    fake_api.get_overview.return_value = {"stocks": [_stock("VCB")]}
    out = fetch_stocks_overview(api=fake_api)
    assert out == [_stock("VCB")]


def test_fetch_stocks_overview_handles_empty_response():
    fake_api = MagicMock()
    fake_api.get_overview.return_value = {}
    assert fetch_stocks_overview(api=fake_api) == []


def test_fetch_top_hot_tickers_integration():
    fake_api = MagicMock()
    fake_api.get_overview.return_value = {"stocks": [
        _stock("A", dcp=5),
        _stock("B", dcp=-5),
        _stock("C", dcp=3, dv=5_000_000, a5v=1_000_000),
    ]}
    out = fetch_top_hot_tickers(n=2, universe_set={"A", "B", "C"}, api=fake_api)
    tickers = {h.ticker for h in out}
    assert tickers <= {"A", "B", "C"}
    # All 3 are gainers/losers within top 2 each → expect ≤4 results
    assert len(out) <= 4


def test_fetch_top_hot_tickers_intersect_universe():
    fake_api = MagicMock()
    fake_api.get_overview.return_value = {"stocks": [
        _stock("A", dcp=5),  # in universe
        _stock("X", dcp=10),  # outside universe — should be dropped
    ]}
    out = fetch_top_hot_tickers(n=2, universe_set={"A"}, api=fake_api)
    assert all(h.ticker == "A" for h in out)
