---
category: frameworks
title: "Industrial-Park-Master-Reference"
last_updated: 2026-05-12
---

Master reference cho ngành Khu công nghiệp Việt Nam — mental model 6 lớp phân tích. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **KBC · SZC · BCM · IDC · LHG · PHR · GVR · SIP · NTC · VGC**.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Industrial_Park/knowledge.md + web search enrichment (metrics 2025-2026, lease price, FDI data). Format theo chuẩn bank-industry-master-reference.md. |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Mô hình kinh doanh

Doanh nghiệp KCN sinh lợi nhuận từ hai nguồn chính:

- **Cho thuê đất (70-85%):** Mua đất thô → Đền bù/Giải phóng mặt bằng → Xây hạ tầng → Cho thuê đất 50 năm (thu 1 lần trả trước) → Doanh thu lớn nhưng không đều theo thời điểm ký hợp đồng
- **Dịch vụ + Phí quản lý + Nhà xưởng xây sẵn (15-30%):** Thu đều hàng tháng/năm — recurring revenue ổn định hơn; nhà xưởng xây sẵn (RBF) có biên cao hơn đất trống

Driver ngắn hạn là dòng vốn FDI và tiến độ giải phóng mặt bằng. Driver dài hạn là xu hướng China+1, hạ tầng giao thông, và năng lực cung ứng quỹ đất sẵn sàng.

## 1.2 Phân loại doanh nghiệp (structural — không per-quarter)

### Nhóm đầu ngành — quỹ đất lớn

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| KBC | Kinh Bắc | Quỹ đất lớn nhất ngành; KCN Quang Châu, Nam Sơn Hạp Lĩnh, Tràng Duệ, Nam Bình Dương; khách lớn Samsung, Foxconn |
| BCM | Becamex IDC | Liên doanh Singapore (VSIP); đa ngành KCN + đô thị + hạ tầng; mạnh Bình Dương |
| GVR | Tập đoàn Cao su | ~400.000 ha đất cao su → chuyển đổi KCN; quỹ đất tiềm năng lớn nhất dài hạn |

### Nhóm miền Nam — vị trí chiến lược

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| SZC | Sonadezi Châu Đức | KCN Châu Đức (Bà Rịa); gần cảng Cái Mép — lợi thế logistics xuất khẩu |
| IDC | IDICO | Đa ngành: KCN Nhơn Trạch + điện + nước; doanh thu ổn định từ nhiều mảng |
| LHG | Long Hậu | KCN Long Hậu (Long An); nhỏ gọn, gần TP.HCM; quỹ đất hạn chế |
| PHR | Cao su Phước Hòa | Cao su + KCN Bình Dương; đất cao su chuyển đổi KCN |
| NTC | Nam Tân Uyên | KCN Nam Tân Uyên (Bình Dương); nhỏ, gần đầy, tăng trưởng hạn chế |

### Nhóm khác

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| SIP | Sài Gòn Tân Bình | KCN trong nội thành TP.HCM (Tân Bình, Vĩnh Lộc); gần hết quỹ đất |
| VGC | Viglacera | KCN + vật liệu xây dựng; đa ngành |

> **Decision rule phân loại**: Quỹ đất sẵn sàng = giá trị cốt lõi. KCN đầy 100% = không tăng trưởng mới. Nhóm có đất cao su chuyển đổi (GVR, PHR) = pipeline dài hạn nhưng cần thời gian GPMB. Nhóm gần cảng (SZC, IDC) = lợi thế logistics cho sản xuất xuất khẩu.

## 1.3 FDI kiểm soát — yếu tố #1

- **Tỷ trọng FDI:** 70-80% khách thuê KCN là FDI. FDI tăng = KCN hưởng lợi trực tiếp.
- **China+1:** Xu hướng cấu trúc 10-20 năm — doanh nghiệp toàn cầu đa dạng hóa sản xuất khỏi Trung Quốc. Việt Nam = điểm đến #1 khu vực.
- **Ngành FDI chủ lực:** Điện tử (Samsung, Foxconn, Apple supply chain), chip/bán dẫn (NVIDIA, Intel), xe điện (EV), năng lượng tái tạo.
- **FDI 2025:** Giải ngân ước đạt 27,62 tỷ USD (+9% so với cùng kỳ) — cao nhất giai đoạn 2021-2025. Sản xuất chế biến chiếm 82,8%.
- **FDI Q1/2026:** Giải ngân 7,4 tỷ USD trong 4 tháng đầu năm (+9,8% so với cùng kỳ) — cao nhất 5 năm.

