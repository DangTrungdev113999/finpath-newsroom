---
category: frameworks
title: "Oil-Gas-Industry-Master-Reference"
last_updated: 2026-05-12
---

Master reference cho Master Oil & Gas — mental model 6 lớp phân tích ngành dầu khí VN. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **GAS · PLX · PVD · PVS · BSR · OIL · DPM · DCM · PVT**. Knowledge base này gom 6 lớp vào một chỗ để orient nhanh.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap từ agents/Sector_Oil_Gas/knowledge.md + web search bổ sung dữ liệu 2025-2026. Format chuẩn hóa theo bank-industry-master-reference.md. |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Chuỗi giá trị dầu khí

```
THƯỢNG NGUỒN (Upstream) — Thăm dò & Khai thác
    → PVD (khoan), PVS (dịch vụ kỹ thuật), PVN (tập đoàn mẹ)

TRUNG NGUỒN (Midstream) — Vận chuyển & Lưu trữ
    → PVT (vận tải), GAS (phân phối khí)

HẠ NGUỒN (Downstream) — Chế biến & Phân phối
    → BSR (lọc dầu), PLX (Petrolimex), OIL (PVOil)

DỊCH VỤ PHỤ TRỢ
    → PVS, PVC (xây lắp), PVI (bảo hiểm)

PHÂN BÓN & HÓA CHẤT
    → DPM (Đạm Phú Mỹ), DCM (Đạm Cà Mau)
```

## 1.2 Phân loại doanh nghiệp (structural)

### Nhóm thượng nguồn (Upstream)

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| PVD | PV Drilling | 100% phụ thuộc giá dầu + sản lượng khai thác; sở hữu đội giàn khoan tự nâng (jack-up) lớn nhất VN; hưởng lợi trực tiếp từ CAPEX PVN |
| PVS | PTSC | Dịch vụ kỹ thuật dầu khí toàn diện; phụ thuộc CAPEX thăm dò PVN; backlog hợp đồng là chỉ số dẫn dắt |

### Nhóm trung nguồn (Midstream)

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| GAS | PV Gas | Độc quyền phân phối khí nội địa; hợp đồng dài hạn, lợi nhuận ổn định nhất ngành; hưởng lợi từ LNG nhập khẩu (Thị Vải, Hải Lăng) |
| PVT | PV Trans | Vận tải dầu khí; phụ thuộc giá cước + sản lượng khai thác |

### Nhóm hạ nguồn (Downstream)

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| BSR | Bình Sơn Refining | Lọc dầu Dung Quất — nhà máy lọc dầu lớn nhất VN; phụ thuộc crack spread; dự án nâng cấp-mở rộng vận hành từ 2028 |
| PLX | Petrolimex | Bán lẻ xăng dầu lớn nhất (~48% thị phần); biên mỏng ~300-500đ/lít; giá do Bộ Công Thương quyết định |
| OIL | PVOil | Bán lẻ xăng dầu (~20% thị phần); tương tự PLX nhưng quy mô nhỏ hơn |

### Nhóm phân bón & hóa chất

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| DPM | Đạm Phú Mỹ | Sản xuất urê; phụ thuộc giá khí đầu vào + giá urê thế giới; cổ tức cao |
| DCM | Đạm Cà Mau | Tương tự DPM; hệ thống phân phối mạnh miền Tây Nam Bộ |

> **Decision rule phân loại**: Thượng nguồn = biến động mạnh theo giá dầu, upside lớn khi dầu tăng. Trung nguồn = ổn định nhất, defensive. Hạ nguồn = ngược với thượng nguồn khi giá dầu biến động. Phân bón = chu kỳ riêng theo giá urê, không hoàn toàn theo giá dầu.

## 1.3 Ai quyết định luật chơi

