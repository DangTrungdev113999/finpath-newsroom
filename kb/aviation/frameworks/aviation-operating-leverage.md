---
category: frameworks
title: "Aviation-Operating-Leverage"
last_updated: 2026-05-12
---
Deep dive đòn bẩy hoạt động ngành hàng không — tại sao chênh lệch 15 điểm phần trăm tỷ lệ lấp đầy có thể là chênh lãi/lỗ.

---

# 1. Cấu trúc chi phí hãng bay

## 1.1 Chi phí cố định (65-75% tổng chi phí)

Chi phí không đổi theo số hành khách:
- **Thuê máy bay**: Hợp đồng dài hạn USD, cố định theo tháng/năm
- **Khấu hao máy bay sở hữu**: Không đổi
- **Lương phi công, tiếp viên, nhân viên**: Gần như cố định
- **Phí sân bay (phần cố định)**: Slot, hạ cánh
- **Bảo trì định kỳ**: Lịch trình cố định

## 1.2 Chi phí biến đổi (25-35% tổng chi phí)

Chi phí tăng theo số hành khách/chuyến bay:
- **Nhiên liệu**: 25-35% tổng chi phí, biến động theo giá dầu VÀ số chuyến
- **Suất ăn, nước uống**: Theo số khách
- **Hoa hồng đại lý**: Theo doanh thu
- **Phí sân bay biến đổi**: Phí phục vụ hành khách

---

# 2. Công thức đòn bẩy hoạt động

```
DOL = % Thay đổi lợi nhuận hoạt động / % Thay đổi doanh thu
```

**Đặc thù hãng bay**:
- Chi phí cố định cao → DOL cao → Lợi nhuận khuếch đại theo cả 2 chiều
- Tỷ lệ lấp đầy tăng 10 điểm phần trăm → Lợi nhuận có thể tăng 50-80%
- Tỷ lệ lấp đầy giảm 10 điểm phần trăm → Lợi nhuận có thể giảm 50-80% hoặc chuyển lỗ

---

# 3. Minh họa bằng số: Chuyến bay Hà Nội - TP.HCM

**Giả định**:
- Máy bay 180 ghế
- Chi phí cố định: 300 triệu đồng/chuyến
- Chi phí biến đổi: 100.000đ/khách
- Giá vé trung bình: 1.5 triệu đồng
- Phụ trội trung bình: 200.000đ/khách (hành lý, suất ăn, chọn ghế)

| Tỷ lệ lấp đầy | Số khách | Doanh thu | Chi phí | Lợi nhuận |
|---|---|---|---|---|
| 60% | 108 | 184 triệu | 311 triệu | **-127 triệu** |
| 70% | 126 | 214 triệu | 313 triệu | **-99 triệu** |
| 75% | 135 | 229 triệu | 314 triệu | **-85 triệu** |
| 80% | 144 | 245 triệu | 314 triệu | **-69 triệu** |
| 85% | 153 | 260 triệu | 315 triệu | **-55 triệu** |
| 90% | 162 | 275 triệu | 316 triệu | **-41 triệu** |

> **Lưu ý**: Ví dụ đơn giản hóa. Thực tế hãng bay có thêm doanh thu từ hàng hóa, bán vé giá cao (thương gia), và phụ trội cao hơn.

---

# 4. Điểm hòa vốn tỷ lệ lấp đầy

## 4.1 VJC vs HVN

| Chỉ tiêu | VJC | HVN |
|---|---|---|
| Mô hình | Giá rẻ + bán thêm | Truyền thống |
| Chi phí trên ghế-km | Thấp hơn 20-30% | Cao hơn |
| Phụ trội / doanh thu | 25-30% | 10-15% |
| Tuổi đội bay trung bình | 4-5 tuổi | 6-8 tuổi |
| **Tỷ lệ lấp đầy hòa vốn** | **~75%** | **~78-80%** |

## 4.2 Tại sao VJC hòa vốn thấp hơn

