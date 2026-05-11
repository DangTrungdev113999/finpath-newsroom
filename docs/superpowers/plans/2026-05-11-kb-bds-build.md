# KB BĐS Build Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build 18 static knowledge base markdown files at `kb/bds/frameworks/` covering 7 BĐS categories (residential + KCN + retail + office + resort + data center + cross-category frameworks), so Master agent can analyze any Vietnamese real-estate stock.

**Architecture:** Flat folder structure (`kb/bds/frameworks/`) matching `kb/ck/` pattern. Source = 20 Notion BDS pages (1-to-1 mapping minus 2 hub-like pages consolidated). Hybrid execution: subagent fetches Notion + drafts v1, user reviews per category, validator enforces 5 hard rules.

**Tech Stack:** Python 3.13 (uv-managed), Notion MCP, existing `lib/kb_loader.py` (no changes needed), new `lib/kb_bds_validator.py` (TDD), pytest for validation tests.

**Spec reference:** `docs/superpowers/specs/2026-05-11-kb-bds-build-design.md`

---

## File Structure

**Will create:**
- `kb/bds/frameworks/` — 18 markdown files (1 hub + 5 framework chung + 12 category-specific)
- `lib/kb_bds_validator.py` — validates files against 5 principles
- `tests/test_kb_bds_validator.py` — unit tests for validator
- `tests/test_kb_loader_bds.py` — integration test that loader reads `kb/bds/`
- `docs/superpowers/plans/2026-05-11-kb-bds-build.md` — this file

**Will NOT modify:**
- `lib/kb_loader.py` — already generic via `rglob("*.md")`, works with `kb/bds/` out-of-the-box
- Existing `kb/bank/` + `kb/ck/` — independent build, no overlap

---

## Phase 1: Validator scaffolding (TDD)

### Task 1: Create directories

**Files:**
- Create: `kb/bds/frameworks/.gitkeep`

- [ ] **Step 1: Create directories**

```bash
mkdir -p kb/bds/frameworks
touch kb/bds/frameworks/.gitkeep
```

- [ ] **Step 2: Verify**

```bash
ls -la kb/bds/frameworks/
```

Expected: directory exists with `.gitkeep` file.

- [ ] **Step 3: Commit**

```bash
git add kb/bds/frameworks/.gitkeep
git commit -m "chore(kb): scaffold kb/bds/frameworks/ directory"
```

---

### Task 2: Write validator test cases (TDD red phase)

**Files:**
- Create: `tests/test_kb_bds_validator.py`

- [ ] **Step 1: Write the failing test file**

```python
"""Tests for lib.kb_bds_validator — enforces 5 KB BĐS principles."""
from pathlib import Path

import pytest

from lib.kb_bds_validator import validate_kb_file, VALID_APPLIES_TO


VALID_FILE_CONTENT = """---
category: frameworks
title: "BDS-Test-Topic"
last_updated: 2026-05-11
notion_page_id: "abc-123"
source_url: "https://notion.so/abc"
applies_to: ["residential"]
---

# Test Topic

Intro paragraph.

## Khái niệm & cơ chế

Một số định nghĩa.

## Pitfalls (đọc số dễ sai)

- **Bẫy 1**: mô tả bẫy thứ nhất với độ dài đủ thông tin.
- **Bẫy 2**: mô tả bẫy thứ hai với ví dụ lịch sử minh họa.

## Case study lịch sử

> **2024 — Residential — Lag P&L**:
> Mô tả case study.
>
> **Không analogize sang**: KCN (xem `bds-kcn-lease-structure.md`).

## Source log

- https://notion.so/abc
- Stamp: build 2026-05-11. Review every 3 years.
"""


@pytest.fixture
def valid_file(tmp_path):
    f = tmp_path / "bds-test.md"
    f.write_text(VALID_FILE_CONTENT, encoding="utf-8")
    return f


def test_valid_file_passes(valid_file):
    assert validate_kb_file(valid_file) == []


def test_missing_applies_to_fails(tmp_path):
    f = tmp_path / "bad.md"
    bad = VALID_FILE_CONTENT.replace('applies_to: ["residential"]\n', "")
    f.write_text(bad, encoding="utf-8")
    violations = validate_kb_file(f)
    assert any("applies_to" in v for v in violations)


def test_invalid_applies_to_value_fails(tmp_path):
    f = tmp_path / "bad.md"
    bad = VALID_FILE_CONTENT.replace('["residential"]', '["bogus_category"]')
    f.write_text(bad, encoding="utf-8")
    violations = validate_kb_file(f)
    assert any("invalid" in v.lower() for v in violations)


def test_missing_khai_niem_section_fails(tmp_path):
    f = tmp_path / "bad.md"
    bad = VALID_FILE_CONTENT.replace("## Khái niệm & cơ chế", "## Random Section")
    f.write_text(bad, encoding="utf-8")
    violations = validate_kb_file(f)
    assert any("Khái niệm" in v for v in violations)


def test_missing_pitfalls_section_fails(tmp_path):
    f = tmp_path / "bad.md"
    bad = VALID_FILE_CONTENT.replace("## Pitfalls (đọc số dễ sai)", "## Random")
    f.write_text(bad, encoding="utf-8")
    violations = validate_kb_file(f)
    assert any("Pitfalls" in v for v in violations)


def test_pitfall_count_below_2_fails(tmp_path):
    f = tmp_path / "bad.md"
    bad = VALID_FILE_CONTENT.replace(
        "- **Bẫy 2**: mô tả bẫy thứ hai với ví dụ lịch sử minh họa.\n",
        "",
    )
    f.write_text(bad, encoding="utf-8")
    violations = validate_kb_file(f)
    assert any("pitfall" in v.lower() and "2" in v for v in violations)


def test_missing_source_log_fails(tmp_path):
    f = tmp_path / "bad.md"
    bad = VALID_FILE_CONTENT.split("## Source log")[0]
    f.write_text(bad, encoding="utf-8")
    violations = validate_kb_file(f)
    assert any("Source log" in v for v in violations)


def test_valid_applies_to_enum_values():
    expected = {"residential", "kcn", "retail", "office", "resort", "data_center", "all"}
    assert VALID_APPLIES_TO == expected
```