| Yếu tố | Vai trò | Tác động |
|---|---|---|
| **Giá dầu Brent/WTI** | #1 quan trọng nhất | 70% câu chuyện ngành; dầu tăng → upstream lời, downstream có thể lỗ (nhập đắt) |
| **PVN** | Tập đoàn mẹ | Quyết định kế hoạch thăm dò, CAPEX, phân bổ sản lượng; PVS/PVD phụ thuộc trực tiếp |
| **Bộ Công Thương** | Quản lý giá bán lẻ | Quyết định giá xăng dầu mỗi 10-15 ngày; ảnh hưởng PLX/OIL |
| **OPEC+** | Cung dầu toàn cầu | Quyết định sản lượng dầu thế giới → ảnh hưởng giá |

## 1.4 Đặc thù thị trường Việt Nam

- VN sản xuất dầu nhưng **NHẬP KHẨU ròng xăng dầu thành phẩm** (~30% nhu cầu)
- Sản lượng khai thác giảm dần (~8-10 triệu tấn/năm, từ đỉnh 20 triệu tấn)
- Khí tự nhiên tăng vai trò (điện khí theo QHĐ8, phân bón)
- Dự án LNG nhập khẩu đang triển khai: Thị Vải (mở rộng 7 triệu m³/ngày từ 3/2025), Hải Lăng
- Trung hạn 5-10 năm dầu khí vẫn là trụ cột năng lượng quốc gia
- Dự án trọng điểm đang được đẩy nhanh: Lô B – Ô Môn, Lạc Đà Vàng, Cá Voi Xanh, Sư Tử Trắng giai đoạn 2B, Kèn Bầu

## 1.5 Mùa vụ ngành dầu khí

| Quý | Upstream (PVD, PVS) | Downstream (BSR, PLX) | Phân bón (DPM, DCM) |
|---|---|---|---|
| Q1 | Trung bình (sau Tết chậm) | Cao (nhu cầu Tết) | Thấp |
| Q2 | Cao (mùa khoan) | Trung bình | Cao (vụ Hè Thu) |
| Q3 | Cao | Trung bình | Cao |
| Q4 | Trung bình-Cao | Cao (cuối năm) | Thấp |

**Lưu ý:** Giá dầu biến động 20% có thể xóa hết ảnh hưởng mùa vụ.

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics quan trọng

### Tier 1 — Phản ứng ngay

| Metric | Ý nghĩa | Áp dụng | Benchmark |
|---|---|---|---|
| **Giá dầu Brent** | Toàn ngành | Tất cả | >70 USD: tốt upstream; <60 USD: xấu upstream |
| **Sản lượng khai thác** | Bán được bao nhiêu | PVD, GAS | So kế hoạch PVN |
| **Crack spread** | Chênh lệch dầu thô vs xăng/diesel | BSR | Cao → BSR lời |
| **Giá khí đầu vào** | Chi phí nguyên liệu | DPM, DCM | Khí rẻ → biên cao |
| **Giá urê thế giới** | Giá bán sản phẩm | DPM, DCM | Cao → lợi nhuận tăng |
| **Utilization rate** | % công suất vận hành | BSR | >90% tốt; <80% bảo trì/lỗ |

### Tier 2 — Phản ứng chậm

| Metric | Ý nghĩa | Áp dụng |
|---|---|---|
| **Backlog hợp đồng** | Giá trị hợp đồng đã ký chưa thực hiện | PVS, PVD |
| **CAPEX thăm dò PVN** | Đầu tư thăm dò | PVD, PVS |
| **Freight rate** | Giá cước vận tải | PVT |
| **GRM** | Lợi nhuận/thùng dầu lọc | BSR (>5 USD tốt; <3 USD yếu) |
| **Tỷ giá USD/VND** | Dầu giao dịch bằng USD | USD tăng → upstream hưởng, downstream thiệt |
| **Rig utilization** | % giàn khoan hoạt động | PVD |

### Tier 3 — Dài hạn

