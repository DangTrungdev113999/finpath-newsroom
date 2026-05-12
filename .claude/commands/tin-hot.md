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

## Step 6 — Sequential per-ticker orchestration (MAIN-DRIVEN, V1.4 ARCHITECTURE)

⚠️ ARCHITECTURE (V1.4 fix 2026-05-12 — discovered Claude Code Task tool gated
by nesting depth):

`/tin-hot` does NOT dispatch `newsroom-pipeline` as subagent (level 1 subagent
can't nested-dispatch Editor/Story/Master at level 2 — Task tool unavailable
in subagent context). Instead MAIN session (level 0) orchestrates each ticker's
6 pipeline steps directly, dispatching level 1 subagents (Editor / Story Editor
/ Format Director / Master / Headline) per step. This satisfies `newsroom-pipeline.md`
HARD RULE "no inline-execute for Steps 2-5 + 3.5 + 4.5" — each judgment step
gets its own subagent context window + skill loading.

For each `to_dispatch` entry, MAIN session sequentially runs these per-ticker steps:

### Per-ticker Step 1 — Crawler (Bash, MAIN inline) — V1.5 DATE-FILTERED

```bash
[{i}/{M}] Crawling {ticker} (cats: {cats}, dcp={dcp}%, dvp={dvp}%)
```

⚠️ V1.5 PATCH — crawler MUST bias toward TODAY's news (last 24-48h):

User triggered /tin-hot vì ticker hot **phiên nay**. News từ 3-5 ngày trước về
cluster events cũ sẽ bị Story Editor reject `dup_event` nếu pipeline đã viết
bài về cluster đó trong ngày gần đây. To produce a fresh article about
TODAY's session, crawler MUST find URLs PUBLISHED IN LAST 24-48 HOURS.

MAIN executes per `.claude/agents/newsroom-pipeline.md` Step 1 instructions
PLUS V1.5 date filter:

**WebSearch queries (3-4 queries) — V1.5 date-biased:**
Today = `$(date +%-d/%-m/%Y)` (vd "12/5/2026")

- Query 1: `{ticker} phiên {today_short}` (vd "NVL phiên 12/5")
- Query 2: `{ticker} hôm nay {dcp_direction}` (direction = "tăng"/"giảm" theo dcp)
- Query 3: `{ticker} {today_short} {category_keyword}` (volume_explosion → "khối lượng đột biến", price_decrement → "giảm sàn"/"bán tháo", etc.)
- Query 4: `{ticker} catalyst tin nóng phiên {today_short}`

**Tavily search filter (2-tier fallback — V1.5.1 refinement):**

Tier 1 — strict day filter (catches today-only news):
```python
mcp__tavily__tavily_search(
    query="{ticker} phiên {today_short}",
    time_range="day",
    country="Vietnam",
    max_results=10,
)
```

Tier 2 — week filter with domain restriction (catches recent corporate
actions / dividend announcements / nghị quyết HĐQT that may explain
volume_explosion without explicit "today's session" news):
```python
mcp__tavily__tavily_search(
    query="{ticker} {company_name} cổ tức báo cáo tin tức",
    time_range="week",
    country="Vietnam",
    max_results=10,
    include_domains=["cafef.vn", "vietstock.vn", "vneconomy.vn",
                     "vietnambiz.vn", "tinnhanhchungkhoan.vn",
                     "ndh.vn", "fireant.vn", "baodautu.vn"],
)
```

⚠ Ticker name collision warning: nếu ticker = tên viết tắt trùng tỉnh/địa
danh (vd QNS = Đường Quảng Ngãi but "QNS"+"Quảng Ngãi" có thể trả tin tỉnh),
PHẢI include `include_domains` để biased finance sources. Bỏ phố "Quảng Ngãi"
khỏi query 1 nếu cần. Use full company name khi search.

Tier 3 fallback — if tiers 1+2 đều 0-results: broader month range, no domain
filter, accept that catalyst may be technical/positioning-driven (block trade
or chart breakout) and pass that interpretation to Story Editor.

**WebFetch filter:**
- Reject URLs without explicit today's date marker (12/5 / 2026-05-12) OR clear "hôm nay"/"phiên này"
- Prefer URLs published within last 24-48h
- If <3 today-specific URLs found → fall back broader search BUT clearly mark which URLs are "today's session" vs "background context"

**Crawler script call (V1.5 — add --hot-mode flag passthrough):**
```bash
uv run python lib/stages/run_crawler.py {ticker} \
  --candidates-json /tmp/crawler-input-{ticker}.json \
  --session-id $SESSION_ID \
  --trigger-type tin-hot \
  --trigger-args N=$N
```

(Note: candidates JSON itself encodes today's date preference via crawled_at /
published_time fields. No script change needed — date filter happens at
WebSearch + WebFetch layer above.)

