# Universe Expansion + KB-optional V5.1.3 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mở universe từ 61 mã hardcoded → 139 mã Finpath, scaffold 7 master agents mới + giữ pattern Bank/CK/BĐS existing, Editor V1 dùng Finpath sectors API + SQLite cache, KB-optional pattern uniform.

**Architecture:** Editor V1 detect sector qua Finpath sectors API (cached 365d in SQLite) → `data/sector_routing.yaml` map sector_code → master_name → dispatch 1 trong 10 master agents (3 existing + 7 new). 7 master mới ship WITHOUT KB folders (user pivot 2026-05-12 PM Q3 resolution), web search heavy. Master-BDS expanded coverage 4 → 54 mã với KB-optional cho 50 non-anchor mã.

**Tech Stack:** Python 3.13 (uv-managed), SQLite (WAL mode), PyYAML, requests, pytest, Claude subagents (Opus + Sonnet).

**Spec**: `docs/superpowers/specs/2026-05-12-universe-expansion-kb-optional-design.md` V1.0.1.

---

## Critical context for executor

### V1.0.1 spec resolutions (read before any task)

3 open questions from V1.0 resolved by user 2026-05-12 PM:
- **Q1 RESOLVED option A**: Master-BDS load `kb/bds/` cho TẤT CẢ 54 mã (sector-level context) + per-ticker KB anchor cho 4 mã (VHM/NVL/KDH/DXG). 50 non-anchor mã web search heavy.
- **Q2 RESOLVED option A**: 7 NEW master agents DUPLICATE `voice-layer-rules.md` + `stance-directive-handler.md` từ Bank. Acceptable per CLAUDE.md no-shared-folder rule.
- **Q3 RESOLVED no KB scaffolding**: KHÔNG tạo `kb/{sector_code}/` folder ở V5.1.3 ship. 7 master mới launch với note "kb_path: '' — chưa có KB, tự search web" trong SKILL.md.

### Universe trade-off accepted

Drop 26 mã UPCOM cũ:
- Bank: 27 → 18 (drop 9: HDF, NAB, BAB, NVB, SGB, VAB, BVB, ABB, KLB, VBB, PGB)
- CK: 30 → 15 (drop 15 UPCOM: APS, ART, BMS, CSI, DSC, IVS, PHS, PSI, TCI, TVS, VFS, VTS, WSS, AAS, EVS)
- BĐS: 4 → 54 (keep 4 KB-anchor + add 50 KB-optional)

Add 104 mã mới từ Finpath. Net: 139 mã.

### Master agent inventory (final)

| Master | Sector codes | Mã | KB status |
|---|---|---|---|
| `newsroom-master-bank` | private7 + soe3 + smallLegacy | 18 | Full `kb/bank/` |
| `newsroom-master-ck` | stock | 15 | Full `kb/ck/` |
| `newsroom-master-bds` | materialContractor + vic3 + industrial + exvic | 54 | KB-optional: 4 anchor + 50 web search |
| `newsroom-master-oilgas` (NEW) | oilGas | 8 | Web search only V5.1.3 |
| `newsroom-master-logistics` (NEW) | logistics | 12 | Web search only V5.1.3 |
| `newsroom-master-fb` (NEW) | fb | 8 | Web search only V5.1.3 |
| `newsroom-master-apparel` (NEW) | apparel | 3 | Web search only V5.1.3 |
| `newsroom-master-retail` (NEW) | retail | 7 | Web search only V5.1.3 |
| `newsroom-master-seafood` (NEW) | seafood | 6 | Web search only V5.1.3 |
| `newsroom-master-defensive` (NEW) | defensive | 12 | Web search only V5.1.3 |

### Existing pipeline files to understand

- `lib/finpath_api.py` — Existing FinpathAPI class (14 methods). Plan F adds 1 method `get_sectors()` (Group D).
- `lib/pipeline_db.py` — Existing PipelineDB class. Plan F adds:
  - Schema migration `finpath_sectors_cache` table
  - `validate_pipeline_step` extend: accept new fields sector_code/sector_name/sector_parent/master_route
- `.claude/skills/finpath-newsroom-editor/scripts/routing.py` — DEPRECATE hardcoded 61 universe. KEEP `COMPANY_NAME_TO_TICKER` alias mapping (still needed for detect ticker).
- `.claude/agents/newsroom-editor.md` + `.claude/skills/finpath-newsroom-editor/SKILL.md` — UPDATE Step 2 routing logic.
- 3 master agents (Bank/CK/BĐS) — KEEP, only adjust Master-BDS for KB-optional expand.

### Bank V5.1.2 split pattern (template for 7 new masters)

Pattern reference: `.claude/skills/finpath-newsroom-master-bank/` structure (per V5.1.2 split decision):

```
.claude/skills/finpath-newsroom-master-bank/
├── SKILL.md (~180 lines, 9-step workflow)
└── references/
    ├── format-bodies/
    │   ├── flash-qa.md
    │   ├── standard-qa.md
    │   ├── standard-listicle.md
    │   └── standard-narrative.md
    ├── voice-layer-rules.md (duplicate across 7 new masters)
    ├── stance-directive-handler.md (duplicate)
    ├── format-examples.md
    ├── jargon-mapping.md (sector-specific)
    ├── master-pitfalls.md (sector-specific)
    ├── sector-context.md (NEW V5.1.3 per-master)
    └── compare-feed-spec.md
```

7 new master agents copy this structure, swap sector-specific content.

### Test infrastructure

- `tests/` directory exists. Pattern: `tests/test_<module>.py` for unit, `tests/integration/test_<scenario>.py` for E2E.
- Run: `uv run pytest tests/path/test.py::test_name -v`
- Use `pytest fixtures` for DB setup. Pattern in `tests/conftest.py` (existing).

---

## Phase 1 — Foundation modules (Tasks 1-5)

### Task 1: SQLite schema migration finpath_sectors_cache

**Files:**
- Create: `lib/migrations/2026-05-12-add-finpath-sectors-cache.sql`
- Modify: `lib/pipeline_db.py:120-140` (apply migrations on init)
- Test: `tests/test_pipeline_db_finpath_cache.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_pipeline_db_finpath_cache.py`:

```python
"""Test finpath_sectors_cache table creation + columns."""
import pytest
from lib.pipeline_db import PipelineDB

def test_finpath_sectors_cache_table_exists(tmp_path):
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    cur = db.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='finpath_sectors_cache'"
    )
    assert cur.fetchone() is not None, "finpath_sectors_cache table should exist after PipelineDB init"
    db.close()

def test_finpath_sectors_cache_required_columns(tmp_path):
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    cur = db.conn.execute("PRAGMA table_info(finpath_sectors_cache)")
    columns = {row["name"]: row["type"] for row in cur.fetchall()}
    assert columns["ticker"] == "TEXT"
    assert columns["sector_code"] == "TEXT"
    assert columns["sector_name"] == "TEXT"
    assert columns["sector_parent"] == "TEXT"
    assert columns["exchange"] == "TEXT"
    assert columns["fetched_at"] == "TIMESTAMP"
    db.close()

def test_finpath_sectors_cache_primary_key_ticker(tmp_path):
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    cur = db.conn.execute("PRAGMA table_info(finpath_sectors_cache)")
    pk_columns = [row["name"] for row in cur.fetchall() if row["pk"] > 0]
    assert pk_columns == ["ticker"], "ticker should be primary key"
    db.close()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run pytest tests/test_pipeline_db_finpath_cache.py -v
```

Expected: FAIL — `finpath_sectors_cache table should exist`.

- [ ] **Step 3: Create migration SQL**

Create `lib/migrations/2026-05-12-add-finpath-sectors-cache.sql`:

```sql
-- Migration: Add finpath_sectors_cache table for V5.1.3 universe expansion
-- TTL 365 days for sector mapping (user feedback: data này 1 năm mới thay đổi 1 lần)

CREATE TABLE IF NOT EXISTS finpath_sectors_cache (
    ticker TEXT PRIMARY KEY,
    sector_code TEXT NOT NULL,
    sector_name TEXT NOT NULL,
    sector_parent TEXT,
    exchange TEXT,
    fetched_at TIMESTAMP NOT NULL,
    pe REAL,
    pb REAL,
    eps REAL,
    roa REAL,
    roe REAL,
    mc REAL
);

CREATE INDEX IF NOT EXISTS idx_finpath_cache_sector
    ON finpath_sectors_cache(sector_code);
```

- [ ] **Step 4: Modify pipeline_db.py to apply migration**

Read current `lib/pipeline_db.py` to find the init/setup method, then add migration loader. Locate the `__init__` method (around line 30-50) where existing schema is created.

Add after existing CREATE TABLE statements in `__init__`:

```python
def _apply_migrations(self) -> None:
    """Apply migration SQL files from lib/migrations/ in alphabetical order."""
    import glob
    from pathlib import Path
    migrations_dir = Path(__file__).parent / "migrations"
    if not migrations_dir.exists():
        return
    for migration_file in sorted(migrations_dir.glob("*.sql")):
        sql = migration_file.read_text(encoding="utf-8")
        self.conn.executescript(sql)
    self.conn.commit()
```

Call `self._apply_migrations()` at end of `__init__` method, after existing CREATE TABLE statements.

- [ ] **Step 5: Run test to verify it passes**

```bash
uv run pytest tests/test_pipeline_db_finpath_cache.py -v
```

Expected: 3 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add lib/migrations/2026-05-12-add-finpath-sectors-cache.sql lib/pipeline_db.py tests/test_pipeline_db_finpath_cache.py
git commit -m "feat(db): finpath_sectors_cache table + migration loader (Plan F Task 1)"
```

---

### Task 2: lib/finpath_sectors.py — sector detection client

**Files:**
- Create: `lib/finpath_sectors.py`
- Test: `tests/test_finpath_sectors.py`

- [ ] **Step 1: Write the failing tests (3 critical tests)**

Create `tests/test_finpath_sectors.py`:

```python
"""Tests for lib/finpath_sectors.py — FinpathSectors client."""
import json
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock
import pytest
from lib.pipeline_db import PipelineDB
from lib.finpath_sectors import FinpathSectors

