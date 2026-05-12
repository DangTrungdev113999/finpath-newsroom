# Pipeline Run History — Design Spec V1.0

**Date**: 2026-05-12 PM
**Author**: Brainstormed with em (Claude) via /superpowers:brainstorming
**Status**: Draft — pending user review before plan
**Subsystem**: H (Pipeline Run History) — from session 2026-05-12 PM feedback
**Depends on**: Existing `lib/render_compare_feed.py` + React viewer

---

## 1. Goal

Tách phần Crawl funnel khỏi per-article view → tạo **standalone page `/pipeline-runs`** showing toàn bộ lịch sử pipeline runs với 3-level browse: **Session → Batch → Funnel detail**.

Sau spec này:
- Article view sạch hơn (remove RightColumn section 5 crawl_funnel)
- User browse lịch sử các lần chạy pipeline để biết: bao nhiêu tin fetched, bao nhiêu chosen, lý do reject
- Multi-ticker `/tin-hot N` runs grouped under 1 session — không trộn flat
- Article header có link `funnel_batch_id` jump to `/pipeline-runs` filtered

## 2. Problem statement (từ feedback 2026-05-12 PM)

User feedback:

> "phần này cho mỗi bài viết không cần nữa, nhưng không bỏ, tôi cần vẫn cần đọc để biết pipeline đó chạy thì bao nhiêu tin được tìm thấy, reject tin nào lý do reject"
>
> "giờ bố trí cái crawl funnel đó ở đâu thì hợp lý để xem được lịch sử những lần chạy, xem được bao nhiêu bài được fetch, bao nhiêu bài được chọn, reject, lý do"

Vấn đề:
1. **Per-article funnel clutters article view** — reader cần focus vào nội dung, không phải metadata reject.
2. **Funnel data scattered** — mỗi article md có funnel của batch đó, không có view nhìn tổng.
3. **Multi-ticker `/tin-hot N` runs** — không có cách group, list flat 12+ batch rows trộn lẫn lịch sử.
4. **No history page** — user không có cách xem "5 lần run gần đây fetched bao nhiêu, reject pattern thế nào".

## 3. Out of scope (defer V1.1+)

- **Pagination/chunking** of pipeline-runs.json — V1.0 ship single file. V1.1 add monthly partition khi file > 5MB.
- **Real-time live progress** (show pipeline đang chạy) — V1.0 chỉ history (completed sessions).
- **Per-source analytics** (vd "VnEconomy reject rate Q1: 45%") — defer V2.
- **Funnel reject pattern analytics** (vd "Top 5 reject reasons last 7 days") — defer V2.
- **Export to CSV** — defer V1.1.
- **Filter by reject reason** — defer V1.1 (V1.0: ticker + date + status only).

## 4. Architecture overview

### 3-layer architecture

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: SQL persistence (extend crawl_log schema)      │
│   - ADD: session_id, trigger_type, trigger_args         │
│   - Index: session_id, crawled_at                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Backend builder (lib/render_compare_feed.py)   │
│   - NEW build_pipeline_runs_manifest()                  │
│   - Query crawl_log JOIN generated_news GROUP BY session│
│   - Write output/compare-feed/pipeline-runs.json        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 3: Frontend (React)                               │
│   - NEW route /pipeline-runs → PipelineRunsPage         │
│   - 3-level browse: Session → Batch → Funnel detail     │
│   - REMOVE article RightColumn section 5 crawl_funnel   │
│   - ADD batch_id hyperlink in article header            │
└─────────────────────────────────────────────────────────┘
```

### Key changes

| Aspect | Before | After |
|---|---|---|
| Crawl funnel location | RightColumn section 5 per-article | Standalone `/pipeline-runs` page |
| Session grouping | Flat per funnel_batch_id | Grouped by session_id (multi-ticker `/tin-hot` = 1 session) |
| Schema | crawl_log without session metadata | + session_id, trigger_type, trigger_args |
| Build output | manifest.json only | + pipeline-runs.json |
| Article header batch_id | Display only | Hyperlink to `/pipeline-runs?batch_id=<id>` |

## 5. Schema change

### Migration SQL

`lib/migrations/2026-05-12-add-session-grouping.sql`:

```sql
-- Add session grouping fields to crawl_log (V5.1.4 / Subsystem H)

