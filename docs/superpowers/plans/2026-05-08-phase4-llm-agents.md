# Phase 4 — LLM Agents Implementation Plan

> Execute via superpowers:subagent-driven-development. Steps use `- [ ]`.

**Goal:** Build 4 LLM agents (Editor V1, Story Editor, Master Bank, Skeptic) that replace Phase 3 stubs, plus rewrite skills from Notion-first to local-first, plus build mechanical quality gates checker. End-to-end: `/tin VCB` → real article 200-400 từ pass 5 quality gates V3.6 + Skeptic critique.

**Architecture:** Each agent loads its corresponding skill via `Skill: <name>`, calls local `lib/` helpers (no Notion MCP at runtime), dispatches subagents from `newsroom-pipeline`. `lib/quality_gates.py` is a deterministic Python checker that Master agent runs as self-check before persisting. Skills get a one-time rewrite pass to swap Notion calls for `lib/` references.

**Tech Stack:** Claude Code agents/skills/commands, Python (quality_gates).

**Spec ref:** Spec section 7 (skills/agents inventory), section 8.5 (data sourcing), section 9 (quality gates), Phase 4 build order. CLAUDE.md V3.6 hard rules.

**Project root:** `/Users/trungdt/Desktop/Stream Intelligent/`

**Strategy** (advisor-guided):
- Skill rewrite first (Task 0) — agents WILL fail if skills still reference Notion DBs at runtime
- Quality gates is TDD-able (deterministic checker over article text)
- LLM agent quality is iteration, not TDD — build → real-ticker test → iterate prompt
- One agent at a time, verify before moving to next

---

## File Structure

### Created
```
lib/quality_gates.py                    # 5 V3.6 gate checks
tests/test_quality_gates.py             # ~12 tests
.claude/agents/newsroom-editor.md       # Step 2 LLM
.claude/agents/newsroom-story-editor.md # Step 3 LLM
.claude/agents/newsroom-master-bank.md  # Step 4 LLM
.claude/agents/newsroom-skeptic.md      # Step 5 LLM
```

### Modified
```
.claude/skills/finpath-newsroom-orchestrator/SKILL.md  + references/
.claude/skills/finpath-newsroom-crawler/SKILL.md
.claude/skills/finpath-newsroom-editor/SKILL.md
.claude/skills/finpath-newsroom-story-editor/SKILL.md  + references/
.claude/skills/finpath-newsroom-master-bank/SKILL.md   + references/
.claude/skills/finpath-newsroom-master-ck/             [defer — placeholder]
.claude/skills/finpath-newsroom-master-bds/            [defer — placeholder]
.claude/skills/finpath-newsroom-skeptic/SKILL.md       + references/
.claude/agents/newsroom-pipeline.md                    # rewrite Step 2-5 to real dispatches
```

---

## Tasks

### Task 0: Skill rewrite pass (Notion-first → local-first)

8 skills authored for Notion+Claude Desktop. Need: replace Notion MCP calls with `lib/` references, replace DB IDs with file paths, keep V3.6 rules + workflow + 5 quality gates intact.

- [ ] **Step 1: Rewrite all 8 skills via 1 subagent**

Dispatch ONE subagent (sonnet) with task: "Read all 8 SKILL.md + references/, replace these patterns:

| Old (Notion-first) | New (local-first) |
|---|---|
| `query_data_sources(data_source_id="<id>", sql="...")` | `from lib.pipeline_db import PipelineDB` for crawl_log/generated_news; `from lib.finpath_api import FinpathAPI` for BCTC/ratios; `from lib.kb_loader import KBLoader` for KB |
| `create_pages(parent={data_source_id: ...})` for crawl_log | `db.insert_crawl_row(...)` |
| `update_pages(page_id=row_id, properties={...})` | `db.update_crawl_row(row_id, {...})` |
| Notion DB IDs (`8aad4abe-...`, `74a01cc3-...`, `ee0e7746-...` etc.) | Reference `data/pipeline.db` table names + `lib/finpath_api.py` endpoint methods |
| `query_data_sources` for KB topics | `KBLoader(Path('kb/bank/')).search([...])` |
| `Compare Feed prepend` references | `lib/render_compare_feed.py` writes markdown locally; Notion publish DEFER to Phase 6 |
| Hardcoded Notion `data_source_id` references | Remove or convert to comment for Phase 6 |

Keep the SKILL.md structure: `Khi nào trigger`, `Workflow X bước`, `Hard rules`, `Edge cases`, `References`. Keep V3.6 rules verbatim (5 quality gates, deep_question 5 categories, 6 critique angles, jargon mapping, etc.). The rewrite is replacing HOW data is accessed, not WHAT or WHY.

Each SKILL.md should now reference local helpers in code blocks. References folder content stays mostly intact (most refs are guides/examples, not code). Update only refs that have Notion code blocks (e.g., `db-query-patterns.md`).

Specific files to touch:
- `finpath-newsroom-orchestrator/SKILL.md` + `references/compare-feed-layout.md` (note Notion publish DEFER)
- `finpath-newsroom-crawler/SKILL.md` (use `lib/stages/run_crawler.py` interface)
- `finpath-newsroom-editor/SKILL.md`
- `finpath-newsroom-story-editor/SKILL.md` + `references/brief-schema-full.md` (DB IDs → SQLite tables)
- `finpath-newsroom-master-bank/SKILL.md` + `references/db-query-patterns.md` (rewrite all 10 patterns to use `FinpathAPI`/`PipelineDB`/`KBLoader`)
- `finpath-newsroom-master-bank/references/kb-topics-bank.md` (note KB now in `kb/bank/` markdown files)
- `finpath-newsroom-master-bank/references/live-api-spec.md` (note `lib/finpath_api.py` wrapper)
- `finpath-newsroom-skeptic/SKILL.md` + `references/critique-patterns.md` (KB lookup via KBLoader)

