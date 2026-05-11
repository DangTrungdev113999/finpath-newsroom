---
category: frameworks
title: "Bank-Industry-Master-Reference"
last_updated: 2026-05-11
---
Master reference cho Master Bank — mental model 6 lớp phân tích ngành ngân hàng VN. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **VCB · TCB · MBB · ACB · BID · CTG · VPB**. Ba deep dive (NIM-cycle, NPL-reading, Target-vs-Actual) mang chi tiết cơ chế và số liệu lịch sử; master reference này gom 6 lớp vào một chỗ để orient nhanh.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-11 | v2.0 — Refactor to pure static (parity CK v1.2). Điền đầy đủ Lớp 4-6 (skeletal trong Notion source). Strip Notion frontmatter. Add Hướng dẫn tra dữ liệu thời gian thực. |
| 2026-05-08 | v1.1 — Bootstrap từ Notion (bank-industry-master-reference). Thêm NHNN deep dive, TPDN sub-section, changelog. |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Mô hình kinh doanh

Ngân hàng Việt Nam sinh lợi nhuận từ hai nguồn chính:

- **Thu nhập lãi thuần (70-80%):** Huy động (lãi suất thấp) → Cho vay (lãi suất cao) → Chênh lệch = NIM × Tài sản sinh lời
- **Thu nhập ngoài lãi (20-30%):** Phí dịch vụ (chuyển tiền, bảo lãnh), bancassurance, kinh doanh ngoại tệ/trái phiếu, ngân hàng số

Driver ngắn hạn là chu kỳ lãi suất (NHNN). Driver dài hạn là tăng trưởng tín dụng + tái cấu trúc danh mục (retail/SME cao hơn corporate lớn).

## 1.2 Phân loại ngân hàng (structural — không per-quarter)

### Nhóm quốc doanh (Big 4)

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| VCB | Vietcombank | Quản trị rủi ro tốt nhất quốc doanh; thị phần ngoại hối + thanh toán quốc tế lớn nhất; NIM thấp nhưng chất lượng tài sản cao |
| BID | BIDV | Cho vay doanh nghiệp nhà nước + dự án hạ tầng lớn nhất ngành; NIM thấp nhất nhóm; TPDN exposure cao hơn VCB |
| CTG | VietinBank | Cân bằng corporate + SME; cho vay doanh nghiệp sản xuất + xuất khẩu; hưởng lợi chu kỳ công nghiệp |
| MBB | MB Bank | Kỹ thuật số hàng đầu quốc doanh; CASA cao nhất nhóm (≈ top tier tư nhân); hệ sinh thái MCredit + MB Ageas |

### Nhóm tư nhân lớn

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| TCB | Techcombank | Retail-banking + hệ sinh thái BĐS/Masan; CASA cao cấu trúc; NIM trên 4% khi NIM ngành ≈ 3% |
| ACB | ACB | Bảo thủ nhất nhóm tư nhân; SME + khách hàng cá nhân; NPL thấp nhất tư nhân lớn; ít exposure BĐS |
| VPB | VPB | Consumer-finance heavy qua FE Credit; NIM cao nhất nhóm nhưng NPL cao hơn tương ứng; chu kỳ tiêu dùng ảnh hưởng trực tiếp |

> **Decision rule phân loại**: Quốc doanh = nhiệm vụ chính sách → NIM thấp hơn, coverage cao hơn, credit growth do NHNN/Chính phủ drive. Tư nhân = market-driven → NIM cao hơn nhưng NPL cycle rõ hơn, cần phân tích chất lượng danh mục kỹ hơn.

## 1.3 NHNN kiểm soát

