---
category: frameworks
title: "Retail-Industry-Master-Reference"
last_updated: 2026-05-12
---

Master reference cho Master Retail — mental model 6 lớp phân tích ngành bán lẻ VN. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **MWG · FRT · PNJ · DGW**. Các deep dive (Retail-SSSG-reading, Retail-inventory-cycle) mang chi tiết cơ chế; master reference này gom 6 lớp vào một chỗ để orient nhanh.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Retail/knowledge.md + web search. Đầy đủ 6 lớp. |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Mô hình kinh doanh

Bán lẻ Việt Nam sinh lợi nhuận từ hai nguồn chính:

- **Biên gộp (Gross margin):** Mua hàng giá thấp từ nhà cung cấp → Bán giá cao hơn cho người tiêu dùng → Chênh lệch = Biên gộp (20-40% tùy phân khúc)
- **Thu nhập phụ trợ (5-15%):** Bán trả góp (lãi suất tiêu dùng), dịch vụ hậu mãi, cho thuê không gian, hoa hồng bán bảo hiểm

Driver ngắn hạn là sức mua tiêu dùng (lãi suất, lạm phát, tâm lý). Driver dài hạn là chuyển dịch kênh truyền thống → hiện đại + thị phần consolidation.

## 1.2 Phân loại mô hình (structural)

### Bán lẻ điện máy/công nghệ (CE - Consumer Electronics)

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| MWG | Thế giới Di động | Dẫn đầu thị phần ~45% CE; đa chuỗi (TGDĐ/ĐMX + BHX + An Khang + AVAKids); TGDĐ/ĐMX là cash cow |
| FRT | FPT Retail | FPT Shop #2 CE sau MWG; Long Châu là growth engine dược phẩm |
| DGW | Digiworld | Phân phối ICT B2B (không bán lẻ trực tiếp); biên mỏng ~5-8%, volume lớn |

### Bán lẻ chuyên biệt

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| PNJ | Phú Nhuận Jewelry | Dẫn đầu trang sức; biên cao 20-25%; phụ thuộc giá vàng + thu nhập khả dụng |

### Bán lẻ grocery (tham chiếu — chưa có mã riêng trong universe)

| Chuỗi | DN sở hữu | Đặc trưng |
|---|---|---|
| Bách Hoá Xanh | MWG | Grocery chain lớn nhất MWG; biên mỏng 22-26%; đang trên lộ trình hoà vốn |
| WinMart | MSN | Thuộc Masan; mạng lưới rộng; đang tái cấu trúc |

## 1.3 Quyền lực định giá theo phân khúc

| Phân khúc | Quyền lực | Giải thích |
|---|---|---|
| Điện máy | Nhà sản xuất | Apple, Samsung định giá; retailer chỉ cạnh tranh dịch vụ/trả góp |
| Grocery | Bán lẻ | Chuỗi lớn ép nhà cung cấp; WinMart/BHX có thể đàm phán giá |
| Dược phẩm | Bán lẻ + Nhà nước | Giá thuốc bị kiểm soát một phần; chuỗi có biên cao hơn nhà thuốc độc lập |
| Trang sức | Bán lẻ | PNJ có thương hiệu mạnh; định giá premium so với tiệm vàng nhỏ |
| ICT B2B | Nhà cung cấp | DGW là trung gian; biên do vendor quyết định |

## 1.4 Cạnh tranh theo phân khúc

| Phân khúc | Mức độ | Market leader | Ghi chú |
|---|---|---|---|
| Điện máy | Cao | MWG ~45% | FRT #2; Nguyễn Kim/Điện máy Chợ Lớn/CellphoneS chia phần còn lại |
| Grocery | Rất cao, phân mảnh | Chưa ai >5% | BHX + WinMart + Co.op + ngoại (AEON, Lotte) + chợ truyền thống 75% |
| Dược phẩm | Cao | Long Châu (FRT) | An Khang (MWG), Pharmacity, nhà thuốc độc lập |
| Trang sức | Trung bình | PNJ | SJC, DOJI, tiệm vàng gia đình |
| ICT B2B | Trung bình | DGW ~30% | FPT Trading, Synnex |

## 1.5 Mùa vụ quan trọng

| Quý | Điện máy | Grocery | Dược | Trang sức |
|---|---|---|---|---|
| Q1 | **Cao** (Tết, iPhone) | **Rất cao** | Bình thường | **Cao** (mùa cưới) |
| Q2 | **Thấp nhất** | **Thấp nhất** | Cao (nắng, dịch) | Thấp |
| Q3 | Trung bình (back to school) | Trung bình | Trung bình | Thấp |
| Q4 | **Cao** (iPhone mới, Black Friday) | Cao | Cao (lạnh, cúm) | **Cao** (Noel, cưới) |

