# Headline Craft Agent V1.0 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Triển khai dedicated Headline Craft agent (Step 4.5) chuyên giật tít — đọc tiêu đề là muốn click vào bài. 4 hard criteria + 8-point scoring + benchmark "TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?".

**Architecture:** Master writes body + draft_title. Step 4.5 Headline agent (Sonnet) generates 5 title candidates → score 8-point rubric → pick best → replace title in DB. Skeptic critiques full article post-replacement with new `weak_title` angle (10 angles total). Pipeline V5.0 (11 steps) → V5.1 (12 steps).

**Tech Stack:** Python 3.13 (uv), SQLite, Sonnet subagent, pytest, regex for hard criteria detection.

**Spec**: `docs/superpowers/specs/2026-05-12-headline-craft-agent-design.md` V1.0.

**Coupled with**: Plan B `docs/superpowers/plans/2026-05-11-master-article-format-diversity.md` — see "V5.1 PATCH NOTICE" block at top of plan B for patches required to plan B tasks.

---

## Execution order recommendation

Run interleaved with Plan B:

```
Plan B Task 1 (format_registry.yaml — apply V5.1 patch, omit title fields)
↓
Plan C Task 1 (lib/headline_scorer.py — independent, can run parallel with B Task 2)
↓
Plan B Tasks 2-5 (Market Snapshot, pipeline_version, validate_pipeline_step, no_hedging gates)
↓
Plan C Task 2 (tests for scorer — depends on Task 1)
↓
Plan B Task 6 (per-format gates — apply V5.1 patch, drop check_title_per_format)
↓
Plan C Task 3 (Headline agent .md)
↓
Plan B Tasks 7-11 (foundation completion + Format Director)
↓
Plan C Task 4 (skill SKILL.md)
↓
Plan C Task 5 (pipeline orchestrator Step 4.5 insertion)
↓
Plan C Task 6 (schema validation for step_4_5 with hard criteria check)
↓
Plan B Tasks 12-15 (Story Editor + Master — apply V5.1 patch for Master, drop title gate)
↓
Plan C Task 7 (Skeptic 10 angles + weak_title)
↓
Plan B Tasks 16-22 (render + frontend + CLAUDE.md)
↓
Plan C Task 8 (CLAUDE.md sections for Headline)
↓
Plan B Task 23-24 (verification) + Plan C Task 9 (E2E verification — title quality check)
```

Total: 9 tasks plan C, interleaved with 24 tasks plan B = 33 atomic commits.

---

## Phase 1 — Scorer module (Tasks 1-2)

### Task 1: `lib/headline_scorer.py` — pure functions

**Files:**
- Create: `lib/headline_scorer.py`

- [ ] **Step 1: Create file with all 6 detector functions + scorer + pick_best**

