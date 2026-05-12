---
category: frameworks
title: "Aviation-Industry-Master-Reference"
last_updated: 2026-05-12
---
Master reference cho Master Aviation — mental model 6 lớp phân tích ngành hàng không VN. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **VJC · HVN · ACV · SCS · NCT · SGN**. Ba deep dive (Operating-Leverage, Fuel-Sensitivity, Cargo-Economics) mang chi tiết cơ chế và số liệu lịch sử; master reference này gom 6 lớp vào một chỗ để orient nhanh.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Aviation/knowledge.md + web search enrichment. Thêm data 2025-2026 (83.5 triệu HK, Long Thành 06/2026). |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Hai mô hình kinh doanh — KHÔNG GỘP CHUNG

| Loại | Đặc điểm | Mã | Driver chính |
|---|---|---|---|
| **HÃNG BAY** | Vận chuyển HK + hàng hóa, chi phí cố định cao, doanh thu biến động, rủi ro cao | VJC, HVN | Giá nhiên liệu, tỷ lệ lấp đầy ghế, tỷ giá USD |
| **SÂN BAY/DỊCH VỤ** | Thu phí mọi hãng/HK/hàng hóa, không bay, không lo giá dầu, ổn định | ACV, SCS, NCT, SGN | Lượng hành khách, sản lượng cargo |

> **Decision rule**: KHÔNG BAO GIỜ đánh giá chung ACV với VJC/HVN — mô hình hoàn toàn khác.

## 1.2 Doanh nghiệp chính (Universe)

| Mã | Tên | Sàn | Mô hình | Đặc trưng cấu trúc |
|---|---|---|---|---|
| **ACV** | Tổng công ty Cảng hàng không Việt Nam | UPCOM | Sân bay độc quyền | 22 sân bay, biên 40-50%, Long Thành catalyst lớn nhất |
| **VJC** | Vietjet Air | HOSE | Hãng bay giá rẻ (LCC) | Thu thêm phụ trội 25-30% doanh thu, đội bay trẻ 4-5 tuổi, chi phí trên ghế-km thấp hơn HVN 20-30% |
| **HVN** | Vietnam Airlines | HOSE | Hãng bay truyền thống (FSC) | Nợ/vốn chủ >5x, nhà nước sở hữu ~86%, được hỗ trợ 12.000 tỷ giai đoạn COVID |
| **SCS** | Saigon Cargo Service | HOSE | Nhà ga hàng hóa | Biên 30-40%, phụ thuộc xuất nhập khẩu, hưởng lợi Samsung/Apple |
| **NCT** | Noibai Cargo Terminal | HNX | Nhà ga hàng hóa | Tương tự SCS, phục vụ sân bay Nội Bài |
| **SGN** | Saigon Ground Services | HOSE | Dịch vụ mặt đất | Phụ thuộc số chuyến bay, check-in, hành lý |

## 1.3 Chuỗi giá trị

```
HK mua vé → ACV thu phí phục vụ (100-200k/người) → SGN check-in/hành lý 
→ Hãng bay thu vé + phụ trội → Hãng trả phí hạ cánh + nhiên liệu + thuê máy bay 
→ ACV sân bay đến thu phí

Cargo: Shipper → SCS/NCT nhà ga hàng hóa → Hãng bay → ACV thu phí
```

**ACV thu phí MỌI BƯỚC** — vị thế độc quyền tự nhiên.

## 1.4 Yếu tố quyết định lợi nhuận

| Yếu tố | Tác động hãng bay | Tác động sân bay |
|---|---|---|
| **Lượng hành khách** | +++ (driver số 1) | +++ (driver số 1) |
| **Giá nhiên liệu Jet A1** | --- (25-35% chi phí) | Không ảnh hưởng |
| **Tỷ giá USD/VND** | -- (thuê máy bay + nhiên liệu bằng USD) | + (doanh thu quốc tế quy VND tăng) |
| **Cạnh tranh** | -- (áp lực giá vé) | Độc quyền |
| **Chính sách visa** | ++ | ++ |
| **Dịch bệnh** | --- (doanh thu về 0) | --- |