- [ ] **Step 2: Run test to verify all fail (validator not implemented yet)**

Run: `uv run pytest tests/test_kb_bds_validator.py -v`

Expected: All tests FAIL with `ModuleNotFoundError: No module named 'lib.kb_bds_validator'`.

---

### Task 3: Implement validator (TDD green phase)

**Files:**
- Create: `lib/kb_bds_validator.py`

- [ ] **Step 1: Write the validator**

```python
"""KB BĐS validator — enforces 5 hard rules per design spec 2026-05-11.

Usage:
  from lib.kb_bds_validator import validate_kb_file
  violations = validate_kb_file(Path("kb/bds/frameworks/bds-res-presales-backlog.md"))
  if violations:
      for v in violations:
          print(f"  ✗ {v}")

Rules enforced (machine-checkable subset of design Section 5):
  - 5.5 Pitfall section has ≥ 2 bullet items
  - Structural: required sections present (Khái niệm, Pitfalls, Source log)
  - Frontmatter: applies_to field with valid enum values

Rules NOT machine-checked (require manual review):
  - 5.1 Static-only (no anchor data Q1/2026) — too fuzzy, manual review
  - 5.2 0% English jargon — too many edge cases (proper nouns, code blocks), manual grep
  - 5.3 Case study 3-label format — varies by file, manual verify
  - 5.4 Source log URL validity — manual verify
"""
from __future__ import annotations

import re
from pathlib import Path

VALID_APPLIES_TO = {
    "residential",
    "kcn",
    "retail",
    "office",
    "resort",
    "data_center",
    "all",
}

REQUIRED_SECTIONS = [
    "## Khái niệm",
    "## Pitfalls",
    "## Source log",
]


def _extract_frontmatter(text: str) -> str | None:
    m = re.match(r"^---\n([\s\S]*?)\n---\n", text)
    return m.group(1) if m else None


def _extract_applies_to(fm: str) -> list[str] | None:
    """Parse applies_to: ["x", "y"] line from frontmatter."""
    m = re.search(r'^applies_to:\s*\[(.*?)\]\s*$', fm, re.MULTILINE)
    if not m:
        return None
    raw = m.group(1)
    values = [v.strip().strip('"').strip("'") for v in raw.split(",")]
    return [v for v in values if v]


def _count_pitfall_items(text: str) -> int:
    """Count bullet items inside ## Pitfalls section (until next ## heading)."""
    m = re.search(r"## Pitfalls[^\n]*\n([\s\S]*?)(?=\n## |\Z)", text)
    if not m:
        return 0
    section = m.group(1)
    bullets = re.findall(r"^\s*[-*]\s+", section, re.MULTILINE)
    numbered = re.findall(r"^\s*\d+\.\s+", section, re.MULTILINE)
    return len(bullets) + len(numbered)


def validate_kb_file(path: Path) -> list[str]:
    """Return list of violation strings. Empty list = file passes validator.

    Raises FileNotFoundError if path does not exist.
    """
    text = path.read_text(encoding="utf-8")
    violations: list[str] = []

    fm = _extract_frontmatter(text)
    if fm is None:
        violations.append("Missing frontmatter block")
    else:
        applies = _extract_applies_to(fm)
        if applies is None:
            violations.append("Missing applies_to field in frontmatter")
        elif not applies:
            violations.append("applies_to is empty list")
        else:
            for v in applies:
                if v not in VALID_APPLIES_TO:
                    violations.append(
                        f"applies_to has invalid value '{v}' "
                        f"(allowed: {sorted(VALID_APPLIES_TO)})"
                    )

    for section in REQUIRED_SECTIONS:
        if section not in text:
            violations.append(f"Missing required section: {section}")

    pitfall_count = _count_pitfall_items(text)
    if pitfall_count < 2:
        violations.append(
            f"Pitfall section has {pitfall_count} bullets (require ≥ 2)"
        )

    return violations
```

- [ ] **Step 2: Run tests to verify all pass**

Run: `uv run pytest tests/test_kb_bds_validator.py -v`

Expected: All 8 tests PASS.

- [ ] **Step 3: Commit validator + tests**

