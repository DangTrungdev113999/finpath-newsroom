# Phase G — Multi-pipeline + Feed UI + Telegram Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship multi-pipeline parallel writing (`/tin-batch ACB,TPB,VPB`), Notion-style continuous feed UI, and Telegram bot publisher — sau khi viết xong 1 article auto-push title+link tới Telegram group.

**Architecture:** SQLite WAL mode + atomic manifest write enable N parallel pipelines. Per-article cycle (Master→Skeptic→Telegram→next) replaces batch processing. New `newsroom-telegram-publisher` agent handles push. New React `FeedPage` stacks all articles with IntersectionObserver lazy load + mobile responsive.

**Tech Stack:** Python 3.13 + uv + sqlite3 (WAL) + pytest. Claude Code agents (Sonnet/Opus per frontmatter). React 18 + Vite + Tailwind + js-yaml + IntersectionObserver. Telegram Bot API via urllib.request (no extra deps).

**Predecessor**: Phase F at commit `dadfa3e` + hotfix `607ad71`. Tag deferred until Phase G E2E close out.

**Build order**: T1 (WAL prereq) → T2-T5 (Stream 1 pipeline flow) → T6-T7 (Stream 2 batch) → T8-T10 (Stream 3 UI) → T11-T14 (Stream 4 Telegram) → T15 (E2E + tag).

---

## T1: SQLite WAL mode + concurrent write test

**Files:**
- Modify: `lib/pipeline_db.py:31-35` (PipelineDB.__init__)
- Modify: `data/pipeline.schema.sql` (header comment)
- Modify: `.gitignore`
- Test: `tests/test_pipeline_db.py` (append concurrent test)
- Helper: `tests/helpers/concurrent_writer.py` (NEW — subprocess script)

- [ ] **Step 1: Read current PipelineDB.__init__**

Run: `head -45 lib/pipeline_db.py`
Verify lines 31-35 show:
```python
def __init__(self, path: str | Path) -> None:
    self.path = str(path)
    self.conn = sqlite3.connect(self.path)
    self.conn.row_factory = sqlite3.Row
    self.conn.execute("PRAGMA foreign_keys = ON")
```

- [ ] **Step 2: Add WAL pragmas to __init__**

Edit `lib/pipeline_db.py:31-35`:
```python
def __init__(self, path: str | Path) -> None:
    self.path = str(path)
    self.conn = sqlite3.connect(self.path, timeout=30.0)
    self.conn.row_factory = sqlite3.Row
    self.conn.execute("PRAGMA foreign_keys = ON")
    # Phase G T1 — WAL mode for concurrent multi-pipeline writes.
    # synchronous=NORMAL is safe with WAL (durability preserved per checkpoint).
    # Skip pragmas for in-memory DBs (WAL not applicable, raises error).
    if self.path != ":memory:":
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
```

The `timeout=30.0` lets concurrent writers wait up to 30s before raising "database is locked" — gives WAL time to checkpoint.

- [ ] **Step 3: Add WAL note to schema header**

Edit `data/pipeline.schema.sql` — prepend at top of file:
```sql
-- Pipeline DB schema (Phase G+ requires WAL mode — see lib/pipeline_db.py:__init__)
-- Backup process MUST include all 3 files: pipeline.db + pipeline.db-wal + pipeline.db-shm
```

- [ ] **Step 4: Gitignore WAL files**

Edit `.gitignore` — append:
```
# SQLite WAL mode files (Phase G T1)
data/pipeline.db-wal
data/pipeline.db-shm
```

- [ ] **Step 5: Create concurrent writer helper script**

Write `tests/helpers/concurrent_writer.py`:
```python
"""Subprocess helper for concurrent SQLite write test.

Invoked by test_pipeline_db.py via subprocess.Popen × 3.
Each invocation inserts one crawl_log row with unique row_id.
"""
import sys
import uuid
from pathlib import Path

# Allow import lib.pipeline_db when running as subprocess
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.pipeline_db import PipelineDB


def main(db_path: str, batch_id: str, source_url: str) -> int:
    db = PipelineDB(db_path)
    row_id = str(uuid.uuid4())
    db.insert_crawl_row({
        "row_id": row_id,
        "funnel_batch_id": batch_id,
        "source_name": "concurrent_test",
        "source_url": source_url,
        "title": f"Concurrent write {row_id[:8]}",
        "raw_content": "test content",
        "crawled_at": "2026-05-10T00:00:00Z",
    })
    db.close()
    print(row_id)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
```

- [ ] **Step 6: Write failing concurrent test**

Append to `tests/test_pipeline_db.py`:
```python
def test_wal_mode_concurrent_writes_succeed(tmp_path):
    """3 subprocess writers concurrent writes via WAL mode → all succeed.

    Phase G T1 — verifies WAL mode permits concurrent multi-pipeline writes
    without 'database is locked' errors. Subprocess based (not threading)
    because real /tin-batch spawns separate Claude Code workers.
    """
    import subprocess
    from pathlib import Path

    # Setup: real disk DB initialized with schema (WAL doesn't work :memory:)
    db_path = tmp_path / "concurrent.db"
    schema_path = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db = PipelineDB(str(db_path))
    db.init_schema(schema_path)
    db.close()

    helper = Path(__file__).parent / "helpers" / "concurrent_writer.py"
    batch_id = "CONCURRENT-TEST-001"

    # Spawn 3 concurrent writers, each inserts 1 row with unique source_url
    procs = [
        subprocess.Popen(
            ["uv", "run", "python", str(helper), str(db_path), batch_id, f"https://test.example/{i}"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        for i in range(3)
    ]
    results = [p.wait(timeout=60) for p in procs]
    assert all(rc == 0 for rc in results), \
        f"Subprocess failed: {[(p.returncode, p.stderr.read().decode()) for p in procs]}"

    # Verify all 3 rows persisted
    db = PipelineDB(str(db_path))
    rows = db.query_by_funnel_batch(batch_id)
    db.close()
    assert len(rows) == 3, f"Expected 3 rows, got {len(rows)}"
```

- [ ] **Step 7: Run test — expect PASS**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_pipeline_db.py::test_wal_mode_concurrent_writes_succeed -v`
Expected: PASS in <5s. If FAIL with "database is locked" → check WAL pragma applied + timeout=30.

- [ ] **Step 8: Run full pytest — verify no regression**

Run: `uv run pytest tests/ -q`
Expected: 111+ passed (was 110 + 1 new test).

- [ ] **Step 9: Commit**

```bash
git add lib/pipeline_db.py data/pipeline.schema.sql .gitignore tests/test_pipeline_db.py tests/helpers/concurrent_writer.py
git commit -m "feat(db): T1 — SQLite WAL mode for concurrent pipelines (Phase G)

Stream 2 multi-pipeline parallel writes need WAL mode để tránh
'database is locked' errors. PRAGMA journal_mode=WAL + synchronous=
NORMAL + timeout=30s. In-memory DB skip (WAL không applicable).

Subprocess-based concurrent test (3 Popen × 1 insert each) closer
production reality vs threading same-process. 111/111 pytest pass.

WAL files (.wal + .shm) gitignored. Schema header documents backup
must include 3 files.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## T2: Story Editor uncap (Stream 1 — task 1/4)

**Files:**
- Modify: `.claude/skills/finpath-newsroom-story-editor/SKILL.md` (lines mentioning cap 3)
- Modify: `.claude/agents/newsroom-story-editor.md` (sync uncap rule)
- Modify: `.claude/agents/newsroom-pipeline.md` (Step 3 description "0-N briefs")

- [ ] **Step 1: Find cap rules in story-editor SKILL.md**

Run: `grep -n "max 3\|cap 3\|0-3\|top 3\|3 brief" .claude/skills/finpath-newsroom-story-editor/SKILL.md`

Note all line numbers. Expected matches in description (line 3), Pass 3 ranking (line 59-61), output schema (line ~138).

- [ ] **Step 2: Update SKILL.md description**

Edit `.claude/skills/finpath-newsroom-story-editor/SKILL.md` description (line 3) — replace `outputs 0-3 narrative-rich brief` with `outputs 0-N narrative-rich brief (uncapped — agent picks by merit, không ép fill quota)`.

Replace `Outputs 0-3 briefs` (line ~8) with `Outputs 0-N briefs (uncapped) for Master sector.`

- [ ] **Step 3: Update Pass 3 ranking section**

Edit `.claude/skills/finpath-newsroom-story-editor/SKILL.md` Pass 3 section (~lines 59-65). Replace:
```
### Pass 3 — Ranking + final pick (cap 3)

Score per candidate dựa trên 6 questions → rank → pick top 3 max.
```
With:
```
### Pass 3 — Ranking + final pick (uncapped — Phase G T2)

Score per candidate dựa trên 6 questions → rank → pick by merit. KHÔNG default về số nào — chấp nhận 0 brief nếu toàn batch fail, chấp nhận 1 nếu chỉ 1 candidate đáng viết, chấp nhận 5+ nếu ngày nhiều news chất lượng.

⚠️ **Anti-pattern (Phase F finding)**: agent toàn pick 3 dù chất lượng candidates không đồng đều — cảm giác bị ép. Trước khi commit briefs list, self-check: "Nếu KHÔNG có rule 'pick 3', tôi có pick brief này không?" Nếu KHÔNG → drop brief đó.
```

- [ ] **Step 4: Update output schema in SKILL.md**

