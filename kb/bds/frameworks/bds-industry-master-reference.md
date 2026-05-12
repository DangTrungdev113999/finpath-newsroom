---
category: frameworks
title: "BDS-Industry-Master-Reference"
last_updated: 2026-05-12
notion_page_id: "35d273c7-a9a1-81ca-84b4-eb18795d8a70"
source_url: "https://notion.so/35d273c7a9a181ca84b4eb18795d8a70"
applies_to: ["all"]
---

# Ngành bất động sản Việt Nam — Tham chiếu ngành (6 lớp mental model)

File này là neo nhận thức cho Master bất động sản: đọc trước khi phân tích bất kỳ mã nào thuộc ngành bất động sản Việt Nam. Sáu lớp mental model dưới đây tổ chức cách đọc ngành — từ cấu trúc doanh thu sáu loại bất động sản, đến chu kỳ vĩ mô, đòn bẩy, pháp lý, và định vị từng nhóm mã — nhằm tránh phán đoán từ bề ngoài và phát hiện đặc thù từng phân khúc.

Ngành bất động sản Việt Nam có sáu loại chính, mỗi loại có cơ chế doanh thu và rủi ro khác hẳn nhau: phát triển dân cư, khu công nghiệp, bán lẻ trung tâm thương mại, văn phòng cho thuê, nghỉ dưỡng, và trung tâm dữ liệu. Master không áp dụng một khung phân tích cho tất cả — phải nhận diện loại bất động sản từ mã rồi mới áp dụng khung tương ứng.

---

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | Merge từ knowledge.md Agent BĐS: thêm mùa vụ (1.3), bẫy đọc doanh thu (2.4), link cycle-indicators.md |
| 2026-05-11 | Khởi tạo — tổng hợp từ 20 framework Notion + bootstrap từ Bank/CK mẫu hình |

---

## LỚP 1 — Hiểu ngành: cấu trúc doanh thu sáu loại bất động sản

### 1.1 Sáu loại bất động sản và mô hình doanh thu

| Loại | Mô hình doanh thu | Đặc trưng |
|---|---|---|
| Phát triển dân cư | Ghi nhận một lần khi bàn giao (POS — ghi nhận khi bàn giao) | Mẫu hình doanh thu rất lồi theo quý — đỉnh-đáy chênh 3-5 lần |
| Khu công nghiệp | Ghi nhận một lần khi ký hợp đồng (Kinh Bắc, IDICO) hoặc dàn trải | Ghi nhận một lần lớn khi ký hợp đồng FDI; dòng tiền thu tiền trước nhanh mạnh |
| Bán lẻ trung tâm thương mại | Định kỳ hàng tháng (cố định + phần trăm doanh số) | Doanh thu định kỳ ổn định, biên gộp 60-70% |
| Văn phòng cho thuê | Định kỳ hàng tháng | Ổn định nhưng nhạy cảm làm việc kết hợp |
| Nghỉ dưỡng | Lai — bán biệt thự (một lần) + vận hành (định kỳ) | Phụ thuộc 100% du lịch + chính sách thị thực |
| Trung tâm dữ liệu | Định kỳ (thuê rack + điện) | Mới nổi 2024, định giá cao nhất trong ngành |

### 1.2 Hai chuẩn ghi nhận doanh thu theo VAS

Chuẩn kế toán Việt Nam (chuẩn mực số 14 và 15) quy định hai phương pháp ghi nhận doanh thu bất động sản:

- **Ghi nhận khi bàn giao**: phát triển dân cư áp dụng (Vinhomes, Novaland, Khang Điền, Đất Xanh, Nam Long)
- **Ghi nhận theo tiến độ**: một số dự án hạ tầng + cho thuê dài hạn áp dụng (Vincom Retail, Kinh Bắc một số hợp đồng)

Chi tiết: xem `bds-revenue-recognition-vas.md`.

### 1.3 Mùa vụ ngành — Q4 cao nhất

| Q1 | Q2-Q3 | Q4 |
|---|---|---|
| Thấp (sau Tết) | Trung bình | **Cao nhất** (đẩy bàn giao + doanh số) |

