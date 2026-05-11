# Bank + CK Universe Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand Bank + CK universe trong Finpath Newsroom pipeline từ MVP (7+5=12 mã) → toàn bộ niêm yết HOSE/HNX/UPCOM (27+30=57 mã). BĐS giữ nguyên 4 mã.

**Architecture:** Big-bang rollout, 5 atomic commit phase A-E + Phase F verification. Pure data update — KHÔNG rewrite KB framework markdown, Master skill workflow, Finpath API endpoints. TDD Phase A foundational (catch alias regression early), Phase B-E parallel-safe mechanical text update sau Phase A pass.

**Tech Stack:** Python 3.13 (uv), pytest, Markdown KB, Claude agent + skill markdown.

**Spec reference:** `docs/superpowers/specs/2026-05-11-bank-ck-universe-expansion-design.md`

---

## File Structure

**Will modify (14 file):**

| Phase | File | Change type |
|---|---|---|
| A | `.claude/skills/finpath-newsroom-editor/scripts/routing.py` | Expand BANK_UNIVERSE 7→27, CK_UNIVERSE 5→30 |
| A | `.claude/skills/finpath-newsroom-editor/scripts/ticker_detection.py` | Expand alias map ~16→80, SHORT_FORM_TO_TICKER 8→57 |
| B | `.claude/skills/finpath-newsroom-master-bank/SKILL.md` | Frontmatter description text |
| B | `.claude/skills/finpath-newsroom-master-ck/SKILL.md` | Frontmatter description text |
| B | `.claude/agents/newsroom-master-bank.md` | Wrapper description text |
| B | `.claude/agents/newsroom-master-ck.md` | Wrapper description text |
| C | `kb/bank/frameworks/bank-industry-master-reference.md` | Append rows tiering tables |
| C | `kb/ck/frameworks/ck-industry-master-reference.md` | Append rows mô hình kinh doanh tables |
| D | `.claude/agents/newsroom-pipeline.md` | Universe references text |
| D | `.claude/agents/newsroom-editor.md` | Description + Step 2 text |
| D | `.claude/skills/finpath-newsroom-orchestrator/SKILL.md` | Universe section text |
| E | `.claude/commands/tin.md` | Alias mapping expanded |
| E | `.claude/commands/tin-batch.md` | Alias mapping expanded |
| E | `CLAUDE.md` | Architecture map text |

**Will create (1 file):**

- `tests/test_routing_expanded.py` — new unit tests cho expanded universe + alias detection

---

## Phase A — Universe registry + alias (TDD foundational)

### Task 1: Write failing tests for expanded universe + alias

**Files:**
- Create: `tests/test_routing_expanded.py`

- [ ] **Step 1: Write the failing test file**

```python
"""Tests for Bank + CK universe expansion (spec 2026-05-11)."""
import sys
from pathlib import Path

# Add skill scripts to path for import
SCRIPTS_DIR = Path(__file__).parent.parent / ".claude" / "skills" / "finpath-newsroom-editor"
sys.path.insert(0, str(SCRIPTS_DIR))

from scripts.routing import BANK_UNIVERSE, CK_UNIVERSE, BDS_UNIVERSE, FULL_UNIVERSE, get_sector
from scripts.ticker_detection import detect_combined, COMPANY_NAME_TO_TICKER, SHORT_FORM_TO_TICKER


# === Universe size assertions ===

def test_bank_universe_27_tickers():
    assert len(BANK_UNIVERSE) == 27


def test_ck_universe_30_tickers():
    assert len(CK_UNIVERSE) == 30


def test_bds_universe_unchanged():
    assert BDS_UNIVERSE == ["VHM", "NVL", "KDH", "DXG"]


def test_full_universe_61_tickers():
    assert len(FULL_UNIVERSE) == 61


# === Bank universe membership ===

def test_bank_hose_tickers_present():
    expected = ["VCB", "CTG", "BID", "TCB", "MBB", "ACB", "VPB", "HDB",
                "STB", "SHB", "EIB", "TPB", "MSB", "LPB", "OCB", "VIB"]
    for t in expected:
        assert t in BANK_UNIVERSE, f"Missing HOSE bank: {t}"


def test_bank_hnx_tickers_present():
    for t in ["NAB", "BAB", "NVB", "SGB"]:
        assert t in BANK_UNIVERSE, f"Missing HNX bank: {t}"


def test_bank_upcom_tickers_present():
    for t in ["VAB", "BVB", "ABB", "KLB", "VBB", "PGB", "HDF"]:
        assert t in BANK_UNIVERSE, f"Missing UPCOM bank: {t}"


# === CK universe membership ===

def test_ck_hose_tickers_present():
    for t in ["SSI", "VND", "HCM", "VCI", "VIX"]:
        assert t in CK_UNIVERSE, f"Missing HOSE CK: {t}"


def test_ck_hnx_tickers_present():
    expected = ["SHS", "MBS", "BVS", "BSI", "AGR", "CTS", "APG", "EVS",
                "IVS", "PSI", "TVS", "WSS", "ORS", "VFS", "TCI"]
    for t in expected:
        assert t in CK_UNIVERSE, f"Missing HNX CK: {t}"


def test_ck_upcom_tickers_present():
    expected = ["DSC", "FTS", "CSI", "SBS", "PHS", "ART", "APS", "BMS", "AAS", "VTS"]
    for t in expected:
        assert t in CK_UNIVERSE, f"Missing UPCOM CK: {t}"


# === get_sector for all expanded tickers ===

def test_get_sector_all_bank():
    for ticker in BANK_UNIVERSE:
        assert get_sector(ticker) == "Bank", f"{ticker} should map to Bank"


def test_get_sector_all_ck():
    for ticker in CK_UNIVERSE:
        assert get_sector(ticker) == "CK", f"{ticker} should map to CK"


def test_get_sector_unknown_ticker_returns_none():
    assert get_sector("XYZ") is None
    assert get_sector("ZZZ") is None


# === Alias detection — new Bank companies ===

def test_alias_sacombank_detects_stb():
    assert "STB" in detect_combined("Sacombank công bố lợi nhuận quý 1")


def test_alias_eximbank_detects_eib():
    assert "EIB" in detect_combined("Eximbank tăng vốn điều lệ năm 2026")


def test_alias_hdbank_detects_hdb():
    assert "HDB" in detect_combined("HDBank phát hành cổ phiếu thưởng")


def test_alias_tpbank_detects_tpb():
    assert "TPB" in detect_combined("TPBank công bố BCTC quý 2")


def test_alias_lpbank_detects_lpb():
    assert "LPB" in detect_combined("LPBank đổi tên từ LienVietPostBank")


def test_alias_maritime_bank_detects_msb():
    assert "MSB" in detect_combined("Maritime Bank tăng tín dụng 12%")


def test_alias_nam_a_bank_detects_nab():
    assert "NAB" in detect_combined("Nam Á Bank niêm yết HNX 2024")


# === Alias detection — new CK companies ===

def test_alias_fpts_detects_fts():
    assert "FTS" in detect_combined("FPTS báo cáo doanh thu môi giới")


def test_alias_mbs_detects():
    assert "MBS" in detect_combined("MB Securities tăng vốn cho vay ký quỹ")


def test_alias_bsi_detects():
    assert "BSI" in detect_combined("BIDV Securities công bố lợi nhuận quý 1")


def test_alias_agriseco_detects_agr():
    assert "AGR" in detect_combined("Agriseco mở rộng thị phần môi giới")


def test_alias_petrosetco_detects_psi():
    assert "PSI" in detect_combined("Petrosetco công bố doanh thu tự doanh")


# === Pass 2 short-form uppercase regex ===

def test_short_form_regex_covers_all_universe():
    """SHORT_FORM_TO_TICKER must cover all 57 new tickers + 4 BĐS."""
    for ticker in BANK_UNIVERSE + CK_UNIVERSE + BDS_UNIVERSE:
        assert ticker in SHORT_FORM_TO_TICKER, f"Missing SHORT_FORM entry: {ticker}"


def test_short_form_detects_raw_uppercase_stb():
    """STB alone (no Sacombank in text) should still detect."""
    assert "STB" in detect_combined("STB công bố lợi nhuận Q2/2026")


def test_short_form_detects_raw_uppercase_eib():
    assert "EIB" in detect_combined("EIB tăng vốn lên 25 nghìn tỷ")


# === No regression — existing MVP detection still works ===

def test_existing_mvp_bank_detection():
    """VCB/TCB/MBB detection still works after expansion."""
    text = "Vietcombank công bố lợi nhuận quý 1, Techcombank cùng giảm NIM."
    detected = detect_combined(text)
    assert "VCB" in detected
    assert "TCB" in detected


def test_existing_mvp_ck_detection():
    text = "SSI và VNDirect cạnh tranh thị phần môi giới HOSE."
    detected = detect_combined(text)
    assert "SSI" in detected
    assert "VND" in detected
```