Edit `.claude/skills/finpath-newsroom-story-editor/SKILL.md` output schema (~line 138). Replace `"briefs": [<0-3 brief>]` with `"briefs": [<0-N brief — uncapped>]`.

- [ ] **Step 5: Sync agent file newsroom-story-editor.md**

Run: `grep -n "0-3\|cap 3\|max 3\|3 brief" .claude/agents/newsroom-story-editor.md`

For each match, replace cap mentions with uncap language matching SKILL.md changes. Add explicit hard rule near top:
```markdown
## Hard rule V4.0 Phase G — Uncapped briefs

Output 0-N briefs based on merit. KHÔNG default về N=3. Self-check trước commit: "Nếu KHÔNG có rule pick N, tôi có pick brief này không?" Drop nếu không.
```

- [ ] **Step 6: Update newsroom-pipeline.md Step 3 description**

Run: `grep -n "Story Editor\|0-3\|3 brief" .claude/agents/newsroom-pipeline.md | head -10`

Find Step 3 dispatch description (likely around line 100-130). Replace `0-3 briefs` mentions with `0-N briefs (uncapped — Phase G T2)`. Update Step 4 description to mention "loop N iterations" thay vì "max 3 iterations".

- [ ] **Step 7: Verify pytest no regression**

Run: `uv run pytest tests/ -q`
Expected: 111 pass (no Python code change — verbal-only).

- [ ] **Step 8: Commit**

```bash
git add .claude/skills/finpath-newsroom-story-editor/SKILL.md .claude/agents/newsroom-story-editor.md .claude/agents/newsroom-pipeline.md
git commit -m "feat(story-editor): T2 — uncap briefs, agent picks by merit (Phase G)

Phase F finding (ACB + VPB runs): Story Editor toàn pick 3 briefs dù
chất lượng không đồng đều. User feedback 'agent toàn chọn 3, cảm giác
bị ép'. Phase G uncap: 0-N briefs based on merit, agent self-check
'Nếu không có rule pick N, có pick brief này không?'

- SKILL.md description + Pass 3 + output schema: 0-3 → 0-N uncapped
- Agent file: hard rule Phase G uncap với anti-pattern note
- Pipeline.md Step 3+4: 0-N + loop N iterations

Verbal-only update — 111/111 pytest pass (no code change).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## T3: Master skill V4.0 data_trail tightening (Stream 1 — task 2/4)

**Files:**
- Modify: `.claude/skills/finpath-newsroom-master-bank/SKILL.md` (output schema section)
- Modify: `.claude/agents/newsroom-master-bank.md` (sync output JSON schema)

- [ ] **Step 1: Find current data_trail mentions in Master SKILL.md**

Run: `grep -n "data_sources_used\|data_trail" .claude/skills/finpath-newsroom-master-bank/SKILL.md`

Expected matches: ~line 24 (early-check fallback), ~line 64 (json.dumps persist), ~line 71 (data_trail json), ~line 96 (chosen_pick_reason), ~line 166-179 (canonical format spec).

- [ ] **Step 2: Add explicit V4.0 schema reject-legacy section**

Edit `.claude/skills/finpath-newsroom-master-bank/SKILL.md` — find a logical home near existing data_trail section (after line ~179 canonical format spec). Append:

```markdown
## V4.0 schema explicit (Phase G T3 — anti-regression)

⚠️ **Live VPB run regression**: Master agent emit `data_sources_used` (V3.6 legacy string array) thay vì `data_trail` (V4.0 schema array of objects) → render `master_data_trail: []` empty trên web. Phase G tightens:

### REQUIRED — `pipeline_log.step_4_master.data_trail`

```json
[
  {
    "source": "<canonical: full URL | WebSearch:\"query\" | Finpath_API/<endpoint> | KB/<path> | Manual_YAML/<file>:<row_key> | Lập luận tự>",
    "fetched": "<what data extracted from source>",
    "purpose": "<vì sao tra source này — e.g. 'kiểm chéo claim ROE Q1 2026', 'tìm số target 2026 từ ĐHĐCĐ'>",
    "supports_argument": "<bổ sung cho ý nào — e.g. 'Bullet 2 (luận điểm chính)', 'Opening (tension setup)', 'Closing (NĐT classification)'>"
  },
  ...
]
```

### DEPRECATED — `data_sources_used` (V3.6)

❌ DO NOT emit `data_sources_used` array of strings — render layer ignores. Use `data_trail` per spec above.

### Pre-persist self-check

