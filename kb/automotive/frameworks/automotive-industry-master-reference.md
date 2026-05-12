---
category: frameworks
title: "Automotive-Industry-Master-Reference"
last_updated: 2026-05-12
---
Master reference cho ngành Ô tô & Phụ tùng VN — mental model 6 lớp phân tích. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **VEA · HAX · HHS · SVC · TMT · DRC · SRC · CSM · PAC**. Thaco, VinFast KHÔNG niêm yết tại VN — ngành ô tô trên sàn chủ yếu = phân phối + phụ tùng + lốp.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Automotive/knowledge.md + web search 2025-2026 data |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Chuỗi giá trị

| Mắt xích | Đặc điểm | DN tiêu biểu |
|---|---|---|
| Linh kiện | 80-85% nhập khẩu (TQ, Nhật, Hàn, Thái); 15-20% nội địa | — |
| Lắp ráp | Liên doanh Toyota/Hyundai/Kia/Mazda; VinFast (niêm yết Mỹ); Thaco (chưa niêm yết) | VEA (cổ tức liên doanh) |
| Phân phối | Đại lý ủy quyền theo hãng; biên 5-10% | HAX (Mercedes, MG), HHS (xe TQ), SVC (Toyota, Ford) |
| Dịch vụ sau bán | Bảo dưỡng, sửa chữa, phụ tùng, bảo hiểm, đăng kiểm; biên 20-30% | SVC, CTF |
| Lốp/Ắc quy | Sản xuất; phụ thuộc giá cao su + số xe lưu hành | DRC, SRC, CSM, PAC |

**60-70% xe bán trả góp** → lãi suất là biến số #1 ảnh hưởng sức mua.

## 1.2 Doanh nghiệp niêm yết

### Phân phối xe

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| **VEA** | VEAM — Tổng Công ty Máy động lực và Máy nông nghiệp | Liên doanh Honda/Toyota/Ford; lợi nhuận cực kỳ ổn định từ cổ tức; tiền mặt khổng lồ; cổ tức tiền mặt cao nhất nhóm |
| **HAX** | Dịch vụ Ô tô Hàng Xanh | Mercedes (sang) + MG (phổ thông); biên mỏng 5-8%; 2024 DT +69% đạt 1.817 tỷ, LNST +54% đạt 34 tỷ; đang niêm yết công ty con MG |
| **SVC** | Savico | Đa hãng (Toyota, Ford, Volvo); DT ổn định; biên 6-10%; dịch vụ sau bán mạnh |
| **HHS** | Đầu tư Dịch vụ Hoàng Huy | Xe tải + xe TQ (DFSK, Changan); hưởng lợi xu hướng xe TQ giá rẻ; biên thấp |

### Sản xuất/Lắp ráp

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| **TMT** | Ô tô TMT | Sản xuất xe tải; 2024 lỗ 123 tỷ do tái cấu trúc + chuyển đổi Euro 5; recovery từ 2025 |

### Lốp xe

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| **DRC** | Cao su Đà Nẵng | Biên 20-30%; xuất khẩu ~40%; radial biên cao hơn; phụ thuộc giá cao su (40-50% giá thành) |
| **SRC** | Cao su Sao Vàng | Nội địa chủ yếu; bias tire; biên thấp hơn DRC |
| **CSM** | Casumina | Lốp xe máy + ô tô; thị trường miền Nam |

### Ắc quy

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| **PAC** | Pin Ắc quy Miền Nam | Ổn định theo số xe lưu hành; biên 15-20%; ít chu kỳ |

> **Decision rule phân loại**: Phân phối = biên mỏng (5-10%) nhưng DT lớn, nhạy LPTB + lãi suất. Lốp = biên dày (20-30%) nhưng nhạy giá cao su. VEA = play cổ tức thuần từ liên doanh, ít biến động.

## 1.3 Biến số quyết định

### Tier 1 — Phản ứng ngay

| Biến số | Cơ chế | Ngưỡng |
|---|---|---|
| **Lãi suất cho vay mua xe** | 70% trả góp → lãi suất +1% = trả góp +500k-1tr/tháng | 7-10%/năm bình thường |
| **LPTB (lệ phí trước bạ)** | Giảm 50% LPTB → sản lượng +20-30% ngay | Thường áp dụng 6-12 tháng |
| **Thuế TTĐB** | 35-150% theo dung tích; xe điện miễn đến 2027 | — |
| **Sản lượng VAMA** | Benchmark ngành; >400k xe/năm = tốt | 2025: 604k xe (+22% YoY) |

