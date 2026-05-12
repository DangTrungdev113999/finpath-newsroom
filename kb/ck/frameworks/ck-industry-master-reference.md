---
category: frameworks
title: "CK-Industry-Master-Reference"
last_updated: 2026-05-12
---

# Công ty chứng khoán Việt Nam — Tham chiếu ngành (6 lớp mental model)

File này là neo nhận thức cho Master CK: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **SSI · VND · HCM · VCI · SHS**. Sáu lớp mental model dưới đây tổ chức cách đọc ngành — từ cấu trúc doanh thu, chu kỳ thanh khoản, đến định vị từng mã — nhằm tránh phán đoán từ bề ngoài và phát hiện tín hiệu phân hóa sớm.

---

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-11 | Khởi tạo — tổng hợp từ 5 deep dive + nguồn Notion CK sector |

---

## LỚP 1 — Hiểu ngành: cấu trúc doanh thu và mô hình kinh doanh

### 1.1 Bốn dòng doanh thu cốt lõi (theo Thông tư 210/2014/TT-BTC)

Công ty chứng khoán Việt Nam sinh lợi nhuận từ bốn nguồn chính:

1. **Môi giới cổ phiếu và chứng khoán phái sinh** — Phí giao dịch tính trên giá trị lệnh. Tỷ lệ phí điển hình 2026 dao động 0,07–0,10% (giảm mạnh từ 0,15–0,25% năm 2018). Doanh thu mảng này biến động thuận chiều và gần như tức thì với giá trị giao dịch bình quân ngày.

2. **Cho vay ký quỹ** — Công ty chứng khoán cho khách hàng vay tiền để mua cổ phiếu, thu lãi suất 12–14%/năm (2026). Biên lợi nhuận mảng này cao (~5–7 điểm phần trăm so với lãi vay huy động vốn). Dư nợ phụ thuộc vào tâm lý thị trường và hạn mức theo quy định.

3. **Tự doanh (đầu tư danh mục tài sản tài chính)** — Công ty dùng vốn tự có để mua cổ phiếu, trái phiếu, chứng chỉ tiền gửi. Lãi/lỗ ghi nhận phụ thuộc vào phân loại tài sản (xem Lớp 2).

4. **Ngân hàng đầu tư (IB)** — Bao gồm: bảo lãnh phát hành cổ phiếu (phí 2–5% giá trị), bảo lãnh phát hành trái phiếu doanh nghiệp (0,5–2%), tư vấn mua bán và sáp nhập (1–3%). Mảng IB có biên lợi nhuận ~84% nhưng chu kỳ dài (thường trễ 6–12 tháng so với khởi sắc thanh khoản).

### 1.2 Ba mô hình kinh doanh chủ đạo tại Việt Nam

| Mô hình | Đặc trưng | Đại diện |
|---|---|---|
| Truyền thống đầy đủ dịch vụ | Môi giới + ký quỹ chiếm phần lớn; IB phụ trợ | SSI, HCM, VND, VIX |
| Ngân hàng đầu tư dẫn dắt | IB + tự doanh tỷ trọng cao; môi giới phụ | VCI |
| Bán lẻ tập trung sàn | Tập trung thị phần HNX, ký quỹ tích cực | SHS |
| Liên kết ngân hàng mẹ | Vốn rẻ từ NH mẹ, phân phối sản phẩm IB nội bộ | MBS, BSI, CTS, AGR, BVS, VFS |
| Bán lẻ/specialty nhỏ | Quy mô vốn nhỏ, niche khách hàng, ít hưởng lợi FTSE | APG, EVS, IVS, PSI, TVS, WSS, ORS, TCI |
| UPCOM nhỏ | Thanh khoản thấp, ít visibility analyst, phụ thuộc chu kỳ | DSC, FTS, CSI, SBS, PHS, ART, APS, BMS, AAS, VTS |

### 1.2.bis Phân nhóm chi tiết theo mã

*Bảng dưới gom 30 mã CK vào phân nhóm + đặc thù riêng. Số liệu định lượng tra Finpath API; bảng này chỉ ghi định vị cấu trúc.*

