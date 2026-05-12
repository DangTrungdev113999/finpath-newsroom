# Universe Expansion + KB-optional — Design Spec V1.0

**Date**: 2026-05-12 PM
**Author**: Brainstormed with em (Claude) via /superpowers:brainstorming
**Status**: Draft — pending user review before plan
**Subsystem**: F (Universe Expansion / KB-optional) — from session 2026-05-12 PM feedback
**Depends on**: Spec B `2026-05-11-master-article-format-diversity-design.md` V1.2 (Format + Voice + Stance directive)
**Coupled with**: Spec A `2026-05-12-hot-ticker-trigger-design.md` V1.1 — universe set thay đổi từ 61 → 139, Spec A cần V1.2 PATCH

---

## 1. Goal

Mở universe Finpath Newsroom từ **61 mã hardcoded** (Bank 27 + CK 30 + BĐS 4) lên **139 mã Finpath** (mở rộng 2.3x, cover 8 sector). Mã có KB local → dùng KB depth; mã chưa KB → web search heavy.

Scaffold **7 master agents mới** (oilGas / Logistics / FB / Apparel / Retail / Seafood / Defensive) trong 1 lượt theo pattern Bank/CK/BĐS — KHÔNG dùng "master-generic temporary".

Sau spec này:
- Editor V1 dùng Finpath sectors API để detect sector (real-time, cached 365 ngày).
- 10 master agents covering 139 mã (Bank/CK/BĐS existing + 7 new).
- KB folder pattern uniform: `kb/{sector_code}/` optional, master load nếu tồn tại.
- Migration đơn giản: Khi 1 sector cần depth, anh build `kb/{sector_code}/` đầy đủ — master tự pick up KB depth (no code change).

## 2. Problem statement (từ feedback 2026-05-12 PM)

User feedback nguyên văn:

> "hiện tại đang bị giới hạn các mã do kb ngành. tôi cần mã nào cũng viết được, mã nào có kb rồi thì cứ dùng mà nào chưa có tự vẫn tự đi tiếp được, bằng cách search web thôi"

Vấn đề cụ thể:

1. **Universe giới hạn**: 61 mã (Bank 27 + CK 30 + BĐS 4) — không cover blue chip ngoài Bank/CK/BĐS (HPG, FPT, MWG, VNM, GAS, BSR, ...).
2. **KB-dependent gate**: Editor V1 reject ticker outside 61 universe → user không viết được tin về 80+ mã blue chip còn lại trên thị trường.
3. **Single master per sector**: Bank/CK/BĐS có dedicated master, nhưng oil&gas/retail/fb/... không có → blocker hard.
4. **Story Editor stance examples Bank-coded**: 7-layer framework universal nhưng examples toàn ROA/NPL/NIM/PEG (Bank-only) — gap cho non-Bank sector.

## 3. Out of scope (defer)

- **Coverage > 139 mã** (OTC, mới IPO, penny outside Finpath universe). Phase 2 sau khi 139-mã stable. Defer to Spec F V2.0.
- **Per-ticker KB depth files** (`kb/{sector}/peers/{TICKER}.md`). V5.1.3 ship với minimal `kb/{sector_code}/overview.md` — user grow gradually.
- **Sector-specific quality gates**. V5.1.3 dùng 8 gates V5.1.2 uniform. Future sector-specific gates (vd "oilGas mention crack spread") defer.
- **Web search hallucination prevention** (semantic data trail validation). Existing `no_english_jargon` + `data_trail` cite URL đủ cho V5.1.3.
- **Real-time sector_code update** (khi Finpath thay đổi sector schema). TTL 365d acceptable vì sector ít thay đổi.

## 4. Architecture overview