ALTER TABLE crawl_log ADD COLUMN session_id TEXT;
ALTER TABLE crawl_log ADD COLUMN trigger_type TEXT;     -- 'tin' | 'tin-hot' | 'tin-batch'
ALTER TABLE crawl_log ADD COLUMN trigger_args TEXT;     -- 'VHM' | 'N=3' | NULL

CREATE INDEX IF NOT EXISTS idx_crawl_log_session ON crawl_log(session_id);
CREATE INDEX IF NOT EXISTS idx_crawl_log_crawled_desc ON crawl_log(crawled_at DESC);
```

### Backward compatibility

- Pre-V1.0 crawl_log rows có `session_id = NULL` — backend builder treat as "legacy session" (fabricate session_id = funnel_batch_id, trigger_type="tin", trigger_args=ticker).
- No data loss, no rewrite — just NULL handling in query.

### Orchestrator stamp

`.claude/agents/newsroom-pipeline.md` add Step 0:

```python
import uuid
session_id = str(uuid.uuid4())
trigger_type = detect_trigger_type()  # tin/tin-hot/tin-batch
trigger_args = ticker if trigger_type == "tin" else f"N={n}"

# Pass to crawl_log inserts:
db.insert_crawl_row({
    ...,
    "session_id": session_id,
    "trigger_type": trigger_type,
    "trigger_args": trigger_args,
})
```

## 6. Backend builder

### New function in `lib/render_compare_feed.py`

```python
def build_pipeline_runs_manifest(db: PipelineDB, output_path: Path) -> int:
    """Build pipeline-runs.json from crawl_log + generated_news.

    Returns # sessions written.
    Pattern: same as update_manifest() — atomic write to temp + rename.
    """
    # Query: group by session_id, batches by funnel_batch_id
    sessions = _query_sessions(db)
    payload = {"sessions": sessions, "built_at": datetime.now(timezone.utc).isoformat()}

    # Atomic write
    tmp = output_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, output_path)
    return len(sessions)