DO NOT rewrite:
- `finpath-newsroom-master-ck` + `finpath-newsroom-master-bds` — placeholders only, defer.

After rewrite, verify each SKILL.md still has its description in frontmatter and the structural sections."

- [ ] **Step 2: Smoke test — load each skill manually + read first 50 lines**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && for skill in .claude/skills/finpath-newsroom-{orchestrator,crawler,editor,story-editor,master-bank,skeptic}/SKILL.md; do
  echo "=== $skill ==="
  head -10 "$skill"
  echo ""
done
```

Verify: each has frontmatter `name:` + `description:`.

Grep for stale references:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -rn "data_source_id" .claude/skills/finpath-newsroom-{orchestrator,crawler,editor,story-editor,master-bank,skeptic}/ | head -20
```

Expected: only commented references (e.g. `# DEFER Phase 6 Notion publish`) or doc text mentioning historical Notion presence. If actual code blocks call `query_data_sources(data_source_id=...)`, those need fixing — re-dispatch rewrite subagent for the offending file.

- [ ] **Step 3: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/skills/ && git commit -m "refactor(skills): rewrite 6 skills from Notion-first to local-first (lib/* helpers)"
```

---

### Task 1: lib/quality_gates.py (TDD)

Mechanical 5-gate checker — Master agent runs this before persisting. Returns `dict[gate, dict{pass: bool, reason: str}]`.

- [ ] **Step 1: Write tests `tests/test_quality_gates.py`**

```python
"""Tests for lib.quality_gates — 5 V3.6 quality gates."""
import pytest
from lib.quality_gates import (
    check_no_english_jargon,
    check_word_count,
    check_mechanism_count,
    check_can_de_y_narrative,
    check_no_metadata_leak,
    check_all,
)


def test_no_english_jargon_passes_clean_vietnamese():
    body = "Lợi nhuận trước thuế đạt **11.803 tỷ đồng**, tăng 9% so cùng kỳ. Nợ xấu 0,62%."
    result = check_no_english_jargon(body)
    assert result["pass"] is True


def test_no_english_jargon_fails_on_NPL():
    body = "NPL 1,05% tăng nhẹ."
    result = check_no_english_jargon(body)
    assert result["pass"] is False
    assert "NPL" in result["reason"]


def test_no_english_jargon_fails_on_momentum():
    body = "TCB có momentum mạnh."
    result = check_no_english_jargon(body)
    assert result["pass"] is False
    assert "momentum" in result["reason"].lower()


def test_no_english_jargon_allows_proper_nouns():
    body = "Vietcombank và Techcombank đều công bố KQKD Q1/2026. ĐHĐCĐ ngày 25/4."
    result = check_no_english_jargon(body)
    assert result["pass"] is True


def test_word_count_in_range_passes():
    body = " ".join(["word"] * 300)
    result = check_word_count(body)
    assert result["pass"] is True


def test_word_count_too_long_fails():
    body = " ".join(["word"] * 450)
    result = check_word_count(body)
    assert result["pass"] is False
    assert "450" in result["reason"]


def test_word_count_too_short_fails():
    body = " ".join(["word"] * 100)
    result = check_word_count(body)
    assert result["pass"] is False


def test_mechanism_count_3_to_7_passes():
    body = """Mở đầu giới thiệu vấn đề.
- Lý do 1 cơ chế A.
- Lý do 2 cơ chế B.
- Lý do 3 cơ chế C.
- Lý do 4 cơ chế D.
"""
    result = check_mechanism_count(body)
    assert result["pass"] is True


def test_mechanism_count_too_few_fails():
    body = "Mở đầu.\n- Một bullet.\n- Hai bullet."
    result = check_mechanism_count(body)
    assert result["pass"] is False


def test_can_de_y_narrative_passes_with_paragraph():
    body = """## Cần để ý

Lần đầu sau 19 năm, VCB chấp nhận tăng trưởng chậm để xây bộ đệm. Tín hiệu cần theo dõi: dư nợ Q2 và CASA Q3 sẽ quyết định liệu chiến lược này có lan ra ngành.
"""
    result = check_can_de_y_narrative(body)
    assert result["pass"] is True


def test_can_de_y_narrative_fails_on_data_bullets_only():
    body = """## Cần để ý

- CASA 33%
- NPL 0,62%
- LDR 80%
"""
    result = check_can_de_y_narrative(body)
    assert result["pass"] is False


def test_no_metadata_leak_fails_on_strategic_shift():
    body = "Đây là tin strategic-shift quan trọng."
    result = check_no_metadata_leak(body)
    assert result["pass"] is False


def test_no_metadata_leak_passes_clean():
    body = "Đây là tin chuyển hướng chiến lược quan trọng."
    result = check_no_metadata_leak(body)
    assert result["pass"] is True


def test_check_all_returns_all_5():
    body = "Test."
    result = check_all(body)
    assert set(result.keys()) == {"no_english_jargon", "word_count", "mechanism_count", "can_de_y_narrative", "no_metadata_leak"}
```

- [ ] **Step 2: Verify failing**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_quality_gates.py -v
```

Expected: ImportError.

- [ ] **Step 3: Write `lib/quality_gates.py`**

