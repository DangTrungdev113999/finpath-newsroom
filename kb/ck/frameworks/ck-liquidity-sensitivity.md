---
category: frameworks
title: "CK-Liquidity-sensitivity"
last_updated: 2026-05-12
---

Lợi nhuận công ty chứng khoán Việt có **hệ số nhạy cao** với thanh khoản thị trường — cao hơn hầu hết các ngành khác, kể cả ngân hàng. Đây là chủ đề xuyên suốt vì thanh khoản ảnh hưởng đồng thời cả 4 dòng doanh thu: môi giới, cho vay ký quỹ, ngân hàng đầu tư và tự doanh — nhưng mỗi kênh có độ nhạy, tốc độ và mức độ trễ khác nhau.

## Khái niệm & cơ chế

**Thanh khoản** trong framework này = giá trị giao dịch khớp lệnh bình quân phiên (GTGD bq/phiên) trên HOSE + HNX. Không bao gồm giao dịch thoả thuận và giao dịch phái sinh (hai mảng có cơ chế phí riêng biệt).

4 kênh truyền dẫn từ thanh khoản vào lợi nhuận công ty chứng khoán:

**1. Môi giới** — quan hệ tuyến tính gần như trực tiếp với GTGD bq. Doanh thu = phí % × giá trị giao dịch qua công ty. Thanh khoản toàn thị trường tăng 30% → doanh thu môi giới tăng xấp xỉ 30% (giả định thị phần và phí không đổi). Đây là kênh nhạy nhất và phản ứng ngay trong cùng quý.

**2. Cho vay ký quỹ** — quan hệ có độ trễ 1-2 quý (hiệu ứng trễ). Dư nợ ký quỹ bám theo diễn biến VN-Index hơn là GTGD/phiên: nhà đầu tư vay khi thị trường tăng và trả dần khi thị trường giảm. Thanh khoản giảm 30% → dư nợ ký quỹ giảm chỉ 10-15% sau 1-2 quý (sticky — khách không tất toán ngay). Tốc độ mở rộng nhanh hơn tốc độ co lại.

**3. Ngân hàng đầu tư** — chu kỳ phát hành vốn lồng vào chu kỳ thị trường, có độ trễ 6-12 tháng so với thanh khoản. Doanh nghiệp quyết định phát hành khi thị trường tốt nhưng deal thực sự đóng muộn hơn. Thanh khoản giảm 30% → ngân hàng đầu tư có thể sụp 50%+ nếu rơi vào chu kỳ thị trường vốn đóng băng.

**4. Tự doanh** — định giá theo giá thị trường mỗi quý (tài sản tài chính ghi nhận theo giá thị trường — FVTPL). Lợi nhuận tự doanh không thể dự báo đơn giản từ GTGD bq mà phụ thuộc vào cơ cấu danh mục cụ thể từng công ty: cổ phiếu niêm yết (nhạy VN-Index cao), trái phiếu chính phủ (nhạy lãi suất thấp), hay tài sản tài chính sẵn sàng để bán (không hiện ra kết quả kinh doanh quý).

**Hệ số khuếch đại tổng hợp**: Dữ liệu Q1/2026 cho thấy GTGD bq tăng 39% (từ ~22.000 → ~30.500 tỷ/phiên) nhưng doanh thu toàn khối công ty chứng khoán tăng 62% (từ 19.400 → 31.500 tỷ đồng). Hệ số khuếch đại ~1,6× vì cho vay ký quỹ tích lũy dư nợ (tăng nhanh hơn thanh khoản) và tự doanh ghi nhận lãi định giá theo giá thị trường đồng thời. [Cần verify qua nhiều quý để xác nhận hệ số ổn định].

## Quy định pháp lý + threshold

**HOSE/HNX công bố** — giá trị giao dịch hàng tháng và theo quý, danh sách top 10 thị phần môi giới mỗi quý. Đây là nguồn dữ liệu chính để tính toán GTGD bq/phiên.