> **Quy tắc**: LUÔN so YoY, KHÔNG so QoQ do seasonal bias quá lớn.

## 1.6 Chuyển dịch kênh

- **Truyền thống → Hiện đại:** ~75% bán lẻ VN vẫn là chợ/tiệm nhỏ; chuỗi hiện đại chỉ ~25%
- **Offline → Online:** TMĐT ~10-12% tổng bán lẻ (2025); tốc độ tăng ~25-30%/năm
- **Sàn TMĐT:** Shopee 56% thị phần (giảm từ 64%); TikTok Shop 41% (tăng mạnh từ 17%); Lazada/Tiki thu hẹp
- **Xu hướng 2026:** Social commerce, livestream shopping, mua sắm giải trí; logistics siêu tốc

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics quan trọng

**Tier 1 — Thị trường phản ứng ngay**

| Chỉ số | Cách đọc | Benchmark |
|---|---|---|
| **SSSG** (Same-store sales growth) | Dương = tăng trưởng thật; Âm = cửa hàng cũ yếu | CE >3% / Grocery >10% / Dược >15% |
| **Doanh thu từng chuỗi** | Tổng tăng nhưng chuỗi lõi giảm = nguy hiểm | Tách riêng từng chuỗi |
| **Net store opening** | Dương = mở rộng; Âm = co cụm | BHX: 200-400/năm, Long Châu: 200-300/năm |
| **Biên gộp** | Giảm = phải giảm giá cạnh tranh | CE: 20-25%, Grocery: 22-26%, Dược: 30-40%, ICT: 5-8% |

**Tier 2 — Phản ứng 1-3 quý**

| Chỉ số | Benchmark |
|---|---|
| Doanh thu/m² | Tăng = hiệu quả điểm bán tốt |
| Vòng quay hàng tồn kho | CE: 6-8x, Grocery: 12-15x, Dược: 4-6x, ICT: 8-10x |
| Thời gian hoà vốn cửa hàng mới | BHX: 18-24 tháng, Long Châu: 12 tháng, CE: 6-12 tháng |
| SG&A/DT | CE: 12-15%, Grocery: 18-22%, Dược: 15-18%, ICT: 3-5% |

**Tier 3 — Dài hạn**

Thị phần / Doanh thu online / Unit economics chuỗi mới / Doanh thu trả góp & hậu mãi

## 2.2 Tăng trưởng thật vs ảo

```
SSSG dương = tăng trưởng THẬT (khách mua nhiều hơn tại cửa hàng cũ)
SSSG âm + Tổng DT tăng = tăng nhờ mở mới, KHÔNG BỀN VỮNG
```

> **Decision rule**: Khi đọc BCTC, PHẢI tách SSSG. "Doanh thu +20%" vô nghĩa nếu SSSG âm.

## 2.3 Rủi ro hàng tồn kho — đặc thù ngành

| Loại hàng | Tốc độ mất giá | Mức rủi ro |
|---|---|---|
| Điện thoại | 20-30% / 6 tháng | **Rất cao** |
| Laptop | 15-20% / 6 tháng | Cao |
| Thực phẩm tươi | Hỏng 3-7 ngày | Cao (vòng quay cao bù) |
| Thuốc | Hạn 1-3 năm | Thấp |
| Trang sức vàng | Không mất giá (giữ theo giá vàng) | Thấp |

**Báo động đỏ:** HTK tăng đột biến + Vòng quay giảm = sắp xả giá → ăn mòn biên gộp

## 2.4 Bẫy BCTC bán lẻ

| Bẫy | Cách xử lý |
|---|---|
| "Doanh thu tăng 20%" | Tách SSSG — nếu âm thì không bền |
| "Lợi nhuận tăng vọt" | Kiểm tra hoàn nhập dự phòng HTK |
| "Biên gộp cải thiện" | Xem biên từng chuỗi — chuỗi nào kéo lên? |
| "Chuỗi mới lỗ giảm" | Kiểm tra net store opening — có đóng cửa hàng lỗ? |
| "Mở 300 cửa hàng" | Nhìn NET (mở - đóng) |
| "HTK giảm" | Kiểm tra vòng quay + biên — giảm do bán được hay xả giá? |

## 2.5 Đánh giá mở rộng chuỗi mới

- **Tốt:** SSSG dương tăng dần, biên cải thiện, timeline hoà vốn đúng kế hoạch
- **Xấu:** SSSG âm, biên không cải thiện >2 năm, dời deadline, lỗ kéo dài >3 năm

