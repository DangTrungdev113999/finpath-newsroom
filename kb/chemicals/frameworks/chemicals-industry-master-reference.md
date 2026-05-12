---
category: frameworks
title: "Chemicals-Industry-Master-Reference"
last_updated: 2026-05-12
---

Master reference cho ngành Hóa chất Việt Nam — mental model 6 lớp phân tích. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm hóa chất. Ngành hóa chất VN đa dạng: phân bón (đạm/NPK/lân), hóa chất công nghiệp (phốt pho vàng), cao su, nhựa, sơn, tẩy rửa.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Chemicals/knowledge.md + web search enrichment. Hoàn thiện 6 lớp: Hiểu ngành, Đọc số, Hiểu chu kỳ, Hiểu vĩ mô, Định giá, Case study. |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Phân loại doanh nghiệp

| Phân khúc | Mã tiêu biểu | Sản phẩm chính | Đặc thù kinh doanh |
|---|---|---|---|
| **Phân bón — Đạm** | DPM, DCM | Urê từ khí tự nhiên | Phụ thuộc giá khí đầu vào + giá urê thế giới; biên lãi = giá urê - giá khí |
| **Phân bón — NPK/Lân** | LAS, BFC, DDV | NPK, super lân | Phụ thuộc mùa vụ nông nghiệp; biến động ít hơn đạm |
| **Hóa chất công nghiệp** | DGC | Phốt pho vàng (P4), axit photphoric, thuốc trừ sâu | Biên gộp 30-40% cao nhất ngành; phụ thuộc giá P4 + chính sách Trung Quốc |
| **Hóa chất cơ bản** | CSV | Xút, axit, clo | Phục vụ công nghiệp nội địa; biên ổn định hơn |
| **Nhựa xây dựng** | BMP, NTP | Ống nhựa PVC/PE | Liên quan chu kỳ bất động sản + xây dựng |
| **Nhựa bao bì** | AAA, SPP | Bao bì, màng PE | Phụ thuộc giá hạt nhựa + nhu cầu FMCG/xuất khẩu |
| **Cao su** | GVR, PHR, DPR | Mủ cao su thiên nhiên | Phụ thuộc giá cao su thế giới + diện tích canh tác |
| **Sơn** | APC | Sơn xây dựng, công nghiệp | Liên quan bất động sản + xây dựng |
| **Chất tẩy rửa** | NET, LIX | Bột giặt, nước rửa | Tiêu dùng thiết yếu — ổn định nhất ngành |

## 1.2 Universe chính (niêm yết HOSE/HNX/UPCOM)

**Nhóm 1 — Phân bón đạm (Core):**
- **DPM** (HOSE): Đạm Phú Mỹ — lớn nhất ngành đạm VN, công suất 800.000 tấn urê/năm, ~30% xuất khẩu
- **DCM** (HOSE): Đạm Cà Mau — công suất 800.000 tấn urê/năm, tập trung nội địa + xuất khẩu Campuchia

**Nhóm 2 — Hóa chất công nghiệp:**
- **DGC** (HOSE): Hóa chất Đức Giang — nhà xuất khẩu phốt pho vàng lớn nhất châu Á, biên gộp 30-40%
- **CSV** (HOSE): Hóa chất Cơ bản miền Nam — xút, clo, axit

**Nhóm 3 — Phân bón NPK/Lân:**
- **LAS** (HOSE): Supe Phốt phát và Hóa chất Lâm Thao
- **BFC** (HOSE): Phân bón Bình Điền
- **DDV** (HNX): DAP - VINACHEM

**Nhóm 4 — Cao su:**
- **GVR** (HOSE): Tập đoàn Công nghiệp Cao su Việt Nam — sở hữu ~400.000 ha đất, doanh thu cao su ~30%, lợi nhuận chủ yếu từ chuyển đổi đất
- **PHR** (HOSE): Cao su Phước Hòa
- **DPR** (HOSE): Cao su Đồng Phú

**Nhóm 5 — Nhựa:**
- **BMP** (HOSE): Nhựa Bình Minh — ống nhựa PVC
- **NTP** (HNX): Nhựa Tiền Phong — ống nhựa
- **AAA** (HOSE): Nhựa An Phát — bao bì

## 1.3 Chuỗi giá trị

