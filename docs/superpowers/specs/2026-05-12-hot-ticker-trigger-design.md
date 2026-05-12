# Hot Ticker Trigger — Design Spec V1.0

**Date**: 2026-05-12
**Author**: Brainstormed với em (Claude)
**Status**: Draft — pending user review before plan
**Subsystem**: A (Hot ticker trigger) from initial 5-subsystem feedback
**Independent from**: Spec B (Format Diversity) + Spec C (Headline Craft). Subsystem A là **entry point mới**, dispatches existing pipeline V5.1 (đã có Step 1.5 + Step 3.5 + Step 4.5). KHÔNG patch B/C.

---

## 1. Goal

Thêm command `/tin-hot N` lấy top N mã từ mỗi 4 bên (Tăng giá / Giảm giá / Bùng nổ / Cạn cung) từ Finpath API → intersect 61-mã universe → dispatch pipeline V5.1 cho mỗi mã unique. Mục tiêu: bài Newsroom mang tính thời điểm theo sếp feedback "bám sát các mã hot, top 10 tăng/giảm trong ngày".

## 2. User flow

```
User: /tin-hot 4
↓
Pipeline:
  1. Call Finpath API /api/stocks/v2/overview
  2. Apply default filters: marketCap top 100, avgDay5Value ≥ 10 tỷ, secType=S, price > 0
  3. INTERSECT FULL_UNIVERSE (61 mã Bank/CK/BĐS) — narrow to universe BEFORE compute top N
  4. Compute 4 lists per stockDataUtils.ts logic — top N from universe-only
  5. Dedup overlap (mã ở nhiều bên)
  6. Report: "Found {X} unique mã từ top {N} mỗi bên — dispatching pipeline cho từng mã"
  7. Dispatch existing /tin pipeline V5.1 per ticker (sequential, NOT parallel)
  8. Per-ticker progress emission (advisor-suggested UX)
  9. Final summary: N bài generated, link to feed viewer
```

**Advisor blocker resolved**: Intersect đặt TRƯỚC compute top N (was AFTER). Lý do: nếu intersect SAU, top 4 globally toàn mã ngoài universe (vd FOX/GEX/NLG/BSR) → `/tin-hot 4` trả 0-1 mã từ "Tăng giá". Chuyển intersect lên trước → `/tin-hot N` reliably trả N mã từ mỗi bên trong universe (~10-15 mã universe thường nằm trong top 100 marketCap, đủ fill 4-10 per category).

Command nghĩa rõ: **"top N movers OF Newsroom 61 universe per category"** — không phải top globally rồi filter.

## 3. Out of scope (defer)

- **Cron auto-trigger** — chỉ manual command MVP
- **Filter customization từ user** (vd `/tin-hot 4 --marketcap=400`) — luôn dùng default filters
- **Universe expansion** beyond 61 mã — chỉ trong universe
- **Parallel dispatch** — sequential, an toàn DB write
- **Real-time monitoring** dashboard
- **Multi-day historical** (vd top movers tuần qua) — chỉ hôm nay
- **Mid-day vs end-of-day timing** — bất kể giờ nào, user gọi command thì run

## 4. Architecture overview

### Pipeline triggered by `/tin-hot` differ from manual `/tin`

```
/tin <TICKER>:
  1 ticker → 1 pipeline V5.1 run → N briefs → N articles

/tin-hot N:
  16+ candidates → intersect 61 → M unique tickers → M sequential pipeline runs
                                                      → Each = 1 pipeline V5.1 = N briefs = N articles
                                                      → Total articles = sum(N per pipeline run)
```

`/tin-hot` chỉ là **batched entry point** — KHÔNG modify pipeline. Mỗi ticker chạy pipeline V5.1 nguyên gốc.

### Architectural decisions

