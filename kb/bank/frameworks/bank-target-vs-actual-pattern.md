---
notion_page_id: "358273c7-a9a1-81b9-ae4b-f37b05ec9224"
source_url: "https://www.notion.so/358273c7a9a181b9ae4bf37b05ec9224"
last_synced: 2026-05-08T09:07:07.892727+00:00
category: frameworks
title: "Bank-Target-vs-Actual-pattern"
---
Framework đọc pattern target vs actual — decision rules cho Master Bank agent. Không phải bank nào miss target cũng dở; không phải vượt cũng tốt. Đọc context: bank conservative vs aggressive, NHNN room cycle, reset behavior.

## Định nghĩa & công thức

ĐHCĐ thường niên (tháng 4 hằng năm) ra chỉ tiêu kế hoạch năm:

- Tăng trưởng tín dụng (constrained bởi room NHNN giao đầu năm)
- Tăng trưởng tổng tài sản
- Lợi nhuận trước thuế (LNTT)
- ROE, NIM (một số bank)
- Tỷ lệ nợ xấu trần
**Tỷ lệ hoàn thành** = (Actual cumulative) / (Target năm) × 100%

Track rolling: Q1, H1, 9M, FY.

## Cách đọc — pattern + tracking + reset

### 1. Phân loại bank theo thái độ đặt target

**Conservative** (set thấp → beat ổn định):

- VCB historical thường đặt LNTT growth 5-10%, actual thường vượt 5-15%
- ACB historical 10% growth → actual 10-15% (2024 ACB target +10% LNTT lên 22,000 tỷ + tín dụng 14%)
- BID, CTG quốc doanh — set theo guidance NHNN/Bộ Tài chính, beat nhẹ thường lệ
**Mid-aggressive** (set vừa → swing theo macro):

- MBB 2024: target LNTT 27,884-28,410 tỷ (+6-8%); giai đoạn 2024-2029 plan +12%/năm
- TCB historical aggressive growth assumption nhưng có lúc beat lúc miss
**Aggressive** (set cao → miss rất phổ biến):

- VPB 2024: target tăng trưởng tín dụng +25%, huy động +22% → actual hoàn thành 75% target lợi nhuận → MISS lớn
- BVB 2024: target +2.8x → Q1 đạt 35% target → cảnh báo sớm
### 2. Rule of thumb tracking quý

Dựa trên empirical 2022-2024:

- Q1 cumulative ≥22% target → tracking tốt
- H1 ≥45-50% target → likely beat
- 9M ≥70% target → beat khả năng cao
- 9M <60% target → very likely MISS
**Caveat**: Bank conservative thường skewed Q4 (push tín dụng cuối năm để dùng hết room). 9M <70% chưa đủ kết luận với VCB/ACB.

### 3. Pattern target lợi nhuận 2024 — case study

**Beat rõ:**

- LPB: 12,168 tỷ (+73% YoY), 116% kế hoạch
- TPB: 7,600 tỷ (+36%), vượt
- NamA: 4,545 tỷ (+38%), vượt 13.6% target
- HDB: actual >16,000 tỷ vs target 15,852 tỷ
- CTG: 26,300 tỷ (+8.7%), vượt
- MSB: 6,903 tỷ (+18.4%), vượt 6,800 tỷ target
- VCB: cơ bản hoàn thành 42,000 tỷ target (record toàn ngành)
- SHB, SeABank: vượt
**Miss đáng chú ý:**

- VPB: ~75% kế hoạch — miss lớn do FE Credit lỗ + NIM compression + provisioning cao
### 4. Reset target giữa năm = red flag

Nếu bank điều chỉnh target lợi nhuận GIẢM trong ĐHCĐ bất thường → tín hiệu management thừa nhận miss. **2022 nhiều bank reset sau khi NHNN siết room Q3.**

Reset target LÊN ít gặp ở VN — bank conservative không revise up giữa năm dù dư địa, để Q4 beat surprise.

### 5. NHNN nới room giữa năm — leading indicator beat

NHNN cấp thêm room cho bank đạt >80% chỉ tiêu sau H1. **28/8/2024** NHNN cấp thêm cho:

- TCB 124% chỉ tiêu H1
- ACB 121%
- HDB 119%
→ Cả 3 bank này đều beat target năm 2024 sau đó.

### 6. Target tăng trưởng tín dụng vs ngành

NHNN đặt room ngành: 2024 = 15% (thực tế cuối năm vượt 15%); 2025 = 16%; 2026+ lộ trình bỏ room (Nghị quyết 62/2022/QH15).

