# Headline Craft Agent — Design Spec V1.0

**Date**: 2026-05-12
**Author**: Brainstormed with em (Claude)
**Status**: Draft — pending user review before plan
**Subsystem**: C (Headline Craft) from initial 5-subsystem feedback
**Depends on / conflicts with**: V5.0 Format Diversity spec `docs/superpowers/specs/2026-05-11-master-article-format-diversity-design.md` — title_pattern logic moves from Format Director → Headline agent.

---

## 1. Goal

Tạo dedicated **Headline Craft agent** chuyên giật tít sao cho **đọc tiêu đề là muốn click vào bài**. Title chiếm 90% quyết định reader có đọc bài hay không — title yếu thì insight Master viết sâu cỡ nào cũng phí.

Sau spec này:
- Master tập trung 100% vào body + draft title (không lo title craft).
- Headline agent (Step 4.5 mới) generate 5 candidates → score → pick best.
- 4 hard criteria + scoring 8 điểm enforce "must-click" quality.

## 2. Problem statement

Feedback sếp: **"bị chê title"**. Hiện tại (V5.0 plan):
- Format Director chọn `title_pattern` per format (4 patterns).
- Master viết title bám pattern.
- Gate 4 enforce pattern structure.

Pattern OK nhưng pattern ≠ CRAFT. "Vì sao to nhất lại đi chậm nhất?" pattern đúng (có `?`) nhưng so với "TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?" thì kém hook hẳn:
- Thiếu ticker → SEO + recognition yếu
- Không dramatic verb
- Không specific big number
- Vague (to nhất = ai?)

→ Title craft phải tách dedicated agent.

## 3. Benchmark example — "TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?"

User định nghĩa benchmark này = vàng. Breakdown:

| Element | Có | Note |
|---|---|---|
| Ticker | ✅ TCB | Đầu title — eye-catch ngay |
| Dramatic verb | ✅ hy sinh | Tension implied |
| Specific big number | ✅ 5.000 tỷ/năm | Stakes rõ ràng |
| Open question hook | ✅ để đổi lấy gì? | Curiosity instant |
| Ngắn | ✅ 9 từ | Compact |
| Bình dân | ✅ no jargon, no English | Accessible |
| Bình dân nguy hiểm | ✅ stakes massive + verb dramatic | Sharp tension trong simple words |

## 4. Out of scope (defer)

- Headline override CROSS-FORMAT (vd flash_qa → standard_narrative swap based on title). Format đã fix khi Format Director chốt; Headline craft TRONG format đã pick.
- Multi-language title (English variant cho social). MVP Vietnamese only.
- A/B test title ngoài viewer. Defer separate spec.
- Social-platform-specific title (Twitter character limit, FB hook style). MVP single canonical title.

## 5. Architecture overview

### Pipeline V5.1 (12 steps, +1 so V5.0)

```
Step 1: Crawler
Step 1.5: Market Snapshot
Step 2: Editor V1
Step 3: Story Editor
Step 3.5: Format Director (V5.0)
         ← V5.1 PATCH: remove title_pattern logic (move to Headline)
Step 4: Master sector — write body + DRAFT title
         ← V5.1 PATCH: Master removes title_pattern gate (gate 4 V5.0 removed for Master)
         ↓
Step 4.5: Headline Craft (subagent newsroom-headline-craft NEW, Sonnet)
         Generate 5 candidates → score → pick best → replace Master draft title
         ↓
Step 5: Skeptic — critique full article with NEW title
Step 6: Render
Step 7-9: Phase H1
```

### Conflict resolution với V5.0 plan B