```
NGUYÊN LIỆU → SẢN PHẨM:
├── Khí tự nhiên → Đạm urê (DPM, DCM)
├── Quặng apatit (Lào Cai) → Phốt pho vàng, axit photphoric (DGC)
├── Dầu thô → Hạt nhựa PVC/PE → Ống nhựa (BMP), bao bì (AAA)
├── Mủ cao su → Cao su thiên nhiên (GVR, PHR)
└── Hóa chất cơ bản → Sơn (APC), chất tẩy rửa (NET)

KHÁCH HÀNG:
├── Phân bón → Nông dân (nội địa 70% + xuất khẩu 30%)
├── Hóa chất CN → Nhà máy (điện tử, bán dẫn, dệt may, thực phẩm)
├── Nhựa → Xây dựng + Bao bì (FMCG, xuất khẩu)
├── Cao su → Lốp xe, găng tay, đệm
└── Sơn, tẩy rửa → Xây dựng, hộ gia đình
```

## 1.4 Ai quyết định luật chơi

**Biến số #1 — Giá nguyên liệu thế giới:**
- Giá khí tự nhiên → chi phí DPM/DCM (60-70% giá thành)
- Giá P4 (phốt pho vàng) → doanh thu DGC
- Giá hạt nhựa → biên BMP/AAA
- Giá cao su SICOM/TOCOM → GVR/PHR

**Biến số #2 — Trung Quốc (ảnh hưởng lớn nhất):**
- Trung Quốc chiếm 80% sản lượng P4 thế giới → siết sản xuất vì ô nhiễm = DGC hưởng lợi
- Trung Quốc chiếm 25% xuất khẩu urê → hạn chế xuất khẩu = DPM/DCM lời
- Từ 2018, Trung Quốc gần như ngừng xuất khẩu phốt pho, chỉ sản xuất nội địa

**Biến số #3 — Ấn Độ:**
- Nhập khẩu phân bón lớn nhất thế giới → ảnh hưởng cầu urê toàn cầu

**Biến số #4 — Mùa vụ nông nghiệp:**
- Hè Thu (tháng 4-8): bón nhiều → DPM/DCM/LAS cao điểm
- Đông Xuân (tháng 10-2): nhu cầu thấp hơn

**Biến số #5 — Chính sách VN:**
- Thuế xuất khẩu phân bón 5%
- Quy định môi trường ngày càng chặt

## 1.5 Đặc thù doanh nghiệp chính

### DPM/DCM — Phụ thuộc chênh lệch giá

```
Biên lợi nhuận = Giá urê thế giới - Giá khí đầu vào (hợp đồng PVN)

Cơ chế:
- Giá khí điều chỉnh theo hợp đồng (6-12 tháng/lần), lag so với giá dầu
- Giá urê biến động daily theo thị trường quốc tế
- Giá urê tăng nhanh hơn giá khí → biên mở rộng → lãi lớn
- Giá urê giảm trong khi giá khí chưa điều chỉnh → biên co → lãi mỏng
```

**Benchmark giá urê:**
- Trung Đông (Yuzhnyy): benchmark chính
- 2024-2025: dao động $350-450/tấn
- 2026 dự báo: quanh $400-450/tấn nếu không có cú sốc

### DGC — "Ngôi sao" hóa chất Việt Nam

- Việt Nam có quặng apatit Lào Cai → nguồn nguyên liệu tự có → chi phí thấp
- Nhà xuất khẩu phốt pho vàng lớn nhất châu Á
- Biên gộp 30-40% — cao nhất ngành
- Trung Quốc chiếm 80% cung P4 thế giới → Trung Quốc siết = DGC hưởng lợi trực tiếp
- Chất lượng P4 của DGC được đánh giá gần như tốt nhất thế giới (vượt Kazakhstan)
- Ứng dụng P4: bán dẫn, thực phẩm (phụ gia), thuốc trừ sâu, chất chống cháy

**Benchmark giá P4:**
- $3.000-4.000/tấn = bình thường
- $4.000-5.000/tấn = cao
- >$5.000/tấn = đỉnh chu kỳ
- 2025 dự báo: $4.000-4.100/tấn (tăng 5-7% so cùng kỳ)

### GVR — Cao su + Đất

- Sở hữu ~400.000 ha đất (giá trị ẩn lớn)
- Doanh thu cao su chỉ ~30% tổng doanh thu
- Lợi nhuận chủ yếu từ chuyển đổi đất (KCN, bất động sản) — khoản 1 lần
- **Phân tích GVR = phân tích đất + bất động sản KCN, không chỉ cao su**

## 1.6 Mùa vụ kinh doanh

