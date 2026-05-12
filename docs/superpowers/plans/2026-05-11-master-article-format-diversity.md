# Master Article Format Diversity V5.0 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Phá vỡ pattern dập khuôn 1-format trong Master article. Triển khai 4-format menu + Voice Layer 5 rule + Format Director agent Sonnet (step 3.5) + 9 gates V5.0 + Step 1.5 Market Snapshot + version-gate migration.

**Architecture:** Format Registry yaml file là source of truth → Format Director subagent enriches Story Editor brief với `format_id` + `tone_bias` + `length_target` per option → Master sector applies per-format pattern + 9-gate check. Pipeline V4.0 (9 steps) → V5.0 (11 steps: + Step 1.5 Market Snapshot, + Step 3.5 Format Director). Migration via `pipeline_version` column (V5.0 rows enforce new schema, V3.6/V4.0 rows skip).

**Tech Stack:** Python 3.13 (uv-managed), SQLite (WAL mode), Claude subagents (Opus + Sonnet), React + TypeScript + Tailwind (Vite), pytest, PyYAML.

**Spec**: `docs/superpowers/specs/2026-05-11-master-article-format-diversity-design.md` V5.1.

---

## 🚨 V5.1.2 PATCH NOTICE (2026-05-12 PM) — apply EVERY task

**Spec reference**: `docs/superpowers/specs/2026-05-11-master-article-format-diversity-design.md` V5.1.2 PATCH at top.

After Spec B V1.2 patches, this plan adds Phase 6 (Tasks 23-30) and amends prior tasks:

### Amend Task 1 — `data/format_registry.yaml`
SKIP fields below from all 4 format definitions (already noted V5.1, repeat for clarity):
- `title_pattern`, `title_must_contain` / `title_must_contain_one_of`, `title_tension_words`, `title_must_match_regex`

### Amend Task 5 — `lib/gate_checker.py`
Function `check_no_hedging` REWRITE: KHÔNG dùng regex match từ ("có thể", "tùy thuộc",...). DÙNG LLM-as-judge với 2 test:
- Test 1 — Reverse-truth test: Đảo ngược sự thật, câu vẫn đúng? → fail.
- Test 2 — Direction check: Có cam kết direction không? → false = fail.
- Implementation: gate gọi Sonnet inline với prompt "Apply 2 tests to this sentence: <text>. Return {test_1: pass/fail, test_2: pass/fail, reason: str}". Tokens ~50 per call.

Function `check_em_dash_density` (NEW): count `—` (U+2014) trong body, fail nếu `count > word_count / 100`. Max 1 em dash / 100 từ.

### Amend Task 12-15 — Master sector prompts
**REMOVE** sections:
- "Title hook test 5s" guideline
- "tension word required (?, —, hy sinh, đánh đổi, nghịch lý,...)"
- "Title must start with..." patterns
- Any field instructing Master to generate title

**ADD** sections:
- "KHÔNG generate title. Trả về body + insight + data_trail. Field title sẽ do Headline agent generate sau."
- "Nhận stance_directive object từ brief. Body PHẢI viết theo `stance_directive.direction` + `stance_directive.key_evidence`. Được phép note caveat trong closing nếu data có nuance — caveat KHÔNG được làm bài 'ba phải' (fail Voice Rule 2)."

### Amend Task 4 — pipeline_db.py validate
`_STEP_4_REQUIRED_V5` REMOVE field `final_title`. Title sẽ vào `_STEP_4_5_REQUIRED` (Plan C).

`_STEP_3_REQUIRED_V5` ADD field `stance_directive: dict` — required với keys `{direction, confidence, reason, key_evidence}`.

Story Editor brief schema (`brief_json` JSON in DB) MUST contain `stance_directive` object — validation tại step_3 persist.

### Phase 6 (Tasks 23-30) — V5.1.2 SPLIT + new features

Inserted at end of plan. See Phase 6 section below.

---

## 🚨 V5.1 PATCH NOTICE (2026-05-12) — apply EVERY task

After Subsystem C (Headline Craft) brainstorm, **title craft moved out of plan B** to dedicated Headline agent. Executor MUST apply these edits to the original task content below:

### Task 1 — `data/format_registry.yaml`
SKIP fields below from all 4 format definitions:
- `title_pattern`
- `title_must_contain` / `title_must_contain_one_of`
- `title_tension_words`
- `title_must_match_regex`

Keep only: `length_range`, `length_target`, `structure`, `opening_min`, `opening_max`, `bullets_count`, `bullet_min_length`, `tags`, `trigger_categories`, `tie_break_signal`.