### Tier 2 — Phản ứng 1-3 quý

| Biến số | Cơ chế |
|---|---|
| Tỷ giá USD/JPY | Xe Nhật = ~40% thị trường; JPY yếu = xe Nhật rẻ hơn |
| Giá cao su | 40-50% giá thành lốp; cao su +20% = biên lốp -5-8 đpt |
| Tồn kho xe | Tồn kho cao = áp lực giảm giá + promotion |
| Mix sản phẩm | Hybrid/EV tỷ trọng tăng = dynamic giá mới |

### Tier 3 — Dài hạn

| Biến số | Cơ chế |
|---|---|
| Tỷ lệ sở hữu/1.000 dân | VN: 50 (Thái: 250, Malaysia: 400) → dư địa gấp 5-10x |
| GDP/người | >$4.000/người = ngưỡng motorization tăng tốc |
| Số xe lưu hành | 5-6 triệu xe (+10-15%/năm) → nhu cầu lốp/dịch vụ tăng đều |
| Tỷ lệ EV/Hybrid | 2025: 40% xe du lịch mới là EV+Hybrid |

## 1.4 Đặc thù thị trường Việt Nam

- **Motorization sớm**: 50 xe/1.000 dân (Thái 250, Malaysia 400) → dư địa cấu trúc gấp 5-10x
- **Nội địa hóa thấp**: 80-85% linh kiện nhập → nhạy tỷ giá
- **Mùa vụ rõ**: T7 (Ngâu) thấp nhất | T10-T12 cao nhất | T1-T3 thấp sau Tết
- **Xe TQ xâm nhập**: 2025 thị phần tăng nhanh (DFSK, MG, BYD) → đe dọa Nhật/Hàn, tốt cho HHS
- **EV/Hybrid bùng nổ**: 2025 chiếm ~40% xe du lịch; miễn LPTB 100% đến 28/2/2027

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics quan trọng

**Tier 1 — Thị trường phản ứng ngay**:
1. Sản lượng toàn TT (VAMA + VinFast + TC Motor): >400k xe/năm = tốt; 2025: 604k (+22%)
2. Sản lượng theo DN/hãng (VAMA monthly report)
3. Lãi suất cho vay mua xe: 7-10%/năm bình thường
4. Biên gộp: Phân phối 5-10% | Lốp 20-30% | Phụ tùng/DV 15-25%
5. Chính sách LPTB/TTĐB

**Tier 2**: Tỷ giá USD/JPY, Tồn kho xe, DT dịch vụ sau bán, Mix sản phẩm (EV/Hybrid %), Giá cao su

**Tier 3 (dài hạn)**: Tỷ lệ sở hữu/1.000 dân, GDP/người, Số xe lưu hành, Thị phần xe TQ

## 2.2 Đọc số theo phân khúc

### Phân phối (HAX, HHS, SVC)

```
Lợi nhuận = Sản lượng × Biên/xe + DT dịch vụ sau bán
```

Check list:
- Tồn kho (>60 ngày = áp lực)
- DT dịch vụ % tổng DT (>15% = healthy)
- LPTB có ưu đãi không?
- Lãi suất cho vay mua xe trend?

### Lốp (DRC, SRC)

```
Lợi nhuận = Sản lượng × (Giá bán − Giá cao su)
```

Check list:
- Giá cao su (40-50% giá thành) — cao su giảm = biên nở
- DRC xuất khẩu ~40% → USD/VND ảnh hưởng
- Tỷ lệ radial (biên cao hơn bias)
- Số xe lưu hành (nhu cầu thay thế)

### VEA (play cổ tức)

```
Lợi nhuận = Cổ tức từ liên doanh Honda/Toyota/Ford
```

Check list:
- Honda/Toyota thị phần VN (>50% cộng gộp)
- Chính sách chia cổ tức VEA (tiền mặt cao)
- Không cần phân tích sâu BCTC — VEA = hold for dividend

## 2.3 Bẫy phổ biến

| Bẫy | Thực tế |
|---|---|
| Sản lượng +20% | Do LPTB giảm → hết ưu đãi sẽ giảm ("vay mượn" tương lai) |
| DT đột biến 1 quý | 1-2 deal lớn hoặc campaign, không bền |
| DRC biên 28% | Cao su đang rẻ → tạm thời; cao su tăng sẽ nén biên |
| T7 giảm 30% | Tháng Ngâu = bình thường, so cùng kỳ T7 |
| "TT bão hòa" | SAI — VN 50 xe/1.000 dân, dư địa gấp 5-10x |
| HAX lãi +54% | Từ nền thấp 2023; biên vẫn mỏng 1.9% |
| TMT lỗ kỷ lục | Tái cấu trúc Euro 5; recovery từ 2025 |

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Nguyên tắc cốt lõi

