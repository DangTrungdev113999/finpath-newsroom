---
category: frameworks
title: "Tourism-Industry-Master-Reference"
last_updated: 2026-05-12
---

Master reference cho Master Tourism — mental model 6 lớp phân tích ngành du lịch VN. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc ngành Du lịch & Khách sạn.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Tourism/knowledge.md + web search enrichment. Thêm data RevPAR/Occupancy 2025, visa policy 2025-2026, danh sách mã niêm yết. |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Chuỗi giá trị

```
KHÁCH DU LỊCH (Quốc tế + Nội địa)
→ VẬN CHUYỂN: Hàng không (VJC, HVN, ACV)
→ LƯU TRÚ: Khách sạn (VIC-Vinpearl, AGG), resort, homestay
→ ĂN UỐNG & GIẢI TRÍ: Nhà hàng, theme park (VinWonders, Đầm Sen)
→ MUA SẮM & LỮ HÀNH: Tour operator (VTR), OTA

Du lịch = HỆ SINH THÁI, không phải ngành đơn lẻ
Đóng góp GDP du lịch ~10% GDP VN (trực tiếp + gián tiếp)
```

## 1.2 Phân loại doanh nghiệp niêm yết

### Nhóm lữ hành

| Mã | Tên | Sàn | Đặc trưng cấu trúc |
|---|---|---|---|
| VTR | Vietravel | UPCOM | "Ông vua lữ hành" VN; biên lợi nhuận mỏng 3-5%; phụ thuộc volume; đang tái cấu trúc tài chính |

### Nhóm công viên giải trí / điểm đến

| Mã | Tên | Sàn | Đặc trưng cấu trúc |
|---|---|---|---|
| DSN | Công viên nước Đầm Sen | HOSE | Doanh thu theo lượng khách; mùa vụ rõ (hè peak); chi phí cố định cao |
| HOT | Du lịch - Dịch vụ Hội An | UPCOM | Điểm đến di sản UNESCO; hưởng lợi khách quốc tế cao cấp |
| TCT | Cáp treo Núi Bà Tây Ninh | UPCOM | Độc quyền tuyến cáp; mùa vụ theo lễ hội tâm linh |

### Nhóm sân bay (độc quyền)

| Mã | Tên | Sàn | Đặc trưng cấu trúc |
|---|---|---|---|
| ACV | Cảng hàng không Việt Nam | UPCOM | Độc quyền 22 sân bay; doanh thu theo hành khách; margin cao; Long Thành sắp mở |

### Nhóm hàng không

| Mã | Tên | Sàn | Đặc trưng cấu trúc |
|---|---|---|---|
| HVN | Vietnam Airlines | HOSE | Hãng quốc gia; đang tái cơ cấu xóa lỗ lũy kế; nhạy giá dầu |
| VJC | Vietjet Air | HOSE | Low-cost carrier; đội bay trẻ; tài chính tốt hơn HVN |

### Nhóm khách sạn/resort (tích hợp trong tập đoàn)

| Mã | Tên | Sàn | Đặc trưng cấu trúc |
|---|---|---|---|
| VIC | Vingroup | HOSE | Vinpearl 45+ KS/resort ~18.000 phòng + VinWonders + Golf; du lịch chỉ 1 mảng trong đa ngành |

> **Lưu ý**: Cổ phiếu du lịch thuần trên sàn VN rất ít — chủ yếu VTR, DSN, HOT, TCT. Các DN lớn chưa niêm yết: Sun Group, Saigontourist, Mường Thanh. Phân tích du lịch qua sàn VN = phân tích GIÁN TIẾP qua ACV, VJC, VIC.

## 1.3 Ai quyết định luật chơi

