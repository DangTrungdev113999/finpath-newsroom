---
category: frameworks
title: "Bank-NPL-reading"
last_updated: 2026-05-12
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

Hệ thống niêm yết khoảng 2-2.5% (dao động theo chu kỳ), toàn hệ thống cao hơn do nhóm NH kiểm soát đặc biệt. Nhóm quốc doanh thường dưới 1%, nhóm tư nhân tiêu dùng 2-3%.

Decision rule:

- <1.5% = vượt trội (nhóm quốc doanh VCB/BID/CTG + tư nhân lớn quản lý risk tốt)
- 1.5-2.5% = bình thường cho nhóm tư nhân healthy
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

Quá hạn 10-90 ngày → có thể trượt nhóm 3 quý sau. Cuối 2024 toàn ngành: 211.7 nghìn tỷ, 1.25% tín dụng (giảm 7% so cùng kỳ).

Decision rule: nợ nhóm 2 tăng so quý trước trong khi NPL còn flat → 1-2 quý sau NPL sẽ tăng.

### 4. Nợ tái cơ cấu

- **TT 02/2023** (gia hạn TT 06): hết hiệu lực 31/12/2024 → từ 2025 nợ tái cơ cấu phải bộc lộ vào nhóm thật
- **TT 53/2024** cho bão Yagi: tái cơ cấu đến 31/12/2025, đáo hạn cuối 31/12/2026
- Q3/2024: 126.4 nghìn tỷ tái cơ cấu = 0.87% dư nợ hệ thống. Cuối 2024 đa phần dưới 0.5%, VPB còn >1%

Decision rule: bank có nợ tái cơ cấu cao + LLR thấp = rủi ro composite cao.

### NPL formation rate (tốc độ tạo mới)

Q2/2024: 0.16% — quan trọng hơn level tĩnh. Bank có NPL flat nhưng formation rate cao = đang xóa nợ tích cực để giấu.

## Benchmark dài hạn + ranges (NPL + coverage + nợ xấu thật)

KHÔNG per-bank per-quarter snapshot. Dùng cho Master sanity-check khi Finpath API trả số thực tế.

### NPL reported range (historical 2020-2026)

| Tier | NPL reported | Bank typical |
|---|---|---|
| **Low risk** | <1% | Quốc doanh (VCB, BID, CTG) — cho vay corporate được bảo lãnh chính sách |
| **Mid** | 1-2% | Tư nhân lớn quản lý risk tốt (TCB, MBB, ACB) |
| **High** | 2-3% | Tư nhân consumer/SME-heavy (VPB, HDB) — cho vay phân khúc yield cao + risk cao |

### Coverage ratio (LLR — Loan Loss Reserve / NPL) range

| Tier | Coverage ratio | Bank typical |
|---|---|---|
| **Conservative** | >200% | Quốc doanh + tư nhân top conservative (VCB, MBB, ACB) — over-reserved |
| **Adequate** | 100-200% | Tư nhân healthy (TCB, HDB) |
| **Stressed** | <100% | Bank đang stress (VPB FE Credit cycle 2022-2024) |

### Nợ xấu thật vs reported công thức

```
Nợ xấu thật = NPL reported + Nợ tái cơ cấu + Trái phiếu VAMC + TPDN BĐS exposure
```

Ví dụ lịch sử: NPL 1.5% reported + Tái cơ cấu 2.0% + VAMC 0.5% = Nợ xấu thật ~4.0%.

### Threshold cảnh báo

- **Coverage <100%**: bank under-reserved, risk khi NPL spike
- **Nợ xấu thật > 5%**: bank trong stress mode, cần quan sát theo quý
- **NPL spike >50% so cùng kỳ**: bank flag risk lớn (vd VPB FE Credit 2022 spike consumer NPL)

## Reference points lịch sử VN

- **2012**: NPL boom hệ thống >4%. VAMC thành lập, cơ chế trái phiếu đặc biệt "treo" nợ. Tổng nhận đến 2025: ~450,000 tỷ.
- **2015-2016**: Clean-up VAMC bonds; big4 trích lập mạnh.
- **2020-2021**: COVID restructuring qua TT 01/2020 + TT 03/2021 (cho phép giữ nguyên nhóm nợ).
- **Q3/2022**: Tỷ lệ bao phủ đỉnh 143.2% — bank trích đậm phòng rủi ro sau Covid + trái phiếu doanh nghiệp. Đỉnh trùng với pre-crisis trái phiếu.
- **2022-2023**: Khủng hoảng trái phiếu doanh nghiệp (Vạn Thịnh Phát, Tân Hoàng Minh) → NPL bộc lộ trong sector bất động sản, kéo biên lãi vay nén đồng thời.
- **TT 02/2023**: Cho phép cơ cấu lại nợ giữ nhóm; gia hạn TT 06 đến 31/12/2024.
- **2024**: NPL niêm yết quay vùng đỉnh lịch sử 2.21-2.26%, LLR đáy 5 năm 91.4%. Bão Yagi giữa Q3/2024 → TT 53/2024 ra đời.
- **2025**: TT 02 hết hiệu lực. NPL niêm yết Q1/2025 lên khoảng 2.7%.

