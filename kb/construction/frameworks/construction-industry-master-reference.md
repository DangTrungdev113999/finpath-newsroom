---
category: frameworks
title: "Construction-Industry-Master-Reference"
last_updated: 2026-05-12
---

Master reference cho Master Construction — mental model 6 lớp phân tích ngành Xây dựng & VLXD Việt Nam. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **CTD · HBC · VCG · FCN · HUT · PC1 · LCG**. Ngành xây dựng gắn chặt với chu kỳ bất động sản (60-70%) và đầu tư công (30-40%).

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Construction/knowledge.md + web search bổ sung data 2025-2026. |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Chuỗi giá trị

- **Upstream (VLXD):** Xi măng, thép, gạch, kính, ống nhựa, sơn
  - DN: HPG, HSG, NKG (thép), HT1, BCC, HOM (xi măng), BMP, NTP (ống nhựa), VGC (kính)
- **Midstream (Xây dựng):** Thi công nhà ở, chung cư, cầu đường, sân bay, metro
  - DN: CTD, HBC, VCG (dân dụng), FCN, PC1 (hạ tầng)
- **Downstream:** BĐS (VHM, NVL, KDH) + Đầu tư công (cao tốc, sân bay, metro)

## 1.2 Phân loại doanh nghiệp

| Phân khúc | DN tiêu biểu | Đặc thù |
|---|---|---|
| Thép XD | HPG, HSG, NKG, TLH | Chu kỳ, phụ thuộc giá thép + BĐS + ĐTC |
| Xi măng | HT1, BCC, HOM | Cung > cầu, cạnh tranh giá |
| Ống nhựa | BMP, NTP | Ổn định, BMP+NTP >50% thị phần |
| Kính | VGC | Phụ thuộc BĐS thương mại |
| Nhà thầu dân dụng | CTD, HBC, VCG | Biên mỏng 5-8%, rủi ro chậm thanh toán |
| Hạ tầng | FCN, PC1, LCG, HUT | Phụ thuộc đầu tư công |

### Nhà thầu lớn niêm yết (2025-2026)

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| **CTD** | Coteccons | Nhà thầu dân dụng lớn nhất; backlog 62.500 tỷ (kỷ lục 2026); biên gộp cải thiện từ 6% lên 8% |
| **HBC** | Hòa Bình | Top 2 nhà thầu dân dụng; tái cấu trúc 2023-2024; target 2026: DT 10.000 tỷ, LN 250 tỷ |
| **VCG** | Vinaconex | Đa ngành (xây dựng + BĐS); backlog ~25.000 tỷ; LN cao nhất ngành 2025 |
| **FCN** | FECON | Chuyên nền móng + hạ tầng ngầm; hưởng lợi đầu tư công |
| **PC1** | Power Construction 1 | Hạ tầng điện + năng lượng; đa dạng hóa sang BĐS KCN |
| **LCG** | Licogi 16 | Hạ tầng giao thông; backlog 7.000 tỷ (+22% YoY) |
| **HUT** | Tasco | Hạ tầng giao thông; BOT cao tốc |

## 1.3 Ai quyết định luật chơi

- **BĐS (60-70% nhu cầu):** BĐS tốt → triển khai dự án → mua VLXD + thuê nhà thầu
- **Đầu tư công (30-40%):** Giải ngân tăng → xi măng, thép, nhà thầu hạ tầng hưởng lợi; là "phao cứu sinh" khi BĐS yếu
- **Giá NVL:** Thép (quặng sắt + than cốc ~60-70%), xi măng (than ~30-40%), ống nhựa (hạt nhựa PVC/PE)
- **Cạnh tranh TQ:** Thép TQ giá rẻ ép giá nội địa, thuế CBPG là "lá chắn"

## 1.4 Đặc thù ngành VN

- **Xây dựng:** Phân mảnh (top 5 ~10% thị trường), biên mỏng 5-8%, rủi ro chậm thanh toán, dòng tiền thường âm, Q3 mùa mưa yếu nhất
- **Thép:** HPG ~35% thị phần nội địa; DQ2 vận hành từ 2024 tăng công suất HRC
- **Xi măng:** Công suất ~110 triệu tấn, nhu cầu ~65-70 triệu tấn, xuất khẩu ~35-40 triệu tấn
- **Ống nhựa:** Ổn định, BMP + NTP >50% thị phần