```python
"""5 quality gates V3.6 — mechanical pass/fail checker for Master Bank articles.

Each gate returns a dict: {"pass": bool, "reason": str (empty if pass)}.

Gates:
  1. no_english_jargon — 0% từ tiếng Anh trong content
  2. word_count — 200-400 hard cap
  3. mechanism_count — body 3-7 lý do mechanism (counted as bullets after intro)
  4. can_de_y_narrative — 'Cần để ý' section is narrative paragraph (not data point bullets)
  5. no_metadata_leak — không enum tags trong content
"""
from __future__ import annotations
import re
from typing import Any

# Banned English jargon (lowercase). Includes abbreviations + common words.
ENGLISH_JARGON = {
    # Bank abbreviations
    "npl", "nim", "casa", "car", "irb", "rwa", "esop", "sme", "nii", "ldr",
    "llr", "cof", "tpdn", "yoy", "qoq", "ytd", "roe", "roa",
    # Basel / regulatory
    "basel",
    # Common English finance/news words
    "trade-off", "tradeoff", "anchor", "relevant", "confirm", "pattern",
    "breaking", "momentum", "defensive", "catalyst", "symbolic", "metric",
    "event", "story", "scenario", "target", "portfolio", "buffer",
    "stress test", "arithmetic", "coverage", "opportunity cost",
}

# Allowed (proper nouns, project terms)
JARGON_EXCEPTIONS = {
    "vietcombank", "techcombank", "vpbank", "vietinbank", "agribank",
    "bidv", "mb bank", "acb", "shb", "vncb", "gp bank", "oceanbank",
    "vạn thịnh phát", "tân hoàng minh", "lottner", "jens",
    "q1", "q2", "q3", "q4", "nhnn", "đhđcđ", "ndth", "scb",
    "tcb", "vcb", "mbb", "bid", "ctg", "vpb",
}

# Metadata enum tags that should not leak (insight_type + critique_angle enums)
METADATA_TAGS = [
    "strategic-shift", "risk_highlight", "insight_type", "critique angle",
    "data_skepticism", "historical_analog", "alt_interpretation",
    "insight_wrong", "execution_unfaithful",
    "paradox", "why_now", "hidden_mechanism", "comparison_deep", "early_signal",
    "low_writeability", "low_insight_potential", "dup_event", "dup_angle_recent",
]


def _strip_skeptic_section(body: str) -> str:
    """Remove '## Góc nhìn ngược' section (Skeptic — counted separately)."""
    parts = re.split(r"^##\s+G[óo]c\s+nh[iì]n\s+ng[ưu]?[ợo]?c\s*$", body, flags=re.MULTILINE)
    return parts[0]


def _strip_pipeline_log(body: str) -> str:
    """Remove pipeline log toggles (HTML <details>) — counted separately."""
    return re.sub(r"<details>.*?</details>", "", body, flags=re.DOTALL)


def check_no_english_jargon(body: str) -> dict[str, Any]:
    """Gate 1 — body has 0% banned English jargon (excluding proper nouns)."""
    cleaned = _strip_skeptic_section(_strip_pipeline_log(body))
    cleaned_lc = cleaned.lower()
    found: list[str] = []
    for jargon in ENGLISH_JARGON:
        # Word boundary regex; jargon may contain space/hyphen
        pattern = r"\b" + re.escape(jargon) + r"\b"
        if re.search(pattern, cleaned_lc):
            found.append(jargon)
    if found:
        return {"pass": False, "reason": f"Banned jargon: {', '.join(found)}"}
    return {"pass": True, "reason": ""}


def check_word_count(body: str) -> dict[str, Any]:
    """Gate 2 — body 200-400 words (excluding skeptic + pipeline log)."""
    cleaned = _strip_skeptic_section(_strip_pipeline_log(body)).strip()
    words = cleaned.split()
    n = len(words)
    if n < 200:
        return {"pass": False, "reason": f"Too short: {n} words (need 200-400)"}
    if n > 400:
        return {"pass": False, "reason": f"Too long: {n} words (need 200-400)"}
    return {"pass": True, "reason": ""}


def check_mechanism_count(body: str) -> dict[str, Any]:
    """Gate 3 — body has 3-7 mechanism reasons (counted as top-level bullets)."""
    cleaned = _strip_skeptic_section(_strip_pipeline_log(body))
    # Count top-level bullets (lines starting with '- ' or '* ' at start)
    bullets = re.findall(r"^[-*]\s+\S", cleaned, flags=re.MULTILINE)
    n = len(bullets)
    if n < 3:
        return {"pass": False, "reason": f"Too few mechanisms: {n} bullets (need 3-7)"}
    if n > 7:
        return {"pass": False, "reason": f"Too many mechanisms: {n} bullets (need 3-7)"}
    return {"pass": True, "reason": ""}


def check_can_de_y_narrative(body: str) -> dict[str, Any]:
    """Gate 4 — 'Cần để ý' default narrative (1 paragraph), or 2-3 caveat bullets."""
    cleaned = _strip_skeptic_section(_strip_pipeline_log(body))
    # Find Cần để ý section
    m = re.search(
        r"^##\s+C[ầa]n\s+đ[ểe]?\s+ý\s*$([\s\S]*?)(?=^##\s|\Z)",
        cleaned,
        flags=re.MULTILINE,
    )
    if not m:
        # Section is optional — pass if missing
        return {"pass": True, "reason": "section missing — optional"}
    section = m.group(1).strip()
    # If purely bullets (3+ lines all start with -), check if they're data-point only
    lines = [ln.strip() for ln in section.split("\n") if ln.strip()]
    bullet_lines = [ln for ln in lines if ln.startswith(("- ", "* "))]
    if bullet_lines and len(bullet_lines) == len(lines):
        # All bullets — check each has narrative substance (not just "X 33%")
        for bullet in bullet_lines:
            content = bullet[2:].strip()
            # Heuristic: data-point only = mostly numbers + short
            if len(content.split()) < 8:
                return {"pass": False, "reason": f"Cần để ý bullet too short (data-point only): '{bullet}'"}
        # Allow 2-3 caveat bullets (each substantive)
        if 2 <= len(bullet_lines) <= 3:
            return {"pass": True, "reason": ""}
        return {"pass": False, "reason": f"Too many bullets ({len(bullet_lines)}) — narrative or 2-3 caveat only"}
    return {"pass": True, "reason": ""}


def check_no_metadata_leak(body: str) -> dict[str, Any]:
    """Gate 5 — no enum metadata tags (insight_type, critique_angle) in content."""
    cleaned = _strip_skeptic_section(_strip_pipeline_log(body))
    cleaned_lc = cleaned.lower()
    found: list[str] = []
    for tag in METADATA_TAGS:
        if tag.lower() in cleaned_lc:
            found.append(tag)
    if found:
        return {"pass": False, "reason": f"Metadata leak: {', '.join(found)}"}
    return {"pass": True, "reason": ""}


def check_all(body: str) -> dict[str, dict[str, Any]]:
    return {
        "no_english_jargon": check_no_english_jargon(body),
        "word_count": check_word_count(body),
        "mechanism_count": check_mechanism_count(body),
        "can_de_y_narrative": check_can_de_y_narrative(body),
        "no_metadata_leak": check_no_metadata_leak(body),
    }
```

