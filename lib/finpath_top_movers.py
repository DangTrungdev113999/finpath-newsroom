"""V5.1 Subsystem A — Top movers compute for /tin-hot N command.

Pipeline:
  1. fetch_stocks_overview(api) — wrapper around FinpathAPI.get_overview
  2. normalize(raw_stock_list) → list[NormalizedStock] (extract fields)
  3. apply_default_filters(stocks) — exclude low liquidity / zero price /
     non-S secType / take top 100 by marketcap
  4. compute_top_lists(filtered, n) → 4 categories of length n each:
       - tang (gainers, sorted by change_pct desc)
       - giam (losers, sorted by change_pct asc)
       - bung_no (volume spike, sorted by volume_ratio desc — vol/avg_5d_vol)
       - can_cung (low supply, sorted by some metric — see spec)
  5. dedup(lists) — keep first-seen order across all 4 lists
  6. intersect_universe(tickers, universe_set) — filter to universe membership
  7. fetch_top_hot_tickers(api, n, universe_set) — top-level helper combining
     all steps. Returns list[HotTicker] with category origin tagged.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass
class HotTicker:
    ticker: str
    category: str  # "tang" | "giam" | "bung_no" | "can_cung"
    rank: int  # 1-based within category
    price: float
    change_pct: float
    volume: int
    volume_ratio: float
    marketcap: int

    def to_dict(self) -> dict:
        return {
            "ticker": self.ticker,
            "category": self.category,
            "rank": self.rank,
            "price": self.price,
            "change_pct": self.change_pct,
            "volume": self.volume,
            "volume_ratio": self.volume_ratio,
            "marketcap": self.marketcap,
        }


def normalize(raw: list[dict]) -> list[dict]:
    """Extract relevant fields from raw API shape."""
    out = []
    for s in raw:
        try:
            out.append({
                "ticker": s["c"],
                "price": s.get("p", 0),
                "change_pct": s.get("dcp", 0),
                "volume": s.get("dv", 0),
                "avg_5d_volume": s.get("a5v", 1),
                "marketcap": s.get("mc", 0),
                "sec_type": s.get("st", ""),
                "volume_ratio": (s.get("dv", 0) / s["a5v"]) if s.get("a5v") else 0,
            })
        except (KeyError, ZeroDivisionError):
            continue
    return out


def apply_default_filters(stocks: list[dict]) -> list[dict]:
    """Exclude low liquidity / non-S secType / zero price / take top 100 by mc."""
    filtered = [
        s for s in stocks
        if s["price"] > 0
        and s["sec_type"] == "S"
        and s["volume"] > 0
        and s["avg_5d_volume"] > 0
    ]
    filtered.sort(key=lambda s: s["marketcap"], reverse=True)
    return filtered[:100]


def compute_top_lists(filtered: list[dict], n: int) -> dict[str, list[dict]]:
    """Compute 4 top lists. n ∈ [1, 25] (validation lift)."""
    if not (1 <= n <= 25):
        raise ValueError(f"n={n} out of range [1, 25]")
    tang = sorted(filtered, key=lambda s: s["change_pct"], reverse=True)[:n]
    giam = sorted(filtered, key=lambda s: s["change_pct"])[:n]
    bung_no = sorted(filtered, key=lambda s: s["volume_ratio"], reverse=True)[:n]
    # can_cung: low supply = high price * low volume relative to history.
    # Simpler heuristic: lowest volume_ratio among gainers (price up, vol thin).
    gainers = [s for s in filtered if s["change_pct"] > 0]
    can_cung = sorted(gainers, key=lambda s: s["volume_ratio"])[:n]
    return {"tang": tang, "giam": giam, "bung_no": bung_no, "can_cung": can_cung}


def dedup(category_lists: dict[str, list[dict]]) -> list[HotTicker]:
    """Flatten 4 lists into a single deduped list (first-seen wins)."""
    seen: set[str] = set()
    result: list[HotTicker] = []
    for category, stocks in category_lists.items():
        for rank, s in enumerate(stocks, 1):
            t = s["ticker"]
            if t in seen:
                continue
            seen.add(t)
            result.append(HotTicker(
                ticker=t,
                category=category,
                rank=rank,
                price=s["price"],
                change_pct=s["change_pct"],
                volume=s["volume"],
                volume_ratio=s["volume_ratio"],
                marketcap=s["marketcap"],
            ))
    return result


def intersect_universe(hot_tickers: list[HotTicker], universe_set: set[str]) -> list[HotTicker]:
    """Keep only tickers in V5.1.3 Finpath universe (~139 mã)."""
    return [h for h in hot_tickers if h.ticker in universe_set]


class _APILike(Protocol):
    def get_overview(self) -> dict: ...


def fetch_stocks_overview(api: Optional[_APILike] = None) -> list[dict]:
    """Wrapper: fetch raw stocks list from Finpath API."""
    if api is None:
        from lib.finpath_api import FinpathAPI
        api = FinpathAPI()
    response = api.get_overview()
    return response.get("stocks", [])


def fetch_top_hot_tickers(
    n: int = 4,
    universe_set: Optional[set[str]] = None,
    api: Optional[_APILike] = None,
) -> list[HotTicker]:
    """Top-level: fetch + normalize + filter + compute + dedup + intersect.

    Args:
        n: Number per category (1-25). After dedup the total returned may be
           ≤ 4n.
        universe_set: V5.1.3 Finpath cache tickers (~139). If None, no intersect
           — for testing.

    Returns:
        list[HotTicker] deduped, intersected to universe (if provided).
    """
    raw = fetch_stocks_overview(api)
    normalized = normalize(raw)
    filtered = apply_default_filters(normalized)
    categories = compute_top_lists(filtered, n)
    deduped = dedup(categories)
    if universe_set is not None:
        return intersect_universe(deduped, universe_set)
    return deduped