```python
"""Headline scoring module V1.0 — 8-point rubric for title craft.

Headline Craft agent uses these pure functions to score 5 title candidates.
Functions are testable independently + callable code-level for fallback.

Benchmark: 'TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?' should score 7/8.
"""
from __future__ import annotations
import re
from typing import Any

# Reuse V5.0 tension word pool (was in quality_gates, now also used here)
from lib.quality_gates import TITLE_TENSION_WORDS

DRAMATIC_VERBS = [
    "hy sinh", "đánh đổi", "đặt cược", "bỏ phiếu", "lội ngược",
    "lao dốc", "rút khỏi", "vượt mặt", "tung đòn", "đặt cọc",
    "chấp nhận thua", "tự chậm lại", "đập cửa", "thoát hiểm",
    "chấp nhận hi sinh", "đánh cược", "đổ vỡ", "vực dậy",
    "tiếp đà", "phá kỷ lục", "soán ngôi", "lấn sang", "rơi vào",
]

PR_CLICKBAIT_WORDS = [
    "cú nổ", "bí mật", "sốc", "hot", "thông tin nóng",
    "không thể tin nổi", "cú twist", "kỳ tích", "hé lộ",
]

# 61-ticker universe (sync with lib/stages/run_crawler.py FULL_UNIVERSE)
ALL_TICKERS = [
    # Bank 27
    "VCB", "CTG", "BID", "TCB", "MBB", "ACB", "VPB", "HDB",
    "STB", "SHB", "EIB", "TPB", "MSB", "LPB", "OCB", "VIB",
    "NAB", "BAB", "NVB", "SGB",
    "VAB", "BVB", "ABB", "KLB", "VBB", "PGB", "HDF",
    # CK 30
    "SSI", "VND", "HCM", "VCI", "VIX",
    "SHS", "MBS", "BVS", "BSI", "AGR", "CTS", "APG", "EVS",
    "IVS", "PSI", "TVS", "WSS", "ORS", "VFS", "TCI",
    "DSC", "FTS", "CSI", "SBS", "PHS", "ART", "APS", "BMS", "AAS", "VTS",
    # BĐS 4
    "VHM", "NVL", "KDH", "DXG",
]
GROUP_REFS = ["Big4", "Big 4", "tư nhân top", "tư nhân", "Big5"]


def has_ticker(title: str) -> bool:
    """Check title contains at least 1 ticker OR group reference."""
    for t in ALL_TICKERS:
        if re.search(rf"\b{t}\b", title):
            return True
    for g in GROUP_REFS:
        if g in title:
            return True
    return False


def has_specific_number(title: str) -> bool:
    """Check title contains number with financial unit."""
    return bool(re.search(
        r"\d+([.,]\d+)?\s*(tỷ|triệu|nghìn|%|đ|/năm|/tháng|/quý|đ/tháng|bps|điểm)",
        title, re.IGNORECASE
    ))


def has_dramatic_verb(title: str) -> bool:
    tlc = title.lower()
    return any(v in tlc for v in DRAMATIC_VERBS)


def has_tension_word(title: str) -> bool:
    tlc = title.lower()
    return any(w in tlc for w in TITLE_TENSION_WORDS)


def has_paradox_pattern(title: str) -> bool:
    return bool(re.search(r"\bmà\b|\bnhưng\b|\bthật ra\b|\bthực ra\b|\bkỳ thực\b", title.lower()))


def has_open_question(title: str) -> bool:
    return title.rstrip().endswith("?")


def has_pr_clickbait(title: str) -> bool:
    tlc = title.lower()
    return any(w in tlc for w in PR_CLICKBAIT_WORDS)


def has_english(title: str) -> bool:
    """Reuse quality_gates English jargon check on title."""
    from lib.quality_gates import ENGLISH_JARGON
    tlc = title.lower()
    return any(re.search(rf"\b{re.escape(j)}\b", tlc) for j in ENGLISH_JARGON)


def check_hard_criteria(title: str) -> dict[str, Any]:
    """Run 4 hard criteria. Returns {pass: bool, failed: [str]}.
    Any failure → reject title; Headline agent must regenerate.
    """
    failed = []
    if not has_ticker(title):
        failed.append("ticker_missing")
    if len(title.split()) > 12:
        failed.append("too_long")
    if not (has_dramatic_verb(title) or has_specific_number(title) or
            has_paradox_pattern(title) or has_open_question(title)):
        failed.append("no_hook")
    if has_pr_clickbait(title):
        failed.append("pr_clickbait")
    if has_english(title):
        failed.append("english_jargon")
    return {"pass": len(failed) == 0, "failed": failed}


def score_title(title: str) -> dict[str, Any]:
    """8-point rubric. Returns {score, max, elements}.
    Only call after check_hard_criteria passes.
    """
    elements = {
        "ticker": has_ticker(title),
        "dramatic_verb": has_dramatic_verb(title),
        "specific_number": has_specific_number(title),
        "open_question": has_open_question(title),
        "tension_word": has_tension_word(title),
        "paradox_pattern": has_paradox_pattern(title),
        "extra_concise": len(title.split()) <= 10,
    }
    score = 0
    if elements["dramatic_verb"]: score += 2
    if elements["specific_number"]: score += 2
    if elements["open_question"]: score += 1
    if elements["tension_word"]: score += 1
    if elements["paradox_pattern"]: score += 1
    if elements["extra_concise"]: score += 1
    return {"score": score, "max": 8, "elements": elements}


def pick_best_candidate(candidates: list[str]) -> dict[str, Any]:
    """Apply hard criteria filter + score → return best.

    Returns: {final_title, picked_score, all_scored}
    Raises ValueError if 0 candidates pass hard criteria (orchestrator should
    regenerate up to 2 retries before escalating).
    """
    scored = []
    for c in candidates:
        hard = check_hard_criteria(c)
        entry = {
            "text": c,
            "hard_pass": hard["pass"],
            "hard_failed": hard["failed"],
        }
        if hard["pass"]:
            entry.update(score_title(c))
        scored.append(entry)

    passing = [s for s in scored if s["hard_pass"]]
    if not passing:
        raise ValueError(f"All {len(candidates)} candidates failed hard criteria")
    # Sort by score DESC, tie-break by length ASC
    passing.sort(key=lambda x: (-x["score"], len(x["text"])))
    best = passing[0]
    return {
        "final_title": best["text"],
        "picked_score": best["score"],
        "all_scored": scored,
    }
```

- [ ] **Step 2: Commit**

```bash
git add lib/headline_scorer.py
git commit -m "feat(headline): scorer module V1.0 — 4 hard criteria + 8-point rubric (Plan C Task 1)

Pure functions: has_ticker / has_dramatic_verb / has_specific_number /
has_paradox_pattern / has_open_question / has_pr_clickbait / has_english.

check_hard_criteria: returns {pass, failed}. Reject if missing ticker /
too long / no hook / PR clickbait / English jargon.

score_title: 8-point rubric. dramatic_verb +2, specific_number +2,
open_question +1, tension_word +1, paradox_pattern +1, extra_concise +1.

pick_best_candidate: filter hard pass + sort score DESC tie-break length ASC.
ValueError if 0 candidates pass.
"
```

---

### Task 2: Tests for headline_scorer

**Files:**
- Create: `tests/test_headline_scorer.py`

- [ ] **Step 1: Write comprehensive tests**