def _query_sessions(db: PipelineDB) -> list[dict]:
    """Aggregate sessions from crawl_log + generated_news."""
    # Query crawl_log JOIN generated_news for all rows with session_id
    # Group by session_id
    # For each session: group batches by funnel_batch_id
    # For each batch: separate picked (chosen=true) vs rejected
    sessions_dict = {}

    cur = db.conn.execute("""
        SELECT
            cl.session_id,
            cl.trigger_type,
            cl.trigger_args,
            cl.funnel_batch_id,
            cl.ticker,
            cl.sector_code,
            cl.sector_name,
            cl.hot_nhom,
            cl.hot_rank,
            cl.crawled_at,
            cl.source_name,
            cl.source_url,
            cl.published_at,
            cl.editor_v1_decision,
            cl.editor_v1_note,
            cl.story_editor_decision,
            cl.story_editor_reject_label,
            cl.story_editor_reject_reason,
            gn.article_id,
            gn.title AS chosen_title,
            gn.accepted_hypothesis
        FROM crawl_log cl
        LEFT JOIN generated_news gn ON gn.row_id = cl.row_id
        WHERE cl.session_id IS NOT NULL OR cl.funnel_batch_id IS NOT NULL
        ORDER BY cl.crawled_at DESC, cl.session_id, cl.funnel_batch_id
        LIMIT 5000
    """)

    for row in cur.fetchall():
        session_id = row["session_id"] or row["funnel_batch_id"]  # legacy fallback
        if session_id not in sessions_dict:
            sessions_dict[session_id] = {
                "session_id": session_id,
                "trigger_type": row["trigger_type"] or "tin",
                "trigger_args": row["trigger_args"] or row["ticker"],
                "started_at": row["crawled_at"],
                "ended_at": row["crawled_at"],
                "fetched_total": 0,
                "chosen_total": 0,
                "rejected_total": 0,
                "_batches": {},  # build dict first, convert to list later
            }
        session = sessions_dict[session_id]
        session["ended_at"] = max(session["ended_at"], row["crawled_at"])

        batch_id = row["funnel_batch_id"]
        if batch_id not in session["_batches"]:
            session["_batches"][batch_id] = {
                "funnel_batch_id": batch_id,
                "ticker": row["ticker"],
                "sector_code": row["sector_code"],
                "sector_name": row["sector_name"],
                "hot_nhom": row["hot_nhom"],
                "hot_rank": row["hot_rank"],
                "fetched_count": 0,
                "chosen_count": 0,
                "rejected_count": 0,
                "funnel_detail": {"picked": [], "rejected": []},
            }
        batch = session["_batches"][batch_id]
        batch["fetched_count"] += 1
        session["fetched_total"] += 1

        # Classify picked vs rejected
        is_chosen = bool(row["article_id"]) and (row["accepted_hypothesis"] in (True, 1))
        if is_chosen:
            batch["chosen_count"] += 1
            session["chosen_total"] += 1
            batch["funnel_detail"]["picked"].append({
                "source": row["source_name"],
                "url": row["source_url"],
                "published": row["published_at"],
                "reason": f"OK — accepted_hypothesis: true. Title: {row['chosen_title'] or 'N/A'}",
            })
        else:
            batch["rejected_count"] += 1
            session["rejected_total"] += 1
            reject_agent, reject_label, reject_reason = _classify_reject(row)
            batch["funnel_detail"]["rejected"].append({
                "source": row["source_name"],
                "url": row["source_url"],
                "published": row["published_at"],
                "reject_agent": reject_agent,
                "reject_label": reject_label,
                "reason": reject_reason,
            })

    # Convert _batches dict to list, sort by hot_rank then ticker
    sessions = []
    for session_id, session in sessions_dict.items():
        session["batches"] = sorted(
            session["_batches"].values(),
            key=lambda b: (b["hot_rank"] if b["hot_rank"] is not None else 999, b["ticker"])
        )
        del session["_batches"]
        sessions.append(session)

    # Sort sessions by started_at desc
    sessions.sort(key=lambda s: s["started_at"], reverse=True)
    return sessions


def _classify_reject(row: dict) -> tuple[str, str, str]:
    """Returns (reject_agent, reject_label, reject_reason).

    Reject can happen at:
    - Editor V1: editor_v1_decision == "reject" → reject_agent="editor_v1"
    - Story Editor: story_editor_decision == "reject" → reject_agent="story_editor"
    - Master: no generated_news row + Editor + Story passed → reject_agent="master"
    """
    if row["editor_v1_decision"] == "reject":
        return ("editor_v1", row["editor_v1_note"] or "unknown", row["editor_v1_note"] or "")
    if row["story_editor_decision"] == "reject":
        return ("story_editor", row["story_editor_reject_label"] or "unknown", row["story_editor_reject_reason"] or "")
    if not row["article_id"]:
        return ("master", "accepted_hypothesis_false", "Master rejected — no article persisted")
    return ("unknown", "unclassified", "")
```

### Integration in render flow

`render_compare_feed.py` main flow extension:

```python
def main():
    # ... existing render per-article markdown ...

    # NEW V1.0 Subsystem H — build pipeline runs manifest
    output_dir = Path("output/compare-feed")
    runs_path = output_dir / "pipeline-runs.json"
    n = build_pipeline_runs_manifest(db, runs_path)
    print(f"Built pipeline-runs.json with {n} sessions")