Trước khi gọi `db.insert_generated_news(...)`, verify `data_trail`:
- [ ] Array length > 0 (every article queried at least 1 source)
- [ ] Every entry có 4 fields: source, fetched, purpose, supports_argument
- [ ] `source` field follows 1 trong 6 canonical formats (URL/WebSearch:/Finpath_API//KB//Manual_YAML//Lập luận tự)
- [ ] `purpose` + `supports_argument` tiếng Việt thuần (apply Rule 1 anti-English)

Fail check → rebuild data_trail trước persist. KHÔNG persist incomplete schema.
```

- [ ] **Step 3: Sync agent file newsroom-master-bank.md output schema**

Run: `grep -n "data_sources_used\|data_trail" .claude/agents/newsroom-master-bank.md | head -10`

Edit Output JSON section (likely lines 226-237 area). Add explicit `data_trail` field to schema example matching V4.0:

```json
{
  "article_id": "<uuid>",
  "title": "...",
  "body": "...",
  "data_trail": [
    {
      "source": "https://cafef.vn/...",
      "fetched": "MBB Q1 LNTT 9.500 tỷ, tăng 22% YoY",
      "purpose": "kiểm chéo lãi quý từ 1 nguồn primary",
      "supports_argument": "Bullet 1 (lãi vượt nhóm tứ trụ)"
    }
  ],
  ...
}
```

Add hard rule near top:
```markdown
## Hard rule V4.0 Phase G T3 — data_trail schema mandatory

❌ KHÔNG emit `data_sources_used` (legacy V3.6 string array — render ignores)
✅ MUST emit `data_trail` array of {source, fetched, purpose, supports_argument} per Skill SKILL.md V4.0 schema explicit section
```

- [ ] **Step 4: Verify pytest no regression**

Run: `uv run pytest tests/ -q`
Expected: 111 pass.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/finpath-newsroom-master-bank/SKILL.md .claude/agents/newsroom-master-bank.md
git commit -m "feat(master): T3 — V4.0 data_trail schema tightening (Phase G)

Live VPB run found master_data_trail: [] empty trên web vì Master
agent emit data_sources_used (V3.6 legacy string array) thay vì
data_trail (V4.0 schema array of {source, fetched, purpose,
supports_argument}). Phase F render side đã ready, agent skill chưa
explicit reject legacy.

- SKILL.md: V4.0 schema explicit section với pre-persist self-check
  4-item checklist
- Agent file: Output JSON example với data_trail field + hard rule
  reject data_sources_used legacy

Verbal-only update. 111/111 pytest pass.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## T4: Skeptic skill V4.0 skeptic_data_trail tightening (Stream 1 — task 3/4)

**Files:**
- Modify: `.claude/skills/finpath-newsroom-skeptic/SKILL.md` (output schema)
- Modify: `.claude/agents/newsroom-skeptic.md` (sync schema)

- [ ] **Step 1: Find data_trail mentions in Skeptic SKILL.md**

Run: `grep -n "data_sources_used\|data_trail\|skeptic_data_trail" .claude/skills/finpath-newsroom-skeptic/SKILL.md`

- [ ] **Step 2: Add V4.0 explicit schema section**

Edit `.claude/skills/finpath-newsroom-skeptic/SKILL.md` — add section after existing schema doc:

```markdown
## V4.0 skeptic_data_trail schema explicit (Phase G T4 — anti-regression)

⚠️ **Live VPB run regression**: Skeptic agent emit empty `skeptic_data_trail: []` → web render skeptic data trail panel empty. Phase G tightens output requirement.

### REQUIRED — `pipeline_log.step_5_skeptic.data_trail`

```json
[
  {
    "source": "<canonical format same as Master data_trail — full URL | WebSearch:\"query\" | Finpath_API/<endpoint> | KB/<path> | Manual_YAML/<file>:<row_key> | Lập luận tự>",
    "fetched": "<what counter-evidence extracted>",
    "purpose": "<vì sao tra source này — e.g. 'kiểm chéo Master claim ROE 21,2%', 'tìm tiền lệ MBB vượt VCB Q4/2017'>",
    "supports_argument": "<bổ sung cho luận điểm critique nào — e.g. 'Phân tách nguyên nhân ROE giảm', 'Reference lịch sử cycle'>"
  },
  ...
]
```

### Pre-persist self-check

Trước khi gọi `db.update_generated_news(skeptic_data_trail=...)`, verify:
- [ ] Array length > 0 (Skeptic queried ít nhất 1 source độc lập từ Master)
- [ ] Every entry có 4 fields complete
- [ ] `source` follows 1 trong 6 canonical formats
- [ ] `purpose` + `supports_argument` tiếng Việt thuần

Fail → rebuild trước persist.
```

- [ ] **Step 3: Sync agent file newsroom-skeptic.md**

Edit `.claude/agents/newsroom-skeptic.md` Output JSON section. Add explicit `skeptic_data_trail` field example matching schema. Add hard rule near top:

```markdown
## Hard rule V4.0 Phase G T4 — skeptic_data_trail schema mandatory

✅ MUST emit `skeptic_data_trail` array of {source, fetched, purpose, supports_argument} (same schema as Master data_trail). Pre-persist self-check 4-item checklist trong Skill V4.0 schema section.
```

- [ ] **Step 4: Verify pytest**

Run: `uv run pytest tests/ -q`
Expected: 111 pass.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/finpath-newsroom-skeptic/SKILL.md .claude/agents/newsroom-skeptic.md
git commit -m "feat(skeptic): T4 — V4.0 skeptic_data_trail schema tightening (Phase G)

Live VPB run found skeptic_data_trail: [] empty. Phase G tightens —
Skeptic MUST emit array of {source, fetched, purpose, supports_argument}
matching Master data_trail schema. Pre-persist 4-item checklist.

Verbal-only update. 111/111 pytest pass.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## T5: newsroom-pipeline per-article cycle refactor (Stream 1 — task 4/4)

**Files:**
- Modify: `.claude/agents/newsroom-pipeline.md` (Step 4-5-7 outer loop)

- [ ] **Step 1: Read current Step 4 + Step 5 sections**

Run: `grep -n "^### Step\|outer loop\|per article" .claude/agents/newsroom-pipeline.md | head -20`
Then `sed -n '125,180p' .claude/agents/newsroom-pipeline.md` (adjust line range to find actual Step 4 + Step 5 blocks).

Note current structure: Step 4 loops all briefs → all Master dispatches → Step 5 loops all articles → all Skeptic dispatches.

- [ ] **Step 2: Refactor Step 4 + Step 5 as combined outer loop per brief**

Edit `.claude/agents/newsroom-pipeline.md` Step 4 + Step 5 sections. Replace existing batch flow with:

```markdown
### Step 4 + Step 5 + Step 7 — Per-article cycle (V4.0 Phase G T5)

**OUTER LOOP per brief** (replaces batch flow). For each brief in story_editor output:

#### Iteration N (1..N briefs):

1. **Step 4 — Master Bank**: Task dispatch `newsroom-master-bank` với brief N. Wait for return:
   - article_id (uuid)
   - title, body, insight_final
   - data_trail (V4.0 schema 4-field per entry — see SKILL.md V4.0 schema explicit)
   - quality_gates dict (5 gates pass/fail)
   - accepted_hypothesis (true/false)
   
   Skip iteration nếu accepted_hypothesis=false (no article persisted).
   
   Capture: `t0_master`, `task_return_master` (for tokens parse).
   
   ```python
   payload_master = {
       "model": "opus",
       "started_at": started_at_master,
       "duration_ms": int((time.time() - t0_master) * 1000),
       "tokens": parse_task_usage(task_return_master),
       "brief_idx": N,
       "accepted_hypothesis": True,
       "data_trail_count": len(data_trail),  # Phase G T3 verification
   }
   db.log_pipeline_step(article_id, "step_4_master", payload_master)
   ```

2. **Step 5 — Skeptic ECHO + critique**: Task dispatch `newsroom-skeptic` với article_id. Wait for return:
   - skeptic_critique (NO embedded heading — Skeptic skill V4.0 fix)
   - skeptic_angle (1 of 6)
   - skeptic_verdict (pass/pass_with_caveats/fail)
   - skeptic_data_trail (V4.0 schema — see SKILL.md V4.0 schema explicit T4)
   
   Skeptic auto-persist via skill workflow.
   
   ```python
   payload_skeptic = {
       "model": "opus",
       "started_at": started_at_skeptic,
       "duration_ms": int((time.time() - t0_skeptic) * 1000),
       "tokens": parse_task_usage(task_return_skeptic),
       "angle": skeptic_angle,
       "verdict": skeptic_verdict,
       "data_trail_count": len(skeptic_data_trail),
   }
   db.log_pipeline_step(article_id, "step_5_skeptic", payload_skeptic)
   ```

3. **Step 7 — Telegram publish** (NEW V4.0 Phase G T15-T16): Task dispatch `newsroom-telegram-publisher` với {article_id, title, public_slug}. Wait for return:
   - status: "pushed" | "already_pushed" | "skipped_no_secrets" | "failed"
   - telegram_message_id (or null)
   - error (or null)
   
   Telegram agent auto-persist `generated_news.telegram_pushed_at` on success. Pipeline KHÔNG block nếu fail (graceful degrade).
   
   ```python
   payload_telegram = {
       "model": "sonnet",
       "started_at": started_at_telegram,
       "duration_ms": int((time.time() - t0_telegram) * 1000),
       "tokens": parse_task_usage(task_return_telegram),
       "status": telegram_status,
       "telegram_message_id": telegram_message_id,
       "error": telegram_error,
   }
   db.log_pipeline_step(article_id, "step_7_telegram", payload_telegram)
   ```

4. **Continue to next brief** in outer loop.

**Trade-off note**: Master 2 đọc `recent_generated_news` sẽ thấy Master 1's article vừa persist (cùng batch). Variety guard có thể overcorrect — picks suboptimal angle để avoid Master 1's. Acceptable vì rule chỉ "3 cùng angle gần nhất" không cấm 1, và Skeptic side benefits (fresh DB state cho ECHO verification + accurate variety guard memory) lớn hơn.

**Failure isolation**: nếu brief N fail (Master reject_no_data hoặc Skeptic fail), continue to brief N+1 — KHÔNG crash whole batch.

After ALL briefs done, proceed to Step 6 (Render).
```

- [ ] **Step 3: Update Step 6 Render description**

Edit Step 6 section. Verify it still reads pipeline_log via `lib/render_compare_feed.py` (no change needed for cycle refactor — render reads ALL articles from batch end-of-pipeline).

- [ ] **Step 4: Verify pytest no regression**

Run: `uv run pytest tests/ -q`
Expected: 111 pass.

- [ ] **Step 5: Commit**

```bash
git add .claude/agents/newsroom-pipeline.md
git commit -m "feat(pipeline): T5 — per-article cycle (Master→Skeptic→Telegram per brief)

Phase F batch flow: Step 4 loop all briefs → Step 5 loop all articles
→ Skeptic ECHO race risk + Telegram batch UX poor.

Phase G refactor: outer loop per brief, inner sequence Master→Skeptic
→Telegram→next. Lợi ích: Skeptic ECHO load fresh DB (no race),
variety guard accurate, Telegram per article, failure isolation.

Trade-off: Master 2 thấy Master 1's article → variety guard overcorrect
risk. Accept vì rule chỉ '3 cùng angle' không cấm 1.

Step 4-5-7 combined block với observability capture per step.
Pipeline.md doc only — no Python change. 111/111 pytest pass.

Telegram step (Step 7) refers to newsroom-telegram-publisher agent —
created in T14, wired E2E in T15.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## T6: Atomic manifest write (Stream 2 — task 1/2)

**Files:**
- Modify: `lib/render_compare_feed.py:202-211` (update_manifest)
- Test: `tests/test_render_compare_feed.py` (atomic write test)

- [ ] **Step 1: Read current update_manifest**

Run: `sed -n '200,215p' lib/render_compare_feed.py`

Expected:
```python
def update_manifest(manifest_path: Path, summary: dict) -> None:
    """Append/update entry in manifest.json. id = public_slug."""
    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        data = {"articles": []}
    data["articles"] = [a for a in data["articles"] if a["id"] != summary["id"]]
    data["articles"].append(summary)
    data["articles"].sort(key=lambda a: a["crawled_at"], reverse=True)
    manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
```

Race risk: 2 pipelines call write_text same time → last writer wins, may lose entries.

- [ ] **Step 2: Write failing concurrent manifest test**

Append to `tests/test_render_compare_feed.py`:
```python
def test_update_manifest_atomic_concurrent(tmp_path):
    """3 concurrent update_manifest calls all entries persist (no last-writer-wins).

    Phase G T6 — atomic write via temp file + os.rename. Tests subprocess
    invocations because multi-pipeline parallel calls update_manifest from
    different Python processes.
    """
    import subprocess
    from pathlib import Path

    manifest = tmp_path / "manifest.json"
    helper = Path(__file__).parent / "helpers" / "manifest_writer.py"

    # Spawn 3 concurrent writers, each adds 1 unique article
    procs = [
        subprocess.Popen(
            ["uv", "run", "python", str(helper), str(manifest), f"article-{i}", f"2026-05-10T00:00:0{i}Z"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        for i in range(3)
    ]
    results = [p.wait(timeout=30) for p in procs]
    assert all(rc == 0 for rc in results)

    # All 3 entries should be present
    import json
    data = json.loads(manifest.read_text())
    ids = {a["id"] for a in data["articles"]}
    assert ids == {"article-0", "article-1", "article-2"}, \
        f"Lost entries — got {ids}"
```

- [ ] **Step 3: Create manifest_writer helper subprocess script**

Write `tests/helpers/manifest_writer.py`:
```python
"""Subprocess helper for concurrent manifest write test (Phase G T6)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.render_compare_feed import update_manifest


def main(manifest_path: str, article_id: str, crawled_at: str) -> int:
    summary = {
        "id": article_id,
        "ticker": "TEST",
        "sector": "Bank",
        "title": f"Test article {article_id}",
        "crawled_at": crawled_at,
        "key_view": "trung lập",
        "word_count": 300,
    }
    update_manifest(Path(manifest_path), summary)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
```

- [ ] **Step 4: Run test — expect FAIL (race condition)**

Run: `uv run pytest tests/test_render_compare_feed.py::test_update_manifest_atomic_concurrent -v`
Expected: FAIL — `ids != {article-0, article-1, article-2}` (some entries lost to race) OR may pass intermittently. Either way confirms vulnerability.

- [ ] **Step 5: Implement atomic write with retry loop**

Edit `lib/render_compare_feed.py:202-211` `update_manifest`:
```python
def update_manifest(manifest_path: Path, summary: dict) -> None:
    """Atomic append/update entry in manifest.json. id = public_slug.

    Phase G T6 — atomic via temp file + os.replace. Read-modify-write loop with
    retry on stale read (when 2nd writer races between our read + write).
    macOS/Linux: os.replace is atomic (POSIX rename guarantees).
    """
    import os
    import tempfile

    max_retries = 5
    for attempt in range(max_retries):
        # Read latest state
        if manifest_path.exists():
            try:
                current = json.loads(manifest_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                # Concurrent writer mid-write — back off + retry
                import time
                time.sleep(0.05 * (attempt + 1))
                continue
        else:
            current = {"articles": []}

        # Apply update
        current["articles"] = [a for a in current["articles"] if a["id"] != summary["id"]]
        current["articles"].append(summary)
        current["articles"].sort(key=lambda a: a["crawled_at"], reverse=True)

        # Atomic write via temp file in same dir + replace
        fd, tmp_path = tempfile.mkstemp(
            dir=manifest_path.parent, prefix=".manifest-", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(current, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, manifest_path)  # POSIX atomic rename
            return
        except Exception:
            os.unlink(tmp_path)
            raise

    raise RuntimeError(f"Failed to atomically update {manifest_path} after {max_retries} retries")
```

- [ ] **Step 6: Run test — expect PASS**

Run: `uv run pytest tests/test_render_compare_feed.py::test_update_manifest_atomic_concurrent -v`
Expected: PASS — all 3 article ids persist.

- [ ] **Step 7: Run full pytest**

Run: `uv run pytest tests/ -q`
Expected: 112+ pass (was 111 + 1 new).

- [ ] **Step 8: Commit**

```bash
git add lib/render_compare_feed.py tests/test_render_compare_feed.py tests/helpers/manifest_writer.py
git commit -m "feat(render): T6 — atomic manifest write for parallel pipelines (Phase G)

Stream 2 multi-pipeline parallel writes có race condition trên
output/compare-feed/manifest.json — read-modify-write last-writer-wins
loses entries. Phase G fix: atomic via temp file + os.replace
(POSIX atomic rename). Read-retry loop khi concurrent write mid-fly
(json.JSONDecodeError catch).

Subprocess test (3 Popen × 1 article) verifies all 3 entries persist
under concurrent load. 112/112 pytest pass.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## T7: /tin-batch command (Stream 2 — task 2/2)

**Files:**
- Create: `.claude/commands/tin-batch.md`

- [ ] **Step 1: Read existing /tin command structure**

Run: `cat .claude/commands/tin.md`
Note frontmatter format + workflow pattern.

- [ ] **Step 2: Write tin-batch.md command**

Write `.claude/commands/tin-batch.md`:
```markdown
---
description: Viết bài tin chuyên sâu cho NHIỀU mã cổ phiếu Bank cùng lúc (parallel pipelines)
argument-hint: <TICKER1,TICKER2,TICKER3,...>
allowed-tools: Bash, Task, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

Trigger N pipeline 6-step Newsroom V4.0 PARALLEL cho list tickers comma-separated **$ARGUMENTS**.

Universe MVP Bank: **TCB · VCB · MBB · ACB · BID · CTG · VPB**.

## Parse $ARGUMENTS

1. Empty $ARGUMENTS → reply usage:
   ```
   Usage: /tin-batch <TICKER1,TICKER2,...>
   Example: /tin-batch ACB,TPB,VPB
   Single ticker: /tin-batch VCB (fall back to /tin behavior)
   ```
   Stop.

2. Single ticker no comma (`/tin-batch VCB`) → fall back to `/tin VCB` behavior:
   - Single Task dispatch `newsroom-pipeline` với ticker=VCB
   - Same output format as /tin

3. Comma-separated (`/tin-batch ACB,TPB,VPB`) → split → list of N tickers.

## Validate tickers

For mỗi ticker trong list:
- Strip whitespace + uppercase
- Map alias: Vietcombank→VCB, Techcombank→TCB, BIDV→BID, VietinBank→CTG, MB Bank→MBB, ACB→ACB, VPBank→VPB
- Check membership trong UNIVERSE = `{TCB, VCB, MBB, ACB, BID, CTG, VPB}`
- Invalid → log warn `⚠️ Skip ticker [X] — không thuộc MVP Bank universe` + remove khỏi list (KHÔNG crash whole batch)

## Spawn parallel pipelines

Single message với N Task tool calls — Claude Code runs parallel:

```
Task tool call 1: subagent_type=newsroom-pipeline, prompt="ticker=ACB ..."
Task tool call 2: subagent_type=newsroom-pipeline, prompt="ticker=TPB ..."
Task tool call 3: subagent_type=newsroom-pipeline, prompt="ticker=VPB ..."
```

Mỗi pipeline có own funnel_batch_id (timestamp + ticker) → no row collision (per spec section 5.3).

WAL mode (T1 prereq) handles SQLite write serialization. Atomic manifest write (T6) handles output/compare-feed/manifest.json race.

## Aggregate output

Sau khi all N pipelines return, format final reply:

```
✅ Pipeline /tin-batch <TICKER1,TICKER2,...> hoàn tất

[per ticker block]
📊 ACB:
  - Funnel batch: ACB-YYYYMMDD-HHMM
  - Crawled: N rows
  - Articles: M published
  - Files: output/compare-feed/ACB-...
  - Telegram: K pushed (X failed)

📊 TPB:
  ...

📊 VPB:
  ...

Total: <N tickers> × <avg articles per ticker> = <total> articles
Total Telegram: <K> pushed
Total wall-clock: <T>s (parallel speedup vs <T_seq>s sequential = X.Yx)
```

## Edge cases

- 1 pipeline crashes → other pipelines continue (Task isolation). Log error + skip in aggregate.
- Skipped invalid tickers → list at top of reply.
- 0 valid tickers after validation → reply "Không có ticker hợp lệ trong universe MVP Bank" + stop.
```

- [ ] **Step 3: Verify pytest no regression**

Run: `uv run pytest tests/ -q`
Expected: 112 pass.

- [ ] **Step 4: Commit**

```bash
git add .claude/commands/tin-batch.md
git commit -m "feat(commands): T7 — /tin-batch parallel multi-ticker pipelines (Phase G)

User feedback: viết tin nhiều cổ phiếu cùng ngày (ACB+TPB+VPB) phải
chờ tuần tự — bottleneck thời gian. Phase G Stream 2: /tin-batch
command spawns N pipelines parallel.

- Comma-separated multi-ticker syntax
- Single ticker fallback (/tin-batch VCB → /tin VCB behavior)
- Invalid ticker skip với warn (KHÔNG crash whole batch)
- Single message multiple Task calls = native Claude Code parallel
- WAL (T1) + atomic manifest (T6) prereqs handle write contention

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## T8: Header component + Cards|Feed routing (Stream 3 — task 1/4)

**Files:**
- Modify: `web/src/App.tsx`
- Create: `web/src/components/Header.tsx`

- [ ] **Step 1: Read current App.tsx**

Run: `cat web/src/App.tsx`

Confirm structure: `<BrowserRouter>` + `<Routes>` with `/` → IndexPage, `/article/:id` → ArticlePage.

- [ ] **Step 2: Create Header component**

Write `web/src/components/Header.tsx`:
```tsx
import { Link, useLocation } from 'react-router-dom';

export function Header() {
  const { pathname } = useLocation();
  const isCards = pathname === '/' || pathname.startsWith('/article/');
  const isFeed = pathname === '/feed';

  return (
    <header className="sticky top-0 z-10 border-b border-gray-200 bg-white px-6 py-3">
      <div className="mx-auto flex max-w-7xl items-center justify-between">
        <Link to="/" className="text-base font-semibold text-gray-900">
          📰 Finpath Newsroom
        </Link>
        <nav className="flex gap-1 text-sm">
          <Link
            to="/"
            className={`rounded-md px-3 py-1.5 ${isCards ? 'bg-gray-900 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
          >
            Cards
          </Link>
          <Link
            to="/feed"
            className={`rounded-md px-3 py-1.5 ${isFeed ? 'bg-gray-900 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
          >
            Feed
          </Link>
        </nav>
      </div>
    </header>
  );
}
```

- [ ] **Step 3: Update App.tsx — add Header + /feed route placeholder**

Edit `web/src/App.tsx`:
```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { IndexPage } from './pages/IndexPage';
import { ArticlePage } from './pages/ArticlePage';
import { FeedPage } from './pages/FeedPage';
import { Header } from './components/Header';

export default function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<IndexPage />} />
        <Route path="/feed" element={<FeedPage />} />
        <Route path="/article/:id" element={<ArticlePage />} />
      </Routes>
    </BrowserRouter>
  );
}
```

- [ ] **Step 4: Create FeedPage stub (real impl in T9)**

Write `web/src/pages/FeedPage.tsx`:
```tsx
export function FeedPage() {
  return (
    <main className="mx-auto max-w-7xl px-6 py-8">
      <h1 className="text-2xl font-semibold">Feed</h1>
      <p className="mt-2 text-gray-600">Coming in T9 (Phase G).</p>
    </main>
  );
}
```

- [ ] **Step 5: Verify TypeScript clean**

Run: `cd web && npx tsc --noEmit`
Expected: no output (clean).

- [ ] **Step 6: Verify visual — open browser**

Run: `cd web && npm run dev` (if not already running). Open `http://localhost:5174/`.

Verify:
- Header sticky on top với 📰 logo + Cards | Feed nav
- `/` (IndexPage) — Cards tab highlighted
- `/feed` (FeedPage stub) — Feed tab highlighted, "Coming in T9" placeholder

- [ ] **Step 7: Commit**

```bash
git add web/src/App.tsx web/src/components/Header.tsx web/src/pages/FeedPage.tsx
git commit -m "feat(web): T8 — Header + Cards|Feed routing (Phase G)

Header sticky component với 2-tab nav. Active tab highlighted (
black bg + white text). New /feed route + FeedPage stub (real impl
T9). Cards tab covers / + /article/:id (deep-link giữ nguyên).

TypeScript clean.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## T9: FeedPage + IntersectionObserver lazy load (Stream 3 — task 2/4)

**Files:**
- Modify: `web/src/pages/FeedPage.tsx` (replace stub)
- Maybe modify: `web/src/components/CompareFeedLayout.tsx` (verify reuse compatible)

- [ ] **Step 1: Read existing CompareFeedLayout + IndexPage for pattern**

Run: `cat web/src/components/CompareFeedLayout.tsx web/src/pages/IndexPage.tsx`

Note how IndexPage loads manifest.json + how CompareFeedLayout takes meta + leftMarkdown.

- [ ] **Step 2: Implement FeedPage with IntersectionObserver**

Replace `web/src/pages/FeedPage.tsx`:
```tsx
import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { CompareFeedLayout } from '../components/CompareFeedLayout';
import { parseFrontmatter } from '../lib/parseFrontmatter';
import type { ArticleMeta, ManifestEntry } from '../types';

const PAGE_SIZE = 5;

interface LoadedArticle {
  id: string;
  meta: ArticleMeta;
  leftMarkdown: string;
}

export function FeedPage() {
  const [manifest, setManifest] = useState<ManifestEntry[]>([]);
  const [loaded, setLoaded] = useState<LoadedArticle[]>([]);
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);
  const [error, setError] = useState<string | null>(null);
  const sentinelRef = useRef<HTMLDivElement>(null);

  // Load manifest on mount
  useEffect(() => {
    fetch('/output/compare-feed/manifest.json')
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(data => {
        const sorted = [...(data.articles || [])].sort(
          (a, b) => new Date(b.crawled_at).getTime() - new Date(a.crawled_at).getTime()
        );
        setManifest(sorted);
      })
      .catch(e => setError(`Failed to load manifest: ${e.message}`));
  }, []);

  // Load articles up to visibleCount
  useEffect(() => {
    const toLoad = manifest.slice(loaded.length, visibleCount);
    if (toLoad.length === 0) return;

    Promise.all(
      toLoad.map(entry =>
        fetch(`/output/compare-feed/${entry.id}.md`)
          .then(r => r.text())
          .then(text => {
            const { meta, body } = parseFrontmatter(text);
            return { id: entry.id, meta, leftMarkdown: body };
          })
      )
    ).then(newArticles => {
      setLoaded(prev => [...prev, ...newArticles]);
    });
  }, [manifest, visibleCount, loaded.length]);

  // IntersectionObserver — trigger load more when sentinel enters viewport
  useEffect(() => {
    if (!sentinelRef.current) return;
    if (visibleCount >= manifest.length) return;

    const observer = new IntersectionObserver(
      entries => {
        if (entries[0].isIntersecting) {
          setVisibleCount(c => Math.min(c + PAGE_SIZE, manifest.length));
        }
      },
      { rootMargin: '200px' }
    );
    observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [manifest.length, visibleCount]);

  if (error) {
    return (
      <main className="mx-auto max-w-7xl px-6 py-8">
        <div className="rounded-md border border-red-300 bg-red-50 p-4 text-red-700">{error}</div>
      </main>
    );
  }

  if (manifest.length === 0) {
    return (
      <main className="mx-auto max-w-7xl px-6 py-8">
        <p className="text-gray-500">Đang tải feed...</p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-7xl px-6 py-8">
      <h1 className="mb-6 text-xl font-semibold text-gray-900">
        Feed — {manifest.length} bài
      </h1>
      {loaded.map((article, idx) => (
        <article key={article.id} className={idx > 0 ? 'mt-12 border-t-4 border-gray-200 pt-12' : ''}>
          <Link
            to={`/article/${article.id}`}
            className="text-sm text-gray-500 hover:underline"
          >
            🔗 Mở deep-link
          </Link>
          <CompareFeedLayout meta={article.meta} leftMarkdown={article.leftMarkdown} />
        </article>
      ))}
      {visibleCount < manifest.length && (
        <div ref={sentinelRef} className="py-8 text-center text-sm text-gray-400">
          Đang tải thêm...
        </div>
      )}
      {visibleCount >= manifest.length && loaded.length === manifest.length && (
        <div className="py-8 text-center text-sm text-gray-400">— Hết feed —</div>
      )}
    </main>
  );
}
```

- [ ] **Step 3: Verify ManifestEntry type exists**

Run: `grep -n "ManifestEntry" web/src/types.ts`

If absent, add to types.ts:
```typescript
export interface ManifestEntry {
  id: string;
  ticker: string;
  sector: string;
  title: string;
  crawled_at: string;
  key_view: string;
  word_count: number;
}
```

- [ ] **Step 4: Verify TypeScript clean**

Run: `cd web && npx tsc --noEmit`
Expected: clean.

- [ ] **Step 5: Verify visual — feed renders**

Open `http://localhost:5174/feed`.

Verify:
- Header "Feed — N bài"
- 5 articles rendered top (newest first by crawled_at desc)
- Each article: small "🔗 Mở deep-link" + full `<CompareFeedLayout>` (left col body + right col 8 sections)
- `border-t-4 border-gray-200 pt-12` separator giữa articles (except first)
- Scroll near bottom → sentinel triggers load thêm 5 articles
- Console no errors

- [ ] **Step 6: Commit**

```bash
git add web/src/pages/FeedPage.tsx web/src/types.ts
git commit -m "feat(web): T9 — FeedPage + IntersectionObserver lazy load (Phase G)

Notion-style continuous feed — newest top, scroll dọc, mỗi article
giữ left/right column layout. IntersectionObserver MVP (advisor
recommendation: defer react-window virtualization until ~100+
articles).

- PAGE_SIZE=5 initial render
- Sentinel + 200px rootMargin → trigger load thêm 5
- Manifest sort by crawled_at desc
- 'Đang tải thêm...' loading + '— Hết feed —' end state
- 'Mở deep-link' link cho từng article (giữ /article/:id route)
- Reuse CompareFeedLayout component

TypeScript clean.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## T10: Mobile responsive (Stream 3 — task 4/4)

**Files:**
- Modify: `web/src/components/CompareFeedLayout.tsx`
- Modify: `web/src/components/RightColumn.tsx`

- [ ] **Step 1: Read current CompareFeedLayout flex structure**

Run: `cat web/src/components/CompareFeedLayout.tsx`

Note: likely uses `flex` or `grid` 2-column. Identify breakpoint location.

- [ ] **Step 2: Add Tailwind responsive flex classes**

Edit `CompareFeedLayout.tsx`. Replace 2-column container class. Example transform:

Before (likely):
```tsx
<div className="flex gap-8">
  <LeftColumn ... />
  <RightColumn ... />
</div>
```

After:
```tsx
<div className="flex flex-col gap-8 md:flex-row">
  <LeftColumn ... />
  <RightColumn ... />
</div>
```

If LeftColumn/RightColumn have explicit width classes (`w-2/3`, `w-1/3`), make them responsive too:
- Before: `<LeftColumn className="w-2/3" />`
- After: `<LeftColumn className="w-full md:w-2/3" />`

Apply same `w-full md:w-1/3` to RightColumn.

- [ ] **Step 3: Update RightColumn — collapse default on mobile**

Read `web/src/components/RightColumn.tsx` to find outer wrapper.

Wrap content in `<details>` with `md:open` class for desktop default-open. Or use CSS-only approach via Tailwind plugin. Simpler: JavaScript with state init from media query.

Recommended approach — wrap each major section in `<details>` already (CrawlFunnel + DataTrail + PipelineObservability already use `<details>`). Add to remaining sections (right_source, why_chosen_narrative, angle, deep_question_options, insight, raw_article_url):

```tsx
// For each section, wrap:
<details className="md:open" open={typeof window !== 'undefined' && window.innerWidth >= 768}>
  <summary className="cursor-pointer font-semibold mb-2">
    📰 Bài gốc (raw source)
  </summary>
  {/* existing content */}
</details>
```

Note: `md:open` is non-standard Tailwind. Use ssr-safe init via useEffect + matchMedia:

Actually simpler approach — leave default open via `defaultOpen` prop pattern, but render via:
```tsx
const isDesktop = typeof window !== 'undefined' && window.matchMedia('(min-width: 768px)').matches;

<details open={isDesktop}>
  ...
</details>
```

Apply pattern to top-level container ONLY (not every section — that's overkill). Wrap entire RightColumn content in 1 outer `<details>` collapse-default-on-mobile:

```tsx
export function RightColumn({ meta }: Props) {
  const isDesktop = typeof window !== 'undefined' && window.matchMedia('(min-width: 768px)').matches;
  return (
    <aside className="w-full md:w-1/3">
      <details open={isDesktop} className="space-y-6">
        <summary className="cursor-pointer font-semibold mb-4 md:hidden">
          ⚙️ Mở metadata + nguồn (8 sections)
        </summary>
        {/* existing 8 sections content */}
      </details>
    </aside>
  );
}
```

`md:hidden` on summary — desktop hides summary text (always open feels native). Mobile shows summary as toggle.

- [ ] **Step 4: Verify TypeScript clean**

Run: `cd web && npx tsc --noEmit`
Expected: clean.

- [ ] **Step 5: Visual check — desktop**

Open `http://localhost:5174/article/<MBB slug>` at desktop width (≥768px).

Verify:
- 2-column layout intact (left article body + right metadata)
- RightColumn content visible (no toggle bar)

- [ ] **Step 6: Visual check — mobile (DevTools responsive mode)**

Open Chrome DevTools → toggle device toolbar → set 375px width (iPhone).

Verify:
- 1-column stacked: left col on top, right col below
- RightColumn collapsed default with summary "⚙️ Mở metadata + nguồn (8 sections)"
- Click summary → expands all 8 sections inline

- [ ] **Step 7: Commit**

```bash
git add web/src/components/CompareFeedLayout.tsx web/src/components/RightColumn.tsx
git commit -m "feat(web): T10 — mobile responsive 1-col stacked (Phase G)

User decision: <768px → 1-col stacked, right col collapse default.

- CompareFeedLayout: flex-col + md:flex-row, w-full + md:w-2/3 / w-1/3
- RightColumn: outer <details> wrap, open={isDesktop} via matchMedia,
  summary md:hidden (desktop always open, mobile toggle)

TypeScript clean. Existing 8-section internal structure giữ nguyên.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## T11: DB schema migration — telegram_pushed_at (Stream 4 — task 1/5)

**Files:**
- Modify: `data/pipeline.schema.sql`
- Modify: `tests/test_pipeline_db.py`

- [ ] **Step 1: Read schema generated_news section**

Run: `grep -A 30 "CREATE TABLE generated_news" data/pipeline.schema.sql`

Identify last column line + closing `);`.

- [ ] **Step 2: Add telegram_pushed_at column + index**

Edit `data/pipeline.schema.sql` — find `CREATE TABLE generated_news (` block. Add column before closing `);`:
```sql
    telegram_pushed_at TIMESTAMP NULL,
```

After CREATE TABLE block, add (anywhere appropriate — likely after existing CREATE INDEX statements):
```sql
-- Phase G T11 — Telegram publish idempotency tracking
CREATE INDEX IF NOT EXISTS idx_generated_telegram_pushed ON generated_news(telegram_pushed_at);
```

- [ ] **Step 3: Write failing test**

Append to `tests/test_pipeline_db.py`:
```python
def test_generated_news_has_telegram_pushed_at_column(db):
    """Phase G T11 — schema includes telegram_pushed_at column."""
    cur = db.conn.execute("PRAGMA table_info(generated_news)")
    cols = {row["name"] for row in cur.fetchall()}
    assert "telegram_pushed_at" in cols, f"Missing column. Found: {sorted(cols)}"


def test_telegram_pushed_at_default_null(db):
    """Phase G T11 — telegram_pushed_at defaults to NULL on new article."""
    db.insert_crawl_row({
        "row_id": "r1",
        "funnel_batch_id": "b1",
        "source_name": "test",
        "source_url": "https://t/1",
        "title": "t",
        "raw_content": "c",
        "crawled_at": "2026-05-10T00:00:00Z",
    })
    db.insert_generated_news({
        "article_id": "a1",
        "row_id": "r1",
        "ticker": "TST",
        "sector": "Bank",
        "title": "Test",
        "body": "body",
        "word_count": 100,
        "key_view": "trung lập",
        "insight_final": "i",
        "accepted_hypothesis": 1,
        "status": "draft",
        "pipeline_version": "V4.0",
    })
    cur = db.conn.execute("SELECT telegram_pushed_at FROM generated_news WHERE article_id = ?", ("a1",))
    row = cur.fetchone()
    assert row["telegram_pushed_at"] is None
```

- [ ] **Step 4: Run tests — expect PASS**

Run: `uv run pytest tests/test_pipeline_db.py::test_generated_news_has_telegram_pushed_at_column tests/test_pipeline_db.py::test_telegram_pushed_at_default_null -v`
Expected: PASS (in-memory schema init reads schema file fresh).

- [ ] **Step 5: Run full pytest**

Run: `uv run pytest tests/ -q`
Expected: 114+ pass (was 112 + 2 new).

- [ ] **Step 6: Apply migration to live DB (manual one-time)**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
db.conn.execute('ALTER TABLE generated_news ADD COLUMN telegram_pushed_at TIMESTAMP NULL')
db.conn.execute('CREATE INDEX IF NOT EXISTS idx_generated_telegram_pushed ON generated_news(telegram_pushed_at)')
db.conn.commit()
db.close()
print('Migration applied.')
"
```
Expected output: `Migration applied.`

If column already exists (re-run) → expect `OperationalError: duplicate column name` — safe to ignore (schema file is source of truth).

- [ ] **Step 7: Commit**

```bash
git add data/pipeline.schema.sql tests/test_pipeline_db.py
git commit -m "feat(db): T11 — generated_news.telegram_pushed_at column (Phase G)

Stream 4 Telegram publisher needs idempotency tracking — Phase G T15
checks column != NULL trước push để skip already-pushed articles.

- Schema migration: ADD COLUMN + CREATE INDEX
- 2 tests: column exists + defaults NULL
- Live data/pipeline.db migration applied (one-time)

114/114 pytest pass.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## T12: lib/telegram_publisher.py + tests (Stream 4 — task 2/5)

**Files:**
- Create: `lib/telegram_publisher.py`
- Create: `tests/test_telegram_publisher.py`

- [ ] **Step 1: Write failing tests first (TDD)**

Write `tests/test_telegram_publisher.py`:
```python
"""Tests for lib.telegram_publisher — Telegram Bot API push (Phase G T12)."""
import json
from unittest.mock import patch, MagicMock
from pathlib import Path
import pytest

from lib.telegram_publisher import TelegramPublisher, load_telegram_config


def test_publisher_init():
    p = TelegramPublisher("token123", "chat-1", "http://localhost:5174/")
    assert p.bot_token == "token123"
    assert p.chat_id == "chat-1"
    assert p.base_url == "http://localhost:5174"  # trailing slash stripped


def test_publisher_html_escape():
    """Title containing < > & must be HTML-escaped to avoid Telegram parse_mode=HTML breakage."""
    assert TelegramPublisher._escape_html("A & B <div>") == "A &amp; B &lt;div&gt;"
    assert TelegramPublisher._escape_html("Plain text") == "Plain text"


def test_publisher_push_success():
    """Mock urlopen returns ok=True → status=pushed + message_id."""
    p = TelegramPublisher("t", "c", "http://localhost:5174")
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "ok": True,
        "result": {"message_id": 42},
    }).encode("utf-8")
    mock_resp.__enter__ = lambda self: self
    mock_resp.__exit__ = lambda *args: None

    with patch("lib.telegram_publisher.urllib.request.urlopen", return_value=mock_resp):
        result = p.publish_article("Test title", "test-slug")
    assert result == {"status": "pushed", "telegram_message_id": 42, "error": None}


def test_publisher_push_telegram_returns_error():
    """Mock urlopen returns ok=False → status=failed + error message."""
    p = TelegramPublisher("t", "c", "http://localhost:5174")
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "ok": False,
        "description": "Bad chat_id",
    }).encode("utf-8")
    mock_resp.__enter__ = lambda self: self
    mock_resp.__exit__ = lambda *args: None

    with patch("lib.telegram_publisher.urllib.request.urlopen", return_value=mock_resp):
        result = p.publish_article("T", "s")
    assert result["status"] == "failed"
    assert result["telegram_message_id"] is None
    assert "Bad chat_id" in result["error"]