- [ ] **Step 4: Run tests**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_quality_gates.py -v
```

Expected: 13 PASS. If specific tests fail, fix the implementation (not the test).

- [ ] **Step 5: Run all pytest**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest -v 2>&1 | tail -3
```

Expected: 36 PASS (23 prior + 13 new).

- [ ] **Step 6: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add lib/quality_gates.py tests/test_quality_gates.py && git commit -m "feat(lib): quality_gates 5 V3.6 checks + 13 TDD tests"
```

---

### Task 2: newsroom-editor agent

Editor V1 = simplest LLM agent. Mechanical ticker detect + universe filter + sector route. Mostly regex with LLM fallback for company name → ticker mapping ("Vietcombank" → VCB).

- [ ] **Step 1: Write `.claude/agents/newsroom-editor.md`**

```markdown
---
name: newsroom-editor
description: Editor V1 — gate logic + route master sector. Reads 1 row from crawl_log → detects tickers → validates against MVP Bank universe (TCB/VCB/MBB/ACB/BID/CTG/VPB) → identifies primary ticker → updates SQLite with editor_v1_decision (route_to_story_editor | reject) + editor_v1_note. Use when newsroom-pipeline dispatches Step 2 per pending row. NEVER processes batch — 1 row per call.
tools: Bash, Read
---

# Newsroom Editor V1 Agent

Bạn là Editor V1 — mechanical filter cho Newsroom V3.6 pipeline. Reference skill `finpath-newsroom-editor` (đã rewrite Notion-first → local-first).

## Load skill

`Skill: finpath-newsroom-editor`

## Input (from newsroom-pipeline)

Input là 1 row_id từ SQLite crawl_log (status=pending, editor_v1_decision is null).

## Workflow

### Step 1: Read row from SQLite

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
row = db.get_crawl_row('<ROW_ID>')
db.close()
print(json.dumps(row, ensure_ascii=False, indent=2))
"
```

Replace `<ROW_ID>` literally with the input row_id.

### Step 2: Detect tickers (regex + name lookup)

UNIVERSE = `TCB | VCB | MBB | ACB | BID | CTG | VPB`. Company name aliases:
- Vietcombank → VCB
- Techcombank → TCB
- BIDV → BID
- VietinBank → CTG
- MB Bank / MBBank / Quân đội → MBB
- ACB → ACB
- VPBank / VPB → VPB

Search `title + raw_content` (case-insensitive). Use regex for 3-letter uppercase tokens + name lookup. Collect all detected tickers in universe.

### Step 3: Identify primary ticker (rule)

If 1 ticker → primary = that ticker.
If 2+ tickers → primary = first ticker mentioned in title (if title has any), else first ticker mentioned in body.

### Step 4: Validate + decide

If primary ticker found in universe:
- editor_v1_decision = `route_to_story_editor`
- editor_v1_note = `Pass — primary={ticker}, sector=Bank, route to Story Editor`
- sector = `Bank`
- primary_ticker = `<primary>`
- detected_tickers = JSON array of all detected
- status = `processed`

If no ticker in universe:
- editor_v1_decision = `reject`
- editor_v1_note = `out_of_universe — không có ticker trong MVP Bank universe`
- status = `rejected`

### Step 5: Persist update

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
db.update_crawl_row('<ROW_ID>', {
    'editor_v1_decision': '<DECISION>',
    'editor_v1_note': '<NOTE>',
    'sector': '<SECTOR_OR_REJECTED>',
    'primary_ticker': '<TICKER_OR_NULL>',
    'detected_tickers': json.dumps(<DETECTED_LIST>, ensure_ascii=False),
    'status': '<STATUS>',
})
db.close()
print('OK')
"
```