- [ ] **Step 2: Run tests to verify they FAIL**

Run: `uv run pytest tests/test_routing_expanded.py -v`

Expected: Many test FAIL với errors như `len(BANK_UNIVERSE) == 27` failing assertion (currently 7), `Missing alias: ...`, `Missing SHORT_FORM entry: ...`.

---

### Task 2: Expand `BANK_UNIVERSE` + `CK_UNIVERSE` in routing.py

**Files:**
- Modify: `.claude/skills/finpath-newsroom-editor/scripts/routing.py:15-18`

- [ ] **Step 1: Update universe constants**

Replace lines 15-18 trong `routing.py`:

```python
# Universe constants
BANK_UNIVERSE = [
    # HOSE (16)
    "VCB", "CTG", "BID", "TCB", "MBB", "ACB", "VPB", "HDB",
    "STB", "SHB", "EIB", "TPB", "MSB", "LPB", "OCB", "VIB",
    # HNX (4)
    "NAB", "BAB", "NVB", "SGB",
    # UPCOM (7)
    "VAB", "BVB", "ABB", "KLB", "VBB", "PGB", "HDF",
]  # 27 mã
CK_UNIVERSE = [
    # HOSE (5)
    "SSI", "VND", "HCM", "VCI", "VIX",
    # HNX (15)
    "SHS", "MBS", "BVS", "BSI", "AGR", "CTS", "APG", "EVS",
    "IVS", "PSI", "TVS", "WSS", "ORS", "VFS", "TCI",
    # UPCOM (10)
    "DSC", "FTS", "CSI", "SBS", "PHS", "ART", "APS", "BMS", "AAS", "VTS",
]  # 30 mã
BDS_UNIVERSE = ["VHM", "NVL", "KDH", "DXG"]  # 4 mã (unchanged)
FULL_UNIVERSE = BANK_UNIVERSE + CK_UNIVERSE + BDS_UNIVERSE  # 61 mã
```

- [ ] **Step 2: Run universe + get_sector tests**

Run: `uv run pytest tests/test_routing_expanded.py -v -k "universe or get_sector"`

Expected: All universe/sector tests PASS. Alias tests still FAIL (need Task 3).

---

### Task 3: Expand `COMPANY_NAME_TO_TICKER` aliases

**Files:**
- Modify: `.claude/skills/finpath-newsroom-editor/scripts/ticker_detection.py:70-90`

- [ ] **Step 1: Replace COMPANY_NAME_TO_TICKER dict**

Replace lines 70-90 trong `ticker_detection.py`:

```python
COMPANY_NAME_TO_TICKER = {
    # Bank HOSE (alias lowercase + Vietnamese variations)
    "techcombank": "TCB",
    "vietcombank": "VCB",
    "vietin": "CTG",
    "vietinbank": "CTG",
    "công thương": "CTG",
    "bidv": "BID",
    "đầu tư phát triển": "BID",
    "mbbank": "MBB",
    "mb bank": "MBB",
    "quân đội": "MBB",
    "acb": "ACB",
    "á châu": "ACB",
    "vpbank": "VPB",
    "việt nam thịnh vượng": "VPB",
    "hdbank": "HDB",
    "phát triển tp.hcm": "HDB",
    "sacombank": "STB",
    "sacom": "STB",
    "sài gòn thương tín": "STB",
    "shb": "SHB",
    "sài gòn-hà nội": "SHB",
    "eximbank": "EIB",
    "xuất nhập khẩu": "EIB",
    "tpbank": "TPB",
    "tiên phong bank": "TPB",
    "maritime bank": "MSB",
    "hàng hải": "MSB",
    "msb": "MSB",
    "lpbank": "LPB",
    "liên việt": "LPB",
    "lộc phát": "LPB",
    "ocb": "OCB",
    "phương đông": "OCB",
    "vib": "VIB",
    "quốc tế việt nam": "VIB",
    # Bank HNX
    "nam á bank": "NAB",
    "nam a": "NAB",
    "namabank": "NAB",
    "bắc á bank": "BAB",
    "bacabank": "BAB",
    "ncb": "NVB",
    "quốc dân": "NVB",
    "saigonbank": "SGB",
    "sài gòn công thương": "SGB",
    # Bank UPCOM
    "việt á bank": "VAB",
    "vietabank": "VAB",
    "bản việt bank": "BVB",
    "viet capital bank": "BVB",
    "abbank": "ABB",
    "an bình bank": "ABB",
    "kienlongbank": "KLB",
    "kiên long": "KLB",
    "vietbank": "VBB",
    "việt nam thương tín": "VBB",
    "pgbank": "PGB",
    "xăng dầu petrolimex": "PGB",
    "hợp tác xã": "HDF",
    # CK HOSE
    "ssi securities": "SSI",
    "vndirect": "VND",
    "hsc": "HCM",
    "tp.hcm securities": "HCM",
    "vietcap": "VCI",
    "bản việt ck": "VCI",
    "bản việt chứng khoán": "VCI",
    "vix": "VIX",
    "vietnam investment securities": "VIX",
    # CK HNX
    "shs": "SHS",
    "sài gòn-hà nội ck": "SHS",
    "mb securities": "MBS",
    "mbs": "MBS",
    "bảo việt ck": "BVS",
    "bvsc": "BVS",
    "bidv securities": "BSI",
    "bsc": "BSI",
    "agriseco": "AGR",
    "vietinbank securities": "CTS",
    "cts securities": "CTS",
    "apg securities": "APG",
    "everest securities": "EVS",
    "ivs": "IVS",
    "đầu tư việt nam ck": "IVS",
    "petrosetco": "PSI",
    "dầu khí ck": "PSI",
    "thiên việt ck": "TVS",
    "tvs": "TVS",
    "phố wall": "WSS",
    "wall street ck": "WSS",
    "tps": "ORS",
    "tiên phong ck": "ORS",
    "nhất việt ck": "VFS",
    "thành công ck": "TCI",
    # CK UPCOM
    "dsc": "DSC",
    "đông sài gòn ck": "DSC",
    "fpts": "FTS",
    "csi": "CSI",
    "kiến thiết ck": "CSI",
    "sbsc": "SBS",
    "sacombank securities": "SBS",
    "phú hưng ck": "PHS",
    "bos securities": "ART",
    "apec ck": "APS",
    "châu á thái bình dương ck": "APS",
    "bảo minh ck": "BMS",
    "smart invest": "AAS",
    "việt tín ck": "VTS",
    # BĐS (unchanged)
    "vinhomes": "VHM",
    "novaland": "NVL",
    "khang điền": "KDH",
    "đất xanh": "DXG",
}
```

- [ ] **Step 2: Run alias tests**

Run: `uv run pytest tests/test_routing_expanded.py -v -k "alias"`

Expected: All alias tests PASS. Short-form tests still FAIL.

---

### Task 4: Expand `SHORT_FORM_TO_TICKER` regex coverage

**Files:**
- Modify: `.claude/skills/finpath-newsroom-editor/scripts/ticker_detection.py:96-105`

- [ ] **Step 1: Replace SHORT_FORM_TO_TICKER dict**

Replace lines 96-105 trong `ticker_detection.py`:

```python
SHORT_FORM_TO_TICKER = {
    # Special case: 2-char "MB" maps to MBB (legacy alias)
    "MB": "MBB",
    # Bank HOSE
    "VCB": "VCB", "CTG": "CTG", "BID": "BID", "TCB": "TCB", "MBB": "MBB",
    "ACB": "ACB", "VPB": "VPB", "HDB": "HDB", "STB": "STB", "SHB": "SHB",
    "EIB": "EIB", "TPB": "TPB", "MSB": "MSB", "LPB": "LPB", "OCB": "OCB",
    "VIB": "VIB",
    # Bank HNX
    "NAB": "NAB", "BAB": "BAB", "NVB": "NVB", "SGB": "SGB",
    # Bank UPCOM
    "VAB": "VAB", "BVB": "BVB", "ABB": "ABB", "KLB": "KLB", "VBB": "VBB",
    "PGB": "PGB", "HDF": "HDF",
    # CK HOSE
    "SSI": "SSI", "VND": "VND", "HCM": "HCM", "VCI": "VCI", "VIX": "VIX",
    # CK HNX
    "SHS": "SHS", "MBS": "MBS", "BVS": "BVS", "BSI": "BSI", "AGR": "AGR",
    "CTS": "CTS", "APG": "APG", "EVS": "EVS", "IVS": "IVS", "PSI": "PSI",
    "TVS": "TVS", "WSS": "WSS", "ORS": "ORS", "VFS": "VFS", "TCI": "TCI",
    # CK UPCOM
    "DSC": "DSC", "FTS": "FTS", "CSI": "CSI", "SBS": "SBS", "PHS": "PHS",
    "ART": "ART", "APS": "APS", "BMS": "BMS", "AAS": "AAS", "VTS": "VTS",
    # BĐS (unchanged)
    "VHM": "VHM", "NVL": "NVL", "KDH": "KDH", "DXG": "DXG",
}
```

The `TICKER_UPPER_REGEX` builds automatically from dict keys (sorted longest-first).

- [ ] **Step 2: Run full Task 1 test suite**

Run: `uv run pytest tests/test_routing_expanded.py -v`

Expected: All ~30 tests PASS.

- [ ] **Step 3: Verify existing tests still pass (no regression)**

Run: `uv run pytest tests/ -v 2>&1 | tail -5`

