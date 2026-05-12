---
category: frameworks
title: "Utilities-Industry-Master-Reference"
last_updated: 2026-05-12
---

Master reference cho ngành Điện/Tiện ích VN — mental model 6 lớp phân tích. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **POW · REE · PC1 · GEG · NT2 · PPC · QTP · SHP · BWE · TDM**.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Utilities/knowledge.md + web research QHĐ 8 / EVN pricing / PDP8 adjusted 2025. |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Phân loại

**ĐIỆN:** Thuỷ điện (đập) | Nhiệt điện than | Nhiệt điện khí/LNG | Điện gió | Điện mặt trời | Điện sinh khối

**NƯỚC:** Sản xuất nước sạch | Xử lý nước thải | Hạ tầng nước (đường ống, trạm bơm)

## 1.2 Doanh nghiệp niêm yết

### Điện

| Phân khúc | Doanh nghiệp tiêu biểu | Đặc thù |
|---|---|---|
| Thuỷ điện | REE, PC1, SHP, SJD, CHP, TBC, HDG | Biên 60-70%, phụ thuộc mưa, chi phí cận biên gần 0 |
| Nhiệt than | QTP, PPC, BTP | Biên 15-25%, phụ thuộc giá than, dài hạn giảm theo net zero |
| Nhiệt khí/LNG | POW, NT2 | Biên 15-25%, phụ thuộc giá khí + sản lượng PVN |
| Điện gió/mặt trời | GEG, BCG, GEX | Giá ưu đãi (FIT) cố định 20 năm, phụ thuộc gió/nắng, nhiều dự án chuyển tiếp vướng |
| Đa nguồn | REE, POW, PC1 | Đa dạng hoá = ổn định hơn |

### Nước

| Phân khúc | Doanh nghiệp tiêu biểu | Đặc thù |
|---|---|---|
| Sản xuất nước sạch | TDM, BWE, DNW, VCW | Biên 30-50%, doanh thu định kỳ, rất ổn định |
| Hạ tầng nước | BWE, REE | Đầu tư đường ống, nhà máy xử lý |

## 1.3 Chuỗi giá trị điện

```
SẢN XUẤT → TRUYỀN TẢI → PHÂN PHỐI → TIÊU DÙNG
   IPP        EVN NPT      EVN PC       Hộ/DN
```

- **Sản xuất:** Nhà máy điện (REE, POW, PC1, QTP, PPC, NT2, SHP...) → bán cho EVN hoặc thị trường cạnh tranh
- **Truyền tải:** Đường dây 220-500kV, EVN NPT độc quyền (chưa niêm yết)
- **Phân phối:** Đường dây trung/hạ thế → người dùng cuối

**EVN = "ÔNG CHỦ":**
- Sở hữu truyền tải + phân phối + nhiều nhà máy điện
- Mua điện từ IPP (nhà máy tư nhân), bán lẻ cho người dùng
- Giá bán lẻ do Nhà nước quy định → EVN thường lỗ khi giá đầu vào tăng
- Monopsony → nhà máy tư nhân phải bán cho EVN, không tự quyết giá hoàn toàn
- Thị trường bán buôn điện cạnh tranh (VWEM) đang phát triển nhưng chưa hoàn chỉnh

## 1.4 Yếu tố quyết định

**ĐIỆN:**
- EVN + Bộ Công Thương: giá bán lẻ, giá mua (PPA), sản lượng huy động (Qc)
- EVN gọi thuỷ điện trước (rẻ nhất) → nhiệt → gió/mặt trời
- **Thời tiết:** La Nina (mưa) → thuỷ điện TỐT | El Nino (hạn) → thuỷ điện XẤU
- **Giá nguyên liệu:** Than/khí → chi phí số 1 cho nhiệt điện
- **QHĐ 8 điều chỉnh:** Tăng gió, mặt trời, LNG. Giảm than dài hạn

**NƯỚC:**
- Đô thị hoá + KCN → nhu cầu tăng cấu trúc
- Giá nước nhà nước quy định, nước công nghiệp giá cao hơn → biên tốt hơn

## 1.5 Đặc thù thị trường Việt Nam

