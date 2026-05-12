---
description: Trigger pipeline V5.1.4 cho top N mã từ 4 bên (Tăng giá / Giảm giá / Bùng nổ / Cạn cung) intersect Finpath ~139 universe. Default N=4, max N=10. Sequential dispatch với shared SESSION_ID + per-ticker progress emission. Idempotency 60-min window.
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

## Step 2 — Shared SESSION_ID generation (V5.1.4 — same pattern as /tin-batch)

`/tin-hot N` dispatches N parallel-safe-but-sequential pipelines. All N tickers MUST share ONE session_id so `/pipeline-runs` viewer groups them as 1 session × N batches.

```bash
SESSION_ID=$(uuidgen)
TRIGGER_TYPE="tin-hot"
TRIGGER_ARGS="N=$N"
echo "Hot session: $SESSION_ID ($TRIGGER_TYPE $TRIGGER_ARGS)"
```

**CRITICAL** — `SESSION_ID` sinh ĐÚNG 1 LẦN. KHÔNG `uuidgen` per ticker. Child `newsroom-pipeline` Step 0 inherits từ parent prompt và KHÔNG sinh thêm UUID (xem `.claude/agents/newsroom-pipeline.md` Step 0 inheritance check).

## Step 3 — Fetch + intersect ~139 universe + compute (V1.2 PATCH)

V1.2 PATCH integration: intersect uses `FinpathSectors.get_all_cached_tickers()` (~139 mã V5.1.3) thay vì hardcoded `FULL_UNIVERSE` 71 mã. Auto-refresh cache nếu empty.

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
from lib.finpath_sectors import FinpathSectors
from lib.finpath_top_movers import fetch_top_hot_tickers, compute_top_lists, apply_default_filters, intersect_universe, fetch_stocks_overview

N = <N from Step 1>

# V1.2 PATCH: load Finpath cache, auto-refresh if empty
db = PipelineDB('data/pipeline.db')
fs = FinpathSectors(db)
universe = set(fs.get_all_cached_tickers())
if not universe:
    print('Universe cache empty — refreshing from Finpath API...')
    fs.refresh_cache()
    universe = set(fs.get_all_cached_tickers())

# Full pipeline: fetch → filter → intersect → compute → dedup
stocks = fetch_stocks_overview()
filtered = apply_default_filters(stocks)
universe_stocks = intersect_universe(filtered, universe)
lists = compute_top_lists(universe_stocks, N)
deduped = []
seen = {}
order = []
for cat in ['price_increment', 'price_decrement', 'volume_explosion', 'depleted_supply']:
    for h in lists.get(cat, []):
        if h.code not in seen:
            seen[h.code] = []
            order.append(h.code)
        seen[h.code].append(cat)
deduped = [(t, seen[t]) for t in order]

output = {
    'N': N,
    'universe_size': len(universe),
    'total_universe_in_top100': len(universe_stocks),
    'lists': {cat: [t.to_dict() for t in items] for cat, items in lists.items()},
    'unique_tickers': [{'ticker': t, 'categories': cats} for t, cats in deduped],
}
print(json.dumps(output, ensure_ascii=False, indent=2))
db.close()
" > /tmp/tin-hot-result.json
```

⚠ V1.2 PATCH NOTE: NO foreign flow enrichment (Spec G V1.1 PATCH reverted). Master/Story Editor judge khi nào call foreign flow on-demand qua `references/foreign-flow-when-to-call.md`.

## Step 4 — Pre-flight summary

Read `/tmp/tin-hot-result.json` + emit:

```
🔥 Top Hot Tickers — Finpath Universe (~139 mã) — N={N}
Session: {SESSION_ID}

Top tăng giá (price_increment):
  1. <ticker> ({+pct}%)
  ...

Top giảm giá (price_decrement): <similar>
Top bùng nổ KL (volume_explosion): <similar>
Top cạn cung KL (depleted_supply): <similar>

📊 Unique sau dedup: {M} mã sẽ dispatch pipeline V5.1.4
  - {ticker1} — {categories}
  ...
