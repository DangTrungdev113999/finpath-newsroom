# Newsroom V4.0 Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Steps use `- [ ]`.

**Goal:** Transform Newsroom V3.6 → V4.0: bài có "luận điểm" thay vì liệt kê; title-as-hook; 1 paragraph + 3-7 substantive bullets pattern; multi-article output (3 briefs = 3 files); 8-section right column user-readable; KB cleanup to Frameworks tree only.

**Architecture:** Schema migration (SQLite + brief JSON) → quality gates rewrite (drop mechanism count + Cần để ý, add title-as-hook + body pattern) → skill content rewrite → agent prompt updates → render layer rewrite (multi-article + 8 sections) → E2E `/tin MBB` verification.

**Tech Stack:** Python 3.13 + uv, sqlite3, pytest, React 18 + TS + Vite, Tailwind. No new deps.

**Spec ref:** `docs/superpowers/specs/2026-05-08-newsroom-v4-redesign.md`. CLAUDE.md V3.6 rules to update for V4.0.

**Project root:** `/Users/trungdt/Desktop/Stream Intelligent/`

**Predecessor commit:** tag `phase-4-llm-agents` (V3.6 baseline).

---

## File Structure

### Modified
```
data/pipeline.schema.sql           # +public_slug column
lib/quality_gates.py               # rewrite V3.6 → V4.0 (5 gates)
lib/slugify.py                     # NEW — hook → URL slug
lib/render_compare_feed.py         # rewrite ~200 → ~450 lines (multi-article + 8 sections)
tests/test_quality_gates.py        # rewrite tests for V4.0
tests/test_slugify.py              # NEW
tests/test_render_compare_feed.py  # update for multi-article + 8 sections

.claude/skills/finpath-newsroom-story-editor/SKILL.md
.claude/skills/finpath-newsroom-master-bank/SKILL.md
.claude/skills/finpath-newsroom-master-bank/references/bullet-examples.md  # NEW
.claude/skills/finpath-newsroom-skeptic/SKILL.md

.claude/agents/newsroom-story-editor.md
.claude/agents/newsroom-master-bank.md
.claude/agents/newsroom-skeptic.md
.claude/agents/newsroom-pipeline.md
.claude/commands/tin.md            # $1 → $ARGUMENTS

web/src/types.ts                   # V4.0 schema
web/src/lib/parseArticle.ts        # update if needed
web/src/components/RightColumn.tsx # 8 sections
web/src/components/CrawlFunnel.tsx # narrative + vai trò labels
web/src/components/QuestionOptions.tsx     # NEW
web/src/components/DataTrail.tsx           # NEW

CLAUDE.md                          # V4.0 rules
```

### Deleted
```
kb/bank/history/                   # 10 files
kb/bank/per-ticker/                # 21 files
kb/bank/frameworks/bank-annual-reports-master-reference.md
kb/bank/frameworks/bank-ceo-cfo-master-reference.md
kb/bank/frameworks/bank-dhdcd-master-reference.md
kb/bank/frameworks/bank-ma-master-reference.md
kb/bank/frameworks/bank-research-reports-master-reference.md
kb/bank/frameworks/banking-ma-vietnam-master-reference.md
kb/bank/frameworks/research-reports-index.md
kb/bank/frameworks/research-vcbs-banking-2025.md
```

### Kept (4 files only)
```
kb/bank/frameworks/bank-industry-master-reference.md
kb/bank/frameworks/bank-nim-cycle.md
kb/bank/frameworks/bank-npl-reading.md
kb/bank/frameworks/bank-target-vs-actual-pattern.md
```

---

## Tasks

### Task 1: SQLite schema migration — `public_slug` column

**Files:**
- Modify: `data/pipeline.schema.sql`
- Manual migration of existing `data/pipeline.db`

- [ ] **Step 1: Update schema file**

Open `data/pipeline.schema.sql` and add to `generated_news` table definition (after `pipeline_log TEXT,`):

```sql
  public_slug         TEXT,
```

Plus add unique index after `CREATE INDEX idx_generated_ticker_published ...`:

```sql
CREATE UNIQUE INDEX IF NOT EXISTS idx_generated_public_slug ON generated_news(public_slug);
```

Note: NULL allowed for migration backward compat. Will be NOT NULL in fresh inserts after V4.0.