> **Nguyên tắc cốt lõi**: Phân tích KCN mà không phân tích FDI = thiếu 80% bức tranh.

## 1.4 Giải phóng mặt bằng (GPMB) — nút thắt #1

- **GPMB xong:** Giá trị CAO — cho thuê ngay được
- **Đang GPMB:** Giá trị TRUNG BÌNH — 1-2 năm nữa mới sẵn sàng
- **Chờ phê duyệt:** Giá trị THẤP — 2-5 năm, chưa chắc được duyệt

> **Quỹ đất lớn chưa GPMB ≠ giá trị tức thì.** Phải phân biệt: đất sẵn sàng vs đang GPMB vs chờ phê duyệt.

## 1.5 Đặc thù thị trường Việt Nam

- Hơn 400 KCN quy hoạch toàn quốc; tỷ lệ lấp đầy trung bình >80%
- Giá thuê tăng cấu trúc: Việt Nam rẻ hơn Trung Quốc 2-3 lần, Thái Lan 1,5 lần
- DT theo hợp đồng — biến động mạnh theo quý, đừng đánh giá 1 quý đơn lẻ
- Q4 thường mạnh hơn (FDI đẩy quyết định cuối năm)
- RBF (nhà xưởng xây sẵn) tăng tỷ trọng → xu hướng cải thiện biên lợi nhuận

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics quan trọng

**Tier 1 — Thị trường phản ứng ngay:**

| Metric | Ý nghĩa | Benchmark 2025-2026 |
|---|---|---|
| Tỷ lệ lấp đầy | >85% = gần hết quỹ đất, <70% = còn nhiều đất trống | Bắc: 83-86%; Nam: 90-92% |
| Giá thuê (USD/m²/50 năm) | Tăng 5-10% = bình thường, >15% = thiếu cung | Bắc: 133-145; Nam: 189-200 |
| Diện tích cho thuê mới (ha) | Nhu cầu FDI trực tiếp | So cùng kỳ năm trước |
| FDI đăng ký mới VN | Cầu KCN toàn ngành | ~33-38 tỷ USD/năm |
| Quỹ đất sẵn sàng cho thuê (ha) | Pipeline doanh thu | So tổng diện tích |

**Tier 2 — Phản ứng chậm 1-3 quý:**

| Metric | Benchmark |
|---|---|
| DT dịch vụ recurring | Tăng theo diện tích đã cho thuê |
| DT nhà xưởng xây sẵn (RBF) | Tăng tỷ trọng = biên cải thiện |
| Biên lợi nhuận gộp | Đất: 50-70%; RBF: 40-60%; Dịch vụ: 30-50% |
| Tiến độ GPMB | GPMB xong = sẵn sàng cho thuê |
| Pipeline KCN mới được phê duyệt | Quỹ đất tương lai |

**Tier 3 — Dài hạn:**

| Metric | Ý nghĩa |
|---|---|
| Vị trí KCN | Gần cảng, sân bay, cao tốc = hấp dẫn hơn |
| Anchor tenant | Samsung, Foxconn, Apple supply chain. Mất = rủi ro |
| Xu hướng China+1 | Cấu trúc 10-20 năm |
| Hạ tầng mới | Cao tốc, cảng, sân bay gần KCN |

## 2.2 Cách đọc doanh thu

- DT nhảy theo thời điểm ký HĐ — phải nhìn CẢ NĂM + pipeline
- Check: Tổng diện tích cho thuê mới, giá thuê, pipeline đang đàm phán, DT recurring, deferred revenue (doanh thu chờ ghi nhận)

```
DT tăng 300% 1 quý ≠ tốt bền vững → Nhìn cả năm + pipeline đàm phán
```

