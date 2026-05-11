# Bank + CK Universe Expansion — Design Spec v1.0

**Date:** 2026-05-11
**Author:** Claude (drafted via brainstorming with user @dangtrungicloud)
**Status:** Draft — awaiting user review

## 1. Mục tiêu

Expand `Bank` + `CK` universe của Finpath Newsroom pipeline từ MVP (7 Bank + 5 CK = 12 mã) → toàn bộ mã niêm yết HOSE/HNX/UPCOM (~57 mã). BĐS giữ nguyên 4 mã residential (user không yêu cầu mở rộng).

**Universe sau expand (~61 mã total):**

| Sector | MVP cũ | FULL mới | Thay đổi |
|---|---|---|---|
| Bank | 7 | 27 (HOSE 16 + HNX 4 + UPCOM 7) | +20 |
| CK | 5 | 30 (HOSE 5 + HNX 15 + UPCOM 10) | +25 |
| BĐS | 4 | 4 (không đổi) | 0 |
| **TỔNG** | **16** | **61** | **+45** |

**Nguyên tắc cốt lõi (theo CLAUDE.md đã chốt):**
- KB chỉ chứa static knowledge — framework markdown dùng chung mọi mã (KHÔNG cần KB riêng per-ticker)
- Master skills V4.0 universe-agnostic — workflow + 5 quality gates apply cho mọi ticker
- Data động per-ticker (BCTC quý, doanh số, NPL realtime) → Master web_search realtime
- Manual YAML curated (`credit_room.yaml` 7 MVP entries hiện tại) → KEEP MVP only, mã mới Master web_search

## 2. Scope

### In scope

- Universe registry (`routing.py`) — 2 list constants
- Ticker alias (`ticker_detection.py`) — ~80 new alias entries (full coverage policy)
- Master skill description metadata (4 file: 2 SKILL + 2 agent wrapper)
- KB tiering tables (2 file: bank-industry-master-reference + ck-industry-master-reference) — extend rows, không rewrite framework
- Pipeline + Editor + Orchestrator universe references (3 file)
- Commands alias mapping (2 file: tin.md + tin-batch.md)
- CLAUDE.md architecture map (1 file)
- Unit tests (≥ 30 new tests cho expanded universe + alias)
- Verification smoke tests (3 sample tickers + Finpath spot-check)

### Out of scope

- ❌ KB framework content rewrite (frameworks markdown vẫn dùng chung)
- ❌ Master skill workflow change (workflow giống nhau cho mọi ticker)
- ❌ BĐS universe expand (defer per user request)
- ❌ Curated YAML expand (static-only principle — web_search realtime cho mã mới)
- ❌ Notion publish automation expand
- ❌ Web viewer changes (web/ không biết universe, render từ DB rows)
- ❌ Finpath API endpoint changes (assume Bank-specific endpoints work cho 27 banks; spot-check trong verification)

## 3. Ticker list (em research — user verify sau)

### Bank — 27 mã

**HOSE (16):**

| # | Ticker | Tên đầy đủ | Alias chính |
|---|---|---|---|
| 1 | VCB | Ngân hàng TMCP Ngoại thương Việt Nam | Vietcombank |
| 2 | CTG | Ngân hàng TMCP Công thương Việt Nam | VietinBank, Vietin |
| 3 | BID | Ngân hàng TMCP Đầu tư & Phát triển Việt Nam | BIDV, BID Bank |
| 4 | TCB | Ngân hàng TMCP Kỹ thương Việt Nam | Techcombank |
| 5 | MBB | Ngân hàng TMCP Quân đội | MB, MB Bank, MBBank |
| 6 | ACB | Ngân hàng TMCP Á Châu | ACB |
| 7 | VPB | Ngân hàng TMCP Việt Nam Thịnh vượng | VPBank |
| 8 | HDB | Ngân hàng TMCP Phát triển TP.HCM | HDBank |
| 9 | STB | Ngân hàng TMCP Sài Gòn Thương Tín | Sacombank, Sacom |
| 10 | SHB | Ngân hàng TMCP Sài Gòn-Hà Nội | SHB |
| 11 | EIB | Ngân hàng TMCP Xuất nhập khẩu Việt Nam | Eximbank |
| 12 | TPB | Ngân hàng TMCP Tiên Phong | TPBank |
| 13 | MSB | Ngân hàng TMCP Hàng Hải | Maritime Bank, MSB |
| 14 | LPB | Ngân hàng TMCP Lộc Phát Việt Nam | LPBank, Liên Việt |
| 15 | OCB | Ngân hàng TMCP Phương Đông | OCB |
| 16 | VIB | Ngân hàng TMCP Quốc tế Việt Nam | VIB |