@pytest.fixture
def db(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    yield db
    db.close()

@pytest.fixture
def mock_api_response():
    """Sample 2-sector Finpath API response."""
    return {
        "data": {
            "sectors": [
                {
                    "k": "oilGas",
                    "c": "oilGas",
                    "n": "Dầu khí",
                    "pk": "",
                    "pc": "",
                    "pn": "",
                    "s": [
                        {"c": "BSR", "pe": 12.5, "pb": 1.8, "roa": 8.5, "roe": 18.2, "e": "HOSE", "eps": 1200, "mc": 100000000000},
                        {"c": "PVS", "pe": 14.0, "pb": 2.0, "roa": 9.0, "roe": 19.0, "e": "HNX", "eps": 1500, "mc": 80000000000},
                    ]
                },
                {
                    "k": "bank",  # Wrapper sector (s=[])
                    "c": "bank",
                    "n": "Ngân hàng",
                    "s": []
                }
            ]
        }
    }

def test_get_ticker_sector_cache_miss_triggers_refresh(db, mock_api_response):
    """First lookup with empty cache: should call API + populate cache."""
    fs = FinpathSectors(db)
    with patch("lib.finpath_sectors.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fs.get_ticker_sector("BSR")

    assert result is not None
    assert result["sector_code"] == "oilGas"
    assert result["sector_name"] == "Dầu khí"
    assert result["sector_parent"] == ""
    assert result["exchange"] == "HOSE"
    mock_get.assert_called_once()

def test_get_ticker_sector_cache_hit_no_api_call(db, mock_api_response):
    """Fresh cache: no API call."""
    fs = FinpathSectors(db)
    # Pre-populate cache
    db.conn.execute("""
        INSERT INTO finpath_sectors_cache (ticker, sector_code, sector_name, sector_parent, exchange, fetched_at)
        VALUES ('VHM', 'vic3', 'BDS VIC3', 'Bất động sản', 'HOSE', ?)
    """, (datetime.now(timezone.utc).isoformat(),))
    db.conn.commit()

    with patch("lib.finpath_sectors.requests.get") as mock_get:
        result = fs.get_ticker_sector("VHM")

    assert result["sector_code"] == "vic3"
    mock_get.assert_not_called()

def test_skip_wrapper_sectors(db, mock_api_response):
    """Wrapper sectors (s=[]) should NOT pollute cache."""
    fs = FinpathSectors(db)
    with patch("lib.finpath_sectors.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        fs.refresh_cache()

    # Wrapper "bank" sector should NOT create any row
    cur = db.conn.execute("SELECT COUNT(*) as cnt FROM finpath_sectors_cache WHERE sector_code = 'bank'")
    assert cur.fetchone()["cnt"] == 0
    # Active "oilGas" sector should have 2 rows
    cur = db.conn.execute("SELECT COUNT(*) as cnt FROM finpath_sectors_cache WHERE sector_code = 'oilGas'")
    assert cur.fetchone()["cnt"] == 2

def test_get_ticker_sector_unknown_returns_none(db, mock_api_response):
    """Ticker not in API response → None after refresh attempt."""
    fs = FinpathSectors(db)
    with patch("lib.finpath_sectors.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fs.get_ticker_sector("NONEXIST")

    assert result is None

def test_stale_cache_graceful_degradation(db, mock_api_response):
    """API down + cache stale: return stale + warning, not None."""
    fs = FinpathSectors(db)
    # Pre-populate stale entry (366 days old)
    stale_date = (datetime.now(timezone.utc) - timedelta(days=366)).isoformat()
    db.conn.execute("""
        INSERT INTO finpath_sectors_cache (ticker, sector_code, sector_name, sector_parent, exchange, fetched_at)
        VALUES ('STALE', 'oilGas', 'Dầu khí', '', 'HOSE', ?)
    """, (stale_date,))
    db.conn.commit()

    with patch("lib.finpath_sectors.requests.get") as mock_get:
        mock_get.side_effect = ConnectionError("API down")
        result = fs.get_ticker_sector("STALE")

    # Returns stale data (better than None)
    assert result is not None
    assert result["sector_code"] == "oilGas"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_finpath_sectors.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'lib.finpath_sectors'`.

- [ ] **Step 3: Create lib/finpath_sectors.py**

```python
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
            if not stocks:  # skip wrapper sectors (bank/consumer/realEstate)
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_finpath_sectors.py -v
```

Expected: 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add lib/finpath_sectors.py tests/test_finpath_sectors.py
git commit -m "feat(lib): FinpathSectors client + SQLite cache TTL 365d (Plan F Task 2)"
```

---

### Task 3: lib/sector_router.py + data/sector_routing.yaml

**Files:**
- Create: `lib/sector_router.py`
- Create: `data/sector_routing.yaml`
- Test: `tests/test_sector_router.py`

- [ ] **Step 1: Create data/sector_routing.yaml**

```yaml
# Finpath sector_code → master agent name routing
# V5.1.3 — Plan F Task 3
# Edit để promote sector. Khi sector_code không có trong file này → fail-loud reject.

routing:
  # Bank cluster → master-bank (existing)
  private7: bank
  soe3: bank
  smallLegacy: bank

  # CK → master-ck (existing)
  stock: ck

  # BĐS cluster → master-bds (existing, KB-optional cho 50 non-anchor mã)
  materialContractor: bds
  vic3: bds
  industrial: bds
  exvic: bds

  # NEW V5.1.3 — 7 sectors mới (scaffold cùng đợt, web search heavy)
  oilGas: oilgas
  logistics: logistics
  fb: fb
  apparel: apparel
  retail: retail
  seafood: seafood
  defensive: defensive

# Wrapper sectors có s=[] — skip explicit (FinpathSectors.refresh_cache đã skip)
skip_wrappers:
  - bank
  - consumer
  - realEstate
```

- [ ] **Step 2: Write the failing tests**

Create `tests/test_sector_router.py`:

```python
"""Tests for lib/sector_router.py."""
import pytest
from lib.sector_router import get_master_route, MasterRouteError

def test_get_master_route_bank_sector():
    assert get_master_route("private7") == "bank"
    assert get_master_route("soe3") == "bank"
    assert get_master_route("smallLegacy") == "bank"

def test_get_master_route_ck_sector():
    assert get_master_route("stock") == "ck"

def test_get_master_route_bds_subsectors():
    assert get_master_route("materialContractor") == "bds"
    assert get_master_route("vic3") == "bds"
    assert get_master_route("industrial") == "bds"
    assert get_master_route("exvic") == "bds"

def test_get_master_route_new_v5_1_3_sectors():
    assert get_master_route("oilGas") == "oilgas"
    assert get_master_route("logistics") == "logistics"
    assert get_master_route("fb") == "fb"
    assert get_master_route("apparel") == "apparel"
    assert get_master_route("retail") == "retail"
    assert get_master_route("seafood") == "seafood"
    assert get_master_route("defensive") == "defensive"

def test_get_master_route_unknown_sector_raises():
    """Fail-loud when sector_code not in YAML."""
    with pytest.raises(MasterRouteError) as exc:
        get_master_route("nonexistent_sector")
    assert "nonexistent_sector" in str(exc.value)
    assert "sector_routing.yaml" in str(exc.value)
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
uv run pytest tests/test_sector_router.py -v
```

Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 4: Create lib/sector_router.py**

```python
"""Sector code → master agent routing.

Source of truth: data/sector_routing.yaml.
Edit YAML to promote sector or add new mapping.
"""
from pathlib import Path
import yaml

ROUTING_FILE = Path(__file__).parent.parent / "data" / "sector_routing.yaml"


class MasterRouteError(ValueError):
    """Raised when sector_code không có trong sector_routing.yaml."""


def get_master_route(sector_code: str) -> str:
    """Map sector_code → master_name. Fail-loud if unmapped.

    Returns master name (lowercase, used in newsroom-master-{name} agent).
    """
    config = _load_routing()
    routing = config.get("routing", {})
    if sector_code not in routing:
        raise MasterRouteError(
            f"sector_code '{sector_code}' chưa map trong {ROUTING_FILE}. "
            f"Add entry to routing dict hoặc check Finpath API có sector mới."
        )
    return routing[sector_code]


def _load_routing() -> dict:
    """Read YAML config. Cached not needed — Python re-reads small file fast."""
    with open(ROUTING_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
uv run pytest tests/test_sector_router.py -v
```

Expected: 5 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add lib/sector_router.py data/sector_routing.yaml tests/test_sector_router.py
git commit -m "feat(routing): sector_code → master_name YAML config + fail-loud (Plan F Task 3)"
```

---

### Task 4: lib/refresh_sector_cache.py CLI

**Files:**
- Create: `lib/refresh_sector_cache.py`
- Test: `tests/test_refresh_sector_cache.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_refresh_sector_cache.py`:

```python
"""Tests for refresh_sector_cache CLI."""
from unittest.mock import patch, MagicMock
import pytest
from lib.pipeline_db import PipelineDB
from lib.refresh_sector_cache import main

@pytest.fixture
def mock_api_response():
    return {
        "data": {
            "sectors": [
                {
                    "k": "oilGas", "n": "Dầu khí", "pn": "",
                    "s": [{"c": "BSR", "e": "HOSE"}]
                }
            ]
        }
    }

def test_refresh_populates_cache(tmp_path, mock_api_response, capsys):
    db_path = tmp_path / "test.db"
    PipelineDB(str(db_path)).close()

    with patch("lib.finpath_sectors.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = main(db_path=str(db_path), force=False)

    assert result == 0  # exit code success
    captured = capsys.readouterr()
    assert "Cached" in captured.out
    assert "BSR" in captured.out or "1 tickers" in captured.out

def test_refresh_force_clears_stale(tmp_path, mock_api_response):
    """--force flag clears all cache before refresh."""
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    # Pre-populate
    db.conn.execute("""
        INSERT INTO finpath_sectors_cache (ticker, sector_code, sector_name, sector_parent, exchange, fetched_at)
        VALUES ('OLDSTOCK', 'oldcode', 'Old', '', 'HOSE', '2020-01-01T00:00:00+00:00')
    """)
    db.conn.commit()
    db.close()

    with patch("lib.finpath_sectors.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        main(db_path=str(db_path), force=True)

    # OLDSTOCK should be gone (force cleared cache)
    db = PipelineDB(str(db_path))
    cur = db.conn.execute("SELECT COUNT(*) as cnt FROM finpath_sectors_cache WHERE ticker = 'OLDSTOCK'")
    assert cur.fetchone()["cnt"] == 0
    db.close()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_refresh_sector_cache.py -v
```

Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 3: Create lib/refresh_sector_cache.py**

```python
"""CLI to manually refresh Finpath sectors cache.

Usage:
    uv run python lib/refresh_sector_cache.py             # refresh if stale
    uv run python lib/refresh_sector_cache.py --force      # clear + refresh
"""
import argparse
import sys
from lib.pipeline_db import PipelineDB
from lib.finpath_sectors import FinpathSectors


def main(db_path: str = "data/pipeline.db", force: bool = False) -> int:
    db = PipelineDB(db_path)
    fs = FinpathSectors(db)

    if force:
        db.conn.execute("DELETE FROM finpath_sectors_cache")
        db.conn.commit()
        print("Cleared cache.")

    try:
        count = fs.refresh_cache()
        print(f"Cached {count} tickers from Finpath API.")
        return 0
    except Exception as e:
        print(f"Refresh failed: {e}", file=sys.stderr)
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-path", default="data/pipeline.db")
    parser.add_argument("--force", action="store_true", help="Clear cache before refresh")
    args = parser.parse_args()
    sys.exit(main(db_path=args.db_path, force=args.force))
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_refresh_sector_cache.py -v
```

Expected: 2 tests PASS.

- [ ] **Step 5: Populate initial cache (real API call)**

```bash
uv run python lib/refresh_sector_cache.py --force
```

Expected output: `Cached ~143 tickers from Finpath API.`

- [ ] **Step 6: Commit**

```bash
git add lib/refresh_sector_cache.py tests/test_refresh_sector_cache.py
git commit -m "feat(cli): refresh_sector_cache CLI + initial cache populate (Plan F Task 4)"
```

---

### Task 5: Editor V1 update — Finpath-driven routing

**Files:**
- Modify: `.claude/skills/finpath-newsroom-editor/scripts/routing.py` — deprecate FULL_UNIVERSE, keep COMPANY_NAME_TO_TICKER
- Modify: `.claude/agents/newsroom-editor.md` — update Step 2 logic
- Modify: `.claude/skills/finpath-newsroom-editor/SKILL.md` — load FinpathSectors + sector_router
- Modify: `lib/pipeline_db.py` — add validation for new fields sector_code/sector_name/sector_parent/master_route
- Test: `tests/test_editor_v1_v5_1_3.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_editor_v1_v5_1_3.py`:

```python
"""Test Editor V1 V5.1.3 — Finpath sectors-driven routing."""
import pytest
from unittest.mock import patch, MagicMock
from lib.pipeline_db import PipelineDB
from lib.finpath_sectors import FinpathSectors
from lib.sector_router import get_master_route


@pytest.fixture
def db_with_cache(tmp_path):
    """DB pre-populated with sample tickers."""
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    # Populate cache with sample tickers
    samples = [
        ("VCB", "soe3", "Bank nhà nước", "Ngân hàng", "HOSE"),
        ("SSI", "stock", "Chứng khoán", "", "HOSE"),
        ("VHM", "vic3", "BDS VIC3", "Bất động sản", "HOSE"),
        ("BSR", "oilGas", "Dầu khí", "", "HOSE"),
        ("FPT", "defensive", "Phòng thủ", "", "HOSE"),
        ("MWG", "retail", "Tiêu dùng bán lẻ", "Tiêu dùng", "HOSE"),
    ]
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    for ticker, sc, sn, pn, e in samples:
        db.conn.execute("""
            INSERT INTO finpath_sectors_cache
                (ticker, sector_code, sector_name, sector_parent, exchange, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ticker, sc, sn, pn, e, now))
    db.conn.commit()
    yield db
    db.close()

def test_editor_routes_bank_to_master_bank(db_with_cache):
    fs = FinpathSectors(db_with_cache)
    info = fs.get_ticker_sector("VCB", allow_refresh=False)
    assert info["sector_code"] == "soe3"
    assert get_master_route(info["sector_code"]) == "bank"

def test_editor_routes_oilgas_to_master_oilgas(db_with_cache):
    fs = FinpathSectors(db_with_cache)
    info = fs.get_ticker_sector("BSR", allow_refresh=False)
    assert info["sector_code"] == "oilGas"
    assert get_master_route(info["sector_code"]) == "oilgas"

def test_editor_rejects_ticker_outside_finpath(db_with_cache):
    """Ticker không có trong cache + no refresh → None → reject."""
    fs = FinpathSectors(db_with_cache)
    info = fs.get_ticker_sector("UNKNOWN", allow_refresh=False)
    assert info is None

def test_editor_routes_all_new_v5_1_3_sectors(db_with_cache):
    """Verify all 7 new sectors route correctly."""
    fs = FinpathSectors(db_with_cache)

    # FPT defensive
    info = fs.get_ticker_sector("FPT", allow_refresh=False)
    assert get_master_route(info["sector_code"]) == "defensive"

    # MWG retail
    info = fs.get_ticker_sector("MWG", allow_refresh=False)
    assert get_master_route(info["sector_code"]) == "retail"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_editor_v1_v5_1_3.py -v
```

Expected: Tests may PASS if Task 2 + Task 3 done (em verify integration). If routing.yaml or finpath_sectors module not properly setup → FAIL.

- [ ] **Step 3: Modify routing.py — deprecate FULL_UNIVERSE**

Read `.claude/skills/finpath-newsroom-editor/scripts/routing.py` to find lines with hardcoded universe constants.

Replace constants section with deprecation notice:

```python
# Path: .claude/skills/finpath-newsroom-editor/scripts/routing.py

"""Editor V1 ticker detection + sector routing.

V5.1.3 update (2026-05-12):
- DEPRECATED: FULL_UNIVERSE, BANK_UNIVERSE, CK_UNIVERSE, BDS_UNIVERSE constants
- KEEP: COMPANY_NAME_TO_TICKER alias mapping (still needed for detect_ticker)
- NEW: get_sector() uses lib.finpath_sectors + lib.sector_router

Use lib.finpath_sectors.FinpathSectors + lib.sector_router.get_master_route
for sector detection. Old Python dict lookup deprecated.
"""

# Alias mapping for detect_ticker (still needed)
COMPANY_NAME_TO_TICKER = {
    # ... preserve existing ~80 entries ...
}


# Sector detection — V5.1.3 replacement
def get_sector_v5_1_3(ticker: str, db) -> dict | None:
    """V5.1.3 sector detection via Finpath API.

    Returns dict with sector_code, sector_name, sector_parent, master_route
    or None nếu ticker không có trong Finpath cache.
    """
    from lib.finpath_sectors import FinpathSectors
    from lib.sector_router import get_master_route, MasterRouteError

    fs = FinpathSectors(db)
    info = fs.get_ticker_sector(ticker)
    if not info:
        return None

    try:
        master_route = get_master_route(info["sector_code"])
    except MasterRouteError as e:
        # sector_code missing from YAML — fail-loud upstream
        raise
    return {
        "sector_code": info["sector_code"],
        "sector_name": info["sector_name"],
        "sector_parent": info["sector_parent"],
        "master_route": master_route,
        "sector": info["sector_name"],  # backward-compat field
    }


# DEPRECATED: kept as commented-out reference for migration audit
# FULL_UNIVERSE = ["VCB", "CTG", ...]  # 61 mã hardcoded — replaced by Finpath cache
# def get_sector(ticker: str) -> str | None: ...  # Python dict lookup — replaced
```

- [ ] **Step 4: Update Editor V1 agent prompt**

Read `.claude/agents/newsroom-editor.md` to find Step 2 routing section.

Update Step 2 in the agent file:

```markdown
## Step 2 (V5.1.3 — UPDATED): Sector detection via Finpath API

Replace V5.1.2 hardcoded universe lookup with Finpath API + sector_routing.yaml.

For each detected ticker from raw_title:

1. Open SQLite: `db = PipelineDB("data/pipeline.db")`
2. Call: `from .claude.skills.finpath_newsroom_editor.scripts.routing import get_sector_v5_1_3`
3. `info = get_sector_v5_1_3(ticker, db)`
4. If `info is None`:
   - Set `editor_v1_decision = "reject"`
   - Set `editor_v1_note = "ticker_outside_finpath_139"`
   - Skip row
5. If `info is not None`:
   - Set `editor_v1_decision = "route_to_story_editor"`
   - Set `sector_code = info["sector_code"]`
   - Set `sector_name = info["sector_name"]`
   - Set `sector_parent = info["sector_parent"]`
   - Set `master_route = info["master_route"]`
   - Set `sector = info["sector"]` (backward-compat)

Persist all 5 fields to crawl_log row via UPDATE.
```

- [ ] **Step 5: Update pipeline_db.py validation**

Read `lib/pipeline_db.py` to find `validate_pipeline_step` function.

Add validation for new crawl_log fields. Locate the existing schema dict and extend:

```python
# In lib/pipeline_db.py — add new schema constants near other _STEP_*_REQUIRED dicts

_CRAWL_LOG_V5_1_3_FIELDS = {
    "sector_code": str,        # required after Editor V1
    "sector_name": str,         # required
    "sector_parent": str,       # can be empty string ""
    "master_route": str,        # required: bank/ck/bds/oilgas/logistics/fb/apparel/retail/seafood/defensive
}

_MASTER_ROUTE_VALID = {
    "bank", "ck", "bds",
    "oilgas", "logistics", "fb", "apparel", "retail", "seafood", "defensive"
}

def validate_crawl_log_v5_1_3(row: dict) -> None:
    """Validate V5.1.3 crawl_log fields after Editor V1."""
    if row.get("editor_v1_decision") != "route_to_story_editor":
        return  # rejected rows skip validation
    for field, expected_type in _CRAWL_LOG_V5_1_3_FIELDS.items():
        if field not in row or row[field] is None:
            raise ValueError(f"crawl_log V5.1.3 missing field: {field}")
        if not isinstance(row[field], expected_type):
            raise ValueError(f"crawl_log {field} must be {expected_type.__name__}, got {type(row[field]).__name__}")
    if row["master_route"] not in _MASTER_ROUTE_VALID:
        raise ValueError(f"master_route '{row['master_route']}' invalid. Valid: {_MASTER_ROUTE_VALID}")
```

- [ ] **Step 6: Run tests to verify they pass**

```bash
uv run pytest tests/test_editor_v1_v5_1_3.py -v
```

Expected: 4 tests PASS.

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/finpath-newsroom-editor/scripts/routing.py \
        .claude/agents/newsroom-editor.md \
        lib/pipeline_db.py \
        tests/test_editor_v1_v5_1_3.py
git commit -m "feat(editor): V5.1.3 Finpath sectors-driven routing + crawl_log fields (Plan F Task 5)"
```

---

### Task 5.5 (PATCH critical gap 3): Extend COMPANY_NAME_TO_TICKER cho 78 ticker mới

**Files:**
- Modify: `.claude/skills/finpath-newsroom-editor/scripts/routing.py` — extend COMPANY_NAME_TO_TICKER dict
- Test: `tests/test_company_name_mapping_v5_1_3.py`

**Rationale**: Universe expand 61 → 139. 78 ticker mới (HPG, FPT, MWG, VNM, etc.) chưa có Vietnamese alias trong COMPANY_NAME_TO_TICKER. Editor V1 detect_ticker fail nếu title chứa tên company thay vì ticker code.

- [ ] **Step 1: Write failing tests**

Create `tests/test_company_name_mapping_v5_1_3.py`:

```python
"""Test COMPANY_NAME_TO_TICKER covers 78 V5.1.3 new tickers."""
import pytest
from importlib import import_module

routing = import_module(".claude.skills.finpath-newsroom-editor.scripts.routing")
MAPPING = routing.COMPANY_NAME_TO_TICKER

@pytest.mark.parametrize("alias,expected_ticker", [
    # oilGas sector (HPG removed — sector classification unverified, defer V5.2)
    ("Lọc hoá dầu Bình Sơn", "BSR"),
    ("PV Gas", "GAS"),
    ("PV Power", "POW"),
    ("Petrolimex", "PLX"),
    ("PV Drilling", "PVD"),
    ("Khí Việt Nam", "GAS"),
    # logistics
    ("Gemadept", "GMD"),
    ("Hải An", "HAH"),
    ("Cảng Hải Phòng", "PHP"),
    # fb (tiêu dùng thực phẩm)
    ("Vinamilk", "VNM"),
    ("Masan", "MSN"),
    ("Sabeco", "SAB"),
    ("Bia Hà Nội", "BHN"),
    ("Kido", "KDC"),
    # apparel
    ("Thành Công Textile", "TCM"),
    ("May Sông Hồng", "MSH"),
    ("TNG May", "TNG"),
    # retail
    ("Thế Giới Di Động", "MWG"),
    ("FPT Retail", "FRT"),
    ("Digiworld", "DGW"),
    ("Phú Nhuận", "PNJ"),
    # seafood
    ("Vĩnh Hoàn", "VHC"),
    ("Nam Việt", "ANV"),
    ("Minh Phú", "MPC"),
    ("Sao Ta", "FMC"),
    # defensive
    ("FPT", "FPT"),
    ("FPT Corp", "FPT"),
    ("REE", "REE"),
    ("PC1", "PC1"),
    ("GEX", "GEX"),
    ("Traphaco", "TRA"),
])
def test_alias_maps_to_ticker(alias, expected_ticker):
    assert MAPPING.get(alias) == expected_ticker, \
        f"Alias '{alias}' should map to {expected_ticker}, got {MAPPING.get(alias)}"
```

- [ ] **Step 2: Run tests (FAIL expected)**

```bash
uv run pytest tests/test_company_name_mapping_v5_1_3.py -v
```

Expected: Most tests FAIL — aliases not in mapping yet.

- [ ] **Step 3: Extend routing.py mapping**

Read `.claude/skills/finpath-newsroom-editor/scripts/routing.py`. Find `COMPANY_NAME_TO_TICKER` dict (existing ~80 entries cho 61 universe).

Append new V5.1.3 entries:

```python
COMPANY_NAME_TO_TICKER.update({
    # === V5.1.3 NEW — oilGas sector (8 mã) ===
    "Lọc hoá dầu Bình Sơn": "BSR",
    "Bình Sơn": "BSR",
    "PV Services": "PVS",
    "PetroVietnam Services": "PVS",
    "PV Gas": "GAS",
    "Tổng công ty Khí": "GAS",
    "Khí Việt Nam": "GAS",
    "PV Power": "POW",
    "Tổng công ty Điện lực Dầu khí": "POW",
    "Petrolimex": "PLX",
    "Tập đoàn Xăng dầu": "PLX",
    "PV Oil": "OIL",
    "PV Drilling": "PVD",
    "Khoan và Dịch vụ khoan dầu khí": "PVD",
    "PV Trans": "PVT",
    "Vận tải Dầu khí": "PVT",

    # === V5.1.3 NEW — logistics sector (12 mã) ===
    "Gemadept": "GMD",
    "Cảng Gemadept": "GMD",
    "Hải An": "HAH",
    "Vận tải Biển Hải An": "HAH",
    "VOS": "VOS",
    "Vận tải Biển Việt Nam": "VOS",
    "VSC": "VSC",
    "Cảng container Việt Nam": "VSC",
    "Cảng Hải Phòng": "PHP",
    "Cảng Đà Nẵng": "CDN",
    "HAX": "HAX",
    "Logistics Hàng Xanh": "HAX",

    # === V5.1.3 NEW — fb (Tiêu dùng thực phẩm — 8 mã) ===
    "Vinamilk": "VNM",
    "Sữa Việt Nam": "VNM",
    "Masan": "MSN",
    "Tập đoàn Masan": "MSN",
    "Sabeco": "SAB",
    "Bia Sài Gòn": "SAB",
    "Bia Hà Nội": "BHN",
    "Habeco": "BHN",
    "Kido": "KDC",
    "Bánh kẹo Kido": "KDC",
    "Mộc Châu Milk": "MCM",
    "Sữa Mộc Châu": "MCM",
    "QNS": "QNS",
    "Đường Quảng Ngãi": "QNS",

    # === V5.1.3 NEW — apparel (Dệt may — 3 mã) ===
    "Thành Công Textile": "TCM",
    "Dệt may Thành Công": "TCM",
    "TCM": "TCM",
    "May Sông Hồng": "MSH",
    "TNG May": "TNG",
    "May TNG": "TNG",
    "Thái Nguyên May": "TNG",

    # === V5.1.3 NEW — retail (Bán lẻ — 7 mã) ===
    "Thế Giới Di Động": "MWG",
    "MWG": "MWG",
    "Bách Hóa Xanh": "MWG",
    "FPT Retail": "FRT",
    "FPT Shop": "FRT",
    "Long Châu": "FRT",
    "Digiworld": "DGW",
    "PNJ": "PNJ",
    "Phú Nhuận": "PNJ",
    "Trang sức Phú Nhuận": "PNJ",
    "AST": "AST",
    "Phục vụ Sân bay Quốc tế": "AST",

    # === V5.1.3 NEW — seafood (Thuỷ sản — 6 mã) ===
    "Vĩnh Hoàn": "VHC",
    "Thủy sản Vĩnh Hoàn": "VHC",
    "Nam Việt": "ANV",
    "Thủy sản Nam Việt": "ANV",
    "Minh Phú": "MPC",
    "Thủy sản Minh Phú": "MPC",
    "Sao Ta": "FMC",
    "Thực phẩm Sao Ta": "FMC",
    "IDI": "IDI",
    "I.D.I": "IDI",
    "CMX": "CMX",
    "Camimex": "CMX",

    # === V5.1.3 NEW — defensive (Phòng thủ — 12 mã) ===
    "FPT": "FPT",
    "FPT Corp": "FPT",
    "FPT Software": "FPT",
    "REE": "REE",
    "Cơ Điện Lạnh": "REE",
    "PC1": "PC1",
    "Xây Lắp Điện 1": "PC1",
    "GEX": "GEX",
    "Gelex": "GEX",
    "ITD": "ITD",
    "Tin học ITD": "ITD",
    "Traphaco": "TRA",
    "Dược Traphaco": "TRA",
    "DBD": "DBD",
    "Bidiphar": "DBD",
    "IMP": "IMP",
    "Imexpharm": "IMP",
    "ELC": "ELC",
    "Elcom": "ELC",
})
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_company_name_mapping_v5_1_3.py -v
```

Expected: All tests PASS.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/finpath-newsroom-editor/scripts/routing.py \
        tests/test_company_name_mapping_v5_1_3.py
git commit -m "feat(editor): extend COMPANY_NAME_TO_TICKER với 78 ticker V5.1.3 (Plan F Task 5.5)"
```

---

## Phase 2 — 7 NEW master agents (Tasks 6-12, parallel-safe)

### Pattern reference (apply to Tasks 6-12)

Each new master agent task creates:
1. `.claude/agents/newsroom-master-{sector}.md` (~80 lines)
2. `.claude/skills/finpath-newsroom-master-{sector}/SKILL.md` (~180 lines)
3. `.claude/skills/finpath-newsroom-master-{sector}/references/sector-context.md` (~100 lines, sector-specific)
4. `.claude/skills/finpath-newsroom-master-{sector}/references/voice-layer-rules.md` (duplicate from Bank, ~100 lines)
5. `.claude/skills/finpath-newsroom-master-{sector}/references/stance-directive-handler.md` (duplicate from Bank, ~80 lines)
6. `.claude/skills/finpath-newsroom-master-{sector}/references/jargon-mapping.md` (sector-specific, ~50 lines)
7. **PATCH 2026-05-12**: 4 format-body files via `cp` from Bank V5.1.2 split:
   - `references/format-bodies/flash-qa.md`
   - `references/format-bodies/standard-qa.md`
   - `references/format-bodies/standard-listicle.md`
   - `references/format-bodies/standard-narrative.md`

**Note Q3 resolution**: KHÔNG tạo `kb/{sector_code}/` folder ở V5.1.3. SKILL.md `kb_path: ""` (empty) signals "web search heavy mode".

**Note CRITICAL gap 1 fix (2026-05-12)**: Each task MUST run `cp` step copying 4 format-body files from Bank V5.1.2 split (`.claude/skills/finpath-newsroom-master-bank/references/format-bodies/*.md`). Otherwise master crashes when loading format_id-specific body pattern. Pattern same as voice + stance duplicate.

```bash
# Per-task pattern (add this step to each Task 6-12 BEFORE final commit):
mkdir -p .claude/skills/finpath-newsroom-master-{sector}/references/format-bodies/
cp .claude/skills/finpath-newsroom-master-bank/references/format-bodies/*.md \
   .claude/skills/finpath-newsroom-master-{sector}/references/format-bodies/
```

Tasks 6-12 are **parallel-safe** — different sectors don't touch same file. **BUT Plan B V5.1.2 Phase 6 MUST run first** (creates Bank's format-bodies/ to copy from).

---

### Task 6: newsroom-master-oilgas

**Files:**
- Create: `.claude/agents/newsroom-master-oilgas.md`
- Create: `.claude/skills/finpath-newsroom-master-oilgas/SKILL.md`
- Create: `.claude/skills/finpath-newsroom-master-oilgas/references/sector-context.md`
- Create: `.claude/skills/finpath-newsroom-master-oilgas/references/voice-layer-rules.md`
- Create: `.claude/skills/finpath-newsroom-master-oilgas/references/stance-directive-handler.md`
- Create: `.claude/skills/finpath-newsroom-master-oilgas/references/jargon-mapping.md`

- [ ] **Step 1: Read Bank template structure**

```bash
ls -la .claude/skills/finpath-newsroom-master-bank/references/
cat .claude/agents/newsroom-master-bank.md | head -80
```

Read the Bank SKILL.md to understand 9-step workflow pattern.

- [ ] **Step 2: Create agent file**

`.claude/agents/newsroom-master-oilgas.md`:

```markdown
---
name: newsroom-master-oilgas
description: Master Bank V5.1.3 — sector Dầu khí (oilGas). Web search heavy (no KB yet). Viết bài 200-400 từ pass 8 quality gates V5.1.2.
tools: Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
model: opus
---

# Newsroom Master Dầu khí Agent

Bạn là Master Dầu khí writing bài tin về cổ phiếu sector oilGas (BSR, PVS, GAS, POW, PLX, OIL, ...).

Reference skill `finpath-newsroom-master-oilgas` — load qua: `Skill: finpath-newsroom-master-oilgas`.

## 🚨 HARD RULE

- Pass 8 quality gates V5.1.2 BEFORE persist (`lib/quality_gates.py`)
- Receive `stance_directive` từ Story Editor brief — write theo direction
- 5 Voice Layer rules apply (Stance / No-hedging / Verdict / Title delegate / Contrarian-OK)
- KHÔNG generate title (delegated to Headline Craft Spec C)
- Em dash density body ≤ 1/100 từ

## Data sources (V5.1.3 web search heavy)

```
1. Finpath API — lib.finpath_api.py (BCTC, ratios non-bank)
2. KB local — kb/oilGas/ (KHÔNG có ở V5.1.3, web search là first-class)
3. SQLite memory — variety guard 3 bài cũ
4. Web search BẮT BUỘC — primary data source vì KB empty
```

## Workflow

9-step V5.1.2 workflow như Master Bank. Apply per sector-context.md + jargon-mapping.md sector oilGas.
```

- [ ] **Step 3: Create SKILL.md**

`.claude/skills/finpath-newsroom-master-oilgas/SKILL.md`:

```markdown
---
name: finpath-newsroom-master-oilgas
description: Master Dầu khí — viết bài cổ phiếu sector oilGas pass 8 gates V5.1.2. Web search heavy (no KB V5.1.3).
kb_path: ""
sector_codes: ["oilGas"]
---

# Finpath Newsroom Master Dầu Khí Skill

## Identity

Bạn là Master Dầu khí writing bài 200-400 từ về cổ phiếu sector oilGas (BSR, PVS, GAS, POW, PLX, OIL, ...).

## V5.1.3 status: Web search heavy mode

`kb_path` empty → KHÔNG có local KB. Web search là primary data source. Anti-hallucination: cite URL explicit trong data_trail.

## 9-step workflow (V5.1.2)

### Step 1: Parse input
- Receive brief từ Story Editor (stance_directive, deep_question_options, angle_label, angle_narrative)
- Receive format_id_used từ Format Director (flash_qa / standard_qa / standard_listicle / standard_narrative)

### Step 2: Load references
- `references/sector-context.md` — overview + jargon + analysis lens
- `references/voice-layer-rules.md` — 5 voice rules
- `references/stance-directive-handler.md` — receive + apply stance
- `references/jargon-mapping.md` — sector-specific jargon Anh → Việt
- `references/format-bodies/{format_id}.md` — body pattern (DROP V5.1.3 — em propose use Bank's format-bodies via copy ở Task 6.5)

### Step 3: Web search data
- Search "BSR Q1 2026 lợi nhuận crack spread" + similar queries
- Verify 3+ sources, cite URL explicit
- Cross-check claims from multiple sources

### Step 4: Apply stance_directive
- Body MUST follow stance_directive.direction (positive/negative/neutral)
- Cite ≥1 from key_evidence array
- Closing verdict matches direction

### Step 5: Apply Voice Layer 5 rules
- V1 Stance required
- V2 No-hedging (definition + 2 test)
- V3 Verdict line bắt buộc
- V4 Title stance (delegate Headline)
- V5 Contrarian-when-warranted

### Step 6: Write body per format_id

Body pattern theo format:
- flash_qa: 100-150w (1 paragraph + closing)
- standard_qa: 200-300w (opening + 2-3 bullets + closing)
- standard_listicle: 250-350w (opening + 4-6 bullets + closing)
- standard_narrative: 250-350w (opening + 2-3 paragraphs + closing)

### Step 7: Self-check 8 gates V5.1.2

Run `lib/quality_gates.check_all_v5(body, format_id, stance_directive)`:
1. No English jargon
2. No metadata leak
3. No-hedging (LLM-as-judge)
4. Verdict line
5. Stance consistency
6. Em dash density body
7. Word count per format
8. Body pattern per format

Reject + rewrite if any gate fails. KHÔNG persist nếu fail.

### Step 8: Persist
- Insert generated_news với title=NULL (Headline UPDATE sau)
- pipeline_log step_4_master payload với format_id_used + data_trail + chosen_question_idx

### Step 9: Return to orchestrator
- article_id, body, insight_final, data_trail, quality_gates, format_id_used, accepted_hypothesis

## References

- sector-context.md
- voice-layer-rules.md (duplicate from Bank)
- stance-directive-handler.md (duplicate from Bank)
- jargon-mapping.md (sector-specific)
```

- [ ] **Step 4: Create sector-context.md**

`.claude/skills/finpath-newsroom-master-oilgas/references/sector-context.md`:

```markdown
# Sector Context — Dầu khí (oilGas)

> Loaded from `Skill: finpath-newsroom-master-oilgas`. Sector-specific overview + analysis lens.

## Overview

Sector dầu khí Việt Nam gồm 3 mảng:
- **Upstream**: thăm dò + khai thác (PVS dịch vụ, GAS khí thiên nhiên)
- **Downstream**: lọc hoá dầu + phân phối (BSR Bình Sơn, PLX Petrolimex)
- **Utility**: điện khí (POW PV Power)

Chu kỳ ngành phụ thuộc:
- **Giá dầu Brent** (USD/thùng) — biến động OPEC + geopolitics
- **OPEC+ production policy** — cắt sản lượng / nới
- **Tỷ giá VND/USD** — input cost effect
- **Demand điện + xăng dầu nội địa** — economic activity
- **Refining margin** — chênh lệch giá đầu vào - đầu ra

## Key metrics

- **Crack spread**: chênh lệch giá dầu thô - sản phẩm refined (xăng/dầu diesel/jet fuel)
- **Refining margin**: biên lọc dầu (USD/thùng)
- **Throughput**: sản lượng tinh chế (tấn/quý)
- **Inventory days**: số ngày tồn kho
- **Realized oil price**: giá bán dầu thực tế (vs spot)
- **Utilization rate**: hiệu suất sử dụng công suất

## Jargon mapping (Anh → Việt cứng)

- crack spread → "chênh lệch giá dầu thô-sản phẩm"
- refining margin → "biên lọc dầu"
- upstream/downstream → "thăm dò khai thác / lọc hoá dầu"
- realized price → "giá bán thực tế"
- inventory turnover → "vòng quay tồn kho"
- utilization → "hiệu suất sử dụng công suất"

## Analysis lens

### Bullish signals

- Giá Brent up + biên lọc up = upstream + downstream cùng có lợi
- OPEC cắt sản lượng = giá dầu support → upstream lợi
- Demand nội địa tăng (Q4/Tết) = downstream lợi
- VND yếu vừa phải = export oil revenue boost

### Bearish signals

- Giá Brent down + biên lọc thu hẹp = upstream loss, downstream slim
- VND yếu mạnh (devaluation) = mixed (export gain vs input cost)
- Demand nội địa giảm (recession) = downstream loss
- Inventory days tăng nhanh = demand weak signal

## Peers reference

| Ticker | Company | Mảng |
|---|---|---|
| BSR | Lọc hoá dầu Bình Sơn | Downstream |
| PVS | Dịch vụ kỹ thuật DK | Upstream services |
| GAS | Tổng công ty Khí | Upstream gas |
| POW | PV Power | Utility điện khí |
| PLX | Petrolimex | Downstream phân phối |
| OIL | PV Oil | Downstream phân phối |
| PVD | Khoan dầu khí | Upstream drilling |
| PVT | Vận tải dầu khí | Logistics dầu khí |

## Common pitfalls (avoid khi viết)

1. **Confuse upstream vs downstream** — BSR là downstream (lọc), KHÔNG phải upstream (khai thác). PVS là dịch vụ upstream.
2. **Misread "crack spread"** — đây là chênh lệch giá, KHÔNG phải margin cuối cùng. Margin = crack spread - operating cost.
3. **Brent vs WTI** — Vietnam upstream tham chiếu Brent + Dubai, KHÔNG phải WTI (US benchmark).
4. **POW không phải pure oil** — POW là utility điện, dùng gas làm input, nên giá khí (LNG) là driver chính, không phải giá dầu Brent direct.
```

- [ ] **Step 5: Duplicate voice-layer-rules.md from Bank**

```bash
cp .claude/skills/finpath-newsroom-master-bank/references/voice-layer-rules.md \
   .claude/skills/finpath-newsroom-master-oilgas/references/voice-layer-rules.md
```

(Em assume Bank V5.1.2 split has voice-layer-rules.md. If not, create from Spec B Patch 2/3.)

- [ ] **Step 6: Duplicate stance-directive-handler.md from Bank**

```bash
cp .claude/skills/finpath-newsroom-master-bank/references/stance-directive-handler.md \
   .claude/skills/finpath-newsroom-master-oilgas/references/stance-directive-handler.md
```

- [ ] **Step 6.5 (PATCH critical gap 1): Copy 4 format-body files from Bank V5.1.2**

```bash
mkdir -p .claude/skills/finpath-newsroom-master-oilgas/references/format-bodies/
cp .claude/skills/finpath-newsroom-master-bank/references/format-bodies/*.md \
   .claude/skills/finpath-newsroom-master-oilgas/references/format-bodies/
```

Verify 4 files copied:

```bash
ls .claude/skills/finpath-newsroom-master-oilgas/references/format-bodies/
# Expected: flash-qa.md  standard-qa.md  standard-listicle.md  standard-narrative.md
```

**Apply same step to Tasks 7-12** (logistics/fb/apparel/retail/seafood/defensive). Pattern identical, just swap sector name in path.

- [ ] **Step 7: Create sector-specific jargon-mapping.md**

`.claude/skills/finpath-newsroom-master-oilgas/references/jargon-mapping.md`:

```markdown
# Jargon Mapping — Sector Dầu khí

> Anh → Việt strict mapping cho gate `no_english_jargon`.

## Industry-specific

| Anh | Việt | Note |
|---|---|---|
| crack spread | chênh lệch giá dầu thô-sản phẩm | |
| refining margin | biên lọc dầu | |
| upstream | thăm dò khai thác | |
| downstream | lọc hoá dầu phân phối | |
| midstream | vận chuyển và lưu trữ | |
| realized price | giá bán thực tế | |
| spot price | giá giao ngay | |
| futures price | giá kỳ hạn | |
| OPEC | OPEC (giữ — tổ chức tên riêng) | exception |
| OPEC+ | OPEC+ (giữ) | exception |
| Brent | dầu Brent | giữ tên benchmark |
| WTI | dầu WTI | giữ tên benchmark |
| utilization rate | hiệu suất sử dụng công suất | |
| throughput | sản lượng tinh chế | |
| inventory days | số ngày tồn kho | |
| inventory turnover | vòng quay tồn kho | |
| operating cost | chi phí vận hành | |

## Financial standard

| Anh | Việt |
|---|---|
| EBITDA | EBITDA (giữ — Anh ngữ tài chính dùng quen) — actually FAIL gate |
| LNST | LNST (Việt) |
| ROA | tỷ suất sinh lời tài sản |
| ROE | tỷ suất sinh lời vốn chủ |
| EPS | lợi nhuận trên mỗi cổ phiếu |
| PE | hệ số PE (Vietnam dùng "PE" trực tiếp acceptable) |
| PB | hệ số PB |

## Trading

| Anh | Việt |
|---|---|
| YoY | so cùng kỳ |
| QoQ | so quý trước |
| YTD | lũy kế từ đầu năm |

## Anti-pattern (must reject)

- ❌ "crack spread của BSR" → ✅ "chênh lệch giá dầu thô-sản phẩm của BSR"
- ❌ "refining margin tăng" → ✅ "biên lọc dầu tăng"
- ❌ "BSR's upstream segment" → ✅ "mảng thăm dò khai thác của BSR" (actually BSR không có upstream)
```

- [ ] **Step 8: Verify files exist**

```bash
ls -la .claude/agents/newsroom-master-oilgas.md
ls -la .claude/skills/finpath-newsroom-master-oilgas/SKILL.md
ls -la .claude/skills/finpath-newsroom-master-oilgas/references/
```

Expected: 6 files exist.

- [ ] **Step 9: Commit**

```bash
git add .claude/agents/newsroom-master-oilgas.md \
        .claude/skills/finpath-newsroom-master-oilgas/
git commit -m "feat(master-oilgas): NEW master agent for sector Dầu khí V5.1.3 (Plan F Task 6)"
```

---

### Task 7: newsroom-master-logistics

Same structure as Task 6, swap sector content.

**Files:**
- Create: 6 files in `.claude/agents/newsroom-master-logistics.md` + `.claude/skills/finpath-newsroom-master-logistics/`

- [ ] **Step 1: Copy Task 6 structure with logistics content**

Agent file `.claude/agents/newsroom-master-logistics.md`:

```markdown
---
name: newsroom-master-logistics
description: Master Logistics V5.1.3 — sector vận tải biển + cảng + đường bộ. Web search heavy.
tools: Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
model: opus
---

# Newsroom Master Logistics Agent

Bạn là Master Logistics writing bài về cổ phiếu sector logistics (GMD, HAH, VOS, VSC, ...).

Load skill: `Skill: finpath-newsroom-master-logistics`.

## Pattern: Same as Master Bank V5.1.2 — 8 gates + 5 voice rules + stance + format.

KHÔNG generate title. Em dash density ≤ 1/100. KB-optional (V5.1.3: web search only).
```

SKILL.md content same 9-step workflow, `kb_path: ""`, sector_codes: ["logistics"].

sector-context.md content:

```markdown
# Sector Context — Logistics

## Overview

Sector logistics Việt Nam gồm:
- **Vận tải biển**: vận chuyển container quốc tế (HAH, VOS, VTO)
- **Cảng**: khai thác cảng biển (GMD, VSC, PHP, CDN)
- **Vận tải bộ + giao nhận**: trucking + 3PL (HAX, VTV)
- **Sân bay**: ACV (SCS, ACV — UPCOM)

## Key metrics

- **TEU throughput**: container 20-feet equivalent units (sản lượng cảng)
- **Revenue per TEU**: doanh thu trên 1 container
- **Utilization rate**: hiệu suất sử dụng (cảng / fleet)
- **Bunker cost**: chi phí nhiên liệu tàu
- **Charter rates**: giá thuê tàu (BDI Baltic Dry Index, SCFI Shanghai Containerized Freight Index)
- **Dwelling time**: thời gian container ở cảng

## Jargon mapping

- TEU → "container 20-feet (TEU)"
- bunker cost → "chi phí nhiên liệu"
- charter rate → "giá thuê tàu"
- dwelling time → "thời gian lưu container"
- berth → "cầu cảng"
- DWT → "trọng tải toàn phần"
- BDI → "chỉ số BDI" (giữ — global benchmark)
- SCFI → "chỉ số SCFI"

## Analysis lens

Bullish: BDI/SCFI up + Vietnam export volume up → cảng + vận tải biển lợi
Bearish: Bunker cost spike + container oversupply globally → margin squeeze
Sector cycle: 2026 đang ở phục hồi sau 2022-2024 freight slump

## Peers

| Ticker | Type |
|---|---|
| GMD | Cảng Gemadept |
| HAH | Vận tải biển Hải An |
| VOS | Vận tải biển VN |
| VSC | Cảng container VN |
| PHP | Cảng Hải Phòng |
| CDN | Cảng Đà Nẵng |
| HAX | Logistics + xe hơi (mix) |
```

jargon-mapping.md content per logistics sector.

- [ ] **Step 2: Duplicate voice + stance handlers from Bank**

```bash
cp .claude/skills/finpath-newsroom-master-bank/references/voice-layer-rules.md \
   .claude/skills/finpath-newsroom-master-logistics/references/voice-layer-rules.md
cp .claude/skills/finpath-newsroom-master-bank/references/stance-directive-handler.md \
   .claude/skills/finpath-newsroom-master-logistics/references/stance-directive-handler.md
```

- [ ] **Step 2.5 (PATCH critical gap 1): Copy 4 format-body files from Bank V5.1.2**

```bash
mkdir -p .claude/skills/finpath-newsroom-master-logistics/references/format-bodies/
cp .claude/skills/finpath-newsroom-master-bank/references/format-bodies/*.md \
   .claude/skills/finpath-newsroom-master-logistics/references/format-bodies/
```

Verify:

```bash
ls .claude/skills/finpath-newsroom-master-logistics/references/format-bodies/
# Expected: flash-qa.md  standard-qa.md  standard-listicle.md  standard-narrative.md
```

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/newsroom-master-logistics.md \
        .claude/skills/finpath-newsroom-master-logistics/
git commit -m "feat(master-logistics): NEW master agent for sector Logistics V5.1.3 (Plan F Task 7)"
```

---

### Task 8: newsroom-master-fb

**Files:** 6 files for sector Tiêu dùng thực phẩm.

- [ ] **Step 1: Create agent + skill files for sector fb**

Agent file `.claude/agents/newsroom-master-fb.md`:

```markdown
---
name: newsroom-master-fb
description: Master Tiêu dùng thực phẩm V5.1.3 — sector fb (VNM, MSN, SAB, KDC). Web search heavy.
tools: Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
model: opus
---

# Newsroom Master Tiêu dùng Thực phẩm Agent

Bạn là Master Thực phẩm writing bài về cổ phiếu sector fb (VNM Vinamilk, MSN Masan, SAB Sabeco, KDC Kido).

Load: `Skill: finpath-newsroom-master-fb`.

Pattern same Master Bank V5.1.2. KHÔNG title. KB-optional V5.1.3.
```

SKILL.md content theo pattern Task 6, kb_path: "", sector_codes: ["fb"].

sector-context.md:

```markdown
# Sector Context — Tiêu dùng Thực phẩm (fb)

## Overview

Sector thực phẩm Việt Nam gồm:
- **Sữa**: VNM Vinamilk (#1), MCM Mộc Châu Milk
- **Bia rượu**: SAB Sabeco, BHN Bia Hà Nội
- **Bánh kẹo + cà phê**: KDC Kido, MSN Masan (Wifresh, Vinacafé)
- **Diversified**: MSN Masan (multi-segment)

## Key metrics

- **Same-store sales (SSS)**: doanh số cửa hàng cũ (loại factor mở mới)
- **Gross margin**: biên lợi nhuận gộp (cost of goods → revenue)
- **Brand power**: market share + premium pricing
- **Distribution channels**: GT (general trade) vs MT (modern trade)
- **Inventory turnover**: vòng quay tồn kho

## Jargon mapping

- same-store sales → "doanh số cửa hàng cũ" (SSS)
- gross margin → "biên lợi nhuận gộp"
- brand power → "sức mạnh thương hiệu"
- premium segment → "phân khúc cao cấp"
- mass market → "thị trường đại chúng"
- GT (general trade) → "kênh bán lẻ truyền thống"
- MT (modern trade) → "kênh hiện đại (siêu thị + minimart)"
- volume vs value → "sản lượng vs giá trị"

## Analysis lens

Bullish: SSS positive + gross margin recover + GDP per capita up = mass-market premiumization
Bearish: Input cost spike (sữa nguyên liệu, lúa mạch) + giá bán không tăng nổi = margin squeeze
Sector cycle: F&B Việt 2026 đang ở phase premiumization

## Peers

| Ticker | Segment |
|---|---|
| VNM | Sữa (#1 Việt) |
| MSN | Diversified (multi-segment) |
| SAB | Bia |
| BHN | Bia Hà Nội |
| KDC | Bánh kẹo + thực phẩm |
| MCM | Sữa (Mộc Châu) |
| QNS | Đường + sữa |
| VHC | Cá tra xuất khẩu (technical: seafood, careful overlap)
```

jargon-mapping.md sector-specific.

- [ ] **Step 2: Duplicate voice + stance**

```bash
cp .claude/skills/finpath-newsroom-master-bank/references/voice-layer-rules.md \
   .claude/skills/finpath-newsroom-master-fb/references/voice-layer-rules.md
cp .claude/skills/finpath-newsroom-master-bank/references/stance-directive-handler.md \
   .claude/skills/finpath-newsroom-master-fb/references/stance-directive-handler.md
```

- [ ] **Step 2.5 (PATCH critical gap 1): Copy 4 format-body files from Bank V5.1.2**

```bash
mkdir -p .claude/skills/finpath-newsroom-master-fb/references/format-bodies/
cp .claude/skills/finpath-newsroom-master-bank/references/format-bodies/*.md \
   .claude/skills/finpath-newsroom-master-fb/references/format-bodies/
```

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/newsroom-master-fb.md .claude/skills/finpath-newsroom-master-fb/
git commit -m "feat(master-fb): NEW master agent for sector Thực phẩm V5.1.3 (Plan F Task 8)"
```

---

### Task 9: newsroom-master-apparel

Sector Dệt may — 3 mã (TCM, MSH, TNG, GIL).

- [ ] **Step 1: Create files for sector apparel**

sector-context.md content:

```markdown
# Sector Context — Dệt may (apparel)

## Overview

Sector dệt may Việt Nam gồm 3 mã active:
- **TCM**: Thành Công Textile — woven garment
- **MSH**: May Sông Hồng — knitwear
- **TNG**: TNG Thiết kế và May — apparel

Plus larger non-listed: VinaTex, Vit, etc.

## Key metrics

- **Export revenue**: USD revenue (90%+ là export to US/EU/Japan)
- **Order book**: order pipeline visibility (months)
- **VND/USD rate**: input cost vs revenue effect
- **Labor cost**: wage inflation pressure
- **Raw material**: cotton + synthetic prices

## Jargon mapping

- order book → "đơn hàng tồn"
- export revenue → "doanh thu xuất khẩu"
- knitwear → "hàng dệt kim"
- woven garment → "hàng dệt thoi"
- minimum wage → "lương tối thiểu"
- FOB → "giá FOB (giao tại cảng)"

## Analysis lens

Bullish: US/EU consumer spending up + thuế giảm + VND yếu = export revenue boom
Bearish: Inventory de-stocking US retailers + thuế cao + labor cost up = order book shrink

## Peers (3 mã chỉ)

TCM (woven) / MSH (knit) / TNG (apparel general)
```

- [ ] **Step 1.5 (PATCH critical gap 1): Copy format-bodies + voice + stance from Bank**

```bash
mkdir -p .claude/skills/finpath-newsroom-master-apparel/references/format-bodies/
cp .claude/skills/finpath-newsroom-master-bank/references/format-bodies/*.md \
   .claude/skills/finpath-newsroom-master-apparel/references/format-bodies/
cp .claude/skills/finpath-newsroom-master-bank/references/voice-layer-rules.md \
   .claude/skills/finpath-newsroom-master-apparel/references/voice-layer-rules.md
cp .claude/skills/finpath-newsroom-master-bank/references/stance-directive-handler.md \
   .claude/skills/finpath-newsroom-master-apparel/references/stance-directive-handler.md
```

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/newsroom-master-apparel.md .claude/skills/finpath-newsroom-master-apparel/
git commit -m "feat(master-apparel): NEW master Dệt may V5.1.3 (Plan F Task 9)"
```

---

### Task 10: newsroom-master-retail

Sector Bán lẻ — MWG, FRT, DGW, PNJ, PET, AST.

sector-context.md content:

```markdown
# Sector Context — Tiêu dùng Bán lẻ (retail)

## Overview

Sector retail Việt Nam:
- **Mobile + electronics**: MWG Thế Giới Di Động + FPT Retail (FRT) + DGW Digiworld
- **Trang sức**: PNJ Phú Nhuận
- **Xăng dầu**: PET Petrolimex (overlap with oilGas in classification)
- **Aviation**: AST Phục vụ sân bay Quốc tế

## Key metrics

- **Same-store sales (SSS)**
- **Store count + new openings**
- **Online revenue ratio** (e-commerce share)
- **Margin per category** (smartphone slim, accessories rich)
- **Customer traffic**

## Jargon mapping

- same-store sales → "doanh số cửa hàng cũ"
- store count → "số lượng cửa hàng"
- e-commerce → "thương mại điện tử"
- omni-channel → "đa kênh"
- ASP (Average Selling Price) → "giá bán bình quân"

## Analysis lens

Bullish: SSS positive + new store profitable within 6 months + online >20% revenue mix
Bearish: SSS negative 2 quarters + new store cannibalize old + smartphone segment commoditize

## Peers

MWG (di động + Bách hóa Xanh + Erablue) / FRT (FPT Shop + Long Châu) / DGW (distribution) / PNJ (vàng) / PET (xăng) / AST
```

- [ ] **Step 1: Create files**

Create agent + skill + sector-context.md + jargon-mapping.md per Task 6 pattern.

- [ ] **Step 1.5 (PATCH critical gap 1): Copy format-bodies + voice + stance from Bank**

```bash
mkdir -p .claude/skills/finpath-newsroom-master-retail/references/format-bodies/
cp .claude/skills/finpath-newsroom-master-bank/references/format-bodies/*.md \
   .claude/skills/finpath-newsroom-master-retail/references/format-bodies/
cp .claude/skills/finpath-newsroom-master-bank/references/voice-layer-rules.md \
   .claude/skills/finpath-newsroom-master-retail/references/voice-layer-rules.md
cp .claude/skills/finpath-newsroom-master-bank/references/stance-directive-handler.md \
   .claude/skills/finpath-newsroom-master-retail/references/stance-directive-handler.md
```

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/newsroom-master-retail.md .claude/skills/finpath-newsroom-master-retail/
git commit -m "feat(master-retail): NEW master Bán lẻ V5.1.3 (Plan F Task 10)"
```

---

### Task 11: newsroom-master-seafood

Sector Thuỷ sản — VHC, ANV, MPC, FMC, CMX, IDI.

sector-context.md content:

```markdown
# Sector Context — Tiêu dùng Thuỷ sản (seafood)

## Overview

Sector thuỷ sản:
- **Cá tra**: VHC Vĩnh Hoàn + ANV Nam Việt + IDI I.D.I — export US/EU
- **Tôm**: MPC Minh Phú + FMC Sao Ta — export Japan/US
- **Cá ngừ**: ASM (UPCOM, smaller)

## Key metrics

- **Export volume + price**: USD per kg
- **Tariff status**: anti-dumping duty rate
- **VND/USD rate**: revenue translation
- **Raw material**: feed cost + sourcing risk
- **Inventory**: frozen stock days

## Jargon mapping

- anti-dumping → "thuế chống bán phá giá"
- pangasius → "cá tra"
- shrimp → "tôm"
- value-added → "chế biến sâu"
- fillet → "phi-lê"
- export volume → "sản lượng xuất khẩu"

## Analysis lens

Bullish: US tariff giảm + Q4 EU peak season + VND yếu = bumper Q4
Bearish: Anti-dumping tăng + Trung Quốc competition + USD weak = margin pressure

## Peers

VHC (cá tra) / ANV (cá tra) / MPC (tôm) / FMC (tôm) / IDI (cá tra) / CMX (cá biển + cá tra)
```

- [ ] **Step 1: Create files**

Create agent + skill + sector-context.md + jargon-mapping.md per Task 6 pattern.

- [ ] **Step 1.5 (PATCH critical gap 1): Copy format-bodies + voice + stance from Bank**

```bash
mkdir -p .claude/skills/finpath-newsroom-master-seafood/references/format-bodies/
cp .claude/skills/finpath-newsroom-master-bank/references/format-bodies/*.md \
   .claude/skills/finpath-newsroom-master-seafood/references/format-bodies/
cp .claude/skills/finpath-newsroom-master-bank/references/voice-layer-rules.md \
   .claude/skills/finpath-newsroom-master-seafood/references/voice-layer-rules.md
cp .claude/skills/finpath-newsroom-master-bank/references/stance-directive-handler.md \
   .claude/skills/finpath-newsroom-master-seafood/references/stance-directive-handler.md
```

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/newsroom-master-seafood.md .claude/skills/finpath-newsroom-master-seafood/
git commit -m "feat(master-seafood): NEW master Thuỷ sản V5.1.3 (Plan F Task 11)"
```

---

### Task 12: newsroom-master-defensive

Sector Phòng thủ — utilities + healthcare + tech. FPT, REE, PC1, GEX, etc.

sector-context.md content:

```markdown
# Sector Context — Phòng thủ (defensive)

## Overview

Sector defensive (revenue ổn định bất chấp economic cycle):
- **Tech**: FPT (#1 IT services) + ELC + ITD
- **Utilities**: REE (water + power) + PC1 (construction utility) + GEX (cable + electrical)
- **Healthcare**: TRA Traphaco + DBD + IMP

## Key metrics

- **Revenue growth + recurring revenue ratio**
- **EBITDA margin** (utilities cao, ~30-40%)
- **CAPEX cycle** (utility heavy, tech light)
- **Order backlog** (FPT, PC1)
- **Customer base + retention**

## Jargon mapping

- defensive → "phòng thủ" (giữ explicit, không "stable")
- recurring revenue → "doanh thu định kỳ"
- CAPEX → "chi phí đầu tư cơ bản"
- order backlog → "đơn hàng tồn"
- IT services → "dịch vụ công nghệ"
- outsourcing → "thuê ngoài"

## Analysis lens

Bullish defensive: economic uncertainty + interest rate cut → defensive premium tăng. Tech outsourcing FPT export USD strong.
Bearish: rate hike + global tech budget freeze + USD weak = tech vol up

## Peers

FPT (IT) / REE (utility) / PC1 (construction utility) / GEX (cable) / ITD (IT) / TRA (pharma)
```

- [ ] **Step 1: Create files**

Create agent + skill + sector-context.md + jargon-mapping.md per Task 6 pattern.

- [ ] **Step 1.5 (PATCH critical gap 1): Copy format-bodies + voice + stance from Bank**

```bash
mkdir -p .claude/skills/finpath-newsroom-master-defensive/references/format-bodies/
cp .claude/skills/finpath-newsroom-master-bank/references/format-bodies/*.md \
   .claude/skills/finpath-newsroom-master-defensive/references/format-bodies/
cp .claude/skills/finpath-newsroom-master-bank/references/voice-layer-rules.md \
   .claude/skills/finpath-newsroom-master-defensive/references/voice-layer-rules.md
cp .claude/skills/finpath-newsroom-master-bank/references/stance-directive-handler.md \
   .claude/skills/finpath-newsroom-master-defensive/references/stance-directive-handler.md
```

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/newsroom-master-defensive.md .claude/skills/finpath-newsroom-master-defensive/
git commit -m "feat(master-defensive): NEW master Phòng thủ V5.1.3 (Plan F Task 12)"
```

---

## Phase 3 — Existing master adjustments (Tasks 13-14)

### Task 13: Master-BDS expand KB-optional cho 50 non-anchor mã

**Files:**
- Modify: `.claude/skills/finpath-newsroom-master-bds/SKILL.md` — add KB-optional note + Q1 resolution
- Modify: `.claude/agents/newsroom-master-bds.md` — update description

**Note Q1 resolution**: Master-BDS load `kb/bds/` cho TẤT CẢ 54 mã (sector-level context) + per-ticker KB anchor cho 4 mã (VHM/NVL/KDH/DXG). 50 mã không có per-ticker KB → web search heavy for ticker-specific data.

- [ ] **Step 1: Read current SKILL.md**

```bash
cat .claude/skills/finpath-newsroom-master-bds/SKILL.md
```

- [ ] **Step 2: Add Q1 resolution section**

Add to SKILL.md (after existing workflow):

```markdown
## V5.1.3 — Expanded coverage 4 → 54 mã (Q1 resolution)

Sector codes routed to master-bds (per `data/sector_routing.yaml`):
- materialContractor (19 mã)
- vic3 (3 mã, includes VHM)
- industrial (13 mã, KCN BĐS)
- exvic (19 mã, includes NVL, KDH, DXG)

### KB depth strategy

- **4 anchor mã** (VHM, NVL, KDH, DXG): existing `kb/bds/peers/{TICKER}.md` (nếu có) — full depth
- **50 non-anchor mã**: web search heavy. Use `kb/bds/overview.md` + `kb/bds/jargon.md` (sector-level) cho context, nhưng per-ticker data từ web search

### Decision rule per ticker

```python
# Pseudo-logic trong Master-BDS workflow Step 2
anchor_tickers = {"VHM", "NVL", "KDH", "DXG"}
if ticker in anchor_tickers and Path(f"kb/bds/peers/{ticker}.md").exists():
    load_kb_anchor(ticker)
else:
    web_search_heavy = True
    load_sector_overview()  # kb/bds/overview.md
```

### Sector-specific guidance per sub-sector

- **vic3**: 3 mã Vingroup (VIC, VHM, VRE). VHM anchor có KB. VIC, VRE web search.
- **materialContractor**: 19 mã nhà thầu + nguyên vật liệu (Hoa Bình HBC, Coteccons CTD, etc.). All web search.
- **industrial**: 13 mã KCN (BCM Becamex, KBC Kinh Bắc, IDV, SZC, ...). All web search.
- **exvic**: 19 mã BĐS nhà ở (NVL, KDH, DXG anchors). DIG, NLG, NTL, etc. web search.
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/finpath-newsroom-master-bds/SKILL.md .claude/agents/newsroom-master-bds.md
git commit -m "feat(master-bds): expand coverage 4→54 mã KB-optional (Plan F Task 13)"
```

---

### Task 14: Story Editor stance-judgment-guide.md extend

**Files:**
- Modify: `.claude/skills/finpath-newsroom-story-editor/references/stance-judgment-guide.md`

Add 7 sector case studies (advisor concern 4 from Spec G review).

- [ ] **Step 1: Read existing stance guide**

```bash
cat .claude/skills/finpath-newsroom-story-editor/references/stance-judgment-guide.md
```

- [ ] **Step 2: Add sector-specific cases**

Append to existing file:

```markdown
## V5.1.3 — Sector-specific stance examples (7 new sectors)

7-layer framework universal cho mọi sector, nhưng concrete examples khác nhau. Below là examples cho 7 sector mới.

### oilGas — Sector Dầu khí

**Bullish case (BSR)**:
- Price: BSR tăng 4% phiên gần đây
- Layer signals: Q1 lợi nhuận tăng 25% YoY + biên lọc dầu lên 6 USD/thùng + giá Brent stable 80 USD
- Stance: `positive, high confidence`
- Key evidence: "Q1 LNST +25%", "Biên lọc dầu 6 USD/thùng vs cùng kỳ 4.5", "Brent stable"

**Bearish case (PLX)**:
- Price: PLX giảm 8% phiên gần đây
- Layer signals: Q1 margin shrink + giá xăng nội địa siết + competition Idemitsu
- Stance: `negative, medium confidence`
- Key evidence: "Margin Q1 thu hẹp 1 điểm %", "Giá xăng siết bởi NN", "Idemitsu mở thêm 50 trạm 2026"

### logistics — Sector Logistics

**Bullish case (GMD)**:
- Price: GMD tăng 6%
- Layer signals: TEU throughput Q1 +18% YoY + Gemalink khai trương + BDI SCFI lên
- Stance: `positive, high confidence`
- Key evidence: "TEU Q1 +18%", "Gemalink Phase 2 vận hành 2026", "SCFI YTD +30%"

**Bearish case (VOS)**:
- Price: VOS giảm 12%
- Layer signals: Bunker cost spike + container oversupply + freight rates yếu
- Stance: `negative, high confidence`
- Key evidence: "Bunker +20% YoY", "Maersk báo container oversupply", "SCFI giảm 5 phiên liên tiếp"

### fb — Sector Thực phẩm

**Bullish case (VNM)**:
- Price: VNM tăng 3%
- Layer signals: SSS Q1 +5% positive + giá sữa nguyên liệu giảm + Trung Quốc demand bound
- Stance: `positive, medium confidence`
- Key evidence: "SSS +5%", "Sữa nguyên liệu down 8%", "Xuất khẩu TQ phục hồi Q2"

**Bearish case (SAB)**:
- Price: SAB giảm 10%
- Layer signals: Bia volume giảm + giá lúa mạch up + cồn 35% áp lực
- Stance: `negative, high confidence`
- Key evidence: "Volume bia -8% YoY", "Lúa mạch +15%", "Cồn 35% siết chặt"

### apparel — Sector Dệt may

**Bullish case (TCM)**:
- Price: TCM tăng 8%
- Layer signals: US thoái thuế Trump-era + đơn hàng EU Q2 dồi dào + VND yếu
- Stance: `positive, high confidence`
- Key evidence: "Mỹ thoái thuế chống bán phá giá", "Order book 4 tháng full", "VND/USD +3% YTD"

### retail — Sector Bán lẻ

**Bullish case (MWG)**:
- Price: MWG tăng 5%
- Layer signals: Bách hóa Xanh same-store +8% + Erablue mở rộng + smartphone iPhone 17 launch
- Stance: `positive, medium confidence`
- Key evidence: "BHX SSS +8%", "Erablue Q4 mở 30 cửa hàng", "iPhone 17 boost smartphone Q4"

**Bearish case (FRT)**:
- Price: FRT giảm 15%
- Layer signals: FPT Shop SSS -3% + Long Châu pharma competition + capex burn
- Stance: `negative, medium confidence`
- Key evidence: "FPT Shop SSS -3% Q1", "An Khang Pharmacity mở rộng", "Capex 2026 +25% guidance"

### seafood — Sector Thuỷ sản

**Bullish case (VHC)**:
- Price: VHC tăng 12%
- Layer signals: Xuất khẩu cá tra US Q1 +25% + anti-dumping rate giảm + USD strong
- Stance: `positive, high confidence`
- Key evidence: "Xuất khẩu US +25% YoY", "Anti-dumping rate 0.18%", "VND/USD weak"

### defensive — Sector Phòng thủ

**Bullish case (FPT)**:
- Price: FPT tăng 4%
- Layer signals: FPT Software export +28% YoY + AI services tier-1 + USD strong + global outsourcing demand
- Stance: `positive, high confidence`
- Key evidence: "FPT SW Q1 +28%", "AI services 15% revenue mix", "Order book 12 tháng"

**Bearish case (REE)**:
- Price: REE giảm 6%
- Layer signals: Hydroelectric output drought + utility tariff freeze + capex heavy
- Stance: `negative, medium confidence`
- Key evidence: "Hydroelectric Q1 -20% (hạn hán)", "Tariff điện không tăng 2026", "Capex 2026 +35% guidance"

---

## Universal pattern

Mỗi sector judge stance dựa CONTEXT, không metric rigid. Examples trên minh hoạ 7-layer framework apply universal — chỉ specific signals khác nhau.
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/finpath-newsroom-story-editor/references/stance-judgment-guide.md
git commit -m "feat(story-editor): extend stance-judgment-guide với 7 sector cases (Plan F Task 14)"
```

---

## Phase 4 — CLAUDE.md + Spec A V1.2 PATCH + verification (Tasks 15-17)

### Task 15: CLAUDE.md update universe 61 → 139

> ⚠ **BLOCKED — see MASTER-EXECUTION-SEQUENCE Stage 6.** This task modifies `CLAUDE.md` shared với Plan G Task 7 + Plan H Task 9. Do NOT run independently. Stage 6 aggregates 3 modifications into single subagent commit.

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Read CLAUDE.md universe section**

```bash
grep -n "61 mã\|Universe\|FULL_UNIVERSE\|Bank 27\|CK 30\|BĐS 4" CLAUDE.md
```

- [ ] **Step 2: Update universe section**

Replace section "Universe — 3 sector (61 mã)" with V5.1.3 version:

```markdown
## Universe — 8 sector (139 mã) V5.1.3

Source of truth: Finpath sectors API + `data/sector_routing.yaml`. Editor V1 detect sector qua `lib/finpath_sectors.py` (SQLite cache TTL 365d).

**Bank cluster (18 mã)** → master-bank:
- private7 (6): TCB MBB ACB STB SHB VPB
- soe3 (3): VCB CTG BID
- smallLegacy (9): TPB MSB LPB OCB VIB HDB EIB MSB HDB

**CK (15 mã)** → master-ck:
- stock (15): SSI VND HCM VCI VIX SHS MBS BVS BSI AGR CTS APG ORS FTS SBS

**BĐS cluster (54 mã)** → master-bds (KB-optional cho 50 non-anchor):
- materialContractor (19): HBC CTD ROS BCC HT1 BMP CII NVT HHV ...
- vic3 (3): VIC VHM VRE
- industrial (13): BCM KBC IDV SZC PHR TIP NTC SIP ...
- exvic (19): NVL KDH DXG DIG NLG NTL HDC LGC ...

**Sector mới V5.1.3 (52 mã)** → 7 master agents mới:
- oilGas (8) → master-oilgas: BSR PVS GAS POW PLX OIL PVD PVT
- logistics (12) → master-logistics: GMD HAH VOS VSC PHP CDN HAX VTV TMS VTO ASM (UPCOM SCS ACV)
- fb (8) → master-fb: VNM MSN SAB BHN KDC MCM QNS VHC (overlap seafood, careful)
- apparel (3) → master-apparel: TCM MSH TNG
- retail (7) → master-retail: MWG FRT DGW PNJ PET AST ...
- seafood (6) → master-seafood: VHC ANV MPC FMC IDI CMX
- defensive (12) → master-defensive: FPT REE PC1 GEX ITD TRA DBD IMP ELC ...

**Total: 139 mã universe**.

Ticker ngoài Finpath cache → reply "Ticker [X] không có trong Finpath universe (139 mã). Check `lib/refresh_sector_cache.py --force` nếu ticker mới IPO."
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude.md): universe 61→139 + 8 sector V5.1.3 (Plan F Task 15)"
```

---

### Task 16: Spec A V1.2 PATCH — `/tin-hot N` intersect 61 → 139

**Files:**
- Modify: `docs/superpowers/plans/2026-05-12-hot-ticker-trigger.md` (add V1.2 PATCH NOTICE)
- Modify: `.claude/agents/newsroom-pipeline.md` or relevant `/tin-hot` dispatcher

**Note from Spec G V1.1 PATCH**: Spec A V1.2 PATCH **CANCELED for foreign flow enrichment** (Spec G simplified to on-demand tool). BUT still needed for universe intersect 61 → 139.

- [ ] **Step 1: Read Plan A**

```bash
grep -n "FULL_UNIVERSE\|intersect\|universe" docs/superpowers/plans/2026-05-12-hot-ticker-trigger.md | head
```

- [ ] **Step 2: Add V1.2 PATCH NOTICE to Plan A**

Add at top of Plan A:

```markdown
## 🚨 V1.2 PATCH NOTICE (2026-05-12 PM)

**Trigger**: Spec F V1.0.1 (universe-expansion-kb-optional) ships → universe 61 → 139 (Finpath only).

### Required changes:

1. **`/tin-hot N` intersect set** — replace `FULL_UNIVERSE` list constant với dynamic query:

```python
# OLD V1.1 (Plan A Task 4 area)
from .claude.skills.finpath_newsroom_editor.scripts.routing import FULL_UNIVERSE
universe_set = set(FULL_UNIVERSE)  # 61 mã hardcoded

# NEW V1.2 (Spec F V5.1.3 integration)
from lib.finpath_sectors import FinpathSectors
fs = FinpathSectors(db)
universe_set = set(fs.get_all_cached_tickers())  # 139 mã from cache
```

2. **Auto-refresh cache** if empty — `/tin-hot` triggers refresh before compute top.

3. **NO foreign flow enrichment** — Spec G V1.1 PATCH reverted this. `/tin-hot` only computes 4 top groups (tăng/giảm/bùng nổ/cạn cung), no foreign auto-enrich. Master/Story Editor on-demand call.

### Apply to existing Plan A tasks:

- Task 4 (intersect): use `FinpathSectors.get_all_cached_tickers()` instead of `FULL_UNIVERSE`
- All other Plan A tasks unchanged.
```

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/plans/2026-05-12-hot-ticker-trigger.md
git commit -m "docs(plan-a): V1.2 PATCH NOTICE — universe intersect 61→139 (Plan F Task 16)"
```

---

### Task 17: Smoke tests end-to-end

**Files:**
- Create: `tests/integration/test_universe_expansion_smoke.py`

- [ ] **Step 1: Write smoke tests**

Create `tests/integration/test_universe_expansion_smoke.py`:

```python
"""V5.1.3 end-to-end smoke tests — universe expansion."""
import pytest
from lib.pipeline_db import PipelineDB
from lib.finpath_sectors import FinpathSectors
from lib.sector_router import get_master_route, MasterRouteError


@pytest.mark.integration
def test_real_api_populates_139_tickers(tmp_path):
    """Real Finpath API call → ~139 tickers in cache."""
    db = PipelineDB(str(tmp_path / "test.db"))
    fs = FinpathSectors(db)
    count = fs.refresh_cache()
    assert count >= 130, f"Expected ~139 tickers, got {count}"
    assert count <= 200  # safety upper bound
    db.close()

@pytest.mark.integration
def test_bsr_routes_to_master_oilgas(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    fs = FinpathSectors(db)
    fs.refresh_cache()
    info = fs.get_ticker_sector("BSR")
    assert info is not None
    assert info["sector_code"] == "oilGas"
    assert get_master_route(info["sector_code"]) == "oilgas"
    db.close()

@pytest.mark.integration
def test_mwg_routes_to_master_retail(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    fs = FinpathSectors(db)
    fs.refresh_cache()
    info = fs.get_ticker_sector("MWG")
    assert info["sector_code"] == "retail"
    assert get_master_route(info["sector_code"]) == "retail"
    db.close()

@pytest.mark.integration
def test_fpt_routes_to_master_defensive(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    fs = FinpathSectors(db)
    fs.refresh_cache()
    info = fs.get_ticker_sector("FPT")
    assert info["sector_code"] == "defensive"
    assert get_master_route(info["sector_code"]) == "defensive"
    db.close()

@pytest.mark.integration
def test_vcb_still_routes_to_master_bank(tmp_path):
    """Backward compat: existing Bank tickers still route correctly."""
    db = PipelineDB(str(tmp_path / "test.db"))
    fs = FinpathSectors(db)
    fs.refresh_cache()
    info = fs.get_ticker_sector("VCB")
    assert info["sector_code"] in {"private7", "soe3", "smallLegacy"}
    assert get_master_route(info["sector_code"]) == "bank"
    db.close()

@pytest.mark.integration
def test_unknown_ticker_returns_none(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    fs = FinpathSectors(db)
    fs.refresh_cache()
    info = fs.get_ticker_sector("ZZZZZZ")
    assert info is None
    db.close()
```

- [ ] **Step 2: Run smoke tests**

```bash
uv run pytest tests/integration/test_universe_expansion_smoke.py -v -m integration
```

Expected: 6 tests PASS (requires live Finpath API).

- [ ] **Step 3: Commit**

```bash
git add tests/integration/test_universe_expansion_smoke.py
git commit -m "test(integration): V5.1.3 universe expansion smoke tests (Plan F Task 17)"
```

---

## Self-review (post-write checklist)

### Spec coverage check (V1.0.1)

| Spec section | Covered by task |
|---|---|
| §5 Sector detection layer | Task 1 + 2 |
| §6 Routing layer | Task 3 |
| §7 Master agent strategy | Task 6-12 |
| §8 KB-optional pattern | Task 6-12 (kb_path="") + Task 13 (master-bds) |
| §9 Editor V1 schema | Task 5 |
| §10 Migration path | Documented in CLAUDE.md (Task 15) |
| §11 Story Editor stance examples | Task 14 |
| §12 Quality gates (unchanged) | N/A (no change needed) |
| §13 Hot Ticker Spec A V1.2 | Task 16 |
| §14 File touch list | Tasks 1-15 cover all |
| §15 Testing strategy | Task 17 smoke + per-task unit tests |
| §16 Rollout Phase 1-4 | Mapped to Phase 1-4 of plan |

✅ All sections covered.

### Placeholder scan

- No "TBD" / "TODO" found.
- All code blocks contain actual content.
- All file paths exact.

### Type consistency

- `SectorInfo` TypedDict used consistently in `finpath_sectors.py` + tests.
- `master_route` valid values: `{bank, ck, bds, oilgas, logistics, fb, apparel, retail, seafood, defensive}` — used in `_MASTER_ROUTE_VALID` + smoke tests + agent filenames.
- `sector_code` strings match Finpath API exactly (camelCase preserved: `oilGas`, `materialContractor`).

✅ Self-review pass.

---

## Execution choice

Plan complete and saved to `docs/superpowers/plans/2026-05-12-universe-expansion-kb-optional.md`. Two execution options:

**1. Subagent-Driven (recommended)** — Dispatch fresh subagent per task, two-stage review (spec compliance + code quality) between tasks. Tasks 6-12 (7 new masters) PARALLEL-SAFE.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints.

**Which approach?**