Expected: All 200+ tests PASS (170 existing + ~30 new).

- [ ] **Step 4: Commit Phase A**

```bash
git add .claude/skills/finpath-newsroom-editor/scripts/routing.py \
        .claude/skills/finpath-newsroom-editor/scripts/ticker_detection.py \
        tests/test_routing_expanded.py
git commit -m "feat(routing): expand Bank universe 7→27 + CK 5→30

- BANK_UNIVERSE: 7 → 27 (HOSE 16 + HNX 4 + UPCOM 7)
- CK_UNIVERSE: 5 → 30 (HOSE 5 + HNX 15 + UPCOM 10)
- BDS_UNIVERSE unchanged (4)
- COMPANY_NAME_TO_TICKER: ~16 → ~80 alias entries
- SHORT_FORM_TO_TICKER: 8 → 57 ticker codes
- 30 new unit tests in test_routing_expanded.py

200+ tests pass. Phase A foundation cho universe expansion."
```

---

## Phase B — Master skill + agent wrapper description metadata

### Task 5: Update master-bank SKILL frontmatter

**Files:**
- Modify: `.claude/skills/finpath-newsroom-master-bank/SKILL.md:3`

- [ ] **Step 1: Read current frontmatter**

```bash
sed -n '1,6p' .claude/skills/finpath-newsroom-master-bank/SKILL.md
```

Note: line 3 has `description:` with "7 Vietnamese banking stocks (TCB/VCB/MBB/ACB/BID/CTG/VPB)".

- [ ] **Step 2: Replace universe text**

Find: `7 Vietnamese banking stocks (TCB/VCB/MBB/ACB/BID/CTG/VPB)`
Replace: `27 listed Vietnamese banks niêm yết HOSE (16) / HNX (4) / UPCOM (7)`

- [ ] **Step 3: Update Step 1 validation reference trong SKILL body**

Find any inline references như `ticker in {TCB/VCB/MBB/ACB/BID/CTG/VPB}` → replace với reference to `routing.BANK_UNIVERSE` (27 mã) or generic "Bank universe 27 mã".

```bash
grep -n "TCB/VCB/MBB/ACB/BID/CTG/VPB\|7 Vietnamese banking" .claude/skills/finpath-newsroom-master-bank/SKILL.md
```

Apply Edit per line found.

---

### Task 6: Update master-ck SKILL frontmatter

**Files:**
- Modify: `.claude/skills/finpath-newsroom-master-ck/SKILL.md:3`

- [ ] **Step 1: Read current frontmatter**

```bash
sed -n '1,6p' .claude/skills/finpath-newsroom-master-ck/SKILL.md
```

- [ ] **Step 2: Replace universe text**

Find: `5 Vietnamese securities/brokerage stocks (SSI/VND/HCM/VCI/SHS)`
Replace: `30 listed Vietnamese securities/brokerage firms niêm yết HOSE (5) / HNX (15) / UPCOM (10)`

- [ ] **Step 3: Update body references**

```bash
grep -n "SSI/VND/HCM/VCI/SHS\|5 Vietnamese securities\|5 mã ck universe" .claude/skills/finpath-newsroom-master-ck/SKILL.md
```

Apply Edit per line found. Replace with `30 mã CK universe` or reference to `CK_UNIVERSE` from routing.py.

---

### Task 7: Update master-bank agent wrapper

**Files:**
- Modify: `.claude/agents/newsroom-master-bank.md:3,34`

- [ ] **Step 1: Replace description**

Find: `Reads brief V4.0 from Story Editor (deep_question_options array + angle_label + narratives) → picks 1 question`
The `description:` field already mentions only V4.0 schema, not specific tickers. Update only if tickers listed.

```bash
grep -n "MVP universe\|TCB/VCB/MBB/ACB/BID/CTG/VPB\|7 Vietnamese banking" .claude/agents/newsroom-master-bank.md
```

- [ ] **Step 2: Update Step 1 validation reference**

Line 34: `- ticker in MVP universe` → `- ticker in BANK_UNIVERSE (27 mã, see routing.py)`

---

### Task 8: Update master-ck agent wrapper

**Files:**
- Modify: `.claude/agents/newsroom-master-ck.md`

- [ ] **Step 1: Find references**

```bash
grep -n "5 mã\|SSI, VND, HCM, VCI, SHS\|{SSI, VND, HCM, VCI, SHS}\|5 Vietnamese securities" .claude/agents/newsroom-master-ck.md
```

- [ ] **Step 2: Update each reference**

For each occurrence, replace với `30 mã CK universe (see routing.CK_UNIVERSE)`.

Specific line: Step 1 validation `ticker in CK universe \`{SSI, VND, HCM, VCI, SHS}\`` → `ticker in CK_UNIVERSE (30 mã)`.

- [ ] **Step 3: Commit Phase B**

```bash
git add .claude/skills/finpath-newsroom-master-bank/SKILL.md \
        .claude/skills/finpath-newsroom-master-ck/SKILL.md \
        .claude/agents/newsroom-master-bank.md \
        .claude/agents/newsroom-master-ck.md
git commit -m "feat(skill): master-bank + master-ck description universe expanded

- master-bank SKILL: '7 stocks' → '27 listed banks'
- master-ck SKILL: '5 stocks' → '30 listed CK firms'
- Agent wrapper Step 1 validation references routing.BANK_UNIVERSE / CK_UNIVERSE
- Workflow + 5 quality gates: NO CHANGE (universe-agnostic)"
```

---

## Phase C — KB master-reference tiering tables

### Task 9: Extend Bank tiering table

**Files:**
- Modify: `kb/bank/frameworks/bank-industry-master-reference.md`

- [ ] **Step 1: Locate tier section**

```bash
grep -n "## .*[Tt]ier\|## .*phân.*nhóm\|## 1.2\|Big4\|Tư nhân top\|Tư nhân BĐS" kb/bank/frameworks/bank-industry-master-reference.md | head -10
```

Find existing tier table (likely Section 1.2 or similar).

- [ ] **Step 2: Read current tier table to understand format**

Read 20-30 lines around the tier table found in Step 1 to understand column structure.

