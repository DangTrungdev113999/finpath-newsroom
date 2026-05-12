"""V5.1 Subsystem A — Top movers compute for /tin-hot N command.

Compute 4 categories (price_increment / price_decrement / volume_explosion /
depleted_supply) mirroring finpath-web stockDataUtils.ts.

Source-of-truth references (Plan A spec lines 340+):
  /Users/trungdt/Desktop/finpath-web/src/Modules/stock-real-time/utils/stockDataUtils.ts
  /Users/trungdt/Desktop/finpath-web/src/Modules/top-stocks/constants/index.ts

Pipeline:
  1. fetch_stocks_overview(api) → list[normalized dict] via FinpathAPI.get_overview
  2. apply_default_filters(stocks) → top 100 marketCap + avgDay5Value ≥ 10 tỷ
     + price > 0 + secType=='S'
  3. compute_top_lists(filtered, n) → 4 categories of up to n HotTicker each
  4. dedup_tickers(lists) → [(ticker, categories_present)] first-seen order

V1.2 PATCH (Spec F V5.1.3 integration): orchestrator (`tin-hot.md` command)
intersects with `FinpathSectors.get_all_cached_tickers()` (~139 mã) BEFORE
calling `compute_top_lists`. This module accepts `intersect_universe`
helper for that step.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Optional


LIQUIDITY_THRESHOLD_BILLION = 10  # 10 tỷ VND (DEFAULT_FILTERS.liquidity)
MARKET_CAP_TOP = 100  # DEFAULT_FILTERS.marketCap

# Field name mapping API raw → normalized (per convertDataOverViewStock)
FIELD_MAP = {
    "c": "code", "dcp": "dayChangePercent", "dc": "dayChange",
    "dvp": "dayVolPercent", "dv": "dayVolume",
    "mc": "marketCap", "a5v": "avgDay5Value",
    "p": "price", "st": "secType",
}


CATEGORIES = (
    "price_increment",
    "price_decrement",
    "volume_explosion",
    "depleted_supply",
)


@dataclass
class HotTicker:
    """Top-mover ticker with category tag + rank within category."""
    code: str
    price: float
    day_change_percent: float
    day_vol_percent: float
    category: str  # one of CATEGORIES
    rank: int  # 1 = top of category

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _normalize(raw: dict) -> dict:
    """Map API field shortcuts → normalized names per FIELD_MAP."""
    return {FIELD_MAP.get(k, k): v for k, v in raw.items()}


def fetch_stocks_overview(api=None) -> list[dict]:
    """Use FinpathAPI.get_overview() then normalize fields.

    Reuses existing caching + timeout + error handling. Defensive:
    missing 'stocks' key → [].

    Args:
        api: Optional injected FinpathAPI instance for testing. Defaults
            to new FinpathAPI().

    Returns: list of normalized stock dicts.
    """
    if api is None:
        from lib.finpath_api import FinpathAPI
        api = FinpathAPI()
    raw = api.get_overview()
    raw_stocks = raw.get("stocks", []) if isinstance(raw, dict) else []
    return [_normalize(s) for s in raw_stocks]


def apply_default_filters(stocks: list[dict]) -> list[dict]:
    """Top 100 marketCap + avgDay5Value ≥ 10 tỷ + price > 0 + secType S.

    Mirrors filter-helpers.ts:applyFilters with DEFAULT_FILTERS.
    """
    sorted_by_mc = sorted(stocks, key=lambda s: -(s.get("marketCap") or 0))
    top_n = sorted_by_mc[:MARKET_CAP_TOP]
    threshold = LIQUIDITY_THRESHOLD_BILLION * 1_000_000_000
    return [
        s for s in top_n
        if s.get("avgDay5Value", 0) >= threshold
        and s.get("price", 0) > 0
        and s.get("secType") == "S"
    ]


def intersect_universe(stocks: list[dict], universe_set: set[str]) -> list[dict]:
    """Keep only stocks whose code is in the V5.1.3 Finpath universe (~139)."""
    return [s for s in stocks if s.get("code") in universe_set]


def compute_top_lists(filtered: list[dict], n: int) -> dict[str, list[HotTicker]]:
    """Compute 4 categories, take top N from each.

    Mirrors stockDataUtils.ts:
    - topPriceIncrement: dayChangePercent >= 0, sort desc
    - topPriceDecrement: dayChangePercent <= 0, sort asc
    - topVolumeExplosion: dayVolPercent >= 0, sort desc
    - topDepletedSupply: dayVolPercent >= 0, sort asc

    Note: depleted_supply uses dvp >= 0 (not <= 0) — verbatim from source.

    Args:
        filtered: stocks post default-filter (and post intersect universe
            per V1.2 PATCH if caller wants universe constraint)
        n: top N per category (1-10)

    Returns:
        {"price_increment": [HotTicker, ...], "price_decrement": [...], ...}

    Raises:
        ValueError if n out of [1, 10] range.
    """
    if n < 1 or n > 10:
        raise ValueError(f"N must be 1-10, got {n}")

    pi_raw = sorted(
        [s for s in filtered if s.get("dayChangePercent", 0) >= 0],
        key=lambda s: -s["dayChangePercent"],
    )[:n]
    pd_raw = sorted(
        [s for s in filtered if s.get("dayChangePercent", 0) <= 0],
        key=lambda s: s["dayChangePercent"],
    )[:n]
    ve_raw = sorted(
        [s for s in filtered if s.get("dayVolPercent", 0) >= 0],
        key=lambda s: -s["dayVolPercent"],
    )[:n]
    ds_raw = sorted(
        [s for s in filtered if s.get("dayVolPercent", 0) >= 0],
        key=lambda s: s["dayVolPercent"],
    )[:n]

    def _wrap(items: list[dict], cat: str) -> list[HotTicker]:
        return [
            HotTicker(
                code=s["code"],
                price=s.get("price", 0),
                day_change_percent=s.get("dayChangePercent", 0),
                day_vol_percent=s.get("dayVolPercent", 0),
                category=cat,
                rank=i + 1,
            )
            for i, s in enumerate(items)
        ]

    return {
        "price_increment": _wrap(pi_raw, "price_increment"),
        "price_decrement": _wrap(pd_raw, "price_decrement"),
        "volume_explosion": _wrap(ve_raw, "volume_explosion"),
        "depleted_supply": _wrap(ds_raw, "depleted_supply"),
    }


def dedup_tickers(
    lists: dict[str, list[HotTicker]],
) -> list[tuple[str, list[str]]]:
    """Flatten + dedup. Returns [(ticker, [categories_present]), ...] in
    first-seen order.

    Order convention: price_increment first, then decrement, volume_explosion,
    depleted_supply. Duplicates merged with categories list (a ticker that
    appears in 2 categories is reported once with both category names).
    """
    seen: dict[str, list[str]] = {}
    order: list[str] = []
    for cat in CATEGORIES:
        for ticker in lists.get(cat, []):
            if ticker.code not in seen:
                seen[ticker.code] = []
                order.append(ticker.code)
            seen[ticker.code].append(cat)
    return [(t, seen[t]) for t in order]


def fetch_top_hot_tickers(
    n: int = 4,
    universe_set: Optional[set[str]] = None,
    api=None,
) -> list[tuple[str, list[str]]]:
    """Top-level helper: fetch → filter → (intersect) → compute → dedup.

    V1.2 PATCH: when universe_set is provided (canonical use), intersect
    happens AFTER default filters but BEFORE compute_top_lists, so the
    top-N candidates are drawn from universe-only stocks.

    Args:
        n: N per category (1-10). After dedup the total returned may be ≤ 4n.
        universe_set: V5.1.3 Finpath cache tickers (~139). If None, no
            intersect — for testing or full-HOSE use.
        api: Optional injected FinpathAPI instance for testing.

    Returns:
        list[(ticker, [categories_present])] deduped, first-seen order.
    """
    stocks = fetch_stocks_overview(api)
    filtered = apply_default_filters(stocks)
    if universe_set is not None:
        filtered = intersect_universe(filtered, universe_set)
    categories = compute_top_lists(filtered, n)
    return dedup_tickers(categories)