- **Room tín dụng:** NHNN cấp hạn mức tăng trưởng tín dụng đầu năm cho từng ngân hàng (dựa trên TT 52/2018 xếp hạng × hệ số chung). NH điểm cao → room cao hơn bình quân ngành.
- **Lãi suất điều hành:** Lãi suất tái cấp vốn, OMO, trần lãi suất huy động <6 tháng — công cụ kiểm soát COF ngành.
- **Quy định trích lập:** TT 11/2021 (phân loại nợ nhóm 1-5), TT 02/2023 (tái cơ cấu giữ nhóm — đã hết hiệu lực 31/12/2024), TT 53/2024 (bão Yagi — đến 31/12/2025).
- **Vốn an toàn:** Basel II áp dụng toàn hệ thống; Basel III đang triển khai (yêu cầu vốn cao hơn, ảnh hưởng dài hạn ROE).

> **Nguyên tắc cốt lõi**: Phân tích ngân hàng mà không phân tích NHNN = thiếu 50% bức tranh.

## 1.3.bis NHNN deep dive

**Room tín dụng**: NH điểm cao → room cao hơn bình quân. Historical: 2024 ~15%, 2025 ~16% (thực hiện 19.01%). Nới room giữa năm khi NH đạt >80% chỉ tiêu H1 (case 28/8/2024: TCB, ACB, HDB). Bank đặt target cao hơn room = pre-bid kỳ vọng được nâng.

**Lãi suất điều hành**: Cycle 2022-2025 — NHNN nâng mạnh 9-10/2022 → lãi huy động 12 tháng peak 9-10%; giảm dần 2023-2024. Lãi suất điều hành đảo chiều → NIM lag 1-3 quý (xem deep dive NIM-cycle).

**Prudential**: TT 11/2021 (phân loại nợ nhóm 1-5); TT 02/2023 (tái cơ cấu giữ nhóm — hết hiệu lực 31/12/2024, từ 2025 nợ tái cơ cấu bộc lộ nhóm thật); TT 53/2024 (bão Yagi — đến 31/12/2025).

## 1.4 Cấu trúc thu nhập — vai trò từng mảng

| Mảng | Tỷ trọng điển hình | Nhạy với |
|---|---|---|
| Thu nhập lãi thuần | 70-80% | Chu kỳ lãi suất NHNN, CASA, loan mix |
| Phí dịch vụ | 10-15% | Tăng trưởng giao dịch, bancassurance (rủi ro complaint) |
| Kinh doanh ngoại tệ + trái phiếu | 5-10% | Tỷ giá, biến động lãi suất thị trường |
| Ngân hàng số + khác | 1-5% | Hệ sinh thái, cross-selling |

## 1.5 Đặc thù thị trường Việt Nam

- ~30 NH niêm yết, top 10 chiếm >70% tổng tài sản
- Cho vay bất động sản ~20-25% dư nợ toàn ngành → bất động sản đóng băng = 1/4 danh mục rủi ro
- Bancassurance bùng nổ 2020-2023, giai đoạn 2023-2024 nhiều khiếu nại → rủi ro phí giảm
- Mobile banking phát triển nhanh nhất Đông Nam Á
- Basel II đã áp dụng toàn hệ thống; Basel III đang triển khai

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics quan trọng

**Tier 1 — Thị trường phản ứng ngay**: NIM (biên lãi thuần, >4% tư nhân cao / ~3% quốc doanh), tăng trưởng tín dụng vs room NHNN (>80% H1 = on track nới mid-year), NPL (<1% tốt / >2% theo dõi chặt), Coverage ratio (>200% bảo thủ / <100% stress), LNTT % kế hoạch năm (Q1 22-28% on-track).

**Tier 2 — Phản ứng 1-3 quý**: CASA trend QoQ (Q1 thường giảm 1-2 đpt do Tết Âm lịch — seasonal), COF lag lãi suất điều hành 1-2 quý, CIR, NFI (bancassurance + phí + trading).

**Tier 3 — Dài hạn**: ROE (>15% tốt), CAR (≥8% Basel II; ≥10-12% Basel III), LDR (<85% tốt thanh khoản), P/B (đáy ~0.8-1.0x; trung bình 1.3-1.8x; đỉnh 2.5-3.0x).