- [ ] **Step 3: Extend tier table with 20 new banks**

Use Edit tool to append rows to existing table. Schema example (adapt to actual table format):

```markdown
| Ticker | Tier | Đặc thù chính |
|---|---|---|
| (existing rows) | | |
| HDB | Tư nhân top | Phát triển TP.HCM, mua HDFC Saudi, mở rộng FE Credit 2024 |
| STB | Tư nhân top | Sài Gòn Thương Tín, post-Trầm Bê 2022 phục hồi, nợ xấu giảm |
| SHB | Tư nhân mid | Sài Gòn-Hà Nội, exposure BĐS lớn, NPL biến động cycle |
| EIB | Tư nhân mid | Eximbank, cổ đông phân tán, xuất nhập khẩu định hướng |
| TPB | Tư nhân mid | Tiên Phong, tech-retail focus, ESOP đậm |
| MSB | Tư nhân mid | Maritime Bank, vận tải biển legacy, đang chuyển hướng retail |
| LPB | Tư nhân mid | Lộc Phát (đổi tên 2024), mạng lưới rộng từ Postal Bank |
| OCB | Tư nhân mid | Phương Đông, retail mid-market, NPL low |
| VIB | Tư nhân mid | Quốc tế, mạnh thẻ tín dụng, cho vay tiêu dùng |
| NAB | Tư nhân small | Nam Á Bank, vừa niêm yết HNX, mid-cap |
| BAB | Tư nhân small | Bắc Á Bank, mạnh Bắc Trung Bộ, mid-cap |
| NVB | Tư nhân small | NCB, từng kiểm soát đặc biệt, đang phục hồi |
| SGB | Tư nhân small | Saigonbank, sở hữu state-owned background |
| VAB | UPCOM small | Việt Á Bank, low liquidity |
| BVB | UPCOM small | Bản Việt Bank, retail focus phía Nam |
| ABB | UPCOM small | ABBank (An Bình), exposure DN vừa |
| KLB | UPCOM small | Kienlongbank, mạng lưới mỏng |
| VBB | UPCOM small | VietBank, mid-low cap |
| PGB | UPCOM small | PGBank (Petrolimex), niche năng lượng |
| HDF | UPCOM cooperative | Co-op Bank, không phải TMCP thuần |
```

- [ ] **Step 4: Verify row count**

Read tier table section. Count unique tickers: should be ≥ 27 unique Bank tickers.

---

### Task 10: Extend CK mô hình kinh doanh table

**Files:**
- Modify: `kb/ck/frameworks/ck-industry-master-reference.md`

- [ ] **Step 1: Locate business model table**

```bash
grep -n "## 1.2\|mô hình kinh doanh\|Truyền thống đầy đủ\|đầu tư dẫn dắt\|Bán lẻ tập trung" kb/ck/frameworks/ck-industry-master-reference.md | head -10
```

- [ ] **Step 2: Read existing table format**

Read 20-30 lines around the table to understand column structure.

- [ ] **Step 3: Extend table với 25 CK firms mới**

Append to table:

```markdown
| Ticker | Mô hình | Đặc thù |
|---|---|---|
| (existing rows: SSI, VND, HCM, VCI, SHS) | | |
| VIX | Truyền thống | Vietnam Investment Securities, mid-cap HOSE |
| MBS | Liên kết NH mẹ | MB Securities, vốn từ MBBank, IB tăng |
| BVS | Liên kết NH mẹ | Bảo Việt CK, phân khối insurance product |
| BSI | Liên kết NH mẹ | BIDV Securities, mạnh trái phiếu doanh nghiệp |
| AGR | Liên kết NH mẹ | Agriseco, Agribank backing, retail focus |
| CTS | Liên kết NH mẹ | VietinBank Securities, mid-tier IB |
| VFS | Liên kết NH mẹ | Nhất Việt CK |
| APG | Small/specialty | APG Securities, niche client |
| EVS | Small/specialty | Everest Securities, mid-tier |
| IVS | Small/specialty | Đầu tư Việt Nam CK |
| PSI | Small/specialty | Dầu khí (Petrosetco backing) |
| TVS | Small/specialty | Thiên Việt CK |
| WSS | Small/specialty | Phố Wall Securities |
| ORS | Small/specialty | TPS Tiên Phong CK |
| TCI | Small/specialty | Thành Công CK |
| DSC | UPCOM small | Đông Sài Gòn CK |
| FTS | UPCOM small | FPTS (FPT Securities) |
| CSI | UPCOM small | Kiến Thiết CK |
| SBS | UPCOM small | Sacombank Securities (đã bán khỏi Sacombank) |
| PHS | UPCOM small | Phú Hưng CK |
| ART | UPCOM small | BOS Securities |
| APS | UPCOM small | APEC CK |
| BMS | UPCOM small | Bảo Minh CK |
| AAS | UPCOM small | Smart Invest |
| VTS | UPCOM small | Việt Tín CK |
```

- [ ] **Step 4: Verify row count**

Count unique CK tickers in table: should be ≥ 30.

- [ ] **Step 5: Commit Phase C**

```bash
git add kb/bank/frameworks/bank-industry-master-reference.md \
        kb/ck/frameworks/ck-industry-master-reference.md
git commit -m "kb: extend Bank + CK tiering tables for expanded universe

- Bank tiering: existing Big4/Top + add 20 mới (mid 7, small 11, co-op 1)
- CK mô hình: existing 5 + add 25 mới (Liên kết NH mẹ 7, Small/specialty 9,
  UPCOM small 9)
- Framework content: NO CHANGE (chỉ extend rows)"
```

---

## Phase D — Pipeline + Editor + Orchestrator universe references

### Task 11: Update newsroom-pipeline.md

**Files:**
- Modify: `.claude/agents/newsroom-pipeline.md`

- [ ] **Step 1: Find universe references**

```bash
grep -n "FULL_UNIVERSE\|7 Bank\|5 CK\|4 BĐS\|16 mã\|TCB|VCB|MBB\|SSI|VND|HCM\|MVP" .claude/agents/newsroom-pipeline.md
```

- [ ] **Step 2: Update universe lines**