## 1.5 Mùa vụ

| Quý | Xây dựng | Thép | Xi măng | Ống nhựa |
|---|---|---|---|---|
| Q1 | Thấp (sau Tết) | Thấp | Thấp | Thấp |
| Q2 | Tăng | Cao | Cao | Tăng |
| Q3 | **Thấp nhất (mùa mưa)** | Giảm | Giảm | TB |
| Q4 | **Cao nhất** | Cao | Cao nhất | Cao nhất |

**Quy tắc:** So cùng kỳ, KHÔNG so quý liền trước.

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics quan trọng

### Tier 1 — Phản ứng ngay

| Metric | Ý nghĩa | Benchmark |
|---|---|---|
| **Backlog** | DT tương lai đảm bảo | Tăng → tốt; CTD 62.500 tỷ (kỷ lục 2026), VCG 25.000 tỷ |
| **Giá bán SP** | Giá thép, xi măng, ống | So cùng kỳ + giá đầu vào |
| **Sản lượng tiêu thụ** | Tấn bán được | So KH + cùng kỳ |
| **Biên gộp** | Thép 12-18%, xi măng 25-35%, ống 30-40%, nhà thầu 5-8% (trung bình 8.2% 2024) |
| **Giải ngân ĐTC** | Vốn nhà nước giải ngân | 2025: >95% KH (~80.700 tỷ); 2026 KH: 930.000 tỷ (+20% YoY) |

### Tier 2 — Phản ứng chậm

| Metric | Benchmark |
|---|---|
| Giá NVL | Tăng → ép biên, giảm → biên mở |
| Phải thu KH | Nhà thầu: >40% DT = nguy hiểm; áp lực thu hồi công nợ tăng 2025-2026 |
| CFO | Âm nhiều năm = đáng lo |
| Nợ vay/Vốn chủ | >1.5x = rủi ro cao; ngành Debt/EBITDA trung bình 5.3x (2024) |
| Tỷ lệ XK | Xi măng 40-50%, HPG 20-30% |
| Interest coverage | Ngành trung bình 2.7x (2024, cải thiện từ 1.5x 2023) |

### Tier 3 — Dài hạn

- Công suất mới, pipeline ĐTC, thị phần, thuế CBPG
- Backlog growth (MBS dự báo +24% YoY 2026)
- Quy mô ngành: 633.750 tỷ VND (2024) → dự kiến 1.014.795 tỷ VND (2029), CAGR 7.6%

## 2.2 Đọc số theo phân khúc

### Thép (HPG, HSG, NKG)

- Công thức: Giá bán × Sản lượng − Giá NVL
- Check: Giá thép nội địa, HRC VN vs TQ, quặng sắt + than cốc, sản lượng, thuế CBPG
- HPG: Tách thép XD / HRC / ống thép / tôn mạ / nông nghiệp / BĐS

### Xi măng (HT1, BCC, HOM)

- Công thức: Sản lượng × Giá bán − Chi phí than
- Check: Sản lượng nội địa + XK, giá than (30-40% giá thành), cung vs cầu, giá XK vs nội địa

### Ống nhựa (BMP, NTP)

- Công thức: Sản lượng × Giá bán − Giá hạt nhựa
- Check: Giá PVC/PE/PP, sản lượng, thị phần, nhu cầu hạ tầng nước + BĐS

### Nhà thầu (CTD, HBC, VCG)

- Focus: Backlog + Biên LN + Dòng tiền + Phải thu
- Biên gộp <5% = quá cạnh tranh, >10% = tốt
- Phải thu >40% DT = rủi ro, CFO âm nhiều năm = "ứng tiền cho chủ đầu tư"
- 2025: DT toàn ngành >186.900 tỷ (+16%), LN >10.100 tỷ (+93%)

### Hạ tầng (FCN, PC1, LCG, HUT)

- Focus: Giải ngân ĐTC + Backlog
- Backlog nhà nước an toàn hơn BĐS tư nhân

## 2.3 Bẫy phổ biến