| Phân khúc | Đặc điểm |
|---|---|
| **Điện chung** | Thiếu điện triền miên, tăng 8-12%/năm, thiếu mùa khô (T3-T6) |
| **Thuỷ điện** | Biên 60-70%, chi phí gần 0, biến động theo thời tiết (La Nina = bùng, El Nino = sụp) |
| **Nhiệt điện** | Biên 15-25%, ổn hơn, than dài hạn giảm (mục tiêu net zero 2050) |
| **Năng lượng tái tạo** | QHĐ 8 mục tiêu 28-36% năm 2030, FIT 1 hết, dự án chuyển tiếp vướng pháp lý |
| **Nước** | Biên 30-50%, định kỳ, tăng 8-12%/năm, gần như không có chu kỳ |

## 1.6 Mùa vụ

| Quý | Thuỷ điện | Nhiệt điện | Nước |
|---|---|---|---|
| Q1 | Thấp (khô bắt đầu) | Cao (bù thuỷ) | Tăng nhẹ |
| **Q2** | **Thấp nhất** | **Cao nhất** | **Cao** |
| **Q3** | **Cao nhất (mùa mưa)** | Thấp | Trung bình |
| Q4 | Cao | Thấp-Trung bình | Trung bình |

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics điện

**Tier 1 — Thị trường phản ứng ngay:**
1. **Sản lượng (kWh/MWh)** — so cùng kỳ + kế hoạch EVN huy động (Qc)
2. **Giá bán bình quân (ASP - đ/kWh)** — Thuỷ: 600-900đ | Nhiệt than: 1.200-1.600đ | Nhiệt khí: 1.500-2.000đ
3. **Biên gộp** — Thuỷ: 60-70% | Nhiệt: 15-25%
4. **Lượng mưa/mực nước hồ** (thuỷ điện) — NOAA dự báo La Nina/El Nino
5. **Giá than/khí** (nhiệt điện) — chi phí đầu vào chính

**Tier 2 — Phản ứng 1-3 quý:**
- Capacity factor (hệ số công suất)
- Giá VWEM (thị trường bán buôn)
- Chi phí bảo trì định kỳ
- Hợp đồng mua bán điện (PPA) dài hạn

**Tier 3 — Dài hạn:**
- QHĐ 8 điều chỉnh
- Dự án năng lượng tái tạo chuyển tiếp
- Nhu cầu điện toàn quốc (+8-12%/năm)
- Giá bán lẻ điện bình quân EVN (2.444 đ/kWh từ 05/2025)

## 2.2 Metrics nước

1. **Sản lượng (m3)** — so cùng kỳ
2. **Giá bán (đ/m3)** — Công nghiệp giá cao hơn, biên tốt hơn
3. **Biên gộp** — 30-50%
4. **Số hộ/KCN kết nối** — động lực tăng trưởng
5. **Công suất nhà máy**
6. **Cổ tức** — Yield 4-7%

## 2.3 REE — Case đặc biệt (holding đa mảng)

- Thuỷ điện (~35-40% lợi nhuận) + Điện gió/mặt trời (~10-15%) + Nước (~15-20% qua BWE) + Cơ điện lạnh (~20-25%)
- Portfolio đa dạng nhất sàn VN, cổ tức 4-6%
- **PHẢI TÁCH:** Lợi nhuận thuỷ điện vs nước vs cơ điện lạnh vs đầu tư tài chính

## 2.4 Bẫy phổ biến

| Bẫy | Thực tế | Kiểm tra |
|---|---|---|
| "SHP lợi nhuận +80%" | Mùa mưa nhiều, 1 mùa | La Nina? Năm sau El Nino? |
| "QTP lợi nhuận -30%" | Giá than tăng | Xu hướng giá than dài hạn |
| "POW doanh thu +20%" | VWEM cao tạm thời | Giá bán bền vững hay đỉnh? |
| "BWE doanh thu +15%" | Bình thường | Đúng xu hướng cấu trúc |
| "REE lợi nhuận giảm" | Thuỷ điện yếu | Mảng nào giảm? Mảng nào bù? |
| "Năng lượng tái tạo lãi tốt" | FIT 1 cao, hết = giá giảm | PPA giá bao nhiêu? Còn ưu đãi? |

## 2.5 Checklist

**ĐIỆN:** Sản lượng so cùng kỳ | Mưa/hạn? | Giá than/khí | Giá bán bình quân | Công suất huy động (Qc) | Biên gộp | Bảo trì nhà máy | QHĐ 8