```

Hiển thị màu xanh cho `+pct`, đỏ cho `-pct`.

If M = 0 → emit "Không có mã hot nào trong universe sau filter — exit gracefully" và stop.

## Step 5 — Idempotency check (60-min window)

For each ticker in deduped list, query recent published article:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
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
                age_min = (now - published_at).total_seconds() / 60
                skipped.append({'ticker': ticker, 'reason': f'Đã có bài {age_min:.0f} phút trước'})
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

## Step 6 — Sequential dispatch with shared SESSION_ID + HOT CONTEXT

For each `to_dispatch` entry, in order:

```
[{i}/{M}] Dispatching /tin {ticker}... (categories: {cats}, dcp={dcp}%, dvp={dvp}%)
```

⚠️ CRITICAL — hot context dispatch intent (V1.3 quality patch 2026-05-12):

User trigger `/tin-hot` ngụ ý: **"Tại sao mã này HOT phiên nay?"** — Master/Story
Editor MUST explain TODAY's price/volume action, KHÔNG được gượng ép paradox
giữa lịch sử (Q1 fundamentals) và phiên nay nếu thiếu causal link.

Then dispatch via Task tool (pass shared session metadata + hot context + intent
narrative qua prompt):

```
Task tool call:
  description: "Master pipeline hot ticker {ticker}"
  subagent_type: newsroom-pipeline
  prompt: |
    ticker={ticker}
    session_id=$SESSION_ID
    trigger_type=tin-hot
    trigger_args=N=$N
    hot_category={categories joined}
    hot_metric_today: dcp={dcp:+.2f}% (price change), dvp={dvp:+.2f}% (volume change)

    INTENT (V1.3 HARD RULE — /tin-hot quality):
    User wants to know WHY this ticker is HOT TODAY (last 24-48h session).
    Master + Story Editor MUST find news/event explaining today's move:
      ✅ Block trade / room ngoại announcement (last 1-3 days)
      ✅ News event today (regulator action / earnings released / corporate action)
      ✅ Sector rotation today (peer movement explaining ticker move)
      ✅ Technical breakout (chart level broken today)
      ✅ Foreign flow today (NN mua/bán ròng strong)

    AVOID (gây bài gượng ép):
      ❌ Force-fit paradox giữa Q1/2026 (old) fundamentals và phiên nay
         unless data shows direct causal chain
      ❌ Generic angle về fundamentals nếu không có news today
      ❌ Lead body với LNTT Q1 / ROE / NPL khi user hỏi "tại sao hôm nay tăng/giảm"

    STORY EDITOR specifically:
      - Prefer angle category=why_now hoặc early_signal khi có catalyst today
      - Reject low_writeability nếu không có catalyst rõ — KHÔNG ép bài
      - Cite data trail = today's source (news today + technical today + NN today)

    MASTER specifically:
      - Open body với today's move + catalyst, KHÔNG generic fundamental intro
      - Cite số cụ thể của TODAY: giá +X%, volume +Y%, NN mua/bán Z tỷ phiên nay
      - Old data (Q1/quarterly) chỉ dùng làm CONTEXT supporting today's narrative

    Inherit SESSION_ID from parent — DO NOT generate new uuidgen at Step 0.
```

⚠️ HARD RULE — sequential, NOT parallel. Dispatch tiếp theo CHỈ sau khi current Task return. DB write safety + per-ticker progress emission ưu tiên hơn parallel speedup.

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

## Step 7 — Final summary

```
✅ /tin-hot N=$N hoàn tất:
  - {success_count} mã dispatched thành công
  - {total_articles} bài generated
  - {skipped_count} mã skip (idempotency)
  - {error_count} mã fail

Session: $SESSION_ID
Xem lịch sử: http://localhost:5174/pipeline-runs?session_id=$SESSION_ID
Xem feed: http://localhost:5174/feed
```

## Hard rules

- N ∈ [1, 10] integer. Reject 0, 11+, non-integer.
- SESSION_ID sinh ĐÚNG 1 LẦN ở Step 2; tất cả N pipeline children inherit.
- Sequential dispatch — KHÔNG parallel (DB write safety + UX progress).
- Universe = ~139 mã Finpath cache (V1.2 PATCH), NOT hardcoded FULL_UNIVERSE 71.
- NO foreign flow auto-enrichment (Spec G V1.1 PATCH).
- Ticker fail (Master gates / Story Editor 0 briefs) → skip + continue, log error.
- Empty intersect (0 mã) → exit gracefully với message.
- Idempotency 60-min: skip ticker đã có bài < 60 phút.
- Per-ticker progress emission BẮT BUỘC — silent long wait là UX fail.

## Examples

```
User: /tin-hot 4
Em: 🔥 Top Hot Tickers — Finpath Universe (~139 mã) — N=4
    Session: a1b2c3d4-...

    Top tăng giá: STB +6.8% / VRE +5.2% / BSR +4.1% / GVR +3.9%
    Top giảm giá: NVL -3.2% / VGC -2.8% / VIX -2.5% / OCB -2.1%
    Top bùng nổ: QNS / BMP / DXG / LPB
    Top cạn cung: VCG / PLX / VIB / KDC

    📊 Unique sau dedup: 16 mã

    [1/16] Dispatching /tin STB... ✅ done in 3m12s, 1 article
    [2/16] Dispatching /tin VRE... ✅ done in 2m48s, 1 article
    ...

    ✅ /tin-hot N=4 hoàn tất: 14 mã, 14 bài (2 skip idempotency, 0 fail)
    Session: a1b2c3d4-...
```