```

### Output JSON shape

```json
{
  "built_at": "2026-05-12T15:30:00Z",
  "sessions": [
    {
      "session_id": "abc-def-123",
      "trigger_type": "tin-hot",
      "trigger_args": "N=3",
      "started_at": "2026-05-12T14:30:00Z",
      "ended_at": "2026-05-12T15:15:00Z",
      "fetched_total": 95,
      "chosen_total": 24,
      "rejected_total": 71,
      "batches": [
        {
          "funnel_batch_id": "VHM-20260512-1430",
          "ticker": "VHM",
          "sector_code": "vic3",
          "sector_name": "BDS VIC3",
          "hot_nhom": "tăng_giá",
          "hot_rank": 1,
          "fetched_count": 10,
          "chosen_count": 3,
          "rejected_count": 7,
          "funnel_detail": {
            "picked": [
              {
                "source": "VnEconomy",
                "url": "...",
                "published": "2026-04-21",
                "reason": "OK — accepted_hypothesis: true. Title: Q1/2026 VHM lãi..."
              }
            ],
            "rejected": [
              {
                "source": "CafeF",
                "url": "...",
                "published": "2026-05-08",
                "reject_agent": "story_editor",
                "reject_label": "low_writeability",
                "reason": "Product news nhà ở xã hội 650 triệu — không generate được deep question..."
              }
            ]
          }
        }
      ]
    }
  ]
}
```

## 7. Frontend page UI

### Route registration

`web/src/App.tsx`:

```tsx
<Route path="/pipeline-runs" element={<PipelineRunsPage />} />
```

### PipelineRunsPage layout

```
┌─────────────────────────────────────────────────────────┐
│ Header navigation: [Feed] [Pipeline runs ◀] [Tài liệu] │
├─────────────────────────────────────────────────────────┤
│ Lịch sử pipeline run                                    │
│                                                          │
│ 🔍 [Ticker filter ▼] [📅 Date range ▼] [Status ▼]       │
│ "100 session" → "12/100 session sau filter"             │
├─────────────────────────────────────────────────────────┤
│ ▼ /tin-hot 3 · 12/05 14:30 · 12 ticker × 4 nhóm        │
│   📊 95 fetched, 24 chosen, 71 rejected                 │
│                                                          │
│   ┌── VHM · vic3 · tăng_giá #1 · 10/3/7 [▶]            │
│   ├── FPT · defensive · tăng_giá #2 · 8/2/6 [▶]        │
│   ├── BSR · oilGas · giảm_giá #1 · 12/3/9 [▼]          │
│   │   ✅ ĐÃ CHỌN (3)                                    │
│   │     • VnEconomy 12/05 — OK, data confirm           │
│   │     • Tuổi Trẻ 12/05 — OK, accepted_hypothesis: true│
│   │     • Báo Pháp luật 12/05 — Master picked Q0       │
│   │   ❌ KHÔNG CHỌN (9)                                 │
│   │     • CafeF 11/05 — low_writeability               │
│   │     • Báo Đầu tư 10/05 — low_insight_potential     │
│   │     • ...                                           │
│   └── ... (9 batches more, collapsible)                 │
│                                                          │
├─────────────────────────────────────────────────────────┤
│ ▶ /tin VHM · 12/05 09:55 · single · 10/3/7              │
│ ▶ /tin BSR · 11/05 16:20 · single · 8/2/6               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### URL state

```
/pipeline-runs                            # all sessions
/pipeline-runs?ticker=VHM,BSR             # filter ticker
/pipeline-runs?date=7d                    # last 7 days (also: 30d, all, today)
/pipeline-runs?status=success             # only success (all/success/failed)
/pipeline-runs?batch_id=VHM-20260512-1430 # pre-expand specific batch
```

URL state persists across page reload + sharing.

### Component breakdown

| Component | Responsibility | Lines |
|---|---|---|
| `PipelineRunsPage` | Page shell + filter bar + URL state | ~200 |
| `PipelineSession` | Session row collapsed + expanded batches | ~80 |
| `PipelineBatch` | Batch row collapsed + funnel detail | ~60 |
| `CrawlFunnel` (reuse) | Detail picked/rejected list | (existing) |