| Mã | Mô hình | Đặc thù cấu trúc |
|---|---|---|
| SSI | Truyền thống đầy đủ dịch vụ | Vốn chủ lớn nhất ngành; SSIAM phân phối quốc tế; danh mục tự doanh nghiêng trái phiếu + chứng chỉ tiền gửi |
| HCM | Truyền thống đầy đủ dịch vụ | HSC; danh mục tự doanh 100% cổ phiếu FVTPL; danh tiếng tốt với nhà đầu tư nước ngoài |
| VND | Truyền thống đầy đủ dịch vụ | VNDirect; bán lẻ thị phần lớn; dư nợ ký quỹ / vốn chủ thường cao |
| VIX | Truyền thống đầy đủ dịch vụ | Vietnam Investment Securities; mid-cap HOSE; tăng vốn mạnh giai đoạn 2024-2026 |
| VCI | Ngân hàng đầu tư dẫn dắt | Vietcap; danh mục AFS tích lũy nhiều năm tạo "dự trữ lãi"; biên lợi nhuận IB cao nhất nhóm |
| SHS | Bán lẻ tập trung sàn | Sài Gòn - Hà Nội; thị phần dẫn đầu HNX; tự doanh FVTPL cổ phiếu cao |
| MBS | Liên kết ngân hàng mẹ | MB Securities; vốn từ MBBank; IB tăng dần qua các năm |
| BVS | Liên kết ngân hàng mẹ | Bảo Việt CK; phân phối sản phẩm bảo hiểm liên kết |
| BSI | Liên kết ngân hàng mẹ | BIDV Securities (BSC); mạnh trái phiếu doanh nghiệp; mạng lưới rộng |
| AGR | Liên kết ngân hàng mẹ | Agriseco; Agribank backing; retail focus tỉnh |
| CTS | Liên kết ngân hàng mẹ | VietinBank Securities; mid-tier IB; cross-selling khách hàng VietinBank |
| VFS | Liên kết ngân hàng mẹ | Nhất Việt CK; quy mô vốn vừa; định hướng IB |
| APG | Bán lẻ/specialty nhỏ | APG Securities; niche client; quy mô nhỏ |
| EVS | Bán lẻ/specialty nhỏ | Everest Securities; mid-tier; cơ cấu cổ đông tập trung |
| IVS | Bán lẻ/specialty nhỏ | Đầu tư Việt Nam CK; quy mô nhỏ |
| PSI | Bán lẻ/specialty nhỏ | CK Dầu khí; Petrosetco backing; niche ngành năng lượng |
| TVS | Bán lẻ/specialty nhỏ | Thiên Việt CK; quy mô vừa; định hướng IB và quản lý quỹ |
| WSS | Bán lẻ/specialty nhỏ | Phố Wall Securities; quy mô nhỏ |
| ORS | Bán lẻ/specialty nhỏ | TPS Tiên Phong CK; quy mô vừa; bán lẻ |
| TCI | Bán lẻ/specialty nhỏ | Thành Công CK; quy mô nhỏ |
| DSC | UPCOM nhỏ | Đông Sài Gòn CK; quy mô nhỏ |
| FTS | UPCOM nhỏ | FPT Securities (FPTS); fintech-oriented; mid-cap |
| CSI | UPCOM nhỏ | Kiến Thiết CK; quy mô nhỏ |
| SBS | UPCOM nhỏ | Sacombank Securities (đã bán khỏi Sacombank); cơ cấu cổ đông tái cấu trúc |
| PHS | UPCOM nhỏ | Phú Hưng CK; mid-low; định hướng retail |
| ART | UPCOM nhỏ | BOS Securities; cơ cấu cổ đông biến động lịch sử |
| APS | UPCOM nhỏ | APEC CK; cơ cấu cổ đông biến động lịch sử |
| BMS | UPCOM nhỏ | Bảo Minh CK; backing Bảo Minh insurance group |
| AAS | UPCOM nhỏ | Smart Invest; fintech retail focus |
| VTS | UPCOM nhỏ | Việt Tín CK; quy mô nhỏ |

### 1.3 Phân loại CTCK theo nhóm (Q1/2026)

| Nhóm | Mã tiêu biểu | Đặc điểm |
|---|---|---|
| **Top 5** | VPS 15,3%, SSI 11,1%, TCBS 8,9%, VCI 7,4%, HCM 7,3% | Thống trị thị phần môi giới |
| **Tier 2** | MBS 5,3%, VND 4,8%, SHS, BSI | 3-7% thị phần |
| **Ngoại** | Mirae, KIS, Shinhan | Lãi suất margin 8-10% (vốn mẹ nước ngoài) |
| **Liên kết NH** | TCBS, VPBankS, VCBS, MBKE | Lãi suất margin 9-11% |
| **Fintech** | DNSE, Pinetree | Phí 0, app-first |

**Mốc 2025-2026**: VPS IPO (VCSH ~29.000 tỷ) | TCBS VCSH #1 (~45.000 tỷ) | Top 10 thị phần môi giới ~69% | **FTSE nâng hạng 21/09/2026** | VN đạt **11,8 triệu tài khoản** cuối 2025

### 1.4 Cơ cấu doanh thu theo CTCK (structural)

```
VPS: MG 35% + Margin 30% + TD 20% + IB 10%
SSI: Cân bằng — MG 30% + Margin 25% + TD 25% + IB 10%
TCBS: IB 25% + Margin 30% + TP 20% + MG 20%
VND: TD 35% + Margin 25% + MG 25% + IB 15%
MAS: Margin 45% + MG 30% + TD 15%
```

### 1.5 Nguồn vốn cho vay ký quỹ

| Nguồn | Chi phí | Ghi chú |
|---|---|---|
| VCSH | Thấp nhất | Spread cao nhất |
| Vay ngân hàng | 6-8%/năm | Cho vay 9-14%, ăn chênh 3-6% |
| Phát hành trái phiếu | 7-9%/năm | Chi phí cao hơn vay NH |

| Nhóm CTCK | Lãi suất margin | Lý do |
|---|---|---|
| Ngoại | 8-10% | Vốn mẹ nước ngoài |
| Liên kết NH | 9-11% | Vay NH mẹ |
| Lớn độc lập | 9-12% | Vay ngoài |
| Nhỏ | 11-14% | Vốn ít |

### 1.6 Đặc thù thị trường Việt Nam cần nhớ