- [ ] **Step 2: Migrate existing DB**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import sqlite3
conn = sqlite3.connect('data/pipeline.db')
cur = conn.execute(\"PRAGMA table_info(generated_news)\")
cols = [r[1] for r in cur.fetchall()]
if 'public_slug' not in cols:
    conn.execute('ALTER TABLE generated_news ADD COLUMN public_slug TEXT')
    conn.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_generated_public_slug ON generated_news(public_slug)')
    conn.commit()
    print('Migrated: public_slug added')
else:
    print('public_slug already exists, skip')
conn.close()
"
```

Expected: "Migrated: public_slug added" or "skip" if already exists.

- [ ] **Step 3: Verify**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import sqlite3
conn = sqlite3.connect('data/pipeline.db')
cur = conn.execute('SELECT name FROM pragma_table_info(\"generated_news\")')
cols = [r[0] for r in cur.fetchall()]
print('public_slug present:', 'public_slug' in cols)
conn.close()
"
```

Expected: `public_slug present: True`.

- [ ] **Step 4: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add data/pipeline.schema.sql && git commit -m "feat(db): add public_slug column to generated_news for V4.0 multi-article URLs"
```

---

### Task 2: lib/slugify.py + tests (TDD)

**Files:**
- Create: `lib/slugify.py`
- Test: `tests/test_slugify.py`

- [ ] **Step 1: Write failing test**

Create `tests/test_slugify.py`:

```python
"""Tests for lib.slugify — Vietnamese hook → URL-safe slug."""
import pytest
from lib.slugify import slugify_hook


def test_simple_question_hook():
    title = "Vì sao to nhất lại đi chậm nhất?"
    assert slugify_hook(title) == "vi-sao-to-nhat-lai-di-cham-nhat"


def test_declarative_paradox_hook():
    title = "TCB chia cổ tức 67% kỷ lục — nhưng phần lớn không phải tiền mặt"
    result = slugify_hook(title)
    assert result.startswith("tcb-chia-co-tuc-67-ky-luc-nhung-phan-lon")
    assert len(result) <= 60


def test_strips_diacritics():
    assert slugify_hook("Đánh đổi tốc độ lấy độ bền") == "danh-doi-toc-do-lay-do-ben"


def test_truncates_to_60_chars():
    long = "a " * 100
    result = slugify_hook(long)
    assert len(result) <= 60


def test_truncate_strips_trailing_partial_word():
    # 60-char cutoff in middle of a word — must drop partial word
    title = "VCB target 2026 chỉ 5 phần trăm Vì sao ngân hàng to nhất đi chậm"
    result = slugify_hook(title)
    assert len(result) <= 60
    assert not result.endswith("-")
    # Must end with full word, not "ch" or "cha"
    assert "-" in result
    last_word = result.rsplit("-", 1)[-1]
    assert len(last_word) >= 2


def test_drops_special_chars():
    assert slugify_hook("Đầu tư @ 2026!") == "dau-tu-2026"


def test_consecutive_hyphens_collapsed():
    assert slugify_hook("a   b   —   c") == "a-b-c"


def test_empty_falls_back():
    assert slugify_hook("") == "untitled"
    assert slugify_hook("???") == "untitled"
```

- [ ] **Step 2: Run failing**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_slugify.py -v
```

Expected: ImportError.

- [ ] **Step 3: Write `lib/slugify.py`**

```python
"""Slugify Vietnamese hook titles to URL-safe slugs (max 60 chars)."""
from __future__ import annotations
import re
import unicodedata


def slugify_hook(text: str, max_len: int = 60) -> str:
    """Convert Vietnamese title hook to URL-safe slug.

    Rules:
    - Lowercase
    - Strip Vietnamese diacritics (NFKD + drop combining)
    - Replace non-alphanumeric with hyphen
    - Collapse consecutive hyphens
    - Trim leading/trailing hyphens
    - Truncate to max_len chars
    - Drop trailing partial word after truncate (split by - and drop last fragment if cut mid-word)
    - Empty result → "untitled"
    """
    if not text:
        return "untitled"

    # Strip diacritics
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    # Vietnamese-specific: đ → d, Đ → d (NFKD doesn't split these)
    text = text.replace("đ", "d").replace("Đ", "d")
    text = text.lower()
    # Replace non-alphanumeric with hyphen
    text = re.sub(r"[^a-z0-9]+", "-", text)
    # Collapse + trim hyphens
    text = re.sub(r"-+", "-", text).strip("-")

    if len(text) <= max_len:
        return text or "untitled"

    # Truncate + drop partial trailing word
    truncated = text[:max_len]
    # If cut in middle of word, drop the last fragment (split at last hyphen)
    if not text[max_len:max_len + 1].startswith("-") and "-" in truncated:
        truncated = truncated.rsplit("-", 1)[0]
    truncated = truncated.rstrip("-")
    return truncated or "untitled"
```

- [ ] **Step 4: Run tests pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_slugify.py -v
```

Expected: 8 PASS.

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add lib/slugify.py tests/test_slugify.py && git commit -m "feat(lib): slugify_hook — Vietnamese title → URL slug + 8 TDD tests"
```

---

### Task 3: Quality Gates V4.0 (TDD — rewrite)

**Files:**
- Modify: `lib/quality_gates.py` — drop `check_mechanism_count` + `check_can_de_y_narrative`, add `check_body_pattern` + `check_title_as_hook`
- Modify: `tests/test_quality_gates.py` — drop V3.6 mechanism + Cần để ý tests, add V4.0 body pattern + title hook tests

- [ ] **Step 1: Rewrite test file**

Replace `tests/test_quality_gates.py` content:

```python
"""Tests for lib.quality_gates V4.0 — 5 gates."""
import pytest
from lib.quality_gates import (
    check_no_english_jargon,
    check_word_count,
    check_body_pattern,
    check_title_as_hook,
    check_no_metadata_leak,
    check_all,
)


# === Gate 1: 0% English jargon ===

def test_no_english_jargon_passes_clean_vietnamese():
    body = "Lợi nhuận trước thuế đạt **11.803 tỷ đồng**, tăng 9% so cùng kỳ. Nợ xấu 0,62%."
    assert check_no_english_jargon(body)["pass"] is True


def test_no_english_jargon_fails_on_NPL():
    assert check_no_english_jargon("NPL 1,05% tăng nhẹ.")["pass"] is False


def test_no_english_jargon_fails_on_momentum():
    assert check_no_english_jargon("TCB có momentum mạnh.")["pass"] is False


def test_no_english_jargon_allows_proper_nouns():
    body = "Vietcombank và Techcombank công bố KQKD Q1/2026. ĐHĐCĐ ngày 25/4."
    assert check_no_english_jargon(body)["pass"] is True


# === Gate 2: Word count 200-400 ===

def test_word_count_in_range_passes():
    assert check_word_count(" ".join(["w"] * 300))["pass"] is True


def test_word_count_too_long_fails():
    assert check_word_count(" ".join(["w"] * 450))["pass"] is False


def test_word_count_too_short_fails():
    assert check_word_count(" ".join(["w"] * 100))["pass"] is False


# === Gate 3: Body pattern — 1 paragraph + 3-7 bullets + closing ===

VALID_BODY = """Đại hội cổ đông Techcombank 25/4 thông qua chia cổ tức tổng 67% — nhưng câu chuyện thật là chiến lược ngược chiều thị trường, ngân hàng đang đánh đổi.

- **Cổ tức 67% tách thành hai phần khác bản chất**: 7% tiền mặt tương đương 4.960 tỷ đồng, còn 60% là cổ phiếu thưởng phát hành từ lợi nhuận giữ lại — không rút đồng tiền mặt nào khỏi ngân hàng.

- **Lần đầu lịch sử BĐS giảm xuống 28,9%**: bán lẻ và doanh nghiệp vừa nhỏ tăng 33% so cùng kỳ, đạt 395 nghìn tỷ — bù vào chỗ trống bằng phân khúc rủi ro thấp hơn.

- **CEO thừa nhận hy sinh 5.000 tỷ lợi nhuận tiềm năng mỗi năm**: đánh đổi này nhằm duy trì 3 lớp phòng thủ thanh khoản theo chuẩn quốc tế mới — chiến lược dài hạn không phải phản xạ chu kỳ.

TCB phù hợp nhà đầu tư giá trị nắm trên 12 tháng — không phù hợp lướt sóng kỳ vọng đà ngắn hạn.
"""


def test_body_pattern_valid_passes():
    assert check_body_pattern(VALID_BODY)["pass"] is True


def test_body_pattern_no_opening_paragraph_fails():
    body = """- **Bullet 1**: opening missing này phải là paragraph mới đúng pattern V4.0 thật sự.
- **Bullet 2**: another bullet với content đầy đủ ít nhất hai mươi từ để qua check substantive.
- **Bullet 3**: third bullet cũng đầy đủ content và bold highlight đặt đầu cho rõ.

Closing sentence here."""
    result = check_body_pattern(body)
    assert result["pass"] is False
    assert "opening" in result["reason"].lower()


def test_body_pattern_too_few_bullets_fails():
    body = """Opening paragraph đầy đủ ba mươi từ trở lên mô tả sự kiện và đặt setup cho phần thân bài, làm rõ tension.

- **Bullet 1**: chỉ có một bullet không đủ pattern V4.0 cần ba bullet trở lên cho mechanism.

Closing.
"""
    assert check_body_pattern(body)["pass"] is False


def test_body_pattern_too_many_bullets_fails():
    bullets = "\n".join(
        [f"- **Bold {i}**: bullet content đầy đủ ít nhất hai mươi từ để pass substantive check trong gate này." for i in range(1, 9)]
    )
    body = f"Opening paragraph đầy đủ ba mươi từ mô tả sự kiện và đặt setup cho thân bài rõ ràng tension.\n\n{bullets}\n\nClosing.\n"
    assert check_body_pattern(body)["pass"] is False


def test_body_pattern_bullet_too_short_fails():
    body = """Opening paragraph đầy đủ ba mươi từ trở lên mô tả sự kiện và đặt setup cho thân bài làm rõ tension.

- **Bold**: short.
- **Bold 2**: cũng ngắn.
- **Bold 3**: vẫn ngắn.

Closing.
"""
    assert check_body_pattern(body)["pass"] is False


def test_body_pattern_bullet_no_bold_fails():
    body = """Opening paragraph đầy đủ ba mươi từ trở lên mô tả sự kiện và đặt setup cho thân bài làm rõ tension đó.

- Plain bullet content đầy đủ hai mươi từ nhưng không có bold highlight cần thiết theo V4.0 pattern.
- Plain bullet 2 cũng không có bold highlight nên fail check substantive vì không emphasis keypoint.
- Plain bullet 3 tương tự thiếu bold tag.

Closing.
"""
    assert check_body_pattern(body)["pass"] is False


def test_body_pattern_can_de_y_section_fails():
    body = """Opening paragraph đầy đủ ba mươi từ trở lên mô tả sự kiện và đặt setup cho thân bài làm rõ tension.

- **Bold 1**: bullet content đầy đủ ít nhất hai mươi từ để pass substantive check trong gate này.
- **Bold 2**: bullet content cũng đủ hai mươi từ để pass substantive check thực sự đấy.
- **Bold 3**: bullet cuối cùng cũng đủ content và bold highlight đầu cho rõ ràng.

## Cần để ý

Caveat narrative.

Closing.
"""
    result = check_body_pattern(body)
    assert result["pass"] is False
    assert "cần để ý" in result["reason"].lower() or "can de y" in result["reason"].lower()


# === Gate 4: Title-as-hook ===

def test_title_question_passes():
    assert check_title_as_hook("Vì sao ngân hàng to nhất đi chậm nhất?")["pass"] is True


def test_title_paradox_dash_passes():
    assert check_title_as_hook("TCB hy sinh 5.000 tỷ — đổi lấy gì?")["pass"] is True


def test_title_summary_fails():
    assert check_title_as_hook("TCB Q1/2026 lãi 8.900 tỷ tăng 22%")["pass"] is False


def test_title_with_tension_word_passes():
    assert check_title_as_hook("VCB chấp nhận tăng trưởng chậm — đánh đổi rủi ro")["pass"] is True


def test_title_dash_no_tension_fails():
    assert check_title_as_hook("TCB Q1/2026 — kết quả mới nhất")["pass"] is False


# === Gate 5: No metadata leak ===

def test_no_metadata_leak_fails_on_strategic_shift():
    assert check_no_metadata_leak("Đây là tin strategic-shift quan trọng.")["pass"] is False


def test_no_metadata_leak_passes_clean():
    assert check_no_metadata_leak("Đây là tin chuyển hướng chiến lược.")["pass"] is True


# === check_all ===

def test_check_all_returns_5_gates():
    result = check_all("Test body.", title="Test?")
    assert set(result.keys()) == {
        "no_english_jargon", "word_count", "body_pattern",
        "title_as_hook", "no_metadata_leak"
    }
```

- [ ] **Step 2: Run failing tests**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_quality_gates.py -v
```

Expected: many failures — old functions exist but no `check_body_pattern` / `check_title_as_hook` / new `check_all` signature.

- [ ] **Step 3: Rewrite `lib/quality_gates.py`**

```python
"""5 quality gates V4.0 — mechanical pass/fail checker for Master Bank articles.

Gates:
  1. no_english_jargon — 0% từ tiếng Anh trong content
  2. word_count — 200-400 hard cap
  3. body_pattern — 1 opening paragraph + 3-7 substantive bullets + 1 closing
  4. title_as_hook — title contains '?' or '—' + tension word
  5. no_metadata_leak — không enum tags trong content
"""
from __future__ import annotations
import re
from typing import Any

ENGLISH_JARGON = {
    # Bank abbreviations
    "npl", "nim", "casa", "car", "irb", "rwa", "esop", "sme", "nii", "ldr",
    "llr", "cof", "tpdn", "yoy", "qoq", "ytd", "roe", "roa",
    "basel",
    # Common English finance/news words
    "trade-off", "tradeoff", "anchor", "relevant", "confirm", "pattern",
    "breaking", "momentum", "defensive", "catalyst", "symbolic", "metric",
    "event", "story", "scenario", "target", "portfolio", "buffer",
    "stress test", "arithmetic", "coverage", "opportunity cost",
}

METADATA_TAGS = [
    "strategic-shift", "risk_highlight", "insight_type", "critique angle",
    "data_skepticism", "historical_analog", "alt_interpretation",
    "insight_wrong", "execution_unfaithful",
    "paradox", "why_now", "hidden_mechanism", "comparison_deep", "early_signal",
    "low_writeability", "low_insight_potential", "dup_event", "dup_angle_recent",
]

TITLE_TENSION_WORDS = [
    "hy sinh", "đánh đổi", "nghịch lý", "vì sao", "đổi lấy",
    "không phải", "bù lại", "thay vì", "chấp nhận",
]


def _strip_skeptic_section(body: str) -> str:
    """Remove Skeptic '## Góc nhìn ngược' section if present."""
    parts = re.split(
        r"^#{2,3}\s+G[óo]c\s+nh[iì]n\s+ng[ưu]?[ợo]?c\s*$",
        body, flags=re.MULTILINE,
    )
    return parts[0]


def _strip_pipeline_log(body: str) -> str:
    return re.sub(r"<details>.*?</details>", "", body, flags=re.DOTALL)


def _clean(body: str) -> str:
    return _strip_skeptic_section(_strip_pipeline_log(body))


def check_no_english_jargon(body: str) -> dict[str, Any]:
    cleaned = _clean(body).lower()
    found = [j for j in ENGLISH_JARGON if re.search(r"\b" + re.escape(j) + r"\b", cleaned)]
    if found:
        return {"pass": False, "reason": f"Banned jargon: {', '.join(found)}"}
    return {"pass": True, "reason": ""}


def check_word_count(body: str) -> dict[str, Any]:
    cleaned = _clean(body).strip()
    n = len(cleaned.split())
    if n < 200:
        return {"pass": False, "reason": f"Too short: {n} words (need 200-400)"}
    if n > 400:
        return {"pass": False, "reason": f"Too long: {n} words (need 200-400)"}
    return {"pass": True, "reason": ""}


def check_body_pattern(body: str) -> dict[str, Any]:
    """Gate 3 — body structure: 1 opening paragraph + 3-7 substantive bullets + 1 closing.

    NO '## Cần để ý' section allowed. Bullets must be ≥20 words with ≥1 bold.
    """
    cleaned = _clean(body).strip()

    # Check no `## Cần để ý` heading
    if re.search(r"^#{2,3}\s+C[ầa]n\s+đ[ểe]?\s+ý", cleaned, flags=re.MULTILINE):
        return {"pass": False, "reason": "Contains '## Cần để ý' section — drop it in V4.0"}

    # Split into blocks separated by blank lines
    blocks = [b.strip() for b in re.split(r"\n\s*\n", cleaned) if b.strip()]
    if len(blocks) < 3:
        return {"pass": False, "reason": f"Need ≥3 blocks (opening + bullets + closing), got {len(blocks)}"}

    opening = blocks[0]
    closing = blocks[-1]
    middle = blocks[1:-1]

    # Opening: must be paragraph (not bullet), ≥30 words
    if opening.startswith(("- ", "* ")):
        return {"pass": False, "reason": "Opening block must be paragraph, not bullet"}
    if len(opening.split()) < 30:
        return {"pass": False, "reason": f"Opening paragraph too short: {len(opening.split())} words (need ≥30)"}

    # Closing: 1 sentence, not bullet
    if closing.startswith(("- ", "* ")):
        return {"pass": False, "reason": "Closing must be sentence, not bullet"}
    if closing.startswith("#"):
        return {"pass": False, "reason": "Closing must not be heading"}

    # Middle: each block must be a bullet group OR single bullet
    # Collect all bullets from middle blocks
    bullets: list[str] = []
    for block in middle:
        for line in block.split("\n"):
            line = line.strip()
            if line.startswith(("- ", "* ")):
                bullets.append(line[2:].strip())
            elif line:
                # Non-bullet line in middle = continuation of previous bullet (multi-line) — append
                if bullets:
                    bullets[-1] += " " + line
                else:
                    return {"pass": False, "reason": f"Non-bullet, non-opening text in middle: '{line[:60]}'"}

    if len(bullets) < 3:
        return {"pass": False, "reason": f"Need 3-7 bullets, got {len(bullets)}"}
    if len(bullets) > 7:
        return {"pass": False, "reason": f"Need 3-7 bullets, got {len(bullets)}"}

    # Each bullet: ≥20 words AND ≥1 bold (`**...**`)
    for i, b in enumerate(bullets, start=1):
        words = len(b.split())
        if words < 20:
            return {"pass": False, "reason": f"Bullet {i} too short: {words} words (need ≥20)"}
        if "**" not in b:
            return {"pass": False, "reason": f"Bullet {i} missing bold (**...**) highlight"}

    return {"pass": True, "reason": ""}


def check_title_as_hook(title: str) -> dict[str, Any]:
    """Gate 4 — title contains '?' OR '—' + tension word.

    Tension words: hy sinh, đánh đổi, nghịch lý, vì sao, đổi lấy,
                   không phải, bù lại, thay vì, chấp nhận.
    """
    if not title:
        return {"pass": False, "reason": "Title empty"}
    title_lc = title.lower()
    if "?" in title:
        return {"pass": True, "reason": ""}
    if "—" in title:
        for word in TITLE_TENSION_WORDS:
            if word in title_lc:
                return {"pass": True, "reason": ""}
        return {"pass": False, "reason": "Title has '—' but no tension word"}
    return {"pass": False, "reason": "Title is summary — needs '?' or '—' + tension word"}


def check_no_metadata_leak(body: str) -> dict[str, Any]:
    cleaned = _clean(body).lower()
    found = [t for t in METADATA_TAGS if t.lower() in cleaned]
    if found:
        return {"pass": False, "reason": f"Metadata leak: {', '.join(found)}"}
    return {"pass": True, "reason": ""}


def check_all(body: str, title: str = "") -> dict[str, dict[str, Any]]:
    """Run all 5 V4.0 gates. Pass title for Gate 4."""
    return {
        "no_english_jargon": check_no_english_jargon(body),
        "word_count": check_word_count(body),
        "body_pattern": check_body_pattern(body),
        "title_as_hook": check_title_as_hook(title),
        "no_metadata_leak": check_no_metadata_leak(body),
    }
```

- [ ] **Step 4: Run tests pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_quality_gates.py -v
```

Expected: ~22 PASS.

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add lib/quality_gates.py tests/test_quality_gates.py && git commit -m "feat(lib): quality_gates V4.0 — drop mechanism+caveat, add body_pattern+title_hook (5 gates)"
```

---

### Task 4: KB cleanup — delete 39 files

**Files:**
- Delete: 10 in `kb/bank/history/`
- Delete: 21 in `kb/bank/per-ticker/`
- Delete: 8 in `kb/bank/frameworks/` (non-Frameworks-tree files)

- [ ] **Step 1: Delete history + per-ticker directories**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && rm -rf kb/bank/history kb/bank/per-ticker
```

- [ ] **Step 2: Delete 8 non-Frameworks-tree files in frameworks/**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && cd kb/bank/frameworks && rm -f \
  bank-annual-reports-master-reference.md \
  bank-ceo-cfo-master-reference.md \
  bank-dhdcd-master-reference.md \
  bank-ma-master-reference.md \
  bank-research-reports-master-reference.md \
  banking-ma-vietnam-master-reference.md \
  research-reports-index.md \
  research-vcbs-banking-2025.md
```

- [ ] **Step 3: Verify final state — 4 files only**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && ls -1 kb/bank/frameworks/
echo "---"
echo "Total: $(find kb/bank -name '*.md' | wc -l | tr -d ' ')"
```

Expected output:
```
bank-industry-master-reference.md
bank-nim-cycle.md
bank-npl-reading.md
bank-target-vs-actual-pattern.md
---
Total: 4
```

If any other file shows, delete it manually.

- [ ] **Step 4: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add -A kb/ && git commit -m "chore(kb): V4.0 cleanup — keep only 4 Frameworks tree files (delete 39)"
```

---

### Task 5: Update CLAUDE.md for V4.0

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Read current CLAUDE.md**

Read `/Users/trungdt/Desktop/Stream Intelligent/CLAUDE.md` to find the "5 Quality Gates V3.6" + body pattern sections.

- [ ] **Step 2: Replace 5 quality gates section**

Find the section starting with `## 5 Quality Gates V3.6 (HARD CAP cho bài Master)` and replace the entire 5-gate list with:

```markdown
## 5 Quality Gates V4.0 (HARD CAP cho bài Master)

Bài fail 1/5 gate → tự reject + rewrite, KHÔNG persist:

1. **0% từ tiếng Anh** trong content (kể cả viết tắt NPL/NIM/CASA/CAR/Basel/IRB/RWA/ESOP, kể cả từ thông dụng trade-off/anchor/momentum/defensive/symbolic/catalyst/breaking/portfolio/buffer/stress test/metric/event/story/scenario/target). Exception: tên riêng (Vietcombank, Techcombank, Q1/Q2, NHNN, ĐHĐCĐ) + Pipeline log internal toggle.
2. **Word count 200-400 từ HARD CAP** body chính. 401+ → reject + rewrite.
3. **Body pattern**: 1 opening paragraph (≥30 từ, không bullet) + 3-7 substantive bullets (each ≥20 từ + ≥1 bold highlight `**...**`) + 1 closing sentence (không bullet, không heading). KHÔNG `## Cần để ý` section.
4. **Title-as-hook**: Title chứa `?` HOẶC `—` + ≥1 tension word: `hy sinh`, `đánh đổi`, `nghịch lý`, `vì sao`, `đổi lấy`, `không phải`, `bù lại`, `thay vì`, `chấp nhận`.
5. **No metadata leak** — KHÔNG có `strategic-shift` / `risk_highlight` / `insight_type` / `Critique angle` / 5-category enum (paradox/why_now/hidden_mechanism/comparison_deep/early_signal) trong bài đọc.

Heading hợp lệ DUY NHẤT trong body Master: KHÔNG có heading. Skeptic append `## Góc nhìn ngược` riêng (không tính vào gates Master).
```

- [ ] **Step 3: Update related sections**

Search for "Cần để ý" in CLAUDE.md — remove all references trong rules (still OK trong glossary nếu có context historical).

- [ ] **Step 4: Add slug + multi-article note**

Append to CLAUDE.md a new section before "Notion publish — DEFER MVP":

```markdown
## Multi-article output V4.0

Story Editor pick 1-3 brief → Master generate 1 article per brief → 1 markdown file per article.

- File naming: `<TICKER>-<YYYYMMDD>-<HHMM>-<hook-slug>.md`
- `hook-slug` = title hook slugified (lowercase + ASCII + hyphen + max 60 chars). Implementation: `lib/slugify.py:slugify_hook()`.
- DB: `generated_news.public_slug` UNIQUE column.
- Manifest entry uses `id = public_slug`.
- URL: `/article/<public_slug>`.

3 briefs = 3 separate articles, each = 1 card on IndexPage.

## Body pattern V4.0 (overview)

```
[Title hook — question or declarative paradox]

[Opening paragraph 30-60 từ — sự kiện + tension/setup, có thể end với câu hỏi]

- **Bold highlight 1**: bullet ≥20 từ với connector + mechanism reasoning
- **Bold highlight 2**: bullet ≥20 từ
- **Bold highlight 3**: bullet ≥20 từ
- ... up to 7 bullets

[Closing — 1 câu phân loại NĐT phù hợp]
```

KHÔNG `## Cần để ý` section. Caveats compress vào closing hoặc inline trong bullets.
```

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add CLAUDE.md && git commit -m "docs: update CLAUDE.md to V4.0 rules (5 gates + body pattern + multi-article slug)"
```

---

### Task 6: Master Bank skill — bullet examples + V4.0 workflow

**Files:**
- Create: `.claude/skills/finpath-newsroom-master-bank/references/bullet-examples.md`
- Modify: `.claude/skills/finpath-newsroom-master-bank/SKILL.md`

- [ ] **Step 1: Create bullet-examples.md**

```bash
mkdir -p "/Users/trungdt/Desktop/Stream Intelligent/.claude/skills/finpath-newsroom-master-bank/references"
```

Create `.claude/skills/finpath-newsroom-master-bank/references/bullet-examples.md`:

```markdown
# Bullet Substance Examples — V4.0

Mỗi bullet trong body Master phải:
1. Bold = keypoint paradox / milestone / contrastive (KHÔNG chỉ data point)
2. Body bullet kết nối 2-3 facts thành argument (không tóm tắt)
3. Có connector: `vì`, `do đó`, `đánh đổi`, `bù lại`, `nhưng`, `trong khi`, `thay vì`, `nhờ`, `để`
4. Có data anchor cụ thể (số + đơn vị + so sánh)
5. Reader học mechanism: quy định / phép tính / chu kỳ / cạnh tranh / lịch sử / customer behavior

---

## ❌ BAD bullets (passes mechanical gate ≥20 từ + bold, fails substance)

❌ Data summary tóm tắt fact:
> `**TCB Q1/2026 lãi 8.900 tỷ**: tăng 22,6% so cùng kỳ, cao nhất lịch sử quý 1, tổng thu nhập hoạt động 13.700 tỷ tăng 17,8%.`

→ Đây là tóm tắt fact, không phải mechanism. Reader không học được "vì sao".

❌ Data + nguyên nhân generic:
> `**CASA 37,9%**: giảm từ đỉnh 40,4% cuối 2025, do chu kỳ Tết hết tiền nên khách rút tiền không kỳ hạn để chi tiêu Tết.`

→ Có data + nguyên nhân, nhưng vẫn data-driven, không connect với insight.

❌ Liệt kê data points:
> `**Vốn điều lệ 113.738 tỷ đồng**: TCB nâng vốn từ 70.862 tỷ qua chia cổ phiếu thưởng + ESOP, vượt VCB 99.674 tỷ.`

→ Chỉ liệt kê số. Không giải thích "vì sao" hành động này có ý nghĩa.

---

## ✅ GOOD bullets (mechanism + paradox + contrastive)

✅ Paradox + contrastive unpacking:
> `**Cổ tức 67% tách thành hai phần khác bản chất**: 7% tiền mặt tương đương 4.960 tỷ đồng, còn 60% là cổ phiếu thưởng phát hành từ lợi nhuận giữ lại — không rút đồng tiền mặt nào khỏi ngân hàng.`

→ Bold = keypoint paradox ("tách hai phần khác bản chất"). Body unpacks → reader hiểu cơ chế kế toán, không chỉ thấy "67% lớn".

✅ Milestone + cause-and-effect + structural reason:
> `**Lần đầu lịch sử BĐS giảm xuống 28,9%**: bán lẻ + doanh nghiệp vừa nhỏ tăng 33% so cùng kỳ, đạt 395 nghìn tỷ — bù vào chỗ trống. CEO Jens Lottner thừa nhận ngân hàng "hy sinh" khoảng 5.000 tỷ lợi nhuận tiềm năng/năm so với cho vay phân khúc rủi ro cao, để duy trì 3 lớp phòng thủ thanh khoản.`

→ Bold = milestone ("lần đầu < 30%"). Bullet kết nối: BĐS giảm + bán lẻ tăng + CEO admit trade-off + structural reason (3 layer phòng thủ). 4 facts thành 1 luận điểm.

✅ Counter-intuitive + thay vì pattern:
> `**TCB chọn tăng vốn qua bút toán thay vì phát hành mới**: chia cổ phiếu thưởng từ lợi nhuận giữ lại không tạo dòng tiền mới, không pha loãng cổ đông hiện hữu — đánh đổi tốc độ huy động lấy giữ tỷ lệ kiểm soát của nhóm sáng lập.`

→ Bold = decision contrast. Body unpacks "thay vì" mechanism → reader hiểu trade-off cấu trúc cổ đông.

---

## Recipe để viết 1 bullet substantive

Step 1 — Chọn keypoint:
- Paradox: 2 thứ ngược chiều cùng lúc
- Milestone: lần đầu / cao nhất / thấp nhất
- Contrastive: thay vì X, làm Y
- Quote anchor: CEO/Chủ tịch nói gì

Step 2 — Bold keypoint thành sentence ngắn (≤15 từ).

Step 3 — Body bullet kết nối 2-3 facts:
- Số cụ thể (bao gồm đơn vị + so sánh YoY/QoQ/peers)
- Connector kéo argument flow
- Mechanism reasoning (1 trong 5: quy định / phép tính / chu kỳ / cạnh tranh / customer behavior)

Step 4 — Total ≥20 words, đảm bảo reader học được cái gì mới.

---

## Anti-patterns to avoid

- KHÔNG bullet = data summary thuần
- KHÔNG bullet < 20 words
- KHÔNG bullet không bold
- KHÔNG bullet 100% là số (% và tỷ đồng), thiếu mechanism reasoning
- KHÔNG bullet bắt đầu bằng `**TCB:**` hoặc `**Q1:**` (label only) — bold phải là keypoint phrase
```

- [ ] **Step 2: Read current Master Bank SKILL.md**

```bash
cat "/Users/trungdt/Desktop/Stream Intelligent/.claude/skills/finpath-newsroom-master-bank/SKILL.md" | head -60
```

- [ ] **Step 3: Update Master Bank SKILL.md (replace V3.6 rules with V4.0)**

Open `.claude/skills/finpath-newsroom-master-bank/SKILL.md`. Find section `## 5 Rules CRITICAL` (or similar — V3.6 rules section) and replace with:

```markdown
## 5 Rules CRITICAL V4.0 (cannot skip)

**Rule 1 — 0% từ tiếng Anh** — kể cả viết tắt NPL/NIM/CASA/CAR/Basel/IRB/RWA/ESOP, kể cả thông dụng trade-off/anchor/momentum/defensive. Dùng tiếng Việt thuần. Bảng mapping: see `references/jargon-mapping.md`.

**Rule 2 — Title-as-hook** (NEW V4.0):
- Title MUST chứa `?` (câu hỏi) HOẶC `—` + ≥1 tension word: `hy sinh`, `đánh đổi`, `nghịch lý`, `vì sao`, `đổi lấy`, `không phải`, `bù lại`, `thay vì`, `chấp nhận`
- ❌ Bad: `TCB Q1/2026 lãi 8.900 tỷ tăng 22%` (summary)
- ✅ Good: `TCB hy sinh 5.000 tỷ — đổi lấy gì?` (declarative paradox)
- ✅ Good: `Vì sao to nhất lại đi chậm nhất?` (question)

Master nhận `chosen_question` từ Story Editor → có quyền re-phrase thành declarative hook clickable hơn.

**Rule 3 — Body pattern V4.0** (NEW):

```
[Title hook]

[Opening paragraph ≥30 từ — sự kiện + tension/setup, có thể end với câu hỏi]

- **Bold keypoint 1**: substantive bullet ≥20 từ với connector + mechanism
- **Bold keypoint 2**: bullet ≥20 từ
- **Bold keypoint 3**: bullet ≥20 từ
- ... up to 7 bullets

[Closing — 1 câu phân loại NĐT]
```

⚠️ **Đọc `references/bullet-examples.md` TRƯỚC khi viết body** — examples concrete bad vs good bullets.

KHÔNG `## Cần để ý` section (V3.6 dropped). Caveats merge vào bullets hoặc closing.

**Rule 4 — Word count 200-400 HARD CAP** body chính. 401+ → reject + rewrite.

**Rule 5 — No metadata leak** — KHÔNG `strategic-shift` / `risk_highlight` / 5 category enum (paradox / why_now / etc) trong content. Variety_guard_angle persist là free-text Vietnamese, không enum.
```

Then find section `## Workflow 9 bước` and update Bước 1 (Validate brief) + Bước 7 (Write article) + Bước 8 (Self-check):

For **Bước 1 — Validate brief V4.0**:
```markdown
1. **Validate brief V4.0** — ticker in universe, brief có:
   - `deep_question_options` (array of 2-3 questions với category + pick_hint)
   - `angle_label`, `angle_narrative`, `why_chosen_narrative`
   - `insight_hypothesis`
   
   Nếu schema sai → `Master_decision: reject_no_data`, `Master_note: invalid_brief_schema_v4`.
```

For **Bước 7 — Pick question + Write article**:
```markdown
7. **Pick deep_question + Write article** — V4.0:
   - Read `deep_question_options` (3 candidates)
   - Pick 1 dựa trên: data foundation strength, freshness, angle WOW potential
   - Master quyền free reformulate question (rephrase clickable hơn)
   - Write body theo Pattern V4.0 (1 paragraph + 3-7 bullets + closing)
   - Title = hook (question OR declarative paradox với tension word)
   - Đọc `references/bullet-examples.md` cho substance pattern
```

For **Bước 8 — Self-check 5 gates V4.0**:
```markdown
8. **Self-check 5 gates V4.0** — `lib.quality_gates.check_all(body, title)`:
   - no_english_jargon
   - word_count 200-400
   - body_pattern (1 paragraph + 3-7 substantive bullets + closing, no Cần để ý)
   - title_as_hook
   - no_metadata_leak
   
   Fail any → REWRITE specific issue → re-check. Loop until ALL 5 PASS.
```

For **Bước 9 — Persist with V4.0 fields**:
```markdown
9. **Persist generated_news với V4.0 fields**:
   - `chosen_question_idx` (int 0-2)
   - `chosen_pick_reason` (narrative tiếng Việt — vì sao pick câu này)
   - `skip_reasons` (JSON dict — `{idx: reason_narrative}` cho 2 câu skip)
   - `data_trail` (JSON array — per source: `{source, fetched, used_for}`)
   - `public_slug` (call `lib.slugify.slugify_hook(title)`)
```

- [ ] **Step 4: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/skills/finpath-newsroom-master-bank/ && git commit -m "feat(skill): Master Bank V4.0 — bullet examples + 5 rules + 9-step V4.0 workflow"
```

---

### Task 7: Story Editor skill — multi-option brief V4.0

**Files:**
- Modify: `.claude/skills/finpath-newsroom-story-editor/SKILL.md`

- [ ] **Step 1: Read current SKILL.md**

```bash
cat "/Users/trungdt/Desktop/Stream Intelligent/.claude/skills/finpath-newsroom-story-editor/SKILL.md" | head -50
```

- [ ] **Step 2: Replace brief schema section**

Find section `## Brief schema V3.6` (or similar — single deep_question schema) and replace with:

```markdown
## Brief schema V4.0

Story Editor outputs narrative-rich brief với 2-3 deep_question OPTIONS để Master tự chọn.

```yaml
brief_v4:
  row_id: "<crawl_log row>"
  ticker: "TCB"
  sector: "Bank"

  # User-readable narratives (Story Editor viết trực tiếp tiếng Việt thuần — NO enum)
  why_chosen_narrative: |
    3-5 câu narrative — vì sao chọn bài này.
    Vd: "Tin Q1/2026 mới 1 ngày, có 3 yếu tố hiếm cùng xuất hiện — paradox 
    CEO công khai 'hy sinh 5.000 tỷ/năm' + quyết định BĐS lần đầu < 30% + 
    timing perfect 12 ngày sau ĐHĐCĐ. Source này là duy nhất trong batch 
    decode đủ 4 con số mechanism."
  
  angle_label: "Tag ngắn — vd 'Đánh đổi chủ động — chuyển hướng chiến lược'"
  
  angle_narrative: |
    2-3 câu — bài đi theo hướng nào, tại sao chọn hướng đó.
    Vd: "Bài đi theo hướng nghịch lý — TCB cùng lúc làm 2 hành động ngược 
    chiều: chia cổ tức kỷ lục + rút BĐS dưới 30%. Đào sâu cơ chế đằng sau."
  
  source_rationale: "1-2 câu — vì sao chọn nguồn này trong batch"

  # Multi-option questions (V4.0 NEW)
  deep_question_options:
    - question: "Vì sao 2 quyết định ngược chiều xảy ra cùng lúc?"
      category: paradox
      pick_hint: "Có quote CEO mạnh + 2 hành động đối lập rõ"
    - question: "Vì sao bây giờ là thời điểm rút BĐS, không phải 2023?"
      category: why_now
      pick_hint: "Timing với khủng hoảng BĐS 2022-23, dễ liên hệ Vạn Thịnh Phát"
    - question: "TCB hy sinh 5.000 tỷ/năm — phép tính nào ra con số đó?"
      category: hidden_mechanism
      pick_hint: "Cần report nội bộ TCB, web search có thể fail"
  
  insight_hypothesis: "1 câu specific Master verify với data"
  memory_check: { passed: bool, recent_angles: [...], recent_categories: [...] }
```

⚠️ **DROPPED từ V3.6**: `data_spec`, `data_anchor`, `angle_alternatives`, single `deep_question`, single `deep_question_category`. V4.0 dùng `deep_question_options` array.

⚠️ **Narrative fields BẮT BUỘC**: `why_chosen_narrative` + `angle_narrative` + `source_rationale` — viết tiếng Việt thuần, USER-READABLE, KHÔNG enum keywords (paradox/why_now/etc).

⚠️ **Master flexibility**: Master quyền free reformulate chosen question để clickable hơn. Master persist `chosen_question_idx` + `chosen_pick_reason` + `skip_reasons[idx]: narrative` cho 2 câu skip.
```

- [ ] **Step 3: Update Workflow Pass 2 expert questions**

Find section `## Workflow 6-pass V3.6` `### Pass 2 — 6 Expert Questions` and update Câu 5 + Câu 6:

```markdown
**Câu 5 — Angle**: TÊN GỌI bài (free-text VN, vd "Đánh đổi chủ động"). Plus narrative 2-3 câu giải thích hướng tiếp cận.

**Câu 6 — Deep question OPTIONS** (V4.0 NEW):
- Generate **2-3 candidate questions**, mỗi câu thuộc 1 trong 5 category: `paradox`, `why_now`, `hidden_mechanism`, `comparison_deep`, `early_signal`
- Mỗi option có `pick_hint` 1 câu — gợi ý Master vì sao pick câu này (data foundation? freshness? complexity?)
- Master tự chọn 1 trong 3 dựa trên context của họ
- Nếu KHÔNG generate được ≥2 options thuộc 5 category → reject `low_writeability`
```

- [ ] **Step 4: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/skills/finpath-newsroom-story-editor/SKILL.md && git commit -m "feat(skill): Story Editor V4.0 — multi-option brief + narrative fields"
```

---

### Task 8: Skeptic skill — ECHO verification + data trail

**Files:**
- Modify: `.claude/skills/finpath-newsroom-skeptic/SKILL.md`

- [ ] **Step 1: Read current SKILL.md**

```bash
cat "/Users/trungdt/Desktop/Stream Intelligent/.claude/skills/finpath-newsroom-skeptic/SKILL.md" | head -50
```

- [ ] **Step 2: Add ECHO verification step at top of Workflow**

Find section `## Workflow 8-step Option D hybrid V2.4` (or similar). Replace step 1 with:

```markdown
### 1. Validate input + ECHO verification (V4.0 — bug fix from /tin TCB run)

Before any reasoning, MUST echo loaded article to confirm correct read:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
cur = db.conn.execute('SELECT title, body FROM generated_news WHERE article_id = ?', ('<ARTICLE_ID>',))
row = cur.fetchone()
db.close()
if row:
    print('LOADED article_id <ARTICLE_ID>')
    print('Title:', row['title'])
    print('Body first 30 chars:', row['body'][:30])
else:
    print('ERROR: article_id <ARTICLE_ID> not found')
"
```

**Verification rule**: Title + first 30 chars of body MUST be quoted in your reasoning. If you cannot quote them, ABORT with error "article load mismatch — refused to critique without verification".

Required input fields: row_id, ticker, master_output {title, body, key_view, insight_final}, brief_context {angle_label, deep_question (chosen), raw_article_url}.
```

- [ ] **Step 3: Add data trail output schema**

Find section `## Output V2.4` and replace với:

```markdown
## Output V4.0

```json
{
  "skeptic_critique": "<100-300 từ tiếng Việt thuần>",
  "skeptic_angle": "<1 of 6: data_skepticism|historical_analog|alt_interpretation|risk_highlight|insight_wrong|execution_unfaithful>",
  "skeptic_verdict": "<pass|pass_with_caveats|fail>",
  "skeptic_data_trail": [
    {
      "source": "<url or kb path or api endpoint>",
      "fetched": "<1-line what data extracted>",
      "used_for": "<which counter-evidence point in critique>"
    },
    ...
  ]
}
```

⚠️ **NEW V4.0**: `skeptic_data_trail` array. Mỗi independent fetch (Finpath API, KB grep, WebSearch, WebFetch raw) → 1 entry với what fetched + what used for.

⚠️ **NEW V4.0**: Title verification echo (Step 1 above) BẮT BUỘC trước Pass 1 fresh impression.
```

- [ ] **Step 4: Update persist step**

Find persist section (likely Step 8) and update:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from datetime import datetime, timezone
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
db.update_generated_news('<ARTICLE_ID>', {
    'skeptic_critique': <CRITIQUE_TEXT>,
    'skeptic_angle': '<1 of 6>',
    'skeptic_verdict': '<pass|pass_with_caveats|fail>',
    'status': 'published',
    'published_at': datetime.now(timezone.utc).isoformat(),
})
# V4.0: persist data_trail in pipeline_log JSON
cur = db.conn.execute('SELECT pipeline_log FROM generated_news WHERE article_id = ?', ('<ARTICLE_ID>',))
existing = cur.fetchone()
log = json.loads(existing['pipeline_log']) if existing and existing['pipeline_log'] else {}
log['step_5_skeptic'] = {
    'angle': '<1 of 6>',
    'verdict': '<pass|...>',
    'data_trail': <DATA_TRAIL_LIST>,
}
db.update_generated_news('<ARTICLE_ID>', {'pipeline_log': json.dumps(log, ensure_ascii=False)})
db.close()
"
```

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/skills/finpath-newsroom-skeptic/SKILL.md && git commit -m "feat(skill): Skeptic V4.0 — ECHO verification (article confusion fix) + data_trail output"
```

---

### Task 9: Update 4 agents + slash command

**Files:**
- Modify: `.claude/agents/newsroom-story-editor.md`
- Modify: `.claude/agents/newsroom-master-bank.md`
- Modify: `.claude/agents/newsroom-skeptic.md`
- Modify: `.claude/agents/newsroom-pipeline.md`
- Modify: `.claude/commands/tin.md`

- [ ] **Step 1: Update story-editor agent**

Open `.claude/agents/newsroom-story-editor.md`. Find brief output JSON section and replace with V4.0 schema (deep_question_options array, narrative fields). Add note: "BẮT BUỘC `why_chosen_narrative` + `angle_narrative` viết trực tiếp tiếng Việt thuần USER-READABLE, KHÔNG enum keywords".

Specifically replace the `## Output: brief JSON (per picked row)` section with:

```markdown
## Output: brief JSON V4.0 (per picked row)

```json
{
  "row_id": "<crawl_log row>",
  "ticker": "VCB",
  "sector": "Bank",
  "why_chosen_narrative": "3-5 câu narrative tiếng Việt thuần — vì sao chọn bài này. KHÔNG enum.",
  "angle_label": "Tag ngắn — vd 'Đánh đổi chủ động'",
  "angle_narrative": "2-3 câu giải thích hướng tiếp cận — tiếng Việt thuần, không enum",
  "source_rationale": "1-2 câu vì sao chọn nguồn này trong batch",
  "deep_question_options": [
    {
      "question": "Câu hỏi 1 đào sâu",
      "category": "paradox",
      "pick_hint": "1 câu gợi ý Master vì sao pick câu này"
    },
    {
      "question": "Câu hỏi 2",
      "category": "why_now",
      "pick_hint": "..."
    },
    {
      "question": "Câu hỏi 3",
      "category": "hidden_mechanism",
      "pick_hint": "..."
    }
  ],
  "insight_hypothesis": "1 câu specific Master verify",
  "memory_check": {"passed": true, "recent_angles": [], "recent_categories": []}
}
```

⚠️ NARRATIVE fields (`why_chosen_narrative`, `angle_narrative`, `source_rationale`) viết trực tiếp tiếng Việt thuần USER-READABLE. KHÔNG enum (paradox/hidden_mechanism/etc) trong narrative — enum chỉ trong `deep_question_options[].category`.

⚠️ MULTI-OPTION (V4.0): 2-3 deep_question candidates. Master tự chọn 1.
```

- [ ] **Step 2: Update master-bank agent**

Open `.claude/agents/newsroom-master-bank.md`. Update workflow + output:

Replace Step 1 "Validate brief":
```markdown
### 1. Validate brief V4.0

- ticker in MVP universe
- brief có `deep_question_options` (array 2-3) + `angle_label` + narrative fields
- Mỗi option có `category` ∈ {paradox, why_now, hidden_mechanism, comparison_deep, early_signal}

Fail → `master_decision: reject_no_data`, `master_note: invalid_brief_schema_v4`.
```

Add new Step 6.5 between web search and write:
```markdown
### 6.5. Pick question từ options (V4.0 NEW)

Read `deep_question_options` (3 candidates) → pick 1 based on:
- Data foundation strength (Finpath/KB available?)
- Freshness (event mới?)
- Angle WOW potential
- Skip questions cần data Master không có

Log:
- `chosen_question_idx`: 0/1/2
- `chosen_pick_reason`: narrative tiếng Việt — vì sao pick này
- `skip_reasons`: dict per skipped idx — narrative vì sao skip

Master quyền free reformulate question khi viết title hook.
```

Replace Step 7 "Write article":
```markdown
### 7. Write article V4.0 — 200-400 từ pattern

```
[Title hook — question OR declarative paradox với tension word]

[Opening paragraph 30-60 từ — sự kiện + tension/setup]

- **Bold keypoint 1**: substantive bullet ≥20 từ với connector + mechanism
- **Bold keypoint 2**: bullet ≥20 từ
- **Bold keypoint 3**: bullet ≥20 từ
- ... up to 7 bullets

[Closing — 1 câu phân loại NĐT phù hợp]
```

⚠️ **MUST đọc `.claude/skills/finpath-newsroom-master-bank/references/bullet-examples.md` TRƯỚC khi viết** — examples concrete bad vs good bullets.

⚠️ KHÔNG `## Cần để ý` section. Caveats merge vào bullets hoặc closing.
```

Replace Step 8 "Quality gates":
```markdown
### 8. Run 5 gates V4.0 self-check

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && cat > /tmp/article-body.txt <<'BODYEOF'
<paste full body here>
BODYEOF
echo "<TITLE>" > /tmp/article-title.txt
uv run python -c "
import json
from lib.quality_gates import check_all
body = open('/tmp/article-body.txt', encoding='utf-8').read()
title = open('/tmp/article-title.txt', encoding='utf-8').read().strip()
result = check_all(body, title)
print(json.dumps(result, ensure_ascii=False, indent=2))
print('ALL PASS:', all(g['pass'] for g in result.values()))
"
```

5 gates V4.0: no_english_jargon | word_count | body_pattern | title_as_hook | no_metadata_leak.

Fail any gate → REWRITE specific issue (drop jargon, restructure to pattern, hook the title) → re-check. Loop until ALL 5 PASS.
```

Update Step 9 "Persist":
```markdown
### 9. Persist generated_news V4.0

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json, uuid
from datetime import datetime, timezone
from lib.pipeline_db import PipelineDB
from lib.slugify import slugify_hook
db = PipelineDB('data/pipeline.db')
article_id = str(uuid.uuid4())
title = '<TITLE>'
slug_base = '<TICKER>-<YYYYMMDD>-<HHMM>-' + slugify_hook(title)
# Collision check
cur = db.conn.execute('SELECT public_slug FROM generated_news WHERE public_slug LIKE ?', (slug_base + '%',))
existing = [r['public_slug'] for r in cur.fetchall()]
slug = slug_base
suffix = 2
while slug in existing:
    slug = f'{slug_base}-{suffix}'
    suffix += 1

db.insert_generated_news({
    'article_id': article_id,
    'row_id': '<ROW_ID>',
    'ticker': '<TICKER>',
    'sector': 'Bank',
    'title': title,
    'body': <BODY>,
    'word_count': <N>,
    'key_view': '<lạc quan|thận trọng|trung lập>',
    'insight_final': '<1 câu>',
    'variety_guard_angle': '<from brief.angle_label>',
    'accepted_hypothesis': 1,
    'data_sources_used': json.dumps([...], ensure_ascii=False),
    'brief_json': json.dumps(<brief_dict>, ensure_ascii=False),
    'pipeline_log': json.dumps({
        'step_4_master': {
            'chosen_question_idx': <idx>,
            'chosen_pick_reason': '<narrative>',
            'skip_reasons': {<idx>: '<narrative>', ...},
            'data_trail': [{'source':..., 'fetched':..., 'used_for':...}, ...],
            'gates_passed': True,
        }
    }, ensure_ascii=False),
    'public_slug': slug,
    'status': 'draft',
    'pipeline_version': 'V4.0',
})
db.update_crawl_row('<ROW_ID>', {
    'master_decision': 'write_article',
    'master_note': 'OK — accepted_hypothesis: true',
})
db.close()
print(article_id, slug)
"
```

Output: article_id + public_slug.
```

- [ ] **Step 3: Update skeptic agent**

Open `.claude/agents/newsroom-skeptic.md`. Add ECHO verification at top of workflow:

```markdown
### 0. ECHO verification (V4.0 — REQUIRED — fix article confusion bug)

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
cur = db.conn.execute('SELECT title, body FROM generated_news WHERE article_id = ?', ('<ARTICLE_ID>',))
row = cur.fetchone()
db.close()
if row:
    print('LOADED article_id <ARTICLE_ID>')
    print('Title:', row['title'])
    print('Body first 30 chars:', row['body'][:30])
else:
    print('ABORT: article_id not found')
"
```

⚠️ MUST quote title + body[:30] in your reasoning before Pass 1. If mismatch → ABORT with "article load mismatch".
```

Update output JSON to include `skeptic_data_trail`:

```markdown
## Output JSON V4.0

```json
{
  "skeptic_critique": "<100-300 từ>",
  "skeptic_angle": "<1 of 6>",
  "skeptic_verdict": "<pass|pass_with_caveats|fail>",
  "skeptic_data_trail": [
    {
      "source": "<url|kb_path|api>",
      "fetched": "<what extracted>",
      "used_for": "<counter-evidence point in critique>"
    }
  ]
}
```
```

Update persist:

```markdown
### 8. Persist V4.0

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from datetime import datetime, timezone
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
db.update_generated_news('<ARTICLE_ID>', {
    'skeptic_critique': <CRITIQUE>,
    'skeptic_angle': '<angle>',
    'skeptic_verdict': '<pass|...>',
    'status': 'published',
    'published_at': datetime.now(timezone.utc).isoformat(),
})
# V4.0: persist data_trail in pipeline_log
cur = db.conn.execute('SELECT pipeline_log FROM generated_news WHERE article_id = ?', ('<ARTICLE_ID>',))
existing = cur.fetchone()
log = json.loads(existing['pipeline_log']) if existing['pipeline_log'] else {}
log['step_5_skeptic'] = {
    'angle': '<angle>',
    'verdict': '<verdict>',
    'data_trail': <DATA_TRAIL>,
}
db.update_generated_news('<ARTICLE_ID>', {'pipeline_log': json.dumps(log, ensure_ascii=False)})
db.close()
"
```
```

- [ ] **Step 4: Fix slash command $1 bug**

Open `.claude/commands/tin.md`. Find lines using `$1` and replace ALL with `$ARGUMENTS`. The first paragraph becomes:

```markdown
Trigger pipeline 6-step Newsroom V4.0 cho ticker **$ARGUMENTS**.

Universe MVP Bank: **TCB · VCB · MBB · ACB · BID · CTG · VPB**.

Nếu $ARGUMENTS không thuộc universe → reply "Ticker $ARGUMENTS không thuộc MVP Bank universe. CK + BĐS sẽ thêm sau." và dừng pipeline.
```

Continue replacing all `$1` references in the file with `$ARGUMENTS`.

- [ ] **Step 5: Update newsroom-pipeline agent — Step 4-5 dispatch with V4.0 fields**

Open `.claude/agents/newsroom-pipeline.md`. Find Step 4 Master Bank dispatch section and update prompt to include V4.0 brief schema + bullet-examples reference. Find Step 5 Skeptic dispatch section and ensure article_id is passed clearly + ECHO verification reminded.

Find Step 6 render section and update batch ID note: render now generates 1 file per article (multi-article fix), not 1 file per batch.

Specifically replace Step 6 with:

```markdown
### Step 6 — Render (V4.0 multi-article)

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python lib/render_compare_feed.py <funnel_batch_id>
```

V4.0: Loop ALL anchor rows in batch (filter `master_decision='write_article'`). For each:
- Generate `public_slug` from hook
- Render markdown file `output/compare-feed/<TICKER>-<DATE>-<HHMM>-<slug>.md`
- Append entry to `manifest.json`

Output: N files written (N = number of accepted Master articles).
```

- [ ] **Step 6: Commit all 4 agents + command**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/agents/ .claude/commands/ && git commit -m "feat(claude): 4 agents + tin command V4.0 (multi-option pick + ECHO verify + multi-article + \$ARGUMENTS fix)"
```

---

### Task 10: Render layer rewrite — multi-article + 8 sections

**Files:**
- Rewrite: `lib/render_compare_feed.py`
- Update: `tests/test_render_compare_feed.py`

This task is the heaviest (~2 days per advisor estimate).

- [ ] **Step 1: Rewrite test file**

Replace `tests/test_render_compare_feed.py`:

```python
"""Tests for lib.render_compare_feed V4.0 — multi-article + 8 sections."""
import json
from pathlib import Path

import pytest

from lib.pipeline_db import PipelineDB
from lib.render_compare_feed import (
    render_for_funnel_batch,
    render_article_md_v4,
    build_right_column,
)


@pytest.fixture
def populated_db_v4(tmp_path):
    """Seed 1 batch with 3 articles (multi-article scenario)."""
    schema = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db_path = tmp_path / "test.db"
    db = PipelineDB(db_path)
    db.init_schema(schema)
    # Migrate public_slug column
    db.conn.execute("ALTER TABLE generated_news ADD COLUMN IF NOT EXISTS public_slug TEXT")

    # 3 anchor rows (3 picked) + 2 rejected (1 by editor, 1 by story-editor)
    funnel_batch_id = "TCB-20260508-1023"
    
    for i, (rid, src, url, story_dec, master_dec, m_note) in enumerate([
        ("anchor-1", "Báo Pháp luật", "https://bpl.vn/a", "write_brief", "write_article", "Anchor — đầy đủ data"),
        ("anchor-2", "VnEconomy", "https://vne.vn/a", "write_brief", "write_article", "Anchor — angle so sánh"),
        ("anchor-3", "Vietstock", "https://vst.vn/a", "write_brief", "write_article", "Anchor — early signal"),
    ]):
        db.insert_crawl_row({
            "row_id": rid, "funnel_batch_id": funnel_batch_id, "ticker": "TCB",
            "source_name": src, "source_url": url, "title": f"Title {i}",
            "crawled_at": "2026-05-08T10:23:00+07:00",
            "published_time": "2026-05-07T10:00:00+07:00",
            "raw_content": "Raw body.",
            "primary_ticker": "TCB", "sector": "Bank",
            "editor_v1_decision": "route_to_story_editor",
            "story_editor_decision": story_dec,
            "master_decision": master_dec, "master_note": m_note,
            "brief_json": json.dumps({
                "why_chosen_narrative": f"Narrative {i} cho bài chọn này — 3-5 câu giải thích.",
                "angle_label": f"Angle {i}",
                "angle_narrative": f"Narrative angle {i} — 2-3 câu hướng tiếp cận.",
                "source_rationale": f"Rationale {i} — vì sao chọn nguồn.",
                "deep_question_options": [
                    {"question": f"Q1 batch {i}?", "category": "paradox", "pick_hint": "Hint 1"},
                    {"question": f"Q2 batch {i}?", "category": "why_now", "pick_hint": "Hint 2"},
                    {"question": f"Q3 batch {i}?", "category": "hidden_mechanism", "pick_hint": "Hint 3"},
                ],
                "insight_hypothesis": f"Insight {i}",
            }, ensure_ascii=False),
            "status": "published",
        })
    
    # Reject by editor V1
    db.insert_crawl_row({
        "row_id": "rej-edit", "funnel_batch_id": funnel_batch_id, "ticker": "TCB",
        "source_name": "Random Blog", "source_url": "https://blog/a", "title": "Off-topic",
        "crawled_at": "2026-05-08T10:23:00+07:00",
        "primary_ticker": None, "sector": "rejected",
        "editor_v1_decision": "reject", "editor_v1_note": "Off-topic — không phải Bank",
        "status": "rejected",
    })
    # Reject by story editor
    db.insert_crawl_row({
        "row_id": "rej-story", "funnel_batch_id": funnel_batch_id, "ticker": "TCB",
        "source_name": "Other Source", "source_url": "https://other/a", "title": "Dup story",
        "crawled_at": "2026-05-08T10:23:00+07:00",
        "primary_ticker": "TCB", "sector": "Bank",
        "editor_v1_decision": "route_to_story_editor",
        "story_editor_decision": "reject",
        "story_editor_note": "Cùng story 25/4 với BPL anchor, ít quote CEO hơn",
        "status": "rejected",
    })
    
    # 3 generated_news for 3 anchors (multi-article)
    for i, (aid, rid, title) in enumerate([
        ("art-1", "anchor-1", "TCB hy sinh 5.000 tỷ — đổi lấy gì?"),
        ("art-2", "anchor-2", "TCB đổi giấy lấy ngôi vương — vốn hóa kém tứ trụ?"),
        ("art-3", "anchor-3", "Phí dịch vụ TCB lập đỉnh — rời mô hình cho vay?"),
    ]):
        slug = f"TCB-20260508-1023-art-{i+1}"
        db.insert_generated_news({
            "article_id": aid, "row_id": rid,
            "ticker": "TCB", "sector": "Bank",
            "title": title,
            "body": "Opening paragraph đầy đủ ba mươi từ trở lên mô tả sự kiện và đặt setup cho thân bài làm rõ tension.\n\n- **Bold 1**: bullet content đầy đủ ít nhất hai mươi từ để pass substantive check trong gate này.\n- **Bold 2**: bullet content cũng đủ hai mươi từ để pass substantive thực sự đấy hôm nay.\n- **Bold 3**: bullet cuối cùng cũng đủ content và bold highlight đầu cho rõ ràng nhé.\n\nClosing.",
            "word_count": 60,
            "key_view": "thận trọng",
            "insight_final": f"Insight final {i}.",
            "skeptic_critique": f"Critique {i}.",
            "skeptic_angle": "alt_interpretation",
            "skeptic_verdict": "pass_with_caveats",
            "accepted_hypothesis": 1,
            "brief_json": "{}",
            "pipeline_log": json.dumps({
                "step_4_master": {
                    "chosen_question_idx": 0,
                    "chosen_pick_reason": f"Pick reason {i}.",
                    "skip_reasons": {"1": "Skip 1", "2": "Skip 2"},
                    "data_trail": [
                        {"source": "Finpath/bankratios", "fetched": "NIM 3.74%", "used_for": "Bullet 1 anchor"},
                        {"source": "KB/frameworks", "fetched": "Pattern X", "used_for": "Closing"},
                    ],
                    "gates_passed": True,
                },
                "step_5_skeptic": {
                    "angle": "alt_interpretation",
                    "verdict": "pass_with_caveats",
                    "data_trail": [
                        {"source": "Finpath/shareholders", "fetched": "Foreign 22%", "used_for": "Counter risk profile"},
                    ],
                },
            }, ensure_ascii=False),
            "status": "published",
            "published_at": "2026-05-08T16:00:00+07:00",
            "public_slug": slug,
        })
    yield db, db_path
    db.close()


def test_render_writes_n_files_for_n_anchors(populated_db_v4, tmp_path):
    """V4.0 multi-article: 3 anchors → 3 files (not 1)."""
    _, db_path = populated_db_v4
    out_dir = tmp_path / "out"
    result = render_for_funnel_batch(db_path, "TCB-20260508-1023", out_dir)
    assert result["count"] == 3
    md_files = list(out_dir.glob("*.md"))
    assert len(md_files) == 3


def test_render_uses_public_slug_in_filename(populated_db_v4, tmp_path):
    _, db_path = populated_db_v4
    out_dir = tmp_path / "out"
    render_for_funnel_batch(db_path, "TCB-20260508-1023", out_dir)
    md_filenames = sorted(p.name for p in out_dir.glob("*.md"))
    assert md_filenames == [
        "TCB-20260508-1023-art-1.md",
        "TCB-20260508-1023-art-2.md",
        "TCB-20260508-1023-art-3.md",
    ]


def test_manifest_has_n_entries(populated_db_v4, tmp_path):
    _, db_path = populated_db_v4
    out_dir = tmp_path / "out"
    render_for_funnel_batch(db_path, "TCB-20260508-1023", out_dir)
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert len(manifest["articles"]) == 3
    assert all(a["ticker"] == "TCB" for a in manifest["articles"])
    # Sorted by crawled_at desc — all 3 same crawled_at, ok any order


def test_manifest_id_is_public_slug(populated_db_v4, tmp_path):
    _, db_path = populated_db_v4
    out_dir = tmp_path / "out"
    render_for_funnel_batch(db_path, "TCB-20260508-1023", out_dir)
    manifest = json.loads((out_dir / "manifest.json").read_text())
    ids = {a["id"] for a in manifest["articles"]}
    assert "TCB-20260508-1023-art-1" in ids
    assert "TCB-20260508-1023-art-2" in ids
    assert "TCB-20260508-1023-art-3" in ids


def test_render_includes_8_sections_in_right_column(populated_db_v4, tmp_path):
    """Frontmatter contains all 8 sections data for cột phải."""
    _, db_path = populated_db_v4
    out_dir = tmp_path / "out"
    render_for_funnel_batch(db_path, "TCB-20260508-1023", out_dir)
    md_path = out_dir / "TCB-20260508-1023-art-1.md"
    content = md_path.read_text()
    # Section 1: original article info
    assert "right_source:" in content
    # Section 2: why_chosen_narrative
    assert "why_chosen_narrative:" in content
    # Section 3: angle_narrative
    assert "angle_narrative:" in content
    # Section 4: deep_question_options + master pick
    assert "deep_question_options" in content
    assert "chosen_question_idx" in content
    # Section 5: crawl_funnel + reject reasons + agent labels
    assert "crawl_funnel:" in content
    # Section 6: master_data_trail
    assert "master_data_trail:" in content
    # Section 7: skeptic_data_trail
    assert "skeptic_data_trail:" in content
    # Section 8: external link (raw_url, NOT raw_content)
    assert "raw_article_url:" in content
    assert "Raw body." not in content  # raw content NOT embedded


def test_funnel_groups_rejects_with_agent_labels(populated_db_v4, tmp_path):
    _, db_path = populated_db_v4
    out_dir = tmp_path / "out"
    render_for_funnel_batch(db_path, "TCB-20260508-1023", out_dir)
    content = (out_dir / "TCB-20260508-1023-art-1.md").read_text()
    # editor_v1 reject narrative + agent label
    assert "Off-topic" in content
    assert "editor_v1" in content or "Gác cổng" in content
    # story_editor reject narrative + agent label
    assert "Cùng story 25/4" in content
    assert "story_editor" in content or "Tổng biên tập" in content
```

- [ ] **Step 2: Run failing tests**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_render_compare_feed.py -v
```

Expected: many failures — V4.0 functions not implemented yet.

- [ ] **Step 3: Rewrite `lib/render_compare_feed.py`**

```python
"""Render V4.0 — multi-article + 8-section right column for Compare Feed.

Each /tin run with N picked briefs produces N markdown files (1 per article).
Each markdown file has frontmatter with all 8 right-column sections data.
"""
from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow running as `python lib/render_compare_feed.py ...` from project root
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml


REJECT_AGENT_LABELS = {
    "editor_v1": "Gác cổng bỏ",
    "story_editor": "Tổng biên tập bỏ",
    "master": "Phóng viên bỏ",
}


def build_right_column(article: dict, anchor_row: dict, funnel_rows: list[dict]) -> dict:
    """Build the 8-section right-column data structure as frontmatter dict."""
    pipeline_log = _parse_json(article.get("pipeline_log", "{}"))
    brief = _parse_json(anchor_row.get("brief_json", "{}"))
    step_4 = pipeline_log.get("step_4_master", {})
    step_5 = pipeline_log.get("step_5_skeptic", {})

    # Section 1: original article info (raw_source)
    right_source = {
        "name": anchor_row["source_name"],
        "url": anchor_row["source_url"],
        "published": (anchor_row.get("published_time") or "")[:10],
        "raw_title": anchor_row["title"],
    }

    # Section 2: why_chosen_narrative (Story Editor)
    why_chosen_narrative = brief.get("why_chosen_narrative", "")

    # Section 3: angle (Story Editor)
    angle_label = brief.get("angle_label", "")
    angle_narrative = brief.get("angle_narrative", "")

    # Section 4: question options + Master pick
    deep_question_options = brief.get("deep_question_options", [])
    chosen_question_idx = step_4.get("chosen_question_idx", 0)
    chosen_pick_reason = step_4.get("chosen_pick_reason", "")
    skip_reasons = step_4.get("skip_reasons", {})

    # Section 5: crawl funnel — picked + rejected (with agent labels)
    crawl_funnel = _build_funnel(funnel_rows)

    # Section 6: master data trail
    master_data_trail = step_4.get("data_trail", [])

    # Section 7: skeptic data trail
    skeptic_data_trail = step_5.get("data_trail", [])

    # Section 8: raw article URL (link only, NO embed)
    raw_article_url = anchor_row["source_url"]

    return {
        "right_source": right_source,
        "why_chosen_narrative": why_chosen_narrative,
        "angle_label": angle_label,
        "angle_narrative": angle_narrative,
        "deep_question_options": deep_question_options,
        "chosen_question_idx": chosen_question_idx,
        "chosen_pick_reason": chosen_pick_reason,
        "skip_reasons": skip_reasons,
        "crawl_funnel": crawl_funnel,
        "master_data_trail": master_data_trail,
        "skeptic_data_trail": skeptic_data_trail,
        "raw_article_url": raw_article_url,
    }


def _build_funnel(rows: list[dict]) -> dict:
    """Group rows: picked + rejected_by_agent. Each rejected has agent label + narrative reason."""
    picked = []
    rejected = []
    for r in rows:
        item_base = {
            "source": r["source_name"],
            "url": r["source_url"],
            "published": (r.get("published_time") or "")[:10],
        }
        if r.get("master_decision") == "write_article":
            picked.append({**item_base, "reason": r.get("master_note") or "Anchor"})
        elif r.get("master_decision") in ("reject_no_data", "reject_data_conflict"):
            rejected.append({
                **item_base,
                "reject_agent": "master",
                "reject_label": REJECT_AGENT_LABELS["master"],
                "reason": r.get("master_note", "Master reject"),
            })
        elif r.get("story_editor_decision") == "reject":
            rejected.append({
                **item_base,
                "reject_agent": "story_editor",
                "reject_label": REJECT_AGENT_LABELS["story_editor"],
                "reason": r.get("story_editor_note", "Story Editor reject"),
            })
        elif r.get("editor_v1_decision") == "reject":
            rejected.append({
                **item_base,
                "reject_agent": "editor_v1",
                "reject_label": REJECT_AGENT_LABELS["editor_v1"],
                "reason": r.get("editor_v1_note", "Editor V1 reject"),
            })
    return {"picked": picked, "rejected": rejected, "total_candidates": len(rows)}


def _parse_json(s: str) -> dict:
    if not s:
        return {}
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return {}


def render_article_md_v4(article: dict, anchor_row: dict, funnel_rows: list[dict]) -> str:
    """Build the V4.0 markdown file content (frontmatter + 2 sections).

    Body = Master output as-is. Skeptic critique appended in left column section
    via '## Góc nhìn ngược' heading.
    """
    sector = article.get("sector", "Bank")
    sector_icon = {"Bank": "🏦", "CK": "📈", "BĐS": "🏠"}.get(sector, "📰")

    fm = {
        "title": article["title"],
        "ticker": article["ticker"],
        "sector": sector,
        "sector_icon": sector_icon,
        "crawled_at": anchor_row["crawled_at"],
        "funnel_batch_id": anchor_row["funnel_batch_id"],
        "left_meta": {
            "author": _author_for_sector(sector),
            "word_count": article.get("word_count", 0),
            "key_view": article.get("key_view", "trung lập"),
            "skeptic_verdict": article.get("skeptic_verdict", "pass"),
            "pipeline_version": article.get("pipeline_version", "V4.0"),
        },
        "insight": article.get("insight_final", ""),
        # 8-section right column
        **build_right_column(article, anchor_row, funnel_rows),
    }

    fm_yaml = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).strip()
    body = (article.get("body") or "").strip()
    skeptic = (article.get("skeptic_critique") or "").strip()
    left_section = body
    if skeptic:
        left_section += f"\n\n## Góc nhìn ngược\n\n{skeptic}"

    # Right column markdown body — could be empty since frontmatter has all data
    # React component renders sections from frontmatter directly.
    right_section = ""

    return (
        f"---\n{fm_yaml}\n---\n\n"
        f"<!-- left -->\n\n{left_section}\n\n"
        f"<!-- right -->\n\n{right_section}\n"
    )


def _author_for_sector(sector: str) -> str:
    return {"Bank": "Chuyên gia ngân hàng", "CK": "Chuyên gia chứng khoán", "BĐS": "Chuyên gia bất động sản"}.get(sector, "Chuyên gia")


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


def render_for_funnel_batch(db_path: Path, funnel_batch_id: str, output_dir: Path) -> dict:
    """V4.0: Loop ALL anchor rows in batch, render 1 file per article."""
    from lib.pipeline_db import PipelineDB

    db = PipelineDB(db_path)
    rows = db.query_by_funnel_batch(funnel_batch_id)
    if not rows:
        db.close()
        return {"error": f"No rows for batch {funnel_batch_id}"}

    anchors = [r for r in rows if r.get("master_decision") == "write_article"]
    if not anchors:
        db.close()
        return {"error": f"No anchors in batch {funnel_batch_id}"}

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    written = []

    for anchor in anchors:
        cur = db.conn.execute(
            "SELECT * FROM generated_news WHERE row_id = ? ORDER BY published_at DESC LIMIT 1",
            (anchor["row_id"],),
        )
        art_row = cur.fetchone()
        if not art_row:
            continue
        article = dict(art_row)
        public_slug = article.get("public_slug") or f"{anchor['ticker']}-{anchor['row_id']}"
        md_content = render_article_md_v4(article, anchor, rows)
        out_path = output_dir / f"{public_slug}.md"
        out_path.write_text(md_content, encoding="utf-8")
        summary = {
            "id": public_slug,
            "ticker": article["ticker"],
            "sector": article.get("sector", "Bank"),
            "title": article["title"],
            "crawled_at": anchor["crawled_at"],
            "key_view": article.get("key_view", "trung lập"),
            "word_count": article.get("word_count", 0),
        }
        update_manifest(manifest_path, summary)
        written.append(str(out_path))

    db.close()
    return {"count": len(written), "files": written}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("funnel_batch_id")
    parser.add_argument("--db", type=Path, default=Path("data/pipeline.db"))
    parser.add_argument("--output-dir", type=Path, default=Path("output/compare-feed/"))
    args = parser.parse_args()
    result = render_for_funnel_batch(args.db, args.funnel_batch_id, args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if "error" not in result else 2


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests pass**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_render_compare_feed.py -v
```

Expected: 7 PASS.

- [ ] **Step 5: Run all tests — verify no regression**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest -v 2>&1 | tail -3
```

Expected: total ~50 PASS (37 V3.6 + new V4.0 tests).

- [ ] **Step 6: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add lib/render_compare_feed.py tests/test_render_compare_feed.py && git commit -m "feat(lib): render V4.0 — multi-article + 8-section right column + agent reject labels"
```

---

### Task 11: Update React types + add 3 new components

**Files:**
- Modify: `web/src/types.ts`
- Modify: `web/src/lib/parseArticle.ts` (verify still works with V4.0 frontmatter)
- Create: `web/src/components/QuestionOptions.tsx`
- Create: `web/src/components/DataTrail.tsx`
- Modify: `web/src/components/CrawlFunnel.tsx` — agent labels
- Modify: `web/src/components/RightColumn.tsx` — 8 sections

- [ ] **Step 1: Update `web/src/types.ts`**

Replace the existing `ArticleMeta` interface and supporting types (around `WhyChosenItem`, `CrawlFunnelData`) with V4.0:

```ts
export interface SourceMeta {
  name: string;
  url: string;
  published: string;
  raw_title: string;
}

export interface LeftMeta {
  author: string;
  word_count: number;
  key_view: 'lạc quan' | 'thận trọng' | 'trung lập';
  skeptic_verdict: string;
  pipeline_version: string;
}

export interface DeepQuestionOption {
  question: string;
  category: string;
  pick_hint: string;
}

export interface FunnelItem {
  source: string;
  url: string;
  published: string;
  reason: string;
  reject_agent?: 'editor_v1' | 'story_editor' | 'master';
  reject_label?: string;
}

export interface CrawlFunnelData {
  picked: FunnelItem[];
  rejected: FunnelItem[];
  total_candidates: number;
}

export interface DataTrailEntry {
  source: string;
  fetched: string;
  used_for: string;
}

export interface ArticleMeta {
  title: string;
  ticker: string;
  sector: string;
  sector_icon: string;
  crawled_at: string;
  funnel_batch_id: string;
  left_meta: LeftMeta;
  insight: string;
  // V4.0 right-column 8 sections
  right_source: SourceMeta;
  why_chosen_narrative: string;
  angle_label: string;
  angle_narrative: string;
  deep_question_options: DeepQuestionOption[];
  chosen_question_idx: number;
  chosen_pick_reason: string;
  skip_reasons: Record<string, string>;
  crawl_funnel: CrawlFunnelData;
  master_data_trail: DataTrailEntry[];
  skeptic_data_trail: DataTrailEntry[];
  raw_article_url: string;
}

export interface Article {
  id: string;
  meta: ArticleMeta;
  leftMarkdown: string;
  rightMarkdown: string;
}

export interface ArticleSummary {
  id: string;
  ticker: string;
  sector: string;
  title: string;
  crawled_at: string;
  key_view: string;
  word_count: number;
}

export interface Manifest {
  articles: ArticleSummary[];
}
```

Note: `WhyChosenItem` removed (V3.6 data anchor logic).

- [ ] **Step 2: Verify parseArticle.ts still works (frontmatter is backward compatible)**

`parseArticle.ts` uses `js-yaml` to parse YAML frontmatter and casts to `ArticleMeta`. Since V4.0 frontmatter has more fields, the parse will work — extra fields populate; missing legacy fields are not referenced by V4.0 components.

Run TypeScript check:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit
```

Expected: errors in `RightColumn.tsx` (uses old V3.6 types) — fix in Step 5.

- [ ] **Step 3: Create `web/src/components/QuestionOptions.tsx`**

```tsx
import type { DeepQuestionOption } from '../types';

export function QuestionOptions({
  options,
  chosenIdx,
  pickReason,
  skipReasons,
}: {
  options: DeepQuestionOption[];
  chosenIdx: number;
  pickReason: string;
  skipReasons: Record<string, string>;
}) {
  if (!options || options.length === 0) return null;
  return (
    <section>
      <h3>🤔 Tổng biên tập đề xuất {options.length} câu hỏi đào sâu</h3>
      <ol className="space-y-3">
        {options.map((opt, i) => {
          const isPicked = i === chosenIdx;
          return (
            <li key={i} className="leading-relaxed">
              {isPicked ? (
                <>
                  <strong className="text-green-700">(✓ Đã chọn)</strong>{' '}
                  <strong>{opt.question}</strong>
                  <div className="text-sm text-gray-600 mt-1">
                    <em>Phóng viên pick vì</em>: {pickReason || opt.pick_hint}
                  </div>
                </>
              ) : (
                <>
                  {opt.question}
                  <div className="text-sm text-gray-500 mt-1">
                    <em>Skip vì</em>: {skipReasons[String(i)] || 'Không có lý do ghi'}
                  </div>
                </>
              )}
            </li>
          );
        })}
      </ol>
    </section>
  );
}
```

- [ ] **Step 4: Create `web/src/components/DataTrail.tsx`**

```tsx
import type { DataTrailEntry } from '../types';

export function DataTrail({
  title,
  emoji,
  trail,
}: {
  title: string;
  emoji: string;
  trail: DataTrailEntry[];
}) {
  if (!trail || trail.length === 0) return null;
  return (
    <section>
      <h3>{emoji} {title}</h3>
      <ul className="text-sm space-y-2">
        {trail.map((entry, i) => {
          const isUrl = entry.source.startsWith('http://') || entry.source.startsWith('https://');
          return (
            <li key={i}>
              <div>
                → {isUrl ? (
                  <a href={entry.source} target="_blank" rel="noopener noreferrer" className="font-semibold">
                    {entry.source}
                  </a>
                ) : (
                  <span className="font-semibold">{entry.source}</span>
                )}
              </div>
              <div className="text-gray-600 ml-4">
                <em>Tra được</em>: {entry.fetched}
              </div>
              <div className="text-gray-600 ml-4">
                <em>Dùng cho</em>: {entry.used_for}
              </div>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
```

- [ ] **Step 5: Update `web/src/components/CrawlFunnel.tsx` — V4.0 agent labels**

Replace existing `CrawlFunnel.tsx` with:

```tsx
import type { CrawlFunnelData, FunnelItem } from '../types';
import { formatPublishedDate } from '../lib/format';

function FunnelEntry({ item }: { item: FunnelItem }) {
  return (
    <li>
      <a href={item.url} target="_blank" rel="noopener noreferrer">
        <strong>{item.source}</strong>
      </a>{' '}
      <span className="text-gray-500">({formatPublishedDate(item.published)})</span>
      {item.reject_label && (
        <>
          {' '}— <em className="text-red-700">{item.reject_label}</em>
        </>
      )}
      <div className="text-sm text-gray-600 ml-4 mt-1">
        {item.reject_label ? 'Vì sao bỏ' : 'Lý do chọn'}: {item.reason}
      </div>
    </li>
  );
}

export function CrawlFunnel({
  data,
  funnelBatchId,
}: {
  data: CrawlFunnelData;
  funnelBatchId: string;
}) {
  return (
    <details>
      <summary className="text-sm">
        📊 Crawl funnel — đã quét nhiều nguồn, gom {data.total_candidates} bài, chọn {data.picked.length}, loại {data.rejected.length}
      </summary>
      <div className="mt-3 text-sm space-y-4">
        <p className="text-gray-500 text-xs">
          <strong>Funnel batch</strong>: <code>{funnelBatchId}</code>
        </p>
        {data.picked.length > 0 && (
          <div>
            <p className="font-semibold text-green-700 mb-1">✅ ĐÃ CHỌN ({data.picked.length})</p>
            <ul className="space-y-2 pl-4">
              {data.picked.map((item, i) => (
                <FunnelEntry key={i} item={item} />
              ))}
            </ul>
          </div>
        )}
        {data.rejected.length > 0 && (
          <div>
            <p className="font-semibold text-red-700 mb-1">❌ KHÔNG CHỌN ({data.rejected.length})</p>
            <ul className="space-y-2 pl-4">
              {data.rejected.map((item, i) => (
                <FunnelEntry key={i} item={item} />
              ))}
            </ul>
          </div>
        )}
      </div>
    </details>
  );
}
```

- [ ] **Step 6: Rewrite `web/src/components/RightColumn.tsx` for 8 sections V4.0**

Replace existing `RightColumn.tsx` with:

```tsx
import type { ArticleMeta } from '../types';
import { CrawlFunnel } from './CrawlFunnel';
import { QuestionOptions } from './QuestionOptions';
import { DataTrail } from './DataTrail';
import { formatPublishedDate } from '../lib/format';

export function RightColumn({ meta }: { meta: ArticleMeta }) {
  const src = meta.right_source;
  return (
    <section className="space-y-6">
      {/* Section 1: Bài gốc */}
      <section>
        <h3>📰 Bài gốc</h3>
        <p className="font-semibold">{src.raw_title}</p>
        <p className="text-sm text-gray-500 italic">
          Nguồn:{' '}
          <a href={src.url} target="_blank" rel="noopener noreferrer">
            {src.name}
          </a>{' '}
          · Published {formatPublishedDate(src.published)}
        </p>
      </section>

      {/* Section 2: Vì sao chọn */}
      {meta.why_chosen_narrative && (
        <section>
          <h3>🎯 Vì sao chọn bài này</h3>
          <p className="leading-relaxed">{meta.why_chosen_narrative}</p>
        </section>
      )}

      {/* Section 3: Hướng tiếp cận */}
      {meta.angle_label && (
        <section>
          <h3>🧭 Hướng tiếp cận</h3>
          <p className="leading-relaxed">
            <strong>{meta.angle_label}</strong>
            {meta.angle_narrative && <> — {meta.angle_narrative}</>}
          </p>
        </section>
      )}

      {/* Section 4: Question options + Master pick */}
      <QuestionOptions
        options={meta.deep_question_options}
        chosenIdx={meta.chosen_question_idx}
        pickReason={meta.chosen_pick_reason}
        skipReasons={meta.skip_reasons || {}}
      />

      {/* Section 5: Crawl funnel */}
      {meta.crawl_funnel && (
        <CrawlFunnel data={meta.crawl_funnel} funnelBatchId={meta.funnel_batch_id} />
      )}

      {/* Section 6: Master data trail */}
      <DataTrail
        title="Phóng viên đã tra ở đâu"
        emoji="📋"
        trail={meta.master_data_trail}
      />

      {/* Section 7: Skeptic data trail */}
      <DataTrail
        title="Reviewer ngoài đã tra ở đâu"
        emoji="🔍"
        trail={meta.skeptic_data_trail}
      />

      {/* Section 8: Đọc bài gốc — link only, NO embed */}
      <section>
        <h3>📖 Đọc bài gốc</h3>
        <p>
          → <a href={meta.raw_article_url} target="_blank" rel="noopener noreferrer">
            {src.name} — {src.raw_title}
          </a>{' '}
          ({formatPublishedDate(src.published)})
        </p>
      </section>
    </section>
  );
}
```

- [ ] **Step 7: Update `web/src/components/CompareFeedLayout.tsx` to pass meta**

Find and replace the RightColumn call:

```tsx
// Before:
<RightColumn
  source={meta.right_source}
  whyChosen={meta.why_chosen}
  crawlFunnel={meta.crawl_funnel}
  funnelBatchId={meta.funnel_batch_id}
  rawBody={rightMarkdown}