- Trữ lượng dầu/khí còn lại
- Tiến độ dự án LNG
- Kế hoạch CAPEX PVN 5 năm
- Chính sách năng lượng tái tạo (QHĐ8)
- Số lượng giàn JU Đông Nam Á (dự báo 37-38 giàn 2025-2026)

## 2.2 Đọc số theo phân khúc

### Upstream (PVD, PVS)

- **Quan trọng**: Giá dầu + Sản lượng + CAPEX PVN + Backlog
- **Check**: Giá Brent trung bình quý, số giàn khoan hoạt động, rig utilization, backlog so với năm trước, sản lượng vs kế hoạch
- **Benchmark 2025-2026**: PVD doanh thu 2025 đạt 10.500 tỷ đồng (+10% YoY), lợi nhuận trước thuế 1.100 tỷ đồng (+17% YoY)

### Lọc dầu (BSR)

- **Quan trọng**: Crack spread + Utilization rate + GRM
- **Check**: Crack spread Singapore, GRM (>5 USD/thùng tốt), công suất vận hành (target >90%), hàng tồn kho
- **Note**: Dự án nâng cấp-mở rộng Dung Quất vận hành 2028 → nâng tự chủ nhiên liệu lên ~70%

### Phân bón (DPM, DCM)

- **Quan trọng**: Giá urê thế giới + Giá khí đầu vào
- **Check**: Giá urê Yuzhnyy/Trung Đông, giá khí PVN, sản lượng nội địa + xuất khẩu, mùa vụ nông nghiệp (vụ Hè Thu Q2-Q3)
- **Ngưỡng**: Giá urê >400 USD/tấn thuận lợi; <300 USD/tấn khó khăn

### Bán lẻ (PLX, OIL)

- **Quan trọng**: Chênh lệch giá cơ sở + Tồn kho + Sản lượng tiêu thụ
- **Biên cố định** ~300-500 đồng/lít → lợi nhuận phụ thuộc SẢN LƯỢNG
- **Check**: Sản lượng tiêu thụ (tấn), lãi/lỗ tồn kho, quỹ bình ổn, thị phần (PLX ~48%, OIL ~20%)

### Khí (GAS)

- **Quan trọng**: Sản lượng khí + Giá khí bán ra + Tiến độ LNG
- **Đặc thù**: Hợp đồng dài hạn → lợi nhuận ổn định nhất ngành
- **Check**: Sản lượng khí so kế hoạch, tiến độ Thị Vải/Hải Lăng, giá khí đầu vào cho điện khí

## 2.3 Bẫy BCTC dầu khí

| Bẫy | Phải làm gì |
|---|---|
| **BSR lãi kỷ lục** | Check lãi tồn kho bao nhiêu? Bỏ ra, lợi nhuận core? |
| **DPM lợi nhuận tăng 100%** | Check giá urê có bền? Hay đỉnh chu kỳ? |
| **PVD backlog kỷ lục** | Check biên lợi nhuận trên backlog mới |
| **PLX doanh thu tăng 30%** | Check sản lượng (tấn), không chỉ doanh thu (tiền) |
| **GAS lợi nhuận ổn định** | Đừng kỳ vọng tăng trưởng cao — đây là defensive stock |
| **Giá dầu 80 USD = tốt tất cả** | SAI — tốt upstream, XẤU downstream |

## 2.4 Checklist đánh giá BCTC

1. Xác định phân khúc (Upstream/Lọc dầu/Phân bón/Bán lẻ/Khí/Dịch vụ)
2. Check giá đầu vào + đầu ra theo phân khúc
3. Sản lượng so kế hoạch + cùng kỳ
4. Lãi/lỗ tồn kho (đặc biệt BSR, PLX) — 1 lần, không bền
5. Backlog / Hợp đồng mới (PVS, PVD)
6. CAPEX PVN thay đổi?
7. Yếu tố vĩ mô: giá dầu, OPEC+, tỷ giá, nhu cầu toàn cầu

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Nguyên tắc cốt lõi

