---
category: frameworks
title: "CK-Margin-cycle"
last_updated: 2026-05-11
---
Framework đọc chu kỳ cho vay ký quỹ — cơ chế mở rộng/co hẹp theo lãi suất + thanh khoản thị trường. Quyết định yếu tố nào thúc đẩy doanh thu cho 5 mã universe.

## Khái niệm & cơ chế

Cho vay ký quỹ là nguồn thu **ổn định nhất** trong 5 dòng doanh thu công ty CK Việt vì:

- **Lãi suất cho vay 12-14%/năm** (2026 điển hình), biên lãi ~6-8 điểm phần trăm sau khi trừ chi phí vốn vay ngân hàng/phát hành trái phiếu
- Thu định kỳ hàng tháng — không phụ thuộc vào số phiên giao dịch
- Có tài sản đảm bảo (cổ phiếu trong tài khoản khách hàng) → rủi ro tín dụng thấp hơn cho vay thông thường

**Chu kỳ theo thị trường**: Dư nợ mở rộng nhanh khi chỉ số chứng khoán tăng (nhà đầu tư dùng đòn bẩy để mua thêm); ngược lại thu hẹp trong thị trường giảm do (1) nhà đầu tư chủ động trả bớt nợ, (2) giải chấp tự động khi giá cổ phiếu rơi xuống dưới ngưỡng duy trì.

**Chu kỳ theo lãi suất**: Lãi suất liên ngân hàng tăng → chi phí vốn của công ty CK tăng → lãi suất cho vay ký quỹ tăng → một phần nhu cầu đòn bẩy bị triệt tiêu → dư nợ tăng chậm. Ngược lại khi lãi suất giảm → tiền rẻ → dư nợ bùng nổ (giai đoạn 2020-2021 là điển hình).

## 3 hạn mức cứng theo quy định (Quyết định 87/QĐ-UBCK 2017 & Điều 28 TT 121/2020/TT-BTC)

[Nguồn: thuvienphapluat.vn — Quyết định 87/QĐ-UBCK Điều 9; SSC hỏi đáp khoản 3 Điều 28 TT 121]

- **Tổng dư nợ ký quỹ ≤ 200% vốn chủ sở hữu** — trần cứng vĩ mô từng công ty
- Cho 1 khách hàng ≤ **3% vốn chủ** — hạn chế tập trung rủi ro theo khách hàng
- Cho 1 mã chứng khoán ≤ **10% vốn chủ** — hạn chế tập trung rủi ro theo tài sản đảm bảo

Trần 200% là lý do thực chất đằng sau làn sóng tăng vốn 2024-2026 của SSI, VCI, HCM, VND: **muốn mở rộng cho vay ký quỹ thì phải nới vốn chủ trước**. SSI tháng 9/2025 phát hành 415,5 triệu cổ phiếu giá 15.000 đồng, nâng **vốn điều lệ** từ ~20.779 lên ~24.934 tỷ (tổng VCSH cuối Q1/2026 = 38.531 tỷ — bao gồm thặng dư + lợi nhuận giữ lại) với mục đích tường minh là "bổ sung vốn cho vay ký quỹ". HCM trình cổ đông 2026 phát hành thêm ~270 triệu cổ phiếu (huy động ~4.920 tỷ) vì đã chạm trần.

**Lưu ý phân biệt** (bẫy lẫn vốn điều lệ với vốn chủ): Vốn điều lệ = mệnh giá × số cổ phần phát hành (10.000 VND × số cổ phiếu). Vốn chủ sở hữu (VCSH) = vốn điều lệ + thặng dư phát hành + lợi nhuận giữ lại + các quỹ. Trần 200% áp lên **VCSH**, không phải vốn điều lệ. Khi đọc thông cáo "tăng vốn lên X tỷ", phải xác định rõ vốn nào.

## Dữ liệu neo Q1/2026 — 5 mã universe

**Toàn ngành**: Dư nợ cho vay ký quỹ đạt **355 nghìn tỷ đồng** cuối Q1/2026 (không gồm ứng trước tiền bán — nếu gộp đạt ~405 nghìn tỷ), giảm 12% so với đỉnh Q4/2025 (406 nghìn tỷ). Tỷ lệ dư nợ/vốn chủ toàn ngành: **94%** cuối Q1/2026, hạ nhiệt từ mức 116% cuối Q4/2025 — dấu hiệu đòn bẩy đang thu hẹp theo thị trường.