```
Ô tô = ngành CHU KỲ gắn với: Lãi suất + GDP + Chính sách
Cổ phiếu chạy TRƯỚC sản lượng:
- Tăng khi có tin kích cầu (dù sản lượng vẫn thấp)
- Giảm khi hết ưu đãi/lãi suất tăng (dù sản lượng vẫn cao)

Dài hạn: Motorization = xu hướng CẤU TRÚC (50 → 100-200 xe/1.000 dân trong 10-15 năm)
```

## 3.2 Bốn giai đoạn chu kỳ

| Giai đoạn | Đặc điểm | Tín hiệu | Phản ứng CP |
|---|---|---|---|
| **1. Đáy** | Lãi suất cao, sản lượng -15-25%, tồn kho cao | VAMA giảm YoY 3+ tháng | Bắt đầu tăng khi có tin kích cầu |
| **2. Hồi phục** | Lãi suất giảm, LPTB giảm, sản lượng +20-30% | NHNN hạ lãi suất, giảm LPTB | **TĂNG MẠNH NHẤT** (2-4 quý) |
| **3. Tăng trưởng** | Sản lượng cao ổn định, lãi suất thấp | VAMA tăng đều, tồn kho cân bằng | Tăng chậm, sideways |
| **4. Đỉnh → Suy** | Lãi suất tăng, hết LPTB, tồn kho tăng | NHNN nâng lãi suất, hết ưu đãi | Giảm TRƯỚC sản lượng |

## 3.3 Tín hiệu sớm

**Hồi phục (bullish)**:
- NHNN hạ lãi suất điều hành
- Chính phủ giảm LPTB/TTĐB
- Tồn kho đại lý giảm
- Xe mới hot ra mắt
- GDP tăng trên 6%
- VAMA tăng YoY

**Gặp khó (bearish)**:
- NHNN tăng lãi suất
- Hết ưu đãi LPTB
- Tồn kho tăng
- USD/JPY tăng mạnh
- Kinh tế yếu, tiêu dùng giảm
- Thuế TTĐB tăng

---

# LỚP 4: VĨ MÔ

## 4.1 Ma trận tác động

| Yếu tố vĩ mô | Phân phối (HAX/SVC) | Xe TQ (HHS) | Lốp (DRC) | VEA |
|---|---|---|---|---|
| Lãi suất giảm | +++ | ++ | 0 | + |
| Lãi suất tăng | --- | -- | 0 | - |
| Giảm LPTB | +++ | ++ | + | ++ |
| Hết LPTB | --- | -- | 0 | -- |
| USD/JPY tăng | -- | 0 | 0 | - |
| Cao su tăng | 0 | 0 | --- | 0 |
| Xe TQ thị phần tăng | - | +++ | 0 | - |
| EV/Hybrid bùng nổ | - (nếu không có EV) | + | - (EV ít hao lốp) | + (có liên doanh) |

## 4.2 Động lực tăng trưởng

**Cấu trúc (dài hạn)**:
- Motorization: 50 → 100-200 xe/1.000 dân
- GDP/người vượt $4.000
- Đô thị hóa + cao tốc mới
- Xe TQ phổ cập → giá xe giảm
- EV transition (miễn LPTB đến 2027, có thể kéo dài 2030)
- Số xe lưu hành tăng → lốp/dịch vụ tăng

**Chu kỳ (ngắn hạn)**:
- Giảm LPTB/TTĐB
- Lãi suất giảm
- Xe mới hot
- Peak cuối năm (T10-T12)

## 4.3 Rủi ro

- Lãi suất tăng đột biến
- Hết ưu đãi LPTB/TTĐB
- Xe TQ đe dọa Nhật/Hàn (tốt HHS, xấu SVC)
- Tỷ giá tăng mạnh
- Thuế TTĐB tăng
- Giá cao su tăng (ảnh hưởng DRC/SRC)
- Kinh tế yếu, tiêu dùng giảm
- EV transition làm giảm nhu cầu phụ tùng ICE

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 P/E Benchmark