| Quý | DPM/DCM (Đạm) | DGC (P4) | GVR (Cao su) | AAA (Nhựa bao bì) |
|---|---|---|---|---|
| Q1 | Thấp (sau Tết) | Trung bình | **Thấp nhất** (rụng lá) | Trung bình |
| Q2 | **Cao (vụ Hè Thu)** | Trung bình - Cao | Tăng dần | Tăng (xuất khẩu) |
| Q3 | **Cao** | Trung bình | **Cao nhất** (cạo mủ) | Cao |
| Q4 | Giảm dần | Trung bình | Giảm | Cao |

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics theo phân khúc

### Phân bón đạm (DPM, DCM)

| Metric | Benchmark | Ý nghĩa |
|---|---|---|
| Giá urê thế giới | Yuzhnyy, Trung Đông | Quyết định doanh thu |
| Giá khí đầu vào | 60-70% giá thành | Quyết định chi phí |
| Biên gộp | 15-25% bình thường, >25% xuất sắc | Chênh lệch giá urê - giá khí |
| Sản lượng tiêu thụ | So cùng kỳ + kế hoạch năm | Doanh thu tăng vì giá hay sản lượng? |
| Tỷ lệ xuất khẩu | DPM ~30% | Hưởng lợi tỷ giá |
| Cổ tức | 50-80% lợi nhuận, yield 8-12% khi giá cao | Biến động mạnh theo năm |

### Hóa chất công nghiệp (DGC)

| Metric | Benchmark | Ý nghĩa |
|---|---|---|
| Giá P4 xuất khẩu | $3.000-4.000/tấn bình thường, >$4.000 cao | Quyết định doanh thu + biên |
| Sản lượng P4 | DGC ~40.000-50.000 tấn/năm | Năng lực sản xuất |
| Biên gộp | 30-40%, >35% tốt | Cao nhất ngành hóa chất |
| Chính sách Trung Quốc | Siết/nới sản xuất P4 | Biến số #1 cho DGC |

### Cao su (GVR, PHR)

| Metric | Benchmark | Ý nghĩa |
|---|---|---|
| Giá cao su | SICOM (Singapore), TOCOM (Tokyo) | Quyết định biên cao su |
| Doanh thu từ chuyển đổi đất | Có thể > doanh thu cao su | Khoản 1 lần, không bền |
| Diện tích đất GVR | ~400.000 ha | Giá trị ẩn NAV |

### Nhựa (BMP, AAA)

| Metric | Benchmark | Ý nghĩa |
|---|---|---|
| Giá hạt nhựa | Theo giá dầu | Chi phí đầu vào |
| Biên gộp | 15-25% (BMP cao hơn AAA) | Hạt nhựa rẻ → biên tốt |

## 2.2 Cách đọc đúng số liệu

**DPM/DCM:**
- Biên phụ thuộc chênh lệch giá urê - giá khí → không chỉ xem doanh thu
- Giá khí điều chỉnh chậm hơn giá urê (6-12 tháng/lần) → có độ trễ
- Cổ tức biến động: năm tốt 3.000-5.000đ, năm xấu 1.000-2.000đ
- **KHÔNG dùng cổ tức 1 năm đánh giá dài hạn — dùng trung bình 3-5 năm**

**DGC:**
- Trung Quốc siết sản xuất (vì ô nhiễm + quặng cạn kiệt) → giá P4 tăng → DGC lời
- Chi phí thấp nhờ quặng nội địa → vẫn lãi khi giá thấp
- Mở rộng downstream (axit photphoric, chất chống cháy) → giảm phụ thuộc P4 thuần

**GVR:**
- Lợi nhuận cao su ~30% doanh thu, biên thấp
- Lợi nhuận chuyển đổi đất có thể >50% tổng lợi nhuận — **KHÔNG BỀN, KHÔNG LẶP LẠI**
- **PHẢI tách riêng: lợi nhuận cao su vs lợi nhuận chuyển đổi đất**

## 2.3 Bẫy BCTC hóa chất

| Bẫy | Thực tế |
|---|---|
| "DPM lợi nhuận tăng 100%" | Giá urê tăng đột biến — 1 lần, năm sau có thể giảm 50% |
| "DGC biên 40%" | Giá P4 đang đỉnh, check Trung Quốc có nới sản xuất? |
| "GVR lợi nhuận kỷ lục" | Chuyển đổi đất — 1 lần, không lặp lại |
| "DCM yield 12%" | Năm sau có thể chỉ 4% |
| "AAA doanh thu tăng 25%" | Giá tăng hay sản lượng tăng? Giá tăng không bền |

## 2.4 Checklist BCTC hóa chất (8 câu hỏi)

