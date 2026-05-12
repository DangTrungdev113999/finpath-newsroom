---
category: frameworks
title: "Transport-Industry-Master-Reference"
last_updated: 2026-05-12
---

Master reference cho Master Transport — mental model 6 lớp phân tích ngành vận tải VN. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **GMD · HAH · VSC · VOS · PVT · ACV · VJC · HVN · SCS · PHP · SGP**.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Transport/knowledge.md + web research. 6 lớp đầy đủ. |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Phân loại phân khúc

| Phân khúc | Mã tiêu biểu | Đặc thù | Độ biến động |
|---|---|---|---|
| **Cảng biển** | GMD, VSC, PHP, SGP | Doanh thu ổn định, phụ thuộc xuất nhập khẩu, tài sản cố định lớn | Thấp |
| **Vận tải biển** | VOS, HAH | Phụ thuộc cước (BDI, SCFI), biến động cực mạnh theo chu kỳ | Rất cao |
| **Vận tải dầu khí** | PVT | Phụ thuộc sản lượng khai thác + cước thuê tàu | Trung bình |
| **Sân bay** | ACV | "Toll gate" — thu phí mọi hãng bay, mọi hành khách. Độc quyền 22 sân bay | Thấp |
| **Hãng bay** | VJC, HVN | Chi phí cố định cao, doanh thu biến động. Rủi ro nhất ngành | Rất cao |
| **Cargo hàng không** | SCS | Vận chuyển hàng hóa đường không, hưởng lợi thương mại điện tử | Trung bình |
| **Logistics** | GMD, TMS, STG | Biên lợi nhuận thấp, cạnh tranh cao, phụ thuộc thương mại điện tử + xuất nhập khẩu | Trung bình |
| **Vận tải đường bộ** | STG, doanh nghiệp nhỏ | Phân mảnh, biên mỏng nhất | Cao |
| **Khu công nghiệp & Kho bãi** | GMD, SLP | Ổn định, hưởng lợi thương mại điện tử + vốn đầu tư trực tiếp nước ngoài | Thấp |

## 1.2 Chuỗi giá trị vận tải

```
XUẤT KHẨU: Nhà máy → Vận tải bộ (STG) → Cảng (GMD/PHP) → Tàu (VOS/HAH) → Cảng nước ngoài
NHẬP KHẨU: Cảng nước ngoài → Tàu → Cảng VN → Kho bãi → Vận tải bộ → Nhà máy/Bán lẻ
HÀNG KHÔNG: Hành khách/Hàng hóa → Sân bay (ACV) → Hãng bay (VJC/HVN) → Sân bay đích
THƯƠNG MẠI ĐIỆN TỬ: Đặt hàng → Kho phân phối → Giao hàng chặng cuối
```

## 1.3 Luật chơi ngành

- **Xuất nhập khẩu**: Quyết định số 1 cho cảng + logistics. Xuất nhập khẩu tăng → sản lượng tăng
- **Cước vận tải**: BDI/SCFI (biển), giá vé + phụ phí nhiên liệu (hàng không). Cước cao → lãi lớn, cước thấp → lỗ
- **Nhiên liệu**: Chiếm 25-40% chi phí (hàng không ~30%, vận tải biển ~25%). Giá dầu tăng → ép biên lợi nhuận
- **Vốn đầu tư trực tiếp nước ngoài + Thương mại điện tử**: Vốn ngoại → nhà máy mới → xuất nhập khẩu tăng. Thương mại điện tử → kho bãi + giao hàng chặng cuối tăng
- **Chính phủ**: ACV độc quyền 22 sân bay. Quy hoạch cảng nước sâu (Cái Mép, Lạch Huyện, Nam Đình Vũ)

## 1.4 Đặc thù thị trường Việt Nam