- **Beta cực cao**: cổ phiếu CK biến động gấp 1,5-2,5 lần VN-Index
- **Bào mòn phí (fee compression)**: TCBS miễn phí 2023, DNSE miễn phí trọn đời 2024 → phí điển hình 2026 còn 0,07–0,10%. Áp lực này không đảo chiều.
- **Liên kết ngân hàng mẹ**: TCBS–Techcombank, VPBankS–VPBank, VCBS–Vietcombank tạo lợi thế huy động vốn giá rẻ và phân phối sản phẩm IB. Công ty chứng khoán độc lập (SSI, VCI, HCM) phải tự tạo dòng khách hàng IB.
- **FTSE nâng hạng thị trường mới nổi (10/2025, có hiệu lực 9/2026)**: vốn ngoại thụ động đổ vào; VCI/SSI/HCM hưởng lợi trực tiếp qua IB và bảo lãnh phát hành; VND/SHS hưởng gián tiếp qua thanh khoản tăng.
- **Margin toàn ngành**: ~370-400 nghìn tỷ (Q3/2025). Margin/VCSH >2x = rủi ro hệ thống

### 1.7 Cạnh tranh & Xu hướng ngành

**NH-backed vs Indie:**
- **Liên kết NH** (TCBS, VPBankS, MBS): funding ~3-4% → ép indie phải huy động TP/CP cost 7-9%
- Game chuyển từ "brokerage commission" sang "interest rate spread" — ai vốn rẻ hơn thắng
- TCBS lãi suất margin 9,5-10,5% vs SSI 12-13%

**Fintech — DNSE, Pinetree:**
- Zero-commission loss leader, monetize qua margin + data
- KHÁC Robinhood vì VN không có PFOF (payment for order flow)
- Fintech-only (không NH mẹ) thua 3-5 năm tới trừ khi M&A

**Race to zero — bẫy biên lợi nhuận:**
- Phí môi giới 2015: 0,35% → 2025: 0,1-0,15%, fintech 0%
- Top 10 chiếm >75% thị phần (~80 CTCK)
- **Dự báo**: 2026-2028: 3-5 CTCK nhỏ sáp nhập/rút giấy phép

**M&A consolidation 2026-2030:**
- VN vào chu kỳ consolidation như Hàn Quốc 2000s và Thái Lan 2010s. Dự báo 80 → 30-40 CTCK 2030
- **Targets tiềm năng**: BOS, APG, PHS, FTS. Định giá 1,5-2,5x book
- **Watch**: CTCK tăng vốn bất thường, đổi cổ đông lớn, C-level Hàn/Nhật/Đài

---

## LỚP 2 — Đọc số: các chỉ số then chốt và cách giải mã

### 2.1 Tài sản tự doanh — ba phân loại kế toán

Tài sản tài chính ghi nhận theo giá thị trường (FVTPL — ghi nhận lãi/lỗ vào lợi nhuận mỗi quý) là phân loại phổ biến nhất. Ngoài ra có hai loại khác:

- **Giữ đến đáo hạn (HTM)**: trái phiếu chính phủ/ngân hàng — thu lãi cố định, không bị biến động thị trường ghi nhận vào lợi nhuận quý.
- **Sẵn sàng để bán (AFS)**: lãi/lỗ chưa thực hiện ghi vào vốn chủ sở hữu, không xuất hiện trên báo cáo lợi nhuận quý — đây là điểm dễ nhầm khi đọc so sánh ROE giữa các công ty.

### 2.2 Giới hạn theo quy định (Thông tư 121/2020/TT-BTC)

| Giới hạn | Mức quy định |
|---|---|
| Trần dư nợ ký quỹ | 200% vốn chủ sở hữu |
| Cho vay 1 khách hàng | ≤3% vốn chủ sở hữu |
| Cho vay 1 mã chứng khoán | ≤10% vốn chủ sở hữu |
| Tổng nợ / vốn chủ | ≤5 lần |
| Hệ số an toàn vốn (CAR) | ≥180% |
| Trái phiếu doanh nghiệp tự doanh | ≤70% vốn chủ sở hữu |
| 1 tổ chức phát hành | ≤15% vốn chủ sở hữu |

### 2.3 Chỉ số đọc nhanh từ báo cáo tài chính

- **Tỷ lệ dư nợ ký quỹ / vốn chủ** (margin utilization): cho biết còn bao nhiêu dư địa tăng trưởng mà không cần tăng vốn. Trên 150% → gần trần, khả năng cao phải phát hành thêm cổ phiếu.
- **Tỷ trọng FVTPL cổ phiếu trong danh mục tự doanh**: tỷ trọng càng cao → biến động lợi nhuận quý càng lớn khi thị trường điều chỉnh.
- **Thị phần môi giới** (theo báo cáo HNX/HOSE hằng quý): biến động thị phần quan trọng hơn mức tuyệt đối — mất 1 điểm phần trăm thị phần tương đương mất hàng chục tỷ doanh thu/quý tại mức GTGD hiện tại.
- **Hệ số giá trị thị trường / giá trị sổ sách (P/B)**: chuẩn định giá ngành; P/B ngành CK Việt thường 1,2–2,5 lần tùy chu kỳ.

### 2.4 Bẫy số liệu phổ biến

- Đừng nhầm **dư nợ cho vay ký quỹ** với **tổng tài sản**: hai con số cách nhau gấp 2–3 lần.
- Công ty có **AFS lớn** (như VCI) trông ROE thấp hơn thực chất vì lãi chưa thực hiện không vào P&L.
- **Doanh thu IB quý** không phản ánh pipeline — hợp đồng ký quý trước thường ghi nhận doanh thu quý sau.

---

## LỚP 3 — Hiểu chu kỳ: bốn pha thị trường và phản ứng từng mảng

→ Chi tiết và dữ liệu lịch sử: [`ck-liquidity-sensitivity.md`](ck-liquidity-sensitivity.md) và [`ck-margin-cycle.md`](ck-margin-cycle.md)

