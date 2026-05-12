---
category: frameworks
title: "CK-IB-revenue-volatility"
last_updated: 2026-05-12
---

Doanh thu ngân hàng đầu tư là mảng biến động nhất trong 5 nguồn thu của công ty chứng khoán Việt — phụ thuộc hoàn toàn vào chu kỳ phát hành vốn và hoạt động mua bán sáp nhập. Tốt trong năm thị trường tăng, sụp trong năm thị trường đóng băng. Master CK cần đọc kỹ framework này để không đánh giá sai cơ cấu lợi nhuận của công ty chứng khoán phụ thuộc nhiều vào mảng này.

## Khái niệm & cơ chế

Doanh thu ngân hàng đầu tư của công ty chứng khoán Việt đến từ 3 mảng chính:

1. **Bảo lãnh phát hành cổ phiếu** — phát hành lần đầu ra công chúng, phát hành riêng lẻ, phát hành quyền. Phí bảo lãnh 2-5% giá trị phát hành. Phụ thuộc vào chu kỳ thị trường — năm thị trường tốt doanh nghiệp đua nhau huy động vốn; năm thị trường xấu cửa đóng.

2. **Bảo lãnh và đại lý phát hành trái phiếu doanh nghiệp** — phí 0,5-2% giá trị phát hành. Đây là mảng lớn nhất về khối lượng: tổng giá trị phát hành trái phiếu doanh nghiệp toàn ngành 2024 đạt 485.000 tỷ đồng, 2025 đạt 644.300 tỷ đồng. Rủi ro cao: công ty chứng khoán đứng tên bảo lãnh chịu trách nhiệm pháp lý nếu tổ chức phát hành vỡ nợ.

3. **Tư vấn mua bán sáp nhập và tái cơ cấu** — phí thành công 1-3% giá trị thương vụ. Mỗi thương vụ là khoản thu một lần lớn, không phân kỳ. Ví dụ: thương vụ 400 triệu USD tạo doanh thu tư vấn ~4-12 triệu USD (~100-300 tỷ) ghi nhận đúng quý đóng thương vụ.

**Cơ chế biến động cao**: Cả 3 mảng đều phụ thuộc vào (a) chu kỳ thị trường vốn, (b) môi trường pháp lý phát hành, và (c) tâm lý nhà đầu tư về tài sản doanh nghiệp phát hành. Không có doanh thu định kỳ như cho vay ký quỹ — một quý không có thương vụ là quý doanh thu ngân hàng đầu tư về gần bằng không.

**Chu kỳ bùng nổ - sụp đổ**: Mảng ngân hàng đầu tư là nguồn thu biến động nhất trong 5 dòng thu của công ty chứng khoán. Năm thị trường vốn tốt (2020-2021): doanh thu tăng vọt. Năm khủng hoảng (2022): doanh thu sụp 40-70% so với cùng kỳ. Năm phục hồi (2024-2025): ấm dần nhưng chưa về đỉnh.

## Quy định pháp lý + threshold

**Nghị định 65/2022/NĐ-CP** (có hiệu lực 16/9/2022) — sửa đổi Nghị định 153/2020 về chào bán trái phiếu doanh nghiệp riêng lẻ:
- Yêu cầu **xếp hạng tín nhiệm** cho một số loại trái phiếu (lộ trình từ 1/1/2023)
- Yêu cầu công bố mục đích sử dụng vốn rõ ràng, cam kết sử dụng đúng mục đích
- Bổ sung quy định về đại diện người sở hữu trái phiếu
- Yêu cầu mở tài khoản riêng nhận tiền phát hành
- Siết điều kiện nhà đầu tư chuyên nghiệp cá nhân

**Nghị định 08/2023/NĐ-CP** — ban hành để giải cứu thị trường sau khủng hoảng 2022, cho phép doanh nghiệp hoãn một số nghĩa vụ theo Nghị định 65, gia hạn một số điều kiện.

**Thông tư 96/2020/TT-BTC** — quy định công bố thông tin trên thị trường chứng khoán, áp dụng cho công ty chứng khoán bảo lãnh phát hành.