| Bẫy | Thực tế |
|---|---|
| HPG DT tăng 30% | Có thể vì giá tăng, SL không đổi → check tấn |
| CTD backlog kỷ lục | Margin thấp → DT cao, LN không tăng |
| HT1 LN tăng 50% | Giá than giảm tạm thời → không bền |
| HBC DT/LN tăng | Phải thu cũng tăng = nợ nhiều hơn → check CFO |
| Xi măng XK tốt | Giá XK thường thấp hơn nội địa |
| ĐTC tăng 20% | Kế hoạch ≠ giải ngân thực |

## 2.4 Checklist BCTC (8 câu hỏi)

1. Xác định phân khúc (VLXD hay nhà thầu?)
2. Giá đầu vào + đầu ra → biên LN
3. Sản lượng (tấn) so cùng kỳ + KH
4. Backlog (nhà thầu) — tăng/giảm? Nguồn từ BĐS tư nhân hay nhà nước?
5. Dòng tiền + Phải thu — CFO âm bao lâu? Phải thu % DT?
6. Giải ngân ĐTC thực tế (so KH)
7. BĐS hồi phục hay đóng băng
8. Vĩ mô: giá NVL, lãi suất, tỷ giá, thuế CBPG

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Nguyên tắc cốt lõi

```
Ngành chu kỳ: Gắn BĐS (60-70%) + ĐTC (30-40%) + giá NVL
Giá CP chạy trước: Tăng khi BĐS mới bắt đầu hồi (dù DT chưa tăng), giảm khi BĐS mới chậm (dù DT vẫn tốt)
ĐTC là phao cứu sinh: Bù đắp khi BĐS yếu
```

## 3.2 Bốn giai đoạn chu kỳ

| Giai đoạn | Đặc điểm | Giá CP |
|---|---|---|
| **1. Đáy** | BĐS đóng băng, VLXD ế, nhà thầu mất HĐ, ĐTC bù đắp | Bắt đầu tăng dù DT/LN vẫn xấu |
| **2. Hồi phục** | BĐS tan băng, nhu cầu + giá tăng, backlog tăng | **Tăng mạnh nhất** (4-8 quý) |
| **3. Tăng trưởng** | BĐS sôi động, VLXD bán chạy, backlog kỷ lục | Tăng chậm/đi ngang |
| **4. Đỉnh → Suy giảm** | BĐS chậm, tồn kho tăng, HĐ mới ít | Giảm dù DT vẫn tốt |

## 3.3 Lịch sử chu kỳ HPG (benchmark)

| Giai đoạn | Thời điểm | KQKD | Giá CP |
|---|---|---|---|
| Đỉnh | Q1-Q2/2022 | LN kỷ lục | 48k (đỉnh) |
| Suy giảm | Q3/22-Q1/23 | LN giảm 70-80% | 48k → 20k |
| Đáy | Q2-Q3/2023 | LN thấp nhất | ~20k |
| Hồi phục | Q4/23-2024 | LN phục hồi, DQ2 vận hành | 20k → 30k |
| Tăng trưởng | 2025 | SL kỷ lục, LN +19% | 27k → 32k |

## 3.4 Tín hiệu sớm

### Đáy hình thành

- Lãi suất giảm, chính sách tháo gỡ BĐS, giải ngân ĐTC tăng
- Giá VLXD ổn định, tồn kho giảm, giao dịch BĐS tăng, insider mua CP

### Đỉnh hình thành

- Lãi suất tăng + siết tín dụng BĐS, giao dịch BĐS chậm
- Nhà máy mới vận hành (cung tăng), giá NVL tăng mạnh
- Phải thu nhà thầu tăng đột biến, insider bán CP

## 3.5 Ma trận kịch bản

| Kịch bản | Kết quả | VD |
|---|---|---|
| BĐS tốt + ĐTC tốt | Bùng nổ | 2021 |
| BĐS yếu + ĐTC tốt | Ổn định | 2023-2024 |
| BĐS yếu + ĐTC yếu | Đáy sâu | Q3-Q4/2022 |
| BĐS tốt + ĐTC yếu | Phục hồi thiếu bền | — |

---

# LỚP 4: HIỂU VĨ MÔ

## 4.1 Yếu tố vĩ mô tác động