| Mã | Dư nợ ký quỹ (Q1/2026) | Vốn chủ sở hữu | Tỷ lệ / VCSH | Dư địa (còn cách trần 200%) | Ghi chú |
|---|---|---|---|---|---|
| **SSI** | 36.928 tỷ | 38.531 tỷ | ~96% | ~104% | Dư nợ giảm 5% so đầu năm sau tăng vốn |
| **VND** | 12.469 tỷ | 21.448 tỷ | ~58% | ~142% | Dư nợ giảm 8%, còn nhiều dư địa nhất |
| **HCM** | ~28.000 tỷ | ~14.700 tỷ (ước tính) | ~190% | ~10% | Chạm trần — lý do tăng vốn khẩn cấp 4.920 tỷ |
| **VCI** | ~16.600 tỷ | ~14.500 tỷ (ước tính) | ~114% | ~86% | Tổng cho vay (gồm ký quỹ + cho vay khác) |
| **SHS** | ~10.502 tỷ | ~8.500 tỷ (ước tính) | ~124% | ~76% | Tăng 15% so đầu năm, +126% so cùng kỳ |

**Ghi chú**: VCSH của HCM, VCI, SHS là ước tính từ BCTC Q4/2025 và xu hướng Q1/2026 — BCTC kiểm toán Q1/2026 chưa công bố đầy đủ tại thời điểm viết (5/2026). SSI và VND có số chính xác từ BCTC quý đã công bố.

**Quan sát then chốt**: Tỷ lệ dư địa toàn thị trường giảm xuống dưới 50% là dấu hiệu đòn bẩy đã căng — Q2/2021 chạm ~29% thì thị trường lập đỉnh ngay sau. Q2/2025 toàn ngành còn 45,6% dư địa, thấp nhất kể từ Q2/2022. Q1/2026 phục hồi về ~53% nhờ giảm dư nợ + tăng vốn.

## Dữ liệu lịch sử toàn ngành (chu kỳ)

| Thời điểm | Tổng dư nợ ký quỹ | Tỷ lệ dư nợ/VCSH | Ghi chú |
|---|---|---|---|
| Q4/2021 | ~280 nghìn tỷ | 129% | Đỉnh lịch sử — ngay trước khi VN-Index lập đỉnh 1.500 |
| Q4/2022 | ~150 nghìn tỷ | ~70% | Thị trường sụp — nhà đầu tư trả nợ loạt |
| Q1/2025 | 281,8 nghìn tỷ | ~96% | Mở rộng trở lại, VCSH toàn ngành 292,9 nghìn tỷ |
| Q2/2025 | 295,7 nghìn tỷ | ~155% | Còn 45,6% dư địa (tuoitre.vn 26/7/2025) — thấp nhất từ Q2/2022 |
| Q3/2025 | 380 nghìn tỷ | 115% | Kỷ lục giai đoạn 2022-2025; HCM gần cạn |
| Q4/2025 | ~406 nghìn tỷ | 116% | Đỉnh tuyệt đối lịch sử ngành CK |
| Q1/2026 | ~355 nghìn tỷ | 94% | Thu hẹp theo điều chỉnh VN-Index |

**Chu kỳ 2018 — NHNN siết tín dụng chứng khoán**: Khi ngân hàng thắt chặt cho vay với công ty CK, các công ty phải phát hành trái phiếu bổ sung nguồn vốn — chi phí vốn tăng, một phần biên lãi cho vay ký quỹ bị ăn mòn. Thanh khoản thị trường giảm đồng thời do nhà đầu tư bị siết nguồn tiền. Doanh thu cho vay ký quỹ chiếm 30-50% tổng doanh thu một số công ty CK lớn — khi chu kỳ co hẹp, kết quả kinh doanh phân hóa mạnh giữa công ty có vốn chủ dồi dào và công ty phụ thuộc vay ngắn hạn.

**Chu kỳ 2020-2021 — lãi suất thấp + COVID rally**: Lãi suất điều hành NHNN xuống đáy, tín dụng ngân hàng dồi dào → chi phí vốn công ty CK giảm → lãi suất cho vay ký quỹ giảm về 11-12% → dư nợ toàn ngành tăng từ ~100 nghìn tỷ (2019) lên ~280 nghìn tỷ (Q4/2021), gần gấp 3×. Thị trường lập đỉnh 1.500 điểm, tiếp theo là đợt giải chấp mạnh 2022 khi NHNN tăng lãi suất.

