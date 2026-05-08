# Phase 2 — Data Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Steps use checkbox `- [ ]`.

**Goal:** Build the Python data infrastructure that pipeline + agents will consume — SQLite ops, Finpath API wrapper, Notion KB ingest+loader, manual YAML stubs.

**Architecture:** `uv`-managed Python 3.13+ venv. `lib/` package with focused modules: `pipeline_db.py` (SQLite), `finpath_api.py` (typed HTTP wrapper with in-memory cache), `notion_fetch.py` (MCP helper), `kb_ingest.py` (one-time Notion → markdown), `kb_loader.py` (runtime grep). Tests via `pytest`. KB content lives in `kb/bank/` as markdown with YAML frontmatter (notion_page_id, source_url, last_synced).

**Tech Stack:** Python 3.13+, uv, requests, pyyaml, pytest, sqlite3 (stdlib).

**Spec reference:** `docs/superpowers/specs/2026-05-08-newsroom-cli-migration-design.md` Section 4 (data layer), Section 8 Phase 2.

**Project instructions:** `CLAUDE.md` data sourcing rule (Finpath API + YAML + KB local).

**Project root:** `/Users/trungdt/Desktop/Stream Intelligent/`

---

## File Structure

### Created
```
pyproject.toml                          # uv project + deps
.python-version                         # 3.13
data/pipeline.schema.sql                # SQLite DDL
lib/__init__.py
lib/pipeline_db.py                      # SQLite ops (insert/update/query crawl_log + generated_news)
lib/finpath_api.py                      # 14 Bank endpoints, typed, cached
lib/notion_fetch.py                     # MCP helper — page traversal
lib/kb_ingest.py                        # bootstrap CLI: Notion → kb/bank/<cat>/<slug>.md
lib/kb_loader.py                        # runtime grep + load
data/manual/targets.yaml                # Targets vs Actual (3-5 row stub)
data/manual/credit_room.yaml            # NHNN allocation (3-5 row stub)
data/manual/nhnn_circulars.yaml         # thông tư stub
kb/bank/                                # populated by kb_ingest run (Step ?)
tests/__init__.py
tests/test_pipeline_db.py
tests/test_finpath_api.py
tests/test_kb_loader.py
```

### Modified
```
.gitignore                              # add .venv/, kb/bank/.last_synced/
```

---

## Tasks

### Task 1: Init Python project with uv

**Files:**
- Create: `pyproject.toml`, `.python-version`
- Modify: `.gitignore`

