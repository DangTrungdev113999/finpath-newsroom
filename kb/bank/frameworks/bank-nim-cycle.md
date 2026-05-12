---
category: frameworks
title: "Bank-NIM-cycle"
last_updated: 2026-05-12
---
Framework đọc chu kỳ biên lãi thuần — decision rules cho Master Bank agent. NIM của bank VN đang trong cycle compression dài hạn; cần đọc theo pha lãi suất NHNN + CASA + loan mix.

## Định nghĩa & công thức

**NIM** (Net Interest Margin, biên lãi thuần) = Thu nhập lãi thuần / Tài sản sinh lời bình quân

Trong đó:

- **YEA** (Yield on Earning Assets, lợi suất tài sản sinh lời) = Thu lãi / Tài sản sinh lời
- **COF** (Cost of Funds, chi phí vốn) = Chi lãi / Tổng nguồn vốn huy động
- NIM ≈ YEA - COF (xấp xỉ, sai số do mẫu khác nhau)
**CASA** (Current Account Savings Account, tiền gửi không kỳ hạn) = driver chính ở VN. Lãi suất CASA chỉ 0.1-0.5%/năm → kéo COF xuống mạnh nếu tỷ trọng cao.

## Cách đọc — pha cycle + loan mix

### 1. NIM theo chu kỳ lãi suất NHNN

- **Lãi suất tăng (tightening)**: Loan yield re-price quarterly tăng nhanh, deposit cost tăng chậm hơn (lock kỳ hạn dài) → NIM nở 1-2 quý đầu cycle
- **Lãi suất giảm (easing)**: Ngược lại — loan yield giảm trước, deposit cost giảm chậm → NIM compress
- **Lag effect 1-3 quý** tùy mix kỳ hạn deposit. Bank CASA cao có lag ngắn vì funding ít chịu re-price
## Benchmark dài hạn + ranges (NIM/CASA per bank type)

KHÔNG per-bank per-quarter snapshot. Dùng cho Master sanity-check khi Finpath API trả số realtime.

### NIM range theo bank type (historical 2020-2026)

| Tier | NIM range | Bank typical |
|---|---|---|
| **High** | >4% | Tư nhân consumer-finance heavy (VPB), tư nhân retail-strong (TCB, MBB, VIB) |
| **Mid** | 3-4% | Tư nhân corporate (ACB, STB, HDB) |
| **Low stable** | ~3% | Quốc doanh (VCB, CTG, BID) — cho vay corporate yield thấp do chính sách ngành |

Trend dài hạn 2011-2025: NIM bình quân 27 NH giảm từ 3,88% → 2,93% (secular compression).

### CASA range theo bank type

| Tier | CASA range | Bank typical |
|---|---|---|
| **Top** | 30-37% | MBB, TCB, VCB |
| **Mid** | 18-25% | CTG, ACB, BID, TPB |
| **Low** | <15% | STB, VIB, VPB, HDB, SHB |

**KEY INSIGHT**: CASA cao ≠ NIM cao tự động. Phụ thuộc loan mix (corporate yield thấp vs retail/SME yield cao).

### Loan yield range theo segment

| Segment | Yield range |
|---|---|
| Retail / consumer finance | 12-20%/năm |
| SME | 9-12%/năm |
| Corporate big | 7-9%/năm |
| DNNN / state-led project | 5-7%/năm |

**Decision rule**: NIM expansion thực chất từ shift mix sang retail/SME — KHÔNG phải chỉ repricing chu kỳ.

### 3. NIM trend dài hạn (secular decline)

Bình quân 27 NH niêm yết:

- 2011: 3.88%
- 2022: 3.55% (đỉnh post-COVID)
- 2023: 3.16%
- 2024: 2.88%
- 2025: 2.93%
→ Compression ~0.95 đpt trong 14 năm. Lý do: cạnh tranh, regulation hỗ trợ doanh nghiệp (cap lãi suất cho vay), lãi suất cho vay floor down theo chính sách.

Trend YEA vs COF (2024 → 2025): YEA 7.02% → 7.06% (gần đứng yên), COF 4.12% → 4.35% (tăng). Compression do COF push, không phải YEA collapse.

## Reference points lịch sử VN