```
Dầu khí là ngành CHU KỲ — lên xuống theo giá dầu (quyết định 70%)

Cổ phiếu chạy TRƯỚC giá dầu:
- Tăng khi dầu bắt đầu hồi
- Giảm khi dầu bắt đầu giảm

Mỗi phân khúc phản ứng NGƯỢC NHAU:
- Dầu tăng → Upstream xanh, Downstream đỏ
- Dầu giảm → Upstream đỏ, Downstream xanh
```

## 3.2 Chu kỳ giá dầu theo phân khúc

**Giá dầu TĂNG:**

| Phân khúc | Tác động | Lý do |
|---|---|---|
| Upstream (PVD, PVS) | Xanh mạnh | Doanh thu + lợi nhuận tăng trực tiếp |
| GAS | Xanh | Giá khí bán tăng theo giá dầu |
| Lọc dầu (BSR) | Trung lập | Tùy crack spread |
| Bán lẻ (PLX, OIL) | Trung lập | Lãi tồn kho ngắn hạn, nhưng nhập đắt hơn |
| Phân bón (DPM, DCM) | Đỏ | Giá khí đầu vào tăng (trừ khi urê tăng nhanh hơn) |
| Vận tải (PVT) | Xanh | Cước tăng theo hoạt động |

**Giá dầu GIẢM:** Ngược lại hoàn toàn

## 3.3 Bốn giai đoạn chu kỳ (Upstream)

| Giai đoạn | Đặc điểm | Tín hiệu nhận diện | Giá cổ phiếu |
|---|---|---|---|
| **ĐÁY** | Dầu thấp (<50-60 USD), OPEC+ cắt, PVN cắt CAPEX, lợi nhuận giảm/lỗ | Rig count chạm đáy, insider mua | Bắt đầu tăng (mua vào) |
| **HỒI PHỤC** | Dầu hồi 60-80 USD, PVN tăng CAPEX, backlog tăng | OPEC+ kỷ luật, tồn kho giảm | TĂNG MẠNH NHẤT |
| **TĂNG TRƯỞNG** | Dầu cao 80-100+ USD, lợi nhuận tăng đều | Dự án mới được phê duyệt | Tăng chậm/đi ngang |
| **ĐỈNH → SUY GIẢM** | Dầu bắt đầu giảm, OPEC+ bất đồng | Shale oil Mỹ tăng, tồn kho tăng | Bắt đầu giảm dù BCTC còn tốt |

## 3.4 Tín hiệu sớm nhận diện chu kỳ

### Đáy hình thành (cần 2-3/6 tín hiệu)

- OPEC+ cắt giảm mạnh
- Giá dầu ổn định 2-3 tháng liên tiếp
- Rig count toàn cầu chạm đáy
- PVN tăng CAPEX
- Tồn kho dầu thế giới giảm
- Insider mua cổ phiếu

### Đỉnh hình thành (cần 2-3/6 tín hiệu)

- OPEC+ bất đồng, một số nước tăng sản lượng
- Tồn kho dầu tăng 3 tuần liên tiếp
- Nhu cầu toàn cầu chậm (Trung Quốc yếu)
- Giá >100 USD → shale oil Mỹ tăng sản xuất
- PVN review/hoãn dự án
- Insider bán cổ phiếu

## 3.5 Chu kỳ phân bón (DPM, DCM) — riêng biệt

Phân bón có chu kỳ RIÊNG, không hoàn toàn theo giá dầu:

**Giá urê TĂNG:**
- Khí châu Âu đắt
- Trung Quốc hạn chế xuất khẩu
- Nhu cầu nông nghiệp mạnh (La Nina)

**Giá urê GIẢM:**
- Châu Âu hạ giá khí
- Trung Quốc mở xuất khẩu
- Nhu cầu yếu (El Nino)

## 3.6 Case study: Chu kỳ 2024-2026

