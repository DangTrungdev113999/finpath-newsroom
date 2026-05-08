---
notion_page_id: "358273c7-a9a1-81f9-a3d7-c67887064b64"
source_url: "https://www.notion.so/358273c7a9a181f9a3d7c67887064b64"
last_synced: 2026-05-08T09:07:07.892226+00:00
category: frameworks
title: "Bank-NPL-reading"
---
Framework đọc nợ xấu ngân hàng — decision rules cho Master Bank agent. KHÔNG đọc NPL đơn lẻ, phải combo 4 chỉ số.

## Định nghĩa & công thức

NPL (Non-Performing Loan, nợ xấu) = nợ nhóm 3-5 theo phân loại NHNN (Thông tư 11/2021, sửa đổi TT 02/2023).

- **Nhóm 1**: Đủ tiêu chuẩn (quá hạn ≤10 ngày)
- **Nhóm 2**: Cần chú ý (10-90 ngày) — KHÔNG phải NPL nhưng là chỉ báo sớm 1-2 quý
- **Nhóm 3**: Dưới chuẩn (90-180 ngày)
- **Nhóm 4**: Nghi ngờ (180-360 ngày)
- **Nhóm 5**: Có khả năng mất vốn (>360 ngày)
**Tỷ lệ NPL** = (Nhóm 3+4+5) / Tổng dư nợ cho vay

**LLR** (Loan Loss Reserve, bao nợ xấu) = Dự phòng rủi ro tín dụng / NPL × 100% — đo "đệm" của bank.

## Cách đọc — combo 4 chỉ số

### 1. NPL ratio

VN cuối 2024: niêm yết ~2.26%, toàn hệ thống 4.55% (loại 5 NH kiểm soát đặc biệt còn 1.69%). Q1/2025 niêm yết 2.7% (lên từ 2.4%).

Decision rule:

- <1.5% = vượt trội (VCB ~1%, TCB ~1.2% Q1/2025)
- 1.5-2.5% = bình thường
- >3% trong nhóm niêm yết = red flag
### 2. LLR (bao nợ xấu)

Đỉnh ngành Q3/2022: 143.2%. Cuối 2024 toàn ngành: 91.4% — đáy 5 năm.

Phân hóa cuối 2024:

- Quốc doanh ~165%
- Tư nhân doanh nghiệp ~76%
- Tư nhân cá nhân ~62%
- NH khác <50% (35.24% cụ thể)
Decision rule:

- LLR >100% = đệm dày (VCB historical >200%)
- 50-100% = vừa đủ
- <50% = mỏng nguy hiểm
### 3. Nợ nhóm 2 — leading indicator

Quá hạn 10-90 ngày → có thể trượt nhóm 3 quý sau. Cuối 2024 toàn ngành: 211.7 nghìn tỷ, 1.25% tín dụng (giảm 7% YoY).

Decision rule: nợ nhóm 2 tăng QoQ trong khi NPL còn flat → 1-2 quý sau NPL sẽ tăng.

### 4. Nợ tái cơ cấu

- **TT 02/2023** (gia hạn TT 06): hết hiệu lực 31/12/2024 → từ 2025 nợ tái cơ cấu phải bộc lộ vào nhóm thật
- **TT 53/2024** cho bão Yagi: tái cơ cấu đến 31/12/2025, đáo hạn cuối 31/12/2026
- Q3/2024: 126.4 nghìn tỷ tái cơ cấu = 0.87% dư nợ hệ thống. Cuối 2024 đa phần dưới 0.5%, **VPB còn >1%**
Decision rule: bank có nợ tái cơ cấu cao + LLR thấp = rủi ro composite cao.

### NPL formation rate (tốc độ tạo mới)

Q2/2024: 0.16% — quan trọng hơn level tĩnh. Bank có NPL flat nhưng formation rate cao = đang xóa nợ tích cực để giấu.

## Reference points lịch sử VN