- **2020-2021**: NIM ngành cao do COVID + lãi suất NHNN thấp + tín dụng tăng. TCB peak ~5%.
- **Q3/2022**: NIM đỉnh cycle 3.55% bình quân. Trùng đỉnh LLCR ngành (143.2%) — pre-crisis trái phiếu.
- **Q4/2022**: NHNN nâng lãi suất điều hành 1000bp tháng 9-10/2022. Lãi suất huy động 12T peaked 9-10%.
- **2023**: COF nở vọt → NIM ngành giảm về vùng đáy 3.16%.
- **Q1-Q2/2024**: NIM 27 NH niêm yết 3.4-3.43% — đáy 4 quý liên tiếp. VCB Q1/2024: 3.07% (top quốc doanh do shift retail). BID giảm mạnh.
- **2024 cả năm**: Lãi suất huy động 12T quốc doanh 4.68%, tư nhân lớn 4.5-5% (vs 6-8% năm 2023). Lãi suất cho vay bình quân 7.3-9.5% (vs 9.4-11.4% năm 2023) — đầu vào và đầu ra cùng giảm.
- **2025**: Tín dụng toàn ngành tăng 19.01% nhưng NIM bình quân chỉ 2.93%. TCB CASA cuối 2025: 40.4% (số dư 268,700 tỷ).
- **2026 outlook**: Bank tư nhân quy mô lớn (MBB, TCB, VPB, HDB) kỳ vọng phục hồi NIM >4.6%; quốc doanh quanh 2.9-3% (vẫn thấp do nhiệm vụ hỗ trợ kinh tế).
## Gotchas

- **NIM tăng QoQ không hẳn tốt** nếu do shift sang segment rủi ro cao (consumer subprime, BĐS đầu cơ).
- **CASA cao Q4** một phần do dòng tiền cuối năm doanh nghiệp; Q1 thường drop ~1-2 đpt (Q1/2025 toàn ngành 18.48%, giảm 1.4 đpt từ Q4/2024).
- **NIM Q1 thường thấp** do tính daily average + Tết Âm lịch (giao dịch chậm, CASA giảm tạm thời).
- **Bank vay nhiều liên ngân hàng** (TCB, VPB, MSB historical) bị tác động mạnh khi lãi liên ngân hàng tăng — không phản ánh khả năng huy động dân.
- **Bank có công ty con tài chính tiêu dùng** (FE Credit của VPB, MCredit của MBB, HD Saison của HDB) có NIM bị bóp méo lên — nên xem riêng bank standalone.
- **NIM "tốt" của bank quốc doanh quanh 3%** không phải dở — họ cố tình maintain low yield để ổn định ngành. So tuyệt đối với tư nhân là sai pattern.
## Áp dụng khi viết tin

5 câu hỏi cho Master agent:

1. NIM QoQ + YoY: hướng + tốc độ? Đáy hay đỉnh chu kỳ?
1. CASA QoQ: tăng/giảm bao nhiêu đpt? Đang ở top/mid/low tier?
1. YEA và COF tách riêng: ai đẩy NIM hơn (lợi suất hay chi phí vốn)?
1. Loan mix shift retail/SME/corporate? Có shift chưa hay vẫn còn dư địa?
1. Pha NHNN: tăng hay giảm lãi suất → predict NIM 1-2 quý sau (lag).
## Realtime data fetch guidance (cho Master Bank)

Khi viết bài quý cụ thể về NIM/CASA, Master KHÔNG đọc số từ KB. Phải fetch realtime:

- **NIM/CASA/COF/NPL/LDR realtime per bank**: Finpath API `get_bank_ratios(ticker)` — endpoint `/api/stocks/bankfinancialratios/{ticker}` trả NIM/CASA/COF/NPL/LDR/PE/PB/ROE quarterly + yearly.
- **NIM trend nhiều quý**: parse `quarterlyProfits` từ `get_bank_ratios` (trả 8+ quarters).
- **NIM batch nhiều bank cùng lúc**: `get_bank_ratios_batch(['VCB', 'TCB', 'MBB'])` cho competitive comparison.
- **Net interest income breakdown**: `get_net_interest_income(ticker)`.
- **Loan + deposit growth**: `get_deposit_credit(ticker)` — credit growth + deposit composition (CASA breakdown).
- **Lãi suất điều hành NHNN realtime**: web_search "NHNN lãi suất tái cấp vốn [date]" hoặc "lãi suất điều hành NHNN [năm]".
- **CASA peer comparison toàn ngành quarter**: web_search "CASA Q[X]/[Y] toàn ngành" hoặc "top 10 ngân hàng CASA quý [X]".

Pipeline log: `data_trail[].source = "Finpath_API/bankfinancialratios"` hoặc `"WebSearch/<keyword>"`.

## Cross-link

- [bank-npl-reading.md](./bank-npl-reading.md) — NIM compress mạnh có thể che dấu nợ xấu tăng (giảm trích lập để giữ lợi nhuận).
- [bank-target-vs-actual-pattern.md](./bank-target-vs-actual-pattern.md) — Bank đặt target NIM cao hơn historical = pre-bid kỳ vọng repricing thuận lợi → hợp lý hay aggressive?
- [bank-industry-master-reference.md](./bank-industry-master-reference.md) — Lớp 3 chu kỳ lãi suất NHNN ↔ NIM phase analysis.
## Nguồn web đã dùng (search 06/05/2026)