### 3.1 Bốn pha chu kỳ thanh khoản

| Pha | Đặc trưng | Tín hiệu nhận diện |
|---|---|---|
| **Tích lũy** | GTGD thấp, thị trường sideways | GTGD bình quân HOSE dưới 15.000 tỷ/phiên |
| **Bùng nổ** | GTGD tăng mạnh, thị phần xáo trộn | GTGD vượt 20.000 tỷ/phiên, dư nợ ký quỹ tăng nhanh |
| **Quá nhiệt** | Dư nợ ký quỹ gần trần, giải chấp rủi ro cao | Tỷ lệ sử dụng dư nợ ký quỹ toàn ngành > 150% vốn chủ |
| **Điều chỉnh** | GTGD giảm, tự doanh FVTPL lỗ | GTGD dưới 15.000 tỷ, chỉ số điều chỉnh ≥15% |

### 3.2 Hệ số khuếch đại (~1,6 lần)

Khi giá trị giao dịch bình quân tăng, doanh thu toàn ngành tăng nhanh hơn do ký quỹ và tự doanh cùng hưởng lợi đồng thời. Thực nghiệm Q1/2026: GTGD bình quân tăng 39% → doanh thu khối công ty chứng khoán tăng 62%.

### 3.3 Độ trễ phản ứng từng mảng

- **Môi giới**: tức thì trong cùng quý.
- **Cho vay ký quỹ**: trễ 1–2 quý (cần thời gian giải ngân và tăng hạn mức).
- **Ngân hàng đầu tư**: trễ 6–12 tháng (pipeline tích lũy → deal đóng → ghi nhận doanh thu).
- **Tự doanh FVTPL cổ phiếu**: tức thì — phản ánh ngay lợi nhuận quý qua định giá lại.

---

## LỚP 4 — Định vị từng mã: vị thế dài hạn (structural positioning)

*Lớp này chỉ ghi định vị chiến lược bền vững — không ghi số quý gần nhất. Số liệu cụ thể xem từng deep dive hoặc tra Finpath API.*

### SSI — Truyền thống đầy đủ dịch vụ

**Vị thế**: Công ty chứng khoán lớn nhất theo vốn chủ; đủ cả bốn mảng; danh mục tự doanh nghiêng trái phiếu và chứng chỉ tiền gửi — rủi ro thấp.

**Ưu thế dài hạn**: thương hiệu, khách hàng tổ chức, năng lực IB + phân phối quốc tế (SSIAM); hưởng lợi FTSE qua IB và bảo lãnh phát hành.

**Rủi ro cấu trúc**: thị phần môi giới bị bào mòn bởi đối thủ miễn phí (VPS, TCBS, DNSE); cần tăng vốn định kỳ.

### VND — Tăng trưởng tích cực, đa mảng

**Vị thế**: Tăng trưởng tích cực cả thị phần môi giới lẫn ký quỹ; tập trung bán lẻ. Dư nợ / vốn chủ thường ở mức cao → cần theo dõi ngưỡng trần quy định.

**Rủi ro cấu trúc**: không có ngân hàng mẹ lớn → chi phí vốn cao hơn TCBS/VPBankS; ngân hàng đầu tư chưa là mảng dẫn dắt.

### HCM — Chất lượng cao, thân thiện khối ngoại

**Vị thế**: Danh mục tự doanh 100% cổ phiếu FVTPL → biến động lợi nhuận quý cao nhất nhóm; bù lại hưởng lợi hoàn toàn khi thị trường tăng. Danh tiếng tốt với nhà đầu tư nước ngoài.

**Ưu thế dài hạn**: khách hàng nước ngoài và tổ chức; hưởng lợi FTSE qua bảo lãnh phát hành; đang trong giai đoạn tăng vốn mở rộng ký quỹ.

**Rủi ro cấu trúc**: thị trường giảm mạnh → lợi nhuận tự doanh âm ngay lập tức.

### VCI — Ngân hàng đầu tư biên cao chuyên biệt

**Vị thế**: Mô hình ngân hàng đầu tư dẫn dắt; danh mục AFS (tài sản sẵn sàng để bán) tích lũy nhiều năm tạo "dự trữ lãi" chưa thực hiện — bộ đệm vốn dài hạn. Biên lợi nhuận ngân hàng đầu tư cao nhất nhóm.

**Rủi ro cấu trúc**: doanh thu ngân hàng đầu tư biến động theo chu kỳ phát hành; thị phần môi giới nhỏ → ít hưởng lợi ngắn hạn khi thanh khoản tăng.

### SHS — Bán lẻ tập trung HNX

**Vị thế**: Thị phần dẫn đầu tại HNX; danh mục tự doanh tập trung cổ phiếu FVTPL → nhạy cảm cao với thanh khoản và định giá cổ phiếu.

**Rủi ro cấu trúc**: quy mô vốn nhỏ → tăng vốn liên tục là áp lực; ngân hàng đầu tư yếu hơn đối thủ lớn; ít hưởng lợi trực tiếp từ FTSE.

---

## LỚP 5 — Định giá: khung và thông số tham chiếu

→ Xem thêm chi tiết: [`ck-brokerage-marketshare.md`](ck-brokerage-marketshare.md)

### 5.1 Phương pháp định giá phổ biến

