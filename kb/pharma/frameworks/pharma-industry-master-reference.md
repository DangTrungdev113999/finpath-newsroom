---
category: frameworks
title: "Pharma-Industry-Master-Reference"
last_updated: 2026-05-12
---

Master reference cho Master Pharma — mental model 6 lớp phân tích ngành dược phẩm VN. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **DHG · IMP · DMC · TRA · DBD · PME · OPC**.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Pharma/knowledge.md + web search enrichment. Điền đầy đủ 6 lớp + phụ lục. |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Đặc thù Dược VN vs Dược Mỹ/châu Âu

| Dược Mỹ/châu Âu | Dược VN |
|---|---|
| Nghiên cứu phát triển thuốc MỚI, chi phí tỷ đô | Sản xuất thuốc GENERIC (hết bản quyền) |
| Bằng sáng chế 10-20 năm, biên lợi nhuận gộp 70-80% | Biên lợi nhuận gộp 40-55%, cạnh tranh giá + kênh phân phối |
| Rủi ro nghiên cứu phát triển: 90% thất bại | KHÔNG nghiên cứu thuốc mới — tập trung sản xuất + phân phối |

**Kết luận cốt lõi**: Dược VN = SẢN XUẤT + PHÂN PHỐI thuốc generic. KHÔNG so sánh với Pfizer, Roche, Novartis.

## 1.2 Chuỗi giá trị

```
Nguyên liệu (API) → Sản xuất (GMP) → Phân phối (ETC/OTC) → Người dùng (BHYT 90%+)
```

| Khâu | Đặc điểm | Doanh nghiệp tiêu biểu |
|---|---|---|
| **Nguyên liệu (API)** | Nhập 90%+ từ Trung Quốc, Ấn Độ → biến số chi phí lớn nhất | — |
| **Sản xuất** | Nhà máy GMP (WHO-GMP, EU-GMP, PIC/S). EU-GMP = "vé VIP" | DHG, IMP, DMC, TRA, PME, DBD, OPC |
| **Phân phối ETC** | Bệnh viện: 65-70% thị trường, đấu thầu → giá bị ép, volume lớn | DN sản xuất + DNM, Zuellig Pharma |
| **Phân phối OTC** | Nhà thuốc: 30-35%, biên CAO hơn, phụ thuộc thương hiệu | DN sản xuất + Long Châu (FRT), An Khang (MWG) |
| **Xuất khẩu** | <5% — chưa phải mảng trọng yếu | — |

## 1.3 Phân loại doanh nghiệp