```python
"""Tests for lib/headline_scorer — 4 hard criteria + 8-point rubric."""
from __future__ import annotations
import pytest
from lib.headline_scorer import (
    has_ticker, has_specific_number, has_dramatic_verb, has_tension_word,
    has_paradox_pattern, has_open_question, has_pr_clickbait, has_english,
    check_hard_criteria, score_title, pick_best_candidate,
)

BENCHMARK = "TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?"


# === Detectors ===

def test_has_ticker_vcb():
    assert has_ticker("VCB Q1 báo cáo lợi nhuận") is True

def test_has_ticker_tcb():
    assert has_ticker(BENCHMARK) is True

def test_has_ticker_group_big4():
    assert has_ticker("Big4 đầu sàn — vì sao chậm nhất?") is True

def test_has_ticker_missing():
    assert has_ticker("Ngân hàng tư nhân tăng trưởng quý 1") is False

def test_has_ticker_partial_match_rejected():
    """Substring match should not pass (\\b boundary)."""
    assert has_ticker("XYZVCB123") is False

def test_has_specific_number_5000_ty():
    assert has_specific_number("TCB hy sinh 5.000 tỷ") is True

def test_has_specific_number_percent():
    assert has_specific_number("TCB chia 67%") is True

def test_has_specific_number_per_year():
    assert has_specific_number(BENCHMARK) is True

def test_has_specific_number_none():
    assert has_specific_number("VCB đáng giữ dài hạn") is False

def test_has_dramatic_verb_hy_sinh():
    assert has_dramatic_verb(BENCHMARK) is True

def test_has_dramatic_verb_lao_doc():
    assert has_dramatic_verb("VPB lao dốc Q1") is True

def test_has_dramatic_verb_none():
    assert has_dramatic_verb("VCB tăng trưởng quý 1") is False

def test_has_tension_word_doi_lay():
    assert has_tension_word(BENCHMARK) is True

def test_has_paradox_pattern_ma():
    assert has_paradox_pattern("VCB to nhất mà chậm nhất") is True

def test_has_paradox_pattern_thuc_ra():
    assert has_paradox_pattern("VPB lãi đẹp — thật ra chỉ FE Credit kéo") is True

def test_has_paradox_pattern_none():
    assert has_paradox_pattern("VCB Q1 báo cáo") is False

def test_has_open_question():
    assert has_open_question(BENCHMARK) is True

def test_has_open_question_no_qm():
    assert has_open_question("VCB Q1 lợi nhuận tăng") is False

def test_has_pr_clickbait_cu_no():
    assert has_pr_clickbait("Cú nổ lớn từ VCB") is True

def test_has_pr_clickbait_none():
    assert has_pr_clickbait(BENCHMARK) is False

def test_has_english_nim():
    assert has_english("VCB NIM giảm 30bps") is True

def test_has_english_clean():
    assert has_english(BENCHMARK) is False


# === Hard criteria ===

def test_hard_criteria_benchmark_passes():
    assert check_hard_criteria(BENCHMARK)["pass"] is True

def test_hard_criteria_no_ticker_fails():
    result = check_hard_criteria("Hy sinh 5.000 tỷ — đổi lấy gì?")
    assert result["pass"] is False
    assert "ticker_missing" in result["failed"]

def test_hard_criteria_too_long_fails():
    long = " ".join(["VCB"] + ["word"] * 13)
    result = check_hard_criteria(long)
    assert result["pass"] is False
    assert "too_long" in result["failed"]

def test_hard_criteria_no_hook_fails():
    result = check_hard_criteria("VCB Q1 báo cáo lợi nhuận quý 1")
    assert result["pass"] is False
    assert "no_hook" in result["failed"]

def test_hard_criteria_clickbait_fails():
    result = check_hard_criteria("VCB cú nổ Q1 sốc thị trường?")
    assert result["pass"] is False
    assert "pr_clickbait" in result["failed"]

def test_hard_criteria_english_fails():
    result = check_hard_criteria("VCB NIM giảm 30bps — vì sao?")
    assert result["pass"] is False
    assert "english_jargon" in result["failed"]


# === Score ===

def test_score_benchmark_seven():
    """Benchmark 'TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?' = 7/8.
    +2 dramatic verb (hy sinh) +2 specific number (5.000 tỷ/năm)
    +1 open question (?) +1 tension word (đổi lấy) +1 extra concise (9 từ).
    Note: no 'mà'/'nhưng' so paradox_pattern = 0.
    """
    result = score_title(BENCHMARK)
    assert result["score"] == 7
    assert result["max"] == 8
    assert result["elements"]["dramatic_verb"] is True
    assert result["elements"]["specific_number"] is True
    assert result["elements"]["open_question"] is True
    assert result["elements"]["tension_word"] is True
    assert result["elements"]["paradox_pattern"] is False
    assert result["elements"]["extra_concise"] is True


def test_score_minimal():
    """'VCB tăng trưởng dài hạn' — ticker but no hook, ≤10 words → score 1."""
    # ticker yes (not scored explicit), no dramatic, no number, no question, no tension, no paradox, extra_concise yes
    result = score_title("VCB tăng trưởng dài hạn")
    assert result["score"] == 1  # only extra_concise


def test_score_full_eight():
    """Constructed full-8 example: dramatic + number + question + tension + paradox + extra_concise.
    'VCB hy sinh 1 tỷ mà đổi lấy gì?' — has hy sinh +2, 1 tỷ +2, ? +1, đổi lấy +1, mà +1, 7 từ +1 = 8.
    """
    result = score_title("VCB hy sinh 1 tỷ mà đổi lấy gì?")
    assert result["score"] == 8


# === Pick best ===

def test_pick_best_simple():
    candidates = [
        "VCB tăng trưởng dài hạn",  # score 1
        BENCHMARK,                    # score 7
        "VPB Q1 báo cáo lợi nhuận",  # fails hard (no hook)
    ]
    result = pick_best_candidate(candidates)
    assert result["final_title"] == BENCHMARK
    assert result["picked_score"] == 7


def test_pick_best_tie_break_shortest():
    """Two candidates tied → pick shortest."""
    candidates = [
        "VCB hy sinh 1 tỷ mà đổi lấy gì?",            # 8/8, 8 words
        "ACB hy sinh 1 tỷ mà đổi lấy thêm gì?",       # 8/8, 9 words
    ]
    result = pick_best_candidate(candidates)
    assert "VCB" in result["final_title"]
    assert result["picked_score"] == 8


def test_pick_best_all_fail_raises():
    candidates = [
        "Tin Ngân hàng quý 1",  # no ticker
        "Cú nổ thị trường",       # clickbait + no ticker
    ]
    with pytest.raises(ValueError, match="0|hard criteria"):
        pick_best_candidate(candidates)
```