**Quy tắc quan trọng**: KHÔNG đánh giá doanh nghiệp từ 1 quý — phải nhìn cả năm. Doanh thu Q1 thấp là bình thường do mùa vụ, không phải tín hiệu yếu.

### 1.4 Mô hình lai — không phải mã nào cũng thuần một loại

Nhiều mã có 2-4 mảng kinh doanh song song. Vingroup là lai ba mảng (Vinhomes + Vincom Retail + Vinpearl + Vincom Office). Becamex là lai khu công nghiệp + dân cư. Đầu tư Phát triển Xây dựng là lai dân cư + nghỉ dưỡng. CEO Group là lai dân cư + nghỉ dưỡng. Khi viết bài về mã lai, phải phân rã theo phân khúc rồi mới đánh giá tổng thể.

Chi tiết: xem `bds-hybrid-business-models.md`.

---

## LỚP 2 — Đọc số: các chỉ số then chốt theo loại

### 2.1 Phát triển dân cư

Bốn chỉ số cốt lõi:

- **Doanh số bán trước hàng quý** — chỉ báo sớm doanh thu 12-18 tháng tới
- **Doanh số chờ ghi nhận trên doanh thu năm** — tầm nhìn doanh thu (1-2 lần bình thường, trên 4 lần tốt như Vinhomes)
- **Tỷ lệ chuyển đổi doanh số chờ ghi nhận thành doanh thu trong 24 tháng** — chỉ báo chất lượng (trên 90% như Vinhomes; 12% như Novaland do pháp lý tắc)
- **Tỷ lệ pháp lý sạch trong quỹ đất** — Vinhomes trên 70%, Novaland dưới 40% trước 2024

Chi tiết: xem `bds-res-presales-backlog.md`, `bds-res-land-bank-nav.md`, `bds-res-project-lifecycle.md`.

### 2.2 Khu công nghiệp

Bốn chỉ số cốt lõi:

- **Diện tích cho thuê được trong năm (héc-ta)** × **Giá thuê bình quân** = doanh thu năm
- **Diện tích thương phẩm còn lại** — khác tổng quỹ đất (Becamex 4.743 héc-ta tổng nhưng chỉ 848 héc-ta thương phẩm)
- **Tỷ lệ lấp đầy theo vùng** (miền Nam quý 3 năm 2024 đạt 82%)
- **Vốn đầu tư trực tiếp nước ngoài đăng ký so với giải ngân** — tỷ lệ giải ngân 50-70% là bình thường

Chi tiết: xem `bds-kcn-fdi-demand-mechanism.md`, `bds-kcn-inventory-pricing.md`, `bds-kcn-lease-structure.md`.

### 2.3 Bán lẻ, văn phòng, nghỉ dưỡng, trung tâm dữ liệu

Mỗi loại có chỉ số riêng — xem file framework tương ứng. Chỉ số chung: tỷ lệ lấp đầy, tiền cho thuê bình quân, tỷ lệ gia hạn, biên lợi nhuận gộp.

### 2.4 Cách đọc doanh thu bất động sản — tránh bẫy phổ biến

```
❌ "NVL doanh thu Q4 +200% → hồi phục mạnh"
✅ "NVL bàn giao 1 dự án lớn Q4 → doanh thu 1 quý, quý sau có thể gần 0"

Flow: Presales → Deferred revenue ↑ → Bàn giao 2-3 năm sau → Doanh thu ghi nhận
```

| Bẫy | Thực tế |
|---|---|
| "Doanh thu tăng 200%" | Bàn giao 1 dự án, quý sau có thể 0 |
| "Lợi nhuận tăng vọt" | Chuyển nhượng dự án (1 lần) |
| "Quỹ đất 10.000 héc-ta" | Chưa pháp lý = chưa phát triển được |
| "Doanh số bán trước kỷ lục" | 1 dự án hot, không phải tất cả |

### 2.5 Hai chỉ số đòn bẩy chung cho ngành