## 2.6 Checklist BCTC (8 bước)

1. Tách doanh thu từng chuỗi
2. SSSG từng chuỗi
3. Net store opening
4. Biên gộp từng chuỗi
5. HTK + vòng quay
6. Lộ trình hoà vốn chuỗi mới
7. So YoY (KHÔNG QoQ)
8. Vĩ mô (lãi suất, tỷ giá, VAT, sức mua, TMĐT)

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Nguyên tắc cốt lõi

```
Giá cổ phiếu bán lẻ chạy theo KỲ VỌNG tương lai, KHÔNG theo KQKD hiện tại:
- Giá tăng khi KQKD vẫn xấu nhưng BỚT XẤU
- Giá giảm khi KQKD vẫn tốt nhưng BỚT TỐT
```

## 3.2 Bốn giai đoạn chu kỳ bán lẻ

| Giai đoạn | KQKD | Giá CP | Tín hiệu nhận diện |
|---|---|---|---|
| **Đáy** | Lỗ/LN giảm mạnh | Bắt đầu tăng | LN -40-60% YoY, SSSG -10-20%, HTK giảm |
| **Hồi phục** | LN dương, SSSG dương | **Tăng mạnh nhất** | SSSG chuyển dương, SG&A giảm, insider mua |
| **Tăng trưởng** | LN tăng đều | Tăng chậm/đi ngang | SSSG ổn định +3-5%, biên ổn định |
| **Đỉnh** | Vẫn tốt nhưng chậm lại | Bắt đầu giảm | SSSG giảm tốc 2 quý, mở ồ ạt, HTK tăng |

## 3.3 Tín hiệu đáy (nên tích luỹ)

Cần 2-3/7 tín hiệu:

1. Lãi suất đạt đỉnh, bắt đầu giảm
2. HTK bắt đầu giảm
3. SSSG bớt âm (-20% → -5%)
4. SG&A giảm (cắt chi phí)
5. Đóng cửa hàng lỗ xong
6. Insider mua cổ phiếu
7. Chính phủ kích cầu (giảm VAT, đầu tư công)

> **Mạnh nhất:** KQKD xấu + ≥3 tín hiệu + Giá đã -40-60% từ đỉnh

## 3.4 Tín hiệu đỉnh (nên giảm tỷ trọng)

Cần 2-3/6 tín hiệu:

1. Lãi suất bắt đầu tăng
2. HTK tăng đột biến + vòng quay giảm
3. SSSG giảm tốc 2 quý liên tiếp
4. Biên gộp giảm 2-3 quý liên tiếp
5. Mở ồ ạt + SSSG giảm (cannibalization)
6. Insider bán cổ phiếu

> **Nguy hiểm:** KQKD tốt + ≥3 tín hiệu đảo chiều + Giá đã +100-200% từ đáy

## 3.5 Case study MWG (2022-2026)

| Giai đoạn | Thời điểm | KQKD | Giá |
|---|---|---|---|
| Đáy | Q3-Q4/2022 | LN -50-60%, SSSG -20% | ~30k |
| Trigger | Q4/22-Q1/23 | LN vẫn giảm NHƯNG: lãi suất giảm, HTK giảm, SSSG bớt âm | 30k→40k |
| Hồi phục | Q2-Q4/2023 | SSSG dương, BHX bớt lỗ | 40k→55k |
| Tăng trưởng | 2024 | LN tăng đều, BHX gần hoà vốn | 55k→65k |
| Chậm lại | 2025-2026 | LN tăng nhưng tốc độ giảm; tiêu dùng phục hồi chậm | 60-70k |

## 3.6 Chu kỳ sản phẩm (CE)

- **iPhone mới:** Ra mắt Q3-Q4 hàng năm → Doanh thu TGDĐ/FPT Shop tăng 1-2 quý
- **Chu kỳ thay thế:** Điện thoại 2-3 năm, Laptop 4-5 năm
- **Năm không có sản phẩm breakthrough:** SSSG thường thấp hơn

---

# LỚP 4: ĐỊNH VỊ TỪNG MÃ (STRUCTURAL POSITIONING)

*Lớp này chỉ ghi định vị chiến lược bền vững — không ghi số quý gần nhất.*

