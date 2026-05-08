"""Finpath API wrapper — public Bank endpoints.

Verified 2026-05-08: https://api.finpath.vn returns 200 OK no auth.
Endpoints documented in spec section 4.4.
"""
from __future__ import annotations
from typing import Any
import requests


class FinpathAPI:
    """Wrapper for 14 Bank-relevant Finpath endpoints with in-memory cache."""

    def __init__(self, base_url: str = "https://api.finpath.vn", timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._cache: dict[str, Any] = {}

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
