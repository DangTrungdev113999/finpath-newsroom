---
category: frameworks
title: "Insurance-Industry-Master-Reference"
last_updated: 2026-05-12
---

Master reference cho Master Insurance — mental model 6 lớp phân tích ngành bảo hiểm VN. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **BVH · PVI · BMI · BIC · MIG · PTI · PGI · VNR · PRE**. Source gốc từ `agents/Sector_Insurance/knowledge.md` + web research 05/2026.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Insurance/knowledge.md + web research. Thêm universe niêm yết chi tiết, metrics benchmark 2024-2025, bancassurance crisis context, hard/soft market cycle. |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Mô hình kinh doanh

Công ty bảo hiểm Việt Nam sinh lợi nhuận từ hai nguồn chính:

- **Lợi nhuận bảo hiểm (Underwriting) — 30-50%:** Thu phí - Bồi thường - Chi phí = Lãi/Lỗ bảo hiểm
- **Lợi nhuận đầu tư — 50-70% (NGUỒN CHÍNH):** Float (tiền chờ bồi thường) → đầu tư: trái phiếu, tiền gửi, chứng khoán, bất động sản

> **Nguyên tắc cốt lõi**: Nhiều công ty chấp nhận LỖ bảo hiểm miễn LÃI đầu tư bù lại. Phân tích bảo hiểm VN = 50% phân tích đầu tư.

## 1.2 Phân loại — 3 nhóm chính

### Bảo hiểm phi nhân thọ (Non-life)

| Mã | Tên | Sàn | Đặc trưng cấu trúc |
|---|---|---|---|
| **BVH** | Tập đoàn Bảo Việt | HOSE | Lớn nhất — nhân thọ + phi nhân thọ + đầu tư; cần phân tích 3 mảng riêng |
| **PVI** | PVI Holdings | HNX | Thị phần phi nhân thọ #1 (~16%); hệ sinh thái PVN; tăng giá mạnh nhất 2024-2025 (+59%) |
| **BMI** | Bảo Minh | HOSE | Chi phối nhà nước; đang tái cấu trúc 2025-2026; mạng lưới miền Nam |
| **BIC** | Bảo hiểm BIDV | HOSE | Hệ sinh thái BIDV; bancassurance channel với ngân hàng mẹ |
| **MIG** | Bảo hiểm Quân đội (MIC) | HOSE | Hệ sinh thái MB; bancassurance + bảo hiểm quân đội |
| **PTI** | Bảo hiểm Bưu điện | HNX | Forbes Top 50 Niêm yết 2025; thanh khoản bùng nổ 2025 (x38 lần) |
| **PGI** | Bảo hiểm Petrolimex (PJICO) | HOSE | Niche năng lượng/xăng dầu; mạng lưới Petrolimex |

### Tái bảo hiểm (Reinsurance)

| Mã | Tên | Sàn | Đặc trưng cấu trúc |
|---|---|---|---|
| **VNR** | Tái bảo hiểm Quốc gia (Vinare) | HNX | Tái bảo hiểm duy nhất niêm yết lớn; ít cạnh tranh; biên cao |
| **PRE** | Tái bảo hiểm Hà Nội | HNX | Tái bảo hiểm mid-cap; đa dạng hóa danh mục |

### Bảo hiểm nhân thọ (Life)

- **Manulife, Prudential, AIA, Dai-ichi**: KHÔNG niêm yết → chỉ phân tích gián tiếp qua BVH (mảng nhân thọ chiếm ~50% lợi nhuận BVH)
- Nhân thọ VN đang khủng hoảng 2023-2025: doanh thu giảm 3 năm liên tiếp (2023: -12%, 2024: -5.7%, 2025F: -1.3%)

## 1.3 Universe niêm yết — 9 mã

**HOSE (5):** BVH · BMI · BIC · MIG · PGI

**HNX (4):** PVI · PTI · VNR · PRE

> **Decision rule phân loại**: Phi nhân thọ = hợp đồng 1 năm, bồi thường nhanh, cạnh tranh giá khốc liệt. Nhân thọ = hợp đồng 10-30 năm, float lớn hơn, đang crisis. Tái bảo hiểm = ít cạnh tranh, biên cao nhưng nhạy thiên tai lớn.