**HNX (4):**

| # | Ticker | Tên đầy đủ | Alias chính |
|---|---|---|---|
| 17 | NAB | Ngân hàng TMCP Nam Á | Nam Á Bank, Nam A |
| 18 | BAB | Ngân hàng TMCP Bắc Á | Bắc Á Bank, BacABank |
| 19 | NVB | Ngân hàng TMCP Quốc Dân | NCB |
| 20 | SGB | Ngân hàng TMCP Sài Gòn Công thương | Saigonbank |

**UPCOM (7):**

| # | Ticker | Tên đầy đủ | Alias chính |
|---|---|---|---|
| 21 | VAB | Ngân hàng TMCP Việt Á | Việt Á Bank, VietABank |
| 22 | BVB | Ngân hàng TMCP Bản Việt | Bản Việt Bank, Viet Capital |
| 23 | ABB | Ngân hàng TMCP An Bình | ABBank |
| 24 | KLB | Ngân hàng TMCP Kiên Long | Kienlongbank |
| 25 | VBB | Ngân hàng TMCP Việt Nam Thương Tín | VietBank |
| 26 | PGB | Ngân hàng TMCP Xăng dầu Petrolimex | PGBank |
| 27 | HDF | Ngân hàng TMCP Hợp tác xã | Co-op Bank |

### CK — 30 mã

**HOSE (5):**

| # | Ticker | Tên đầy đủ | Alias chính |
|---|---|---|---|
| 1 | SSI | Công ty CP Chứng khoán SSI | Sài Gòn, SSI Securities |
| 2 | VND | Công ty CP Chứng khoán VNDIRECT | VNDirect, VND Securities |
| 3 | HCM | Công ty CP Chứng khoán TP.HCM | HSC |
| 4 | VCI | Công ty CP Chứng khoán Vietcap | Vietcap, Bản Việt CK |
| 5 | VIX | Công ty CP Chứng khoán Vietnam Investment | VIX, VnInvest |

**HNX (15):**

| # | Ticker | Tên đầy đủ | Alias chính |
|---|---|---|---|
| 6 | SHS | Công ty CP CK Sài Gòn-Hà Nội | SHS, Sài Gòn Hà Nội CK |
| 7 | MBS | Công ty CP CK MB | MB Securities, MBS CK |
| 8 | BVS | Công ty CP CK Bảo Việt | Bảo Việt CK, BVSC |
| 9 | BSI | Công ty CP CK BIDV | BIDV Securities, BSC |
| 10 | AGR | Công ty CP CK Agribank | Agriseco |
| 11 | CTS | Công ty CP CK Vietinbank | VietinBank Securities, CTS |
| 12 | APG | Công ty CP CK APG | APG Securities |
| 13 | EVS | Công ty CP CK Everest | Everest Securities |
| 14 | IVS | Công ty CP CK Đầu tư Việt Nam | IVS, ĐT Việt Nam CK |
| 15 | PSI | Công ty CP CK Dầu khí | Petrosetco, PSI |
| 16 | TVS | Công ty CP CK Thiên Việt | TVS, Thiên Việt CK |
| 17 | WSS | Công ty CP CK Phố Wall | Phố Wall, Wall Street |
| 18 | ORS | Công ty CP CK Tiên Phong | TPS, Tiên Phong CK |
| 19 | VFS | Công ty CP CK Nhất Việt | Nhất Việt CK, NVS |
| 20 | TCI | Công ty CP CK Thành Công | TCI Securities |

**UPCOM (10):**

| # | Ticker | Tên đầy đủ | Alias chính |
|---|---|---|---|
| 21 | DSC | Công ty CP CK DSC | DSC, Đông Sài Gòn |
| 22 | FTS | Công ty CP CK FPT | FPTS |
| 23 | CSI | Công ty CP CK Kiến Thiết | CSI |
| 24 | SBS | Công ty CP CK SBS | SBSC, Sacombank Securities |
| 25 | PHS | Công ty CP CK Phú Hưng | Phú Hưng |
| 26 | ART | Công ty CP CK BOS | ART, BOS Securities |
| 27 | APS | Công ty CP CK Châu Á Thái Bình Dương | APEC, APS |
| 28 | BMS | Công ty CP CK Bảo Minh | Bảo Minh CK |
| 29 | AAS | Công ty CP CK Smart Invest | Smart Invest, AAS |
| 30 | VTS | Công ty CP CK Việt Tín | Việt Tín CK |