## 1.5 Đặc thù thị trường Việt Nam

**Đòn bẩy hoạt động cực cao (hãng bay)**:
- Tỷ lệ lấp đầy 85% → LÃI
- Tỷ lệ lấp đầy 70% → LỖ
- Chênh 15 điểm phần trăm = chênh lãi/lỗ

**VJC**: Giá rẻ + bán thêm phụ trội 25-30% doanh thu, đội bay trẻ → chi phí bảo trì thấp, chi phí trên ghế-km thấp hơn HVN 20-30%.

**HVN**: Nhà nước sở hữu ~86%, nợ cao, từng âm vốn chủ sở hữu, được cứu 12.000 tỷ giai đoạn COVID. Rủi ro tài chính RẤT CAO.

**ACV**: Độc quyền 22 sân bay, biên 40-50%, Long Thành giai đoạn 1 tăng công suất 25 triệu HK/năm.

## 1.6 Tính mùa vụ

| Thời điểm | HK nội địa | HK quốc tế | Hàng hóa |
|---|---|---|---|
| T1-T2 | **Cao (Tết)** | Cao | Trung bình |
| T7-T8 | **Cao nhất (hè)** | **Cao nhất** | **Cao** |
| T9-T10 | **Thấp nhất** | Giảm | Cao (xuất khẩu Giáng sinh) |
| T11-T12 | Tăng | Tăng | **Cao nhất** |

> **Quy tắc**: Q1 (Tết) + Q3 (hè) = đỉnh hành khách. Q3 cuối - Q4 đầu = đáy. Hàng hóa đỉnh Q3-Q4.

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics HÃNG BAY

### Tier 1 — Thị trường phản ứng ngay

| Metric | Giải thích | Ngưỡng tham chiếu |
|---|---|---|
| **Tỷ lệ lấp đầy (Load Factor)** | % ghế được lấp đầy = RPK/ASK | >85% tốt, 80-85% hòa vốn, <75% lỗ |
| **Ghế-km cung ứng (ASK)** | Tổng ghế × km = CUNG | So cùng kỳ |
| **Hành khách-km vận chuyển (RPK)** | Hành khách × km = CẦU | So cùng kỳ |
| **Doanh thu trên ghế-km (RASK)** | Doanh thu / ASK | Tăng → giá vé tốt |
| **Chi phí trên ghế-km (CASK)** | Chi phí / ASK | VJC < HVN 20-30% |
| **Giá nhiên liệu Jet A1** | 25-35% tổng chi phí hãng bay | Brent × 1.1-1.2 |

### Tier 2

| Metric | Ngưỡng tham chiếu |
|---|---|
| Phụ trội / tổng doanh thu | VJC: 25-30%, HVN: 10-15% |
| Tuổi đội bay trung bình | VJC: 4-5 tuổi, HVN: 6-8 tuổi |
| Nợ / vốn chủ sở hữu | VJC: 1-2x, HVN: >5x |
| Tỷ lệ lấp đầy hòa vốn | VJC: ~75%, HVN: ~78-80% |

## 2.2 Metrics SÂN BAY (ACV)

| Metric | Ngưỡng tham chiếu |
|---|---|
| Tổng hành khách | So cùng kỳ + so 2019 (trước COVID) |
| Tỷ trọng HK quốc tế / tổng | ~35-40% (quốc tế biên cao hơn) |
| Biên lợi nhuận | 40-50% |
| Tiến độ Long Thành | Catalyst lớn nhất, khai thương mại 06/2026 |

## 2.3 So sánh VJC vs HVN

| Metric | VJC | HVN |
|---|---|---|
| Mô hình | Giá rẻ + bán thêm | Truyền thống |
| Tỷ lệ lấp đầy | 85-90% | 80-85% |
| Chi phí trên ghế-km | Thấp hơn 20-30% | Cao hơn |
| Phụ trội / doanh thu | 25-30% | 10-15% |
| Nợ / vốn chủ | 1-2x | >5x |
| Thị phần nội địa | ~45% | ~35% |
| Rủi ro tài chính | Trung bình | **RẤT CAO** |

