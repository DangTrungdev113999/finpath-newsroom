# Hot Ticker Trigger V1.0 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Triển khai command `/tin-hot N` (default 4, max 10) — fetch Finpath API top movers → intersect 61 universe TRƯỚC compute top N → dedup → sequential dispatch pipeline V5.1 với progress emission.

**Architecture:** Extend `lib/finpath_api.py:FinpathAPI` với `get_overview()` method. Standalone module `lib/finpath_top_movers.py` cho compute logic (4 categories mirror finpath-web stockDataUtils.ts). Command file `.claude/commands/tin-hot.md` orchestrate Bash + Task dispatch. No conflict với Spec B/C — Subsystem A là entry-point layer.

**Tech Stack:** Python 3.13 (uv), requests (via existing FinpathAPI), pytest, Task tool for pipeline dispatch.

**Spec**: `docs/superpowers/specs/2026-05-12-hot-ticker-trigger-design.md` V1.1.

---

## 🚨 V1.2 PATCH NOTICE (2026-05-12 PM)

**Trigger**: Spec F V1.0.1 (universe-expansion-kb-optional) ships → universe 61 → 139 (Finpath cache only).

### Required changes:

1. **`/tin-hot N` intersect set** — replace `FULL_UNIVERSE` list constant with dynamic query:

```python
# OLD V1.1 (Plan A Task 4 area)
from .claude.skills.finpath_newsroom_editor.scripts.routing import FULL_UNIVERSE
universe_set = set(FULL_UNIVERSE)  # 61 mã hardcoded

# NEW V1.2 (Spec F V5.1.3 integration)
from lib.finpath_sectors import FinpathSectors
fs = FinpathSectors(db)
universe_set = set(fs.get_all_cached_tickers())  # ~139 mã from cache
```

2. **Auto-refresh cache** if empty — `/tin-hot` triggers `fs.refresh_cache()` before compute top.

3. **NO foreign flow enrichment** — Spec G V1.1 PATCH reverted this. `/tin-hot` only computes 4 top groups (tăng/giảm/bùng nổ/cạn cung), no foreign auto-enrich. Master/Story Editor call foreign flow API on-demand via `references/foreign-flow-when-to-call.md`.

### Apply to existing Plan A tasks:

- Task 4 (intersect): use `FinpathSectors.get_all_cached_tickers()` instead of `FULL_UNIVERSE`
- All other Plan A tasks unchanged.
- ❌ NO new task added for foreign flow auto-enrichment (Spec G simplified to on-demand only).

---

## Critical context for executor

### Findings from codebase exploration

1. **`lib/finpath_api.py` exists** với `FinpathAPI` class (caching, timeout, raise_for_status). Plan EXTENDS class với `get_overview()` method.
2. **`lib/stages/run_crawler.py` exports `FULL_UNIVERSE`** (61 mã Bank + CK + BĐS). Plan imports for intersect.
3. **No `.claude/commands/tin-hot.md` exists yet** — `.claude/commands/tin.md` existing pattern as reference.
4. **`db.recent_generated_news(ticker, limit)`** returns empty when pipeline produced 0 articles → idempotency 60-min window safe.
5. **Finpath API source-of-truth**: `/Users/trungdt/Desktop/finpath-web/src/Modules/stock-real-time/utils/stockDataUtils.ts` + `top-stocks/constants/index.ts`. Em đã read.

### Run commands

```bash
# Python tests
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_finpath_top_movers.py -v

# Manual smoke against real API
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.finpath_top_movers import fetch_stocks_overview
stocks = fetch_stocks_overview()
print(f'Got {len(stocks)} stocks')
"

# Trigger /tin-hot
# In Claude Code: /tin-hot 4
```

---

## Phase 1 — Python helper module (Tasks 1-2)

### Task 1: Extend `FinpathAPI` with `get_overview()` method

**Files:**
- Modify: `lib/finpath_api.py`
- Test: `tests/test_finpath_api.py`

- [ ] **Step 1: Write failing test**

Append to `tests/test_finpath_api.py`:

```python
def test_get_overview_calls_correct_endpoint(monkeypatch):
    """Verify get_overview hits /api/stocks/v2/overview."""
    from lib.finpath_api import FinpathAPI
    captured_url = []
    def fake_get(self, path, params=None):
        captured_url.append(path)
        return {"stocks": [{"c": "VCB", "p": 92500}]}
    monkeypatch.setattr(FinpathAPI, "_get", fake_get)
    api = FinpathAPI()
    result = api.get_overview()
    assert captured_url == ["/api/stocks/v2/overview"]
    assert result == {"stocks": [{"c": "VCB", "p": 92500}]}


def test_get_overview_uses_cache(monkeypatch):
    """Second call uses cached value (FinpathAPI._cache pattern)."""
    from lib.finpath_api import FinpathAPI
    call_count = [0]
    def fake_get(self, path, params=None):
        call_count[0] += 1
        return {"stocks": []}
    monkeypatch.setattr(FinpathAPI, "_get", fake_get)
    api = FinpathAPI()
    api.get_overview()
    api.get_overview()
    # _get already implements caching via _cache, so 2 calls → 2 _get hits
    # (cache is at _get level, not method level — verify pass-through)
    assert call_count[0] == 2  # Caller relies on _get's own cache logic
```

- [ ] **Step 2: Run test — fail**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_finpath_api.py::test_get_overview_calls_correct_endpoint -v
```
Expected: AttributeError — get_overview doesn't exist.

- [ ] **Step 3: Add `get_overview` method**

In `lib/finpath_api.py`, append to `FinpathAPI` class (after existing methods, before close of class):

```python
    # === Group F: Top movers (V5.1 — Subsystem A) ===

    def get_overview(self) -> dict:
        """Full HOSE stock overview for top-movers compute.

        Returns: {"stocks": [{c, dcp, dvp, mc, a5v, p, st, ...}, ...]} (raw API shape).
        Uses inherited _get() caching + timeout. Public endpoint, no auth.
        """
        return self._get("/api/stocks/v2/overview")
```

- [ ] **Step 4: Run test — verify pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_finpath_api.py -v
```
Expected: all green.

- [ ] **Step 5: Commit**

```bash
git add lib/finpath_api.py tests/test_finpath_api.py
git commit -m "feat(finpath_api): get_overview method for top movers (Plan A Task 1)

V5.1 Subsystem A — extend FinpathAPI class với method gọi
/api/stocks/v2/overview. Reuses inherited _get() caching + timeout.
"
```

---

### Task 2: `lib/finpath_top_movers.py` + tests

**Files:**
- Create: `lib/finpath_top_movers.py`
- Create: `tests/test_finpath_top_movers.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_finpath_top_movers.py`:

```python
"""Tests for lib/finpath_top_movers — fetch + filter + compute + intersect + dedup."""
from __future__ import annotations
import pytest
from unittest.mock import MagicMock, patch
from lib.finpath_top_movers import (
    fetch_stocks_overview, apply_default_filters, compute_top_lists,
    dedup_tickers, HotTicker, _normalize, LIQUIDITY_THRESHOLD_BILLION,
    MARKET_CAP_TOP,
)


SAMPLE_RAW_STOCK = {
    "c": "VCB", "dcp": 2.5, "dc": 1500, "dvp": 50.0, "dv": 1000000,
    "mc": 500_000_000_000, "a5v": 50_000_000_000, "p": 92500, "st": "S",
}


def test_normalize_maps_fields():
    out = _normalize(SAMPLE_RAW_STOCK)
    assert out["code"] == "VCB"
    assert out["dayChangePercent"] == 2.5
    assert out["dayChange"] == 1500
    assert out["dayVolPercent"] == 50.0
    assert out["dayVolume"] == 1000000
    assert out["marketCap"] == 500_000_000_000
    assert out["avgDay5Value"] == 50_000_000_000
    assert out["price"] == 92500
    assert out["secType"] == "S"


def test_apply_default_filters_excludes_low_liquidity():
    stocks = [
        {"code": "A", "secType": "S", "marketCap": 1000, "avgDay5Value": 1_000_000_000, "price": 10},
        {"code": "B", "secType": "S", "marketCap": 500, "avgDay5Value": 50_000_000_000, "price": 20},
    ]
    filtered = apply_default_filters(stocks)
    codes = [s["code"] for s in filtered]
    assert "A" not in codes
    assert "B" in codes


def test_apply_default_filters_excludes_zero_price():
    stocks = [{"code": "X", "secType": "S", "marketCap": 100, "avgDay5Value": 50_000_000_000, "price": 0}]
    assert apply_default_filters(stocks) == []


def test_apply_default_filters_excludes_non_S_secType():
    stocks = [{"code": "Y", "secType": "FU", "marketCap": 100, "avgDay5Value": 50_000_000_000, "price": 10}]
    assert apply_default_filters(stocks) == []


def test_apply_default_filters_takes_top_100_marketcap():
    """Apply marketCap top 100 cut."""
    stocks = [
        {"code": f"T{i}", "secType": "S", "marketCap": 1000 - i, "avgDay5Value": 100_000_000_000, "price": 10}
        for i in range(150)
    ]
    filtered = apply_default_filters(stocks)
    assert len(filtered) == 100
    # Top by marketCap → first item should be T0 (mcap 1000)
    assert filtered[0]["code"] == "T0"


def test_compute_top_lists_n_2():
    filtered = [
        {"code": "A", "dayChangePercent": 5.0, "dayVolPercent": 100, "price": 10},
        {"code": "B", "dayChangePercent": -3.0, "dayVolPercent": 50, "price": 20},
        {"code": "C", "dayChangePercent": 2.0, "dayVolPercent": 200, "price": 30},
        {"code": "D", "dayChangePercent": -1.0, "dayVolPercent": 10, "price": 40},
    ]
    lists = compute_top_lists(filtered, 2)
    assert [t.code for t in lists["price_increment"]] == ["A", "C"]
    assert [t.code for t in lists["price_decrement"]] == ["B", "D"]
    assert [t.code for t in lists["volume_explosion"]] == ["C", "A"]
    assert [t.code for t in lists["depleted_supply"]] == ["D", "B"]


def test_compute_top_lists_invalid_n_raises():
    with pytest.raises(ValueError, match="1-10"):
        compute_top_lists([], 0)
    with pytest.raises(ValueError, match="1-10"):
        compute_top_lists([], 11)


def test_compute_top_lists_n_within_range():
    """N=1 và N=10 both valid."""
    filtered = [{"code": f"T{i}", "dayChangePercent": float(i), "dayVolPercent": 0, "price": 10} for i in range(15)]
    lists1 = compute_top_lists(filtered, 1)
    assert len(lists1["price_increment"]) == 1
    lists10 = compute_top_lists(filtered, 10)
    assert len(lists10["price_increment"]) == 10


def test_dedup_keeps_first_seen_order():
    lists = {
        "price_increment": [HotTicker("A", 10, 1, 1, "price_increment", 1)],
        "price_decrement": [HotTicker("B", 10, -1, 1, "price_decrement", 1)],
        "volume_explosion": [HotTicker("A", 10, 1, 1, "volume_explosion", 1)],  # dup of A
        "depleted_supply": [],
    }
    deduped = dedup_tickers(lists)
    codes = [t for t, _ in deduped]
    assert codes == ["A", "B"]
    a_entry = next(t for t in deduped if t[0] == "A")
    assert "price_increment" in a_entry[1]
    assert "volume_explosion" in a_entry[1]


def test_dedup_empty_lists():
    lists = {cat: [] for cat in ["price_increment", "price_decrement", "volume_explosion", "depleted_supply"]}
    assert dedup_tickers(lists) == []


def test_hot_ticker_to_dict():
    t = HotTicker(code="VCB", price=92500, day_change_percent=2.5, day_vol_percent=50.0, category="price_increment", rank=1)
    d = t.to_dict()
    assert d == {
        "code": "VCB", "price": 92500, "day_change_percent": 2.5,
        "day_vol_percent": 50.0, "category": "price_increment", "rank": 1,
    }


def test_fetch_stocks_overview_uses_finpath_api():
    with patch("lib.finpath_top_movers.FinpathAPI") as mock_class:
        mock_api = MagicMock()
        mock_api.get_overview.return_value = {"stocks": [SAMPLE_RAW_STOCK]}
        mock_class.return_value = mock_api
        stocks = fetch_stocks_overview()
        mock_api.get_overview.assert_called_once()
        assert len(stocks) == 1
        assert stocks[0]["code"] == "VCB"


def test_fetch_stocks_overview_accepts_injected_api():
    """For testing: can inject mock FinpathAPI."""
    fake_api = MagicMock()
    fake_api.get_overview.return_value = {"stocks": [SAMPLE_RAW_STOCK]}
    stocks = fetch_stocks_overview(api=fake_api)
    assert stocks[0]["code"] == "VCB"


def test_fetch_stocks_overview_handles_empty_response():
    fake_api = MagicMock()
    fake_api.get_overview.return_value = {"stocks": []}
    assert fetch_stocks_overview(api=fake_api) == []


def test_fetch_stocks_overview_handles_malformed_response():
    """Defensive: missing 'stocks' key → empty list."""
    fake_api = MagicMock()
    fake_api.get_overview.return_value = {}
    assert fetch_stocks_overview(api=fake_api) == []
```