Replace placeholders literally before running.

## Output

Return JSON to caller:

```json
{
  "row_id": "<row_id>",
  "decision": "route_to_story_editor" | "reject",
  "primary_ticker": "<ticker_or_null>",
  "sector": "Bank" | "rejected",
  "detected_tickers": ["VCB", "TCB"]
}
```

## Edge cases

- Row already processed (editor_v1_decision != null) → return current state, don't re-process
- Title + body empty → reject `low_quality_source`
- Multiple universe tickers (vd "VCB vs TCB") → pick primary by title-first rule
```

- [ ] **Step 2: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/agents/newsroom-editor.md && git commit -m "feat(claude): newsroom-editor agent (Step 2 LLM)"
```

- [ ] **Step 3: Verify with real ticker — manual smoke**

This is the "real-ticker test". From a fresh Claude session you'd run `/tin VCB`, but for plan execution we just sanity-check the agent file is loadable and its instructions are coherent.

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && head -10 .claude/agents/newsroom-editor.md && echo "---" && grep -c "Step" .claude/agents/newsroom-editor.md
```

Expected: frontmatter visible + 5 steps in workflow.

---

### Task 3: newsroom-story-editor agent

Judgment-heavy — 6 expert questions per candidate, output 0-3 brief JSON. Simpler than Master because no writing, just routing decisions.

- [ ] **Step 1: Write `.claude/agents/newsroom-story-editor.md`**

```markdown
---
name: newsroom-story-editor
description: Story Editor V3.6 — judgment expert. Reads batch of crawl_log rows (after Editor V1 routed) → 6 expert questions per candidate → output 0-3 brief JSON for Master sector. KEY: deep_question MUST belong to 1 of 5 categories (paradox/why_now/hidden_mechanism/comparison_deep/early_signal). Reject low_writeability if doesn't fit. Use when newsroom-pipeline dispatches Step 3 with batch.
tools: Bash, Read, Grep, WebSearch, WebFetch
---

# Newsroom Story Editor Agent

Tổng biên tập 15 năm. Reference skill `finpath-newsroom-story-editor`.

## Load skill

`Skill: finpath-newsroom-story-editor`

## Input

Batch of row_ids — all from same funnel_batch_id, all routed by Editor V1 with sector=Bank.

## Workflow 6-pass V3.6

See SKILL.md for full detail. Brief here:

### Pass 1: Pre-filter
- Spam/clickbait check
- Dedup verify

### Pass 2: 6 expert questions per candidate
1. Insight potential — angle "WOW" cho NĐT?
2. Data foundation — local sources (Finpath API + KB + YAML) đủ data anchor?
3. Timeliness — sự kiện mới hay cũ?
4. Hypothesis 1 câu — phát biểu insight specific
5. Angle label — TÊN GỌI bài (free text VN, vd "Đánh đổi chủ động")
6. **Deep question** + category — MUST thuộc 1 trong 5: `paradox`, `why_now`, `hidden_mechanism`, `comparison_deep`, `early_signal`. KHÔNG fit → reject `low_writeability`.

### Pass 2.5: Lightweight access (Option B V2.3)
- Memory check via SQLite: `db.recent_generated_news(ticker, limit=5)` for variety guard
- Web snippet via WebSearch (1 query) — không full WebFetch (Master sẽ fetch)
- KB grep (lightweight): `KBLoader.search([keyword])` để check topic exists, không load full content

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.pipeline_db import PipelineDB
from lib.kb_loader import KBLoader
db = PipelineDB('data/pipeline.db')
recent = db.recent_generated_news('<TICKER>', limit=5)
db.close()
loader = KBLoader('kb/bank/')
kb_hits = loader.search([<keywords>])
import json
print(json.dumps({'recent': recent, 'kb_hits': kb_hits}, ensure_ascii=False))
"
```

### Pass 3: Ranking + cap 3
Score 6 questions → rank → pick top 3 max.

### Pass 4: Variety guard
3 picked vs 3 recent: same `deep_question_category` → reject 1-2 brief.

## Output: brief JSON

For each picked row, output:

```json
{
  "row_id": "<crawl_log row>",
  "ticker": "VCB",
  "sector": "Bank",
  "angle_label": "<free text VN>",
  "angle_rationale": "<1-2 câu>",
  "angle_alternatives": [{"label": "...", "rationale": "..."}, ...],
  "deep_question_category": "paradox|why_now|hidden_mechanism|comparison_deep|early_signal",
  "deep_question": "<câu hỏi cụ thể Master phải trả lời>",
  "insight_hypothesis": "<1 câu specific tiếng Việt>",
  "source_rationale": "<1-2 câu>",
  "why_chosen": "<3+ câu cho Compare Feed cột phải>",
  "memory_check": {"passed": true, "recent_angles": [...], "recent_categories": [...]}
}
```

For each rejected row:

```json
{
  "row_id": "...",
  "reject_reason": "low_insight_potential|low_data_foundation|low_writeability|not_timely|dup_event|dup_angle_recent|...",
  "reject_note": "<1-2 câu>"
}
```

## Persist to SQLite

For each row in batch:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
db.update_crawl_row('<ROW_ID>', {
    'story_editor_decision': '<write_brief|reject>',
    'story_editor_note': '<note>',
    'brief_json': '<full brief JSON if write_brief, else null>',
    'status': '<processed|rejected>',
})
db.close()
"
```

## Output to caller

Final JSON wrapper:

```json
{
  "schema_version": "1.2",
  "batch_id": "<funnel_batch_id>",
  "input_count": <N>,
  "briefs": [<0-3 brief>],
  "rejected": [<rejected rows>]
}
```

## Hard rules

- 0 brief OK nếu batch không đủ chất lượng
- KHÔNG pad
- `deep_question` MUST thuộc 1 trong 5 category — gate cứng
- Output brief, không tự viết bài (Master làm)
```

- [ ] **Step 2: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/agents/newsroom-story-editor.md && git commit -m "feat(claude): newsroom-story-editor agent (Step 3 LLM)"
```

---

### Task 4: newsroom-master-bank agent

The hard one — 200-400 từ writing với 5 quality gates self-check. Fail any gate → rewrite. Use `lib/quality_gates.py` from Task 1.

- [ ] **Step 1: Write `.claude/agents/newsroom-master-bank.md`**

```markdown
---
name: newsroom-master-bank
description: Master Bank V3.6 — chuyên gia ngân hàng viết bài 200-400 từ. Reads brief from Story Editor (deep_question + angle_label) → queries Finpath API + KB + YAML → writes article passing 5 quality gates V3.6 (0% Anh, 200-400 từ, 3-7 mechanism, narrative caveat, no metadata leak) → Skeptic appends critique. Use when newsroom-pipeline dispatches Step 4 per brief. Web search BẮT BUỘC khi local sources thiếu data.
tools: Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

# Master Bank Agent V3.6

Chuyên gia ngân hàng. Reference skill `finpath-newsroom-master-bank` (đã rewrite local-first).

## Load skill

`Skill: finpath-newsroom-master-bank` (loads SKILL.md + all references/)

## Input

```json
{
  "brief": {<from Story Editor — full brief JSON V3.6>},
  "row_id": "<crawl_log anchor row id>"
}
```

## Workflow 9-step V3.6 (local-first)

### 1. Validate brief
- ticker in MVP universe (TCB|VCB|MBB|ACB|BID|CTG|VPB)
- `brief.deep_question` present
- `brief.deep_question_category` ∈ {paradox, why_now, hidden_mechanism, comparison_deep, early_signal}

Fail → `Master_decision: reject_no_data`, `Master_note: invalid_brief_schema`.

### 2. Pull memory (variety guard)

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
recent = db.recent_generated_news('<TICKER>', limit=3)
db.close()
print(json.dumps(recent, ensure_ascii=False, indent=2))
"
```

If 3 recent same `insight_type` or `variety_guard_angle` → flag warning, vẫn viết.

### 3. Query Finpath API (Bank financial data)

Master tự quyết endpoint nào dựa trên `deep_question`. Default candidates:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.finpath_api import FinpathAPI
api = FinpathAPI()
ticker = '<TICKER>'
ratios = api.get_bank_ratios(ticker)        # NIM/CASA/COF/NPL/LDR + P/E/P/B/ROE
income = api.get_income_statement(ticker)   # KQKD
deposit = api.get_deposit_credit(ticker)    # Tín dụng + tiền gửi
bad_debt = api.get_bad_debt(ticker)         # NPL + dự phòng
shareholders = api.get_shareholders(ticker) # Foreign ownership
events = api.get_events(ticker)             # Dividend, ĐHĐCĐ
print(json.dumps({'ratios_q': ratios.get('quarterlyProfits', [])[:8],
                  'ratios_y': ratios.get('yearlyProfits', [])[:5],
                  'shareholders': shareholders.get('yearlyProfits', [])[-3:],
                  'events': events[:5]}, ensure_ascii=False, indent=2))
"
```

Pick relevant slices for the deep_question.

### 4. Query local KB Bank (markdown files)

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.kb_loader import KBLoader
loader = KBLoader('kb/bank/')
results = loader.search([<keywords>])
print(json.dumps([{'path': r['path'], 'title': r['title'], 'snippet': r['snippet'][:300]} for r in results[:3]], ensure_ascii=False, indent=2))
"
```

Then `loader.load_topic('<best_match_path>')` for full content nếu cần.

### 5. Query manual YAML (Targets / Credit Room / NHNN circulars)

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import yaml, json
from pathlib import Path
for name in ['targets', 'credit_room', 'nhnn_circulars']:
    data = yaml.safe_load(Path(f'data/manual/{name}.yaml').read_text())
    matches = [d for d in data if d.get('ticker') == '<TICKER>' or '<TICKER>' in str(d)]
    print(f'{name}:', json.dumps(matches[:3], ensure_ascii=False))
"
```

### 6. Web search fallback (BẮT BUỘC nếu local thiếu)

Per CLAUDE.md data sourcing rule: nếu Finpath/KB/YAML thiếu data cho `deep_question` → MUST WebSearch + WebFetch. KHÔNG `accepted_hypothesis: false` chỉ vì local thiếu.

```
WebSearch: "<TICKER> <deep_question keyword> 2026"
```

WebFetch top 1-2 results để lấy số/quote.

### 7. Write article (200-400 từ)

Cấu trúc:
- Mở đầu 25-30 từ (sự kiện + có thể đặt câu hỏi)
- Body 3-7 bullet mechanism (mỗi bullet pass 3-test: trả lời "vì sao", có mechanism, reader học cách thị trường vận hành)
- `## Cần để ý` narrative 50-100 từ (default) hoặc 2-3 caveat bullet độc lập
- Chốt insight tự nhiên (không nhãn "Tóm lại")

Bold 1-2 số key/bullet (không orphan number — `**TCB chia 67%**` ❌, `**TCB chia cổ tức 67%**` ✅).