- [ ] **Step 1: Init pyproject + lock python version**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && echo "3.13" > .python-version && uv init --no-readme --no-workspace --no-pin-python --bare
```

- [ ] **Step 2: Write `pyproject.toml`**

Replace generated content with:
```toml
[project]
name = "finpath-newsroom"
version = "0.1.0"
description = "Finpath Newsroom V3.6 — Claude Code CLI migration"
requires-python = ">=3.13"
dependencies = [
    "requests>=2.32",
    "pyyaml>=6.0",
    "python-frontmatter>=1.1",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-mock>=3.12",
    "responses>=0.25",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

- [ ] **Step 3: Create venv + install deps**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv sync
```

Expected: `.venv/` created, deps installed. `.venv/bin/python` resolves.

- [ ] **Step 4: Update `.gitignore`**

Append to `/Users/trungdt/Desktop/Stream Intelligent/.gitignore`:
```
# uv
.venv/
uv.lock

# KB sync metadata (gitignore — KB markdown content IS tracked)
kb/.last_synced/
```

- [ ] **Step 5: Smoke test**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "import requests, yaml, frontmatter; print('OK')"
```

Expected: `OK`.

- [ ] **Step 6: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add pyproject.toml .python-version .gitignore && git commit -m "chore(py): init uv project with requests + pyyaml + frontmatter + pytest"
```

---

### Task 2: SQLite schema + pipeline_db (TDD)

**Files:**
- Create: `data/pipeline.schema.sql`, `lib/__init__.py`, `lib/pipeline_db.py`, `tests/__init__.py`, `tests/test_pipeline_db.py`

- [ ] **Step 1: Write `data/pipeline.schema.sql`**

```sql
-- Finpath Newsroom Pipeline State Schema
-- Version: V3.6
-- Tables: crawl_log + generated_news

CREATE TABLE IF NOT EXISTS crawl_log (
  row_id              TEXT PRIMARY KEY,
  funnel_batch_id     TEXT NOT NULL,
  ticker              TEXT NOT NULL,
  -- Crawler fields
  source_name         TEXT NOT NULL,
  source_url          TEXT NOT NULL,
  title               TEXT NOT NULL,
  raw_content         TEXT,
  published_time      TEXT,
  crawled_at          TEXT NOT NULL,
  -- Editor V1 fields
  detected_tickers    TEXT,
  primary_ticker      TEXT,
  sector              TEXT,
  editor_v1_decision  TEXT,
  editor_v1_note      TEXT,
  -- Story Editor fields
  story_editor_decision TEXT,
  story_editor_note   TEXT,
  brief_json          TEXT,
  -- Master fields
  master_decision     TEXT,
  master_note         TEXT,
  -- Pipeline state
  status              TEXT NOT NULL DEFAULT 'pending',
  pipeline_version    TEXT NOT NULL DEFAULT 'V3.6',
  pipeline_log        TEXT,
  notes               TEXT
);

CREATE INDEX IF NOT EXISTS idx_crawl_log_funnel ON crawl_log(funnel_batch_id);
CREATE INDEX IF NOT EXISTS idx_crawl_log_ticker_status ON crawl_log(ticker, status);
CREATE UNIQUE INDEX IF NOT EXISTS idx_crawl_log_url ON crawl_log(source_url);

CREATE TABLE IF NOT EXISTS generated_news (
  article_id          TEXT PRIMARY KEY,
  row_id              TEXT NOT NULL,
  ticker              TEXT NOT NULL,
  sector              TEXT NOT NULL,
  title               TEXT NOT NULL,
  body                TEXT NOT NULL,
  word_count          INTEGER,
  key_view            TEXT,
  insight_final       TEXT,
  insight_type        TEXT,
  variety_guard_angle TEXT,
  accepted_hypothesis INTEGER NOT NULL,
  data_sources_used   TEXT,
  brief_json          TEXT,
  history_referenced  TEXT,
  skeptic_critique    TEXT,
  skeptic_angle       TEXT,
  skeptic_verdict     TEXT,
  status              TEXT NOT NULL DEFAULT 'draft',
  published_at        TEXT,
  pipeline_version    TEXT NOT NULL DEFAULT 'V3.6',
  pipeline_log        TEXT,
  FOREIGN KEY (row_id) REFERENCES crawl_log(row_id)
);

CREATE INDEX IF NOT EXISTS idx_generated_ticker_published ON generated_news(ticker, published_at DESC);
```

- [ ] **Step 2: Write `lib/__init__.py`** (empty file)

```bash
touch "/Users/trungdt/Desktop/Stream Intelligent/lib/__init__.py" "/Users/trungdt/Desktop/Stream Intelligent/tests/__init__.py"
```

- [ ] **Step 3: Write failing test `tests/test_pipeline_db.py`**

```python
"""Tests for lib.pipeline_db — SQLite ops on crawl_log + generated_news."""
import pytest
import tempfile
import os
from pathlib import Path

from lib.pipeline_db import PipelineDB


@pytest.fixture
def db():
    """Fresh in-memory DB initialized with schema."""
    schema_path = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db = PipelineDB(":memory:")
    db.init_schema(schema_path)
    yield db
    db.close()


def test_init_schema_creates_tables(db):
    """Schema init creates crawl_log + generated_news tables."""
    tables = db.list_tables()
    assert "crawl_log" in tables
    assert "generated_news" in tables


def test_insert_crawl_row_returns_row_id(db):
    """insert_crawl_row returns the row_id used."""
    row_id = db.insert_crawl_row({
        "row_id": "uuid-1",
        "funnel_batch_id": "VCB-20260508-1530",
        "ticker": "VCB",
        "source_name": "Báo Pháp luật",
        "source_url": "https://example.com/a1",
        "title": "Test article",
        "crawled_at": "2026-05-08T15:30:00+07:00",
    })
    assert row_id == "uuid-1"


def test_insert_duplicate_url_raises(db):
    """Inserting same source_url twice raises (UNIQUE constraint)."""
    base = {
        "funnel_batch_id": "VCB-20260508-1530",
        "ticker": "VCB",
        "source_name": "X",
        "source_url": "https://example.com/dup",
        "title": "T",
        "crawled_at": "2026-05-08T00:00:00+07:00",
    }
    db.insert_crawl_row({"row_id": "u1", **base})
    with pytest.raises(Exception):
        db.insert_crawl_row({"row_id": "u2", **base})


def test_get_crawl_row_returns_dict(db):
    """get_crawl_row returns dict with all fields, None for unset."""
    db.insert_crawl_row({
        "row_id": "uuid-2",
        "funnel_batch_id": "TCB-20260508-1530",
        "ticker": "TCB",
        "source_name": "VnEconomy",
        "source_url": "https://example.com/a2",
        "title": "T2",
        "crawled_at": "2026-05-08T00:00:00+07:00",
    })
    row = db.get_crawl_row("uuid-2")
    assert row["ticker"] == "TCB"
    assert row["status"] == "pending"  # default
    assert row["editor_v1_decision"] is None  # not set


def test_update_crawl_row_partial(db):
    """update_crawl_row updates only the keys passed."""
    db.insert_crawl_row({
        "row_id": "uuid-3",
        "funnel_batch_id": "B",
        "ticker": "VCB",
        "source_name": "X",
        "source_url": "https://example.com/a3",
        "title": "T",
        "crawled_at": "2026-05-08T00:00:00+07:00",
    })
    db.update_crawl_row("uuid-3", {
        "editor_v1_decision": "route_to_story_editor",
        "primary_ticker": "VCB",
        "sector": "Bank",
    })
    row = db.get_crawl_row("uuid-3")
    assert row["editor_v1_decision"] == "route_to_story_editor"
    assert row["sector"] == "Bank"
    assert row["title"] == "T"  # untouched


def test_query_by_funnel_batch(db):
    """query_by_funnel_batch returns all rows for batch_id, sorted by crawled_at desc."""
    for i, ts in enumerate(["2026-05-08T10:00:00+07:00", "2026-05-08T12:00:00+07:00"]):
        db.insert_crawl_row({
            "row_id": f"u{i}",
            "funnel_batch_id": "VCB-20260508-1530",
            "ticker": "VCB",
            "source_name": f"S{i}",
            "source_url": f"https://example.com/{i}",
            "title": "T",
            "crawled_at": ts,
        })
    rows = db.query_by_funnel_batch("VCB-20260508-1530")
    assert len(rows) == 2
    # newest first
    assert rows[0]["crawled_at"] == "2026-05-08T12:00:00+07:00"


def test_insert_generated_news_links_to_crawl_row(db):
    """generated_news insert with row_id FK works."""
    db.insert_crawl_row({
        "row_id": "u-anchor",
        "funnel_batch_id": "B",
        "ticker": "VCB",
        "source_name": "X",
        "source_url": "https://example.com/anchor",
        "title": "T",
        "crawled_at": "2026-05-08T00:00:00+07:00",
    })
    aid = db.insert_generated_news({
        "article_id": "art-1",
        "row_id": "u-anchor",
        "ticker": "VCB",
        "sector": "Bank",
        "title": "Article title",
        "body": "Body...",
        "word_count": 354,
        "accepted_hypothesis": 1,
    })
    assert aid == "art-1"
    arts = db.recent_generated_news("VCB", limit=3)
    assert len(arts) == 1
    assert arts[0]["title"] == "Article title"
```

- [ ] **Step 4: Run failing test**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_pipeline_db.py -v
```

Expected: FAIL with "No module named 'lib.pipeline_db'".

- [ ] **Step 5: Write `lib/pipeline_db.py`**

```python
"""SQLite ops cho pipeline state — crawl_log + generated_news.

Thin wrapper around sqlite3 stdlib, dict-in/out interface.
"""
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Any


class PipelineDB:
    """SQLite handle for crawl_log + generated_news."""

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

    def init_schema(self, schema_path: str | Path) -> None:
        sql = Path(schema_path).read_text(encoding="utf-8")
        self.conn.executescript(sql)
        self.conn.commit()

    def list_tables(self) -> list[str]:
        cur = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        return [r["name"] for r in cur.fetchall()]

    def insert_crawl_row(self, data: dict[str, Any]) -> str:
        cols = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        sql = f"INSERT INTO crawl_log ({cols}) VALUES ({placeholders})"
        self.conn.execute(sql, list(data.values()))
        self.conn.commit()
        return data["row_id"]

    def get_crawl_row(self, row_id: str) -> dict[str, Any] | None:
        cur = self.conn.execute("SELECT * FROM crawl_log WHERE row_id = ?", (row_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def update_crawl_row(self, row_id: str, updates: dict[str, Any]) -> None:
        if not updates:
            return
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        sql = f"UPDATE crawl_log SET {set_clause} WHERE row_id = ?"
        self.conn.execute(sql, [*updates.values(), row_id])
        self.conn.commit()

    def query_by_funnel_batch(self, batch_id: str) -> list[dict[str, Any]]:
        cur = self.conn.execute(
            "SELECT * FROM crawl_log WHERE funnel_batch_id = ? ORDER BY crawled_at DESC",
            (batch_id,),
        )
        return [dict(r) for r in cur.fetchall()]

    def query_pending_for_editor(self) -> list[dict[str, Any]]:
        cur = self.conn.execute(
            "SELECT * FROM crawl_log WHERE status = 'pending' AND editor_v1_decision IS NULL"
        )
        return [dict(r) for r in cur.fetchall()]

    def insert_generated_news(self, data: dict[str, Any]) -> str:
        cols = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        sql = f"INSERT INTO generated_news ({cols}) VALUES ({placeholders})"
        self.conn.execute(sql, list(data.values()))
        self.conn.commit()
        return data["article_id"]

    def update_generated_news(self, article_id: str, updates: dict[str, Any]) -> None:
        if not updates:
            return
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        sql = f"UPDATE generated_news SET {set_clause} WHERE article_id = ?"
        self.conn.execute(sql, [*updates.values(), article_id])
        self.conn.commit()

    def recent_generated_news(self, ticker: str, limit: int = 3) -> list[dict[str, Any]]:
        cur = self.conn.execute(
            "SELECT * FROM generated_news WHERE ticker = ? AND status = 'published' "
            "ORDER BY published_at DESC LIMIT ?",
            (ticker, limit),
        )
        return [dict(r) for r in cur.fetchall()]

    def close(self) -> None:
        self.conn.close()
```

- [ ] **Step 6: Run tests pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_pipeline_db.py -v
```

Expected: 7 passed.

- [ ] **Step 7: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add data/ lib/ tests/ && git commit -m "feat(lib): pipeline_db SQLite wrapper + schema + 7 TDD tests"
```

---

### Task 3: Finpath API wrapper (TDD with mocked HTTP)

**Files:**
- Create: `lib/finpath_api.py`, `tests/test_finpath_api.py`

- [ ] **Step 1: Write failing test `tests/test_finpath_api.py`**

```python
"""Tests for lib.finpath_api — Bank endpoints wrapper."""
import pytest
import responses

from lib.finpath_api import FinpathAPI


@pytest.fixture
def api():
    return FinpathAPI(base_url="https://api.finpath.vn")


@responses.activate
def test_get_bank_ratios_returns_data(api):
    """get_bank_ratios returns the .data dict from response."""
    responses.add(
        responses.GET,
        "https://api.finpath.vn/api/stocks/bankfinancialratios/VCB",
        json={"data": {"yearlyProfits": [{"code": "VCB", "nim": 2.6}], "quarterlyProfits": []}},
        status=200,
    )
    result = api.get_bank_ratios("VCB")
    assert "yearlyProfits" in result
    assert result["yearlyProfits"][0]["code"] == "VCB"


@responses.activate
def test_get_bank_ratios_batch_csv(api):
    """get_bank_ratios_batch joins tickers with comma."""
    responses.add(
        responses.GET,
        "https://api.finpath.vn/api/stocks/bankfinancialratios-eboard",
        json={"data": [{"code": "TCB"}, {"code": "VCB"}]},
        status=200,
    )
    result = api.get_bank_ratios_batch(["TCB", "VCB"])
    assert len(result) == 2
    assert responses.calls[0].request.url.endswith("?codes=TCB%2CVCB") or \
        responses.calls[0].request.url.endswith("?codes=TCB,VCB")


@responses.activate
def test_caches_repeat_calls(api):
    """Same ticker query twice → 1 HTTP call (in-memory cache)."""
    responses.add(
        responses.GET,
        "https://api.finpath.vn/api/stocks/bankfinancialratios/VCB",
        json={"data": {"yearlyProfits": [], "quarterlyProfits": []}},
        status=200,
    )
    api.get_bank_ratios("VCB")
    api.get_bank_ratios("VCB")
    assert len(responses.calls) == 1


@responses.activate
def test_404_raises(api):
    responses.add(
        responses.GET,
        "https://api.finpath.vn/api/stocks/bankfinancialratios/XXX",
        json={"error": "not found"},
        status=404,
    )
    with pytest.raises(Exception):
        api.get_bank_ratios("XXX")


@responses.activate
def test_get_shareholders(api):
    responses.add(
        responses.GET,
        "https://api.finpath.vn/api/stocks/shareholderstructure/VCB",
        json={"data": {"yearlyProfits": [{"foreign_pct": 22}]}},
        status=200,
    )
    result = api.get_shareholders("VCB")
    assert "yearlyProfits" in result


@responses.activate
def test_get_events(api):
    responses.add(
        responses.GET,
        "https://api.finpath.vn/api/events/VCB",
        json={"data": [{"event": "dividend"}]},
        status=200,
    )
    result = api.get_events("VCB")
    assert isinstance(result, list)
    assert result[0]["event"] == "dividend"
```

- [ ] **Step 2: Run failing test**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_finpath_api.py -v
```

Expected: FAIL "No module named 'lib.finpath_api'".

- [ ] **Step 3: Write `lib/finpath_api.py`**

```python
"""Finpath API wrapper — public Bank endpoints.

Verified 2026-05-08: https://api.finpath.vn returns 200 OK no auth.
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
        """NIM, CASA, COF, NPL, LDR, P/E, P/B, ROE."""
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
```

- [ ] **Step 4: Run tests pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_finpath_api.py -v
```

Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add lib/finpath_api.py tests/test_finpath_api.py && git commit -m "feat(lib): finpath_api wrapper 14 Bank endpoints + cache + 6 TDD tests"
```

---

### Task 4: notion_fetch helper

**Files:**
- Create: `lib/notion_fetch.py`

This module is a thin async-style helper for Notion MCP calls — used by `kb_ingest.py`. Since Notion MCP is only callable from Claude (not from plain Python), this module's actual implementation will be minimal: it documents the protocol for retrieving pages + blocks via MCP, and defines pure-data helpers for converting block trees to markdown. The orchestrator code (kb_ingest.py CLI) will be invoked BY Claude with MCP tools available, not by a plain Python entrypoint.

- [ ] **Step 1: Write `lib/notion_fetch.py`**

```python
"""Notion MCP helpers — block tree → markdown conversion.

Note: Notion MCP tools are accessible only when this module's helpers
are called from a Claude Code session that has loaded the relevant
mcp__notion__* tools. Pure functions in this module work on already-fetched
block dicts (no HTTP calls of their own).
"""
from __future__ import annotations
from typing import Any


def render_rich_text(rich_text: list[dict]) -> str:
    """Convert Notion rich_text array to markdown inline string."""
    parts = []
    for span in rich_text:
        text = span.get("plain_text", "")
        ann = span.get("annotations", {})
        href = span.get("href")
        if ann.get("code"):
            text = f"`{text}`"
        if ann.get("bold"):
            text = f"**{text}**"
        if ann.get("italic"):
            text = f"*{text}*"
        if href:
            text = f"[{text}]({href})"
        parts.append(text)
    return "".join(parts)


def render_block(block: dict, children_rendered: str = "") -> str:
    """Convert a single Notion block dict to markdown.

    Args:
        block: Notion block (with type + type-specific data)
        children_rendered: pre-rendered markdown of nested children blocks
    """
    btype = block.get("type", "")
    payload = block.get(btype, {})

    if btype == "paragraph":
        text = render_rich_text(payload.get("rich_text", []))
        return f"{text}\n\n" + children_rendered

    if btype == "heading_1":
        text = render_rich_text(payload.get("rich_text", []))
        return f"# {text}\n\n" + children_rendered

    if btype == "heading_2":
        text = render_rich_text(payload.get("rich_text", []))
        return f"## {text}\n\n" + children_rendered

    if btype == "heading_3":
        text = render_rich_text(payload.get("rich_text", []))
        return f"### {text}\n\n" + children_rendered

    if btype == "bulleted_list_item":
        text = render_rich_text(payload.get("rich_text", []))
        nested = "\n".join(f"  {line}" for line in children_rendered.splitlines() if line)
        return f"- {text}\n" + (f"{nested}\n" if nested else "")

    if btype == "numbered_list_item":
        text = render_rich_text(payload.get("rich_text", []))
        return f"1. {text}\n"

    if btype == "quote":
        text = render_rich_text(payload.get("rich_text", []))
        return f"> {text}\n\n"

    if btype == "code":
        text = render_rich_text(payload.get("rich_text", []))
        lang = payload.get("language", "")
        return f"```{lang}\n{text}\n```\n\n"

    if btype == "callout":
        text = render_rich_text(payload.get("rich_text", []))
        emoji = payload.get("icon", {}).get("emoji", "")
        return f"> {emoji} {text}\n\n" + children_rendered

    if btype == "toggle":
        summary = render_rich_text(payload.get("rich_text", []))
        return f"<details><summary>{summary}</summary>\n\n{children_rendered}</details>\n\n"

    if btype == "divider":
        return "---\n\n"

    if btype == "child_page":
        title = payload.get("title", "")
        return f"[{title}]\n\n"

    if btype == "column_list" or btype == "column":
        # column wrapping handled by caller; render children inline
        return children_rendered

    return ""  # unsupported types skipped


def slugify(text: str, max_len: int = 60) -> str:
    """Convert title to URL-safe slug for filenames."""
    import re
    import unicodedata

    # Strip accents
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:max_len] or "untitled"
```

- [ ] **Step 2: TypeScript-style smoke test (Python)**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.notion_fetch import render_rich_text, slugify, render_block
assert render_rich_text([{'plain_text': 'hi', 'annotations': {'bold': True}}]) == '**hi**'
assert slugify('🏦 Banking — KQKD Q1/2026') == 'banking-kqkd-q1-2026'
assert render_block({'type': 'paragraph', 'paragraph': {'rich_text': [{'plain_text': 'p', 'annotations': {}}]}}) == 'p\n\n'
print('OK')
"
```

Expected: `OK`.

- [ ] **Step 3: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add lib/notion_fetch.py && git commit -m "feat(lib): notion_fetch — Notion block → markdown rendering helpers"
```

---

### Task 5: kb_ingest CLI

**Files:**
- Create: `lib/kb_ingest.py`

This script crawls Notion's Bank Sector hub via MCP (executed from Claude Code session) and writes markdown files to `kb/bank/`. Since Python can't directly call MCP, this script is **invoked through Claude's Bash tool** — Claude provides MCP results via Read tool or environment, OR (recommended) the script uses subprocess to invoke a Claude Code session with MCP. For Phase 2, we structure the code as a callable Python module + a CLI that the user runs from Claude (which has MCP tools loaded).

The simpler approach for Phase 2: **the kb_ingest is run BY Claude in a session that has Notion MCP loaded**, NOT as a standalone python entrypoint. The "CLI" is conceptual: Claude executes a series of `mcp__notion__*` calls + writes markdown via Write tool.

For this task, we create a **helper module** that provides building blocks (slugify, render_block, frontmatter writer), and a **runbook** documented in the module docstring. Actual ingest is performed by a Claude session running `python lib/kb_ingest.py --bank-sector-id 359273c7-a9a1-810f-9306-cb6227d9c94a` — but the script itself doesn't make HTTP calls; it expects pre-fetched block trees passed via stdin or file.

To keep Phase 2 testable WITHOUT requiring live Notion access, we make `kb_ingest.py` accept a **JSON dump of the block tree** as input.

- [ ] **Step 1: Write `lib/kb_ingest.py`**

```python
"""KB ingest — convert Notion Bank Sector page tree to markdown files.

Workflow:
  1. Claude session fetches Notion blocks via mcp__notion__API-get-block-children
     (recursive), saves the tree as JSON to /tmp/bank-sector-tree.json
  2. Run: python lib/kb_ingest.py /tmp/bank-sector-tree.json kb/bank/
  3. Script renders each KB topic page as a markdown file with frontmatter:
       notion_page_id, source_url, last_synced, category, title

Bank Sector hub ID: 359273c7-a9a1-810f-9306-cb6227d9c94a

Tree JSON format:
  {
    "pages": [
      {
        "id": "<uuid>",
        "title": "<title>",
        "url": "https://notion.so/...",
        "last_edited_time": "<iso>",
        "category": "frameworks|trends|history|per-ticker",
        "blocks": [<block dict>, <block dict>, ...]
      },
      ...
    ]
  }
"""
from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from lib.notion_fetch import render_block, slugify


def render_blocks_recursive(blocks: list[dict]) -> str:
    """Render a flat list of blocks (children are inlined) into markdown.

    The input format expects each block to optionally have a "children" key
    with already-fetched child blocks.
    """
    out = []
    for blk in blocks:
        children = blk.get("children", [])
        children_md = render_blocks_recursive(children) if children else ""
        out.append(render_block(blk, children_md))
    return "".join(out)


def write_kb_page(page: dict, output_dir: Path) -> Path:
    """Write a single KB page to output_dir/<category>/<slug>.md.

    Returns the file path written.
    """
    category = page.get("category", "uncategorized")
    title = page.get("title", "Untitled")
    slug = slugify(title)
    cat_dir = output_dir / category
    cat_dir.mkdir(parents=True, exist_ok=True)
    file_path = cat_dir / f"{slug}.md"

    body_md = render_blocks_recursive(page.get("blocks", []))

    fm_lines = [
        "---",
        f'notion_page_id: "{page["id"]}"',
        f'source_url: "{page.get("url", "")}"',
        f'last_synced: {datetime.now(timezone.utc).isoformat()}',
        f'category: {category}',
        f'title: "{title.replace(chr(34), chr(92) + chr(34))}"',
        "---",
        "",
    ]
    file_path.write_text("\n".join(fm_lines) + body_md, encoding="utf-8")
    return file_path


def ingest(tree_json_path: Path, output_dir: Path) -> dict:
    data = json.loads(tree_json_path.read_text(encoding="utf-8"))
    pages = data.get("pages", [])
    written = []
    errors = []
    for page in pages:
        try:
            path = write_kb_page(page, output_dir)
            written.append(str(path))
        except Exception as e:  # noqa: BLE001
            errors.append({"page_id": page.get("id"), "error": str(e)})
    return {"written": written, "errors": errors, "count": len(written)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tree_json", type=Path, help="Path to JSON file with Notion block tree")
    parser.add_argument("output_dir", type=Path, default=Path("kb/bank/"), nargs="?")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    if not args.tree_json.exists():
        print(f"Error: {args.tree_json} not found", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)
    result = ingest(args.tree_json, args.output_dir)
    print(json.dumps(result, indent=2))
    return 0 if not result["errors"] else 2


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Smoke test with synthetic input**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && cat > /tmp/test-tree.json <<'EOF'
{
  "pages": [
    {
      "id": "test-page-1",
      "title": "Test Framework",
      "url": "https://notion.so/test",
      "category": "frameworks",
      "blocks": [
        {
          "type": "heading_2",
          "heading_2": {"rich_text": [{"plain_text": "Intro", "annotations": {}}]}
        },
        {
          "type": "paragraph",
          "paragraph": {"rich_text": [{"plain_text": "Hello world.", "annotations": {}}]}
        }
      ]
    }
  ]
}
EOF
mkdir -p /tmp/test-kb
uv run python lib/kb_ingest.py /tmp/test-tree.json /tmp/test-kb/
ls /tmp/test-kb/frameworks/
cat /tmp/test-kb/frameworks/test-framework.md
```

Expected: file `test-framework.md` exists with frontmatter + heading + paragraph. JSON output shows `"count": 1`.

- [ ] **Step 3: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add lib/kb_ingest.py && git commit -m "feat(lib): kb_ingest CLI — Notion tree JSON → kb/bank/ markdown files"
```

---

### Task 6: Run live KB ingest from Notion

**Files:**
- Create: `kb/bank/<category>/<slug>.md` files (multiple, depending on Notion content)
- Create: `kb/bank/.last_synced/<page_id>` marker files (gitignored)

This task is performed by Claude (MCP-equipped) — fetch Notion Bank Sector tree + run ingest.

- [ ] **Step 1: Fetch Bank Sector hub + sub-pages via MCP**

The hub page `359273c7-a9a1-810f-9306-cb6227d9c94a` already verified shared. Crawl recursively:
1. Get hub block children → find mention links + child_page blocks
2. For "📚 KB ngành Ngân hàng" sub-page (if linked) → get children
3. For "🔬 Frameworks" sub-page (`358273c7-a9a1-81a6-82fa-c31c02a5df62`) → get children
4. For each child page found: fetch its blocks recursively (depth 3 max)

Build the JSON tree:
```json
{"pages": [{"id": ..., "title": ..., "url": ..., "category": ..., "blocks": [...]}]}
```

Categorize:
- Frameworks page children → `category: frameworks`
- KB-ngành children → infer from title: `trends` (CASA-evolution, NPL-benchmark) / `history` (2018-NPL-spike) / `frameworks` / `per-ticker` (VCB-strategic-shifts)

Save tree to `/tmp/bank-sector-tree.json`.

- [ ] **Step 2: Run ingest**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python lib/kb_ingest.py /tmp/bank-sector-tree.json kb/bank/
```

Expected: JSON output with `count: N` (N = number of KB topics fetched), `errors: []`.

- [ ] **Step 3: Spot check 2 files**

```bash
ls kb/bank/
cat kb/bank/frameworks/$(ls kb/bank/frameworks/ | head -1)
```

- [ ] **Step 4: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add kb/ && git commit -m "feat(kb): bootstrap Bank Sector KB from Notion (one-time ingest)"
```

---

### Task 7: kb_loader runtime (TDD)

**Files:**
- Create: `lib/kb_loader.py`, `tests/test_kb_loader.py`

- [ ] **Step 1: Write failing test**

```python
"""Tests for lib.kb_loader."""
import pytest
from pathlib import Path

from lib.kb_loader import KBLoader


@pytest.fixture
def kb_dir(tmp_path):
    """Create a fake kb/ tree."""
    fw = tmp_path / "frameworks"
    fw.mkdir()
    (fw / "big4-pattern.md").write_text(
        "---\ntitle: \"Big4 vs tư nhân pattern\"\ncategory: frameworks\n---\n\n"
        "Big4 (VCB BID CTG VietinBank) under-promise hơn tư nhân.",
        encoding="utf-8",
    )
    (fw / "casa-evolution.md").write_text(
        "---\ntitle: \"CASA evolution\"\ncategory: frameworks\n---\n\n"
        "Tỷ lệ CASA tăng trend 2020-2025.",
        encoding="utf-8",
    )
    return tmp_path


def test_search_returns_matching_files(kb_dir):
    loader = KBLoader(kb_dir)
    results = loader.search(["Big4"])
    assert len(results) == 1
    assert "big4-pattern.md" in results[0]["path"]


def test_search_multiple_keywords_AND(kb_dir):
    loader = KBLoader(kb_dir)
    results = loader.search(["Big4", "VCB"])
    assert len(results) == 1


def test_search_no_match(kb_dir):
    loader = KBLoader(kb_dir)
    results = loader.search(["NoSuchTopic"])
    assert results == []


def test_load_topic_returns_full_content(kb_dir):
    loader = KBLoader(kb_dir)
    content = loader.load_topic("frameworks/big4-pattern.md")
    assert "under-promise" in content


def test_load_topic_missing_raises(kb_dir):
    loader = KBLoader(kb_dir)
    with pytest.raises(FileNotFoundError):
        loader.load_topic("frameworks/missing.md")


def test_search_by_category(kb_dir):
    loader = KBLoader(kb_dir)
    results = loader.search(["CASA"], category="frameworks")
    assert len(results) == 1
    assert results[0]["category"] == "frameworks"
```

- [ ] **Step 2: Run failing test**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_kb_loader.py -v
```

Expected: FAIL "No module named 'lib.kb_loader'".

- [ ] **Step 3: Write `lib/kb_loader.py`**

```python
"""KB runtime loader — read kb/bank/ markdown files (no Notion calls).

Usage:
  loader = KBLoader(Path("kb/bank/"))
  matches = loader.search(["NPL", "Basel"])
  body = loader.load_topic(matches[0]["path"])
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Any


class KBLoader:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def _all_files(self) -> list[Path]:
        if not self.root.exists():
            return []
        return list(self.root.rglob("*.md"))

    @staticmethod
    def _extract_frontmatter(text: str) -> dict[str, str]:
        m = re.match(r"^---\n([\s\S]*?)\n---\n", text)
        if not m:
            return {}
        fm: dict[str, str] = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip().strip('"')
        return fm

    def search(self, keywords: list[str], category: str | None = None) -> list[dict[str, Any]]:
        """Return KB files matching ALL keywords (case-insensitive).

        Optionally filter by category.
        """
        if not keywords:
            return []
        keywords_lc = [k.lower() for k in keywords]
        results: list[dict[str, Any]] = []
        for path in self._all_files():
            text = path.read_text(encoding="utf-8")
            text_lc = text.lower()
            if not all(k in text_lc for k in keywords_lc):
                continue
            fm = self._extract_frontmatter(text)
            cat = fm.get("category", path.parent.name)
            if category and cat != category:
                continue
            relpath = str(path.relative_to(self.root))
            score = sum(text_lc.count(k) for k in keywords_lc)
            results.append({
                "path": relpath,
                "title": fm.get("title", path.stem),
                "category": cat,
                "score": score,
                "snippet": text[len(text) - len(text.lstrip()):].split("\n\n")[1][:200] if "\n\n" in text else "",
            })
        results.sort(key=lambda r: r["score"], reverse=True)
        return results

    def load_topic(self, relative_path: str) -> str:
        full = self.root / relative_path
        if not full.exists():
            raise FileNotFoundError(f"KB topic not found: {relative_path}")
        return full.read_text(encoding="utf-8")
```

- [ ] **Step 4: Run tests pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_kb_loader.py -v
```

Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add lib/kb_loader.py tests/test_kb_loader.py && git commit -m "feat(lib): kb_loader runtime grep + load + 6 TDD tests"
```

---

### Task 8: Manual YAML stubs

**Files:**
- Create: `data/manual/targets.yaml`, `data/manual/credit_room.yaml`, `data/manual/nhnn_circulars.yaml`

- [ ] **Step 1: Write `data/manual/targets.yaml`**

```yaml
# Targets vs Actual — kế hoạch ĐHĐCĐ vs thực tế per quý
# Source: nghị quyết ĐHĐCĐ năm + quarterly BCTC
# MOCK stubs cho Phase 2 testing — replace với data thật khi cần

- ticker: VCB
  year: 2026
  target_lntt_ty: 44000             # tỷ đồng — kế hoạch năm
  target_credit_growth_pct: 16.5
  actual_lntt_q1_ty: 11803
  actual_credit_growth_q1_pct: 4.2
  source: "Nghị quyết ĐHĐCĐ 25/4/2026"
  source_url: "https://example.com/vcb-dhcd-2026"

- ticker: TCB
  year: 2026
  target_lntt_ty: 31500
  target_credit_growth_pct: 19.0
  actual_lntt_q1_ty: 8870
  actual_credit_growth_q1_pct: 5.1
  source: "Nghị quyết ĐHĐCĐ 22/4/2026"
  source_url: "https://example.com/tcb-dhcd-2026"

- ticker: MBB
  year: 2026
  target_lntt_ty: 28000
  target_credit_growth_pct: 18.0
  actual_lntt_q1_ty: 6500
  actual_credit_growth_q1_pct: 4.5
  source: "Nghị quyết ĐHĐCĐ 20/4/2026"
  source_url: "https://example.com/mbb-dhcd-2026"
```

- [ ] **Step 2: Write `data/manual/credit_room.yaml`**

```yaml
# Credit Room — NHNN allocation per bank per năm
# Source: thông báo NHNN + công bố ngân hàng
# MOCK stubs cho Phase 2 testing

- ticker: VCB
  year: 2026
  credit_room_pct: 16.0
  notes: "Big4 chuẩn vốn quốc tế cao hơn → room ưu đãi"

- ticker: TCB
  year: 2026
  credit_room_pct: 19.0
  notes: "Tư nhân vốn lớn, room cao do CASA + NIM tốt"

- ticker: MBB
  year: 2026
  credit_room_pct: 18.0
  notes: "Tech bank positioning"

- ticker: BID
  year: 2026
  credit_room_pct: 14.5
  notes: "Big4 conservative"
```

- [ ] **Step 3: Write `data/manual/nhnn_circulars.yaml`**

```yaml
# NHNN circulars affecting Bank sector
# MOCK stubs cho Phase 2 testing

- title: "Thông tư 02/2025/TT-NHNN"
  effective_date: 2025-04-01
  affected_topics: ["NPL classification", "Coverage ratio"]
  summary: "Siết tiêu chí phân loại nợ xấu nhóm 3-5, yêu cầu coverage ratio tối thiểu 100%."
  url: "https://example.com/nhnn-tt02-2025"

- title: "Thông tư 06/2025/TT-NHNN"
  effective_date: 2025-09-01
  affected_topics: ["Credit room", "Capital buffer"]
  summary: "Cấp room tín dụng theo CAR + NPL benchmark Q2 mỗi năm."
  url: "https://example.com/nhnn-tt06-2025"

- title: "Thông tư 11/2025/TT-NHNN"
  effective_date: 2026-01-01
  affected_topics: ["Basel III implementation"]
  summary: "Lộ trình áp dụng tiêu chuẩn vốn quốc tế mới (Basel III) cho Big4 từ 1/1/2026."
  url: "https://example.com/nhnn-tt11-2025"
```

- [ ] **Step 4: Smoke test load**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import yaml
from pathlib import Path
for name in ['targets', 'credit_room', 'nhnn_circulars']:
    data = yaml.safe_load(Path(f'data/manual/{name}.yaml').read_text())
    assert isinstance(data, list) and len(data) >= 3, f'{name} should be list with 3+ items'
    print(f'{name}: {len(data)} items OK')
"
```

Expected: each file loads with ≥3 items.

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add data/manual/ && git commit -m "feat(data): YAML stubs — targets + credit_room + nhnn_circulars (3-4 row each)"
```

---

### Task 9: Final test sweep + tag

- [ ] **Step 1: Run full pytest**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest -v
```

Expected: ~19 tests pass (7 pipeline_db + 6 finpath_api + 6 kb_loader).

- [ ] **Step 2: Tag**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git tag phase-2-data-layer
```

---

## Acceptance criteria for Phase 2 done

1. ✅ `uv run pytest -v` passes ~19 tests
2. ✅ `lib/pipeline_db.py` SQLite ops working (insert/update/query)
3. ✅ `lib/finpath_api.py` 14 endpoints typed + cached
4. ✅ `lib/notion_fetch.py` block→markdown helpers + slugify
5. ✅ `lib/kb_ingest.py` CLI accepts JSON tree → writes kb/bank/<category>/<slug>.md
6. ✅ KB Bank ingested from Notion (kb/bank/ has files)
7. ✅ `lib/kb_loader.py` runtime grep working
8. ✅ 3 YAML stub files exist
9. ✅ git tag `phase-2-data-layer`

---

## Out of scope for Phase 2

- ❌ Crawler Python script (Phase 3)
- ❌ render_compare_feed.py (Phase 3)
- ❌ Slash command + agents (Phase 3-4)
- ❌ Master Bank LLM logic (Phase 4)