```bash
git add lib/kb_bds_validator.py tests/test_kb_bds_validator.py
git commit -m "feat(kb): add kb_bds_validator — enforces structural rules"
```

---

## Phase 2: Subagent draft v1

### Task 4: Spawn subagent to fetch Notion + draft 18 files

**Files:**
- Create: `kb/bds/frameworks/*.md` (18 files via subagent)

- [ ] **Step 1: Dispatch general-purpose subagent**

Use Agent tool with `subagent_type: "general-purpose"`. Prompt:

```
You are drafting 18 markdown files for kb/bds/frameworks/ — a static knowledge base
for Vietnamese real-estate stocks. Full spec at docs/superpowers/specs/2026-05-11-kb-bds-build-design.md.

YOUR TASK — 2 stages:

STAGE 1: Fetch 20 Notion pages via Notion MCP (mcp__notion__API-get-block-children).
Page IDs (format with dashes for UUID):

Hub & roots (2 pages — for hub file):
  35d273c7-a9a1-81ca-84b4-eb18795d8a70  (BĐS Sector hub)
  35d273c7-a9a1-8190-b873-fadad6e1c7a0  (KB BĐS root)

Framework chung (5 pages):
  35d273c7-a9a1-81bf-929a-fbbe138f93cc  (Debt-leverage-general)
  35d273c7-a9a1-81cd-94f7-d4a41d830898  (Macro-cycle-and-credit)
  35d273c7-a9a1-8138-8005-d61d898f3fdc  (Revenue-recognition-VAS)
  35d273c7-a9a1-81d7-aa0c-eae5ac0a6707  (Legal-framework-overview)
  35d273c7-a9a1-8102-b0fd-f183e8075e7c  (Hybrid-business-models)

Residential (3):
  35d273c7-a9a1-817d-a2e7-ee0fd8c7335a  (RES-Presales-backlog)
  35d273c7-a9a1-81f2-91a2-ddd655c965f7  (RES-Land-bank-NAV)
  35d273c7-a9a1-810b-9d77-f095899340a6  (RES-Project-lifecycle)

KCN (3):
  35d273c7-a9a1-815a-9a2b-f075d768f14f  (KCN-FDI-demand-mechanism)
  35d273c7-a9a1-8159-821a-ff256913a328  (KCN-Inventory-and-pricing)
  35d273c7-a9a1-8150-b2ff-f1c429d93275  (KCN-Lease-structure)

Retail (3):
  35d273c7-a9a1-8165-8cf4-fbbbcbba4e48  (RETAIL-Footfall-mechanism)
  35d273c7-a9a1-81e2-8703-f25520100191  (RETAIL-Tenant-mix-quality)
  35d273c7-a9a1-8164-af6c-f1a19073e216  (RETAIL-Anchor-vs-SME-tenants)

Office (2):
  35d273c7-a9a1-819d-909a-d8587dabaa43  (OFFICE-Class-tiering)
  35d273c7-a9a1-8194-8eac-c0b3e6ea1732  (OFFICE-Hybrid-work-impact)

Resort (3):
  35d273c7-a9a1-8159-9836-edc1628c2ef0  (RESORT-Condotel-legal-pitfalls)
  35d273c7-a9a1-815c-b071-d2a8f6230a8e  (RESORT-Tourism-cycle)
  35d273c7-a9a1-816c-a987-d5466d863c4d  (RESORT-Hybrid-model)

Data Center (1):
  35d273c7-a9a1-8165-adb0-f87372d60534  (DC-Hyperscaler-and-power)

Extract plain_text from each block. Ignore Notion JSON noise. If a block has
has_children=true, recursively fetch via mcp__notion__API-get-block-children.

STAGE 2: Write 18 markdown files to /Users/trungdt/Desktop/Stream Intelligent/kb/bds/frameworks/:

File names (each maps 1-to-1 with a Notion page, plus 1 hub merging 2 root pages):

  bds-industry-master-reference.md           ← merge: BĐS Sector hub + KB BĐS root
  bds-revenue-recognition-vas.md             ← Revenue-recognition-VAS
  bds-debt-leverage.md                       ← Debt-leverage-general
  bds-macro-cycle-credit.md                  ← Macro-cycle-and-credit
  bds-legal-framework.md                     ← Legal-framework-overview
  bds-hybrid-business-models.md              ← Hybrid-business-models
  bds-res-presales-backlog.md                ← RES-Presales-backlog
  bds-res-land-bank-nav.md                   ← RES-Land-bank-NAV
  bds-res-project-lifecycle.md               ← RES-Project-lifecycle
  bds-kcn-fdi-demand-mechanism.md            ← KCN-FDI-demand-mechanism
  bds-kcn-inventory-pricing.md               ← KCN-Inventory-and-pricing
  bds-kcn-lease-structure.md                 ← KCN-Lease-structure
  bds-retail-footfall-mechanism.md           ← RETAIL-Footfall-mechanism
  bds-retail-tenant-mix-quality.md           ← RETAIL-Tenant-mix-quality
  bds-retail-anchor-vs-sme-tenants.md        ← RETAIL-Anchor-vs-SME-tenants
  bds-office-class-tiering.md                ← OFFICE-Class-tiering
  bds-office-hybrid-work-impact.md           ← OFFICE-Hybrid-work-impact
  bds-resort-condotel-legal-pitfalls.md      ← RESORT-Condotel-legal-pitfalls
  bds-resort-tourism-cycle.md                ← RESORT-Tourism-cycle
  bds-resort-hybrid-model.md                 ← RESORT-Hybrid-model
  bds-dc-hyperscaler-power.md                ← DC-Hyperscaler-and-power

FILE TEMPLATE (use exactly this structure):

---
category: frameworks
title: "BDS-{Topic}"
last_updated: 2026-05-11
notion_page_id: "<uuid>"
source_url: "https://notion.so/<id-no-dashes>"
applies_to: [<from list: residential, kcn, retail, office, resort, data_center, all>]
---

# {Vietnamese pure title}

{Intro 2-3 sentences — purpose + when Master reads}

## Khái niệm & cơ chế

{Definitions + mechanism, Vietnamese pure}

## Threshold benchmark dài hạn

{Long-term ranges, e.g. "D/E peak 1.5-2.0x normal, >2.5x warning". NOT per-quarter snapshots.}

## Pitfalls (đọc số dễ sai)

- **Bẫy 1**: descriptive bullet ≥20 words with historical example
- **Bẫy 2**: another bullet ≥20 words
- ... aim 3-5 pitfalls per file

## Case study lịch sử

> **{Year} — {Type: residential/kcn/retail/office/resort/dc} — Minh họa {mechanism}**:
> {2-3 sentences}
>
> **Không analogize sang**: {other BĐS types with link to relevant framework file}

## Regulatory (if applicable)

{Laws + Circulars, historical (already enacted)}

## Source log

- {Notion URL}
- {News URLs from Notion source log}
- Stamp: build 2026-05-11. Review every {N} years.

CRITICAL CONTENT RULES (per spec Section 5):

1. STATIC ONLY — NO anchor data Q1/Q2/Q3/Q4 2026. NO "hiện tại / hiện hành / đến nay /
   tính đến". Historical case studies with year label OK. Future-tense projections NOT OK.

2. VIETNAMESE PURE — 0% English jargon. Mapping table:
   - pre-sales → doanh số bán trước
   - backlog → doanh số chờ ghi nhận
   - landbank → quỹ đất
   - NAV → giá trị tài sản ròng
   - P/NAV → hệ số giá trên giá trị tài sản ròng
   - cap rate → tỷ suất sinh lời cho thuê
   - GFA → tổng diện tích sàn
   - NLA → diện tích cho thuê thuần
   - occupancy rate → tỷ lệ lấp đầy
   - footfall → lượt khách
   - anchor tenant → khách thuê chủ chốt
   - FDI → vốn đầu tư trực tiếp nước ngoài
   - hyperscaler → khách hàng đám mây lớn
   - condotel → căn hộ khách sạn
   - lease → hợp đồng thuê
   - POS recognition → ghi nhận khi bàn giao
   - POC recognition → ghi nhận theo tiến độ
   - lump-sum → ghi nhận một lần
   - recurring revenue → doanh thu định kỳ
   - EXCEPTION: proper nouns (Vinhomes, Vincom Retail, Ocean City, Aqua City,
     Sun Group...) + stock tickers (VHM, NVL, KDH, DXG, KBC, VRE, SDI, NTL...).

3. CASE STUDY 3-LABEL — every case study MUST have year + type + mechanism + "Không
   analogize sang" line. If Notion source has case study, reformat to this template.

4. STRIP NOTION ANNOTATIONS — Notion content often has [SUY LUẬN] / [CHƯA VERIFY] /
   [SOURCE] / [Stamp] tags. STRIP all 4 from KB output (those are internal Notion
   annotations, not for Master consumption). Keep the underlying content, drop the tags.

5. EACH FILE ≥ 2 PITFALLS. If Notion source has fewer, expand from spec discussion +
   reasonable analyst common knowledge.

6. HUB FILE (bds-industry-master-reference.md) MUST CONTAIN:
   - 6-layer mental model (copy CK pattern from kb/ck/frameworks/ck-industry-master-reference.md)
   - Routing table: ticker → loại BĐS → framework file apply (≥ 30 tickers covered:
     VHM, NVL, KDH, DXG, NLG, KBC, BCM, IDC, SZC, SIP, SNZ, VRE, AEON, SDI, NTL,
     and listed REITs / hybrid players)

7. applies_to FIELD per file:
   - Framework chung (5 files): ["all"]
   - bds-res-*: ["residential"]
   - bds-kcn-*: ["kcn"]
   - bds-retail-*: ["retail"]
   - bds-office-*: ["office"]
   - bds-resort-*: ["resort"]
   - bds-dc-*: ["data_center"]
   - bds-industry-master-reference.md: ["all"]

OUTPUT FORMAT — for each file written, print:
  ✓ kb/bds/frameworks/<filename>.md  (<line_count> lines)

End with summary: "18 files drafted. Ready for user review."

IMPORTANT — read the actual CK pattern first:
  Read /Users/trungdt/Desktop/Stream Intelligent/kb/ck/frameworks/ck-industry-master-reference.md
  Read /Users/trungdt/Desktop/Stream Intelligent/kb/ck/frameworks/ck-margin-cycle.md
These show the expected voice + section depth + writing style.
```