**Vốn tối thiểu công ty chứng khoán bảo lãnh phát hành** (Thông tư 121/2020/TT-BTC): Công ty chứng khoán hoạt động bảo lãnh phát hành chứng khoán phải duy trì vốn điều lệ tối thiểu **300 tỷ đồng** — ngưỡng loại phần lớn công ty chứng khoán nhỏ khỏi mảng này. Thực tế chỉ khoảng 20-25 công ty chứng khoán trong tổng số ~80 có giấy phép bảo lãnh phát hành.

**Quy định xếp hạng tín nhiệm** (lộ trình NĐ 65/2022): Từ 2023 một số loại trái phiếu doanh nghiệp phát hành riêng lẻ bắt buộc có xếp hạng tín nhiệm từ tổ chức được Bộ Tài chính cấp phép. Việt Nam hiện có 3 công ty xếp hạng tín nhiệm được cấp phép: VIS Rating, FiinRatings, và CRIF Vietnam.

## Benchmark dài hạn (ranges) — KHÔNG per-quarter

### Range cấu trúc doanh thu ngân hàng đầu tư / tổng doanh thu công ty chứng khoán (historical)

- **5-10% tổng doanh thu toàn ngành** công ty chứng khoán (năm phục hồi 2024: ~3.500 tỷ / ~70.000 tỷ tổng doanh thu ngành ≈ 5%)
- **10-20% cho công ty chứng khoán thiên ngân hàng đầu tư** (VCI, HCM): cơ cấu VCI 2024 — ngân hàng đầu tư chiếm khoảng 10%; HCM kỳ vọng 200-240 tỷ / tổng doanh thu ~1.500-2.000 tỷ ≈ 10-16%
- **<5% cho công ty chứng khoán thiên bán lẻ** (VPS, TCBS): tập trung môi giới + cho vay ký quỹ, ít hoạt động tư vấn phát hành

### Range phí dịch vụ ngân hàng đầu tư

- **Bảo lãnh phát hành cổ phiếu** (phát hành lần đầu + tăng vốn): 2-5% giá trị phát hành
- **Tư vấn mua bán sáp nhập**: 1-3% giá trị thương vụ (phí thành công — chỉ tính khi đóng thương vụ)
- **Bảo lãnh trái phiếu doanh nghiệp**: 0,5-2% giá trị phát hành; đại lý phân phối 0,3-1%

### Range giá trị phát hành trái phiếu doanh nghiệp toàn ngành theo năm

| Giai đoạn | Khối lượng phát hành | Ghi chú |
|---|---|---|
| 2019 | ~297.000 tỷ | Nền tảng trước bùng nổ |
| 2020 | ~403.000 tỷ | +35,9% so với 2019 — bắt đầu bùng nổ |
| 2021 | ~606.000 tỷ | Đỉnh lịch sử — BĐS + ngân hàng phát hành ồ ạt |
| 2022 | ~337.000 tỷ | Sụp -44% sau khủng hoảng Tân Hoàng Minh + Vạn Thịnh Phát |
| 2023 | ~297.000 tỷ | Tiếp tục co lại — nhà đầu tư mất niềm tin |
| 2024 | ~485.000 tỷ | Phục hồi +40% — thị trường ổn định hơn sau NĐ 08/2023 |
| 2025 | ~644.000 tỷ | +35,5% so với 2024 — tăng tốc phục hồi |

### Range biên lợi nhuận ngành ngân hàng đầu tư toàn khối công ty chứng khoán

- 9T/2025: Tổng doanh thu ngân hàng đầu tư 60 công ty chứng khoán = 3.550 tỷ, lợi nhuận = 3.000 tỷ → **biên lợi nhuận ~84%** (cao do chi phí cố định thấp — chủ yếu nhân lực tư vấn)
- Top 10 công ty chứng khoán chiếm **91,3%** tổng doanh thu ngân hàng đầu tư toàn ngành → mảng này cực kỳ tập trung, không có cơ hội công ty nhỏ

## Case study lịch sử + chu kỳ

### 2020-2021 — Thị trường trái phiếu doanh nghiệp bùng nổ

