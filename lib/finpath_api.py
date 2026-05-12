"""Finpath API wrapper — public Bank endpoints + V5.1.3 foreign flow.

Verified 2026-05-08: https://api.finpath.vn returns 200 OK no auth.
Endpoints documented in spec section 4.4.

V5.1.3 (Plan G Task 2): 3 foreign flow methods backed by SQLite hybrid TTL
cache (`finpath_foreign_cache` table) — graceful fallback to stale payload
when upstream API errors and a stale entry exists; raise RuntimeError when
neither fresh nor stale data are available.
"""
from __future__ import annotations
import json
import logging
from datetime import datetime, timezone
from typing import Any, Optional
import requests


log = logging.getLogger(__name__)


class FinpathAPI:
    """Wrapper for 14 Bank-relevant Finpath endpoints with in-memory cache,
    plus 3 V5.1.3 foreign flow endpoints with SQLite hybrid TTL cache."""

    def __init__(
        self,
        base_url: str = "https://api.finpath.vn",
        timeout: int = 10,
        db: Any = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._cache: dict[str, Any] = {}  # in-memory cache for Bank endpoints
        self.db = db  # SQLite handle for V5.1.3 foreign flow cache (optional)

    def _get(self, path: str, params: dict[str, str] | None = None) -> Any:
        cache_key = f"{path}?{params}" if params else path
        if cache_key in self._cache:
            return self._cache[cache_key]
        url = f"{self.base_url}{path}"
        r = requests.get(url, params=params, timeout=self.timeout)
        r.raise_for_status()
        body = r.json()
        if "data" not in body:
            raise ValueError(f"Unexpected response shape from {path}: missing 'data'")
        self._cache[cache_key] = body["data"]
        return body["data"]

    # === Group A: BCTC ===

    def get_income_statement(self, ticker: str) -> dict[str, list]:
        return self._get(f"/api/stocks/incomes/{ticker}")

    def get_balance_sheet(self, ticker: str) -> dict[str, list]:
        return self._get(f"/api/stocks/balancesheets/{ticker}")

    def get_full_income(self, ticker: str) -> dict[str, list]:
        return self._get(f"/api/stocks/fullincomestatements/{ticker}")

    def get_full_balance_sheet(self, ticker: str) -> dict[str, list]:
        return self._get(f"/api/stocks/fullbalancesheets/{ticker}")

    def get_cashflow(self, ticker: str) -> dict[str, list]:
        return self._get(f"/api/stocks/fullcashflows/{ticker}")

    # === Group B: Bank-specific ratios ===

    def get_bank_ratios(self, ticker: str) -> dict[str, list]:
        """NIM, CASA, COF, NPL, LDR, P/E, P/B, ROE for one bank."""
        return self._get(f"/api/stocks/bankfinancialratios/{ticker}")

    def get_bank_ratios_batch(self, tickers: list[str]) -> list[dict]:
        """Multi-ticker batch."""
        return self._get(
            "/api/stocks/bankfinancialratios-eboard",
            params={"codes": ",".join(tickers)},
        )

    # === Group C: Specific items ===

    def get_net_interest_income(self, ticker: str) -> dict[str, list]:
        return self._get(f"/api/stocks/netinterestincomes/{ticker}")

    def get_deposit_credit(self, ticker: str) -> dict[str, list]:
        return self._get(f"/api/stocks/depositcredit/{ticker}")

    def get_bad_debt(self, ticker: str) -> dict[str, list]:
        return self._get(f"/api/stocks/baddebt/{ticker}")

    # === Group D: Ownership ===

    def get_shareholders(self, ticker: str) -> dict[str, list]:
        return self._get(f"/api/stocks/shareholderstructure/{ticker}")

    # === Group E: Events / news ===

    def get_events(self, ticker: str) -> list[dict]:
        return self._get(f"/api/events/{ticker}")

    def get_news(self, ticker: str) -> list[dict]:
        return self._get(f"/api/news/{ticker}")

    def get_company_profile(self, ticker: str) -> dict:
        return self._get(f"/api/stocks/companyprofile/{ticker}")

    # === Group F: Top movers (V5.1 — Subsystem A, Plan A Task 1) ===

    def get_overview(self) -> dict:
        """Full HOSE stock overview for top-movers compute.

        Returns: {"stocks": [{c, dcp, dvp, mc, a5v, p, st, ...}, ...]} (raw API shape).
        Uses inherited _get() caching + timeout. Public endpoint, no auth.
        """
        return self._get("/api/stocks/v2/overview")

    # === Group G: Foreign flow (V5.1.3 — Plan G Task 2) ===

    _VALID_FOREIGN_PERIODS = {"1D", "1W", "1M", "3M", "6M", "1Y"}

    def get_foreign_rooms(self) -> list[dict]:
        """All foreign flow snapshot. Cached 15 min in SQLite.

        Returns list of room dicts. Filter ste=='S' for stocks (caller's job).
        """
        return self._sqlite_cached_get(
            cache_key="rooms",
            endpoint="/v2/rooms",
            url_path="/api/stocks/v2/rooms",
            ttl=900,
            unwrap_key=("data", "rooms"),
            default=[],
        )

    def get_foreign_roomstatistics(self, ticker: str, period: str = "1D") -> dict:
        """Per-ticker NN flow stats for period. Cached 1h per (ticker, period)."""
        if period not in self._VALID_FOREIGN_PERIODS:
            raise ValueError(
                f"period '{period}' invalid. Must be one of "
                f"{sorted(self._VALID_FOREIGN_PERIODS)}"
            )
        return self._sqlite_cached_get(
            cache_key=f"roomstat:{ticker}:{period}",
            endpoint="/roomstatistics",
            url_path=f"/api/stocks/roomstatistics/{ticker}",
            params={"type": period},
            ttl=3600,
            unwrap_key=("data",),
            default={},
        )

    def get_foreign_roombars(self, ticker: str) -> list[dict]:
        """Time series daily NN flow bars. Cached 6h per ticker."""
        return self._sqlite_cached_get(
            cache_key=f"roombars:{ticker}",
            endpoint="/roombars",
            url_path=f"/api/stocks/roombars/{ticker}",
            ttl=21600,
            unwrap_key=("data", "bars"),
            default=[],
        )

    # === SQLite cache helpers ===

    def _sqlite_cached_get(
        self,
        cache_key: str,
        endpoint: str,
        url_path: str,
        ttl: int,
        unwrap_key: tuple,
        default: Any,
        params: Optional[dict] = None,
    ) -> Any:
        """Generic SQLite cache lookup + API fetch + stale-fallback graceful.

        Flow:
          1. If no db handle, fetch live (no cache layer).
          2. Lookup cache row by `cache_key`. If fresh (age < ttl) → return.
          3. Else fetch API. On success: persist + return.
          4. On API failure: return stale payload if any (warn). Else raise.
        """
        if not self.db:
            return self._fetch_api_unwrapped(
                url_path, unwrap_key, default, params=params
            )

        cached_fresh, stale = self._sqlite_cache_lookup(cache_key)
        if cached_fresh is not None:
            return self._unwrap(cached_fresh, unwrap_key, default)

        try:
            payload = self._fetch_api(url_path, params=params)
            self._sqlite_cache_set(cache_key, endpoint, payload, ttl)
            return self._unwrap(payload, unwrap_key, default)
        except Exception as e:
            if stale is not None:
                log.warning("API %s failed, using stale cache: %s", url_path, e)
                return self._unwrap(stale, unwrap_key, default)
            raise RuntimeError(
                f"Finpath API {url_path} failed + no cache: {e}"
            ) from e

    def _sqlite_cache_lookup(
        self, cache_key: str
    ) -> tuple[Optional[dict], Optional[dict]]:
        """Return (fresh_payload | None, stale_payload | None)."""
        cur = self.db.conn.execute(
            "SELECT payload, fetched_at, ttl_seconds FROM finpath_foreign_cache "
            "WHERE cache_key = ?",
            (cache_key,),
        )
        row = cur.fetchone()
        if not row:
            return None, None
        fetched_at = datetime.fromisoformat(row["fetched_at"])
        if fetched_at.tzinfo is None:
            fetched_at = fetched_at.replace(tzinfo=timezone.utc)
        age = (datetime.now(timezone.utc) - fetched_at).total_seconds()
        payload = json.loads(row["payload"])
        if age < row["ttl_seconds"]:
            return payload, None
        return None, payload

    def _sqlite_cache_set(
        self, cache_key: str, endpoint: str, payload: dict, ttl: int
    ) -> None:
        self.db.conn.execute(
            """
            INSERT INTO finpath_foreign_cache (cache_key, endpoint, payload, fetched_at, ttl_seconds)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(cache_key) DO UPDATE SET
                payload = excluded.payload,
                fetched_at = excluded.fetched_at,
                ttl_seconds = excluded.ttl_seconds
            """,
            (
                cache_key,
                endpoint,
                json.dumps(payload),
                datetime.now(timezone.utc).isoformat(),
                ttl,
            ),
        )
        self.db.conn.commit()

    def _fetch_api(self, path: str, params: Optional[dict] = None) -> dict:
        """HTTP GET with headers + timeout. Returns body JSON.

        `requests` is imported at module level so unittest.mock can patch
        `lib.finpath_api.requests.get`.
        """
        r = requests.get(
            f"{self.base_url}{path}",
            params=params,
            timeout=self.timeout,
            headers={
                "accept": "application/json",
                "client-type": "web",
                "origin": "https://finpath.vn",
                "user-agent": "Mozilla/5.0",
            },
        )
        r.raise_for_status()
        return r.json()

    def _fetch_api_unwrapped(
        self,
        path: str,
        unwrap_key: tuple,
        default: Any,
        params: Optional[dict] = None,
    ) -> Any:
        """No-cache fallback path (used when db handle absent)."""
        payload = self._fetch_api(path, params=params)
        return self._unwrap(payload, unwrap_key, default)

    @staticmethod
    def _unwrap(payload: dict, unwrap_key: tuple, default: Any) -> Any:
        """Navigate nested dict path safely (`('data', 'rooms')` etc.)."""
        current: Any = payload
        for key in unwrap_key:
            if not isinstance(current, dict):
                return default
            current = current.get(key, default)
        return current if current is not None else default
