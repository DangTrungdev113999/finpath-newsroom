"""Market Snapshot — Step 1.5 of V5.0 pipeline.

Soft fetch: failure → None, never raises. Brief proceeds without
ticker_market_data when this returns None. V5 Contrarian degrades to
prose-only guidance in that case.

Investigated 2026-05-12: Finpath API has NO real-time quote endpoint.
Probed routes (all return E_ROUTE_NOT_FOUND):
  - /api/stocks/quote/{ticker}
  - /api/stocks/quotes/{ticker}
  - /api/stocks/price/{ticker}
  - /api/stocks/prices/{ticker}
  - /api/stocks/price-history/{ticker}
  - /api/stocks/marketprice/{ticker}
Only /api/stocks/companyprofile/{ticker} returns 200 — but exposes
founding date, charter capital, listing info (NOT real-time price).

Consequence: FinpathAPI has no get_quote() method today. This module's
hasattr(api, "get_quote") check returns False and fetch_market_snapshot
always returns None — soft degrade by design. When a quote endpoint
ships, add get_quote to FinpathAPI and this module starts returning
real snapshots without further changes here.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any

from lib.finpath_api import FinpathAPI


@dataclass
class MarketSnapshot:
    price_today: float
    pct_change_today: float
    volume_ratio_3d: float
    fetched_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def fetch_market_snapshot(ticker: str) -> MarketSnapshot | None:
    """Fetch real-time quote via Finpath API. Returns None on any failure.

    Used in pipeline Step 1.5 to populate `brief.ticker_market_data` so Master
    can do mood-aware opening (acknowledge market red/green day in tone)
    without forcing stance follow.
    """
    try:
        api = FinpathAPI()
        # get_quote MAY not be implemented yet — defensive try
        if not hasattr(api, "get_quote"):
            return None
        raw = api.get_quote(ticker)
        if not isinstance(raw, dict) or "price" not in raw:
            return None
        return MarketSnapshot(
            price_today=float(raw["price"]),
            pct_change_today=float(raw.get("pct_change", 0.0)),
            volume_ratio_3d=float(raw.get("volume_ratio_3d", 1.0)),
            fetched_at=datetime.now(timezone.utc).isoformat(),
        )
    except (ConnectionError, KeyError, ValueError, TypeError):
        return None
    except Exception:
        # Catch-all defensive — Step 1.5 NEVER blocks pipeline
        return None