## 8. Filter scope (MVP V1.0)

### 3 filters

| Filter | Type | Options |
|---|---|---|
| **Ticker** | Multi-select | All Finpath universe (~139 mã from Spec F) + plus "All" |
| **Date range** | Single-select | Hôm nay / 7 ngày / 30 ngày / Tất cả |
| **Status** | Single-select | Tất cả / Success (chosen_total ≥ 1) / Failed (chosen_total == 0) |

### Filter logic

```typescript
function applyFilters(
  sessions: PipelineSession[],
  filters: FilterState
): PipelineSession[] {
  let result = sessions;
  if (filters.tickers.length > 0) {
    result = result.filter((s) =>
      s.batches.some((b) => filters.tickers.includes(b.ticker))
    );
  }
  if (filters.dateRange !== 'all') {
    const cutoff = computeCutoff(filters.dateRange);
    result = result.filter((s) => new Date(s.started_at) >= cutoff);
  }
  if (filters.status !== 'all') {
    result = result.filter((s) =>
      filters.status === 'success' ? s.chosen_total > 0 : s.chosen_total === 0
    );
  }
  return result;
}
```

## 9. Article view changes

### RightColumn.tsx — remove section 5

Read existing `RightColumn.tsx`. Remove the section rendering CrawlFunnel:

```tsx
// REMOVE this section:
{meta.crawl_funnel && (
  <CrawlFunnel data={meta.crawl_funnel} funnelBatchId={meta.funnel_batch_id} />
)}
```

Right column count: 7 → 6 sections (Skeptic already paused 2026-05-12, funnel removed now).

### CompareFeedLayout.tsx — hyperlink batch_id

Current:

```tsx
🕐 Crawled {formatCrawledAt(meta.crawled_at)} · Funnel batch: {meta.funnel_batch_id}
```

New (V1.0):

```tsx
🕐 Crawled {formatCrawledAt(meta.crawled_at)} · Funnel batch:{' '}
<a
  href={`/pipeline-runs?batch_id=${meta.funnel_batch_id}`}
  className="text-brand hover:underline"
>
  {meta.funnel_batch_id}
</a>
```

Reader click batch_id → jump to `/pipeline-runs` filtered with batch pre-expanded.

### types.ts — keep CrawlFunnelData

Component `CrawlFunnel.tsx` + types `CrawlFunnelData/FunnelItem` KEEP — reused trong PipelineRunsPage. Just relocate consumer from RightColumn → PipelineBatch.

### Header.tsx — add nav link

Add link "Pipeline runs" to header navigation, similar to existing "Feed" + "Tài liệu" links.

## 10. Data flow

```
1. Pipeline trigger: /tin <X> or /tin-hot N
   ↓
2. Orchestrator Step 0: generate session_id (uuid)
   ↓
3. Crawler Step 1: insert crawl_log row với session_id + trigger_type + trigger_args
   ↓
4. Editor V1 / Story Editor / Master / Skeptic: update crawl_log rows + insert generated_news
   ↓
5. Render Step 6:
   - Per-article markdown (existing)
   - update manifest.json (existing)
   - NEW: build_pipeline_runs_manifest() → pipeline-runs.json
   ↓
6. Git publish Step 7: commit + push includes pipeline-runs.json
   ↓
7. GitHub Pages serves pipeline-runs.json statically
   ↓
8. React PipelineRunsPage fetches → renders 3-level browse
```

## 11. Pagination strategy

### V1.0 ship: single file

Estimated size:
- ~12 batch/day × 5KB each = 60KB/day
- 6 tháng = ~10MB single file
- Acceptable cho GitHub Pages serving + browser parse

### V1.1 trigger: file > 5MB

When `pipeline-runs.json` > 5MB:
- Partition monthly: `pipeline-runs-2026-05.json`, `pipeline-runs-2026-06.json`
- Add `pipeline-runs-index.json` listing partitions + date ranges
- React lazy-load chunks (on-scroll OR via filter date selection)

