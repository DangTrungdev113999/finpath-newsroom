---
category: frameworks
title: "Food-Industry-Master-Reference"
last_updated: 2026-05-12
---

Master reference cho Master Food — mental model 6 lớp phân tích ngành Thực phẩm & Đồ uống (F&B) VN. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **VNM · SAB · MSN · QNS · KDC · MCH · SBT**. Ba deep dive (NVL-cycle, Premium-transition, Seasonality-pattern) mang chi tiết cơ chế và số liệu lịch sử; master reference này gom 6 lớp vào một chỗ để orient nhanh.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Food/knowledge.md + web research. Format theo bank-industry-master-reference.md parity. |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Mô hình kinh doanh

Ngành F&B Việt Nam sinh lợi nhuận từ hai mảng chính:

- **Sản xuất (70-90% DT):** Mua nguyên liệu (sữa bột, mạch nha, đường, bột mì, cà phê) → Chế biến → Phân phối qua GT/MT/TMĐT/HoReCa/Xuất khẩu
- **Thương mại/Dịch vụ (10-30%):** Bán lẻ (WinMart/MSN), nhà hàng/cafe (Phúc Long/MSN), xuất khẩu

Driver ngắn hạn là giá nguyên vật liệu + sức mua tiêu dùng. Driver dài hạn là tăng trưởng dân số trung lưu + premium hoá sản phẩm.

## 1.2 Phân loại doanh nghiệp (structural — không per-quarter)

### Nhóm Sữa

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| VNM | Vinamilk | #1 sữa VN (~40% thị phần); DT >60.000 tỷ/năm; cổ tức đều 4.000-5.000đ/năm; premium (A2, organic, Greenfarm); XK Trung Đông, Mỹ, Đông Nam Á |

### Nhóm Bia

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| SAB | Sabeco | #1 bia VN (~40% thị phần); ThaiBev sở hữu ~36%; NĐ100 ảnh hưởng volume; biên gộp 28-32%; mùa vụ Q2-Q3 |
| BHN | Habeco | #2 bia VN; mạnh miền Bắc; volume giảm dài hạn do NĐ100 |

### Nhóm FMCG đa mảng

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| MSN | Masan Group | Holding: MCH (FMCG) + WCM (bán lẻ) + MML (thịt) + Phúc Long + TCB (35%); restructure 2022-2025 thành công |
| MCH | Masan Consumer | #1 FMCG VN (mì Omachi, nước mắm Chinsu, gia vị); biên gộp 40-50% cao nhất ngành; brand mạnh nhất |
| KDC | Kido | Bánh kẹo + Dầu ăn + Kem; mùa vụ Tết rõ (Q1); đang premium hoá |