**2024-2025**: Upstream bùng nổ — PVD đạt doanh thu cao nhất 10 năm (10.500 tỷ đồng năm 2025), lợi nhuận trước thuế 1.100 tỷ (+17%). PVS backlog kỷ lục từ các dự án Lô B, Lạc Đà Vàng.

**2026**: Giá dầu dự báo về vùng 60-65 USD/thùng do dư cung OPEC+. Tuy nhiên, dòng tiền vào cổ phiếu dầu khí VN không hoàn toàn theo giá dầu mà chủ yếu phản ánh chu kỳ đầu tư trong nước đang được kích hoạt trở lại.

---

# LỚP 4: HIỂU VĨ MÔ

## 4.1 Yếu tố vĩ mô tác động ngành

| Yếu tố | Tác động |
|---|---|
| **Giá dầu Brent** | #1 — 70% câu chuyện ngành |
| **OPEC+** | Cắt/tăng sản lượng → ảnh hưởng trực tiếp giá dầu |
| **Nhu cầu toàn cầu** | Trung Quốc + Mỹ + EU = 60% nhu cầu |
| **Shale oil Mỹ** | >70 USD → tăng sản xuất → ép giá |
| **Tỷ giá USD/VND** | USD tăng → upstream xanh, downstream đỏ |
| **Giá khí (Henry Hub, TTF)** | GAS, DPM, DCM |
| **Địa chính trị** | Chiến tranh → gián đoạn cung → giá tăng đột biến |
| **CAPEX PVN** | PVD, PVS trực tiếp; là leading indicator cho ngành |

## 4.2 Ma trận ảnh hưởng vĩ mô

| Yếu tố | Upstream | BSR | PLX/OIL | DPM/DCM | GAS |
|---|---|---|---|---|---|
| Giá dầu tăng | Xanh | Trung lập | Trung lập | Đỏ | Xanh |
| Giá dầu giảm | Đỏ | Trung lập | Trung lập | Xanh | Đỏ |
| USD tăng | Xanh | Đỏ | Đỏ | Trung lập | Trung lập |
| OPEC+ cắt | Xanh | Đỏ | Đỏ | Trung lập | Trung lập |
| Trung Quốc yếu | Đỏ | Đỏ | Trung lập | Đỏ | Đỏ |
| PVN tăng CAPEX | Xanh mạnh | Trung lập | Trung lập | Trung lập | Trung lập |

## 4.3 Động lực & Rủi ro

### Động lực cấu trúc (dài hạn)

- LNG nhập khẩu phát triển (Thị Vải, Hải Lăng)
- Điện khí tăng theo QHĐ8
- Dự án mỏ mới: Cá Voi Xanh, Lô B – Ô Môn, Lạc Đà Vàng
- An ninh năng lượng quốc gia được ưu tiên

### Rủi ro cấu trúc (dài hạn)

- Năng lượng xanh cạnh tranh
- Mỏ cũ cạn kiệt, sản lượng giảm
- Shale oil Mỹ tạo trần giá 80-90 USD
- Phụ thuộc quyết định PVN

### Động lực chu kỳ (ngắn hạn)

- OPEC+ cắt giảm kỷ luật
- Trung Quốc mở cửa tăng nhu cầu
- PVN tăng CAPEX thăm dò
- La Nina tăng nhu cầu phân bón

### Rủi ro chu kỳ (ngắn hạn)

- OPEC+ bất đồng
- Suy thoái toàn cầu
- Crack spread thu hẹp
- Trung Quốc mở xuất khẩu urê
- Bảo trì nhà máy (BSR, DPM)

## 4.4 Câu hỏi agent phải trả lời

1. Giá dầu xu hướng? OPEC+ đang làm gì?
2. PVN thay đổi CAPEX?
3. Crack spread mở/thu hẹp? (BSR)
4. Giá urê xu hướng? Trung Quốc hạn chế xuất khẩu? (DPM/DCM)
5. Dự án mới sắp vận hành?
6. Bảo trì nhà máy trong quý?

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 P/E cho ngành chu kỳ — Bẫy lớn nhất