**Khách quốc tế (#1):**
- 2019: 18 triệu lượt (pre-COVID peak)
- 2025: 13,9 triệu lượt (YTD tháng 8/2025, +20,7% so cùng kỳ)
- Mục tiêu 2026: 25 triệu lượt
- Thị trường nguồn: Trung Quốc (#1, 30-35%), Hàn Quốc (#2), Nhật Bản, Đài Loan, Mỹ, EU

**Chính sách visa (2025-2026):**
- Miễn visa song phương: 15 quốc gia
- Miễn visa đơn phương: 12 quốc gia (bao gồm Ba Lan, Séc, Thụy Sĩ từ 2025)
- E-visa: mở rộng áp dụng cho TẤT CẢ quốc gia và vùng lãnh thổ
- Thời hạn visa du lịch: 45 ngày (tăng từ 30 ngày)

**Sức mua nội địa:** 100 triệu dân, thu nhập tăng → du lịch nội địa tăng mạnh

**Rủi ro Trung Quốc:** TQ mở/đóng biên = game changer (30-35% khách quốc tế)

## 1.4 Mùa vụ

| Tháng | Đặc điểm |
|---|---|
| T1-T2 | **Peak #1** (Tết Nguyên Đán + Tết Trung Quốc/Hàn Quốc) |
| T3-T6 | Cao (xuân + hè bắt đầu) |
| T7-T8 | **Peak #2** (hè) |
| T9-T10 | **Thấp nhất** (bão, mưa miền Trung) |
| T11-T12 | Cao (Giáng sinh, Năm mới) |

**Quy tắc:** Q1 + Q3 mạnh nhất. Q3 cuối có thể bị bão. Q4 đầu yếu nhất.

## 1.5 Đặc thù thị trường Việt Nam

- **Chi phí cố định cao** → Đòn bẩy hoạt động: khách giảm 30% → lợi nhuận giảm 70-80%; ngược lại tương tự
- **Occupancy rate = Metric số 1**: >70% lãi | 50-70% hòa vốn | <50% lỗ
- **VN = Điểm đến giá rẻ** (rẻ hơn Thái Lan, Bali) → doanh thu/khách thấp → cần volume lớn
- **Doanh thu/khách quốc tế:** VN ~1.000-1.200 USD (Thái Lan: ~1.500 USD)
- **Thời gian lưu trú trung bình:** VN 3-4 đêm (mục tiêu: 5-7 đêm)
- **Cạnh tranh khu vực**: Thái Lan #1 (40 triệu khách/năm), VN #3-4 Đông Nam Á

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics quan trọng

### Tier 1 — Phản ứng ngay

| Metric | Áp dụng | Benchmark 2025 |
|---|---|---|
| Lượng khách quốc tế đến VN | Toàn ngành | 2019: 18 triệu. Mục tiêu 2026: 25 triệu |
| Occupancy rate | Khách sạn, resort | Hà Nội 59,5%, TPHCM 65,7% (YTD T8/2025) |
| RevPAR = Occupancy × ADR | Khách sạn | VN +17% YoY (2025), dẫn đầu khu vực |
| ADR (giá phòng trung bình/đêm) | Khách sạn | Hà Nội 124 USD, TPHCM 121 USD (2025) |
| Lượng hành khách qua sân bay | ACV, VJC | So cùng kỳ + so 2019 |

### Tier 2 — Phản ứng chậm

| Metric | Benchmark |
|---|---|
| Doanh thu/khách | VN: 1.000-1.200 USD/khách quốc tế (Thái: 1.500 USD) |
| Thời gian lưu trú trung bình | VN: 3-4 đêm, mục tiêu: 5-7 đêm |
| Cơ cấu khách theo quốc tịch | TQ 30-35%, Hàn 20%, Nhật 7%, Mỹ+EU 15% |
| Phòng khách sạn mới | Nhiều quá → ép occupancy + giá |
| GOP margin | >35% tốt, <25% yếu |

### Tier 3 — Dài hạn

- Xếp hạng du lịch VN (UNWTO, WEF Travel & Tourism Index)
- Đường bay quốc tế mới
- Visa policy updates
- Hạ tầng mới (sân bay Long Thành, cao tốc)

## 2.2 Bộ 3: Occupancy + ADR + RevPAR

```
RevPAR = Occupancy × ADR = Doanh thu/phòng có sẵn

Ví dụ: Khách sạn 100 phòng
- Occupancy 70%, ADR 80 USD → RevPAR = 56 USD
- Occupancy 60%, ADR 100 USD → RevPAR = 60 USD

RevPAR tăng = TỐT | RevPAR giảm = XẤU
Tăng occupancy → Lợi nhuận tăng MẠNH (chi phí cố định không đổi)
LÝ TƯỞNG: Occupancy + ADR tăng cùng lúc
```

**Benchmark 2025 (CBRE Vietnam):**
- Hà Nội: Occupancy 59,5%, ADR 124 USD, RevPAR 74 USD (+21% YoY)
- TPHCM: Occupancy 65,7%, ADR 121 USD, RevPAR 79 USD (+18% YoY)
- Phân khúc cao cấp TPHCM: Occupancy 83%, ADR ~180 USD

## 2.3 Đòn bẩy hoạt động

```
Khách sạn 100 phòng: Chi phí cố định 500 triệu/tháng, chi phí biến đổi 200.000đ/khách/đêm

Occupancy 50% (1.500 đêm): Doanh thu 1,2 tỷ | Chi phí 800 triệu | Lợi nhuận 400 triệu
Occupancy 70% (2.100 đêm): Doanh thu 1,68 tỷ (+40%) | Chi phí 920 triệu (+15%) | Lợi nhuận 760 triệu (+90%!)

→ Doanh thu tăng 40% → Lợi nhuận tăng 90% (chi phí cố định KHÔNG ĐỔI)
```

## 2.4 Bẫy phổ biến

| Bẫy | Thực tế |
|---|---|
| "Khách quốc tế tăng 30%" | Có thể base COVID thấp → phải so 2019 |
| "Khách sạn doanh thu tăng 40%" | Có thể do mở khách sạn mới → check RevPAR same-hotel |
| "Occupancy 80%" | ADR có thể giảm → check RevPAR |
| "VIC mảng du lịch lãi" | VIC đa ngành → phải tách mảng riêng |
| "Khách TQ quay lại" | TQ có thể hạn chế lại bất cứ lúc nào |
| "Resort mới khai trương" | Occupancy thấp ban đầu → check ramp-up (6-12 tháng) |

## 2.5 Checklist đánh giá

1. Khách quốc tế quý/năm? So cùng kỳ + so 2019
2. Occupancy + ADR + RevPAR?
3. Cơ cấu khách: TQ bao nhiêu %?
4. Cung phòng mới: ép occupancy + giá?
5. Mùa vụ: Q3 cuối (bão) yếu là bình thường
6. Chi phí cố định: nhân sự, thuê mặt bằng, bảo trì
7. Hạ tầng mới: sân bay, đường bay
8. Visa + Chính sách quảng bá

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Nguyên tắc

- Du lịch = CHU KỲ + MÙA VỤ + TAIL RISK
- Giá cổ phiếu chạy TRƯỚC lượng khách thực tế
- Tin tốt (nới visa, mở đường bay) → Cổ phiếu tăng ngay

## 3.2 Bốn giai đoạn

| Giai đoạn | Đặc điểm | Cổ phiếu |
|---|---|---|
| ĐÁY | Khách gần 0, khách sạn đóng cửa, LỖ NẶNG | Tăng TRƯỚC khi khách quay lại |
| HỒI PHỤC | Khách quay lại, occupancy tăng nhanh, revenge travel | **TĂNG MẠNH NHẤT** (100-300%), kéo dài 1-2 năm |
| TĂNG TRƯỞNG | Khách vượt pre-crisis, khách sạn mở mới, lợi nhuận ổn định | Tăng chậm |
| ĐỈNH → SUY GIẢM | Cung > cầu, kinh tế chậm, hoặc dịch mới | Giảm |

## 3.3 Bằng chứng lịch sử — ACV

| Giai đoạn | Thời điểm | Hành khách | Giá cổ phiếu |
|---|---|---|---|
| Đỉnh | 2019 | 116 triệu lượt (ATH) | ~85.000đ |
| Sụp đổ | 2020-2021 | Giảm 70-80% | 85.000đ → 55.000đ |
| Đáy | Q3/2021 | Gần 0 khách quốc tế | ~55.000đ |
| Hồi phục | 2022-2023 | 90% mức 2019 | 55.000đ → 80.000đ |
| Vượt 2019 | 2024-2025 | Vượt 2019 | 80.000đ → 95.000đ |

## 3.4 Tín hiệu sớm

**Du lịch sắp hồi phục:**
- Dịch kiểm soát / Vaccine phổ biến
- Nới visa / Mở biên / TQ mở biên
- Đường bay quốc tế mở lại
- Booking tăng (Google Trends "Vietnam travel")
- Giá dầu giảm → vé rẻ

**Du lịch sắp chạm đỉnh:**
- Cung khách sạn tăng quá nhanh → ép occupancy
- ADR giảm
- Kinh tế suy thoái / Dịch bệnh mới
- Giá dầu tăng mạnh

---

# LỚP 4: HIỂU VĨ MÔ

## 4.1 Yếu tố vĩ mô

| Yếu tố | Tác động |
|---|---|
| Khách quốc tế | **#1** — TQ mở/đóng biên = game changer |
| Visa policy | Nới → khách tăng ngay (VN đã nới e-visa toàn cầu 2025) |
| Giá dầu | Tăng → vé đắt → ít bay |
| Tỷ giá | VND yếu → VN rẻ cho khách ngoại |
| GDP nước nguồn | TQ, Hàn, Nhật giàu → đi du lịch nhiều |
| Dịch bệnh | Tail risk: Doanh thu → 0 |
| Thời tiết | Bão → khách hủy |
| Cạnh tranh khu vực | Thái, Bali quảng bá mạnh |
| Hạ tầng mới | Sân bay Long Thành (dự kiến 2026), đường bay mới |
| Thu nhập nội địa | Tăng → du lịch nội địa tăng |

## 4.2 Phụ thuộc Trung Quốc — Rủi ro lớn nhất

- TQ = 30-35% khách quốc tế đến VN
- TQ MỞ biên → khách đổ sang, toàn ngành tăng vọt
- TQ ĐÓNG biên → mất 30-35% khách, khó bù bằng nước khác
- **Phân tích du lịch VN PHẢI theo dõi chính sách TQ**

## 4.3 Ma trận ảnh hưởng

| Yếu tố | KS/Resort | Hàng không | Theme park | Lữ hành |
|---|---|---|---|---|
| Khách quốc tế tăng | +++ | +++ | ++ | ++ |
| TQ mở biên | +++ | ++ | ++ | +++ |
| Dầu tăng | 0 | -- | 0 | - |
| VND yếu | + | 0 | + | + |
| Dịch bệnh | --- | --- | --- | --- |
| Bão | -- | - | - | - |
| Cung khách sạn mới | - | 0 | 0 | 0 |
| Nới visa | ++ | ++ | + | ++ |

## 4.4 Động lực tăng trưởng

**Cấu trúc (dài hạn):**
- Trung lưu châu Á mở rộng
- VN rẻ + ẩm thực + biển + di sản UNESCO
- Sân bay Long Thành (2026)
- Đường bay quốc tế mới
- Thu nhập VN tăng
- Digital tourism + e-visa toàn cầu

**Chu kỳ (ngắn hạn):**
- TQ mở biên (2023)
- Nới visa 45 ngày (2023)
- Giá dầu giảm
- Revenge travel
- Sự kiện lớn (SEA Games, F1, concert quốc tế)

## 4.5 Rủi ro

| Rủi ro | Mức độ |
|---|---|
| Dịch bệnh mới | Cao — tail risk, doanh thu → 0 |
| TQ đóng biên | Cao — mất 30% khách |
| Cung khách sạn tăng nhanh | Trung bình — ép occupancy |
| Giá dầu tăng mạnh | Trung bình — vé đắt |
| Suy thoái toàn cầu | Trung bình |
| Thiên tai (bão) | Thấp — tạm thời |
| Cạnh tranh Thái, Bali | Thấp — dài hạn |

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 EV/EBITDA — Phương pháp chính cho khách sạn

- Khách sạn: chi phí cố định + khấu hao lớn → EBITDA phản ánh tốt hơn lợi nhuận ròng
- Premium resort: 12-18x | Khách sạn thành phố: 8-14x | Khu vực: 10-15x
- **EV/Room:** VN 50-100.000 USD/phòng (< khu vực 100-200.000 USD)

## 5.2 P/E — Cẩn thận đòn bẩy hoạt động

- Lợi nhuận biến động mạnh → Dùng P/E normalized (trung bình 3-5 năm) hoặc P/E forward
- VTR: P/E 10-15x | ACV: P/E 20-30x (độc quyền)

## 5.3 EV/Room

- VN: 50-100.000 USD/phòng → còn rẻ so khu vực (Thái 100-150.000 USD, Singapore 300-500.000 USD)
- Rẻ → cơ hội, nhưng check occupancy + ADR

## 5.4 Bẫy định giá

- "Khách sạn P/E 8x = rẻ" → Có thể đỉnh mùa, occupancy 85% tạm thời
- "ACV P/E 30x = đắt" → Độc quyền + tăng trưởng 15%/năm → xứng premium
- "VTR P/E 5x = rẻ" → Biên 3-5%, 1 mùa xấu là lỗ

**Tín hiệu tốt:** RevPAR + Occupancy + ADR tăng + Cung không tăng quá nhanh → Lợi nhuận tăng mạnh nhờ đòn bẩy → xứng premium

---

# LỚP 6: TƯ VẤN

## 6.1 Phân biệt rủi ro

| Tình huống | Loại | Phản ứng |
|---|---|---|
| Khách giảm T9-T10 | Mùa vụ | Bình thường |
| Khách quốc tế giảm 3 tháng liên tiếp | Xu hướng | Xem kinh tế TQ/Hàn/Nhật |
| Bão lớn → khách sạn đóng 2 tuần | Sự kiện | Tạm thời |
| COVID mới → biên giới đóng | Tail risk | Giảm exposure ngay |
| TQ hạn chế du lịch nước ngoài | Chính sách | Nghiêm trọng |
| Khách sạn mới → occupancy cũ giảm | Cung tăng | Theo dõi RevPAR same-hotel |

## 6.2 Tư vấn theo profile

**NĐT dài hạn (>1 năm):**
- Focus: ACV (độc quyền, Long Thành), VIC (nếu tách được mảng du lịch)
- Tránh: BĐS nghỉ dưỡng pháp lý phức tạp, lữ hành nhỏ
- Rủi ro: Dịch bệnh — tail risk luôn tồn tại

**NĐT trung hạn (3-12 tháng):**
- Vào: TQ mở biên + nới visa + dầu giảm + pre-season
- Thoát: Dịch mới + TQ siết + occupancy giảm + cung tăng nhanh

**NĐT ngắn hạn (<3 tháng):**
- Vào: Trước Tết (T11-T12) hoặc trước hè (T4-T5)
- Thoát: Sau peak hoặc mùa bão (T9-T10)
- Catalyst: TQ mở biên, visa mới, sự kiện quốc tế, dầu giảm

## 6.3 Khi nào VÀO (cần 2-3/7)

1. Dịch kiểm soát / hết dịch
2. TQ mở biên
3. Nới visa thị trường lớn
4. Đường bay quốc tế mới
5. Occupancy tăng từ đáy
6. Giá dầu giảm
7. Insider mua cổ phiếu

**Mạnh nhất:** Post-dịch + TQ mở + visa nới = triple catalyst → Cổ phiếu +100-300%

## 6.4 Khi nào THOÁT (cần 2-3/6)

1. Dịch bệnh mới
2. TQ đóng biên
3. RevPAR giảm (Occupancy + ADR giảm)
4. Cung khách sạn tăng quá nhanh
5. Giá dầu tăng >30%
6. Insider bán cổ phiếu

---

# PHỤ LỤC

## A. Severity

- **green:** Khách quốc tế + Occupancy + ADR + RevPAR tăng | Không dịch/thiên tai | Lợi nhuận tăng mạnh
- **yellow:** Khách tăng nhưng ADR giảm | Occupancy tăng nhờ khách sạn mới | Mùa bão 1-2 tháng | TQ chưa mở hoàn toàn
- **red:** Khách quốc tế giảm mạnh | Dịch mới | RevPAR giảm | Cung khách sạn quá nhanh | Lợi nhuận giảm/lỗ
- **blue:** Trung tính

## B. Câu đánh giá mẫu

**Khách quốc tế tăng + RevPAR tốt:**
> "Lượng khách quốc tế đến VN tăng {X}% so cùng kỳ, vượt mức trước COVID. {ticker}: {Y}% phòng có người ở (tăng từ {Z}%), giá phòng trung bình tăng {W}%. Chi phí vận hành gần như không đổi → lợi nhuận tăng mạnh hơn doanh thu."

**TQ mở biên:**
> "TQ dỡ hạn chế du lịch nước ngoài. Khách TQ đến VN tăng {X}%, chiếm {Y}% tổng khách quốc tế. {ticker} doanh thu tăng {Z}% nhờ khách TQ quay lại."

**Cung khách sạn tăng nhanh:**
> "Dù khách tăng {X}%, occupancy {ticker} giảm từ {Y}% xuống {Z}% vì nhiều khách sạn mới mở. Giá phòng giảm {W}% để cạnh tranh. Xu hướng này tiếp tục → lợi nhuận bị ảnh hưởng."

**Đáy chu kỳ (post-dịch):**
> "Doanh thu {ticker} còn thấp hơn {X}% so trước dịch — nhưng khách quốc tế hồi phục nhanh: +{Y}% so quý trước. Miễn visa {Z} nước mới, nhiều đường bay quốc tế mở lại. Cổ phiếu du lịch thường hồi phục mạnh nhất khi khách bắt đầu quay lại — trước cả khi doanh thu về mức cũ."

## C. Quy tắc cho agent

1. RevPAR = metric tổng hợp nhất → LUÔN check
2. So với 2019 mới chính xác → KHÔNG chỉ so cùng kỳ năm COVID
3. TQ = 30-35% khách → PHẢI theo dõi chính sách TQ
4. Đòn bẩy hoạt động cao → Lợi nhuận biến động GẤP 2-3 LẦN doanh thu
5. Dịch bệnh = tail risk → PHẢI cảnh báo NĐT
6. VIC đa ngành → PHẢI tách mảng du lịch
7. Cung khách sạn mới → có thể ép occupancy dù khách tăng
8. Mùa vụ rõ → so cùng kỳ, không so quý trước
9. KHÔNG dùng thuật ngữ tiếng Anh → PHẢI dịch
10. KHÔNG bịa data → Thiếu → nói thiếu

## D. Danh sách mã universe (tham khảo)

| Mã | Tên | Phân khúc | Sàn |
|---|---|---|---|
| VTR | Vietravel | Lữ hành | UPCOM |
| DSN | Công viên nước Đầm Sen | Theme park | HOSE |
| HOT | Du lịch Hội An | Điểm đến | UPCOM |
| TCT | Cáp treo Núi Bà Tây Ninh | Điểm đến | UPCOM |
| ACV | Cảng hàng không VN | Sân bay | UPCOM |
| HVN | Vietnam Airlines | Hàng không | HOSE |
| VJC | Vietjet Air | Hàng không | HOSE |
| VIC | Vingroup (Vinpearl) | Đa ngành | HOSE |

---

## Hướng dẫn tra dữ liệu thời gian thực (cho Master Tourism)

KB master này chỉ cung cấp framework + threshold + range historical. Khi viết bài quarter cụ thể, Master phải:

1. **Query KB framework** (file này) — static guidance.
2. **Finpath API** cho data realtime:
   - `get_income_statement(ticker)` + `get_balance_sheet(ticker)` — BCTC quarter
   - `get_events(ticker)` + `get_news(ticker)` — sự kiện + tin
3. **Web_search** cho data đặc thù:
   - Lượng khách quốc tế từ Tổng cục Du lịch (vietnamtourism.gov.vn)
   - RevPAR/Occupancy/ADR từ CBRE Vietnam, STR Global
   - Visa policy updates từ Bộ Ngoại giao
   - TQ travel policy từ nguồn tin quốc tế

Pipeline log V4.0 emit `data_trail` array: `{source, fetched, purpose, supports_argument}` per fact. KHÔNG bịa số.

---

## Cross-link

| Reference | Nội dung chính |
|---|---|
| `kb/bank/frameworks/bank-industry-master-reference.md` | Template format chuẩn KB |
| `agents/Sector_Tourism/knowledge.md` | Source gốc bootstrap |