## 2.4 Hiểu đòn bẩy hoạt động

Ví dụ chuyến bay Hà Nội - TP.HCM 180 ghế:
- Chi phí cố định: ~300 triệu đồng
- Chi phí biến đổi: ~100.000đ/khách

| Tỷ lệ lấp đầy | Số khách | Kết quả |
|---|---|---|
| 70% | 126 | Lỗ ~124 triệu |
| 90% | 162 | Lãi ~8 triệu/chuyến |

> **Quy tắc**: Tỷ lệ lấp đầy +10 điểm phần trăm → lợi nhuận có thể +50-80%.

## 2.5 Bẫy phổ biến khi đọc số

| Bẫy | Cách kiểm tra |
|---|---|
| Doanh thu tăng 25% | Kiểm tra tỷ lệ lấp đầy + doanh thu trên ghế-km. Doanh thu tăng mà tỷ lệ lấp đầy giảm = cung thừa |
| HVN hết lỗ | Kiểm tra lợi nhuận từ hoạt động kinh doanh vs khoản bất thường (xóa nợ) |
| ACV lợi nhuận +40% | So với 2019, không chỉ so cùng kỳ |
| VJC tỷ lệ lấp đầy 90% | Kiểm tra doanh thu trên ghế-km — có thể giảm giá vé để lấp đầy |

## 2.6 Checklist khi đọc BCTC

**Hãng bay**: Tỷ lệ lấp đầy? ASK vs RPK? Doanh thu trên ghế-km? Chi phí trên ghế-km? Giá dầu? Tỷ giá USD? Phụ trội/HK? Nợ/vốn chủ? So 2019?

**Sân bay**: Tổng HK? Quốc tế vs nội địa? So 2019? Long Thành? Biên lợi nhuận?

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Nguyên tắc cốt lõi

- **Hãng bay**: Rủi ro nhất, chu kỳ mạnh nhất. Thuận lợi: lãi khủng. Khó khăn: lỗ nặng/phá sản.
- **ACV**: Ít chu kỳ nhất, chỉ bị ảnh hưởng bởi dịch bệnh + suy thoái nặng.
- Giá cổ phiếu chạy TRƯỚC khi lợi nhuận cải thiện.

## 3.2 Bốn giai đoạn chu kỳ hãng bay

| Giai đoạn | Đặc trưng | Giá cổ phiếu |
|---|---|---|
| **1. Đáy/Khủng hoảng** | Dịch/suy thoái, tỷ lệ lấp đầy sụp, lỗ nặng | -50% đến -70% |
| **2. Hồi phục** | HK quay lại, tỷ lệ lấp đầy hồi, lợi nhuận dương, **giá tăng mạnh nhất** | +100% đến +300% |
| **3. Tăng trưởng** | HK vượt trước khủng hoảng, mở đường bay mới | Tăng chậm |
| **4. Đỉnh → Suy giảm** | Cung > cầu, tỷ lệ lấp đầy giảm, doanh thu trên ghế-km giảm, cạnh tranh | Giảm dần |

## 3.3 Tín hiệu sớm

**Sắp hồi phục**: Dịch kiểm soát, dầu giảm, visa nới, đường bay quốc tế mở, tỷ lệ lấp đầy tăng từ đáy.

**Sắp gặp khó**: Dầu +30%, ASK > RPK (cung vượt cầu), doanh thu trên ghế-km giảm 2 quý, hãng mới gia nhập, USD tăng mạnh.

## 3.4 Case study: Chu kỳ COVID 2020-2025

- **2020**: Doanh thu ngành về gần 0, HVN lỗ nặng, VJC giảm mạnh.
- **2021-2022**: Nội địa phục hồi trước, quốc tế chậm hơn.
- **2023-2024**: Quốc tế bứt phá, tổng HK vượt 2019.
- **2025**: Kỷ lục mới 83.5 triệu HK (+10.7% so cùng kỳ).

---

# LỚP 4: HIỂU VĨ MÔ

## 4.1 Yếu tố vĩ mô tác động