## 2.3 Bẫy BCTC KCN

| Bẫy | Cách tránh |
|---|---|
| DT tăng 300% quý này | Nhìn cả năm + pipeline; có thể chỉ là timing ký HĐ |
| Tỷ lệ lấp đầy 95% = tốt | Check: KCN mới được phê duyệt? Không KCN mới = hết tăng trưởng |
| Quỹ đất 5.000 ha | Tách rõ: sẵn sàng vs đang GPMB vs chờ phê duyệt |
| FDI tăng 20% | Check: FDI vào KCN nào? Có vào KCN của mã đang phân tích? |
| Lấp đầy 100% | Không còn đất = không tăng trưởng trừ khi có KCN mới |
| P/E thấp năm ký HĐ lớn | DT đột biến 1 năm → P/E giả thấp |

## 2.4 Checklist BCTC (8 câu hỏi)

1. Diện tích cho thuê mới bao nhiêu? Giá bao nhiêu?
2. Tỷ lệ lấp đầy từng KCN hiện tại?
3. Xu hướng giá thuê tăng/giảm?
4. Quỹ đất phân loại: sẵn sàng / đang GPMB / chờ phê duyệt?
5. Pipeline KCN mới được phê duyệt?
6. Khách thuê mới: Samsung? Apple supply chain? Foxconn?
7. DT recurring (dịch vụ + phí quản lý) tăng/giảm?
8. Tiến độ GPMB có đúng kế hoạch?

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Nguyên tắc cốt lõi

```
KCN = ngành ít chu kỳ nhất Việt Nam:
- FDI = xu hướng cấu trúc (China+1), không phải chu kỳ ngắn hạn
- Hợp đồng thuê 50 năm — doanh thu đã ký ổn định
- Đất công nghiệp hữu hạn — cung không thể tăng nhanh

Cổ phiếu KCN = growth ổn định, gần giống FPT
DT biến động theo thời điểm ký HĐ — không phải chu kỳ thật
```

## 3.2 Wave FDI — chu kỳ dài hạn

| Wave | Thời kỳ | Đặc trưng | KCN hưởng lợi |
|---|---|---|---|
| Wave 1 | 2005-2015 | Samsung, Intel vào VN | Bắc Ninh, Đồng Nai |
| Wave 2 | 2018-2023 | Apple, Foxconn mở rộng supply chain | Bắc Giang, Hải Phòng |
| Wave 3 | 2024-2030+ | AI/chip/bán dẫn, xe điện (EV) | KCN nào nắm bắt được? |

> **Đầu tư KCN = đặt cược vào wave FDI tiếp theo.**

## 3.3 Tín hiệu nhận diện

### KCN sắp tốt
- FDI tăng mạnh, deal FDI lớn (Samsung, Apple, NVIDIA)
- Tỷ lệ lấp đầy + giá thuê tăng
- KCN mới được phê duyệt, GPMB hoàn thành
- Cao tốc/cảng/sân bay mới gần KCN

### KCN sắp khó
- FDI giảm (suy thoái toàn cầu, thương chiến leo thang)
- FDI chuyển sang Ấn Độ, Indonesia
- GPMB vướng mắc kéo dài
- Cung KCN tăng quá nhanh so với cầu
- Anchor tenant rút
- VND mạnh làm KCN "đắt hơn" với FDI

---

# LỚP 4: HIỂU VĨ MÔ

## 4.1 Yếu tố vĩ mô tác động KCN

| Yếu tố | Tác động |
|---|---|
| **FDI vào VN** | #1 — 80%. Tăng = cầu KCN tăng trực tiếp |
| **China+1** | MEGA TREND 10-20 năm — VN = điểm đến #1 |
| **Thương chiến Mỹ-Trung** | FDI chuyển từ Trung Quốc sang VN |
| **Hạ tầng (cao tốc, cảng, sân bay)** | KCN gần = hưởng lợi trực tiếp |
| **Giá thuê so khu vực** | VN rẻ hơn Trung Quốc 2-3x, Thái Lan 1,5x |
| **Nhân lực** | Trẻ, giá rẻ; thiếu kỹ sư là thách thức |
| **GPMB** | Nút thắt #1 — chậm = không có đất cho thuê |
| **VND** | Mạnh = KCN "đắt hơn" cho FDI USD |
| **ESG + xanh** | FDI ngày càng ưu tiên KCN xanh, hạ tầng bền vững |