1. Xác định phân khúc: Phân bón / Hóa chất CN / Cao su / Nhựa?
2. Giá đầu vào + đầu ra hiện tại (urê, P4, cao su, hạt nhựa) so với cùng kỳ?
3. Sản lượng (tấn): Doanh thu tăng vì giá hay sản lượng?
4. Biên lợi nhuận so cùng kỳ — mở rộng hay co lại?
5. Khoản bất thường: GVR chuyển đổi đất? Hoàn nhập dự phòng?
6. Cổ tức DPM/DCM: năm này vs trung bình 3-5 năm?
7. Chính sách Trung Quốc: siết/nới xuất khẩu urê? siết/nới sản xuất P4?
8. Mùa vụ: Hè Thu = peak phân bón, Q1 cao su thấp nhất?

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Nguyên tắc cốt lõi

```
Hóa chất = ngành chu kỳ nguyên liệu (commodity cycle)

Cung thiếu → Giá tăng → Lợi nhuận kỷ lục
Cung thừa → Giá giảm → Lãi mỏng/lỗ

Cổ phiếu chạy theo giá nguyên liệu, thường TRƯỚC 1-2 tháng
→ Giá cổ phiếu tăng TRƯỚC khi BCTC đẹp
→ Giá cổ phiếu giảm TRƯỚC khi BCTC xấu
```

## 3.2 Bốn giai đoạn chu kỳ

| Giai đoạn | Đặc điểm | Nhận diện | Cổ phiếu |
|---|---|---|---|
| **Đáy** | Cung thừa, giá thấp, nhà sản xuất đóng cửa → cung bắt đầu giảm | P/E cao (E thấp), tin xấu liên tục | Bắt đầu tăng |
| **Tăng trưởng** | Cung thiếu, biên mở rộng nhanh, lợi nhuận tăng mạnh | Giá nguyên liệu tăng, tin tốt từ Trung Quốc siết | **TĂNG MẠNH NHẤT** |
| **Đỉnh** | Nhà sản xuất mới gia nhập, cung tăng lại | P/E thấp nhất (E cao) = **BẪY** | Tăng chậm/đi ngang |
| **Giảm** | Cung thừa, biên co lại, lợi nhuận giảm | Giá nguyên liệu giảm, tin xấu từ Trung Quốc nới | Giảm TRƯỚC BCTC xấu |

## 3.3 Bẫy P/E ngành chu kỳ

```
P/E THẤP (E cao) = Đỉnh chu kỳ → CẨN THẬN, có thể BÁN
P/E CAO (E thấp) = Đáy chu kỳ → Cơ hội MUA

Lý do: E (lợi nhuận) ở đỉnh/đáy tạm thời, không đại diện cho tương lai
```

## 3.4 Case study DPM (2020-2025)

| Thời điểm | Giá urê ($/tấn) | Giá DPM | Giai đoạn |
|---|---|---|---|
| 2020 (Đáy) | $200-250 | ~12.000đ | Đáy |
| 2021 - Q1/2022 (Tăng) | $500-900 | 12k → 55k | **Tăng mạnh nhất** |
| Q2/2022 (Đỉnh) | ~$900 | ~55.000đ | Đỉnh |
| Q3/2022 - 2023 (Giảm) | $300-400 | 55k → 28k | Giảm |
| 2024-2025 (Ổn định) | $350-450 | 25-35k | Tích lũy |

**Bài học:** DPM tăng 4.5x trong 18 tháng khi giá urê tăng mạnh, rồi giảm 50% khi giá urê quay đầu.

## 3.5 Tín hiệu sớm

**Giá sắp tăng (cân nhắc MUA):**
- Trung Quốc hạn chế xuất khẩu urê / siết sản xuất P4
- Nhà máy lớn đóng cửa bảo trì
- Thiên tai/chiến tranh gián đoạn cung (Trung Đông, Nga-Ukraine)
- Tồn kho thế giới thấp
- La Niña (mưa tốt, nông nghiệp cần phân bón)

**Giá sắp giảm (cân nhắc BÁN):**
- Trung Quốc mở xuất khẩu urê / nới sản xuất P4
- Nhà máy mới vận hành
- Tồn kho thế giới tăng
- El Niño (hạn hán, nông nghiệp yếu)
- Giá đã tăng >50% trong 6 tháng

---

# LỚP 4: HIỂU VĨ MÔ

## 4.1 Yếu tố vĩ mô tác động