**NƯỚC:** Sản lượng | Khách mới | Giá nước | Công suất nhà máy | Biên gộp | Cổ tức

---

# LỚP 3: CHU KỲ

## 3.1 Nguyên tắc

- **Nước:** KHÔNG có chu kỳ — ổn nhất, doanh thu tăng đều 8-12%/năm
- **Thuỷ điện:** Chu kỳ thời tiết 2-4 năm (La Nina ↔ El Nino), KHÔNG theo kinh tế vĩ mô
- **Nhiệt điện:** Ít chu kỳ, biên theo giá than/khí, sản lượng ổn định hơn
- **Năng lượng tái tạo:** Phụ thuộc chính sách FIT/PPA

## 3.2 La Nina / El Nino

**La Nina (mưa nhiều):**
- Hồ đầy → sản lượng +30-50% → lợi nhuận kỷ lục → cổ phiếu tăng mạnh (1-2 năm)
- Nhiệt điện bị gọi ít hơn

**El Nino (hạn hán):**
- Hồ cạn → sản lượng -20-40% → doanh thu giảm → cổ phiếu giảm
- Nhiệt điện hưởng lợi (EVN gọi bù)

**Chiến lược:** MUA thuỷ điện khi dự báo La Nina | BÁN khi dự báo El Nino | Theo dõi NOAA

## 3.3 Tín hiệu sớm

**Thuỷ điện tốt:** NOAA dự báo La Nina | Mực nước hồ > trung bình | Mùa mưa sớm | VWEM cao

**Thuỷ điện khó:** NOAA dự báo El Nino | Mực nước hồ < trung bình | Mùa khô kéo dài

**Nhiệt điện tốt:** El Nino | Giá than/khí giảm | VWEM cao | EVN huy động nhiều

---

# LỚP 4: VĨ MÔ

## 4.1 Tác động

| Yếu tố | Thuỷ | Nhiệt | Nước | Năng lượng tái tạo |
|---|---|---|---|---|
| La Nina/El Nino | +++/--- | -/+ | ~ | ~ |
| Giá than | ~ | --- | ~ | ~ |
| Giá khí/LNG | ~ | -- | ~ | ~ |
| Giá bán lẻ điện tăng | + | + | ~ | + |
| QHĐ 8 điều chỉnh | ~ (ít nhà máy mới) | - (than giảm dài hạn) | ~ | +++ |
| FDI + KCN | ~ | ~ | ++ | ~ |
| Đô thị hoá | ~ | ~ | +++ | ~ |
| FIT/PPA mới | ~ | ~ | ~ | ++/-- |

## 4.2 QHĐ 8 điều chỉnh (phê duyệt 04/2025)

**Mục tiêu 2030:**
- Năng lượng tái tạo (không tính thuỷ điện): 28-36% tổng công suất
- Điện mặt trời: 46.459-73.416 MW
- Điện gió trên bờ + gần bờ: 26.066-38.029 MW
- Điện sinh khối + rác: 3.009-4.881 MW

**Tầm nhìn 2050:**
- Năng lượng tái tạo: 74-75% tổng công suất
- Nhiệt điện than: phase-out dần

**Vốn đầu tư 2026-2030:** ~136,3 tỷ USD cho nguồn điện + lưới truyền tải

## 4.3 Động lực tăng trưởng

**Cấu trúc (dài hạn):**
- Nhu cầu điện +8-12%/năm
- Đô thị hoá → nước tăng
- KCN → điện + nước công nghiệp
- QHĐ 8: năng lượng tái tạo + LNG tăng, than giảm
- Giá bán lẻ điện tăng dần (2.444 đ/kWh từ 05/2025)
- VWEM phát triển → cơ hội IPP giỏi

**Chu kỳ (ngắn hạn):**
- La Nina
- Giá than/khí giảm
- Thiếu điện mùa khô
- FIT/PPA mới

## 4.4 Rủi ro

| Rủi ro | Ai bị ảnh hưởng |
|---|---|
| El Nino | Thuỷ điện --- |
| Giá than/khí tăng | Nhiệt điện -- |
| EVN ép giá PPA | Tất cả IPP |
| Năng lượng tái tạo chuyển tiếp vướng | GEG, BCG, GEX |
| Than phase-out | QTP, PPC, BTP |
| Giá bán lẻ không tăng kịp | EVN lỗ → ép nhà máy |
| Giá nước bị ép | Doanh nghiệp nước |

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 Phương pháp