- **Xuất khẩu/GDP ~90%** (top thế giới) → Xuất nhập khẩu quyết định cảng + logistics
- **Cảng chuyển dịch**: Cảng nội thành (TP.HCM, Hải Phòng cũ) → di dời. Cảng nước sâu (Cái Mép, Lạch Huyện) → tăng mạnh. GMD (Gemalink) hưởng lợi nhất
- **ACV = "Toll Gate"**: Thu phí mọi hãng bay, mọi hành khách. Không cạnh tranh, không rủi ro cước
- **Hãng bay = Rủi ro nhất**: Chi phí cố định cao, doanh thu biến động. Giá dầu + tỷ giá + cạnh tranh + dịch bệnh
- **Sản lượng 2025**: ~1,17 tỷ tấn hàng qua cảng biển (+12% so cùng kỳ), ~34,36 triệu TEU container (+11%)
- **Đội tàu VN**: 1.434 tàu, tổng ~9,4 triệu DWT (73 tàu đăng ký mới năm 2025)

## 1.5 Mùa vụ

| Quý | Cảng biển | Hàng không | Logistics |
|---|---|---|---|
| Q1 | Trung bình (sau Tết xuất khẩu chậm) | Cao (Tết du lịch) | Trung bình |
| Q2 | Tăng dần | **Thấp nhất** | Tăng dần |
| Q3 | **Cao (mùa xuất khẩu)** | Cao (hè) | Cao |
| Q4 | **Cao nhất (Giáng sinh)** | Cao (Noel) | Cao nhất |

*Cảng đỉnh Q3-Q4 (mùa xuất khẩu Giáng sinh). Hàng không đỉnh Q1 (Tết) + Q3 (hè).*

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics quan trọng

### Tier 1 — Thị trường phản ứng ngay

| Metric | Áp dụng | Benchmark |
|---|---|---|
| Sản lượng TEU | Cảng (GMD, VSC, PHP, HAH) | So cùng kỳ + tổng ngành; TEU tăng = xuất nhập khẩu tốt |
| Lượng hành khách | ACV, VJC, HVN | So cùng kỳ + so 2019 (pre-COVID); quốc tế vs nội địa |
| Cước biển (BDI/SCFI) | VOS, HAH, PVT | BDI >2.000 = thuận lợi; SCFI theo tuyến cụ thể |
| Hệ số sử dụng ghế (Load factor) | VJC, HVN | Tốt: >85%, trung bình: 80-85%, xấu: <75% |
| Giá nhiên liệu | VJC, HVN, VOS | Jet fuel/Bunker fuel; chiếm 25-30% chi phí |
| Xuất nhập khẩu VN | Cảng + Logistics | Số liệu Tổng cục Hải quan hàng tháng |

### Tier 2 — Phản ứng chậm (1-3 quý)

| Metric | Áp dụng | Benchmark |
|---|---|---|
| Doanh thu trên mỗi hành khách-km (Yield) | VJC, HVN | Tăng → giá vé/cơ cấu tốt hơn |
| Giá thuê kho | GMD, SLP | Tăng → cầu cao |
| Tỷ lệ lấp đầy kho | GMD, SLP | >90% = tốt, <70% = dư cung |
| Chi phí thuê tàu/máy bay | VJC, VOS | Đắt → ép biên lợi nhuận |
| Tỷ giá USD/VND | Cảng, hàng không | Doanh thu USD; USD tăng → doanh thu VND tăng (cảng), chi phí tăng (hãng bay) |

### Tier 3 — Dài hạn

| Metric | Ý nghĩa |
|---|---|
| Công suất cảng mới | Cung tăng → ép giá hoặc tăng doanh thu |
| Đội tàu/máy bay | Mở rộng → doanh thu + chi phí tăng |
| Vốn đầu tư trực tiếp nước ngoài vào VN | Nhà máy mới → xuất nhập khẩu tăng cấu trúc |
| Terminal mới (Long Thành, Tân Sơn Nhất T3) | ACV hưởng lợi dài hạn |
| Nam Đình Vũ giai đoạn 3 | GMD công suất +800.000 TEU (cuối 2025) |

## 2.2 Đọc số theo phân khúc

### Cảng biển (GMD, VSC, PHP, HAH)

**Quan trọng**: Sản lượng TEU + Giá xếp dỡ

