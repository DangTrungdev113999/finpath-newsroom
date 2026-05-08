# Master Pitfalls — Common Mistakes

12 pitfalls khi đọc data + viết bài Bank. Master phải avoid.

## CFS Reading Pitfalls (7) — V2.4 quan trọng

CFS = Cash Flow Statement (Lưu chuyển tiền tệ). Cần đọc cẩn thận khi viết bài về thanh khoản, capacity tăng trưởng, M&A.

### Pitfall 1: LCTT_HDKD âm KHÔNG luôn xấu
- LCTT_HDKD (lưu chuyển tiền từ hoạt động kinh doanh) âm có thể là dấu hiệu ngân hàng đang **mở rộng cho vay** mạnh — tốt
- KHÔNG phải lúc nào cũng = trouble
- Cross-check với credit growth + LDR → có context mới kết luận

### Pitfall 2: Cổ tức trả thực tế ≠ Cổ tức công bố
- DB field `Co_tuc_da_tra` = thực tế chi
- ĐHĐCĐ thường công bố tỷ lệ % nhưng chi cụ thể có thể chậm 1-2 quý
- Khi viết "TCB chia cổ tức 7% năm 2025" — phải verify Co_tuc_da_tra Q4/2025 hay Q1/2026 đã thấy chưa

### Pitfall 3: LCTT_HDDT (đầu tư) — phân biệt mua TPCP vs M&A
- LCTT_HDDT âm có thể là:
  - (a) Mua TPCP/TPDN dài hạn — bình thường, tốt
  - (b) M&A acquisition — khác hẳn
- Cross-check với note thuyết minh + DB M&A → biết case nào

### Pitfall 4: LCTT_HDTC (tài chính) — ESOP vs phát hành mới
- LCTT_HDTC dương có thể là:
  - (a) Phát hành ESOP nhỏ — không quan trọng
  - (b) Phát hành cổ phiếu mới quy mô lớn — material event
  - (c) Vay nợ mới — khác
- Ngân hàng to (VCB, BID, CTG) khó tăng vốn → mỗi lần là big news

### Pitfall 5: Tien_va_tuong_duong_cuoi_ky vs Tiền gửi NHNN
- DB field `Tien_va_tuong_duong_cuoi_ky_ty_dong` = cash + cash equivalents
- KHÔNG phải = tiền gửi NHNN (dự trữ bắt buộc)
- Đừng nhầm khi viết về liquidity

### Pitfall 6: Free Cash Flow không có khái niệm thuần ngân hàng
- FCF (free cash flow) là khái niệm corp finance, không apply thuần cho bank
- Bank dùng LCTT_HDKD + LCTT_HDDT làm proxy
- KHÔNG viết "FCF của VCB Q1..." — sai concept

### Pitfall 7: thuan_trong_ky_ty_dong = Net change in cash
- Đây là tổng (HDKD + HDDT + HDTC)
- Mỗi quý có thể swing lớn (vd Q1 -50K tỷ, Q2 +30K tỷ) — KHÔNG phải trend
- Nhìn 4 quý liên tiếp mới có pattern thật

## BCTC Reading Pitfalls (5)

### Pitfall 8: NPL nhóm 3-4-5 vs NPL theo quy định mới
- Pre-2024: NPL = nhóm 3-4-5
- Post Thông tư 02/2023: bao gồm cả nợ tái cơ cấu giữ nhóm
- So sánh giai đoạn phải cùng metric

### Pitfall 9: NIM annualize trong quarterly report
- Một số báo cáo show NIM của quý (không annualize) — số nhỏ hơn
- Phải verify: NIM 0.8% (quý) ≠ NIM 3.2% (annualized)
- DB BCTC Bank Quarter standardize annualized

### Pitfall 10: ROE/ROA dùng vốn bình quân vs vốn cuối kỳ
- Vốn bình quân (average) = (đầu kỳ + cuối kỳ) / 2 — đúng
- Vốn cuối kỳ — overstated nếu vốn vừa tăng
- VCB BCTC dùng average, một số bank tư nhân dùng cuối kỳ → so sánh phải cẩn thận

### Pitfall 11: Tăng trưởng tín dụng vs hạn mức NHNN giao
- "Tăng trưởng tín dụng 12%" có thể là:
  - (a) Đã đạt 12% trong năm — actual
  - (b) Hạn mức NHNN giao 12% — chưa actual
- Verify với DB Credit Room + actual loans Q1

### Pitfall 12: Vốn điều lệ vs Vốn chủ sở hữu
- Vốn điều lệ = par × số cổ phiếu (face value)
- Vốn chủ sở hữu = điều lệ + thặng dư + lợi nhuận giữ lại + các quỹ
- Bank to (VCB) vốn chủ sở hữu thường gấp 3-4x điều lệ
- KHÔNG nhầm khi viết "TCB vốn lớn nhất tư nhân" — phải clarify metric nào

## Definition Pitfalls (3) — V2.5 mới sau TCB run

### Pitfall 13: Tiền gửi (deposit) có 2-3 định nghĩa khác nhau