| Decision | Choice | Rationale |
|---|---|---|
| **Manual command vs cron** | Manual `/tin-hot N` MVP | Anh muốn linh hoạt; cron defer Phase 2 |
| **Dedup overlap** | Auto dedup | Mã FOX ở cả "Tăng giá" + "Bùng nổ" → 1 bài, không trùng |
| **Universe filter** | Intersect 61 FULL_UNIVERSE | Master Bank/CK/BĐS chỉ có KB cho 61 mã; ticker ngoài → bài yếu |
| **Default N if no arg** | N = 4 | Smallest meaningful (= 16 candidates max → ~3-5 unique trong universe) |
| **Max N** | 10 (= 40 candidates max → ~10-15 unique) | Tránh dispatch quá nhiều bài 1 lúc |
| **Parallel vs sequential dispatch** | Sequential | DB write safety (WAL mode tốt nhưng simplicity > speed) |
| **Failure handling** | One ticker fail → skip + continue, log error | Robust batch run |

## 5. Command syntax

### `/tin-hot N`

- `N` (optional, default 4, max 10) — số top từ mỗi bên (universe-only)
- Hoặc `/tin-hot` (không arg) — default N=4

### Examples (yield reliable sau khi intersect TRƯỚC compute)

```
/tin-hot              → N=4, 16 candidates universe-only, ~8-14 unique (sau dedup)
/tin-hot 4            → same as above
/tin-hot 10           → N=10, 40 candidates, ~20-30 unique
/tin-hot 20           → ERROR: N must be 1-10
```

Yield realistic vì có 61 mã universe / 4 lists → universe-coverage thường 10-15 mã có dayChangePercent ≠ 0 → fill top N dễ.

### Pre-flight output (BEFORE dispatch)

```
🔥 Top Hot Tickers (N=4)
  Top tăng giá: FOX (+2.96%), DXG (+2.55%), TCH (+2.41%), CII (+2.28%)
  Top giảm giá: <list>
  Top bùng nổ: QNS, CII, FOX, DXG
  Top cạn cung: <list>

📊 Sau intersect FULL_UNIVERSE (61 mã Bank/CK/BĐS):
  ✓ DXG (BĐS) — Tăng giá + Bùng nổ
  ✓ TCB (Bank) — Tăng giá
  ✓ VND (CK) — Tăng giá
  ✓ EIB (Bank) — Bùng nổ
  → 4 mã unique sẽ dispatch pipeline V5.1

Proceeding with /tin DXG → /tin TCB → /tin VND → /tin EIB sequentially...
```

User thấy ngay cái gì sẽ được run trước khi commit.

## 6. Finpath API integration

### Endpoint

```python
# lib/finpath_top_movers.py (NEW)
GET https://api.finpath.vn/api/stocks/v2/overview
→ {"data": {"stocks": [{...}, ...]}}
```

Public, no auth required (anh confirmed).

### Raw stock fields (per `convertDataOverViewStock`)

| API field | Normalized | Type | Meaning |
|---|---|---|---|
| `c` | `code` | str | Ticker (e.g. "FOX") |
| `dcp` | `dayChangePercent` | float | % change today |
| `dc` | `dayChange` | float | Absolute change |
| `dvp` | `dayVolPercent` | float | % volume vs avg |
| `dv` | `dayVolume` | int | Today's volume |
| `mc` | `marketCap` | float | Market cap (tỷ) |
| `a5v` | `avgDay5Value` | float | 5-day avg trading value |
| `p` | `price` | float | Current price |
| `st` | `secType` | str | "S"/"E"/"ETF"/"FU"/"CW"/"W" |

### Default filters (per `DEFAULT_FILTERS` in finpath-web)

```python
def apply_default_filters(stocks: list[dict]) -> list[dict]:
    """1. Sort marketCap desc → top 100. 2. Filter avgDay5Value ≥ 10 tỷ + price > 0 + secType = S."""
    sorted_by_mc = sorted(stocks, key=lambda s: -(s.get("marketCap") or 0))
    top_100 = sorted_by_mc[:100]
    return [
        s for s in top_100
        if s.get("avgDay5Value", 0) >= 10_000_000_000  # 10 tỷ VND
        and s.get("price", 0) > 0
        and s.get("secType") == "S"
    ]
```