Checklist:
- TEU so cùng kỳ, so tổng ngành
- Giá xếp dỡ tăng/giảm
- Tỷ lệ lấp đầy (>80% = tốt)
- Cảng nước sâu vs nội thành (nước sâu đang chiếm thị phần)
- Xuất nhập khẩu VN trend
- Vốn đầu tư trực tiếp nước ngoài cam kết mới

**GMD đặc biệt**: Tách doanh thu cảng / logistics / kho. Gemalink (Cái Mép) = động lực tăng trưởng mạnh. Nam Đình Vũ giai đoạn 3 công suất ~800.000 TEU vận hành cuối 2025 → tổng công suất Nam Đình Vũ vượt 2 triệu TEU (+60%).

### Sân bay (ACV)

**"Toll Gate"** — thu phí mọi hãng, mọi hành khách

Checklist:
- Lượng hành khách (quốc tế + nội địa) so cùng kỳ và so 2019
- Sản lượng hàng hóa (cargo)
- Phí dịch vụ trend
- Công suất sử dụng các sân bay
- Tiến độ Long Thành

**KHÔNG bị ảnh hưởng**: Giá dầu, cạnh tranh hãng bay, giá vé → Chỉ phụ thuộc LƯỢNG hành khách

### Hãng bay (VJC, HVN)

**Quan trọng**: Hệ số sử dụng ghế × Doanh thu trên hành khách − Chi phí (nhiên liệu + thuê máy bay)

Checklist:
- Hệ số sử dụng ghế (>85% = tốt, <75% = xấu)
- Doanh thu trên hành khách-km (yield) trend
- Nhiên liệu (~30% chi phí) trend
- Tỷ giá (chi phí thuê máy bay + nhiên liệu bằng USD)
- Đội bay mở rộng/thu hẹp
- Đường bay mới
- Doanh thu phụ trợ (hành lý, đồ ăn)

**RỦI RO NHẤT**: Chi phí cố định cao, doanh thu biến động. Dịch bệnh/giá dầu tăng → lỗ khủng

### Vận tải biển (VOS, HAH, PVT)

**Quan trọng**: Cước × Sản lượng − Nhiên liệu

Checklist:
- Cước (BDI/SCFI) trend
- Sản lượng vận chuyển
- Giá bunker fuel
- Tuổi đội tàu (tàu mới hiệu quả hơn)
- Hợp đồng thuê dài hạn vs spot

**BIẾN ĐỘNG CỰC MẠNH**: 2021 cước tăng 5-10 lần → lãi kỷ lục. 2023 cước giảm → lợi nhuận giảm 80%.

**HAH đặc biệt**: Đang trẻ hóa đội tàu (nhận thêm tàu đóng mới 2024-2025), cải thiện hiệu quả khai thác.

## 2.3 Bẫy phổ biến

| Bẫy | Thực tế | Cách kiểm tra |
|---|---|---|
| "GMD doanh thu tăng 25%" | Có thể Gemalink mới (base thấp) | Tách TEU cảng cũ vs cảng mới |
| "VJC hệ số sử dụng ghế 90%" | Doanh thu trên hành khách có thể thấp (giảm giá vé) | Kiểm tra yield tăng/giảm |
| "VOS lãi kỷ lục" | Cước đột biến do gián đoạn, KHÔNG bền | Cước có bền? Gián đoạn chuỗi cung ứng còn không? |
| "ACV lợi nhuận tăng 40%" | Base COVID thấp | So với 2019 mới chính xác |
| "Xuất nhập khẩu tăng 15%" | Có thể tăng giá, không tăng lượng | Kiểm tra sản lượng (tấn, TEU) |
| "BDI tăng 50%" | BDI cho hàng rời, SCFI cho container — khác nhau | Xác định đúng chỉ số theo loại tàu |

## 2.4 Checklist BCTC vận tải (7 câu hỏi)

1. Sản lượng (TEU/hành khách/tấn) — so cùng kỳ + so 2019?
2. Giá cước/phí — bền vững hay đột biến?
3. Chi phí nhiên liệu — chiếm % chi phí, xu hướng giá dầu?
4. Tỷ giá USD/VND — doanh thu USD hay chi phí USD?
5. Công suất mới — cảng/terminal/tàu/máy bay bao giờ vận hành?
6. Xuất nhập khẩu VN — tăng trưởng, vốn đầu tư nước ngoài mới?
7. Yếu tố đặc biệt — gián đoạn chuỗi cung ứng, dịch bệnh, đường bay mới, thuế quan mới?

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Chu kỳ theo phân khúc