## Gotchas

- **NPL flat không tốt** nếu bank đang xóa nợ aggressive (write-off) hoặc bán cho VAMC để "ẩn". Check formation rate.
- **LLR cao không = an toàn** nếu cho vay tập trung 1 sector/khách hàng (rủi ro tập trung). VCB exposure vốn đầu tư nước ngoài cao, BID exposure doanh nghiệp nhà nước.
- **Nợ nhóm 2 giảm** không hẳn tốt — có thể chỉ là chuyển nhóm sang tái cơ cấu (ẩn dưới TT 02/53).
- **NPL bank quốc doanh thấp hơn tư nhân**, KHÔNG có nghĩa risk thấp — họ có exposure doanh nghiệp nhà nước với chính sách, mặt khác bank tư nhân nhỏ hay che giấu nợ.
- **Đọc NPL Q4 thận trọng** — bank push xóa nợ và trích lập cuối năm để làm đẹp bảng cân đối.
- **Bank quốc doanh** mặc định LLR cao hơn vì kiểm tra thanh tra ngành ngặt hơn — không tự thân = quản lý tốt hơn.

## Áp dụng khi viết tin

5 câu Master agent tự hỏi trước khi argue về chất lượng tài sản:

1. NPL ratio so quý trước + so cùng kỳ: hướng nào, tốc độ?
1. LLR có giảm khi NPL tăng không? (đệm đang mỏng đi)
1. Nợ nhóm 2 trend? (leading indicator 1-2 quý)
1. Nợ tái cơ cấu (đặc biệt bank dính bất động sản/Yagi) còn bao nhiêu?
1. So peer cùng nhóm (quốc doanh/tư nhân doanh nghiệp/tư nhân cá nhân) — đang ở vùng cao hay thấp ngành?

## Realtime data fetch guidance (cho Master Bank)

Khi viết bài quý cụ thể về NPL, Master KHÔNG đọc số từ KB. Phải fetch thực tế:

- **NPL thực tế per bank**: Finpath API `get_bank_ratios(ticker)` → field NPL trong response.
- **Bad debt detail**: `get_bad_debt(ticker)` — endpoint `/api/stocks/baddebt/{ticker}` — phân nhóm 3-5 + tái cơ cấu + VAMC.
- **Coverage ratio (LLR)**: parse từ `get_bank_ratios` (nếu có) hoặc tính từ `get_balance_sheet` (Loan Loss Reserve / Total NPL).
- **TPDN exposure ẩn**: `get_balance_sheet(ticker)` → "Tài sản tài chính sẵn sàng để bán" hoặc thuyết minh BCTC chi tiết. Web_search bổ sung "[TICKER] TPDN exposure BCTC Q[X]/[Y]".
- **Nợ tái cơ cấu** (TT 02/2023 / TT 53/2024): web_search "[TICKER] nợ tái cơ cấu Q[X]/[Y]" hoặc thuyết minh BCTC.
- **NHNN circular impact recent**: query `data/manual/nhnn_circulars.yaml` first, web_search bổ sung nếu cần.

Pipeline log: `data_trail[].source = "Finpath_API/bankfinancialratios"` / `"Finpath_API/baddebt"` / `"YAML/nhnn_circulars.yaml"` / `"WebSearch/<keyword>"`.

## Cross-link

- [bank-nim-cycle.md](./bank-nim-cycle.md) — Bank biên lãi vay nén mạnh có thể đi đôi với giảm trích lập (chuyển rủi ro sang bảng cân đối) — coverage ratio drop là tín hiệu sớm.
- [bank-target-vs-actual-pattern.md](./bank-target-vs-actual-pattern.md) — Bank đặt target NPL thấp hơn historical → có realistic không? Cần verify với credit growth target.
- [bank-industry-master-reference.md](./bank-industry-master-reference.md) — Lớp 2 đọc số (Tier 1: NPL + coverage), Lớp 6 case study TPDN crisis 2022.

## Nguồn web đã dùng (search 06/05/2026)