| Mã | Định vị cốt lõi | Ưu thế dài hạn | Rủi ro cấu trúc |
|---|---|---|---|
| **MWG** | Đa chuỗi lớn nhất VN; TGDĐ/ĐMX cash cow + BHX growth bet | Thị phần CE #1; mạng lưới rộng nhất; cross-selling đa chuỗi | BHX đốt tiền kéo dài; CE bão hoà; TMĐT cạnh tranh |
| **FRT** | CE #2 + Long Châu growth engine | Long Châu dẫn đầu dược phẩm; biên cao + nhu cầu ổn định; ít phụ thuộc chu kỳ tiêu dùng | FPT Shop cạnh tranh trực tiếp MWG; tốc độ mở Long Châu |
| **PNJ** | Dẫn đầu trang sức; thương hiệu mạnh | Biên cao; khách hàng trung thành; ít cạnh tranh online | Phụ thuộc giá vàng; thu nhập khả dụng; mùa vụ cao |
| **DGW** | Phân phối ICT B2B; không bán lẻ | Volume lớn; quan hệ với Apple/Samsung/Xiaomi | Biên mỏng ~5-8%; phụ thuộc tỷ giá; không có pricing power |

> **Decision rule**: MWG/FRT = pure retail exposure. PNJ = luxury discretionary + gold price. DGW = B2B distribution, không nên so trực tiếp với retailer.

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 P/E theo chu kỳ — Bẫy lớn nhất

| Giai đoạn | P/E | Hành động |
|---|---|---|
| Đáy | Rất cao/âm | **Nên MUA** |
| Hồi phục | Giảm nhanh | Giá tăng mạnh nhất |
| Tăng trưởng | Ổn định | Giá tăng theo E |
| Đỉnh | **Thấp nhất** | Nên BÁN |

> **Bẫy P/E**: P/E thấp ở đỉnh chu kỳ KHÔNG = rẻ (vì E đang peak, sắp giảm).

## 5.2 P/E band MWG (tham chiếu lịch sử)

| Pha | P/E trailing |
|---|---|
| Đáy (Q4/2022) | 40-50x / âm (lỗ) |
| Hồi phục (2023) | 25-35x |
| Tăng trưởng (2024) | 18-25x |
| Ổn định (2025-2026) | 15-20x |

## 5.3 EV/EBITDA

Dùng khi: Doanh nghiệp lỗ / Chuỗi mới đốt tiền / Khấu hao cao (mở nhiều cửa hàng)

| Giai đoạn | EV/EBITDA |
|---|---|
| Đáy | 15-20x |
| Hồi phục | 10-15x |
| Tăng trưởng | 8-12x |
| Đỉnh | 6-10x |

## 5.4 SOTP — Bắt buộc với DN đa chuỗi

| Chuỗi MWG | Phương pháp | Mức tham chiếu |
|---|---|---|
| TGDĐ/ĐMX (có lãi) | P/E forward | 15-18x |
| BHX (mới có lãi) | EV/Sales | 0.5-1.5x doanh thu |
| An Khang (hoà vốn) | EV/Sales/DCF | 0.3-0.8x doanh thu |
| AVAKids (đốt tiền) | — | ~0 |

## 5.5 So sánh peer hợp lệ

- **Hợp lệ:** MWG CE vs FRT FPT Shop / MWG BHX vs MSN WinMart / FRT Long Châu vs Pharmacity
- **Không hợp lệ:** MWG consolidated vs DGW (bán lẻ vs B2B)

## 5.6 Khi định giá không quan trọng

- **Đáy:** Không nhìn P/E, nhìn tín hiệu bớt xấu
- **Đỉnh:** P/E thấp không = rẻ (E đang peak), nhìn tín hiệu đảo chiều

---

# LỚP 6: VĨ MÔ & RỦI RO

## 6.1 Ma trận tác động vĩ mô

| Yếu tố | Điện máy | Grocery | Dược | Trang sức | ICT B2B |
|---|---|---|---|---|---|
| Sức mua giảm | Tiêu cực | Trung tính | Tích cực | Tiêu cực | Tiêu cực |
| Lãi suất tăng | Tiêu cực | Tích cực | Tích cực | Tiêu cực | Trung tính |
| Tỷ giá tăng | Tiêu cực | Tích cực | Trung tính | Trung tính | Tiêu cực |
| TMĐT tăng | Tiêu cực | Trung tính | Trung tính | Trung tính | Tích cực |
| BĐS hồi phục | Tích cực | Trung tính | Tích cực | Tích cực | Trung tính |
| Sản phẩm mới ra | Tích cực | Tích cực | Tích cực | Tích cực | Tích cực |

## 6.2 Động lực tăng trưởng

**Cấu trúc (5-10 năm):**
- Chuyển dịch truyền thống → hiện đại (từ 25% lên 40-50%)
- Đô thị hoá (~40% → 50% 2030)
- Tầng lớp trung lưu tăng
- TMĐT còn dư địa (từ 10% lên 20-25%)
- Hợp nhất ngành (consolidation)