| Phân khúc | Đặc tính chu kỳ | Beta |
|---|---|---|
| **Cảng biển (GMD, VSC, PHP)** | Ổn định nhất, theo xuất nhập khẩu dài hạn | Thấp |
| **Sân bay (ACV)** | Ổn định, phục hồi theo du lịch, Long Thành = xúc tác | Thấp |
| **Hãng bay (VJC, HVN)** | Chu kỳ mạnh nhất, bùng nổ/sụp đổ cực đoan | **Rất cao** |
| **Vận tải biển (VOS, HAH)** | Bùng nổ-sụp đổ cực đoan (2021 cước 5-10x, 2023 giảm 80%) | **Rất cao** |
| **Logistics (TMS, STG)** | Theo xuất nhập khẩu + thương mại điện tử | Trung bình |

## 3.2 Chu kỳ hãng bay (4 giai đoạn)

| Giai đoạn | Đặc trưng | Phản ứng giá cổ phiếu |
|---|---|---|
| **Đáy** | Dịch bệnh/suy thoái → hành khách giảm, lỗ lớn | Giá cổ phiếu tăng TRƯỚC khi hành khách hồi phục |
| **Hồi phục** | Hành khách tăng, giá vé tăng, lợi nhuận dương | **Giá cổ phiếu TĂNG MẠNH NHẤT** |
| **Tăng trưởng** | Hành khách ổn định, mở rộng đội bay | Giá cổ phiếu tăng chậm |
| **Đỉnh → Suy giảm** | Cạnh tranh tăng, giá dầu tăng, hệ số sử dụng ghế giảm | Giá cổ phiếu giảm dù lợi nhuận còn tốt |

## 3.3 Chu kỳ cước biển (VOS, HAH)

| Giai đoạn | Đặc trưng | Chiến lược |
|---|---|---|
| **Bình thường** | Cước ổn định, lợi nhuận mỏng | Hold hoặc tránh |
| **Gián đoạn** | Đứt gãy chuỗi cung ứng → cước tăng 5-10 lần → lợi nhuận bùng nổ | Mua khi gián đoạn mới bắt đầu |
| **Bình thường lại** | Chuỗi hồi phục → cước giảm → lợi nhuận giảm 80% | Bán khi cước bắt đầu giảm |

**VOS = "EVENT-DRIVEN"** — mua khi có sự kiện gián đoạn (Biển Đỏ, Suez), bán khi cước giảm. KHÔNG đầu tư dài hạn.

## 3.4 Tín hiệu sớm

### Sắp tốt
- **Cảng + Logistics**: Xuất nhập khẩu tăng, vốn nước ngoài tăng, TEU tăng, cảng mới vận hành
- **Hãng bay**: Hành khách tăng, giá dầu giảm, visa nới lỏng, hệ số sử dụng ghế tăng
- **Vận tải biển**: Gián đoạn chuỗi cung ứng mới (chiến tranh, thiên tai, đình công)

### Đỉnh/suy giảm
- Xuất nhập khẩu giảm (thương chiến, suy thoái toàn cầu)
- Giá dầu tăng mạnh (>30%)
- Cung tàu/máy bay > cầu
- Cước biển đã tăng 3-5 lần (sắp đỉnh)
- Dịch bệnh mới

---

# LỚP 4: VĨ MÔ

## 4.1 Yếu tố vĩ mô tác động