**Thông tư 121/2020/TT-BTC — hệ số vốn khả dụng (CAR)** — công ty chứng khoán phải duy trì CAR ≥ 180%. Khi CAR giảm dưới 150% → Uỷ ban Chứng khoán Nhà nước (UBCKNN) yêu cầu kiểm soát đặc biệt. Thanh khoản thị trường giảm → giá cổ phiếu giảm → tài sản tài chính ghi nhận theo giá thị trường giảm → vốn khả dụng giảm → CAR có thể tiệm cận ngưỡng kiểm soát. Cơ chế này tạo ra vòng phản hồi âm: thị trường xấu → công ty chứng khoán phải thu hẹp hoạt động → thanh khoản tiếp tục giảm.

**TT 121/2020 Điều 28 — trần dư nợ ký quỹ**: Tổng dư nợ ký quỹ ≤ 200% vốn chủ sở hữu (VCSH). Khi thanh khoản bùng nổ → nhà đầu tư cần nhiều đòn bẩy hơn → công ty chứng khoán phải tăng vốn để nới trần. Đây là lý do làn sóng tăng vốn 2024-2026 song hành với chu kỳ thanh khoản tăng.

## Benchmark dài hạn (ranges)

Số dùng để Master CK kiểm tra tính hợp lý khi web_search dữ liệu realtime. Toàn bộ là range lịch sử, KHÔNG phải snapshot per-quarter.

### Thanh khoản HOSE lịch sử (GTGD bq/phiên cả năm)

| Giai đoạn | GTGD bq/phiên | Trạng thái thị trường |
|---|---|---|
| 2018 | ~5.380 tỷ | Bùng nổ đầu tiên — VN-Index ~1.200 Q1 |
| 2019 | ~5.000-6.500 tỷ | Ổn định sau đỉnh 2018 |
| 2020 | ~10.231 tỷ | Phục hồi hậu COVID, dòng tiền vào sàn |
| **2021** | **~21.593 tỷ** | **Đỉnh lịch sử cả năm — lợi nhuận CTCK kỷ lục** |
| **2022** | **~17.004 tỷ** | **Giảm 21,24% — VN-Index sụp 32,8%** |
| 2023 | ~15.000-18.000 tỷ | Tích lũy — phục hồi chậm |
| 2024 | ~20.000-25.000 tỷ | Phục hồi rõ — FTSE đề cử nâng hạng |
| 2025 | **23.627 tỷ** bq cả năm, ~30.000+ tỷ Q3 | Bùng nổ — KRX 5/2025, FTSE nâng hạng 10/2025 |
| 2026 (Q1) | ~30.500+ tỷ/tháng 3 | Tiếp tục bùng nổ — GTGD bq bình ổn ở mức cao |

**Phiên kỷ lục**: 29/7/2025 — GTGD 71.763 tỷ/phiên. Đây là chỉ báo mốc "thị trường cuồng nhiệt" — có thể là tín hiệu dẫn cho đỉnh chu kỳ. Chỉ dùng khi đặt trong ngữ cảnh, không lấy làm đại diện cho bình quân phiên thông thường.

### Hệ số nhạy doanh thu theo từng mảng (quy tắc quyết định)

| Mảng | Khi GTGD bq giảm 30% | Độ trễ | Ghi chú |
|---|---|---|---|
| Môi giới | Doanh thu giảm ~30% | Cùng quý | Gần tuyến tính — nhạy nhất |
| Cho vay ký quỹ | Dư nợ giảm 10-15% | 1-2 quý | Hiệu ứng trễ — khách trả dần |
| Ngân hàng đầu tư | Có thể giảm 50%+ | 6-12 tháng | Sụp mạnh khi chu kỳ thị trường vốn đóng |
| Tự doanh | Không thể ước lượng thẳng | Cùng quý (FVTPL) | Phụ thuộc cơ cấu danh mục từng công ty |

### Hệ số nhạy lợi nhuận theo cơ cấu danh mục (structural)

Mức độ nhạy tổng hợp phân hoá theo cơ cấu kinh doanh từng công ty chứng khoán:

| Công ty | Mức nhạy tổng hợp | Nguyên nhân cấu trúc |
|---|---|---|
| **HCM** | Cao nhất | 100% tự doanh theo giá thị trường cổ phiếu → định giá theo giá thị trường toàn bộ |
| **SHS** | Cao | 89% tự doanh theo giá thị trường cổ phiếu diện rộng |
| **VND** | Trung bình-cao | 68% theo giá thị trường đa tài sản, ngân hàng đầu tư nhỏ |
| **SSI** | Trung bình | FVTPL 87% nhưng chủ yếu trái phiếu + chứng chỉ tiền gửi (nhạy lãi suất, không nhạy VN-Index) |
| **VCI** | Thấp ngắn hạn — cao dài hạn | 83% tài sản sẵn sàng để bán → lãi/lỗ không vào kết quả kinh doanh quý; nhưng lãi tiềm ẩn lớn |

Lưu ý: Đây là nhận định cơ cấu dựa trên danh mục tự doanh từng công ty. Hệ số nhạy lợi nhuận số cụ thể (regression 5 năm) chưa được xác nhận chính thức — cần kiểm tra khi viết bài.

## Case study lịch sử + chu kỳ

### 2020-2021 — COVID rally: Thanh khoản gấp 4-5 lần trong 2 năm

Dòng tiền đổ vào thị trường chứng khoán trong bối cảnh lãi suất NHNN giảm xuống đáy và tiêu dùng bị hạn chế vì giãn cách xã hội. GTGD bq HOSE nhảy từ ~6.000 tỷ (2019) → ~10.231 tỷ (2020) → ~21.593 tỷ (2021). Cả 4 mảng cùng bùng nổ: phí môi giới tăng tuyến tính theo GTGD; dư nợ ký quỹ toàn ngành tăng từ ~100 nghìn tỷ lên ~280 nghìn tỷ (gần gấp 3×); ngân hàng đầu tư có thị trường trái phiếu doanh nghiệp kỷ lục ~606.000 tỷ phát hành (2021); tự doanh ghi nhận lãi định giá theo giá thị trường khổng lồ khi VN-Index tiến lên 1.500 điểm. Lợi nhuận toàn khối công ty chứng khoán lập kỷ lục lịch sử.

### 2022 — Sụp đổ kép: Thanh khoản giảm 21% + VN-Index mất 32,8%

GTGD bq HOSE từ 21.593 tỷ (2021) xuống 17.004 tỷ (2022) — giảm 21,24%. Doanh thu môi giới giảm tương ứng. Nghiêm trọng hơn: VN-Index rơi 32,8% kéo theo tự doanh lỗ định giá toàn ngành ~7.664 tỷ đồng (gấp 3 lần cùng kỳ 2021, nhiều công ty báo lỗ mảng này); khủng hoảng Tân Hoàng Minh + Vạn Thịnh Phát đóng băng thị trường trái phiếu doanh nghiệp → ngân hàng đầu tư sụp 40-60% so với 2021. Dư nợ ký quỹ co lại chậm hơn: toàn ngành từ ~280 nghìn tỷ xuống ~150 nghìn tỷ — giảm gần 50% nhưng phần lớn phải qua giải chấp tự động do giá cổ phiếu rơi (không phải khách tự nguyện tất toán).

**Hệ quả bất đối xứng**: Chi phí cố định (lương, hệ thống, chi phí vốn vay ngân hàng) vẫn trả đầy đủ khi doanh thu môi giới sụp quá nửa → lợi nhuận giảm nhanh hơn doanh thu rất nhiều. Mô hình bất đối xứng: giai đoạn bùng nổ lợi nhuận tăng nhanh hơn doanh thu (đòn bẩy hoạt động dương); giai đoạn sụp đổ lợi nhuận mất nhanh hơn doanh thu (đòn bẩy hoạt động âm).

### 2023 — Phục hồi ngầm: Thanh khoản ổn định, không bùng nổ

GTGD bq tăng dần từ ~12.000 → ~18.000 tỷ trong năm. Tâm lý thận trọng sau khủng hoảng 2022. Doanh thu môi giới phục hồi chậm. Dư nợ ký quỹ ổn định ở đáy. Ngân hàng đầu tư rất yếu (tổng phát hành trái phiếu doanh nghiệp chỉ ~297.000 tỷ, bằng đáy 2019). Đây là giai đoạn "tích lũy" — kết quả kinh doanh cải thiện nhẹ nhưng chưa rõ xu hướng tăng trưởng.

