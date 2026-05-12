---
category: frameworks
title: "Sugar-Industry-Master-Reference"
last_updated: 2026-05-12
---

Master reference cho Master Sugar — mental model 6 lớp phân tích ngành mía đường VN. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **SBT · QNS · LSS · SLS**. Ngành mía đường là ngành chu kỳ commodity điển hình — giá đường quốc tế (#11) và thuế CBPG là 2 biến số quyết định 70-80% lợi nhuận.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Sugar/knowledge.md + web research. Đầy đủ 6 lớp + Phụ lục. |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Tổng quan thị trường

- **Sản xuất nội địa:** ~1.0-1.2 triệu tấn/năm (từ mía)
- **Nhập khẩu:** ~1.5-1.8 triệu tấn/năm (đường thô → tinh luyện)
- **Tiêu thụ:** ~2.5-3.0 triệu tấn/năm → VN = NHẬP KHẨU RÒNG
- **Công nghiệp (60-65%):** Nước giải khát, bánh kẹo, sữa, thực phẩm chế biến
- **Tiêu dùng trực tiếp (35-40%):** Hộ gia đình, nhà hàng, quán ăn

## 1.2 Chuỗi giá trị

### Nguyên liệu

| Nguồn | Đặc điểm |
|---|---|
| **Mía nội địa** | Vùng trồng: ĐBSCL, miền Trung, Tây Nguyên, Sơn La. Vụ ép: T10→T4. Chi phí mía: 50-60% giá thành. Năng suất VN (55-65 tấn/ha) THẤP hơn Thái (70-80) và Brazil (75-85). |
| **Đường thô nhập** | Nguồn: Thái Lan, Brazil, Ấn Độ, Úc. Phụ thuộc giá ICE #11. |

### Sản xuất

- **Nhà máy ép mía:** Mía → đường thô → tinh luyện (vụ ép T10-T4)
- **Nhà máy tinh luyện:** Đường thô nhập → tinh luyện (quanh năm)
- **Phụ phẩm quan trọng:**
  - **Điện sinh khối:** Đốt bã mía → bán EVN, biên 30-40%
  - **Ethanol:** Mật rỉ → cồn, nhiên liệu sinh học, biên 15-20%
  - **Phân bón hữu cơ:** Từ bùn lọc

> **SBT phụ phẩm chiếm 15-25% doanh thu** — "bộ đệm" khi giá đường yếu.

### Phân phối

- **Công nghiệp:** Coca-Cola, Pepsi, Vinamilk, bánh kẹo (60-65%)
- **Bán lẻ:** Siêu thị, chợ truyền thống (35-40%)
- SBT có kênh phân phối mạnh nhất ngành

## 1.3 Phân loại doanh nghiệp

| Mã | Tên | Đặc trưng cấu trúc | Sàn |
|---|---|---|---|
| **SBT** | TTC AgriS (Thành Thành Công - Biên Hòa) | #1 VN — Ép mía + Tinh luyện + Phụ phẩm. ~35-40% thị phần. Biên gộp 10-15%, volume lớn nhất. | HOSE |
| **QNS** | Đường Quảng Ngãi | Đường (~40% DT) + Vinasoy (~50% DT). Đường theo chu kỳ, Vinasoy ổn định — PHẢI tách phân tích. | HOSE |
| **LSS** | Mía Đường Lam Sơn | Ép mía miền Bắc (Thanh Hóa). Nhỏ, vùng nguyên liệu hạn chế. | HOSE |
| **SLS** | Mía Đường Sơn La | Ép mía Tây Bắc (Sơn La). Nhỏ, mùa vụ rõ, năng suất mía tốt hơn miền Nam. | HOSE |

> **BHS (Đường Biên Hòa)** đã hủy niêm yết để sáp nhập vào SBT (2018).

> **Decision rule phân loại:** Ngành đường VN trên sàn CHỦ YẾU phân tích **SBT + QNS**. LSS/SLS là mid-cap, thanh khoản thấp hơn.

## 1.4 Ai quyết định luật chơi

### 1. Giá đường thế giới (#1 quan trọng nhất)

- **ICE Sugar #11 ($/lb)** = benchmark toàn cầu
- Biến động lịch sử: $0.10/lb (đáy) → $0.27/lb (đỉnh 2023) → $0.14/lb (5/2026)
- #11 tăng → VN bán giá cao → lợi nhuận tăng
- #11 giảm → nhập rẻ ép giá nội địa → lợi nhuận giảm

### 2. Thuế CBPG + Chống trợ cấp (#2 quan trọng)

- VN áp thuế CBPG **42.99%** + CTC **4.65%** lên đường Thái Lan (từ 8/2021)
- Hiệu lực đến **15/6/2026** — sắp hết hạn, cần theo dõi rà soát cuối kỳ
- CBPG duy trì = "lá chắn sống còn" | CBPG gỡ = SBT, QNS chịu áp lực lớn

### 3. Cung cầu toàn cầu

| Quốc gia | Vai trò | Tác động |
|---|---|---|
| **Brazil** | #1 xuất khẩu (~45% toàn cầu) | Mùa vụ + tỷ lệ ethanol quyết định cung thế giới |
| **Ấn Độ** | #2 sản xuất | Chính sách xuất khẩu ảnh hưởng giá mạnh |
| **Thái Lan** | #3 xuất khẩu, đối thủ trực tiếp VN | Chi phí thấp hơn VN ~15-20% |

### 4. Thời tiết

- **El Niño** → hạn hán Brazil/Ấn Độ → cung giảm → giá tăng
- **La Niña** → mưa tốt → mía tốt → cung tăng → giá giảm

### 5. Vụ ép mía (T10→T4)

- Sản lượng đường nội địa tập trung vụ ép
- Ngoài vụ (T5-T9) → chủ yếu tinh luyện đường nhập
- Vụ tốt (năng suất cao, CCS cao) → biên tốt
- Vụ xấu (hạn, sâu bệnh) → chi phí cao

## 1.5 Đặc thù ngành VN

| Đặc thù | Chi tiết |
|---|---|
| **Năng suất mía thấp** | VN 55-65 tấn/ha vs Thái 70-80 vs Brazil 75-85 → Chi phí sản xuất cao hơn Thái ~15-20% |
| **Thuế CBPG = "lá chắn" sống còn** | Bỏ thuế → Thái bán $0.35/kg vs VN $0.45/kg → VN thua |
| **Phụ phẩm = giá trị bổ sung** | Đường biên mỏng 10-15%, điện sinh khối biên 30-40%, ethanol biên 15-20% |
| **QNS = 2 ngành** | Đường (~40% DT) theo chu kỳ, Vinasoy (~50% DT) ổn định → PHẢI tách phân tích |
| **Đường nhập lậu + gian lận** | Rủi ro thường trực, ảnh hưởng giá nội địa |

## 1.6 Mùa vụ — DT có tính mùa RẤT RÕ

| Tháng | Vụ ép | Sản lượng | Doanh thu |
|---|---|---|---|
| T10-T12 | Bắt đầu | Tăng dần | Tăng |
| **T1-T4** | **Cao điểm** | **Cao nhất** | **Cao nhất** |
| T5-T9 | Hết vụ | Thấp (tinh luyện) | Thấp |

> **Q1-Q2 (niên độ 7-6) mạnh nhất. Q3 yếu nhất.** So sánh YoY cùng kỳ, KHÔNG so QoQ.

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics quan trọng

### Tier 1 — Thị trường phản ứng ngay

| Metric | Ý nghĩa | Benchmark |
|---|---|---|
| **Giá ICE #11** | Quyết định giá bán | >$0.20/lb tốt, $0.15-0.20 trung bình, <$0.15 xấu |
| **Giá đường nội địa** | Giá bán thực tế | So #11 + thuế CBPG + chi phí vận chuyển |
| **Sản lượng đường (tấn)** | Volume bán | So cùng kỳ + kế hoạch năm |
| **Biên gộp** | Lời/tấn | Thuần 10-15%; có phụ phẩm 15-20% |
| **Thuế CBPG** | Bảo vệ nội địa | Duy trì = tốt, giảm/gỡ = xấu |

### Tier 2 — Phản ứng 1-2 quý

| Metric | Ý nghĩa | Benchmark |
|---|---|---|
| **CCS (chữ đường)** | Hàm lượng đường/tấn mía | >10 tốt, 9-10 trung bình, <9 kém |
| **Sản lượng mía ép (tấn)** | Vụ ép tốt/xấu | Năng suất tấn/ha |
| **Doanh thu phụ phẩm** | Thu bổ sung từ điện + ethanol | SBT: 15-25% doanh thu |
| **Giá đường thô nhập** | Chi phí tinh luyện | Nhập rẻ → biên tinh luyện tốt |
| **Tồn kho đường** | Cao → ép giá bán | Vụ ép tăng (bình thường), ngoài vụ giảm |

### Tier 3 — Dài hạn

| Metric | Ý nghĩa |
|---|---|
| Diện tích mía | Nông dân trồng tăng/giảm |
| Xu hướng giảm đường (low-sugar) | Dài hạn: NGK, thực phẩm giảm đường |
| Chính sách ethanol VN (E5, E10) | Bắt buộc pha → nhu cầu ethanol tăng |
| Quy hoạch điện 8 | Điện sinh khối được ưu tiên → doanh thu điện tăng |
| Tỷ giá USD/VND | Nhập đường thô bằng USD → USD tăng = chi phí tăng |

## 2.2 SBT — Cách đọc BCTC

**TÁCH 3 PHẦN:**

1. **Đường từ mía (T10-T4):**
   - Chi phí mía ~50-60% giá thành
   - CCS cao → nhiều đường/tấn mía → biên tốt

2. **Đường tinh luyện từ nhập (quanh năm):**
   - Biên = giá tinh luyện − giá thô nhập − chi phí sản xuất
   - Phụ thuộc #11 + tỷ giá

3. **Phụ phẩm (15-25% doanh thu):**
   - Điện sinh khối: biên 30-40%
   - Ethanol: biên 15-20%
   - "Bộ đệm" khi đường yếu

> **SBT biên MỎNG (10-15% gộp) → Giá đường ±5% = Lợi nhuận ±30-50%** (đòn bẩy hoạt động cao)

## 2.3 QNS — TÁCH đường vs Vinasoy

| Mảng | Tỷ trọng DT | Đặc điểm | KB áp dụng |
|---|---|---|---|
| **Đường** | ~40% | Theo chu kỳ, biên thấp | KB Sugar (file này) |
| **Vinasoy** | ~50% | Ổn định, biên cao hơn | KB Thực phẩm |
| Khác | ~10% | Bánh kẹo, nước | - |

> QNS lợi nhuận tăng 30% → kiểm tra Vinasoy gánh hay đường thực sự tốt?

## 2.4 Bẫy BCTC phổ biến

| Bẫy | Thực tế | Cách check |
|---|---|---|
| "SBT lợi nhuận tăng 200%" | Giá #11 tăng đột biến 1 chu kỳ | Giá #11 bền? Hay đang đỉnh? |
| "SBT doanh thu tăng 25%" | Giá tăng, lượng không đổi | Check sản lượng (tấn) |
| "SBT biên 18%" | Phụ phẩm kéo lên | Tách biên đường vs phụ phẩm |
| "QNS lợi nhuận tăng 30%" | Vinasoy gánh, đường yếu | TÁCH đường vs Vinasoy |
| "CBPG bảo vệ → yên tâm" | Review 5 năm, có thể gỡ | Khi nào review? Khả năng duy trì? |
| "Vụ ép tốt = lợi nhuận tốt" | Sản lượng cao nhưng giá có thể thấp | Sản lượng × Giá = Doanh thu |
| "DT Q3 giảm 40% vs Q1" | Hết vụ ép = bình thường | So cùng kỳ Q3 năm trước |

## 2.5 Checklist BCTC (8 câu hỏi)

1. Giá #11 xu hướng? Tăng → lợi nhuận tăng, giảm → lợi nhuận giảm
2. Giá đường nội địa? So cùng kỳ
3. Sản lượng đường (tấn)? Vụ ép: mía × CCS. Tinh luyện: nhập × biên
4. Biên gộp? Tách đường vs phụ phẩm
5. Thuế CBPG còn? Sắp review = rủi ro
6. Doanh thu phụ phẩm? Tăng = bộ đệm tốt
7. Tồn kho? Ngoài vụ vẫn cao = bán chậm
8. QNS: Tách đường vs Vinasoy

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Nguyên tắc cốt lõi

```
Đường = NGÀNH CHU KỲ COMMODITY (như thép, dầu khí, cao su)

Cung thiếu (hạn Brazil/Ấn Độ) → giá tăng → SBT lãi lớn
Cung thừa (mùa vụ tốt toàn cầu) → giá giảm → SBT lỗ/lãi mỏng

Chu kỳ ~3-5 năm:
Giá thấp → nông dân bỏ mía → cung giảm → giá tăng → 
trồng nhiều → cung tăng → giá giảm → lặp lại

Cổ phiếu chạy TRƯỚC giá đường ~1-2 tháng
```

## 3.2 Bốn giai đoạn chu kỳ

| Giai đoạn | Đặc điểm | Giá #11 | Cổ phiếu |
|---|---|---|---|
| **1. Đáy** | Cung thừa, nông dân bỏ mía, doanh nghiệp lỗ/hòa | <$0.15/lb | Giảm/đi ngang, P/E cao (E thấp) |
| **2. Hồi phục** | Cung thiếu, biên mở rộng, lợi nhuận vọt | $0.18-0.25/lb | **TĂNG MẠNH NHẤT** |
| **3. Đỉnh** | Trồng nhiều trở lại, biên cao nhưng chậm lại | >$0.25/lb | Tăng chậm/đi ngang |
| **4. Suy giảm** | Cung thừa trở lại, biên co, lợi nhuận giảm | Giảm từ đỉnh | Giảm TRƯỚC giá |

> **P/E thấp nhất ở đỉnh chu kỳ → BẪY** (E đang đỉnh, sẽ giảm)

## 3.3 Lịch sử chu kỳ SBT (2019-2026)

| Giai đoạn | Thời điểm | Giá #11 | SBT |
|---|---|---|---|
| Đáy | 2019-2020 | $0.10-0.12/lb | 12-15k |
| Hồi phục | 2021-2022 | $0.18-0.20/lb + CBPG | 15k→22k |
| Đỉnh | Q4/2023 | $0.27/lb (đỉnh 12 năm) | 22k→28k |
| Suy giảm | 2024-2025 | $0.18-0.22/lb | 28k→20-24k |
| Đáy mới? | 5/2026 | $0.14/lb | Theo dõi |

## 3.4 Tín hiệu sớm

### Giá sắp TĂNG

- El Niño → hạn Brazil/Ấn Độ (theo dõi NOAA)
- Ấn Độ hạn chế/cấm xuất khẩu
- Brazil chuyển mía → ethanol (giá dầu/ethanol Brazil tăng)
- Tồn kho đường thế giới giảm (theo dõi ISO)
- Diện tích mía toàn cầu giảm

### Giá sắp GIẢM

- La Niña → mưa tốt toàn cầu → mía tốt
- Ấn Độ mở xuất khẩu
- Brazil tăng sản xuất đường (giá dầu giảm)
- Tồn kho thế giới tăng
- Giá đã tăng >50% trong 6 tháng

---

# LỚP 4: HIỂU VĨ MÔ

## 4.1 Yếu tố vĩ mô tác động

| Yếu tố | Tác động | Mức độ |
|---|---|---|
| **Giá ICE #11** | Quyết định giá bán + lợi nhuận | #1 quan trọng nhất |
| **Thuế CBPG** | "Lá chắn" bảo vệ nội địa | #2 quan trọng |
| **Thời tiết (El Niño/La Niña)** | Cung toàn cầu + mía VN | Cao |
| **Chính sách Ấn Độ** | #2 sản xuất đường thế giới | Cao |
| **Chính sách Brazil** | #1 sản xuất + xuất khẩu | Cao |
| **Giá dầu** | Brazil chọn ethanol hay đường | Trung bình |
| **Tỷ giá USD/VND** | Chi phí nhập đường thô | Trung bình |
| **Tỷ giá BRL** | Brazil xuất khẩu bằng USD | Trung bình |
| **Nhu cầu nội địa VN** | Tăng 3-5%/năm | Thấp (ổn định) |
| **Xu hướng low-sugar** | Dài hạn: giảm tiêu thụ | Rủi ro dài hạn |

## 4.2 Brazil → Ethanol: cơ chế quan trọng

```
Brazil sản xuất CẢ đường LẪN ethanol từ mía (~55% ethanol, 45% đường)

Giá dầu CAO → Brazil chuyển mía → ethanol → ÍT ĐƯỜNG → giá TĂNG
Giá dầu THẤP → Brazil chuyển mía → đường → NHIỀU ĐƯỜNG → giá GIẢM

=> GIÁ DẦU TĂNG = GIÁ ĐƯỜNG TĂNG (gián tiếp qua Brazil)
```

## 4.3 Ma trận ảnh hưởng

| Yếu tố | SBT đường | SBT phụ phẩm | QNS đường | QNS Vinasoy |
|---|---|---|---|---|
| #11 tăng | +++ | 0 | ++ | 0 |
| #11 giảm | --- | 0 | -- | 0 |
| CBPG duy trì | +++ | 0 | ++ | 0 |
| CBPG gỡ | --- | 0 | -- | 0 |
| El Niño | +/- (mía VN yếu, giá TG tăng) | - | +/- | 0 |
| Giá dầu tăng | + | + (ethanol) | + | 0 |
| USD tăng | - | 0 | - | 0 |
| Low-sugar | - (dài hạn) | 0 | - | 0 |

## 4.4 Tình hình 2025-2026

### Giá đường thế giới (tính đến 5/2026)

- ICE #11: ~$0.14/lb — giảm ~29% so cùng kỳ 2025, ~40% so đỉnh 2023
- Dự báo: bearish, có thể test $0.12-0.125/lb nếu Brazil sản xuất 43-44+ triệu tấn 2026/27
- Cung thừa toàn cầu 2025/26: 1.2-8.3 triệu tấn (tùy nguồn)

### Brazil 2025/26

- Sản lượng kỷ lục: 44.7 triệu tấn (+2.3% YoY)
- 2026/27 dự báo giảm còn ~40 triệu tấn (tỷ lệ đường/ethanol thay đổi)

### Ấn Độ 2025/26

- Sản lượng phục hồi: 32.8-35.3 triệu tấn (+26% YoY)
- Thời tiết thuận lợi + diện tích trồng tăng

### Thuế CBPG VN

- Hiệu lực đến **15/6/2026** — sắp hết hạn
- Rà soát cuối kỳ từ tháng 4/2025
- Rủi ro lớn nếu không được gia hạn

## 4.5 Câu hỏi agent phải trả lời về vĩ mô

1. Giá #11 ở đâu? Xu hướng tăng/giảm?
2. Thuế CBPG còn hiệu lực? Khi nào hết hạn/review?
3. Ấn Độ siết hay mở xuất khẩu?
4. Brazil chuyển ethanol hay đường? (theo giá dầu)
5. Vụ ép VN tốt/xấu? CCS bao nhiêu?
6. QNS: Tách riêng đường vs Vinasoy
7. SBT: Doanh thu phụ phẩm bao nhiêu %?

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 P/E — Ngành chu kỳ (cẩn thận BẪY)

```
❌ "SBT P/E 6x = rẻ" → Giá #11 đang ĐỈNH, E sẽ giảm
✅ "SBT P/E 18x + giá #11 vừa đáy + Ấn Độ siết XK" → Cơ hội
```

**Normalized P/E (trung bình 3-5 năm):**
- SBT: 10-16x
- QNS: 8-14x

**P/E theo chu kỳ:**

| Pha | P/E điển hình | Hành động |
|---|---|---|
| Đáy | 15-20x (E thấp) | MUA (nếu có catalyst phục hồi) |
| Hồi phục | 10-14x | Giữ — giá tăng mạnh nhất |
| Đỉnh | 6-10x (E đỉnh) | BẪY → BÁN |
| Suy giảm | 8-12x | Tránh |

## 5.2 EV/EBITDA

- SBT: 5-9x
- So sánh peer khu vực: Khon Kaen (Thái Lan) 6-10x

## 5.3 Dividend Yield

| Mã | Đặc điểm | Yield điển hình |
|---|---|---|
| **SBT** | Không đều, theo chu kỳ | Giá cao: 5-8%, giá thấp: 2-3% |
| **QNS** | Đều hơn (Vinasoy ổn định) | 5-8% — QNS = "cổ phiếu cổ tức" tốt hơn SBT |

## 5.4 Bẫy định giá

| Bẫy | Thực tế | Cách tránh |
|---|---|---|
| "SBT P/E 7x = rẻ" | Giá đỉnh, E sẽ giảm 50% | Dùng Normalized P/E |
| "SBT yield 8%" | Năm giá cao, năm sau 3% | Dùng yield trung bình 3 năm |
| "QNS P/E 10x = rẻ" | Có thể vì đường yếu | Tách P/E đường vs Vinasoy |
| "LSS/SLS P/E thấp" | Thanh khoản kém, quy mô nhỏ | Discount cho liquidity |

## 5.5 Khi nào SBT RẺ thật

Cần 3/6 điều kiện:
1. #11 ở đáy (<$0.15/lb) + bắt đầu tăng
2. Ấn Độ hạn chế xuất khẩu
3. El Niño → hạn Brazil
4. Thuế CBPG duy trì/tăng
5. Giá dầu tăng (Brazil chuyển ethanol)
6. Vụ ép VN tốt (CCS cao)

## 5.6 Khi nào QNS RẺ thật

Cần 2/4 điều kiện:
1. Đường ở đáy chu kỳ
2. Vinasoy doanh thu tăng đều
3. Yield trung bình 3 năm >6%
4. P/E <10x

---

# LỚP 6: CASE STUDY LỊCH SỬ

### Case 1 — SBT 2021-2023: CBPG + giá đường = siêu chu kỳ

Thuế CBPG áp dụng từ 8/2021 + giá #11 tăng mạnh 2022-2023 → SBT lợi nhuận bùng nổ. Cổ phiếu từ ~15k lên ~28k. **Bài học:** CBPG là "lá chắn" quan trọng nhất cho ngành đường VN. Khi CBPG + giá #11 cùng thuận lợi = siêu chu kỳ.

### Case 2 — Niên độ 2025-2026: bức tranh "đắng"

Giá #11 giảm ~40% từ đỉnh + cung thừa toàn cầu + đường nhập lậu bùng phát → SBT, QNS kết quả kinh doanh thấp kỷ lục. LSS là hiếm hoi lợi nhuận tăng (nhờ kiểm soát chi phí). **Bài học:** Giá #11 giảm mạnh → toàn ngành chịu áp lực, không phân biệt quy mô.

### Case 3 — QNS: Vinasoy cứu đường

Nhiều quý đường yếu nhưng QNS lợi nhuận ổn định nhờ Vinasoy (~50% doanh thu) không theo chu kỳ đường. **Bài học:** QNS an toàn hơn SBT cho NĐT dài hạn muốn exposure ngành đường nhưng không muốn volatility cao.

### Case 4 — P/E trap Q4/2023

SBT P/E ~7x tại đỉnh giá #11 (10/2023). Nhiều phân tích kết luận "rẻ". Sau đó #11 giảm 40% → E giảm mạnh → P/E thực tế cao hơn nhiều. **Bài học:** P/E ngành chu kỳ phải xét theo phase chu kỳ, không so tuyệt đối.

---

# PHỤ LỤC

## A. Severity (màu sắc đánh giá tin)

| Màu | Điều kiện |
|---|---|
| **green** | #11 tăng + sản lượng tốt + biên mở | CBPG duy trì/tăng | Phụ phẩm DT tốt | Vụ ép CCS cao |
| **yellow** | #11 đi ngang | Lợi nhuận tăng nhờ phụ phẩm | Vụ ép trung bình | CBPG sắp review |
| **red** | #11 giảm mạnh | CBPG giảm/gỡ | Vụ ép kém | Đường Thái tràn vào | Lợi nhuận giảm/lỗ |
| **blue** | Trung tính — thông tin, không có impact rõ |

## B. Câu đánh giá mẫu

**SBT giá đường tốt:**
> "{ticker} lãi tăng {X}% nhờ giá đường quốc tế tăng {Y}% — hạn Brazil + Ấn Độ siết xuất khẩu. Vụ ép chất lượng tốt, ép nhiều đường/tấn mía. Công ty còn lời từ điện bã mía + cồn."

**SBT giá đường giảm:**
> "{ticker} lãi giảm {X}% vì giá đường quốc tế giảm {Y}% — Ấn Độ mở xuất khẩu tăng cung. Biên mỏng nên giá giảm 5% = lợi nhuận giảm 30-40%. Thuế bảo vệ vẫn còn — không có sẽ tệ hơn."

**Thuế CBPG:**
> "Tích cực: Thuế đánh vào đường Thái duy trì — VN không bị cạnh tranh rẻ. Không có thuế, Thái rẻ hơn ~20%. Hết hạn {tháng/năm} — cần theo dõi rà soát."

**Đáy chu kỳ:**
> "Giá đường quốc tế giảm {X}% từ đỉnh, lợi nhuận {ticker} giảm {Y}%. Tuy nhiên, hạn Brazil + Ấn Độ siết xuất khẩu — hai nước lớn nhất cùng giảm cung, giá thường hồi phục."

## C. Quy tắc cho agent

1. **Giá #11 = #1** → CHECK TRƯỚC mọi phân tích
2. **Thuế CBPG = "lá chắn sống còn"** → MENTION + check hạn review
3. **SBT biên MỎNG** → Giá ±5% = Lợi nhuận ±30-50%
4. **Phụ phẩm = "bộ đệm"** → TÁCH doanh thu đường vs phụ phẩm
5. **QNS = 2 ngành** → TÁCH đường vs Vinasoy
6. **P/E đỉnh giá = BẪY** → dùng Normalized P/E
7. **Brazil + Ấn Độ quyết định cung** → theo dõi chính sách + thời tiết
8. **Vụ ép T10-T4** → Doanh thu mùa vụ RÕ → so cùng kỳ
9. **KHÔNG dùng thuật ngữ** → DỊCH sang tiếng Việt
10. **KHÔNG bịa số** → Thiếu data → nói thiếu

## D. Thuật ngữ → Tiếng Việt

| Thuật ngữ | Dịch |
|---|---|
| Giá #11 tăng | Giá đường quốc tế tăng — bán được giá cao hơn |
| Thuế CBPG | Thuế chống bán phá giá đánh vào đường Thái nhập VN — giúp VN không bị cạnh tranh rẻ |
| CCS cao | Mía chất lượng tốt — ép nhiều đường hơn/tấn mía |
| El Niño | Nắng nóng ở nước trồng mía lớn → sản lượng giảm → giá tăng |
| Brazil chuyển ethanol | Brazil dùng mía làm nhiên liệu thay đường → ít đường → giá tăng |
| Phụ phẩm | Đốt bã mía phát điện + làm cồn — nguồn thu bổ sung |
| Biên 12% | Bán 100 đồng lời 12 đồng — mỏng, giá ±5% ảnh hưởng lớn |
| Vụ ép | Mùa thu hoạch mía (T10→T4) — nhà máy chạy hết công suất |
| Tinh luyện | Chuyển đường thô thành đường trắng tinh khiết |
| YoY | So với cùng kỳ năm trước |
| QoQ | So với quý trước |

---

## Hướng dẫn tra dữ liệu thời gian thực (cho Master Sugar)

KB master này chỉ cung cấp framework + threshold + range historical. Khi viết bài cụ thể, Master phải:

1. **Query KB framework** (file này) — static guidance
2. **Web search** cho data realtime:
   - Giá ICE #11 hiện tại (tradingeconomics, investing.com)
   - Tin tức ngành đường VN (cafef, vietstock, baodautu)
   - Chính sách Ấn Độ, Brazil mới nhất
   - Thuế CBPG update (Bộ Công Thương)
3. **BCTC công ty** từ website IR hoặc vietstock/cafef

---

## Cross-link (dự kiến)

| Deep dive | Nội dung chính |
|---|---|
| `sugar-cbpg-timeline.md` | Lịch sử thuế CBPG VN + timeline review |
| `sugar-brazil-ethanol.md` | Cơ chế Brazil chọn ethanol vs đường |
| `sugar-company-profiles.md` | Profile chi tiết SBT, QNS, LSS, SLS |

---

## Phần suy luận (cần verify)

- **"SBT 35-40% thị phần"** — tổng hợp từ nhiều nguồn, cần verify từ báo cáo thường niên SBT
- **"CBPG 42.99% + CTC 4.65%"** — từ QĐ 477/QĐ-BCT, hiệu lực đến 15/6/2026
- **"Năng suất mía VN 55-65 tấn/ha vs Thái 70-80"** — approximate, cần verify từ Hiệp hội Mía đường VN
- **"Giá #11 $0.14/lb (5/2026)"** — từ web search 5/2026, giá biến động hàng ngày