- [ ] **Step 2: Wait for subagent completion**

Subagent reports `✓ kb/bds/frameworks/<file>.md` per file. Expect 18 success lines + summary "18 files drafted. Ready for user review."

- [ ] **Step 3: Verify file count**

```bash
ls kb/bds/frameworks/*.md | wc -l
```

Expected: `18` (plus `.gitkeep` already there — total `ls` output line count: 19).

- [ ] **Step 4: Commit draft v1 as rollback point**

```bash
git add kb/bds/frameworks/
git commit -m "feat(kb): BĐS draft v1 from Notion (subagent) — pre-review"
```

---

### Task 5: Run validator on draft v1

**Files:**
- Test: existing `lib/kb_bds_validator.py`

- [ ] **Step 1: Write validation script + run**

```bash
uv run python -c "
from pathlib import Path
from lib.kb_bds_validator import validate_kb_file

files = sorted(Path('kb/bds/frameworks').glob('*.md'))
total_violations = 0
for f in files:
    violations = validate_kb_file(f)
    if violations:
        print(f'\\n✗ {f.name}:')
        for v in violations:
            print(f'    {v}')
        total_violations += len(violations)
    else:
        print(f'✓ {f.name}')
print(f'\\nTotal: {total_violations} violations across {len(files)} files')
"
```