Find: 
```
- **Bank** (7): `TCB | VCB | MBB | ACB | BID | CTG | VPB`
- **CK** (5): `SSI | VND | HCM | VCI | SHS`
- **BĐS** (4): `VHM | NVL | KDH | DXG` (KBC defer — KCN pattern khác)
```

Replace với:
```
- **Bank** (27): HOSE 16 (VCB/CTG/BID/TCB/MBB/ACB/VPB/HDB/STB/SHB/EIB/TPB/MSB/LPB/OCB/VIB) + HNX 4 (NAB/BAB/NVB/SGB) + UPCOM 7 (VAB/BVB/ABB/KLB/VBB/PGB/HDF)
- **CK** (30): HOSE 5 (SSI/VND/HCM/VCI/VIX) + HNX 15 (SHS/MBS/BVS/BSI/AGR/CTS/APG/EVS/IVS/PSI/TVS/WSS/ORS/VFS/TCI) + UPCOM 10 (DSC/FTS/CSI/SBS/PHS/ART/APS/BMS/AAS/VTS)
- **BĐS** (4): `VHM | NVL | KDH | DXG` (KBC defer — KCN pattern khác)
```

Total: 27 + 30 + 4 = 61 mã.

- [ ] **Step 3: Update "16 mã universe" references**

Find: `FULL UNIVERSE 16 mã` or `16 mã universe Finpath Newsroom`
Replace với: `FULL_UNIVERSE 61 mã`

- [ ] **Step 4: Update universe section + reject message**

Line ~104 or near reject message: `"Ticker [X] không thuộc 16 mã universe Finpath Newsroom (Bank/CK/BĐS)."` → `"Ticker [X] không thuộc 61 mã universe Finpath Newsroom (Bank/CK/BĐS)."`

---

### Task 12: Update newsroom-editor.md

**Files:**
- Modify: `.claude/agents/newsroom-editor.md`

- [ ] **Step 1: Update description frontmatter**

Find: `FULL_UNIVERSE (16 mã: 7 Bank + 5 CK + 4 BĐS)`
Replace: `FULL_UNIVERSE (61 mã: 27 Bank + 30 CK + 4 BĐS)`

- [ ] **Step 2: Update Step 2 universe text**

Find:
```
FULL_UNIVERSE 16 mã (3 sector):
- **Bank** (7): TCB · VCB · MBB · ACB · BID · CTG · VPB
- **CK** (5): SSI · VND · HCM · VCI · SHS
- **BĐS** (4): VHM · NVL · KDH · DXG (KBC defer)
```

Replace với:
```
FULL_UNIVERSE 61 mã (3 sector):
- **Bank** (27): HOSE 16 + HNX 4 + UPCOM 7 — see routing.BANK_UNIVERSE
- **CK** (30): HOSE 5 + HNX 15 + UPCOM 10 — see routing.CK_UNIVERSE
- **BĐS** (4): VHM · NVL · KDH · DXG (KBC defer)
```

- [ ] **Step 3: Update Aliases section**

Section "Aliases coverage trong scripts/ticker_detection.py" — replace ngắn gọn list aliases hiện tại với reference:

```
Aliases coverage trong `scripts/ticker_detection.py`:
- Pass 1 company names: ~80 entries covering 57 expanded tickers
- Pass 2 short-form ticker: regex auto-derived từ `SHORT_FORM_TO_TICKER` dict (57 tickers + 4 BĐS = 61, sorted longest-first)
- See `tests/test_routing_expanded.py` cho expected detection cases
```

- [ ] **Step 4: Update Step 4 reject message**

Find: `out_of_universe — không có ticker trong 16 mã FULL_UNIVERSE`
Replace: `out_of_universe — không có ticker trong 61 mã FULL_UNIVERSE`

---

### Task 13: Update orchestrator SKILL.md

**Files:**
- Modify: `.claude/skills/finpath-newsroom-orchestrator/SKILL.md`

- [ ] **Step 1: Find universe references**

```bash
grep -n "16 mã\|TCB/VCB/MBB/ACB/BID/CTG/VPB\|SSI/VND/HCM/VCI/SHS\|VHM/NVL/KDH/DXG" .claude/skills/finpath-newsroom-orchestrator/SKILL.md
```

- [ ] **Step 2: Update description line + Universe section**

Find frontmatter `description:`: replace "16 mã thuộc 3 sector" → "61 mã thuộc 3 sector".

Replace ticker enumeration: `(TCB/VCB/MBB/ACB/BID/CTG/VPB/SSI/VND/HCM/VCI/SHS/VHM/NVL/KDH/DXG)` → `(see routing.FULL_UNIVERSE: 27 Bank + 30 CK + 4 BĐS = 61 mã)`.

- [ ] **Step 3: Update "Universe 16 mã" body section**

Find section header `## Universe 16 mã` → `## Universe 61 mã`. Update body listing.

- [ ] **Step 4: Commit Phase D**

```bash
git add .claude/agents/newsroom-pipeline.md \
        .claude/agents/newsroom-editor.md \
        .claude/skills/finpath-newsroom-orchestrator/SKILL.md
git commit -m "agent(newsroom): pipeline + editor + orchestrator universe expanded

- newsroom-pipeline.md: FULL_UNIVERSE 16 → 61 mã references
- newsroom-editor.md: description + Step 2 + reject message
- orchestrator SKILL.md: description + universe section
- All reference routing.BANK_UNIVERSE / CK_UNIVERSE (single source of truth)"
```

---

## Phase E — Commands + CLAUDE.md

### Task 14: Update tin.md command

**Files:**
- Modify: `.claude/commands/tin.md`

- [ ] **Step 1: Update universe description**

Find:
```
- **Bank** (7): TCB · VCB · MBB · ACB · BID · CTG · VPB
- **CK** (5): SSI · VND · HCM · VCI · SHS
- **BĐS** (4): VHM · NVL · KDH · DXG (KBC defer — KCN pattern khác)
```

Replace với:
```
- **Bank** (27): HOSE 16 + HNX 4 + UPCOM 7 (see routing.BANK_UNIVERSE)
- **CK** (30): HOSE 5 + HNX 15 + UPCOM 10 (see routing.CK_UNIVERSE)
- **BĐS** (4): VHM · NVL · KDH · DXG (KBC defer)
```