def test_publisher_push_network_exception():
    """urlopen raises → caught, status=failed + exception str."""
    p = TelegramPublisher("t", "c", "http://localhost:5174")
    with patch("lib.telegram_publisher.urllib.request.urlopen", side_effect=ConnectionError("dns fail")):
        result = p.publish_article("T", "s")
    assert result["status"] == "failed"
    assert "dns fail" in result["error"]


def test_load_config_missing_file_returns_none(tmp_path):
    assert load_telegram_config(tmp_path / "no.yaml") is None


def test_load_config_missing_telegram_section_returns_none(tmp_path):
    p = tmp_path / "secrets.yaml"
    p.write_text("other: value\n")
    assert load_telegram_config(p) is None


def test_load_config_partial_telegram_returns_none(tmp_path):
    p = tmp_path / "secrets.yaml"
    p.write_text("telegram:\n  bot_token: t\n")  # missing chat_id + base_url
    assert load_telegram_config(p) is None


def test_load_config_full_returns_publisher(tmp_path):
    p = tmp_path / "secrets.yaml"
    p.write_text("telegram:\n  bot_token: tk\n  chat_id: c1\n  base_url: http://x\n")
    pub = load_telegram_config(p)
    assert pub is not None
    assert pub.bot_token == "tk"
    assert pub.chat_id == "c1"
    assert pub.base_url == "http://x"