## 1.4 Quản lý ngành

- **Bộ Tài chính**: Quy định dự phòng, an toàn vốn, phê duyệt sản phẩm mới
- **Luật Kinh doanh Bảo hiểm 2023 + Thông tư 67**: Siết chặt bancassurance — cấm bán bảo hiểm liên kết đầu tư 60 ngày trước/sau giải ngân khoản vay
- **Luật Tín dụng 2024 (có hiệu lực 07/2024)**: Cấm ngân hàng bán kèm bảo hiểm không bắt buộc với dịch vụ tài chính
- **Bảo hiểm bắt buộc**: Xe cơ giới, cháy nổ, xây dựng — nguồn thu ổn định

## 1.5 Đặc thù thị trường Việt Nam

- **Thâm nhập thấp**: ~3.5% GDP (Thái Lan 5%, Singapore 9%) → dư địa tăng trưởng lớn dài hạn
- **Bancassurance khủng hoảng 2023-2025**: Bùng nổ 2020-2022 → scandal mis-selling 2023-2024 → hủy hợp đồng hàng loạt → quy định siết chặt
- **Cạnh tranh khốc liệt phi nhân thọ**: ~30 công ty, race to bottom về phí
- **Danh mục đầu tư điển hình**: 30-40% tiền gửi + 20-30% trái phiếu + 10-20% cổ phiếu (BIẾN ĐỘNG) + 5-10% bất động sản

## 1.6 Mùa vụ

| Quý | Phí bảo hiểm | Bồi thường | Lợi nhuận đầu tư |
|---|---|---|---|
| Q1 | Trung bình | Thấp | Theo TTCK + lãi suất |
| Q2 | Tăng | Trung bình | Theo TTCK + lãi suất |
| Q3 | Trung bình | **Cao (mùa bão T8-10)** | Theo TTCK + lãi suất |
| Q4 | Cao | Trung bình - Cao | Theo TTCK + lãi suất |

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics quan trọng

### Tier 1 — Thị trường phản ứng ngay

| Metric | Ý nghĩa | Benchmark VN |
|---|---|---|
| **Combined Ratio (CR)** | Chi phí bảo hiểm / Phí thu | <95%: Tốt, 95-100%: Trung bình, >100%: Xấu |
| **Tăng trưởng phí gốc** | Doanh thu bảo hiểm tăng | Phi nhân thọ: 10-12%/năm (2024-2025); Nhân thọ: âm 2023-2025 |
| **Lợi nhuận đầu tư** | 50-70% tổng lợi nhuận | Nhạy với lãi suất + TTCK |
| **Loss ratio** | Bồi thường / Phí | <60%: Tốt, 60-70%: TB, >75%: Xấu (VN trung bình ~35% phi nhân thọ) |

### Tier 2 — Phản ứng 1-3 quý

| Metric | Benchmark |
|---|---|
| Expense ratio | <30%: Tốt, >35%: Cao |
| Dự phòng bồi thường | Tăng = nhiều claim chờ xử lý |
| Danh mục đầu tư | Nhiều cổ phiếu = biến động lớn |
| Phí mới nhân thọ | Giảm = bancassurance yếu (BVH focus) |

### Tier 3 — Dài hạn

- Tỷ lệ thâm nhập bảo hiểm / GDP
- Retention rate (nhân thọ)
- Embedded Value (nhân thọ — BVH)
- Solvency ratio (hệ số khả năng thanh toán)

## 2.2 Combined Ratio — Chỉ số cốt lõi phi nhân thọ

```
CR = Loss Ratio + Expense Ratio

< 95%:     Xuất sắc — lãi bảo hiểm
95-100%:   Hòa vốn bảo hiểm — sống bằng lãi đầu tư
100-105%:  Lỗ bảo hiểm nhẹ
> 105%:    Lỗ nặng
> 110%:    Nguy hiểm

Bảo hiểm VN thường CR 95-105% → sống bằng lãi đầu tư
Benchmark tốt theo Bộ Tài chính: 96.5-98%
```

> **Lưu ý**: Cách tính CR theo quy định Bộ Tài chính VN khác chuẩn quốc tế → CR báo cáo VN thường thấp (thuận lợi) hơn cùng công ty tính theo chuẩn global.

