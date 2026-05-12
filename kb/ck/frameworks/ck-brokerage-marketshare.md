---
category: frameworks
title: "CK-Brokerage-marketshare"
last_updated: 2026-05-12
---

Thị phần môi giới HOSE/HNX là chỉ báo dẫn trước cho doanh thu phí giao dịch và quy mô tệp khách hàng — nhưng cần đọc kết hợp với mức phí trên từng giao dịch, vì áp lực bào mòn phí khiến thị phần cao chưa chắc đi kèm lợi nhuận cao.

## Khái niệm & cơ chế

Thị phần môi giới = phần trăm giá trị giao dịch khớp lệnh qua từng công ty CK so với tổng giá trị giao dịch toàn sàn. HOSE và HNX công bố chính thức mỗi quý, danh sách top 10, không bao gồm giao dịch thoả thuận riêng (thoả thuận thường không qua hệ thống khớp lệnh trung tâm).

**Tại sao là chỉ báo dẫn trước?**

- Thị phần cao → tệp khách hàng lớn → nhu cầu cho vay ký quỹ lớn hơn → đòn bẩy doanh thu margin quý sau. Đây là cơ chế hai tầng: môi giới lôi kéo khách, margin giữ chân khách và sinh lợi nhuận cao hơn.
- Thị phần thay đổi đột biến (±1 điểm phần trăm trở lên) là tín hiệu sớm cho thấy một công ty CK đang thắng hoặc thua trong cuộc đua thu hút khách hàng cá nhân — tác động đến doanh thu sẽ hiện ra 1-2 quý sau.
- Công bố theo quý (không theo tháng) → báo trước nhưng không thể làm tín hiệu ngắn hạn dưới 3 tháng.

**Giới hạn của chỉ số:** Thị phần top 10 HOSE chiếm khoảng 66-68% toàn thị trường; phần còn lại chia cho ~70 công ty CK khác. Không có độc quyền thị phần — ngay VPS dẫn đầu liên tục cũng chỉ chiếm 15-20%.

## Cơ chế cạnh tranh + bào mòn phí

**Quỹ đạo bào mòn phí (2018-2026):**

| Giai đoạn | Mức phí điển hình | Sự kiện |
|---|---|---|
| 2018 | ~0,15-0,20% giá trị giao dịch | Mức phổ biến toàn ngành |
| 2021-2022 | ~0,10-0,15% | Cạnh tranh leo thang, VPS áp phí thấp thu hút khách lẻ |
| 2023 | TCBS triển khai miễn phí giao dịch | Kỷ nguyên "miễn phí hoá" bắt đầu — TCBS 0%; VPS ~0,06% |
| 2024 | DNSE miễn phí trọn đời, MBS tung "miễn phí giao dịch trọn đời" | Nhiều công ty CK học theo |
| 2026 | Phí điển hình khách lẻ trực tuyến: 0,07-0,10%; khách tổ chức: 0,10-0,15% | SSI, VCI, HCM, VND vẫn giữ phí >0% nhưng bị áp lực giảm |

**Cơ chế bù trừ (không phải miễn phí thật sự):** TCBS và DNSE không thu phí môi giới nhưng bù bằng doanh thu lãi cho vay ký quỹ (lãi suất 12-14%/năm). Mô hình: thu hút khách bằng miễn phí → nuôi khách bằng dịch vụ cho vay ký quỹ. TCBS ghi nhận hơn 1.600 tỷ đồng doanh thu lãi cho vay năm 2023 — cao nhất ngành — trong khi thu phí môi giới gần bằng 0.

**Quy tắc đọc:** Thị phần tăng ≠ doanh thu tăng khi bào mòn phí diễn ra mạnh. VPS tăng từ 13% (Q1/2021) lên 20% (Q1/2024) nhưng lợi nhuận mảng môi giới tăng chậm hơn nhiều vì phí trên mỗi giao dịch thấp. SSI giữ thị phần thấp hơn VPS nhưng lợi nhuận cao hơn nhờ phí cao hơn + doanh thu ngân hàng đầu tư + tự doanh.