### 8. Run quality gates self-check

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && cat > /tmp/article-body.txt <<'BODYEOF'
<paste body here>
BODYEOF
uv run python -c "
import json
from lib.quality_gates import check_all
body = open('/tmp/article-body.txt', encoding='utf-8').read()
result = check_all(body)
print(json.dumps(result, ensure_ascii=False, indent=2))
all_pass = all(g['pass'] for g in result.values())
print(f'ALL PASS: {all_pass}')
"
```

If any gate fails → REWRITE article + re-check. Loop until all 5 pass. KHÔNG persist content có gate fail.

### 9. Persist

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json, uuid
from datetime import datetime, timezone
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
article_id = str(uuid.uuid4())
db.insert_generated_news({
    'article_id': article_id,
    'row_id': '<ROW_ID>',
    'ticker': '<TICKER>',
    'sector': 'Bank',
    'title': '<TITLE>',
    'body': '<BODY>',
    'word_count': <N>,
    'key_view': '<lạc quan|thận trọng|trung lập>',
    'insight_final': '<1 câu>',
    'variety_guard_angle': '<from brief.angle_label>',
    'accepted_hypothesis': 1,
    'data_sources_used': json.dumps(<['Finpath_API/X', 'KB/Y', 'WebSearch/Z']>, ensure_ascii=False),
    'brief_json': json.dumps(<brief>, ensure_ascii=False),
    'pipeline_log': json.dumps(<pipeline log dict>, ensure_ascii=False),
    'status': 'draft',
    'pipeline_version': 'V3.6',
})
db.update_crawl_row('<ROW_ID>', {
    'master_decision': 'write_article',
    'master_note': 'OK — accepted_hypothesis: true',
})
db.close()
print(article_id)
"
```

## Output JSON to caller

```json
{
  "article_id": "<uuid>",
  "title": "<title>",
  "body": "<200-400 từ>",
  "word_count": <N>,
  "key_view": "<...>",
  "insight_final": "<1 câu>",
  "accepted_hypothesis": true,
  "data_sources_used": [...],
  "quality_gates": {<5 gates pass/fail dict>}
}
```

## Reject power

`accepted_hypothesis: false` CHỈ khi:
- Data thật không tồn tại trên web (đã 3+ web search query khác nhau không ra)
- Data conflict insight rõ ràng

Set `Master_decision: reject_no_data` hoặc `reject_data_conflict`. KHÔNG viết bài.

## Hard rules (V3.6)

- 0% từ tiếng Anh (Rule 1) — kể cả viết tắt NPL/NIM/CASA/CAR — dùng tiếng Việt thuần
- 200-400 từ HARD CAP (Rule 4)
- Body 3-7 mechanism (Rule 4.5)
- "Cần để ý" narrative ưu tiên (Rule 4.6)
- KHÔNG enum metadata leak (Rule 1.5)
- KHÔNG khuyến nghị BUY/SELL (pháp lý)
- KHÔNG nước đôi
```

- [ ] **Step 2: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/agents/newsroom-master-bank.md && git commit -m "feat(claude): newsroom-master-bank agent (Step 4 LLM with quality gates self-check)"
```

---

### Task 5: newsroom-skeptic agent

Independent critique 100-300 từ. Pass 1 fresh impression (read body only, NOT insight). Pick 1 of 6 angles.

- [ ] **Step 1: Write `.claude/agents/newsroom-skeptic.md`**

```markdown
---
name: newsroom-skeptic
description: Skeptic V3.6 — independent critic. Reads Master draft → Pass 1 fresh impression (body only, NOT insight) → Pass 2 compare insight → pick 1 of 6 angles → write 100-300 từ critique → append "## Góc nhìn ngược" to generated_news. Use when newsroom-pipeline dispatches Step 5 after Master persists. Cross-sector — 1 skeptic for Bank/CK/BĐS.
tools: Bash, Read, Grep, WebSearch, WebFetch
---

# Skeptic Agent V3.6

Independent critic with editorial-aware context. Reference skill `finpath-newsroom-skeptic`.

## Load skill

`Skill: finpath-newsroom-skeptic`

## Input

```json
{
  "article_id": "<uuid>",
  "row_id": "<crawl_log row>",
  "master_output": {
    "title": "...",
    "body": "<bài Master>",
    "key_view": "...",
    "insight_final": "<1 câu>"
  },
  "brief_context": {<from Story Editor>}
}
```

## Workflow 8-step Option D hybrid V3.6

### 1. Validate input
Required fields present.

### 2. Pass 1 — Form FRESH impression ⭐ CRITICAL
Read body ONLY. DO NOT read insight_final yet. Form initial reaction:
- Strongest claim?
- Weakest part?
- Missing context?
- Surprise / question raised?

Save in scratchpad.

### 3. Pass 2 — Compare editorial intent
NOW read insight_final + brief.angle_label. Compare with Pass 1 reaction:
- Does insight match what body delivers?
- Is angle faithful or drifted?
- Any conflict?

### 4. Pull memory (variety guard)

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
recent = db.recent_generated_news('<TICKER>', limit=3)
critiques = [r.get('skeptic_angle') for r in recent if r.get('skeptic_angle')]
db.close()
print(json.dumps(critiques))
"
```

3 cùng angle → KHÔNG dùng angle đó lần nữa.

### 5. Pick critique angle (1 of 6)