**Chu kỳ (1-3 năm):**
- Chu kỳ thay thế sản phẩm (iPhone mới, laptop refresh)
- Lãi suất giảm → trả góp dễ hơn
- Kích cầu chính phủ (giảm VAT, đầu tư công)
- BĐS hồi phục → nhu cầu nội thất, điện máy
- Giá hàng nhập giảm (tỷ giá thuận lợi)

## 6.3 Rủi ro cấu trúc

- **Bão hoà điểm bán:** Số cửa hàng tối ưu có giới hạn; mở thêm = cannibalization
- **TMĐT ăn thị phần offline:** Shopee/TikTok Shop/Lazada cạnh tranh trực tiếp
- **Dân số già:** Giảm nhu cầu sản phẩm công nghệ mới
- **Cạnh tranh ngoại:** AEON, Lotte, Central Retail mở rộng
- **Đa chuỗi đốt tiền:** BHX/An Khang/AVAKids chưa hoà vốn kéo lùi ROE

## 6.4 Rủi ro chu kỳ

- **Sức mua suy giảm:** Lạm phát, thất nghiệp, bất động sản đóng băng
- **Lãi suất tăng:** Chi phí trả góp tăng, nhu cầu giảm
- **Tỷ giá tăng:** Giá hàng nhập tăng, biên gộp giảm
- **HTK ứ đọng:** Sản phẩm lỗi thời, phải xả giá
- **Chiến tranh giá:** Cạnh tranh gay gắt ăn mòn biên

## 6.5 Sáu câu hỏi vĩ mô bắt buộc

1. **Sức mua?** (GDP, lạm phát, tâm lý tiêu dùng)
2. **Lãi suất** lên hay xuống?
3. **Sự kiện kích cầu?** (VAT, iPhone mới, BĐS hồi phục)
4. **Chuyển dịch truyền thống → hiện đại** nhanh/chậm?
5. **Cạnh tranh** tăng/giảm? Chiến tranh giá hay consolidation?
6. **Rủi ro tồn kho?** Sản phẩm mới sắp ra?

---

## Kế hoạch kinh doanh 2026 (tham chiếu)

| Mã | Doanh thu mục tiêu | Lợi nhuận mục tiêu | Tăng trưởng |
|---|---|---|---|
| MWG | 185.000 tỷ | 9.200 tỷ LNST | DT +18%, LNST +30% |
| FRT | 59.500 tỷ | 1.550 tỷ LNTT | DT +16%, LNTT +27% |
| DGW | 31.500 tỷ | 660 tỷ LNST | DT +18%, LNST +20% |
| PNJ | — | ~3.409 tỷ LNST | LNST +20%+ |

---

## Hướng dẫn tra dữ liệu thời gian thực (cho Master Retail)

KB master này chỉ cung cấp framework + threshold + range historical. Khi viết bài quarter cụ thể, Master phải:

1. **Query KB framework** (file này + deep dive nếu có) — static guidance
2. **Finpath API** cho data realtime:
   - `get_income_statement(ticker)` + `get_balance_sheet(ticker)` — BCTC quarter
   - Inventory turnover, gross margin từ financial statements
   - `get_events(ticker)` + `get_news(ticker)` — ĐHĐCĐ + tin
3. **Web_search** cho data Finpath API không có:
   - SSSG từng chuỗi (thường chỉ công bố trong investor presentation)
   - Net store opening (báo cáo hoạt động)
   - Thị phần TMĐT
   - Xu hướng tiêu dùng, sự kiện iPhone mới

---

## Cross-link (dự kiến)

| Deep dive | Nội dung chính |
|---|---|
| `retail-sssg-reading.md` | Cách tính SSSG, phân biệt tăng trưởng thật vs ảo |
| `retail-inventory-cycle.md` | Rủi ro HTK theo loại hàng, vòng quay benchmark |

---

## Phần suy luận (cần verify)

Các điểm dưới đây tổng hợp từ framework + data historical — cần verify khi đưa vào bài cụ thể:

- **"MWG thị phần ~45% CE"** — con số estimate từ nhiều báo cáo analyst; verify với data market research mới nhất
- **"Benchmark SSSG: CE >3%, Grocery >10%, Dược >15%"** — analytical heuristic; thực tế varies theo năm
- **"P/E band MWG 15-50x qua cycle"** — historical range; số cụ thể quý hiện tại phải fetch từ Finpath API
- **"BHX hoà vốn timeline 18-24 tháng"** — MWG công bố nhiều lần nhưng đã dời deadline; verify announcement mới nhất