## Benchmark dài hạn + threshold delta

Số dùng cho Master sanity-check khi web_search realtime data thị phần. Toàn bộ là range historical, KHÔNG per-quarter snapshot.

### Range thị phần Top 10 HOSE (historical 2021-2026)

| Tier | Thị phần range | Đặc điểm |
|---|---|---|
| Top 1-3 | 11-20% mỗi mã | Leader — VPS dominate khách lẻ trực tuyến từ 2021, SSI/TCBS truyền thống |
| Top 4-7 | 5-10% mỗi mã | Competitive segment — VCI/HCM/VND/MBS/MAS |
| Top 8-10 | 3-5% mỗi mã | Niche/cận biên — VPBankS, KIS, FPTS, VCBS |

### Range thị phần Top 10 HNX

- HNX nhỏ hơn HOSE ~10× về thanh khoản → broker top HNX khác top HOSE
- SHS thường top 5-10 HNX (mạnh khối tổ chức + nhà đầu tư khu vực)
- Niche broker chuyên HNX có tỷ trọng tương đối lớn dù tuyệt đối thấp

### Threshold delta thị phần (tín hiệu cho Master)

- **Delta <0,5 điểm phần trăm**: nhiễu — KHÔNG nên viết bài
- **Delta 0,5-1,0 đpt**: tín hiệu yếu — đáng quan sát
- **Delta 1,0-2,0 đpt**: tín hiệu rõ — viết bài về structural shift
- **Delta >2,0 đpt**: tín hiệu mạnh — change of guard hoặc disruption sự kiện

### Range biên phí môi giới (fee compression timeline)

- **2018**: 0,15-0,25% per giao dịch (chuẩn ngành cũ)
- **2021-2023**: 0,10-0,15% retail; 0,05-0,10% tổ chức
- **2024 onwards**: 0,05-0,10% retail; 0,03-0,05% tổ chức (TCBS/DNSE zero-fee disruption)
- **Block trade thoả thuận**: ~0,03-0,05%, riêng broker-tổ chức relationships có thể thấp hơn

### Per-công ty CK structural positioning (KHÔNG per-quarter)

- **VPS**: Leader khách lẻ trực tuyến (mô hình miễn phí giao dịch + biên lợi nhuận từ ký quỹ)
- **SSI**: Truyền thống mạnh full-service, suy giảm thị phần do online disruption
- **TCBS**: Backed bởi Techcombank, mô hình miễn phí giao dịch tận dụng tệp khách ngân hàng
- **VCI**: Mid-tier mạnh IB tổ chức + tăng vốn liên tục mở rộng ký quỹ
- **HCM**: Mạnh khối ngoại + nhà đầu tư tổ chức nước ngoài
- **VND**: Suy giảm sau sự cố hệ thống 2024, đang tái cơ cấu
- **SHS**: Chuyên HNX + mục tiêu top 10 HOSE qua tái cấu trúc
- **MBS / VPBankS / VCBS**: Liên kết ngân hàng mẹ → tệp khách chuyển tự nhiên

## Dữ liệu lịch sử — Thay đổi thứ hạng Top 10 HOSE (2021-2026)

| Mốc thời gian | Sự kiện | Bối cảnh |
|---|---|---|
| **Q1/2021** | VPS lần đầu soán ngôi SSI lên #1 HOSE | Thị phần VPS 13,24%; SSI nhường vị trí sau >10 năm dẫn đầu |
| Q3/2021 | VPS tăng lên 16,5% — gần gấp đôi SSI | Bùng nổ thanh khoản 2021, mô hình phí thấp–khách lẻ của VPS thắng thế |
| Cả năm 2021 | VPS: 16,14% — SSI: 11,05% | Xác lập khoảng cách mới giữa #1 và #2 |
| Q1/2024 | VPS đạt đỉnh **20,29%** — VPS gần chiếm 1/5 toàn thị trường HOSE | SSI và VND xuống thấp nhất nhiều năm (SSI 9,32%; VND 6,01%) |
| Cả năm 2024 | Nhóm **tăng**: TCBS (+0,86 đpt), HCM (+1,09), VCI (+1,61). Nhóm **giảm**: SSI (-1,26), VND (-1,14) | VCI từ #7 lên #5; VND từ #3 xuống #6-7 sau sự cố hệ thống 3/2024 |
| Q1/2025 | VPS tiếp tục #1; SSI hồi phục nhẹ | Chỉnh sửa cục bộ, cấu trúc top 5 chưa thay đổi |
| **Q1/2026** | VPS **15,32%** — SSI **11,14%** — TCBS 8,85% — **VCI vượt HCM** (7,35% vs 7,30%) | VPS tăng +1,04 đpt; SSI giảm -1,36 đpt; VCBS thay Mirae vào top 10 |