### 4-layer pipeline insertion

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Sector Detection (Editor V1 - MODIFY)          │
│   - Call Finpath sectors API → SQLite cache TTL 365d   │
│   - Reverse lookup: ticker → sector_code               │
│   - Reject ticker không có trong Finpath cache          │
│   - Auto-refresh cache 1 lần khi ticker miss            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Routing (data/sector_routing.yaml - NEW)       │
│   - sector_code → master_name                           │
│   - bank / ck / bds / oilgas / logistics / fb /         │
│     apparel / retail / seafood / defensive              │
│   - Fail-loud nếu sector_code không trong YAML          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 3: Master Agent (10 agents)                       │
│   - 3 existing: bank/ck/bds (Bank/CK have KB, BĐS       │
│     KB-optional for 50 non-anchor mã)                   │
│   - 7 new: oilgas/logistics/fb/apparel/retail/seafood/  │
│     defensive (all KB-optional, web search heavy)       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 4: Migration (user-driven, future)                │
│   - Build kb/{sector_code}/ depth                       │
│   - Master tự pick up KB (no code change)               │
│   - Web search reduced → KB-anchored automatically       │
└─────────────────────────────────────────────────────────┘
```

### Key changes vs V5.1.2

| Aspect | V5.1.2 | V5.1.3 (this spec) |
|---|---|---|
| Universe size | 61 mã hardcoded | 139 mã từ Finpath API |
| Sector detection | `routing.py` Python dict | Finpath API + SQLite cache 365d |
| Master agents | 3 (Bank/CK/BĐS) | 10 (existing 3 + 7 new) |
| BĐS coverage | 4 mã anchor | 54 mã (4 anchor + 50 KB-optional) |
| CK coverage | 30 mã | 15 mã (Finpath only — drop 15 UPCOM nhỏ) |
| Bank coverage | 27 mã | 18 mã (Finpath only — drop 9 UPCOM nhỏ) |
| KB folder | 3 sector (bank/ck/bds) | 10 sector folders (kb-optional) |
| Stance examples (Story Editor) | Bank-coded only | Extend 7 sector examples |

### Universe trade-off (acknowledged)

Drop **26 mã** vs current 61:
- Bank: 27 → 18 (drop 9 UPCOM: HDF, NAB, BAB, NVB, SGB, VAB, BVB, ABB, KLB, VBB, PGB)
- **CK: 30 → 15 (drop 15 UPCOM)** — HALVING — accepted vì Finpath không có data
- BĐS: 4 → 4 (+50 từ Finpath BĐS sub-sectors)

Add **104 mã mới** từ Finpath (FPT, HPG, GAS, BSR, GMD, VNM, MSN, MWG, FRT, ...).

Net: 61 - 26 + 104 = **139 mã**.

## 5. Sector detection layer

### Finpath sectors API

**Endpoint**: `https://api.finpath.vn/api/stocks/v2/sectors`

**Response shape**:

```json
{
  "data": {
    "sectors": [
      {
        "k": "oilGas",           // sector_code (unique key)
        "c": "oilGas",           // sector code (same as k)
        "n": "Dầu khí",          // sector name (Vietnamese)
        "pk": "",                // parent key (empty if no parent)
        "pn": "",                // parent name
        "s": [                   // stocks array
          {
            "c": "BSR",          // ticker
            "pe": 12.5,
            "pb": 1.8,
            "eps": 1200,
            "roa": 8.5,
            "roe": 18.2,
            "mc": 100000000000,  // market cap
            "e": "HOSE"
          }
        ]
      }
    ]
  }
}
```

**Sector list** (15 active + 3 wrapper empty):

| sector_code | sector_name | parent | #ticker | master_route |
|---|---|---|---|---|
| `private7` | Bank tư nhân top | Ngân hàng | 6 | bank |
| `soe3` | Bank nhà nước | Ngân hàng | 3 | bank |
| `smallLegacy` | Bank vừa và nhỏ | Ngân hàng | 9 | bank |
| `stock` | Chứng khoán | (none) | 15 | ck |
| `materialContractor` | BDS nhà thầu | Bất động sản | 19 | bds |
| `vic3` | BDS VIC3 | Bất động sản | 3 | bds |
| `industrial` | BDS khu công nghiệp | Bất động sản | 13 | bds |
| `exvic` | BDS nhà ở | Bất động sản | 19 | bds |
| `oilGas` | Dầu khí | (none) | 8 | oilgas (NEW) |
| `logistics` | Logistics | (none) | 12 | logistics (NEW) |
| `fb` | Tiêu dùng thực phẩm | Tiêu dùng | 8 | fb (NEW) |
| `apparel` | Tiêu dùng dệt may | Tiêu dùng | 3 | apparel (NEW) |
| `retail` | Tiêu dùng bán lẻ | Tiêu dùng | 7 | retail (NEW) |
| `seafood` | Tiêu dùng thuỷ sản | Tiêu dùng | 6 | seafood (NEW) |
| `defensive` | Phòng thủ | (none) | 12 | defensive (NEW) |
| `bank` | Ngân hàng (wrapper) | (none) | 0 | SKIP (wrapper) |
| `consumer` | Tiêu dùng (wrapper) | (none) | 0 | SKIP (wrapper) |
| `realEstate` | Bất động sản (wrapper) | (none) | 0 | SKIP (wrapper) |

**Total active sectors**: 15. **Total wrapper sectors**: 3 (SKIP via `s == []` check).

### SQLite cache schema

Table `finpath_sectors_cache` trong `data/pipeline.db`:

```sql
CREATE TABLE IF NOT EXISTS finpath_sectors_cache (
    ticker TEXT PRIMARY KEY,                -- VCB, BSR, FPT, ...
    sector_code TEXT NOT NULL,              -- private7, oilGas, stock, ...
    sector_name TEXT NOT NULL,              -- "Bank tư nhân top", "Dầu khí"
    sector_parent TEXT,                     -- "Ngân hàng", "", NULL
    exchange TEXT,                          -- HOSE/HNX/UPCOM
    fetched_at TIMESTAMP NOT NULL,          -- UTC ISO format
    pe REAL, pb REAL, eps REAL, roa REAL, roe REAL, mc REAL  -- snapshot fields
);

CREATE INDEX idx_finpath_cache_sector ON finpath_sectors_cache(sector_code);
```