## 2.3 Lợi nhuận đầu tư — Nguồn chính

```
Danh mục điển hình:
- Tiền gửi ngân hàng: 30-40%
- Trái phiếu: 20-30%
- Cổ phiếu: 10-20% (BIẾN ĐỘNG LỚN)
- Bất động sản: 5-10%

Lãi suất↑ → Lợi nhuận đầu tư TỐT (tiền gửi + TP mới yield cao)
Lãi suất↓ → Lợi nhuận đầu tư YẾU
TTCK↑ → Lợi nhuận TỐT (lãi danh mục cổ phiếu)
TTCK↓ → Lợi nhuận XẤU (có thể lỗ trên giấy hoặc thực)
```

## 2.4 BVH — Phân tích 3 mảng BẮT BUỘC

```
1. Nhân thọ (~50% lợi nhuận): phí mới, retention, bancassurance
2. Phi nhân thọ (~25% lợi nhuận): CR, bồi thường, thị phần
3. Quản lý quỹ (~15% lợi nhuận): danh mục, lãi/lỗ chứng khoán
4. Khác (~10%): Bất động sản, dịch vụ
```

## 2.5 Bẫy BCTC bảo hiểm

| Bẫy | Cách check |
|---|---|
| "Lợi nhuận tăng 30%" | Lợi nhuận bảo hiểm vs lợi nhuận đầu tư? CR bao nhiêu? |
| "Phí tăng 15%" | CR tăng hay giảm? Có phải race to bottom? |
| "Bồi thường giảm" | Dự phòng tăng hay giảm? Shift claim sang năm sau? |
| "Phí mới tăng" (nhân thọ) | Retention rate? Complaint rate? Hủy hợp đồng? |
| "Lãi đầu tư kỷ lục" | Lãi đã hiện thực hay còn trên giấy? % cổ phiếu trong danh mục? |

## 2.6 Checklist BCTC bảo hiểm (7 câu hỏi)

1. CR bao nhiêu? <100% hay >100%?
2. Phí gốc tăng/giảm so cùng kỳ? So quý trước?
3. Bồi thường có đột biến không? (thiên tai, dịch bệnh?)
4. Lợi nhuận đầu tư từ đâu? Đã hiện thực hay chưa?
5. Danh mục: % cổ phiếu vs trái phiếu vs tiền gửi?
6. BVH: tách 3 mảng riêng biệt
7. Vĩ mô: lãi suất? TTCK? Thiên tai? Bancassurance?

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Nguyên tắc cốt lõi

```
2 CHU KỲ CHỒNG NHAU:

1. UNDERWRITING CYCLE (5-7 năm)
   Soft market (3-4 năm): Cạnh tranh giảm phí → CR↑ → lỗ bảo hiểm
   Hard market (2-3 năm): Tăng phí đồng loạt → CR↓ → lãi bảo hiểm

2. CHU KỲ ĐẦU TƯ (theo TTCK + lãi suất)
   Lãi suất↑ + TTCK↑ → Lợi nhuận đầu tư tốt
   Lãi suất↓ + TTCK↓ → Lợi nhuận đầu tư yếu
```

## 3.2 Chu kỳ underwriting

```
GĐ1: SOFT MARKET
├── Cạnh tranh giảm phí → CR↑ → nhiều công ty lỗ
├── Công ty nhỏ phá sản/rút lui
└── Giá cổ phiếu: Giảm/đi ngang

GĐ2: CHUYỂN GIAO (trigger: thiên tai lớn / nhiều công ty lỗ nặng)
├── Bồi thường khổng lồ → buộc tăng phí
├── Giá cổ phiếu: Giảm mạnh ngắn hạn → hồi nhanh
└── ĐIỂM MUA

GĐ3: HARD MARKET
├── Phí tăng 10-20% đồng loạt → CR↓ → Lợi nhuận tăng mạnh
├── Giá cổ phiếu: TĂNG MẠNH NHẤT
└── Kéo dài 2-3 năm

GĐ4: TRỞ LẠI CẠNH TRANH → Quay về GĐ1
```