### 2024-2026 — Mức mới: Thanh khoản ổn định 20.000-30.000 tỷ+/phiên

GTGD bq toàn thị trường ổn định quanh 20.000-25.000 tỷ năm 2024, tăng tốc lên 23.627 tỷ bq cả năm 2025 (với Q3 bq 30.000+ tỷ). Năm 2026 tiếp tục duy trì 30.000+ tỷ/phiên tháng 3. Hệ thống KRX vận hành 5/2025 cải thiện năng lực xử lý lệnh; FTSE nâng hạng thị trường chứng khoán Việt Nam 10/2025 thu hút dòng vốn ngoại mới. Toàn khối công ty chứng khoán Q1/2026 doanh thu đạt 31.500 tỷ (+62% so cùng kỳ), dẫn đầu SSI (+33% lên 1.593 tỷ lợi nhuận) và VPS (+68% lên 1.547 tỷ).

## Chu kỳ cổ phiếu chứng khoán (bổ sung)

Cổ phiếu chứng khoán là **leading indicator** — tăng/giảm trước VN-Index 2-4 tuần:

```
1. ĐÁY: VNI giảm mạnh, GTGD cạn → cổ phiếu CK tăng TRƯỚC VNI (smart money vào)
2. HỒI PHỤC: GTGD tăng nhanh, margin tăng → cổ phiếu CK tăng mạnh nhất (50-100%)
3. SÔI ĐỘNG: VNI tăng đều → cổ phiếu CK tăng cùng VNI
4. ĐỈNH: GTGD đỉnh, margin kỷ lục → cổ phiếu CK giảm TRƯỚC VNI
```

**Bằng chứng SSI**: Q1/22 đỉnh (VNI 1.500, SSI 48k) → Q4/22 đáy (VNI 870 -42%, SSI 16k -67%) → Q2/23 hồi (VNI 1.100 +26%, SSI 28k +75%)

## Tín hiệu VÀO (cần 2-3/9)

1. NHNN hạ lãi suất
2. GTGD chạm đáy + bắt đầu tăng
3. Margin thấp (NĐT đã trả nợ)
4. TK mở mới tăng
5. VNI phá kháng cự
6. Nâng hạng tiến triển
7. Insider CTCK mua cổ phiếu
8. CTCK mua cổ phiếu quỹ (treasury stock)
9. Khối ngoại đảo chiều mua ròng sau bán ròng kéo dài

## Tín hiệu THOÁT (cần 2-3/7)

1. NHNN tăng lãi suất
2. Margin kỷ lục
3. GTGD bắt đầu giảm
4. TK mở mới đạt đỉnh
5. CTCK tăng vốn ồ ạt
6. Nâng hạng thất bại
7. Insider CTCK bán cổ phiếu

## Bẫy khi đọc số thanh khoản

1. **Nhầm thanh khoản khớp lệnh với giao dịch thoả thuận** — Top 10 HOSE thị phần môi giới chỉ tính giao dịch khớp lệnh trung tâm. Giao dịch thoả thuận (lô lớn giữa tổ chức) không vào chỉ số này và không trực tiếp tạo phí môi giới theo GTGD bq thông thường.

2. **Gộp phái sinh vào thanh khoản cổ phiếu** — Phái sinh (hợp đồng tương lai VN30, quyền chọn) có giá trị giao dịch lớn nhưng cơ chế phí hoàn toàn khác: theo hợp đồng, không theo giá trị danh mục. Thanh khoản phái sinh tăng không làm doanh thu môi giới cổ phiếu tăng theo.

3. **Bỏ sót hiệu ứng trễ của cho vay ký quỹ** — Khi GTGD bq giảm mạnh trong quý, doanh thu môi giới giảm ngay nhưng dư nợ ký quỹ vẫn duy trì một thời gian. Phân tích quý ngắn hạn dễ kết luận sai về mức độ ảnh hưởng tổng hợp đến lợi nhuận.