Tổng phát hành trái phiếu doanh nghiệp 2021 đạt kỷ lục ~606.000 tỷ đồng, riêng nhóm bất động sản phát hành ~214.000 tỷ (gấp 3 lần 2020). Công ty chứng khoán thu phí bảo lãnh + phân phối mạnh. Thị trường phát hành lần đầu ra công chúng và tăng vốn cũng sôi động. Đây là năm đỉnh doanh thu ngân hàng đầu tư trước khủng hoảng 2022.

### Tháng 4/2022 — Tân Hoàng Minh: Cú sốc đầu tiên

Uỷ ban Chứng khoán Nhà nước hủy 9 đợt phát hành trái phiếu của 3 công ty thuộc Tập đoàn Tân Hoàng Minh (tổng giá trị 10.030 tỷ đồng, phát hành từ 7/2021 đến 3/2022) do công bố thông tin sai sự thật. Ngay lập tức làn sóng lo ngại về tính pháp lý của trái phiếu doanh nghiệp riêng lẻ lan rộng. Chính phủ ban hành Nghị định 65/2022 để siết chặt quy định.

### Tháng 10/2022 — Vạn Thịnh Phát – SCB: Khủng hoảng toàn diện

Bà Trương Mỹ Lan bị khởi tố (tháng 10/2022) sau scandal trái phiếu "khống" gắn với Ngân hàng SCB và Công ty Chứng khoán Tân Việt (TVSI). Tổng thiệt hại hơn 30.081 tỷ đồng với 35.824 người bị hại. Hậu quả ngay lập tức:
- Nhà đầu tư đổ xô rút tiền khỏi SCB, yêu cầu mua lại trái phiếu trước hạn
- Thị trường trái phiếu doanh nghiệp đóng băng — doanh nghiệp không thể phát hành mới
- Tổng phát hành trái phiếu doanh nghiệp cả năm 2022 sụp về 337.000 tỷ (-44% so với 2021)

Tác động trực tiếp lên doanh thu ngân hàng đầu tư toàn ngành: ước tính giảm 40-60% so với cùng kỳ 2021 do thị trường trái phiếu đóng + phát hành cổ phiếu trì hoãn (VN-Index giảm -32,8% cả năm 2022).

### 2023 — Phục hồi rất chậm, tâm lý thận trọng

Chính phủ ban hành Nghị định 08/2023 để hoãn một số quy định NĐ 65/2022, giải cứu doanh nghiệp gặp khó. Tổng phát hành 2023 tiếp tục giảm về ~297.000 tỷ vì nhà đầu tư cá nhân vẫn mất niềm tin sau Vạn Thịnh Phát. Doanh thu ngân hàng đầu tư toàn khối phục hồi chậm.

### 2024-2026 — Ổn định mức mới, cơ cấu khác trước

Thị trường trái phiếu doanh nghiệp phục hồi về 485.000 tỷ (2024) rồi 644.000 tỷ (2025) nhưng cơ cấu khác: ít trái phiếu bất động sản không tài sản đảm bảo; nhiều hơn trái phiếu ngân hàng + doanh nghiệp có xếp hạng tín nhiệm. Thị phần ngân hàng đầu tư dịch chuyển mạnh sang công ty chứng khoán thuộc ngân hàng (VPBankS, TCBS) nhờ tệp khách hàng tổ chức + năng lực vốn. Tổng doanh thu ngân hàng đầu tư 9T/2025 đạt 3.550 tỷ (+23% so cùng kỳ), lợi nhuận 3.000 tỷ (+29%).

## Bẫy khi đọc số

1. **Nhầm doanh thu ngân hàng đầu tư với phí môi giới** — Phí ngân hàng đầu tư là khoản một lần lớn từ thương vụ cụ thể, không phải phí thu theo mỗi lệnh giao dịch. Trên báo cáo tài chính công ty chứng khoán, hai dòng này nằm tách biệt: "Doanh thu hoạt động môi giới" vs "Doanh thu nghiệp vụ bảo lãnh phát hành" và "Doanh thu hoạt động tư vấn".

2. **Bẫy lump sum một thương vụ lớn** — 1 thương vụ mua bán sáp nhập 200 tỷ phí tư vấn ghi nhận 1 quý → lợi nhuận tăng vọt +30%. Quý tiếp theo về mức nền. Không được ngoại suy xu hướng từ 1 quý có thương vụ lớn bất thường.

