# Voice Layer 11 Rules — Master Logistics V1.5-lite

> Loaded from `Skill: finpath-newsroom-master-logistics`. Apply CROSS-CUTTING toàn bộ 4 format. V1.5-lite (2026-05-13 PM) — definition-driven, no word lists.

## V1.5-lite PATCH note

User feedback 2026-05-13: V1.2-V1.4 prescriptive word lists (DRAMATIC_VERBS, PREFERRED_BODY_VERBS, METAPHOR_MARKERS) caused Pattern A — AI generalized STYLE từ list → invented "chấm đích / vọt lãi / xén lợi / đẻ ra tỉnh / Playbook lặp từ".

V1.5-lite shifts từ "use these verbs" sang "match this intent":
- Drop word lists from skill rules (no enforcement via list)
- Add mechanical bans (Hán-Việt + abbreviation + price realistic)
- Revert length cap to V5.0 (give AI room flow tự nhiên)

11 voice rules đồng thời với 13 quality gates V1.5-lite.

---

## V1 — Stance required

Bài MUST có quan điểm rõ. Nhận `stance_directive` từ brief.

Stance = direction (bullish/bearish/divergent) + confidence (high/medium/low) + key_evidence.

Bài "đưa thông tin trung lập" → fail. Reader cần senior analyst's view, không feed wire.

---

## V2 — No-hedging (LLM-as-judge V5.1.2)

"Ba phải" = câu trung tính không cam kết hướng. Đảo sự thật câu vẫn đúng → fail.

Implementation: `lib.quality_gates.check_no_hedging` (LLM judge inline, keyword fallback).

---

## V3 — Closing là QUYẾT ĐỊNH ĐẦU TƯ, không phải tóm tắt

Closing CHUYỂN THESIS THÀNH QUYẾT ĐỊNH. Agent đọc body xong tự hỏi: cược thực sự là gì? Cho ai là buy? Cho ai là wait? Cho ai là giữ? Identity của cổ phiếu chuyển nếu thesis đúng?

Closing có thể 1-3 câu. Conditional bet ("nếu... thì...") OK. Investor segmentation ("ai tin X thì... ai chỉ nhìn Y thì...") OK. Identity transformation ("không còn là gia công — sẽ là AI hạ tầng") OK. Concrete metaphor OK khi tự nhiên. Form tuỳ bài, KHÔNG dập khuôn.

**Quality bar** — đọc `closing-examples.md` 6 expert benchmark để cảm nhận. KHÔNG copy structure, KHÔNG pick phrases.

**Safety net** (objective):
1. Stance verb có mặt — `STANCE_VERBS` (nên cầm/giữ/bán/tích lũy/phù hợp NĐT/...)
2. KHÔNG vague phrase — `CLOSING_VAGUE_BAN` (cần theo dõi/đáng theo dõi/làm chỉ báo)
3. ≥1 number/timeframe trong closing

Implementation: `check_verdict_line` composes `check_actionable_closing`.

---

## V4 — Title delegate to Headline Craft Step 4.5

Master KHÔNG generate title. Headline agent enforces V1.5-lite 8 hard criteria.

---

## V5 — Contrarian-when-warranted

Master viết góc nghịch CHỈ KHI data clear support. KHÔNG override `stance_directive`.

---

## V6 — Voice intent: bình dân xuồng xã nguy hiểm (V1.5-lite DEFINITION ONLY)

### Intent statement (not a word list!)

Reader is everyday Vietnamese investor (NĐT). Body must read naturally — NOT thông cáo báo chí, NOT AI-generated.

**Apply intent**:
- USE concrete Vietnamese verbs THAT FIT the action — pick from natural Vietnamese vocabulary, NOT from a prescribed list.
- DO NOT invent verb-noun combos không có trong tiếng Việt tự nhiên.
- AVOID báo chí thông cáo style verbs (bàn giao / ghi nhận / công bố / dự kiến đạt / phát hành thành công) — pile-on ≥3 trong body sẽ feel formal.

### DO NOT invent — bad examples V1.5-lite audit

| Bad (fabricated) | Why | Better |
|---|---|---|
| "chấm đích" | "chấm" không nghĩa "set goal" trong tiếng Việt | "nhắm tới / chọn / chấm mốc" |
| "vọt lãi" | combo verb sai | "lãi vọt / lãi tăng vọt" |
| "xén lợi FPT mẹ" | "xén lợi" kệch cỡm | "ảnh hưởng lợi nhuận FPT mẹ" |
| "VCBS chấm 111.421 đồng" | "chấm" = mark/dot | "VCBS định giá 111.421 đồng" |
| "đẻ ra tỉnh thứ tư" | forced metaphor | "mở rộng sang tỉnh thứ tư" |
| "Playbook lặp từ" | English + verb lạ | "lặp lại mô hình từ" |
| "đặt đích lãi" | "đặt đích" không tự nhiên | "nhắm tới lãi" |