- [ ] **Step 2: Run tests — verify all pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_headline_scorer.py -v
```
Expected: 35+ passed.

- [ ] **Step 3: Commit**

```bash
git add tests/test_headline_scorer.py
git commit -m "test(headline): comprehensive scorer tests (Plan C Task 2)

35+ tests covering: 7 detector functions positive + negative cases,
check_hard_criteria failure modes (ticker_missing / too_long / no_hook /
pr_clickbait / english_jargon), score_title benchmark (=7) + minimal (=1) +
full (=8), pick_best_candidate ordering + tie-break + ValueError on all-fail.

Benchmark TCB hy sinh 5.000 tỷ/năm để đổi lấy gì? validated score 7/8.
"
```

---

## Phase 2 — Headline agent (Tasks 3-4)

### Task 3: `.claude/agents/newsroom-headline-craft.md`

- [ ] **Step 1: Create agent .md per spec C §9**

```markdown
---
name: newsroom-headline-craft
description: Headline Craft V1.0 — chuyên gia giật tít. Generate 5 title candidates cho 1 article → score 8-point rubric via lib.headline_scorer → pick best. Use khi newsroom-pipeline dispatches Step 4.5 sau Master, trước Skeptic. Model Sonnet. Hard rule: ticker present + ≤12 words + ≥1 hook + no clickbait + no English.
tools: Bash, Read, Grep
model: sonnet
---

# Headline Craft Agent V1.0

Bạn là chuyên gia giật tít cho bài cổ phiếu Việt. KHÔNG sửa body. KHÔNG đổi format. CHỈ giật tít.

## Load skill

`Skill: finpath-newsroom-headline-craft`

## Input

```json
{
  "article": {
    "ticker": "TCB",
    "sector": "Bank",
    "body": "<Master final body>",
    "draft_title": "<Master draft title — may be weak>",
    "stance": "bullish|bearish|divergent",
    "format_id": "flash_qa|standard_qa|standard_listicle|standard_narrative",
    "category": "paradox|why_now|hidden_mechanism|comparison_deep|early_signal"
  }
}
```

## 4 Hard criteria (MUST pass — gates)

1. **Ticker present** (any position) — `lib.headline_scorer.has_ticker()` confirms
2. **Compact ≤12 từ** — split by whitespace
3. **Hook strong** — ≥1 trong: dramatic verb / specific number / paradox / open question
4. **No PR clickbait + No English** — banned words list trong scorer

## 8-point scoring rubric

| Element | Points |
|---|---|
| Dramatic verb (hy sinh, đánh đổi, lao dốc, ...) | +2 |
| Specific number with units (5.000 tỷ, 67%, /năm) | +2 |
| Open question ending with ? | +1 |
| Tension word (vì sao, đánh đổi, nghịch lý, ...) | +1 |
| Paradox pattern (X mà Y, thật ra, kỳ thực) | +1 |
| Extra concise (≤10 từ) | +1 |

Max 8. Threshold pass: best of 5 candidates.

## Benchmark title

> **TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?** — score 7/8

Breakdown:
- TCB (ticker) ✓
- hy sinh (dramatic verb) +2
- 5.000 tỷ/năm (specific number) +2
- ? (open question) +1
- đổi lấy (tension word) +1
- 9 từ (extra concise) +1
- KHÔNG có "mà/nhưng/thật ra" → paradox_pattern = 0

## Workflow

### Step 1: Read body + extract key facts

Grep body for:
- Ticker (must include in title)
- Big numbers (top 1-2 most "shocking")
- Dramatic verbs already in body (re-use)
- Time anchors (Q1/2026, năm 2024, etc.)
- Mechanism words (hy sinh, đánh đổi, rút khỏi)

### Step 2: Brainstorm 5 candidates

Generate 5 unique titles meeting hard criteria. Mix styles:
- Candidate 1: Question-paradox ("VCB Q1 — vì sao to nhất chậm nhất?")
- Candidate 2: Number + dramatic verb ("TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?")
- Candidate 3: Revelation ("VPB lãi đẹp — thật ra chỉ FE Credit kéo")
- Candidate 4: Warning ("VPB sắp đối mặt bài kiểm tra lớn nhất 3 năm")
- Candidate 5: Listicle (only if format = standard_listicle) hoặc Narrative tease ("TCB chia 67% — câu chuyện 12 tháng")