| Nhóm | P/E range | Ghi chú |
|---|---|---|
| VEA | 8-12x | Ổn định, dividend play |
| HAX | 8-15x | Biến động theo campaign |
| HHS | 8-14x | Xe TQ, growth chưa chứng minh |
| SVC | 8-12x | Đa hãng, ổn định |
| DRC | 8-14x | Chu kỳ cao su |
| PAC | 8-12x | Ổn định |
| TMT | 10-18x (khi có lãi) | Recovery play |

## 5.2 P/E theo chu kỳ

| Pha | P/E | Hành động |
|---|---|---|
| Đáy (E thấp) | 15-20x | MUA — P/E cao nhưng E sắp hồi |
| Hồi phục | 10-15x | HOLD — E đang tăng |
| Đỉnh (E cao) | 6-10x | CẨN THẬN — P/E thấp nhưng E sắp giảm |

## 5.3 Bẫy định giá

| Bẫy | Giải thích |
|---|---|
| HAX P/E 8x "rẻ" | E đang đỉnh do LPTB kích cầu; hết ưu đãi E sẽ giảm |
| DRC P/E 9x "rẻ" | Cao su đang rẻ → biên tốt tạm thời; cao su tăng biên sẽ giảm |
| TMT P/E N/A | Đang lỗ; xem recovery roadmap, không dùng P/E |

**Mua đúng thời điểm**:
- Phân phối: Lãi suất đáy + LPTB sắp giảm + GDP tăng
- DRC: Cao su đáy + xe lưu hành tăng + radial tỷ trọng tăng

---

# LỚP 6: TƯ VẤN

## 6.1 Phân biệt tình huống

| Tình huống | Đánh giá |
|---|---|
| T7 giảm 25% | Tháng Ngâu — bình thường, so cùng kỳ |
| Giảm 3 tháng liên tiếp | Xu hướng — check lãi suất + chính sách |
| LPTB → sản lượng +30% | Tốt nhưng "vay mượn" tương lai |
| Xe TQ 5%→15% thị phần | Cấu trúc — tốt HHS, đe dọa Nhật/Hàn |
| Lãi suất +2% | Nghiêm trọng — trả góp +1tr/tháng |
| EV/Hybrid 40% xe mới | Transition — check portfolio DN có EV không |

## 6.2 Theo profile NĐT

**Dài hạn (>1 năm)**:
- VEA: Dividend play ổn định từ liên doanh
- DRC: Lốp, growth cấu trúc từ xe lưu hành
- SVC: Đa hãng + dịch vụ sau bán
- Tránh: HAX (nhạy campaign), HHS (xe TQ chưa chứng minh)

**Trung hạn (3-12 tháng)**:
- VÀO: Lãi suất giảm + LPTB giảm + tồn kho giảm
- THOÁT: Lãi suất tăng + hết LPTB + tồn kho tăng

**Ngắn hạn (<3 tháng)**:
- Mua T8-T9 trước peak T10-T12
- Tránh T7 (Ngâu)
- Catalyst: LPTB, xe mới hot, tin đại lý mới

## 6.3 Khi nào VÀO/THOÁT

**VÀO phân phối** (đạt 2-3/6):
- [ ] Lãi suất giảm
- [ ] LPTB giảm
- [ ] Tồn kho giảm
- [ ] VAMA tăng YoY
- [ ] Xe mới hot
- [ ] GDP tăng >6%

**VÀO DRC** (đạt 2-3/4):
- [ ] Cao su đáy
- [ ] Xe lưu hành +>10%
- [ ] Xuất khẩu tăng
- [ ] Radial tỷ trọng tăng

**THOÁT** (đạt 2-3/5):
- [ ] Lãi suất tăng
- [ ] Hết LPTB
- [ ] Tồn kho tăng
- [ ] VAMA giảm 2-3 tháng liên tiếp
- [ ] USD/JPY tăng mạnh

## 6.4 Dịch thuật ngữ cho NĐT

| Thuật ngữ | Diễn giải |
|---|---|
| LPTB | Lệ phí trước bạ — phí đăng ký xe, thường 10-12% giá xe |
| TTĐB | Thuế tiêu thụ đặc biệt — 35-150% theo dung tích động cơ |
| Motorization | Giai đoạn chuyển từ xe máy sang ô tô — VN đang ở đầu |
| Tháng Ngâu | T7 âm lịch — kiêng mua xe → doanh số thấp nhất năm |
| 50 xe/1.000 dân | Trong 1.000 người VN chỉ 50 có ô tô (Thái 250) → còn dư địa |
| DT dịch vụ | Doanh thu bảo dưỡng, sửa chữa — recurring, biên cao |
| Lốp radial | Lốp cao cấp, bền, êm — giá bán cao, biên tốt hơn bias |
| EV/BEV | Xe điện chạy pin — miễn LPTB 100% đến 2027 |
| Hybrid | Xe xăng + điện — tiết kiệm nhiên liệu, xu hướng 2025-2026 |
| VAMA | Hiệp hội các nhà sản xuất ô tô VN — báo cáo sản lượng monthly |