- [DNSE — Lợi nhuận phân hóa 2025](https://www.dnse.com.vn/senses/tin-tuc/loi-nhuan-phan-hoa-ro-net-dau-la-chien-luoc-cua-cac-ngan-hang-trong-nam-2025-35037689) — TCB NIM ~5% → >4%, VCB NIM tiệm cận VietinBank, VPB hoàn thành chỉ 75% kế hoạch 2024, ACB lợi nhuận giảm do NIM
- [Tierra — NIM là gì](https://www.tierra.vn/tin-tuc/nim-la-gi) — công thức NIM, NIM 2024 các bank: VIB 4.9%, MBB 4.5%, EIB 2.5%, KLB cao trong nhóm nhỏ
- [VNBA — NIM Q1/2024](https://vnba.org.vn/vi/xu-huong-nim-cua-he-thong-ngan-hang-quy-1-2024-14402.htm) — VCB Q1/2024 3.07% top quốc doanh, BID giảm mạnh, HDB+TCB tốt nhóm tư nhân DN
- [DNSE — CASA Q1/2025](https://www.dnse.com.vn/senses/tin-tuc/loat-ngan-hang-giam-ty-le-casa-vi-tri-top-dau-goi-ten-mb-techcombank-vietcombank-35046266) — CASA 27 NH Q1/2025 18.48% (giảm 1.4 đpt từ Q4/2024)
- [Saigon Times — NIM Q2/2024](https://thesaigontimes.vn/xu-huong-nim-cua-he-thong-ngan-hang/) — NIM 27 NH niêm yết 3.4% Q1, 3.41% Q2/2024; lãi suất huy động 12T quốc doanh 4.68%, tư nhân lớn 4.5-5%; lãi cho vay 7.3-9.5% (vs 9.4-11.4% 2023)
- [Người Quan Sát — NIM 2025 + CASA Q4/2025](https://nguoiquansat.vn/tin-dung-but-toc-nim-chung-lai-du-dia-bien-lai-sau-2025-con-bao-nhieu-275511.html) — NIM bình quân 27 NH 2011-2025: 3.88% → 2.93%; CASA Q4/2025 12 bank breakdown (MBB 36.83%, TCB 34.48%, VCB 33.72%, BID 21.13%, VPB 13.65%, SHB 7.96%); YEA/COF 2025 7.06%/4.35%
- [Tin nhanh chứng khoán — Áp lực giữ NIM 2026](https://www.tinnhanhchungkhoan.vn/ap-luc-giu-nim-cua-cac-ngan-hang-post384335.html) — TCB CASA cuối 2025 40.4%, số dư 268,700 tỷ; outlook 2026 tư nhân lớn >4.6%, quốc doanh 2.9-3%
- [VietnamBiz — CASA top tier](https://vietnambiz.vn/loat-ngan-hang-giam-ty-le-casa-vi-tri-top-dau-goi-ten-mb-techcombank-vietcombank-202557103547575.htm) — cross-check CASA Q1/2025 với DNSE
- [Techcombank IR — Kết quả 6 tháng 2024](https://techcombank.com/thong-tin/thong-bao/techcombank-cong-bo-ket-qua-kinh-doanh-6-thang-dau-nam-2024) — TCB Q2/2024 NIM 4.6%, COF 3.2%
- [Nhịp Cầu Đầu Tư — Bản đồ lợi thế NH](https://m.nhipcaudautu.vn/tai-chinh/ban-do-loi-the-ngan-hang-3350425/) — historical CASA top (TCB/VCB/MBB), retail mix VIB 87%, ACB 64%
- [Tạp chí Tài chính — NIM theo group Q2/2024](https://tapchitaichinh.vn/nganh-ngan-hang-loi-nhuan-va-ty-le-no-xau-cung-dat-dinh.html) — quốc doanh NIM 2.73% Q2, tư nhân DN 3.96%; CASA cụm quốc doanh 50-60% toàn hệ thống
## Phần suy luận (cần verify)

Các điểm dưới Claude rút từ data + framework chung, không có nguồn VN cite trực tiếp:

- **"Lag effect 1-3 quý" NIM theo lãi suất NHNN** — common bank finance theory (asset-liability management), không nguồn VN cụ thể
- **Loan yield by segment** (retail 12-20% / SME 9-12% / corporate 7-9% / DNNN 5-7%) — approximate ranges từ kiến thức chung, không 1 báo break down như vậy
- **"NIM expansion thực chất từ shift mix sang retail/SME"** — analytical heuristic, không analyst cụ thể
- **"Bank quốc doanh maintain low yield để ổn định ngành"** — common interpretation, không nguồn direct
- **Profile bank theo NIM tier** (high >4% / mid 3-4% / low ~3% quốc doanh) — Claude phân loại từ data historical range, không per-bank Q4/2025 cụ thể
- **"Q1 CASA thường drop do Tết Âm lịch"** — empirical observation, không analyst public lý do này
- **"Bank có công ty con tài chính tiêu dùng bóp NIM lên"** — common interpretation, không analyst quantify
- **5 câu hỏi Master agent** ở section Áp dụng — checklist Claude tổng hợp

