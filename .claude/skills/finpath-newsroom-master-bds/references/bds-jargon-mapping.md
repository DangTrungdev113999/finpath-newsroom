# BĐS Jargon Mapping V4.0 — Tiếng Việt thuần

## ⚠️ QUY TẮC CỨNG — 0% TỪ TIẾNG ANH TRONG CONTENT USER-FACING

**Bài Master + Skeptic + Compare Feed cột trái + insight_final = KHÔNG được có 1 từ tiếng Anh nào.**

V4.0 BAN heading `## Cần để ý` — caveats merge vào bullets hoặc closing. Rule này áp dụng cho mọi phần content user-facing (opening paragraph + bullets + closing + Skeptic critique).

Rule binary: hoặc 0% Anh, hoặc fail self-check (`no_english_jargon` gate), KHÔNG persist. Exception: tên riêng (Vinhomes, Novaland, Khang Điền, Đất Xanh, VHM, NVL, KDH, DXG, NHNN, Q1/Q2/Q3/Q4) + Pipeline log internal toggle.

### Bảng thay thế tiếng Anh → tiếng Việt thuần

Bảng KHÔNG đầy đủ. Quy tắc: thấy từ Anh → tìm tiếng Việt thay. Không có cách nói tiếng Việt → reformulate câu.

| Tiếng Anh | Tiếng Việt thuần |
|---|---|
| pre-sales | doanh số bán trước / hợp đồng đã ký |
| backlog | doanh số chờ ghi nhận |
| GFA | tổng diện tích sàn |
| NAV | giá trị tài sản ròng |
| land bank | quỹ đất |
| project | dự án |
| developer | chủ đầu tư |
| legal status | pháp lý dự án |
| land use right certificate | sổ đỏ / sổ hồng |
| apartment | căn hộ chung cư |
| townhouse | nhà liền kề |
| shophouse | nhà phố thương mại |
| villa | biệt thự |
| land lot | đất nền |
| condotel | căn hộ khách sạn |
| absorption rate | tỷ lệ hấp thụ / tỷ lệ bán được |
| project lifecycle | chu kỳ phát triển dự án |
| TPDN | trái phiếu doanh nghiệp |
| FDI | vốn đầu tư trực tiếp nước ngoài |
| LNTT / LNST | lợi nhuận trước thuế / lợi nhuận sau thuế |
| total assets | tổng tài sản |
| total debt / equity | tổng nợ / vốn chủ sở hữu |
| project liquidity | thanh khoản dự án |
| EBITDA | lợi nhuận trước lãi vay, thuế và khấu hao |
| ROE / ROA | tỷ suất sinh lời trên vốn / trên tài sản |
| momentum | đà tăng / đà |
| defensive | thận trọng / phòng thủ |
| catalyst | yếu tố thúc đẩy |
| speculation | đầu cơ |
| trade-off | đánh đổi |
| anchor | nguồn chính / căn cứ chính |
| relevant | liên quan |
| confirm | xác nhận |
| pattern | mô hình / khuôn mẫu |
| breaking | vừa xảy ra / mới |
| move (noun) | bước đi / quyết định / động thái |
| symbolic | mang tính biểu tượng |
| metric | chỉ số |
| event | sự kiện |
| story | câu chuyện |
| scenario | kịch bản |
| target | mục tiêu / kế hoạch |
| portfolio | danh mục |
| opportunity cost | chi phí cơ hội |
| stress test | kiểm thử căng |
| buffer | đệm phòng vệ |
| YoY / QoQ / YTD | so cùng kỳ / so quý trước / từ đầu năm |

## ⚠️ CRITICAL — Enum metadata KHÔNG được leak vào content user-facing

Brief V4.0 có 3 enum nội bộ — CHỈ dùng làm metadata, KHÔNG xuất hiện trong text user đọc. Self-check gate `no_metadata_leak` quét content cho 3 enum families bên dưới.

### Enum `insight_type` (Story Editor → Master)
8 giá trị: `phân loại cổ phiếu | decode | risk | pattern | catalyst | strategic-shift | industry-impact | position`

| Enum (metadata only) | Viết trong content (tiếng Việt) |
|---|---|
| `strategic-shift` | "chuyển hướng chiến lược" / "đổi mô hình kinh doanh" |
| `decode` | "giải mã" / "đọc hiểu" |
| `catalyst` | "điểm xúc tác" / "yếu tố thúc đẩy" |
| `industry-impact` | "tác động ngành" / "ảnh hưởng đến ngành" |
| `pattern` | "mô hình" / "khuôn mẫu lặp lại" |
| `risk` | "rủi ro" / "điểm rủi ro" |
| `position` | "vị thế" / "định vị cạnh tranh" |

