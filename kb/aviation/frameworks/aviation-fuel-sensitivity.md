---
category: frameworks
title: "Aviation-Fuel-Sensitivity"
last_updated: 2026-05-12
---
Deep dive độ nhạy giá nhiên liệu ngành hàng không — biến số số 1 ảnh hưởng lợi nhuận hãng bay.

---

# 1. Tỷ trọng nhiên liệu trong chi phí

| Loại hãng | Tỷ trọng nhiên liệu / tổng chi phí |
|---|---|
| Hãng giá rẻ (VJC) | 25-30% |
| Hãng truyền thống (HVN) | 30-35% |
| Sân bay (ACV) | **0%** (không bay) |
| Nhà ga hàng hóa (SCS, NCT) | **0%** |

> **Quy tắc**: Nhiên liệu là chi phí lớn nhất có thể biến động nhanh của hãng bay. Sân bay/dịch vụ hoàn toàn miễn nhiễm.

---

# 2. Mối quan hệ giá dầu Brent và Jet A1

**Công thức gần đúng**:
```
Giá Jet A1 ($/thùng) ≈ Giá Brent × 1.1 đến 1.2
```

Chênh lệch (crack spread) do:
- Chi phí lọc dầu
- Vận chuyển đến sân bay
- Lưu kho

**Ví dụ**:
| Brent ($/thùng) | Jet A1 ($/thùng) | Jet A1 (VND/lít) |
|---|---|---|
| $60 | $66-72 | ~15.000 |
| $80 | $88-96 | ~20.000 |
| $100 | $110-120 | ~25.000 |
| $120 | $132-144 | ~30.000 |

---

# 3. Độ nhạy lợi nhuận theo giá dầu

## 3.1 VJC (ước tính)

| Giá Brent | Tác động chi phí | Biên lợi nhuận | Nhận định |
|---|---|---|---|
| $60 | Base | 8-10% | **LÃI TỐT** |
| $70 | +500-700 tỷ/năm | 6-8% | Vẫn lãi |
| $80 | +1.000-1.200 tỷ/năm | 4-6% | Biên mỏng |
| $90 | +1.500-1.800 tỷ/năm | 2-4% | Căng thẳng |
| $100 | +2.000-2.500 tỷ/năm | 0-2% | Gần hòa vốn |
| $120+ | +3.000+ tỷ/năm | Âm | **LỖ** |

## 3.2 HVN (ước tính)

HVN nhạy hơn VJC vì:
- Đội bay già hơn → tiêu hao nhiên liệu cao hơn
- Mô hình truyền thống → ít phụ trội bù đắp
- Nợ cao → chi phí tài chính đã ăn mòn biên

Khi Brent >$80, HVN gần như chắc chắn lỗ hoạt động nếu không có hỗ trợ.

---

# 4. Cơ chế hedging (phòng ngừa rủi ro nhiên liệu)

## 4.1 Các công cụ hedging

| Công cụ | Mô tả | Ưu | Nhược |
|---|---|---|---|
| Hợp đồng tương lai (Futures) | Mua quyền mua dầu giá cố định | Cố định chi phí | Mất lợi nếu dầu giảm |
| Quyền chọn (Options) | Quyền (không nghĩa vụ) mua giá cố định | Linh hoạt | Phí quyền chọn đắt |
| Swap | Trao đổi dòng tiền với đối tác | Đơn giản | Rủi ro đối tác |

## 4.2 Thực tế tại Việt Nam

- **VJC**: Đã từng hedge một phần (30-50% nhu cầu), nhưng không công bố chi tiết
- **HVN**: Ít hedge do hạn chế tài chính + quốc doanh có cơ chế hỗ trợ

> **Lưu ý**: Hedge giúp ổn định chi phí nhưng KHÔNG loại bỏ rủi ro. Nếu hedge ở giá cao rồi dầu giảm → bất lợi.

---

# 5. Tác động tỷ giá USD/VND

Nhiên liệu tính bằng USD → tỷ giá là yếu tố nhân đôi:

**Công thức**:
```
Chi phí nhiên liệu VND = Giá Jet A1 (USD) × Tỷ giá USD/VND × Lượng tiêu thụ
```

| Tỷ giá USD/VND | Tác động khi Brent = $80 |
|---|---|
| 24.000 | Base |
| 25.000 (+4%) | Chi phí nhiên liệu +4% |
| 26.000 (+8%) | Chi phí nhiên liệu +8% |

> **Quy tắc**: USD tăng 1% → chi phí nhiên liệu tăng ~1%. Kết hợp dầu tăng + USD tăng = "kép" rủi ro.

---

# 6. Ứng dụng khi phân tích

## 6.1 Checklist trước khi đánh giá hãng bay

1. **Giá Brent hiện tại?** <$70 = thuận lợi, $70-90 = trung tính, >$90 = bất lợi
2. **Xu hướng 3-6 tháng?** Tăng hay giảm?
3. **Tỷ giá USD/VND?** Ổn định hay tăng?
4. **Hãng có hedge không?** Tỷ lệ bao nhiêu %? Giá hedge bao nhiêu?

## 6.2 Tín hiệu vào/thoát theo dầu

| Tín hiệu | Hành động |
|---|---|
| Brent giảm về <$70 từ >$90 | **CƠ HỘI** — chi phí giảm mạnh, đòn bẩy khuếch đại |
| Brent tăng >$100 | **CẢNH BÁO** — cân nhắc giảm vị thế hãng bay |
| Brent tăng + USD tăng | **CẢNH BÁO KÉP** — ưu tiên ACV thay vì VJC/HVN |

## 6.3 So sánh độ nhạy VJC vs ACV

| Yếu tố | VJC | ACV |
|---|---|---|
| Dầu +$10/thùng | Chi phí +500-700 tỷ/năm | **Không ảnh hưởng** |
| USD +5% | Chi phí +3-4% | Doanh thu quốc tế +5% (có lợi) |
| Dịch bệnh | Doanh thu → 0 | Doanh thu → 0 |
| Cạnh tranh tăng | Giá vé giảm, biên nén | Không ảnh hưởng (độc quyền) |

---

# 7. Case study: Chu kỳ dầu 2022-2025

| Giai đoạn | Brent | Tác động |
|---|---|---|
| Q1-Q2/2022 | $100-120 (chiến tranh Ukraine) | VJC lỗ nặng, HVN lỗ kỷ lục |
| Q3-Q4/2022 | $80-95 | Vẫn căng thẳng |
| 2023 | $70-90 | Biên mỏng, phục hồi chậm |
| 2024 | $70-85 | Cải thiện dần |
| Q1/2025 | $75-80 | VJC lãi bùng nổ (kết hợp tỷ lệ lấp đầy cao) |

> **Bài học**: Dầu từ >$100 về <$80 + tỷ lệ lấp đầy hồi = điểm mua hãng bay. Ngược lại, dầu từ <$70 lên >$90 = điểm thoát.

---

## Cross-link

| File | Nội dung |
|---|---|
| [`aviation-industry-master-reference.md`](./aviation-industry-master-reference.md) | Framework tổng quan 6 lớp |
| [`aviation-operating-leverage.md`](./aviation-operating-leverage.md) | Đòn bẩy hoạt động, break-even |