/>

// After:
<RightColumn meta={meta} />
```

- [ ] **Step 8: TypeScript check**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit
```

Expected: 0 errors.

- [ ] **Step 9: Update `ArticleCard.tsx` — drop "key_view chip" + "category" per Card spec**

Open `web/src/components/ArticleCard.tsx` and simplify:

```tsx
import { Link } from 'react-router-dom';
import type { ArticleSummary } from '../types';
import { formatCrawledAt } from '../lib/format';

export function ArticleCard({ article }: { article: ArticleSummary }) {
  return (
    <Link
      to={`/article/${article.id}`}
      className="block rounded-lg border border-gray-200 p-4 hover:border-gray-400 hover:shadow-sm transition no-underline"
    >
      <div className="flex items-center justify-between mb-3 text-xs text-gray-500">
        <span className="font-semibold rounded bg-blue-100 text-blue-800 px-2 py-0.5">
          {article.ticker}
        </span>
        <span>
          {article.word_count} từ · 🕐 {formatCrawledAt(article.crawled_at)}
        </span>
      </div>
      <h3 className="text-base font-semibold text-gray-900 leading-snug mt-0">
        {article.title}
      </h3>
    </Link>
  );
}
```

- [ ] **Step 10: TS recheck + commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit
echo "---"
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add web/ && git commit -m "feat(web): V4.0 — types + 8-section RightColumn + DataTrail + QuestionOptions + agent labels"
```

---

### Task 12: E2E smoke test + tag V4.0

**Files:**
- Run: `/tin MBB` interactively (manual user action)
- Verify: output, gates, viewer

This task requires interactive Claude Code session — not runnable as pure Bash.

- [ ] **Step 1: Run all pytest**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest -v 2>&1 | tail -3
```