**Xu hướng dài hạn (2021→2026):** Phân hoá rõ thành 3 nhóm — (1) **Nhóm tiến**: TCBS, VCI, HCM — mở rộng dần; (2) **Nhóm ổn định**: VPS giữ #1 liên tục; (3) **Nhóm chậm**: SSI, VND — mất dần thị phần dù vẫn top 10.

Các công ty CK có liên kết ngân hàng lớn (TCBS–TCB, VPBankS–VPB, VCBS–VCB, MBS–MB) có lợi thế tăng trưởng thị phần qua tệp khách hàng ngân hàng mẹ chuyển sang — nhóm này đang chiếm hơn 3 suất trong top 10 HOSE.

## Bẫy khi đọc thị phần

1. **Nhầm HOSE với toàn thị trường** — HOSE là sàn cổ phiếu lớn nhất nhưng không bao gồm HNX (cổ phiếu vừa nhỏ + trái phiếu) và UPCoM (công ty chưa niêm yết chính thức). SHS vắng mặt top 10 HOSE nhưng đây là đặc điểm cấu trúc, không phải yếu kém tuyệt đối — SHS theo HNX.

2. **Nhầm thị phần khớp lệnh với giao dịch thoả thuận** — Top 10 HOSE chỉ tính giao dịch khớp lệnh trung tâm. Các lô lớn qua giao dịch thoả thuận riêng ngoài sàn không tính vào đây, dễ thiếu.

3. **Bẫy "thị phần lên ≠ doanh thu lên" khi bào mòn phí mạnh** — VPS dẫn đầu 21 quý liên tiếp nhưng lợi nhuận mảng môi giới thấp hơn SSI vì phí trên giao dịch thấp hơn nhiều. Cần đọc kết hợp: thị phần × phí trung bình × tổng giá trị giao dịch toàn thị trường.

4. **Bẫy "thị phần khách lẻ vs khách tổ chức"** — VPS mạnh ở khách cá nhân (hàng triệu tài khoản, phí siêu thấp). SSI và HCM mạnh ở khối ngoại và quỹ đầu tư (phí cao hơn, giá trị giao dịch mỗi lệnh lớn hơn). Hai mô hình kinh doanh khác biệt dù cùng nằm top 5.

5. **Thị phần bị bóp méo bởi 1-2 phiên giao dịch lớn bất thường** — Phiên kỷ lục 29/7/2025 đạt 71.763 tỷ đồng giá trị giao dịch (cao nhất lịch sử). Công ty CK nào bắt được lệnh lớn trong phiên đó sẽ có thị phần quý đó cao hơn bình thường. Đọc thị phần 1 quý duy nhất dễ bị sai lệch.

6. **Thị phần môi giới không bao gồm tự doanh** — Giao dịch mua bán bằng vốn công ty (tự doanh) không tính vào chỉ số thị phần. VCI và SHS có mảng tự doanh lớn nhưng thị phần môi giới ở mức tương đối — hai chỉ số đo hai điều khác nhau.

## 5 câu hỏi cho Master agent khi viết tin về thị phần