**TTL**: 365 ngày (user feedback "data này 1 năm mới thay đổi 1 lần"). 

**Refresh policy**:
1. Pipeline run lookup ticker → check cache row exists + `fetched_at` < 365d ago.
2. Cache hit → use cached data.
3. Cache miss OR stale → call Finpath API → rebuild full cache (all 143 tickers) → retry lookup.
4. Auto-refresh trigger: `/tin <UNKNOWN_TICKER>` → 1-shot refresh attempt → if still miss → reject.
5. Manual refresh: `uv run python lib/refresh_sector_cache.py --force` (admin override).

**Graceful degradation**: Finpath API down + cache stale → use stale cache + log warning. Cache empty + API down → fail-loud.

### lib/finpath_sectors.py module

```python
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Optional, TypedDict
import requests
from lib.pipeline_db import PipelineDB

class SectorInfo(TypedDict):
    sector_code: str
    sector_name: str
    sector_parent: str
    exchange: str

CACHE_TTL_DAYS = 365
API_URL = "https://api.finpath.vn/api/stocks/v2/sectors"

class FinpathSectors:
    def __init__(self, db: PipelineDB):
        self.db = db

    def get_ticker_sector(
        self, ticker: str, allow_refresh: bool = True
    ) -> Optional[SectorInfo]:
        """Return ticker's sector info, or None if ticker not in Finpath.

        Flow:
        1. Check cache row exists + fresh (< TTL).
        2. If cache hit: return row.
        3. If cache miss + allow_refresh: refresh all + retry once.
        4. If still miss after refresh: return None.
        """
        row = self._cache_lookup(ticker)
        if row and self._is_fresh(row["fetched_at"]):
            return self._row_to_info(row)

        if allow_refresh:
            self.refresh_cache()
            row = self._cache_lookup(ticker)
            if row:
                return self._row_to_info(row)

        return None  # ticker not in Finpath

    def refresh_cache(self) -> int:
        """Fetch API + repopulate cache. Returns # tickers cached."""
        try:
            response = requests.get(
                API_URL,
                headers={
                    "accept": "application/json",
                    "client-type": "web",
                    "origin": "https://finpath.vn",
                    "user-agent": "Mozilla/5.0",
                },
                timeout=10,
            )
            response.raise_for_status()
        except Exception as e:
            # Graceful degradation: keep stale cache
            self._log_warning(f"Finpath API fetch failed: {e}")
            return 0

        data = response.json()["data"]["sectors"]
        now = datetime.now(timezone.utc).isoformat()
        rows = []
        for sector in data:
            if not sector.get("s"):  # skip wrapper sectors
                continue
            for stock in sector["s"]:
                rows.append({
                    "ticker": stock["c"],
                    "sector_code": sector["k"],
                    "sector_name": sector["n"],
                    "sector_parent": sector.get("pn", ""),
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
            INSERT INTO finpath_sectors_cache (ticker, sector_code, sector_name, sector_parent, exchange, fetched_at, pe, pb, eps, roa, roe, mc)
            VALUES (:ticker, :sector_code, :sector_name, :sector_parent, :exchange, :fetched_at, :pe, :pb, :eps, :roa, :roe, :mc)
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

    def _is_fresh(self, fetched_at_str: str) -> bool:
        fetched_at = datetime.fromisoformat(fetched_at_str)
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
            "exchange": row["exchange"],
        }
```

## 6. Routing layer

### data/sector_routing.yaml

```yaml
# Finpath sector_code → master agent name
# Edit để promote sector (vd: 'oilGas: oilgas' → 'oilGas: oilgas-deep')
# Khi sector_code không có trong file này → fail-loud, log warning, reject ticker

routing:
  # Bank cluster → master-bank (existing)
  private7: bank
  soe3: bank
  smallLegacy: bank

  # CK → master-ck (existing)
  stock: ck

  # BĐS cluster → master-bds (existing, expanded coverage)
  # Note: 4 mã KB-anchor (VHM/NVL/KDH/DXG), 50 mã KB-optional web search heavy
  materialContractor: bds
  vic3: bds
  industrial: bds
  exvic: bds

  # NEW V5.1.3 — 7 sectors (all KB-optional, master scaffold sẵn)
  oilGas: oilgas
  logistics: logistics
  fb: fb
  apparel: apparel
  retail: retail
  seafood: seafood
  defensive: defensive

# Future migration: khi build kb/oilGas/ đầy depth + tách master-oilgas-deep,
# edit: oilGas: oilgas-deep

skip_wrappers:
  - bank
  - consumer
  - realEstate
```