- **2012**: NPL boom hệ thống >4%. VAMC thành lập, cơ chế trái phiếu đặc biệt "treo" nợ. Tổng nhận đến 2025: ~450,000 tỷ.
- **2015-2016**: Clean-up VAMC bonds; big4 trích lập mạnh.
- **2020-2021**: COVID restructuring qua TT 01/2020 + TT 03/2021 (cho phép giữ nguyên nhóm nợ).
- **Q3/2022**: LLCR đỉnh 143.2% — bank trích đậm phòng rủi ro post-Covid + bond corporate. Đỉnh trùng với pre-crisis trái phiếu.
- **2022-2023**: Khủng hoảng TPDN (Vạn Thịnh Phát, Tân Hoàng Minh) → NPL bộc lộ trong sector BĐS, kéo NIM compression đồng thời.
- **TT 02/2023**: Cho phép cơ cấu lại nợ giữ nhóm; gia hạn TT 06 đến 31/12/2024.
- **2024**: NPL niêm yết quay vùng đỉnh lịch sử 2.21-2.26%, LLR đáy 5 năm 91.4%. Bão Yagi giữa Q3/2024 → TT 53/2024 ra đời.
- **2025**: TT 02 hết hiệu lực. Q1/2025 NPL niêm yết 2.7%. Best NPL: VCB 1%, TCB 1.2%.
## Gotchas

- **NPL flat không tốt** nếu bank đang xóa nợ aggressive (write-off) hoặc bán cho VAMC để "ẩn". Check formation rate.
- **LLR cao không = an toàn** nếu loan tập trung 1 sector/khách hàng (concentration risk). VCB exposure FDI cao, BID exposure DNNN.
- **Nợ nhóm 2 giảm** không hẳn tốt — có thể chỉ là chuyển nhóm sang restructured (ẩn dưới TT 02/53).
- **NPL bank quốc doanh thấp hơn tư nhân**, KHÔNG có nghĩa risk thấp — họ có exposure DNNN với chính sách, mặt khác bank tư nhân nhỏ hay che giấu nợ.
- **Đọc NPL Q4 thận trọng** — bank push xóa nợ và trích lập cuối năm để clean BS.
- **Bank state-owned** mặc định LLR cao hơn vì kiểm tra thanh tra ngành ngặt hơn — không tự thân = quản lý tốt hơn.
## Áp dụng khi viết tin

5 câu Master agent tự hỏi trước khi argue về chất lượng tài sản:

1. NPL ratio QoQ + YoY: hướng nào, tốc độ?
1. LLR có giảm khi NPL tăng không? (đệm đang mỏng đi)
1. Nợ nhóm 2 trend? (leading indicator 1-2 quý)
1. Nợ tái cơ cấu (đặc biệt bank dính BĐS/Yagi) còn bao nhiêu?
1. So peer cùng nhóm (quốc doanh/tư nhân DN/tư nhân cá nhân) — đang ở vùng cao hay thấp ngành?
## Cross-link

