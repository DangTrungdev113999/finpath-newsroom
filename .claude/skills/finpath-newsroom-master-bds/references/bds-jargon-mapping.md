# BĐS Jargon Mapping — Tiếng Việt thuần

## ⚠️ QUY TẮC CỨNG — 0% TỪ TIẾNG ANH TRONG CONTENT USER-FACING

**Bài Master + Skeptic + Compare Feed cột trái + Cần để ý + insight_final = KHÔNG được có 1 từ tiếng Anh nào.**

Rule binary: hoặc 0% Anh, hoặc fail self-check, KHÔNG persist. Exception: tên riêng (HOSE, VHM, NVL, KDH, DXG, NHNN, UBCK, Q1/Q2/Q3/Q4) + Pipeline log internal.

### Bảng thay thế tiếng Anh → tiếng Việt thuần

Bảng KHÔNG đầy đủ. Quy tắc: thấy từ Anh → tìm tiếng Việt thay. Không có cách nói tiếng Việt → reformulate câu.

| Tiếng Anh | Tiếng Việt thuần |
|---|---|
| pre-sales | doanh thu chưa ghi nhận / hợp đồng đã ký |
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
| LNTT | lãi trước thuế / lợi nhuận trước thuế |
| total assets | tổng tài sản |
| project liquidity | thanh khoản dự án |
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
| YoY / QoQ / YTD | so cùng kỳ / so quý trước / từ đầu năm |

## ⚠️ CRITICAL — Enum metadata KHÔNG được leak vào content user-facing

Brief có 2 enum nội bộ — CHỈ dùng làm metadata, KHÔNG xuất hiện trong text user đọc.

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

### Enum `Critique angle` Skeptic (6 options)
`data_skepticism | historical_analog | alt_interpretation | risk_highlight | insight_wrong | execution_unfaithful` — cùng quy tắc. Mapping xem master-bank `references/jargon-mapping.md`.

### Anti-patterns

❌ "Đánh đổi chủ động (strategic-shift)" — KHÔNG để enum tag trong ngoặc
✅ "Đánh đổi chủ động — chuyển hướng chiến lược"

❌ "tin strategic-shift"
✅ "tin chuyển hướng chiến lược"

### Exception
Pipeline log toggle internal CÓ THỂ giữ enum dạng `code style backtick` cho power-user verify.

## Self-check trước khi viết xong

2 bước (binary pass/fail):

1. **0% Anh**: quét body + Cần để ý + insight_final + Skeptic. Có 1 từ tiếng Anh nào (kể cả viết tắt pre-sales/GFA/NAV/condotel, kể cả thông dụng move/momentum/defensive) → fail, REWRITE. Exception: tên riêng + Pipeline log internal.
2. **Enum leak**: search content cho 8 `insight_type` + 6 `Critique angle`. Nếu xuất hiện trong narrative → REPLACE bằng tiếng Việt theo bảng "Enum metadata" ở trên.