## 3.3 Tín hiệu nhận diện

### Đáy (→ hard market) — Cơ hội MUA

1. CR ngành >100% nhiều quý liên tiếp
2. Công ty nhỏ rút lui/phá sản
3. Thiên tai lớn (bão, lũ)
4. Bắt đầu tăng phí đồng loạt
5. Lãi suất tăng

### Đỉnh (→ soft market) — Cân nhắc THOÁT

1. CR <90% (quá tốt — sắp có cạnh tranh mới)
2. Công ty mới gia nhập thị trường
3. Phí bắt đầu giảm
4. TTCK giảm mạnh

---

# LỚP 4: HIỂU VĨ MÔ

## 4.1 Yếu tố vĩ mô tác động

| Yếu tố | Tác động | Mức độ |
|---|---|---|
| **Lãi suất** | #1: ↑ → Lợi nhuận đầu tư tốt | Rất cao |
| **TTCK** | #2: ↑ → Danh mục cổ phiếu lãi | Cao |
| **Thiên tai** | Ngắn hạn lỗ → sau đó phí↑ | Cao (mùa bão Q3) |
| **GDP/Thu nhập** | ↑ → Nhu cầu bảo hiểm tăng | Trung bình |
| **Bảo hiểm bắt buộc** | Mở rộng → Doanh thu↑ ổn định | Trung bình |
| **Bancassurance** | Kênh bán chính nhân thọ; scandal ảnh hưởng lớn | Rất cao (BVH) |

## 4.2 Ma trận nhạy cảm

| Yếu tố | Phi nhân thọ | Nhân thọ | Tái bảo hiểm | Lợi nhuận đầu tư |
|---|---|---|---|---|
| Lãi suất↑ | Trung lập | Trung lập | Trung lập | **Tốt mạnh** |
| Lãi suất↓ | Trung lập | Trung lập | Trung lập | **Xấu mạnh** |
| TTCK↑ | Trung lập | Trung lập | Trung lập | **Tốt** |
| TTCK↓ | Trung lập | Trung lập | Trung lập | **Xấu** |
| Thiên tai | **Xấu mạnh** | Trung lập | **Xấu mạnh** | Trung lập |
| Thu nhập↑ | Tốt | **Tốt mạnh** | Tốt | Trung lập |
| Bancassurance scandal | Trung lập | **Xấu mạnh** | Trung lập | Trung lập |

## 4.3 Động lực tăng trưởng

**Cấu trúc (dài hạn):**
- Thâm nhập ~3.5% GDP → dư địa gấp đôi so khu vực
- Đô thị hóa + thu nhập tầng lớp trung lưu tăng
- Già hóa dân số → bảo hiểm sức khỏe + hưu trí tăng
- Số hóa → giảm chi phí vận hành

**Chu kỳ (ngắn hạn):**
- Lãi suất↑ → lãi đầu tư tốt
- Soft → Hard market
- Sau thiên tai → nhu cầu↑ + phí↑
- Bancassurance hồi phục (dự kiến từ 2026)

## 4.4 Rủi ro

**Cấu trúc:**
1. Thiên tai lớn liên tiếp → lỗ nhiều quý
2. Soft market kéo dài → CR xấu dai dẳng
3. TTCK↓ kéo dài → lỗ danh mục cổ phiếu
4. Lãi suất↓ → lợi nhuận đầu tư yếu
5. Bancassurance scandal tiếp tục → nhân thọ chưa phục hồi

**Chu kỳ:**
1. Bão lớn Q3 → bồi thường đột biến
2. TTCK điều chỉnh mạnh → lỗ trên giấy/thực
3. Quy định mới siết chặt

## 4.5 Context 2024-2025

- **Phi nhân thọ hồi phục mạnh**: +10.2% năm 2024, dự kiến +10.3% năm 2025
- **Nhân thọ tiếp tục co lại**: -5.7% năm 2024, dự kiến -1.3% năm 2025 → phục hồi từ 2026
- **Bancassurance crisis**: Luật mới cấm bán kèm có hiệu lực 07/2024 → kênh bán yếu đi
- **PVI outperform**: +59% năm 2025, thị phần #1 phi nhân thọ (~16%)

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 Phương pháp định giá phổ biến