Mỗi nguồn dùng định nghĩa khác. KHÔNG bao giờ trộn số mà không nói rõ định nghĩa.

| Nguồn | Định nghĩa | Bao gồm gì |
|---|---|---|
| DB BCTC Wichart `Huy_dong_ty_dong` | Hẹp | Tiền gửi khách hàng (CA + TD), KHÔNG có CD/giấy tờ có giá |
| TCB official press release "tiền gửi khách hàng" | Rộng | Bao gồm CD + sinh lời tự động |
| BCTC NHNN "huy động vốn thị trường 1" | Trung | Bao gồm liên ngân hàng |

**Case study TCB Q1/2026** đã từng phát hiện:
- DB Wichart: 599.808 tỷ → giảm 19.103 tỷ QoQ (-3,09%)
- TCB official: 651.000 tỷ → tăng 14,2% YoY
- KHÔNG mâu thuẫn — 2 định nghĩa khác. Khi viết phải clarify "theo định nghĩa Wichart" / "theo công bố TCB".

**Rule**: Khi có discrepancy >5%, Master phải:
1. Note source định nghĩa cụ thể trong Pipeline log
2. Skeptic raise nếu Master không clarify
3. Body bài viết "tiền gửi (theo BCTC Wichart) ..." chứ không "tiền gửi ..."

### Pitfall 14: Tăng trưởng tín dụng — TCB official vs DB calc

TCB (và một số bank) có thể công bố tăng trưởng tín dụng YTD theo **định nghĩa nội bộ** khác với DB BCTC Wichart `Du_no_ty_dong` calc.

**Case TCB Q1/2026**:
- TCB official: +2,89% YTD
- DB calc: Du_no Q4/2025 = 767.617 tỷ → Q1/2026 = 796.864 tỷ = **+3,81% YTD** (chênh 0,9pp)

**Lý do** có thể: Du_no Wichart bao gồm investment banking book / trái phiếu doanh nghiệp / nợ liên ngân hàng. TCB official có thể chỉ tính loans-to-customers thuần.

**Rule**:
- Master query DB → tính growth từ DB → so với TCB official
- Nếu chênh ≥0,5pp → note discrepancy trong Pipeline log + Skeptic potentially raise
- KHÔNG silent dùng số TCB official mà bỏ qua DB calc

### Pitfall 15: CASA Q1 quarterly có thể chưa có trong DB Wichart

Wichart upload BCTC theo timeline:
- BS (bảng cân đối) + IS (kết quả KD) + PT (phụ lục thuyết minh) — upload sớm sau ĐHĐCĐ
- CFS (lưu chuyển tiền tệ) — upload sau 1-2 tuần
- CASA detail / NIM / ROE quarterly — đôi khi không upload Q1, chờ H1 hoặc 9M

**Case TCB Q1/2026**: DB row có LNTT/NPL/Du_no/Huy_dong nhưng `CASA_pct = NULL`, `NIM_pct = NULL`, `ROE_pct = NULL`.

**Rule**:
- Master KHÔNG silent skip field NULL — phải log "DB null cho CASA Q1, fallback web search"
- Web search lấy CASA từ TCB press release / sell-side report
- Skeptic verify: nếu Master claim CASA mà DB null → flag "data từ source nào?"

## Enum Leak Pitfalls (2) — V2.5 mới

### Pitfall 16: Enum metadata KHÔNG được leak vào content user-facing

Story Editor brief có 2 enum: `insight_type` (8 options) + `Critique angle` (6 options). Master và Skeptic dùng làm metadata variety guard. NHƯNG enum tag KHÔNG được xuất hiện trong text user đọc.

**Anti-pattern thường gặp**:
- ❌ "Trade-off chủ động (strategic-shift)" → bỏ ngoặc enum, dùng tiếng Việt
- ❌ "tin strategic-shift" → "tin chuyển hướng chiến lược"
- ❌ "Skeptic angle = `risk_highlight`" trong narrative → "Skeptic chọn góc 'rủi ro bị bỏ qua'"

**Rule**:
- Brief.angle viết FREE STYLE tiếng Việt — KHÔNG đính tag enum trong ngoặc
- Compare Feed cột phải "Cách viết & lý do chọn" — viết tiếng Việt thuần, không tag
- Pipeline log toggle CÓ THỂ giữ enum tag dưới dạng `code style backtick` vì là log internal cho power-user
- Body bài Master + Skeptic body — TUYỆT ĐỐI không enum tag

Xem `references/jargon-mapping.md` section "CRITICAL — Enum metadata KHÔNG được leak" để có bảng mapping đầy đủ.

### Pitfall 17: Jargon Anh không giải thích lần đầu

**Anti-pattern**: viết "trade-off", "anchor", "relevant", "confirm", "pattern" trong content mà không giải thích.

**Rule**: Lần đầu xuất hiện jargon Anh → giải thích tiếng Việt + viết tắt Anh trong ngoặc. Lần sau dùng viết tắt. Self-check trước khi finalize: gạch chân tất cả từ Anh, mỗi từ phải có giải thích lần đầu.

Xem bảng đầy đủ trong `references/jargon-mapping.md`.