| Yếu tố | Ai bị ảnh hưởng nhất | Chiều tác động |
|---|---|---|
| **Giá nguyên liệu thế giới (#1)** | Tất cả | Giá tăng → doanh thu tăng (nếu đầu vào ổn định) |
| **Chính sách Trung Quốc (#2)** | DGC, DPM, DCM | Siết = VN lợi, Nới = VN thiệt |
| **Giá dầu** | DPM (khí), BMP/AAA (hạt nhựa) | Tăng = chi phí tăng |
| **Tỷ giá USD/VND tăng** | DPM, DCM, DGC (xuất khẩu) | Tăng = có lợi cho xuất khẩu |
| **La Niña (mưa)** | DPM, DCM, LAS | Có lợi cho nông nghiệp → cầu phân bón tăng |
| **El Niño (hạn)** | Phân bón | Bất lợi — nông nghiệp yếu |
| **Bất động sản/Xây dựng hồi phục** | BMP, NTP, APC, GVR | Có lợi — nhu cầu ống nhựa, sơn, đất KCN |
| **Nhu cầu ô tô Trung Quốc** | GVR, PHR | Có lợi — cầu cao su lốp xe |
| **Ngành bán dẫn toàn cầu** | DGC | P4 dùng trong sản xuất chip |

## 4.2 Trung Quốc — Biến số lớn nhất

**Phốt pho vàng (P4):**
- Trung Quốc chiếm 80% sản lượng thế giới
- Từ 2018, gần như ngừng xuất khẩu — chỉ sản xuất nội địa
- Quặng phosphate chất lượng cao đang cạn kiệt (Vân Nam, Quý Châu, Hồ Bắc)
- Siết môi trường kéo dài → **DGC hưởng lợi cấu trúc dài hạn**

**Urê:**
- Trung Quốc chiếm 25% xuất khẩu urê toàn cầu
- Hạn chế xuất khẩu theo mùa vụ để ưu tiên nội địa
- Mở/siết → giá urê thế giới biến động → DPM/DCM ảnh hưởng

**Cao su:**
- Trung Quốc = nước tiêu thụ lớn nhất (lốp xe, găng tay)
- Kinh tế Trung Quốc yếu = cầu cao su giảm = giá giảm

## 4.3 Ma trận ảnh hưởng

| Yếu tố | DPM/DCM | DGC | GVR | AAA | BMP |
|---|---|---|---|---|---|
| Giá urê tăng | +++ | | | | |
| Giá P4 tăng | | +++ | | | |
| Giá cao su tăng | | | ++ | | |
| Giá dầu tăng | - (chi phí) | | | - | - |
| Trung Quốc siết xuất khẩu/sản xuất | ++ | +++ | | | |
| Trung Quốc mở xuất khẩu/sản xuất | -- | --- | | | |
| La Niña (mưa nhiều) | ++ | | + | | |
| Bất động sản hồi phục | | | + | | ++ |
| Ngành bán dẫn tăng trưởng | | ++ | | | |

## 4.4 Xu hướng 2025-2026

**Dự báo giá phân bón:**
- Giá urê trong nước 2025: dư địa tăng 12-15% so cùng kỳ
- Giá urê 2026: dự báo giảm 8-10% so với 2025, quanh $400-450/tấn
- Giá nội địa thường có độ trễ so với giá thế giới

**Dự báo DGC:**
- Giá P4 xuất khẩu 2025: $4.000-4.100/tấn (tăng 5-7%)
- Trung Quốc tiếp tục siết sản xuất → cung P4 vẫn căng

**Xung đột Trung Đông:**
- Đốt giá urê tăng sốc 14% (tháng 5/2026)
- Rủi ro giá biến động ngắn hạn

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 Nguyên tắc định giá ngành chu kỳ

```
KHÔNG DÙNG P/E 1 năm cho ngành chu kỳ!

P/E thấp (E cao) = Đỉnh chu kỳ → KHÔNG PHẢI RẺ
P/E cao (E thấp) = Đáy chu kỳ → KHÔNG PHẢI ĐẮT

Dùng: Normalized P/E (P/E trung bình 3-5 năm) hoặc Dividend Yield trung bình
```

## 5.2 Phương pháp định giá theo phân khúc

| Doanh nghiệp | Phương pháp chính | Lưu ý |
|---|---|---|
| DPM, DCM | Normalized P/E + Dividend yield TB 3-5 năm | Yield >8% hấp dẫn, 5-8% hợp lý, <5% đắt |
| DGC | P/E + EV/EBITDA | P/E 8-12x hợp lý khi biên >30% |
| GVR | **NAV đất + P/E cao su** | NAV đất >> Market cap, nhưng discount dài hạn (chuyển đổi mất 5-10 năm) |
| AAA, SPP | P/E | Không có đặc thù riêng |
| BMP, NTP | P/E + Dividend yield | Ổn định hơn phân bón |

## 5.3 Dividend Yield cho DPM/DCM

```
Yield = Cổ tức / Giá cổ phiếu

Benchmark:
>8%: Hấp dẫn
5-8%: Hợp lý
<5%: Đắt

QUAN TRỌNG: Dùng cổ tức TRUNG BÌNH 3-5 năm, KHÔNG dùng 1 năm
(Cổ tức năm tốt có thể gấp 3-4 lần năm xấu)
```

## 5.4 NAV cho GVR

- GVR sở hữu ~400.000 ha đất
- NAV đất >> Market cap (theo giá đất hiện tại)
- NHƯNG: chuyển đổi đất làm KCN/bất động sản mất nhiều năm (5-10 năm)
- → Discount kéo dài là hợp lý
- → "Value trap" nếu không có catalyst chuyển đổi đất cụ thể

## 5.5 Vùng định giá tham khảo

| Mã | P/E hợp lý | Tình huống đặc biệt |
|---|---|---|
| DPM | Normalized 8-12x | Đỉnh chu kỳ P/E 5-6x = BẪY |
| DCM | Normalized 8-12x | Tương tự DPM |
| DGC | 10-15x | Biên >35% xứng đáng premium |
| GVR | P/E cao su + NAV đất | Cần catalyst đất cụ thể |

## 5.6 Khi nào MUA/BÁN

**Điều kiện MUA DPM/DCM (cần 2-3/5):**
1. Giá urê chạm đáy + ổn định
2. Trung Quốc hạn chế xuất khẩu urê
3. Giá khí PVN chưa điều chỉnh tăng
4. Mùa vụ Hè Thu sắp đến (Q1 vào)
5. Tồn kho urê thế giới thấp

**Điều kiện MUA DGC (cần 2-3/4):**
1. Trung Quốc siết sản xuất P4 (chính sách môi trường)
2. Giá P4 đáy hoặc bắt đầu tăng
3. DGC mở rộng downstream (axit photphoric, chất chống cháy)
4. PEG < 1.2x

**Điều kiện MUA GVR (cần 2-3/3):**
1. Có dự án chuyển đổi đất KCN cụ thể (công bố, phê duyệt)
2. Giá cao su hồi phục
3. Bất động sản KCN có nhu cầu (FDI tăng)

**Điều kiện BÁN:**
- DPM/DCM: Giá urê tăng >50%, Trung Quốc mở xuất khẩu, cung mới tăng, P/E <6x
- DGC: Trung Quốc nới sản xuất P4, giá P4 giảm 2 quý liên tiếp, biên <30%
- GVR: Chuyển đổi đất xong, không có catalyst mới

---

# LỚP 6: CASE STUDY LỊCH SỬ

## Case 1 — DPM 2021-2022: Siêu chu kỳ urê

**Bối cảnh:**
- COVID-19 làm gián đoạn chuỗi cung ứng phân bón toàn cầu
- Giá khí tự nhiên tăng vọt (khủng hoảng năng lượng châu Âu)
- Trung Quốc hạn chế xuất khẩu urê để ưu tiên nội địa

**Diễn biến:**
- Giá urê: $250 (2020) → $900 (Q2/2022) — tăng 260%
- Giá DPM: 12.000đ (2020) → 55.000đ (Q2/2022) — tăng 358%
- Biên gộp DPM: 20% → 35%
- Cổ tức năm 2022: 5.000đ/cp (yield >15% so với giá trung bình)

**Sau đỉnh:**
- Giá urê giảm về $300-400
- Giá DPM giảm về 25.000-30.000đ
- Cổ tức giảm về 1.500-2.000đ/cp

**Bài học:**
1. Cổ phiếu hóa chất chạy TRƯỚC giá nguyên liệu 1-2 tháng
2. P/E thấp ở đỉnh chu kỳ là BẪY — không phải rẻ
3. Siêu lợi nhuận không bền — dùng normalized earnings
4. Cổ tức biến động cực lớn — dùng trung bình 3-5 năm

## Case 2 — DGC 2020-2025: Hưởng lợi cấu trúc từ Trung Quốc

**Bối cảnh:**
- Từ 2018, Trung Quốc gần như ngừng xuất khẩu P4
- Chính sách môi trường Trung Quốc ngày càng chặt
- Quặng phosphate chất lượng cao cạn kiệt dần

**Diễn biến:**
- DGC trở thành nhà xuất khẩu P4 lớn nhất châu Á
- Biên gộp duy trì 30-40% — cao nhất ngành
- Giá P4: $2.500 (2020) → $4.500 (2022) → ổn định $4.000+ (2024-2025)
- DGC mở rộng downstream: axit photphoric, chất chống cháy, bán dẫn

**Bài học:**
1. Lợi thế cấu trúc (quặng nội địa + Trung Quốc siết) bền vững hơn lợi thế chu kỳ
2. DGC ít biến động hơn DPM/DCM vì không phụ thuộc 1 sản phẩm
3. Mở rộng downstream giảm phụ thuộc giá P4 thuần
4. Xứng đáng premium P/E so với phân bón thuần

## Case 3 — GVR: Value trap hay cơ hội?

**Bối cảnh:**
- Sở hữu ~400.000 ha đất — NAV đất >> market cap
- Doanh thu cao su chỉ ~30%, biên thấp
- Lợi nhuận phụ thuộc chuyển đổi đất làm KCN

**Vấn đề:**
- Chuyển đổi đất mất 5-10 năm (thủ tục pháp lý phức tạp)
- Lợi nhuận từ đất là 1 lần, không lặp lại
- Cổ phiếu discount liên tục so với NAV

**Khi nào không phải value trap:**
1. Có dự án KCN cụ thể được phê duyệt
2. FDI vào Việt Nam tăng mạnh → nhu cầu đất KCN
3. Giá cao su hồi phục (hỗ trợ mảng kinh doanh chính)

**Bài học:**
1. NAV cao không có nghĩa là cổ phiếu sẽ tăng
2. Cần catalyst cụ thể để unlock giá trị đất
3. Phân tách rõ: lợi nhuận cao su vs lợi nhuận đất

---

# PHỤ LỤC

## A. Severity đánh giá tin tức

- **green:** Giá sản phẩm tăng + sản lượng tăng + biên mở, Trung Quốc siết cung, La Niña, lợi nhuận từ hoạt động kinh doanh chính
- **yellow:** Giá đi ngang, lợi nhuận từ chuyển đổi đất (1 lần), cổ tức cao bất thường, bảo trì nhà máy
- **red:** Giá giảm mạnh + cung tăng, Trung Quốc mở xuất khẩu/sản xuất, El Niño, biên co lại 2+ quý, lợi nhuận giảm/lỗ
- **blue:** Trung tính — không ảnh hưởng rõ ràng

## B. Câu đánh giá mẫu

**DPM hưởng lợi giá urê:**
> "Giá phân bón thế giới tăng {X}% do Trung Quốc hạn chế xuất khẩu. Chi phí khí gần như không đổi. Kết quả: lời nhiều hơn mỗi tấn, lợi nhuận tăng {Y}%."

**DGC hưởng lợi chính sách Trung Quốc:**
> "Trung Quốc (chiếm 80% phốt pho thế giới) siết sản xuất vì ô nhiễm. Giá P4 tăng {X}%. {ticker} là số ít doanh nghiệp ngoài Trung Quốc có thể sản xuất → hưởng lợi trực tiếp. Biên đạt {Y}% — cao nhất ngành."

**GVR lãi từ chuyển đổi đất:**
> "{ticker} lãi {X} tỷ, tăng {Y} lần so cùng kỳ. Phần lớn từ cho thuê đất làm KCN — khoản thu 1 lần. Lợi nhuận cao su thật chỉ tăng {Z}%."

**Đáy chu kỳ phân bón:**
> "Giá phân bón giảm {X}% từ đỉnh. Tuy nhiên, Trung Quốc vừa hạn chế xuất khẩu, tồn kho thấp nhất 3 năm, vụ Hè Thu sắp bắt đầu. Lịch sử: các tín hiệu này xuất hiện cùng lúc → giá thường hồi phục."

## C. Từ điển cho nhà đầu tư ít kinh nghiệm

| Thuật ngữ | Giải thích đơn giản |
|---|---|
| Giá urê tăng | Giá phân bón thế giới tăng — bán được giá cao hơn |
| Giá khí đầu vào | Chi phí nguyên liệu chính để sản xuất phân bón |
| Trung Quốc siết xuất khẩu | Trung Quốc hạn chế bán ra nước ngoài → thiếu hàng → giá tăng |
| Phốt pho vàng (P4) | Hóa chất quan trọng dùng trong thuốc trừ sâu, thực phẩm, điện tử, bán dẫn |
| Biên lợi nhuận mở rộng | Chênh lệch giữa giá bán và chi phí tăng — lời nhiều hơn mỗi tấn |
| GVR chuyển đổi đất | Bán/cho thuê đất cao su làm KCN — lời lớn nhưng 1 lần |
| Yield 10% | Mỗi năm nhận lại 10% tiền đã bỏ ra — từ cổ tức |
| La Niña | Mưa nhiều, tốt cho nông nghiệp → cần nhiều phân bón |
| El Niño | Hạn hán → nông nghiệp yếu → cần ít phân bón |
| Normalized P/E | P/E dùng lợi nhuận trung bình nhiều năm, không phải 1 năm |
| NAV | Giá trị tài sản ròng — ở đây là giá trị đất GVR sở hữu |
| Value trap | Cổ phiếu trông rẻ nhưng không tăng vì không có catalyst |

## D. Quy tắc cho agent

1. "Hóa chất" = nhiều phân khúc khác nhau → **PHẢI xác định cụ thể phân khúc**
2. Giá nguyên liệu thế giới = #1 → **PHẢI check giá urê, P4, cao su, hạt nhựa**
3. Trung Quốc = biến số lớn nhất → **PHẢI theo dõi chính sách Trung Quốc**
4. **KHÔNG dùng P/E 1 năm cho ngành chu kỳ** → Dùng normalized P/E
5. Cổ tức DPM/DCM biến động → **Dùng cổ tức trung bình 3-5 năm**
6. GVR = đất + cao su → **PHẢI tách lợi nhuận cao su vs lợi nhuận chuyển đổi đất**
7. So sánh cùng kỳ, **check vụ Hè Thu vs Đông Xuân**
8. **KHÔNG dùng thuật ngữ tiếng Anh** → PHẢI dịch sang tiếng Việt
9. **KHÔNG bịa số liệu** → Thiếu data → nói rõ thiếu

---

## Hướng dẫn tra dữ liệu thời gian thực

KB master này chỉ cung cấp framework + threshold + range historical. Khi viết bài quý cụ thể, Master phải:

1. **Query KB framework** (file này) — static guidance
2. **Finpath API** cho data realtime:
   - `get_income_statement(ticker)` + `get_balance_sheet(ticker)` — BCTC quý
   - `get_financial_ratios(ticker)` — biên lợi nhuận, ROE, ROA
   - `get_shareholders(ticker)` + `get_events(ticker)` + `get_news(ticker)` — ownership + sự kiện + tin
3. **Web search** cho data Finpath API không có:
   - Giá urê, P4, cao su realtime
   - Chính sách Trung Quốc mới nhất
   - Kế hoạch ĐHĐCĐ, target năm
   - Tin tức ngành gần đây

**KHÔNG bịa số liệu.** Nếu thiếu data → ghi rõ "cần verify từ nguồn X".

---

## Cross-link

| File | Nội dung |
|---|---|
| `kb/chemicals/tickers/dpm.md` | Profile chi tiết DPM (nếu cần tạo) |
| `kb/chemicals/tickers/dgc.md` | Profile chi tiết DGC (nếu cần tạo) |
| `kb/bank/frameworks/bank-industry-master-reference.md` | Mẫu format reference |

---

## Sources

Thông tin bổ sung từ web search (tháng 5/2026):
- [VnEconomy - Dự báo giá phân bón 2026](https://vneconomy.vn/du-bao-gia-phan-bon-dao-chieu-giam-trong-nam-2026.htm)
- [VnEconomy - Cổ phiếu phân bón triển vọng 2026](https://vneconomy.vn/co-phieu-phan-bon-bung-no-trien-vong-the-nao-trong-nam-2026.htm)
- [CafeF - Trung Quốc ngừng xuất khẩu P4](https://cafef.vn/tq-gan-nhu-ngung-xuat-khau-1-mat-hang-cuc-quan-trong-co-hoi-vang-cho-cong-ty-viet-nam-lon-nhat-chau-a-188240807065016192.chn)
- [24hmoney - DGC triển vọng 2025](https://24hmoney.vn/news/dgc-ong-vua-phot-pho-vang-quay-tro-lai-thoi-ky-hoang-kim-2025-c30a2520028.html)
- [DNSE - Doanh nghiệp phân bón hóa chất H1/2025](https://www.dnse.com.vn/senses/tin-tuc/cac-doanh-nghiep-nganh-phan-bon-hoa-chat-lam-an-ra-sao-nua-dau-nam-2025-35120462)