Expected: ~50+ PASS (8 slugify + ~22 quality_gates + 7 render + others).

- [ ] **Step 2: TypeScript check + dev server boot**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit
echo "---"
(npm run dev > /tmp/vite-v4.log 2>&1 &)
sleep 5
curl -sI http://localhost:5173/ | head -1
pkill -f "vite" 2>/dev/null
```

Expected: HTTP 200.

- [ ] **Step 3: Tell user to run /tin MBB**

User must manually:
1. Open Claude Code in project root
2. Run `/tin MBB`
3. Wait for full pipeline (~5-10 min, ~17 subagent dispatches)
4. Verify:
   - 1-3 markdown files in `output/compare-feed/MBB-<date>-<hhmm>-<slug>.md`
   - Each filename = TICKER + date + hook slug
   - Each file passes 5 gates V4.0 (manual check via `lib.quality_gates.check_all`)
   - Web viewer shows 1-3 cards on IndexPage with hook titles
   - Click → ArticlePage shows 8 sections in right column, no enum, agent labels Vietnamese
   - Title is hook (question or declarative paradox), body has 1 paragraph + 3-7 bullets + closing

- [ ] **Step 4: Run quality gates against MBB articles**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json, re
from pathlib import Path
from lib.quality_gates import check_all
md_files = sorted(Path('output/compare-feed').glob('MBB-*.md'))
for f in md_files:
    text = f.read_text(encoding='utf-8')
    title_match = re.search(r'^title:\s*[\"]?(.+?)[\"]?$', text, flags=re.MULTILINE)
    title = title_match.group(1) if title_match else ''
    body_match = re.search(r'<!-- left -->([\s\S]*?)<!-- right -->', text)
    body = body_match.group(1).strip() if body_match else ''
    result = check_all(body, title)
    all_pass = all(g['pass'] for g in result.values())
    print(f'{f.name}: {'PASS' if all_pass else 'FAIL'}')
    for gate, r in result.items():
        if not r['pass']:
            print(f'  - {gate}: {r[\"reason\"]}')
"
```