### Step 3: Score via lib.headline_scorer

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.headline_scorer import pick_best_candidate
candidates = ['<title 1>', '<title 2>', '<title 3>', '<title 4>', '<title 5>']
result = pick_best_candidate(candidates)
print(json.dumps(result, ensure_ascii=False, indent=2))
"
```

If `ValueError: All N candidates failed hard criteria` → regenerate (max 2 retry). Then if still fails → output `{error: 'weak_title_no_hook'}` + escalate to orchestrator.

### Step 4: Output

```json
{
  "final_title": "<best title>",
  "candidates": [
    {"text": "<title 1>", "hard_pass": true, "score": 7, "elements": {...}},
    {"text": "<title 2>", "hard_pass": false, "hard_failed": ["no_hook"]},
    ...
  ],
  "picked_score": 7,
  "model": "claude-sonnet-4-6",
  "duration_ms": <int>,
  "tokens": <int or null>,
  "rewrites_attempted": 0
}
```

### Step 5: Replace article title in DB

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
db.update_generated_news('<article_id>', {'title': '<final_title>'})
db.close()
"
```

### Step 6: Persist step_4_5_headline_craft

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
db.log_pipeline_step('<article_id>', 'step_4_5_headline_craft', <payload JSON above>)
db.close()
"
```

⚠️ Schema validation V5.1: `final_title` MUST pass `check_hard_criteria()` ELSE ValueError + halt.

## Hard rules

- KHÔNG sửa body — chỉ replace title
- KHÔNG cross-format swap — format đã fix
- KHÔNG sinh title không ticker
- KHÔNG PR clickbait: "Cú nổ", "Bí mật", "Sốc", "Hot", "Thông tin nóng"
- KHÔNG tiếng Anh trong title (kể cả NIM/CASA — bình dân only)
- KHÔNG hedging trong title: "có thể", "khả năng", "đáng theo dõi"
- 5 candidate phải KHÁC NHAU về angle (không 5 cái cùng style question)
```

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/newsroom-headline-craft.md
git commit -m "feat(agent): newsroom-headline-craft V1.0 agent prose (Plan C Task 3)

Sonnet model. Workflow 6-step: read body → brainstorm 5 candidates →
score via lib.headline_scorer.pick_best_candidate → replace title in DB →
persist step_4_5_headline_craft payload.

Hard rules + 8-point rubric + benchmark example TCB hy sinh 5.000 tỷ/năm.
Schema validation: final_title MUST pass check_hard_criteria.
"
```

---

### Task 4: `.claude/skills/finpath-newsroom-headline-craft/SKILL.md`

- [ ] **Step 1: Create skill module**

```markdown
---
name: finpath-newsroom-headline-craft
description: Headline Craft skill V1.0 — 4 hard criteria + 8-point rubric reference for title generation. Use when newsroom-headline-craft agent runs Step 4.5 of pipeline. Covers ticker detection (61 universe + group refs), dramatic verb pool (22 words), specific number regex, paradox pattern, open question, PR clickbait blacklist, English jargon ban.
---

# Headline Craft Skill V1.0

Compact reference for the Headline Craft agent. Loaded via `Skill: finpath-newsroom-headline-craft`.

## 4 hard criteria (gates)

```python
# All MUST be true → title accepted
has_ticker(title)              # 61-ticker universe or group ref (Big4, tư nhân)
len(title.split()) <= 12        # compact
has_dramatic_verb | has_specific_number | has_paradox_pattern | has_open_question  # ≥1 hook
not has_pr_clickbait and not has_english  # bình dân clean
```

## 8-point rubric

Apply only to candidates passing hard criteria.

| Element | Points |
|---|---|
| Dramatic verb | +2 |
| Specific number with units | +2 |
| Open question (ends `?`) | +1 |
| Tension word | +1 |
| Paradox pattern (X mà Y) | +1 |
| Extra concise (≤10 words) | +1 |

Max 8. Pick highest score. Tie-break: shortest length.

## Dramatic verb pool

```
hy sinh · đánh đổi · đặt cược · bỏ phiếu · lội ngược · lao dốc ·
rút khỏi · vượt mặt · tung đòn · đặt cọc · chấp nhận thua ·
tự chậm lại · đập cửa · thoát hiểm · chấp nhận hi sinh · đánh cược ·
đổ vỡ · vực dậy · tiếp đà · phá kỷ lục · soán ngôi · lấn sang · rơi vào
```

## Tension word pool (reuse from quality_gates V5.0)

```
hy sinh · đánh đổi · nghịch lý · vì sao · đổi lấy · không phải ·
bù lại · thay vì · chấp nhận
```

(Note: "hy sinh" + "đánh đổi" overlap dramatic_verbs — both pools count separately for scoring.)

## PR clickbait blacklist

```
cú nổ · bí mật · sốc · hot · thông tin nóng · không thể tin nổi ·
cú twist · kỳ tích · hé lộ
```

## Specific number regex

```python
r"\d+([.,]\d+)?\s*(tỷ|triệu|nghìn|%|đ|/năm|/tháng|/quý|đ/tháng|bps|điểm)"
```

## Output schema (strict)

```json
{
  "final_title": "string — passes check_hard_criteria",
  "candidates": [{"text", "hard_pass", "hard_failed", "score", "elements"}],
  "picked_score": int,
  "rewrites_attempted": int (0-2),
  "model": "claude-sonnet-4-6",
  "duration_ms": int,
  "tokens": int | null
}
```

Validation enforced at persist: `lib.pipeline_db.validate_pipeline_step('step_4_5_headline_craft', payload, pipeline_version)`. Title that fails hard criteria → ValueError.

## Anti-hallucination