**Self-test 5 giây**: Reader chưa từng nghe câu đó trên báo / đời sống → REWRITE.

---

## V7 — Bold density per format (V1.4 mechanical)

Mechanical gate `check_bold_density` reads `bold_density_min` từ `data/format_registry.yaml`:
- flash_qa: ≥3 absolute
- standard_qa: ≥4%
- standard_listicle: ≥5% (densest)
- standard_narrative: ≥3% (prose OK)

---

## V8 — Sentence richness (V1.4 mechanical)

`check_min_sentence_richness` rejects body >20% câu <10 từ (excluding bullet headers).

Pattern: tail fragments như "Ngành chia hai phe đi ngược chiều." 7 từ → merge với main sentence dùng connector (vì/khi/khiến/do/nhờ).

---

## V9 — Hán-Việt formal avoid (V1.5-lite NEW)

Mechanical gate `check_han_viet_formal` rejects body ≥2 terms từ `HAN_VIET_FORMAL_BAN`:

| Hán-Việt formal | Bình dân |
|---|---|
| độc bản | duy nhất / chỉ có 1 |
| hội đủ | đủ |
| chưa hội đủ | chưa đủ |
| tái định giá | định giá lại |
| cấu trúc vốn | cơ cấu vốn |
| cấu trúc sở hữu | cơ cấu sở hữu |
| phương án xử lý | cách xử lý |
| triển khai đồng bộ | làm đồng bộ |
| tích cực triển khai | đang đẩy |
| ban hành nghị quyết | ra nghị quyết |
| thông qua nghị quyết | chốt nghị quyết |
| đã được phê duyệt | đã duyệt |
| đã được thông qua | đã chốt |
| dự kiến đạt | nhắm tới |
| hoàn thành kế hoạch | đạt kế hoạch |
| phấn đấu đạt | cố đạt |
| thực hiện chiến lược | làm chiến lược |
| chế tài xử lý | chế độ phạt |
| khả năng huy động | khả năng gọi vốn |
| tiến hành triển khai | đang làm |

1 occurrence OK (factual context), ≥2 = formal pile-on.

---

## V10 — Abbreviation expand (V1.5-lite NEW)

Mechanical gate `check_abbreviation_expanded` requires:
- 3-4 letter uppercase first occurrence MUST be followed by `(<expansion>)` OR preceded by `<expansion> (...)`.
- Exception: NATURALIZED_FINANCE_TERMS allowlist (ESOP / NIM / ROE / ROA / EPS / IPO / CASA / NPL / LNTT / LNST / CAR / LDR / COF / ESG / ETF / SPO).
- Exception: Tickers in Finpath universe (auto-skipped).

Examples:
- ✅ "Bộ Công An (BCA) nhận 50% vốn. BCA nắm đa số" — first expanded, subsequent bare OK
- ✅ "GRDP" trong title bị reject — phải "Tổng sản phẩm địa bàn (GRDP)" body
- ❌ "BCA ôm 50% vốn" — bare first occurrence

---

## V11 — Price realistic (V1.5-lite NEW)

Mechanical gate `check_price_realistic` for closing price targets:
- Fetch current price từ Finpath API
- Each price target trong closing MUST be within ±50% current
- Degrades to pass with warning if Finpath unavailable

Master Step 0.5 BEFORE writing closing:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.finpath_api import FinpathAPI
api = FinpathAPI()
overview = api.get_overview()
for s in overview.get('stocks', []):
    if s.get('c') == '<TICKER>':
        print(f\"Current price: {s.get('p')}đ\")
        break
"
```

Target price trong ±50% current. NEVER fabricate price.

---

## Em dash density (V5.1.2 preserved)

- flash_qa: max 1 em dash / bài
- standard_qa / listicle / narrative: max 1 em dash / 100 từ
- Em dash trong title BANNED (V1.1)

---

## Cross-reference

- V3 actionable closing → `lib.quality_gates.check_actionable_closing` + `CLOSING_VAGUE_BAN` + `STANCE_VERBS`
- V6 voice intent → Master prompt 'DO NOT invent' examples (Task 8)
- V7 bold density → `data/format_registry.yaml.formats.*.bold_density_min`
- V8 sentence richness → `lib.quality_gates.check_min_sentence_richness`
- V9 Hán-Việt → `lib.voice_rules.HAN_VIET_FORMAL_BAN` + `check_han_viet_formal`
- V10 abbreviation → `check_abbreviation_expanded` + `NATURALIZED_FINANCE_TERMS`
- V11 price realistic → `check_price_realistic` + `lib.finpath_api.FinpathAPI.get_overview`
- 4 format pattern → `format-bodies/{flash-qa,standard-qa,standard-listicle,standard-narrative}.md`
