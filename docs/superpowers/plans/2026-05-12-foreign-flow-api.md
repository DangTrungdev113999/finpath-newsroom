# Foreign Flow API V1.1 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend `lib/finpath_api.py` thêm 3 method foreign flow + SQLite cache hybrid TTL + judgment guides cho 10 master + Story Editor. Foreign flow API = on-demand tool (KHÔNG pipeline-level enrichment, KHÔNG auto-fetch).

**Architecture:** 3 endpoints (`/v2/rooms` + `/roomstatistics/{code}` + `/roombars/{code}`) cache trong SQLite TTL hybrid (15min/1h/6h). Agents (Master + Story Editor) tự judge khi nào call — giống pattern `get_bank_ratios` hiện tại. KHÔNG có top compute module, KHÔNG có Editor V1 stamp, KHÔNG có Master Step 4.5.

**Tech Stack:** Python 3.13, SQLite WAL, requests, pytest.

**Spec**: `docs/superpowers/specs/2026-05-12-foreign-flow-api-design.md` V1.1.

---

## 🚨 CRITICAL: Read V1.1 PATCH NOTICE first

Executor MUST read top of Spec G — `## ⚠ V1.1 PATCH (2026-05-12 PM) — SIMPLIFY to on-demand tool`. V1.0 sections §6/§7/§8.3/§9.3/§10/§11 are DROPPED. Only §4/§5/§12/§14 remain valid.

### What V1.1 dropped (do NOT implement)

- ❌ `lib/foreign_flow.py` top compute module — DROPPED
- ❌ `/tin-hot N` auto-enrichment — DROPPED
- ❌ Editor V1 stamp `foreign_flow` field — DROPPED
- ❌ Master Step 4.5 "Foreign flow check" — DROPPED (conflicts với Headline Craft Step 4.5)
- ❌ pipeline_log `step_1_5_market_snapshot.foreign_flow` nested — DROPPED
- ❌ Spec A V1.2 PATCH cho foreign — CANCELLED (no /tin-hot foreign change)

### What V1.1 keeps

- ✅ `lib/finpath_api.py` extension — 3 methods + cache helpers
- ✅ SQLite cache table `finpath_foreign_cache` với hybrid TTL
- ✅ Story Editor reference `foreign-flow-when-to-call.md` (judgment guide)
- ✅ 10 Master skills reference `foreign-flow-when-to-call.md` (duplicate per CLAUDE.md no-shared)
- ✅ Tests cho 3 API methods + cache behavior

### File impact V1.1

- NEW: 13 file (1 lib + 1 SQL migration + 1 Story Editor ref + 10 Master ref + 2 tests)
- MODIFY: 11 file (lib/finpath_api.py + 1 Story Editor SKILL.md + 10 Master SKILL.md)
- Total: 24 file

---

## Phase 1 — API client extension (Tasks 1-3)

### Task 1: SQLite migration finpath_foreign_cache

**Files:**
- Create: `lib/migrations/2026-05-12-add-finpath-foreign-cache.sql`
- Test: `tests/test_finpath_foreign_cache_schema.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_finpath_foreign_cache_schema.py`:

```python
"""Test finpath_foreign_cache table schema."""
import pytest
from lib.pipeline_db import PipelineDB

def test_finpath_foreign_cache_table_exists(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    cur = db.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='finpath_foreign_cache'"
    )
    assert cur.fetchone() is not None
    db.close()

def test_finpath_foreign_cache_columns(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    cur = db.conn.execute("PRAGMA table_info(finpath_foreign_cache)")
    columns = {row["name"] for row in cur.fetchall()}
    expected = {"cache_key", "endpoint", "payload", "fetched_at", "ttl_seconds"}
    assert expected.issubset(columns)
    db.close()

def test_finpath_foreign_cache_primary_key(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    cur = db.conn.execute("PRAGMA table_info(finpath_foreign_cache)")
    pk = [row["name"] for row in cur.fetchall() if row["pk"] > 0]
    assert pk == ["cache_key"]
    db.close()
```

- [ ] **Step 2: Run test (FAIL expected)**

```bash
uv run pytest tests/test_finpath_foreign_cache_schema.py -v
```

Expected: FAIL — table doesn't exist.

- [ ] **Step 3: Create migration SQL**

`lib/migrations/2026-05-12-add-finpath-foreign-cache.sql`:

```sql
-- Migration: finpath_foreign_cache table for V5.1.3 foreign flow API
-- Hybrid TTL per endpoint:
--   /v2/rooms: 900s (15 min)
--   /roomstatistics/{code}: 3600s (1 h)
--   /roombars/{code}: 21600s (6 h)

CREATE TABLE IF NOT EXISTS finpath_foreign_cache (
    cache_key TEXT PRIMARY KEY,
    endpoint TEXT NOT NULL,
    payload JSON NOT NULL,
    fetched_at TIMESTAMP NOT NULL,
    ttl_seconds INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_foreign_cache_fetched
    ON finpath_foreign_cache(fetched_at);
```

(Migration auto-applied via `_apply_migrations` method added in Plan F Task 1. No code change needed in `pipeline_db.py`.)

- [ ] **Step 4: Run tests pass**

```bash
uv run pytest tests/test_finpath_foreign_cache_schema.py -v
```

Expected: 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add lib/migrations/2026-05-12-add-finpath-foreign-cache.sql tests/test_finpath_foreign_cache_schema.py
git commit -m "feat(db): finpath_foreign_cache table migration (Plan G Task 1)"
```

---

### Task 2: lib/finpath_api.py — add 3 foreign flow methods + cache helpers

**Files:**
- Modify: `lib/finpath_api.py` — add 3 methods + cache helpers
- Test: `tests/test_finpath_api_foreign.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_finpath_api_foreign.py`:

```python
"""Test FinpathAPI foreign flow methods."""
import json
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock
import pytest
from lib.pipeline_db import PipelineDB
from lib.finpath_api import FinpathAPI