- **Tỷ lệ tổng nợ trên vốn chủ sở hữu**: dưới 1,5 lần khoẻ; trên 2,5 lần cảnh báo; trên 3,0 lần nguy hiểm (Novaland 2022)
- **Tỷ lệ nợ ròng trên lợi nhuận trước lãi vay, thuế và khấu hao (EBITDA)**: dưới 3 lần khoẻ; trên 7 lần căng

Chi tiết: xem `bds-debt-leverage.md`.

---

## LỚP 3 — Chu kỳ vĩ mô: lãi suất, tín dụng, vốn đầu tư trực tiếp nước ngoài

→ Chi tiết: `bds-macro-cycle-credit.md`

### 3.1 Bốn biến vĩ mô chính

1. **Lãi suất huy động và cho vay** — Ngân hàng Nhà nước điều hành. Ảnh hưởng nhu cầu nhà đầu tư cá nhân + chi phí vốn doanh nghiệp.
2. **Tín dụng bất động sản** — tỷ lệ dư nợ bất động sản trên tổng dư nợ ngân hàng. Ngân hàng Nhà nước kiểm soát.
3. **Tổng sản phẩm quốc nội và thu nhập** — nhu cầu phát triển dân cư tương quan dương.
4. **Tỷ giá đô la Mỹ trên đồng Việt Nam và vốn đầu tư trực tiếp nước ngoài** — chỉ ảnh hưởng khu công nghiệp trực tiếp.

### 3.2 Bốn pha chu kỳ bất động sản Việt Nam (7-10 năm)

| Pha | Đặc trưng |
|---|---|
| Đáy | Sau khủng hoảng, dư nợ thấp, cổ phiếu dưới giá trị tài sản ròng |
| Phục hồi | Lãi suất giảm, doanh số bán hồi phục, định giá lại |
| Mở rộng | Đòn bẩy tăng, bùng nổ doanh số, định giá cao |
| Đỉnh và sụp | Khủng hoảng trái phiếu hoặc siết tín dụng kích hoạt |

### 3.3 Độ trễ truyền dẫn lãi suất

- Ngân hàng Nhà nước hạ lãi suất → cổ phiếu bất động sản tăng: 2-4 tháng (chạy trước)
- Ngân hàng Nhà nước hạ lãi suất → doanh thu bất động sản tăng: 6-12 tháng
- Vốn đầu tư trực tiếp nước ngoài đăng ký → khu công nghiệp ghi nhận doanh thu: 6-18 tháng

---

## LỚP 4 — Đòn bẩy: trái phiếu doanh nghiệp và rủi ro vỡ nợ

→ Chi tiết: `bds-debt-leverage.md`

### 4.1 Bốn cơ chế làm bất động sản dễ vỡ nợ

1. Lệch kỳ hạn — tài sản 5-7 năm, nợ 2-3 năm
2. Dòng tiền lệch báo cáo kết quả — doanh thu ghi nhận khi bàn giao (3-5 năm sau bán)
3. Tài sản đảm bảo là cổ phiếu chính doanh nghiệp — vòng xoáy giảm giá
4. Tập trung ngân hàng cấp tín dụng — đóng băng tiền mặt khi tín nhiệm xấu

### 4.2 Khủng hoảng trái phiếu 2022-2026 (Novaland)

Vụ Vạn Thịnh Phát tháng 10/2022 → Nghị định 65/2022 siết trái phiếu → đóng băng thị trường 12-18 tháng. Novaland chịu cộng hưởng cả bốn cơ chế. Tổng dư nợ cuối 2022: 62.757 tỷ. Nghị định 08/2023 cho phép gia hạn 24 tháng. Mục tiêu tái cơ cấu hoàn thành cuối 2026 — kéo dài 4-5 năm.

---

## LỚP 5 — Pháp lý: Luật Đất đai 2024 và quy trình dự án

→ Chi tiết: `bds-legal-framework.md`

### 5.1 Ba luật nền tảng (hiệu lực 1/8/2024)

