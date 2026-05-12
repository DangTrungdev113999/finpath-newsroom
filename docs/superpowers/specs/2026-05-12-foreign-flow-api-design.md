# Foreign Flow API — Design Spec V1.1

**Date**: 2026-05-12 PM (V1.0 initial), 2026-05-12 PM (V1.1 — simplify to on-demand tool)
**Author**: Brainstormed with em (Claude) via /superpowers:brainstorming
**Status**: Draft — pending user review before plan
**Subsystem**: G (Foreign Flow API) — from session 2026-05-12 PM feedback
**Depends on**: Spec F `2026-05-12-universe-expansion-kb-optional-design.md` V1.0.1 (Finpath API integration pattern)
**Coupled with**: Spec A — NO PATCH NEEDED (V1.1 reverted: foreign flow is on-demand tool, not /tin-hot enrichment)

---

## ⚠ V1.1 PATCH (2026-05-12 PM) — SIMPLIFY to on-demand tool

V1.0 over-designed pipeline enrichment + Editor V1 stamp + dispatcher pre-fetch + Master Step 4.5. User feedback rejected this approach:

> "data realtime, hard code làm gì, cần data thì call api thôi, quan trọng bạn define call khi nào, ai call"
>
> "các master phải tự biết khi nào cần call api để lấy data chứ?"
>
> "cái api này mục đích chính là giống như các api khác để master call data thôi mà, đâu phải lúc nào cũng call đâu, bài nào cần thì mới call"

### Patch summary

Foreign flow API = **on-demand tool** trong toolbox của Master + Story Editor, giống `get_income_statement` / `get_bank_ratios`. KHÔNG pipeline-level enrichment. KHÔNG auto-fetch trong dispatcher. Agents tự judge khi nào cần call.

### Patch 1 — REMOVE pipeline enrichment (overrides §7)

- ❌ DROP: `/tin-hot N` auto-enrichment top 30
- ❌ DROP: `lib/foreign_flow.py` (top compute module orphaned)
- ❌ DROP: Editor V1 stamp `foreign_flow` field in crawl_log
- ❌ DROP: Dispatcher pre-fetch `enrich_top_movers()`
- ❌ DROP: Spec A V1.2 PATCH (no /tin-hot change needed)
- ✅ KEEP: `lib/finpath_api.py` 3 new methods (rooms + roomstatistics + roombars)
- ✅ KEEP: SQLite cache hybrid TTL (15min / 1h / 6h)

### Patch 2 — REMOVE Master Step 4.5 (overrides §9.3)

- ❌ DROP: Master workflow "Step 4.5 Foreign flow check"
- ❌ DROP: Editor V1 brief field `enrichment.foreign_flow`
- ❌ DROP: pipeline_log `step_1_5_market_snapshot.foreign_flow` nested field
- ✅ NEW: Master + Story Editor **judgment guide** — "khi nào tôi nên call foreign API"

### Patch 3 — Judgment guides replace prescriptive steps

Master + Story Editor skill thêm reference file `references/foreign-flow-when-to-call.md`. KHÔNG prescriptive "must call". Chỉ guide WHEN call would add value, examples + anti-patterns.

Story Editor judgment:
- Khi nào: stance signal cần institutional confirmation (vd "VHM tăng giá nhưng tin đồn yếu — check NN flow xác nhận"). Stance KHÔNG bắt buộc call.
- Decision: free-form judgment, không pattern fixed.

Master judgment:
- Khi nào: body cần cite institutional signal cụ thể HOẶC brief mention NN trend HOẶC angle về money flow.
- Decision: free-form judgment, không pattern fixed.
- Cite format: bold số tỷ + period clear ("**NN bán ròng 85,78 tỷ phiên 12/5**").

### Patch 4 — File impact reduction

| Aspect | V1.0 | V1.1 |
|---|---|---|
| NEW files | 16 | **8** (drop lib/foreign_flow.py + 7 redundant docs) |
| MODIFY files | 15 | **3** (only lib/finpath_api.py + 1 SKILL.md per skill that uses) |
| Total impact | 31 | **11** |
| Effort | 2-3 ngày | **1 ngày** với subagent parallel |

### Patch 5 — Spec changelog V1.1 entry

```
- V1.1 (2026-05-12 PM) — SIMPLIFY to on-demand tool (user pivot)
  - Foreign flow API = tool trong toolbox, not pipeline enrichment
  - DROP /tin-hot auto-enrichment, Editor V1 stamp, Master Step 4.5
  - DROP lib/foreign_flow.py top compute (orphaned)
  - DROP Spec A V1.2 PATCH (no /tin-hot change)
  - KEEP 3 API methods + SQLite cache hybrid TTL
  - ADD judgment guides for Master + Story Editor (when to call)
  - File impact: 31 → 11
  - Rationale: User feedback "master tự biết khi nào cần call api như các api khác"
```

### Files actually needed for V1.1 (final list)

**NEW**:
- `lib/finpath_api.py` extension (3 methods, +120 lines — KEEP)
- `lib/migrations/2026-05-12-add-finpath-foreign-cache.sql` (+30 lines — KEEP)
- `.claude/skills/finpath-newsroom-story-editor/references/foreign-flow-when-to-call.md` (~80 lines)
- `.claude/skills/finpath-newsroom-master-{bank,ck,bds,oilgas,logistics,fb,apparel,retail,seafood,defensive}/references/foreign-flow-when-to-call.md` (~80 lines × 10 = ~800 lines duplicate)
- `tests/test_finpath_api_foreign.py` (~150 lines)
- `tests/test_foreign_flow_judgment.py` (~100 lines — agent-level judgment validation, not top compute)