| Yếu tố | Hãng bay | Sân bay/dịch vụ |
|---|---|---|
| Lượng hành khách | +++ | +++ |
| Giá dầu | --- (tăng = xấu) | Không ảnh hưởng |
| Tỷ giá USD | -- (tăng = xấu) | + (doanh thu quốc tế quy VND tăng) |
| Cạnh tranh | -- | Độc quyền |
| Visa nới | ++ | ++ |
| Dịch bệnh | --- | --- |

## 4.2 Giá dầu — Biến số số 1 cho hãng bay

| Giá dầu Brent (USD/thùng) | Biên lợi nhuận VJC | Nhận định |
|---|---|---|
| $60 | 8-10% | **LÃI TỐT** |
| $80 | 4-6% | Biên mỏng |
| $100 | 0-2% | Gần hòa vốn |
| $120+ | Âm | **LỖ** |

Mỗi $10 tăng → chi phí VJC +1.000-1.500 tỷ/năm. ACV không ảnh hưởng.

## 4.3 Động lực và rủi ro dài hạn

**Động lực**:
- Tầng lớp trung lưu tăng nhanh
- Việt Nam điểm đến hấp dẫn (visa miễn cho 30+ quốc gia)
- Long Thành giai đoạn 1: 25 triệu HK/năm, khai thương mại 06/2026
- Hàng không giá rẻ mở rộng quốc tế
- Hàng hóa tăng theo sản xuất công nghiệp (Samsung, Apple, Intel)

**Rủi ro**:
- Dịch bệnh mới (doanh thu → 0)
- Dầu +30%
- Cạnh tranh giá khốc liệt
- USD tăng mạnh
- HVN nợ không xử lý được → rủi ro hệ thống

## 4.4 Số liệu thị trường 2025-2026

| Chỉ tiêu | 2025 (thực hiện) | 2026 (dự báo) |
|---|---|---|
| Tổng hành khách | 83.5 triệu | ~95 triệu (+13.6%) |
| Hành khách quốc tế | 46.6 triệu | — |
| Hành khách nội địa | 36.9 triệu | — |
| Hàng hóa | — | ~1.6 triệu tấn (+9.3%) |

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 ACV — Định giá premium hợp lý

- **P/E**: 20-35x (xứng vì độc quyền, biên 40-50%, tăng trưởng 10-15%/năm)
- **EV/HK**: $80-120/HK → còn rẻ so với khu vực Đông Nam Á ($100-200/HK)
- Long Thành giai đoạn 1 → tăng HK 25 triệu/năm → EV/HK sẽ giảm về vùng hấp dẫn

## 5.2 VJC — Định giá chu kỳ

| Pha | P/E | Nhận định |
|---|---|---|
| Đáy (lỗ) | Âm/vô cực | **LÚC MUA** |
| Hồi phục | 15-25x | Giá tăng mạnh nhất |
| Đỉnh | 8-12x | **BẪY** (E đang cao nhất chu kỳ) |

- **EV/EBITDAR**: 6-10x. So sánh: AirAsia 6-8x, IndiGo 10-14x.

## 5.3 HVN — Khó định giá

Nợ/vốn chủ >5x, từng âm vốn chủ sở hữu → P/E, P/B vô nghĩa → **RỦI RO CAO, KHÔNG CHẮC CHẮN CAO**.

## 5.4 Bẫy định giá

- **Sai**: VJC P/E 10x = rẻ (thực tế: dầu rẻ + tỷ lệ lấp đầy đỉnh → E đang cao nhất)
- **Sai**: ACV P/E 30x = đắt (thực tế: độc quyền + Long Thành → xứng premium)
- **Đúng**: Mua VJC khi dầu đáy + tỷ lệ lấp đầy hồi + P/E "trông cao"
- **Đúng**: Mua ACV khi HK tăng + Long Thành tiến triển + P/E <25x

---

# LỚP 6: TƯ VẤN PHÂN LOẠI

## 6.1 Phân biệt loại rủi ro