| Yếu tố | Tác động | Ai bị ảnh hưởng nhiều nhất |
|---|---|---|
| **Xuất nhập khẩu VN** | Số 1 cho cảng + logistics | GMD, PHP, VSC, STG, HAH |
| **Du lịch** | Số 1 cho hàng không | ACV, VJC, HVN |
| **Giá dầu** | Chi phí số 1 hãng bay + tàu | VJC, HVN, VOS, PVT |
| **Vốn đầu tư nước ngoài** | Nhà máy mới → xuất nhập khẩu cấu trúc | Cảng, logistics |
| **USD/VND** | Doanh thu USD | GMD hưởng lợi; VJC chi phí tăng |
| **Chuỗi cung ứng** | Gián đoạn → cước tăng | VOS, HAH (ngắn hạn) |
| **GDP Mỹ + EU + Trung Quốc** | Nhu cầu hàng VN | Cảng, logistics |
| **Thương mại điện tử** | Kho bãi + giao hàng chặng cuối | GMD, SLP, SCS |
| **Thuế quan (Trump 2.0)** | Rủi ro xuất khẩu sang Mỹ | Toàn ngành |

## 4.2 Ma trận ảnh hưởng

| Yếu tố | Cảng | Sân bay | Hãng bay | Vận tải biển | Logistics |
|---|---|---|---|---|---|
| Xuất nhập khẩu tăng | +++ | + | + | + | ++ |
| Du lịch tăng | + | +++ | +++ | + | + |
| Giá dầu tăng | = | = | --- | -- | - |
| Vốn nước ngoài tăng | ++ | + | + | + | ++ |
| USD tăng | + | = | - | + | = |
| Gián đoạn chuỗi | + | = | = | +++ | + |
| Thương mại điện tử tăng | + | = | = | = | +++ |

## 4.3 Động lực tăng trưởng

**Cấu trúc (dài hạn)**:
- VN = trung tâm sản xuất mới (China+1) → xuất nhập khẩu tăng
- Vốn nước ngoài tăng (Samsung, Intel, Apple chuyển dây chuyền) → cảng, logistics, cargo
- Du lịch VN tăng 10-15%/năm → ACV, VJC
- Sân bay Long Thành → ACV công suất tăng đột biến
- Cái Mép + Nam Đình Vũ → GMD đón tàu lớn hơn
- Thương mại điện tử → kho bãi + giao hàng chặng cuối

**Chu kỳ (ngắn hạn)**: Giá dầu giảm, đơn xuất khẩu mới, gián đoạn chuỗi cung ứng, visa nới lỏng

## 4.4 Rủi ro

| Rủi ro | Ai bị ảnh hưởng |
|---|---|
| Suy thoái toàn cầu → xuất nhập khẩu giảm | Cảng, logistics, vận tải biển |
| Thương chiến (thuế quan Trump 2.0) | Toàn ngành, đặc biệt xuất khẩu sang Mỹ |
| Giá dầu tăng mạnh (>30%) | VJC, HVN, VOS |
| Dịch bệnh mới | Hàng không |
| Cung > Cầu (tàu/máy bay mới quá nhiều) | Ép giá, giảm hệ số sử dụng ghế |
| Vốn nước ngoài chuyển sang Ấn Độ/Indonesia | Cảng, logistics dài hạn |
| VJC/HVN vay USD + USD tăng | Lỗ tỷ giá |
| Công suất cảng tăng nhanh hơn xuất nhập khẩu | Ép giá xếp dỡ |

## 4.5 Câu hỏi vĩ mô quan trọng

1. Xuất nhập khẩu VN tăng/giảm? Đơn hàng mới từ đâu?
2. Hành khách sân bay tăng/giảm? Quốc tế vs nội địa?
3. Giá dầu xu hướng thế nào?
4. Vốn nước ngoài cam kết mới bao nhiêu?
5. Cước biển bình thường hay đang đột biến?
6. Gián đoạn chuỗi cung ứng? (Biển Đỏ, Suez, đình công cảng)
7. Thuế quan mới từ Mỹ/EU?

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 Phương pháp định giá theo phân khúc

| Phân khúc | Phương pháp chính | Lý do |
|---|---|---|
| **Cảng (GMD, VSC, PHP)** | EV/EBITDA + P/E | Doanh thu ổn định, EBITDA phản ánh khấu hao lớn |
| **Sân bay (ACV)** | P/E + EV/Hành khách | Độc quyền, tính giá trị trên mỗi hành khách |
| **Hãng bay (VJC, HVN)** | EV/EBITDA + P/E normalized | Lợi nhuận biến động, cần normalize qua chu kỳ |
| **Vận tải biển (VOS, HAH)** | P/E normalized hoặc P/B | Bùng nổ-sụp đổ, P/E đỉnh = bẫy |
| **Logistics (TMS, STG)** | P/E | Tương đối ổn định |