**MODIFY**:
- `lib/finpath_api.py` (+120 lines extension)
- `.claude/skills/finpath-newsroom-story-editor/SKILL.md` (+5 lines reference load)
- 10× `.claude/skills/finpath-newsroom-master-{sector}/SKILL.md` (+5 lines reference load each)

**Total V1.1**: 13 NEW + 11 MODIFY = ~24 file. Reduced from V1.0 31 → 24 actual.

### What V1.0 sections to IGNORE (overridden by V1.1)

When Plan G executor reads spec, IGNORE these V1.0 sections:
- §6 `lib/foreign_flow.py` module — DROPPED
- §7 `/tin-hot N` enrichment flow — DROPPED
- §8.3 Brief schema `enrichment` field — DROPPED
- §9.3 Master Step 4.5 — DROPPED, replaced with judgment guide
- §10 Pipeline log observability `step_1_5_market_snapshot.foreign_flow` — DROPPED
- §11 Spec A V1.2 PATCH — CANCELLED

Read §4, §5, §12 (edge cases), §14 (testing API methods) — these remain valid.

---

## V1.1 Architecture (simplified)

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: API Client (lib/finpath_api.py EXTEND)         │
│   - get_foreign_rooms()                                 │
│   - get_foreign_roomstatistics(code, type)              │
│   - get_foreign_roombars(code)                          │
│   - SQLite cache hybrid TTL (15min / 1h / 6h)           │
└─────────────────────────────────────────────────────────┘
                          ↓
                  (No middle layer)
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Agent on-demand calls                          │
│   - Master sectors: call when body needs NN cite        │
│   - Story Editor: call when stance needs institutional  │
│     signal confirmation                                 │
│   - Both: free-form judgment, no prescribed pattern     │
└─────────────────────────────────────────────────────────┘
```

Tương tự pattern hiện tại với `get_bank_ratios()` — Master Bank gọi khi cần ratios, không pipeline auto-stamp.

---

## V1.1 Story Editor judgment guide

`references/foreign-flow-when-to-call.md` content draft:

```markdown
# Foreign Flow — Khi nào Story Editor call API?

> Free-form judgment. KHÔNG prescriptive "must call". Guide WHEN call adds stance signal.

## Call API khi:

1. **Ticker đang Hot (tăng/giảm mạnh)** + stance unclear → call `get_foreign_rooms()` lookup ticker dnva
   - Confirms institutional direction (top_buy = bullish confirm, top_sell = caution)

2. **Brief candidate "ai đẩy giá"** angle → call để check NN sentiment
   - Vd "VHM tăng kịch trần — institutional có theo không?"

3. **Sector cycle inflection** + need confirmation → call multiple peers
   - Vd Bank cluster tăng đồng loạt → check NN flow Bank tổng thể

## KHÔNG call khi:

- Stance đã clear từ 7-layer khác (don't waste API call)
- Brief về fundamental sự kiện (Q1 report, BCTC) — NN flow không relevant
- Ticker không Hot + không price action — NN flow signal weak

## Cite format trong stance_directive

Nếu call → add to `key_evidence`:
- "NN bán ròng 85,78 tỷ phiên 12/5" (cụ thể số + period)
- "Top 30 NN bán ròng" (rank context)
- Period tuỳ depth: 1D cho intraday, 1W cho trend
```

---

## V1.1 Master judgment guide (10 copies, 1 per master)

`references/foreign-flow-when-to-call.md` content draft:

```markdown
# Foreign Flow — Khi nào Master call API?

> Free-form judgment. Same pattern as get_income_statement / get_bank_ratios — call when body needs the data.

## Call API khi viết bài:

1. **Brief angle mention NN flow** (vd "VHM giảm giá khi NN bán mạnh")
   - MUST cite số liệu cụ thể trong body
   - Call: `api.get_foreign_rooms()` → lookup ticker dnva

2. **Body cần institutional context** (vd "ai đẩy giá hôm nay?")
   - Call để answer question concretely

3. **Cite multi-period trend** (vd "NN bán ròng 5 phiên liên tiếp")
   - Call: `api.get_foreign_roomstatistics(ticker, period="1W")`

4. **Time series narrative** (vd "30 ngày qua institutional sentiment")
   - Call: `api.get_foreign_roombars(ticker)` for chart-like trend

## KHÔNG call khi:

- Bài về fundamental (lãi/lỗ/ROE) — NN flow off-topic
- Format flash_qa (100-150 từ ngắn) — không đủ space cite extra signal
- Brief KHÔNG mention NN + angle khác — không force fit

## Cite format

- Bold số tỷ: `**NN bán ròng 85,78 tỷ**`
- Format VN: 85780000000 → "85,78 tỷ"
- Period clear: "phiên 12/5" / "tuần qua" / "30 ngày"

## Data trail entry

```yaml
data_trail:
  - source: "Finpath_API/foreign-rooms"
    fetched: "dnva = -85780000000 (today net VND)"
    purpose: "cite NN sell pressure"
    supports_argument: "Opening question paragraph"
```

## Anti-patterns

- ❌ Cite NN khi không relevant tới insight ("force fit")
- ❌ "NN đang có vẻ bán" (vague — phải số cụ thể)
- ❌ "85.78 billion" (Anh — phải VN "85,78 tỷ")
```

---

## 1. Goal

Extend `lib/finpath_api.py` thêm 3 method foreign flow (khối ngoại mua/bán ròng) — data source cho 3 use case:

1. **`/tin-hot N` auto-enrichment** — sau khi compute top 4 nhóm Hot, cross-check với top 30 NN mua/bán → flag `foreign_status` + `dnva` value → Story Editor + Master tự đào sâu.
2. **Story Editor stance judgment** — NN flow là 1 signal trong 7-layer nội lực (vd "MWG tăng giá + NN mua ròng 200 tỷ 5 phiên = strong bullish").
3. **Master data trail** — cite NN flow concrete trong body (vd "**NN bán ròng 85,78 tỷ phiên 12/5**").

Sau spec này: pipeline V5.1.3 có signal NN flow đầy đủ ở 3 entry point. Hot Ticker dispatch tự enrich, Story Editor + Master tự call drilldown khi cần.

## 2. Problem statement (từ feedback 2026-05-12 PM)

User feedback:

> "ở khi call ở finpath thêm api khối ngoại này vào [screenshot Cổ phiếu nổi bật → tab Nước ngoài]"
>
> "api này cũng dùng để làm data cho các agent khác đào sâu viết bài đó nhé"
>
> "gộp mịa vào tin hot đi, lúc chạy xem top 4 kia có nằm trong top nn không, nếu có thì thêm dữ liệu để viết bài thôi, tách ra vầy không ổn"

Vấn đề:

1. **Thiếu signal foreign flow** — Master + Story Editor không có cách query NN mua/bán ròng dù đây là signal cực mạnh (institutional money flow direction).
2. **Hot Ticker enrich gap** — `/tin-hot N` chỉ biết "top tăng/giảm giá" mà KHÔNG biết NN có cùng phe không. Master viết bài thiếu chiều sâu.
3. **Stance signal weak** — 7-layer nội lực mention "vĩ mô" nhưng không có concrete tín hiệu institutional sentiment.

## 3. Out of scope (defer)

- **Phân tích insider trading** (`/api/stocks/insider-transactions/{code}`) — defer V5.2.
- **Sector flow aggregation** — chỉ per-ticker MVP, sector-level flow defer.
- **Real-time WebSocket updates** — pipeline trigger-based, không cần streaming.
- **Top NN by sector / market cap segmentation** — V5.1.3 dùng top 30 absolute.
- **Foreign holding ratio** — `/api/stocks/shareholderstructure/{code}` đã có sẵn ở Spec hiện tại. Spec G chỉ focus flow.

## 4. Architecture overview

### 3-layer architecture

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: API Client (lib/finpath_api.py EXTEND)         │
│   - get_foreign_rooms()                                 │
│   - get_foreign_roomstatistics(code, type)              │
│   - get_foreign_roombars(code)                          │
│   - SQLite cache hybrid TTL                             │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Top NN compute (lib/foreign_flow.py NEW)       │
│   - compute_top_foreign_buy(n=30): top mua ròng 1D     │
│   - compute_top_foreign_sell(n=30): top bán ròng 1D     │
│   - check_ticker_foreign_status(ticker):                │
│       → top_buy | top_sell | normal | no_data           │
│   - enrich_top_movers(tickers): bulk enrichment         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 3: Pipeline integration                           │
│   3a. /tin-hot AUTO-enrichment                          │
│       - After Hot Ticker compute top 4 nhóm             │
│       - Bulk enrich → crawl_log foreign_flow field      │
│                                                         │
│   3b. ON-DEMAND drilldown                               │
│       - Story Editor: get_foreign_roomstatistics()      │
│         cho stance judgment 7-layer                     │
│       - Master: cite trong body khi flag != normal      │
└─────────────────────────────────────────────────────────┘
```

### Key changes vs V5.1.2

| Aspect | V5.1.2 | V5.1.3 (this spec) |
|---|---|---|
| Foreign flow data source | None | 3 Finpath endpoints |
| Hot Ticker enrichment | KHÔNG có | AUTO-enrich top movers với NN status |
| Story Editor stance signals | 7-layer (no NN) | 7-layer + NN flow signal |
| Master data trail sources | API + KB + web | + Foreign flow API |
| Pipeline log observability | step_1_5 ticker_status only | step_1_5 + foreign_flow nested |

## 5. API endpoints + Caching

### 5.1 Finpath endpoints

| Endpoint | Returns | TTL | Cache key |
|---|---|---|---|
| `GET /api/stocks/v2/rooms` | All 1902 records snapshot (stocks + warrants) với 6 periods foreign data | 15 min | `"rooms"` (global single row) |
| `GET /api/stocks/roomstatistics/{code}?type=<period>` | Per-ticker NN flow stats theo period (1D/1W/1M/3M/6M/1Y) | 1 h | `f"roomstat:{code}:{type}"` |
| `GET /api/stocks/roombars/{code}` | Time series daily NN flow chart-like | 6 h | `f"roombars:{code}"` |

Periods supported (param `type`):
- `1D` — today only
- `1W` — last 5 trading days
- `1M` — last month
- `3M` — last 3 months
- `6M` — last 6 months
- `1Y` — last year

### 5.2 Response shape `/v2/rooms`

```json
{
  "data": {
    "rooms": [
      {
        "c": "VHM",                 // ticker
        "sn": "Vinhomes",            // VN name
        "p": 50500,                  // current price
        "e": "HOSE",                 // exchange
        "ste": "S",                  // S = Stock, W = Warrant (filter "S" only)
        "td": "12/05/2026",          // trading date
        "t": "10:35:00",             // last update time
        // === Foreign trading fields ===
        "dnva": -85780000000,        // today NET VALUE amount (VND) [negative = bán ròng]
        "dnv": -200000,              // today NET volume (số CP)
        "dbva": 12000000000,         // today bought volume amount
        "dbv": 50000,                // today bought volume
        "dsva": 97780000000,         // today sold volume amount
        "dsv": 250000,               // today sold volume
        // Same prefix for week (w*), month (m*), 3-month (m3*), 6-month (m6*), year (y*)
        "wnva": -340000000000,       // week net VND
        "mnva": -1200000000000,      // month net VND
        "m3nva": 50000000000,
        "m6nva": 200000000000,
        "ynva": -500000000000
      }
    ]
  }
}
```

**Field naming convention**:
- Prefix: `d` (today) / `w` (week 5d) / `m` (month) / `m3` (3M) / `m6` (6M) / `y` (year)
- Suffix:
  - `bv` = bought volume (số CP)
  - `bva` = bought volume amount (VND)
  - `sv` / `sva` = sold (bán)
  - `nv` / `nva` = NET (mua ròng) — negative = bán ròng
  - `tv` / `tva` = total

### 5.3 SQLite cache schema

```sql
-- Migration: lib/migrations/2026-05-12-add-finpath-foreign-cache.sql

CREATE TABLE IF NOT EXISTS finpath_foreign_cache (
    cache_key TEXT PRIMARY KEY,           -- "rooms" | "roomstat:VHM:1W" | "roombars:VHM"
    endpoint TEXT NOT NULL,                -- "/v2/rooms" | "/roomstatistics" | "/roombars"
    payload JSON NOT NULL,                 -- raw API response (compressed-able)
    fetched_at TIMESTAMP NOT NULL,         -- UTC ISO format
    ttl_seconds INTEGER NOT NULL           -- 900 | 3600 | 21600
);

CREATE INDEX idx_foreign_cache_fetched ON finpath_foreign_cache(fetched_at);
```

### 5.4 lib/finpath_api.py extension

```python
# Add to FinpathAPI class

def get_foreign_rooms(self) -> list[dict]:
    """All 1902 records foreign flow snapshot. Cached 15 min in SQLite.

    Returns list of room dict with foreign trading fields.
    Filter ste == 'S' for stocks only (1902 → ~700 mã after filter).
    """
    payload = self._cache_get("rooms", endpoint="/v2/rooms", ttl=900)
    if payload is None:
        payload = self._fetch_api("/api/stocks/v2/rooms")
        self._cache_set("rooms", endpoint="/v2/rooms", payload=payload, ttl=900)
    return payload.get("data", {}).get("rooms", [])

def get_foreign_roomstatistics(self, ticker: str, period: str = "1D") -> dict:
    """Per-ticker NN flow statistics for given period.

    period ∈ {1D, 1W, 1M, 3M, 6M, 1Y}
    Cached 1 hour per (ticker, period).
    """
    assert period in {"1D", "1W", "1M", "3M", "6M", "1Y"}
    cache_key = f"roomstat:{ticker}:{period}"
    payload = self._cache_get(cache_key, endpoint="/roomstatistics", ttl=3600)
    if payload is None:
        payload = self._fetch_api(
            f"/api/stocks/roomstatistics/{ticker}",
            params={"type": period}
        )
        self._cache_set(cache_key, endpoint="/roomstatistics", payload=payload, ttl=3600)
    return payload.get("data", {})

def get_foreign_roombars(self, ticker: str) -> list[dict]:
    """Time series daily NN flow bars. Cached 6 hours."""
    cache_key = f"roombars:{ticker}"
    payload = self._cache_get(cache_key, endpoint="/roombars", ttl=21600)
    if payload is None:
        payload = self._fetch_api(f"/api/stocks/roombars/{ticker}")
        self._cache_set(cache_key, endpoint="/roombars", payload=payload, ttl=21600)
    return payload.get("data", {}).get("bars", [])

def _cache_get(self, cache_key: str, endpoint: str, ttl: int) -> dict | None:
    """SQLite cache lookup with TTL check."""
    cur = self.db.conn.execute(
        "SELECT payload, fetched_at, ttl_seconds FROM finpath_foreign_cache WHERE cache_key = ?",
        (cache_key,)
    )
    row = cur.fetchone()
    if not row:
        return None
    fetched_at = datetime.fromisoformat(row["fetched_at"])
    age = (datetime.now(timezone.utc) - fetched_at).total_seconds()
    if age > row["ttl_seconds"]:
        # Stale — still return as fallback if API fails
        self._stale_payloads[cache_key] = json.loads(row["payload"])
        return None
    return json.loads(row["payload"])

def _cache_set(self, cache_key: str, endpoint: str, payload: dict, ttl: int) -> None:
    """SQLite cache upsert."""
    self.db.conn.execute("""
        INSERT INTO finpath_foreign_cache (cache_key, endpoint, payload, fetched_at, ttl_seconds)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(cache_key) DO UPDATE SET
            payload = excluded.payload,
            fetched_at = excluded.fetched_at,
            ttl_seconds = excluded.ttl_seconds
    """, (cache_key, endpoint, json.dumps(payload), datetime.now(timezone.utc).isoformat(), ttl))
    self.db.conn.commit()

def _fetch_api(self, path: str, params: dict | None = None) -> dict:
    """HTTP GET with timeout + graceful degradation."""
    try:
        r = requests.get(
            f"{self.base_url}{path}",
            params=params,
            timeout=self.timeout,
            headers={"client-type": "web", "origin": "https://finpath.vn"}
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        # Try fallback stale cache
        if path in self._stale_payloads:
            self._log_warning(f"API fail {path}, using stale cache: {e}")
            return self._stale_payloads[path]
        raise RuntimeError(f"Finpath API {path} failed: {e}")
```

### 5.5 Graceful degradation

| Scenario | Behavior |
|---|---|
| Cache hit + fresh | Return cached |
| Cache miss | Fetch API → cache → return |
| Cache stale + API success | Refresh cache → return new |
| Cache stale + API fail | Return stale + log warning |
| Cache empty + API fail | Raise RuntimeError (fail-loud) |

## 6. Top NN compute logic

### lib/foreign_flow.py (NEW module)

```python
"""Foreign flow top compute + ticker status check."""
from __future__ import annotations
from typing import Literal, TypedDict
from lib.finpath_api import FinpathAPI

ForeignStatus = Literal["top_buy", "top_sell", "normal", "no_data"]

class ForeignFlowEnrichment(TypedDict):
    status: ForeignStatus
    dnva: int        # today net VND (negative = bán ròng)
    dnv: int         # today net volume (số CP)
    ticker: str

TOP_N_DEFAULT = 30   # Top 30 NN mua + top 30 NN bán

def compute_top_foreign_buy(rooms: list[dict], n: int = TOP_N_DEFAULT) -> set[str]:
    """Return set of top N tickers by today net VALUE bought (positive dnva)."""
    stocks = [r for r in rooms if r.get("ste") == "S" and r.get("dnva", 0) > 0]
    sorted_stocks = sorted(stocks, key=lambda r: r["dnva"], reverse=True)
    return {r["c"] for r in sorted_stocks[:n]}

def compute_top_foreign_sell(rooms: list[dict], n: int = TOP_N_DEFAULT) -> set[str]:
    """Return set of top N tickers by today net VALUE sold (most negative dnva)."""
    stocks = [r for r in rooms if r.get("ste") == "S" and r.get("dnva", 0) < 0]
    sorted_stocks = sorted(stocks, key=lambda r: r["dnva"])  # ascending = most negative first
    return {r["c"] for r in sorted_stocks[:n]}

def check_ticker_foreign_status(
    ticker: str, rooms: list[dict],
    top_buy_set: set[str], top_sell_set: set[str]
) -> ForeignFlowEnrichment:
    """Single ticker lookup. Use bulk enrich_top_movers for batch."""
    flow = next((r for r in rooms if r["c"] == ticker and r.get("ste") == "S"), None)
    if not flow:
        return {"status": "no_data", "dnva": 0, "dnv": 0, "ticker": ticker}

    if ticker in top_buy_set:
        status = "top_buy"
    elif ticker in top_sell_set:
        status = "top_sell"
    else:
        status = "normal"

    return {
        "status": status,
        "dnva": flow.get("dnva", 0),
        "dnv": flow.get("dnv", 0),
        "ticker": ticker,
    }

def enrich_top_movers(
    api: FinpathAPI, tickers: list[str]
) -> dict[str, ForeignFlowEnrichment]:
    """Bulk enrichment for /tin-hot top movers. Single rooms API call."""
    rooms = api.get_foreign_rooms()
    top_buy = compute_top_foreign_buy(rooms)
    top_sell = compute_top_foreign_sell(rooms)
    return {
        t: check_ticker_foreign_status(t, rooms, top_buy, top_sell)
        for t in tickers
    }
```

### 6.1 Edge cases

| Case | Handling |
|---|---|
| `dnva == 0` (no NN trading) | status = "normal" (even if in top 30 list, can't happen since top 30 filter > 0 hoặc < 0) |
| Ticker là chứng quyền (`ste == "W"`) | Skip — Hot Ticker pre-filter stocks only |
| Ticker không trong `rooms` (newly listed) | status = "no_data" |
| Sàn đóng (weekend, holiday) | `dnva` = 0 cho tất cả → top_buy/top_sell sets EMPTY → all status "normal" |
| Less than 30 tickers có positive dnva | top_buy_set ngắn hơn 30 (no padding) |

## 7. `/tin-hot N` enrichment flow

### 7.1 Integration with Hot Ticker (Spec A V1.1)

Spec A V1.1 flow hiện tại:

```
/tin-hot 3
   ↓
1. Compute top 4 nhóm (tăng/giảm/bùng nổ/cạn cung) → 12 ticker
2. Intersect Finpath universe (139 mã after Spec F V5.1.3)
3. Sequential dispatch pipeline per ticker
```

V5.1.3 thay đổi step 2.5 (giữa intersect và dispatch):

```
/tin-hot 3
   ↓
1. Compute top 4 nhóm → 12 ticker
2. Intersect Finpath universe (139 mã)
3. ★ NEW: enrich_top_movers(api, 12_tickers) — single rooms API call
   → returns dict[ticker → ForeignFlowEnrichment]
4. Stamp foreign_flow field vào crawl_log per ticker
5. Sequential dispatch pipeline per ticker (Story Editor + Master see enrichment)
```

### 7.2 crawl_log row schema extension

```yaml
crawl_log row:
  ticker: "VHM"
  source_url: "..."
  hot_nhom: "tang_gia"               # which Hot Ticker nhóm
  hot_rank: 1                         # rank within nhóm
  # V5.1.2 fields (Spec F)
  sector_code: "vic3"
  sector_name: "BDS VIC3"
  master_route: "bds"
  # NEW V5.1.3 (Spec G)
  foreign_flow:
    status: "top_sell"                # top_buy | top_sell | normal | no_data
    dnva: -85780000000                # today net VND
    dnv: -200000                      # today net volume
```

### 7.3 Sample enrichment data

`/tin-hot 3` output example (12 ticker enriched):

| Ticker | Nhóm | Rank | Foreign status | dnva |
|---|---|---|---|---|
| VHM | tăng_giá | 1 | **top_sell** | -85.78 tỷ |
| FPT | tăng_giá | 2 | top_buy | +120 tỷ |
| HPG | tăng_giá | 3 | normal | -2 tỷ |
| ... | ... | ... | ... | ... |

→ Story Editor thấy VHM tăng giá nhưng NN bán ròng top → flag "ai đang đẩy giá khi NN rút?" → stance caution.

→ FPT tăng giá + NN mua top → confirm bullish → stance positive high confidence.

## 8. Story Editor stance integration

### 8.1 Foreign flow signal trong 7-layer

Spec F + B đã define 7-layer nội lực. NN flow là **signal cross-cutting** — không phải layer mới mà là input cho judgment của các layer:

- **Tài chính**: NN mua ròng = institutional confidence in fundamentals
- **Sector cycle**: NN mua/bán sector-wide = cycle inflection
- **Vĩ mô**: NN flow direction = capital allocation signal

### 8.2 references/foreign-flow-signal.md (Story Editor skill NEW)

`.claude/skills/finpath-newsroom-story-editor/references/foreign-flow-signal.md`:

```markdown
# Foreign Flow Signal — Story Editor stance judgment

> Loaded from `Skill: finpath-newsroom-story-editor`. Apply khi brief có `enrichment.foreign_flow`.

## Signal matrix 4-quadrant

|  | Price up | Price down |
|---|---|---|
| **NN top_buy** | STRONG BULLISH — institutional confirm | "Ai đang đặt cược ngược?" — positive medium |
| **NN top_sell** | "Ai đẩy giá khi NN rút?" — caution flag | STRONG BEARISH — institutional confirm sell |
| **NN normal** | Price signal only (no NN confirmation) | Price signal only |
| **NN no_data** | Skip foreign signal | Skip foreign signal |

## Stance directive integration

Khi NN signal strong (top_buy / top_sell):
- Add to `stance_directive.key_evidence` array
- Format: "NN [mua/bán] ròng [X] tỷ phiên [date]"
- Cite specific dnva value (do NOT round)

Khi NN signal contradicts price (vd top_sell + price up):
- Stance confidence DROP (high → medium)
- `stance_directive.reason` MUST mention contradiction explicitly

## Examples

### Case 1: VHM tăng 6,8% + NN bán ròng 85,78 tỷ

```yaml
stance_directive:
  direction: neutral
  confidence: medium
  reason: |
    VHM tăng kịch trần 6,8% phiên 12/5 nhưng khối ngoại bán ròng top
    thị trường (-85,78 tỷ). Tín hiệu CONTRADICT — institutional thoát
    trong khi retail đẩy giá. Cần check WHO đang mua + tin gì làm
    catalyst trước khi confirm direction.
  key_evidence:
    - "NN bán ròng 85,78 tỷ phiên 12/5"
    - "Top 30 NN bán ròng thị trường"
    - "Price +6.8% intraday"
```

### Case 2: FPT tăng + NN mua ròng top

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
    - "Top 30 NN mua ròng thị trường"
    - "Price +5.5% với volume confirm"
```

## Drilldown when needed

Khi enrichment status = "normal" nhưng Story Editor judge cần check NN trend:
- Call `lib.finpath_api.get_foreign_roomstatistics(ticker, period="1W")`
- Period default 1W (smoother signal than 1D)
- Cite period explicitly trong reason ("NN bán ròng 5 phiên liên tiếp 340 tỷ")
```

### 8.3 Brief schema V5.1.3 extension

Story Editor brief V5.1.2 đã có `stance_directive`. V5.1.3 thêm field `enrichment` (Editor V1 stamp):

```yaml
brief:
  ticker: "VHM"
  deep_question_options: [...]
  angle_label: "..."
  stance_directive: {...}      # V5.1.2 (Spec B)
  enrichment:                   # NEW V5.1.3 (Spec G)
    foreign_flow:
      status: "top_sell"
      dnva: -85780000000
      dnv: -200000
```

## 9. Master data trail integration

### 9.1 When to cite

Master cite NN flow trong body khi:
1. **Brief enrichment status != "normal"** (top_buy / top_sell) — AUTO-include
2. **Story Editor angle_narrative mention NN flow** — follow angle
3. **Master judge cần đào sâu** (free decision) — call `lib.finpath_api.get_foreign_roomstatistics()`

### 9.2 references/foreign-flow-usage.md (Master skill NEW)

Each của 10 master skill có file này (duplicate per CLAUDE.md no-shared rule):

`.claude/skills/finpath-newsroom-master-{sector}/references/foreign-flow-usage.md`:

```markdown
# Foreign Flow Usage — Master

> Loaded when brief có enrichment.foreign_flow HOẶC angle mention NN.

## Cite format (Vietnamese)

- **Bold key number**: `**NN bán ròng 85,78 tỷ**`
- **Format VN**: 85780000000 → "85,78 tỷ" (dấu phẩy thập phân, đơn vị "tỷ")
- **Period clear**: "phiên 12/5" hoặc "tuần qua" tuỳ data source period

## Data trail entry MUST

```yaml
data_trail:
  - source: "Finpath_API/foreign-rooms"
    fetched: "dnva = -85780000000 (today net VND)"
    purpose: "cite NN sell pressure"
    supports_argument: "Opening tension question"
```

## On-demand drilldown

Khi cần history (vd "5 phiên liên tiếp"):

```python
stats = finpath_api.get_foreign_roomstatistics(ticker, period="1W")
# stats trả NN flow per day trong 5 trading days
```

## Examples

### Bullet body listicle

> - **NN bán ròng 85,78 tỷ phiên 12/5**: institutional rút trong khi giá tăng kịch trần, cần check ai đang đẩy giá (retail FOMO? prop trading?)

### Opening paragraph

> Cổ phiếu VHM tăng kịch trần 6,8% phiên 12/5, nhưng **khối ngoại bán ròng 85,78 tỷ** — top 1 thị trường. Câu hỏi: tại sao institutional thoát khi giá đỉnh ATH?

## Anti-pattern

- ❌ "NN có vẻ đang bán" (vague) — phải có CON SỐ cụ thể
- ❌ "85.78 billion VND" (Anh) — phải VN "85,78 tỷ"
- ❌ "NN bán ròng nhiều" (no number) — quantify
```

### 9.3 Master prompt update (each 10 master)

Master SKILL.md thêm reference loader:

```yaml
# Frontmatter
loads_when_relevant:
  - references/foreign-flow-usage.md  # when brief.enrichment.foreign_flow != null
```

Master prompt section (in 9-step workflow):

```
Step 4.5: Foreign flow check
  If brief.enrichment.foreign_flow.status in {"top_buy", "top_sell"}:
    - Load references/foreign-flow-usage.md
    - MUST cite dnva value trong body (≥1 bullet hoặc opening)
    - data_trail entry MUST có source = "Finpath_API/foreign-rooms"
  Else if Master judge cần drilldown:
    - Call lib.finpath_api.get_foreign_roomstatistics(ticker, period)
    - Cite per drilldown response
```

## 10. Pipeline log observability

### 10.1 Schema extension

`step_1_5_market_snapshot` (existing Python helper) extend với foreign flow:

```yaml
step_1_5_market_snapshot:
  model: "python"
  duration_ms: 850
  ticker_status: "Hot"            # V5.0
  day_change_pct: 6.8              # V5.0
  foreign_flow:                    # NEW V5.1.3
    status: "top_sell"
    dnva: -85780000000
    dnv: -200000
    fetched_at_cache: "2026-05-12T10:35:00Z"
    cache_hit: true
```

### 10.2 Editor V1 stamps foreign_flow trong crawl_log

Editor V1 V5.1.3 logic update:

```python
def editor_v1_decide(crawl_row, foreign_enrichment: dict | None = None):
    # ... existing logic (Spec F V5.1.3) ...
    result = {
        "editor_v1_decision": "route_to_story_editor",
        "sector_code": ...,
        "master_route": ...,
    }
    if foreign_enrichment:  # only when /tin-hot dispatched
        result["foreign_flow"] = foreign_enrichment
    return result
```

### 10.3 Master data trail emit

Master pipeline_log entry includes foreign cite count:

```yaml
step_4_master:
  model: opus
  duration_ms: 45000
  tokens: 8500
  format_id_used: "standard_listicle"
  data_trail_count: 12
  foreign_flow_cited: true        # NEW V5.1.3 — true if body cite NN
  foreign_flow_source: "brief_enrichment"  # brief_enrichment | master_drilldown | none
```

## 11. Spec A V1.2 PATCH (Hot Ticker)

Spec A V1.1 cần V1.2 PATCH NOTICE để integrate foreign flow enrichment:

### Required changes (deferred to Plan A patch)

1. **Step 2.5 NEW**: After intersect Finpath universe, call `enrich_top_movers(api, top_4_groups_tickers)`.
2. **crawl_log schema**: Add `foreign_flow` JSON field per row.
3. **Pipeline observability**: Stamp foreign_flow info in `step_1_5_market_snapshot`.
4. **Edge case**: Sàn đóng (weekend) → all status "normal" — Spec A continue dispatch (no skip).
5. **No new command** — `/tin-nn` decision reverted per user feedback ("gộp mịa vào tin hot").

→ Add Spec A V1.2 PATCH NOTICE inline trong Plan A khi execute.

## 12. Edge cases summary

| Case | Behavior |
|---|---|
| API down + cache empty | Fail-loud — pipeline crash with clear error |
| API down + cache stale | Use stale + log warning, pipeline continues |
| Sàn đóng (weekend) | All `dnva == 0` → all status "normal" → no enrichment, pipeline normal |
| Ticker không có trong `/v2/rooms` | status = "no_data", dnva=0, dnv=0 |
| Ticker là warrant (`ste == "W"`) | Pre-filtered by Hot Ticker (stocks only) |
| Less than 30 tickers có `dnva > 0` | `top_buy_set` ngắn hơn 30 — không pad, accept |
| `/tin <SINGLE>` (không phải `/tin-hot`) | KHÔNG auto-enrich. Story Editor + Master có thể call drilldown trực tiếp. |
| Cache TTL hết khi pipeline đang chạy | Use cached value (started run-snapshot consistency), refresh next run |
| Multiple parallel `/tin-hot` runs | SQLite WAL handles concurrent reads. Cache writes serialize via INSERT OR REPLACE. |

## 13. File touch list

### NEW files

```
# Library
lib/foreign_flow.py                                                     (~150 lines)
lib/migrations/2026-05-12-add-finpath-foreign-cache.sql                 (~30 lines)

# Story Editor skill — foreign flow signal
.claude/skills/finpath-newsroom-story-editor/references/foreign-flow-signal.md  (~100 lines)

# 10 Master skills — foreign flow usage (duplicate per CLAUDE.md no-shared)
.claude/skills/finpath-newsroom-master-bank/references/foreign-flow-usage.md            (~80 lines)
.claude/skills/finpath-newsroom-master-ck/references/foreign-flow-usage.md              (~80 lines)
.claude/skills/finpath-newsroom-master-bds/references/foreign-flow-usage.md             (~80 lines)
.claude/skills/finpath-newsroom-master-oilgas/references/foreign-flow-usage.md          (~80 lines)
.claude/skills/finpath-newsroom-master-logistics/references/foreign-flow-usage.md       (~80 lines)
.claude/skills/finpath-newsroom-master-fb/references/foreign-flow-usage.md              (~80 lines)
.claude/skills/finpath-newsroom-master-apparel/references/foreign-flow-usage.md         (~80 lines)
.claude/skills/finpath-newsroom-master-retail/references/foreign-flow-usage.md          (~80 lines)
.claude/skills/finpath-newsroom-master-seafood/references/foreign-flow-usage.md         (~80 lines)
.claude/skills/finpath-newsroom-master-defensive/references/foreign-flow-usage.md       (~80 lines)

# Orchestrator skill — enrichment doc
.claude/skills/finpath-newsroom-orchestrator/references/foreign-flow-enrichment.md      (~100 lines)

# Tests
tests/test_foreign_flow.py                                              (~200 lines)
tests/test_finpath_api_foreign.py                                       (~150 lines)
```

**Total NEW**: 2 lib + 12 skill references + 2 test = **16 file mới**.

### MODIFY files

```
# Finpath API extension
lib/finpath_api.py                                                      (+120 lines: 3 methods + cache helpers)

# Editor V1 — stamp foreign_flow field
.claude/agents/newsroom-editor.md                                       (+20 lines)
.claude/skills/finpath-newsroom-editor/SKILL.md                         (+10 lines)

# Pipeline DB schema validation
lib/pipeline_db.py                                                      (+30 lines: foreign_flow field validation)

# 10 Master SKILL.md — add Step 4.5 (foreign flow check)
.claude/skills/finpath-newsroom-master-bank/SKILL.md                    (+15 lines per master × 10)
[× 10 master]

# Story Editor SKILL.md — load foreign-flow-signal.md
.claude/skills/finpath-newsroom-story-editor/SKILL.md                   (+10 lines)

# CLAUDE.md — note foreign flow data source
CLAUDE.md                                                               (+10 lines)
```

**Total MODIFY**: 1 lib + 1 agent + 12 skill files + 1 CLAUDE.md = **15 file modify**.

## 14. Testing strategy

### Unit tests

`tests/test_foreign_flow.py`:
- `compute_top_foreign_buy` — sort + filter + n parameter
- `compute_top_foreign_sell` — most negative first
- `check_ticker_foreign_status` — 4 outcomes (top_buy / top_sell / normal / no_data)
- `enrich_top_movers` — bulk single API call
- Edge: `dnva == 0` → status normal
- Edge: ste != "S" → no_data
- Edge: less than 30 positive dnva → smaller set

`tests/test_finpath_api_foreign.py`:
- `get_foreign_rooms` — cache hit / miss / TTL
- `get_foreign_roomstatistics` — params period validation
- `get_foreign_roombars` — time series structure
- Cache fallback — API down + stale → return stale
- Cache empty + API fail → raise RuntimeError

### Integration tests

`tests/integration/test_tin_hot_with_foreign_enrichment.py`:
- `/tin-hot 2` end-to-end → 8 ticker enriched
- Verify crawl_log row has `foreign_flow` field
- Verify pipeline_log has `step_1_5.foreign_flow`
- Verify Master cite NN flow when status != normal

`tests/integration/test_master_foreign_drilldown.py`:
- Master với brief có `enrichment.foreign_flow.status = "top_sell"` → body MUST cite
- Master với brief no enrichment + judge call drilldown → cite from roomstatistics

### Regression tests

- `/tin VCB` (no enrichment) still works exactly như V5.1.2
- 17 V4.0 articles still render (foreign_flow field nullable)

## 15. Rollout

### Phase 1 — Foundation (Tasks 1-4)

1. SQLite migration `finpath_foreign_cache`
2. `lib/finpath_api.py` extension — 3 new methods + cache helpers
3. `lib/foreign_flow.py` — top compute + status check + bulk enrich
4. Unit tests pass

### Phase 2 — Story Editor + Master integration (Tasks 5-8)

5. Story Editor `references/foreign-flow-signal.md` + SKILL.md update
6. 10 Master skills `references/foreign-flow-usage.md` (duplicate) + SKILL.md Step 4.5
7. pipeline_db.py validation for `foreign_flow` field
8. Editor V1 stamp foreign_flow per row

### Phase 3 — Hot Ticker enrichment + Spec A V1.2 PATCH (Tasks 9-10)

9. `lib/stages/run_market_snapshot.py` integrate enrichment trong `/tin-hot N` flow
10. Spec A V1.2 PATCH NOTICE inline trong Plan A

### Phase 4 — CLAUDE.md + verification (Tasks 11-12)

11. CLAUDE.md note foreign flow data source
12. Smoke tests: `/tin-hot 2` → 8 ticker enriched + verify Master cite

**Estimated effort**: 16 NEW + 15 MODIFY = ~2-3 ngày với subagent-driven-development parallel.

## 16. Open questions / deferred

### Deferred to V5.1.4+

- **`/api/stocks/insider-transactions/{code}`** — insider trading signal. V5.2.
- **Sector-level foreign flow aggregation** — V5.2.
- **WebSocket real-time updates** — pipeline trigger-based, không cần streaming.
- **Foreign holding ratio trend** — `/api/stocks/shareholderstructure/{code}` đã có.
- **Auto-promote period (1D → 1W → 1M) when 1D signal weak** — defer judgment to Master.

### Open questions for user review

- **Q1**: TOP_N_DEFAULT = 30 — anh OK match screenshot Finpath treemap (~30 mã visible)? Hay anh muốn config?

- **Q2**: Master prompt Step 4.5 (foreign flow check) — apply cho TẤT CẢ 10 master agents giống nhau? Hay sector-specific behavior (vd Bank cite NN khác cách BĐS cite)?

- **Q3**: `/tin <SINGLE>` (non-hot) — em propose KHÔNG auto-enrich vì user đã specify ticker explicit. Story Editor + Master có thể on-demand drilldown. Anh OK?

## 17. Spec changelog

```
- V1.0 (2026-05-12 PM) — Initial spec from brainstorming session
  - 3 Finpath foreign endpoints: /v2/rooms + /roomstatistics + /roombars
  - SQLite cache hybrid TTL (15min / 1h / 6h)
  - lib/foreign_flow.py NEW: top compute + status check + bulk enrich
  - /tin-hot N AUTO-enrichment top 30 NN mua/bán
  - Story Editor stance integration with foreign-flow-signal reference
  - 10 Master skills foreign-flow-usage reference (duplicate, no-shared per CLAUDE.md)
  - Pipeline observability extend step_1_5_market_snapshot.foreign_flow
  - Spec A V1.2 PATCH note (no separate /tin-nn command — user pivot)
  - Rationale: User feedback "gộp vào tin hot, không tách command riêng"
  - Use cases: 3 (Hot Ticker enrich AUTO + Story Editor stance ON-DEMAND + Master data trail ON-DEMAND)
```