| Luật | Điểm mới |
|---|---|
| Luật Đất đai 31/2024/QH15 | Bỏ khung giá đất 5 năm; đấu giá bắt buộc dự án lớn; cấm phân lô bán nền đô thị loại III trở lên |
| Luật Nhà ở 27/2023/QH15 | Quy định bán nhà ở hình thành trong tương lai; ưu đãi nhà ở xã hội |
| Luật Kinh doanh Bất động sản 29/2023/QH15 | Môi giới qua sàn; doanh nghiệp FDI nhận chuyển nhượng dự án |

### 5.2 Năm bước pháp lý một dự án dân cư

1. Chấp thuận chủ trương đầu tư — 6-18 tháng
2. Giao đất hoặc cho thuê đất — 3-6 tháng
3. Quy hoạch chi tiết tỷ lệ một phần năm trăm — 6-12 tháng
4. Giấy phép xây dựng — 2-3 tháng
5. Giấy phép bán hàng — phụ thuộc thoả mãn đủ điều kiện

Tổng thời gian: 24-48 tháng. Sau Luật 2024 kỳ vọng giảm xuống 18-30 tháng.

---

## LỚP 6 — Định vị từng nhóm mã (routing theo loại)

Master nhận diện loại bất động sản từ mã rồi áp dụng khung tương ứng. Routing table cover các mã chính trong universe Việt Nam.

### 6.1 Phát triển dân cư (residential)

| Mã | Đặc thù | Framework cần đọc |
|---|---|---|
| Vinhomes (VHM) | Lớn nhất Việt Nam, quỹ đất 16.000 héc-ta, pháp lý sạch trên 70% | `bds-res-presales-backlog.md`, `bds-res-land-bank-nav.md`, `bds-res-project-lifecycle.md` |
| Novaland (NVL) | Quỹ đất 10.000 héc-ta nhưng pháp lý tắc — Aqua City | `bds-res-*` + `bds-debt-leverage.md` |
| Khang Điền (KDH) | Tập trung Thành phố Hồ Chí Minh, quỹ đất 700-1.000 héc-ta | `bds-res-*` |
| Đất Xanh (DXG) | Quỹ đất 3.000-4.000 héc-ta, lai môi giới qua DXS | `bds-res-*` + `bds-hybrid-business-models.md` |
| Nam Long (NLG) | Quỹ đất nhỏ, tập trung Thành phố Hồ Chí Minh trung lưu | `bds-res-*` |
| An Gia (AGG), Phát Đạt (PDR), Hà Đô (HDG), Đất Xanh Services (DXS) | Các mã phát triển dân cư khác | `bds-res-*` |
| Hoàng Quân (HQC) | Phân khúc trung bình thấp, tập trung phía Nam | `bds-res-*` |
| Hoàng Huy (TCH) | Đa mảng phân khúc Hải Phòng — dân cư + dịch vụ | `bds-res-*` + `bds-hybrid-business-models.md` |
| Văn Phú Invest (VPI) | Trung cấp Hà Nội + Hồ Chí Minh, quỹ đất 200-300 héc-ta | `bds-res-*` |
| Hodeco (HDC) | Trung cấp Bà Rịa-Vũng Tàu | `bds-res-*` |
| Cenland (CRE) | Môi giới bất động sản lớn — không phải developer, ghi nhận phí giao dịch | `bds-hybrid-business-models.md` |

### 6.2 Khu công nghiệp (kcn)