### Enum `deep_question_options[].category` (V4.0 — Story Editor → Master)
5 giá trị: `paradox | why_now | hidden_mechanism | comparison_deep | early_signal` — CHỈ dùng metadata phân loại câu hỏi đào sâu, KHÔNG được viết trong content.

| Enum (metadata only) | Viết trong content (tiếng Việt) |
|---|---|
| `paradox` | "nghịch lý" / "2 sự kiện ngược chiều" |
| `why_now` | "vì sao thời điểm này" / "vì sao chọn lúc này" |
| `hidden_mechanism` | "cơ chế ẩn" / "cách vận hành đằng sau con số" |
| `comparison_deep` | "so sánh sâu" / "đối chiếu góc nhìn mới" |
| `early_signal` | "chỉ dấu sớm" / "tín hiệu sớm của chu kỳ" |

### Enum `Critique angle` Skeptic (6 options)
`data_skepticism | historical_analog | alt_interpretation | risk_highlight | insight_wrong | execution_unfaithful` — cùng quy tắc. Mapping xem master-bank `references/jargon-mapping.md`.

### Anti-patterns

❌ "Đánh đổi chủ động (strategic-shift)" — KHÔNG để enum tag trong ngoặc
✅ "Đánh đổi chủ động — chuyển hướng chiến lược"

❌ "tin strategic-shift"
✅ "tin chuyển hướng chiến lược"

❌ "Câu hỏi đào sâu thuộc loại paradox"
✅ "Câu hỏi đào sâu về nghịch lý 2 sự kiện ngược chiều"

### Exception
Pipeline log toggle internal CÓ THỂ giữ enum dạng `code style backtick` cho power-user verify.

## Self-check trước khi viết xong (V4.0)

2 bước (binary pass/fail) — bám sát 2 quality gate V4.0 `no_english_jargon` + `no_metadata_leak`:

1. **0% Anh** (gate `no_english_jargon`): quét title + opening paragraph + bullets + closing + insight_final + Skeptic critique. Có 1 từ tiếng Anh nào (kể cả viết tắt pre-sales/backlog/GFA/NAV/condotel/land bank/project/developer, kể cả thông dụng move/momentum/defensive/catalyst/portfolio/trade-off) → fail, REWRITE. Exception: tên riêng (Vinhomes/Novaland/Khang Điền/Đất Xanh/VHM/NVL/KDH/DXG/NHNN/Q1-4) + Pipeline log internal toggle.

2. **Enum leak** (gate `no_metadata_leak`): search content cho 8 `insight_type` + 5 `deep_question_options[].category` (paradox/why_now/hidden_mechanism/comparison_deep/early_signal) + 6 `Critique angle`. Nếu xuất hiện trong narrative → REPLACE bằng tiếng Việt theo các bảng "Enum metadata" ở trên.

Fail gate 1 hoặc 2 → KHÔNG persist, loop rewrite cho đến khi pass cả 5 gate V4.0 (no_english_jargon + word_count 200-400 + body_pattern + title_as_hook + no_metadata_leak).

## V4.0 body pattern — KHÔNG heading `## Cần để ý`

V4.0 BAN heading `## Cần để ý`. Caveat phải merge vào bullet substantive HOẶC closing sentence — không được tách thành section riêng.

### Pattern good (V4.0):
- Caveat merge vào bullet: `**Doanh số bán trước co 4 quý — chỉ dấu sớm cho chu kỳ trầm tới**: ... — nhà đầu tư cần theo dõi số Q2 trước khi quyết định.`
- Caveat merge vào closing: `VHM phù hợp NĐT giá trị giữ trên 12 tháng — chấp nhận mẫu hình doanh thu lồi theo quý để đổi lấy quỹ đất pháp lý sạch trên 70%, miễn doanh số bán trước Q2 không co thêm dưới 6 nghìn tỷ.`

### Pattern bad (V3.6 — V4.0 BAN):
```
## Cần để ý
Q2/2026 báo cáo tài chính chính thức công bố giữa tháng 7 — số doanh số bán trước thực tế sẽ xác nhận hay phản bác xu hướng đang thấy.
```
→ Fail gate `body_pattern`. REWRITE bằng cách merge vào bullet hoặc closing.