| Phân khúc | DN tiêu biểu | Đặc thù |
|---|---|---|
| **Sản xuất lớn** | DHG (#1 thị phần ~10%), IMP, DMC | EU-GMP nhiều, đấu thầu nhóm 1-2, OTC mạnh |
| **Sản xuất trung** | TRA, PME (Stada), DBD | TRA mạnh đông dược; DBD đột phá thuốc ung thư |
| **Đông dược** | TRA, OPC | Biên cao, xu hướng tự nhiên, ít phụ thuộc API nhập |
| **Phân phối** | DNM, Zuellig Pharma | Biên mỏng 5-10%, volume lớn |
| **Chuỗi nhà thuốc** | FRT (Long Châu), MWG (An Khang) | Xem KB Bán lẻ — không thuộc universe Dược |

## 1.4 Ai quyết định luật chơi

| Chủ thể | Vai trò | Tác động |
|---|---|---|
| **Bộ Y tế + Cục Quản lý Dược** | Phê duyệt visa thuốc, quy định đấu thầu, giá trần, danh mục BHYT | Quyết định sống/chết doanh nghiệp |
| **Đấu thầu bệnh viện** | 65-70% thị trường, phân nhóm 1-5 theo tiêu chí kỹ thuật | Nhóm 1 (EU-GMP): giá cao, ít cạnh tranh; Nhóm 3-5 (WHO-GMP): giá thấp, cạnh tranh khốc liệt |
| **BHYT** | 90%+ dân số có BHYT → thuốc trong danh mục mới bán được ở bệnh viện | Mở rộng danh mục = cơ hội; thu hẹp = rủi ro |
| **TQ + Ấn Độ** | 90%+ API nhập khẩu | Siết nguồn cung → giá tăng; USD tăng → chi phí tăng |

## 1.5 Đặc thù thị trường Việt Nam

- **Nhu cầu thiết yếu**: Doanh thu ngành tăng đều 8-12%/năm, ngành PHÒNG THỦ
- **Chi tiêu dược thấp**: VN ~70-80 USD/người (Thái Lan ~140 USD) → dư địa tăng trưởng gấp đôi
- **90% API nhập khẩu**: Phụ thuộc TQ/Ấn Độ + tỷ giá USD/VND
- **EU-GMP = Lợi thế #1**: Chỉ 5-7 DN đạt → "câu lạc bộ VIP" đấu thầu nhóm 1
- **Đấu thầu = Game #1**: Trúng/trượt = sống/chết với kênh ETC
- **Quy mô thị trường 2025**: ~7.5 tỷ USD, chiếm ~1.78% GDP, 32.2% chi tiêu y tế

## 1.6 Mùa vụ

| Quý | Đặc điểm |
|---|---|
| Q1 | **Thấp nhất** — sau Tết Âm lịch, đấu thầu bệnh viện chưa xong |
| Q2-Q3 | Tăng dần — mùa dịch, cảm cúm |
| Q4 | **Cao nhất** — bệnh viện đẩy mua cuối năm + mùa cúm |

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics quan trọng

### Tier 1 — Thị trường phản ứng ngay

| Metric | Benchmark | Ý nghĩa |
|---|---|---|
| Tăng trưởng doanh thu | Ngành 8-12%, >12% = tốt | So với benchmark ngành |
| Biên lợi nhuận gộp | DHG: 50-55%, IMP: 45-50%, TB: 40-50% | Phản ánh mix ETC/OTC + EU-GMP |
| Tỷ trọng ETC/OTC | DHG: OTC 60%, ETC 40% | OTC cao = biên cao + ổn định |
| Kết quả đấu thầu | Trúng nhiều = doanh thu ổn định | Trượt nhiều gói = báo động |
| Số sản phẩm EU-GMP | Nhiều → nhóm 1 → biên cao | Lợi thế cấu trúc |

### Tier 2 — Phản ứng 1-3 quý

| Metric | Ý nghĩa |
|---|---|
| Giá API nhập | Tăng → biên giảm (lag 1-2 quý) |
| Tỷ giá USD/VND | Tăng → chi phí tăng |
| Visa thuốc mới | Nhiều → portfolio mở rộng |
| Chi phí bán hàng/Doanh thu | 15-25%, tăng nhanh → ép biên |
| Tồn kho | Tăng bất thường = bán chậm |

### Tier 3 — Dài hạn

- Chi tiêu dược/đầu người
- Dân số già hóa
- Dây chuyền EU-GMP mới
- Đối tác ngoại (chuyển giao công nghệ)

## 2.2 ETC vs OTC — So sánh chi tiết

| | ETC (Bệnh viện) | OTC (Nhà thuốc) |
|---|---|---|
| **Tỷ trọng thị trường** | 65-70% (~5.75 tỷ USD 2025) | 30-35% (~1.8 tỷ USD 2025) |
| **Biên lợi nhuận** | THẤP (đấu thầu ép giá) | CAO (tự định giá) |
| **Volume** | Lớn, ổn định nếu trúng thầu | Phụ thuộc thương hiệu |
| **Phụ thuộc** | Đấu thầu, BHYT, tiêu chuẩn GMP | Marketing, kênh phân phối |
| **Tốc độ tăng trưởng 2020-2025** | CAGR 8.4% | CAGR 6.8% |

## 2.3 EU-GMP — "Vé VIP" đấu thầu

### Phân nhóm đấu thầu (Thông tư 40/2025/TT-BYT)

| Nhóm | Tiêu chí | Đặc điểm |
|---|---|---|
| **Nhóm 1** | EU-GMP/PIC/S, sản xuất toàn bộ tại VN | Giá cao nhất, ít cạnh tranh, 69 thuốc đạt tiêu chí (Q1/2026) |
| Nhóm 2 | EU-GMP/PIC/S, một phần công đoạn | Giá khá cao |
| Nhóm 3-5 | WHO-GMP | Giá thấp, cạnh tranh khốc liệt |

### DN có EU-GMP (tính đến 2026)

| DN | Số dây chuyền EU-GMP | Ghi chú |
|---|---|---|
| IMP | 3-4 | Nhiều nhất ngành, kháng sinh mạnh |
| DHG | 2-3 | OTC + ETC cân bằng |
| PME | 1-2 | Stada backing |

**Chi phí đầu tư EU-GMP**: 200-500 tỷ + 2-3 năm xây dựng → rào cản gia nhập cao

## 2.4 Bẫy BCTC dược phẩm

| Bẫy | Cách kiểm tra |
|---|---|
| Doanh thu tăng đột biến | Do 1 gói thầu lớn? Có bền vững không? |
| Biên tăng bất thường | Giá API giảm tạm thời? Xu hướng dài hạn? |
| Chi phí bán hàng tăng nhanh | Doanh thu OTC tăng tương ứng không? |
| Tồn kho tăng | Bán chậm hay chuẩn bị mùa cao điểm? |

## 2.5 Checklist BCTC Dược (8 câu hỏi)

1. Doanh thu tăng % (so ngành 8-12%)?
2. Tách ETC/OTC — kênh nào tăng? Biên thay đổi?
3. Biên lợi nhuận gộp so cùng kỳ — tăng/giảm từ đâu?
4. Kết quả đấu thầu, trúng nhóm mấy? Bao nhiêu gói?
5. EU-GMP mới? Số sản phẩm nhóm 1 tăng?
6. Giá API + Tỷ giá USD ảnh hưởng chi phí?
7. Visa thuốc mới được cấp?
8. Chính sách đấu thầu/BHYT thay đổi gì?

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Nguyên tắc cốt lõi

```
Dược = PHÒNG THỦ — ÍT CHU KỲ NHẤT trong các ngành

- Ốm phải uống thuốc, BHYT trả phần lớn → doanh thu tăng đều 8-12%
- Giữ tốt khi thị trường giảm, tăng CHẬM khi thị trường bùng nổ
- "Áo mưa" — cần khi trời mưa, không cần khi trời nắng
```

## 3.2 So sánh với ngành khác

| Tình huống | Dược | Ngành chu kỳ (Thép, BĐS) |
|---|---|---|
| Kinh tế tốt | Tăng 8-12%, UNDERPERFORM thị trường | Tăng 30-50%+ |
| Kinh tế xấu | Vẫn tăng 8-12%, OUTPERFORM thị trường | Giảm 30-50% |

## 3.3 Catalyst chính sách

| Catalyst | Tác động |
|---|---|
| Thông tư đấu thầu mới (TT 40/2025) | Xáo trộn thị phần — ưu tiên thuốc nội EU-GMP |
| Mở rộng danh mục BHYT | Thêm thuốc được thanh toán = bán nhiều hơn |
| EU-GMP mới | Doanh thu + biên tăng ngay |
| Đối tác ngoại | Chuyển giao sản phẩm + công nghệ |
| Dịch bệnh | Doanh thu tăng đột biến (1 lần) |

## 3.4 Tín hiệu sớm

**Tốt (mua/giữ):**
- Thông tư ưu tiên thuốc nội địa
- DN đạt EU-GMP mới
- Mở rộng danh mục BHYT
- Giá API giảm
- Dân số già hóa
- Thu nhập bình quân tăng
- Chuỗi nhà thuốc mở rộng (hưởng lợi OTC)

**Xấu (thận trọng):**
- Thông tư bất lợi cho thuốc nội
- Giá API tăng 2 quý liên tiếp
- USD tăng mạnh
- Thu hẹp danh mục BHYT
- Thuốc TQ/Ấn Độ tràn vào
- Trượt nhiều gói thầu

---

# LỚP 4: HIỂU VĨ MÔ

## 4.1 Yếu tố vĩ mô theo mức độ quan trọng

| Yếu tố | Mức độ | Ghi chú |
|---|---|---|
| Chính sách đấu thầu | #1 | TT 40/2025: ưu tiên thuốc nội EU-GMP |
| Chính sách BHYT | #2 | 90%+ dân số, danh mục thuốc quyết định |
| Thu nhập/GDP | Dài hạn | Chi tiêu dược tăng theo thu nhập |
| Dân số già | Cấu trúc | VN đang già hóa nhanh |
| Giá API | Chi phí | Biến động ngắn hạn |
| Tỷ giá USD | Chi phí | 90% API nhập = exposure USD |
| Dịch bệnh | Đột biến | Không dự đoán được |

## 4.2 Ma trận ảnh hưởng vĩ mô theo DN

| Yếu tố | DHG | IMP | TRA |
|---|---|---|---|
| Thông tư mới | Hưởng lợi vừa | Hưởng lợi mạnh (EU-GMP nhiều nhất) | Trung tính |
| Giá API tăng | Ảnh hưởng vừa | Ảnh hưởng mạnh | Ít ảnh hưởng (đông dược) |
| Chuỗi nhà thuốc mở rộng | Hưởng lợi mạnh (OTC 60%) | Trung tính | Hưởng lợi (đông dược OTC) |
| Dân số già | Hưởng lợi | Hưởng lợi | Hưởng lợi mạnh (đông dược/bổ dưỡng) |

## 4.3 Động lực tăng trưởng

**Cấu trúc (dài hạn):**
- Chi tiêu dược thấp (dư địa gấp đôi so khu vực)
- Dân số già hóa
- BHYT phủ 90%+ dân số
- EU-GMP mở rộng
- Chuỗi nhà thuốc phát triển
- Xu hướng đông dược/tự nhiên
- Đối tác ngoại chuyển giao công nghệ

**Chu kỳ (ngắn hạn):**
- Thông tư ưu tiên thuốc nội
- Giá API giảm
- Mùa cúm/dịch bệnh
- EU-GMP mới đi vào hoạt động

## 4.4 Rủi ro

| Rủi ro | Mức độ | Ghi chú |
|---|---|---|
| Thông tư bất lợi | Cao | Đảo ngược ưu đãi thuốc nội |
| Giá API tăng mạnh | Trung bình | Ép biên 1-2 quý |
| Thuốc TQ/Ấn Độ tràn vào | Cao | Cạnh tranh giá khốc liệt nhóm 3-5 |
| USD tăng mạnh | Trung bình | Chi phí tăng |
| Thu hẹp danh mục BHYT | Cao | Giảm doanh thu ETC |
| Tăng trưởng chậm (8-12%) | Thấp | Đặc thù ngành phòng thủ |

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 Phương pháp định giá phổ biến

- **P/E**: Phương pháp chính. Dược phòng thủ → P/E cao hơn ngành chu kỳ
- **PEG**: P/E chia cho tăng trưởng EPS. <1.0x rẻ, 1.0-1.5x hợp lý, >1.5x đắt
- **Dividend Yield**: Ngành ổn định → cổ tức đều. DHG 3-5%, TRA 4-6%

## 5.2 Vùng P/E theo DN

| DN | P/E range | Lý do |
|---|---|---|
| DHG | 15-22x | #1 thị phần + Taisho (Nhật) 32% + OTC mạnh (Hapacol, Coldi) |
| IMP | 12-18x | EU-GMP nhiều nhất, đấu thầu nhóm 1 mạnh |
| TRA | 12-18x | Đông dược, OTC, biên cao |
| PME | 10-15x | Stada backing, quy mô nhỏ hơn |
| DN nhỏ | 8-12x | WHO-GMP, cạnh tranh giá |

**P/E dược CAO hơn ngành khác vì**: Ổn định, predictable, phòng thủ, dòng tiền đều

## 5.3 PEG — Công cụ định giá chính

| PEG | Đánh giá |
|---|---|
| <1.0x | Rẻ — cân nhắc mua |
| 1.0-1.5x | Hợp lý |
| >1.5x | Đắt (trừ khi có catalyst EU-GMP mới) |

## 5.4 Dividend Yield

| DN | Yield | Đặc điểm |
|---|---|---|
| DHG | 3-5% | Ổn định, Taisho backing |
| IMP | 3-4% | Tái đầu tư EU-GMP |
| TRA | 4-6% | Cao nhất nhóm |

Không cao bằng phân bón (DPM/DCM) nhưng ỔN ĐỊNH hơn nhiều.

## 5.5 Bẫy định giá

- ❌ So P/E dược với ngành chu kỳ (HPG, thép) → sai bản chất
- ❌ DN dược P/E 8x = rẻ (có thể WHO-GMP, cạnh tranh giá, không có moat)
- ✅ Rẻ = PEG <1.0x + catalyst (EU-GMP, thông tư ưu đãi)

---

# LỚP 6: ĐỊNH VỊ TỪNG MÃ (STRUCTURAL POSITIONING)

## 6.1 Universe Pharma (7 mã chính)

| Mã | Tên | Sàn | Định vị cốt lõi |
|---|---|---|---|
| **DHG** | Dược Hậu Giang | HOSE | #1 thị phần ~10%; Taisho (Nhật) sở hữu 32%; OTC mạnh (Hapacol, Coldi); biên 50-55% |
| **IMP** | Imexpharm | HOSE | EU-GMP nhiều nhất ngành (3-4 dây chuyền); tiên phong kháng sinh; ETC mạnh nhóm 1 |
| **DMC** | Domesco | HOSE | CFR (Mỹ) sở hữu; sản xuất + phân phối cân bằng; đa dạng danh mục |
| **TRA** | Traphaco | HOSE | #1 đông dược VN; biên cao; ít phụ thuộc API nhập; xu hướng tự nhiên |
| **DBD** | Bidiphar | HOSE | Đột phá thuốc ung thư "made in Vietnam"; đang đầu tư EU-GMP |
| **PME** | Pymepharco | HOSE | Stada (Đức) sở hữu; EU-GMP 1-2 dây chuyền; quy mô trung |
| **OPC** | OPC Pharma | HOSE | Đông dược; thương hiệu truyền thống; OTC focus |

## 6.2 Ma trận so sánh

| Mã | EU-GMP | OTC/ETC | Đối tác ngoại | Moat chính |
|---|---|---|---|---|
| DHG | 2-3 | 60/40 | Taisho (Nhật) 32% | Thương hiệu OTC + kênh phân phối |
| IMP | 3-4 | 40/60 | — | EU-GMP nhiều nhất → đấu thầu nhóm 1 |
| DMC | Có | 50/50 | CFR (Mỹ) | Danh mục đa dạng |
| TRA | — | 70/30 | — | Đông dược #1 + ít phụ thuộc API |
| DBD | Đang đầu tư | 50/50 | — | Thuốc ung thư niche |
| PME | 1-2 | 40/60 | Stada (Đức) | Chuyển giao công nghệ Đức |
| OPC | — | 80/20 | — | Thương hiệu đông dược truyền thống |

## 6.3 Decision rule phân loại

- **EU-GMP focus** (IMP, PME): Hưởng lợi thông tư mới, đấu thầu nhóm 1, nhưng đầu tư vốn lớn
- **OTC focus** (DHG, TRA, OPC): Biên cao, ổn định, hưởng lợi chuỗi nhà thuốc mở rộng
- **Đông dược** (TRA, OPC): Ít phụ thuộc API nhập, xu hướng tự nhiên, biên cao nhất
- **Đối tác ngoại** (DHG-Taisho, DMC-CFR, PME-Stada): Chuyển giao công nghệ + vốn + quản trị

---

# PHỤ LỤC

## A. Severity cho đánh giá tin

| Mức | Tiêu chí |
|---|---|
| **green** | Doanh thu >12%, biên ổn/tăng, trúng thầu tốt, OTC tăng |
| **yellow** | Doanh thu 8-10%, biên giảm nhẹ, trượt 1-2 gói, doanh thu nhờ dịch bệnh |
| **red** | Doanh thu giảm, biên giảm mạnh, thông tư bất lợi, lợi nhuận giảm |
| **blue** | Trung tính, chờ thêm data |

## B. Câu đánh giá mẫu

**ETC + OTC tốt:**
> "{ticker} doanh thu tăng {X}% — cao hơn ngành (8-12%). Doanh thu qua nhà thuốc tăng {Y}% nhờ chuỗi mở rộng — kênh này lời hơn bệnh viện."

**EU-GMP mới:**
> "{ticker} vừa đưa dây chuyền chuẩn châu Âu vào hoạt động. Doanh thu thuốc nhóm 1 tăng {X}%, biên cải thiện từ {Z}% lên {W}%."

**API tăng ép biên:**
> "{ticker} doanh thu tăng {X}% nhưng lợi nhuận chỉ tăng {Y}% — giá nguyên liệu từ Trung Quốc tăng {Z}%."

**Phòng thủ khi thị trường xấu:**
> "Thị trường giảm {X}%, {ticker} vẫn tăng doanh thu {Y}%, lợi nhuận {Z}%. Thuốc là nhu cầu thiết yếu."

**Trượt thầu:**
> "{ticker} doanh thu kênh bệnh viện giảm {X}% do trượt {Y} gói thầu. Đang đẩy mạnh bán qua nhà thuốc (tăng {Z}%)."

## C. Quy tắc cho agent

1. Dược VN = sản xuất generic → KHÔNG so với Pfizer, Roche
2. EU-GMP = lợi thế #1 → Check số dây chuyền
3. ETC vs OTC → PHẢI tách rõ khi phân tích
4. Đấu thầu = "sống chết" với kênh ETC
5. Dược = PHÒNG THỦ — đừng kỳ vọng tăng 30-50%
6. API nhập 90% → Giá API + USD = biến số chi phí lớn nhất
7. 10-15%/năm ĐỀU = đã tốt cho ngành này
8. KHÔNG dùng thuật ngữ tiếng Anh → PHẢI dịch
9. KHÔNG bịa data — verify từ BCTC hoặc web search

## D. Thuật ngữ — Mapping tiếng Anh → tiếng Việt

| Thuật ngữ | Dịch | Giải thích đơn giản |
|---|---|---|
| EU-GMP | Chuẩn châu Âu | Nhà máy chuẩn châu Âu — bán thuốc giá cao cho bệnh viện lớn |
| WHO-GMP | Chuẩn WHO | Chuẩn cơ bản — cạnh tranh giá |
| PIC/S | Chuẩn quốc tế | Tương đương EU-GMP |
| Đấu thầu nhóm 1 | — | Bệnh viện mua thuốc giá cao nhất, chỉ thuốc tốt nhất vào được |
| OTC | Bán qua nhà thuốc | Lời hơn bán cho bệnh viện |
| ETC | Bán cho bệnh viện | Qua đấu thầu — giá ép nhưng volume lớn |
| API | Nguyên liệu làm thuốc | Nhập 90% từ TQ/Ấn Độ |
| Generic | Thuốc hết bản quyền | Cạnh tranh giá, không có patent |
| Phòng thủ | — | Cổ phiếu ít biến động — giữ tốt khi thị trường giảm |
| Taisho | — | Tập đoàn dược Nhật — sở hữu 32% DHG |

---

## Hướng dẫn tra dữ liệu thời gian thực (cho Master Pharma)

KB master này chỉ cung cấp framework + threshold + range historical. Khi viết bài quarter cụ thể, Master phải:

1. **Query KB framework** (file này) — static guidance
2. **Finpath API** cho data realtime:
   - `get_income_statement(ticker)` + `get_balance_sheet(ticker)` — BCTC quarter
   - `get_financial_ratios(ticker)` — biên lợi nhuận, ROE, PE, PB
   - `get_shareholders(ticker)` + `get_events(ticker)` + `get_news(ticker)` — ownership + sự kiện + tin
3. **Web search** cho data Finpath API không có:
   - Kết quả đấu thầu cụ thể
   - Thông tư mới Bộ Y tế
   - Giá API xu hướng
   - Visa thuốc mới được cấp
   - EU-GMP mới đi vào hoạt động

Pipeline log V4.0 emit `data_trail` array: `{source, fetched, purpose, supports_argument}` per fact. KHÔNG bịa số.

---

## Cross-link

| File | Nội dung chính |
|---|---|
| `kb/pharma/tickers/` | Per-ticker deep dive (DHG, IMP, TRA...) — tạo khi cần |
| `data/manual/` | YAML curated data nếu có |

---

## Phần suy luận (cần verify)

Các điểm dưới đây rút từ framework + data historical — cần verify khi đưa vào bài cụ thể:

- **"DHG thị phần ~10%"** — số từ nhiều báo cáo 2023-2025, verify với data mới nhất
- **"Taisho sở hữu 32% DHG"** — kiểm tra cập nhật tỷ lệ sở hữu
- **"IMP có 3-4 dây chuyền EU-GMP"** — verify từ website công ty hoặc BCTC
- **"ETC 65-70%, OTC 30-35%"** — tỷ lệ thị trường, có thể thay đổi theo năm
- **"69 thuốc đạt tiêu chí nhóm 1 Q1/2026"** — số từ Thông tư 40/2025, cập nhật theo đợt mới