| Mã | Đặc thù | Framework cần đọc |
|---|---|---|
| Kinh Bắc (KBC) | Quỹ đất 3.861 héc-ta, SGI-HCM Campus AI 2 tỷ đô la Mỹ | `bds-kcn-*` + `bds-dc-hyperscaler-power.md` |
| IDICO (IDC) | Quỹ đất 3.217 héc-ta, 1.428 héc-ta sẵn sàng | `bds-kcn-*` |
| Becamex (BCM) | Quỹ đất 4.700 héc-ta, lai khu công nghiệp + dân cư | `bds-kcn-*` + `bds-hybrid-business-models.md` |
| Saigon VRG Investment (SIP) | Khu công nghiệp ven Thành phố Hồ Chí Minh | `bds-kcn-*` |
| Sonadezi Châu Đức (SZC) | Khu công nghiệp Bà Rịa-Vũng Tàu | `bds-kcn-*` |
| Viglacera (VGC) | Khu công nghiệp + vật liệu xây dựng | `bds-kcn-*` |
| Long Hậu (LHG) | Khu công nghiệp Long An | `bds-kcn-*` |
| Itaco (ITA) | Khu công nghiệp Long An và Tân Tạo | `bds-kcn-*` |

### 6.3 Bán lẻ (retail)

| Mã | Đặc thù | Framework cần đọc |
|---|---|---|
| Vincom Retail (VRE) | Thuần phân khúc bán lẻ duy nhất niêm yết, 80+ trung tâm thương mại | `bds-retail-*` |
| Vingroup (VIC) | Vincom Retail là một mảng | `bds-retail-*` + `bds-hybrid-business-models.md` |

### 6.4 Văn phòng (office)

| Mã | Đặc thù | Framework cần đọc |
|---|---|---|
| Cơ Điện Lạnh (REE) | Etown 1-5 chiếm 30-40% doanh thu, mã đa mảng | `bds-office-*` + `bds-hybrid-business-models.md` |
| Vingroup (VIC) | Vincom Office trong Landmark 81 | `bds-office-*` + `bds-hybrid-business-models.md` |
| Đất Xanh (DXG) | Một số văn phòng trong dự án dân cư | `bds-office-*` |

### 6.5 Nghỉ dưỡng (resort)

| Mã | Đặc thù | Framework cần đọc |
|---|---|---|
| Vinpearl (VPL) | Niêm yết 2025, 30+ khách sạn và resort | `bds-resort-*` |
| CEO Group (CEO) | Lai dân cư + nghỉ dưỡng, Sonasea Vân Đồn và Phú Quốc | `bds-resort-*` + `bds-hybrid-business-models.md` |
| Đầu tư Phát triển Xây dựng (DIG) | Lai dân cư + nghỉ dưỡng tại Vũng Tàu | `bds-resort-*` + `bds-hybrid-business-models.md` |
| Novaland (NVL) | NovaWorld Phan Thiết, Hồ Tràm — bản chất dân cư có tiện ích resort | `bds-resort-*` + `bds-res-*` |

### 6.6 Trung tâm dữ liệu (data_center)

| Mã | Đặc thù | Framework cần đọc |
|---|---|---|
| Kinh Bắc (KBC) | SGI-HCM Campus trung tâm dữ liệu AI 2 tỷ đô la Mỹ | `bds-dc-hyperscaler-power.md` + `bds-kcn-*` |
| FPT Corporation (FPT) | 4 trung tâm dữ liệu FPT Telecom, hợp tác NVIDIA | `bds-dc-hyperscaler-power.md` |
| Viettel Global Investment (VGI) | Viettel IDC là nhà cung cấp lớn nhất Việt Nam (5 trung tâm dữ liệu) | `bds-dc-hyperscaler-power.md` |
| Becamex (BCM) | Liên doanh Sembcorp năng lượng tái tạo cho trung tâm dữ liệu | `bds-dc-hyperscaler-power.md` + `bds-kcn-*` |

---

## Hướng dẫn tra dữ liệu thời gian thực

Khi phân tích bài viết mới, tra theo thứ tự:

1. **Báo cáo tài chính quý** — phân khúc doanh thu, đòn bẩy, tồn kho
2. **Báo cáo thường niên** — danh sách dự án chủ lực, quỹ đất chi tiết
3. **Framework knowledge base** — 21 file framework dưới đây cho cơ chế và lịch sử (file tham chiếu này là file thứ 22)
4. **Tìm kiếm web** — khi báo cáo tài chính thiếu số liệu cụ thể (cafef.vn, theleader.vn, vneconomy.vn, vietstock.vn)

---