- **P/B (giá / giá trị sổ sách)**: Phương pháp chính cho bảo hiểm VN
- **P/E điều chỉnh**: Loại bỏ lãi/lỗ một lần (đặc biệt lãi/lỗ chứng khoán chưa hiện thực)
- **Embedded Value (EV)**: Chỉ áp dụng mảng nhân thọ (BVH)

## 5.2 Vùng định giá tham chiếu (P/B)

| Ticker | P/B thông thường | Ghi chú |
|---|---|---|
| BVH | 1.5-2.5x | Premium — lớn nhất, đa dạng hóa |
| PVI | 1.2-2.0x | Thị phần #1 phi nhân thọ |
| BMI, BIC | 1.0-1.8x | Mid-tier, ổn định |
| VNR | 1.0-1.5x | Tái bảo hiểm, biên cao |
| Bảo hiểm nhỏ | 0.8-1.2x | Thanh khoản thấp |

**Soft market**: P/B thấp → cơ hội nếu sắp hard market
**Hard market**: P/B cao → cẩn thận nếu sắp soft market

## 5.3 P/E — Cẩn thận

- Dùng P/E trailing 12 tháng hoặc trung bình 3 năm
- Loại bồi thường đột biến + lãi/lỗ chứng khoán chưa hiện thực
- BVH: 12-20x | BMI, BIC: 8-15x | VNR: 8-12x

## 5.4 Embedded Value — Nhân thọ (BVH)

```
P/EV (Giá / Embedded Value):
< 1.0x: Rẻ
1.0-1.5x: Hợp lý
> 2.0x: Đắt

Chỉ áp dụng mảng nhân thọ BVH
```

## 5.5 Bẫy định giá

- P/E thấp có thể do lợi nhuận cao bất thường (lãi cổ phiếu)
- P/B thấp có thể do EV giảm (bancassurance yếu — BVH)
- CR quá tốt (<90%) → sắp thu hút cạnh tranh → margin compression

---

# LỚP 6: CASE STUDY LỊCH SỬ

### Bancassurance Crisis 2023-2025

Giai đoạn 2020-2022 bancassurance bùng nổ — ngân hàng đẩy mạnh bán bảo hiểm nhân thọ cho khách hàng vay. 2023-2024 scandal mis-selling bùng phát: khách hàng phát hiện mua bảo hiểm không phù hợp, hủy hợp đồng hàng loạt, khiếu nại tăng vọt. Luật Kinh doanh Bảo hiểm 2023 + Thông tư 67 + Luật Tín dụng 2024 siết chặt → kênh bancassurance yếu đi rõ rệt. **Bài học**: Kênh phân phối mạnh nhưng rủi ro pháp lý cao; nhân thọ VN mất 3 năm (2023-2025) để hấp thụ khủng hoảng, dự kiến phục hồi từ 2026.

### PVI Outperform 2024-2025

PVI Holdings (mã PVI trên HNX) tăng giá +59% năm 2025, đánh dấu năm thứ hai liên tiếp dẫn đầu ngành. Thị phần phi nhân thọ #1 (~16%), hưởng lợi từ hệ sinh thái PVN (dầu khí), CR ổn định. **Bài học**: Thị phần + hệ sinh thái mạnh = lợi thế cạnh tranh bền vững trong ngành cạnh tranh cao.

### PTI — Bùng nổ thanh khoản 2025

PTI (Bảo hiểm Bưu điện) thanh khoản tăng x38 lần so năm trước, được Forbes vinh danh Top 50 Niêm yết 2025, dù lợi nhuận ròng 9 tháng giảm 8%. **Bài học**: Thanh khoản không luôn tương quan với fundamentals — có thể do expectation rotation hoặc flow chuyển từ mã khác.

---

## Hướng dẫn tra dữ liệu thời gian thực (cho Master Insurance)

KB master này chỉ cung cấp framework + threshold + range historical. Khi viết bài quarter cụ thể, Master phải:

1. **Query KB framework** (file này) — static guidance
2. **Finpath API** cho data realtime (nếu có):
   - `get_income_statement(ticker)` + `get_balance_sheet(ticker)` — BCTC quarter
   - `get_financial_ratios(ticker)` — PE/PB/ROE
   - `get_shareholders(ticker)` + `get_events(ticker)` + `get_news(ticker)` — ownership + ĐHĐCĐ + tin