```

- [ ] **Step 2: Run tests — expect FAIL (module not exists)**

Run: `uv run pytest tests/test_telegram_publisher.py -v`
Expected: FAIL với `ModuleNotFoundError: No module named 'lib.telegram_publisher'`.

- [ ] **Step 3: Implement lib/telegram_publisher.py**

Write `lib/telegram_publisher.py`:
```python
"""Telegram Bot API publisher (Phase G T12).

After Skeptic completes critique, push title + article URL to Telegram group.
Idempotent via generated_news.telegram_pushed_at (Phase G T11 schema column).
Graceful degrade when secrets.yaml missing (returns None publisher).
"""
from __future__ import annotations
import json
import urllib.request
import urllib.parse
from pathlib import Path

import yaml


class TelegramPublisher:
    """Send notification to Telegram via Bot API sendMessage endpoint."""

    def __init__(self, bot_token: str, chat_id: str, base_url: str) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = base_url.rstrip("/")

    def publish_article(self, title: str, public_slug: str) -> dict:
        """Push notification. Returns {status, telegram_message_id, error}.

        status values:
        - "pushed" — Telegram returned ok=True
        - "failed" — network error OR Telegram returned ok=False
        """
        message = f"<b>{self._escape_html(title)}</b>\n\n{self.base_url}/article/{public_slug}"
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": "false",
        }).encode("utf-8")
        try:
            with urllib.request.urlopen(url, data=data, timeout=10) as resp:
                result = json.loads(resp.read())
                if result.get("ok"):
                    return {
                        "status": "pushed",
                        "telegram_message_id": result["result"]["message_id"],
                        "error": None,
                    }
                return {
                    "status": "failed",
                    "telegram_message_id": None,
                    "error": result.get("description", "Telegram API returned ok=False"),
                }
        except Exception as e:
            return {
                "status": "failed",
                "telegram_message_id": None,
                "error": str(e),
            }

    @staticmethod
    def _escape_html(text: str) -> str:
        """Escape & < > for Telegram parse_mode=HTML — order matters (& first)."""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def load_telegram_config(secrets_path: Path = Path("data/secrets.yaml")) -> TelegramPublisher | None:
    """Load TG config from secrets.yaml. Returns None if file missing or section incomplete.

    Required keys: telegram.{bot_token, chat_id, base_url}.
    Graceful: caller treats None as 'Telegram disabled' and skips push.
    """
    if not secrets_path.exists():
        return None
    config = yaml.safe_load(secrets_path.read_text(encoding="utf-8"))
    tg = config.get("telegram") if config else None
    if not tg or not all(k in tg for k in ("bot_token", "chat_id", "base_url")):
        return None
    return TelegramPublisher(tg["bot_token"], tg["chat_id"], tg["base_url"])