## 2.2 Nợ xấu "thật" vs báo cáo

```
Nợ xấu thật = NPL báo cáo + Nợ tái cơ cấu + Trái phiếu VAMC + TPDN BĐS ẩn

Ví dụ lịch sử: NPL 1.5% + Tái cơ cấu 2.0% + VAMC 0.5% = Nợ xấu thật ~4.0%
```

→ Master PHẢI tính nợ xấu thật, KHÔNG chỉ nhìn NPL báo cáo.

Deep dive: xem [`bank-npl-reading.md`](./bank-npl-reading.md).

## 2.3 Bẫy BCTC ngân hàng

- **Tổng tài sản ≠ dư nợ cho vay**: dư nợ thường chỉ 50-65% tổng tài sản; phần còn lại là tiền gửi NHNN, chứng khoán đầu tư, tài sản cố định.
- **Vốn điều lệ ≠ vốn chủ sở hữu**: vốn chủ sở hữu = vốn điều lệ + lợi nhuận giữ lại + các quỹ. Dùng vốn chủ để tính ROE, không dùng vốn điều lệ.
- **NIM giảm ≠ xấu tuyệt đối**: bank quốc doanh cố tình giữ NIM thấp để hỗ trợ doanh nghiệp nhà nước. So sánh NIM chỉ có nghĩa trong cùng nhóm (quốc doanh vs quốc doanh, tư nhân vs tư nhân).
- **Dự phòng giảm mạnh QoQ**: có thể do bank đã write-off hoặc do bank giảm trích để "bơm" lợi nhuận. Kiểm tra coverage ratio — nếu coverage giảm khi NPL tăng = báo động đỏ.

## 2.3.bis Trái phiếu doanh nghiệp ngân hàng nắm giữ

Khủng hoảng Vạn Thịnh Phát (10/2022) + Tân Hoàng Minh (4/2022) cho thấy TPDN bất động sản ngân hàng nắm giữ là rủi ro lớn không kém NPL truyền thống.

### Cách đọc từ BCTC

- Khoản mục **"Chứng khoán đầu tư sẵn sàng để bán"** + **"Trái phiếu doanh nghiệp"** → identify exposure tuyệt đối
- Tỷ trọng TPDN / vốn chủ sở hữu → mức độ nguy hiểm
- Thuyết minh BCTC: TPDN phân theo ngành (bất động sản là nhóm rủi ro nhất), kỳ hạn, mức độ rủi ro

### Decision rule

- TPDN bất động sản / vốn chủ cao + LLR thấp = composite risk
- TPDN đáo hạn trong 6-12 tháng = pressure point
- 2026 có áp lực đáo hạn TPDN tăng nửa đầu năm — watchpoint

## 2.4 Checklist BCTC (7 câu hỏi)

1. NIM tăng/giảm QoQ/YoY? Từ đâu — YEA hay COF?
2. Tín dụng tăng bao nhiêu? Còn bao nhiêu room so với chỉ tiêu NHNN?
3. Nợ xấu THẬT = NPL + tái cơ cấu + VAMC + TPDN? Coverage đủ không?
4. Dự phòng tăng/giảm? Coverage ratio trend nào?
5. NFI ra sao? Bancassurance contribute bao nhiêu?
6. CIR tăng/giảm? Chi phí được kiểm soát tốt không?
7. Vĩ mô: lãi suất NHNN, room tín dụng, bất động sản, TPDN đáo hạn?

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Nguyên tắc cốt lõi

