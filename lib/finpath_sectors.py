"""Finpath sectors API client with SQLite cache (TTL 365 days).

User feedback 2026-05-12: "data này 1 năm mới thay đổi 1 lần".
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Optional, TypedDict
import logging
import requests

from lib.pipeline_db import PipelineDB

log = logging.getLogger(__name__)

CACHE_TTL_DAYS = 365
API_URL = "https://api.finpath.vn/api/stocks/v2/sectors"
API_TIMEOUT = 10
API_HEADERS = {
    "accept": "application/json",
    "client-type": "web",
    "origin": "https://finpath.vn",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
}


class SectorInfo(TypedDict):
    sector_code: str
    sector_name: str
    sector_parent: str
    exchange: str


class FinpathSectors:
    """Sector detection client for V5.1.3 universe expansion."""

    def __init__(self, db: PipelineDB):
        self.db = db

    def get_ticker_sector(
        self, ticker: str, allow_refresh: bool = True
    ) -> Optional[SectorInfo]:
        """Return ticker's sector info, or None if not in Finpath.

        Flow:
        1. Check cache row exists + fresh (< TTL).
        2. If cache hit + fresh → return.
        3. If cache miss + allow_refresh → refresh + retry once.
        4. If API down + cache has stale row → return stale (graceful).
        5. If API down + no row → None.
        """
        row = self._cache_lookup(ticker)
        if row and self._is_fresh(row["fetched_at"]):
            return self._row_to_info(row)

        if allow_refresh:
            try:
                self.refresh_cache()
            except Exception as e:
                log.warning(f"Finpath API refresh failed: {e}")
                if row:
                    log.warning(f"Returning stale cache for {ticker}")
                    return self._row_to_info(row)
                return None
            row = self._cache_lookup(ticker)
            if row:
                return self._row_to_info(row)

        return None

    def refresh_cache(self) -> int:
        """Fetch API + repopulate cache. Skip wrapper sectors (s=[]).

        Returns # tickers cached.
        """
        response = requests.get(
            API_URL, headers=API_HEADERS, timeout=API_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()["data"]["sectors"]

        now = datetime.now(timezone.utc).isoformat()
        rows = []
        for sector in data:
            stocks = sector.get("s") or []
            if not stocks:
                continue
            for stock in stocks:
                rows.append({
                    "ticker": stock["c"],
                    "sector_code": sector["k"],
                    "sector_name": sector["n"],
                    "sector_parent": sector.get("pn") or "",
                    "exchange": stock.get("e", ""),
                    "fetched_at": now,
                    "pe": stock.get("pe"),
                    "pb": stock.get("pb"),
                    "eps": stock.get("eps"),
                    "roa": stock.get("roa"),
                    "roe": stock.get("roe"),
                    "mc": stock.get("mc"),
                })

        self.db.conn.executemany("""
            INSERT INTO finpath_sectors_cache
                (ticker, sector_code, sector_name, sector_parent, exchange, fetched_at, pe, pb, eps, roa, roe, mc)
            VALUES
                (:ticker, :sector_code, :sector_name, :sector_parent, :exchange, :fetched_at, :pe, :pb, :eps, :roa, :roe, :mc)
            ON CONFLICT(ticker) DO UPDATE SET
                sector_code = excluded.sector_code,
                sector_name = excluded.sector_name,
                sector_parent = excluded.sector_parent,
                exchange = excluded.exchange,
                fetched_at = excluded.fetched_at,
                pe = excluded.pe, pb = excluded.pb, eps = excluded.eps,
                roa = excluded.roa, roe = excluded.roe, mc = excluded.mc
        """, rows)
        self.db.conn.commit()
        return len(rows)

    def get_all_cached_tickers(self) -> list[str]:
        """Return all ticker symbols currently in cache. Used by /tin-hot intersect."""
        cur = self.db.conn.execute("SELECT ticker FROM finpath_sectors_cache")
        return [row["ticker"] for row in cur.fetchall()]

    def _is_fresh(self, fetched_at_str: str) -> bool:
        fetched_at = datetime.fromisoformat(fetched_at_str)
        if fetched_at.tzinfo is None:
            fetched_at = fetched_at.replace(tzinfo=timezone.utc)
        age = datetime.now(timezone.utc) - fetched_at
        return age < timedelta(days=CACHE_TTL_DAYS)

    def _cache_lookup(self, ticker: str) -> Optional[dict]:
        cur = self.db.conn.execute(
            "SELECT * FROM finpath_sectors_cache WHERE ticker = ?", (ticker,)
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def _row_to_info(self, row: dict) -> SectorInfo:
        return {
            "sector_code": row["sector_code"],
            "sector_name": row["sector_name"],
            "sector_parent": row["sector_parent"] or "",
            "exchange": row["exchange"] or "",
        }