Expected: Output lists violations per file. Save full output for use in review tasks.

- [ ] **Step 2: Manually grep for English jargon**

```bash
cd kb/bds/frameworks && rg -i "\b(pre-sales|backlog|landbank|cap rate|footfall|anchor tenant|hyperscaler|condotel|lease|lump-sum|recurring revenue|GFA|NLA|FDI|occupancy)\b" --type md 2>/dev/null || echo "(no matches)"
```

Expected: List of English jargon occurrences (file:line). Save output for review tasks.

- [ ] **Step 3: Grep for anchor data + Notion annotation leaks**

```bash
cd kb/bds/frameworks && rg "\[SUY LUẬN\]|\[CHƯA VERIFY\]|hiện tại|hiện hành|đến nay|tính đến" --type md 2>/dev/null || echo "(no matches)"
```

Expected: List of anchor data + annotation leaks. Save output for review tasks.

---

## Phase 3: Review per category

Each review task: read 1-6 files, apply fixes from validator + grep output (English jargon → Vietnamese, strip annotations, strip rolling current refs, add missing pitfalls), re-run validator + grep until clean, then proceed.

### Task 6: Review hub + framework chung (6 files)

**Files:**
- Modify: `kb/bds/frameworks/bds-industry-master-reference.md`
- Modify: `kb/bds/frameworks/bds-revenue-recognition-vas.md`
- Modify: `kb/bds/frameworks/bds-debt-leverage.md`
- Modify: `kb/bds/frameworks/bds-macro-cycle-credit.md`
- Modify: `kb/bds/frameworks/bds-legal-framework.md`
- Modify: `kb/bds/frameworks/bds-hybrid-business-models.md`

- [ ] **Step 1: Read all 6 files**

Use Read tool on each. Note section structure + identify violations from Task 5 output.

- [ ] **Step 2: Fix English jargon per file**

For each file, replace English jargon using mapping table (Section 5.2 of spec). Use Edit tool with `replace_all=true` per jargon word where safe (NOT within proper nouns or code blocks).

Example for `bds-revenue-recognition-vas.md`:
- Replace `pre-sales` → `doanh số bán trước`
- Replace `backlog` → `doanh số chờ ghi nhận`
- Replace `recurring` → `định kỳ`
- Replace `lump-sum` → `ghi nhận một lần`

- [ ] **Step 3: Strip Notion annotations**

For each file, find + delete `[SUY LUẬN]`, `[CHƯA VERIFY]`, `[SOURCE]` tags but KEEP the underlying content sentences. Use Edit tool.

- [ ] **Step 4: Strip rolling current refs**

For each file, find phrases like "hiện tại / hiện hành / đến nay / tính đến tháng X" and either delete or rephrase to historical year-labeled. Use Edit tool.

- [ ] **Step 5: Verify hub file routing table**

Open `bds-industry-master-reference.md`. Verify routing table exists covering ≥ 30 tickers:
- VHM, NVL, KDH, DXG, NLG → bds-res-*
- KBC, BCM, IDC, SZC, SIP, SNZ → bds-kcn-*
- VRE, AEON → bds-retail-*
- SDI, NTL → bds-resort-*
- VNG Data, CMC, FPT DC → bds-dc-*

If missing → add table via Edit tool.

- [ ] **Step 6: Re-run validator on these 6 files**

```bash
uv run python -c "
from pathlib import Path
from lib.kb_bds_validator import validate_kb_file
files = ['bds-industry-master-reference', 'bds-revenue-recognition-vas',
         'bds-debt-leverage', 'bds-macro-cycle-credit', 'bds-legal-framework',
         'bds-hybrid-business-models']
for name in files:
    f = Path(f'kb/bds/frameworks/{name}.md')
    violations = validate_kb_file(f)
    print(('✓' if not violations else '✗'), name)
    for v in violations:
        print(f'    {v}')
"
```