```
P/E PHẢN TRỰC GIÁC:
- Đáy: P/E CAO (E thấp/lỗ) → LÚC MUA
- Đỉnh: P/E THẤP (E cao nhất) → LÚC BÁN

❌ "PVD P/E 8x = rẻ" → Có thể đang đỉnh chu kỳ
✅ "PVD P/E 30x + dầu vừa chạm đáy" → Cơ hội vì E sắp hồi
```

## 5.2 Phương pháp định giá theo phân khúc

| Phân khúc | Phương pháp | Lý do |
|---|---|---|
| Upstream (PVD, PVS) | EV/EBITDA + Normalized P/E | Dùng E trung bình qua chu kỳ 5-7 năm |
| Lọc dầu (BSR) | EV/EBITDA + so GRM với peer | Biến động lớn theo crack spread |
| Bán lẻ (PLX, OIL) | P/E | Biên cố định, tương đối ổn |
| Phân bón (DPM, DCM) | Normalized P/E + Dividend yield | Cổ tức cao 50-80% lợi nhuận |
| Khí (GAS) | P/E + DCF | Hợp đồng dài hạn, dòng tiền ổn định |
| Dịch vụ (PVS) | EV/EBITDA + Backlog/Mcap | Backlog phản ánh doanh thu tương lai |

## 5.3 Normalized P/E

- Dùng E trung bình 5-7 năm (qua cả đỉnh lẫn đáy)
- Ví dụ: PVD E đỉnh 3.000 đồng, E đáy 200 đồng, E trung bình 1.500 đồng → Normalized P/E = 20x

## 5.4 Dividend Yield (phân bón)

- DPM, DCM trả cổ tức 50-80% lợi nhuận
- Yield >10%: hấp dẫn (check bền?). 6-10%: hợp lý. <5%: đắt
- Phải dùng cổ tức trung bình 3-5 năm, không dùng 1 năm

## 5.5 Backlog/Market Cap (dịch vụ)

- Backlog/Mcap >1.0x: hấp dẫn
- 0.5-1.0x: hợp lý
- <0.5x: đắt
- Check margin trên backlog mới

## 5.6 Vùng định giá chu kỳ (P/B)

| Pha thị trường | P/B điển hình | Hành động |
|---|---|---|
| Đáy chu kỳ | 0.6-0.9x | MUA (E sẽ phục hồi) |
| Hồi phục early-cycle | 0.9-1.3x | Giá tăng mạnh nhất |
| Bùng nổ mid-cycle | 1.3-1.8x | Ổn định |
| Đỉnh chu kỳ | 1.8-2.5x | CẨN THẬN (E sắp giảm) |

## 5.7 Bẫy định giá

| Bẫy | Thực tế |
|---|---|
| P/E thấp = rẻ | Có thể đang đỉnh chu kỳ, E sắp giảm |
| P/B <1 = rẻ | Có thể mỏ cạn kiệt, backlog giảm |
| Dividend yield cao = tốt | Có thể giá urê đỉnh, cổ tức không bền |

---

# LỚP 6: TƯ VẤN

## 6.1 Phân biệt loại rủi ro

| Tình huống | Loại | Phản ứng |
|---|---|---|
| Dầu giảm 10%/tháng | Biến động bình thường | Theo dõi |
| Dầu giảm 30%/3 tháng | Chu kỳ đảo chiều | Giảm upstream |
| BSR lỗ 1 quý (bảo trì) | Sự kiện | Bình thường |
| BSR lỗ 2 quý (crack spread âm) | Cấu trúc | Đánh giá lại |
| DPM lợi nhuận giảm Q4 (hết mùa vụ) | Mùa vụ | Bình thường |
| DPM lợi nhuận giảm 3 quý (urê giảm) | Chu kỳ | Xem urê có hồi? |