| Yếu tố | Tác động |
|---|---|
| **BĐS dân dụng** | #1 — 60-70% nhu cầu |
| **Đầu tư công** | #2 — 30-40% nhu cầu; 2026 KH 930.000 tỷ (+20% YoY) |
| **Lãi suất** | Giảm → BĐS hồi → VLXD tăng |
| **Giá NVL thế giới** | Quặng sắt, than, hạt nhựa — global supply chain disruptions |
| **Tỷ giá USD/VND** | NVL nhập USD, USD tăng → chi phí tăng |
| **Thuế CBPG thép TQ** | Bảo vệ thép nội địa |
| **Chính sách BĐS** | Luật, tín dụng, phê duyệt dự án |

## 4.2 Ma trận ảnh hưởng

| Yếu tố | HPG | HT1 | BMP | CTD | FCN |
|---|---|---|---|---|---|
| BĐS hồi phục | ++ | + | + | ++ | ~ |
| ĐTC tăng | + | ++ | ~ | ~ | ++ |
| Giá NVL tăng | - | - | - | ~ | ~ |
| Lãi suất tăng | - | - | - | - | ~ |
| Thuế CBPG thép | ++ | ~ | ~ | ~ | ~ |
| Thép TQ rẻ tràn vào | -- | ~ | ~ | + | + |

## 4.3 Động lực tăng trưởng

### Cấu trúc (dài hạn)

- Đô thị hoá 40% → 50% (2030)
- Cao tốc Bắc-Nam 5.000km (2030)
- Sân bay Long Thành (2025-2026)
- Metro HN + TPHCM
- 1 triệu căn NOXH
- HPG mở rộng HRC (DQ2)
- 27 dự án BĐS quy mô lớn tổng vốn 115 tỷ USD (2025)

### Chu kỳ (ngắn hạn)

- Lãi suất giảm → BĐS hồi
- Giải ngân ĐTC đẩy mạnh Q4
- Giá NVL giảm → biên cải thiện
- Thuế CBPG thép TQ

## 4.4 Rủi ro

### Cấu trúc

- Xi măng cung > cầu kéo dài
- Thép TQ giá rẻ (nếu không có thuế CBPG)
- Nhà thầu phân mảnh, biên <5%
- Phải thu nhà thầu không thu hồi được
- Chi phí NVL tăng từ supply chain disruptions

### Chu kỳ

- BĐS đóng băng → VLXD giảm 30-40%
- ĐTC giải ngân chậm (site preparation, land pricing complexities)
- Giá NVL tăng mạnh
- Mùa mưa kéo dài
- Siết tín dụng BĐS

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 P/E ngành chu kỳ — Bẫy

- **Bẫy:** P/E thấp ≠ rẻ (có thể đỉnh chu kỳ, E sắp giảm)
- **Đáy:** P/E cao/âm → lúc MUA
- **Đỉnh:** P/E thấp nhất → lúc BÁN

## 5.2 Phương pháp theo phân khúc

| Phân khúc | Phương pháp |
|---|---|
| Thép | EV/EBITDA + Normalized P/E (E trung bình 5-7 năm) |
| Xi măng | P/E + EV/tấn công suất |
| Ống nhựa | P/E + Dividend yield |
| Nhà thầu | P/E + Backlog/Market cap |
| Hạ tầng | P/E + Pipeline dự án |

## 5.3 Benchmarks

**HPG EV/EBITDA:**
- Đáy: 12-15x | Hồi phục: 8-12x | Tăng trưởng: 6-10x | Đỉnh: 5-7x

**Nhà thầu Backlog/Mcap:**
- >1.5x → hấp dẫn | 0.8-1.5x → hợp lý | <0.8x → hết việc/quá đắt
- Lưu ý: Check margin + nguồn backlog (BĐS tư nhân rủi ro hơn nhà nước)

**Ống nhựa Dividend Yield:**
- >7% → hấp dẫn | 4-7% → hợp lý | <4% → đắt

**P/E theo giai đoạn:**
- Đáy: 15-25x/âm | Hồi phục: 10-18x | Tăng trưởng: 8-14x | Đỉnh: 6-10x

---

# LỚP 6: TƯ VẤN

## 6.1 Phân biệt rủi ro