3. **Bẫy giao dịch nội bộ** — Khi công ty chứng khoán bảo lãnh phát hành cho công ty cùng hệ sinh thái (TCBS bảo lãnh trái phiếu cho Techcombank, MBS bảo lãnh cho MB Bank), phí có thể không phản ánh giá thị trường. Doanh thu ngân hàng đầu tư từ giao dịch nội bộ cần đọc kèm thuyết minh báo cáo tài chính.

4. **Nhầm công ty chứng khoán tự phát hành trái phiếu với doanh thu ngân hàng đầu tư** — Một số công ty chứng khoán phát hành trái phiếu riêng để huy động vốn cho vay ký quỹ (SSI, VCI, HCM đều làm vậy). Đây là **chi phí tài chính**, không phải doanh thu ngân hàng đầu tư. Đọc thuyết minh báo cáo tài chính để phân biệt.

5. **Nhầm giá trị thương vụ pipeline với doanh thu** — Công ty chứng khoán thường công bố "pipeline X tỷ USD deal value". Đây là tổng giá trị thương vụ đang tư vấn, chứ không phải doanh thu ngân hàng đầu tư. Phí thực thu chỉ 1-3% giá trị và chỉ ghi nhận khi thương vụ hoàn tất. Ví dụ: HCM công bố pipeline 1,2 tỷ USD (2023-2024) → doanh thu ngân hàng đầu tư thực tế nhiều năm chỉ 200-240 tỷ mỗi năm.

6. **Bẫy rủi ro bảo lãnh trái phiếu** — Công ty chứng khoán đứng tên bảo lãnh phát hành trái phiếu doanh nghiệp có thể bị truy đòi nếu tổ chức phát hành vỡ nợ hoặc không công bố thông tin đầy đủ. Vụ TVSI trong khủng hoảng Vạn Thịnh Phát là ví dụ điển hình. Khi đọc doanh thu ngân hàng đầu tư từ bảo lãnh trái phiếu, phải xem cả khoản dự phòng rủi ro tiềm ẩn.

## 5 câu hỏi cho Master agent khi viết tin về ngân hàng đầu tư

1. **Cơ cấu thương vụ là gì?** — Tỷ trọng từ bảo lãnh phát hành cổ phiếu / bảo lãnh trái phiếu doanh nghiệp / tư vấn mua bán sáp nhập? Mỗi loại có rủi ro và biên lợi nhuận khác nhau. Mua bán sáp nhập có biên cao nhất nhưng không thể dự báo.

2. **Thu nhập quý có phải từ 1 thương vụ lớn không?** — Kiểm tra thuyết minh báo cáo tài chính để xem có thương vụ nào đột biến. Nếu có 1 thương vụ chiếm >50% doanh thu ngân hàng đầu tư quý, không được ngoại suy xu hướng.

3. **Thị phần đang dịch chuyển theo hướng nào?** — Công ty chứng khoán thuộc ngân hàng (VPBankS, TCBS, ACBS) đang tăng thị phần ngân hàng đầu tư nhờ năng lực vốn + tệp khách hàng tổ chức. Công ty chứng khoán độc lập (SSI, VCI, HCM, SHS) đang giữ thị phần hay thu hẹp?

4. **Rủi ro bảo lãnh trái phiếu doanh nghiệp là bao nhiêu?** — Công ty chứng khoán có đang bảo lãnh cho tổ chức phát hành nào đang gặp khó về dòng tiền không? Cần tra thêm danh sách trái phiếu doanh nghiệp sắp đáo hạn của tổ chức phát hành liên quan.

5. **Chu kỳ phát hành vốn đang ở giai đoạn nào?** — Thị trường phát hành lần đầu ra công chúng đang mở hay đóng? Tổng phát hành trái phiếu doanh nghiệp quý gần nhất tăng hay giảm? Số liệu này quyết định nền doanh thu ngân hàng đầu tư cả ngành.

## Realtime data fetch guidance (cho Master CK)

Khi viết bài về doanh thu ngân hàng đầu tư quý cụ thể:

- **Doanh thu ngân hàng đầu tư per công ty chứng khoán quarter**: Finpath API `get_income_statement(ticker)` → tìm dòng "Doanh thu nghiệp vụ bảo lãnh phát hành" + "Doanh thu hoạt động tư vấn" (2 dòng tách biệt trong phần thu từ hoạt động môi giới và ngân hàng đầu tư)
- **Tổng phát hành trái phiếu doanh nghiệp toàn ngành quarter**: web_search "tổng giá trị phát hành trái phiếu doanh nghiệp Q[X]/[Y]" hoặc tra báo cáo định kỳ của Hiệp hội Thị trường Trái phiếu Việt Nam (VBMA) tại vbma.org.vn
- **Top thương vụ mua bán sáp nhập + phát hành lần đầu quarter**: web_search "thương vụ M&A lớn Q[X]/[Y] Việt Nam" hoặc "IPO Q[X]/[Y] HOSE" — Diễn đàn Mua bán Sáp nhập Việt Nam thường tổng hợp
- **Rủi ro vỡ nợ tổ chức phát hành có công ty chứng khoán bảo lãnh**: Finpath API `get_news(ticker)` + `get_events(ticker)` + web_search "[tên tổ chức phát hành] vỡ nợ trái phiếu 2026" hoặc "chậm thanh toán trái phiếu 2026"
- **Thị phần ngân hàng đầu tư per công ty chứng khoán**: Không có cơ quan công bố chính thức như thị phần môi giới HOSE. Phải tổng hợp từ BCTC từng công ty hoặc báo cáo phân tích của công ty chứng khoán (TBTC, DNSE Research, BSC Research). web_search "thị phần tư vấn phát hành trái phiếu doanh nghiệp 2026 top công ty chứng khoán"
- **Cấu trúc doanh thu ngân hàng đầu tư chi tiết**: web_search "[TICKER] doanh thu tư vấn bảo lãnh phát hành Q[X]/[Y]" hoặc tra bản cáo bạch và báo cáo thường niên trên website công ty chứng khoán

## Cross-link

- [ck-margin-cycle.md](./ck-margin-cycle.md) — Doanh thu ngân hàng đầu tư biến động mạnh + cho vay ký quỹ ổn định = 2 nguồn thu cân bằng nhau. Công ty chứng khoán phụ thuộc nhiều vào ngân hàng đầu tư (VCI, HCM) có lợi nhuận biến động hơn công ty thiên về cho vay ký quỹ. Khi đọc cơ cấu lợi nhuận, xem tỷ trọng 2 mảng này để phân loại mô hình kinh doanh.
- [ck-brokerage-marketshare.md](./ck-brokerage-marketshare.md) — Công ty chứng khoán mạnh ngân hàng đầu tư thường cũng mạnh khối ngoại và tổ chức (HCM, SSI, VCI). Liên kết qua tệp khách hàng tổ chức — cùng mối quan hệ với quỹ đầu tư, tổ chức tài chính tạo lợi thế cả 2 mảng. Ngược lại công ty chứng khoán thiên bán lẻ (VPS) ít doanh thu ngân hàng đầu tư.
- [ck-proprietary-trading.md](./ck-proprietary-trading.md) — Công ty chứng khoán bảo lãnh trái phiếu doanh nghiệp đôi khi giữ lại một phần trái phiếu trong danh mục tự doanh. Khoản giữ lại này chịu rủi ro vỡ nợ và biến động giá trái phiếu thứ cấp — mảng tự doanh và ngân hàng đầu tư liên kết với nhau qua kênh này.

## Source log