### Task 1 — `tests/test_format_registry.py`
SKIP assertions about title fields:
- `test_get_format_flash_qa_fields`: remove `assert fmt["title_pattern"] == "question"`
- `test_get_format_standard_qa_tension_words`: REMOVE entire test (tension words now in Headline agent's `lib/headline_scorer.py` not registry)

### Task 6 — Per-format gates
SKIP function `check_title_per_format` (Subsystem C `lib/headline_scorer.py` replaces it). SKIP all `test_per_format_title_*` tests:
- `test_per_format_title_flash_qa_needs_question_mark`
- `test_per_format_title_standard_listicle_numbered`
- `test_per_format_title_standard_narrative_em_dash`

`check_all_v5` signature: `check_all_v5(body, format_id, stance)` — drop `title` arg. Returns 8 gates (was 9): 6 universal + 2 per-format (`word_count`, `body_pattern`). Update `test_check_all_v5_dispatches_per_format` to match.

### Task 9 — Format Director agent prose
SKIP `title_pattern` from Format Director output schema. Format Director outputs only structural fields (length_range, bullets_count, structure). Title decided by Headline agent in Step 4.5.

5-step flow Step 4 in agent prose mentions "title hint" — REMOVE that mention. Format Director doesn't touch title.

### Task 13-15 — Master agents (Bank/CK/BĐS)
`check_all_v5` invocation drops `title` arg. Step 8 = 8 gates not 9. Master DOES still write a `draft_title` field — it gets replaced in Step 4.5 by Headline agent.

Add to Step 9 persist payload: `draft_title` field (Master's attempt — kept for observability + diff vs final). Final title comes from Step 4.5 Headline (separate persist via `db.update_generated_news`).

### Task 16 — Skeptic agent
10 angles total (was 9). Add `weak_title` (Layer 2 for Headline agent's hard criteria — flag clickbait risk + title-vs-body mismatch).

### Pipeline orchestrator (newsroom-pipeline.md)
INSERT Step 4.5 dispatch sau Step 4 — exact prose in Subsystem C spec §10. Use Task dispatch to `newsroom-headline-craft` agent. Subsystem C provides own plan covering this step.

### Subsystem C plan dependencies
The above patches assume Subsystem C plan (TBD — to be written) implements:
- `lib/headline_scorer.py` (8-point rubric)
- `.claude/agents/newsroom-headline-craft.md`
- `.claude/skills/finpath-newsroom-headline-craft/SKILL.md`
- Pipeline Step 4.5 dispatch

Executor should run plan B + plan C tasks in interleaved order (foundation in parallel, Master agent updates after both `lib/quality_gates.py` AND `lib/headline_scorer.py` ready).

---

## Critical context for executor

### Findings from codebase exploration (must read before Task 1)

1. **`lib/quality_gates.py` ALREADY EXISTS** (~280 LOC) with 5 V4.0 gates. Plan EXTENDS this file, does NOT create new `lib/gate_checker.py` as spec section 7 suggested.

2. **`pipeline_version` column ALREADY EXISTS** in both `crawl_log` + `generated_news` tables with DEFAULT 'V3.6' (per `data/pipeline.schema.sql`). Plan does NOT add column — instead bumps DEFAULT to 'V5.0' in code paths inserting new rows, and adds version-gate logic to `validate_pipeline_step`.

3. **`lib/finpath_api.py` does NOT have `get_quote()` method** — has BCTC + ratios + deposit/credit + bad debt + shareholders + events + news. Task 2 investigates available endpoints; if no real-time quote exists, Step 1.5 Market Snapshot returns `None` (V5 Contrarian degrades to prose-only — soft fetch by design).

4. **`web/src/types.ts` exists** (not `types/index.ts` as spec assumed). `ArticleMeta.pipeline_log` already optional with extensible `PipelineLog` interface.

5. **Story Editor brief schema** has `deep_question_options` array with `{question, category, pick_hint}` per option. V5.0 enriches with `stance + format_id + format_reason + tone_bias + length_target`.

### Models routing (per agent frontmatter)

| Agent | Model | Notes |
|---|---|---|
| `newsroom-pipeline` (orchestrator) | sonnet | Existing |
| `newsroom-editor` | sonnet | Existing |
| `newsroom-story-editor` | opus | Existing |
| `newsroom-format-director` (NEW) | sonnet | Per user decision in brainstorm |
| `newsroom-master-{bank,ck,bds}` | opus | Existing |
| `newsroom-skeptic` | opus | Existing |

### Run commands cheatsheet

```bash
# Python tests (use uv per project convention)
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/ -v

# Single test
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_quality_gates.py::test_check_no_hedging -v

# Frontend dev server (run in browser to verify visual)
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npm run dev
# → http://localhost:5176

# Type check frontend
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit

# Full pipeline run for ticker
/tin VCB
```

---

## Phase 1 — Foundation modules (Tasks 1-7)

### Task 1: Format Registry — yaml file + Python loader

**Files:**
- Create: `data/format_registry.yaml`
- Create: `lib/format_registry.py`
- Create: `tests/test_format_registry.py`

- [ ] **Step 1: Write the failing test**

`tests/test_format_registry.py`:

```python
"""Tests for lib/format_registry — load + lookup format definitions."""
from __future__ import annotations
import pytest
from lib.format_registry import (
    load_registry, get_format, get_candidates_for_category, FORMAT_IDS,
)


def test_load_registry_returns_4_formats():
    reg = load_registry()
    assert set(reg.keys()) == {"flash_qa", "standard_qa", "standard_listicle", "standard_narrative"}


def test_format_ids_constant_matches_registry():
    reg = load_registry()
    assert set(FORMAT_IDS) == set(reg.keys())


def test_get_format_flash_qa_fields():
    fmt = get_format("flash_qa")
    assert fmt["length_range"] == [100, 150]
    assert fmt["length_target"] == 130
    assert fmt["structure"] == "paragraph_only"
    assert fmt["bullets_count"] == [0, 0]
    assert fmt["title_pattern"] == "question"


def test_get_format_standard_qa_tension_words():
    fmt = get_format("standard_qa")
    assert "hy sinh" in fmt["title_tension_words"]
    assert "đánh đổi" in fmt["title_tension_words"]
    assert fmt["bullets_count"] == [3, 6]
    assert fmt["bullet_min_length"] == 20


def test_get_candidates_paradox():
    candidates = get_candidates_for_category("paradox")
    assert candidates == ["standard_qa"]


def test_get_candidates_hidden_mechanism_returns_2():
    candidates = set(get_candidates_for_category("hidden_mechanism"))
    assert candidates == {"standard_qa", "standard_narrative"}


def test_get_candidates_comparison_deep():
    assert get_candidates_for_category("comparison_deep") == ["standard_listicle"]


def test_get_candidates_unknown_returns_empty():
    assert get_candidates_for_category("nonexistent_category") == []


def test_get_format_invalid_raises():
    with pytest.raises(KeyError):
        get_format("nonexistent_format")
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_format_registry.py -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'lib.format_registry'`.

- [ ] **Step 3: Create `data/format_registry.yaml`**

```yaml
# Format Registry V5.0 — source of truth for Master article formats.
# Story Editor + Format Director read this; Master applies per-format pattern.
# Add new formats here without touching agent prose (registry abstraction).
formats:
  flash_qa:
    length_range: [100, 150]
    length_target: 130
    structure: paragraph_only
    bullets_count: [0, 0]
    bullet_min_length: 0
    title_pattern: question
    title_must_contain: ["?"]
    title_tension_words: []
    tags: [factual, short]
    trigger_categories: []  # fallback for factual single Q, not in 5 deep_question category

  standard_qa:
    length_range: [200, 300]
    length_target: 250
    structure: opening_bullets_closing
    opening_min: 30
    opening_max: 80
    bullets_count: [3, 6]
    bullet_min_length: 20
    title_pattern: question_or_paradox
    title_must_contain_one_of: ["?", "—"]
    title_tension_words:
      - "hy sinh"
      - "đánh đổi"
      - "nghịch lý"
      - "vì sao"
      - "đổi lấy"
      - "không phải"
      - "bù lại"
      - "thay vì"
      - "chấp nhận"
    tags: [insight, paradox]
    trigger_categories: [paradox, why_now, hidden_mechanism]

  standard_listicle:
    length_range: [250, 350]
    length_target: 300
    structure: short_opening_dense_bullets
    opening_min: 0
    opening_max: 30
    bullets_count: [4, 7]
    bullet_min_length: 25
    title_pattern: numbered_declarative
    title_must_match_regex: '^(\d+|[Mm]ột|[Hh]ai|[Bb]a|[Bb][ốố]n|[Nn][ăă]m)\s+'
    title_tension_words: []
    tags: [comparison, signals]
    trigger_categories: [comparison_deep, early_signal]

  standard_narrative:
    length_range: [250, 350]
    length_target: 300
    structure: flow_paragraphs
    opening_min: 40
    bullets_count: [0, 2]
    bullet_min_length: 20  # if bullet present
    title_pattern: declarative_story
    title_must_contain: ["—"]  # em dash chia 2 vế
    title_tension_words: []
    tags: [mechanism, time_flow]
    trigger_categories: [hidden_mechanism]
    tie_break_signal: narrative_timeline_markers  # ≥3 → pick narrative over qa
```

- [ ] **Step 4: Create `lib/format_registry.py`**

```python
"""Format Registry V5.0 — loader for data/format_registry.yaml.

Source of truth for 4 Master article formats. Story Editor + Format Director
read this; Master applies per-format pattern + per-format gate check.
"""
from __future__ import annotations
import yaml
from functools import lru_cache
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "data" / "format_registry.yaml"

FORMAT_IDS = ["flash_qa", "standard_qa", "standard_listicle", "standard_narrative"]


@lru_cache(maxsize=1)
def load_registry() -> dict[str, dict[str, Any]]:
    """Load format_registry.yaml. Cached after first call (file is static)."""
    raw = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    return raw["formats"]


def get_format(format_id: str) -> dict[str, Any]:
    """Return single format spec by ID. Raises KeyError if unknown."""
    reg = load_registry()
    if format_id not in reg:
        raise KeyError(f"Unknown format_id: {format_id!r} (valid: {list(reg.keys())})")
    return reg[format_id]


def get_candidates_for_category(category: str) -> list[str]:
    """Filter formats whose `trigger_categories` contains the given category.

    Returns format_ids in catalog order. Empty list if no matches.
    """
    reg = load_registry()
    return [fid for fid, spec in reg.items() if category in spec.get("trigger_categories", [])]
```

- [ ] **Step 5: Run tests — verify pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_format_registry.py -v
```
Expected: 8 passed.

- [ ] **Step 6: Commit**

```bash
git add data/format_registry.yaml lib/format_registry.py tests/test_format_registry.py
git commit -m "feat(format-registry): add 4-format catalog yaml + Python loader (Phase 1.1)

V5.0 foundation. Source of truth for Master article formats.
Story Editor + Format Director read this; Master applies per-format pattern.
"
```

---

### Task 2: Market Snapshot — investigate Finpath API + implement Step 1.5

**Files:**
- Create: `lib/stages/run_market_snapshot.py`
- Create: `tests/test_run_market_snapshot.py`
- Modify (maybe): `lib/finpath_api.py` — add `get_quote(ticker)` if endpoint exists

- [ ] **Step 1: Investigate available quote endpoint**

Run probe to discover real-time price endpoints:

```bash
curl -sS "https://api.finpath.vn/api/stocks/companyprofile/VCB" | python -m json.tool | head -40
curl -sS "https://api.finpath.vn/api/stocks/incomes/VCB" | python -m json.tool | head -20
# Try common patterns
curl -sS "https://api.finpath.vn/api/stocks/quote/VCB" 2>&1 | head -5
curl -sS "https://api.finpath.vn/api/stocks/prices/VCB" 2>&1 | head -5
curl -sS "https://api.finpath.vn/api/stocks/price-history/VCB" 2>&1 | head -5
```

Document finding in commit message. If no quote endpoint exists, Step 1.5 returns `None` (defensive — V5 Contrarian degrades to prose-only).

- [ ] **Step 2: Write failing test (works for both endpoint-exists and degraded modes)**

`tests/test_run_market_snapshot.py`:

```python
"""Tests for lib/stages/run_market_snapshot — Step 1.5 fetch ticker quote.

Soft-fetch by design: failure returns None, never raises.
"""
from __future__ import annotations
import json
from unittest.mock import MagicMock, patch
import pytest
from lib.stages.run_market_snapshot import fetch_market_snapshot, MarketSnapshot


def test_fetch_returns_none_when_api_unavailable():
    """Network error → return None, do not raise."""
    with patch("lib.stages.run_market_snapshot.FinpathAPI") as mock_api:
        mock_api.return_value.get_quote.side_effect = ConnectionError("network down")
        result = fetch_market_snapshot("VCB")
        assert result is None


def test_fetch_returns_none_when_no_get_quote_method():
    """If FinpathAPI doesn't expose get_quote, soft-fail returns None."""
    with patch("lib.stages.run_market_snapshot.FinpathAPI") as mock_api:
        # Simulate missing method (current API state)
        del mock_api.return_value.get_quote
        result = fetch_market_snapshot("VCB")
        assert result is None


def test_fetch_returns_snapshot_on_success():
    """Happy path: API returns dict with price + pct_change."""
    fake_quote = {"price": 92500, "pct_change": -3.2, "volume_ratio_3d": 1.4}
    with patch("lib.stages.run_market_snapshot.FinpathAPI") as mock_api:
        mock_api.return_value.get_quote.return_value = fake_quote
        result = fetch_market_snapshot("VCB")
        assert result is not None
        assert result.price_today == 92500
        assert result.pct_change_today == -3.2
        assert result.volume_ratio_3d == 1.4
        assert result.fetched_at  # ISO 8601 timestamp set


def test_fetch_returns_none_when_response_missing_price():
    """Malformed response without 'price' key → None (defensive)."""
    with patch("lib.stages.run_market_snapshot.FinpathAPI") as mock_api:
        mock_api.return_value.get_quote.return_value = {"junk": "data"}
        result = fetch_market_snapshot("VCB")
        assert result is None


def test_snapshot_to_dict():
    """MarketSnapshot serializable to brief.ticker_market_data shape."""
    snap = MarketSnapshot(price_today=100, pct_change_today=2.5, volume_ratio_3d=1.1, fetched_at="2026-05-11T14:00:00+00:00")
    d = snap.to_dict()
    assert d == {
        "price_today": 100,
        "pct_change_today": 2.5,
        "volume_ratio_3d": 1.1,
        "fetched_at": "2026-05-11T14:00:00+00:00",
    }
```

- [ ] **Step 3: Run test — fail**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_run_market_snapshot.py -v
```
Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 4: Implement `lib/stages/run_market_snapshot.py`**

```python
"""Market Snapshot — Step 1.5 of V5.0 pipeline.

Soft fetch: failure → None, never raises. Brief proceeds without
ticker_market_data when this returns None. V5 Contrarian degrades to
prose-only guidance in that case.

Investigated 2026-05-11: Finpath API quote endpoint availability TBD
(see Task 2 Step 1 commit). If get_quote not available, this module
always returns None — soft degrade by design.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any

from lib.finpath_api import FinpathAPI


@dataclass
class MarketSnapshot:
    price_today: float
    pct_change_today: float
    volume_ratio_3d: float
    fetched_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def fetch_market_snapshot(ticker: str) -> MarketSnapshot | None:
    """Fetch real-time quote via Finpath API. Returns None on any failure.

    Used in pipeline Step 1.5 to populate `brief.ticker_market_data` so Master
    can do mood-aware opening (acknowledge market red/green day in tone)
    without forcing stance follow.
    """
    try:
        api = FinpathAPI()
        # get_quote MAY not be implemented yet — defensive try
        if not hasattr(api, "get_quote"):
            return None
        raw = api.get_quote(ticker)
        if not isinstance(raw, dict) or "price" not in raw:
            return None
        return MarketSnapshot(
            price_today=float(raw["price"]),
            pct_change_today=float(raw.get("pct_change", 0.0)),
            volume_ratio_3d=float(raw.get("volume_ratio_3d", 1.0)),
            fetched_at=datetime.now(timezone.utc).isoformat(),
        )
    except (ConnectionError, KeyError, ValueError, TypeError):
        return None
    except Exception:
        # Catch-all defensive — Step 1.5 NEVER blocks pipeline
        return None
```

- [ ] **Step 5: Run tests — verify pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_run_market_snapshot.py -v
```
Expected: 5 passed.

- [ ] **Step 6: Commit**

```bash
git add lib/stages/run_market_snapshot.py tests/test_run_market_snapshot.py
git commit -m "feat(pipeline): Step 1.5 Market Snapshot soft-fetch (Phase 1.2)

V5.0 mood-sync data source. Calls FinpathAPI.get_quote if available,
returns None on any failure. Brief proceeds without ticker_market_data
when None — V5 Contrarian degrades to prose-only guidance.

Finpath API quote endpoint TBD: implementation defensive against missing method.
"
```

---

### Task 3: Bump `pipeline_version` default to V5.0 in code paths

**Files:**
- Modify: `lib/pipeline_db.py:188-209` (`insert_generated_news`)
- Modify: `lib/render_compare_feed.py` — default pipeline_version frontmatter
- Test: `tests/test_pipeline_db.py` (extend)

Schema file (`data/pipeline.schema.sql`) keeps DEFAULT 'V3.6' for back-compat with existing rows. Only NEW rows get V5.0.

- [ ] **Step 1: Write failing test**

Append to `tests/test_pipeline_db.py`:

```python
def test_insert_generated_news_defaults_pipeline_version_v5(tmp_path):
    """V5.0: new rows get pipeline_version=V5.0 unless caller specifies."""
    from lib.pipeline_db import PipelineDB
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    db.init_schema("data/pipeline.schema.sql")
    # Seed a crawl_log row first (FK)
    db.insert_crawl_row({
        "row_id": "r1", "funnel_batch_id": "b1", "ticker": "VCB",
        "source_name": "CafeF", "source_url": "http://example.com/1",
        "title": "T", "crawled_at": "2026-05-11T00:00:00Z",
    })
    # Insert WITHOUT pipeline_version → should default to V5.0 (not V3.6)
    article_data = {
        "article_id": "a1", "row_id": "r1", "ticker": "VCB", "sector": "Bank",
        "title": "Test", "body": "...", "accepted_hypothesis": 1, "status": "draft",
    }
    db.insert_generated_news(article_data)
    row = db.conn.execute("SELECT pipeline_version FROM generated_news WHERE article_id='a1'").fetchone()
    assert row["pipeline_version"] == "V5.0"
    db.close()


def test_insert_generated_news_explicit_version_preserved(tmp_path):
    """Caller can override default (e.g. test fixtures simulating legacy V4.0)."""
    from lib.pipeline_db import PipelineDB
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    db.init_schema("data/pipeline.schema.sql")
    db.insert_crawl_row({
        "row_id": "r2", "funnel_batch_id": "b2", "ticker": "VCB",
        "source_name": "CafeF", "source_url": "http://example.com/2",
        "title": "T", "crawled_at": "2026-05-11T00:00:00Z",
    })
    db.insert_generated_news({
        "article_id": "a2", "row_id": "r2", "ticker": "VCB", "sector": "Bank",
        "title": "Test", "body": "...", "accepted_hypothesis": 1, "status": "draft",
        "pipeline_version": "V4.0",  # explicit override
    })
    row = db.conn.execute("SELECT pipeline_version FROM generated_news WHERE article_id='a2'").fetchone()
    assert row["pipeline_version"] == "V4.0"
    db.close()
```

- [ ] **Step 2: Run test — fail**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_pipeline_db.py::test_insert_generated_news_defaults_pipeline_version_v5 -v
```
Expected: FAIL — value is "V3.6" (current schema default).

- [ ] **Step 3: Modify `lib/pipeline_db.py:insert_generated_news`**

Replace function body to default pipeline_version to V5.0:

```python
def insert_generated_news(self, data: dict[str, Any]) -> str:
    # V5.0 Phase 1.3 — default pipeline_version to V5.0 unless caller specifies.
    # Existing rows (V3.6/V4.0) preserved via schema DEFAULT; only NEW inserts
    # via this method get V5.0 → enables version-gate validation downstream.
    data = {**data}  # don't mutate caller's dict
    if "pipeline_version" not in data:
        data["pipeline_version"] = "V5.0"

    # V4.0 Phase H2 — validate pipeline_log schema BEFORE insert.
    raw_log = data.get("pipeline_log")
    if raw_log:
        try:
            log = json.loads(raw_log) if isinstance(raw_log, str) else raw_log
        except (json.JSONDecodeError, TypeError):
            log = {}
        pipeline_version = data["pipeline_version"]
        for step_key in ("step_3_5_format_director", "step_4_master", "step_5_skeptic"):
            if step_key in log:
                validate_pipeline_step(step_key, log[step_key], pipeline_version=pipeline_version)

    cols = ", ".join(data.keys())
    placeholders = ", ".join("?" for _ in data)
    sql = f"INSERT INTO generated_news ({cols}) VALUES ({placeholders})"
    self.conn.execute(sql, list(data.values()))
    self.conn.commit()
    return data["article_id"]
```

- [ ] **Step 4: Run tests — verify pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_pipeline_db.py -v
```
Expected: All pass (existing + 2 new tests). Note: `validate_pipeline_step` becomes version-aware in Task 4 — until then, signature update would break existing tests. Resolve by: in Step 3 above, only pass `pipeline_version=` kwarg if function signature accepts it. Defer kwarg passing to Task 4 — write Step 3 above as-is BUT after Task 4 modifies validate_pipeline_step signature, this works correctly. If Task 4 not yet done, existing call sites would TypeError. **Sequencing: do Task 4 immediately after Task 3 Step 3 (single commit if needed).**

- [ ] **Step 5: Commit**

```bash
git add lib/pipeline_db.py tests/test_pipeline_db.py
git commit -m "feat(pipeline_db): default pipeline_version=V5.0 for new rows (Phase 1.3)

V5.0 migration foundation. Schema DEFAULT 'V3.6' preserved for legacy rows;
new inserts via insert_generated_news get V5.0 → enables version-gate
validation in validate_pipeline_step (Task 4).
"
```

---

### Task 4: Version-gate validation in `validate_pipeline_step`

**Files:**
- Modify: `lib/pipeline_db.py:41-107` (`validate_pipeline_step` + schemas)
- Test: `tests/test_pipeline_db.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_pipeline_db.py`:

```python
def test_validate_v5_step_4_requires_observability():
    """V5.1: step_4_master MUST emit model + duration_ms (observability)."""
    from lib.pipeline_db import validate_pipeline_step
    import pytest
    # Content fields complete, but observability missing
    payload = {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "ok",
        "skip_reasons": {},
        "data_trail": [{"source": "x", "fetched": "y"}],
        "format_id_used": "standard_qa",
        # ❌ Missing: model, duration_ms
    }
    with pytest.raises(ValueError, match="model|duration_ms"):
        validate_pipeline_step("step_4_master", payload, pipeline_version="V5.0")


def test_validate_v5_step_4_observability_complete_passes():
    from lib.pipeline_db import validate_pipeline_step
    payload = {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "ok",
        "skip_reasons": {},
        "data_trail": [{"source": "x", "fetched": "y"}],
        "format_id_used": "standard_qa",
        "model": "claude-opus-4-7",
        "duration_ms": 12500,
        # tokens optional
    }
    validate_pipeline_step("step_4_master", payload, pipeline_version="V5.0")


def test_validate_v5_step_4_empty_model_rejects():
    """model must be non-empty string."""
    from lib.pipeline_db import validate_pipeline_step
    import pytest
    payload = {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "ok",
        "skip_reasons": {},
        "data_trail": [{"source": "x"}],
        "format_id_used": "standard_qa",
        "model": "",  # ❌ empty
        "duration_ms": 12500,
    }
    with pytest.raises(ValueError, match="empty"):
        validate_pipeline_step("step_4_master", payload, pipeline_version="V5.0")


def test_validate_v4_step_4_no_observability_required():
    """V4.0 back-compat: observability NOT required (was prose-only)."""
    from lib.pipeline_db import validate_pipeline_step
    payload = {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "ok",
        "skip_reasons": {},
        "data_trail": [{"source": "x", "fetched": "y"}],
        # No model, no duration_ms → V4.0 should accept
    }
    validate_pipeline_step("step_4_master", payload, pipeline_version="V4.0")


def test_validate_v3_skips_step_3_5_check():
    """V3.6 rows: no step_3_5_format_director schema enforcement."""
    from lib.pipeline_db import validate_pipeline_step
    # Empty payload would fail V5.0 schema, but V3.6 has no such schema
    validate_pipeline_step("step_3_5_format_director", {}, pipeline_version="V3.6")
    # No exception raised


def test_validate_v4_skips_step_3_5_check():
    """V4.0 rows: also skip step_3_5 (was not in V4.0)."""
    from lib.pipeline_db import validate_pipeline_step
    validate_pipeline_step("step_3_5_format_director", {}, pipeline_version="V4.0")


def test_validate_v5_enforces_step_3_5():
    """V5.0 rows: step_3_5_format_director MUST have format_picks."""
    from lib.pipeline_db import validate_pipeline_step
    import pytest
    with pytest.raises(ValueError, match="step_3_5_format_director"):
        validate_pipeline_step("step_3_5_format_director", {}, pipeline_version="V5.0")


def test_validate_v5_step_4_requires_format_id_used():
    """V5.0 step_4_master gets format_id_used required field added."""
    from lib.pipeline_db import validate_pipeline_step
    import pytest
    payload = {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "Test reason",
        "skip_reasons": {},
        "data_trail": [{"source": "Finpath_API/test", "fetched": "data"}],
        # MISSING: format_id_used (required only in V5.0)
    }
    with pytest.raises(ValueError, match="format_id_used"):
        validate_pipeline_step("step_4_master", payload, pipeline_version="V5.0")


def test_validate_v4_step_4_no_format_id_used_required():
    """V4.0 step_4_master: format_id_used NOT required (back-compat)."""
    from lib.pipeline_db import validate_pipeline_step
    payload = {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "Test reason",
        "skip_reasons": {},
        "data_trail": [{"source": "Finpath_API/test", "fetched": "data"}],
    }
    # No format_id_used — V4.0 should accept this
    validate_pipeline_step("step_4_master", payload, pipeline_version="V4.0")


def test_validate_v5_step_4_valid_passes():
    """V5.0 step_4_master with format_id_used present passes."""
    from lib.pipeline_db import validate_pipeline_step
    payload = {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "Test reason",
        "skip_reasons": {},
        "data_trail": [{"source": "Finpath_API/test", "fetched": "data"}],
        "format_id_used": "standard_qa",
    }
    validate_pipeline_step("step_4_master", payload, pipeline_version="V5.0")
```

- [ ] **Step 2: Run test — fail**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_pipeline_db.py::test_validate_v5_step_4_requires_format_id_used -v
```
Expected: FAIL — function signature does not accept `pipeline_version` kwarg.

- [ ] **Step 3: Modify `lib/pipeline_db.py`**

Replace lines 17-107 (schema constants + `validate_pipeline_step`):

```python
# V5.1 — Observability fields required across ALL agent-emitted steps for V5.0+.
# Fixes "trước có rồi mà chả thấy hoạt động": observability was prose-rule
# only, orchestrator could skip merge → blank in viewer. Now fail-loud for V5.0+.
# V4.0/V3.6 rows skip (back-compat — those were prose-rule era).
_OBSERVABILITY_REQUIRED: dict[str, type | tuple] = {
    "model": str,
    "duration_ms": int,
    # tokens OPTIONAL — Claude Code không guarantee <usage> trong Task return.
    # parse_task_usage() returns None gracefully khi missing.
}

# step_4_master V4.0 baseline (NO observability — back-compat).
_STEP_4_REQUIRED_V4: dict[str, type | tuple] = {
    "chosen_question_idx": int,
    "chosen_pick_reason": str,
    "skip_reasons": dict,
    "data_trail": list,
}

# step_4_master V5.0 extension: adds format_id_used + observability.
_STEP_4_REQUIRED_V5: dict[str, type | tuple] = {
    **_STEP_4_REQUIRED_V4,
    **_OBSERVABILITY_REQUIRED,
    "format_id_used": str,
}

# step_5_skeptic V4.0 baseline (NO observability — back-compat).
_STEP_5_REQUIRED_V4: dict[str, type | tuple] = {
    "angle": str,
    "verdict": str,
    "skeptic_data_trail": list,
}

# step_5_skeptic V5.0 (adds observability).
_STEP_5_REQUIRED_V5: dict[str, type | tuple] = {
    **_STEP_5_REQUIRED_V4,
    **_OBSERVABILITY_REQUIRED,
}

# step_3_5_format_director — NEW in V5.0 (always with observability).
_STEP_3_5_REQUIRED: dict[str, type | tuple] = {
    **_OBSERVABILITY_REQUIRED,
    "format_picks": list,
}

# Non-empty constraint per step. model MUST not be empty string when present.
_NON_EMPTY_FIELDS: dict[str, set[str]] = {
    "step_4_master": {"chosen_pick_reason", "data_trail"},
    "step_5_skeptic": {"angle", "verdict", "skeptic_data_trail"},
    "step_3_5_format_director": {"format_picks"},
}
# Observability non-empty applies only for V5.0+ — added dynamically in validate_pipeline_step.


def _version_ge(a: str, b: str) -> bool:
    """Compare pipeline_version strings like 'V5.0' >= 'V4.0'.

    Strips 'V' prefix, splits on '.', compares as tuples of ints.
    Defensive: malformed versions → False (skip new schema).
    """
    def _parse(v: str) -> tuple[int, ...]:
        try:
            return tuple(int(p) for p in v.lstrip("Vv").split("."))
        except (ValueError, AttributeError):
            return (0,)
    return _parse(a) >= _parse(b)


def validate_pipeline_step(step_key: str, payload: dict, pipeline_version: str = "V4.0") -> None:
    """Raise ValueError if `payload` missing required fields for `step_key`.

    Version-aware (V5.0 Phase 1.4 + V5.1 observability):
    - V4.0 and earlier: enforce step_4_master + step_5_skeptic baselines
      (NO observability — was prose-rule era). step_3_5 skipped.
    - V5.0+: + step_3_5_format_director, step_4_master.format_id_used required,
      AND observability fields (model + duration_ms) required across step_3_5/4/5.

    Default pipeline_version='V4.0' preserves baseline for callers not yet updated.
    """
    is_v5_plus = _version_ge(pipeline_version, "V5.0")

    required_map: dict[str, dict[str, type | tuple]] = {
        "step_4_master": _STEP_4_REQUIRED_V5 if is_v5_plus else _STEP_4_REQUIRED_V4,
        "step_5_skeptic": _STEP_5_REQUIRED_V5 if is_v5_plus else _STEP_5_REQUIRED_V4,
    }
    if is_v5_plus:
        required_map["step_3_5_format_director"] = _STEP_3_5_REQUIRED

    # V5.1 — observability non-empty (model) applies only for V5.0+ rows.
    non_empty_fields = dict(_NON_EMPTY_FIELDS)
    if is_v5_plus:
        for step in ("step_4_master", "step_5_skeptic", "step_3_5_format_director"):
            non_empty_fields[step] = non_empty_fields.get(step, set()) | {"model"}

    required = required_map.get(step_key)
    if not required:
        return  # observability-only step or version doesn't enforce this step

    missing = []
    wrong_type = []
    empty = []
    for field, expected_type in required.items():
        if field not in payload:
            missing.append(field)
            continue
        value = payload[field]
        if not isinstance(value, expected_type):
            wrong_type.append(f"{field} (got {type(value).__name__}, expected {expected_type.__name__})")
            continue
        # V5.1: use locally-computed non_empty_fields (observability added dynamically)
        if field in non_empty_fields.get(step_key, set()) and not value:
            empty.append(field)

    # Entry-level checks for data_trail arrays (V4.0 Phase H2).
    bad_entries: list[str] = []
    entry_field_map = {
        "step_4_master": "data_trail",
        "step_5_skeptic": "skeptic_data_trail",
    }
    entry_field = entry_field_map.get(step_key)
    if entry_field and entry_field in payload and isinstance(payload[entry_field], list):
        for idx, entry in enumerate(payload[entry_field]):
            if not isinstance(entry, dict):
                bad_entries.append(f"{entry_field}[{idx}] is {type(entry).__name__} (must be dict)")
            elif "source" not in entry or not entry.get("source"):
                bad_entries.append(f"{entry_field}[{idx}] missing/empty 'source' key")

    if missing or wrong_type or empty or bad_entries:
        errors = []
        if missing:
            errors.append(f"missing keys: {missing}")
        if wrong_type:
            errors.append(f"wrong type: {wrong_type}")
        if empty:
            errors.append(f"empty (must be non-empty): {empty}")
        if bad_entries:
            errors.append(f"bad entries: {bad_entries}")
        raise ValueError(
            f"pipeline_log[{step_key!r}] schema violation (version={pipeline_version}) — "
            f"{'; '.join(errors)}. This usually means the {step_key} subagent was bypassed "
            f"(orchestrator self-executed inline) or emitted legacy schema. MUST dispatch via Task tool."
        )
```

- [ ] **Step 4: Update `log_pipeline_step` to read `pipeline_version` from row**

In `lib/pipeline_db.py` around line 219, modify `log_pipeline_step`:

```python
def log_pipeline_step(self, article_id: str, step_key: str, payload: dict) -> None:
    """Shallow-MERGE payload into pipeline_log[step_key].

    V5.0 Phase 1.4 — reads row's pipeline_version to apply version-aware
    schema validation (V3.6/V4.0 skip V5.0-only checks).
    """
    cur = self.conn.execute(
        "SELECT pipeline_log, pipeline_version FROM generated_news WHERE article_id = ?",
        (article_id,),
    )
    row = cur.fetchone()
    if not row:
        return
    pipeline_version = row["pipeline_version"] if "pipeline_version" in row.keys() else "V4.0"
    log = json.loads(row["pipeline_log"]) if row["pipeline_log"] else {}
    log[step_key] = {**log.get(step_key, {}), **payload}
    validate_pipeline_step(step_key, log[step_key], pipeline_version=pipeline_version)
    self.conn.execute(
        "UPDATE generated_news SET pipeline_log = ? WHERE article_id = ?",
        (json.dumps(log, ensure_ascii=False), article_id),
    )
    self.conn.commit()
```

- [ ] **Step 5: Run all tests — verify no regression + new tests pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_pipeline_db.py -v
```
Expected: all green (new V5 tests + existing V4 tests via default `pipeline_version='V4.0'`).

- [ ] **Step 6: Commit**

```bash
git add lib/pipeline_db.py tests/test_pipeline_db.py
git commit -m "feat(pipeline_db): version-gate validation V3.6/V4.0/V5.0/V5.1 (Phase 1.4)

V5.0 migration:
- Splits _STEP_4_REQUIRED into _V4 (baseline) + _V5 (+ format_id_used)
- Splits _STEP_5_REQUIRED into _V4 (baseline) + _V5 (+ observability)
- Adds _STEP_3_5_REQUIRED for new Format Director step
- validate_pipeline_step takes pipeline_version kwarg
- log_pipeline_step reads row.pipeline_version automatically
- V3.6/V4.0 rows skip V5.0 schema checks (back-compat)

V5.1 observability enforcement (fixes 'chả thấy hoạt động'):
- _OBSERVABILITY_REQUIRED constant (model: str, duration_ms: int)
- Merged into V5 step_3_5 / step_4 / step_5 schemas
- Non-empty check for model dynamically added for V5.0+ rows
- V4.0 rows back-compat (no observability enforcement)
- tokens stays optional (Claude Code <usage> not guaranteed)
"
```

- [ ] **Step 7: Update agent prompt prose — observability emission required**

After implementing schema enforcement, the orchestrator agent prompt `.claude/agents/newsroom-pipeline.md` MUST emit observability fields in every `db.log_pipeline_step` call. The existing "Observability" section (V4.0 Phase F C2) already documents the pattern but was prose-rule only. V5.1 makes it enforced.

Find existing observability block in newsroom-pipeline.md and add WARNING note:

```markdown
### Observability — REQUIRED V5.1+ (enforced by schema validation)

⚠️ HARD RULE: Every `db.log_pipeline_step` call cho V5.0+ row MUST include:
- `model`: agent model string (e.g. "claude-opus-4-7", "claude-sonnet-4-6")
- `duration_ms`: int — elapsed wall-clock milliseconds since Task dispatch
- `tokens`: optional — parse_task_usage(task_return), None acceptable

Schema validation fails-loud nếu thiếu model + duration_ms. Pipeline halt. Bug surfaces immediately instead of silent blank in viewer.
```

Update orchestrator agent prompt accordingly in **separate Task** (Task 11 Pipeline orchestrator update — extend HARD RULE section there).

This Task 4 step focuses on schema enforcement only.

---

### Task 5: Extend `lib/quality_gates.py` with 4 new universal gates

**Files:**
- Modify: `lib/quality_gates.py` (extend, do NOT create gate_checker.py per spec)
- Test: `tests/test_quality_gates.py`

New gates: `check_no_hedging`, `check_verdict_line`, `check_stance_consistency`, `check_sentence_density`.

- [ ] **Step 1: Write failing tests for `check_no_hedging`**

Append to `tests/test_quality_gates.py`:

```python
# === V5.0 Phase 1.5 — no_hedging gate ===

def test_no_hedging_pass():
    from lib.quality_gates import check_no_hedging
    body = "VCB sẽ tăng trưởng. NĐT nên giữ. Q1 đang mạnh."
    assert check_no_hedging(body)["pass"] is True


def test_no_hedging_rejects_co_the():
    from lib.quality_gates import check_no_hedging
    body = "VCB có thể tăng trưởng. NĐT nên giữ."
    result = check_no_hedging(body)
    assert result["pass"] is False
    assert "có thể" in result["reason"]


def test_no_hedging_rejects_tuy_thuoc():
    from lib.quality_gates import check_no_hedging
    body = "Tăng trưởng tùy thuộc thị trường."
    assert check_no_hedging(body)["pass"] is False


def test_no_hedging_rejects_dang_theo_doi():
    from lib.quality_gates import check_no_hedging
    body = "Đây là sự kiện đáng theo dõi trong tương lai."
    assert check_no_hedging(body)["pass"] is False


def test_no_hedging_rejects_kha_nang_cao():
    from lib.quality_gates import check_no_hedging
    body = "Khả năng cao sẽ tăng. Nhưng chưa rõ."
    result = check_no_hedging(body)
    assert result["pass"] is False
```

- [ ] **Step 2: Write failing tests for `check_verdict_line`**

```python
# === V5.0 Phase 1.5 — verdict_line gate ===

VERDICT_OK = """
Tích cực dài hạn cho VCB. NĐT đang cầm nên giữ 12 tháng — chiến lược phòng thủ Q1 sẽ thành lợi thế.
"""

VERDICT_MISSING_DIRECTION = """
NĐT đang cầm nên giữ 12 tháng — chiến lược phòng thủ Q1 sẽ thành lợi thế.
"""

VERDICT_MISSING_TIMEFRAME = """
Tích cực cho VCB. NĐT đang cầm nên giữ — chiến lược phòng thủ Q1 sẽ thành lợi thế.
"""

VERDICT_MISSING_HOLDER_ACTION = """
Tích cực dài hạn cho VCB trong 12 tháng tới.
"""


def test_verdict_line_pass():
    from lib.quality_gates import check_verdict_line
    body = "Opening paragraph here.\n\n- bullet\n\n" + VERDICT_OK
    assert check_verdict_line(body)["pass"] is True


def test_verdict_line_rejects_missing_direction():
    from lib.quality_gates import check_verdict_line
    body = "Opening here.\n\n- bullet\n\n" + VERDICT_MISSING_DIRECTION
    result = check_verdict_line(body)
    assert result["pass"] is False
    assert "direction" in result["reason"]


def test_verdict_line_rejects_missing_timeframe():
    from lib.quality_gates import check_verdict_line
    body = "Opening here.\n\n- bullet\n\n" + VERDICT_MISSING_TIMEFRAME
    result = check_verdict_line(body)
    assert result["pass"] is False
    assert "timeframe" in result["reason"]


def test_verdict_line_rejects_missing_holder_action():
    from lib.quality_gates import check_verdict_line
    body = "Opening here.\n\n- bullet\n\n" + VERDICT_MISSING_HOLDER_ACTION
    result = check_verdict_line(body)
    assert result["pass"] is False
    assert "action_for_holder" in result["reason"]
```

- [ ] **Step 3: Write failing tests for `check_stance_consistency`**

```python
# === V5.0 Phase 1.5 — stance_consistency gate ===

BULLISH_BODY = "VCB tăng trưởng tích cực, đáng giữ. Cơ hội mạnh, ổn định lợi thế."
BEARISH_BODY = "VCB có rủi ro yếu. Cảnh báo căng thẳng. Đỉnh ngắn hạn đáng lo."
MIXED_BODY = "VCB tăng trưởng tích cực nhưng rủi ro cũng cao. Cảnh báo cần lưu ý."


def test_stance_bullish_matches():
    from lib.quality_gates import check_stance_consistency
    assert check_stance_consistency(BULLISH_BODY, "bullish")["pass"] is True


def test_stance_bearish_matches():
    from lib.quality_gates import check_stance_consistency
    assert check_stance_consistency(BEARISH_BODY, "bearish")["pass"] is True


def test_stance_bullish_brief_bearish_body_rejects():
    from lib.quality_gates import check_stance_consistency
    result = check_stance_consistency(BEARISH_BODY, "bullish")
    assert result["pass"] is False
    assert "tone bearish" in result["reason"]


def test_stance_bearish_brief_bullish_body_rejects():
    from lib.quality_gates import check_stance_consistency
    result = check_stance_consistency(BULLISH_BODY, "bearish")
    assert result["pass"] is False


def test_stance_divergent_balanced_passes():
    from lib.quality_gates import check_stance_consistency
    assert check_stance_consistency(MIXED_BODY, "divergent")["pass"] is True


def test_stance_no_keywords_rejects():
    from lib.quality_gates import check_stance_consistency
    body = "VCB là ngân hàng. Q1 ra báo cáo."  # No stance words
    result = check_stance_consistency(body, "bullish")
    assert result["pass"] is False
    assert "lifeless" in result["reason"].lower()
```

- [ ] **Step 4: Write failing tests for `check_sentence_density`**

```python
# === V5.0 Phase 1.5 — sentence_density gate ===

DENSE_BODY = (
    "VCB Q1/2026 LNTT đạt 11.218 tỷ — chỉ tăng 1,3% so cùng kỳ. "
    "Chi phí dự phòng tăng 38% do tích lũy buffer. "
    "Tăng trưởng tín dụng VCB 1,8% YTD thấp hơn CTG. "
    "Đây là chiến lược phòng thủ cho 2027. "
    "NĐT giữ VCB 12 tháng nhờ ổn định."
)

FLUFF_BODY = (
    "Đây là điều cần lưu ý. "
    "Cần theo dõi sát sao xu hướng này. "
    "Tình hình có nhiều biến động trong thời gian tới. "
    "Diễn biến đang theo chiều hướng tích cực. "
    "Điều này rất quan trọng với nhà đầu tư."
)


def test_sentence_density_dense_body_passes():
    from lib.quality_gates import check_sentence_density
    assert check_sentence_density(DENSE_BODY)["pass"] is True


def test_sentence_density_fluff_body_rejects():
    from lib.quality_gates import check_sentence_density
    result = check_sentence_density(FLUFF_BODY)
    assert result["pass"] is False
    assert "density" in result["reason"].lower()


def test_sentence_density_mixed_at_threshold():
    """80% threshold: 4/5 sentences dense → pass."""
    from lib.quality_gates import check_sentence_density
    body = (
        "VCB Q1 LNTT 11.218 tỷ. "
        "Chi phí dự phòng tăng 38% YoY. "
        "CTG tăng 11,4% so cùng kỳ. "
        "Tín dụng 1,8% YTD. "
        "Điều này cần lưu ý."  # only fluff (1 of 5)
    )
    assert check_sentence_density(body)["pass"] is True


def test_sentence_density_bullet_labels_excluded():
    """Bullet labels like '**X:**' not counted as sentences."""
    from lib.quality_gates import check_sentence_density
    body = (
        "VCB tăng 11,4% so cùng kỳ Q1/2026. "
        "**Chi phí dự phòng tăng 38%:** buffer tích lũy do rủi ro BĐS."
    )
    assert check_sentence_density(body)["pass"] is True
```

- [ ] **Step 5: Run tests — fail (all 4 sets)**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_quality_gates.py -v -k "hedging or verdict or stance or density"
```
Expected: FAIL — functions don't exist.

- [ ] **Step 6: Append implementations to `lib/quality_gates.py`**

```python
# === V5.0 Phase 1.5 — Voice Layer gates ===

HEDGING_TERMS = [
    "có thể", "tùy thuộc", "vẫn chờ", "khả năng cao", "đáng theo dõi",
    "nhiều khả năng", "chưa rõ", "có khả năng",
]


def check_no_hedging(body: str) -> dict[str, Any]:
    """V5.0 Gate 6 — reject hedging terms in body (no nước đôi)."""
    cleaned = _clean(body).lower()
    found = [t for t in HEDGING_TERMS if t in cleaned]
    if found:
        return {"pass": False, "reason": f"Hedging terms: {', '.join(found)}"}
    return {"pass": True, "reason": ""}


DIRECTION_KEYWORDS_RE = re.compile(
    r"(tích cực|tiêu cực|cảnh báo|đáng giữ|đáng chú ý|rủi ro|cơ hội|"
    r"nên giữ|nên chờ|nên thận trọng|tăng trưởng dài hạn|đỉnh ngắn hạn|"
    r"đáng lo|không nên cắt|không nên|đáng tích lũy)",
    re.IGNORECASE,
)
TIMEFRAME_KEYWORDS_RE = re.compile(
    r"(12 tháng|18 tháng|6 tháng|3 tháng|Q[1-4](/\d{4})?|năm \d{4}|"
    r"ngắn hạn|trung hạn|dài hạn|trung-dài hạn|quý tới)",
    re.IGNORECASE,
)
# Holder action: "NĐT|nhà đầu tư|người..." within 50 chars of action verb
HOLDER_ACTION_RE = re.compile(
    r"(NĐT|nhà đầu tư|người (giữ|cầm)|đang (cầm|giữ)|holder|"
    r"khớp NĐT)[^.]*?(giữ|chờ|tích lũy|thận trọng|cắt|không nên|nên)",
    re.IGNORECASE,
)


def check_verdict_line(body: str) -> dict[str, Any]:
    """V5.0 Gate 7 — closing must contain 3 elements: direction + timeframe + holder action.

    Inspects last 2 paragraphs of body (post-cleaning). Universal across formats.
    """
    cleaned = _clean(body).strip()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", cleaned) if b.strip()]
    closing_text = "\n".join(blocks[-2:]) if len(blocks) >= 2 else cleaned

    has_direction = bool(DIRECTION_KEYWORDS_RE.search(closing_text))
    has_timeframe = bool(TIMEFRAME_KEYWORDS_RE.search(closing_text))
    has_holder_action = bool(HOLDER_ACTION_RE.search(closing_text))

    missing = []
    if not has_direction:
        missing.append("direction")
    if not has_timeframe:
        missing.append("timeframe")
    if not has_holder_action:
        missing.append("action_for_holder")

    if missing:
        return {"pass": False, "reason": f"Verdict missing: {missing}"}
    return {"pass": True, "reason": ""}


BULLISH_TERMS = [
    "tăng trưởng", "tích cực", "đáng giữ", "đáng chú ý", "cơ hội",
    "mạnh", "ổn định", "lợi thế", "phòng thủ thành công",
    "buffer tích lũy", "cao hơn", "vượt", "lấn", "ngon", "tăng mua",
    "đáng tích lũy",
]
BEARISH_TERMS = [
    "rủi ro", "cảnh báo", "yếu", "lỗ", "giảm",
    "đỉnh ngắn hạn", "không nên", "đáng lo", "đe dọa", "căng thẳng",
    "tiêu cực", "bùng phát", "lao dốc", "cẩn thận", "thận trọng",
]


def check_stance_consistency(body: str, stance: str) -> dict[str, Any]:
    """V5.0 Gate 8 — Master article tone matches brief stance.

    Counts bullish vs bearish keyword occurrences in body. Ratio determines
    tone direction. Cross-stance mismatch → reject. Empty stance keywords → reject (lifeless).
    """
    cleaned = _clean(body).lower()
    bullish = sum(1 for t in BULLISH_TERMS if t in cleaned)
    bearish = sum(1 for t in BEARISH_TERMS if t in cleaned)
    total = bullish + bearish

    if total == 0:
        return {"pass": False, "reason": "Article has no stance keywords (lifeless)"}

    bull_ratio = bullish / total

    if stance == "bullish" and bull_ratio < 0.5:
        return {"pass": False, "reason": f"Brief=bullish but body tone bearish ({bullish} bull vs {bearish} bear)"}
    if stance == "bearish" and bull_ratio > 0.5:
        return {"pass": False, "reason": f"Brief=bearish but body tone bullish ({bullish} bull vs {bearish} bear)"}
    if stance == "divergent" and (bull_ratio < 0.3 or bull_ratio > 0.7):
        return {"pass": False, "reason": f"Brief=divergent but body one-sided ({bull_ratio:.0%} bullish)"}

    return {"pass": True, "reason": ""}


# Sentence density: each sentence must contain ≥1 specific element.
SPECIFIC_ELEMENT_RE = re.compile(
    r"(\d+([.,]\d+)?(%|đ|tỷ|nghìn|triệu)?|"  # numbers w/ optional units
    r"\b(VCB|TCB|MBB|CTG|BID|VPB|HDB|STB|SHB|EIB|TPB|MSB|LPB|OCB|VIB|ACB|"
    r"SSI|VND|HCM|VCI|VIX|SHS|MBS|BVS|"
    r"VHM|NVL|KDH|DXG|"
    r"Big4|HOSE|HNX|UPCOM|NHNN|ĐHĐCĐ)\b|"  # ticker/proper nouns
    r"(cao hơn|thấp hơn|gấp|vượt|hơn|thấp nhất|cao nhất|so với|so cùng kỳ)|"  # comparative
    r"(Q[1-4]|năm \d{4}|tháng \d|quý|tuần|YTD|YoY|QoQ|hôm nay)|"  # time
    r"(do|vì|nhờ|khiến|dẫn đến|kéo theo|bổ sung|trở thành|chuyển|tích lũy|đánh đổi)|"  # mechanism
    r"(rút|chuyển|duy trì|phòng thủ|lấn sang|tăng|giảm|đi chậm|nới|co)",  # action verb
    re.IGNORECASE,
)


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences. Heuristic: '. ! ?' as delimiters.

    Note: Vietnamese abbreviations like "Q1." may produce false splits — known
    limitation, tune lexicon if recall problems emerge (spec §18).
    """
    # Treat '. ' as boundary unless followed by lowercase (continuation)
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]


def _is_bullet_label(sentence: str) -> bool:
    """Detect bullet label form like '- **X:**' or '**X:**' — not a free sentence."""
    s = sentence.lstrip("- *").strip()
    return bool(re.match(r"^\*\*[^*]+\*\*:?\s*$", s))


def check_sentence_density(body: str) -> dict[str, Any]:
    """V5.0 Gate 9 — ≥80% sentences in body contain ≥1 specific element.

    Banned fluff sentences (e.g. "Đây là điều cần lưu ý") have no element →
    fail. Bullet labels excluded from count.
    """
    cleaned = _clean(body).strip()
    sentences = _split_sentences(cleaned)
    # Filter: skip bullet labels (markup-only "lines")
    countable = [s for s in sentences if not _is_bullet_label(s)]
    if not countable:
        return {"pass": True, "reason": ""}  # empty body — defer to word_count gate
    has_element = [bool(SPECIFIC_ELEMENT_RE.search(s)) for s in countable]
    pass_count = sum(has_element)
    ratio = pass_count / len(countable)
    if ratio < 0.8:
        fluff = [s for s, ok in zip(countable, has_element) if not ok]
        return {
            "pass": False,
            "reason": f"Density {ratio:.0%} (<80%) — {len(fluff)} fluff sentences: {fluff[:3]}",
        }
    return {"pass": True, "reason": ""}
```

- [ ] **Step 7: Run all tests — verify pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_quality_gates.py -v
```
Expected: all green.

- [ ] **Step 8: Commit**

```bash
git add lib/quality_gates.py tests/test_quality_gates.py
git commit -m "feat(quality_gates): 4 new V5.0 universal gates (Phase 1.5)

Voice Layer enforcement:
- check_no_hedging: reject 'có thể', 'tùy thuộc', 'đáng theo dõi', ...
- check_verdict_line: closing must have direction + timeframe + holder action
- check_stance_consistency: body tone matches brief.stance (bullish/bearish/divergent)
- check_sentence_density: ≥80% sentences contain specific element (number/name/comparative/time/mechanism/action)

Extends existing quality_gates.py — does not create new gate_checker.py.
"
```

---

### Task 6: Per-format gates + dispatch registry in `quality_gates.py`

**Files:**
- Modify: `lib/quality_gates.py`
- Test: `tests/test_quality_gates.py`

Per-format gates: `word_count` ranges differ, `body_pattern` structure differs, `title_pattern` regex differs.

- [ ] **Step 1: Write failing tests for per-format gate dispatch**

Append to `tests/test_quality_gates.py`:

```python
# === V5.0 Phase 1.6 — per-format gates + dispatch ===

def test_per_format_flash_qa_word_count():
    from lib.quality_gates import check_word_count_per_format
    body_100w = " ".join(["word"] * 100)
    assert check_word_count_per_format(body_100w, "flash_qa")["pass"] is True
    body_200w = " ".join(["word"] * 200)
    assert check_word_count_per_format(body_200w, "flash_qa")["pass"] is False  # > 150


def test_per_format_standard_qa_word_count_unchanged():
    from lib.quality_gates import check_word_count_per_format
    body_250w = " ".join(["word"] * 250)
    assert check_word_count_per_format(body_250w, "standard_qa")["pass"] is True
    body_100w = " ".join(["word"] * 100)
    assert check_word_count_per_format(body_100w, "standard_qa")["pass"] is False


def test_per_format_flash_qa_body_pattern_no_bullets():
    """Flash format: paragraph only, NO bullets."""
    from lib.quality_gates import check_body_pattern_per_format
    body_with_bullet = (
        "Opening paragraph of about thirty words flash qa minimum length minimum "
        "test test test test test test test test test.\n\n- bullet violation here\n\nClosing."
    )
    result = check_body_pattern_per_format(body_with_bullet, "flash_qa")
    assert result["pass"] is False
    assert "bullet" in result["reason"].lower()


def test_per_format_flash_qa_body_paragraph_only_passes():
    from lib.quality_gates import check_body_pattern_per_format
    body = (
        "VCB chia cổ tức 21% bằng cổ phiếu chốt phương án phát hành 21:1 vốn điều "
        "lệ tăng từ 83.557 lên 101.124 tỷ pha loãng EPS giấy tờ khoảng 17% nhưng "
        "P/E forward thực tế không đổi vì cổ tức cổ phiếu chuyển hạch toán LNCPS "
        "vốn cổ phần không đổi giá trị doanh nghiệp NĐT giữ dài hạn theo cốt lõi."
    )
    assert check_body_pattern_per_format(body, "flash_qa")["pass"] is True


def test_per_format_standard_listicle_min_4_bullets():
    """Listicle requires 4-7 bullets, each ≥25 words."""
    from lib.quality_gates import check_body_pattern_per_format
    body_3bullets = (
        "Opening ngắn 20 từ test test test test test test test test test test test "
        "test test test test test test test.\n\n"
        "- **Bullet 1**: " + " ".join(["word"] * 25) + "\n"
        "- **Bullet 2**: " + " ".join(["word"] * 25) + "\n"
        "- **Bullet 3**: " + " ".join(["word"] * 25) + "\n\n"
        "Closing."
    )
    result = check_body_pattern_per_format(body_3bullets, "standard_listicle")
    assert result["pass"] is False
    assert "4" in result["reason"] or "bullet" in result["reason"].lower()


def test_per_format_title_flash_qa_needs_question_mark():
    from lib.quality_gates import check_title_per_format
    assert check_title_per_format("VCB chia cổ tức — pha loãng tới mức nào?", "flash_qa")["pass"] is True
    assert check_title_per_format("VCB chia cổ tức 21%.", "flash_qa")["pass"] is False


def test_per_format_title_standard_listicle_numbered():
    from lib.quality_gates import check_title_per_format
    assert check_title_per_format("5 dấu hiệu Big4 và tư nhân đang đi ngược", "standard_listicle")["pass"] is True
    assert check_title_per_format("Big4 và tư nhân đang đi ngược", "standard_listicle")["pass"] is False  # no leading number


def test_per_format_title_standard_narrative_em_dash():
    from lib.quality_gates import check_title_per_format
    assert check_title_per_format("TCB chia cổ tức 67% — câu chuyện CASA 12 tháng", "standard_narrative")["pass"] is True
    assert check_title_per_format("TCB chia cổ tức 67%", "standard_narrative")["pass"] is False  # no em dash


def test_check_all_v5_dispatches_per_format():
    """check_all_v5 runs universal + per-format. Standard_qa with valid V4-pattern article passes."""
    from lib.quality_gates import check_all_v5
    body = (
        "VCB Q1/2026 LNTT 11.218 tỷ — chỉ tăng 1,3% so cùng kỳ. "
        "Vì sao to nhất sàn lại đi chậm nhất Q1/2026?\n\n"
        "- **Chi phí dự phòng tăng 38%**: VCB tăng buffer trước rủi ro nợ xấu BĐS chấp nhận hy sinh LNTT.\n"
        "- **Biên lãi vay co từ 3,06% xuống 2,71%**: ưu tiên giữ khách hàng tốt thay đẩy lãi suất.\n"
        "- **Tăng trưởng tín dụng 1,8% YTD**: trong khi CTG 4,3% và BID 3,8% VCB tự chậm có chủ đích.\n\n"
        "Tích cực dài hạn cho VCB. NĐT đang cầm nên giữ 12 tháng — chiến lược phòng thủ Q1 sẽ thành lợi thế."
    )
    title = "Vì sao to nhất sàn lại đi chậm nhất quý này?"
    results = check_all_v5(body, title, format_id="standard_qa", stance="bullish")
    # All universal + per-format should pass
    failed = [(k, v) for k, v in results.items() if not v["pass"]]
    assert not failed, f"Unexpected failures: {failed}"
```

- [ ] **Step 2: Run test — fail**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_quality_gates.py -v -k "per_format or check_all_v5"
```
Expected: FAIL — functions don't exist.

- [ ] **Step 3: Append implementations to `lib/quality_gates.py`**

```python
# === V5.0 Phase 1.6 — per-format gates ===

from lib.format_registry import get_format


def check_word_count_per_format(body: str, format_id: str) -> dict[str, Any]:
    """V5.0 Gate 2 — word count must be within format's length_range."""
    cleaned = _clean(body).strip()
    n = len(cleaned.split())
    fmt = get_format(format_id)
    lo, hi = fmt["length_range"]
    if n < lo:
        return {"pass": False, "reason": f"Too short: {n} words (need {lo}-{hi} for {format_id})"}
    if n > hi:
        return {"pass": False, "reason": f"Too long: {n} words (need {lo}-{hi} for {format_id})"}
    return {"pass": True, "reason": ""}


def check_body_pattern_per_format(body: str, format_id: str) -> dict[str, Any]:
    """V5.0 Gate 3 — body structure per format spec.

    flash_qa: paragraph only, NO bullets.
    standard_qa: opening ≥30 + 3-6 bullets ≥20w + closing.
    standard_listicle: opening ≤30 + 4-7 bullets ≥25w + closing.
    standard_narrative: opening ≥40 + flow paragraphs + 0-2 bullets.
    """
    cleaned = _clean(body).strip()
    fmt = get_format(format_id)
    structure = fmt["structure"]
    blocks = [b.strip() for b in re.split(r"\n\s*\n", cleaned) if b.strip()]

    # No '## Cần để ý' allowed in any format
    if re.search(r"^#{2,3}\s+C[ầa]n\s+đ[ểe]?\s+ý", cleaned, flags=re.MULTILINE):
        return {"pass": False, "reason": "Contains '## Cần để ý' section — banned"}

    if structure == "paragraph_only":
        # flash_qa: no bullet lines anywhere
        for line in cleaned.split("\n"):
            if line.lstrip().startswith(("- ", "* ")):
                return {"pass": False, "reason": "flash_qa: bullet found, format requires paragraph only"}
        return {"pass": True, "reason": ""}

    if structure in ("opening_bullets_closing", "short_opening_dense_bullets"):
        # standard_qa or standard_listicle
        if len(blocks) < 3:
            return {"pass": False, "reason": f"Need ≥3 blocks (opening + bullets + closing), got {len(blocks)}"}
        opening = blocks[0]
        closing = blocks[-1]
        middle = blocks[1:-1]
        if opening.startswith(("- ", "* ")):
            return {"pass": False, "reason": "Opening must be paragraph, not bullet"}

        opening_words = len(opening.split())
        opening_min = fmt.get("opening_min", 0)
        opening_max = fmt.get("opening_max")
        if opening_words < opening_min:
            return {"pass": False, "reason": f"Opening too short: {opening_words} words (need ≥{opening_min} for {format_id})"}
        if opening_max is not None and opening_words > opening_max:
            return {"pass": False, "reason": f"Opening too long: {opening_words} words (need ≤{opening_max} for {format_id})"}

        if closing.startswith(("- ", "* ")) or closing.startswith("#"):
            return {"pass": False, "reason": "Closing must be sentence, not bullet/heading"}

        # Collect bullets
        bullets: list[str] = []
        for block in middle:
            for line in block.split("\n"):
                line = line.strip()
                if line.startswith(("- ", "* ")):
                    bullets.append(line[2:].strip())
                elif line and bullets:
                    bullets[-1] += " " + line
                elif line:
                    return {"pass": False, "reason": f"Non-bullet text in middle: '{line[:60]}'"}

        b_lo, b_hi = fmt["bullets_count"]
        if not (b_lo <= len(bullets) <= b_hi):
            return {"pass": False, "reason": f"Need {b_lo}-{b_hi} bullets, got {len(bullets)}"}
        bullet_min = fmt["bullet_min_length"]
        for i, b in enumerate(bullets, 1):
            words = len(b.split())
            if words < bullet_min:
                return {"pass": False, "reason": f"Bullet {i} too short: {words} words (need ≥{bullet_min} for {format_id})"}
            if "**" not in b:
                return {"pass": False, "reason": f"Bullet {i} missing bold highlight"}
        return {"pass": True, "reason": ""}

    if structure == "flow_paragraphs":
        # standard_narrative: opening + flow paragraphs + ≤2 highlight bullets allowed
        if len(blocks) < 2:
            return {"pass": False, "reason": "narrative: need ≥2 paragraphs"}
        opening = blocks[0]
        if opening.startswith(("- ", "* ")):
            return {"pass": False, "reason": "Opening must be paragraph"}
        opening_words = len(opening.split())
        if opening_words < fmt.get("opening_min", 40):
            return {"pass": False, "reason": f"Opening too short: {opening_words} words (need ≥40)"}
        # Count bullet lines
        bullet_count = sum(1 for line in cleaned.split("\n") if line.lstrip().startswith(("- ", "* ")))
        b_lo, b_hi = fmt["bullets_count"]
        if bullet_count > b_hi:
            return {"pass": False, "reason": f"narrative: {bullet_count} bullets, max {b_hi} highlights allowed"}
        return {"pass": True, "reason": ""}

    return {"pass": False, "reason": f"Unknown structure: {structure}"}


def check_title_per_format(title: str, format_id: str) -> dict[str, Any]:
    """V5.0 Gate 4 — title pattern per format.

    flash_qa: must contain '?' (question).
    standard_qa: '?' OR '—' + tension word.
    standard_listicle: numbered declarative (leading number).
    standard_narrative: contains '—' (em dash splits 2 vế).
    """
    if not title:
        return {"pass": False, "reason": "Title empty"}
    fmt = get_format(format_id)
    pattern = fmt["title_pattern"]

    if pattern == "question":
        if "?" not in title:
            return {"pass": False, "reason": "flash_qa title must contain '?'"}
        return {"pass": True, "reason": ""}

    if pattern == "question_or_paradox":
        if "?" in title:
            return {"pass": True, "reason": ""}
        if "—" in title:
            tlc = title.lower()
            for tword in fmt.get("title_tension_words", []):
                if tword in tlc:
                    return {"pass": True, "reason": ""}
            return {"pass": False, "reason": "Title has '—' but no tension word"}
        return {"pass": False, "reason": "standard_qa title needs '?' OR '—' + tension word"}

    if pattern == "numbered_declarative":
        regex = fmt.get("title_must_match_regex", r"^\d+\s+")
        if re.search(regex, title):
            return {"pass": True, "reason": ""}
        return {"pass": False, "reason": "standard_listicle title must start with number ('5 dấu hiệu...', '3 lý do...')"}

    if pattern == "declarative_story":
        if "—" not in title:
            return {"pass": False, "reason": "standard_narrative title must contain '—' (em dash)"}
        return {"pass": True, "reason": ""}

    return {"pass": False, "reason": f"Unknown title_pattern: {pattern}"}


def check_all_v5(body: str, title: str, format_id: str, stance: str) -> dict[str, dict[str, Any]]:
    """Run all 9 V5.0 gates: 6 universal + 3 per-format.

    Universal: no_english_jargon, no_metadata_leak, no_hedging, verdict_line,
               stance_consistency, sentence_density.
    Per-format: word_count, body_pattern, title_pattern.
    """
    return {
        "no_english_jargon": check_no_english_jargon(body),
        "no_metadata_leak": check_no_metadata_leak(body),
        "no_hedging": check_no_hedging(body),
        "verdict_line": check_verdict_line(body),
        "stance_consistency": check_stance_consistency(body, stance),
        "sentence_density": check_sentence_density(body),
        "word_count": check_word_count_per_format(body, format_id),
        "body_pattern": check_body_pattern_per_format(body, format_id),
        "title_pattern": check_title_per_format(title, format_id),
    }
```

- [ ] **Step 4: Run all tests**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_quality_gates.py -v
```
Expected: all green.

- [ ] **Step 5: Commit**

```bash
git add lib/quality_gates.py tests/test_quality_gates.py
git commit -m "feat(quality_gates): per-format gates + check_all_v5 dispatch (Phase 1.6)

V5.0 9-gate enforcement:
- check_word_count_per_format: per-format range (flash 100-150, standard 200-350)
- check_body_pattern_per_format: 4 structures (paragraph_only / opening_bullets_closing /
  short_opening_dense_bullets / flow_paragraphs)
- check_title_per_format: 4 patterns (question / question_or_paradox / numbered_declarative / declarative_story)
- check_all_v5: orchestrator combining 6 universal + 3 per-format gates

Reads format spec from lib/format_registry. Existing 5 V4.0 gates (check_all) preserved for back-compat.
"
```

---

### Task 7: Pipeline observability schema — `step_3_5_format_director` payload

Already covered in Task 4 (`_STEP_3_5_REQUIRED`). This task verifies integration with `log_pipeline_step` for the new step key.

**Files:**
- Test: `tests/test_pipeline_db.py`

- [ ] **Step 1: Write integration test**

```python
def test_log_pipeline_step_3_5_format_director(tmp_path):
    """Logging step_3_5_format_director with valid payload persists."""
    from lib.pipeline_db import PipelineDB
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    db.init_schema("data/pipeline.schema.sql")
    db.insert_crawl_row({
        "row_id": "r1", "funnel_batch_id": "b1", "ticker": "VCB",
        "source_name": "CafeF", "source_url": "http://x.com/1",
        "title": "T", "crawled_at": "2026-05-11T00:00:00Z",
    })
    db.insert_generated_news({
        "article_id": "a1", "row_id": "r1", "ticker": "VCB", "sector": "Bank",
        "title": "T", "body": "...", "accepted_hypothesis": 1, "status": "draft",
        # pipeline_version defaults to V5.0 via Task 3
    })
    payload = {
        "format_picks": [
            {"option_idx": 0, "format_id": "standard_qa", "format_reason": "test", "tone_bias": "neutral", "length_target": 250},
        ],
        "candidates_considered_per_option": [],
        "variety_check": {},
        "model": "claude-sonnet-4-6",
        "duration_ms": 8400,
        "tokens": 1240,
    }
    db.log_pipeline_step("a1", "step_3_5_format_director", payload)
    # Verify persisted
    row = db.conn.execute("SELECT pipeline_log FROM generated_news WHERE article_id='a1'").fetchone()
    import json
    log = json.loads(row["pipeline_log"])
    assert "step_3_5_format_director" in log
    assert log["step_3_5_format_director"]["format_picks"][0]["format_id"] == "standard_qa"
    db.close()


def test_log_pipeline_step_3_5_empty_format_picks_rejects(tmp_path):
    """Empty format_picks → ValueError (non-empty constraint)."""
    from lib.pipeline_db import PipelineDB
    import pytest
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    db.init_schema("data/pipeline.schema.sql")
    db.insert_crawl_row({
        "row_id": "r1", "funnel_batch_id": "b1", "ticker": "VCB",
        "source_name": "CafeF", "source_url": "http://x.com/1",
        "title": "T", "crawled_at": "2026-05-11T00:00:00Z",
    })
    db.insert_generated_news({
        "article_id": "a1", "row_id": "r1", "ticker": "VCB", "sector": "Bank",
        "title": "T", "body": "...", "accepted_hypothesis": 1, "status": "draft",
    })
    with pytest.raises(ValueError, match="format_picks"):
        db.log_pipeline_step("a1", "step_3_5_format_director", {"format_picks": []})
    db.close()
```

- [ ] **Step 2: Run tests — verify pass (validate_pipeline_step already implements this)**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_pipeline_db.py::test_log_pipeline_step_3_5_format_director tests/test_pipeline_db.py::test_log_pipeline_step_3_5_empty_format_picks_rejects -v
```
Expected: pass (logic already in Task 4).

- [ ] **Step 3: Commit**

```bash
git add tests/test_pipeline_db.py
git commit -m "test(pipeline_db): step_3_5_format_director persistence integration (Phase 1.7)

Validates Task 4 version-gate logic works end-to-end via log_pipeline_step.
"
```

---

## Phase 2 — Format Director agent (Tasks 8-11)

### Task 8: Format picker logic — `lib/format_picker_logic.py`

5-step deterministic flow exposed as Python helper. Used by Format Director agent (as logic reference in prompt) AND testable independently.

**Files:**
- Create: `lib/format_picker_logic.py`
- Create: `tests/test_format_picker_logic.py`

- [ ] **Step 1: Write failing tests**

`tests/test_format_picker_logic.py`:

```python
"""Tests for lib/format_picker_logic — 5-step format selection flow."""
from __future__ import annotations
import pytest
from lib.format_picker_logic import pick_format_for_option


# Build minimal option fixtures
def _option(category="paradox", narrative="...", data_trail_preview=None, key_metric_count=2):
    return {
        "category": category,
        "narrative_setup": narrative,
        "data_trail_preview": data_trail_preview or [{"source": "Finpath_API/test"}, {"source": "KB/test"}, {"source": "WebSearch/test"}],
        "key_metric_count": key_metric_count,
    }


def test_paradox_picks_standard_qa():
    result = pick_format_for_option(_option(category="paradox"), market_data=None)
    assert result["format_id"] == "standard_qa"
    assert result["tone_bias"] == "neutral"
    assert result["length_target"] == 250


def test_why_now_picks_standard_qa():
    result = pick_format_for_option(_option(category="why_now"), market_data=None)
    assert result["format_id"] == "standard_qa"


def test_comparison_deep_picks_listicle():
    result = pick_format_for_option(_option(category="comparison_deep"), market_data=None)
    assert result["format_id"] == "standard_listicle"


def test_early_signal_picks_listicle():
    result = pick_format_for_option(_option(category="early_signal"), market_data=None)
    assert result["format_id"] == "standard_listicle"


def test_hidden_mechanism_no_timeline_picks_qa():
    opt = _option(category="hidden_mechanism", narrative="Cơ chế NIM nội tại")
    result = pick_format_for_option(opt, market_data=None)
    assert result["format_id"] == "standard_qa"


def test_hidden_mechanism_3_timeline_markers_picks_narrative():
    opt = _option(
        category="hidden_mechanism",
        narrative="Q1/2025 TCB rút 12.000 tỷ. Đến cuối 2024 quyết định. Năm 2026 thấy kết quả.",
    )
    result = pick_format_for_option(opt, market_data=None)
    assert result["format_id"] == "standard_narrative"


def test_unknown_category_falls_back_flash_qa():
    """Factual question without 5-category → flash_qa fallback."""
    result = pick_format_for_option(_option(category="factual_single"), market_data=None)
    assert result["format_id"] == "flash_qa"


def test_length_downgrade_low_data_depth():
    """data_trail_preview≤2 sources AND key_metric_count≤1 → downgrade standard→flash."""
    opt = _option(
        category="paradox",
        data_trail_preview=[{"source": "KB/test"}],
        key_metric_count=1,
    )
    result = pick_format_for_option(opt, market_data=None)
    assert result["format_id"] == "flash_qa"


def test_mood_red_tone_bias():
    market_data = {"pct_change_today": -4.5}
    result = pick_format_for_option(_option(category="paradox"), market_data=market_data)
    assert result["tone_bias"] == "acknowledge_market_red"


def test_mood_green_tone_bias():
    market_data = {"pct_change_today": 5.0}
    result = pick_format_for_option(_option(category="paradox"), market_data=market_data)
    assert result["tone_bias"] == "acknowledge_market_green"


def test_mood_neutral_under_threshold():
    market_data = {"pct_change_today": 1.5}
    result = pick_format_for_option(_option(category="paradox"), market_data=market_data)
    assert result["tone_bias"] == "neutral"


def test_format_reason_contains_template():
    """format_reason fills template, no free-write."""
    result = pick_format_for_option(_option(category="paradox"), market_data=None)
    assert "Category=" in result["format_reason"]
    assert "paradox" in result["format_reason"]


def test_returned_keys():
    """Output shape: 4 fields."""
    result = pick_format_for_option(_option(), market_data=None)
    assert set(result.keys()) == {"format_id", "format_reason", "tone_bias", "length_target"}
```

- [ ] **Step 2: Run test — fail**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_format_picker_logic.py -v
```
Expected: ModuleNotFoundError.

- [ ] **Step 3: Implement `lib/format_picker_logic.py`**

```python
"""Format picker logic — 5-step deterministic flow.

Exposed as Python helper so Format Director agent can reference + so logic
is testable independently. Agent prompt mirrors this logic but Python
exposes it for code-level fallback / testing / future Format Director
swap (vd to a Haiku agent).

Used by:
- newsroom-format-director agent (mirrors logic in prose)
- lib/stages tests
- Future: lib/stages/run_format_director.py fallback if agent fails
"""
from __future__ import annotations
import re
from typing import Any

from lib.format_registry import load_registry, get_candidates_for_category, FORMAT_IDS

# Step 1 — category → candidates filter (from registry)
# Step 2 — tie-break for hidden_mechanism: ≥3 timeline markers → narrative

TIMELINE_MARKER_RE = re.compile(
    r"(Q[1-4]/?\d{0,4}|năm \d{4}|tháng \d{1,2}|cuối năm|đầu năm|"
    r"\d{4}|hồi \d{4})",
    re.IGNORECASE,
)


def _count_timeline_markers(text: str) -> int:
    return len(TIMELINE_MARKER_RE.findall(text or ""))


def _format_reason_template(category: str, candidates: list[str], chosen: str, extra: str = "") -> str:
    base = f"Category={category} → candidates={candidates}. Picked={chosen}."
    if extra:
        return f"{base} {extra}"
    return base


def pick_format_for_option(option: dict, market_data: dict | None) -> dict[str, Any]:
    """Run 5-step flow on 1 deep_question_option.

    Args:
      option: {category, narrative_setup, data_trail_preview, key_metric_count}
      market_data: {pct_change_today, ...} or None

    Returns:
      {format_id, format_reason, tone_bias, length_target}
    """
    category = option.get("category", "")
    narrative = option.get("narrative_setup", "")
    data_preview = option.get("data_trail_preview") or []
    key_metric_count = option.get("key_metric_count", 0)

    # Step 1 — category → candidates
    candidates = get_candidates_for_category(category)
    if not candidates:
        # Fallback: factual single Q → flash_qa
        chosen = "flash_qa"
        extra = f"No candidates for category={category!r}, fallback flash_qa."
    elif len(candidates) == 1:
        chosen = candidates[0]
        extra = ""
    else:
        # Step 2 — tie-break (hidden_mechanism: 2 candidates)
        n_markers = _count_timeline_markers(narrative)
        if n_markers >= 3 and "standard_narrative" in candidates:
            chosen = "standard_narrative"
            extra = f"Tie-break: {n_markers} timeline markers → narrative."
        else:
            chosen = "standard_qa"
            extra = f"Tie-break: {n_markers} timeline markers (<3) → qa."

    # Step 3 — length downgrade for shallow data
    n_sources = len(data_preview)
    if n_sources <= 2 and key_metric_count <= 1 and chosen.startswith("standard_"):
        chosen_old = chosen
        chosen = "flash_qa"
        extra += f" Downgrade {chosen_old}→flash_qa (sources={n_sources}, metrics={key_metric_count})."

    # Step 4 — tone bias from market mood
    tone_bias = "neutral"
    if market_data:
        pct = market_data.get("pct_change_today", 0)
        if pct <= -3.0:
            tone_bias = "acknowledge_market_red"
        elif pct >= 3.0:
            tone_bias = "acknowledge_market_green"

    # Step 5 — length target from registry
    reg = load_registry()
    length_target = reg[chosen]["length_target"]

    format_reason = _format_reason_template(category, candidates or ["fallback"], chosen, extra=extra.strip())

    return {
        "format_id": chosen,
        "format_reason": format_reason,
        "tone_bias": tone_bias,
        "length_target": length_target,
    }
```

- [ ] **Step 4: Run tests — verify pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_format_picker_logic.py -v
```
Expected: 13 passed.

- [ ] **Step 5: Commit**

```bash
git add lib/format_picker_logic.py tests/test_format_picker_logic.py
git commit -m "feat(format-picker): 5-step format selection logic Python helper (Phase 2.1)

Deterministic implementation mirroring Format Director agent prose.
- Step 1: category → candidates from registry
- Step 2: tie-break hidden_mechanism via timeline markers (≥3 → narrative)
- Step 3: length downgrade for shallow data
- Step 4: tone bias from market_data pct_change
- Step 5: length_target from registry

Exposed for testing + future fallback if agent fails.
"
```

---

### Task 9: Format Director agent — `.claude/agents/newsroom-format-director.md`

**Files:**
- Create: `.claude/agents/newsroom-format-director.md`

- [ ] **Step 1: Write agent file**

```markdown
---
name: newsroom-format-director
description: Format Director V5.0 — enrich Story Editor brief with format_id + tone_bias + length_target per deep_question_option. Reads brief V5.0 (with stance) + ticker_market_data (optional) → applies 5-step deterministic flow via lib.format_picker_logic → outputs format_picks array. Use when newsroom-pipeline dispatches Step 3.5 between Story Editor and Master sector. Model Sonnet for cost + stability.
tools: Bash, Read, Grep
model: sonnet
---

# Newsroom Format Director Agent V5.0

Bạn quyết format cho từng deep_question_option trong brief Story Editor. KHÔNG viết bài, KHÔNG critique. Chỉ pick format.

## 🚨 HARD RULE — KHÔNG sáng tạo step mới

Pick format theo 5-step deterministic flow trong section "Workflow" dưới đây. KHÔNG suy luận extra. KHÔNG pick format ngoài 4 catalog. KHÔNG đẻ trigger_category mới.

Nếu confused / data thiếu / category không match → **fallback `flash_qa`** + log lý do. Bao giờ cũng emit format_id valid (1 trong 4: flash_qa | standard_qa | standard_listicle | standard_narrative).

## Input

```json
{
  "brief": {
    "ticker": "VCB",
    "sector": "Bank",
    "deep_question_options": [
      {
        "question": "...",
        "category": "paradox|why_now|hidden_mechanism|comparison_deep|early_signal",
        "stance": "bullish|bearish|divergent",
        "narrative_setup": "...",
        "data_trail_preview": [...],
        "key_metric_count": 3
      },
      ...
    ]
  },
  "ticker_market_data": {  // may be null
    "price_today": 92500,
    "pct_change_today": -3.2,
    "volume_ratio_3d": 1.4,
    "fetched_at": "..."
  } | null
}
```

## Output (structured JSON, NOT free prose)

```json
{
  "brief_enriched": {
    "ticker": "VCB",
    "sector": "Bank",
    "deep_question_options": [
      {
        "question": "...",
        "category": "...",
        "stance": "...",
        "narrative_setup": "...",
        "data_trail_preview": [...],
        "key_metric_count": 3,
        "format_id": "standard_qa",          // NEW V5.0
        "format_reason": "Category=paradox → candidates=['standard_qa']. Picked=standard_qa.",
        "tone_bias": "neutral",               // neutral | acknowledge_market_red | acknowledge_market_green
        "length_target": 250
      },
      ...
    ]
  },
  "format_director_log": {
    "format_picks": [
      {"option_idx": 0, "format_id": "standard_qa", "format_reason": "...", "tone_bias": "neutral", "length_target": 250},
      ...
    ],
    "candidates_considered_per_option": [
      {"option_idx": 0, "category": "paradox", "candidates": ["standard_qa"]},
      ...
    ],
    "variety_check": {
      "recent_3_articles_same_ticker_formats": ["standard_qa", "standard_qa", "standard_listicle"],
      "current_pick_diversity_warning": false
    }
  }
}
```

## Workflow — 5-step deterministic flow

Reference Python implementation: `lib/format_picker_logic.py::pick_format_for_option`. Agent prose mirrors but you execute via thinking — do NOT shell out to Python (avoid latency + parsing).

**FOR EACH option in `brief.deep_question_options`:**

### Step 1 — Category → candidate formats

| category | candidates |
|---|---|
| `paradox` | `[standard_qa]` |
| `why_now` | `[standard_qa]` |
| `hidden_mechanism` | `[standard_qa, standard_narrative]` ← multi |
| `comparison_deep` | `[standard_listicle]` |
| `early_signal` | `[standard_listicle]` |
| (anything else / factual single Q) | `[flash_qa]` (fallback) |

### Step 2 — Tie-breaking (chỉ chạy khi >1 candidate)

`hidden_mechanism` case:
- Count timeline markers trong `narrative_setup`: matches regex `(Q[1-4]/?\d{0,4}|năm \d{4}|tháng \d|cuối năm|đầu năm|\d{4})`
- IF count ≥3 → pick `standard_narrative`
- ELSE → pick `standard_qa`

### Step 3 — Length downgrade

IF `len(data_trail_preview) <= 2` AND `key_metric_count <= 1` AND picked is standard_*:
- Downgrade picked → `flash_qa`
- Reason: data nông không justify dài 250+ từ.

ELSE: keep picked.

### Step 4 — Tone bias

| pct_change_today | tone_bias |
|---|---|
| ≤ -3.0% | `acknowledge_market_red` |
| ≥ +3.0% | `acknowledge_market_green` |
| else / market_data null | `neutral` |

### Step 5 — Length target

Read from `data/format_registry.yaml` (or hard-code defaults below):
- flash_qa: 130
- standard_qa: 250
- standard_listicle: 300
- standard_narrative: 300

## Variety check (anti-self-bias)

Before final output, query 3 most-recent articles for `brief.ticker`:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
rows = db.recent_generated_news('<TICKER>', limit=3)
formats = []
for r in rows:
    pl = json.loads(r.get('pipeline_log') or '{}')
    fid = pl.get('step_4_master', {}).get('format_id_used', 'unknown')
    formats.append(fid)
print(json.dumps(formats))
db.close()
"
```

IF all 3 same as current pick → set `variety_check.current_pick_diversity_warning: true` in log + add note `"Recent 3 articles all use {fmt} — consider alternative if data supports"` to `format_reason`. **Do NOT change pick** (data justifies pick is sticky).

## Format spec reference

Load `data/format_registry.yaml` via Read tool when need to look up. 4 formats only:
- `flash_qa` 100-150 từ, paragraph only, no bullets, title needs `?`
- `standard_qa` 200-300 từ, opening + 3-6 bullets + closing, title `?` or `—` + tension word
- `standard_listicle` 250-350 từ, opening ≤30 + 4-7 dense bullets + closing, title numbered ("5 dấu hiệu...")
- `standard_narrative` 250-350 từ, flow paragraphs, 0-2 bullets, title with `—`

## Persist to SQLite

For the batch of articles being processed (1 per picked brief from Story Editor):

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
payload = {
    'format_picks': <JSON list from output above>,
    'candidates_considered_per_option': <list>,
    'variety_check': <dict>,
    'model': 'claude-sonnet-4-6',
    'duration_ms': <int>,
    'tokens': <int or null>,
}
for article_id in <article_ids list>:
    db.log_pipeline_step(article_id, 'step_3_5_format_director', payload)
db.close()
"
```

⚠️ pipeline_log validation cứng (V5.0): `format_picks` MUST be non-empty list. Empty list → ValueError, không persist.

## Hard rules

- Output STRUCTURED JSON, no free prose
- `format_id` ∈ 4 valid IDs — code-level validation rejects otherwise
- Fallback `flash_qa` khi confused / unknown category
- `format_reason` follow template, không creative write
- KHÔNG dispatch sub-agent — pure mapping logic
- KHÔNG re-run nếu Master escalates (Master's escalation log handled trong step_4_master separately)
```

- [ ] **Step 2: Verify agent file is well-formed**

```bash
head -10 .claude/agents/newsroom-format-director.md
```

Expected: shows YAML frontmatter `name: newsroom-format-director`, `model: sonnet`.

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/newsroom-format-director.md
git commit -m "feat(agent): newsroom-format-director V5.0 agent prose (Phase 2.2)

Sonnet model. Enriches Story Editor brief with format_id + tone_bias +
length_target per option. 5-step deterministic flow mirrors
lib.format_picker_logic. Variety check warns when 3 recent articles
same ticker all picked same format.

Hard rules: structured JSON output, fallback flash_qa, no creative
format invention, format_reason template-filled.
"
```

---

### Task 10: Format Director skill — `.claude/skills/finpath-newsroom-format-director/SKILL.md`

**Files:**
- Create: `.claude/skills/finpath-newsroom-format-director/SKILL.md`

- [ ] **Step 1: Inspect existing skill template**

```bash
cat .claude/skills/finpath-newsroom-editor/SKILL.md | head -40
```

Look at frontmatter pattern (`name`, `description`, etc.).

- [ ] **Step 2: Create skill file**

```markdown
---
name: finpath-newsroom-format-director
description: Format Director skill V5.0 — 5-step flow to pick format_id per deep_question_option. Use when newsroom-format-director agent runs Step 3.5 of pipeline. Covers category → candidate filter, hidden_mechanism tie-break via timeline markers, length downgrade heuristic, tone bias from market mood, variety guard.
---

# Format Director Skill V5.0

Compact reference for the Format Director agent. Loaded via `Skill: finpath-newsroom-format-director` at agent invocation.

## Format catalog summary (load `data/format_registry.yaml` for full spec)

| format_id | length | structure | title pattern | trigger categories |
|---|---|---|---|---|
| `flash_qa` | 100-150 từ | paragraph only, no bullets | `?` (question) | fallback (factual single Q) |
| `standard_qa` | 200-300 từ | opening + 3-6 bullets + closing | `?` OR `—` + tension word | paradox, why_now, hidden_mechanism |
| `standard_listicle` | 250-350 từ | opening ≤30 + 4-7 dense bullets + closing | numbered ("5 dấu hiệu...") | comparison_deep, early_signal |
| `standard_narrative` | 250-350 từ | flow paragraphs, 0-2 bullets | declarative story with `—` | hidden_mechanism (tie-break) |

## 5-step flow (deterministic, no creativity)

1. **Category → candidates filter** (5 trigger_categories defined). No match → fallback `flash_qa`.
2. **Tie-break** (only when 2 candidates, only for `hidden_mechanism`): count timeline markers in `narrative_setup` matching `(Q[1-4]/?\d{0,4}|năm \d{4}|tháng \d|cuối năm|\d{4})`. ≥3 → narrative; else → qa.
3. **Length downgrade**: IF `len(data_trail_preview) ≤ 2` AND `key_metric_count ≤ 1` AND picked starts with `standard_` → downgrade to `flash_qa`. Rationale: shallow data → don't pad.
4. **Tone bias**: `pct_change_today ≤ -3%` → `acknowledge_market_red`; `≥ +3%` → `acknowledge_market_green`; else → `neutral`.
5. **Length target** from registry: flash=130, qa=250, listicle/narrative=300.

## Output schema (strict)

```json
{
  "brief_enriched": { /* original brief + 4 new fields per option */ },
  "format_director_log": {
    "format_picks": [{"option_idx": int, "format_id": str, "format_reason": str, "tone_bias": str, "length_target": int}],
    "candidates_considered_per_option": [{"option_idx": int, "category": str, "candidates": [str]}],
    "variety_check": {"recent_3_articles_same_ticker_formats": [str], "current_pick_diversity_warning": bool}
  }
}
```

Each `format_pick.format_id` MUST ∈ {flash_qa, standard_qa, standard_listicle, standard_narrative}. Validation enforced at persist by `lib.pipeline_db.validate_pipeline_step('step_3_5_format_director', ...)`.

## Anti-hallucination guards

- `format_reason` follows template: `"Category={X} → candidates={Y}. Picked={Z}. {extra}"`. No free-form essay.
- Fallback `flash_qa` when confused — don't try to invent.
- No new format ideas — `format_registry.yaml` is closed catalog. Add format → edit yaml + restart pipeline.

## Variety guard

Query 3 most-recent articles via:

```python
db.recent_generated_news(ticker, limit=3)
```

If all 3 same `format_id_used` (read from each `pipeline_log.step_4_master.format_id_used`) AND current pick same → emit `current_pick_diversity_warning: true` + note in `format_reason`. Do NOT change pick — data justifies pick wins.

## Edge cases

- `category` not in 5 known → fallback `flash_qa`.
- `data_trail_preview` missing or empty → treat as `n_sources=0`, may downgrade.
- `market_data` null (Step 1.5 soft-failed) → `tone_bias: neutral` always.
- `narrative_setup` empty → 0 timeline markers → hidden_mechanism picks qa.
```

- [ ] **Step 3: Commit**

```bash
mkdir -p .claude/skills/finpath-newsroom-format-director
# (Write tool already created file; just verify)
git add .claude/skills/finpath-newsroom-format-director/SKILL.md
git commit -m "feat(skill): finpath-newsroom-format-director V5.0 SKILL.md (Phase 2.3)

Compact reference loaded via Skill: finpath-newsroom-format-director.
Covers 4-format catalog, 5-step flow, anti-hallu guards, variety check.
"
```

---

### Task 11: Pipeline orchestrator — integrate Step 1.5 + Step 3.5

**Files:**
- Modify: `.claude/agents/newsroom-pipeline.md`

- [ ] **Step 1: Read current pipeline.md to locate insertion points**

```bash
grep -n "### Step " .claude/agents/newsroom-pipeline.md
```

Insertion points:
- After "### Step 1 — Crawler" section → add "### Step 1.5 — Market Snapshot"
- After "### Step 3 — Story Editor" section → add "### Step 3.5 — Format Director"

- [ ] **Step 2: Add Step 1.5 section after Step 1**

Insert after the Step 1 Crawler closing (typically followed by `### Step 2`):

```markdown
### Step 1.5 — Market Snapshot (Python self-execute)

Fetch ticker quote (price + pct_change) via Finpath API. Soft fetch — failure → None, do NOT block pipeline.

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.stages.run_market_snapshot import fetch_market_snapshot
snap = fetch_market_snapshot('<TICKER>')
print(json.dumps(snap.to_dict() if snap else None, ensure_ascii=False))
" > /tmp/market_snapshot.json
```

Result is passed downstream to Format Director via brief (`brief.ticker_market_data` field).

**Observability**: log Step 1.5 to each article in batch:

```python
db.log_pipeline_step(article_id, "step_1_5_market_snapshot", {
    "model": "python",
    "started_at": started_at,
    "duration_ms": duration_ms,
    "tokens": None,
    "result": <snapshot dict or None>,
    "soft_failed": <True if None>,
})
```

If snapshot None → log `soft_failed: true` + `result: null`. Pipeline continues.
```

- [ ] **Step 3: Add Step 3.5 section after Step 3**

Insert after Step 3 Story Editor (typically before `### Step 4`):

```markdown
### Step 3.5 — Format Director (Task dispatch)

Enrich Story Editor brief with format_id + tone_bias + length_target per deep_question_option.

**Dispatch via Task tool** (do NOT inline self-execute — schema validation will fail):

```
Task: newsroom-format-director
prompt: <JSON input from §"Input" section of newsroom-format-director.md>
```

Input includes:
- `brief` from Story Editor (with `stance` field per option, V5.0)
- `ticker_market_data` from Step 1.5 (may be null)

Output: `brief_enriched` (input + 4 new fields per option) + `format_director_log`.

**Pre-Master**: replace original brief with enriched version. Master receives brief V5.0 with format pre-picked.

**Observability**: log step_3_5_format_director to each article in batch:

```python
db.log_pipeline_step(article_id, "step_3_5_format_director", {
    "model": "claude-sonnet-4-6",
    "started_at": started_at,
    "duration_ms": duration_ms,
    "tokens": parse_task_usage(task_return),
    "format_picks": format_picks,                       # required, non-empty
    "candidates_considered_per_option": [...],
    "variety_check": {...},
})
```

**Schema validation**: `step_3_5_format_director.format_picks` MUST be non-empty list. Validation in `lib.pipeline_db.validate_pipeline_step` enforces.

**HARD RULE — no inline self-execute**: orchestrator MUST dispatch Task. Inline pick = silently wrong format → Master writes wrong pattern → 9-gate reject loop. If subagent crashes, STOP pipeline + report.
```

- [ ] **Step 4: Update Step 4 Master section to mention format input**

Find existing Step 4 section, locate the "Input" subsection, and update to reflect new field:

Inside the existing `### Step 4 — Master sector` section, find the input description and add:

```markdown
**V5.0 NEW**: brief includes `format_id` + `tone_bias` + `length_target` per option (from Format Director step 3.5). Master picks option as before, then applies the picked option's `format_id` pattern from `data/format_registry.yaml`. Persists `step_4_master.format_id_used = <final_format_id>` (post-escalation).
```

- [ ] **Step 5: Update HARD RULE section to cover Step 3.5**

Find existing HARD RULE block at top of pipeline.md, extend:

Change `Steps 2-5` references to `Steps 2-5, 3.5`. Update example list:
- `Step 2 (newsroom-editor)`
- `Step 3 (newsroom-story-editor)`
- `Step 3.5 (newsroom-format-director)` ← NEW
- `Step 4 (newsroom-master-{bank,ck,bds})`
- `Step 5 (newsroom-skeptic)`

Acceptable shortcuts list extend: `Step 1.5 (Market Snapshot)` is mechanical Python → orchestrator self-runs.

- [ ] **Step 6: Commit**

```bash
git add .claude/agents/newsroom-pipeline.md
git commit -m "feat(orchestrator): integrate Step 1.5 + Step 3.5 in pipeline V5.0 (Phase 2.4)

Pipeline V4.0 (9 steps) → V5.0 (11 steps):
- Step 1.5 Market Snapshot: Python self-execute, soft fetch
- Step 3.5 Format Director: Task dispatch, hard rule no inline

Step 4 Master input contract updated for format_id field.
HARD RULE extended to cover Step 3.5 no-inline-execute.
"
```

---

## Phase 3 — Story Editor + Master + Skeptic updates (Tasks 12-17)

### Task 12: Story Editor brief V5.0 schema — add `stance` field

**Files:**
- Modify: `.claude/agents/newsroom-story-editor.md` (brief schema + Pass 2 question)
- Modify: `.claude/skills/finpath-newsroom-story-editor/SKILL.md` (if exists)

- [ ] **Step 1: Add `stance` as required field in brief JSON schema**

Locate the brief JSON example in `.claude/agents/newsroom-story-editor.md` (around line 80+). Update to V5.0:

```json
{
  "row_id": "<crawl_log row>",
  "ticker": "VCB",
  "sector": "Bank",
  "why_chosen_narrative": "...",
  "angle_label": "...",
  "angle_narrative": "...",
  "source_rationale": "...",
  "deep_question_options": [
    {
      "question": "...",
      "category": "paradox|why_now|hidden_mechanism|comparison_deep|early_signal",
      "stance": "bullish|bearish|divergent",                          // V5.0 NEW REQUIRED
      "narrative_setup": "...",                                       // V5.0 NEW — Master fetches from this
      "data_trail_preview": [{"source": "Finpath_API/...", "fetched": "..."}, ...],  // V5.0 NEW
      "key_metric_count": 3,                                          // V5.0 NEW — int, for length downgrade
      "pick_hint": "..."
    },
    ...
  ],
  "insight_hypothesis": "...",
  "memory_check": {...}
}
```

- [ ] **Step 2: Add Pass 2.5 step "Pick stance"**

Insert a new sub-step in Pass 2 (around 6 expert questions):

```markdown
### Pass 2.6 — Pick stance per option (V5.0 NEW)

For each `deep_question_option`, pick stance based on data + insight direction:
- **`bullish`**: tích cực, đáng giữ — when data + insight argue positive outcome
- **`bearish`**: tiêu cực, cảnh báo — when data + insight argue negative outcome
- **`divergent`**: phân hoá rõ — when data + insight argue 2 sides (e.g. comparison_deep showing winners + losers)

Stance is independent of market mood (V5 Contrarian rule). Pick what the DATA justifies — Master will write accordingly. Format Director picks tone_bias separately (mood-sync).

⚠️ If `category=divergent` is not picked by ≥1 of 2-3 options, flag the brief — Story Editor should consider whether comparison angle deserves divergent stance.
```

- [ ] **Step 3: Update output schema sample at end**

Find the "Output to caller" section, update to mention V5.0:

```markdown
## Output to caller

```json
{
  "schema_version": "1.3",          # V5.0 bump — adds stance + narrative_setup + data_trail_preview + key_metric_count per option
  "batch_id": "<funnel_batch_id>",
  ...
}
```
```

- [ ] **Step 4: Update Hard rules section**

Append to Hard rules list:
```markdown
- **V5.0 stance required** — every `deep_question_options[*]` MUST have `stance ∈ {bullish, bearish, divergent}`. Reject missing stance.
- **V5.0 data_trail_preview** — list at least 1 source so Format Director can apply length downgrade heuristic.
- **V5.0 key_metric_count** — count of key financial metrics in narrative_setup. 0-2+ acceptable.
```

- [ ] **Step 5: Commit**

```bash
git add .claude/agents/newsroom-story-editor.md
git commit -m "feat(story-editor): brief V5.0 schema — add stance + narrative_setup + data_trail_preview + key_metric_count per option (Phase 3.1)

Brief schema V4.0 → V5.0. Story Editor picks stance per option (bullish/bearish/divergent).
New Pass 2.6 covers stance assignment based on data direction, not market mood.

Schema version bumped 1.2 → 1.3.
"
```

---

### Task 13: Master Bank — format-aware article generation

**Files:**
- Modify: `.claude/agents/newsroom-master-bank.md`

Sections to update:
- Step 1: Validate brief V5.0 — check `stance` + `format_id` present
- Step 6.5: Master pick option (existing) — note format inherited from picked option
- Step 7: Apply format pattern from registry
- Step 8: Run `check_all_v5` (9 gates) instead of `check_all` (5 gates)
- Step 8.5: Format escalation (one-shot, length-only)
- Step 9: Persist with `format_id_used`

- [ ] **Step 1: Update brief validation in Step 1**

Find "### 1. Validate brief V4.0" section. Rename to V5.0 and add checks:

```markdown
### 1. Validate brief V5.0

- ticker in BANK_UNIVERSE (27 mã)
- brief có `deep_question_options` (array 2-3+)
- Mỗi option có:
  - `category` ∈ {paradox, why_now, hidden_mechanism, comparison_deep, early_signal}
  - `stance` ∈ {bullish, bearish, divergent}                  ← V5.0 NEW
  - `format_id` ∈ {flash_qa, standard_qa, standard_listicle, standard_narrative}  ← V5.0 NEW (from Format Director)
  - `format_reason`, `tone_bias`, `length_target`             ← V5.0 NEW

Fail → `master_decision: reject_no_data`, `master_note: invalid_brief_schema_v5`.
```

- [ ] **Step 2: Add Step 6.5 format awareness note**

After existing Step 6.5 (Master picks 1 option), add:

```markdown
**V5.0 format inheritance**: Picked option's `format_id` becomes the article's format. Apply pattern from `data/format_registry.yaml` (see Step 7).
```

- [ ] **Step 3: Replace Step 8 gate check (5 → 9 gates)**

Find existing Step 8 with `check_all`. Replace:

```markdown
### 8. Quality gates V5.0 (9 gates via check_all_v5)

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.quality_gates import check_all_v5
body = '''<MASTER BODY HERE>'''
title = '''<MASTER TITLE HERE>'''
format_id = '<FORMAT_ID FROM OPTION>'
stance = '<STANCE FROM OPTION>'
results = check_all_v5(body, title, format_id=format_id, stance=stance)
print(json.dumps(results, ensure_ascii=False, indent=2))
"
```

9 gates: 6 universal (no_english_jargon, no_metadata_leak, no_hedging, verdict_line, stance_consistency, sentence_density) + 3 per-format (word_count, body_pattern, title_pattern).

ANY gate fails → rewrite + re-check. Max 2 retry per format. Then escalate (Step 8.5).
```

- [ ] **Step 4: Add Step 8.5 escalation rule**

After Step 8, before Step 9 persist:

```markdown
### 8.5 — Format escalation (one-shot, length-only) — V5.0 NEW

After 2 failed retries on Gate 2 word_count (too long for flash_qa or too short for standard_*), check if data depth justifies escalation:

- IF format_id=flash_qa AND `len(actual data_trail) ≥ 3` AND `actual key_metric_count ≥ 2` AND article word_count too long for flash_qa range:
  - Escalate `flash_qa → standard_qa` (one-shot only)
  - Log `format_escalation: {from: "flash_qa", to: "standard_qa", reason: "data_trail=N sources, key_metrics=M"}` in step_4_master
  - Re-run check_all_v5 with new format_id
  - If still fails after escalation → master_decision: `reject_no_format_fit` + master_note explaining

- ELSE (any other format mismatch) → **NO cross-tier swap**. Format Director's structural decision is final. Reject + rewrite within original format.
```

- [ ] **Step 5: Update Step 9 persist to include `format_id_used`**

Find existing Step 9 persist call. Add to payload:

```python
db.log_pipeline_step(article_id, "step_4_master", {
    # ... existing fields ...
    "format_id_used": <final_format_id>,       # V5.0 REQUIRED — post-escalation
    "format_escalation_reason": <str or None>,  # V5.0 optional
})
```

⚠️ Validation: pipeline_log[step_4_master] in V5.0 row REQUIRES `format_id_used` non-empty string. Missing → ValueError.

- [ ] **Step 6: Add bullet pool guidance section**

After existing "Hard rule" section, add:

```markdown
## Bullet pool — đa dạng bullet style (V5.0)

4 loại bullet technique — sử dụng ≥2 loại khác nhau trong 1 bài (chỉ áp dụng cho format có bullets):

| Type | Trigger phrase | Example |
|---|---|---|
| **contrast** | nhưng, ngược lại | "**Big4 +28%, tư nhân -5%** — nhưng 2 hướng cùng có lý." |
| **causation** | vì vậy, dẫn đến | "**CASA giảm xuống 35%** — vì vậy biên lãi vay 2026 sẽ phải xuống theo." |
| **warning** | coi chừng, lưu ý | "**Nợ xấu nhóm 2 vượt 2,4%** — coi chừng pattern 2022 lặp lại." |
| **revelation** | thật ra, kỳ thực | "**Lãi 3.842 tỷ trông đẹp** — thật ra chỉ FE Credit kéo, core bank đi ngang." |

Bullet style không phải hard gate (soft guidance). Skeptic `lifeless_writing` angle catches monotony.
```

- [ ] **Step 7: Commit**

```bash
git add .claude/agents/newsroom-master-bank.md
git commit -m "feat(master-bank): format-aware article generation V5.0 (Phase 3.2)

- Brief V5.0 validation: stance + format_id + tone_bias + length_target required
- Step 8: check_all_v5 (9 gates) replaces check_all (5 gates)
- Step 8.5: format escalation rule (flash_qa → standard_qa one-shot, length-only)
- Step 9: persist format_id_used + optional format_escalation_reason
- Bullet pool guidance: 4 technique types (contrast/causation/warning/revelation)

Master agent inherits format from Story Editor + Format Director's pick.
"
```

---

### Task 14: Master CK — same updates as Master Bank

**Files:**
- Modify: `.claude/agents/newsroom-master-ck.md`

Apply IDENTICAL changes as Task 13 (Master Bank), but reference CK_UNIVERSE (30 mã) instead of BANK_UNIVERSE.

- [ ] **Step 1: Apply Steps 1-6 from Task 13 to newsroom-master-ck.md**

Find equivalent sections in master-ck.md. Apply same diffs as Task 13. Differences:
- BANK_UNIVERSE → CK_UNIVERSE (30 mã)
- Sector-specific KB (kb/ck/ vs kb/bank/) — already in existing prose
- Same 9 gates + same escalation rule

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/newsroom-master-ck.md
git commit -m "feat(master-ck): format-aware V5.0 — mirror Task 13 changes (Phase 3.3)

Identical pattern to newsroom-master-bank (Phase 3.2). CK_UNIVERSE 30 mã.
"
```

---

### Task 15: Master BĐS — same updates

**Files:**
- Modify: `.claude/agents/newsroom-master-bds.md`

- [ ] **Step 1: Apply Steps 1-6 from Task 13 to newsroom-master-bds.md**

Same pattern. BDS_UNIVERSE 4 mã (VHM, NVL, KDH, DXG).

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/newsroom-master-bds.md
git commit -m "feat(master-bds): format-aware V5.0 — mirror Task 13 changes (Phase 3.4)

Identical pattern to newsroom-master-bank. BDS_UNIVERSE 4 mã.
"
```

---

### Task 16: Skeptic — 9 critique angles + format-aware

**Files:**
- Modify: `.claude/agents/newsroom-skeptic.md`

- [ ] **Step 1: Locate existing 6-angle section**

```bash
grep -n "Critique angle\|critique angle\|6 angle\|angle =" .claude/agents/newsroom-skeptic.md
```

- [ ] **Step 2: Update angle list 6 → 9**

Find the "Pick 1 of 6 angle" section. Update to:

```markdown
## 9 Critique Angles V5.0

Pass 1 form fresh impression (read body ONLY, NOT insight). Pass 2 compare. Pick 1 of 9:

| Angle | When to use | Notes |
|---|---|---|
| `data_skepticism` | Master claim số nhưng context unclear | V4.0 existing |
| `historical_analog` | Master không reference lịch sử + có analog quan trọng | V4.0 |
| `alt_interpretation` | Master read data 1 cách, có cách read ngược hợp lý | V4.0 |
| `risk_highlight` | Master không raise risk Master nên raise | V4.0 |
| `insight_wrong` | Insight CONFLICT với data thực tế — Story Editor pick sai | V4.0 |
| `execution_unfaithful` | Insight đúng nhưng bài execute lệch | V4.0 |
| `lifeless_writing` | Body có ≥2 fluff sentence (sentence_density borderline) | **V5.0 NEW** — Layer 2 cho Gate 9 |
| `verdict_weak` | Verdict pass regex nhưng mâu thuẫn nội tại / hedging trá hình | **V5.0 NEW** — Layer 2 cho Gate 7 |
| `stance_drift` | Brief.stance vs body tone subtly off (passes Layer 1 ratio test) | **V5.0 NEW** — Layer 2 cho Gate 8 |

3 critique gần nhất KHÔNG dùng cùng angle 3 lần liên tiếp.
```

- [ ] **Step 3: Add format-aware critique adjustments**

Add new section before "Pick 1 of 9":

```markdown
## Format-aware critique (V5.0)

Read `step_4_master.format_id_used` từ DB before critiquing. Adjust expectations:

- **`flash_qa`**: KHÔNG critique "thiếu bullet" — flash là paragraph thuần.
- **`standard_narrative`**: KHÔNG critique "ít bullet" — narrative ít cố ý (0-2 highlights).
- **`standard_listicle`**: KHÔNG critique "thiếu opening dài" — listicle là dense bullets.
- **`standard_qa`**: pattern V4.0 baseline.

Format không phải critique target. Voice + insight + data là critique target.
```

- [ ] **Step 4: Update output schema**

Find Skeptic output JSON. Update `angle` allowed values:

```json
{
  "angle": "data_skepticism|historical_analog|alt_interpretation|risk_highlight|insight_wrong|execution_unfaithful|lifeless_writing|verdict_weak|stance_drift",
  ...
}
```

- [ ] **Step 5: Update hard rules**

```markdown
- **V5.0 angle set**: 9 angles. `lifeless_writing` / `verdict_weak` / `stance_drift` are Layer 2 enforcement for code-level gates 7/8/9 — flag subtle issues that pass regex.
```

- [ ] **Step 6: Commit**

```bash
git add .claude/agents/newsroom-skeptic.md
git commit -m "feat(skeptic): 9 critique angles + format-aware V5.0 (Phase 3.5)

3 new angles:
- lifeless_writing (Layer 2 sentence_density)
- verdict_weak (Layer 2 verdict_line)
- stance_drift (Layer 2 stance_consistency)

Critique expectations adjusted per format_id_used from step_4_master.
"
```

---

### Task 17: Pipeline orchestrator — Step 5 Skeptic input contract

**Files:**
- Modify: `.claude/agents/newsroom-pipeline.md` (Step 5 section)

- [ ] **Step 1: Update Step 5 input to include format context**

Find existing Step 5 Skeptic section. Add:

```markdown
**V5.0 NEW input**: pass `format_id_used` from `step_4_master.format_id_used` to Skeptic so it can adjust critique expectations per format.
```

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/newsroom-pipeline.md
git commit -m "feat(orchestrator): Step 5 input includes format_id_used (Phase 3.6)

Skeptic receives format context for format-aware critique.
"
```

---

## Phase 4 — Frontend + render (Tasks 18-20)

### Task 18: render_compare_feed — format pick output in right column

**Files:**
- Modify: `lib/render_compare_feed.py`
- Test: `tests/test_render_compare_feed.py`

- [ ] **Step 1: Write failing test**

Append to `tests/test_render_compare_feed.py`:

```python
def test_render_includes_format_director_section(tmp_path):
    """V5.0: right column markdown includes format pick reasoning."""
    from lib.render_compare_feed import build_right_column

    article = {
        "article_id": "a1",
        "ticker": "VCB",
        "title": "Vì sao to nhất lại đi chậm?",
        "body": "...",
        "pipeline_version": "V5.0",
        "pipeline_log": '{"step_3_5_format_director": {"format_picks": [{"option_idx": 0, "format_id": "standard_qa", "format_reason": "Category=paradox → candidates=[standard_qa]. Picked=standard_qa.", "tone_bias": "neutral", "length_target": 250}], "candidates_considered_per_option": [{"option_idx": 0, "category": "paradox", "candidates": ["standard_qa"]}], "variety_check": {"recent_3_articles_same_ticker_formats": ["standard_qa", "standard_listicle", "standard_qa"], "current_pick_diversity_warning": false}, "model": "claude-sonnet-4-6", "duration_ms": 8400, "tokens": 1240}, "step_4_master": {"chosen_question_idx": 0, "chosen_pick_reason": "test", "skip_reasons": {}, "data_trail": [{"source": "x", "fetched": "y"}], "format_id_used": "standard_qa"}}',
    }
    anchor_row = {"row_id": "r1", "ticker": "VCB"}
    funnel_rows = []

    rc = build_right_column(article, anchor_row, funnel_rows)
    assert "format_director" in rc
    assert rc["format_director"]["format_id"] == "standard_qa"
    assert rc["format_director"]["format_reason"]
    assert rc["format_director"]["tone_bias"] == "neutral"


def test_render_v4_article_no_format_director_section(tmp_path):
    """V3.6/V4.0 legacy articles: format_director field absent (graceful)."""
    from lib.render_compare_feed import build_right_column
    article = {
        "article_id": "a1",
        "ticker": "VCB",
        "title": "Test",
        "body": "...",
        "pipeline_version": "V4.0",
        "pipeline_log": '{"step_4_master": {"chosen_question_idx": 0, "chosen_pick_reason": "x", "skip_reasons": {}, "data_trail": [{"source": "x", "fetched": "y"}]}}',  # NO format_id_used (V4.0)
    }
    rc = build_right_column(article, {"row_id": "r1", "ticker": "VCB"}, [])
    assert rc.get("format_director") in (None, {})  # absent or empty
```

- [ ] **Step 2: Run test — fail**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_render_compare_feed.py::test_render_includes_format_director_section -v
```
Expected: FAIL — function doesn't expose format_director.

- [ ] **Step 3: Modify `lib/render_compare_feed.py:build_right_column`**

Locate function and add new section after pipeline_log parsing:

```python
def build_right_column(article: dict, anchor_row: dict, funnel_rows: list[dict]) -> dict:
    # ... existing code that parses pipeline_log ...
    pipeline_log_raw = article.get("pipeline_log", "{}")
    try:
        pipeline_log = json.loads(pipeline_log_raw) if isinstance(pipeline_log_raw, str) else (pipeline_log_raw or {})
    except json.JSONDecodeError:
        pipeline_log = {}

    # V5.0 — Format Director section (graceful degrade if missing)
    step_3_5 = pipeline_log.get("step_3_5_format_director")
    format_director = None
    if step_3_5 and isinstance(step_3_5, dict):
        picks = step_3_5.get("format_picks") or []
        # Use first pick's format_id (chosen by Master per chosen_question_idx)
        chosen_idx = pipeline_log.get("step_4_master", {}).get("chosen_question_idx", 0)
        pick = next((p for p in picks if p.get("option_idx") == chosen_idx), picks[0] if picks else None)
        if pick:
            format_director = {
                "format_id": pick.get("format_id"),
                "format_reason": pick.get("format_reason"),
                "tone_bias": pick.get("tone_bias", "neutral"),
                "length_target": pick.get("length_target"),
                "variety_check": step_3_5.get("variety_check", {}),
            }

    # Existing right column construction continues here
    rc = {
        # ... existing fields ...
        "format_director": format_director,  # V5.0 NEW — None for V3.6/V4.0 articles
    }
    return rc
```

- [ ] **Step 4: Update `render_article_md_v4` to emit format_director in frontmatter**

Find function `render_article_md_v4`. Add `format_director` field to yaml dump:

```python
def render_article_md_v4(article: dict, anchor_row: dict, funnel_rows: list[dict]) -> str:
    rc = build_right_column(article, anchor_row, funnel_rows)
    # ... existing frontmatter assembly ...
    frontmatter["format_director"] = rc.get("format_director")  # may be None for V4.0
    # ... emit yaml + body ...
```

- [ ] **Step 5: Run tests — verify pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_render_compare_feed.py -v
```
Expected: all green.

- [ ] **Step 6: Commit**

```bash
git add lib/render_compare_feed.py tests/test_render_compare_feed.py
git commit -m "feat(render): emit format_director section in right column V5.0 (Phase 4.1)

build_right_column extracts step_3_5_format_director from pipeline_log.
Graceful degrade for V3.6/V4.0 articles (format_director: None).
Frontmatter includes format_director field for viewer consumption.
"
```

---

### Task 19: Frontend types + FormatPickPanel component

**Files:**
- Modify: `web/src/types.ts`
- Create: `web/src/components/FormatPickPanel.tsx`
- Modify: `web/src/components/RightColumn.tsx` — render new panel

- [ ] **Step 1: Add types to `web/src/types.ts`**

Append to file:

```typescript
// V5.0 — Format Director output
export interface FormatPick {
  option_idx: number;
  format_id: 'flash_qa' | 'standard_qa' | 'standard_listicle' | 'standard_narrative';
  format_reason: string;
  tone_bias: 'neutral' | 'acknowledge_market_red' | 'acknowledge_market_green';
  length_target: number;
}

export interface VarietyCheck {
  recent_3_articles_same_ticker_formats?: string[];
  current_pick_diversity_warning?: boolean;
}

export interface FormatDirectorData {
  format_id: string;
  format_reason: string;
  tone_bias: string;
  length_target: number;
  variety_check?: VarietyCheck;
}

// Extend ArticleMeta
export interface ArticleMeta {
  // ... existing fields ...
  format_director?: FormatDirectorData | null;  // V5.0 — null for V3.6/V4.0 legacy
}
```

(Note: actual edit appends `format_director?` to existing `ArticleMeta` interface — find existing interface and inject the new line.)

- [ ] **Step 2: Create `web/src/components/FormatPickPanel.tsx`**

```tsx
import type { FormatDirectorData } from '../types';

const FORMAT_LABELS: Record<string, { label: string; color: string }> = {
  flash_qa: { label: 'Flash Q&A', color: 'bg-blue-100 text-blue-700' },
  standard_qa: { label: 'Standard Q&A', color: 'bg-green-100 text-green-700' },
  standard_listicle: { label: 'Listicle', color: 'bg-purple-100 text-purple-700' },
  standard_narrative: { label: 'Narrative', color: 'bg-orange-100 text-orange-700' },
};

const TONE_LABELS: Record<string, string> = {
  neutral: 'Trung lập',
  acknowledge_market_red: 'Phiên đỏ',
  acknowledge_market_green: 'Phiên xanh',
};

export function FormatPickPanel({ data }: { data: FormatDirectorData | null | undefined }) {
  if (!data) {
    return null; // Graceful degrade — legacy V3.6/V4.0 articles
  }
  const label = FORMAT_LABELS[data.format_id] || { label: data.format_id, color: 'bg-gray-100 text-gray-700' };
  const toneLabel = TONE_LABELS[data.tone_bias] || data.tone_bias;
  const varietyWarn = data.variety_check?.current_pick_diversity_warning;

  return (
    <details className="mb-4">
      <summary className="section-pill cursor-pointer">
        Format chọn
      </summary>
      <div className="mt-3 text-sm pl-3 border-l-2 border-fg-4/40">
        <div className="mb-2">
          <span className={`inline-block rounded px-2 py-1 text-xs font-semibold ${label.color}`}>
            {label.label}
          </span>
          <span className="ml-2 text-fg-2">
            Mục tiêu {data.length_target} từ · Tone: {toneLabel}
          </span>
        </div>
        <div className="text-fg-2 mb-2">
          <em>Lý do</em>: {data.format_reason}
        </div>
        {varietyWarn && data.variety_check?.recent_3_articles_same_ticker_formats && (
          <div className="text-rec text-xs italic">
            ⚠️ Cảnh báo đa dạng: 3 bài gần đây toàn dùng cùng format này.
          </div>
        )}
      </div>
    </details>
  );
}
```

- [ ] **Step 3: Integrate into `RightColumn.tsx`**

```bash
grep -n "import\|export" web/src/components/RightColumn.tsx | head -20
```

Find the existing RightColumn component. Add import + render:

```tsx
// Add to imports
import { FormatPickPanel } from './FormatPickPanel';

// Inside render, place FormatPickPanel near the top (after Source / Why Chosen):
<FormatPickPanel data={meta.format_director} />
```

(Exact placement: per existing right-column section ordering, place after `WhyChosen` block and before `AngleNarrative`.)

- [ ] **Step 4: Type check frontend**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit
```

Expected: no type errors.

- [ ] **Step 5: Visual smoke test**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npm run dev
```

Open `http://localhost:5176/feed`. Observe:
- Legacy V4.0 articles: no FormatPickPanel (graceful degrade)
- (After E2E run in Phase 6) New V5.0 articles: FormatPickPanel visible with format label + reason

- [ ] **Step 6: Commit**

```bash
git add web/src/types.ts web/src/components/FormatPickPanel.tsx web/src/components/RightColumn.tsx
git commit -m "feat(viewer): FormatPickPanel component V5.0 (Phase 4.2)

Renders format_director from step_3_5 in right column. Per-format
color badge + format_reason + tone_bias label + variety_check warning.
Graceful degrade (returns null) for V3.6/V4.0 articles without
step_3_5_format_director field.
"
```

---

### Task 20: ArticleLoader — surface format_director from frontmatter

**Files:**
- Modify: `web/src/lib/parseArticle.ts` (or wherever frontmatter parser lives)

- [ ] **Step 1: Locate frontmatter parser**

```bash
grep -rn "format_director\|deep_question_options\|frontmatter" web/src/lib/ | head -10
```

- [ ] **Step 2: Add format_director extraction**

In the parser, surface `frontmatter.format_director` into the article meta object:

```typescript
const meta: ArticleMeta = {
  // ... existing fields ...
  format_director: frontmatter.format_director ?? null,
};
```

- [ ] **Step 3: Type check**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit
```

- [ ] **Step 4: Commit**

```bash
git add web/src/lib/parseArticle.ts
git commit -m "feat(viewer): surface format_director from frontmatter (Phase 4.3)

ArticleLoader extracts format_director field and passes to FormatPickPanel.
"
```

---

## Phase 5 — CLAUDE.md + V5.0 bump (Tasks 21-22)

### Task 21: CLAUDE.md content update

**Files:**
- Modify: `CLAUDE.md`

Sections to update:
- "## 5 Quality Gates V4.0" → "## 9 Quality Gates V5.0"
- "## Body pattern V4.0" → "## Body pattern V5.0 (per format)"
- "## 6 Critique Angles (Skeptic)" → "## 9 Critique Angles (Skeptic)"
- "## Hard rules cho Master + Skeptic" — extend with stance + verdict rules
- All "V4.0" references → "V5.0" except changelog/history

- [ ] **Step 1: Backup current CLAUDE.md**

```bash
cp CLAUDE.md /tmp/CLAUDE.md.v4-backup
```

- [ ] **Step 2: Update "5 Quality Gates V4.0" section**

Find existing section. Replace title + content:

```markdown
## 9 Quality Gates V5.0 (HARD CAP cho bài Master)

Bài fail 1/9 gate → tự reject + rewrite, KHÔNG persist:

### Universal (6 — áp dụng tất cả 4 format)
1. **no_english_jargon** — 0% từ tiếng Anh trong content (giữ exception: tên riêng + Pipeline log internal).
2. **no_metadata_leak** — KHÔNG `strategic-shift` / `risk_highlight` / `insight_type` / `Critique angle` / 5-category enum / `format_id` enum trong bài đọc.
3. **no_hedging (NEW V5.0)** — Reject: "có thể", "tùy thuộc", "vẫn chờ", "khả năng cao", "đáng theo dõi", "nhiều khả năng", "chưa rõ".
4. **verdict_line (NEW V5.0)** — Closing có 3 yếu tố: hướng + khung TG + action cho NĐT ĐANG cầm. Hybrid enforce: Layer 1 regex + Layer 2 Skeptic `verdict_weak` angle.
5. **stance_consistency (NEW V5.0)** — Master tone matches brief.stance (bullish/bearish/divergent). Layer 1 keyword ratio + Layer 2 Skeptic `stance_drift` angle.
6. **sentence_density (NEW V5.0)** — ≥80% câu trong body có ≥1 specific element (số / tên riêng / comparative / time marker / mechanism word / action verb). Layer 2 Skeptic `lifeless_writing` angle.

### Per-format (3)
7. **word_count** — Per format range: flash_qa 100-150 / standard_qa 200-300 / standard_listicle 250-350 / standard_narrative 250-350.
8. **body_pattern** — Per format structure: flash_qa paragraph only / standard_qa opening+bullets+closing / standard_listicle opening ngắn+dense bullets / standard_narrative flow paragraphs.
9. **title_pattern** — Per format: flash_qa MUST `?` / standard_qa `?` or `—` + tension word / standard_listicle numbered declarative / standard_narrative `—` em dash.
```

- [ ] **Step 3: Update "Body pattern" section**

Find existing "## Body pattern V4.0". Replace with per-format catalog:

```markdown
## Body pattern V5.0 (per format)

Format chọn bởi Format Director step 3.5 → Master apply pattern:

### flash_qa (100-150 từ)
```
[Title question with ?]

[Paragraph 100-150 từ trả lời thẳng. NO bullets. Closing là câu cuối.]
```

### standard_qa (200-300 từ) — pattern V4.0 hiện tại
```
[Title — question hoặc declarative paradox + tension word]
[Opening 30-80 từ — sự kiện + tension]
- **Bold highlight 1**: bullet ≥20 từ với mechanism reasoning
- **Bold highlight 2**: bullet ≥20 từ
- **Bold highlight 3**: bullet ≥20 từ
[Closing — 1 câu verdict (hướng + khung TG + holder action)]
```

### standard_listicle (250-350 từ)
```
[Title — numbered "5 dấu hiệu...", "3 lý do..."]
[Opening ngắn ≤30 từ]
- **Bullet 1 dense**: ≥25 từ
- **Bullet 2 dense**: ≥25 từ
- **Bullet 3 dense**: ≥25 từ
- **Bullet 4 dense**: ≥25 từ
- ... up to 7 bullets
[Closing ngắn 1 câu verdict]
```

### standard_narrative (250-350 từ)
```
[Title — declarative story với em dash "X — câu chuyện Y"]
[Opening ≥40 từ]
[Đoạn flow 2 — chuỗi nguyên nhân-kết quả]
[Đoạn flow 3 — kết luận flow]
[Bold highlight 0-2 paragraph nhấn]
[Closing verdict 2 câu]
```

Caveats compress vào closing hoặc inline. KHÔNG `## Cần để ý` section. KHÔNG `## Key takeaway`.
```

- [ ] **Step 4: Update "6 Critique Angles" → "9 Critique Angles"**

Find existing "## 6 Critique Angles (Skeptic)". Replace:

```markdown
## 9 Critique Angles (Skeptic)

Skeptic Pass 1 form FRESH impression (đọc body ONLY, KHÔNG xem insight) → Pass 2 compare. Pick 1 of 9:

| Angle | Khi nào dùng |
|---|---|
| `data_skepticism` | Master claim số nhưng context unclear |
| `historical_analog` | Master không reference lịch sử + có analog quan trọng |
| `alt_interpretation` | Master read data 1 cách, có cách read ngược hợp lý |
| `risk_highlight` | Master không raise risk Master nên raise |
| `insight_wrong` | Insight CONFLICT với data thực tế — Story Editor pick sai |
| `execution_unfaithful` | Insight đúng nhưng bài execute lệch |
| `lifeless_writing` (V5.0) | Body có ≥2 fluff sentence — Layer 2 Gate 9 |
| `verdict_weak` (V5.0) | Verdict pass regex nhưng mâu thuẫn nội tại — Layer 2 Gate 7 |
| `stance_drift` (V5.0) | Stance subtle drift even when keyword ratio passes — Layer 2 Gate 8 |

3 critique gần nhất KHÔNG dùng cùng angle 3 lần liên tiếp.
```

- [ ] **Step 5: Extend "Hard rules cho Master + Skeptic"**

Append to existing hard rules section:

```markdown
- **V5.0 stance bắt buộc** — Master MUST bám stance brief picked. Reject nếu tone ngược.
- **V5.0 verdict line** — Closing 3 yếu tố mandatory: hướng + khung TG + action holder. Không "Cần theo dõi" chung chung.
- **V5.0 format_id sticky** — Master nhận format từ Format Director (step 3.5). Chỉ escalate one-shot flash_qa → standard_qa khi data depth justifies.
- **V5.0 contrarian-OK** — Stance KHÔNG cần khớp mood ngày. Mã đỏ vẫn có thể bullish, mã xanh có thể bearish — khi data justify.
```

- [ ] **Step 6: V4.0 → V5.0 global rename**

```bash
# Visually inspect remaining V4.0 references
grep -n "V4.0" CLAUDE.md
```

Replace remaining "V4.0" references with "V5.0" (preserve historical references e.g. "V3.6 → V4.0 migration" left as-is).

- [ ] **Step 7: Verify CLAUDE.md still parses**

```bash
wc -l CLAUDE.md && head -50 CLAUDE.md
```

Sanity check.

- [ ] **Step 8: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude.md): V4.0 → V5.0 — 9 gates + 9 angles + per-format body patterns (Phase 5.1)

- '5 Quality Gates V4.0' → '9 Quality Gates V5.0' (6 universal + 3 per-format)
- 'Body pattern V4.0' → 'Body pattern V5.0 (per format)' covering 4 formats
- '6 Critique Angles' → '9 Critique Angles' (+ lifeless_writing, verdict_weak, stance_drift)
- 'Hard rules cho Master + Skeptic' extended with V5.0 stance + verdict + format_id rules
- All non-historical 'V4.0' → 'V5.0'
"
```

---

### Task 22: Pipeline version bump in code — V4.0 → V5.0 frontmatter default

**Files:**
- Modify: `lib/render_compare_feed.py` — find `pipeline_version` default in frontmatter generation

- [ ] **Step 1: Locate pipeline_version reference**

```bash
grep -n "pipeline_version\|V4.0\|V5.0" lib/render_compare_feed.py
```

- [ ] **Step 2: Update default**

In `render_article_md_v4` (or equivalent), find:
```python
frontmatter["pipeline_version"] = article.get("pipeline_version") or "V4.0"
```

Replace with:
```python
frontmatter["pipeline_version"] = article.get("pipeline_version") or "V5.0"
```

- [ ] **Step 3: Run render tests — verify no regression**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_render_compare_feed.py -v
```

- [ ] **Step 4: Commit**

```bash
git add lib/render_compare_feed.py
git commit -m "chore(render): bump pipeline_version frontmatter default V4.0 → V5.0 (Phase 5.2)

V5.0 articles emit pipeline_version=V5.0 in frontmatter; viewer
uses this to gate FormatPickPanel render (legacy V4.0 articles
preserve their frontmatter value).
"
```

---

## Phase 6 — Verification (Tasks 23-24)

### Task 23: E2E run /tin for 1 sample per sector

Run full pipeline for one Bank + one CK + one BĐS ticker. Verify all 11 steps execute, format diversity achieved, gates pass.

**Files:**
- Run: `/tin VCB` (Bank)
- Run: `/tin SSI` (CK)
- Run: `/tin VHM` (BĐS)

- [ ] **Step 1: Start dev server (visual check baseline)**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npm run dev &
# Wait for "ready in X ms" line in stdout, browser to http://localhost:5176/feed
```

Note current article count in feed.

- [ ] **Step 2: Run `/tin VCB`**

Trigger pipeline. Observe:
- Step 1.5 Market Snapshot log entry (soft fetch attempt)
- Step 3.5 Format Director Task dispatch (Sonnet model in pipeline_log)
- Step 4 Master uses format from brief
- Step 5 Skeptic with format-aware adjustments
- New article appears in feed with FormatPickPanel visible

- [ ] **Step 3: Verify pipeline_log persisted correctly**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
row = db.conn.execute(
    \"SELECT article_id, pipeline_version, pipeline_log FROM generated_news WHERE ticker='VCB' ORDER BY published_at DESC LIMIT 1\"
).fetchone()
log = json.loads(row['pipeline_log'])
print('pipeline_version:', row['pipeline_version'])
print('step_1_5_market_snapshot:', 'present' if 'step_1_5_market_snapshot' in log else 'MISSING')
print('step_3_5_format_director:', 'present' if 'step_3_5_format_director' in log else 'MISSING')
if 'step_3_5_format_director' in log:
    print('  format_picks count:', len(log['step_3_5_format_director'].get('format_picks', [])))
    print('  model:', log['step_3_5_format_director'].get('model'))
print('step_4_master.format_id_used:', log.get('step_4_master', {}).get('format_id_used', 'MISSING'))
db.close()
"
```

Expected:
- `pipeline_version: V5.0`
- `step_3_5_format_director: present` with `format_picks count` ≥1, `model: claude-sonnet-4-6`
- `step_4_master.format_id_used` ∈ 4 valid IDs

- [ ] **Step 4: Repeat for SSI + VHM**

Same checks for CK + BĐS tickers.

- [ ] **Step 5: Variety check across 3 articles**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
rows = db.conn.execute(
    \"SELECT ticker, pipeline_log FROM generated_news WHERE pipeline_version='V5.0' ORDER BY published_at DESC LIMIT 9\"  # 3 sectors × ~3 articles
).fetchall()
from collections import Counter
fmts = [json.loads(r['pipeline_log']).get('step_4_master', {}).get('format_id_used') for r in rows]
print(Counter(fmts))
db.close()
"
```

Expected: ≥2 different format_ids represented (not all standard_qa).

- [ ] **Step 6: Commit verification log**

```bash
# Save verification output for record
git log --oneline -10 > /tmp/verification.log
# Add as memo to repo if useful, else just note pass/fail in task tracker
```

- [ ] **Step 7: Document any failures**

If gates fail / Master gets stuck / format_id missing → debug + fix individual task before marking Task 23 complete. Common issues:
- Format Director agent prompt has typos → fix agent .md
- check_all_v5 false positives (regex too strict) → tune in lib/quality_gates.py
- Variety check bash script syntax error → fix in agent .md

- [ ] **Step 8: Commit any fixes**

```bash
git add <fixed files>
git commit -m "fix(<scope>): <issue> caught in E2E verification (Phase 6.1)"
```

---

### Task 24: Visual verification + final commit

**Files:**
- None (visual only)

- [ ] **Step 1: Compare V4.0 vs V5.0 articles side-by-side in viewer**

Open both:
- `http://localhost:5176/feed` — list view
- Click into 1 V4.0 legacy article — should NOT show FormatPickPanel (graceful degrade)
- Click into 1 new V5.0 article — should show FormatPickPanel with format badge + reason + tone

- [ ] **Step 2: Verify format diversity in new articles**

Check that 3 articles run in Task 23 don't all have the same format. Visual badge colors should differ.

- [ ] **Step 3: Verify Voice Layer applied**

Read closing line of each new article. Should match V3 verdict format:
- Direction word (tích cực/tiêu cực/cảnh báo)
- Timeframe (X tháng / Q? / ngắn-trung-dài hạn)
- Action for holder (NĐT đang cầm nên giữ/chờ/thận trọng)

If any article missing → check Skeptic angle `verdict_weak` flagged in step_5_skeptic.

- [ ] **Step 4: Type check + final test run**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/ -v 2>&1 | tail -30
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit
```

Expected: all green.

- [ ] **Step 5: Final summary commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git log --oneline 5b4ea7f..HEAD
```

Review commit list (should be ~24 commits from this plan + advisor patch). If clean, no final commit needed. If accumulated dirty files, commit them:

```bash
git add -A && git status  # review
git commit -m "chore: post-V5.0 cleanup (Phase 6.2)"
```

- [ ] **Step 6: Mark plan complete**

Plan execution complete. Push to origin/main when user approves.

---

## Self-review checklist (post-plan-writing)

### Spec coverage

- ✅ §5 Format Catalog → Tasks 1, 12-15 (registry + agent prose covers all 4)
- ✅ §6 Voice Layer 5 rules → Tasks 5, 12-15 (no_hedging gate, stance field, verdict_line gate, title pattern, V5 Contrarian in agent prose)
- ✅ §6 Mood-sync minimal → Task 2 (Step 1.5 Market Snapshot)
- ✅ §6 Bullet pool → Task 13-15 (prose section in Master agents)
- ✅ §7 9 gates → Tasks 5, 6 (extend quality_gates.py)
- ✅ §7.1 Hybrid enforcement Gates 7+8 → Tasks 5 (Layer 1) + 16 (Skeptic Layer 2 angles)
- ✅ §8 Format Director agent → Tasks 8, 9, 10, 11
- ✅ §9 Format Registry → Task 1
- ✅ §10 Brief V5.0 schema → Task 12 (Story Editor adds stance + narrative_setup + data_trail_preview + key_metric_count)
- ✅ §10.1 pipeline_version + migration → Tasks 3, 4
- ✅ §11 Master + escalation → Tasks 13-15
- ✅ §12 Skeptic 9 angles → Task 16
- ✅ §13 Pipeline observability → Tasks 7, 18, 19 (DB + render + viewer)
- ✅ §14 Pipeline version bump → Tasks 21, 22
- ✅ §15 File touch list — all 23 files addressed
- ✅ §16 Testing — TDD throughout
- ✅ §17 Rollout 6 phases → Tasks grouped by phase
- ✅ §18 Open questions — heuristics noted as tunable post-launch

### Placeholder scan

- No "TBD" / "implement later" placeholders in task steps.
- Task 2 has investigation step for Finpath quote endpoint — explicit step, not deferred.
- All code blocks complete (no `# ...` stubs).

### Type consistency

- `FormatPick` interface in types.ts matches `format_picks` payload in pipeline_db schema
- `FormatDirectorData` shape matches `build_right_column` output
- `pick_format_for_option` return shape matches Format Director agent output
- `check_all_v5` signature `(body, title, format_id, stance)` consistent across Tasks 5, 6, 13-15
- `format_id_used` field consistently used in step_4_master across DB validation + agents + render

---

## Phase 6 — V5.1.2 SPLIT + stance + no-hedging redefine + em dash (Tasks 23-30)

**Trigger**: After Phase 5 done. Apply 5 patches từ Spec B V1.2.

**Why split**: Hiện tại agents/newsroom-pipeline.md = 508 lines, master-{bank,ck,bds}/SKILL.md = 359-414 lines. V5.1 thêm 4 format body + voice + stance sẽ balloon 500+. SPLIT để mỗi file ≤200 lines, dễ navigate + edit.

**Strategy**: Move existing content to references/, SKILL.md giữ core workflow + reference loaders. Duplicate `voice-layer-rules.md` + `stance-directive-handler.md` 3 copies trong 3 master skill (CLAUDE.md cấm shared folder).

### Task 23: Split orchestrator skill + agent

**Files:**
- Modify: `.claude/agents/newsroom-pipeline.md` (508 → ~180 lines)
- Modify: `.claude/skills/finpath-newsroom-orchestrator/SKILL.md` (existing → ~140 lines)
- Create: `.claude/skills/finpath-newsroom-orchestrator/references/observability-emit.md`
- Create: `.claude/skills/finpath-newsroom-orchestrator/references/db-persist-patterns.md`
- Create: `.claude/skills/finpath-newsroom-orchestrator/references/failure-recovery.md`
- Create: `.claude/skills/finpath-newsroom-orchestrator/references/step-1-5-market-snapshot.md`
- Create: `.claude/skills/finpath-newsroom-orchestrator/references/step-3-5-format-director.md`
- Create: `.claude/skills/finpath-newsroom-orchestrator/references/step-4-5-headline-craft.md`

- [ ] **Step 1: Read current pipeline.md (508 lines)**

```bash
cat .claude/agents/newsroom-pipeline.md | head -60
```

- [ ] **Step 2: Extract observability content → observability-emit.md**

Source lines: `newsroom-pipeline.md:298-345` (payload_master + payload_skeptic patterns) + `newsroom-pipeline.md:75-130` (observability summary).

Target file content:

```markdown
# Pipeline Observability — Emit pattern per step

> Loaded from `Skill: finpath-newsroom-orchestrator` references. Orchestrator MUST emit `pipeline_log` payload after each step with required schema.

## Required fields V5.0+ (fail-loud)

Per `lib/pipeline_db.py::_OBSERVABILITY_REQUIRED`:
- `model: str` — agent model used (opus/sonnet)
- `duration_ms: int` — wall time
- `tokens: int | None` — optional (Claude Code không guarantee `<usage>`)

## Per-step extras

- step_4_master: `chosen_question_idx, chosen_pick_reason, skip_reasons, data_trail, format_id_used, accepted_hypothesis`
- step_4_5_headline_craft: `final_title, final_loi, candidates, hard_criteria_pass`
- step_5_skeptic: `angle, verdict, skeptic_data_trail` ⏸ PAUSED 2026-05-12

## Emit pattern (Python)

```python
import time
t0 = time.time()
started_at = datetime.now(timezone.utc).isoformat()
# ... dispatch agent ...
payload = {
    "model": "opus",
    "started_at": started_at,
    "duration_ms": int((time.time() - t0) * 1000),
    "tokens": parse_task_usage(task_return),
    # step-specific extras here
}
db.log_pipeline_step(article_id, "step_4_master", payload)
```

## Failure: validation rejects payload

`lib/pipeline_db.py::validate_pipeline_step` raises `ValueError` nếu thiếu required field. KHÔNG workaround — fix dispatch để collect đủ field.
```

- [ ] **Step 3: Extract DB persist patterns → db-persist-patterns.md**

Source lines: `newsroom-pipeline.md:185-250` (DB write patterns) + scattered DB query examples.

Target file content (~80 lines):

```markdown
# SQLite Persist Patterns — Orchestrator

> Loaded from `Skill: finpath-newsroom-orchestrator`. All DB writes go through `lib/pipeline_db.py::PipelineDB`. NEVER raw `sqlite3.connect()`.

## Open + WAL mode

```python
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')  # WAL auto-enabled
# ... operations ...
db.close()
```

## Persist generated_news (Master output)

[full pattern with code example — extracted from current pipeline.md]

## UPDATE title (Headline output, V5.1)

```python
db.conn.execute(
    "UPDATE generated_news SET title = ?, headline_final = ?, updated_at = CURRENT_TIMESTAMP WHERE article_id = ?",
    (final_title, final_loi, article_id)
)
db.conn.commit()
```

## Log pipeline_step

```python
db.log_pipeline_step(article_id, "step_4_master", payload)
# Auto validates via _OBSERVABILITY_REQUIRED + step-specific schema
```

## Atomic batch (multi-row)

```python
with db.conn:  # auto rollback on exception
    for row in rows:
        db.conn.execute(..., row)
```
```

- [ ] **Step 4: Extract failure recovery → failure-recovery.md**

Source: `newsroom-pipeline.md:346-410` (failure isolation, brief-level retry, batch survival).

Target file content (~60 lines): per-step failure handling. Brief N fail → continue brief N+1. Master accepted_hypothesis=false → skip Skeptic + render. Git publish fail → self-heal actions. Pages wait timeout → fallback URL.

- [ ] **Step 5: NEW step-1-5-market-snapshot.md**

Content (~80 lines): Step 1.5 Market Snapshot Python helper (lib/stages/run_market_snapshot.py). Reads ticker → Finpath API price + volume → compute `ticker_status` (Hot/Cold/Normal) + `day_change_pct`. Emit payload. No agent dispatch.

- [ ] **Step 6: NEW step-3-5-format-director.md**

Content (~100 lines): Dispatch newsroom-format-director subagent. Input: briefs[] + market_snapshot + variety_guard (last 3 format). Output: format_picks[]. Validate response shape before persist step_3_5.

- [ ] **Step 7: NEW step-4-5-headline-craft.md**

Content (~100 lines): Dispatch newsroom-headline-craft subagent AFTER Master persist. Input: article_id (Headline reads body từ DB) + brief + stance_directive. Output: final_title + final_loi + candidates. UPDATE generated_news.title. Persist step_4_5 payload.

- [ ] **Step 8: Update SKILL.md (140 lines)**

Keep: core workflow + dispatch logic + hard rules.
Move out: observability detail, DB patterns, failure recovery, step-1-5/3-5/4-5 detail.

At bottom of SKILL.md add references section:

```markdown
## References (load on-demand)

For detail beyond core flow:
- `references/observability-emit.md` — pipeline_log emit pattern
- `references/db-persist-patterns.md` — SQLite write patterns
- `references/failure-recovery.md` — per-step failure handling
- `references/step-1-5-market-snapshot.md` — Market Snapshot helper
- `references/step-3-5-format-director.md` — Format Director dispatch
- `references/step-4-5-headline-craft.md` — Headline Craft dispatch + UPDATE
- `references/compare-feed-layout.md` — (existing) viewer layout
```

- [ ] **Step 9: Update agent file (180 lines)**

Keep: HARD RULE + Skill load instruction. Move detail to skill references. Agent body becomes thin: load skill, run flow.

- [ ] **Step 10: Test loadability**

Run dispatch dry-run:
```bash
echo "TEST" | uv run python -c "
from pathlib import Path
skill = Path('.claude/skills/finpath-newsroom-orchestrator')
assert skill.exists()
refs = list((skill / 'references').glob('*.md'))
assert len(refs) >= 7, f'expected 7 refs, got {len(refs)}'
print(f'OK {len(refs)} references')
"
```

- [ ] **Step 11: Commit**

```bash
git add .claude/agents/newsroom-pipeline.md .claude/skills/finpath-newsroom-orchestrator/
git commit -m "refactor(orchestrator): split skill into 7 references (V5.1.2 patch 5)"
```

### Task 24: Split master-bank skill

**Files:**
- Modify: `.claude/skills/finpath-newsroom-master-bank/SKILL.md` (359 → ~180 lines)
- Create: `.claude/skills/finpath-newsroom-master-bank/references/format-bodies/flash-qa.md`
- Create: `.claude/skills/finpath-newsroom-master-bank/references/format-bodies/standard-qa.md`
- Create: `.claude/skills/finpath-newsroom-master-bank/references/format-bodies/standard-listicle.md`
- Create: `.claude/skills/finpath-newsroom-master-bank/references/format-bodies/standard-narrative.md`
- Create: `.claude/skills/finpath-newsroom-master-bank/references/voice-layer-rules.md`
- Create: `.claude/skills/finpath-newsroom-master-bank/references/stance-directive-handler.md`

- [ ] **Step 1: Create flash-qa.md (~70 lines)**

```markdown
# Format: flash_qa (100-150 từ)

> Loaded from `Skill: finpath-newsroom-master-bank`. Apply khi `format_id == "flash_qa"`.

## Khi nào dùng

Ticker_status = Hot (top tăng/giảm/bùng nổ/cạn cung) + data_richness ∈ {low, medium}. Người đọc cần info nhanh khi mã đang nóng.

## Body pattern

```
[1 câu mở (≥20 từ): nêu question chính]

[1 paragraph trả lời (60-100 từ): answer + verdict]

[1 câu closing (≤20 từ): verdict ngắn cho NĐT cầm]
```

- KHÔNG bullet
- KHÔNG heading "## Cần để ý"
- Max 1 em dash / bài (Spec B Patch 4)

## Word count

- Total: 100-150 từ HARD CAP. <100 fail no_data. >150 fail word_count.
- Opening: ≥20 từ
- Body paragraph: 60-100 từ
- Closing: ≤20 từ

## Bold highlight

≥1 bold `**...**` trong body paragraph. Highlight 1 số key (VD: `**lãi +17%**`).

## Verdict line

Closing MUST có verdict cho NĐT phân loại (Voice Rule 3):
- ✅ "Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động ngắn hạn"
- ❌ "Cần thêm thông tin để đánh giá" (ba phải, fail Voice Rule 2)

## Examples Bank sector

### Example 1: VCB +6.8% Hot
Title (by Headline agent): "VCB tăng 6,8% sau khi Q1 lãi vượt 11%, đà tăng còn tiếp?"

Body (130 từ):
> Vietcombank tăng kịch trần 6,8% trong phiên sáng 12/5 sau khi công bố lãi quý 1 vượt 11% so cùng kỳ, vì sao thị trường phản ứng mạnh đến vậy?
>
> Lãi tăng vì biên lãi vay nới rộng từ 3,1% lên 3,3% nhờ huy động giá rẻ tăng. Nợ xấu vẫn ở mức an toàn 0,9%, ROA giữ ổn định 1,8%. **Tín dụng quý 1 tăng 3,5%** cao hơn trung bình ngành 2,1%. Phía sau con số: VCB đang ăn được phần lợi từ chu kỳ NHNN nới lỏng, không phải tăng nóng tín dụng.
>
> Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động ngắn hạn theo phiên.

### Example 2: TCB -6.5% Cold panic
[full second example similar pattern]
```

- [ ] **Step 2: Create standard-qa.md (~80 lines)**

[same pattern: định nghĩa khi nào dùng + body pattern + word count + bold rule + verdict + 2 example Bank sector]

- [ ] **Step 3: Create standard-listicle.md (~90 lines)**

[same pattern, this is current default — port existing V4.0 body pattern guide here]

- [ ] **Step 4: Create standard-narrative.md (~80 lines)**

[same pattern]

- [ ] **Step 5: Create voice-layer-rules.md (~100 lines)**

```markdown
# Voice Layer 5 Rules — Master Bank

> Loaded from `Skill: finpath-newsroom-master-bank`. Apply CROSS-CUTTING toàn bộ 4 format.

## V1 — Stance required

Bài MUST có quan điểm rõ. Nhận `stance_directive` từ brief (see `stance-directive-handler.md`).

## V2 — No-hedging (definition-based, KHÔNG list từ)

### Định nghĩa "ba phải" (hedging)

Câu khẳng định trung tính không cam kết hướng nào, có thể đúng dù sự thật ngược lại.

### Test 1 — Đảo sự thật

Đảo ngược sự thật, câu vẫn đúng? → fail.
- ❌ "Cổ phiếu có thể tăng tùy thuộc thị trường" (tăng/giảm đều đúng → BA PHẢI)
- ✅ "Cổ phiếu sẽ tăng vì Q1 lãi vượt 30%" (có direction + lý do)

### Test 2 — Direction check

Có cam kết direction không? → không = fail.
- ❌ "Vẫn còn phải chờ thêm dữ liệu mới biết"
- ✅ "Đà tăng có thể chững lại Q2 nếu NHNN siết lãi suất" (có direction)

### Implementation

LLM-as-judge runs 2 tests trên từng câu body. Gate fail = bài có ≥1 câu fail BA PHẢI.

## V3 — Verdict line bắt buộc

Closing MUST có verdict cụ thể cho NĐT. Không "tùy quan điểm", không "tham khảo".

## V4 — Title stance (delegated to Headline)

V5.1: Master KHÔNG generate title. Headline agent enforce title stance match body. Master chỉ cần đảm bảo body có stance rõ → Headline auto-pick title cùng hướng.

## V5 — Contrarian-when-warranted

Master được phép viết góc nghịch CHỈ KHI data clear support. KHÔNG override stance_directive (nếu stance positive, không tự ý viết negative).
```

- [ ] **Step 6: Create stance-directive-handler.md (~80 lines)**

```markdown
# Stance Directive Handler — Master Bank

> Loaded from `Skill: finpath-newsroom-master-bank`. Apply khi parse brief.

## Schema

```yaml
stance_directive:
  direction: "positive" | "negative" | "neutral"
  confidence: "high" | "medium" | "low"
  reason: |
    Free-form prose 1-3 câu Vietnamese.
  key_evidence:
    - "..."
```

## Receive

Parse from brief_json[stance_directive]. Required field — fail-loud nếu missing.

## Apply rules

1. **Body MUST follow direction**. Opening + verdict cùng hướng `direction`.
2. **Body MUST cite ≥1 evidence** từ `key_evidence` array (preserve wording where possible).
3. **Caveat permitted in closing** nếu data nuance. Caveat phải có direction (không ba phải).
4. **NEVER override stance** — Voice Rule V5 không apply để override stance_directive.

## Examples

### Stance: positive (mã giảm sàn nhưng nội lực OK)

Brief:
```yaml
direction: positive
reason: "Mã giảm sàn hôm nay nhưng Q1 lãi vẫn tăng 17%, ROA stable, không có scandal pháp lý → tin tích cực: panic temporary."
key_evidence: ["Q1 lãi +17%", "Không có scandal", "Sector cycle vẫn up"]
```

Body MUST:
- Opening: "Cổ phiếu X giảm sàn hôm nay, nhưng Q1 lãi vẫn tăng 17%..." (positive direction).
- Closing verdict: "Mã phù hợp NĐT tích lũy giá oversold" (positive).

Body MUST NOT:
- Mở bằng "tin xấu" / "đáng lo".
- Closing "chờ xem thêm" (ba phải, violation V2).

### Stance: negative (mã tăng trần nhưng PE/PB cao + earnings yếu)

[example case 2]

### Stance: neutral (mixed signal)

[example case 3]
```

- [ ] **Step 7: Update SKILL.md (180 lines)**

Keep: 9-step workflow + Anti-pattern jargon mapping reference + finpath API patterns + KB structure.

Move out (now in references/):
- 4 format body patterns → format-bodies/*.md
- Voice 5 rules → voice-layer-rules.md
- Stance handling → stance-directive-handler.md

Add references section listing 6 new files + 5 existing.

- [ ] **Step 8: Verify dispatch**

```bash
ls .claude/skills/finpath-newsroom-master-bank/references/
# Expected: 12 files (4 format-bodies/ + voice + stance + 6 existing)
```

- [ ] **Step 9: Commit**

```bash
git add .claude/skills/finpath-newsroom-master-bank/
git commit -m "refactor(master-bank): split skill — 4 format-bodies + voice + stance (V5.1.2)"
```

### Task 25: Split master-ck skill

Same pattern as Task 24, BUT examples use SSI/HCM/VND tickers (CK sector). voice-layer-rules + stance-directive-handler là copy-paste từ master-bank (acceptable duplicate per CLAUDE.md no-shared-folder rule).

[Steps 1-9 same structure, content swap to CK sector — full content omitted here for brevity, follow Task 24 mapping]

### Task 26: Split master-bds skill

Same pattern as Task 24, BUT examples use VHM/NVL/KDH/DXG tickers (BĐS sector). Note BĐS specific: data_richness thường low (BCTC quarterly thiếu), so flash_qa + standard_qa formats sẽ phổ biến hơn.

[Steps 1-9 same structure, content swap to BĐS sector]

### Task 27: Master prompts dỡ title generation rule (3 sector)

**Files:**
- Modify: `.claude/agents/newsroom-master-bank.md`
- Modify: `.claude/agents/newsroom-master-ck.md`
- Modify: `.claude/agents/newsroom-master-bds.md`

- [ ] **Step 1: Find title rule in master-bank.md**

```bash
grep -n "title\|Title\|tension" .claude/agents/newsroom-master-bank.md
```

- [ ] **Step 2: Remove title generation sections**

DELETE blocks:
- "Title hook test 5s — đọc 5 giây phải thấy rõ insight"
- "Tension word required: ?, —, hy sinh, đánh đổi, nghịch lý"
- "Title style guide per format" (table mapping format→title style)
- Any "title" field in output JSON schema

- [ ] **Step 3: Add stance_directive parsing instructions**

ADD section:

```markdown
## Stance Directive (V5.1.2)

Brief V5.1 chứa `stance_directive` object. Parse + apply per `references/stance-directive-handler.md`:

1. Read `brief["stance_directive"]["direction"]` → bài phải viết theo hướng này.
2. Read `brief["stance_directive"]["key_evidence"]` → cite ≥1 evidence trong body.
3. Closing verdict MUST match direction.
4. KHÔNG generate title. Trả về body + insight + data_trail.
```

- [ ] **Step 4: Update output schema**

Master return JSON:

```json
{
  "article_id": "uuid",
  "body": "...",
  "insight_final": "...",
  "data_trail": [...],
  "quality_gates": {...},
  "format_id_used": "standard_listicle",
  "accepted_hypothesis": true
}
```

REMOVE field `"title"` from output schema. Note in prompt: "title sẽ do Headline agent generate sau."

- [ ] **Step 5: Repeat for master-ck.md + master-bds.md**

Same edits across 3 agent files.

- [ ] **Step 6: Run test**

```bash
uv run pytest tests/test_master_prompts.py -v
# Expected: tests verify no "title" in output schema
```

- [ ] **Step 7: Commit**

```bash
git add .claude/agents/newsroom-master-*.md
git commit -m "refactor(master): remove title generation (V5.1.2 — Headline owns title)"
```

### Task 28: Story Editor brief schema add stance_directive

**Files:**
- Modify: `.claude/agents/newsroom-story-editor.md`
- Modify: `.claude/skills/finpath-newsroom-story-editor/SKILL.md`
- Modify: `lib/pipeline_db.py` — `_STEP_3_REQUIRED_V5` add stance_directive
- Test: `tests/test_pipeline_db_validation.py::test_v5_step_3_requires_stance_directive`

- [ ] **Step 1: Write failing test**

```python
def test_v5_step_3_requires_stance_directive():
    payload = {
        "model": "opus",
        "duration_ms": 5000,
        "briefs": [],
    }
    with pytest.raises(ValueError, match="stance_directive"):
        validate_pipeline_step("step_3_story_editor", payload, pipeline_version="V5.1.2")
```

- [ ] **Step 2: Update pipeline_db.py**

```python
_STEP_3_REQUIRED_V5 = {
    **_STEP_3_REQUIRED_V4,
    **_OBSERVABILITY_REQUIRED,
    "briefs": list,  # array of brief objects
}
# Per-brief schema enforced via _BRIEF_SCHEMA_V5
_BRIEF_SCHEMA_V5 = {
    **_BRIEF_SCHEMA_V4,
    "stance_directive": dict,
}
_STANCE_DIRECTIVE_REQUIRED = {
    "direction": str,        # positive/negative/neutral
    "confidence": str,       # high/medium/low
    "reason": str,
    "key_evidence": list,
}
```

In `validate_pipeline_step`, when version >= V5.1.2 and step_3, iterate briefs[] and validate each against _BRIEF_SCHEMA_V5 + stance_directive nested validation.

- [ ] **Step 3: Run test passes**

```bash
uv run pytest tests/test_pipeline_db_validation.py::test_v5_step_3_requires_stance_directive -v
```

- [ ] **Step 4: Update Story Editor prompt**

ADD section in `.claude/agents/newsroom-story-editor.md`:

```markdown
## Stance Directive Output (V5.1.2)

For EACH brief output, include `stance_directive` object:

```yaml
stance_directive:
  direction: "positive" | "negative" | "neutral"
  confidence: "high" | "medium" | "low"
  reason: |
    Free-form prose 1-3 câu giải thích WHY stance đó.
    Cross-intersect:
    - Price event (Step 1.5 Market Snapshot)
    - Internal strength (broad 7-layer: tài chính + quản trị + chiến lược + vận hành + sản phẩm + sector cycle + vĩ mô)
    - Context narrative
  key_evidence:
    - "..."
    - "..."
```

KHÔNG dập khuôn matrix 2×2 (PE cao=negative, giảm sàn=positive). Stance dựa REASON narrative, không metric đơn lẻ.
```

- [ ] **Step 5: Update Story Editor skill**

`.claude/skills/finpath-newsroom-story-editor/SKILL.md` thêm references/`stance-judgment-guide.md` (~120 lines) — 7-layer nội lực definition + 6 case study (Hot+healthy, Hot+degraded, Cold+healthy, Cold+degraded, Normal+mixed, Normal+early signal).

- [ ] **Step 6: Commit**

```bash
git add lib/pipeline_db.py .claude/agents/newsroom-story-editor.md .claude/skills/finpath-newsroom-story-editor/ tests/
git commit -m "feat(story-editor): add stance_directive brief field + 7-layer judgment (V5.1.2)"
```

### Task 29: Master receive + apply stance_directive

**Files:**
- Modify: `lib/quality_gates.py` — `check_stance_consistency` accept stance_directive object
- Modify: `.claude/skills/finpath-newsroom-master-{bank,ck,bds}/references/stance-directive-handler.md` (Task 24-26 already create file, this task add tests + integration)
- Test: `tests/test_stance_application.py` (NEW)

- [ ] **Step 1: Write failing test**

```python
def test_master_body_follows_stance_positive():
    stance = {
        "direction": "positive",
        "confidence": "high",
        "reason": "Mã giảm sàn nhưng Q1 lãi vẫn tăng 17%, ROA stable",
        "key_evidence": ["Q1 lãi +17%", "ROA stable"],
    }
    body = "Cổ phiếu X giảm sàn hôm nay, nhưng Q1 lãi vẫn tăng 17%..."
    result = check_stance_consistency(body, stance)
    assert result.passed
    assert "Q1 lãi +17%" in body  # evidence cited
```

- [ ] **Step 2: Implement check_stance_consistency**

```python
def check_stance_consistency(body: str, stance_directive: dict) -> GateResult:
    direction = stance_directive["direction"]
    evidence = stance_directive["key_evidence"]
    
    # Test 1: Body cites ≥1 evidence (substring match)
    cited = [e for e in evidence if e in body]
    if not cited:
        return GateResult(passed=False, reason=f"Body không cite evidence nào từ key_evidence={evidence}")
    
    # Test 2: Closing line matches direction (LLM-as-judge)
    closing = body.strip().split("\n")[-1]  # last non-empty line
    judge_result = llm_direction_check(closing, expected=direction)
    if not judge_result["match"]:
        return GateResult(passed=False, reason=f"Closing '{closing}' không match direction '{direction}'")
    
    return GateResult(passed=True, evidence_cited=cited)
```

- [ ] **Step 3: Run tests pass**

- [ ] **Step 4: Commit**

```bash
git add lib/quality_gates.py tests/test_stance_application.py
git commit -m "feat(gates): stance_consistency check — evidence cited + direction match (V5.1.2)"
```

### Task 30: Voice Rule 2 redefine — LLM-as-judge no-hedging

**Files:**
- Modify: `lib/gate_checker.py` (or `lib/quality_gates.py`) — `check_no_hedging` REWRITE
- Test: `tests/test_no_hedging_redefine.py` (NEW)

- [ ] **Step 1: Write failing tests**

```python
def test_no_hedging_test_1_reverse_truth_fails_for_dual_outcome():
    """'có thể tăng tùy thuộc thị trường' → reverse-truth pass → BA PHẢI"""
    text = "Cổ phiếu có thể tăng tùy thuộc thị trường"
    result = check_no_hedging(text)
    assert not result.passed
    assert "reverse_truth" in result.reason

def test_no_hedging_passes_directional():
    """'sẽ tăng vì Q1 lãi vượt 30%' → có direction + lý do → PASS"""
    text = "Cổ phiếu sẽ tăng vì Q1 lãi vượt kỳ vọng 30%"
    result = check_no_hedging(text)
    assert result.passed

def test_no_hedging_passes_conditional_with_direction():
    """'có thể chững lại nếu NHNN siết' → có direction → PASS"""
    text = "Đà tăng có thể chững lại Q2 nếu NHNN siết lãi suất"
    result = check_no_hedging(text)
    assert result.passed

def test_no_hedging_fails_no_direction():
    """'vẫn còn chờ' → không direction → BA PHẢI"""
    text = "Vẫn còn phải chờ thêm dữ liệu mới biết"
    result = check_no_hedging(text)
    assert not result.passed
```

- [ ] **Step 2: Implement check_no_hedging with 2 LLM tests**

```python
def check_no_hedging(text: str) -> GateResult:
    """
    Definition-based: "Ba phải" = câu khẳng định trung tính không cam kết hướng,
    có thể đúng dù sự thật ngược lại.
    
    Test 1 — Reverse-truth: Đảo ngược sự thật, câu vẫn đúng?
    Test 2 — Direction: Có cam kết direction không?
    """
    prompt = f"""Apply 2 tests to this Vietnamese sentence about stock analysis:

Sentence: "{text}"

Test 1 — Reverse-truth: Imagine the actual outcome is OPPOSITE of what the sentence implies. Does the sentence still hold? If yes, the sentence is hedging.

Test 2 — Direction: Does the sentence commit to a direction (up/down/strong/weak/positive/negative)? If no direction is committed, the sentence is hedging.

Return JSON:
{{
    "test_1_reverse_truth": "pass" | "fail",   // pass = NOT hedging
    "test_2_direction": "pass" | "fail",        // pass = has direction
    "reason": "1-line explanation"
}}
"""
    response = sonnet_call(prompt, max_tokens=100)
    result = json.loads(response)
    passed = result["test_1_reverse_truth"] == "pass" and result["test_2_direction"] == "pass"
    return GateResult(passed=passed, reason=result["reason"])
```

- [ ] **Step 3: Run tests pass (each test call ~50 tokens, LLM-as-judge stable)**

- [ ] **Step 4: Add em dash body density check**

```python
def check_em_dash_density(body: str) -> GateResult:
    """Em dash (—, U+2014) density ≤ 1 / 100 từ."""
    em_count = body.count("—")
    word_count = len(body.split())
    density = em_count / (word_count / 100) if word_count > 0 else 0
    if density > 1:
        return GateResult(passed=False, reason=f"Em dash density {density:.2f}/100 words > 1")
    return GateResult(passed=True)
```

- [ ] **Step 5: Wire into check_all_v5**

```python
def check_all_v5(body: str, format_id: str, stance_directive: dict) -> list[GateResult]:
    gates = [
        check_no_english_jargon(body),       # Gate 1
        check_no_metadata_leak(body),         # Gate 2
        check_no_hedging(body),               # Gate 3 (REDEFINED)
        check_verdict_line(body),             # Gate 4
        check_stance_consistency(body, stance_directive),  # Gate 5 (now uses stance_directive)
        check_em_dash_density(body),          # Gate 6 NEW
        check_word_count_per_format(body, format_id),  # Gate 7
        check_body_pattern_per_format(body, format_id),  # Gate 8
    ]
    return gates
```

Total 8 gates (was 9 in V5.0, title_pattern removed → 8 in V5.1, em_dash_density added in V5.1.2 → still 8 since stance_consistency was implicit before).

- [ ] **Step 6: Commit**

```bash
git add lib/gate_checker.py lib/quality_gates.py tests/
git commit -m "refactor(gates): no-hedging redefine LLM-as-judge + em_dash_density (V5.1.2)"
```

---

## Phase 6 — Self-review checklist

### Spec coverage check (V5.1.2)
- [ ] Patch 1 (Master no-title): Task 27 dỡ title rule ✓
- [ ] Patch 2 (Stance directive): Task 28 brief schema + Task 29 Master apply ✓
- [ ] Patch 3 (Voice Rule 2 redefine): Task 30 LLM-as-judge ✓
- [ ] Patch 4 (Em dash policy): Task 30 em_dash_density + Plan C em dash regex title ✓
- [ ] Patch 5 (Master skill SPLIT): Task 24-26 ✓
- [ ] Patch 5b (Orchestrator skill SPLIT): Task 23 ✓

### Placeholder scan
- [ ] Task 25 (Split master-ck) full content omitted — rely on Task 24 mapping. Mitigate: executor must apply Task 24 pattern, just swap example tickers. Document as "follow Task 24 structure, swap content".
- [ ] Task 26 (Split master-bds) same.

### Type consistency
- `stance_directive` shape consistent: `{direction, confidence, reason, key_evidence}` across Task 28-29 + Spec B Patch 2.
- `GateResult` field `passed: bool, reason: str, evidence_cited: list[str] | None` consistent Task 29-30.

---

## Execution choice

Plan complete and saved to `docs/superpowers/plans/2026-05-11-master-article-format-diversity.md`. Two execution options:

**1. Subagent-Driven (recommended)** — Dispatch fresh subagent per task, two-stage review (spec compliance + code quality) between tasks. Fast iteration, isolated context per task.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints for user review.

**Which approach?**