## 4.2 Ma trận ảnh hưởng vĩ mô

| Yếu tố | KBC | SZC | IDC | BCM | GVR |
|---|---|---|---|---|---|
| FDI tăng | +++ | ++ | ++ | ++ | ++ |
| Samsung mở rộng | +++ | + | + | + | + |
| Apple supply chain | ++ | + | + | ++ | + |
| Cảng Cái Mép | + | +++ | ++ | + | + |
| Cao tốc Bắc-Nam | ++ | ++ | ++ | ++ | ++ |
| GPMB vướng | -- | - | - | - | -- |
| Chuyển đổi đất cao su | + | + | + | + | +++ |

## 4.3 Động lực tăng trưởng

**Cấu trúc (dài hạn):**
- China+1 — xu hướng 10-20 năm
- Apple, NVIDIA, chip/bán dẫn vào VN
- Đất công nghiệp hữu hạn — cung không thể tăng nhanh
- Hạ tầng mới (cao tốc, cảng, sân bay)
- RBF (nhà xưởng xây sẵn) tăng tỷ trọng
- FTA (Hiệp định thương mại tự do) — VN có nhiều FTA

**Chu kỳ (ngắn hạn):**
- Deal FDI lớn (Samsung, Apple, Foxconn)
- KCN mới được phê duyệt
- GPMB hoàn thành
- Giá thuê tăng

## 4.4 Rủi ro

**Cấu trúc:**
- FDI chuyển sang Ấn Độ, Indonesia
- Cạnh tranh từ KCN các nước ASEAN khác
- Thiếu lao động kỹ năng cao (kỹ sư, kỹ thuật viên)
- Yêu cầu ESG ngày càng cao

**Chu kỳ:**
- FDI giảm do suy thoái toàn cầu
- GPMB vướng mắc kéo dài
- Cung KCN tăng quá nhanh
- Anchor tenant rút
- VND tăng giá mạnh

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 NAV — Phương pháp #1

NAV (Net Asset Value) là phương pháp định giá chính cho KCN:

```
NAV = Giá trị đất (đã thuê + chưa thuê) + RBF + Dịch vụ − Nợ
```

**Cách tính giá trị đất:**
- Đã cho thuê: Giá × Diện tích × Thời gian còn lại
- Chưa thuê (GPMB xong): Giá thị trường
- Chưa GPMB: Discount 30-50%
- Chờ phê duyệt: Discount 50-70%

**Discount to NAV:**
- KCN VN: 20-40% là bình thường
- >40% = có thể rẻ
- <20% = có thể đắt

## 5.2 P/E — Phương pháp phụ

- P/E biến động mạnh vì DT theo HĐ
- Dùng P/E trung bình 3 năm hoặc forward P/E (dựa trên pipeline)
- Benchmark: KBC 8-18x; SZC 10-15x; IDC 8-14x; NTC 8-12x

## 5.3 P/B

- 1,5-3,0x: Hợp lý
- >3x: Có thể đắt
- <1x: Có thể rẻ hoặc đất không có giá trị (GPMB vướng)

## 5.4 Bẫy định giá

| Bẫy | Thực tế |
|---|---|
| P/E thấp năm ký HĐ lớn | DT đột biến 1 năm → P/E giả thấp |
| Quỹ đất lớn nhưng chưa GPMB | Chưa có giá trị tức thì |
| Tỷ lệ lấp đầy 95% | Tốt hiện tại nhưng hết growth nếu không có KCN mới |

**Rẻ thật:**
- Quỹ đất lớn + GPMB sắp xong + FDI wave mới + Discount NAV >30%

**Đắt thật:**
- Gần đầy + không KCN mới + P/E đỉnh HĐ

---

# LỚP 6: CASE STUDY + TƯ VẤN