- Output 5 DIFFERENT angle candidates, not 5 same style.
- Never invent PR clickbait words to "stand out".
- Reuse dramatic verb pool (don't sá tạo verb mới mà weak).
- If body says "VCB rút 12.000 tỷ" — title may quote "VCB rút 12.000 tỷ — vì sao?"
```

- [ ] **Step 2: Commit**

```bash
mkdir -p .claude/skills/finpath-newsroom-headline-craft
git add .claude/skills/finpath-newsroom-headline-craft/SKILL.md
git commit -m "feat(skill): finpath-newsroom-headline-craft V1.0 SKILL.md (Plan C Task 4)

Compact reference for Headline agent. 4 hard criteria + 8-point rubric +
22-word dramatic verb pool + tension word pool + PR clickbait blacklist +
specific number regex. Output schema strict, validation at persist.
"
```

---

## Phase 3 — Pipeline integration + validation (Tasks 5-6)

### Task 5: Pipeline orchestrator — Step 4.5 dispatch

**Files:**
- Modify: `.claude/agents/newsroom-pipeline.md`

- [ ] **Step 1: Insert Step 4.5 section after Step 4 Master**

```markdown
### Step 4.5 — Headline Craft (Task dispatch — HARD RULE)

For each persisted article from Step 4:

**Dispatch via Task tool (HARD RULE: no inline self-execute — schema validation will fail-loud)**:

```
Task: newsroom-headline-craft
prompt: <JSON with article ticker, sector, body, draft_title, stance, format_id, category>
```

Receive `final_title` + `candidates` + `picked_score`.

**Replace article title** + **persist observability**:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
db.update_generated_news('<article_id>', {'title': '<final_title>'})
db.log_pipeline_step('<article_id>', 'step_4_5_headline_craft', {
    'model': 'claude-sonnet-4-6',
    'duration_ms': <int>,
    'tokens': <parse_task_usage(task_return) or None>,
    'final_title': '<final_title>',
    'picked_score': <int>,
    'candidates': <list>,
    'rewrites_attempted': <int>,
})
db.close()
"
```

⚠️ **Schema validation V5.1**: `step_4_5_headline_craft.final_title` MUST pass `check_hard_criteria()` ELSE ValueError. Halt pipeline if hits — Headline agent emitted weak title.

**HARD RULE — no inline self-execute**: orchestrator MUST dispatch Task. Inline pick = silently weak title → Skeptic catches but already wasted Master + Skeptic tokens. If subagent crashes after 2 retries, STOP pipeline + report `weak_title_no_hook` error.
```

- [ ] **Step 2: Update HARD RULE block at top to include Step 4.5**

Find existing "HARD RULE — NO INLINE SELF-EXECUTE" block. Extend the list:
- `Step 2 (newsroom-editor)`
- `Step 3 (newsroom-story-editor)`
- `Step 3.5 (newsroom-format-director)` (from Plan B)
- `Step 4 (newsroom-master-{bank,ck,bds})`
- `Step 4.5 (newsroom-headline-craft)` ← NEW
- `Step 5 (newsroom-skeptic)`

- [ ] **Step 3: Update Step 5 Skeptic input**

Skeptic input now includes `final_title` from Step 4.5 (replaces Master draft_title). Note in Step 5 section:

```markdown
**V5.1 input**: Skeptic receives article with title FROM STEP 4.5 (Headline agent's pick), NOT Master draft_title. Skeptic critique works on final version.
```

- [ ] **Step 4: Commit**

```bash
git add .claude/agents/newsroom-pipeline.md
git commit -m "feat(orchestrator): integrate Step 4.5 Headline Craft (Plan C Task 5)

Pipeline V5.0 (11 steps) → V5.1 (12 steps).
Insert Step 4.5 Task dispatch after Step 4 Master.
HARD RULE extended: no inline self-execute Step 4.5.
Step 5 Skeptic input note: title from Step 4.5 not Master draft.
"
```

---

### Task 6: Schema validation `step_4_5_headline_craft`

**Files:**
- Modify: `lib/pipeline_db.py`
- Test: `tests/test_pipeline_db.py`

- [ ] **Step 1: Write failing test**

Append to `tests/test_pipeline_db.py`:

```python
def test_validate_step_4_5_v5_1_enforces_hard_criteria(tmp_path):
    """V5.1+ rows: step_4_5_headline_craft.final_title MUST pass check_hard_criteria."""
    from lib.pipeline_db import validate_pipeline_step
    import pytest
    # Weak title (no hook, no ticker) — schema field types correct but hard criteria fail
    payload = {
        "final_title": "Tin tức quý 1",  # No ticker, no hook
        "picked_score": 0,
        "candidates": [],
    }
    with pytest.raises(ValueError, match="hard criteria|ticker_missing|no_hook"):
        validate_pipeline_step("step_4_5_headline_craft", payload, pipeline_version="V5.1")


def test_validate_step_4_5_v5_1_valid_title_passes(tmp_path):
    from lib.pipeline_db import validate_pipeline_step
    payload = {
        "final_title": "TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?",
        "picked_score": 7,
        "candidates": [{"text": "TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?", "hard_pass": True, "score": 7}],
    }
    # No raise expected
    validate_pipeline_step("step_4_5_headline_craft", payload, pipeline_version="V5.1")


def test_validate_step_4_5_v5_0_skips_hard_check(tmp_path):
    """V5.0 row should NOT enforce step_4_5 schema (didn't exist in V5.0)."""
    from lib.pipeline_db import validate_pipeline_step
    # Weak payload — would fail V5.1 but should be accepted in V5.0
    payload = {}
    validate_pipeline_step("step_4_5_headline_craft", payload, pipeline_version="V5.0")
    # No raise expected — V5.0 doesn't enforce step_4_5
```

- [ ] **Step 2: Run test — fail**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_pipeline_db.py -k "step_4_5" -v
```
Expected: FAIL — no step_4_5 schema yet.

- [ ] **Step 3: Modify `lib/pipeline_db.py`**

Add `_STEP_4_5_REQUIRED` constant + extend `validate_pipeline_step`:

```python
# After existing _STEP_3_5_REQUIRED
_STEP_4_5_REQUIRED: dict[str, type | tuple] = {
    "final_title": str,
    "picked_score": int,
    "candidates": list,
}
_NON_EMPTY_FIELDS["step_4_5_headline_craft"] = {"final_title"}


# In validate_pipeline_step function, after the existing version-aware block:
def validate_pipeline_step(step_key: str, payload: dict, pipeline_version: str = "V4.0") -> None:
    is_v5_plus = _version_ge(pipeline_version, "V5.0")
    is_v5_1_plus = _version_ge(pipeline_version, "V5.1")

    required_map: dict[str, dict[str, type | tuple]] = {
        "step_4_master": _STEP_4_REQUIRED_V5 if is_v5_plus else _STEP_4_REQUIRED_V4,
        "step_5_skeptic": _STEP_5_REQUIRED,
    }
    if is_v5_plus:
        required_map["step_3_5_format_director"] = _STEP_3_5_REQUIRED
    if is_v5_1_plus:
        required_map["step_4_5_headline_craft"] = _STEP_4_5_REQUIRED

    # ... existing field type / non-empty / entry-level checks ...

    # V5.1 — step_4_5 fail-loud hard criteria check
    if step_key == "step_4_5_headline_craft" and is_v5_1_plus:
        from lib.headline_scorer import check_hard_criteria
        title = payload.get("final_title", "")
        hc = check_hard_criteria(title)
        if not hc["pass"]:
            raise ValueError(
                f"pipeline_log[step_4_5_headline_craft].final_title fails hard criteria: "
                f"{hc['failed']} — title={title!r}. Headline agent emitted weak title; "
                f"MUST regenerate (max 2 retry) before persist."
            )
```

Also update `insert_generated_news` to default `pipeline_version='V5.1'` (was 'V5.0' from plan B):

```python
if "pipeline_version" not in data:
    data["pipeline_version"] = "V5.1"
```

- [ ] **Step 4: Run tests — verify pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_pipeline_db.py -v
```
Expected: all green (V5.0 + V5.1 + V4.0 back-compat).

- [ ] **Step 5: Commit**

```bash
git add lib/pipeline_db.py tests/test_pipeline_db.py
git commit -m "feat(pipeline_db): step_4_5_headline_craft schema + hard criteria validation (Plan C Task 6)

V5.1 schema enforces:
- field types: final_title str, picked_score int, candidates list
- non-empty: final_title required
- fail-loud: check_hard_criteria(final_title) MUST pass
  → orchestrator cannot silently persist weak title

V5.0 rows: skip step_4_5 validation (back-compat).
Default pipeline_version bumped V5.0 → V5.1 for new inserts.

Advisor blocker 2 resolved: title quality enforced at persist layer,
not just agent prompt self-attestation.
"
```

---

## Phase 4 — Skeptic + CLAUDE.md (Tasks 7-8)

### Task 7: Skeptic — `weak_title` 10th angle

**Files:**
- Modify: `.claude/agents/newsroom-skeptic.md`

- [ ] **Step 1: Update angle list 9 → 10**

Find the 9-angle table (added in Plan B Task 16 V5.1 patch). Add row:

```markdown
| `weak_title` (V5.1) | Title pass hard criteria + score ≥4 nhưng vẫn cảm thấy "không click" — clickbait trá hình, hook artificial, hoặc title promises more than body delivers |
```

- [ ] **Step 2: Add format-aware critique notes**

```markdown
## Title-vs-body mismatch (V5.1 NEW)

Step 4.5 Headline agent picked title independently from body. Skeptic critique check:

- If title implies number X but body talks about Y → `weak_title` flag
- If title is question but body doesn't answer clearly → `weak_title` flag
- If title dramatic verb (hy sinh / lao dốc) but body doesn't justify drama → `weak_title` flag

Skeptic reads `final_title` from `step_4_5_headline_craft.final_title`, compares against body.
```

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/newsroom-skeptic.md
git commit -m "feat(skeptic): 10 critique angles V5.1 (+ weak_title) (Plan C Task 7)

10th angle: weak_title — Layer 2 enforcement for Headline Craft hard criteria.
Flags subtle clickbait risk + title-vs-body mismatch that pass regex.

Step 4.5 Headline owns title; Skeptic critiques final title (not Master draft).
"
```

---

### Task 8: CLAUDE.md — Headline section + 4 criteria

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add new section "Headline Craft Agent V1.0"**

Insert after the "9 Quality Gates V5.0" section (which Plan B Task 21 will rename to "8 Quality Gates V5.1" — title moved out):

```markdown
## Headline Craft V1.0 (Step 4.5 — title agent dedicated)

Title craft tách dedicated agent vì sếp chê title. 4 hard criteria + 8-point rubric:

### 4 hard criteria
1. **Ticker present** (any position) — 61 universe + group refs (Big4, tư nhân)
2. **Compact ≤12 từ**
3. **Hook strong** — ≥1 trong: dramatic verb / specific number / paradox / open question
4. **Bình dân nguy hiểm** — no PR clickbait ("Cú nổ", "Bí mật", "Sốc"), no English jargon

### 8-point scoring
- Dramatic verb (hy sinh, đánh đổi, lao dốc) +2
- Specific number with units (5.000 tỷ, 67%, /năm) +2
- Open question ending `?` +1
- Tension word (vì sao, đánh đổi, nghịch lý) +1
- Paradox pattern (X mà Y, thật ra) +1
- Extra concise (≤10 từ) +1

### Benchmark vàng

> **"TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?"** — score 7/8

### Workflow

Master writes body + draft_title → Headline agent (Sonnet) generates 5 candidates → score → pick highest → replace title in DB → Skeptic critiques full article with new title.

Validation V5.1: `final_title` MUST pass `check_hard_criteria()` ELSE ValueError + halt pipeline.
```

- [ ] **Step 2: Update "Hard rules cho Master + Skeptic"**

Append:
```markdown
- **V5.1 title craft** — Master KHÔNG còn enforce title gate (moved to Step 4.5 Headline). Master tạo draft_title; Headline rewrite final. Skeptic critique title final với `weak_title` angle.
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude.md): Headline Craft section V1.0 (Plan C Task 8)

