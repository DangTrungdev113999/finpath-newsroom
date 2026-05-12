---
category: frameworks
title: "Retail-Inventory-Cycle"
last_updated: 2026-05-12
---

Deep dive về rủi ro hàng tồn kho (HTK) trong ngành bán lẻ — yếu tố quyết định biên lợi nhuận và dòng tiền.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ knowledge.md |

---

# TẠI SAO HTK QUAN TRỌNG VỚI BÁN LẺ?

## Đặc thù ngành bán lẻ

- **Vốn lưu động lớn:** HTK thường chiếm 30-50% tổng tài sản
- **Hàng mất giá nhanh:** Đặc biệt điện tử, thời trang
- **Biên mỏng:** Nếu phải xả giá HTK cũ → ăn mòn toàn bộ lợi nhuận
- **Dòng tiền:** HTK tăng = tiền bị "kẹt" trong hàng hoá

## Mối quan hệ HTK — Lợi nhuận

```
HTK tăng + Vòng quay giảm → Hàng bán chậm → Phải giảm giá → Biên giảm → Lợi nhuận giảm
```

> **Quy tắc:** Báo động đỏ khi: HTK tăng nhanh hơn doanh thu + Vòng quay giảm.

---

# RỦI RO HTK THEO LOẠI HÀNG

| Loại hàng | Tốc độ mất giá | Vòng quay benchmark | Rủi ro |
|---|---|---|---|
| Điện thoại | 20-30% / 6 tháng | 6-8 lần/năm | **Rất cao** |
| Laptop | 15-20% / 6 tháng | 5-7 lần/năm | Cao |
| TV/Gia dụng | 10-15% / năm | 4-6 lần/năm | Trung bình |
| Thực phẩm tươi | Hỏng 3-7 ngày | 15-20 lần/năm | Cao (vòng quay bù) |
| Thực phẩm khô/FMCG | Hạn 6-24 tháng | 10-12 lần/năm | Trung bình |
| Thuốc | Hạn 1-3 năm | 4-6 lần/năm | **Thấp** |
| Trang sức vàng | Không mất giá | 2-4 lần/năm | **Thấp** (giá vàng bảo toàn) |

## Giải thích chi tiết

### Điện thoại — Rủi ro cao nhất

- **iPhone:** Giảm 20-30% ngay khi model mới ra
- **Android:** Giảm nhanh hơn do nhiều model mới liên tục
- **Chu kỳ:** Q3-Q4 iPhone mới → Q1-Q2 model cũ mất giá mạnh

**Ví dụ:** MWG Q1/2023 phải xả HTK iPhone 13 khi iPhone 14 ra → biên gộp giảm ~200bps

### Laptop — Rủi ro cao

- **Chu kỳ chip:** Intel/AMD/Apple Silicon ra chip mới → laptop cũ mất giá
- **Back to school:** Q3 là mùa cao điểm → Q4-Q1 HTK cũ tồn

### Thực phẩm tươi — Rủi ro đặc biệt

- **Hao hụt cao:** 5-15% hàng bị hỏng/vứt bỏ
- **Vòng quay rất nhanh:** Phải bán trong 3-7 ngày
- **BHX case:** Biên gộp 22-26% nhưng hao hụt 8-12% → biên thực ~15%

### Thuốc — Rủi ro thấp

- **Nhu cầu ổn định:** Không phụ thuộc chu kỳ kinh tế
- **Hạn dài:** 1-3 năm → không áp lực xả giá
- **Không giảm giá:** Giá thuốc ít khi discount

### Trang sức vàng — Rủi ro đặc biệt thấp

- **Giá vàng bảo toàn:** HTK vàng không mất giá theo thời gian
- **Thậm chí tăng:** Nếu giá vàng tăng → HTK lãi
- **Rủi ro:** Chỉ khi giá vàng giảm mạnh (hiếm)

---

# CHỈ SỐ THEO DÕI HTK

## 1. Vòng quay hàng tồn kho (Inventory Turnover)

```
Vòng quay HTK = Giá vốn hàng bán / HTK bình quân
```

| Phân khúc | Tốt | Trung bình | Xấu |
|---|---|---|---|
| CE | >8x | 6-8x | <6x |
| Grocery | >15x | 12-15x | <12x |
| Dược | >6x | 4-6x | <4x |
| ICT B2B | >10x | 8-10x | <8x |

## 2. Số ngày tồn kho (Days Inventory Outstanding)

```
Số ngày HTK = 365 / Vòng quay HTK
```

| Phân khúc | Tốt | Trung bình | Xấu |
|---|---|---|---|
| CE | <45 ngày | 45-60 ngày | >60 ngày |
| Grocery | <25 ngày | 25-30 ngày | >30 ngày |
| Dược | <60 ngày | 60-90 ngày | >90 ngày |

## 3. Tốc độ tăng HTK vs Doanh thu

| Kịch bản | HTK YoY | DT YoY | Đánh giá |
|---|---|---|---|
| **Lành mạnh** | +10% | +15% | HTK tăng chậm hơn DT → hiệu quả |
| **Trung bình** | +15% | +15% | HTK = DT → theo dõi tiếp |
| **Cảnh báo** | +25% | +15% | HTK tăng nhanh hơn DT → hàng bán chậm |
| **Báo động** | +30% | +5% | HTK tăng mạnh, DT stagnant → sắp xả giá |