Expected: All 6 files show `✓`. Repeat fix steps if any `✗`.

---

### Task 7: Review residential (3 files)

**Files:**
- Modify: `kb/bds/frameworks/bds-res-presales-backlog.md`
- Modify: `kb/bds/frameworks/bds-res-land-bank-nav.md`
- Modify: `kb/bds/frameworks/bds-res-project-lifecycle.md`

- [ ] **Step 1: Apply same 5-step review pattern as Task 6 to these 3 files**

Read → fix English jargon → strip annotations → strip rolling refs → verify case studies have 3-label format + "Không analogize sang" line linking to other framework files.

- [ ] **Step 2: Re-run validator on these 3 files**

```bash
uv run python -c "
from pathlib import Path
from lib.kb_bds_validator import validate_kb_file
for name in ['bds-res-presales-backlog', 'bds-res-land-bank-nav', 'bds-res-project-lifecycle']:
    f = Path(f'kb/bds/frameworks/{name}.md')
    violations = validate_kb_file(f)
    print(('✓' if not violations else '✗'), name)
    for v in violations:
        print(f'    {v}')
"
```

Expected: All 3 files `✓`.

---

### Task 8: Review KCN (3 files)

**Files:**
- Modify: `kb/bds/frameworks/bds-kcn-fdi-demand-mechanism.md`
- Modify: `kb/bds/frameworks/bds-kcn-inventory-pricing.md`
- Modify: `kb/bds/frameworks/bds-kcn-lease-structure.md`

- [ ] **Step 1: Apply 5-step review pattern**

Special attention: KCN has heavy English jargon (FDI, hyperscaler nếu liên quan DC tangential, lease, MOU). Use mapping table strictly.

- [ ] **Step 2: Verify case studies don't analogize KCN pattern to residential**

KCN one-shot lease recognition ≠ residential POS bàn giao. Case study should call this out explicitly.

- [ ] **Step 3: Re-run validator**

```bash
uv run python -c "
from pathlib import Path
from lib.kb_bds_validator import validate_kb_file
for name in ['bds-kcn-fdi-demand-mechanism', 'bds-kcn-inventory-pricing', 'bds-kcn-lease-structure']:
    f = Path(f'kb/bds/frameworks/{name}.md')
    violations = validate_kb_file(f)
    print(('✓' if not violations else '✗'), name)
    for v in violations:
        print(f'    {v}')
"
```

Expected: All 3 files `✓`.

---

### Task 9: Review retail (3 files)

**Files:**
- Modify: `kb/bds/frameworks/bds-retail-footfall-mechanism.md`
- Modify: `kb/bds/frameworks/bds-retail-tenant-mix-quality.md`
- Modify: `kb/bds/frameworks/bds-retail-anchor-vs-sme-tenants.md`

- [ ] **Step 1: Apply 5-step review pattern**

Heavy English jargon expected: footfall, anchor tenant, SME, tenant mix, occupancy rate.

- [ ] **Step 2: Re-run validator**

```bash
uv run python -c "
from pathlib import Path
from lib.kb_bds_validator import validate_kb_file
for name in ['bds-retail-footfall-mechanism', 'bds-retail-tenant-mix-quality', 'bds-retail-anchor-vs-sme-tenants']:
    f = Path(f'kb/bds/frameworks/{name}.md')
    violations = validate_kb_file(f)
    print(('✓' if not violations else '✗'), name)
    for v in violations:
        print(f'    {v}')
"
```

Expected: All 3 files `✓`.

---

### Task 10: Review office (2 files)

**Files:**
- Modify: `kb/bds/frameworks/bds-office-class-tiering.md`
- Modify: `kb/bds/frameworks/bds-office-hybrid-work-impact.md`

- [ ] **Step 1: Apply 5-step review pattern**

Heavy English jargon: Grade A/B/C, hybrid work, work-from-home, prime CBD, occupancy.

- [ ] **Step 2: Re-run validator**

```bash
uv run python -c "
from pathlib import Path
from lib.kb_bds_validator import validate_kb_file
for name in ['bds-office-class-tiering', 'bds-office-hybrid-work-impact']:
    f = Path(f'kb/bds/frameworks/{name}.md')
    violations = validate_kb_file(f)
    print(('✓' if not violations else '✗'), name)
    for v in violations:
        print(f'    {v}')
"
```

Expected: Both files `✓`.

---

### Task 11: Review resort (3 files)

**Files:**
- Modify: `kb/bds/frameworks/bds-resort-condotel-legal-pitfalls.md`
- Modify: `kb/bds/frameworks/bds-resort-tourism-cycle.md`
- Modify: `kb/bds/frameworks/bds-resort-hybrid-model.md`

- [ ] **Step 1: Apply 5-step review pattern**

Heavy English jargon: condotel, RevPAR, ADR, occupancy.

- [ ] **Step 2: Special — verify condotel-legal-pitfalls has ≥ 4 pitfalls**

Condotel pháp lý đặc biệt complex (sổ hồng vs SH du lịch vs chứng nhận sở hữu). File này cần thêm pitfall. Use Edit to add bullets nếu < 4.

- [ ] **Step 3: Re-run validator**