```
Cổ phiếu ngân hàng gắn CHẶT với chu kỳ lãi suất:
- NHNN hạ lãi suất → kỳ vọng NIM tăng + tín dụng tăng → giá CK tăng
- NHNN nâng lãi suất → kỳ vọng NIM bị nén + tín dụng chậm → giá CK giảm

Giá cổ phiếu chạy TRƯỚC số liệu BCTC:
- Tăng khi NHNN mới hạ (dù BCTC vẫn xấu — lag 1-3 quý)
- Giảm khi NHNN mới tăng (dù BCTC vẫn tốt)
```

## 3.2 Chu kỳ lãi suất ↔ ngân hàng

**Lãi suất giảm (nới lỏng):**

- Chi phí huy động giảm trước → NIM nở tạm 1-2 quý đầu
- Tín dụng tăng, bất động sản hồi phục → nợ xấu giảm
- Giá cổ phiếu: TĂNG MẠNH giai đoạn early-cycle
- Sau 2-3 quý: lãi suất cho vay cũng giảm → NIM bị nén lại

**Lãi suất tăng (thắt chặt):**

- Chi phí huy động tăng trước → NIM bị nén tạm
- Tín dụng chậm, nợ xấu tăng, bất động sản đóng băng
- Giá cổ phiếu: GIẢM giai đoạn early-cycle
- Sau 2-3 quý: lãi suất cho vay tăng → NIM phục hồi

Deep dive chu kỳ NIM: xem [`bank-nim-cycle.md`](./bank-nim-cycle.md).

## 3.3 Bốn giai đoạn chu kỳ ngân hàng

| Giai đoạn | Đặc trưng | Tín hiệu nhận diện | Phản ứng thị trường |
|---|---|---|---|
| **Tích lũy** | Tín dụng tăng chậm, NIM đáy, nợ xấu cao | Tăng trưởng tín dụng <10%, NPL >2% | Giá thấp, P/B gần đáy lịch sử |
| **Bùng nổ** | Tín dụng bứt phá, NIM mở rộng, nợ xấu giảm | Tăng trưởng tín dụng >15%, NIM tăng QoQ | Giá tăng mạnh, P/B 1.5-2.0x |
| **Quá nhiệt** | Tín dụng cạn room, NIM đỉnh, bất động sản đầu cơ | Room NHNN được tận dụng hết H1, coverage giảm | Giá cao, định giá kéo dài |
| **Điều chỉnh** | Nợ xấu tăng, NIM bị nén, trích lập tăng | NPL spike YoY, dự phòng tăng mạnh, LNTT miss target | Giá giảm, P/B về 1.0-1.3x |

## 3.4 VCB — bằng chứng lịch sử (chu kỳ 2020-2025)

VCB là ngân hàng có số liệu dài nhất, chất lượng nhất để theo dõi chu kỳ ngành:

- **2020-2021**: NIM cao do lãi suất NHNN thấp + tín dụng tăng mạnh hậu COVID. VCB coverage ratio >300% — over-reserved nhất ngành.
- **Q3/2022**: NIM ngành đạt đỉnh chu kỳ. NHNN nâng lãi suất điều hành mạnh (tháng 9-10/2022) để giữ tỷ giá USD/VND.
- **2023**: COF nở vọt → NIM ngành giảm về vùng đáy. VCB bị ảnh hưởng ít hơn tư nhân do CASA cao cấu trúc.
- **2024-2025**: Tín dụng phục hồi, lãi suất hạ, nhưng NIM vẫn ở vùng thấp do cạnh tranh và nhiệm vụ hỗ trợ doanh nghiệp.

---

# LỚP 4: ĐỊNH VỊ TỪNG MÃ (STRUCTURAL POSITIONING)

*Lớp này chỉ ghi định vị chiến lược bền vững — không ghi số quý gần nhất. Số liệu cụ thể tra Finpath API.*

