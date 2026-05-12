"""Tests for lib/finpath_top_movers — fetch + filter + intersect + compute + dedup.

Plan A spec: source-of-truth is finpath-web/stockDataUtils.ts with the
following invariants:
- Field mapping per FIELD_MAP (c/dcp/dvp/dv/mc/a5v/p/st → canonical names)
- DEFAULT_FILTERS: top 100 marketCap + avgDay5Value ≥ 10 tỷ VND + price > 0
  + secType == "S"
- 4 categories: price_increment / price_decrement (by dayChangePercent),
  volume_explosion / depleted_supply (by dayVolPercent, both filter >= 0)
- N range 1-10
- depleted_supply = filter dvp >= 0, sort ASC (verbatim from source)
"""
from __future__ import annotations
import pytest
from unittest.mock import MagicMock
from lib.finpath_top_movers import (
    HotTicker,
    CATEGORIES,
    LIQUIDITY_THRESHOLD_BILLION,
    _normalize,
    fetch_stocks_overview,
    apply_default_filters,
    intersect_universe,
    compute_top_lists,
    dedup_tickers,
    fetch_top_hot_tickers,
)


def _raw(c, dcp=0, dvp=0, dv=1000000, a5v=20_000_000_000, mc=10**12, p=10000, st="S"):
    """Build raw API-shape stock dict (short field names per live API verification).

    Real /v2/overview fields: c / dcp / dvp / dv / ad5v / mkc / p / ste.
    """
    return {"c": c, "dcp": dcp, "dvp": dvp, "dv": dv,
            "ad5v": a5v, "mkc": mc, "p": p, "ste": st}


# === Normalization ===

def test_normalize_maps_short_to_canonical():
    n = _normalize(_raw("VCB", dcp=2.5, dvp=15.0, p=92500, mc=500_000_000_000))
    assert n["code"] == "VCB"
    assert n["dayChangePercent"] == 2.5
    assert n["dayVolPercent"] == 15.0
    assert n["price"] == 92500
    assert n["marketCap"] == 500_000_000_000
    assert n["secType"] == "S"


def test_normalize_unknown_keys_pass_through():
    n = _normalize({"c": "VCB", "foo": "bar"})
    assert n == {"code": "VCB", "foo": "bar"}


# === Filters ===

def test_filter_excludes_zero_price():
    stocks = [_normalize(_raw("VCB", p=92500)), _normalize(_raw("ZZZ", p=0))]
    out = apply_default_filters(stocks)
    assert {s["code"] for s in out} == {"VCB"}


def test_filter_excludes_non_S_secType():
    stocks = [_normalize(_raw("VCB", st="S")), _normalize(_raw("VNX", st="I"))]
    out = apply_default_filters(stocks)
    assert {s["code"] for s in out} == {"VCB"}


def test_filter_excludes_low_liquidity():
    """avgDay5Value < 10 tỷ → excluded."""
    threshold = LIQUIDITY_THRESHOLD_BILLION * 1_000_000_000
    stocks = [
        _normalize(_raw("VCB", a5v=threshold + 1)),
        _normalize(_raw("LOW", a5v=threshold - 1)),
    ]
    out = apply_default_filters(stocks)
    assert {s["code"] for s in out} == {"VCB"}


def test_filter_takes_top_100_marketcap():
    """Top 100 by marketCap descending."""
    stocks = [_normalize(_raw(f"T{i:03d}", mc=i * 10**11)) for i in range(150)]
    out = apply_default_filters(stocks)
    assert len(out) == 100
    codes = {s["code"] for s in out}
    # Bottom 50 (mc=0..49) dropped — but mc=0 also fails liquidity? Actually
    # all use default a5v=20 tỷ which passes. mc=0 just means lowest sort.
    # Top 100 by mc desc = mc=149..50.
    assert "T149" in codes
    assert "T050" in codes
    assert "T049" not in codes


# === Intersect universe ===

def test_intersect_universe_filters_in():
    stocks = [_normalize(_raw(c)) for c in ["VCB", "XYZ", "FPT"]]
    out = intersect_universe(stocks, {"VCB", "FPT"})
    assert [s["code"] for s in out] == ["VCB", "FPT"]


def test_intersect_universe_empty_set_excludes_all():
    stocks = [_normalize(_raw("VCB"))]
    assert intersect_universe(stocks, set()) == []


# === compute_top_lists ===

def test_compute_top_n_validation():
    with pytest.raises(ValueError):
        compute_top_lists([], n=0)
    with pytest.raises(ValueError):
        compute_top_lists([], n=11)


def test_compute_price_increment_sorted_desc():
    stocks = [
        _normalize(_raw("A", dcp=5)),
        _normalize(_raw("B", dcp=3)),
        _normalize(_raw("C", dcp=-2)),
    ]
    lists = compute_top_lists(stocks, n=2)
    pi = lists["price_increment"]
    assert [h.code for h in pi] == ["A", "B"]
    assert pi[0].rank == 1
    assert pi[1].rank == 2


def test_compute_price_decrement_sorted_asc():
    stocks = [
        _normalize(_raw("A", dcp=5)),
        _normalize(_raw("B", dcp=-3)),
        _normalize(_raw("C", dcp=-5)),
    ]
    lists = compute_top_lists(stocks, n=2)
    pd = lists["price_decrement"]
    assert [h.code for h in pd] == ["C", "B"]