## 6.1 Định vị từng mã

| Mã | Ưu điểm | Nhược điểm | Phù hợp |
|---|---|---|---|
| **KBC** | Quỹ đất lớn nhất; Samsung/Foxconn; pipeline ~115 ha backlog (2025) | DT nhảy theo HĐ; GPMB chậm một số dự án | NĐT dài hạn tin vào FDI |
| **SZC** | Gần cảng Cái Mép; logistics xuất khẩu | Nhỏ hơn KBC; tập trung Bà Rịa | NĐT muốn KCN miền Nam |
| **IDC** | Đa ngành: KCN + điện + nước; DT ổn định | KCN chỉ 1 phần DT | NĐT muốn ổn định |
| **BCM** | VSIP uy tín; đa ngành; Bình Dương | Phức tạp; nhiều mảng | NĐT thích Bình Dương |
| **GVR** | Quỹ đất cao su tiềm năng lớn nhất | Chuyển đổi KCN cần nhiều năm | NĐT cực dài hạn (5-10 năm) |
| **PHR** | Cao su + KCN Bình Dương | Quy mô nhỏ; đất chuyển đổi | NĐT muốn đa dạng |
| **LHG** | Gần TP.HCM | Nhỏ; quỹ đất hạn chế | NĐT muốn mã nhỏ miền Nam |
| **NTC** | Ổn định; gần đầy | Hết growth nếu không mở rộng | NĐT muốn cổ tức |

## 6.2 Theo profile nhà đầu tư

- **Dài hạn (>1 năm):** Focus China+1, quỹ đất. Ưu tiên KBC, GVR. Cổ tức 3-4%
- **Trung hạn (3-12 tháng):** Focus deal FDI cụ thể, GPMB hoàn thành. Ưu tiên KBC, SZC, BCM
- **Ngắn hạn (<3 tháng):** Focus deal FDI cụ thể, BCTC quý. Timing khó vì DT theo HĐ

## 6.3 Khi nào VÀO (cần 2-3/6 tín hiệu)

1. FDI tăng mạnh (>10% so với cùng kỳ)
2. Deal FDI lớn mới (Samsung, Apple, NVIDIA)
3. KCN mới được phê duyệt
4. GPMB hoàn thành
5. Giá thuê tăng
6. Discount NAV >30%

## 6.4 Khi nào THOÁT (cần 2-3/5 tín hiệu)

1. FDI giảm 2 quý liên tiếp
2. FDI chuyển sang Ấn Độ, Indonesia rõ rệt
3. Tỷ lệ lấp đầy + giá thuê giảm
4. Gần đầy + không KCN mới
5. GPMB vướng nghiêm trọng

## 6.5 Thuật ngữ cho NĐT ít kinh nghiệm

| Thuật ngữ | Dịch |
|---|---|
| KCN | Khu công nghiệp — khu đất đã xây hạ tầng để cho nhà máy thuê |
| FDI | Vốn đầu tư trực tiếp nước ngoài — công ty nước ngoài mở nhà máy ở VN |
| Tỷ lệ lấp đầy 85% | 85% đất đã có nhà máy thuê — gần đầy |
| GPMB | Giải phóng mặt bằng — đền bù cho dân để lấy đất — mất nhiều năm |
| China+1 | Xu hướng chuyển nhà máy từ Trung Quốc sang VN để giảm rủi ro |
| $150/m²/50 năm | Mỗi m² thuê 150 USD cho 50 năm — VN vẫn rẻ so với khu vực |
| NAV | Giá trị tài sản ròng — tổng giá trị đất trừ nợ — so với giá CP xem đắt rẻ |
| RBF | Ready-Built Factory — nhà xưởng xây sẵn — thuê ngay không cần tự xây |
| Anchor tenant | Khách thuê chủ lực lớn — Samsung, Foxconn, Apple |

---

# PHỤ LỤC

## A. Severity đánh giá tin tức

