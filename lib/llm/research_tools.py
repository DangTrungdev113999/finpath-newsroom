"""V5.1.9 research tools — pure dispatcher for Gemini + Grok Master free-style.

Each tool is a Python callable returning a dict result. Tools wrap existing
modules (FinpathAPI, KBLoader, PipelineDB) so we don't reimplement business
logic. LLM decides tool selection + call order — no mandated workflow.

Backings:
  - 5 Finpath wrappers (overview / income / balance / cashflow / bank_ratios)
  - kb_search: lib.kb_loader.KBLoader.search
  - read_recent_articles: PipelineDB.recent_generated_news
  - web_search: Tavily REST API (graceful no-op when API key absent)

Usage (Gemini SDK):
    tools = build_research_tools(db=db)
    config = types.GenerateContentConfig(
        tools=tools.callables,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            maximum_remote_calls=8,
        ),
    )

Usage (Grok manual loop):
    tools = build_research_tools(db=db)
    resp = client.chat.completions.create(
        model="grok-4.3",
        messages=messages,
        tools=tools.openai_schema,
    )
    for call in resp.choices[0].message.tool_calls:
        result = tools.dispatch[call.function.name](**json.loads(call.function.arguments))
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import yaml

from lib.finpath_api import FinpathAPI
from lib.kb_loader import KBLoader


DEFAULT_KB_ROOT = Path("kb/")
DEFAULT_SECRETS_PATH = Path("data/secrets.yaml")
TAVILY_BASE_URL = "https://api.tavily.com/search"
DEFAULT_TAVILY_TIMEOUT = 15  # seconds
MAX_KB_SNIPPET_CHARS = 400
MAX_WEB_RESULTS = 5


@dataclass
class ResearchTools:
    """Container exposing tools in two flavors so Gemini SDK + OpenAI SDK can both use them.

    - `callables`: list of Python functions for `google.genai` automatic function calling
      (SDK introspects type hints + docstring to build schema)
    - `openai_schema`: list of dicts in OpenAI function format for the openai/Grok manual loop
    - `dispatch`: name → callable map for the manual loop result execution
    """
    callables: list[Callable[..., dict]]
    openai_schema: list[dict[str, Any]] = field(default_factory=list)
    dispatch: dict[str, Callable[..., dict]] = field(default_factory=dict)


def _load_tavily_key(secrets_path: Path) -> str | None:
    """Read tavily.api_key from secrets.yaml. Returns None when absent/placeholder."""
    if not secrets_path.exists():
        return None
    try:
        raw = yaml.safe_load(secrets_path.read_text(encoding="utf-8")) or {}
    except Exception:
        return None
    section = raw.get("tavily")
    if not isinstance(section, dict):
        return None
    key = section.get("api_key")
    if not isinstance(key, str) or not key.strip():
        return None
    if any(token in key for token in ("REPLACE_", "your-", "fixme")):
        return None
    return key


def build_research_tools(
    *,
    db: Any,
    kb_root: Path = DEFAULT_KB_ROOT,
    secrets_path: Path = DEFAULT_SECRETS_PATH,
    tavily_api_key: str | None = None,
) -> ResearchTools:
    """Construct 8 research tool callables sharing FinpathAPI + KBLoader + db handles.

    `tavily_api_key` override wins over `secrets.tavily.api_key`. When neither is
    available, the `web_search` tool is still callable but returns
    {"ok": False, "error": "tavily_disabled"} so the LLM sees the capability is
    off without raising.
    """
    api = FinpathAPI(db=db)
    kb = KBLoader(kb_root)
    web_key = tavily_api_key or _load_tavily_key(secrets_path)

    def finpath_overview(ticker: str | None = None) -> dict:
        """Get today's market snapshot for ONE ticker (or top-50 by market cap if no ticker).
        Use to grab today's price + market cap + volume before quoting.
        Returns trimmed payload (one ticker row OR top 50) to keep tool context small.
        `ticker`: optional 3-letter ticker. When set, returns just that stock's row.
        """
        try:
            data = api.get_overview()
            stocks = data.get("stocks", []) if isinstance(data, dict) else []
            if ticker:
                wanted = ticker.strip().upper()
                hit = next((s for s in stocks if (s.get("c") or "").upper() == wanted), None)
                trimmed = [hit] if hit else []
            else:
                # Top 50 by market cap — enough for LLM to scan competitors / peer set
                trimmed = sorted(stocks, key=lambda s: s.get("mc") or 0, reverse=True)[:50]
            return {
                "ok": True,
                "source": f"Finpath_API/overview" + (f"/{ticker}" if ticker else "/top50"),
                "data": {"stocks": trimmed, "total_market_count": len(stocks)},
            }
        except Exception as exc:  # noqa: BLE001 — network/parse errors all surface the same
            return {"ok": False, "error": str(exc), "source": "Finpath_API/overview"}

    def finpath_income_statement(ticker: str) -> dict:
        """Quarterly income statement (P&L) for a Vietnamese listed ticker.
        Use to get revenue, gross profit, net profit before/after tax per quarter.
        `ticker`: 3-letter ticker like 'VCB' / 'VHM' / 'FPT'.
        """
        try:
            data = api.get_income_statement(ticker)
            return {"ok": True, "source": f"Finpath_API/income_statement/{ticker}", "data": data}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": str(exc), "source": f"Finpath_API/income_statement/{ticker}"}

    def finpath_balance_sheet(ticker: str) -> dict:
        """Quarterly balance sheet for a ticker. Use for total assets, equity, debt, cash position.
        `ticker`: 3-letter ticker.
        """
        try:
            data = api.get_balance_sheet(ticker)
            return {"ok": True, "source": f"Finpath_API/balance_sheet/{ticker}", "data": data}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": str(exc), "source": f"Finpath_API/balance_sheet/{ticker}"}

    def finpath_cashflow(ticker: str) -> dict:
        """Quarterly cashflow statement (CFO/CFI/CFF) for a ticker. Use to verify free cashflow
        or detect financing-heavy cycles.
        `ticker`: 3-letter ticker.
        """
        try:
            data = api.get_cashflow(ticker)
            return {"ok": True, "source": f"Finpath_API/cashflow/{ticker}", "data": data}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": str(exc), "source": f"Finpath_API/cashflow/{ticker}"}

    def finpath_bank_ratios(ticker: str) -> dict:
        """Bank-only ratios (NIM, CASA, COF, NPL, LDR, P/E, P/B, ROE) per quarter.
        Use ONLY for bank tickers (VCB/CTG/BID/TCB/MBB/ACB/VPB/HDB/STB/SHB/...).
        Returns 4xx-like error for non-bank tickers.
        `ticker`: 3-letter bank ticker.
        """
        try:
            data = api.get_bank_ratios(ticker)
            return {"ok": True, "source": f"Finpath_API/bank_ratios/{ticker}", "data": data}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": str(exc), "source": f"Finpath_API/bank_ratios/{ticker}"}

    def kb_search(query: str, sector: str | None = None) -> dict:
        """Search the Finpath markdown knowledge base for relevant context files.
        Splits `query` on whitespace into keywords; returns top 3 hits with file path,
        title, category, and a short snippet.
        `query`: 2-5 keywords (Vietnamese or English).
        `sector`: optional category filter (e.g. 'bank', 'bds', 'ck'). Default: search all.
        """
        keywords = [w for w in query.split() if w.strip()]
        try:
            hits = kb.search(keywords, category=sector)[:3]
            return {
                "ok": True,
                "source": f"KB/search?q={query}",
                "data": [
                    {
                        "path": h["path"],
                        "title": h["title"],
                        "category": h["category"],
                        "snippet": (h["snippet"] or "")[:MAX_KB_SNIPPET_CHARS],
                    }
                    for h in hits
                ],
            }
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": str(exc), "source": f"KB/search?q={query}"}

    def read_recent_articles(ticker: str, limit: int = 3) -> dict:
        """Read the most recent published articles for a ticker.
        Use for variety guard: avoid repeating the same angle as the last N articles.
        `ticker`: 3-letter ticker.
        `limit`: number of recent articles to return (default 3, max 5).
        """
        n = max(1, min(int(limit), 5))
        try:
            rows = db.recent_generated_news(ticker, limit=n)
            return {
                "ok": True,
                "source": f"DB/recent_articles?ticker={ticker}&limit={n}",
                "data": [
                    {
                        "title": r.get("title"),
                        "variety_guard_angle": r.get("variety_guard_angle"),
                        "insight_final": r.get("insight_final"),
                        "published_at": r.get("published_at"),
                    }
                    for r in rows
                ],
            }
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": str(exc), "source": f"DB/recent_articles?ticker={ticker}"}

    def web_search(query: str, max_results: int = 5) -> dict:
        """Web search via Tavily for breaking news / recent context that's not in the KB.
        Returns title + url + short snippet per hit. Use for fresh quarterly numbers,
        analyst targets, regulatory news. Gracefully degrades when Tavily API key absent.
        `query`: search query in Vietnamese or English.
        `max_results`: 1-5 (default 5).
        """
        if not web_key:
            return {
                "ok": False,
                "error": "tavily_disabled",
                "source": f"WebSearch: {query!r} (no Tavily key in secrets.yaml)",
            }
        n = max(1, min(int(max_results), MAX_WEB_RESULTS))
        payload = json.dumps({
            "api_key": web_key,
            "query": query,
            "max_results": n,
            "search_depth": "basic",
            "include_raw_content": False,
        }).encode("utf-8")
        req = urllib.request.Request(
            TAVILY_BASE_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=DEFAULT_TAVILY_TIMEOUT) as resp:
                body = json.loads(resp.read())
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": str(exc), "source": f"WebSearch: {query!r}"}
        results = body.get("results", []) if isinstance(body, dict) else []
        return {
            "ok": True,
            "source": f"WebSearch: {query!r}",
            "data": [
                {
                    "title": r.get("title"),
                    "url": r.get("url"),
                    "snippet": (r.get("content") or "")[:300],
                }
                for r in results[:n]
            ],
        }

    callables: list[Callable[..., dict]] = [
        finpath_overview,
        finpath_income_statement,
        finpath_balance_sheet,
        finpath_cashflow,
        finpath_bank_ratios,
        kb_search,
        read_recent_articles,
        web_search,
    ]
    dispatch = {fn.__name__: fn for fn in callables}

    # OpenAI tool schema (Grok manual loop). Hand-rolled because we know the
    # signatures — keeps params descriptions in sync with Gemini introspection.
    openai_schema: list[dict[str, Any]] = [
        {
            "type": "function",
            "function": {
                "name": "finpath_overview",
                "description": "Today's market snapshot for ONE ticker (or top-50 if no ticker). Returns trimmed payload.",
                "parameters": {
                    "type": "object",
                    "properties": {"ticker": {"type": "string", "description": "Optional 3-letter ticker"}},
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "finpath_income_statement",
                "description": "Quarterly P&L for a ticker — revenue, gross profit, net profit per quarter.",
                "parameters": {
                    "type": "object",
                    "properties": {"ticker": {"type": "string", "description": "3-letter ticker like VCB / VHM"}},
                    "required": ["ticker"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "finpath_balance_sheet",
                "description": "Quarterly balance sheet for a ticker — assets, equity, debt, cash.",
                "parameters": {
                    "type": "object",
                    "properties": {"ticker": {"type": "string"}},
                    "required": ["ticker"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "finpath_cashflow",
                "description": "Quarterly cashflow (CFO/CFI/CFF) for a ticker.",
                "parameters": {
                    "type": "object",
                    "properties": {"ticker": {"type": "string"}},
                    "required": ["ticker"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "finpath_bank_ratios",
                "description": "Bank-only ratios (NIM, CASA, COF, NPL, LDR, P/E, P/B, ROE). ONLY for bank tickers.",
                "parameters": {
                    "type": "object",
                    "properties": {"ticker": {"type": "string", "description": "3-letter bank ticker"}},
                    "required": ["ticker"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "kb_search",
                "description": "Search the markdown knowledge base. Returns top 3 hits with snippet.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "2-5 keywords"},
                        "sector": {"type": "string", "description": "Optional category filter"},
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_recent_articles",
                "description": "Read the N most recent published articles for a ticker (variety guard).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string"},
                        "limit": {"type": "integer", "description": "1-5, default 3"},
                    },
                    "required": ["ticker"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Web search via Tavily for breaking news. Returns up to 5 results with title/url/snippet.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "max_results": {"type": "integer", "description": "1-5, default 5"},
                    },
                    "required": ["query"],
                },
            },
        },
    ]

    return ResearchTools(callables=callables, openai_schema=openai_schema, dispatch=dispatch)