4. **Bỏ sót hiệu ứng nền** — Phục hồi từ đáy thanh khoản thấp tạo ra tốc độ tăng trưởng ấn tượng về phần trăm nhưng giá trị tuyệt đối vẫn thấp. Q1/2024 doanh thu tăng mạnh vì so với nền thấp 2023, không phải vì quy mô thực sự lớn.

5. **Nhầm thanh khoản tăng → doanh thu tăng tự động** — Bào mòn phí môi giới có thể bù trừ tăng trưởng GTGD. VPS tăng thị phần từ 13% (2021) lên 20% (2024) nhưng lợi nhuận môi giới tăng chậm hơn nhiều vì phí trên mỗi giao dịch liên tục giảm. Cần nhìn cả 3 yếu tố: GTGD bq × thị phần × mức phí.

6. **GTGD bq quý bị bóp méo bởi 1-2 phiên đột biến** — Phiên 29/7/2025 đạt 71.763 tỷ đã đẩy bq quý lên cao bất thường. Số liệu trung vị phiên có ý nghĩa hơn bình quân trong trường hợp phân phối lệch. Khi phân tích phải kiểm tra xem bq quý có bị kéo bởi vài phiên kỷ lục không.

7. **VN-Index tăng không đồng nghĩa thanh khoản tăng** — Năm 2024 VN-Index tăng nhưng GTGD bq nhiều tháng thấp hơn năm 2021, do chỉ số được kéo bởi 1-2 mã vốn hoá lớn (VIC, VHM) mà khối lượng giao dịch hạn chế. Cần nhìn độ rộng — số mã tham gia giao dịch khối lượng cao — để đánh giá sức khoẻ thực của thanh khoản.

## 5 câu hỏi cho Master agent khi viết tin về thanh khoản

1. **GTGD bq/phiên quý này so với cùng kỳ và quý trước là bao nhiêu?** — Phải có số tuyệt đối, không chỉ so sánh tương đối. Nguồn: HOSE công bố tháng hoặc web_search "GTGD bình quân HOSE Q[X]/[Y]".

2. **Mảng nào hưởng lợi nhiều nhất từ chu kỳ thanh khoản hiện tại?** — Giai đoạn đầu tăng: môi giới tăng ngay. Sau 1-2 quý: ký quỹ mới mở rộng rõ. Sau 6-12 tháng: ngân hàng đầu tư mới bùng nổ. Phải định vị đúng vị trí trong chu kỳ.

3. **Cơ cấu danh mục tự doanh của công ty CK đang viết là gì?** — Phần lớn theo giá thị trường cổ phiếu (HCM, SHS) thì thanh khoản/VN-Index biến động tác động trực tiếp. Phần lớn tài sản sẵn sàng để bán (VCI) thì lợi nhuận quý ít bị ảnh hưởng dù thị trường sụp.

4. **Có bào mòn phí môi giới không?** — Nếu công ty CK cùng kỳ giảm phí để cạnh tranh thị phần, doanh thu môi giới có thể tăng chậm hơn GTGD bq rất nhiều. Phải kiểm tra mức phí thực tế song song với số GTGD bq.

5. **Khối ngoại giao dịch chiều nào?** — Khối ngoại bán ròng kỷ lục 139.000 tỷ trong 2025 nhưng VN-Index vẫn tăng 28,7% vì nhà đầu tư nội bù đắp. Công ty CK mạnh khách ngoại (SSI, HCM, VCI) nhận tác động khác với công ty CK thiên khách nội (VPS, SHS). Cùng mức GTGD bq nhưng cơ cấu khách khác nhau → doanh thu khác nhau.

## Realtime data fetch guidance (cho Master CK)

Khi viết bài về chu kỳ thanh khoản hoặc phân tích doanh thu theo thanh khoản:

- **GTGD bq phiên HOSE/HNX theo tháng hoặc quý**: web_search "giá trị giao dịch bình quân HOSE tháng [X]/[Y]" hoặc "thanh khoản HOSE Q[X]/[Y]" — HOSE công bố báo cáo thị trường hàng tháng (có thể tra hsx.vn)
- **Doanh thu môi giới per công ty CK**: Finpath API `get_income_statement(ticker)` → dòng "Doanh thu hoạt động môi giới chứng khoán"
- **Dư nợ ký quỹ per công ty CK**: Finpath API `get_balance_sheet(ticker)` → dòng "Cho vay" hoặc "Tài sản tài chính ghi nhận theo giá thị trường (ký quỹ)"
- **Tổng doanh thu toàn ngành theo quý**: web_search "doanh thu ngành chứng khoán Q[X]/[Y] tỷ đồng" — Stockbiz, Vietstock thường tổng hợp
- **Phiên kỷ lục và đột biến thanh khoản**: web_search "phiên kỷ lục thanh khoản HOSE [năm]" — hữu ích để phát hiện sự kiện "thị trường cuồng nhiệt"
- **So sánh GTGD bq toàn thị trường (HOSE + HNX + UPCoM)**: tapchinganhang.gov.vn, vietnambiz.vn thường tổng hợp số liệu toàn thị trường; HOSE.vn chỉ là sàn cổ phiếu chính

## Cross-link

- [ck-brokerage-marketshare.md](./ck-brokerage-marketshare.md) — Thanh khoản giảm 30% → doanh thu môi giới giảm ~30% (tuyến tính). Kênh nhạy nhất, phản ứng ngay trong cùng quý. Bào mòn phí có thể làm thực tế khác với mức tuyến tính lý thuyết — phải đọc kết hợp thị phần × phí × GTGD bq.

- [ck-margin-cycle.md](./ck-margin-cycle.md) — Thanh khoản giảm 30% → dư nợ ký quỹ giảm 10-15% với độ trễ 1-2 quý (hiệu ứng trễ — sticky). Chu kỳ thanh khoản và chu kỳ ký quỹ tách biệt nhau: ký quỹ co lại chậm hơn khi thị trường xấu nhưng cũng mở rộng chậm hơn khi thị trường phục hồi.

- [ck-ib-revenue-volatility.md](./ck-ib-revenue-volatility.md) — Thanh khoản giảm 30% → ngân hàng đầu tư có thể sụp 50%+ khi chu kỳ thị trường vốn đóng (độ trễ 6-12 tháng). Không kỳ vọng ngân hàng đầu tư bùng nổ trùng với đỉnh VN-Index — deal closure phải chờ sau khi thị trường ổn định.

- [ck-proprietary-trading.md](./ck-proprietary-trading.md) — Thanh khoản biến động → VN-Index biến động → tự doanh định giá theo giá thị trường biến động theo. Mức độ tác động phụ thuộc cơ cấu danh mục: HCM (100% theo giá thị trường cổ phiếu) = nhạy nhất; VCI (83% tài sản sẵn sàng để bán) = ổn định hơn trong ngắn hạn nhưng ẩn lãi/lỗ tiềm năng lớn.

## Nguồn đã dùng (web research tháng 5/2026)

