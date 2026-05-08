# Pipeline Log Format — Step 1-4

Master tạo `<details>📋 Pipeline log</details>` toggle vào page body row Generated News. Skeptic append Step 5-6 sau (xem skeptic/references/pipeline-log-format.md).

## Format Step 1 — Crawler

```markdown
### Step 1 — Crawler (mục đích: thu thập tin gần đây về [TICKER], chưa filter)
- search 20 nguồn × 3 bài mới nhất → <N> candidates
- dedupe URL với DB Crawl Log → <M> candidates mới
- web_fetch full content → <K> rows successfully created
- Funnel_batch_id: <ticker>-<YYYYMMDD-HHMM>
- Published_time logged: yes/no
```

## Format Step 2 — Editor V1

```markdown
### Step 2 — Editor V1 (mục đích: filter universe + spam + dedupe + route đúng sector)
- candidates input: <N>
- ticker detected per candidate: <list>
- universe filter pass: <X>/<N>
- primary ticker identified: <ticker>
- Editor_V1_decision per row: route_to_story_editor=<X> | reject=<Y>
- routed to: <sector>
```

## Format Step 3 — Story Editor V2.4

```markdown
### Step 3 — Story Editor V2.4 (mục đích: judge depth per-batch, output 0-3 brief)
- batch input: <N> candidates (sector=<X>)
- pass 1 pre-filter: <X> spam/dedupe rejected
- pass 2 expert questions: 4 questions per candidate
- pass 2.5 lightweight access: memory + KB topic + DB metadata + web snippet
- pass 3 final pick: <K> brief (cap 3)
- pass 4 variety guard: <pass / triggered>
- briefs output: <list angle + insight_hypothesis>
- rejected: <list reject_reason>
- batch_id: <ticker>-<YYYYMMDD-HHMM>
```

## Format Step 4 — Master sector

```markdown
### Step 4 — Master <Bank|CK|BĐS> V2.4 (mục đích: viết bài deep-dive từ brief)
- brief input: <angle>
- DB queries: <list DBs queried + rows returned>
- KB queries: <list topics fetched>
- Live API: <called / skipped>
- web search fallback: <queries>
- Bước 7.5 finalize insight: <case 1 confirm | case 2 adjust | case 3 reject>
- accepted_hypothesis: <true | false>
- insight_final: "<1 câu>"
- word count: <N>
- Master_decision: write_article | reject_no_data | reject_data_conflict
```

## Insertion logic

Master tạo toggle empty + 4 step. Skeptic append Step 5-6 vào trong toggle (trước </details>).

```python
master_creates_toggle = """
<details>
<summary>📋 Pipeline log</summary>

### Step 1 — Crawler ...
### Step 2 — Editor V1 ...
### Step 3 — Story Editor V2.4 ...
### Step 4 — Master <sector> V2.4 ...

</details>
"""
```