| Mã | Định vị cốt lõi | Ưu thế dài hạn | Rủi ro cấu trúc |
|---|---|---|---|
| **VCB** | Quốc doanh chất lượng tài sản cao nhất; thị phần ngoại hối + thanh toán quốc tế lớn nhất | CASA cấu trúc từ tài khoản doanh nghiệp; quản trị rủi ro nghiêm ngặt nhất; P/B premium cấu trúc (franchise value) | NIM thấp do nhiệm vụ hỗ trợ doanh nghiệp; tăng trưởng tín dụng thường thấp hơn tư nhân |
| **BID** | Quốc doanh lớn nhất theo tổng tài sản; cho vay hạ tầng + doanh nghiệp nhà nước | Hưởng lợi mạnh khi đầu tư hạ tầng công tăng; phí bảo lãnh dự án lớn | NIM thấp nhất Big 4; TPDN bất động sản exposure lịch sử cao hơn VCB |
| **CTG** | Quốc doanh cân bằng corporate + SME công nghiệp/xuất khẩu | Hưởng lợi chu kỳ công nghiệp; mạng lưới phân phối rộng tỉnh | CIR cao (mạng lưới lớn, nhân sự đông); số hóa chậm hơn MBB |
| **MBB** | Quốc doanh số hóa hàng đầu; CASA cao nhất nhóm; hệ sinh thái MCredit + MB Ageas | App ngân hàng số lượng người dùng lớn; cross-selling đa dịch vụ | MCredit nhạy chu kỳ tiêu dùng; sở hữu quân đội hạn chế một số hợp tác quốc tế |
| **TCB** | Tư nhân CASA cao nhất ngành (cấu trúc, không seasonal); hệ sinh thái Masan | CASA → COF thấp → NIM >4% ngay cả khi ngành ở ~3%; danh mục khách hàng cao cấp | Lịch sử liên kết BĐS tạo concentration risk; phí bảo hiểm liên kết dưới áp lực |
| **ACB** | Tư nhân bảo thủ nhất; SME + cá nhân; NPL thấp nhất nhóm tư nhân lịch sử | Chất lượng danh mục tốt → trích lập thấp → lợi nhuận ổn định; ít exposure BĐS nhất | Tăng trưởng không đột phá; ít upside từ BĐS hồi phục; bancassurance nhỏ hơn |
| **VPB** | Tư nhân consumer-finance heavy qua FE Credit; NIM cao nhất nhóm khi cycle tốt | Hưởng lợi mạnh nhất khi consumer credit phục hồi; FE Credit top 2 thị phần tài chính tiêu dùng | NPL cao nhất nhóm khi cycle xấu; FE Credit lỗ 2022-2023 kéo ROE tổng hợp xuống |

> **Decision rule**: Quốc doanh = nhiệm vụ chính sách → NIM thấp hơn, P/B premium chỉ cho VCB (franchise). Tư nhân = market-driven → NIM cycle rõ hơn, phân tích chất lượng danh mục kỹ hơn.

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 Phương pháp định giá phổ biến

- **P/B (giá / giá trị sổ sách)**: phương pháp chính. P/B phản ánh kỳ vọng ROE dài hạn + chất lượng tài sản.
- **P/E điều chỉnh**: loại bỏ lãi/lỗ một lần để thấy lợi nhuận mảng kinh doanh cốt lõi.
- **GGM (Gordon Growth Model)**: P/B = (ROE - g) / (CoE - g). Underestimate VCB/TCB vì không capture franchise value + CASA structural advantage.
- **Sum-of-the-parts**: phù hợp ngân hàng có hệ sinh thái đa dịch vụ (MBB, TCB).

## 5.2 Vùng định giá chu kỳ (P/B — tham chiếu lịch sử)

| Pha thị trường | P/B điển hình ngành |
|---|---|
| Đáy điều chỉnh | 0.8–1.2 lần |
| Phục hồi early-cycle | 1.2–1.8 lần |
| Bùng nổ mid-cycle | 1.8–2.5 lần |
| Đỉnh chu kỳ | 2.5–3.0 lần |