- Bank đặt target tín dụng cao hơn room đầu năm = pre-bid kỳ vọng được nâng room (signal management tự tin xếp hạng)
- Bank đặt thấp hơn = signal tự đánh giá xếp hạng thấp hoặc cẩn trọng
## Reference points lịch sử VN

- **2022**: NHNN siết room tín dụng Q3 → nhiều bank reset target giữa năm. Tổng tăng trưởng tín dụng cả năm 14.5% vs target 14%. Nhiều bank quy mô vừa miss.
- **2023**: Miss diện rộng cho target lợi nhuận do NIM compression Q4/2022 + crisis trái phiếu doanh nghiệp + provisioning cao. ĐHCĐ tháng 4/2023 nhiều bank set thấp do trauma 2022 → vẫn miss vì macro xấu hơn dự báo. Khủng hoảng Tân Hoàng Minh + Vạn Thịnh Phát ăn vào credit quality.
- **2024**: NHNN room đầu năm 15% ngành. Tháng 8/2024 nới cho bank top performer. Cả năm tín dụng vượt 15%. ĐHCĐ tháng 4/2024 bank set conservative do trauma 2023 → Q4 nhiều bank beat đẹp (TPB +36%, LPB +73%, NamA +38%). VPB outlier miss vì FE Credit.
- **2025**: NHNN room 16% ngành. Tăng trưởng thực tế 19.01% — vượt mạnh (do nhiều bank được cấp thêm room).
**Pattern stake-out:**

- Bank state-owned (VCB, BID, CTG): conservative target → meet/slight beat thường lệ
- Bank tư nhân top (MBB, TCB, ACB): mid-aggressive → beat khi macro thuận, miss vừa khi xấu
- Bank high-yield/consumer (VPB, SHB legacy): swing lớn nhất, miss nhiều trong down-cycle
## Gotchas

- **Target ĐHCĐ chỉ là sàn floor pháp lý** — management thường có shadow target nội bộ cao hơn để KPI nhân viên. So với guidance từ analyst day là tốt hơn cho expectation thị trường.
- **Vượt target không = quality good** — có thể đẩy tín dụng vào segment rủi ro hoặc xóa nợ aggressive để in lợi nhuận. Cross-check NPL formation rate.
- **Bank state-owned beat target dễ** vì target được set thấp với guidance Bộ Tài chính — không reflect intrinsic performance. Kết hợp xem ROE để fair evaluation.
- **9M cumulative skewed Q4** là pattern thường gặp với bank conservative — chưa đáng lo nếu room còn dư + Q4 historical strong.
- **Reset target xuống** thường công bố rõ qua NQ ĐHCĐ bất thường; **reset lên hiếm** — bank để Q4 beat surprise tự nhiên.
- **Target tín dụng vs target lợi nhuận có thể nghịch chiều**: bank dùng hết room có khi miss profit (do NIM compress); bank không dùng hết room có khi beat profit (do mix tốt).
## Áp dụng khi viết tin

5 câu hỏi cho Master agent:

1. Target ĐHCĐ năm nay vs actual năm trước: bank đang conservative hay aggressive (dựa profile lịch sử)?
1. Tracking rate cumulative đến quý gần nhất: % target hoàn thành? Compare rule of thumb.
1. NHNN có cấp thêm room/giảm room giữa năm không? (28/8 hay tháng tương tự)
1. Có reset target không? Xuống = red flag, lên = hiếm và rất tích cực.
1. So peer cùng nhóm (state-owned/private top/high-yield) — bank đang outperform/underperform pattern thế nào?
## Cross-link