### lib/sector_router.py

```python
import yaml
from pathlib import Path

ROUTING_FILE = Path("data/sector_routing.yaml")

def get_master_route(sector_code: str) -> str:
    """Map sector_code → master_name. Fail-loud if unmapped."""
    with open(ROUTING_FILE) as f:
        config = yaml.safe_load(f)
    routing = config["routing"]
    if sector_code not in routing:
        raise ValueError(
            f"sector_code '{sector_code}' chưa map trong {ROUTING_FILE}. "
            f"Add entry hoặc check Finpath API có sector mới."
        )
    return routing[sector_code]
```

## 7. Master agent strategy

### 10 master agents

| Master agent | Sector codes | Số mã | KB status | File status |
|---|---|---|---|---|
| `newsroom-master-bank` | private7 + soe3 + smallLegacy | 18 | Full KB `kb/bank/` | EXISTING (V5.1.2 split) |
| `newsroom-master-ck` | stock | 15 | Full KB `kb/ck/` | EXISTING (V5.1.2 split) |
| `newsroom-master-bds` | materialContractor + vic3 + industrial + exvic | 54 | KB-optional: 4 mã anchor (VHM/NVL/KDH/DXG), 50 mã web search heavy | EXISTING (V5.1.2 split, expand coverage) |
| `newsroom-master-oilgas` | oilGas | 8 | KB-optional | **NEW** |
| `newsroom-master-logistics` | logistics | 12 | KB-optional | **NEW** |
| `newsroom-master-fb` | fb | 8 | KB-optional | **NEW** |
| `newsroom-master-apparel` | apparel | 3 | KB-optional | **NEW** |
| `newsroom-master-retail` | retail | 7 | KB-optional | **NEW** |
| `newsroom-master-seafood` | seafood | 6 | KB-optional | **NEW** |
| `newsroom-master-defensive` | defensive | 12 | KB-optional | **NEW** |

### Pattern reuse (7 new masters scaffold theo Bank)

Mỗi master mới copy structure y nguyên từ Bank (V5.1.2 split pattern):

```
.claude/agents/newsroom-master-{sector}.md            (~80 lines, dispatch wrapper)
.claude/skills/finpath-newsroom-master-{sector}/
├── SKILL.md                                          (~180 lines, 9-step workflow)
└── references/
    ├── format-bodies/                                (4 files)
    │   ├── flash-qa.md                               (sector-aware example, vd BSR oil&gas)
    │   ├── standard-qa.md
    │   ├── standard-listicle.md
    │   └── standard-narrative.md
    ├── voice-layer-rules.md                          (copy từ Bank, generic)
    ├── stance-directive-handler.md                   (copy từ Bank, generic)
    ├── sector-context.md                             (NEW per-sector — overview + jargon + key metrics + analysis lens)
    ├── jargon-mapping.md                             (sector-specific, vd oil&gas: crack spread → "chênh lệch giá dầu thô-sản phẩm")
    ├── master-pitfalls.md                            (sector-specific, vd oil&gas: confuse upstream/downstream)
    └── compare-feed-spec.md                          (mirror Bank)
```

**Bootstrap effort**:
- 7 master agents × 9 reference files = 63 file mới reference
- 7 SKILL.md + 7 agent .md = 14 file mới skill/agent
- **Total: 77 file mới** (chấp nhận heavy, scaffold 1 lượt, pattern repeated)

### Sector-context.md template (NEW file per master)

Example `references/sector-context.md` cho master-oilgas:

```markdown
# Sector Context — Dầu khí (oilGas)

> Loaded from `Skill: finpath-newsroom-master-oilgas`. Sector-specific overview + analysis lens.

## Overview

Sector dầu khí Việt Nam gồm 3 mảng:
- **Upstream** (PVS, GAS): thăm dò + khai thác + dịch vụ
- **Downstream** (BSR, PLX): lọc hoá dầu + phân phối
- **Utility** (POW): điện khí

Chu kỳ ngành phụ thuộc:
- Giá dầu Brent (USD/thùng)
- OPEC policy + sản lượng nội địa
- Tỷ giá VND/USD
- Demand điện + xăng dầu nội địa

## Key metrics

- **Crack spread**: chênh lệch giá dầu thô và sản phẩm (xăng/dầu diesel/jet fuel)
- **Refining margin**: biên lọc dầu
- **Throughput**: sản lượng tinh chế (tấn/quý)
- **Inventory days**: số ngày tồn kho
- **Realized oil price**: giá bán dầu thực tế

## Jargon mapping (Anh → Việt)

- crack spread → "chênh lệch giá dầu thô-sản phẩm"
- refining margin → "biên lọc dầu"
- upstream/downstream → "thăm dò khai thác / lọc hoá dầu"
- realized price → "giá bán thực tế"
- inventory turnover → "vòng quay tồn kho"

## Analysis lens

- Giá Brent up + biên lọc up = bullish toàn sector
- Giá Brent down + VND yếu = mixed (upstream loss, downstream gain)
- OPEC cắt sản lượng = catalyst cho upstream
- Demand nội địa tăng (Q4/Tết) = catalyst cho downstream

## Peers reference

BSR (lọc hoá dầu) · PVS (dịch vụ kỹ thuật) · GAS (khí thiên nhiên) · POW (điện khí) · PLX (phân phối xăng dầu)
```