Defer to V1.1 — KHÔNG implement V1.0.

## 12. Edge cases

| Case | Handling |
|---|---|
| Pre-V1.0 crawl_log (no session_id) | Fabricate session_id = funnel_batch_id, trigger_type="tin", trigger_args=ticker. No data loss. |
| Session với 0 ticker fetched (all Editor V1 reject) | Still show session row "0 fetched". Useful debug signal. |
| Session in progress (partial) | KHÔNG show — `build_pipeline_runs_manifest` only includes sessions với generated_news.published_at set OR all batches có editor_v1_decision != null. |
| Multi-day batch (rare) | Group by session_id only. Date display = started_at. Note "X giờ chạy" if duration > 1h. |
| `/tin single` run | trigger_type="tin", trigger_args=ticker, 1 batch. No "Hot nhóm" badge. Cleaner UI. |
| Article deleted but funnel data still in crawl_log | Show batch with chosen_count > 0 but link to article 404 — gracefully show "[Article unavailable]" |
| URL `batch_id` không exist trong data | Show filter result empty + "Không tìm thấy batch" message |
| Cold cache load (no pipeline-runs.json yet) | First page load triggers `render_compare_feed.py` rerun or display "Chưa có data" message |

## 13. File touch list

### NEW files

```
# Backend
lib/migrations/2026-05-12-add-session-grouping.sql                      (~15 lines)

# Frontend
web/src/pages/PipelineRunsPage.tsx                                       (~200 lines)
web/src/components/PipelineSession.tsx                                   (~80 lines)
web/src/components/PipelineBatch.tsx                                     (~60 lines)
web/src/lib/pipelineRunsLoader.ts                                        (~30 lines)

# Tests
tests/test_build_pipeline_runs_manifest.py                               (~150 lines)
web/src/pages/PipelineRunsPage.test.tsx                                  (~100 lines)
```

**Total NEW**: 7 files.

### MODIFY files

```
# Backend
lib/render_compare_feed.py                                               (+150 lines: builder function)
.claude/agents/newsroom-pipeline.md                                      (+15 lines: Step 0 session_id)

# Frontend
web/src/types.ts                                                         (+50 lines: PipelineSession types)
web/src/App.tsx                                                          (+1 line: route)
web/src/components/RightColumn.tsx                                       (-5 lines: remove section 5)
web/src/components/CompareFeedLayout.tsx                                 (+5 lines: batch_id hyperlink)
web/src/components/Header.tsx (or equivalent nav)                        (+5 lines: nav link)

# CLAUDE.md
CLAUDE.md                                                                (+10 lines: pipeline runs note)
```

**Total MODIFY**: 8 files.

**Grand total**: 15 files. Effort: ~1.5 ngày với subagent-driven.

## 14. Testing strategy

### Backend unit tests

`tests/test_build_pipeline_runs_manifest.py`:

- Empty crawl_log → empty sessions list
- 1 session 1 batch → correct shape
- 1 session N batch (tin-hot) → batches sorted by hot_rank then ticker
- Mix legacy (no session_id) + V1.0 rows → legacy fabricated correctly
- Reject classification: editor_v1, story_editor, master
- Picked + rejected counts match aggregates

### Frontend tests

`web/src/pages/PipelineRunsPage.test.tsx`:

- Render with mock data → 3-level structure
- Filter ticker → only sessions với matching batches
- Filter date range → cutoff applied
- Filter status → only success or failed
- URL state hydration → batch_id pre-expanded
- Click batch row → expand funnel detail

### Integration test

- `tests/integration/test_pipeline_runs_end_to_end.py`:
  - Run `/tin VHM` → generate pipeline-runs.json
  - Verify session_id in crawl_log
  - Verify pipeline-runs.json has session
  - Run `/tin-hot 2` → 8 batches grouped under 1 session

### Regression