- [ ] **Step 2: Update alias mapping section**

Find:
```
- Bank: Vietcombank→VCB, Techcombank→TCB, BIDV→BID, VietinBank→CTG, MB Bank→MBB, ACB→ACB, VPBank→VPB
- CK: SSI→SSI, VNDirect→VND, HSC→HCM, Vietcap→VCI, Sài Gòn-Hà Nội→SHS
- BĐS: Vinhomes→VHM, Novaland→NVL, Khang Điền→KDH, Đất Xanh→DXG
```

Replace với:
```
Alias mapping comprehensive — see `.claude/skills/finpath-newsroom-editor/scripts/ticker_detection.py::COMPANY_NAME_TO_TICKER` (~80 alias entries) hoặc fall back regex 3-char ticker (case-sensitive).

Examples:
- Bank: Vietcombank→VCB, Sacombank→STB, Eximbank→EIB, HDBank→HDB, LPBank→LPB, Maritime Bank→MSB, ...
- CK: VNDirect→VND, HSC→HCM, Vietcap→VCI, FPTS→FTS, Petrosetco→PSI, BIDV Securities→BSI, ...
- BĐS: Vinhomes→VHM, Novaland→NVL, Khang Điền→KDH, Đất Xanh→DXG
```

- [ ] **Step 3: Update reject message**

Find: `"Ticker $ARGUMENTS không thuộc 16 mã universe"` → `"Ticker $ARGUMENTS không thuộc 61 mã universe"`

---

### Task 15: Update tin-batch.md command

**Files:**
- Modify: `.claude/commands/tin-batch.md`

- [ ] **Step 1: Update universe description**

Same pattern as Task 14 Step 1.

- [ ] **Step 2: Update validation FULL_UNIVERSE references**

Find:
```
- Check membership trong FULL_UNIVERSE = `{TCB,VCB,MBB,ACB,BID,CTG,VPB,SSI,VND,HCM,VCI,SHS,VHM,NVL,KDH,DXG}`
- Invalid → log warn `⚠️ Skip ticker [X] — không thuộc 16 mã FULL_UNIVERSE`
```

Replace:
```
- Check membership trong FULL_UNIVERSE (61 mã, see routing.py) — use `from scripts.routing import FULL_UNIVERSE` để verify
- Invalid → log warn `⚠️ Skip ticker [X] — không thuộc 61 mã FULL_UNIVERSE`
```

- [ ] **Step 3: Update alias mapping examples**

Same pattern as Task 14 Step 2 — replace specific MVP-only mapping with reference + examples.

- [ ] **Step 4: Update fallback message**

Find: `"Không có ticker hợp lệ trong 16 mã FULL_UNIVERSE"` → `"Không có ticker hợp lệ trong 61 mã FULL_UNIVERSE"`

---

### Task 16: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Find universe references**

```bash
grep -n "16 mã\|7 mã Bank\|5 mã CK\|4 mã BĐS\|MVP Bank universe\|FULL_UNIVERSE\|kb/bank\|kb/ck\|kb/bds" CLAUDE.md
```

- [ ] **Step 2: Update Universe section**

Find:
```
## Universe (MVP Bank only)

7 ticker hợp lệ: **TCB · VCB · MBB · ACB · BID · CTG · VPB**.
```

Replace với:
```
## Universe — 3 sector

**Bank (27)**: HOSE 16 (VCB/CTG/BID/TCB/MBB/ACB/VPB/HDB/STB/SHB/EIB/TPB/MSB/LPB/OCB/VIB) + HNX 4 (NAB/BAB/NVB/SGB) + UPCOM 7 (VAB/BVB/ABB/KLB/VBB/PGB/HDF).

**CK (30)**: HOSE 5 (SSI/VND/HCM/VCI/VIX) + HNX 15 (SHS/MBS/BVS/BSI/AGR/CTS/APG/EVS/IVS/PSI/TVS/WSS/ORS/VFS/TCI) + UPCOM 10 (DSC/FTS/CSI/SBS/PHS/ART/APS/BMS/AAS/VTS).

**BĐS (4)**: VHM · NVL · KDH · DXG (KBC defer — KCN pattern khác).

**Total: 61 mã universe.** Source: `.claude/skills/finpath-newsroom-editor/scripts/routing.py::FULL_UNIVERSE`.
```

- [ ] **Step 3: Update "Ticker ngoài universe" rule**

Find: `Ticker ngoài universe → reply "Ticker [X] không thuộc MVP Bank universe. CK + BĐS sẽ thêm sau."`
Replace: `Ticker ngoài universe → reply "Ticker [X] không thuộc 61 mã FULL_UNIVERSE."`

- [ ] **Step 4: Update architecture map**

Find the architecture map block (around line 26-29). Update text:
```
kb/bank/                         → Markdown KB Bank (27 mã: Big4 + tư nhân top + mid + small + cooperative)
kb/ck/                           → Markdown KB CK (30 mã: HOSE 5 + HNX 15 + UPCOM 10)
kb/bds/                          → Markdown KB BĐS (21 file, 7 category)
```

- [ ] **Step 5: Commit Phase E**

```bash
git add .claude/commands/tin.md .claude/commands/tin-batch.md CLAUDE.md
git commit -m "docs+cmd: tin/tin-batch + CLAUDE.md universe expanded to 61 mã

- tin.md + tin-batch.md: alias mapping → reference ticker_detection.py + examples
- CLAUDE.md: Universe section 61 mã + architecture map
- Reject messages updated 16 → 61"
```

---

## Phase F — Verification + push

### Task 17: Full test suite verification

**Files:**
- None (verification only)

- [ ] **Step 1: Run full pytest suite**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/ -v 2>&1 | tail -10
```

Expected: ~200 tests pass (170 existing + ~30 new). If any FAIL → investigate, fix, re-run.

- [ ] **Step 2: Spot-check Finpath API for small banks**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.finpath_api import FinpathAPI
api = FinpathAPI()
for t in ['STB', 'EIB', 'NAB', 'BVB', 'PGB', 'TPB', 'LPB']:
    try:
        ratios = api.get_bank_ratios(t)
        quarters = len(ratios.get('quarterlyProfits', [])) if isinstance(ratios, dict) else 0
        print(f'{t}: OK ({quarters} quarters)')
    except Exception as e:
        print(f'{t}: FAIL — {type(e).__name__}: {e}')
"
```