Mỗi master mới có 1 file tương tự, content sector-specific (em sẽ generate trong Plan F).

## 8. KB-optional pattern

### Uniform behavior across all 10 masters

```python
def load_data_sources(sector_code: str, ticker: str) -> list[Source]:
    """Master agent load data sources in priority order."""
    sources = []

    # Priority 1: Finpath API (BCTC, ratios, ownership, events)
    sources.append(finpath_api.get_ticker_full(ticker))

    # Priority 2: KB local (optional)
    kb_dir = Path(f"kb/{sector_code}/")
    if kb_dir.exists():
        for md in kb_dir.glob("*.md"):
            sources.append(load_kb_file(md))

    # Priority 3: SQLite memory (variety guard 3 bài cũ)
    sources.append(get_recent_articles(ticker))

    # Priority 4: Web search BẮT BUỘC nếu KB thiếu hoặc data unclear
    if not has_kb_anchor(kb_dir, ticker) or insufficient_data(sources):
        sources.append(web_search(ticker))

    return sources
```

### KB folder naming convention

Sector code match Finpath chính xác:
- `kb/private7/` cho Bank tư nhân top
- `kb/oilGas/` cho Dầu khí
- `kb/fb/` cho Tiêu dùng thực phẩm
- `kb/exvic/` cho BĐS nhà ở (NVL/KDH/DXG)

Cluster code routing-only (KB cluster):
- `kb/bank/` chung cho cả Bank cluster (private7 + soe3 + smallLegacy) — existing
- `kb/ck/` cho stock — existing
- `kb/bds/` cho cả BĐS cluster — existing

**Hybrid lookup**: Master Bank load `kb/bank/` (cluster KB). Master oilgas load `kb/oilGas/` (specific KB). Both supported via configurable per-master KB path.

### Master config — KB path per master

`.claude/skills/finpath-newsroom-master-{sector}/SKILL.md` định nghĩa `kb_path`:

```yaml
# Frontmatter của SKILL.md
kb_path: "kb/oilGas/"
sector_codes: ["oilGas"]  # match sector_routing.yaml destinations
```

Bank cluster:
```yaml
kb_path: "kb/bank/"
sector_codes: ["private7", "soe3", "smallLegacy"]
```

## 9. Editor V1 schema change

### Output schema V5.1.3

**Trước (V5.1.2)**:

```yaml
crawl_log row:
  ticker: "BSR"
  editor_v1_decision: route_to_story_editor | reject
  sector: "Bank" | "CK" | "BĐS"            # 3 sector cứng
```

**Sau (V5.1.3)**:

```yaml
crawl_log row:
  ticker: "BSR"
  editor_v1_decision: route_to_story_editor | reject
  editor_v1_note: str                       # KEEP
  sector_code: "oilGas"                     # NEW — Finpath code
  sector_name: "Dầu khí"                    # NEW — Vietnamese display
  sector_parent: ""                          # NEW — parent group ("Ngân hàng", "", ...)
  master_route: "oilgas"                    # NEW — bank/ck/bds/oilgas/logistics/...
  sector: "Dầu khí"                          # KEEP backward-compat (derived from sector_name)
```

### Editor V1 logic

```python
def editor_v1_decide(crawl_row):
    ticker = detect_ticker(crawl_row["raw_title"])
    if not ticker:
        return {
            "editor_v1_decision": "reject",
            "editor_v1_note": f"ticker_undetected"
        }

    sector_info = finpath_sectors.get_ticker_sector(ticker, allow_refresh=True)
    if not sector_info:
        return {
            "editor_v1_decision": "reject",
            "editor_v1_note": f"ticker_outside_finpath_139"
        }

    try:
        master_route = sector_router.get_master_route(sector_info["sector_code"])
    except ValueError as e:
        return {
            "editor_v1_decision": "reject",
            "editor_v1_note": f"sector_unmapped_in_yaml: {e}"
        }

    return {
        "editor_v1_decision": "route_to_story_editor",
        "editor_v1_note": "",
        "sector_code": sector_info["sector_code"],
        "sector_name": sector_info["sector_name"],
        "sector_parent": sector_info["sector_parent"],
        "master_route": master_route,
        "sector": sector_info["sector_name"],  # backward-compat
    }
```

### routing.py deprecation

`.claude/skills/finpath-newsroom-editor/scripts/routing.py` HIỆN TẠI chứa hardcoded 61 universe + BANK/CK/BĐS mapping. V5.1.3:

- REMOVE function `get_sector(ticker)` (Python dict lookup).
- REPLACE với `from lib.finpath_sectors import get_ticker_sector + from lib.sector_router import get_master_route`.
- KEEP function `COMPANY_NAME_TO_TICKER` (alias mapping, vẫn cần cho detect ticker).

## 10. Migration path (when user promote sector)

User feedback (Q2 brainstorm): "sau tôi sẽ build 7 master sector riêng sau" — but later pivoted to build all 7 at once. Migration path đây cho promote SECTOR đã có master generic → KB-anchored:

Promote `oilGas` master từ scaffold → KB-anchored full depth:

1. **Build KB folder**: `kb/oilGas/` với
   - `overview.md` (sector summary)
   - `key-metrics.md`
   - `jargon.md`
   - `peers/{TICKER}.md` cho 8 mã oilGas (BSR, PVS, GAS, POW, PLX, ...)
2. **Master tự pick up** — KHÔNG cần code change. KB-optional pattern automatic.
3. (Optional) **Update sector_context.md** trong skill references — refine analysis lens.
4. (Optional) **Promote to deep master**: rename `newsroom-master-oilgas` → `newsroom-master-oilgas-deep` + edit `data/sector_routing.yaml`: `oilGas: oilgas-deep` (chỉ cần khi muốn split sub-cluster, vd thêm `oilGas-upstream` / `oilGas-downstream`).

## 11. Story Editor stance examples extension

### Gap from V5.1.2 (advisor blocking 4)

Spec B V1.2 Patch 2 stance_directive 7-layer framework universal nhưng examples trong skill toàn ROA/NPL/NIM/PEG (Bank-coded). 7 sector mới cần stance examples riêng.

### Add file: `references/stance-judgment-guide.md` extension

`.claude/skills/finpath-newsroom-story-editor/references/stance-judgment-guide.md` (existing per Plan B Task 28 step 5) thêm 7 case study per sector:

| Sector | Stance case | 7-layer key signals |
|---|---|---|
| oilGas | Giá Brent up + BSR Q1 lợi nhuận tăng | Crack spread + throughput + inventory |
| logistics | Cảng GMD throughput tăng + tăng giá cước | TEU + revenue/TEU + utilization |
| fb | VNM same-store sales tăng + margin recovery | SSS + gross margin + brand power |
| apparel | TCM Q1 đơn hàng tăng từ Mỹ thoái thuế | Export revenue + USD/VND + EU/US demand |
| retail | MWG mở cửa hàng mới + same-store sales | Store count + SSS + online revenue ratio |
| seafood | VHC Q1 xuất khẩu cá tra tăng | Export volume + giá cá fillet + tariff |
| defensive | DGC giá phốt pho thế giới tăng | Commodity price + COGS hedging |

Mỗi case 30-50 từ Vietnamese prose example. Total ~300-500 từ extension.

## 12. Quality gates (unchanged from V5.1.2)

7 master mới apply 8 gates V5.1.2 uniform:

1. No English jargon (LLM check + regex)
2. No metadata leak
3. No-hedging (LLM-as-judge 2 test)
4. Verdict line bắt buộc
5. Stance consistency (cite ≥1 evidence + direction match)
6. Em dash density body (≤1/100 từ)
7. Word count per format
8. Body pattern per format

Plus 5 Headline criteria (Spec C V1.1):
- Ticker present
- ≤12 từ
- Hook strong (LLM-as-judge 2 sub-test)
- Bình dân nguy hiểm (LLM-as-judge 2 sub-test)
- No em dash

**Sector-specific gates** DEFER (vd "oilGas mention crack spread") — V5.1.3 dùng uniform gates đủ. Future Spec F V2.0 add.

## 13. Hot Ticker (Spec A) interaction

### Spec A V1.1 intersect 61 → 139

Spec A `/tin-hot N` filter ticker thuộc 61 universe BEFORE compute top N. V5.1.3 thay đổi universe 61 → 139 → Spec A intersect set mở rộng.

**Action**: Add **Spec A V1.2 PATCH NOTICE** sau khi V5.1.3 ship:
- Intersect set: 61 hardcoded → `lib/finpath_sectors.py::get_all_cached_tickers()` (139 mã)
- Auto-refresh cache trước compute top
- Reject ticker không có trong Finpath cache (consistent với Editor V1)

Defer detail to Plan A V1.2 — chỉ note ở đây.

## 14. File touch list

### NEW files (V5.1.3)