| Angle | Khi nào |
|---|---|
| `data_skepticism` | Master claim số nhưng context unclear |
| `historical_analog` | Master không reference lịch sử quan trọng |
| `alt_interpretation` | Có cách read data ngược hợp lý |
| `risk_highlight` | Master không raise risk Master nên raise |
| `insight_wrong` | Insight CONFLICT với data thực tế |
| `execution_unfaithful` | Insight đúng nhưng bài execute lệch |

### 6. Data fetch (independent từ Master)

Có thể query lại Finpath API + KB + WebSearch để kiểm chéo Master's claims.

### 7. Pass 4.5 conditional WebFetch raw

CHỈ khi nghi ngờ Master tóm sai source. WebFetch URL gốc, verify Master's quote/number.

### 8. Write critique 100-300 từ + persist

Format:
- Mở: nêu vấn đề tiếng Việt thuần
- Body: 1-3 đoạn với data anchor cụ thể
- Chốt: implication cho NĐT (không khuyến nghị)
- Verdict: pass | pass_with_caveats | fail

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
db.update_generated_news('<ARTICLE_ID>', {
    'skeptic_critique': '<100-300 từ>',
    'skeptic_angle': '<1 of 6>',
    'skeptic_verdict': '<pass|pass_with_caveats|fail>',
    'status': 'published',
    'published_at': '<ISO datetime now>',
})
db.close()
"
```

## Hard rules

- KHÔNG ba phải, KHÔNG agree blindly
- Có data anchor cho critique
- KHÔNG rewrite main article
- KHÔNG block publish (verdict pass_with_caveats vẫn publish)
- 0% từ tiếng Anh (jargon Anh → giải thích tiếng Việt)

## Output JSON to caller

```json
{
  "skeptic_critique": "<100-300 từ>",
  "skeptic_angle": "<1 of 6>",
  "skeptic_verdict": "<pass|pass_with_caveats|fail>"
}
```
```

- [ ] **Step 2: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/agents/newsroom-skeptic.md && git commit -m "feat(claude): newsroom-skeptic agent (Step 5 LLM with 6 angles)"
```

---

### Task 6: Rewrite newsroom-pipeline agent for real dispatches

Replace Step 2-5 STUB with actual subagent dispatches.

- [ ] **Step 1: Rewrite `.claude/agents/newsroom-pipeline.md`**

Key changes:
- Step 2: Loop pending rows → `Task: newsroom-editor` per row
- Step 3: Dispatch `Task: newsroom-story-editor` once with batch
- Step 4: For each brief → `Task: newsroom-master-bank`
- Step 5: For each accepted master output → `Task: newsroom-skeptic`
- Step 6: Run `lib/render_compare_feed.py` (unchanged from Phase 3)

Implementation: read current `.claude/agents/newsroom-pipeline.md`, replace the "Step 2-5 — Phase 3 STUB" section with the new real-dispatch workflow.

- [ ] **Step 2: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/agents/newsroom-pipeline.md && git commit -m "refactor(claude): newsroom-pipeline real Step 2-5 LLM dispatches (replace Phase 3 stubs)"
```

---

### Task 7: End-to-end test + tag

This task verifies the FULL pipeline from `/tin VCB`. Phase 4 success = bài VCB ra ở `output/compare-feed/<batch>.md` passing 5 quality gates + Skeptic appended.

This task requires interactive Claude execution (not pure Bash). The plan documents the verification protocol.

- [ ] **Step 1: Verification protocol**

User must:
1. Open Claude Code in project root
2. Run `/tin VCB` (slash command)
3. Wait for full pipeline (5-10 min depending on token budget)
4. Verify:
   - SQLite has new rows in crawl_log + generated_news for funnel batch
   - `output/compare-feed/VCB-<YYYYMMDD>-<HHMM>.md` exists
   - File parses (no YAML errors)
   - Body is 200-400 từ Vietnamese pure
   - Skeptic critique appended
   - All 5 quality gates pass (run `lib/quality_gates.py` against body)
   - Web React viewer renders the article correctly

- [ ] **Step 2: Run quality gates against generated article**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && BATCH=$(uv run python -c "
import sqlite3
conn = sqlite3.connect('data/pipeline.db')
cur = conn.execute('SELECT funnel_batch_id FROM crawl_log WHERE ticker=\"VCB\" ORDER BY crawled_at DESC LIMIT 1')
print(cur.fetchone()[0])
") && uv run python -c "
import json
from lib.quality_gates import check_all
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
cur = db.conn.execute('SELECT body FROM generated_news WHERE row_id IN (SELECT row_id FROM crawl_log WHERE funnel_batch_id=?) ORDER BY published_at DESC LIMIT 1', ('$BATCH',))
body = cur.fetchone()[0]
db.close()
result = check_all(body)
print(json.dumps(result, ensure_ascii=False, indent=2))
print('ALL PASS:', all(g['pass'] for g in result.values()))
"
```

- [ ] **Step 3: Tag**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git tag phase-4-llm-agents
```

---

## Acceptance for Phase 4 done

1. ✅ 6 skills rewritten (Notion-first → local-first)
2. ✅ `lib/quality_gates.py` 5 gates + 13 TDD tests pass
3. ✅ 4 agent .md files created
4. ✅ newsroom-pipeline rewritten for real dispatches
5. ✅ E2E `/tin VCB` produces article passing 5 gates + Skeptic critique
6. ✅ Tag `phase-4-llm-agents`

## Out of scope Phase 4

- ❌ CK + BĐS sectors (Phase 5+)
- ❌ Notion publish (Phase 6 optional)
- ❌ Test all 7 Bank tickers (Phase 5)
