# Sector Context — Dầu khí (oilGas)

> Loaded from `Skill: finpath-newsroom-master-oilgas`. V5.1.3 — KHÔNG có `kb/oilgas/` folder; file này thay vai trò KB.

## Overview

Sector Dầu khí Việt Nam niêm yết 8 mã chia 3 mảng theo vị trí trong chuỗi giá trị:

| Mảng | Tickers | Vai trò |
|---|---|---|
| **Upstream** (thăm dò khai thác + dịch vụ) | PVS · PVD · PVT | Cung cấp dịch vụ kỹ thuật, khoan thăm dò, vận tải dầu thô. Doanh thu phụ thuộc số dự án dầu khí Việt Nam + giá dầu chu kỳ. |
| **Downstream** (lọc hoá dầu + phân phối) | BSR · PLX · OIL | Lọc dầu thô thành sản phẩm tinh chế (BSR Bình Sơn) + phân phối xăng dầu bán lẻ (PLX Petrolimex, OIL PVOil). Lợi nhuận phụ thuộc biên lọc dầu + chính sách giá xăng dầu nhà nước. |
| **Utility điện khí** | GAS · POW | GAS phân phối khí thiên nhiên cho công nghiệp + điện. POW vận hành nhà máy điện khí, doanh thu theo hợp đồng PPA với EVN. |

## Cycle drivers

Sector Dầu khí Việt Nam vận động theo 4 chu kỳ chồng:

1. **Giá dầu Brent (USD/thùng)** — biến số gốc. Brent up → upstream lợi (doanh thu PVS/PVD/PVT theo dự án mới mở); biên lọc dầu BSR có thể nới hoặc co tuỳ chênh lệch đầu vào-đầu ra.
2. **OPEC+ policy** — quyết định sản lượng họp định kỳ 2-3 tháng. Cắt sản lượng → giá dầu support. Nới sản lượng → giá dầu sụp (2020 + 2014 lessons).
3. **Tỷ giá VND/USD** — dầu thô nhập bằng USD, xăng dầu bán bằng VND. VND yếu vừa → biên BSR/PLX co. VND yếu mạnh + tăng giá xăng → biên hồi.
4. **Demand nội địa** — Q4/Tết peak xăng dầu + điện. Q1 thường thấp. POW phụ thuộc nhu cầu điện toàn quốc + lượng khí Đông Nam Bộ cung cấp.

## Key metrics

| Metric | Tiếng Việt | Áp dụng |
|---|---|---|
| Crack spread | Chênh lệch giá dầu thô-sản phẩm | BSR, PLX (đánh giá biên lọc dầu cycle) |
| Refining margin | Biên lọc dầu | BSR (USD/thùng) |
| Throughput | Sản lượng tinh chế | BSR (triệu tấn/năm), công suất nhà máy Dung Quất ~6,5 triệu tấn |
| Realized oil price | Giá bán thực tế | Upstream (chênh giá Brent so giá bán Việt Nam) |
| Utilization rate | Hiệu suất sử dụng công suất | BSR (>95% = full load), POW (giờ vận hành/năm) |
| Inventory days | Tồn kho dầu thô (số ngày) | PLX, OIL (đánh giá vốn lưu động) |
| Crude oil | Dầu thô | Đầu vào downstream |
| Refined product | Sản phẩm tinh chế (xăng A92/A95, dầu DO, FO) | Đầu ra BSR, đầu vào PLX/OIL phân phối |

## Analysis lens

### Bullish signals

- **Brent up + biên lọc dầu nới** → upstream (PVS/PVD) lợi nhờ dự án mới mở, downstream (BSR) lợi nếu giá dầu thô lên chậm hơn giá xăng (lag effect)
- **OPEC+ cắt sản lượng** → Brent support → upstream Việt Nam được hưởng giá bán cao hơn ngắn hạn
- **Demand Q4/Tết nội địa** → PLX/OIL bán bán lẻ tăng, BSR full load
- **VND yếu vừa (3-5%)** → xuất khẩu dầu thô / sản phẩm xuất ra Đông Nam Á có doanh thu cao hơn quy ra VND
- **POW thiếu khí Đông Nam Bộ** → EVN ép sản lượng POW chạy nhà máy nhiệt điện than backup, giờ vận hành tăng

### Bearish signals