| Phân khúc | Phương pháp | Benchmark |
|---|---|---|
| Thuỷ điện | P/E normalized (trung bình 3-5 năm) + Div yield | 8-14x hợp lý, <8x rẻ, >14x đắt |
| Nhiệt điện | P/E + EV/EBITDA | 6-10x tuỳ chất lượng |
| Nước | P/E + Div yield | 12-20x (premium vì định kỳ), yield 4-7% |
| Năng lượng tái tạo | DCF dòng tiền dự án | Phụ thuộc PPA/FIT |
| REE | SOTP (tổng các phần) | Tách từng mảng |

## 5.2 Bẫy định giá

- "Thuỷ điện P/E 6x = rẻ" → Năm La Nina → lợi nhuận cao bất thường → PHẢI normalize 3-5 năm
- "Thuỷ điện yield 10%" → Năm mưa nhiều, năm sau có thể 3%
- "Nhiệt điện P/E 8x" → Giá than đang rẻ, kiểm tra xu hướng
- "Nước P/E 18x = đắt" → Định kỳ + tăng trưởng xứng premium

**Chiến lược:** Mua thuỷ điện khi El Nino (giá rẻ) → chờ La Nina | Mua nước khi yield >5% + growth >8%

---

# LỚP 6: TƯ VẤN (PROFILE PHÂN LOẠI)

## 6.1 Theo phân khúc

| Phân khúc | Chiến lược |
|---|---|
| **Thuỷ điện** | Mua: dự báo La Nina + giá rẻ | Bán: dự báo El Nino | Cổ tức 5-10% biến động | "Đặt cược thời tiết" |
| **Nhiệt điện** | Ổn hơn | Mua: giá than/khí giảm + VWEM cao | Tránh than dài hạn | POW tốt nhất (đa nguồn) |
| **Nước** | MUA DÀI HẠN | "Trái phiếu có tăng trưởng" | Yield 4-7% + growth 8-12% | NĐT bảo thủ | Ít xúc tác ngắn hạn |
| **REE** | Blue chip ngành tiện ích | Cổ tức 4-6% | Mua: La Nina hoặc giá rẻ |

## 6.2 Theo profile nhà đầu tư

| Profile | Chiến lược |
|---|---|
| **Dài hạn (>1 năm)** | #1 Nước (BWE, TDM) | #2 REE | Tránh nhiệt than, năng lượng tái tạo vướng |
| **Trung hạn (3-12 tháng)** | Thuỷ điện + NOAA La Nina | POW khi giá khí giảm | Nước yield >5% |
| **Ngắn hạn (<3 tháng)** | Thuỷ điện trước mùa mưa (Q2→Q3) | Nhiệt mùa khô (Q1-Q2) | Nước không phù hợp |

## 6.3 Dịch thuật ngữ

| Thuật ngữ | Giải thích |
|---|---|
| La Nina | Thời tiết mưa nhiều — tốt cho thuỷ điện |
| El Nino | Hạn hán — thuỷ điện không có nước |
| EVN gọi điện (Qc) | EVN yêu cầu nhà máy sản xuất — ai được gọi mới có doanh thu |
| Giá than tăng | Nhiên liệu đắt → chi phí tăng → lời ít |
| VWEM | Chợ điện bán buôn — bán giá thị trường |
| FIT | Giá ưu đãi điện gió/mặt trời cố định 20 năm |
| PPA | Hợp đồng mua bán điện dài hạn với giá cố định |
| Nước định kỳ | Thu tiền nước hàng tháng, đều đặn |
| Biên thuỷ điện 65% | 100đ bán → lời 65đ (nước miễn phí) |
| ASP | Giá bán bình quân (đồng/kWh) |
| Capacity factor | Hệ số công suất — sản lượng thực / công suất thiết kế |

---

# PHỤ LỤC

## A. Severity matrix