### 4 compute functions (mirror `stockDataUtils.ts`)

```python
def top_price_increment(stocks: list[dict]) -> list[dict]:
    """Filter dayChangePercent >= 0, sort desc."""
    filtered = [s for s in stocks if s.get("dayChangePercent", 0) >= 0]
    return sorted(filtered, key=lambda s: -s["dayChangePercent"])

def top_price_decrement(stocks: list[dict]) -> list[dict]:
    """Filter dayChangePercent <= 0, sort asc."""
    filtered = [s for s in stocks if s.get("dayChangePercent", 0) <= 0]
    return sorted(filtered, key=lambda s: s["dayChangePercent"])

def top_volume_explosion(stocks: list[dict]) -> list[dict]:
    """Filter dayVolPercent >= 0, sort desc."""
    filtered = [s for s in stocks if s.get("dayVolPercent", 0) >= 0]
    return sorted(filtered, key=lambda s: -s["dayVolPercent"])

def top_depleted_supply(stocks: list[dict]) -> list[dict]:
    """Filter dayVolPercent >= 0, sort asc (lowest volume % first).

    ⚠️ Note (advisor): Source `stockDataUtils.ts:83` uses `dayVolPercent >= 0`
    (not `<= 0`) — replicates Finpath logic verbatim. Tức là "cổ phiếu có
    volume_change DƯƠNG nhỏ nhất" thay vì "volume cạn cung thực sự âm".
    Em không sửa logic — replicate source-of-truth.
    """
    filtered = [s for s in stocks if s.get("dayVolPercent", 0) >= 0]
    return sorted(filtered, key=lambda s: s["dayVolPercent"])
```

## 7. New components

### 7.1 `lib/finpath_top_movers.py` (NEW)

**Advisor concern 2 resolution**: Existing `lib/finpath_api.py:FinpathAPI` class wraps Finpath public API với caching + timeout. Em chọn EXTEND `FinpathAPI.get_overview()` method (consistency với existing pattern) + thêm compute logic riêng trong `finpath_top_movers.py`.

```python
# lib/finpath_api.py — ADD method to existing FinpathAPI class
class FinpathAPI:
    # ... existing methods ...

    def get_overview(self) -> dict:
        """V5.1: full HOSE stock overview for top-movers compute.

        Returns: {"stocks": [{c, dcp, dvp, mc, a5v, p, st, ...}, ...]} (raw API shape).
        Uses inherited _get() caching + raise_for_status + timeout.
        """
        return self._get("/api/stocks/v2/overview")
```