```
# Sector detection
lib/finpath_sectors.py                                                  (~150 lines)
lib/sector_router.py                                                    (~30 lines)
lib/refresh_sector_cache.py                                             (~50 lines, CLI)

# Routing config
data/sector_routing.yaml                                                (~30 lines)

# SQLite schema migration
lib/migrations/2026-05-12-add-finpath-sectors-cache.sql                 (~20 lines)

# 7 NEW master agents (each follows Bank V5.1.2 split pattern)
.claude/agents/newsroom-master-oilgas.md                                (~80 lines)
.claude/agents/newsroom-master-logistics.md                             (~80 lines)
.claude/agents/newsroom-master-fb.md                                    (~80 lines)
.claude/agents/newsroom-master-apparel.md                               (~80 lines)
.claude/agents/newsroom-master-retail.md                                (~80 lines)
.claude/agents/newsroom-master-seafood.md                               (~80 lines)
.claude/agents/newsroom-master-defensive.md                             (~80 lines)

# 7 NEW master skills (each ~SKILL.md + 9 references = 10 files)
.claude/skills/finpath-newsroom-master-oilgas/SKILL.md                  (~180 lines)
.claude/skills/finpath-newsroom-master-oilgas/references/
├── format-bodies/flash-qa.md                                           (~70 lines, BSR example)
├── format-bodies/standard-qa.md                                        (~80 lines)
├── format-bodies/standard-listicle.md                                  (~90 lines)
├── format-bodies/standard-narrative.md                                 (~80 lines)
├── voice-layer-rules.md                                                (~100 lines, copy)
├── stance-directive-handler.md                                         (~80 lines, copy)
├── sector-context.md                                                   (~100 lines)
├── jargon-mapping.md                                                   (~50 lines)
├── master-pitfalls.md                                                  (~60 lines)
└── compare-feed-spec.md                                                (~60 lines, mirror Bank)

[× 7 sectors = 70 files]
```

**Total NEW**: 5 lib/yaml + 7 agent + 7 SKILL.md + 63 reference = **82 file**.

### MODIFY files

```
# Editor V1 — call finpath_sectors + sector_router
.claude/agents/newsroom-editor.md                                       (~30 lines added)
.claude/skills/finpath-newsroom-editor/SKILL.md                         (~20 lines added)
.claude/skills/finpath-newsroom-editor/scripts/routing.py               (deprecate get_sector, keep ticker aliases)

# Pipeline DB schema validation V5.1.3
lib/pipeline_db.py                                                      (add sector_code/sector_name/sector_parent/master_route schema)

# Master-BDS expand coverage (50 new mã, KB-optional)
.claude/skills/finpath-newsroom-master-bds/SKILL.md                     (~20 lines, KB-optional pattern)

# Story Editor stance examples
.claude/skills/finpath-newsroom-story-editor/references/stance-judgment-guide.md  (~300 lines added, 7 sector cases)

# CLAUDE.md
CLAUDE.md                                                               (universe 61→139, sector list update)
```

### DELETE files

```
# Remove dead code
.claude/skills/finpath-newsroom-editor/scripts/routing.py FULL_UNIVERSE  (constants — replaced by Finpath cache)
.claude/skills/finpath-newsroom-editor/scripts/routing.py BANK_UNIVERSE  (replaced)
.claude/skills/finpath-newsroom-editor/scripts/routing.py CK_UNIVERSE    (replaced)
.claude/skills/finpath-newsroom-editor/scripts/routing.py BDS_UNIVERSE   (replaced)
```

## 15. Testing strategy

### Unit tests

- `tests/test_finpath_sectors.py`:
  - Cache lookup hit / miss / stale
  - Refresh cache populate all sectors
  - Skip wrapper sectors (s=[])
  - Graceful degradation (API down + stale cache)
  - Auto-refresh on cache miss

- `tests/test_sector_router.py`:
  - Map sector_code → master_route
  - Fail-loud on unknown sector_code
  - Skip wrapper sectors

- `tests/test_editor_v1_v5_1_3.py`:
  - Reject ticker outside Finpath cache
  - Auto-refresh on unknown ticker
  - Set sector_code/sector_name/sector_parent/master_route correctly
  - Backward-compat `sector` field

### Integration test

- `tests/integration/test_pipeline_oilgas.py`:
  - Full pipeline với ticker BSR (oilGas sector)
  - Verify routing: Editor → master-oilgas (not master-bank)
  - Verify body uses oil&gas jargon (no Anh leak)
  - Verify quality gates pass

- `tests/integration/test_pipeline_bds_non_anchor.py`:
  - Full pipeline với ticker BCM (industrial BDS, no KB anchor)
  - Verify routing: Editor → master-bds (despite no per-ticker KB)
  - Verify web search heavy (data_trail has ≥3 web sources)
  - Verify quality gates pass

### Regression test

- 17 V4.0 articles still render correctly (no schema break).
- `/tin VCB` → master-bank (existing behavior).
- `/tin BSR` → master-oilgas (NEW capability).

## 16. Rollout

### Phase 1 — Foundation (Tasks 1-5)