- [thitruongtaichinhtiente.vn — TBTC 22/10/2025](https://thitruongtaichinhtiente.vn) — 9T/2025 doanh thu ngân hàng đầu tư 60 công ty chứng khoán đạt 3.550 tỷ, top 10 chiếm 91,3%, lợi nhuận 3.000 tỷ (+29% so cùng kỳ)
- [baodautu.vn 25/12/2025](https://baodautu.vn) — 9T/2025 doanh thu ngân hàng đầu tư ~3.400-3.550 tỷ; VPBankS dẫn đầu tăng trưởng 943 tỷ (+82%), 10% thị phần tư vấn phát hành trái phiếu doanh nghiệp phi-ngân hàng
- [vietstock.vn 25/3/2025](https://vietstock.vn) — Doanh thu ngân hàng đầu tư 2024 ~3.500 tỷ (~5% tổng doanh thu khối công ty chứng khoán)
- [vietstock.vn 25/12/2025](https://vietstock.vn) — HCM kỳ vọng doanh thu ngân hàng đầu tư 2025 đạt 200-240 tỷ
- [dnse.com.vn 25/12/2025](https://dnse.com.vn) — ABS Research: 3 động lực hồi phục ngân hàng đầu tư 2025 — thị trường trái phiếu doanh nghiệp ấm lại, phát hành lần đầu + chuyển sàn (TCBS niêm yết 10/2025, LPBankS chào bán 8.780 tỷ), mua bán sáp nhập sôi động
- [xaydungchinhsach.chinhphu.vn 16/9/2022](https://xaydungchinhsach.chinhphu.vn) — Nghị định 65/2022/NĐ-CP toàn văn: siết điều kiện phát hành trái phiếu doanh nghiệp riêng lẻ, yêu cầu xếp hạng tín nhiệm, hiệu lực 16/9/2022
- [baochinhphu.vn 5/4/2022](https://baochinhphu.vn) — Hủy 9 đợt phát hành 10.030 tỷ trái phiếu Tân Hoàng Minh: Uỷ ban Chứng khoán Nhà nước hủy do công bố thông tin sai sự thật
- [vneconomy.vn — 2024](https://vneconomy.vn) — Vụ Vạn Thịnh Phát: 25 mã trái phiếu "khống" 30.081 tỷ đồng, 35.824 người bị hại; tác động ngay lập tức đến niềm tin thị trường trái phiếu tháng 10/2022
- [vietstock.vn 2026](https://vietstock.vn) — Thị trường trái phiếu doanh nghiệp 2025: tổng phát hành 644.300 tỷ (+35,5% so 2024); phát hành riêng lẻ chiếm ~91%
- [kinhtevadubao.vn — 2024](https://kinhtevadubao.vn) — Dữ liệu lịch sử phát hành trái phiếu doanh nghiệp 2021-2024: 2021 (605,9 nghìn tỷ), 2022 (337,1 nghìn tỷ), 2023 (296,8 nghìn tỷ), 2024 (437,9 nghìn tỷ)

## Phần suy luận (cần verify)

**1. Tỷ trọng ngân hàng đầu tư trong cơ cấu doanh thu VCI và HCM các năm khủng hoảng 2022**: Notion ghi VCI là "Leader ngành hàng đầu giai đoạn 2018-2022" với các thương vụ mua bán sáp nhập điển hình (Phúc Long-Masan 400 triệu USD, Pizza4Ps, Điện Gia Lai). Tuy nhiên tỷ trọng cụ thể doanh thu ngân hàng đầu tư / tổng doanh thu VCI năm 2022 chưa có xác nhận từ BCTC kiểm toán độc lập. Cơ cấu 2024 (ngân hàng đầu tư ~10%) là ước tính từ báo cáo phân tích, chưa phải số BCTC tách biệt chính thức.

**2. Mức giảm doanh thu ngân hàng đầu tư Q4/2022 của từng công ty chứng khoán**: Kết luận "40-60% so với cùng kỳ 2021" là suy luận từ mức sụp của tổng phát hành trái phiếu doanh nghiệp toàn ngành (-44%) + VN-Index giảm 32,8% cả năm 2022. Số cụ thể per công ty chứng khoán (SSI, VCI, HCM doanh thu ngân hàng đầu tư Q4/2022) chưa được xác nhận từ nguồn thứ nhất — cần Finpath API `get_income_statement` hoặc BCTC chính thức.

**3. Thị phần ngân hàng đầu tư dịch chuyển sang công ty chứng khoán thuộc ngân hàng bền vững trong dài hạn**: Luận điểm hợp lý vì VPBankS (+82% 9T/2025, 10% thị phần trái phiếu phi-ngân hàng), TCBS (niêm yết + tệp khách hàng Techcombank) đang mạnh lên. Nhưng chưa có dữ liệu đầy đủ để xác nhận xu hướng này là cấu trúc dài hạn hay chỉ phản ánh 2-3 thương vụ lớn trong 1 năm cụ thể.