⚠️ **Uncertain entries — verify trong implementation:** Một số mã có thể đã delist / chưa niêm yết / thay ticker. Spec này chấp nhận list draft, verify bằng web search hoặc Finpath API trước Phase A commit. User confirm sau khi review.

## 4. Data architecture impact

7 layer code/data, decision per layer:

### Layer 1 — `routing.py` universe registry

**File:** `.claude/skills/finpath-newsroom-editor/scripts/routing.py`

**Change:** Update 2 list constants `BANK_UNIVERSE` + `CK_UNIVERSE`. BĐS giữ nguyên.

```python
BANK_UNIVERSE = [
    "VCB", "CTG", "BID", "TCB", "MBB", "ACB", "VPB", "HDB", "STB", "SHB",
    "EIB", "TPB", "MSB", "LPB", "OCB", "VIB",
    "NAB", "BAB", "NVB", "SGB",
    "VAB", "BVB", "ABB", "KLB", "VBB", "PGB", "HDF",
]  # 27

CK_UNIVERSE = [
    "SSI", "VND", "HCM", "VCI", "VIX",
    "SHS", "MBS", "BVS", "BSI", "AGR", "CTS", "APG", "EVS", "IVS", "PSI",
    "TVS", "WSS", "ORS", "VFS", "TCI",
    "DSC", "FTS", "CSI", "SBS", "PHS", "ART", "APS", "BMS", "AAS", "VTS",
]  # 30

BDS_UNIVERSE = ["VHM", "NVL", "KDH", "DXG"]  # unchanged
```

`get_sector()` lookup table tự update qua loop.

### Layer 2 — `ticker_detection.py` alias

**File:** `.claude/skills/finpath-newsroom-editor/scripts/ticker_detection.py`

**Change:** Mở rộng `COMPANY_NAME_TO_TICKER` từ ~16 entries → ~80 entries (full alias coverage per Section 3 list).

**Pass 2 short-form regex:** Update regex `\b(TCB|VCB|...|FTS|VTS)\b` từ 16 → 57 char tickers.

### Layer 3 — Finpath API

**File:** `lib/finpath_api.py`

**Change:** **NO CODE CHANGE.** Generic endpoints (income/balance/cashflow/events/news) work cho mọi listed ticker.

**Risk:** Bank-only endpoints (`get_bank_ratios`, `get_net_interest_income`, `get_deposit_credit`, `get_bad_debt`) có thể không có data cho mã nhỏ (NAB/BAB/SGB/UPCOM banks). Mitigation: Phase F verification spot-check, document trong Master skill nếu thiếu.

### Layer 4 — KB markdown

**Files:**
- `kb/bank/frameworks/bank-industry-master-reference.md`
- `kb/ck/frameworks/ck-industry-master-reference.md`

**Change:** Extend tiering tables only. KHÔNG rewrite framework markdown.

**Bank tiering tables sau expand:**
- Big4 quốc doanh tier: VCB/CTG/BID (existing)
- Tư nhân top tier: TCB/MBB/ACB/VPB/HDB/STB (extend STB)
- Tư nhân mid tier: SHB/EIB/TPB/MSB/LPB/OCB/VIB (NEW 7 rows)
- Tư nhân small tier: NAB/BAB/NVB/SGB/VAB/BVB/ABB/KLB/VBB/PGB/HDF (NEW 11 rows)

**CK tiering tables sau expand:**
- Truyền thống đầy đủ dịch vụ: SSI/VND/HCM/VCI (existing)
- NH đầu tư dẫn dắt: VCI (existing)
- Bán lẻ tập trung: SHS (existing)
- Liên kết ngân hàng mẹ: MBS/BSI/CTS/AGR/VFS (NEW 5 rows)
- Small/specialty: TVS/EVS/PHS/FTS/ART/BVS/IVS/PSI/WSS/ORS/APG/APS/BMS/AAS/DSC/CSI/SBS/TCI/VTS (NEW 19 rows)

Mỗi row mới có 1-2 dòng đặc thù (~30 phút mỗi file).

### Layer 5 — Manual YAML

**Files:** `data/manual/credit_room.yaml`, `data/manual/nhnn_circulars.yaml`, `data/manual/ssc_circulars.yaml`

