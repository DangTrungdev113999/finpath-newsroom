---
category: frameworks
title: "CK-Industry-Master-Reference"
last_updated: 2026-05-11
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
| Truyền thống đầy đủ dịch vụ | Môi giới + ký quỹ chiếm phần lớn; IB phụ trợ | SSI, HCM, VND |
| Ngân hàng đầu tư dẫn dắt | IB + tự doanh tỷ trọng cao; môi giới phụ | VCI |
| Bán lẻ tập trung sàn | Tập trung thị phần HNX, ký quỹ tích cực | SHS |

### 1.3 Đặc thù thị trường Việt Nam cần nhớ

- **Bào mòn phí (fee compression)**: TCBS miễn phí 2023, DNSE miễn phí trọn đời 2024 → phí điển hình 2026 còn 0,07–0,10%. Áp lực này không đảo chiều.
- **Liên kết ngân hàng mẹ**: TCBS–Techcombank, VPBankS–VPBank, VCBS–Vietcombank tạo lợi thế huy động vốn giá rẻ và phân phối sản phẩm IB. Công ty chứng khoán độc lập (SSI, VCI, HCM) phải tự tạo dòng khách hàng IB.
- **FTSE nâng hạng thị trường mới nổi (10/2025, có hiệu lực 9/2026)**: vốn ngoại thụ động đổ vào; VCI/SSI/HCM hưởng lợi trực tiếp qua IB và bảo lãnh phát hành; VND/SHS hưởng gián tiếp qua thanh khoản tăng.

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

## Nguồn tham chiếu

- Thông tư 210/2014/TT-BTC — Bộ Tài chính (phân loại hoạt động công ty chứng khoán)
- Thông tư 121/2020/TT-BTC — giới hạn an toàn tài chính: https://thuvienphapluat.vn/van-ban/Chung-khoan/Thong-tu-121-2020-TT-BTC
- Quyết định 87/QĐ-UBCK/2017 — hạn mức cho vay ký quỹ: https://ssc.gov.vn
- Nghị định 65/2022/NĐ-CP — siết phát hành trái phiếu doanh nghiệp riêng lẻ
- Nghị định 08/2023/NĐ-CP — tháo gỡ khó khăn thị trường trái phiếu doanh nghiệp
- DNSE miễn phí trọn đời 2024: https://dnse.com.vn
- Báo cáo thị phần môi giới HNX Q1/2026: https://hnx.vn
- FTSE Russell nâng hạng 10/2025: https://mekongasean.vn

---

## Phần suy luận (cần verify)

Các nhận định dưới đây được suy luận từ dữ liệu có sẵn — cần xác minh lại trước khi đưa vào bài viết:

1. **Hệ số khuếch đại ~1,6 lần** được tính từ dữ liệu Q1/2026 (GTGD +39% → doanh thu +62%). Cần kiểm tra xem hệ số này có ổn định qua các chu kỳ khác (2020–2021, 2023) hay chỉ đặc thù Q1/2026 khi nhiều mảng cùng hồi phục đồng thời.

2. **VCI "dự trữ lãi AFS"** — phần lãi chưa thực hiện từ danh mục AFS tích lũy là lợi thế bộ đệm vốn dài hạn. Cần xác minh số dư AFS chưa thực hiện tại thời điểm phân tích (không cố định — thay đổi theo giá thị trường cổ phiếu AFS danh mục VCI).

3. **Thị phần HNX của SHS** là lợi thế tương đối — cần xác minh xem xu hướng tập trung giao dịch về HOSE (sau khi FTSE nâng hạng) có làm giảm giá trị lợi thế này không, hoặc sàn HNX vẫn giữ vai trò riêng với nhà đầu tư trong nước.