| Phân khúc | Xanh (tốt) | Vàng (trung tính) | Đỏ (xấu) |
|---|---|---|---|
| Thuỷ điện | La Nina + sản lượng tăng | Mưa bình thường + sản lượng ổn | El Nino + sản lượng giảm mạnh |
| Nhiệt điện | Giá than/khí giảm + gọi nhiều | Ổn định | Giá tăng mạnh + bảo trì |
| Nước | Sản lượng tăng + KCN mới | Sản lượng tăng nhẹ | Hiếm — giá ép + chi phí tăng |
| Năng lượng tái tạo | FIT/PPA tốt + dự án duyệt | Chuyển tiếp chưa có giá | Vướng pháp lý + không PPA |

## B. Câu đánh giá mẫu

**Thuỷ điện La Nina:**
"{ticker} sản xuất {X} triệu kWh — +{Y}% so cùng kỳ nhờ mưa nhiều. Hồ đầy, chạy đầy công suất, nước miễn phí nên gần như toàn bộ doanh thu thêm = lợi nhuận."

**Thuỷ điện El Nino:**
"{ticker} sản lượng -{X}% do hạn, mực nước hồ -{Y}% so trung bình. Dự báo hạn kéo dài {Z} tháng."

**Nhiệt điện giá than tăng:**
"{ticker} doanh thu +{X}% (bù thuỷ điện yếu), nhưng giá than +{Y}% nên lợi nhuận chỉ +{Z}%. Bán nhiều điện hơn nhưng mỗi kWh lời ít hơn."

**Nước ổn định:**
"{ticker} doanh thu nước +{X}% — đều như mọi quý. {Y} KCN mới + {Z} nghìn hộ kết nối. Thu tiền đều hàng tháng."

**REE đa mảng:**
"REE lợi nhuận +{X}%: thuỷ điện đóng góp {Y}% (mưa nhiều), nước +{Z}%, cơ điện +{W}%. Đa mảng bù trừ → ít biến động."

## C. Quy tắc agent

1. Thuỷ điện = đặt cược thời tiết → PHẢI check La Nina/El Nino từ NOAA
2. Chi phí thuỷ điện gần 0 → Biên 60-70% → Sản lượng thêm gần như 100% lợi nhuận
3. Nhiệt điện: giá than/khí = biến số số 1
4. EVN = "ông chủ" → quyết giá mua (PPA) + sản lượng huy động (Qc)
5. Nước = ổn nhất, ít chu kỳ nhất → phòng thủ + cổ tức
6. REE = đa mảng → PHẢI tách: thuỷ vs nước vs cơ điện
7. Năng lượng tái tạo: FIT/PPA quyết định → không PPA = rủi ro lớn
8. P/E thuỷ điện phải normalize qua La Nina + El Nino (3-5 năm)
9. KHÔNG dùng thuật ngữ tiếng Anh → PHẢI dịch
10. KHÔNG bịa data → Thiếu → nói thiếu

---

## Hướng dẫn tra dữ liệu thời gian thực

KB master này chỉ cung cấp framework + threshold + range lịch sử. Khi viết bài quý cụ thể:

1. **Query KB framework** (file này) — static guidance
2. **Web search** cho data realtime:
   - NOAA dự báo La Nina/El Nino
   - Giá than/khí quốc tế
   - QHĐ 8 updates
   - Tin EVN huy động/giá điện
   - BCTC quý gần nhất từng mã
3. **Finpath API** (khi available):
   - `get_income_statement(ticker)` — doanh thu, lợi nhuận
   - `get_balance_sheet(ticker)` — tài sản, nợ
   - `get_events(ticker)` — ĐHĐCĐ, cổ tức
   - `get_news(ticker)` — tin mới

---

## Sources

- [QHĐ 8 điều chỉnh - Bộ Công Thương](https://moit.gov.vn/tin-tuc/phat-trien-nang-luong/chinh-thuc-phe-duyet-quy-hoach-dien-viii-dieu-chinh.html)
- [Toàn văn Quy hoạch điện VIII](https://xaydungchinhsach.chinhphu.vn/toan-van-quy-hoach-phat-trien-dien-luc-quoc-gia-11923051616315244.htm)
- [Biểu giá bán lẻ điện EVN 05/2025](https://www.evn.com.vn/d/vi-VN/news/Bieu-gia-ban-le-dien-theo-Quyet-dinh-so-1279QD-BCT-ngay-0952025-cua-Bo-Cong-Thuong-60-28-502668)
- [EVN áp lực chi phí Q2/2026](https://vneconomy.vn/ap-luc-chi-phi-mua-dien-dau-vao-tang-tu-quy-22026.htm)