- Capture `funnel_batch_id` from output
- Verify: ≥3 of N candidate rows have `published_time` within last 48h. If
  fewer → log warning "low today's coverage, expect Story Editor to reject for
  dup_event" — MAIN can choose to skip this ticker rather than waste pipeline tokens.

### Per-ticker Step 1.5 — Market Snapshot (Bash, MAIN inline)

```bash
uv run python lib/stages/run_market_snapshot.py {ticker}
```

### Per-ticker Step 2 — Editor V1 (Task → newsroom-editor, ONE per row)

For each pending row in funnel_batch_id:
```
Task tool call (from MAIN — level 0 → newsroom-editor level 1):
  description: "Editor V1 row {row_id_short}"
  subagent_type: newsroom-editor
  prompt: "Process row_id={row_id}. Apply Step 2 V5.1.3: FinpathSectors.get_ticker_sector + get_master_route + validate_crawl_log_v5_1_3 + update_crawl_row(row_id, payload). Hot context: dcp={dcp}% dvp={dvp}% — preserve into pipeline_log step_2_editor_v1.hot_context for downstream consumers."
```

### Per-ticker Step 3 — Story Editor (Task → newsroom-story-editor, batch)

```
Task tool call (from MAIN):
  description: "Story Editor batch {ticker}"
  subagent_type: newsroom-story-editor
  prompt: "Process all routed crawl_log rows for funnel_batch_id={funnel_batch_id}. APPLY HOT INTENT V1.3: user trigger /tin-hot ngụ ý 'Tại sao {ticker} HOT phiên nay (dcp={dcp}%, dvp={dvp}%)'. Prefer angle category=why_now hoặc early_signal khi có catalyst today (block trade / news today / sector rotation / breakout / NN flow today). Reject low_writeability nếu không có catalyst rõ — KHÔNG force bài. Cite data trail = today's source."
```

### Per-ticker Step 3.5 — Format Director (Task → newsroom-format-director, per brief)

For each picked brief from Story Editor:
```
Task tool call (from MAIN):
  description: "Format director brief {ticker}"
  subagent_type: newsroom-format-director
  prompt: "Pick format_id + tone_bias + length_target for each deep_question_option in brief: {brief_json}. Apply 5-step deterministic flow."
```

### Per-ticker Step 4 — Master sector (Task → newsroom-master-{master_route})

Read `master_route` field from crawl_log (set by Editor V1):
```
Task tool call (from MAIN):
  description: "Master {master_route} writing for {ticker}"
  subagent_type: newsroom-master-{master_route}   # bank|ck|bds|oilgas|logistics|fb|apparel|retail|seafood|defensive
  prompt: "Write article for brief={brief_json}, row_id={row_id}. master_route={master_route}. APPLY HOT INTENT V1.3: open body với today's move ({dcp}% giá, {dvp}% KL) + catalyst, KHÔNG generic fundamental intro. Cite số cụ thể của TODAY (giá +X%, volume +Y%, NN mua/bán Z tỷ phiên nay). Old data (Q1/quarterly) chỉ dùng làm CONTEXT supporting today's narrative — KHÔNG lead với LNTT Q1 / ROE / NPL."
```

### Per-ticker Step 4.5 — Headline Craft (Task → newsroom-headline-craft)

```
Task tool call (from MAIN):
  description: "Headline craft {article_id}"
  subagent_type: newsroom-headline-craft
  prompt: "Generate title for article_id={article_id} following V1.1 rules: 5 hard criteria + 4 lối + 8-point rubric. Em dash banned. Hot context: title may reference today's move ({dcp}%, {dvp}%) if angle is catalyst-driven."
```

### Per-ticker Step 5 — Skeptic PAUSED

Skip per CLAUDE.md 2026-05-12 decision.

### Per-ticker Step 6 — Render (Bash, MAIN inline)

```bash
uv run python lib/render_compare_feed.py --funnel-batch-id={funnel_batch_id}
```

### Per-ticker Step 7-9 — Git + GH Pages + Telegram (Bash, MAIN inline)

```bash
git add output/compare-feed/ && git commit --no-verify -m "feat(content): {ticker} hot ticker article (session $SESSION_ID)" && git push origin main
# wait for GH Pages deploy (~30s)
gh run watch $(gh run list --limit 1 --json databaseId -q '.[0].databaseId') --exit-status
# publish telegram
uv run python scripts/publish_telegram.py {article_id}
```

Emit completion:
```
  → ✅ {ticker} done in {Xm:Ys}: "{title}" → Telegram msg #{msg_id}
```

If any step fails → log error + continue to next ticker (don't halt /tin-hot batch). Record fail in `errors.append({...})`.

⚠️ HARD RULE preserved — sequential, NOT parallel. Wait for current ticker's full pipeline to finish before starting next ticker. DB write safety + UX progress.

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