---

# PHỤ LỤC

## A. Severity Rating

| green | yellow | red |
|---|---|---|
| Sản lượng + biên tăng | Sản lượng tăng nhờ LPTB (tạm thời) | Sản lượng giảm + lãi suất tăng |
| LPTB/lãi suất giảm | Biên giảm nhẹ do cạnh tranh | Tồn kho tăng mạnh |
| Tồn kho giảm | Xe TQ tăng share (chưa rõ tác động) | Hết LPTB + lãi suất tăng |
| DT dịch vụ tăng | Cao su tăng nhẹ | LN giảm/lỗ |

## B. Câu mẫu

**LPTB kích cầu**:
"Thị trường bán {X}k xe, +{Y}% so cùng kỳ — nhờ giảm 50% lệ phí trước bạ. {ticker} sản lượng +{Z}%. Tuy nhiên ưu đãi có thể hết cuối năm → một phần đã 'vay mượn' trước từ tương lai."

**Lãi suất giảm**:
"Lãi suất vay mua xe giảm từ {X}% xuống {Y}% — trả góp giảm khoảng {Z} triệu/tháng. {ticker} bán {W} xe, +{V}% so cùng kỳ."

**DRC cao su**:
"{ticker} lãi +{X}% nhờ giá cao su (chiếm 40-50% chi phí) giảm {Y}%. Nhu cầu lốp thay thế +{Z}% vì số xe lưu hành tăng đều ~10-15%/năm."

**Motorization**:
"Việt Nam có 50 xe/1.000 dân (Thái 250, Malaysia 400). Thu nhập tăng → chuyển từ xe máy sang ô tô. {ticker} hưởng lợi khi thị trường tăng 2-3 lần trong thập kỷ tới."

**EV transition**:
"Xe điện và hybrid chiếm gần 40% xe du lịch mới trong năm 2025. Ưu đãi miễn lệ phí trước bạ kéo dài đến 28/2/2027, có thể đến 2030. {ticker} cần theo kịp xu hướng điện hóa."

## C. Quy tắc Agent

1. **60-70% trả góp** → LÃI SUẤT = biến số #1
2. **LPTB giảm** = kích cầu NGAY nhưng "vay mượn" tương lai
3. **T7 Ngâu** LUÔN thấp → so cùng kỳ, đừng hoảng
4. **VN motorization** mới bắt đầu → dài hạn TĂNG TRƯỞNG CẤU TRÚC
5. **Biên phân phối MỎNG** (5-10%) → DT dịch vụ QUAN TRỌNG hơn bán xe
6. **DRC** = chu kỳ cao su + growth cấu trúc (xe lưu hành tăng)
7. **Xe TQ** = tốt HHS, đe dọa đại lý Nhật/Hàn
8. **EV/Hybrid** 40% xe mới 2025 → xu hướng không thể đảo ngược
9. **KHÔNG dùng thuật ngữ** → PHẢI dịch cho NĐT hiểu
10. **KHÔNG bịa data** → Thiếu → nói thiếu

---

## Hướng dẫn tra dữ liệu thời gian thực

KB này chỉ cung cấp framework + threshold. Khi viết bài quý cụ thể, cần:

1. **VAMA Monthly Report** (vama.org.vn): Sản lượng tháng/quý/năm
2. **Finpath API**:
   - `get_income_statement(ticker)` + `get_balance_sheet(ticker)` — BCTC
   - `get_financial_ratios(ticker)` — P/E, P/B, ROE
   - `get_events(ticker)` + `get_news(ticker)` — sự kiện, tin tức
3. **Web search**:
   - Giá cao su (cao su RSS3, cao su TSR20)
   - Chính sách LPTB/TTĐB mới nhất
   - Lãi suất cho vay mua xe các ngân hàng
   - Sản lượng VinFast, TC Motor (ngoài VAMA)

---

## Cross-link

| Liên quan | Mục đích |
|---|---|
| `kb/automotive/per-ticker/` | KB chi tiết từng mã (nếu có) |
| VAMA (vama.org.vn) | Sản lượng monthly official |
| `data/manual/` | YAML targets/events nếu cần |