- [ ] **Step 2: Run test — fail**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_finpath_top_movers.py -v
```
Expected: ModuleNotFoundError.

- [ ] **Step 3: Create `lib/finpath_top_movers.py`**

```python
"""Hot Ticker compute — V5.1 Subsystem A.

Uses FinpathAPI.get_overview() to fetch HOSE stock list, applies default
filters (top 100 marketCap, ≥10 tỷ liquidity, secType S, price > 0), then
computes 4 categories (Tăng giá / Giảm giá / Bùng nổ / Cạn cung) mirroring
finpath-web stockDataUtils.ts.

Source-of-truth (replicate verbatim):
  /Users/trungdt/Desktop/finpath-web/src/Modules/stock-real-time/utils/stockDataUtils.ts
  /Users/trungdt/Desktop/finpath-web/src/Modules/top-stocks/constants/index.ts
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

from lib.finpath_api import FinpathAPI

LIQUIDITY_THRESHOLD_BILLION = 10  # 10 tỷ VND (DEFAULT_FILTERS.liquidity)
MARKET_CAP_TOP = 100  # DEFAULT_FILTERS.marketCap

# Field name mapping API raw → normalized (per convertDataOverViewStock)
FIELD_MAP = {
    "c": "code", "dcp": "dayChangePercent", "dc": "dayChange",
    "dvp": "dayVolPercent", "dv": "dayVolume",
    "mc": "marketCap", "a5v": "avgDay5Value",
    "p": "price", "st": "secType",
}


@dataclass
class HotTicker:
    code: str
    price: float
    day_change_percent: float
    day_vol_percent: float
    category: str  # "price_increment" | "price_decrement" | "volume_explosion" | "depleted_supply"
    rank: int  # 1 = top of category

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _normalize(raw: dict) -> dict:
    """Map API field shortcuts → normalized names per FIELD_MAP."""
    return {FIELD_MAP.get(k, k): v for k, v in raw.items()}


def fetch_stocks_overview(api: FinpathAPI | None = None) -> list[dict]:
    """Use FinpathAPI.get_overview() then normalize fields. Reuses existing
    caching + timeout + error handling. Defensive: missing 'stocks' key → [].

    Args:
      api: Optional injected FinpathAPI instance for testing. Defaults to new.

    Returns: list of normalized stock dicts.
    """
    api = api or FinpathAPI()
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


def compute_top_lists(filtered: list[dict], n: int) -> dict[str, list[HotTicker]]:
    """Compute 4 categories, take top N from each.

    Mirrors stockDataUtils.ts:
    - topPriceIncrement: dayChangePercent >= 0, sort desc
    - topPriceDecrement: dayChangePercent <= 0, sort asc
    - topVolumeExplosion: dayVolPercent >= 0, sort desc
    - topDepletedSupply: dayVolPercent >= 0, sort asc

    Note: depleted_supply uses >= 0 not <= 0 — verbatim from source (see Spec §6).

    Args:
      filtered: stocks post default-filter (and post intersect universe per Spec V1.1)
      n: top N per category (1-10)

    Returns:
      {"price_increment": [HotTicker, ...], "price_decrement": [...], ...}
    """
    if n < 1 or n > 10:
        raise ValueError(f"N must be 1-10, got {n}")

    pi_raw = sorted([s for s in filtered if s.get("dayChangePercent", 0) >= 0],
                    key=lambda s: -s["dayChangePercent"])[:n]
    pd_raw = sorted([s for s in filtered if s.get("dayChangePercent", 0) <= 0],
                    key=lambda s: s["dayChangePercent"])[:n]
    ve_raw = sorted([s for s in filtered if s.get("dayVolPercent", 0) >= 0],
                    key=lambda s: -s["dayVolPercent"])[:n]
    ds_raw = sorted([s for s in filtered if s.get("dayVolPercent", 0) >= 0],
                    key=lambda s: s["dayVolPercent"])[:n]

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


def dedup_tickers(lists: dict[str, list[HotTicker]]) -> list[tuple[str, list[str]]]:
    """Flatten + dedup. Returns [(ticker, [categories_present]), ...] in first-seen order.

    Order convention: price_increment first, then decrement, volume_explosion, depleted_supply.
    Duplicates merged with categories list.
    """
    seen: dict[str, list[str]] = {}
    order: list[str] = []
    for cat in ["price_increment", "price_decrement", "volume_explosion", "depleted_supply"]:
        for ticker in lists.get(cat, []):
            if ticker.code not in seen:
                seen[ticker.code] = []
                order.append(ticker.code)
            seen[ticker.code].append(cat)
    return [(t, seen[t]) for t in order]
```

- [ ] **Step 4: Run tests — verify pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_finpath_top_movers.py -v
```
Expected: 13 passed.

- [ ] **Step 5: Commit**

```bash
git add lib/finpath_top_movers.py tests/test_finpath_top_movers.py
git commit -m "feat(top-movers): Python compute module + 13 unit tests (Plan A Task 2)

V5.1 Subsystem A — compute 4 categories mirroring finpath-web
stockDataUtils.ts.

Source-of-truth (replicate verbatim):
- DEFAULT_FILTERS: marketCap top 100, avgDay5Value ≥ 10 tỷ, secType S, price > 0
- topPriceIncrement / topPriceDecrement: dayChangePercent +/- sort
- topVolumeExplosion / topDepletedSupply: dayVolPercent sort
  (Note: both filter >= 0 — verbatim per Finpath logic, see Spec §6)

Exposes: fetch_stocks_overview / apply_default_filters / compute_top_lists / dedup_tickers + HotTicker dataclass.

13 tests covering: field normalization, filter exclusions, top-100 marketCap cut, 4 compute lists, invalid N raises, dedup first-seen order, fetch defensive handling.
"
```

---

## Phase 2 — Smoke test against real API (Task 3)

### Task 3: Manual smoke test + verify field mapping

**Files:**
- None (validation only)

- [ ] **Step 1: Run manual smoke test against real Finpath API**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.finpath_top_movers import fetch_stocks_overview, apply_default_filters, compute_top_lists, dedup_tickers
from lib.stages.run_crawler import FULL_UNIVERSE

print('Fetching stocks overview...')
stocks = fetch_stocks_overview()
print(f'Got {len(stocks)} raw stocks')

print('Applying default filters...')
filtered = apply_default_filters(stocks)
print(f'After filter: {len(filtered)} stocks')

print('Intersecting with FULL_UNIVERSE...')
universe_stocks = [s for s in filtered if s.get('code') in FULL_UNIVERSE]
print(f'In universe: {len(universe_stocks)} stocks')

print('Computing top 4 per category (universe-only)...')
lists = compute_top_lists(universe_stocks, 4)
for cat, items in lists.items():
    print(f'  {cat}: {[(t.code, t.day_change_percent, t.day_vol_percent) for t in items]}')

print('Deduplication...')
deduped = dedup_tickers(lists)
print(f'Unique tickers: {[(t, cats) for t, cats in deduped]}')
"
```

Expected output: 4 lists each với ≤4 tickers từ universe. Deduped list ≤16. Verify codes match Finpath web UI (Image #3 from spec).

- [ ] **Step 2: Cross-check vs Finpath web UI**

Open `https://finpath.vn/thi-truong` (Cổ phiếu nổi bật tab). Compare:
- Top tăng giá universe vs Python output
- Top giảm giá universe vs Python output
- Top bùng nổ universe vs Python output
- Top cạn cung universe vs Python output

If field mapping wrong → Python output codes/values KHÔNG match UI → fix `FIELD_MAP` constant.

- [ ] **Step 3: Document smoke result**

No commit needed (validation only). If issues found → fix Task 2 + re-test.

---

## Phase 3 — Command file (Task 4)

### Task 4: `.claude/commands/tin-hot.md`

**Files:**
- Create: `.claude/commands/tin-hot.md`

- [ ] **Step 1: Inspect existing command pattern**

```bash
cat .claude/commands/tin.md | head -30
```

Note frontmatter format + how /tin parses args.

- [ ] **Step 2: Create command file**

```markdown
---
description: Trigger pipeline V5.1 cho top N mã từ 4 bên (Tăng giá / Giảm giá / Bùng nổ / Cạn cung) intersect FULL_UNIVERSE 61 mã. Default N=4, max N=10. Sequential dispatch với per-ticker progress emission. Idempotency 60-min window.
allowed-tools: Bash, Task, Read
---

# /tin-hot N command

Parse N từ user args. Validate: N ∈ [1, 10] integer. Default N=4 nếu không có arg.

## Step 1 — Validate N

```python
arg = "$ARGUMENTS"  # User's typed arg after /tin-hot
try:
    N = int(arg) if arg.strip() else 4
    assert 1 <= N <= 10
except (ValueError, AssertionError):
    print("⚠️ N must be integer 1-10. Examples: /tin-hot 4 or /tin-hot 10")
    exit(0)
```

## Step 2 — Fetch + compute (intersect TRƯỚC compute per Spec V1.1)

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.finpath_top_movers import fetch_stocks_overview, apply_default_filters, compute_top_lists, dedup_tickers
from lib.stages.run_crawler import FULL_UNIVERSE

N = <N from Step 1>
stocks = fetch_stocks_overview()
filtered = apply_default_filters(stocks)

# V1.1 advisor fix: intersect TRƯỚC compute top N
universe_stocks = [s for s in filtered if s.get('code') in FULL_UNIVERSE]
lists = compute_top_lists(universe_stocks, N)
deduped = dedup_tickers(lists)

output = {
    'N': N,
    'total_universe_in_top100': len(universe_stocks),
    'lists': {cat: [t.to_dict() for t in items] for cat, items in lists.items()},
    'unique_tickers': [{'ticker': t, 'categories': cats} for t, cats in deduped],
}
print(json.dumps(output, ensure_ascii=False, indent=2))
" > /tmp/tin-hot-result.json
```

## Step 3 — Pre-flight summary

Read `/tmp/tin-hot-result.json` + emit:

```
🔥 Top Hot Tickers — Universe Finpath Newsroom (N={N})

Top tăng giá:
  1. <ticker> ({+pct}%)
  ...

Top giảm giá: <similar>

Top bùng nổ KL: <similar>

Top cạn cung KL: <similar>

📊 Unique sau dedup: {M} mã sẽ dispatch pipeline V5.1
  - {ticker1} ({sector}) — {categories}
  - {ticker2} ({sector}) — {categories}
  ...
```

Hiển thị màu xanh cho tích cực (+pct), đỏ cho tiêu cực (-pct). Sector từ `lib.stages.run_crawler.BANK_UNIVERSE/CK_UNIVERSE/BDS_UNIVERSE` membership check.

If M = 0 → emit "Không có mã hot nào trong universe sau filter — exit gracefully" và stop.

## Step 4 — Idempotency check

For each ticker trong deduped list, query recent 60 min:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json, sys
from datetime import datetime, timezone, timedelta
from lib.pipeline_db import PipelineDB

now = datetime.now(timezone.utc)
sixty_min_ago = now - timedelta(minutes=60)

with open('/tmp/tin-hot-result.json') as f:
    data = json.load(f)

db = PipelineDB('data/pipeline.db')
to_dispatch = []
skipped = []
for entry in data['unique_tickers']:
    ticker = entry['ticker']
    recent = db.recent_generated_news(ticker, limit=1)
    if recent and recent[0].get('published_at'):
        try:
            published_at = datetime.fromisoformat(recent[0]['published_at'].replace('Z', '+00:00'))
            if published_at > sixty_min_ago:
                skipped.append({'ticker': ticker, 'reason': f\"Đã có bài {(now - published_at).total_seconds() / 60:.0f} phút trước\"})
                continue
        except (ValueError, AttributeError):
            pass
    to_dispatch.append(entry)
db.close()

print(json.dumps({'to_dispatch': to_dispatch, 'skipped': skipped}, ensure_ascii=False, indent=2))
" > /tmp/tin-hot-dispatch.json
```

Emit skipped tickers nếu có:

```
⚠️ Skipped (idempotency 60-min window):
  - VCB: Đã có bài 23 phút trước
```

## Step 5 — Sequential dispatch + progress emission

For each `to_dispatch` entry, in order:

```
[{i}/{M}] Dispatching /tin {ticker}... (categories: {cats})
```

Then dispatch via Task tool:

```
Task: newsroom-pipeline
prompt: <ticker>
```

Wait for completion. Parse return → count articles + duration.

Emit completion line:
```
  → ✅ done in {Xm:Ys}, {N} articles generated
```
hoặc nếu fail:
```
  → ⚠️ failed: <error message ngắn>
```

Append fail vào `errors.append({'ticker': ticker, 'error': error_msg})` for final summary.

⚠️ HARD RULE — sequential, NOT parallel. Dispatch tiếp theo CHỈ sau khi current Task return.

## Step 6 — Final summary

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
errors = <errors list from dispatch loop>
skipped = <skipped from idempotency>
success = <success list from dispatch loop>
total_articles = sum(s['articles'] for s in success)

print(f'✅ /tin-hot hoàn tất:')
print(f'  - {len(success)} mã dispatched thành công')
print(f'  - {total_articles} bài generated')
print(f'  - {len(skipped)} mã skip (idempotency)')
print(f'  - {len(errors)} mã fail')

if errors:
    with open('/tmp/tin-hot-errors.json', 'w', encoding='utf-8') as f:
        json.dump(errors, f, ensure_ascii=False, indent=2)
    print(f'  Lỗi log: /tmp/tin-hot-errors.json')

print(f'')
print(f'Xem feed: http://localhost:5176/feed')
"
```

## Hard rules

- N ∈ [1, 10] integer. Reject 0, 11+, non-integer.
- Sequential dispatch — KHÔNG parallel (DB write safety).
- Ticker fail (Master gates / Story Editor 0 briefs) → skip + continue, log error.
- Empty intersect (0 mã) → exit gracefully với message.
- Idempotency 60-min: skip ticker đã có bài < 60 phút.
- Per-ticker progress emission BẮT BUỘC — silent long wait là UX fail.

## Examples

```
User: /tin-hot 4
Em: 🔥 Top Hot Tickers — Universe Finpath Newsroom (N=4)
    ... (pre-flight)
    [1/3] Dispatching /tin DXG... ✅ done in 2m18s, 2 articles
    [2/3] Dispatching /tin TCB... ✅ done in 3m42s, 3 articles
    [3/3] Dispatching /tin VHM... ✅ done in 2m51s, 1 article
    ✅ /tin-hot hoàn tất: 3 mã, 6 bài
```
```

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/tin-hot.md
git commit -m "feat(command): /tin-hot N — dispatch top movers pipeline V5.1 (Plan A Task 4)

V5.1 Subsystem A — entry-point command:
- Parse N (default 4, max 10)
- Fetch Finpath overview → filter top 100 → intersect 61 universe
- Compute top N per 4 categories (universe-only)
- Dedup → idempotency 60-min check
- Sequential dispatch với per-ticker progress emission
- Final summary với articles count + errors

HARD RULES: sequential not parallel, fail-skip-continue, empty-graceful-exit.
"
```

---

## Phase 4 — Documentation (Task 5)

### Task 5: CLAUDE.md — new section + command listing

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add section "/tin-hot command V1.0"**

Find appropriate location (after existing pipeline section, before quality gates). Add:

```markdown
## Hot Ticker Trigger V1.0 (Subsystem A) — `/tin-hot N`

Command auto-discover top movers từ Finpath API + dispatch pipeline V5.1 batch.

### Usage
```
/tin-hot              # N=4 default
/tin-hot 4            # explicit
/tin-hot 10           # max
```

### Logic
1. Fetch `GET https://api.finpath.vn/api/stocks/v2/overview` (public, no auth)
2. Default filters: marketCap top 100, avgDay5Value ≥ 10 tỷ, secType=S, price > 0
3. **Intersect FULL_UNIVERSE 61 mã TRƯỚC compute top N** (Spec V1.1 fix — universe-coverage reliable)
4. Compute 4 categories per `stockDataUtils.ts` logic (mirror finpath-web):
   - Tăng giá: dayChangePercent ≥ 0, sort desc
   - Giảm giá: dayChangePercent ≤ 0, sort asc
   - Bùng nổ: dayVolPercent ≥ 0, sort desc
   - Cạn cung: dayVolPercent ≥ 0, sort asc
5. Dedup overlap
6. Idempotency 60-min window (skip ticker đã có bài < 60p)
7. Sequential dispatch pipeline V5.1 với per-ticker progress

### Constraints
- N ∈ [1, 10]
- Sequential dispatch (DB write safety, WAL mode)
- Fail-skip-continue per ticker
- Empty intersect → graceful exit

Source code:
- `lib/finpath_top_movers.py` — compute logic
- `lib/finpath_api.py:FinpathAPI.get_overview()` — API fetch
- `.claude/commands/tin-hot.md` — orchestrator
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude.md): /tin-hot command section V1.0 (Plan A Task 5)

V5.1 Subsystem A — new command documentation. Logic + usage + constraints.
"
```

---

## Phase 5 — E2E verification (Task 6)

### Task 6: Run `/tin-hot 4` end-to-end

**Files:**
- None (verification)

- [ ] **Step 1: Start dev server (visual baseline)**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npm run dev &
# Browser → http://localhost:5176/feed
```

Note current article count + tickers.

- [ ] **Step 2: Trigger `/tin-hot 4`**

In Claude Code session:
```
/tin-hot 4
```

Observe:
- Pre-flight summary displays 4 lists + dedup count
- Per-ticker progress emission (NOT silent wait)
- Sequential dispatch (next only after current done)
- Final summary với articles count

- [ ] **Step 3: Verify articles trong feed**

Refresh `http://localhost:5176/feed`. Verify:
- New articles xuất hiện cho từng ticker dispatched
- Article count matches summary
- Articles có pipeline_version=V5.1 (or V5.0 if not yet bumped)

- [ ] **Step 4: Verify idempotency**

Re-run `/tin-hot 4` ngay. Expected:
- Same tickers selected (market data ít đổi trong ~1 min)
- All skipped với reason "Đã có bài X phút trước"
- No new articles generated

- [ ] **Step 5: Verify error handling**

If any pipeline failed (Master gates reject all, Story Editor 0 briefs):
- `/tmp/tin-hot-errors.json` exists với fail details
- Other tickers continued normally
- Summary count matches

- [ ] **Step 6: Commit any fixes from E2E**

```bash
git status
# If accumulated fixes
git add <files>
git commit -m "fix(<scope>): <issue> caught in E2E /tin-hot verification (Plan A Task 6)"
```

- [ ] **Step 7: Mark plan complete**

Plan A done. Push to origin/main when user approves all 4 plans (B + C + A) E2E results.

---

## Self-review

### Spec coverage
- ✅ §2 user flow → Tasks 4 (command file orchestrates)
- ✅ §5 command syntax (N default 4, max 10) → Task 4 Step 1
- ✅ §6 Finpath API + 4 compute → Tasks 1, 2
- ✅ §7.1 `lib/finpath_top_movers.py` + FinpathAPI.get_overview → Tasks 1, 2
- ✅ §7.2 `.claude/commands/tin-hot.md` → Task 4
- ✅ §7.3 tests → Task 2 (13 tests) + Task 3 manual smoke
- ✅ §8 idempotency + failure handling → Task 4 Step 4-5
- ✅ §9 file touch — all addressed
- ✅ §11 testing strategy — Tasks 2 (unit) + 3 (smoke) + 6 (E2E)
- ✅ §12 rollout phases — mapped to Tasks 1-6

### Placeholder scan
- No TBD / TODO placeholders
- All bash commands complete with concrete inputs

### Type consistency
- `HotTicker` dataclass consistent across Tasks 2 + 4
- `fetch_stocks_overview(api=None)` signature accepts FinpathAPI injection
- `compute_top_lists(stocks, n)` returns dict[str, list[HotTicker]] consistent

### Conflict check
- No conflicts với Plan B (Format Diversity) or Plan C (Headline Craft)
- Subsystem A is independent entry-point layer
- Tests independent (no shared fixtures with B/C)

---

## Execution choice (per user batch strategy — DEFERRED)

User strategy: brainstorm all subsystems → plan all → execute batch. Plan A ready; execution kết hợp với Plan B + Plan C khi user approves all.

After all plans ready:
- **Subagent-Driven** — fresh subagent per task, two-stage review, interleaved order
- **Inline Execution** — batch with checkpoints

Resolved choice TBD per user.