- **Hệ số giá / giá trị sổ sách (P/B)**: phương pháp chính cho công ty chứng khoán. Khoảng P/B lịch sử ngành VN: 1,2–2,5 lần. P/B < 1 thường xuất hiện cuối pha điều chỉnh.
- **Định giá theo tổng hợp các mảng (Sum of the Parts)**: tách riêng giá trị môi giới + ký quỹ + IB + tự doanh → cộng lại. Phù hợp với VCI (IB chiếm tỷ trọng lớn) hoặc SSI (danh mục SSIAM tách biệt).
- **Hệ số giá / lợi nhuận (P/E) điều chỉnh**: loại bỏ lãi/lỗ tự doanh FVTPL một lần để thấy lợi nhuận mảng kinh doanh cốt lõi.

### 5.2 Yếu tố định giá lại (re-rating trigger)

Các sự kiện thường dẫn đến định giá lại toàn ngành:
- FTSE/MSCI nâng hạng (→ nâng P/B bền vững)
- Sửa luật chứng khoán hoặc nới room ngoại
- Thay đổi biên độ giao dịch (T+2 → T+0)
- Chu kỳ phát hành trái phiếu doanh nghiệp hồi phục → IB bùng nổ

### 5.3 Vùng định giá chu kỳ (tham chiếu lịch sử)

| Pha thị trường | P/B điển hình ngành |
|---|---|
| Đáy điều chỉnh (2022–Q1/2023) | 0,9–1,3 lần |
| Phục hồi trung bình (2023–2024) | 1,3–1,8 lần |
| Bùng nổ (2021, 2025–2026) | 1,8–2,5 lần |

---

## LỚP 6 — Case study lịch sử: các chu kỳ lớn đã xảy ra

→ Dữ liệu chi tiết: [`ck-proprietary-trading.md`](ck-proprietary-trading.md) và [`ck-ib-revenue-volatility.md`](ck-ib-revenue-volatility.md)

### Chu kỳ 1 — 2018: NHNN siết tín dụng bất động sản

NHNN siết tín dụng bất động sản, GTGD sụt giảm. Bài học: chính sách tiền tệ ảnh hưởng gián tiếp nhưng sâu đến cả bốn mảng doanh thu.

### Chu kỳ 2 — 2020–2021: Bùng nổ COVID

VN-Index từ ~660 → ~1.500 điểm; GTGD bình quân HOSE năm 2021 đạt ~21.593 tỷ/phiên (đỉnh quý Q3–Q4/2021 ước 25.000–30.000 tỷ/phiên), tăng từ ~6.000 tỷ năm 2019 và ~10.231 tỷ năm 2020; lợi nhuận trên mỗi cổ phiếu các công ty chứng khoán lớn tăng ~5 lần; dư nợ / vốn chủ toàn ngành đạt ~129% (Q4/2021). Bài học: khi cả bốn mảng cùng bùng nổ, hệ số khuếch đại đạt tối đa.

### Chu kỳ 3 — 2022: Khủng hoảng trái phiếu doanh nghiệp

Vụ Tân Hoàng Minh (4/2022) và Vạn Thịnh Phát – SCB (10/2022) đóng băng thị trường trái phiếu doanh nghiệp; NĐ 65/2022 siết phát hành. Doanh thu ngân hàng đầu tư toàn ngành giảm ~60%; danh mục FVTPL bị định giá lại âm ~7.664 tỷ; lợi nhuận mảng tự doanh Q4/2022 giảm 94%. Bài học: ngân hàng đầu tư và tự doanh cổ phiếu là hai mảng khuếch đại rủi ro nhất.

### Chu kỳ 4 — 2023–2024: Phục hồi và bào mòn phí

NĐ 08/2023 tháo gỡ một phần khó khăn trái phiếu doanh nghiệp; thị trường phục hồi chậm. TCBS miễn phí giao dịch (2023), DNSE miễn phí trọn đời (2024) → bào mòn phí trở thành xu hướng không đảo chiều. Bài học: giai đoạn phục hồi thường là lúc cấu trúc cạnh tranh thay đổi vĩnh viễn.

### Chu kỳ 5 — 2025–2026: FTSE nâng hạng + tăng vốn

FTSE nâng hạng Việt Nam (10/2025, hiệu lực 9/2026); GTGD bình quân Q1/2026 vượt 30.000 tỷ/phiên, phiên kỷ lục 29/7/2025 đạt 71.763 tỷ. Các công ty chứng khoán lớn đồng loạt tăng vốn. Bài học: nâng hạng khuếch đại toàn chu kỳ nhưng mức hưởng lợi phân hóa rõ theo mô hình kinh doanh.

---

## Hướng dẫn tra dữ liệu thời gian thực

Khi phân tích bài viết mới, tra theo thứ tự:

1. **Finpath API** — tỷ suất sinh lời vốn chủ, dư nợ ký quỹ, tổng tài sản, lợi nhuận trước thuế theo quý
2. **Dữ liệu thị phần** — báo cáo HNX/HOSE hằng quý (thường công bố trước ngày 15 tháng sau)
3. **Deep dive KB** — 5 file framework dưới đây cho context cơ chế và lịch sử
4. **Tìm kiếm web** — khi Finpath thiếu số liệu cụ thể (cafef.vn, tinnhanhchungkhoan.vn, vneconomy.vn)

### Liên kết đến 5 deep dive framework