**Change:** **NO CHANGE.** Theo static-only principle:
- `credit_room.yaml` keep 7 MVP entries. Mã mới (20 banks) → Master web_search realtime cho credit room data.
- Regulations files generic (không per-ticker) → no change.

Defer YAML expansion. Nếu Phase F discover Master agent thiếu data cho mã mới → optional Phase G later.

### Layer 6 — Master skills + agent wrappers

**Files:**
- `.claude/skills/finpath-newsroom-master-bank/SKILL.md`
- `.claude/skills/finpath-newsroom-master-ck/SKILL.md`
- `.claude/agents/newsroom-master-bank.md`
- `.claude/agents/newsroom-master-ck.md`

**Change:** Frontmatter description universe text update.

Before (Bank): `"Writing in-depth news articles about 7 Vietnamese banking stocks (TCB/VCB/MBB/ACB/BID/CTG/VPB)"`
After: `"Writing in-depth news articles about 27 listed Vietnamese banks (HOSE 16 + HNX 4 + UPCOM 7)"`

Workflow + 5 quality gates: NO CHANGE (universe-agnostic).

### Layer 7 — Commands + Orchestrator + Pipeline + Editor + CLAUDE.md

**Files:**
- `.claude/agents/newsroom-pipeline.md` — universe references line (Section 1 + 2)
- `.claude/agents/newsroom-editor.md` — description text
- `.claude/commands/tin.md` — alias mapping table extended
- `.claude/commands/tin-batch.md` — alias mapping table same
- `.claude/skills/finpath-newsroom-orchestrator/SKILL.md` — Universe section
- `CLAUDE.md` — Architecture map + universe section

**Change:** Mechanical text update — replace MVP universe references với FULL universe + alias coverage.

## 5. Test strategy

### Test 1 — Unit tests `routing.py` + `ticker_detection.py`

**File:** `tests/test_routing_expanded.py` (NEW), `tests/test_ticker_detection.py` (UPDATE)

```python
# tests/test_routing_expanded.py
def test_full_bank_universe_27_tickers():
    assert len(BANK_UNIVERSE) == 27
    for t in ["STB", "EIB", "NAB", "BVB", "PGB"]:
        assert t in BANK_UNIVERSE

def test_full_ck_universe_30_tickers():
    assert len(CK_UNIVERSE) == 30
    for t in ["VIX", "MBS", "FTS", "PSI", "AGR"]:
        assert t in CK_UNIVERSE

def test_get_sector_for_expanded_bank():
    for ticker in BANK_UNIVERSE:
        assert get_sector(ticker) == "Bank"

def test_get_sector_for_expanded_ck():
    for ticker in CK_UNIVERSE:
        assert get_sector(ticker) == "CK"

def test_alias_sacombank():
    detected = detect_combined("Sacombank công bố lợi nhuận quý 1")
    assert "STB" in detected

def test_alias_fpts():
    detected = detect_combined("FPTS báo cáo doanh thu môi giới")
    assert "FTS" in detected
```

Target: ≥ 30 unit tests covering high-priority new tickers.

### Test 2 — Smoke test pipeline per sector

After expand, manual smoke test (no publish):

```bash
/tin STB    # → Editor sets sector=Bank, dispatch master-bank
/tin FTS    # → Editor sets sector=CK, dispatch master-ck
/tin-batch VCB,STB,SSI,FTS    # mixed 2 sector parallel
```