| Tình huống | Loại | Phản ứng |
|---|---|---|
| Q3 DT giảm vs Q2 | Mùa mưa (bình thường) | Không lo |
| Giá thép giảm 1 tháng | Biến động ngắn | Theo dõi |
| Giá thép giảm 3 quý + BĐS yếu | Chu kỳ đảo chiều | Giảm vị thế |
| CTD phải thu tăng 4 quý + CFO âm | Cấu trúc | Cảnh báo mạnh |
| HPG LN kỷ lục | Có thể đỉnh | Check giá thép bền? BĐS chậm? |

## 6.2 Tư vấn theo profile

**Dài hạn (>1 năm):**
- Focus: Đô thị hoá, ĐTC, thị phần
- Ưu tiên: HPG, BMP | Tránh: Xi măng, nhà thầu nhỏ

**Trung hạn (3-12 tháng):**
- Vào: BĐS hồi + lãi suất giảm + giá NVL ổn
- Thoát: BĐS chậm + lãi suất tăng + NVL tăng mạnh

**Ngắn hạn (<3 tháng):**
- Focus: Giải ngân ĐTC Q4, giá thép, BCTC
- Q3 tránh nhà thầu, Q4 vào sớm

## 6.3 Tín hiệu VÀO (cần 2-3/7)

1. Lãi suất giảm + nới tín dụng BĐS
2. Chính sách tháo gỡ BĐS
3. Giao dịch BĐS tăng
4. Giải ngân ĐTC tăng mạnh
5. Giá VLXD ổn định
6. Tồn kho VLXD giảm
7. Insider mua CP

## 6.4 Tín hiệu THOÁT (cần 2-3/6)

1. Lãi suất tăng + siết tín dụng BĐS
2. BĐS chậm 2 quý liên tiếp
3. Giá NVL tăng mạnh
4. Nhà máy mới vận hành
5. Phải thu nhà thầu tăng đột biến
6. Insider bán CP

## 6.5 Dịch thuật ngữ cho NĐT retail

| Thuật ngữ | Dịch |
|---|---|
| Biên gộp tăng | Lời nhiều hơn trên mỗi tấn bán ra |
| Backlog tăng | Đã ký nhiều HĐ, đảm bảo có việc |
| Phải thu tăng | Khách nợ nhiều hơn, chưa trả |
| CFO âm | Chi > thu, phải vay để hoạt động |
| Thuế CBPG | Thuế đánh thép TQ giá rẻ → giúp thép VN bán giá tốt |
| Giải ngân ĐTC | Tiền nhà nước thực sự chi ra xây cầu đường |
| Cung > cầu | NM sản xuất nhiều hơn thị trường cần → phải giảm giá |
| DQ2 | Nhà máy Dung Quất 2 của HPG |
| HRC | Thép cuộn nóng — dùng sản xuất ống, tôn, container |

---

# PHỤ LỤC

## A. Severity cho Earnings Card

**Green:** SL tăng + giá ổn/tăng + NVL ổn/giảm; backlog tăng + biên ổn + phải thu không tăng bất thường; LN tăng từ HĐKD chính

**Yellow:** LN tăng do NVL giảm tạm thời; SL tăng + giá giảm; backlog tăng kèm phải thu tăng; ĐTC KH tốt nhưng giải ngân chậm

**Red:** SL + giá giảm; biên giảm mạnh; CFO âm + phải thu tăng vọt + nợ tăng; LN giảm/lỗ

## B. Câu mẫu

**HPG hưởng lợi:**
> "HPG bán {X} triệu tấn, +{Y}% so cùng kỳ nhờ DQ2 chạy {Z}% công suất. Thuế CBPG giúp thép VN bán giá tốt. LN +{W}% từ bán thép, không có bất thường."

**HT1 bị ép biên:**
> "HT1 bán {X} triệu tấn nhưng LN chỉ +{Y}% vì than (+{Z}%, chiếm >1/3 chi phí). Bán nhiều hơn nhưng lời ít hơn mỗi tấn."

**CTD backlog tăng + phải thu tăng:**
> "CTD ký thêm {X} tỷ, backlog kỷ lục — đảm bảo việc 2-3 năm. Tuy nhiên nợ KH cũng +{Y}% — nhiều chủ đầu tư BĐS chậm trả."

**Đáy chu kỳ:**
> "LN {ticker} -{X}%, quý giảm thứ {Y} do BĐS trầm lắng. Tuy nhiên lãi suất vừa hạ, luật đất đai mới, giải ngân ĐTC +{Z}%. Lịch sử: khi tín hiệu này xuất hiện, giá CP XD thường hồi trước KQKD."