| Deep dive | Nội dung chính |
|---|---|
| [`ck-liquidity-sensitivity.md`](ck-liquidity-sensitivity.md) | Hệ số khuếch đại, GTGD lịch sử, độ nhạy từng mảng và từng mã |
| [`ck-margin-cycle.md`](ck-margin-cycle.md) | Chu kỳ cho vay ký quỹ, giới hạn quy định, lịch sử dư nợ |
| [`ck-brokerage-marketshare.md`](ck-brokerage-marketshare.md) | Thị phần môi giới theo quý, lịch sử bào mòn phí |
| [`ck-proprietary-trading.md`](ck-proprietary-trading.md) | Ba phân loại tài sản tự doanh, rủi ro FVTPL cổ phiếu |
| [`ck-ib-revenue-volatility.md`](ck-ib-revenue-volatility.md) | Chu kỳ IB, lịch sử phát hành trái phiếu doanh nghiệp, biên lợi nhuận |

---

---

## LỚP 7 — Microstructure & Regulatory

### 7.1 T+2 & NPS (Non Pre-funding Settlement)

- **T+2**: Bán cổ phiếu hôm T → tiền về T+2 (~11:30)
- **Thông tư 68/2024 (02/11/2024)**: Bỏ pre-funding cho tổ chức nước ngoài (NPS)
- **Winners**: SSI, HCM, VCI, VND, Mirae (broker tổ chức)
- **Losers**: VPS, DNSE (retail-focused)

### 7.2 Margin Rules (Thông tư 120/2020)

- Tổng dư nợ ≤ 200% VCSH | 1 khách ≤ 3% | 1 mã ≤ 10%
- Ký quỹ: ban đầu ≥50%, duy trì ≥30% (dưới = call margin)
- Haircut: VN30 30-50%, mid 40-60%, small 50-70%

### 7.3 Force Sell & Reflexivity

- Tỷ lệ <30% → call (1-3 phiên nộp thêm) | <20-25% → force sell ngay
- **Reflexivity**: VNI giảm → call → force → giá giảm thêm → call mới
- VN30 giảm mạnh hơn mid-cap trong panic (force sell bluechip vì còn khớp lệnh)

### 7.4 Room ngoại & KRX

- **Room**: 100% CK, sản xuất | 49% logistics, dịch vụ | 30% NH | NVDR: đang nghiên cứu
- **KRX**: Thay SET cũ (~3M lệnh) → ~20M lệnh. Hỗ trợ T+0, short-selling
- **Go-live**: từng module 2026; full dự kiến 09/2026. Impact: GTGD +30-50%

### 7.5 Timeline Regulatory

| Năm | Sự kiện |
|---|---|
| 2015 | NĐ 60 — room CTCK 100% |
| 2021 | TT 120 margin cap 200% |
| 08/2022 | T+2 + bán cổ phiếu chờ về |
| 09/2022 | NĐ 65 siết TPDN |
| 10/2022 | Vạn Thịnh Phát, VNI -42% |
| 11/2024 | TT 68 bỏ pre-funding |
| 09/2026 | FTSE nâng hạng |

---

## LỚP 8 — Vĩ mô & Catalyst

### 8.1 Ma trận ảnh hưởng

| Yếu tố | MG | Margin | Tự doanh | IB |
|---|---|---|---|---|
| VNI tăng | ++ | ++ | +++ | + |
| VNI giảm | -- | -- | --- | - |
| LS giảm | + | + | + | + |
| Nâng hạng | +++ | ++ | ++ | ++ |

### 8.2 Nâng hạng Timeline

| Mốc | Sự kiện |
|---|---|
| 08/10/2025 | FTSE công bố nâng hạng |
| 21/09/2026 | FTSE chính thức nâng hạng (Secondary EM) |
| 2026-2027 | Rebalance 4 pha |
| 2027-2028 | MSCI upgrade (dự kiến) |

**Impact**: Passive 1-8 tỷ USD | Active 2-3x passive | P/B CTCK re-rate 2,5-3,0x

**Sell-the-news risk**: 2-4 tuần trước ngày hiệu lực có thể -5-10%

### 8.3 Độ trễ Catalyst (Lag Effect)

| Loại catalyst | Ví dụ | Độ trễ | Ghi chú |
|---|---|---|---|
| **Vĩ mô** | TT 68, Fed cắt LS, NĐ mới | 6-12 tháng | Cần thời gian truyền dẫn qua hệ thống |
| **Ngành** | KRX go-live, Luật CK sửa đổi | 1-3 tháng | Ảnh hưởng trực tiếp hơn |
| **Nâng hạng** | FTSE xác nhận | Tức thì | Front-run mạnh, có thể sell-the-news |
| **Sự kiện hoảng loạn** | Thuế Trump, địa chính trị | 1-4 tuần | Thường là cơ hội mua nếu KHÔNG kèm khủng hoảng tín dụng |

**Rule**: Catalyst vĩ mô → kiên nhẫn 2-3 quý. Catalyst ngành → hành động trong 1-2 tháng.

---

## LỚP 9 — Causal Chains

### 9.1 NHNN cắt lãi suất → cổ phiếu CTCK tăng

1. NHTM hạ lãi suất huy động → chi phí cơ hội NĐT giảm → tiền vào CK
2. NHTM hạ lãi suất cho vay → CTCK hạ lãi suất margin (14% → 11-12%)
3. TPCP yield giảm → discount rate giảm → P/E mục tiêu tăng
4. Thanh khoản tăng → cả 4 mảng CTCK tăng → Beta 1,8-2,5x

- **Lag**: cổ phiếu CTCK phản ứng mạnh 1-3 tháng (front-run)
- **Breaks when**: Kèm khủng hoảng tín dụng | FED tăng lãi suất mạnh