3. **Web_search** cho data Finpath API không có:
   - CR, loss ratio, expense ratio từ BCTC công ty
   - Thị phần phi nhân thọ/nhân thọ từ Bộ Tài chính
   - Bancassurance metrics từ tin tức
   - Thiên tai / bồi thường đột biến

---

## Thuật ngữ tiếng Việt (ánh xạ cứng)

| Thuật ngữ | Tiếng Việt |
|---|---|
| Combined Ratio (CR) | tỷ lệ kết hợp |
| Loss Ratio | tỷ lệ bồi thường |
| Expense Ratio | tỷ lệ chi phí |
| Premium | phí bảo hiểm |
| Float | tiền chờ bồi thường (dùng để đầu tư) |
| Underwriting | hoạt động bảo hiểm gốc |
| Claim | yêu cầu bồi thường |
| Solvency Ratio | hệ số khả năng thanh toán |
| Embedded Value (EV) | giá trị nội tại (nhân thọ) |
| Bancassurance | bán bảo hiểm qua ngân hàng |
| Soft Market | thị trường cạnh tranh giảm phí |
| Hard Market | thị trường đồng loạt tăng phí |
| Retention Rate | tỷ lệ giữ chân khách hàng |
| Non-life | phi nhân thọ |
| Life | nhân thọ |
| Reinsurance | tái bảo hiểm |

---

## Cross-link

| File | Nội dung |
|---|---|
| `agents/Sector_Insurance/knowledge.md` | Source gốc — agent knowledge base |

---

## Phần suy luận (cần verify)

Các điểm dưới đây rút từ framework + web search — cần verify khi đưa vào bài cụ thể:

- **"PVI thị phần #1 phi nhân thọ ~16%"** — từ web search 05/2026, cần verify với Bộ Tài chính data mới nhất
- **"Loss ratio trung bình phi nhân thọ VN ~35%"** — số liệu 2022, cần verify số mới hơn
- **"CR benchmark 96.5-98%"** — theo Bộ Tài chính, nhưng cách tính VN khác quốc tế
- **"Nhân thọ -1.3% năm 2025"** — forecast GlobalData, cần verify actual khi có
- **"Phi nhân thọ +10.3% năm 2025"** — forecast, cần verify actual khi có

---

## Sources (web research 05/2026)

- [Cổ phiếu ngành bảo hiểm năm 2025 - Topi](https://topi.vn/co-phieu-nganh-bao-hiem.html)
- [PTI Forbes Top 50 2025 - IPA](https://www.ipa.com.vn/pti-duoc-forbes-vinh-danh-top-50-cong-ty-niem-yet-tot-nhat-2025/)
- [Giữ cổ phiếu bảo hiểm nào khiến nhà đầu tư "đau ví" nhất - Vietstock](https://vietstock.vn/2026/01/giu-co-phieu-bao-hiem-nao-khien-nha-dau-tu-dau-vi-nhat-830-1390854.htm)
- [Các chỉ số tài chính quan trọng khi phân tích ngành Bảo hiểm - WiData](https://widata.vn/blogs/cac-chi-so-tai-chinh-quan-trong-khi-phan-tich-nganh-bao-hiem-310)
- [Vietnam's Non-Life Insurance Sector - Vietnam Briefing](https://www.vietnam-briefing.com/news/vietnams-non-life-insurance-sector-attracts-strong-fdi-amid-favorable-regulatory-changes.html/)
- [Vietnam life insurance market forecast - GlobalData](https://www.globaldata.com/media/insurance/vietnam-life-insurance-market-contract-third-consecutive-year-2025-forecasts-globaldata/)
- [Vietnam insurance premium revenue 2024 - The Investor](https://theinvestor.vn/vietnams-insurance-premium-revenue-declines-in-2024-for-second-consecutive-year-d13973.html)
- [Best's Commentary: Bancassurance Regulatory Scrutiny - AM Best](https://news.ambest.com/PR/PressContent.aspx?refnum=34485&altsrc=9)