## Bẫy khi đọc số cho vay ký quỹ

1. **Dư nợ tăng KHÔNG đồng nghĩa nhà đầu tư lạc quan tăng** — có thể đơn giản vì công ty vừa tăng vốn nên trần cho vay được nới. Phải kết hợp với giá trị giao dịch bình quân phiên mới thấy nhu cầu thật. Ví dụ SSI Q1/2026: dư nợ giảm 5% nhưng doanh thu tăng 67% vì lãi suất cho vay tăng lên 13-14%.

2. **Dư địa lý thuyết ≠ dư địa thực** — công ty còn dư địa về trần 200% nhưng đã phân bổ vốn sang tự doanh, trái phiếu, tài sản khác; hoặc không huy động được vốn với chi phí hợp lý. Thực tế toàn thị trường chưa bao giờ chạm 200% — đỉnh Q4/2021 chỉ đến 129%.

3. **Tỷ lệ dư nợ/VCSH cao KHÔNG đồng nghĩa rủi ro cao** — phải nhìn chất lượng tài sản đảm bảo. Công ty CK lớn (SSI, HCM, VCI) cho vay chủ yếu với cổ phiếu vốn hóa lớn trong danh sách ký quỹ được phép — khác hẳn công ty nhỏ cho vay với cổ phiếu đầu cơ vốn hóa thấp.

4. **Nhầm trần 200% dư nợ ký quỹ / VCSH với trần tổng nợ 5× VCSH trong cùng TT 121/2020** — đây là 2 hạn mức khác nhau, áp dụng cho 2 khoản mục khác nhau. Trần tổng nợ 5× cho phép công ty CK vay từ nhiều nguồn (ngân hàng, phát hành trái phiếu, repo); trần 200% chỉ áp cho riêng khoản dư nợ ký quỹ cho khách hàng.

5. **Lãi suất cho vay ký quỹ không đồng đều giữa công ty** — một số công ty CK cho vay lãi thấp để thúc đẩy thị phần môi giới (VPS giảm lãi suất như chiến lược giành thị phần), số khác giữ lãi cao để tối ưu biên lãi cho vay (HCM 14%/năm). Không so sánh phẳng dư nợ mà bỏ qua lãi suất đi kèm.

## 5 câu hỏi cho Master agent khi viết tin về cho vay ký quỹ

1. **Dư nợ so quý trước và so cùng kỳ**: tăng hay giảm? Do mở rộng kinh doanh hay do vừa tăng vốn nới trần?
2. **Tỷ lệ dư nợ/VCSH**: bao nhiêu %? Còn bao nhiêu dư địa đến 200%? HCM (gần trần) hay VND (còn xa)?
3. **Lãi suất cho vay ký quỹ**: tăng hay giảm so quý trước? Biên lãi có bị ăn mòn bởi chi phí vốn tăng không?
4. **Nguồn vốn**: huy động vốn vay ngân hàng hay phát hành trái phiếu? Chi phí vốn thay đổi thế nào?
5. **Chu kỳ thị trường**: VN-Index đang tăng hay giảm? Giai đoạn nào của chu kỳ đòn bẩy (mở rộng/đỉnh/co hẹp/đáy)?

## Nguồn đã dùng (web research tháng 5/2026)