Save output for documentation. Mã nào FAIL → flag trong commit + Master skill comment that web_search needed.

- [ ] **Step 3: Verify routing.get_sector for all 61 tickers**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/.claude/skills/finpath-newsroom-editor" && uv run python -c "
from scripts.routing import BANK_UNIVERSE, CK_UNIVERSE, BDS_UNIVERSE, get_sector
all_t = BANK_UNIVERSE + CK_UNIVERSE + BDS_UNIVERSE
for t in all_t:
    sector = get_sector(t)
    assert sector in ('Bank','CK','BĐS'), f'{t} → {sector} unexpected'
print(f'All {len(all_t)} tickers route correctly to Bank/CK/BĐS')
"
```

Expected output: `All 61 tickers route correctly to Bank/CK/BĐS`.

- [ ] **Step 4: Visual verify KB tiering tables**

```bash
echo "=== Bank tier table ticker count ===" && grep -oE "^\| [A-Z]{3,4} \|" kb/bank/frameworks/bank-industry-master-reference.md | sort -u | wc -l
echo "=== CK mô hình table ticker count ===" && grep -oE "^\| [A-Z]{3,4} \|" kb/ck/frameworks/ck-industry-master-reference.md | sort -u | wc -l
```

Expected:
- Bank: ≥ 27 unique
- CK: ≥ 30 unique

If less → return to Phase C, add missing rows.

- [ ] **Step 5: Smoke check editor agent skill registry**

```bash
grep -c "27 listed\|30 listed\|61 mã\|FULL_UNIVERSE" .claude/skills/finpath-newsroom-master-bank/SKILL.md .claude/skills/finpath-newsroom-master-ck/SKILL.md .claude/skills/finpath-newsroom-orchestrator/SKILL.md .claude/agents/newsroom-pipeline.md .claude/agents/newsroom-editor.md
```

Expected: each file has ≥ 1 match (universe text updated).

---

### Task 18: Final advisor review + push

**Files:**
- None (advisor + push)

- [ ] **Step 1: Call advisor for pre-push review**

Use `advisor()` tool. No params — full conversation auto-forwarded. Advisor will review all 5 phase commits.

- [ ] **Step 2: Fix any issues advisor surfaces**

Apply edits per advisor feedback. Re-commit if needed.

- [ ] **Step 3: Show user commits ahead**

```bash
git log --oneline origin/main..HEAD
```

Expected: 5 commits (Phase A-E).

- [ ] **Step 4: Confirm with user + push**

Ask user "Push 5 commit lên origin/main?". Wait for confirmation.

```bash
git push origin main
```

Expected: push succeeds.

---

## Plan Verification

### Spec Coverage Check

- [x] Spec Section 1 (Mục tiêu): Phases A-E all touch 14 file
- [x] Spec Section 2 (Scope in/out): Task 11 keeps Master workflow unchanged, Phase A-E mechanical only
- [x] Spec Section 3 (Ticker list): Tasks 2-4 embed list in routing.py + ticker_detection.py
- [x] Spec Section 4 Layer 1 (routing.py): Tasks 1-2
- [x] Spec Section 4 Layer 2 (ticker_detection.py): Tasks 1, 3, 4
- [x] Spec Section 4 Layer 3 (Finpath API NO CODE): Task 17 Step 2 verification only
- [x] Spec Section 4 Layer 4 (KB tiering): Tasks 9-10
- [x] Spec Section 4 Layer 5 (Manual YAML NO CHANGE): not in plan (correct — defer)
- [x] Spec Section 4 Layer 6 (Master skill + agent): Tasks 5-8
- [x] Spec Section 4 Layer 7 (Pipeline/Editor/Orchestrator + Commands + CLAUDE.md): Tasks 11-16
- [x] Spec Section 5 Test 1 (unit tests): Task 1 ~30 tests
- [x] Spec Section 5 Test 2 (smoke pipeline): Task 17 — deferred to verification (no LLM dispatch in plan, just route verify)
- [x] Spec Section 5 Test 3 (Finpath spot-check): Task 17 Step 2
- [x] Spec Section 5 Test 4 (KB tiering verify): Task 17 Step 4
- [x] Spec Section 5 Test 5 (existing tests pass): Task 4 Step 3 + Task 17 Step 1
- [x] Spec Section 6 Phase A-F: Plan Phases A-F (Task 1-18)

### Placeholder Scan

- No `TBD` / `TODO` / `fill in details` / `implement later` references
- All test code in Task 1 shown in full (~30 test cases listed)
- All edit operations show concrete find/replace text or full code block
- Grep commands show expected output patterns

### Type / Name Consistency

- `BANK_UNIVERSE` used identically in routing.py (Task 2) + tests (Task 1) + commands (Task 14)
- `CK_UNIVERSE` consistent across routing.py + tests + skills
- `FULL_UNIVERSE` referenced consistently as "61 mã"
- `COMPANY_NAME_TO_TICKER` + `SHORT_FORM_TO_TICKER` dict names consistent ticker_detection.py + tests
- File path `tests/test_routing_expanded.py` used consistently Task 1 + Task 17

---

## Notes for executor

- **TDD discipline Phase A:** Task 1 writes failing tests FIRST. Verify red → green per task (universe → alias → short-form).
- **Phase B-E parallel-safe after A:** Mechanical text update, no dependencies between B/C/D/E. Can dispatch in parallel if needed.
- **Phase F gate before push:** Test 1-5 + advisor review ALL must pass. Don't shortcut.
- **Atomic commits:** 5 commit at end of Phase A/B/C/D/E + optional verification commits in F. Each leaves repo in working state.
- **Ticker list verification:** Spec acknowledges list is draft (HDF Co-op Bank uncertain). If Phase F discovers a ticker truly doesn't exist (delisted/never listed), remove from universe list + tests + commit fix in Phase F.