```python
# lib/finpath_top_movers.py — standalone compute module
"""Hot Ticker compute — uses FinpathAPI.get_overview() for fetch, applies
compute logic mirroring finpath-web stockDataUtils.ts.

Source-of-truth for 4 compute functions:
  /Users/trungdt/Desktop/finpath-web/src/Modules/stock-real-time/utils/stockDataUtils.ts
Default filters:
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


def fetch_stocks_overview(api: FinpathAPI | None = None) -> list[dict]:
    """Use FinpathAPI.get_overview() then normalize fields. Reuses existing
    caching + timeout + error handling. Raises on network/parse error.
    """
    api = api or FinpathAPI()
    raw = api.get_overview()
    raw_stocks = raw.get("stocks", []) if isinstance(raw, dict) else []
    return [_normalize(s) for s in raw_stocks]


def _normalize(raw: dict) -> dict:
    """Map API field shortcuts → normalized names."""
    return {FIELD_MAP.get(k, k): v for k, v in raw.items()}


def apply_default_filters(stocks: list[dict]) -> list[dict]:
    """Top 100 marketCap + avgDay5Value ≥ 10 tỷ + price > 0 + secType S."""
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

    Args:
      filtered: stocks post default-filter
      n: top N per category (1-10)

    Returns:
      {"price_increment": [HotTicker, ...], "price_decrement": [...], ...}
    """
    if n < 1 or n > 10:
        raise ValueError(f"N must be 1-10, got {n}")

    pi = sorted([s for s in filtered if s.get("dayChangePercent", 0) >= 0],
                key=lambda s: -s["dayChangePercent"])[:n]
    pd = sorted([s for s in filtered if s.get("dayChangePercent", 0) <= 0],
                key=lambda s: s["dayChangePercent"])[:n]
    ve = sorted([s for s in filtered if s.get("dayVolPercent", 0) >= 0],
                key=lambda s: -s["dayVolPercent"])[:n]
    ds = sorted([s for s in filtered if s.get("dayVolPercent", 0) >= 0],
                key=lambda s: s["dayVolPercent"])[:n]

    def _wrap(items: list[dict], cat: str) -> list[HotTicker]:
        return [
            HotTicker(
                code=s["code"],
                price=s["price"],
                day_change_percent=s.get("dayChangePercent", 0),
                day_vol_percent=s.get("dayVolPercent", 0),
                category=cat,
                rank=i + 1,
            )
            for i, s in enumerate(items)
        ]

    return {
        "price_increment": _wrap(pi, "price_increment"),
        "price_decrement": _wrap(pd, "price_decrement"),
        "volume_explosion": _wrap(ve, "volume_explosion"),
        "depleted_supply": _wrap(ds, "depleted_supply"),
    }


def intersect_universe(lists: dict[str, list[HotTicker]], universe: list[str]) -> dict[str, list[HotTicker]]:
    """Filter each list to tickers in FULL_UNIVERSE only."""
    return {
        cat: [t for t in items if t.code in universe]
        for cat, items in lists.items()
    }


def dedup_tickers(lists: dict[str, list[HotTicker]]) -> list[tuple[str, list[str]]]:
    """Flatten + dedup. Return [(ticker, [categories_present]), ...].

    Tickers ordered by first-seen across categories: price_increment first, then decrement, volume_explosion, depleted_supply.
    Duplicates merged with categories list.
    """
    seen: dict[str, list[str]] = {}
    order: list[str] = []
    for cat in ["price_increment", "price_decrement", "volume_explosion", "depleted_supply"]:
        for ticker in lists[cat]:
            if ticker.code not in seen:
                seen[ticker.code] = []
                order.append(ticker.code)
            seen[ticker.code].append(cat)
    return [(t, seen[t]) for t in order]
```

### 7.2 `.claude/commands/tin-hot.md` (NEW command)

Skill entry per `.claude/commands/tin.md` pattern.

```markdown
---
description: Trigger pipeline V5.1 cho top N mã từ 4 bên (Tăng giá / Giảm giá / Bùng nổ / Cạn cung) intersect FULL_UNIVERSE 61 mã. Default N=4, max N=10.
allowed-tools: Bash, Task, Read
---

# /tin-hot N command

Parse N từ user args (default 4, max 10).

## Step 1 — Fetch + compute top movers

Run Python helper:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json, sys
from lib.finpath_top_movers import fetch_stocks_overview, apply_default_filters, compute_top_lists, intersect_universe, dedup_tickers
from lib.stages.run_crawler import FULL_UNIVERSE

N = <N from user arg>
stocks = fetch_stocks_overview()
filtered = apply_default_filters(stocks)

# V5.1 FIX: intersect TRƯỚC compute (advisor blocker resolved).
# Filter universe-only → compute top N per category trên universe-restricted set.
universe_stocks = [s for s in filtered if s.get('code') in FULL_UNIVERSE]
lists = compute_top_lists(universe_stocks, N)
deduped = dedup_tickers(lists)

output = {
    'lists_in_universe': {cat: [t.to_dict() for t in items] for cat, items in lists.items()},
    'unique_tickers': [{'ticker': t, 'categories': cats} for t, cats in deduped],
    'total_universe_in_top100': len(universe_stocks),
}
print(json.dumps(output, ensure_ascii=False, indent=2))
" > /tmp/tin-hot-result.json
```