1. SQLite schema migration `finpath_sectors_cache`.
2. `lib/finpath_sectors.py` + tests.
3. `lib/sector_router.py` + `data/sector_routing.yaml` + tests.
4. `lib/refresh_sector_cache.py` CLI + populate cache initial.
5. Editor V1 update + schema validation.

### Phase 2 — 7 NEW master agents (Tasks 6-12)

Parallel-safe — each master agent independent:

6. master-oilgas (agent + skill + 9 references)
7. master-logistics (same pattern)
8. master-fb
9. master-apparel
10. master-retail
11. master-seafood
12. master-defensive

Per master: copy Bank V5.1.2 split structure, swap sector-specific content.

### Phase 3 — Existing master adjustments (Tasks 13-14)

13. Master-BDS expand: SKILL.md note KB-optional for 50 non-anchor mã + web search heavy fallback.
14. Story Editor stance-judgment-guide.md extend 7 sector cases.

### Phase 4 — CLAUDE.md + verification (Tasks 15-16)

15. Update CLAUDE.md universe section (61 → 139, sector list).
16. Smoke tests: `/tin BSR` / `/tin MWG` / `/tin VNM` / `/tin GMD` end-to-end.

**Estimated effort**: 82 file mới + 5 file modify = ~3-4 ngày với subagent-driven-development parallel.

## 17. Open questions / deferred — RESOLVED

### Deferred to V5.1.4+

- **OTC + mới IPO ticker coverage** — Phase 2 web search universal (no Finpath constraint).
- **Per-ticker KB files** (`kb/{sector}/peers/{TICKER}.md`) — manual user-driven growth.
- **Sector-specific quality gates** (vd "oilGas mention crack spread") — V5.1.4.
- **Real-time sector_code change detection** (Finpath schema update) — alerting via manual refresh diff.

### Resolved (2026-05-12 PM user review)

- **Q1 (RESOLVED — option A)**: Master-BDS load `kb/bds/` cho TẤT CẢ 54 mã (sector-level context) + per-ticker KB anchor cho 4 mã (depth). Web search fallback cho 50 mã không có per-ticker KB. Graceful degradation pattern.

- **Q2 (RESOLVED — option A)**: 7 NEW master agents DUPLICATE `voice-layer-rules.md` + `stance-directive-handler.md` từ Bank. Consistent với V5.1.2 split decision (CLAUDE.md cấm `shared-references/`). ~80 lines × 7 master = 560 lines duplicate — acceptable trade-off cho isolation.

- **Q3 (RESOLVED — no KB scaffolding)**: KHÔNG tạo `kb/{sector_code}/` folder cho 7 sector mới ở V5.1.3 ship. 7 master agents mới launch với note **"chưa có KB, tự search web"** trong SKILL.md. KB folder naming convention (camelCase `kb/oilGas/`) chỉ apply khi user build KB sau này. Web search heavy mode cho 7 master mới + 50 BDS non-anchor mã.

### Impact của Q3 resolution

- §14 File touch list: REMOVE `kb/{sector_code}/` folder creation từ Phase 2 tasks. Save ~7 folder bootstrap.
- §8 KB-optional pattern: V5.1.3 ship state = `kb_dir.exists() == False` cho 7 sector mới → 100% Priority 4 (web search). Future user build KB → automatic pickup.
- §7 master skill SKILL.md frontmatter: 7 master mới có note "kb_path: '' # not yet built — use web search heavy" để dispatcher biết.

## 18. Spec changelog

```
- V1.0 (2026-05-12 PM) — Initial spec from brainstorming session
  - Universe 61 → 139 (Finpath only, drop 26 UPCOM)
  - 7 NEW master agents scaffold 1 lượt (oilgas/logistics/fb/apparel/retail/seafood/defensive)
  - Sector detection via Finpath sectors API + SQLite cache TTL 365d
  - data/sector_routing.yaml mapping config
  - Master-BDS expanded coverage 4 → 54 mã, KB-optional
  - Editor V1 schema add sector_code/sector_name/sector_parent/master_route
  - Migration path: build kb/{sector_code}/ → master tự pick up (no code change)
  - Address advisor concerns: Spec A V1.2 PATCH + Story Editor stance examples per sector + auto-refresh on unknown ticker + wrapper sector skip + YAML fail-loud
  - Rationale: User feedback "mã nào cũng viết được, KB có thì dùng, không thì web search" + "build hết master 1 lượt vì có pattern sẵn"

- V1.0.1 (2026-05-12 PM) — 3 open question resolutions
  - Q1 RESOLVED option A: Master-BDS load kb/bds/ cho 54 mã + per-ticker KB anchor cho 4 mã
  - Q2 RESOLVED option A: Accept duplicate voice/stance refs trong 7 master mới (CLAUDE.md no-shared-refs)
  - Q3 RESOLVED: KHÔNG tạo kb/{sector_code}/ folder ở V5.1.3 ship. 7 master mới web search heavy. KB folder naming convention defer cho future user-driven build.
```
