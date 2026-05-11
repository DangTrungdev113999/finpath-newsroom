# CK Jargon Mapping V4.0 — Tiếng Việt thuần

## ⚠️ QUY TẮC CỨNG — 0% TỪ TIẾNG ANH TRONG CONTENT USER-FACING

**Bài Master + Skeptic + Compare Feed cột trái + insight_final = KHÔNG được có 1 từ tiếng Anh nào.**

V4.0 BAN heading `## Cần để ý` — caveats merge vào bullets hoặc closing. Rule này áp dụng cho mọi phần content user-facing (opening paragraph + bullets + closing + Skeptic critique).

Rule binary: hoặc 0% Anh, hoặc fail self-check (`no_english_jargon` gate), KHÔNG persist. Exception: tên riêng (HOSE, HNX, UPCoM, VN-Index, SSI, VND, HCM, VCI, SHS, NHNN, UBCK, Q1/Q2/Q3/Q4, FTSE) + Pipeline log internal toggle.

### Bảng thay thế tiếng Anh → tiếng Việt thuần

Bảng KHÔNG đầy đủ. Quy tắc: thấy từ Anh → tìm tiếng Việt thay. Không có cách nói tiếng Việt → reformulate câu.

| Tiếng Anh | Tiếng Việt thuần |
|---|---|
| margin | cho vay ký quỹ |
| margin outstanding | dư nợ cho vay ký quỹ |
| maintenance margin | tỷ lệ ký quỹ duy trì |
| margin call | bán giải chấp / yêu cầu nộp thêm tiền |
| broker | công ty chứng khoán |
| broker-dealer | công ty chứng khoán |
| brokerage | môi giới |
| prime brokerage | dịch vụ ký quỹ cao cấp |
| proprietary trading / prop trading | tự doanh |
| IB / investment banking | ngân hàng đầu tư / mảng đầu tư |
| trading fee | phí giao dịch |
| market share | thị phần |
| depository | lưu ký |
| repo | giao dịch mua bán có kỳ hạn |
| OTC desk | bàn giao dịch ngoài sàn |
| TPDN | trái phiếu doanh nghiệp |
| AUM | tài sản quản lý |
| NIM | biên lợi nhuận lãi vay |
| ROE / ROA | tỷ suất sinh lời trên vốn / trên tài sản |
| momentum | đà tăng / đà |
| defensive | thận trọng / phòng thủ |
| catalyst | yếu tố thúc đẩy |
| liquidity | thanh khoản |
| turnover | vòng quay |
| matching | khớp lệnh |
| outflow | rút vốn / dòng vốn ra |
| inflow | đổ vốn / dòng vốn vào |
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

### Exception
Pipeline log toggle internal CÓ THỂ giữ enum dạng `code style backtick` cho power-user verify.

## Self-check trước khi viết xong (V4.0)

2 bước (binary pass/fail) — bám sát 2 quality gate V4.0 `no_english_jargon` + `no_metadata_leak`:

1. **0% Anh** (gate `no_english_jargon`): quét title + opening paragraph + bullets + closing + insight_final + Skeptic critique. Có 1 từ tiếng Anh nào (kể cả viết tắt margin/broker/IB/AUM/market share, kể cả thông dụng move/momentum/defensive/catalyst/portfolio/trade-off) → fail, REWRITE. Exception: tên riêng (HOSE, HNX, UPCoM, VN-Index, NHNN, UBCK, FTSE, ticker) + Pipeline log internal toggle.
2. **Enum leak** (gate `no_metadata_leak`): search content cho 8 `insight_type` + 5 `deep_question_options[].category` (paradox/why_now/hidden_mechanism/comparison_deep/early_signal) + 6 `Critique angle`. Nếu xuất hiện trong narrative → REPLACE bằng tiếng Việt theo các bảng "Enum metadata" ở trên.

Fail gate 1 hoặc 2 → KHÔNG persist, loop rewrite cho đến khi pass cả 5 gate V4.0.