## 6.2 Tư vấn theo profile đầu tư

### Dài hạn (>1 năm)

- **Focus**: Dự án mới (LNG, mỏ khí), CAPEX PVN dài hạn
- **Ưu tiên**: GAS (ổn định), PVS (backlog mạnh)
- **Tránh**: PLX (biên mỏng), PVD (quá phụ thuộc giá dầu)
- **Cổ tức**: DPM, DCM nếu yield >8% trung bình 3 năm

### Trung hạn (3-12 tháng)

- **Focus**: Chu kỳ giá dầu, OPEC+, CAPEX PVN
- **Vào upstream**: Dầu chạm đáy + OPEC+ cắt + PVN tăng CAPEX
- **Thoát upstream**: Dầu phá đỉnh + OPEC+ bất đồng + shale oil tăng

### Ngắn hạn (<3 tháng)

- **Focus**: Giá dầu biến động, BCTC, bảo trì nhà máy
- **Catalyst**: OPEC+ họp, EIA inventory, BCTC quý
- **Lưu ý**: Biến động mạnh — không phù hợp nhà đầu tư sợ rủi ro

## 6.3 Tín hiệu VÀO/THOÁT (Upstream)

**VÀO (cần 2-3/6 tín hiệu):**
- Dầu chạm đáy + ổn định 2-3 tháng
- OPEC+ cắt mạnh
- Tồn kho giảm
- PVN tăng CAPEX
- Rig count đáy
- Insider mua

**THOÁT (cần 2-3/6 tín hiệu):**
- Dầu >100 USD kéo dài
- OPEC+ bất đồng
- Tồn kho tăng 3 tuần
- Nhu cầu chậm
- PVN hoãn dự án
- Insider bán

## 6.4 Ngôn ngữ cho nhà đầu tư retail

| Thuật ngữ | Dịch dễ hiểu |
|---|---|
| Crack spread cao | Chênh lệch dầu thô vs xăng lớn → lọc dầu lời nhiều |
| Upstream hưởng lợi | Công ty khai thác/dịch vụ được hưởng lợi |
| OPEC+ cắt giảm | Các nước xuất khẩu dầu lớn bán ít hơn → giá tăng |
| PVN tăng CAPEX | PVN tăng đầu tư thăm dò mỏ mới |
| Backlog cao | Đã ký nhiều hợp đồng, đảm bảo doanh thu tương lai |
| Lãi tồn kho | Mua dầu rẻ trước, bán xăng giá mới → lời chênh lệch (1 lần, không bền) |
| GRM 5 USD/thùng | Mỗi thùng dầu lọc ra xăng, lời khoảng 5 đô |
| Rig utilization | Tỷ lệ giàn khoan hoạt động — cao = ngành bận rộn |
| Jack-up rig | Giàn khoan tự nâng — loại phổ biến ở Đông Nam Á |

---

# PHỤ LỤC

## A. Ngưỡng Severity cho Earnings Card

- **green:** Lợi nhuận tăng từ hoạt động kinh doanh chính (không phải lãi tồn kho)
- **yellow:** Lợi nhuận tăng chủ yếu từ lãi tồn kho, giá dầu chưa rõ, bảo trì 1 quý
- **red:** Giá dầu/urê giảm mạnh, PVN cắt CAPEX, crack spread âm, lỗ tồn kho
- **blue:** Thông tin trung tính

## B. Câu đánh giá mẫu

**Upstream hưởng lợi:** "Giá dầu trung bình {X} USD/thùng, tăng {Y}% so cùng kỳ. PVN tăng đầu tư thăm dò, {ticker} ký thêm {Z} hợp đồng mới. Lợi nhuận tăng {W}% từ hoạt động kinh doanh chính."

**BSR lãi tồn kho:** "{ticker} lãi {X} tỷ, tăng {Y}% so cùng kỳ. Khoảng {Z} tỷ từ lãi tồn kho (1 lần, không bền). Bỏ ra, lợi nhuận thật chỉ tăng {W}%."