| Tình huống | Loại | Phản ứng |
|---|---|---|
| Tỷ lệ lấp đầy giảm T9-10 | Mùa vụ | Bình thường |
| Dầu +10% | Biến động | Theo dõi |
| Dầu +30%+ | Nghiêm trọng | Cân nhắc thoát hãng bay |
| Dịch bệnh mới | KHẨN CẤP | Bán hãng bay NGAY |
| HVN xóa nợ | Tái cơ cấu | Lợi nhuận đẹp 1 lần, kinh doanh chưa chắc tốt |

## 6.2 Phân loại theo profile nhà đầu tư

| Profile | Trọng tâm | Ưu tiên |
|---|---|---|
| Dài hạn >1 năm | Độc quyền, Long Thành | ACV số 1, SCS. Tránh HVN |
| Trung hạn 3-12 tháng | Giá dầu + tỷ lệ lấp đầy + visa | VJC khi dầu giảm + tỷ lệ lấp đầy hồi |
| Ngắn hạn <3 tháng | Mùa du lịch, tin visa | VJC mua T4-5, bán T9. Beta cao |

## 6.3 Tín hiệu vào/thoát

**VÀO VJC (cần 2-3/6)**:
- Dầu đáy
- Tỷ lệ lấp đầy hồi
- Visa nới
- Sau dịch
- Doanh thu trên ghế-km ổn
- Trước mùa cao điểm

**THOÁT VJC (cần 2-3/6)**:
- Dầu +30%
- Tỷ lệ lấp đầy giảm 2 quý
- ASK > RPK (cung vượt cầu)
- Doanh thu trên ghế-km giảm
- Dịch mới
- USD +5%+

**VÀO ACV**: HK tăng, Long Thành tiến triển, P/E <25x, HK quốc tế hồi.

**THOÁT ACV**: Hiếm — chỉ khi dịch nghiêm trọng hoặc P/E >35x.

---

## Hướng dẫn tra dữ liệu thời gian thực (cho Master Aviation)

KB master này chỉ cung cấp framework + threshold + range historical. Khi viết bài quarter cụ thể, Master phải:

1. **Query KB framework** (file này + deep dive) — static guidance.
2. **Finpath API** cho data realtime:
   - `get_income_statement(ticker)` + `get_balance_sheet(ticker)` — BCTC quarter
   - `get_financial_ratios(ticker)` — P/E, P/B, ROE
   - `get_shareholders(ticker)` + `get_events(ticker)` + `get_news(ticker)` — sở hữu + sự kiện + tin
3. **Web_search** cho data Finpath API không có:
   - Số liệu vận hành (ASK, RPK, tỷ lệ lấp đầy, doanh thu trên ghế-km)
   - Giá dầu Brent/Jet A1 realtime
   - Tiến độ Long Thành
   - Thông tin visa, đường bay mới

---

## Cross-link

| Deep dive | Nội dung chính |
|---|---|
| [`aviation-operating-leverage.md`](./aviation-operating-leverage.md) | Đòn bẩy hoạt động, break-even tỷ lệ lấp đầy, VJC vs HVN |
| [`aviation-fuel-sensitivity.md`](./aviation-fuel-sensitivity.md) | Độ nhạy giá nhiên liệu, hedging, tác động biên lợi nhuận |
| [`aviation-cargo-economics.md`](./aviation-cargo-economics.md) | Kinh tế hàng hóa, SCS/NCT, mùa vụ xuất khẩu |

---

## Phụ lục: Thuật ngữ cho nhà đầu tư mới

| Thuật ngữ | Giải thích |
|---|---|
| Tỷ lệ lấp đầy 90% | 90% ghế được lấp đầy |
| Doanh thu trên ghế-km tăng | Giá vé trung bình cao hơn |
| ASK > RPK | Mở chuyến nhưng khách không tăng tương ứng |
| Phụ trội (Ancillary) | Tiền thu thêm: hành lý, đồ ăn, chọn ghế |
| Giá dầu ép biên | Xăng máy bay đắt → lời ít hơn |
| LCC | Hãng giá rẻ — vé rẻ, mọi thứ khác tính thêm |
| FSC | Hãng truyền thống — vé đã bao gồm dịch vụ |
| Long Thành | Sân bay mới ở Đồng Nai — giai đoạn 1 tăng 25 triệu HK/năm |