## 5.2 ACV — Định giá premium

- **EV/Hành khách**: Benchmark quốc tế 100-200 USD/hành khách. ACV ~80-120 USD/hành khách → còn rẻ so khu vực
- **P/E**: Pre-COVID 25-35 lần (premium). Post-COVID 20-30 lần
- **Xứng premium**: Độc quyền + tăng trưởng 10-15%/năm + Long Thành + biên lợi nhuận 40-50%

## 5.3 Hãng bay — P/E phải normalize

- **VJC**: Normalized P/E 12-18 lần (dùng lợi nhuận trung bình 5 năm hoặc loại COVID)
- **HVN**: Khó định giá (nợ lớn, tái cơ cấu liên tục)
- P/E thấp có thể = đỉnh chu kỳ (hệ số sử dụng ghế cao + giá dầu rẻ)

## 5.4 VOS/HAH — Bẫy P/E đỉnh cước

- **2021**: Cước kỷ lục, lợi nhuận trên cổ phiếu 5.000 đồng, P/E 5 lần → trông rẻ
- **2023**: Cước bình thường, lợi nhuận trên cổ phiếu 500 đồng, P/E 50 lần → thực đắt
- **Dùng P/B hoặc P/E normalized** (lợi nhuận trung bình 5-7 năm)

## 5.5 Bẫy định giá

| Bẫy | Thực tế |
|---|---|
| "ACV P/E 30 lần = đắt" | Độc quyền + tăng 15%/năm + Long Thành = xứng premium |
| "VOS P/E 5 lần = rẻ" | Cước đỉnh sẽ giảm → lợi nhuận giảm 80% |
| "VJC P/E 8 lần = rẻ" | Giá dầu thấp, nếu giá dầu tăng → lợi nhuận giảm mạnh |
| "GMD P/E < ACV" | Không so được trực tiếp, ACV độc quyền còn GMD cạnh tranh |

---

# LỚP 6: TƯ VẤN

## 6.1 Phân biệt rủi ro

| Tình huống | Loại | Phản ứng |
|---|---|---|
| Xuất nhập khẩu giảm 1 tháng | Biến động ngắn hạn | Theo dõi |
| Xuất nhập khẩu giảm 3 tháng liên tiếp | Xu hướng | Xem lại cảng + logistics |
| Giá dầu tăng 10% | Biến động | Hãng bay ép biên nhẹ |
| Giá dầu tăng 30% | Nghiêm trọng | Hãng bay lỗ, cân nhắc thoát |
| VOS lãi kỷ lục | Cước đột biến | ĐỪNG đuổi theo giá |
| ACV hành khách giảm 1 quý | Mùa vụ bình thường | Không lo |
| Dịch bệnh mới | Khẩn cấp | Hàng không sụp, cảng ít ảnh hưởng |

## 6.2 Theo profile nhà đầu tư

### Dài hạn (>1 năm)
- **Focus**: Xuất nhập khẩu cấu trúc, vốn nước ngoài, hạ tầng mới
- **Ưu tiên**: ACV (độc quyền, Long Thành), GMD (cảng nước sâu + logistics)
- **Tránh**: VOS, HVN, doanh nghiệp logistics nhỏ

### Trung hạn (3-12 tháng)
- **Focus**: Chu kỳ xuất nhập khẩu, giá dầu, du lịch
- **Vào GMD**: Xuất nhập khẩu hồi phục + vốn nước ngoài tăng
- **Vào VJC**: Giá dầu giảm + du lịch tăng + hệ số sử dụng ghế hồi
- **Thoát VJC**: Giá dầu tăng + cạnh tranh + hệ số sử dụng ghế giảm

### Ngắn hạn (<3 tháng)
- **Focus**: Mùa xuất khẩu đỉnh (Q3-Q4), giá dầu, gián đoạn chuỗi
- **VOS**: Chỉ khi có sự kiện gián đoạn → bán khi cước giảm
- **VJC**: Mua trước mùa hè (Q2 → Q3)
- **Cảng**: Q3-Q4 sản lượng cao nhất