Verify Editor routes correctly. Master can dispatch (don't require article persist).

### Test 3 — Finpath API spot-check (mã nhỏ)

```bash
uv run python -c "
from lib.finpath_api import FinpathAPI
api = FinpathAPI()
for t in ['STB', 'EIB', 'NAB', 'BVB', 'PGB']:
    try:
        ratios = api.get_bank_ratios(t)
        print(f'{t}: OK ({len(ratios.get(\"quarterlyProfits\", []))} quarters)')
    except Exception as e:
        print(f'{t}: FAIL — {e}')
"
```

Document log output. Master skill update nếu API thiếu data cho mã nào → fallback web_search rule.

### Test 4 — KB tiering verification

Manual read check:
- `kb/bank/frameworks/bank-industry-master-reference.md` § 1.2 tier table — verify cover ≥ 27 unique tickers
- `kb/ck/frameworks/ck-industry-master-reference.md` § 1.2 table — verify cover ≥ 30 unique tickers

### Test 5 — Existing tests pass

Existing 170 tests + ~30 new = ~200 pass after expand.

## 6. Implementation phases

5 atomic commit + 1 verification phase.

### Phase A — Universe registry + alias (foundational, TDD)

**Files:** `routing.py`, `ticker_detection.py`, `tests/test_routing_expanded.py` (NEW), `tests/test_ticker_detection.py` (UPDATE)

**TDD sequence:**
1. Write `test_routing_expanded.py` red phase
2. Update `BANK_UNIVERSE` + `CK_UNIVERSE` lists → green
3. Update `test_ticker_detection.py` for new aliases → red
4. Update `COMPANY_NAME_TO_TICKER` + regex → green
5. Pytest pass

**Commit:** `feat(routing): expand Bank universe 7→27 + CK 5→30`

### Phase B — Master skill + agent universe metadata

**Files:** 4 file (2 SKILL.md + 2 agent wrapper)

**Work:** Text update frontmatter description + Step 1 validation line.

**Commit:** `feat(skill): master-bank + master-ck universe expanded`

### Phase C — KB master-reference tiering tables

**Files:** 2 file

**Work:** Append rows vào Bank/CK tiering tables (Section 4 Layer 4 detail). Mỗi row 1-2 câu đặc thù.

**Commit:** `kb: extend Bank + CK tiering tables for expanded universe`

### Phase D — Pipeline + Editor + Orchestrator

**Files:** 3 file (pipeline.md + editor.md + orchestrator SKILL.md)

**Work:** Mechanical text update universe references.

**Commit:** `agent(newsroom): pipeline + editor + orchestrator universe expanded`

### Phase E — Commands + CLAUDE.md

**Files:** 3 file (tin.md + tin-batch.md + CLAUDE.md)

**Work:** Update alias mapping table + architecture map.

**Commit:** `docs+cmd: tin/tin-batch + CLAUDE.md universe expanded`

### Phase F — Verification + commit chain summary

**Work:**
1. Run full pytest `uv run pytest tests/` — expect ~200 pass
2. Smoke test sample tickers (Test 2)
3. Finpath spot-check (Test 3)
4. KB tiering visual verify (Test 4)
5. Advisor review trước push
6. User confirm + push origin/main

## 7. Risks & mitigation

| Risk | Mitigation |
|---|---|
| Em research list 57 mã chứa mã đã delist hoặc thiếu mã mới niêm yết | Phase A trước commit — em web search verify HOSE/HNX/UPCOM list current. User confirm sau khi review spec. |
| Finpath API `get_bank_ratios` thiếu data cho mã nhỏ (NAB/SGB/UPCOM) | Phase F spot-check. Nếu thiếu → Master skill update để document fallback web_search rule. |
| Alias collision (vd "MB" → MBB vs "MB" → mid-cap mining stock) | Pass 2 short-form regex case-sensitive + word boundary. Existing pattern handles tốt (170 test pass current). Mở rộng theo cùng pattern. |
| Some tickers có news volume rất thấp (UPCOM bank) → pipeline 0 candidates | Existing pipeline handles 0-candidate gracefully (reject batch, no crash). Don't fix. |
| KB tiering tables expand mistake (vd nhầm tier) | Manual review trong Phase C, advisor review Phase F. User verify spec list. |
| Big-bang rollout breaks existing Bank/CK pipeline | Phase A TDD catch regression. Existing 170 tests must pass after Phase A green. |

## 8. Success criteria

- [ ] `BANK_UNIVERSE` có 27 mã, `CK_UNIVERSE` có 30 mã trong `routing.py`
- [ ] `ticker_detection.py` có alias cho all 57 new tickers (≥ 80 alias entries total)
- [ ] All 4 master skill + wrapper files có universe description updated
- [ ] 2 KB master-reference files có tiering tables extend với 45 new rows
- [ ] 7 secondary files (pipeline/editor/orchestrator/cmd/CLAUDE.md) text universe synced
- [ ] Pytest pass ~200 tests (170 existing + ~30 new)
- [ ] Smoke `/tin STB` + `/tin FTS` route correctly (Editor sector field set)
- [ ] Finpath API spot-check log saved (≥ 5 small banks verified)
- [ ] Advisor review pass before push
- [ ] User push confirm

## 9. Open questions

(Không có — design đã chốt qua brainstorming. User verify ticker list trong implementation Phase A.)

## 10. Changelog

| Date | Version | Change |
|---|---|---|
| 2026-05-11 | v1.0 | Initial draft sau brainstorming với user |