- Master reference (overview 6 lớp): xem [Bank-Industry-Master-Reference](https://www.notion.so/358273c7a9a1817d8ed1c082f51ab351). Page này là deep dive Lớp 6 (tư vấn) về Target vs Actual.
- Target ↔ NPL: trích lập rủi ro tín dụng đột biến cuối năm là nguyên nhân top miss target lợi nhuận. Xem [Bank-NPL-reading](https://www.notion.so/358273c7a9a181f9a3d7c67887064b64).
- Target ↔ NIM: NIM compression làm net interest income hụt → miss target lợi nhuận. VPB 2024 case: 75% target = combo FE Credit lỗ + NIM compress + provisioning. Xem [Bank-NIM-cycle](https://www.notion.so/358273c7a9a18153adddf609f1239daf).
## Nguồn web đã dùng (search 06/05/2026)

- [LSVN — MB ĐHCĐ 2024](https://lsvn.vn/nam-2024-tong-tai-san-mb-du-kien-vuot-moc-1-trieu-ty-dong-1713746499-a142994.html) — MB target 2024 LNTT 27,884-28,410 tỷ (+6-8%), TTS +13%, kế hoạch 2024-2029 LNTT bình quân 12%/năm
- [VNBA — MSB vượt kế hoạch 2024](https://vnba.org.vn/vi/msb-hoan-thanh-vuot-muc-ke-hoach-kinh-doanh-nam-2024-16687.htm) — MSB 6,903 tỷ LNTT (+18.4%) vượt target 6,800 tỷ
- [Tạp chí Ngân hàng — Review tín dụng 2024 + định hướng 2025](https://tapchinganhang.gov.vn/tang-truong-tin-dung-cho-nen-kinh-te-nhin-lai-nam-2024-va-dinh-huong-nam-2025-15279.html) — NHNN room ngành 2024 ~15%, bối cảnh chính sách
- [Báo Đầu Tư — Room 2025 + cán đích lợi nhuận](https://baodautu.vn/ngan-hang-nha-nuoc-cap-room-tin-dung-nam-2025-nhieu-ngan-hang-can-dich-loi-nhuan-d238799.html) — VCB target 2024 42,000 tỷ, CTG actual 26,300 tỷ (+8.7%), HDB target 15,852 tỷ → >16,000 tỷ, NamA 11T 4,100 tỷ vượt target 4,000 tỷ
- [PHS — Kế hoạch lợi nhuận 2024](https://www.phs.vn/tin-tuc/ke-hoach-loi-nhuan-tang-truong-ngan-hang-van-tiep-tuc-gap-kho-trong-nam-2024/6172345) — ACB target 22,000 tỷ (+10%) tín dụng 14%, MB +6-8%, VPB tín dụng +25% huy động +22%, BVB +2.8x và Q1/2024 đạt 35%
- [Mekong ASEAN — Bức tranh lợi nhuận 2024](https://mekongasean.vn/buc-tranh-loi-nhuan-nganh-ngan-hang-nam-2024-dan-he-lo-37697.html) — Agribank 27,567 tỷ, VCB tín dụng +13.7%, CTG +8.7%, LPB 12,168 tỷ (+73%) 116% kế hoạch, TPB 7,600 tỷ (+36%), NamA 4,545 tỷ (+38%) vượt 13.6% target
- [VNBA — Bức tranh lợi nhuận 2024](https://vnba.org.vn/vi/buc-tranh-loi-nhuan-cua-cac-ngan-hang-nam-2024-16773.htm) — SHB vượt kế hoạch 11,543 tỷ, SeABank +31%, tổng trích lập 27 NH 133,193 tỷ (+8% YoY)
- [24hMoney — Nới room 8/2024](https://24hmoney.vn/news/ngan-hang-co-kha-nang-duoc-tang-room-tang-truong-tin-dung-trong-nua-cuoi-nam-2024-c30a2370417.html) — 28/8/2024 NHNN cấp thêm room cho TCB 124% H1, ACB 121%, HDB 119% (đạt >80% target H1)
- [Báo Chính Phủ — Tín dụng 2024 vượt 15%](https://baochinhphu.vn/tang-truong-tin-dung-nam-2024-vuot-15-102250107170736751.htm) — cả năm 2024 tín dụng vượt 15%, room 2025 dự kiến 16%, lộ trình bỏ room theo NQ 62/2022/QH15
## Phần tự suy luận (cần verify)

Các điểm dưới Claude rút từ data + framework chung, không có nguồn VN cite trực tiếp:

- **Phân loại bank conservative/aggressive** (VCB/ACB conservative, MBB/TCB mid-aggressive, VPB/SHB high-yield aggressive) — Claude tổng hợp từ pattern đặt target 2022-2024, không analyst công bố phân loại này
- **Rule of thumb tracking quý** (Q1 ≥22% / H1 ≥45-50% / 9M ≥70% target = beat; 9M <60% = miss) — Claude rút empirical từ pattern 2024 (HDB 9M 79.8% beat, VPB 9M chậm → miss), không analyst public rule cụ thể
- **"Reset target xuống = red flag, reset lên hiếm ở VN"** — common framework, observation
- **"Bank state-owned beat target dễ vì set thấp với guidance Bộ Tài chính"** — common interpretation, không nguồn direct
- **"9M skewed Q4 với bank conservative"** — empirical pattern, không analyst public
- **"Bank đặt target tín dụng cao hơn room đầu năm = pre-bid kỳ vọng được nâng"** — interpretation từ behavior, không confirm direct
- **"Target ĐHCĐ chỉ là sàn; management có shadow target nội bộ"** — common knowledge nhưng không nguồn public confirm