## 6.3 Khi VÀO (cần 2-3 tín hiệu)

**Cảng + Logistics**: Xuất nhập khẩu tăng, vốn nước ngoài tăng, cảng mới vận hành, USD ổn định/tăng, thương mại điện tử tăng

**Hãng bay**: Hành khách tăng, giá dầu giảm/ổn định, hệ số sử dụng ghế >85%, visa nới lỏng, post-dịch

**Vận tải biển**: Gián đoạn chuỗi cung ứng mới xuất hiện, cước BDI/SCFI bắt đầu tăng

## 6.4 Khi THOÁT (cần 2-3 tín hiệu)

**Cảng + Logistics**: Xuất nhập khẩu giảm 3 tháng, suy thoái Mỹ/EU/Trung Quốc, thương chiến, cung > cầu

**Hãng bay**: Giá dầu tăng >30%, hệ số sử dụng ghế <80%, doanh thu trên hành khách giảm, dịch bệnh mới, người trong công ty bán

**Vận tải biển**: Cước đã tăng 3-5 lần, gián đoạn chuỗi sắp kết thúc, cước bắt đầu giảm

## 6.5 Ngôn ngữ cho nhà đầu tư mới

| Thuật ngữ | Dịch dễ hiểu |
|---|---|
| TEU tăng | Số container qua cảng tăng |
| Hệ số sử dụng ghế 90% | 90% ghế máy bay được lấp đầy |
| Yield tăng | Giá vé trung bình mỗi hành khách tăng |
| Giá dầu ép biên | Xăng dầu tăng → lời ít hơn |
| BDI tăng | Cước vận tải biển hàng rời tăng |
| SCFI tăng | Cước vận tải container từ Thượng Hải tăng |
| ACV = toll gate | ACV thu phí mọi hãng bay, mọi hành khách đi qua |
| Vốn nước ngoài tăng | Nhiều công ty nước ngoài mở nhà máy tại VN |
| Gián đoạn chuỗi | Đường vận chuyển tắc → cước tăng vọt |
| China+1 | Công ty chuyển nhà máy từ Trung Quốc sang VN |
| Giao hàng chặng cuối | Giao hàng từ kho đến tay người mua |
| Doanh thu phụ trợ | Doanh thu từ hành lý, đồ ăn (ngoài vé máy bay) |
| Bunker fuel | Nhiên liệu cho tàu biển |

---

# PHỤ LỤC

## A. Severity (mức độ nghiêm trọng)

**Green (tích cực)**:
- Cảng: TEU tăng + giá xếp dỡ ổn/tăng
- ACV: Hành khách tăng + biên lợi nhuận ổn định
- VJC: Hệ số sử dụng ghế >85% + doanh thu trên hành khách tăng + giá dầu ổn
- Logistics: Xuất nhập khẩu tăng + tỷ lệ lấp đầy kho >90%

**Yellow (theo dõi)**:
- Sản lượng ngang cùng kỳ
- Hệ số sử dụng ghế tốt nhưng doanh thu trên hành khách giảm
- Cước tăng đột biến (sẽ giảm)
- Giá dầu tăng nhẹ 10-15%

**Red (tiêu cực)**:
- Xuất nhập khẩu giảm mạnh
- Hành khách giảm (dịch bệnh/suy thoái)
- Giá dầu tăng >30%
- Cước giảm mạnh sau đỉnh
- Lợi nhuận giảm/lỗ

## B. Câu mẫu

**GMD tăng**: "Container qua GMD tăng {X}% — xuất nhập khẩu tốt + Gemalink đón nhiều tàu lớn hơn."

**VJC lãi nhờ giá dầu**: "VJC lãi tăng {X}% nhờ nhiên liệu bay giảm {Y}%. Nếu giá dầu tăng trở lại, khoản tiết kiệm này sẽ mất."