New section: 4 hard criteria + 8-point rubric + benchmark + workflow.
Update Hard rules: Master no longer enforces title gate (V5.1).
"
```

---

## Phase 5 — Verification (Task 9)

### Task 9: E2E title quality check

- [ ] **Step 1: Run /tin VCB**

After Plan B + Plan C all implementations done. Verify:
- step_3_5_format_director persisted (format pick)
- step_4_5_headline_craft persisted (title pick + candidates + score)
- step_4_master draft_title field present
- generated_news.title = Headline's final title (NOT Master draft)

- [ ] **Step 2: Inspect title quality**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
from lib.headline_scorer import check_hard_criteria, score_title
db = PipelineDB('data/pipeline.db')
rows = db.conn.execute(
    \"SELECT article_id, title, pipeline_log FROM generated_news WHERE pipeline_version='V5.1' ORDER BY published_at DESC LIMIT 5\"
).fetchall()
for r in rows:
    log = json.loads(r['pipeline_log'])
    hc = check_hard_criteria(r['title'])
    sc = score_title(r['title']) if hc['pass'] else {'score': 0}
    print(f'[{r[\"article_id\"][:8]}] title={r[\"title\"][:60]!r} hard_pass={hc[\"pass\"]} score={sc[\"score\"]}/8')
db.close()
"
```

