---
category: frameworks
title: "Textile CMT-FOB-ODM Deep Dive"
last_updated: 2026-05-12
---

Deep dive về 3 mô hình sản xuất ngành dệt may: CMT, FOB, ODM. File này giải thích chi tiết cơ chế, case study chuyển dịch, và cách đọc tín hiệu từ BCTC.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Textile/knowledge.md + analysis |

---

# 1. BA MÔ HÌNH SẢN XUẤT

## 1.1 CMT (Cut-Make-Trim)

**Cơ chế:**
- Khách hàng (Nike, H&M) gửi vải + phụ liệu + mẫu thiết kế
- Nhà máy VN chỉ cắt + may + hoàn thiện
- Nhà máy KHÔNG sở hữu nguyên liệu, KHÔNG quyết định thiết kế

**Biên gộp: 3-8%**

**Ưu điểm:**
- Vốn lưu động thấp (không mua NVL)
- Rủi ro tồn kho thấp
- Dễ scale (chỉ cần lao động + máy may)

**Nhược điểm:**
- Biên cực mỏng
- Dễ bị thay thế bởi nước rẻ hơn (Bangladesh $95/tháng vs VN $300)
- Không có giá trị gia tăng
- Bị ép giá bởi thương hiệu lớn

**DN VN đại diện:** GMC (Garmex Sài Gòn)

## 1.2 FOB (Free On Board)

**Cơ chế:**
- Khách hàng gửi mẫu thiết kế + spec
- Nhà máy VN TỰ MUA nguyên liệu (vải, phụ kiện) + may + giao hàng lên tàu
- Nhà máy chịu trách nhiệm sourcing + chất lượng NVL

**Biên gộp: 10-18%**

**Ưu điểm:**
- Biên cao hơn 2-3x so với CMT
- Kiểm soát chuỗi cung ứng
- Tạo quan hệ sâu hơn với khách (sourcing partner)

**Nhược điểm:**
- Vốn lưu động cao (mua NVL trước 1-2 tháng)
- Rủi ro giá NVL (bông, sợi, vải tăng → biên ép)
- Rủi ro tồn kho NVL nếu đơn bị hủy
- Cần team sourcing + QC mạnh

**DN VN đại diện:** TNG (đang chuyển), GIL, MSH (phần FOB)

## 1.3 ODM (Original Design Manufacturing)

**Cơ chế:**
- Khách hàng chỉ nói concept chung ("áo khoác outdoor mùa đông, giá FOB $30")
- Nhà máy VN TỰ THIẾT KẾ + tự mua NVL + may + giao hàng
- Nhà máy sở hữu IP thiết kế (nhưng khách có thể mua lại design)

**Biên gộp: 15-25%**

**Ưu điểm:**
- Biên cao nhất
- Giá trị gia tăng cao → khó bị thay thế
- Quan hệ đối tác chiến lược với brand
- Có khả năng làm brand riêng trong tương lai

**Nhược điểm:**
- Cần R&D + team design (chi phí cố định cao)
- Ít DN VN có năng lực
- Rủi ro design bị reject → tồn kho cao

**DN VN đại diện:** MSH (portion cao), TCM (portion)

---

# 2. SO SÁNH 3 MÔ HÌNH

| Tiêu chí | CMT | FOB | ODM |
|----------|-----|-----|-----|
| **Biên gộp** | 3-8% | 10-18% | 15-25% |
| **Vốn lưu động** | Thấp | Cao | Cao |
| **Rủi ro NVL** | Không | Cao | Cao |
| **Rủi ro thay thế** | Rất cao | Trung bình | Thấp |
| **Năng lực cần** | Lao động | Sourcing + QC | Design + Sourcing + QC |
| **Quan hệ với brand** | Gia công | Nhà cung cấp | Đối tác chiến lược |
| **Khả năng ép giá** | Bị ép | Trung bình | Có leverage |

---

# 3. CHUYỂN DỊCH CMT → FOB → ODM

## 3.1 Tại sao chuyển dịch là xu hướng bắt buộc?

1. **Lương VN tăng 8-10%/năm** → CMT không còn cạnh tranh với Bangladesh/Campuchia
2. **Brand muốn giảm số supplier** → ưu tiên DN FOB/ODM full-service
3. **ESG requirement** → cần kiểm soát chuỗi cung ứng (FOB/ODM)
4. **Margin pressure** → DN phải tăng biên để survive

## 3.2 Case study: TNG chuyển CMT → FOB

**Bối cảnh:**
- TNG (Thái Nguyên) lịch sử là CMT thuần
- Chi phí lao động thấp (vùng núi phía Bắc)
- Biên gộp ~8-10%