**Đỉnh chu kỳ:**
> "LN {ticker} +{X}% nhưng tốc độ chậm lại (quý trước +{Y}%). Lãi suất bắt đầu tăng, giao dịch BĐS chậm 2 tháng. Khi BĐS chậm, VLXD thường giảm theo với độ trễ 1-2 quý."

## C. Quy tắc agent

1. KHÔNG đánh giá VLXD giống nhau → Thép ≠ Xi măng ≠ Ống nhựa ≠ Nhà thầu
2. KHÔNG chỉ nhìn DT → check sản lượng (tấn)
3. KHÔNG bỏ qua phải thu + CFO với nhà thầu
4. KHÔNG so Q3 với Q2 → LUÔN so cùng kỳ
5. KHÔNG tin KH ĐTC → check giải ngân thực tế
6. KHÔNG quên BĐS → 60-70% nhu cầu VLXD
7. KHÔNG dùng thuật ngữ với NĐT retail → dịch sang bình dân
8. KHÔNG bịa data → thiếu thì nói thiếu

## D. Data 2025-2026 (snapshot)

| Metric | 2024 | 2025 | 2026F |
|---|---|---|---|
| Tăng trưởng ngành XD | 7.2% | 9.62% | 7.1% |
| DT ngành (tỷ VND) | 633.750 | >186.900 (top niêm yết) | — |
| LN ngành (tỷ VND) | — | >10.100 (+93%) | — |
| Biên gộp trung bình | 7.4% | 8.2% | — |
| Giải ngân ĐTC | — | >95% KH (~80.700 tỷ) | KH 930.000 tỷ |
| Debt/EBITDA | 6.0x | 5.3x | — |
| Interest coverage | 1.5x | 2.7x | — |
| CTD backlog | 30.000 tỷ | 35.000 tỷ (H1) | 62.500 tỷ (Q2) |

---

## Hướng dẫn tra dữ liệu thời gian thực (cho Master Construction)

KB master này chỉ cung cấp framework + threshold + range historical. Khi viết bài quarter cụ thể, Master phải:

1. **Query KB framework** (file này) — static guidance.
2. **Finpath API** cho data realtime:
   - Backlog, doanh thu, LN từ BCTC quý
   - Giá NVL (thép, xi măng, hạt nhựa)
   - Phải thu, CFO, nợ vay
3. **Web_search** cho data không có trong API:
   - Giải ngân ĐTC thực tế (Bộ Tài chính)
   - Giá thép nội địa vs TQ
   - Thuế CBPG mới
   - Sự kiện BĐS (luật mới, dự án lớn)

Pipeline log V4.0 emit `data_trail` array: `{source, fetched, purpose, supports_argument}` per fact. KHÔNG bịa số.

---

## Sources (web search 2026-05-12)

- [Ngành xây dựng lập đỉnh lợi nhuận 2025](https://vietstock.vn/2026/02/nganh-xay-dung-lap-dinh-loi-nhuan-2025-ap-luc-thu-hoi-cong-no-ngay-cang-lon-737-1403205.htm)
- [HBC mục tiêu 2026](https://doanhnhan.baophapluat.vn/tap-doan-xay-dung-hoa-binh-hbc-dat-muc-tieu-2026-doanh-thu-10-000-ty-lai-250-ty-xac-dinh-ba-tru-cot-chien-luoc-xuyen-suot.html)
- [Backlog doanh nghiệp xây dựng](https://vneconomy.vn/soi-gia-tri-backlog-cua-cac-doanh-nghiep-nganh-xay-dung.htm)
- [VIS Rating ngành xây dựng 02/2025](https://visrating.com/tin-tuc/nganh-xay-dung-goc-nhin-tin-nhiem-02-2025.22.html)
- [Vietnam Construction Industry Report 2025](https://www.globenewswire.com/news-release/2026/01/27/3226697/28124/en/Vietnam-Construction-Industry-Report-2025-Market-Forecast-to-Expand-by-7-6-to-Reach-VND-1-014-795-5-Billion-by-2029.html)
- [Vietnam Infrastructure 2025](https://vietnam.incorp.asia/vietnam-infrastructure-and-construction-2025/)