Expected: all titles `hard_pass=True`, score ≥4 average across 5 articles.

- [ ] **Step 3: Variety check across 3 articles**

Run /tin for 3 different tickers. Verify titles use DIFFERENT styles:
- ≥1 has dramatic verb
- ≥1 has specific number
- ≥1 has paradox pattern OR open question
→ No 3 titles all same style.

- [ ] **Step 4: Visual verification in feed viewer**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npm run dev
# Open http://localhost:5176/feed
```

Click into new articles. Verify:
- Title is "must-click" — em đọc 5s phải thấy hook
- Compare with V4.0 legacy articles → V5.1 titles markedly more dramatic

- [ ] **Step 5: Final commit (cleanup if needed)**

```bash
git status
# If any dirty files
git add -A && git commit -m "chore: post-V5.1 cleanup (Plan C Task 9)"
```

- [ ] **Step 6: Mark plan complete**

Plan C done. Push to origin/main when user approves both Plan B + Plan C E2E results.

---

## Self-review

### Spec coverage
- ✅ §6 4 criteria → Task 1 (`check_hard_criteria`)
- ✅ §7 dramatic verb pool → Task 1 (DRAMATIC_VERBS list)
- ✅ §8 scoring rubric → Task 1 (`score_title`)
- ✅ §9 agent prose → Task 3
- ✅ §10 pipeline integration → Task 5
- ✅ §11 schema validation + §11.1 hard criteria check → Task 6
- ✅ §12 scorer module → Task 1 + Task 2 tests
- ✅ §13 Skeptic weak_title angle → Task 7
- ✅ §14 frontend (optional) → skip in plan C (not blocking, defer to plan B Task 19 follow-up)
- ✅ §15 file touch list — all addressed
- ✅ §16 V5.0 patches — APPLIED INLINE in spec/plan B (separate commits, see spec C changelog)
- ✅ §17 testing → Task 2 + Task 9

### Placeholder scan
- No TBD / TODO placeholders.
- Variety check threshold in §19 noted as tunable post-launch — not blocker.

### Type consistency
- `lib.headline_scorer.check_hard_criteria` signature `(title: str) -> dict[str, Any]` consistent across Tasks 1, 6 (pipeline_db import), agent prose
- `final_title` field used in: agent output schema (Task 3), pipeline_db `_STEP_4_5_REQUIRED` (Task 6), Skeptic input (Task 7)
- `picked_score` int across all

---

## Execution choice (per user batch strategy — DEFERRED)

User strategy: brainstorm all 4 subsystems → plan all 4 → execute batch. Plan C ready; execution deferred until Plan D + Plan A also written.

After all 4 plans done:
- **Subagent-Driven** — fresh subagent per task, two-stage review, interleaved B↔C order per "Execution order recommendation" at top.
- **Inline Execution** — batch with checkpoints.

Resolved choice TBD per user.