VCB premium cấu trúc ~0.5-1.0x so với Big 4 còn lại (franchise + CASA). TCB/MBB thường trade P/B cao hơn quốc doanh (trừ VCB) do ROE cao hơn. So sánh P/B chỉ có nghĩa trong cùng tier.

## 5.3 Re-rating triggers

- NHNN nới room / hạ lãi suất → re-rate positive
- Bất động sản tháo gỡ pháp lý lớn → giải phóng NPL ẩn → re-rate positive
- Khủng hoảng TPDN mới → re-rate negative
- Basel III siết vốn, tăng vốn điều lệ pha loãng → re-rate negative short-term

---

# LỚP 6: CASE STUDY LỊCH SỬ

### Chu kỳ 1 — 2020-2021: NIM peak hậu COVID + bất động sản bùng nổ

NHNN hạ lãi suất mạnh 2020 → COF giảm nhanh trong khi lãi suất cho vay giảm chậm → NIM ngành đỉnh chu kỳ. Tín dụng bất động sản bùng nổ. Lợi nhuận ngành ngân hàng tăng kỷ lục 2021. **Bài học**: NIM peak + tín dụng bùng nổ đi cùng rủi ro ẩn (BĐS đầu cơ + TPDN ồ ạt). Coverage ratio cao là bộ đệm cho phase điều chỉnh.

### Chu kỳ 2 — 2022: NHNN siết tiền tệ + Khủng hoảng TPDN

Tân Hoàng Minh (4/2022) + Vạn Thịnh Phát–SCB (10/2022) đóng băng thị trường TPDN; NHNN nâng lãi suất điều hành mạnh tháng 9-10/2022 → lãi suất huy động 12 tháng peak 9-10% → COF nở vọt → NIM toàn ngành bị nén mạnh sang 2023. **Bài học**: TPDN bất động sản là rủi ro hệ thống không phản ánh trong NPL thông thường — phải kiểm tra exposure ẩn trong thuyết minh BCTC.

### Chu kỳ 3 — TCB 2022-2025: CASA cấu trúc bền vững qua cycle

TCB NIM đỉnh ~5.78% Q2/2022 → đáy ~4.44% Q2/2023 → phục hồi 2024; CASA cuối 2025 >40% (cao nhất ngành) nhờ hệ sinh thái Masan + TCBS giữ tiền gửi không kỳ hạn khách hàng cao cấp. **Bài học**: CASA từ hệ sinh thái (không từ lãi suất) là lợi thế bền vững qua chu kỳ — NIM TCB cao hơn toàn ngành ~1-1.5 điểm phần trăm ngay cả ở trough.

### Chu kỳ 4 — VPB/FE Credit 2021-2026: consumer credit boom-bust

FE Credit lãi ~620 tỷ Q1/2022 → lỗ ~3,000 tỷ năm 2022 → lỗ ~3,529 tỷ năm 2023 → thu hẹp lỗ 2024 → kỳ vọng phục hồi 3,000-4,000 tỷ từ 2025. **Bài học**: Tài chính tiêu dùng khuếch đại biên độ chu kỳ — NIM cao khi tốt nhưng NPL spike khi kinh tế xấu. Phân tích VPB cần tách standalone bank vs consolidated.

### Chu kỳ 5 — P/B trap quốc doanh (VCB 2021-2024)

VCB P/B trên 3x năm 2021 → về 2.2-2.5x năm 2022-2024. Nhiều phân tích kết luận "VCB đắt" vì so P/B tuyệt đối với tư nhân nhỏ. **Bài học**: P/B phải xét tương đối với ROE + CASA structural advantage + franchise value. GGM thuần underestimate giá trị do không capture franchise. So sánh chỉ có nghĩa trong cùng tier.

---

## Hướng dẫn tra dữ liệu thời gian thực (cho Master Bank)

KB master này chỉ cung cấp framework + threshold + range historical. Khi viết bài quarter cụ thể, Master phải:

1. **Query KB framework** (file này + 3 deep dive: NIM-cycle, NPL-reading, Target-vs-Actual) — static guidance.
2. **Query YAML** (`data/manual/credit_room.yaml` + `nhnn_circulars.yaml`) — semi-static + regulatory archive.
3. **Finpath API** cho data realtime:
   - `get_bank_ratios(ticker)` — NIM/CASA/COF/NPL/LDR/PE/PB/ROE quarterly + yearly
   - `get_bank_ratios_batch([t1,t2,t3])` — competitive comparison
   - `get_income_statement(ticker)` + `get_balance_sheet(ticker)` — BCTC quarter
   - `get_deposit_credit(ticker)` — credit growth + deposit composition
   - `get_bad_debt(ticker)` — NPL detail nhóm 3-5 + tái cơ cấu + VAMC
   - `get_net_interest_income(ticker)` — NII breakdown
   - `get_shareholders(ticker)` + `get_events(ticker)` + `get_news(ticker)` — ownership + ĐHĐCĐ + tin
4. **Web_search** cho data Finpath API không có:
   - ĐHĐCĐ kế hoạch chi tiết + actual quarter (parse từ income_statement + ratios)
   - NHNN nới room mid-year (case 28/8/2024)
   - Recent regulatory updates (TT mới NHNN)
   - Sự kiện thị trường ảnh hưởng sector

Pipeline log V4.0 emit `data_trail` array: `{source, fetched, purpose, supports_argument}` per fact. KHÔNG bịa số.

---

## Cross-link

| Deep dive | Nội dung chính |
|---|---|
| [`bank-nim-cycle.md`](./bank-nim-cycle.md) | Chu kỳ NIM + CASA + loan mix; phase repricing lãi suất NHNN |
| [`bank-npl-reading.md`](./bank-npl-reading.md) | Đọc nợ xấu thật vs reported (NPL + tái cơ cấu + VAMC + TPDN); coverage ratio threshold |
| [`bank-target-vs-actual-pattern.md`](./bank-target-vs-actual-pattern.md) | Pattern ĐHĐCĐ posture (conservative/realistic/aggressive) + Q1 % completion benchmark |

---

## Phần suy luận (cần verify)

Các điểm dưới đây rút từ framework + data historical — không có nguồn VN cite trực tiếp, cần verify khi đưa vào bài cụ thể:

- **"P/B premium VCB 0.5-1.0x so với Big 4 còn lại"** — tổng hợp từ nhiều bài phân tích 2022-2025, không cite nguồn cụ thể. Verify bằng P/B realtime Finpath API khi viết bài.
- **"NIM tư nhân top tier >4%, quốc doanh ~3%"** — range historical tổng hợp; số cụ thể quý hiện tại phải fetch từ Finpath API `get_bank_ratios`.
- **"FE Credit lỗ 3,000 tỷ 2022, 3,529 tỷ 2023"** — trích từ Changelog v1.1 Notion bootstrap (06/05/2026). Cần verify từ BCTC hợp nhất VPB hoặc web_search "FE Credit kết quả kinh doanh 2022 2023".
- **"TCB NIM peak 5.78% Q2/2022, đáy 4.44% Q2/2023"** — số này từ Changelog v1.1 Notion bootstrap; cần xác minh với Finpath API `get_bank_ratios('TCB')` quarterly series.
- **"Bancassurance tỷ trọng 10-15% NFI"** — approximate range; thực tế varies mạnh theo bank (MBB, TCB cao hơn; VCB, BID thấp hơn).
- **"Bốn giai đoạn chu kỳ ngân hàng"** (Tier 1/2/3 threshold table) — framework tổng hợp Claude, không có nguồn analyst VN cụ thể cite ngưỡng này.
- **"Q1 completion benchmark 22-28% on-track"** — analytical heuristic; cần cross-check với data thực từ nhiều năm qua Finpath API.