```bash
uv run python -c "
from pathlib import Path
from lib.kb_bds_validator import validate_kb_file
for name in ['bds-resort-condotel-legal-pitfalls', 'bds-resort-tourism-cycle', 'bds-resort-hybrid-model']:
    f = Path(f'kb/bds/frameworks/{name}.md')
    violations = validate_kb_file(f)
    print(('✓' if not violations else '✗'), name)
    for v in violations:
        print(f'    {v}')
"
```

Expected: All 3 files `✓`.

---

### Task 12: Review data center (1 file)

**Files:**
- Modify: `kb/bds/frameworks/bds-dc-hyperscaler-power.md`

- [ ] **Step 1: Apply 5-step review pattern**

Heavy English jargon: hyperscaler, AWS, Google Cloud, Azure (giữ tên riêng AWS/Google/Azure), Tier 3/4 (giữ — terminology kỹ thuật quốc tế).

Mapping:
- hyperscaler → khách hàng đám mây lớn
- colocation → cho thuê chỗ đặt máy chủ
- power density (kW/rack) → mật độ điện (kW/tủ)
- uptime → thời gian hoạt động ổn định

- [ ] **Step 2: Re-run validator**

```bash
uv run python -c "
from pathlib import Path
from lib.kb_bds_validator import validate_kb_file
f = Path('kb/bds/frameworks/bds-dc-hyperscaler-power.md')
violations = validate_kb_file(f)
print(('✓' if not violations else '✗'), f.stem)
for v in violations:
    print(f'    {v}')
"
```

Expected: File `✓`.

---

### Task 13: Final all-files validator pass + commit review v2

**Files:**
- All 18 files in `kb/bds/frameworks/`

- [ ] **Step 1: Run validator on ALL 18 files**

```bash
uv run python -c "
from pathlib import Path
from lib.kb_bds_validator import validate_kb_file
files = sorted(Path('kb/bds/frameworks').glob('*.md'))
all_pass = True
for f in files:
    violations = validate_kb_file(f)
    if violations:
        all_pass = False
        print(f'\\n✗ {f.name}:')
        for v in violations:
            print(f'    {v}')
    else:
        print(f'✓ {f.name}')
print(f'\\n{\"ALL PASS\" if all_pass else \"VIOLATIONS REMAIN\"}: {len(files)} files')
"
```

Expected: All 18 files `✓`. Output ends with `ALL PASS: 18 files`.

- [ ] **Step 2: Final English jargon sweep**

```bash
cd kb/bds/frameworks && rg -i "\b(pre-sales|backlog|landbank|cap rate|footfall|anchor tenant|hyperscaler|condotel|GFA|NLA|FDI|occupancy|lease|lump-sum)\b" --type md 2>/dev/null
```

Expected: No output (empty). If any output → grep flagged a word, manually decide if it's a proper noun (KEEP — vd "Vincom Retail anchor tenants") or text (FIX with Edit).

- [ ] **Step 3: Final Notion annotation sweep**

```bash
cd kb/bds/frameworks && rg "\[SUY LUẬN\]|\[CHƯA VERIFY\]|hiện tại|hiện hành|đến nay" --type md 2>/dev/null
```

Expected: No output.

- [ ] **Step 4: Commit review v2**

```bash
git add kb/bds/frameworks/
git commit -m "feat(kb): BĐS review v2 — apply 5 principles (Vietnamese pure, static-only, 3-label case studies)"
```

---

## Phase 4: Integration tests

### Task 14: Write kb_loader integration test for BĐS

**Files:**
- Create: `tests/test_kb_loader_bds.py`

- [ ] **Step 1: Write test**

```python
"""Integration test — kb_loader can find BĐS topics."""
from pathlib import Path

from lib.kb_loader import KBLoader


def test_loader_finds_bds_residential_topics():
    loader = KBLoader(Path("kb/bds"))
    results = loader.search(["doanh số bán trước"])
    assert len(results) >= 1
    assert any("res-presales-backlog" in r["path"] for r in results)


def test_loader_finds_bds_legal_topics():
    loader = KBLoader(Path("kb/bds"))
    results = loader.search(["Luật Kinh doanh"])
    assert len(results) >= 1


def test_loader_finds_bds_master_reference():
    loader = KBLoader(Path("kb/bds"))
    results = loader.search(["6 lớp"])  # 6-layer mental model
    assert len(results) >= 1
    assert any("industry-master-reference" in r["path"] for r in results)


def test_loader_returns_all_18_files():
    loader = KBLoader(Path("kb/bds"))
    all_files = loader._all_files()
    md_files = [f for f in all_files if f.suffix == ".md"]
    assert len(md_files) == 18
```

- [ ] **Step 2: Run test**

```bash
uv run pytest tests/test_kb_loader_bds.py -v
```

Expected: All 4 tests PASS.

If any fail → file content missing expected keyword. Re-open the file, ensure key concepts use Vietnamese pure terms (especially `doanh số bán trước`, `Luật Kinh doanh`, `6 lớp`).

- [ ] **Step 3: Commit integration test**

```bash
git add tests/test_kb_loader_bds.py
git commit -m "test(kb): integration test — kb_loader reads kb/bds/ 18 files"
```

---

### Task 15: Manual routing table verification