Expected: all MBB files PASS.

If any FAIL → iterate Master prompt or bullet examples; rerun `/tin MBB` (different batch, won't dedup).

- [ ] **Step 5: Tag V4.0**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git tag v4.0-newsroom-redesign && git tag
```

- [ ] **Step 6: Cleanup pre-V4.0 articles in output (optional)**

If old `TCB-20260508-1023.md` (Phase 4 stub) and `VCB-20260508-1530.md` (Phase 1 sample) are still there and don't follow V4.0 pattern, decide:
- Keep as historical sample (do nothing)
- Delete to clean slate (`rm output/compare-feed/TCB-*.md output/compare-feed/VCB-*.md` — but keep VCB-20260508-1530.md as reference per spec)

User decides. Default: keep all.

---

## Acceptance Criteria for V4.0 Done

1. ✅ All pytest pass (~50+ tests including 8 slugify + 22 quality_gates V4.0 + 7 render V4.0)
2. ✅ `/tin MBB` produces 1-3 markdown files, each:
   - Filename = `MBB-<date>-<hhmm>-<hook-slug>.md`
   - Title is hook (passes Gate 4)
   - Body = 1 paragraph + 3-7 substantive bullets + closing (passes Gate 3)
   - All 5 gates V4.0 PASS
3. ✅ Compare Feed right column shows 8 sections, all user-readable Vietnamese
4. ✅ Multi-article: 3 briefs → 3 files → 3 cards on IndexPage
5. ✅ Crawl funnel reject reasons = narrative + vai trò Vietnamese (Gác cổng / Tổng biên tập / Phóng viên bỏ)
6. ✅ Master data_trail + Skeptic data_trail render trên cột phải
7. ✅ Bug fixes: $ARGUMENTS substitutes correctly, Skeptic ECHO verification works, 3 articles per batch all rendered
8. ✅ KB Bank only 4 frameworks files
9. ✅ Tag `v4.0-newsroom-redesign`
10. ✅ Manual sanity: bài MBB có "luận điểm" + hook clickable, KHÔNG liệt kê. If FAIL → iterate Master prompt + bullet examples.

---

## Out of Scope V4.0

- ❌ Notion publish layer (Phase 6 deferred)
- ❌ CK + BĐS sectors (Phase 5+)
- ❌ Pipeline parallelization
- ❌ Skeptic angle clustering enforcement (variety guard)
- ❌ Auto-rewrite on gate fail (Master self-rewrite is manual loop within agent prompt)