1. **Thay đổi thị phần là bao nhiêu điểm phần trăm?** — Chênh lệch ≥ 1 điểm phần trăm trong 1 quý mới đáng tin là tín hiệu; dưới 0,5 điểm là nhiễu.
2. **Thứ hạng có thay đổi không?** — Vượt qua đối thủ trực tiếp (ví dụ VCI vượt HCM Q1/2026) tạo ra góc nhìn cạnh tranh rõ ràng hơn con số phần trăm thuần tuý.
3. **Mức phí trên mỗi giao dịch của công ty đó là bao nhiêu?** — Nếu chưa rõ, không nên kết luận "thị phần tăng → doanh thu tăng". Cần phân biệt mô hình phí thấp–khối lượng lớn (VPS) vs phí cao–chất lượng khách (SSI, HCM).
4. **Tệp khách chính của công ty CK đó là cá nhân, tổ chức hay khối ngoại?** — Ảnh hưởng đến cách đọc thị phần và tốc độ bào mòn phí. Khách cá nhân dễ chuyển sang nền tảng miễn phí hơn khách tổ chức.
5. **Áp lực cạnh tranh từ đối thủ nào?** — Cần xem công ty CK nào đang tăng thị phần (TCBS, VCI Q1/2026) để xác định ai đang thắng và ai đang mất khách.

## Realtime data fetch guidance (cho Master CK)

Khi viết bài về thị phần công ty CK quarter cụ thể, Master KHÔNG đọc số từ KB. Phải fetch realtime:

- **Top 10 HOSE thị phần quarter X**: web_search "top 10 thị phần HOSE Q[X]/[Y]" hoặc tra trực tiếp website HOSE.vn (công bố mỗi quý)
- **Top 10 HNX thị phần quarter X**: web_search "top 10 thị phần HNX Q[X]/[Y]"
- **Doanh thu môi giới per công ty CK**: Finpath API `get_income_statement(ticker)` — dòng "Doanh thu hoạt động môi giới chứng khoán"
- **Phí môi giới hiện tại per công ty CK**: web_search "[TICKER] biểu phí giao dịch" hoặc website công ty CK
- **Sự kiện thay đổi rank** (broker mới vào top 10, soán ngôi): web_search "[TICKER] thị phần Q[X] HOSE"

## Cross-link

- [ck-margin-cycle.md](./ck-margin-cycle.md) — Thị phần cao + dư nợ ký quỹ cao = lợi nhuận kép; thị phần giảm + bào mòn phí = doanh thu môi giới gãy đôi trong khi doanh thu ký quỹ phụ thuộc vào quy mô tệp khách còn lại.
- [ck-margin-cycle.md](./ck-margin-cycle.md) — Trần 200% dư nợ ký quỹ/vốn chủ sở hữu là ràng buộc cứng: công ty CK muốn mở rộng ký quỹ phục vụ khách hàng thị phần lớn buộc phải tăng vốn trước — giải thích làn sóng phát hành cổ phiếu 2024-2026 của SSI, VCI, HCM.

## Nguồn đã dùng (web research tháng 5/2026)