- **Brent crash** (2020 case Brent âm giá, 2014 -60%) — upstream mất doanh thu dự án; downstream biên lọc co nếu tồn kho mua giá cao
- **OPEC+ nới sản lượng** → Brent sụp ngắn hạn, cycle chuyển từ tăng sang giảm
- **Demand domestic giảm** (suy thoái, dịch covid) → PLX/OIL bán bán lẻ co, BSR phải hạ công suất
- **Chính sách giá xăng dầu nhà nước** kẹp biên — khi Brent up nhưng nhà nước không cho tăng giá xăng đủ → biên downstream bị nén
- **VND yếu mạnh (>8%)** kèm Brent up đồng thời → chi phí đầu vào nhập lên gấp đôi, gây sốc

### Historical analogs (Master tham chiếu khi viết)

1. **BSR 2022 super-cycle Brent $120** — biên lọc dầu Singapore lập kỷ lục 30 USD/thùng (bình thường 5-10), BSR LNTT cả năm vượt 12.000 tỷ. Pattern: kéo dài 9-12 tháng từ khi OPEC+ ổn định sản lượng + chiến tranh Ukraine.
2. **PVD 2020 oil crash âm giá** — Brent xuống âm 37 USD/thùng tháng 4/2020 lần đầu lịch sử do dư thừa kho + cầu sụp covid. PVD mất 70% doanh thu dịch vụ khoan, lỗ năm 2020 nặng. Pattern: oil crash kéo 18-24 tháng phục hồi.
3. **GAS biến động theo OPEC+** — cycle 3-5 năm. Khi giá khí thế giới up → GAS có lợi từ giá hợp đồng dài hạn với EVN/khách hàng công nghiệp. Khi down → biên co vì giá đầu ra bị nén bởi chính sách EVN.
4. **POW 2023 thiếu khí Đông Nam Bộ** — nguồn khí Bể Cửu Long suy giảm tự nhiên, EVN ép POW chạy backup nhiệt điện than. Pattern: vùng đệm cho POW khi khí thiếu, nhưng biên co vì than đắt hơn khí.
5. **PLX 2024 chính sách Quỹ bình ổn giá** — nhà nước cho điều chỉnh giá xăng linh hoạt hơn → biên Petrolimex hồi từ Q3 sau 18 tháng nén.

## Sector-level reading (Master apply khi pick stance)

| Kịch bản | Mảng được lợi | Mảng bị hại |
|---|---|---|
| Brent +20%, OPEC+ cắt sản lượng | Upstream (PVS/PVD/PVT) | Downstream (BSR/PLX) nếu giá xăng chưa kịp theo |
| Brent -30%, OPEC+ nới sản lượng | Upstream lỗ ngắn hạn | Downstream có thể lợi short-term nếu tồn kho mua sau crash |
| VND yếu + Brent flat | Upstream (giá bán USD quy VND tăng) | Downstream (chi phí đầu vào lên) |
| Demand Q4 nội địa tăng | Downstream (PLX/OIL bán lẻ), Utility (POW giờ vận hành) | Upstream ít chịu ảnh hưởng ngắn hạn |
| Nhà nước siết giá xăng | Downstream biên co | Upstream không ảnh hưởng trực tiếp |

## Pitfalls Master cần tránh

1. **Nhầm Brent với WTI** — Brent là chuẩn châu Âu/châu Á, WTI là chuẩn Mỹ. Việt Nam tham chiếu Brent + Singapore Mogas 92.
2. **Confuse biên lọc dầu Việt Nam với Singapore margin** — BSR biên thường thấp hơn Singapore 2-3 USD/thùng do nhà máy Dung Quất công nghệ cũ.
3. **POW không phải pure-play điện khí** — POW có 1-2 nhà máy thuỷ điện nhỏ + backup than. Doanh thu structure không bằng GAS đơn ngành.
4. **PLX không phải lọc dầu** — PLX là phân phối xăng dầu bán lẻ + công nghiệp. Lợi nhuận PLX phụ thuộc biên phân phối, không phụ thuộc trực tiếp Brent.
5. **PVS không phải khoan** — PVS làm dịch vụ kỹ thuật (xây dàn, bảo trì, hỗ trợ). PVD mới là khoan thực địa. Nhầm 2 mã này gây sai bài.