**VOS cước đột biến**: "VOS lãi gấp {X} lần nhờ gián đoạn Biển Đỏ. Khi chuỗi cung ứng hồi phục, cước sẽ giảm, lợi nhuận quý sau giảm mạnh."

**ACV vượt 2019**: "Hành khách qua ACV đạt {X} triệu, vượt trước dịch. ACV thu phí mọi người bay."

**Xuất nhập khẩu giảm**: "Xuất nhập khẩu giảm {X}% do kinh tế Mỹ/EU chậm. Container qua {ticker} giảm {Y}%, doanh thu giảm {Z}%."

**Thuế quan mới**: "Thuế quan Trump 2.0 có thể ảnh hưởng {X}% kim ngạch xuất khẩu VN sang Mỹ — theo dõi sát đơn hàng Q3-Q4."

## C. Quy tắc agent

1. Cảng ≠ Sân bay ≠ Hãng bay ≠ Vận tải biển — ĐỪNG gộp chung
2. ACV = toll gate — KHÁC HOÀN TOÀN hãng bay
3. KHÔNG đuổi VOS khi cước đỉnh — P/E thấp = bẫy
4. Hãng bay biến động CỰC CAO — cảnh báo nhà đầu tư mới
5. Cảng + Logistics → PHẢI kiểm tra xuất nhập khẩu trước
6. Hãng bay → PHẢI kiểm tra giá dầu trước
7. So sản lượng (TEU, hành khách, tấn) — KHÔNG chỉ doanh thu
8. Post-COVID: so với 2019 mới chính xác
9. KHÔNG dùng thuật ngữ tiếng Anh — PHẢI dịch sang tiếng Việt
10. Thiếu dữ liệu → nói thiếu, KHÔNG bịa số

---

## Hướng dẫn tra dữ liệu thời gian thực (cho Master Transport)

KB master này chỉ cung cấp framework + threshold + range historical. Khi viết bài quý cụ thể, Master phải:

1. **Query KB framework** (file này) — static guidance
2. **Finpath API** cho data realtime:
   - `get_income_statement(ticker)` + `get_balance_sheet(ticker)` — BCTC quý
   - `get_shareholders(ticker)` + `get_events(ticker)` + `get_news(ticker)` — sở hữu + ĐHĐCĐ + tin tức
3. **Web search** cho data Finpath API không có:
   - Sản lượng TEU/hành khách cập nhật
   - Cước BDI/SCFI realtime
   - Giá dầu Brent/WTI
   - Xuất nhập khẩu VN hàng tháng (Tổng cục Hải quan)
   - Vốn nước ngoài cam kết mới
   - Tiến độ cảng/sân bay mới

---

## Cross-link (dự kiến)

| Deep dive | Nội dung chính |
|---|---|
| `transport-freight-cycle.md` | Chu kỳ cước BDI/SCFI; giai đoạn gián đoạn chuỗi cung ứng |
| `transport-aviation-cycle.md` | Chu kỳ hàng không; giá dầu vs hệ số sử dụng ghế vs doanh thu trên hành khách |
| `transport-port-capacity.md` | Công suất cảng mới (Gemalink, Nam Đình Vũ, Lạch Huyện, Long Thành) |

---

## Phần suy luận (cần verify)

Các điểm dưới đây rút từ framework + data historical — không có nguồn cite trực tiếp, cần verify khi đưa vào bài cụ thể:

- **"Sản lượng 2025 ~1,17 tỷ tấn, ~34,36 triệu TEU"** — từ web search báo VN. Verify với Cục Hàng hải VN hoặc Tổng cục Hải quan.
- **"BDI >2.000 = thuận lợi"** — heuristic tổng hợp, BDI biến động mạnh theo thời điểm.
- **"ACV EV/Hành khách 80-120 USD"** — range estimate từ phân tích sector, cần verify với data định giá realtime.
- **"Hải Phòng phấn đấu 122 triệu tấn 2026"** — từ Thời báo Tài chính Việt Nam.
- **"Nam Đình Vũ giai đoạn 3 công suất ~800.000 TEU cuối 2025"** — từ báo cáo ngành GTJA.
- **"2021 cước tăng 5-10 lần"** — historical fact, nhưng số chính xác vary theo tuyến.