---

# PHÂN TÍCH HTK TRONG BCTC

## Bước 1: Đọc số liệu HTK

- **Cân đối kế toán:** Khoản mục "Hàng tồn kho"
- **So sánh YoY và QoQ** (nhớ seasonal effect)
- **Thuyết minh BCTC:** Chi tiết cơ cấu HTK (hàng mua, hàng sản xuất, hàng gửi bán)

## Bước 2: Tính vòng quay

```
Vòng quay = GVHB (4 quý gần nhất) / HTK bình quân
```

## Bước 3: So sánh với benchmark

- So với benchmark phân khúc
- So với chính DN kỳ trước
- So với đối thủ cùng ngành

## Bước 4: Đối chiếu với biên gộp

| HTK | Biên gộp | Đánh giá |
|---|---|---|
| Giảm | Tăng | **Tốt:** Bán hết hàng cũ, không cần discount |
| Giảm | Giảm | **Xấu:** Xả giá để giảm HTK |
| Tăng | Tăng | **Tạm OK:** Dự trữ hàng biên cao |
| Tăng | Giảm | **Nguy hiểm:** Hàng tồn + phải discount |

---

# CHU KỲ HTK VÀ GIÁ CỔ PHIẾU

## Mối quan hệ HTK — Chu kỳ

| Giai đoạn | HTK | Vòng quay | Biên gộp | Giá CP |
|---|---|---|---|---|
| **Đỉnh** | Tăng mạnh | Giảm | Đỉnh (sắp giảm) | Bắt đầu giảm |
| **Suy thoái** | Cao | Thấp | Giảm (xả giá) | Giảm mạnh |
| **Đáy** | Bắt đầu giảm | Đáy | Đáy | Bắt đầu tăng |
| **Hồi phục** | Tiếp tục giảm | Tăng | Cải thiện | Tăng mạnh |
| **Tăng trưởng** | Ổn định/Tăng nhẹ | Ổn định | Ổn định | Tăng chậm |

## Tín hiệu từ HTK

### Tín hiệu đáy (mua)

1. HTK bắt đầu giảm sau nhiều quý tăng
2. Vòng quay ngừng giảm / bắt đầu tăng
3. DN công bố đã xả xong hàng cũ
4. Biên gộp ngừng giảm

### Tín hiệu đỉnh (bán)

1. HTK tăng đột biến (+30%+ YoY)
2. Vòng quay giảm 2 quý liên tiếp
3. DT tăng chậm hơn HTK
4. Chu kỳ sản phẩm sắp kết thúc (iPhone mới sắp ra)

---

# CASE STUDY: MWG 2022

## Bối cảnh

- Q2/2022: iPhone 13 series đang bán
- Q3-Q4/2022: iPhone 14 ra → iPhone 13 lỗi thời
- Sức mua giảm do lãi suất tăng

## Diễn biến HTK

| Quý | HTK (tỷ) | YoY | Vòng quay | Biên gộp |
|---|---|---|---|---|
| Q1/2022 | 25.000 | +40% | 7.5x | 22.5% |
| Q2/2022 | 28.000 | +45% | 7.0x | 22.0% |
| Q3/2022 | 30.000 | +50% | 6.5x | 21.0% |
| Q4/2022 | 26.000 | +20% | 6.8x | 20.0% |
| Q1/2023 | 22.000 | -12% | 7.2x | 20.5% |

## Bài học

1. **Q1-Q2/2022:** HTK tăng mạnh = dấu hiệu cảnh báo
2. **Q3/2022:** Vòng quay giảm + Biên giảm = xả giá đang diễn ra
3. **Q4/2022:** HTK bắt đầu giảm = signal tích cực
4. **Q1/2023:** HTK giảm rõ + Vòng quay cải thiện = đáy chu kỳ

---

# CHECKLIST PHÂN TÍCH HTK

1. [ ] HTK YoY tăng/giảm bao nhiêu %?
2. [ ] So với doanh thu YoY thì nhanh hơn hay chậm hơn?
3. [ ] Vòng quay HTK là bao nhiêu? So với benchmark ngành?
4. [ ] Vòng quay trend 4 quý: cải thiện hay xấu đi?
5. [ ] Biên gộp trend ra sao? Có đang giảm cùng HTK tăng?
6. [ ] Cơ cấu HTK: hàng nào chiếm tỷ trọng lớn? Hàng nào rủi ro cao?
7. [ ] Có chu kỳ sản phẩm mới sắp diễn ra? (iPhone, laptop refresh)
8. [ ] DN có công bố kế hoạch xử lý HTK?

---

## Cross-link

- [`retail-industry-master-reference.md`](./retail-industry-master-reference.md) — Mental model 6 lớp ngành bán lẻ
- [`retail-sssg-reading.md`](./retail-sssg-reading.md) — Cách đọc SSSG phân biệt tăng trưởng thật/ảo