- Master reference (overview 6 lớp): xem [Bank-Industry-Master-Reference](https://www.notion.so/358273c7a9a1817d8ed1c082f51ab351). Page này là deep dive Lớp 2 (đọc số) về NPL.
- NPL ↔ NIM: trích lập rủi ro tín dụng ăn vào lợi nhuận → market đôi khi nhầm với NIM compression. Xem [Bank-NIM-cycle](https://www.notion.so/358273c7a9a18153adddf609f1239daf).
- NPL ↔ Target: trích lập đột biến cuối năm là 1 nguyên nhân lớn miss target lợi nhuận. Xem [Bank-Target-vs-Actual-pattern](https://www.notion.so/358273c7a9a181b9ae4bf37b05ec9224).
## Nguồn web đã dùng (search 06/05/2026)

- [TBTC VN — Dự báo nợ xấu 2025 (Mirae Asset)](https://thoibaotaichinhvietnam.vn/du-bao-no-xau-nganh-ngan-hang-nam-2025-tang-nhe-truoc-khi-tiep-tuc-xu-huong-giam-171763.html) — LLR ngành 91.4% cuối 2024, phân hóa quyến doanh/tư nhân, nợ nhóm 2 211.7 nghìn tỷ, NPL 4.35% toàn NHTM, loại 5 TCTD KSĐB còn 1.69%
- [Vietstock — Trích lập dự phòng trước giờ G TT 02](https://vietstock.vn/2024/12/cac-ngan-hang-trich-lap-du-phong-ra-sao-khi-thong-tu-02-sap-het-han-757-1251425.htm) — NPL toàn ngành Q3/2024 ~5%, LLR ngành đỉnh 140%+ 2022 → 82% 2024
- [VNBA — LLR cải thiện Q4/2024](https://vnba.org.vn/vi/ty-le-bao-phu-no-xau-cua-cac-ngan-hang-tiep-tuc-cai-thien-16913.htm) — LLR quốc doanh 165.44% cuối 2024, tư nhân DN 76%, cá nhân 62%, NH khác 35.24%; 7/11 NH nhóm khác LLR <50%
- [DDDN — Nợ xấu Q4/2024 (VPBankS)](https://diendandoanhnghiep.vn/no-xau-ngan-hang-ky-vong-giam-nhe-trong-quy-iv-2024-10146547.html) — NPL niêm yết Q3/2024 2.23% loại KSĐB, dư nợ bão Yagi ~165 nghìn tỷ
- [VnBusiness — TT 02 gia hạn (VIS Rating + SSI)](https://vnbusiness.vn/ngan-hang/them-6-thang-de-giam-bot-noi-lo-ve-no-xau-1100546.html) — NPL ngành 2023 đỉnh 5 năm 1.9%, dự báo 2024 1.7-1.8%
- [Dân Việt — Nợ xấu đỉnh 2024](https://danviet.vn/no-xau-ngan-hang-da-dat-dinh-va-se-ha-nhiet-trong-nam-2025-20250103102452585.htm) — NPL Q3/2024 2.3%, tỷ lệ chuyển quá hạn 0.23% Q3/2024 vs trung bình lịch sử 0.5%/quý
- [Tạp chí Tài chính — NPL + LLCR Q2/2024](https://tapchitaichinh.vn/nganh-ngan-hang-loi-nhuan-va-ty-le-no-xau-cung-dat-dinh.html) — formation rate 0.16% Q2/2024, LLCR đỉnh 143.2% Q3/2022, NPL niêm yết 2.21% giữa 2024
- [TBTC VN — Nợ xấu Q1/2025](https://thoibaotaichinhvietnam.vn/no-xau-ngan-hang-gia-tang-ty-le-bao-phu-xuong-muc-day-5-nam-176395-176395.html) — NPL niêm yết quy mô +18.5% YoY Q1/2025, VCB 1%, TCB 1.2%, VAB 0.7%
- [VNSC — NPL là gì + VAMC](https://www.vnsc.vn/npl-la-gi) — NPL Q1/2025 2.7%, VAMC tổng nhận ~450,000 tỷ
## Phần tự suy luận (cần verify)

Các điểm dưới Claude rút từ data + framework chung, KHÔNG có 1 nguồn VN đưa rule trực tiếp. User nên review và thay bằng rule có authority hơn nếu có:

- **Decision rule NPL ratio** (<1.5% vượt trội / 1.5-2.5% bình thường / >3% red flag) — Claude phân từ phân bố 27 NH niêm yết 2024-2025, không analyst public rule này
- **Decision rule LLR** (>100% đệm dày / 50-100% vừa đủ / <50% mỏng) — tự rút, common sense
- **"NPL flat không tốt nếu đang xóa nợ aggressive"** — empirical observation, common framework banking analysis nhưng không cite nguồn VN cụ thể
- **"LLR cao không = an toàn nếu concentration risk"** — common-sense framework, không nguồn direct
- **"Đọc NPL Q4 thận trọng vì bank push xóa nợ cuối năm"** — empirical observation từ pattern Q4 các năm, không analyst public rõ
- **"Bank state-owned LLR cao hơn vì thanh tra ngặt hơn"** — common interpretation, không 1 nguồn cụ thể
- **5 câu hỏi Master agent** ở section Áp dụng — checklist Claude tổng hợp, cần review
Master agent khi viết tin nên pull data thật từ DB BCTC Quarter Bank trên Notion (không dùng snapshot ở page này).