| Plan B item | Patch V5.1 | Impact |
|---|---|---|
| `data/format_registry.yaml` title_pattern fields | Keep field BUT Format Director không enforce ở step 3.5 | Headline agent reads từ registry để biết "this is flash_qa" → may use as soft constraint |
| `lib/quality_gates.py` `check_title_per_format` | Remove from `check_all_v5` universal call | Master không bị gate cản khi viết draft title |
| `.claude/agents/newsroom-format-director.md` Step 1 (title_pattern in output) | Remove title_pattern from output schema | Format Director output cleaner |
| `.claude/agents/newsroom-master-*.md` Step 8 9-gate check | Drop title_pattern gate from check_all_v5 invocation | Master 8 gates (was 9) — title pure-quality decided by Headline |
| Gate count V5.0: 9 gates → V5.1: 8 gates + Headline-specific gates | Title moves to Headline domain | Pipeline cleaner separation |
| New `lib.headline_scorer` module | NEW V5.1 | Scoring logic for 4 criteria + 8-point rubric |

## 6. 4 Hard criteria

| # | Criteria | Detection method |
|---|---|---|
| 1 | **Ticker present** (any position) | Regex match against 61-ticker universe + group references (Big4, tư nhân top). MUST contain ≥1. |
| 2 | **Compact ≤12 từ** | Word count split by whitespace. Reject >12. |
| 3 | **Hook strong** — ≥1 trong 4: dramatic verb OR specific big number OR paradox "X mà Y" OR open question | Regex match against pools (see §7). Reject if 0. |
| 4 | **Bình dân nguy hiểm** (soft) | No English jargon (reuse `quality_gates.ENGLISH_JARGON`). No PR clickbait ("Cú nổ", "Bí mật", "Sốc"). Skeptic `weak_title` angle catches subtle fluff. |

### 4.5 Voice Layer title_stance (V5.0 V4 rule) — owned by Headline V5.1

Voice Layer V4 (title stance — title chắc nịch, không treo câu hỏi mở không trả lời) trong spec V5.0 originally enforced ở Master + Format Director. V5.1: Headline agent owns này. Enforcement:

- Hard criteria #3 "Hook strong" requires ≥1 trong: dramatic verb / specific number / paradox / open question. Trong đó open question được tách ra (nếu chọn) sẽ MUST có body trả lời rõ — Skeptic `weak_title` flag nếu title hỏi mà body không trả lời.
- Tension words pool (reused từ V5.0 spec §6) đóng góp +1 điểm score → encourage stance-forward titles.
- PR clickbait detection (hard criteria #4) catches fake-stance titles ("Cú nổ", "Bí mật").

→ title_stance không là gate riêng nữa — implicit trong 4 hard criteria của Headline.

## 7. Dramatic verb pool

```python
DRAMATIC_VERBS = [
    "hy sinh", "đánh đổi", "đặt cược", "bỏ phiếu", "lội ngược",
    "lao dốc", "rút khỏi", "vượt mặt", "tung đòn", "đặt cọc",
    "chấp nhận thua", "tự chậm lại", "đập cửa", "thoát hiểm",
    "chấp nhận hi sinh", "đặt cọc", "đánh cược", "đổ vỡ",
    "vực dậy", "tiếp đà", "phá kỷ lục", "soán ngôi",
]
```

## 8. Scoring rubric (8 max)

```python
def score_title(title: str) -> dict:
    score = 0
    has_dramatic = any(v in title.lower() for v in DRAMATIC_VERBS)
    has_specific_number = bool(re.search(r"\d+([.,]\d+)?\s*(tỷ|triệu|nghìn|%|đ|/năm|/tháng|/quý)", title))
    has_open_question = title.rstrip().endswith("?")
    has_tension_word = any(w in title.lower() for w in TITLE_TENSION_WORDS)
    has_paradox_pattern = bool(re.search(r"\bmà\b|\bnhưng\b|\bthực ra\b|\bthật ra\b", title.lower()))
    is_extra_concise = len(title.split()) <= 10

    if has_dramatic: score += 2
    if has_specific_number: score += 2
    if has_open_question: score += 1
    if has_tension_word: score += 1
    if has_paradox_pattern: score += 1
    if is_extra_concise: score += 1

    return {"score": score, "max": 8, "elements": {...}}
```

### Threshold

- Headline agent generates 5 candidates.
- Each candidate must pass 4 hard criteria first (gates).
- Among candidates that pass, pick **highest score**. Tie → pick shortest.
- If all 5 fail hard criteria → regenerate (max 2 retry). If still fail → escalate `weak_title_no_hook` error.

## 9. Headline Craft Agent — `.claude/agents/newsroom-headline-craft.md`

### Frontmatter

```yaml
---
name: newsroom-headline-craft
description: Headline Craft V1.0 — chuyên gia giật tít. Generate 5 title candidates cho 1 article → score 8-point rubric → pick best. Use khi newsroom-pipeline dispatches Step 4.5 sau Master, trước Skeptic. Model Sonnet.
tools: Bash, Read, Grep
model: sonnet
---
```

### Input

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

### Workflow

1. **Read body** — extract key facts: ticker, big numbers, mechanism, time anchor.
2. **Brainstorm 5 candidates** — each MUST:
   - Contain ticker (any position)
   - ≤12 từ
   - Have ≥1 hook element (dramatic verb / specific number / paradox / open question)
3. **Score each via 8-point rubric** (see §8).
4. **Reject candidates failing hard criteria** (recompute if needed).
5. **Pick highest score** — tie-break by shortest length.
6. **Output**:

```json
{
  "final_title": "TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?",
  "candidates": [
    {"text": "...", "score": 7, "elements": {...}, "rejected_reason": null},
    {"text": "...", "score": 6, "elements": {...}, "rejected_reason": null},
    {"text": "...", "score": 5, "elements": {...}, "rejected_reason": null},
    {"text": "...", "score": 4, "elements": {...}, "rejected_reason": "missing dramatic verb"},
    {"text": "...", "score": 3, "elements": {...}, "rejected_reason": null}
  ],
  "picked_score": 7,
  "model": "claude-sonnet-4-6",
  "duration_ms": 6200,
  "tokens": 980
}
```

### Hard rules

- KHÔNG sửa body (chỉ replace title).
- KHÔNG dùng cross-format swap (format đã fix).
- KHÔNG sinh title không có ticker.
- KHÔNG dùng PR clickbait words: "Cú nổ", "Bí mật", "Sốc", "Hot", "Thông tin nóng".
- KHÔNG dùng tiếng Anh trong title (kể cả abbreviations như NIM/CASA — vì title hiển thị cho public, phải bình dân).
- KHÔNG hedging trong title: "có thể", "khả năng", "đáng theo dõi".

## 10. Pipeline integration — Step 4.5

### Dispatch from `.claude/agents/newsroom-pipeline.md`

Insert sau Step 4 Master (per-article), trước Step 5 Skeptic:

```markdown
### Step 4.5 — Headline Craft (Task dispatch)

For each persisted article from Step 4:

**Dispatch via Task tool** (HARD RULE: no inline self-execute):

```
Task: newsroom-headline-craft
prompt: {"article": {ticker, sector, body, draft_title, stance, format_id, category}}
```

Receive `final_title` + `candidates` array + score.

**Replace article title**:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
db.update_generated_news('<article_id>', {'title': '<final_title>'})
db.close()
"
```

**Observability**:

```python
db.log_pipeline_step(article_id, "step_4_5_headline_craft", {
    "model": "claude-sonnet-4-6",
    "started_at": ...,
    "duration_ms": ...,
    "tokens": parse_task_usage(task_return),
    "final_title": final_title,
    "picked_score": int,
    "candidates": [...],  # all 5 for transparency
    "rewrites_attempted": int,
})
```

Schema validation: `step_4_5_headline_craft.final_title` non-empty, `picked_score >= 0`.
```

## 11. Schema validation — `lib/pipeline_db.py` patch

Add `_STEP_4_5_REQUIRED`:

```python
_STEP_4_5_REQUIRED: dict[str, type | tuple] = {
    "final_title": str,
    "picked_score": int,
    "candidates": list,
}
_NON_EMPTY_FIELDS["step_4_5_headline_craft"] = {"final_title"}
```

`validate_pipeline_step` extends to handle step_4_5 in V5.1+ rows (V5.0 + V4.0 skip — back-compat).

### 11.1 Fail-loud hard criteria check at persist (Advisor blocker)

Schema "field exists + non-empty" KHÔNG đủ — agent có thể emit `final_title = "VCB Q1 báo cáo tài chính"` (fail ALL 4 hard criteria) và pass validation. Đây chính là failure mode V4.0 → V5.0 fail-loud designed to prevent.

`validate_pipeline_step` step_4_5 branch MUST also enforce hard criteria:

```python
def validate_pipeline_step(step_key: str, payload: dict, pipeline_version: str = "V4.0") -> None:
    # ... existing logic ...
    if step_key == "step_4_5_headline_craft" and _version_ge(pipeline_version, "V5.1"):
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

Validation runs at every `log_pipeline_step` call → orchestrator cannot silently persist weak title. If hits → orchestrator surfaces ValueError → pipeline halt with diagnostic.

## 12. `lib/headline_scorer.py` — NEW module

```python
"""Headline scoring module — 8-point rubric for title craft.

Exposes pure functions for ticker detection + dramatic verb match + specific
number regex + paradox structure detect + open question check + length count.

Headline Craft agent reads this scoring logic in its prompt; can also be
called code-level for fallback / testing.
"""
from __future__ import annotations
import re
from typing import Any

from lib.quality_gates import TITLE_TENSION_WORDS  # reuse

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

# Reuse 61-ticker universe — import from routing or hardcode
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
    """Check title contains at least 1 ticker or group reference."""
    for t in ALL_TICKERS:
        if re.search(rf"\b{t}\b", title):
            return True
    for g in GROUP_REFS:
        if g in title:
            return True
    return False


def has_specific_number(title: str) -> bool:
    return bool(re.search(r"\d+([.,]\d+)?\s*(tỷ|triệu|nghìn|%|đ|/năm|/tháng|/quý|đ/tháng|bps)", title, re.IGNORECASE))


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
    """Run 4 hard criteria. Returns {pass: bool, failed: [str]}."""
    failed = []
    if not has_ticker(title):
        failed.append("ticker_missing")
    if len(title.split()) > 12:
        failed.append("too_long")
    if not (has_dramatic_verb(title) or has_specific_number(title) or has_paradox_pattern(title) or has_open_question(title)):
        failed.append("no_hook")
    if has_pr_clickbait(title):
        failed.append("pr_clickbait")
    if has_english(title):
        failed.append("english_jargon")
    return {"pass": len(failed) == 0, "failed": failed}


def score_title(title: str) -> dict[str, Any]:
    """8-point rubric. Returns {score, max, elements}."""
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

    Returns {final_title, picked_score, all_scored}.
    Raises ValueError if 0 candidates pass hard criteria.
    """
    scored = []
    for c in candidates:
        hard = check_hard_criteria(c)
        scored_entry = {
            "text": c,
            "hard_pass": hard["pass"],
            "hard_failed": hard["failed"],
        }
        if hard["pass"]:
            s = score_title(c)
            scored_entry.update(s)
        scored.append(scored_entry)

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

## 13. Skeptic V5.1 — `weak_title` critique angle (NEW)

Add 10th angle to Skeptic V5.0 (already 9 angles):

| Angle | When to use |
|---|---|
| `weak_title` (NEW V5.1) | Title pass hard criteria + score ≥4 nhưng vẫn cảm thấy "không click" — clickbait trá hình, hook artificial, hoặc lệch nội dung |

Skeptic compares `final_title` vs body — flag if title promises more than body delivers (clickbait risk).

## 14. Frontend — title rendering unchanged

`ArticleMeta.title` field tiếp tục dùng nguyên. Add observability render trong right column:

```tsx
// FormatPickPanel.tsx hoặc new HeadlineCraftPanel.tsx
<details>
  <summary>Tít được giật</summary>
  <ul>
    {candidates.map(c => (
      <li className={c.text === final_title ? 'font-bold' : ''}>
        {c.text} — score {c.score}/8 {c.text === final_title && '✓ chọn'}
      </li>
    ))}
  </ul>
</details>
```

Optional — chỉ show trong pipeline log debug view. Public reader chỉ thấy final title.

## 15. File touch list

| File | Action | Lines est |
|---|---|---|
| `lib/headline_scorer.py` | NEW | ~150 |
| `.claude/agents/newsroom-headline-craft.md` | NEW | ~200 |
| `.claude/skills/finpath-newsroom-headline-craft/SKILL.md` | NEW | ~80 |
| `.claude/agents/newsroom-pipeline.md` | MODIFY | +60 (insert Step 4.5 dispatch) |
| `.claude/agents/newsroom-master-{bank,ck,bds}.md` (× 3) | MODIFY | -20 each (remove title gate from check_all_v5 call) |
| `.claude/agents/newsroom-skeptic.md` | MODIFY | +20 (weak_title angle, 10 total) |
| `lib/pipeline_db.py` | MODIFY | +20 (step_4_5 schema) |
| `lib/quality_gates.py` | MODIFY | -30 (remove title_pattern from check_all_v5 universal call; keep functions for back-compat tests) |
| `lib/render_compare_feed.py` | MODIFY | +30 (optional headline panel data) |
| `web/src/types.ts` | MODIFY | +15 (HeadlineCraftData type) |
| `web/src/components/HeadlineCraftPanel.tsx` (optional) | NEW | ~70 |
| `data/format_registry.yaml` | MODIFY | -20 (remove title_pattern + title_must_contain* fields — Headline owns) |
| `CLAUDE.md` | MODIFY | +30 (Headline agent rules, 4 criteria, 8-point rubric) |
| `tests/test_headline_scorer.py` | NEW | ~250 |
| `tests/test_pipeline_db.py` | MODIFY | +40 (step_4_5 validation tests) |
| Plan B (`docs/superpowers/plans/2026-05-11-master-article-format-diversity.md`) | PATCH | Tasks 6, 9, 13-15 update — remove title_pattern from Format Director + Master gate |
| Spec B (`docs/superpowers/specs/2026-05-11-master-article-format-diversity-design.md`) | PATCH | §7 gate count 9 → 8, §8 Format Director output schema cleanup |

Total: ~7 new + ~9 modify + 2 patch (V5.0 docs) ≈ 800-1000 LOC.

## 16. Patches required to V5.0 (plan B) — APPLIED INLINE

**Advisor blocker resolution (2026-05-12)**: per user strategy "brainstorm all → plan all → execute" (zero implement-and-delete), patches to V5.0 spec + plan B are applied INLINE concurrent với spec C commit. Plan B will reflect Headline-owns-title từ Task 1 yaml — không cần plan C re-patch sau.

Single canonical patch list (merged from prior §15 + §16):

| V5.0 location | V5.1 patch |
|---|---|
| Spec V5.0 §7 9 gates table | 8 gates (drop `title_pattern` per-format gate — Headline owns title) |
| Spec V5.0 §7 `check_all_v5` signature | `check_all_v5(body, format_id, stance)` — drop `title` arg |
| Spec V5.0 §8 Format Director output schema | Drop `title_pattern` field, drop `title_must_contain*` fields. Keep `length_range`, `bullets_count`, `structure`. |
| Spec V5.0 §9 `data/format_registry.yaml` schema | Remove `title_*` fields from each format spec |
| Spec V5.0 §11 Master Step 8 | 8 gates not 9 (title gate removed) |
| Spec V5.0 §11 Master Step 9 persist | Note Step 4.5 Headline replaces title post-Master (see plan C §10) |
| Spec V5.0 §12 Skeptic angles | 9 → 10 (add `weak_title`) |
| Spec V5.0 §15 file touch | Mark `lib/quality_gates.py` removes `check_title_per_format` |
| Plan B Task 1 `data/format_registry.yaml` | Remove `title_pattern`, `title_must_contain`, `title_must_contain_one_of`, `title_tension_words`, `title_must_match_regex` from all 4 format specs |
| Plan B Task 6 `check_title_per_format` | Remove function entirely. `check_all_v5` signature drops title arg. |
| Plan B Task 6 test file `tests/test_quality_gates.py` | Remove all `test_per_format_title_*` tests. Update `test_check_all_v5_dispatches_per_format` to drop title check. |
| Plan B Task 9 `newsroom-format-director.md` | Remove title_pattern from output schema + 5-step flow Step 4 (was about title — now Headline). |
| Plan B Task 13-15 Master agents `newsroom-master-*.md` | check_all_v5 invocation drops title. Step 8 = 8 gates. Add note "title comes from Step 4.5 Headline post-Master". |
| Plan B Task 16 Skeptic `newsroom-skeptic.md` | 10 angles not 9 (add `weak_title`) |

## 17. Testing strategy

### Unit tests `tests/test_headline_scorer.py`
- `has_ticker` for all 61 universe + group refs
- `has_dramatic_verb` for all pool words + negative case
- `has_specific_number` for "5.000 tỷ" / "67%" / "3 năm" + negative
- `has_paradox_pattern` for "X mà Y" + "thật ra"
- `has_open_question` for `?` ending
- `has_pr_clickbait` for banned words
- `check_hard_criteria` for benchmark title (pass) + various failing cases
- `score_title` benchmark "TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?" → score 7
- `pick_best_candidate` with 5 candidates → highest score wins tie-break shortest

### Integration tests
- Dispatch newsroom-headline-craft with fixture article → verify final_title passes hard criteria
- Full pipeline /tin VCB → verify step_4_5_headline_craft persisted + title replaced

### Visual verification
- Generate 3 articles in 1 run → verify 3 different title styles (variety)
- Compare V5.0 article titles vs V5.1 — measure subjective improvement

## 18. Rollout phases

### Phase 1 — Scorer module + tests
- `lib/headline_scorer.py` + `tests/test_headline_scorer.py`

### Phase 2 — Patch plan B (V5.0 docs)
- Spec V5.0 §7, §8, §9, §11, §12 patches
- Plan B Tasks 6, 13-15, 16 patches
- Remove title gate from quality_gates.check_all_v5

### Phase 3 — Headline agent
- `newsroom-headline-craft.md` + SKILL.md
- Pipeline orchestrator Step 4.5 insertion
- Schema validation step_4_5

### Phase 4 — Skeptic + frontend
- Skeptic 10 angles
- (Optional) HeadlineCraftPanel.tsx
- CLAUDE.md update

### Phase 5 — Verification
- E2E /tin run, verify variety + quality improvement

Estimated effort: ~5-7 ngày after V5.0 implementation done (or done concurrently if V5.0 not yet implemented).

## 19. Open questions / deferred

1. **Title regenerate threshold** — currently 2 retry. Tune sau khi production data.
2. **Dramatic verb pool extension** — initial 22 verbs. Add từ pool sếp/user feedback (planned Phase 5+).
3. **Group reference rules** — comparison_deep articles có thể title chỉ Big4 (group), không specific ticker. Currently `has_ticker()` accepts groups → may be too lax. Consider strict mode: comparison articles MUST có ≥1 ticker specific + group ref.
4. **Score weights tuning** — current 2/2/1/1/1/1. Reassess sau 20+ bài production.
5. **Headline agent self-bias** — risk Sonnet luôn favor 1 style. Add variety check window (last 3 titles same ticker) → encourage style swap if monotone.

## 20. Spec changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-05-12 | Initial draft. 4 hard criteria + 8-point rubric + Step 4.5 placement. Patches required to V5.0 spec/plan B. |