### Nhóm Đường

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| SBT | TTC Sugar | #1 đường VN; biên gộp 10-15% (thấp nhất F&B); chu kỳ giá đường TG (ICE #11); đa mảng: đường + điện sinh khối + ethanol |
| QNS | Đường Quảng Ngãi | 2 mảng: Vinasoy (#1 sữa đậu nành) + Đường; Vinasoy ổn định, đường chu kỳ |

### Nhóm khác

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| BBC | Bibica | Bánh kẹo mid-cap; Lotte sở hữu |
| HHC | Hải Hà | Bánh kẹo; mùa vụ Tết |
| MML | Masan MEATLife | Thịt chế biến; nhạy giá heo + dịch bệnh |

> **Decision rule phân loại**: Sữa/FMCG = phòng thủ, biên cao, growth 5-12%/năm. Bia = nhạy NĐ100 + mùa vụ + sức mua. Đường = chu kỳ mạnh theo giá TG. Bánh kẹo = mùa vụ Tết cực kỳ rõ.

## 1.3 Chuỗi giá trị

**Nguyên liệu:**
- Sữa: Bột sữa NZ/Úc (~40% giá vốn VNM), sữa tươi nội địa
- Bia: Mạch nha + hoa bia nhập khẩu
- Đường: Mía nội địa (vụ ép T10-T4) + đường thô nhập
- Mì: Bột mì nhập khẩu
- Thịt: Thức ăn chăn nuôi (TACN) nhập khẩu

**Phân phối:**
- GT (General Trade - tạp hoá, chợ): ~60%
- MT (Modern Trade - siêu thị, tiện lợi): ~25%
- TMĐT (e-commerce): ~5%
- HoReCa (nhà hàng, khách sạn): ~10%
- Xuất khẩu: VNM (~12%), QNS, MSN

**Thị trường:** 100 triệu dân, tầng lớp trung lưu mở rộng → xu hướng premium hoá

## 1.4 Yếu tố quyết định

| Yếu tố | Tác động | Ai bị nhất |
|---|---|---|
| **Sức mua (#1)** | Thu nhập tăng → premium; yếu → downgrade | Bia nhạy nhất, mì ít nhất |
| **Giá NVL (#2)** | Chiếm 40-70% giá vốn | VNM (bột sữa), SAB (mạch nha), SBT (đường thô) |
| **Kênh phân phối** | GT giảm → MT tăng | DN có hệ thống MT mạnh (VNM, MCH) hưởng lợi |
| **Thương hiệu** | Brand = biên cao + pricing power | VNM, MCH, SAB = top of mind |
| **Chính sách** | NĐ100 (bia), thuế TTĐB, CBPG đường | SAB/BHN (NĐ100), SBT (CBPG) |

## 1.5 Đặc thù thị trường Việt Nam

- Thiết yếu, ít chu kỳ. DT ngành tăng 8-12%/năm (forecast 9.6% 2025)
- Quy mô: 688.800 tỷ đồng năm 2024 (+16.6% so cùng kỳ); hướng tới 760.000 tỷ
- Premium hoá: sữa organic/A2, bia craft, thực phẩm sạch → biên cao
- Bia: NĐ100 giảm sản lượng 5-10%, xu hướng "uống ít + uống đắt"
- VNM + MCH = 60-70% vốn hoá F&B niêm yết
- 323.010 cửa hàng F&B tính đến cuối 2024 (+1.8% so cùng kỳ)

## 1.6 Mùa vụ

| Quý | Sữa | Bia | Mì/Gia vị | Đường | Bánh kẹo |
|---|---|---|---|---|---|
| Q1 | Trung bình | Cao (Tết) | **Rất cao** | Trung bình | **Rất cao** |
| Q2 | Trung bình | **Cao nhất** | Trung bình | Thấp | Thấp |
| Q3 | Trung bình | Cao | Trung bình | **Cao (vụ ép)** | Trung bình |
| Q4 | **Cao** | Trung bình-Cao | **Cao** | Cao | **Cao** |

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics quan trọng

**Tier 1 — Thị trường phản ứng ngay:**
1. Tăng trưởng DT (ngành 8-12%, >12% = tốt)
2. Biên gộp: VNM 43-47%, MCH 40-50%, SAB 28-32%, SBT 10-15%
3. Giá NVL: bột sữa (VNM), mạch nha (SAB), đường thô (SBT)
4. Sản lượng tiêu thụ (DT tăng vì giá hay volume?)
5. Thị phần

**Tier 2 — Phản ứng 1-3 quý:**
6. Chi phí quảng cáo & khuyến mãi/DT: VNM 10-12%, MCH 12-15%
7. Tỷ trọng premium trong mix
8. DT kênh MT vs GT
9. DT xuất khẩu
10. Vòng quay hàng tồn kho

**Tier 3 — Dài hạn:**
- Chi tiêu F&B/người (~25 tỷ USD 2025 → 41 tỷ 2030)
- Đô thị hoá (hướng tới >50% 2030)
- Sản phẩm mới
- M&A

## 2.2 Đọc số theo phân khúc

**Sữa (VNM):**
- Focus: DT nội địa (~80%, tăng 3-5%) + Giá bột sữa (GDT NZ, ~40% giá vốn)
- DT XK ~12% (Trung Đông #1), chi nhánh ngoài ~8%
- Premium: A2, organic, Greenfarm
- Cổ tức: 4.000-5.000đ/cổ phiếu/năm, yield 5-7%

**Bia (SAB):**
- Focus: Sản lượng (triệu lít) + Giá bán trung bình (ASP)
- Biên gộp 28-32% (NVL nhập + thuế tiêu thụ đặc biệt)
- Q2-Q3 (hè) cao nhất, NĐ100 giảm volume
- ThaiBev sở hữu ~36%, chiến lược premium hoá

**FMCG (MCH):**
- Tách DT: Mì, Gia vị, Cà phê, Thịt chế biến
- Biên gộp 40-50% (cao nhất F&B VN)
- MCH nằm trong MSN (+ WCM, MML, TCB, Phúc Long)

**Đường (SBT):**
- Focus: Giá đường TG (ICE #11) + Sản lượng ép (T10-T4)
- Biên gộp 10-15% (thấp nhất F&B)
- Đa mảng: đường + điện sinh khối + ethanol

## 2.3 Bẫy BCTC ngành F&B

| Bẫy | Phải làm |
|---|---|
| VNM DT tăng 10% | Tách nội địa vs XK vs chi nhánh nước ngoài |
| SAB DT tăng 8% | Check sản lượng (có thể giảm, giá tăng bù) |
| VNM biên gộp tăng | Check xu hướng giá bột sữa (GDT) — lag 1-2 quý |
| MCH biên 48% | So cùng kỳ MCH (48% = ổn, 42% = xấu) |
| SBT LN tăng 200% | Giá đường TG cao đột biến, không bền |
| KDC DT Q1 +50% | Mùa Tết, so cùng kỳ năm trước mới có nghĩa |

## 2.4 Checklist BCTC (8 câu hỏi)

1. DT tăng % (so ngành 8-12%, tách phân khúc)
2. Volume tăng hay giảm?
3. Biên gộp (NVL ảnh hưởng sao?)
4. Chi phí quảng cáo & khuyến mãi/DT
5. Premium mix
6. Thị phần
7. Kênh phân phối (GT vs MT vs TMĐT)
8. Vĩ mô (NVL, tỷ giá, sức mua, chính sách)

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Nguyên tắc cốt lõi

```
F&B = Phòng thủ, ít chu kỳ. DT tăng đều 8-12%/năm.
Độ nhạy chu kỳ: Mì/Gia vị (ít nhất) → Sữa → Bia (nhạy nhất). Đường = chu kỳ mạnh.
Cổ phiếu F&B giữ tốt khi VNI giảm, tăng chậm khi VNI bùng nổ.
```

## 3.2 Premium cycle (thay vì boom-bust)

F&B không có chu kỳ boom-bust như ngân hàng/BĐS. Thay vào đó là premium cycle:

| Giai đoạn | Đặc trưng | Tín hiệu nhận diện |
|---|---|---|
| **Downgrade** | Kinh tế yếu: mua rẻ hơn, volume ổn, ASP giảm | Thu nhập giảm, CPI thấp |
| **Hồi phục** | Thu nhập hồi, volume + ASP tăng dần | GDP phục hồi, bán lẻ tăng |
| **Premium hoá** | Kinh tế tốt: sữa organic, bia craft → ASP tăng mạnh, biên cao | Thu nhập tăng, premium mix >30% |
| **Bão hoà** | Volume đi ngang, growth từ XK/M&A/sản phẩm mới | Thị phần ổn định, growth <5% |

## 3.3 VNM timeline (case study)

| Giai đoạn | Đặc điểm | Giá cổ phiếu |
|---|---|---|
| 2015-2018 | DT nội +8-10%, XK mở rộng | 100k → 175k |
| 2019-2020 | Bão hoà, cạnh tranh TH True Milk | 175k → 95k |
| 2021-2023 | DT ngang, tái cấu trúc | 95k → 65k |
| 2024-2025 | Premium (A2, Greenfarm) + XK phục hồi | 60k → 75k |

## 3.4 Tín hiệu

**Sắp tốt:**
- Thu nhập hồi phục
- Giá NVL giảm (bột sữa, mạch nha, đường thô)
- Premium mix tăng
- Quảng cáo/DT giảm mà DT tăng
- Sản phẩm mới thành công
- XK tăng

**Sắp khó:**
- Giá NVL tăng mạnh
- Sức mua giảm
- Cạnh tranh tăng
- Thuế tiêu thụ đặc biệt tăng (bia)
- Thị phần giảm
- Quảng cáo tăng mà DT không tăng

---

# LỚP 4: ĐỊNH VỊ TỪNG MÃ (STRUCTURAL POSITIONING)

*Lớp này chỉ ghi định vị chiến lược bền vững — không ghi số quý gần nhất. Số liệu cụ thể tra Finpath API.*

| Mã | Định vị cốt lõi | Ưu thế dài hạn | Rủi ro cấu trúc |
|---|---|---|---|
| **VNM** | #1 sữa VN, brand mạnh nhất, cổ tức đều | Thị phần ~40%, XK mở rộng, premium (A2/organic), yield 5-7% | Bão hoà nội địa, cạnh tranh TH True Milk, giá bột sữa nhập |
| **SAB** | #1 bia VN, ThaiBev backing | Thị phần ~40%, premium hoá, hưởng lợi du lịch | NĐ100 giảm volume dài hạn, thuế tiêu thụ đặc biệt |
| **MSN** | Holding đa mảng: FMCG + Retail + Thịt + Cafe | Restructure thành công, đa dạng hoá, cross-selling WinMart | WCM/WinMart lỗ kéo dài, đòn bẩy tài chính |
| **MCH** | #1 FMCG VN, biên cao nhất | Brand mạnh (Omachi, Chinsu), biên 40-50%, pricing power | Category mature, growth chậm lại |
| **QNS** | Vinasoy (#1 sữa đậu nành) + Đường | Vinasoy ổn định, đường hưởng lợi CBPG | Đường chu kỳ mạnh, Vinasoy bão hoà |
| **SBT** | #1 đường VN | CBPG bảo hộ, đa mảng (điện, ethanol), capacity lớn | Giá đường TG chu kỳ mạnh, biên thấp nhất F&B |
| **KDC** | Bánh kẹo + Dầu ăn + Kem | Premium hoá, thương hiệu truyền thống | Mùa vụ Tết rõ, cạnh tranh ngoại mạnh |

> **Decision rule**: VNM/MCH = core defensive holding (yield + brand). SAB = trading khi du lịch/tiêu dùng phục hồi. SBT/QNS (mảng đường) = chu kỳ, không buy-and-hold. MSN = restructure play.

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 P/E Benchmark

| DN | P/E range | Lý do |
|---|---|---|
| VNM | 15-22x | #1 sữa, cổ tức đều, brand, XK |
| MCH | 18-25x | Growth FMCG, biên cao |
| SAB | 15-22x | #1 bia, ThaiBev backing |
| QNS | 10-15x | Vinasoy ổn + đường chu kỳ |
| SBT | 10-15x | Đường chu kỳ, biên thấp |
| KDC | 12-18x | Mùa vụ, restructure |

P/E F&B cao vì: ổn định, brand mạnh, cổ tức đều.

## 5.2 PEG (Price/Earnings to Growth)

- <1.0x: Rẻ
- 1.0-1.5x: Hợp lý cho growth (MCH)
- 1.5-2.0x: Hợp lý cho stable (VNM, SAB)
- >2.0x: Đắt

## 5.3 Dividend Yield

- VNM: 4.000-5.000đ/năm, yield 5-7% — #1 cổ tức VN, trả đều 15+ năm
- SAB: 2.000-3.000đ, yield 3-5%
- QNS: 1.500-2.500đ, yield 4-7%

## 5.4 EV/EBITDA so peer khu vực

- VNM/SAB: 10-14x (Thai Beverage 12-16x, Nestlé 18-22x) → hợp lý
- MCH: 12-18x (Indofood 8-12x) → premium vì growth cao

## 5.5 Bẫy định giá

| Sai | Đúng |
|---|---|
| VNM P/E 20x đắt so HPG 12x | Không so được, VNM ổn định, HPG chu kỳ |
| VNM P/E 15x rẻ | Growth 5% → PEG 3x, nhưng yield 6% + growth 5% = 11%/năm vẫn tốt |
| SBT P/E 8x siêu rẻ | Giá đường đỉnh → EPS cao → P/E thấp = bẫy chu kỳ |

---

# LỚP 6: CASE STUDY LỊCH SỬ

### Case 1 — VNM 2019-2025: Bão hoà → Premium hoá

VNM giai đoạn 2015-2018 growth 8-10%/năm, giá 100k → 175k. Từ 2019 bão hoà nội địa, cạnh tranh TH True Milk, giá giảm về 65k. Từ 2024 premium hoá (A2, organic, Greenfarm) + XK phục hồi, giá 60k → 75k. **Bài học**: Ngành bão hoà không có nghĩa cổ phiếu chết — premium hoá + XK mở ra growth mới. Yield 5-7% + growth 5% = total return 10-12% ngay cả khi giá ngang.

### Case 2 — SAB 2019-2025: NĐ100 shock

NĐ100 (12/2019) phạt nặng lái xe uống rượu bia → volume bia giảm 5-10%/năm liên tục. SAB đối phó bằng premium hoá (bia cao cấp), ASP tăng bù volume. **Bài học**: Chính sách có thể thay đổi cấu trúc ngành vĩnh viễn. Bia VN không quay lại peak volume pre-2020, nhưng margin có thể tăng nếu premium thành công.

### Case 3 — MCH 2020-2025: FMCG king + Masan restructure

MCH luôn giữ biên 40-50% cao nhất F&B VN nhờ brand mạnh (Omachi, Chinsu). Masan (MSN) từ tập đoàn đa ngành lỗ retail (WCM) restructure 2022-2025: giảm đòn bẩy, focus core FMCG + Phúc Long. **Bài học**: MCH = crown jewel của MSN. Định giá MSN cần tách MCH (profitable) vs WCM (turnaround).

### Case 4 — SBT 2021-2024: Chu kỳ đường

Giá đường TG (ICE #11) tăng mạnh 2021-2023 + CBPG bảo hộ → SBT lãi kỷ lục. Giá đường giảm 2024 → lợi nhuận giảm theo. **Bài học**: SBT P/E thấp khi giá đường đỉnh là bẫy. Mua đường khi giá đáy (lỗ hoặc lãi thấp), bán khi giá đỉnh (lãi kỷ lục).

### Case 5 — QNS: Hai mảng trái ngược

QNS = Vinasoy (ổn định, growth 5-8%/năm, biên cao) + Đường (chu kỳ, biên thấp). Định giá QNS khó vì 2 mảng khác nhau. **Bài học**: SOTP (Sum-of-the-Parts) phù hợp hơn P/E thuần. Vinasoy định giá 15-18x, đường định giá 8-10x.

---

## Hướng dẫn tra dữ liệu thời gian thực (cho Master Food)

KB master này chỉ cung cấp framework + threshold + range historical. Khi viết bài quarter cụ thể, Master phải:

1. **Query KB framework** (file này + deep dive: NVL-cycle, Premium-transition, Seasonality) — static guidance.
2. **Query YAML** (`data/manual/targets.yaml`) — semi-static targets.
3. **Finpath API** cho data realtime:
   - `get_financial_ratios(ticker)` — biên gộp/EPS/PE/PB/ROE quarterly + yearly
   - `get_income_statement(ticker)` + `get_balance_sheet(ticker)` — BCTC quarter
   - `get_shareholders(ticker)` + `get_events(ticker)` + `get_news(ticker)` — ownership + ĐHĐCĐ + tin
4. **Web_search** cho data Finpath API không có:
   - Giá NVL thế giới (GDT bột sữa, ICE đường, mạch nha)
   - Market share update (Nielsen, Kantar)
   - Sản phẩm mới launch
   - Chính sách (thuế tiêu thụ đặc biệt, CBPG)

Pipeline log emit `data_trail` array: `{source, fetched, purpose, supports_argument}` per fact. KHÔNG bịa số.

---

## Cross-link

| Deep dive | Nội dung chính |
|---|---|
| [`food-nvl-cycle.md`](./food-nvl-cycle.md) | Chu kỳ giá NVL (bột sữa, mạch nha, đường); impact lên biên gộp |
| [`food-premium-transition.md`](./food-premium-transition.md) | Xu hướng premium hoá; case VNM A2, MCH cao cấp |
| [`food-seasonality-pattern.md`](./food-seasonality-pattern.md) | Pattern mùa vụ từng phân khúc; Tết effect |

---

## Phần suy luận (cần verify)

Các điểm dưới đây rút từ framework + data historical — không có nguồn VN cite trực tiếp, cần verify khi đưa vào bài cụ thể:

- **"VNM yield 5-7%"** — range historical tổng hợp; số cụ thể phải tính từ giá realtime.
- **"MCH biên 40-50%"** — range nhiều năm; số cụ thể quý hiện tại phải fetch từ BCTC.
- **"Ngành F&B tăng 9.6% 2025"** — forecast từ iPOS/báo cáo ngành; thực tế có thể khác.
- **"688.800 tỷ DT 2024"** — số từ báo cáo ngành; verify với tổng DT các công ty niêm yết.
- **"P/E range F&B"** — analytical heuristic; cần cross-check với data thực.