- [thitruongtaichinhtiente.vn](https://thitruongtaichinhtiente.vn/nam-2021-gia-tri-giao-dich-binh-quan-phien-tren-hose-dat-hon-21-593-ty-dong-38662.html) — GTGD bq phiên HOSE 2021 = 21.593 tỷ đồng/phiên; tăng 2,6 lần năm 2020 → 2020 ≈ 10.231 tỷ
- [kinhtevadubao.vn](https://kinhtevadubao.vn/thanh-khoan-thi-truong-co-phieu-san-hose-trong-nam-2022-giam-2124-ve-gia-tri-25005.html) — GTGD bq HOSE 2022 = 17.004 tỷ/phiên (-21,24% so 2021); khối lượng bq 653,96 triệu cổ phiếu/phiên
- [tapchinganhang.gov.vn 28/2/2026](http://tapchinganhang.gov.vn/) — TTCK 2025 tổng quan: thanh khoản toàn thị trường 23.627 tỷ bq/phiên cả năm; phiên kỷ lục 29/7/2025 = 71.763 tỷ
- [vietnambiz.vn 31/12/2025](http://vietnambiz.vn/) — VN-Index 1.784 đóng cửa năm 2025; khối ngoại bán ròng 139.000 tỷ trong năm
- [vietstock.vn 5/2026](https://vietstock.vn/2026/05/thi-truong-chung-khoan-hose-thang-42026-chi-so-tang-manh-thanh-khoan-ha-nhiet-830-1439192.htm) — Tháng 4/2026 GTGD bq HOSE ~24.101 tỷ/phiên; tháng 3/2026 khoảng 30.500+ tỷ
- [vneconomy.vn 2026](https://vneconomy.vn/thanh-khoan-se-bung-no-trong-nam-2026-trung-binh-hon-36000-ty-moi-phien.htm) — Dự báo GTGD bq toàn thị trường 2026 khoảng 36.000 tỷ/phiên (+28% so 2025)
- [stockbiz.vn](http://stockbiz.vn/) — Q1/2026 doanh thu toàn khối công ty CK = 31.500 tỷ (+62% so cùng kỳ); môi giới tăng 82%
- [mekongasean.vn 4/2026](https://mekongasean.vn/nganh-chung-khoan-quy-12026-ngoi-vuong-loi-nhuan-doi-chu-nhieu-cong-ty-bao-lo-54738.html) — SSI dẫn đầu lợi nhuận Q1/2026 = 1.593 tỷ (+33%); VPS = 1.547 tỷ (+68%); tổng 40 công ty CK lớn ~7.500 tỷ lợi nhuận (+21% cùng kỳ)
- [kinhtevadubao.vn 23/5/2024](http://kinhtevadubao.vn/) — Chu kỳ 2023 phục hồi chậm; lịch sử HOSE 2018 bq ~5.380 tỷ/phiên
- [vietnamindex.vn 2022](https://vietnamindex.vn/nhieu-cong-ty-chung-khoan-bao-lo-hang-chuc-ty-mang-tu-doanh-a158105.html) — 2022 tự doanh toàn ngành lỗ: định giá lại theo giá thị trường âm ~7.664 tỷ (gấp 3 lần 2021); Q4/2022 lợi nhuận tự doanh giảm 94% so cùng kỳ

## Phần suy luận (cần verify)

**1. Hệ số khuếch đại ~1,6× (doanh thu CTCK tăng 62% khi GTGD bq tăng 39%)**: Suy luận từ Q1/2026 so với Q1/2025. Cơ chế hợp lý — cho vay ký quỹ tích lũy dư nợ tăng nhanh hơn GTGD bq và tự doanh ghi nhận lãi định giá theo giá thị trường đồng thời. Cần kiểm tra qua ít nhất 4-6 quý khác để xác nhận hệ số ổn định.

**2. GTGD bq HOSE 2021 "đỉnh quý" vs "bình quân cả năm"**: Số 21.593 tỷ là bình quân cả năm 2021 (confirmed). Đỉnh quý (Q3-Q4/2021) có thể cao hơn 25.000-30.000 tỷ/phiên — phù hợp với bảng Notion (ghi "25-30k+"). Task brief ghi "peak Q4/2021: 35.000-40.000 tỷ" có thể là số HOSE+HNX+UPCoM cộng gộp, hoặc phiên đỉnh cục bộ — cần xác minh thêm.

**3. Hệ số nhạy lợi nhuận per-ticker (HCM cao nhất, VCI thấp nhất ngắn hạn)**: Suy luận từ cơ cấu danh mục tự doanh (đã xác nhận Q4/2025 và Q1-Q2/2025 từ nhiều nguồn). Hệ số beta số cụ thể (regression 5 năm doanh thu từng CTCK vs GTGD bq HOSE) chưa có nguồn xác nhận độc lập — cần Finpath API `get_income_statement` nhiều quý + regression thủ công.

**4. Chu kỳ ngân hàng đầu tư lag 6-12 tháng**: Suy luận từ Notion và đặc tính vận hành thực tế (pipeline deal cần thời gian để đóng). Số cụ thể "lag 6-12 tháng" chưa được xác nhận bằng regression — đây là ước tính thực tiễn dựa trên quan sát chu kỳ 2021-2022.