- **HOSE công bố 6/4/2026** — Top 10 thị phần môi giới Q1/2026 (nguồn gốc)
- [baodautu.vn — 6/4/2026](https://baodautu.vn/thi-phan-moi-gioi-san-hose-nam-2024-vps-giu-ngoi-vuong-ssi-thu-hep-manh-mieng-banh-d239652.html) — Top 10 + phân tích SSI/TCBS giảm, Mirae ra khỏi top 10
- [vietstock.vn — 6/4/2026](https://vietstock.vn/2026/04/thi-phan-moi-gioi-hose-it-xao-tron-trong-quy-1-vcbs-tro-lai-top-10-830-1423379.htm) — Xác nhận VCBS thay Mirae Asset
- [dnse.com.vn — 6/4/2026](https://www.dnse.com.vn/senses/tin-tuc/thi-phan-hose-quy-i2026-vps-vung-ngoi-vuong-va-tang-manh-nhat-vietcap-vuot-mat-hsc-vao-top-4-35212361) — VPS tăng mạnh nhất, VCI vượt HCM
- [cafef.vn — 6/4/2026](https://cafef.vn/thi-phan-moi-gioi-hose-quy-1-2026-vps-lay-lai-phong-do-vietcap-day-hsc-ra-khoi-top-4-18826040612123642.chn) — SSI/TCBS giảm thị phần
- [doanhnghiephoinhap.vn — 4/2026](https://doanhnghiephoinhap.vn/hnx-cong-bo-thi-phan-moi-gioi-quy-i2026-ssi-vuot-vndirect-vietcap-va-fpts-tro-lai-top-10-132093.html) — HNX top 10 Q1/2026
- [vneconomy.vn — 4/4/2025](https://vneconomy.vn/quy-1-2025-chung-khoan-vps-tiep-tuc-dan-dau-top-10-thi-phan-moi-gioi-tren-hose.htm) — Dữ liệu Q1/2025 + lịch sử 2023-2024
- [vnexpress.net — 2021](https://vnexpress.net/vps-chiem-ngoi-dau-thi-phan-moi-gioi-hose-4258283.html) — Lịch sử VPS soán ngôi SSI Q1/2021
- [cafef.vn — Q1/2024](https://cafef.vn/thi-phan-moi-gioi-hose-quy-1-2024-vps-chiem-1-5-ssi-va-vndirect-xuong-thap-nhat-trong-nhieu-nam-188240403182605081.chn) — VPS chiếm 20,29% Q1/2024
- [stockbiz.vn — 5/2026](https://stockbiz.vn/tin-tuc/shs-quy-12026-tong-tai-san-tang-47-doanh-so-moi-gioi-tang-86-so-voi-cung-ky/39577838) — SHS doanh số môi giới tăng 86% Q1/2026
- [dnse.com.vn — phí giao dịch](https://www.dnse.com.vn/senses/tin-tuc/khong-thu-phi-moi-gioi-cong-ty-chung-khoan-van-lai-nghin-ty-33843460) — Mô hình miễn phí giao dịch + lãi ký quỹ
- [cafef.vn — MBS miễn phí giao dịch trọn đời](https://cafef.vn/cuoc-chien-zero-fee-mbs-tung-chinh-sach-mien-phi-giao-dich-tron-doi-188240115152018139.chn) — Cuộc chiến miễn phí giao dịch 2024

## Phần suy luận (cần verify)

- **VCI vượt HCM nhờ tăng vốn 2024 → mở rộng ký quỹ**: Thị phần VCI tăng +0,96 đpt trong Q1/2026 — mức tăng cao thứ 2 top 10. Nguồn Notion note "VCI hoàn tất phát hành riêng lẻ + cổ phiếu thưởng mid-2024 → vốn mới cho ký quỹ → thu hút nhà đầu tư". Cơ chế hợp lý (tăng vốn → tăng dư địa ký quỹ → thu hút khách cần đòn bẩy) nhưng chưa có xác nhận trực tiếp từ BCTC VCI phân tách.
- **VND mất thị phần do sự cố hệ thống 3/2024**: VND giảm từ #3 (2023) xuống #6-7 (2024-2026) — Notion note "sự cố hệ thống 3/2024". Cần xác minh sự cố cụ thể và thời gian gián đoạn thực tế; chưa có nguồn web confirm độc lập.
- **Mô hình liên kết ngân hàng tạo lợi thế thị phần bền vững**: TCBS (TCB), VPBankS (VPB), VCBS (VCB), MBS (MB) đều đang trong top 10. Cơ chế tệp khách hàng chuyển từ ngân hàng mẹ sang công ty CK con là hợp lý. Tuy nhiên VCBS mới vào lại top 10 Q1/2026 (thay Mirae) — cần theo dõi liệu đây là xu hướng bền vững hay chỉ là biến động 1 quý.
- **SHS hướng top 10 HOSE**: Doanh số môi giới SHS tăng 86% Q1/2026 nhưng chủ yếu trên HNX. Mục tiêu top 10 thị phần theo tái cấu trúc toàn diện — khả năng thực hiện phụ thuộc vào vốn mới và nền tảng công nghệ giao dịch.