**Files:**
- Verify: `kb/bds/frameworks/bds-industry-master-reference.md`

- [ ] **Step 1: Read hub file routing table**

```bash
grep -A 50 "Routing table\|routing.*ticker\|loại BĐS" kb/bds/frameworks/bds-industry-master-reference.md
```

- [ ] **Step 2: Verify minimum coverage**

Required tickers in routing table:
- Residential: VHM, NVL, KDH, DXG, NLG (5 tickers)
- KCN: KBC, BCM, IDC, SZC, SIP, SNZ (6 tickers)
- Retail: VRE, AEON (2)
- Office: any 2 listed REITs
- Resort: SDI, NTL, NVL hybrid (3)
- Data Center: VNG Data, CMC, FPT (3)

**Total ≥ 20 unique tickers** mapped to framework files.

If missing → Edit hub file to add. Re-commit.

---

## Phase 5: Update CLAUDE.md + push

### Task 16: Update CLAUDE.md architecture map

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Find architecture map section**

```bash
grep -n "kb/bank\|kb/ck\|Architecture map" CLAUDE.md
```

- [ ] **Step 2: Update map**

Use Edit tool to update the architecture map block:

Old (find current state):
```
kb/bank/                         → Markdown KB (bootstrap từ Notion Bank Sector page)
```

New (add `kb/bds/` + `kb/ck/`):
```
kb/bank/                         → Markdown KB Bank (7 mã: TCB/VCB/MBB/ACB/BID/CTG/VPB)
kb/ck/                           → Markdown KB CK (5 mã: SSI/VND/HCM/VCI/SHS)
kb/bds/                          → Markdown KB BĐS (18 file, 7 category — residential/KCN/retail/office/resort/DC + framework chung)
```

- [ ] **Step 3: Commit doc update**

```bash
git add CLAUDE.md
git commit -m "docs(claude.md): add kb/bds/ + kb/ck/ to architecture map"
```

---

### Task 17: Push to remote (ASK USER FIRST)

**Files:**
- None modified — git operation only.

- [ ] **Step 1: Show user the commits to be pushed**

```bash
git log --oneline origin/main..HEAD
```

- [ ] **Step 2: Ask user**

> "Sếp xem list commit trên — push lên `origin/main` được chưa?"

- [ ] **Step 3: If user confirms, push**

```bash
git push origin main
```

Expected: Push succeeds. CI (if any) green.

If user declines → leave commits local, user pushes later.

---

## Plan Verification

### Spec Coverage Check

- [x] Spec Section 1 (Mục tiêu): Phase 2-3 builds 18 file static KB
- [x] Spec Section 2 (Scope): Task 4 subagent covers 7 categories
- [x] Spec Section 3 (Architecture): Task 1 creates dir, Task 4 populates
- [x] Spec Section 4 (Per-file template): Task 4 subagent prompt embeds template + applies_to enum from Task 2/3 validator
- [x] Spec Section 5.1 (Static-only): Task 5 grep for rolling refs, Task 6-12 strip
- [x] Spec Section 5.2 (Vietnamese pure): Task 5 jargon grep, Task 6-12 fix via mapping table
- [x] Spec Section 5.3 (Case study guardrail): Subagent prompt requires 3-label, Task 6-12 verify
- [x] Spec Section 5.4 (Source log): Validator REQUIRED_SECTIONS includes `## Source log`
- [x] Spec Section 5.5 (≥ 2 pitfall): Validator `_count_pitfall_items` enforces
- [x] Spec Section 6 Stage 1-2 (Subagent): Task 4
- [x] Spec Section 6 Stage 3 (User review): Tasks 6-12 per category
- [x] Spec Section 6 Stage 4 (kb_loader): Task 14 integration test
- [x] Spec Section 6 Stage 5 (Commit + update CLAUDE.md): Tasks 13, 16
- [x] Spec Section 7 Risks (subagent leak jargon): mitigated by Task 5 grep + Tasks 6-12 fix
- [x] Spec Section 8 Success criteria: covered by Tasks 13, 14, 15

### Placeholder Scan

- No `TBD`, `TODO`, `fill in details`, or `similar to Task N` references.
- All test code shown in full.
- All grep + uv commands shown with full command lines + expected output.

### Type / Name Consistency

- `VALID_APPLIES_TO` enum: 7 values, used identically in validator (Task 3) + test (Task 2) + subagent prompt (Task 4).
- File names: 18 files listed identically in spec Section 3, subagent prompt (Task 4), validation loops (Tasks 5, 13).
- Function name `validate_kb_file` used consistently across Tasks 2, 3, 5, 6-12, 13.

---

## Notes for executor

- **TDD discipline:** Task 2 writes failing tests BEFORE Task 3 implements. Verify red → green transition.
- **Subagent supervision:** Task 4 is the biggest single step. Watch for: incomplete file count, validator violations, English leakage. Don't blindly accept output.
- **Per-category batching (Tasks 6-12):** Designed so each batch is reviewable in 15-30 min. If batch fails validator after 2 fix attempts, escalate to user.
- **Atomic commits:** 6 commit points (Task 1, 3, 4, 13, 14, 16) + optional 17 push. Each leaves repo in working state.