**DPM hưởng lợi:** "Giá phân bón thế giới tăng {X}% do Trung Quốc hạn chế xuất khẩu, chi phí khí gần không đổi. Lợi nhuận tăng {Y}%."

**PVD mất hợp đồng:** "Giá dầu giảm {X}% → PVN cắt đầu tư thăm dò. {ticker} mất {Y} hợp đồng, doanh thu giảm {Z}%."

**Đáy chu kỳ:** "Lợi nhuận giảm {X}% — quý giảm thứ {Y}. Tuy nhiên OPEC+ cắt mạnh, tồn kho giảm, giá dầu ngừng giảm 3 tháng. Lịch sử cho thấy cổ phiếu dầu khí thường hồi trước khi kết quả kinh doanh cải thiện."

## C. Quy tắc agent

1. PHẢI phân biệt upstream vs downstream — không đánh giá giống nhau
2. Giá dầu tăng: Tốt upstream, NGƯỢC LẠI downstream
3. Dùng Normalized P/E hoặc EV/EBITDA cho ngành chu kỳ
4. PHẢI tách lãi/lỗ tồn kho — khoản 1 lần, không bền
5. Bảo trì BSR/DPM = mất sản lượng 1-2 quý, bình thường
6. Đánh giá phân bón PHẢI check giá urê + giá khí đầu vào
7. PHẢI dịch thuật ngữ cho nhà đầu tư retail
8. Thiếu data → nói thiếu, KHÔNG bịa số

---

## Hướng dẫn tra dữ liệu thời gian thực (cho Master Oil & Gas)

KB master này chỉ cung cấp framework + threshold + range historical. Khi viết bài quarter cụ thể, Master phải:

1. **Query KB framework** (file này) — static guidance
2. **Finpath API** cho data realtime:
   - Ratios: P/E, P/B, ROE quarterly + yearly
   - Income statement + Balance sheet — BCTC quarter
   - Events, News — tin tức gần nhất
3. **Web_search** cho data Finpath API không có:
   - Giá dầu Brent/WTI realtime
   - OPEC+ meeting outcomes
   - Crack spread Singapore
   - Giá urê thế giới
   - Backlog cụ thể PVS/PVD
   - Tiến độ dự án LNG, Lô B, Lạc Đà Vàng

Pipeline log emit `data_trail` array: `{source, fetched, purpose, supports_argument}` per fact. KHÔNG bịa số.

---

## Cross-link (placeholder cho deep dive sau)

| Deep dive | Nội dung chính |
|---|---|
| `oil-gas-crack-spread.md` | Chi tiết crack spread Singapore, GRM benchmark, bẫy BSR (todo) |
| `oil-gas-opec-cycle.md` | OPEC+ history, dự báo giá dầu, tín hiệu đảo chiều (todo) |
| `oil-gas-urea-cycle.md` | Chu kỳ phân bón riêng, La Nina/El Nino, Trung Quốc xuất khẩu (todo) |

---

## Nguồn tham khảo

- [Danh sách cổ phiếu ngành dầu khí VN 2026](https://topi.vn/co-phieu-nganh-dau-khi.html)
- [Triển vọng cổ phiếu ngành dầu khí năm 2026](https://nhadautu.vn/trien-vong-co-phieu-nganh-dau-khi-nam-2026-d101354.html)
- [MBS Sector Report: Oil and Gas 2026](https://www.mbs.com.vn/files/uploads/2025/12/Sector_OG_202512111.pdf)
- [Tái khởi động chu kỳ dầu khí 2026](https://thuongtruong.com.vn/news/tai-khoi-dong-chu-ky-dau-khi-co-hoi-nao-mo-ra-trong-nam-2026-158742.html)
- [Vietnam Oil and Gas Market Report](https://www.mordorintelligence.com/industry-reports/vietnam-oil-and-gas-market)