def test_compute_volume_explosion_sorted_desc():
    stocks = [
        _normalize(_raw("A", dvp=20)),
        _normalize(_raw("B", dvp=50)),
        _normalize(_raw("C", dvp=-10)),
    ]
    lists = compute_top_lists(stocks, n=2)
    ve = lists["volume_explosion"]
    # dvp=-10 filtered out (need >= 0). Top: B(50), A(20).
    assert [h.code for h in ve] == ["B", "A"]


def test_compute_depleted_supply_filter_positive_sort_asc():
    """depleted_supply = filter dvp >= 0, sort ASC — verbatim from source."""
    stocks = [
        _normalize(_raw("A", dvp=5)),
        _normalize(_raw("B", dvp=2)),
        _normalize(_raw("C", dvp=-10)),  # filtered out
    ]
    lists = compute_top_lists(stocks, n=2)
    ds = lists["depleted_supply"]
    assert [h.code for h in ds] == ["B", "A"]
    # C is filtered out
    assert all(h.code != "C" for h in ds)


def test_compute_top_lists_returns_4_categories():
    lists = compute_top_lists([_normalize(_raw("A"))], n=1)
    assert set(lists.keys()) == set(CATEGORIES)


# === dedup_tickers ===

def test_dedup_first_seen_order():
    """Ticker in 2 categories merged with categories list; order = first seen."""
    lists = {
        "price_increment": [HotTicker("A", 1, 5.0, 0.0, "price_increment", 1)],
        "price_decrement": [HotTicker("B", 1, -3.0, 0.0, "price_decrement", 1)],
        "volume_explosion": [
            HotTicker("A", 1, 5.0, 30.0, "volume_explosion", 1),  # dup
            HotTicker("C", 1, 1.0, 30.0, "volume_explosion", 2),
        ],
        "depleted_supply": [],
    }
    out = dedup_tickers(lists)
    assert [t for t, _ in out] == ["A", "B", "C"]
    a_cats = dict(out)["A"]
    assert "price_increment" in a_cats
    assert "volume_explosion" in a_cats


def test_dedup_empty_lists():
    out = dedup_tickers({c: [] for c in CATEGORIES})
    assert out == []


# === HotTicker dataclass ===

def test_hot_ticker_to_dict():
    h = HotTicker("VCB", 92500, 2.5, 15.0, "price_increment", 1)
    assert h.to_dict() == {
        "code": "VCB",
        "price": 92500,
        "day_change_percent": 2.5,
        "day_vol_percent": 15.0,
        "category": "price_increment",
        "rank": 1,
    }


# === fetch_stocks_overview ===

def test_fetch_stocks_overview_uses_injected_api():
    fake_api = MagicMock()
    fake_api.get_overview.return_value = {"stocks": [_raw("VCB")]}
    out = fetch_stocks_overview(api=fake_api)
    assert len(out) == 1
    assert out[0]["code"] == "VCB"


def test_fetch_stocks_overview_missing_stocks_key():
    fake_api = MagicMock()
    fake_api.get_overview.return_value = {}
    assert fetch_stocks_overview(api=fake_api) == []


def test_fetch_stocks_overview_non_dict_response():
    fake_api = MagicMock()
    fake_api.get_overview.return_value = None
    assert fetch_stocks_overview(api=fake_api) == []


# === fetch_top_hot_tickers integration ===

def test_fetch_top_hot_tickers_intersects_universe():
    """Stocks outside universe_set must be dropped before compute."""
    fake_api = MagicMock()
    fake_api.get_overview.return_value = {"stocks": [
        _raw("A", dcp=5),  # in universe
        _raw("X", dcp=10),  # outside universe — should be dropped
    ]}
    out = fetch_top_hot_tickers(n=2, universe_set={"A"}, api=fake_api)
    tickers = {t for t, _ in out}
    assert tickers == {"A"}
    assert "X" not in tickers


def test_fetch_top_hot_tickers_no_universe_no_intersect():
    """When universe_set is None, no intersect (all default-filtered stocks)."""
    fake_api = MagicMock()
    fake_api.get_overview.return_value = {"stocks": [
        _raw("A", dcp=5),
        _raw("B", dcp=-3),
    ]}
    out = fetch_top_hot_tickers(n=2, universe_set=None, api=fake_api)
    tickers = {t for t, _ in out}
    assert tickers == {"A", "B"}


def test_fetch_top_hot_tickers_returns_dedup_format():
    """Output is [(ticker, [categories_present]), ...] not list[HotTicker]."""
    fake_api = MagicMock()
    fake_api.get_overview.return_value = {"stocks": [_raw("A", dcp=5, dvp=20)]}
    out = fetch_top_hot_tickers(n=2, universe_set={"A"}, api=fake_api)
    assert isinstance(out, list)
    assert len(out) == 1
    ticker, cats = out[0]
    assert ticker == "A"
    # A is gainer (dcp=5) AND has dvp=20 — should appear in multiple categories.
    assert "price_increment" in cats
    assert "volume_explosion" in cats