## Step 2 — Report to user

Read `/tmp/tin-hot-result.json` + emit pre-flight summary:

```
🔥 Top Hot Tickers (N=4) — Hôm nay

Top tăng giá:
  1. FOX (+2.96%)
  2. DXG (+2.55%)
  3. TCH (+2.41%)
  4. CII (+2.28%)

Top giảm giá: <similar>

Top bùng nổ KL:
  1. QNS (+2.812.4% KL)
  2. CII (+1.123.9% KL)
  3. FOX (+860.6% KL)
  4. DXG (+676.8% KL)

Top cạn cung KL: <similar>

📊 Sau intersect FULL_UNIVERSE (61 mã):
  ✓ DXG (BĐS) — categories: Tăng giá + Bùng nổ
  ✓ <ticker> (Bank/CK/BĐS) — <cats>
  ...

→ {M} mã unique sẽ dispatch pipeline V5.1.
```

## Step 3 — Dispatch pipeline per ticker (sequential + progress emission)

For each `unique_ticker` in `deduped`, emit progress BEFORE dispatch + AFTER each completes:

```
[1/4] Dispatching /tin DXG... (categories: price_increment + volume_explosion)
  → ✅ done in 2m18s, 2 articles generated
[2/4] Dispatching /tin TCB... (categories: price_increment)
  → ✅ done in 3m42s, 3 articles generated
[3/4] Dispatching /tin VND... (categories: volume_explosion)
  → ⚠️ failed: Master gates 0 briefs accepted
[4/4] Dispatching /tin EIB... (categories: depleted_supply)
  → ✅ done in 2m51s, 1 article generated
```

Dispatch via Task tool (sequential, NOT parallel — DB write safety):

```
Task: newsroom-pipeline
prompt: <TICKER>
```

Wait for completion. Parse return → count articles + duration. Emit per-ticker status line.

**Why progress emission (advisor UX fix)**: `/tin-hot 10` worst case = 10 × ~3-5 min = 30-50 min blocking. Without progress emission, user watches frozen prompt. Per-ticker line gives heartbeat — user knows pipeline is running, not stuck.

## Step 4 — Final summary

```
✅ /tin-hot {N} hoàn tất:
  - {M} mã đã dispatch pipeline
  - {total_articles} bài đã generate
  - {failures} mã fail (xem log nếu có)

Xem feed: http://localhost:5176/feed
```

## Hard rules

- N must be 1-10. Reject 0, 11+, or non-integer.
- KHÔNG dispatch parallel — DB write safety.
- Ticker fail (vd Master gates reject all briefs) → skip + continue, log error vào /tmp/tin-hot-errors.json.
- Empty universe intersect (0 mã trong universe sau filter) → report "Không có mã hot nào trong universe — bỏ qua dispatch" + exit gracefully.
- Idempotent: nếu cùng ticker đã chạy `/tin` trong 60 phút qua → skip + report "Đã có bài VCB 30 phút trước, không re-run". Check qua `db.recent_generated_news(ticker, limit=1)` published_at.
```

### 7.3 `tests/test_finpath_top_movers.py` (NEW)

```python
"""Tests for lib/finpath_top_movers — fetch + filter + compute + intersect + dedup."""
from __future__ import annotations
import pytest
from unittest.mock import MagicMock, patch
from lib.finpath_top_movers import (
    fetch_stocks_overview, apply_default_filters, compute_top_lists,
    intersect_universe, dedup_tickers, HotTicker, _normalize,
)


SAMPLE_RAW_STOCK = {
    "c": "VCB", "dcp": 2.5, "dc": 1500, "dvp": 50.0, "dv": 1000000,
    "mc": 500_000_000_000, "a5v": 50_000_000_000, "p": 92500, "st": "S",
}