## Liên kết đến 21 framework knowledge base

### Framework chung (áp dụng cho cả ngành)

| File | Nội dung chính |
|---|---|
| [`bds-revenue-recognition-vas.md`](bds-revenue-recognition-vas.md) | Chuẩn kế toán Việt Nam ghi nhận doanh thu, mẫu hình doanh thu lồi theo quý |
| [`bds-debt-leverage.md`](bds-debt-leverage.md) | Đòn bẩy nợ, bốn cơ chế vỡ nợ, khủng hoảng Novaland |
| [`bds-macro-cycle-credit.md`](bds-macro-cycle-credit.md) | Bốn biến vĩ mô, chu kỳ 7-10 năm, truyền dẫn lãi suất |
| [`bds-legal-framework.md`](bds-legal-framework.md) | Ba luật 2024, quy trình pháp lý dự án |
| [`bds-hybrid-business-models.md`](bds-hybrid-business-models.md) | Phân tích mã lai (Vingroup, Becamex, Đầu tư Phát triển Xây dựng) |

### Phát triển dân cư

| File | Nội dung chính |
|---|---|
| [`bds-res-presales-backlog.md`](bds-res-presales-backlog.md) | Doanh số bán trước, doanh số chờ ghi nhận, chu kỳ 4 giai đoạn |
| [`bds-res-land-bank-nav.md`](bds-res-land-bank-nav.md) | Quỹ đất, giá trị tài sản ròng, phân loại pháp lý |
| [`bds-res-project-lifecycle.md`](bds-res-project-lifecycle.md) | Vòng đời 5-15 năm, dòng tiền theo giai đoạn |
| [`bds-res-cycle-indicators.md`](bds-res-cycle-indicators.md) | Leading/Lagging indicators, backtest VHM, decision matrix |

### Khu công nghiệp

| File | Nội dung chính |
|---|---|
| [`bds-kcn-fdi-demand-mechanism.md`](bds-kcn-fdi-demand-mechanism.md) | Cơ chế FDI tạo nhu cầu, 5 bước truyền dẫn |
| [`bds-kcn-inventory-pricing.md`](bds-kcn-inventory-pricing.md) | Tồn kho, định giá theo vùng |
| [`bds-kcn-lease-structure.md`](bds-kcn-lease-structure.md) | Hợp đồng 30-50 năm, thanh toán thu tiền trước nhanh |

### Bán lẻ

| File | Nội dung chính |
|---|---|
| [`bds-retail-footfall-mechanism.md`](bds-retail-footfall-mechanism.md) | Lượt khách → doanh số khách thuê → tiền cho thuê |
| [`bds-retail-tenant-mix-quality.md`](bds-retail-tenant-mix-quality.md) | Chất lượng cơ cấu khách thuê |
| [`bds-retail-anchor-vs-sme-tenants.md`](bds-retail-anchor-vs-sme-tenants.md) | Khách thuê chủ chốt và doanh nghiệp nhỏ và vừa |

### Văn phòng

| File | Nội dung chính |
|---|---|
| [`bds-office-class-tiering.md`](bds-office-class-tiering.md) | Phân hạng A/B/C, định giá theo hạng |
| [`bds-office-hybrid-work-impact.md`](bds-office-hybrid-work-impact.md) | Tác động làm việc kết hợp, dịch chuyển sang chất lượng cao |

### Nghỉ dưỡng

| File | Nội dung chính |
|---|---|
| [`bds-resort-condotel-legal-pitfalls.md`](bds-resort-condotel-legal-pitfalls.md) | Trường hợp Cocobay 2019, rủi ro cam kết lợi nhuận |
| [`bds-resort-tourism-cycle.md`](bds-resort-tourism-cycle.md) | Chu kỳ du lịch, chính sách thị thực |
| [`bds-resort-hybrid-model.md`](bds-resort-hybrid-model.md) | Ba mô hình lai trong resort |

### Trung tâm dữ liệu

| File | Nội dung chính |
|---|---|
| [`bds-dc-hyperscaler-power.md`](bds-dc-hyperscaler-power.md) | Khách hàng đám mây lớn, hạ tầng điện, định giá cao |