- Article page still renders correctly (no funnel section but no broken layout)
- Article header batch_id is clickable, navigation works

## 15. Rollout

### Phase 1 — Schema + backend (Tasks 1-3)

1. SQLite migration `2026-05-12-add-session-grouping.sql`
2. Orchestrator Step 0 session_id generation
3. `build_pipeline_runs_manifest()` function + tests

### Phase 2 — Frontend page (Tasks 4-6)

4. `PipelineRunsPage` + types + loader
5. `PipelineSession` + `PipelineBatch` components
6. Filter UI + URL state hydration

### Phase 3 — Article view adjustments (Tasks 7-8)

7. Remove RightColumn section 5
8. CompareFeedLayout batch_id hyperlink + Header nav link

### Phase 4 — Verification (Task 9)

9. End-to-end smoke + CLAUDE.md note

**Estimated effort**: 9 tasks × ~1 hour avg = ~9 hours = **~1.5 ngày** với subagent parallel.

## 16. Open questions / deferred

### Deferred to V1.1+

- **Pagination** (file > 5MB) — V1.1
- **Filter by reject reason** (vd "low_writeability") — V1.1
- **Per-source analytics** (VnEconomy reject rate) — V2
- **Export CSV** — V1.1
- **Real-time live progress** — V2
- **Funnel reject pattern heatmap** — V2

### Resolved (2026-05-12 PM user review)

- **Q1 RESOLVED — tiếng Việt**: Header nav label = **"Lịch sử pipeline"** (Vietnamese, consistent với project tone).

- **Q2 RESOLVED — skip legacy hoàn toàn**: Backend builder filter `WHERE session_id IS NOT NULL`. Pre-V1.0 crawl_log rows (legacy, no session_id) → KHÔNG show trong pipeline-runs.json. Simpler logic — no fabrication needed.

- **Q3 RESOLVED — simple readable style**: Article header `batch_id` hyperlink dùng default link style (underline + brand color). KHÔNG icon đặc biệt.

### Impact của resolutions

- §6 builder SQL update: ADD `WHERE cl.session_id IS NOT NULL` filter (drop legacy fabrication code).
- §12 edge case "Pre-V1.0 crawl_log" REMOVED — legacy rows simply excluded.
- §9 hyperlink style simplified — same pattern as existing links.
- §13 file impact unchanged.

### Other open questions DEFERRED to V1.1+

- **Pagination** (file > 5MB) — V1.1
- **Filter by reject reason** (vd "low_writeability") — V1.1
- **Per-source analytics** (VnEconomy reject rate) — V2
- **Export CSV** — V1.1
- **Real-time live progress** — V2
- **Funnel reject pattern heatmap** — V2

## 17. Spec changelog

```
- V1.0 (2026-05-12 PM) — Initial spec from brainstorming session
  - Subsystem H — Pipeline Run History standalone page /pipeline-runs
  - Schema change: crawl_log + session_id, trigger_type, trigger_args
  - Backend builder: build_pipeline_runs_manifest() → pipeline-runs.json
  - Frontend: 3-level browse Session → Batch → Funnel detail
  - Article RightColumn section 5 REMOVED + batch_id hyperlink in header
  - Filter MVP: ticker + date + status
  - Pagination defer V1.1 (single file V1.0)
  - File impact: 7 NEW + 8 MODIFY = 15 files. ~1.5 ngày.
  - Rationale: User feedback "phần này cho mỗi bài viết không cần nữa,
    nhưng không bỏ — cần xem lịch sử pipeline runs"

- V1.0.1 (2026-05-12 PM) — 3 open question resolutions
  - Q1: Header nav label = "Lịch sử pipeline" (Vietnamese)
  - Q2: Skip legacy crawl_log rows hoàn toàn (WHERE session_id IS NOT NULL)
  - Q3: Article header batch_id hyperlink = default link style (underline + brand color)
  - Impact: builder SQL simpler, edge case "Pre-V1.0 rows" removed
```