def test_normalize_maps_fields():
    out = _normalize(SAMPLE_RAW_STOCK)
    assert out["code"] == "VCB"
    assert out["dayChangePercent"] == 2.5
    assert out["secType"] == "S"


def test_apply_default_filters_excludes_low_liquidity():
    stocks = [
        {"code": "A", "secType": "S", "marketCap": 1000, "avgDay5Value": 1_000_000_000, "price": 10},  # 1 tỷ < 10 tỷ
        {"code": "B", "secType": "S", "marketCap": 500, "avgDay5Value": 50_000_000_000, "price": 20},  # 50 tỷ OK
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


def test_compute_top_lists_n_4():
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


def test_intersect_universe_filters():
    lists = {
        "price_increment": [HotTicker("VCB", 100, 2, 50, "price_increment", 1),
                            HotTicker("XYZ", 50, 3, 60, "price_increment", 2)],
        "price_decrement": [], "volume_explosion": [], "depleted_supply": [],
    }
    universe = ["VCB", "TCB"]
    out = intersect_universe(lists, universe)
    assert [t.code for t in out["price_increment"]] == ["VCB"]


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
    # A should have 2 categories
    a_entry = next(t for t in deduped if t[0] == "A")
    assert "price_increment" in a_entry[1]
    assert "volume_explosion" in a_entry[1]


def test_fetch_stocks_overview_calls_correct_url():
    with patch("lib.finpath_top_movers.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"stocks": [SAMPLE_RAW_STOCK]}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        stocks = fetch_stocks_overview()
        mock_get.assert_called_once_with("https://api.finpath.vn/api/stocks/v2/overview", timeout=15)
        assert len(stocks) == 1
        assert stocks[0]["code"] == "VCB"


def test_fetch_stocks_overview_raises_on_network_error():
    with patch("lib.finpath_top_movers.requests.get") as mock_get:
        mock_get.side_effect = ConnectionError("network down")
        with pytest.raises(ConnectionError):
            fetch_stocks_overview()
```

## 8. Pipeline integration

### Idempotency check

Trước khi dispatch /tin per ticker, check published_at gần nhất:

```python
recent = db.recent_generated_news(ticker, limit=1)
if recent and _within_60_min(recent[0]["published_at"]):
    # Skip — đã có bài 60 phút trước
    skipped.append(ticker)
    continue
```

→ Tránh dispatch double-write nếu user run `/tin-hot` 2 lần gần nhau.

**Advisor edge case note**: `recent_generated_news` queries `generated_news WHERE status='published'`. Nếu pipeline V5.1 chạy nhưng Story Editor uncapped picks 0 briefs → KHÔNG persist row vào `generated_news` → `recent` empty → idempotency check pass → re-dispatch allowed. Đây là behavior MONG MUỐN (0-article runs không block retries). Em verified qua `lib/pipeline_db.py:recent_generated_news`.

Nếu sau này thay đổi pipeline để persist row "0-article run marker" → idempotency window sẽ block re-dispatch sai logic. Hiện tại safe.

### Failure handling

Pipeline V5.1 fail (vd Master gates reject) → log error vào `/tmp/tin-hot-errors.json` + continue next ticker. KHÔNG halt batch.

```python
errors = []
try:
    dispatch_pipeline(ticker)
    success.append(ticker)
except Exception as e:
    errors.append({"ticker": ticker, "error": str(e)})
    continue

# At end
with open("/tmp/tin-hot-errors.json", "w") as f:
    json.dump(errors, f, ensure_ascii=False, indent=2)
```

## 9. File touch list

| File | Action | Lines est |
|---|---|---|
| `lib/finpath_top_movers.py` | NEW | ~180 |
| `tests/test_finpath_top_movers.py` | NEW | ~200 |
| `.claude/commands/tin-hot.md` | NEW | ~150 |
| (Optional) `.claude/skills/finpath-newsroom-orchestrator/SKILL.md` | MODIFY | +20 (mention /tin-hot entry point) |
| `CLAUDE.md` | MODIFY | +20 (new command section) |

Total: ~3 new + ~2 modify ≈ 550-650 LOC. Smallest spec trong 4 subsystem.

## 10. Conflicts with Subsystem B/C

**No conflicts**. Subsystem A là entry-point layer trên pipeline V5.1 (B + C đã build). A KHÔNG modify:
- Format Director (Spec B §8)
- Headline Craft (Spec C §9)
- Pipeline orchestrator workflow
- Schema validation
- Master agents

A chỉ thêm:
- 1 module Python tính top movers
- 1 command file `tin-hot.md`
- 1 CLAUDE.md section

## 11. Testing strategy

### Unit tests `tests/test_finpath_top_movers.py`
- `_normalize` field mapping
- `apply_default_filters` excludes low liquidity / zero price / non-S secType
- `compute_top_lists` produces correct order, raises on invalid N
- `intersect_universe` filters correctly
- `dedup_tickers` keeps first-seen order, merges categories
- `fetch_stocks_overview` mocked HTTP correct URL + raises on network error

### Integration test
- Run `lib/finpath_top_movers.py` against real API (manual smoke, not CI) → verify 4 lists non-empty
- Confirm field mapping correct (sample 1-2 tickers vs Finpath web UI)

### E2E test
- Run `/tin-hot 4` → verify reports pre-flight summary + dispatches sequential + collects errors

## 12. Rollout phases

### Phase 1 — Python helper (Day 1)
- `lib/finpath_top_movers.py` + unit tests
- Manual smoke test against real API

### Phase 2 — Command file + integration (Day 2)
- `.claude/commands/tin-hot.md`
- Test `/tin-hot 4` end-to-end against staging DB

### Phase 3 — Documentation (Day 2)
- CLAUDE.md section
- Update orchestrator SKILL.md if applicable

Estimated: ~2-3 days. Smallest subsystem.

## 13. Open questions / deferred

1. **Cron auto-trigger** — Defer Phase 2. Hooks GitHub Actions or local launchd `15:30 hàng ngày → /tin-hot 4`.
2. **Time range filter** (1 giờ vs 1 ngày vs hôm nay) — Currently hard-coded default "Hôm nay" per Finpath web. Tune sau pilot.
3. **Volume explosion threshold** — Currently no minimum (just sort desc). Có thể add filter `dayVolPercent > 100` để chỉ pick "thực sự bùng nổ". Tune post-launch.
4. **Idempotency window** — 60 min default. Tune (30/60/120?) per user feedback.
5. **Universe expansion** — Khi roadmap expand universe (vd thêm KCN, retail) — `/tin-hot` auto pick up vì intersect dynamic.
6. **Failure threshold** — Hiện skip ticker fail và continue. Có thể add "stop on 3 fails in a row" để abort batch nếu API/pipeline broken.
7. **Filter customization** — Defer. User-customizable `marketcap` / `liquidity` / `timeframe` args sau khi defaults validate.

## 14. Spec changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-05-12 | Initial draft. `/tin-hot N` command (default 4, max 10). 4 lists from Finpath public API (`/api/stocks/v2/overview`) → default filters (top 100 marketCap, ≥10 tỷ liquidity, secType S, price > 0) → top N per category → intersect FULL_UNIVERSE → dedup → sequential dispatch pipeline V5.1 per ticker. Idempotency 60-min window. No conflicts with Spec B/C. |
| 1.1 | 2026-05-12 | Advisor review patches: §2 + §7.2 intersect ORDER reversed (intersect TRƯỚC compute top N — fixes yield 0-1 to reliable 4-10 per category); §7.1 FinpathAPI.get_overview() method instead of standalone requests.get (consistency); §7.2 Step 3 per-ticker progress emission (UX fix for long runs); §6 depleted_supply note explaining replicate-source-of-truth; §8 idempotency edge case verified for 0-article runs. |