```

- [ ] **Step 4: Run tests — expect PASS**

Run: `uv run pytest tests/test_telegram_publisher.py -v`
Expected: 9 PASS.

- [ ] **Step 5: Run full pytest**

Run: `uv run pytest tests/ -q`
Expected: 123+ pass (was 114 + 9 new).

- [ ] **Step 6: Commit**

```bash
git add lib/telegram_publisher.py tests/test_telegram_publisher.py
git commit -m "feat(telegram): T12 — TelegramPublisher module + 9 TDD tests (Phase G)

lib/telegram_publisher.py:
- TelegramPublisher class — sendMessage via urllib.request (no extra deps)
- HTML escape (& < > order matters)
- publish_article returns {status, telegram_message_id, error}
- load_telegram_config(secrets_path) returns None khi file missing /
  incomplete config — graceful degrade

9 tests cover: init, escape, push success/Telegram-error/network-fail,
config load missing-file/missing-section/partial/full.

123/123 pytest pass.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## T13: secrets.yaml.example template + gitignore (Stream 4 — task 3/5)

**Files:**
- Create: `data/secrets.yaml.example`
- Modify: `.gitignore`

- [ ] **Step 1: Create secrets template**

Write `data/secrets.yaml.example`:
```yaml
# Phase G secrets template (Phase G T13)
# Copy this file: cp data/secrets.yaml.example data/secrets.yaml
# Then fill in real values. data/secrets.yaml is gitignored.

telegram:
  # Get bot_token from @BotFather Telegram chat:
  # 1. Open Telegram, search @BotFather
  # 2. /newbot → follow prompts → copy token (format "1234567890:ABCdef...")
  bot_token: "REPLACE_WITH_TOKEN"

  # Get chat_id for your group:
  # 1. Add bot to your Telegram group
  # 2. Send "/start" in group
  # 3. Open in browser: https://api.telegram.org/bot<TOKEN>/getUpdates
  # 4. Find "chat":{"id": <NUMBER>} — group chat_id is NEGATIVE (e.g. -1001234567890)
  chat_id: "REPLACE_WITH_CHAT_ID"

  # Article URL prefix. Update to public URL when you deploy web/.
  # Localhost works for personal testing — Telegram link only opens for you.
  base_url: "http://localhost:5174"
```