### 9.2 VNI tăng → 4 mảng đều tăng

1. **MG**: FOMO → TK mở mới → GTGD tăng
2. **Margin**: Wealth effect → thế chấp cổ phiếu lãi vay thêm
3. **Tự doanh FVTPL**: Mark-to-market lãi vào P&L
4. **IB**: IPO pipeline mở (lag 6-12 tháng)

**Magnitude**: VNI +20% trong 2 quý → MG+Margin +40-60%; tự doanh +50-100%

### 9.3 Margin đỉnh → Call margin cascade (Reflexivity)

1. Shock → VNI -5-7% trong 2-3 phiên
2. TK margin chạm ngưỡng duy trì → CTCK call margin
3. Không nộp → force sell bluechip (thanh khoản cao)
4. **Reflexivity**: 1 mã force → kéo mã cùng holder → cascade

**2022**: VNI -43%. Force sell đóng góp ước 15-20% mức giảm

### 9.4 USD tăng → NN bán ròng

- USD/VND +3%/quý hoặc DXY >106 → Passive ETF rút ròng
- **2024**: NN bán ròng ~94.450 tỷ (~3,7 tỷ USD)
- **Double-hit**: SSI (30-40% DT từ tổ chức nước ngoài), HSC (25-35%)

---

## LỚP 10 — Quantitative Reference

### 10.1 Correlations

| Metric | Value |
|---|---|
| VNI ↔ LN CTCK | 0,75-0,85, lag 0-1 quý |
| GTGD ↔ DT MG | 0,90-0,95, real-time |
| LS ↔ Margin demand | -0,65 to -0,75, lag 1-2 quý |

### 10.2 Thresholds

| Metric | Levels |
|---|---|
| GTGD/phiên | <10k trầm / 15-20k TB / >25k sôi động / >35k quá nóng |
| LS margin | <9% demand tăng mạnh / 9-11% ổn / >12% demand giảm / >14% sụt |
| Margin/VCSH | <1,0x an toàn / 1,0-1,5x tối ưu / 1,5-2,0x cảnh báo / >2,0x nguy hiểm |
| Thị phần | <2% phải zero-fee / 5-10% giữ 0,15-0,20% / >10% premium |
| P/B ngành | <0,8x extreme buy / 0,8-1,0x buy / 1,0-1,3x fair / 1,3-1,6x reduce / >1,6x sell |

### 10.3 Leading indicators

1. GTGD bq 20 phiên → DT MG (0-1 quý)
2. LS liên NH → Margin demand (1-2 quý)
3. TK mở mới → GTGD (2-3 quý)
4. Foreign flow → Sentiment (1-2 tháng)
5. VNM ETF flows → VNI (1-5 ngày)

---

## LỚP 11 — Dữ liệu lịch sử bổ sung

### 11.1 Chu kỳ VNI

| Thời điểm | VNI | Sự kiện |
|---|---|---|
| 03/2007 | 1.170 | Đỉnh bong bóng |
| 02/2009 | 235 | Đáy (-80%) |
| 01/2022 | 1.528 | Đỉnh chu kỳ 3 |
| 11/2022 | 873 | Đáy (-43%) |
| 10/2025 | 1.790 | Đỉnh lịch sử mới |

### 11.2 Thanh khoản GTGD/phiên (bổ sung)

| Năm | GTGD | Ghi chú |
|---|---|---|
| 2019 | ~4.100 tỷ | Baseline |
| 2021 | ~21.600 tỷ | **Đỉnh năm** |
| 2024 | 15-20k tỷ | Phục hồi |
| Q3/2025 | ~35k tỷ | KRX launch |
| 08/2025 | 78.200 tỷ | Kỷ lục 1 phiên |

### 11.3 Dư nợ margin (bổ sung)

| Thời điểm | Margin | Margin/VCSH |
|---|---|---|
| Q1/2022 | 200k tỷ | **1,2x (KỶ LỤC)** |
| Q4/2022 | 118k tỷ | 0,7x (sau call margin) |
| Q4/2025 | ~400k tỷ | 1,0x |

### 11.4 VCSH top CTCK (04/2026)

| CTCK | VCSH (tỷ) |
|---|---|
| TCBS | 45.466 |
| VPS | 28.835 |
| SSI | ~26.000 |
| VPBankS | ~20.000 |
| VND | ~18.000 |

---

## LỚP 12 — Ngôn ngữ cho NĐT (từ điển)

| Thuật ngữ | Diễn giải |
|---|---|
| GTGD tăng | Nhiều người mua bán hơn trên sàn |
| Margin tăng | NĐT đang vay tiền mua cổ phiếu nhiều hơn |
| Call margin | Giá giảm quá → phải bán trả nợ |
| Tự doanh lãi/lỗ | CTCK mua cổ phiếu bằng tiền mình → lãi/lỗ |
| Beta cao | Lên nhanh, xuống cũng nhanh |
| Nâng hạng | VN thành thị trường mới nổi → quỹ ngoại đổ tiền vào |
| P/B 2x | Giá = 2 lần giá trị sổ sách |

---

## LỚP 13 — Quy tắc Agent (35 điều)

### Core Rules (1-12)