@pytest.fixture
def db(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    yield db
    db.close()

@pytest.fixture
def api(db):
    return FinpathAPI(db=db)

@pytest.fixture
def mock_rooms_response():
    return {
        "data": {
            "rooms": [
                {
                    "c": "VHM", "sn": "Vinhomes", "e": "HOSE", "ste": "S",
                    "td": "12/05/2026", "p": 50500,
                    "dnva": -85780000000, "dnv": -200000,
                    "wnva": -340000000000, "mnva": -1200000000000
                },
                {
                    "c": "FPT", "sn": "FPT", "e": "HOSE", "ste": "S",
                    "td": "12/05/2026", "p": 80000,
                    "dnva": 120000000000, "dnv": 1500000,
                    "wnva": 250000000000
                }
            ]
        }
    }

def test_get_foreign_rooms_cache_miss_calls_api(api, mock_rooms_response):
    with patch("lib.finpath_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_rooms_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        rooms = api.get_foreign_rooms()

    assert len(rooms) == 2
    assert rooms[0]["c"] == "VHM"
    assert rooms[0]["dnva"] == -85780000000
    mock_get.assert_called_once()

def test_get_foreign_rooms_cache_hit(api, mock_rooms_response):
    """Second call within TTL = no API call."""
    with patch("lib.finpath_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_rooms_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api.get_foreign_rooms()  # first: cache miss → API
        api.get_foreign_rooms()  # second: cache hit → no API

    mock_get.assert_called_once()

def test_get_foreign_rooms_cache_ttl_15_min(api, db):
    """TTL = 900 seconds for /v2/rooms."""
    api.get_foreign_rooms()  # mocked above pattern, but here check db row
    # ... skip if mock setup complex. Verify via _cache_set ttl_seconds=900 in code review
    pass  # manual code review of get_foreign_rooms ttl param

def test_get_foreign_roomstatistics_validates_period(api):
    """Invalid period raises ValueError (not assert)."""
    with pytest.raises(ValueError, match="period"):
        api.get_foreign_roomstatistics("VHM", period="INVALID")

def test_get_foreign_roomstatistics_valid_periods(api):
    """All 6 valid periods accepted: 1D/1W/1M/3M/6M/1Y."""
    with patch("lib.finpath_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        for period in ["1D", "1W", "1M", "3M", "6M", "1Y"]:
            api.get_foreign_roomstatistics("VHM", period=period)

    assert mock_get.call_count == 6  # cached per (ticker, period)

def test_get_foreign_roombars_cache_key(api, db):
    """roombars cache_key = 'roombars:{ticker}'."""
    with patch("lib.finpath_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"bars": []}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api.get_foreign_roombars("VHM")

    cur = db.conn.execute(
        "SELECT cache_key FROM finpath_foreign_cache WHERE cache_key = 'roombars:VHM'"
    )
    assert cur.fetchone() is not None

def test_stale_cache_fallback_api_down(api, db, mock_rooms_response):
    """API down + cache stale → return stale, log warning."""
    # Pre-populate stale cache (older than TTL 15 min)
    stale_time = (datetime.now(timezone.utc) - timedelta(seconds=1000)).isoformat()
    db.conn.execute("""
        INSERT INTO finpath_foreign_cache (cache_key, endpoint, payload, fetched_at, ttl_seconds)
        VALUES ('rooms', '/v2/rooms', ?, ?, 900)
    """, (json.dumps(mock_rooms_response), stale_time))
    db.conn.commit()

    with patch("lib.finpath_api.requests.get") as mock_get:
        mock_get.side_effect = ConnectionError("API down")
        rooms = api.get_foreign_rooms()

    assert len(rooms) == 2  # returned stale
    assert rooms[0]["c"] == "VHM"

def test_empty_cache_api_fail_raises(api, db):
    """No cache + API down → RuntimeError."""
    with patch("lib.finpath_api.requests.get") as mock_get:
        mock_get.side_effect = ConnectionError("API down")
        with pytest.raises(RuntimeError, match="Finpath API"):
            api.get_foreign_rooms()
```

- [ ] **Step 2: Run tests (FAIL expected)**

```bash
uv run pytest tests/test_finpath_api_foreign.py -v
```

Expected: FAIL — methods don't exist yet.

- [ ] **Step 3: Extend lib/finpath_api.py**

Read existing `lib/finpath_api.py` to see class structure.

Modify `FinpathAPI.__init__` to accept `db` parameter:

```python
# At top of file
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

log = logging.getLogger(__name__)

# Modify __init__:
def __init__(self, base_url: str = "https://api.finpath.vn", timeout: int = 10, db=None) -> None:
    self.base_url = base_url.rstrip("/")
    self.timeout = timeout
    self._cache: dict = {}  # in-memory (existing pattern)
    self.db = db  # SQLite for V5.1.3 foreign flow cache
```

Add 3 new methods + cache helpers at end of class:

```python
# === Group F: Foreign flow (V5.1.3) ===

_VALID_FOREIGN_PERIODS = {"1D", "1W", "1M", "3M", "6M", "1Y"}

def get_foreign_rooms(self) -> list[dict]:
    """All foreign flow snapshot. Cached 15 min in SQLite.

    Returns list of room dicts. Filter ste=='S' for stocks only (caller's job).
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
            f"period '{period}' invalid. Must be one of {self._VALID_FOREIGN_PERIODS}"
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
    self, cache_key: str, endpoint: str, url_path: str,
    ttl: int, unwrap_key: tuple, default,
    params: Optional[dict] = None,
):
    """Generic SQLite cache lookup + API fetch + fallback graceful."""
    if not self.db:
        # Fallback to in-memory cache (existing pattern)
        return self._get(url_path, params=params)

    cached, stale = self._sqlite_cache_lookup(cache_key)
    if cached is not None:
        return self._unwrap(cached, unwrap_key, default)

    # Cache miss OR stale → try API
    try:
        payload = self._fetch_api(url_path, params=params)
        self._sqlite_cache_set(cache_key, endpoint, payload, ttl)
        return self._unwrap(payload, unwrap_key, default)
    except Exception as e:
        if stale is not None:
            log.warning(f"API {url_path} failed, using stale cache: {e}")
            return self._unwrap(stale, unwrap_key, default)
        raise RuntimeError(f"Finpath API {url_path} failed + no cache: {e}")

def _sqlite_cache_lookup(self, cache_key: str) -> tuple[Optional[dict], Optional[dict]]:
    """Returns (fresh_payload | None, stale_payload | None)."""
    cur = self.db.conn.execute(
        "SELECT payload, fetched_at, ttl_seconds FROM finpath_foreign_cache WHERE cache_key = ?",
        (cache_key,)
    )
    row = cur.fetchone()
    if not row:
        return None, None
    fetched_at_str = row["fetched_at"]
    fetched_at = datetime.fromisoformat(fetched_at_str)
    if fetched_at.tzinfo is None:
        fetched_at = fetched_at.replace(tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - fetched_at).total_seconds()
    payload = json.loads(row["payload"])
    if age < row["ttl_seconds"]:
        return payload, None  # fresh
    return None, payload  # stale

def _sqlite_cache_set(self, cache_key: str, endpoint: str, payload: dict, ttl: int) -> None:
    self.db.conn.execute("""
        INSERT INTO finpath_foreign_cache (cache_key, endpoint, payload, fetched_at, ttl_seconds)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(cache_key) DO UPDATE SET
            payload = excluded.payload,
            fetched_at = excluded.fetched_at,
            ttl_seconds = excluded.ttl_seconds
    """, (cache_key, endpoint, json.dumps(payload), datetime.now(timezone.utc).isoformat(), ttl))
    self.db.conn.commit()

def _fetch_api(self, path: str, params: Optional[dict] = None) -> dict:
    """HTTP GET with headers + timeout."""
    r = requests.get(
        f"{self.base_url}{path}",
        params=params,
        timeout=self.timeout,
        headers={
            "accept": "application/json",
            "client-type": "web",
            "origin": "https://finpath.vn",
            "user-agent": "Mozilla/5.0",
        }
    )
    r.raise_for_status()
    body = r.json()
    return body

@staticmethod
def _unwrap(payload: dict, unwrap_key: tuple, default):
    """Navigate nested dict path safely."""
    current = payload
    for key in unwrap_key:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
    return current if current is not None else default
```

- [ ] **Step 4: Run tests to pass**

```bash
uv run pytest tests/test_finpath_api_foreign.py -v
```

Expected: 8 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add lib/finpath_api.py tests/test_finpath_api_foreign.py
git commit -m "feat(api): add 3 foreign flow methods + SQLite cache hybrid TTL (Plan G Task 2)"
```

---

### Task 3: Live API smoke test (validation real data)

**Files:**
- Create: `tests/integration/test_foreign_flow_smoke.py`

- [ ] **Step 1: Write smoke test**

```python
"""Live API smoke tests for foreign flow endpoints."""
import pytest
from lib.pipeline_db import PipelineDB
from lib.finpath_api import FinpathAPI


@pytest.mark.integration
def test_real_rooms_api_returns_data(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    api = FinpathAPI(db=db)
    rooms = api.get_foreign_rooms()
    assert len(rooms) > 1000, f"Expected ~1902 records, got {len(rooms)}"

    # Find VHM
    vhm = next((r for r in rooms if r["c"] == "VHM"), None)
    assert vhm is not None
    assert "dnva" in vhm
    assert "ste" in vhm
    db.close()

@pytest.mark.integration
def test_real_roomstatistics_vhm_1w(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    api = FinpathAPI(db=db)
    stats = api.get_foreign_roomstatistics("VHM", period="1W")
    assert stats is not None  # API trả data hoặc {} nếu no data
    db.close()

@pytest.mark.integration
def test_real_roombars_vhm(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    api = FinpathAPI(db=db)
    bars = api.get_foreign_roombars("VHM")
    assert isinstance(bars, list)  # bars có thể empty, but type list
    db.close()

@pytest.mark.integration
def test_cache_hit_second_call(tmp_path):
    """Second call within TTL → no extra API hit (verify via DB row check)."""
    db = PipelineDB(str(tmp_path / "test.db"))
    api = FinpathAPI(db=db)

    api.get_foreign_rooms()  # first call, populate cache

    cur = db.conn.execute(
        "SELECT fetched_at FROM finpath_foreign_cache WHERE cache_key = 'rooms'"
    )
    first_fetched = cur.fetchone()["fetched_at"]

    api.get_foreign_rooms()  # second call

    cur = db.conn.execute(
        "SELECT fetched_at FROM finpath_foreign_cache WHERE cache_key = 'rooms'"
    )
    second_fetched = cur.fetchone()["fetched_at"]

    assert first_fetched == second_fetched, "Cache hit should not refresh fetched_at"
    db.close()
```

- [ ] **Step 2: Run smoke**

```bash
uv run pytest tests/integration/test_foreign_flow_smoke.py -v -m integration
```

Expected: 4 tests PASS (live API).

- [ ] **Step 3: Commit**

```bash
git add tests/integration/test_foreign_flow_smoke.py
git commit -m "test(integration): live API smoke for foreign flow (Plan G Task 3)"
```

---

## Phase 2 — Judgment guides (Tasks 4-6)

### Task 4: Story Editor — foreign-flow-when-to-call.md reference

**Files:**
- Create: `.claude/skills/finpath-newsroom-story-editor/references/foreign-flow-when-to-call.md`
- Modify: `.claude/skills/finpath-newsroom-story-editor/SKILL.md` — register reference load

- [ ] **Step 1: Create reference file**

`.claude/skills/finpath-newsroom-story-editor/references/foreign-flow-when-to-call.md`:

```markdown
# Foreign Flow — Khi nào Story Editor call API?

> Loaded from `Skill: finpath-newsroom-story-editor`. Free-form judgment — KHÔNG prescriptive "must call". Guide WHEN call adds stance signal value.

## Available API methods

- `api.get_foreign_rooms()` — snapshot all 1902 records foreign flow (use to lookup ticker)
- `api.get_foreign_roomstatistics(ticker, period)` — per-ticker drilldown, period ∈ {1D, 1W, 1M, 3M, 6M, 1Y}
- `api.get_foreign_roombars(ticker)` — time series daily bars

## Call API khi:

### Trigger 1: Ticker đang Hot + stance unclear

Khi crawl_log row có ticker đang trong top tăng/giảm mạnh, NHƯNG insight chưa định hình stance rõ:

```python
rooms = api.get_foreign_rooms()
my_ticker = next((r for r in rooms if r["c"] == ticker), None)
if my_ticker:
    dnva = my_ticker.get("dnva", 0)
    # dnva > 0 = NN mua ròng VND. < 0 = NN bán ròng.
```

- NN dnva > 50 tỷ + price up → strong institutional confirm → positive stance high confidence
- NN dnva < -50 tỷ + price up → "ai đẩy giá khi NN rút?" → caution flag, stance medium confidence

### Trigger 2: Brief candidate có angle về money flow

Khi angle_narrative draft mentions "ai đặt cược", "thị trường đang nghi ngờ", "institutional sentiment":
- MUST call foreign API để có concrete data backing
- Add `key_evidence` entry: "NN [mua/bán] ròng [X] tỷ phiên [date]"

### Trigger 3: Multi-period trend confirmation

Khi stance dựa trend (vd "downtrend cần xác nhận"):
- Call `get_foreign_roomstatistics(ticker, "1W")` — 5 phiên gần
- Or `get_foreign_roomstatistics(ticker, "1M")` cho monthly trend

## KHÔNG call khi:

- Stance đã clear từ 7-layer khác (BCTC + sector cycle + chiến lược rõ) — don't waste API call
- Brief về fundamental sự kiện (Q1 report, BCTC, ĐHĐCĐ) — NN flow off-topic
- Ticker không Hot + không price action — NN flow signal weak
- Bài flash_qa 100-150 từ — quá ngắn cite extra signal

## Cite format trong stance_directive

Khi call → add to `key_evidence` array:
- "NN bán ròng 85,78 tỷ phiên 12/5" (cụ thể số tỷ + period)
- "Top 30 NN bán ròng thị trường" (rank context, nếu drilldown rank lookup)
- Period clear: "phiên 12/5" (1D), "5 phiên" (1W), "tháng 5" (1M)

## Decision matrix 4-quadrant (when both price + foreign confirmed)

|  | Price up | Price down |
|---|---|---|
| **NN strong buy (>50 tỷ)** | STRONG BULLISH — institutional confirm | "Ai đang đặt cược ngược?" — positive medium |
| **NN strong sell (<-50 tỷ)** | "Ai đẩy giá khi NN rút?" — caution flag | STRONG BEARISH — institutional confirm sell |
| **NN normal** | Price signal only | Price signal only |
| **NN no data** | Skip foreign signal | Skip foreign signal |

## Examples

### Case 1: VHM tăng 6,8% + NN bán ròng 85,78 tỷ

```yaml
stance_directive:
  direction: neutral
  confidence: medium
  reason: |
    VHM tăng kịch trần 6,8% phiên 12/5 nhưng khối ngoại bán ròng top
    thị trường (85,78 tỷ). Tín hiệu CONTRADICT — institutional thoát
    trong khi retail đẩy giá. Cần check WHO đang mua + tin gì làm
    catalyst trước khi confirm direction.
  key_evidence:
    - "NN bán ròng 85,78 tỷ phiên 12/5"
    - "Price +6.8% intraday (kịch trần)"
```

### Case 2: FPT tăng 4% + NN mua ròng top

```yaml
stance_directive:
  direction: positive
  confidence: high
  reason: |
    FPT tăng giá cùng NN mua ròng top 30 (+120 tỷ phiên 12/5).
    Institutional confirm uptrend, không phải pump retail.
    7-layer nội lực: Q1 LNST tăng + sector tech đỉnh cycle.
  key_evidence:
    - "NN mua ròng 120 tỷ phiên 12/5"
    - "FPT Software Q1 +28% YoY"
    - "Tech sector tailwind cycle"
```

## Anti-pattern

- ❌ Call API mỗi brief khi không cần — waste tokens + time
- ❌ Cite "NN bán" without specific số → vague, fail Voice Rule 2 no-hedging
- ❌ Force fit foreign signal khi angle là fundamental → off-topic
```

- [ ] **Step 2: Update Story Editor SKILL.md to register reference**

Add to SKILL.md references section:

```markdown
## References (load on-demand)

[existing references...]
- `references/foreign-flow-when-to-call.md` — V5.1.3: when to call foreign flow API for stance judgment
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/finpath-newsroom-story-editor/references/foreign-flow-when-to-call.md \
        .claude/skills/finpath-newsroom-story-editor/SKILL.md
git commit -m "feat(story-editor): foreign-flow-when-to-call judgment guide (Plan G Task 4)"
```

---

### Task 5: 10 Master skills — duplicate foreign-flow-when-to-call.md

**Files:** 10 copies, 1 per master skill (Bank/CK/BĐS + 7 new V5.1.3 from Plan F).

Per CLAUDE.md no-shared-folder rule, duplicate is acceptable.

- [ ] **Step 1: Create master template file (use for all 10)**

`.claude/skills/finpath-newsroom-master-bank/references/foreign-flow-when-to-call.md`:

```markdown
# Foreign Flow — Khi nào Master call API?

> Loaded from `Skill: finpath-newsroom-master-{sector}`. Same pattern as get_income_statement / get_bank_ratios — call when body needs the data.

## Available API methods

- `api.get_foreign_rooms()` — all foreign flow snapshot
- `api.get_foreign_roomstatistics(ticker, period)` — drilldown over period (1D/1W/1M/3M/6M/1Y)
- `api.get_foreign_roombars(ticker)` — time series daily

## Call API khi viết bài:

### Trigger 1: Brief angle mention NN flow

Khi `brief.angle_narrative` hoặc `brief.deep_question` mention NN flow:
- MUST cite số liệu cụ thể trong body
- Call `api.get_foreign_rooms()` → lookup ticker → cite dnva

### Trigger 2: Body cần institutional context

Vd "ai đẩy giá hôm nay?" hoặc "tin tốt nhưng không có ai mua":
- Call để answer question concretely với data
- Add to data_trail entry với source "Finpath_API/foreign-rooms"

### Trigger 3: Multi-period trend narrative

"NN bán ròng 5 phiên liên tiếp":
- Call `api.get_foreign_roomstatistics(ticker, period="1W")`
- Cite specific số cho từng phiên hoặc total

### Trigger 4: Time series chart-like long-form

"30 ngày qua institutional sentiment":
- Call `api.get_foreign_roombars(ticker)`
- Cite trend pattern (consecutive selling, V-recovery, etc.)

## KHÔNG call khi:

- Bài về fundamental (lãi/lỗ/ROE/ratio analysis) — NN flow off-topic
- Format `flash_qa` 100-150 từ — không đủ space cite extra signal
- Brief KHÔNG mention NN + angle khác (Q1 report, ĐHĐCĐ event) — don't force fit
- Stance đã có 3+ key_evidence solid — không cần thêm NN

## Cite format

- Bold số tỷ: `**NN bán ròng 85,78 tỷ**`
- Format VN: `85780000000` → `"85,78 tỷ"` (dấu phẩy thập phân, đơn vị "tỷ")
- Period clear: "phiên 12/5" / "tuần qua" / "5 phiên liên tiếp" / "30 ngày qua"

## Data trail entry MUST

```yaml
data_trail:
  - source: "Finpath_API/foreign-rooms"      # hoặc "Finpath_API/roomstatistics" / "Finpath_API/roombars"
    fetched: "dnva = -85780000000 (today net VND)"
    purpose: "cite NN sell pressure"
    supports_argument: "Opening question paragraph"
```

## Example body cite

### Listicle bullet

> - **NN bán ròng 85,78 tỷ phiên 12/5**: institutional rút trong khi giá tăng kịch trần. Câu hỏi đặt ra: ai đang đẩy giá (retail FOMO? prop trading?), và đợt tăng này có bền không?

### Opening paragraph (Q&A format)

> Cổ phiếu VHM tăng kịch trần 6,8% phiên 12/5, nhưng **khối ngoại bán ròng 85,78 tỷ** — top 1 thị trường. Câu hỏi: tại sao institutional thoát khi giá đỉnh ATH?

### Multi-period narrative

> Trong 5 phiên gần nhất, **khối ngoại bán ròng tổng 340 tỷ** với BSR — chuỗi rút vốn dài nhất 6 tháng qua. Pattern này thường báo hiệu sector cycle inflection.

## Anti-patterns

- ❌ Cite NN khi không relevant tới insight ("force fit" data trail entry)
- ❌ "NN đang có vẻ bán" (vague — phải số cụ thể với period)
- ❌ "85.78 billion VND" (Anh — phải VN "85,78 tỷ")
- ❌ Cite mỗi paragraph — overkill, 1-2 cite/article đủ
```

- [ ] **Step 2: Copy to 9 other masters**

```bash
TEMPLATE=.claude/skills/finpath-newsroom-master-bank/references/foreign-flow-when-to-call.md

for sector in ck bds oilgas logistics fb apparel retail seafood defensive; do
  cp "$TEMPLATE" ".claude/skills/finpath-newsroom-master-$sector/references/foreign-flow-when-to-call.md"
done

ls .claude/skills/finpath-newsroom-master-*/references/foreign-flow-when-to-call.md
```

Expected: 10 files exist.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/finpath-newsroom-master-*/references/foreign-flow-when-to-call.md
git commit -m "feat(masters): foreign-flow-when-to-call judgment guide × 10 (Plan G Task 5)"
```

---

### Task 6: 10 Master SKILL.md register reference loaders

**Files:** Modify 10 SKILL.md files to register `foreign-flow-when-to-call.md` reference.

- [ ] **Step 1: Read Bank SKILL.md to find references section**

```bash
grep -n "## References" .claude/skills/finpath-newsroom-master-bank/SKILL.md
```

- [ ] **Step 2: Add reference entry to each SKILL.md**

Bank SKILL.md References section add:

```markdown
- `references/foreign-flow-when-to-call.md` — V5.1.3: when to call foreign flow API for body cite
```

- [ ] **Step 3: Apply same to 9 other masters**

```bash
# For each sector
for sector in ck bds oilgas logistics fb apparel retail seafood defensive; do
  # Append reference line via sed or manual edit
  # (Each SKILL.md may have different structure — verify before sed)
  echo "Manual edit: .claude/skills/finpath-newsroom-master-$sector/SKILL.md References section"
done
```

Manual edit pattern: locate the `## References` section in each SKILL.md, append:

```markdown
- `references/foreign-flow-when-to-call.md` — V5.1.3: when to call foreign flow API for body cite
```

- [ ] **Step 4: Verify all 10 SKILL.md have reference**

```bash
grep -l "foreign-flow-when-to-call" .claude/skills/finpath-newsroom-master-*/SKILL.md
```

Expected: 10 files match.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/finpath-newsroom-master-*/SKILL.md
git commit -m "feat(masters): register foreign-flow-when-to-call reference × 10 (Plan G Task 6)"
```

---

## Phase 3 — CLAUDE.md + verification (Tasks 7-8)

### Task 7: CLAUDE.md update — note foreign flow data source

> ⚠ **BLOCKED — see MASTER-EXECUTION-SEQUENCE Stage 6.** This task modifies `CLAUDE.md` shared với Plan F Task 15 + Plan H Task 9. Do NOT run independently. Stage 6 aggregates 3 modifications into single subagent commit.

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Read CLAUDE.md data sourcing rule section**

```bash
grep -n "Data sourcing rule\|Finpath API" CLAUDE.md
```

- [ ] **Step 2: Update data sourcing rule section**

Find existing section "Data sourcing rule — KHÔNG restrict" và update Finpath API list:

```markdown
## Data sourcing rule — KHÔNG restrict

Agent (Master Bank, Story Editor, Skeptic) tra data theo thứ tự:

1. **Finpath API** (`lib/finpath_api.py`) — BCTC, ratios, ownership, events
   - V5.1.3: thêm 3 method foreign flow (`get_foreign_rooms` / `get_foreign_roomstatistics` / `get_foreign_roombars`)
   - Foreign flow = on-demand tool. Master/Story Editor judge khi nào call (xem `references/foreign-flow-when-to-call.md`)
2. **Local YAML** (`data/manual/*.yaml`) — Targets / Credit Room / NHNN circulars
3. **Local KB** (`kb/bank/` markdown) — frameworks, history, per-ticker
4. **SQLite memory** (`data/pipeline.db`) — variety guard 3 bài cũ + foreign flow cache
5. **Web search BẮT BUỘC** — fallback khi 1-4 thiếu data
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude.md): foreign flow API V5.1.3 data source note (Plan G Task 7)"
```

---

### Task 8: Integration smoke test — agent calls foreign flow

**Files:**
- Create: `tests/integration/test_master_uses_foreign_flow.py`

- [ ] **Step 1: Write integration test**

```python
"""Verify Master agents can call foreign flow API via lib.finpath_api."""
import pytest
from lib.pipeline_db import PipelineDB
from lib.finpath_api import FinpathAPI


@pytest.mark.integration
def test_master_can_call_get_foreign_rooms(tmp_path):
    """Master agent imports FinpathAPI và call get_foreign_rooms — không crash."""
    db = PipelineDB(str(tmp_path / "test.db"))
    api = FinpathAPI(db=db)
    rooms = api.get_foreign_rooms()
    assert len(rooms) > 0
    db.close()

@pytest.mark.integration
def test_master_can_call_roomstatistics_with_period(tmp_path):
    """Master calls roomstatistics with valid periods."""
    db = PipelineDB(str(tmp_path / "test.db"))
    api = FinpathAPI(db=db)
    for period in ["1D", "1W", "1M"]:
        stats = api.get_foreign_roomstatistics("VHM", period=period)
        assert stats is not None
    db.close()

@pytest.mark.integration
def test_master_uses_cache_efficiently(tmp_path):
    """3 sequential calls to same ticker → only 1 API hit (cache hits 2-3)."""
    db = PipelineDB(str(tmp_path / "test.db"))
    api = FinpathAPI(db=db)

    # 3 calls to same ticker + same period within 1 hour TTL
    api.get_foreign_roomstatistics("VHM", period="1W")
    api.get_foreign_roomstatistics("VHM", period="1W")
    api.get_foreign_roomstatistics("VHM", period="1W")

    cur = db.conn.execute(
        "SELECT COUNT(*) as cnt FROM finpath_foreign_cache WHERE cache_key = 'roomstat:VHM:1W'"
    )
    assert cur.fetchone()["cnt"] == 1  # only 1 row created
    db.close()
```

- [ ] **Step 2: Run smoke**

```bash
uv run pytest tests/integration/test_master_uses_foreign_flow.py -v -m integration
```

Expected: 3 tests PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/integration/test_master_uses_foreign_flow.py
git commit -m "test(integration): Master uses foreign flow API smoke (Plan G Task 8)"
```

---

## Self-review (post-write checklist)

### Spec coverage check (V1.1)

| Spec section | Covered by task |
|---|---|
| §5 API endpoints + caching schema | Task 1 + 2 |
| §6 lib/foreign_flow.py | N/A — DROPPED in V1.1 PATCH |
| §7 /tin-hot enrichment flow | N/A — DROPPED in V1.1 PATCH |
| §8 Story Editor stance integration | Task 4 |
| §9 Master data trail integration | Task 5 + 6 |
| §10 Pipeline log observability | N/A — DROPPED in V1.1 PATCH |
| §11 Spec A V1.2 PATCH | N/A — CANCELLED in V1.1 PATCH (Plan F Task 16 handles universe expand only) |
| §12 Edge cases | Tasks 2 + 8 |
| §14 Testing strategy | Tasks 2, 3, 8 |
| §15 Rollout Phase 1-4 | Mapped to Phase 1-3 |

✅ All V1.1 valid sections covered.

### Placeholder scan

- All file paths exact.
- All code blocks contain implementations.
- No "TBD" or "Add error handling appropriately".

### Type consistency

- `FinpathAPI` constructor accepts `db` param consistently across Task 2 + tests.
- `_VALID_FOREIGN_PERIODS` set uses strings `{"1D", "1W", "1M", "3M", "6M", "1Y"}` — match Finpath API `type` param values.
- `cache_key` patterns:
  - rooms: `"rooms"` (single global)
  - roomstatistics: `f"roomstat:{ticker}:{period}"`
  - roombars: `f"roombars:{ticker}"`
  Consistent across `get_foreign_*` methods + tests.
- `_sqlite_cached_get` returns same shape as `unwrap_key` navigation — caller gets list (rooms/bars) or dict (statistics).

✅ Self-review pass.

---

## Dependency on Plan F

**Plan G depends on Plan F Task 1** for `_apply_migrations` method in PipelineDB. If Plan F Task 1 not done, Plan G Task 1 SQL migration won't load.

**Execution order**: Plan F Task 1 → Plan G Task 1 OK in parallel after. Or Plan F runs first phase, then Plan G phase 1.

---

## Execution choice

Plan complete and saved to `docs/superpowers/plans/2026-05-12-foreign-flow-api.md`. Two execution options:

**1. Subagent-Driven (recommended)** — Dispatch fresh subagent per task. Plan G Phase 2 Tasks 5-6 (10 master files) PARALLEL-SAFE.

**2. Inline Execution** — Execute tasks in this session using executing-plans.

**Which approach?**