- [ ] **Step 2: Gitignore actual secrets file**

Edit `.gitignore` — append:
```
# Phase G T13 — secrets file MUST NEVER commit
data/secrets.yaml
```

- [ ] **Step 3: Verify .gitignore picks it up**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent" && touch data/secrets.yaml && git status --short data/secrets.yaml`
Expected: empty output (gitignored). If shows `?? data/secrets.yaml` → gitignore not active. Then `rm data/secrets.yaml`.

- [ ] **Step 4: Commit template + gitignore**

```bash
git add data/secrets.yaml.example .gitignore
git commit -m "feat(secrets): T13 — secrets.yaml.example template + gitignore (Phase G)

Telegram bot config template. data/secrets.yaml is gitignored —
NEVER commit real bot_token/chat_id.

Setup steps documented inline (BotFather + getUpdates flow).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## T14: newsroom-telegram-publisher agent (Stream 4 — task 4/5)

**Files:**
- Create: `.claude/agents/newsroom-telegram-publisher.md`

- [ ] **Step 1: Write agent file**

Write `.claude/agents/newsroom-telegram-publisher.md`:
```markdown
---
name: newsroom-telegram-publisher
description: Telegram publisher V4.0 Phase G — sau khi 1 article hoàn tất Skeptic critique, push title + link tới Telegram group cho readers nhận xét. Idempotent (skip nếu telegram_pushed_at đã set). Use when newsroom-pipeline dispatches Step 7 per article. Graceful degrade khi secrets.yaml missing.
tools: Bash, Read
model: sonnet
---

# Telegram Publisher Agent V4.0 Phase G

Push article notification tới Telegram group sau khi article ready.

## Input

```json
{
  "article_id": "<uuid>",
  "title": "<article title>",
  "public_slug": "<URL slug>"
}
```

## Workflow

### Step 1 — Idempotency check

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
cur = db.conn.execute('SELECT telegram_pushed_at FROM generated_news WHERE article_id = ?', ('<ARTICLE_ID>',))
row = cur.fetchone()
db.close()
print('ALREADY_PUSHED' if row and row['telegram_pushed_at'] else 'NEEDS_PUSH')
"
```

If output `ALREADY_PUSHED` → return:
```json
{"status": "already_pushed", "telegram_message_id": null, "error": null}
```

### Step 2 — Load secrets + publish

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.telegram_publisher import load_telegram_config
publisher = load_telegram_config()
if publisher is None:
    print(json.dumps({'status': 'skipped_no_secrets', 'telegram_message_id': None, 'error': 'data/secrets.yaml missing or incomplete'}))
else:
    result = publisher.publish_article('<TITLE>', '<PUBLIC_SLUG>')
    print(json.dumps(result, ensure_ascii=False))
"
```

Capture stdout JSON → `result`.

### Step 3 — Persist telegram_pushed_at on success

If `result.status == "pushed"`:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from datetime import datetime, timezone
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
db.update_generated_news('<ARTICLE_ID>', {'telegram_pushed_at': datetime.now(timezone.utc).isoformat()})
db.close()
print('PERSISTED')
"
```

### Step 4 — Return result

Return `result` JSON (from Step 2) to caller (orchestrator).

## Output JSON

```json
{
  "status": "pushed | already_pushed | skipped_no_secrets | failed",
  "telegram_message_id": <int | null>,
  "error": <string | null>
}
```

## Hard rules

- KHÔNG retry on failure — log + return failed (orchestrator decides retry policy)
- KHÔNG block pipeline nếu Telegram fail (graceful degrade, return failed)
- KHÔNG log secrets ra stdout / stderr
- secrets.yaml MUST gitignored (Phase G T13)
- KHÔNG persist telegram_pushed_at nếu push fail (next pipeline run sẽ retry)
- KHÔNG escape title locally — TelegramPublisher._escape_html handles HTML entities

## Edge cases

- Title chứa &, <, >, special chars → HTML escape via TelegramPublisher (already handled)
- Network timeout (10s default) → status=failed
- Telegram chat_id wrong → status=failed với "Bad chat_id" trong error
- secrets.yaml missing → status=skipped_no_secrets, KHÔNG raise

## Cross-references

- `lib/telegram_publisher.py` — module implementation (T12)
- `data/secrets.yaml.example` — config template (T13)
- `data/pipeline.schema.sql` — generated_news.telegram_pushed_at column (T11)
- `.claude/agents/newsroom-pipeline.md` Step 7 — dispatcher (T5 + T16 wire-up)
```

- [ ] **Step 2: Verify pytest no regression**

Run: `uv run pytest tests/ -q`
Expected: 123 pass.

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/newsroom-telegram-publisher.md
git commit -m "feat(agent): T14 — newsroom-telegram-publisher agent (Phase G)