- [TBTC VN — Dự báo nợ xấu 2025 (Mirae Asset)](https://thoibaotaichinhvietnam.vn/du-bao-no-xau-nganh-ngan-hang-nam-2025-tang-nhe-truoc-khi-tiep-tuc-xu-huong-giam-171763.html) — LLR ngành 91.4% cuối 2024, phân hóa quyến doanh/tư nhân, nợ nhóm 2 211.7 nghìn tỷ, NPL 4.35% toàn NHTM, loại 5 TCTD KSĐB còn 1.69%
- [Vietstock — Trích lập dự phòng trước giờ G TT 02](https://vietstock.vn/2024/12/cac-ngan-hang-trich-lap-du-phong-ra-sao-khi-thong-tu-02-sap-het-han-757-1251425.htm) — NPL toàn ngành Q3/2024 ~5%, LLR ngành đỉnh 140%+ 2022 → 82% 2024
- [VNBA — LLR cải thiện Q4/2024](https://vnba.org.vn/vi/ty-le-bao-phu-no-xau-cua-cac-ngan-hang-tiep-tuc-cai-thien-16913.htm) — LLR quốc doanh 165.44% cuối 2024, tư nhân DN 76%, cá nhân 62%, NH khác 35.24%; 7/11 NH nhóm khác LLR <50%
- [DDDN — Nợ xấu Q4/2024 (VPBankS)](https://diendandoanhnghiep.vn/no-xau-ngan-hang-ky-vong-giam-nhe-trong-quy-iv-2024-10146547.html) — NPL niêm yết Q3/2024 2.23% loại KSĐB, dư nợ bão Yagi ~165 nghìn tỷ
- [VnBusiness — TT 02 gia hạn (VIS Rating + SSI)](https://vnbusiness.vn/ngan-hang/them-6-thang-de-giam-bot-noi-lo-ve-no-xau-1100546.html) — NPL ngành 2023 đỉnh 5 năm 1.9%, dự báo 2024 1.7-1.8%
- [Dân Việt — Nợ xấu đỉnh 2024](https://danviet.vn/no-xau-ngan-hang-da-dat-dinh-va-se-ha-nhiet-trong-nam-2025-20250103102452585.htm) — NPL Q3/2024 2.3%, tỷ lệ chuyển quá hạn 0.23% Q3/2024 vs trung bình lịch sử 0.5%/quý
- [Tạp chí Tài chính — NPL + LLCR Q2/2024](https://tapchitaichinh.vn/nganh-ngan-hang-loi-nhuan-va-ty-le-no-xau-cung-dat-dinh.html) — formation rate 0.16% Q2/2024, LLCR đỉnh 143.2% Q3/2022, NPL niêm yết 2.21% giữa 2024
- [TBTC VN — Nợ xấu Q1/2025](https://thoibaotaichinhvietnam.vn/no-xau-ngan-hang-gia-tang-ty-le-bao-phu-xuong-muc-day-5-nam-176395-176395.html) — NPL niêm yết quy mô +18.5% so cùng kỳ Q1/2025
- [VNSC — NPL là gì + VAMC](https://www.vnsc.vn/npl-la-gi) — NPL Q1/2025 2.7%, VAMC tổng nhận ~450,000 tỷ

## Phần suy luận (cần verify)

Các điểm dưới Claude rút từ data + framework chung, KHÔNG có 1 nguồn VN đưa rule trực tiếp. User nên review và thay bằng rule có authority hơn nếu có:

- **Decision rule NPL ratio** (<1.5% vượt trội / 1.5-2.5% bình thường / >3% red flag) — Claude phân từ phân bố 27 NH niêm yết 2024-2025, không analyst public rule này
- **Decision rule LLR** (>100% đệm dày / 50-100% vừa đủ / <50% mỏng) — tự rút, common sense
- **"NPL flat không tốt nếu đang xóa nợ aggressive"** — empirical observation, common framework banking analysis nhưng không cite nguồn VN cụ thể
- **"LLR cao không = an toàn nếu rủi ro tập trung"** — common-sense framework, không nguồn direct
- **"Đọc NPL Q4 thận trọng vì bank push xóa nợ cuối năm"** — empirical observation từ pattern Q4 các năm, không analyst public rõ
- **"Bank quốc doanh LLR cao hơn vì thanh tra ngặt hơn"** — common interpretation, không 1 nguồn cụ thể
- **5 câu hỏi Master agent** ở section Áp dụng — checklist Claude tổng hợp, cần review
- **Benchmark range NPL/coverage per tier** (Low risk <1% / Mid 1-2% / High 2-3%; Conservative >200% / Adequate 100-200% / Stressed <100%) — Claude phân loại từ data lịch sử + phân nhóm ngân hàng, không analyst public rule này