**Quá trình chuyển dịch (2020-2025):**
- Đầu tư team sourcing vải
- Hợp tác với supplier vải trong nước + Trung Quốc
- Tăng dần tỷ trọng FOB: 20% (2020) → 35% (2022) → 50%+ (2025 target)

**Kết quả:**
- Biên gộp cải thiện từ ~8% → 12-14%
- Vốn lưu động tăng (receivables + inventory)
- ROE cải thiện do biên cao hơn

**Rủi ro đang diễn ra:**
- Vốn lưu động tăng nhanh hơn DT
- Nếu đơn hàng giảm đột ngột → tồn kho NVL tăng

## 3.3 Case study: MSH — ODM leader

**Bối cảnh:**
- MSH (May Sông Hồng) focus outdoor apparel (jacket, áo khoác)
- Khách hàng: Columbia, North Face, Decathlon — segment cao cấp
- Biên gộp cao nhất ngành: 18-22%

**Chiến lược ODM:**
- Đầu tư R&D center + design team
- Propose design cho brand trước mỗi season
- Tự nghiên cứu vật liệu chống nước, giữ ấm

**Kết quả:**
- Trở thành strategic partner của Columbia/NF
- Giá bán FOB cao hơn 30-50% so với may thông thường
- Ít bị cạnh tranh (ODM outdoor cần expertise)

**Rủi ro:**
- Tập trung thị trường Mỹ → Trump tariff ảnh hưởng trực tiếp
- Nếu Columbia/NF chuyển đơn → khó thay thế ngay

---

# 4. CÁCH ĐỌC TÍN HIỆU TỪ BCTC

## 4.1 Đọc tỷ trọng FOB/ODM

**Nguồn:**
- Báo cáo thường niên → mục "Cơ cấu doanh thu theo phương thức"
- Thuyết minh BCTC → breakdown theo loại hợp đồng
- ĐHĐCĐ slides → management commentary

**Tín hiệu tích cực:**
- Tỷ trọng FOB/ODM tăng YoY
- Management guide tiếp tục chuyển dịch
- Đầu tư sourcing/design được đề cập

**Tín hiệu tiêu cực:**
- Tỷ trọng FOB/ODM giảm (quay lại CMT)
- Management nói "thị trường khó khăn, tập trung CMT"

## 4.2 Đọc biên gộp theo mô hình

| Biên gộp | Interpretation |
|----------|----------------|
| <8% | CMT thuần hoặc FOB bị ép giá |
| 8-12% | Mix CMT + FOB hoặc FOB low-end |
| 12-18% | FOB cao hoặc ODM thấp |
| >18% | ODM cao hoặc niche premium |

**Case MSH:**
- Biên gộp >18% ổn định = ODM dominance confirmed
- Biên gộp giảm về 15% = có thể đang bị ép giá hoặc chuyển FOB

## 4.3 Đọc vốn lưu động

**Tỷ lệ Inventory/DT:**
- CMT: ~5-10% (ít tồn kho, không mua NVL)
- FOB: ~15-25% (mua NVL trước)
- ODM: ~20-30% (mua NVL + bán thành phẩm design)

**Tín hiệu cảnh báo:**
- Inventory tăng nhanh hơn DT + biên giảm = đơn hàng yếu, NVL tồn
- Receivables tăng mạnh = khách chậm trả hoặc đơn hàng lớn cuối quý

## 4.4 Đọc cash flow

**Chuyển dịch FOB/ODM ảnh hưởng:**
- CFO giảm tạm thời (vốn lưu động tăng)
- CFI tăng (đầu tư sourcing, R&D)
- Nếu CFO âm nhiều quý liên tiếp + biên không cải thiện = chuyển dịch thất bại

---

# 5. DECISION RULES CHO MASTER

1. **Khi viết về TNG:** Check tỷ trọng FOB % → biên có cải thiện không? Vốn lưu động có kiểm soát được không?

2. **Khi viết về MSH:** Check biên gộp >18% duy trì không? Khách hàng có diversify hay vẫn tập trung Columbia/NF?

3. **Khi viết về GMC:** Check có tín hiệu chuyển FOB không? Nếu không → structural discount

4. **Khi so sánh DN:** KHÔNG so sánh biên GMC (CMT) với MSH (ODM) — khác mô hình

5. **Khi nhìn cycle:** FOB/ODM hưởng lợi nhiều hơn khi orderbook đầy (biên cao). CMT hưởng lợi khi lương VN chưa tăng nhanh.

---

## Cross-link

| File | Nội dung chính |
|---|---|
| [`textile-industry-master-reference.md`](./textile-industry-master-reference.md) | Mental model 6 lớp ngành dệt may |
| [`textile-fta-rules-of-origin.md`](./textile-fta-rules-of-origin.md) | Quy tắc xuất xứ FTA + DN nào hưởng lợi |