1. **VNI quyết định 80%** → Phân tích VNI trước CTCK
2. **Không tin "LN kỷ lục"** mà không check tự doanh
3. **Margin dao hai lưỡi** → Kỷ lục = rủi ro kỷ lục
4. **Thị phần tăng ≠ DT tăng** nếu phí = 0
5. **Cổ phiếu CK beta cực cao** → Cảnh báo NĐT mới
6. **Cổ phiếu CK leading indicator** → Tăng/giảm trước VNI 2-4 tuần
7. **Dịch thuật ngữ** cho NĐT ít kinh nghiệm
8. **Không bịa data** → Thiếu thì nói thiếu
9. **LUÔN cross-check LN** vs cơ cấu DT
10. **LUÔN breakdown TD**: cổ phiếu nhiều = rủi ro, TP+CCTG = ổn
11. **Pre-funding/NPS** → gắn FTSE 09/2026
12. **Call margin ≠ force sell** — call là yêu cầu, force là hành động

### Quantitative Rules (13-20)

13. **GTGD correlation 0,85** với LN — quan trọng hơn VNI direction
14. **Margin rate >12%** → demand giảm; <9% → demand tăng mạnh
15. **Thị phần >5%** mới có pricing power
16. **P/B <1,0x buy**, >1,6x sell
17. **ETF flows** leading 1-5 ngày
18. **Fed policy** = driver #1 foreign flow
19. **Margin đỉnh ≠ top** nếu Margin/Mcap <2,8%
20. **Nâng hạng có thể thất bại**: check P/E <15x, tỷ trọng >0,5%

### Deep Rules (21-35)

21. **Evaluation gain** có thể 50-80% DT tự doanh quý tăng — EPS đẹp nhưng không tiền. Luôn hỏi realized/unrealized
22. **CIR CTCK** thường KHÔNG gồm lãi vay — tính lại khi so sánh
23. **(Nợ vay + Repo)/VCSH** mới là đòn bẩy thực
24. **FVTPL ↔ AFS reclass** là bẫy giấu lỗ lớn nhất — watch AFS tăng đột biến
25. **NHNN pivot** là leading indicator mạnh nhất CTCK — lead VNI 4-8 tuần
26. **Beta CTCK 1,5-2,5x** VNI đồng đều qua case 2018/2020/2022/2023
27. **Margin/VCSH toàn ngành >2,0x** = red zone (2018, cuối 2021 đều đúng trước crash)
28. **Race to zero** phí MG → monetize qua margin + wealth → risk profile chuyển
29. **CTCK NH-backed** có moat funding rẻ bền vững hơn indie trong chu kỳ LS cao
30. **Top 5 không đảm bảo an toàn**: check governance, concentration
31. **Phát hành >20% vốn** → giảm kỳ vọng giá 20-30%, thanh khoản kỷ lục không cứu được
32. **Insider buying + mua CP quỹ** = tín hiệu đáy mạnh hơn chỉ số kỹ thuật
33. **Catalyst vĩ mô lag 6-12 tháng** — đừng kỳ vọng phản ứng ngay
34. **Sự kiện hoảng loạn ngắn hạn** (địa chính trị, thuế) thường là cơ hội MUA nếu không kèm khủng hoảng tín dụng
35. **Khối ngoại bán ròng kéo dài** → ảnh hưởng mạnh cổ phiếu room ngoại cao (SSI, HCM, VCI)

---

## Nguồn tham chiếu

- Thông tư 210/2014/TT-BTC — Bộ Tài chính (phân loại hoạt động công ty chứng khoán)
- Thông tư 121/2020/TT-BTC — giới hạn an toàn tài chính: https://thuvienphapluat.vn/van-ban/Chung-khoan/Thong-tu-121-2020-TT-BTC
- Thông tư 120/2020/TT-BTC — quy định margin
- Thông tư 68/2024 — bỏ pre-funding cho tổ chức nước ngoài (NPS)
- Quyết định 87/QĐ-UBCK/2017 — hạn mức cho vay ký quỹ: https://ssc.gov.vn
- Nghị định 65/2022/NĐ-CP — siết phát hành trái phiếu doanh nghiệp riêng lẻ
- Nghị định 08/2023/NĐ-CP — tháo gỡ khó khăn thị trường trái phiếu doanh nghiệp
- DNSE miễn phí trọn đời 2024: https://dnse.com.vn
- Báo cáo thị phần môi giới HNX Q1/2026: https://hnx.vn
- FTSE Russell nâng hạng 10/2025: https://mekongasean.vn
- Agent Ngành Chứng Khoán VN Knowledge Base v2.0

---

## Phần suy luận (cần verify)

Các nhận định dưới đây được suy luận từ dữ liệu có sẵn — cần xác minh lại trước khi đưa vào bài viết:

1. **Hệ số khuếch đại ~1,6 lần** được tính từ dữ liệu Q1/2026 (GTGD +39% → doanh thu +62%). Cần kiểm tra xem hệ số này có ổn định qua các chu kỳ khác (2020–2021, 2023) hay chỉ đặc thù Q1/2026 khi nhiều mảng cùng hồi phục đồng thời.

2. **VCI "dự trữ lãi AFS"** — phần lãi chưa thực hiện từ danh mục AFS tích lũy là lợi thế bộ đệm vốn dài hạn. Cần xác minh số dư AFS chưa thực hiện tại thời điểm phân tích (không cố định — thay đổi theo giá thị trường cổ phiếu AFS danh mục VCI).

3. **Thị phần HNX của SHS** là lợi thế tương đối — cần xác minh xem xu hướng tập trung giao dịch về HOSE (sau khi FTSE nâng hạng) có làm giảm giá trị lợi thế này không, hoặc sàn HNX vẫn giữ vai trò riêng với nhà đầu tư trong nước.
