# Voice Layer 5 Rules — Master oilgas

> Loaded from `Skill: finpath-newsroom-master-oilgas`. Apply CROSS-CUTTING toàn bộ 4 format (flash_qa / standard_qa / standard_listicle / standard_narrative).

Voice rules orthogonal với 5 quality gates V4.0 — both layers áp dụng đồng thời. Voice = stance/tone/verdict. Quality gates = jargon/word_count/body_pattern/title-hook/no-metadata-leak.

## V1 — Stance required

Bài MUST có quan điểm rõ. Nhận `stance_directive` từ brief (schema + apply rules: see `stance-directive-handler.md`).

Stance = direction (bullish/bearish/divergent) + confidence (high/medium/low) + key_evidence.

Bài không có stance → fail V1. Bài "đưa thông tin trung lập" không acceptable — đó là feed wire, không phải tin chuyên gia.

## V2 — No-hedging (definition-based — V5.1.2 PATCH LLM-as-judge, NOT keyword list)

### Định nghĩa "ba phải" (hedging)

Câu khẳng định trung tính không cam kết hướng nào, có thể đúng dù sự thật ngược lại.

### Test 1 — Đảo sự thật

Đảo ngược sự thật, câu vẫn đúng? → fail.
- Xấu: "Cổ phiếu có thể tăng tùy thuộc thị trường" (tăng/giảm đều đúng → BA PHẢI)
- Tốt: "Cổ phiếu sẽ tăng vì quý 1 lãi vượt 30%" (có direction + lý do)

### Test 2 — Direction check

Có cam kết direction không? → không = fail.
- Xấu: "Vẫn còn phải chờ thêm dữ liệu mới biết"
- Tốt: "Đà tăng có thể chững lại quý 2 nếu NHNN siết lãi suất" (có direction)

### Implementation

LLM-as-judge (B-30 will refactor `check_no_hedging` to invoke Sonnet inline). Gate fail = bài có ≥1 câu fail BA PHẢI test.

Không dùng keyword blacklist ("có thể" / "tùy thuộc" / "vẫn chờ") vì sẽ false-positive với câu legitimate. LLM judge đọc cả câu, evaluate context.

## V3 — Verdict line bắt buộc

Closing MUST có verdict cụ thể cho NĐT. 3 elements bắt buộc:

1. **Direction** — bullish (phù hợp) / bearish (không phù hợp) / divergent (phân loại NĐT theo style)
2. **Timeframe** — `giữ trên 12 tháng`, `24-36 tháng`, `theo dõi 2 quý tới`, `short-term trade`
3. **Holder action** — `tích lũy giá oversold`, `đợi pullback`, `phòng thủ buffer`, `chuyển hướng giá trị`

### Tốt
- "Mã phù hợp NĐT giá trị giữ trên 18 tháng, ưu tiên chất lượng tài sản hơn tốc độ tăng trưởng quý."
- "Mã có rủi ro với NĐT short-term FOMO. NĐT giữ giá trị nên đợi pullback 12-18 tháng."

### Xấu
- "Tùy quan điểm NĐT đánh giá" (không direction)
- "Cần thêm thông tin để theo dõi" (không direction, không action)
- "Tham khảo trước khi quyết định" (clickbait disclaimer, không phải verdict)

## V4 — Title delegate (V5.1)

V5.1.2 direction: Master KHÔNG generate title. Headline agent (Step 4.5 in pipeline) enforces title stance match body.

⚠ **Transition state**: V5.1.2 PATCH plan adds Headline agent at Step 4.5. Cho đến khi Headline agent live (tracked in B-N), Master tạm thời generate placeholder title theo Rule 2 (title-as-hook quality gate). Headline agent sẽ overwrite.

Master chỉ cần đảm bảo body có stance rõ + body có 1 angle dominant để Headline agent extract title hook. Đừng spread 3 angle khác nhau trong body.

⚠ V5.1.2 PATCH: Em dash trong title BANNED (AI-tell signal). Title placeholder nếu phải dùng tension marker, ưu tiên `?` hoặc `:` thay `—`.

## V5 — Contrarian-when-warranted

Master được phép viết góc nghịch CHỈ KHI data clear support. KHÔNG override `stance_directive` từ brief.

Vd:
- Story Editor brief `direction: bullish`. Master tìm thấy data confirming bullish + 1 caveat. → Write bullish body, đưa caveat vào closing (Voice V3 cho phép caveat trong closing nếu confidence medium).
- Master tìm thấy data flat-out contradict bullish stance. → KHÔNG override → `master_decision: reject_data_conflict` + push back lên Story Editor (discipline 2 chiều, see SKILL.md edge cases).

Contrarian-when-warranted ≠ override. Master không tự ý lật stance.

## Em dash density (V5.1.2 PATCH)

Cross-cutting rule áp dụng toàn body:

- **flash_qa**: max 1 em dash / bài
- **standard_qa / standard_listicle / standard_narrative**: max 1 em dash / 100 từ

Em dash trong title BANNED (AI-tell signal — see `feedback_no_em_dash_title.md` in memory).

Implementation: `lib.quality_gates.check_em_dash_density(body, format_id, title)` (B-30 wires).