1. **Chi phí trên ghế-km thấp hơn**: Đội bay trẻ → bảo trì ít hơn, tiết kiệm nhiên liệu tốt hơn
2. **Phụ trội cao**: 25-30% doanh thu từ hành lý, suất ăn, chọn ghế → biên lợi nhuận cao vì chi phí phục vụ thấp
3. **Mô hình tinh gọn**: Ít dịch vụ miễn phí → ít chi phí cố định trên mỗi hành khách
4. **Một loại máy bay**: Chủ yếu Airbus A320/A321 → đào tạo phi công đơn giản, phụ tùng chuẩn hóa

---

# 5. Ứng dụng khi phân tích

## 5.1 Câu hỏi cần đặt

1. **Tỷ lệ lấp đầy hiện tại so với hòa vốn?** Gap bao nhiêu điểm phần trăm?
2. **Xu hướng ASK vs RPK?** ASK tăng nhanh hơn RPK = cung thừa = tỷ lệ lấp đầy sẽ giảm
3. **Giá nhiên liệu trending?** Nhiên liệu tăng → điểm hòa vốn tăng lên
4. **Phụ trội/khách trending?** Phụ trội tăng → đòn bẩy thuận lợi hơn

## 5.2 Tín hiệu cảnh báo

| Tín hiệu | Ý nghĩa |
|---|---|
| Tỷ lệ lấp đầy giảm về <80% | Gần điểm hòa vốn |
| ASK tăng >15% nhưng RPK tăng <10% | Cung thừa, tỷ lệ lấp đầy sẽ nén |
| Doanh thu trên ghế-km giảm khi tỷ lệ lấp đầy tăng | Giảm giá vé để lấp đầy — LỢI NHUẬN KHÔNG TỐT NHƯ TỶ LỆ LẤP ĐẦY GỢI Ý |
| Phụ trội/khách giảm | Cạnh tranh ép giảm phí hành lý/suất ăn |

## 5.3 Cơ hội từ đòn bẩy

| Tình huống | Cơ hội |
|---|---|
| Tỷ lệ lấp đầy đang 75% + dầu giảm + visa nới | Tỷ lệ lấp đầy sẽ bật lên + đòn bẩy khuếch đại lợi nhuận |
| Q3 (mùa hè) đang đến | Mùa cao điểm → tỷ lệ lấp đầy cao nhất năm |
| Hãng cạnh tranh thu hẹp (Bamboo/Pacific gặp khó) | Cung giảm → tỷ lệ lấp đầy + doanh thu trên ghế-km tăng |

---

# 6. Case study: VJC Q1/2025 vs Q1/2024

**Giả định số liệu** (cần verify từ BCTC/tin tức):

| Chỉ tiêu | Q1/2024 | Q1/2025 | Thay đổi |
|---|---|---|---|
| ASK (tỷ ghế-km) | 8.5 | 9.2 | +8.2% |
| RPK (tỷ HK-km) | 7.3 | 8.1 | +11.0% |
| Tỷ lệ lấp đầy | 85.9% | 88.0% | +2.1 điểm % |
| Doanh thu | 15.000 tỷ | 18.160 tỷ | +21% |
| Lợi nhuận sau thuế | 75 tỷ | 571 tỷ | +661% |

**Phân tích đòn bẩy**:
- Doanh thu tăng 21%
- Lợi nhuận tăng 661%
- DOL = 661% / 21% = **31.5x**

> **Bài học**: Chỉ cần tỷ lệ lấp đầy tăng 2 điểm phần trăm + doanh thu trên ghế-km ổn → lợi nhuận bùng nổ nhờ đòn bẩy hoạt động.

---

## Cross-link

| File | Nội dung |
|---|---|
| [`aviation-industry-master-reference.md`](./aviation-industry-master-reference.md) | Framework tổng quan 6 lớp |
| [`aviation-fuel-sensitivity.md`](./aviation-fuel-sensitivity.md) | Độ nhạy giá nhiên liệu |