| Mức | Tín hiệu |
|---|---|
| **green** | FDI + cho thuê + giá tăng; deal FDI lớn; GPMB xong; KCN mới phê duyệt |
| **yellow** | DT nhảy 1 quý (timing HĐ); FDI đi ngang; GPMB chậm 1-2 dự án |
| **red** | FDI giảm 2+ quý; tỷ lệ lấp đầy + giá giảm; gần đầy không KCN mới; GPMB vướng nhiều; anchor rút |
| **blue** | Trung tính |

## B. Câu đánh giá mẫu

**FDI mới + cho thuê tốt:**
> "{ticker} cho thuê thêm {X} ha — tăng {Y}% so với cùng kỳ. Khách mới: {tên FDI}. Giá {Z} USD/m² — tăng {W}%. China+1 tiếp tục thúc đẩy nhu cầu."

**Gần đầy + chờ KCN mới:**
> "{ticker} đã thuê {X}% — gần hết. Doanh thu quản lý tăng {Y}%. Tăng trưởng chậm lại. Đang xin phê duyệt {tên KCN} — thêm {Z} ha."

**GPMB vướng:**
> "{ticker} có {X} ha quy hoạch nhưng chưa đền bù xong. Quý cho thuê {Y} ha, giảm {Z}% so với cùng kỳ."

**China+1:**
> "Việt Nam nhận {X} tỷ USD FDI trong quý, tăng {Y}%. {ticker}: {Z} công ty mới ký hợp đồng. VN rẻ hơn Trung Quốc 2-3 lần."

## C. Quy tắc agent

1. FDI = #1 → check FDI trước mọi phân tích
2. DT theo HĐ → nhìn cả năm + pipeline
3. Quỹ đất = giá trị #1 → phân biệt: sẵn sàng vs GPMB vs chờ phê duyệt
4. GPMB = nút thắt → tiến độ GPMB quyết định pipeline
5. Tỷ lệ lấp đầy 100% = không tăng trưởng → cần KCN mới
6. NAV = phương pháp định giá #1 → discount >30% có thể hấp dẫn
7. China+1 = xu hướng 10-20 năm → structural, không phải speculation
8. Dịch thuật ngữ cho NĐT mới
9. Không bịa data — verify từ Finpath API / web search

---

## Hướng dẫn tra dữ liệu thời gian thực

KB master này chỉ cung cấp framework + threshold + range historical. Khi viết bài quý cụ thể, Master phải:

1. **Query KB framework** (file này) — static guidance
2. **Finpath API** cho data realtime:
   - `get_financial_ratios(ticker)` — PE/PB/ROE quarterly + yearly
   - `get_income_statement(ticker)` + `get_balance_sheet(ticker)` — BCTC quý
   - `get_shareholders(ticker)` + `get_events(ticker)` + `get_news(ticker)` — ownership + ĐHĐCĐ + tin
3. **Web search** cho data Finpath API không có:
   - Tỷ lệ lấp đầy từng KCN
   - Giá thuê cập nhật
   - Deal FDI mới
   - Tiến độ GPMB
   - Pipeline KCN phê duyệt mới

KHÔNG bịa số — mọi data phải có source.

---

## Cross-link (khi mở rộng)

| File | Nội dung chính |
|---|---|
| `industrial-park-fdi-tracker.md` | (tương lai) Theo dõi FDI wave + deal lớn |
| `industrial-park-gpmb-status.md` | (tương lai) Tiến độ GPMB từng KCN chính |
| `industrial-park-lease-price-trend.md` | (tương lai) Xu hướng giá thuê Bắc/Nam |

---

## Phần suy luận (cần verify)

Các điểm dưới đây rút từ framework + data web search — cần verify khi đưa vào bài cụ thể:

- **"Tỷ lệ lấp đầy Bắc 86%, Nam 90%"** — từ web search 2025; số cụ thể quý hiện tại cần verify
- **"Giá thuê Bắc 133-145 USD/m², Nam 189-200 USD/m²"** — từ web search 2025; cần verify với nguồn cụ thể
- **"FDI giải ngân 27,62 tỷ USD năm 2025"** — từ web search; cần verify số liệu chính thức
- **"KBC backlog ~115 ha"** — từ web search 2025; cần verify BCTC KBC mới nhất