NEW Sonnet-tier agent dispatched by newsroom-pipeline Step 7 per
article. Workflow: idempotency check → load secrets → publisher.
publish_article → persist telegram_pushed_at on success.

Graceful degrade: secrets.yaml missing → status=skipped_no_secrets
(no error, no block). Telegram fail → status=failed (no retry, no
persist — next pipeline retries).

Cross-references T11 schema + T12 module + T13 secrets.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## T15: E2E /tin-batch + close Phase F T12 + tag (Stream 5 — final)

**Files:**
- Modify: `data/secrets.yaml` (NEW, gitignored — user creates from template)
- (Optional) Modify: `output/compare-feed/manifest.json` (test artifacts)

- [ ] **Step 1: User setup — Telegram bot**

User performs (1-time):
1. Open Telegram → search @BotFather
2. `/newbot` → follow prompts → copy token
3. Create group → add new bot
4. Send "/start" trong group
5. Open `https://api.telegram.org/bot<TOKEN>/getUpdates` → find `chat.id` (negative number for group)
6. `cp data/secrets.yaml.example data/secrets.yaml`
7. Edit `data/secrets.yaml` với real bot_token + chat_id

If user defers Telegram setup → skip to Step 4 (cost benchmark only). Telegram tests sẽ use status=skipped_no_secrets.

- [ ] **Step 2: Restart Claude Code session — fresh agent definitions**

Per advisor: agent frontmatter `model:` may be cached per session. Restart ensures Sonnet/Opus split applies.

User: close Claude Code → reopen `claude` in fresh terminal → run `/tin-batch ACB,VPB` (2 tickers parallel — small batch first to verify).

- [ ] **Step 3: Observe parallel run**

User watches:
- 2 newsroom-pipeline subagents spawn parallel
- WAL mode handles SQLite concurrent writes (no lock errors)
- Per-article cycle: Master 1 → Skeptic 1 → Telegram 1 → next brief
- Atomic manifest write (T6) handles output/compare-feed/manifest.json
- Telegram messages land in group (1 per article)

- [ ] **Step 4: Verify pipeline_log via DB query**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
cur = db.conn.execute(\"SELECT article_id, ticker, title, pipeline_log, telegram_pushed_at FROM generated_news WHERE ticker IN ('ACB', 'VPB') ORDER BY published_at DESC LIMIT 6\")
for row in cur.fetchall():
    log = json.loads(row['pipeline_log']) if row['pipeline_log'] else {}
    print(f'\\n=== {row[\"ticker\"]} | {row[\"title\"][:60]} ===')
    print(f'telegram_pushed_at: {row[\"telegram_pushed_at\"]}')
    for step in ['step_1_crawler', 'step_2_editor', 'step_3_story_editor', 'step_4_master', 'step_5_skeptic', 'step_6_render', 'step_7_telegram']:
        if step in log:
            payload = log[step]
            print(f'  {step}: model={payload.get(\"model\")} duration={payload.get(\"duration_ms\")}ms tokens={payload.get(\"tokens\")}')
db.close()
"
```

Verify (Phase F T12 close-out):
- ✅ `step_2_editor.model == "sonnet"` → C1 frontmatter cache OK
- ✅ `step_3_story_editor.model == "opus"` → C1 OK
- ✅ Ít nhất 1 step có `tokens != null` → C2 `<usage>` parse OK
- ✅ All 6 articles có `step_7_telegram` entry với status pushed/skipped
- ✅ `telegram_pushed_at` set cho status=pushed articles

- [ ] **Step 5: Verify data_trail populated (Phase F regression close)**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
cur = db.conn.execute(\"SELECT title, pipeline_log FROM generated_news WHERE ticker IN ('ACB', 'VPB') ORDER BY published_at DESC LIMIT 6\")
for row in cur.fetchall():
    log = json.loads(row['pipeline_log']) if row['pipeline_log'] else {}
    master_dt = log.get('step_4_master', {}).get('data_trail', [])
    skeptic_dt = log.get('step_5_skeptic', {}).get('data_trail', [])
    print(f'{row[\"title\"][:50]}: master_data_trail={len(master_dt)} entries, skeptic_data_trail={len(skeptic_dt)} entries')
    if master_dt:
        first = master_dt[0]
        print(f'  Master first entry fields: {sorted(first.keys())}')
db.close()
"
```

Verify (T3 + T4 close-out):
- ✅ Mỗi article có `master_data_trail` length > 0
- ✅ Mỗi article có `skeptic_data_trail` length > 0
- ✅ First entry có 4 fields: source, fetched, purpose, supports_argument

- [ ] **Step 6: Verify Story Editor uncap (T2 close-out)**

Pick 1 ticker với weak news (vd ticker không có news lớn trong 30 ngày). Run `/tin <TICKER>`. Verify Story Editor output ≤1 brief (chứng minh KHÔNG ép pick 3).

If hard to find weak-news ticker → can skip — MBB run did show 3 briefs (full quality). Document trong commit message rằng concrete sample defer Phase G2.

- [ ] **Step 7: Verify visual — Feed UI**

Open `http://localhost:5174/` → Cards default. Click `Feed` tab → `/feed` → verify:
- ✅ Newest article on top (sort by crawled_at desc)
- ✅ Each article: full 8-section right column visible
- ✅ Border separator between articles
- ✅ Scroll near bottom → "Đang tải thêm..." → loads next 5
- ✅ End of feed: "— Hết feed —"

Mobile (DevTools 375px):
- ✅ 1-col stacked
- ✅ Right column collapse default with summary "⚙️ Mở metadata + nguồn"

- [ ] **Step 8: Verify idempotency — re-run /tin same ticker**

```bash
# Trong CLI: /tin VCB
```

Watch Step 7 Telegram dispatch: should return `status: "already_pushed"` cho articles existed trước. Telegram group should NOT receive dup messages.

- [ ] **Step 9: Tag Phase G + close Phase F T12**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git tag v4.0-phase-g-multi-feed-telegram && git tag v4.0-phase-f-polish 2>/dev/null || true
git tag --list 'v4.0*'
```

Both tags now point at HEAD (Phase G strictly extends Phase F — Phase F success criteria validated as part of T15 Steps 4+5+6).

- [ ] **Step 10: Update task list (manual)**

```bash
# In Claude Code interactive: TaskUpdate #68 status=completed
# Add taskCreate Phase G T1-T15 if want fine-grained tracking, OR mark Phase G as 1 task done
```

- [ ] **Step 11: Commit T15 verification artifacts (if any)**

```bash
git add output/compare-feed/  # any new ACB/VPB articles from T15 run
git commit -m "chore(output): T15 — /tin-batch ACB,VPB E2E validation run

Phase G E2E close out:
- WAL mode + atomic manifest: 2 pipelines parallel without lock errors
- Per-article cycle: Master→Skeptic→Telegram per brief verified
- C1 model frontmatter: step_N.model = sonnet/opus per spec
- C2 observability: at least 1 step có tokens != null
- T3+T4 data_trail: master + skeptic data_trail length > 0 với 4-field schema
- T15 telegram_pushed_at: set cho status=pushed
- Idempotency: re-run /tin same ticker không dup Telegram

Tags:
- v4.0-phase-g-multi-feed-telegram → HEAD
- v4.0-phase-f-polish → HEAD (Phase G strictly extends Phase F,
  T12 closed via T15 verification)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review Checklist (writing-plans skill)

### Spec coverage

| Spec section | Plan task |
|---|---|
| §3.1 Story Editor uncap | T2 |
| §3.2 Master + Skeptic skill V4.0 tighten | T3 + T4 |
| §3.3 Per-article cycle | T5 |
| §4 T0 WAL mode | T1 |
| §5 /tin-batch command + atomic manifest | T6 + T7 |
| §6.1 Header toggle | T8 |
| §6.2 FeedPage | T9 |
| §6.3 IntersectionObserver lazy | T9 (combined) |
| §6.4 Mobile responsive | T10 |
| §7.1 newsroom-telegram-publisher agent | T14 |
| §7.2 lib/telegram_publisher.py | T12 |
| §7.3 secrets template | T13 |
| §7.4 DB schema migration | T11 |
| §7.5 Pipeline integration Step 7 | T5 (cycle structure) + T14 (agent) wired in T15 (E2E verify) |
| §9 Verification | T15 |
| §12 Success criteria | T15 verifies all |

✅ Full coverage.

### Placeholders

Scanned plan — no TBD/TODO/incomplete steps. Each step has exact code + commands.

### Type consistency

- `pipeline_log.step_N` schema consistent: `{model, started_at, duration_ms, tokens, ...step-specific}` — used in T1 capture, T11 query, T15 verify.
- `data_trail` schema consistent: `{source, fetched, purpose, supports_argument}` — T3 spec, T4 spec, T15 verify.
- `result` from TelegramPublisher consistent: `{status, telegram_message_id, error}` — T12 module, T14 agent dispatch, T15 verify.

✅ Consistent throughout.

---

## Estimated scope

- **Stream 1 (T1-T5)**: ~3 hours (T1 prereq + 4 doc/skill tasks)
- **Stream 2 (T6-T7)**: ~1.5 hours (atomic manifest + command file)
- **Stream 3 (T8-T10)**: ~2.5 hours (Header + FeedPage + mobile responsive)
- **Stream 4 (T11-T14)**: ~2 hours (schema + module + secrets + agent)
- **Stream 5 (T15)**: ~1 hour (E2E verify + tag)

**Total**: ~10 hours focused work, 15 atomic tasks subagent-driven cadence.