---

## Khái niệm & cơ chế

Ngành bất động sản Việt Nam là tập hợp sáu loại bất động sản có cơ chế doanh thu, vòng đời và rủi ro khác hẳn nhau: phát triển dân cư, khu công nghiệp, bán lẻ trung tâm thương mại, văn phòng cho thuê, nghỉ dưỡng, và trung tâm dữ liệu. Master sử dụng file tham chiếu này để nhận diện loại bất động sản từ mã, định tuyến đến framework chuyên đề tương ứng, và đảm bảo áp dụng đúng khung phân tích. Cơ chế cốt lõi của ngành là hai đặc thù: chuẩn kế toán Việt Nam ghi nhận doanh thu khi bàn giao tạo mẫu hình doanh thu lồi theo quý, và đòn bẩy nợ cao với kỳ hạn ngắn 2-3 năm trong khi vòng đời dự án 5-7 năm tạo rủi ro tái cơ cấu định kỳ.

## Pitfalls (đọc số dễ sai)

- **Bẫy 1 — Áp dụng một khung cho mã lai**: Vingroup, Becamex, Đầu tư Phát triển Xây dựng, Đất Xanh đều có 2-3 mảng bất động sản. Viết về Vingroup chỉ với khung phát triển dân cư là sai — phải phân rã theo Vinhomes, Vincom Retail, Vinpearl, Vincom Office. Xem `bds-hybrid-business-models.md`.
- **Bẫy 2 — So sánh chỉ số giữa các loại**: tiền cho thuê khu công nghiệp đô la Mỹ trên mét vuông cho cả kỳ thuê 30-50 năm; tiền cho thuê bán lẻ đô la Mỹ trên mét vuông mỗi tháng. Hai con số không so sánh được trực tiếp. Tỷ lệ lấp đầy 95% bán lẻ khác nghĩa với tỷ lệ lấp đầy 82% khu công nghiệp vì cơ chế khách thuê hoàn toàn khác.
- **Bẫy 3 — Đọc doanh thu ghi nhận một lần như doanh thu định kỳ**: Vinhomes quý ghi nhận bàn giao lớn doanh thu 30.000 tỷ; quý không bàn giao 8.000 tỷ — không có nghĩa doanh nghiệp đột nhiên xấu đi. Tương tự Kinh Bắc quý ký hợp đồng FDI lớn doanh thu tăng 555%. Master không được so quý gần với cùng kỳ năm trước mà không hiểu cơ chế ghi nhận. Xem `bds-revenue-recognition-vas.md`.
- **Bẫy 4 — Nhầm doanh số chờ ghi nhận với doanh thu chắc chắn**: Novaland báo doanh số chờ ghi nhận 60.000 tỷ trên giấy nhưng tỷ lệ chuyển đổi thực chỉ khoảng 12% do pháp lý tắc. Master phải đánh giá chất lượng doanh số chờ ghi nhận (pháp lý sạch chưa, khách có vỡ hợp đồng không) thay vì đọc tổng số.
- **Bẫy 5 — Áp dụng chu kỳ một loại cho loại khác**: chu kỳ phát triển dân cư phụ thuộc lãi suất nội địa và tín dụng bất động sản. Chu kỳ khu công nghiệp phụ thuộc dòng vốn đầu tư trực tiếp nước ngoài. Chu kỳ nghỉ dưỡng phụ thuộc du lịch và chính sách thị thực. Ba chu kỳ độc lập nhau — không đồng pha. Mã lai (Becamex) có thể một mảng tăng một mảng giảm cùng lúc.

## Source log

- https://notion.so/35d273c7a9a181ca84b4eb18795d8a70 — BDS Sector hub
- https://notion.so/35d273c7a9a18190b873fadad6e1c7a0 — KB BDS root
- Tổng hợp từ 18 trang Notion framework con
- Stamp: build 2026-05-11. Review every 2 years (cấu trúc tổng quan ổn định).