- [elibook.vn 28/4/2026](https://elibook.vn/2026/04/28/co-phieu-chung-khoan-ssi-hcm-vci-buc-tranh-loi-nhuan-phan-hoa-manh-me-trong-quy-dau-nam-2026.html/) — bức tranh lợi nhuận phân hóa SSI/HCM/VCI Q1/2026; dư nợ toàn ngành 355 nghìn tỷ; tỷ lệ 94% VCSH
- [elibook.vn 20/4/2026](https://elibook.vn/2026/04/20/ssi-du-no-cho-vay-quy-1-giam-5-so-voi-cuoi-nam-2025-nhung-loi-nhuan-tang-truong-manh-44-yoy-dat-con-so-tuyet-doi-cao-nhat-toan-nganh.html/) — SSI Q1/2026: dư nợ 36.928 tỷ (-5%), VCSH 38.531 tỷ, lợi nhuận +44%
- [thoibaotaichinhvietnam.vn](https://thoibaotaichinhvietnam.vn/quy-i2026-shs-ghi-nhan-loi-nhuan-truoc-thue-280-ty-dong-du-no-cho-vay-tang-truong-ky-luc-196077.html) — SHS Q1/2026: dư nợ ~10.502 tỷ (+15% từ đầu năm, +126% so cùng kỳ), kỷ lục lịch sử SHS
- [vietstock.vn 4/2026](https://vietstock.vn/2026/04/chung-khoan-hsc-bao-lai-quy-1-tang-gan-30-du-no-cho-vay-cham-tran-737-1432135.htm) — HCM dư nợ ~28.000 tỷ, chạm trần; lợi nhuận +28%
- [vietnambiz.vn 4/2026](https://vietnambiz.vn/hsc-uoc-tinh-loi-nhuan-quy-i-tang-26-trinh-loat-phuong-an-phat-hanh-gan-500-trieu-co-phieu-20264310195227.htm) — HSC trình phương án tăng vốn 4.920 tỷ bổ sung cho vay ký quỹ
- [thuonghieucongluan.com.vn](https://thuonghieucongluan.com.vn/quy-i-2026-vndirect-tang-truong-loi-nhuan-hon-40-nho-moi-gioi-khoi-sac-a314984.html) — VND Q1/2026: dư nợ ký quỹ 12.469 tỷ (-8%), VCSH 21.448 tỷ, lợi nhuận +42,5%
- [tinnhanhchungkhoan.vn](https://m.tinnhanhchungkhoan.vn/nhieu-cong-ty-chung-khoan-dieu-chinh-lai-suat-margin-len-toi-14nam-post386536.amp) — nhiều công ty CK điều chỉnh lãi suất cho vay ký quỹ lên tới 14%/năm đầu 2026
- [dnse.com.vn](https://www.dnse.com.vn/senses/tin-tuc/tong-du-no-margin-lap-ky-luc-moi-vuot-400000-ty-dong-cuoi-nam-2025-35183485) — tổng dư nợ cho vay ký quỹ Q4/2025 vượt 400.000 tỷ, kỷ lục lịch sử 25 năm thị trường
- [tuoitre.vn 26/7/2025](https://tuoitre.vn/thi-truong-chung-khoan-anh-huong-boi-siet-cho-vay-chung-khoan-715049.htm) — dư địa 45,6% Q2/2025, thấp nhất kể từ Q2/2022
- [vietstock.vn 22/4/2025](https://vietstock.vn) — Q1/2025 toàn ngành 281,8 nghìn tỷ
- [mekongasean.vn 25/4/2026](https://mekongasean.vn/du-no-margin-dat-ky-luc-nhieu-cong-ty-chung-khoan-dang-cang-54569.html) — Q1/2026 dư nợ cho vay ký quỹ tăng chậm, HSC cạn dư địa
- [thuvienphapluat.vn](https://thuvienphapluat.vn/van-ban/Doanh-nghiep/Thong-tu-121-2020-TT-BTC-huong-dan-hoat-dong-cua-cong-ty-chung-khoan-453690.aspx) — Điều 28 TT 121/2020/TT-BTC: trần 200% dư nợ ký quỹ / VCSH
- [ssc.gov.vn](https://ssc.gov.vn/webcenter/portal/ubck/pages_r/l/chitit?dDocName=APPSSCGOVVN1620153615) — SSC hỏi đáp khoản 3 Điều 28 TT 121

**Phần suy luận (cần verify thêm)**:
- VCSH của HCM, VCI, SHS tại Q1/2026 là ước tính từ xu hướng Q4/2025 — BCTC Q1/2026 kiểm toán đầy đủ chưa công bố tại thời điểm viết
- Tác động chu kỳ 2018 NHNN siết tín dụng chứng khoán: kết hợp từ bài báo lịch sử tuoitre.vn + agriseco.com.vn so sánh TT 121 vs TT 210 — không analyst cụ thể nào định lượng chính xác tác động doanh thu
- Lãi suất cho vay ký quỹ 12-14%/năm (2026): xác nhận từ tinnhanhchungkhoan.vn (nhiều công ty lên 14%) và SSI website (13,5%); HCM 14%; VCI 13%
