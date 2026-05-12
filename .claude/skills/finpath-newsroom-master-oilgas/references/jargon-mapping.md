# Jargon Mapping — oilGas Anh → Việt

> Loaded from `Skill: finpath-newsroom-master-oilgas`. Apply CỨNG — KHÔNG để jargon tiếng Anh leak vào content (Rule 1: 0% từ tiếng Anh).

## Exception (giữ tiếng Anh)

| Term | Lý do giữ |
|---|---|
| **OPEC+** | Tên tổ chức quốc tế (không có dịch chính thức tiếng Việt thông dụng). |
| **Brent** | Tên benchmark dầu thô châu Âu (không dịch). |
| **WTI** | Tên benchmark dầu thô Mỹ (giữ, nhưng ưu tiên Brent vì Việt Nam tham chiếu Brent). |

## Mapping cứng — oilgas-specific terms

| English | Vietnamese (dùng trong content) |
|---|---|
| crack spread | chênh lệch giá dầu thô-sản phẩm |
| refining margin | biên lọc dầu |
| upstream | thăm dò khai thác (hoặc "đầu nguồn") |
| downstream | lọc hoá dầu (hoặc "cuối nguồn") |
| midstream | trung nguồn (vận chuyển + lưu trữ) |
| realized price | giá bán thực tế |
| utilization rate | hiệu suất sử dụng công suất |
| throughput | sản lượng tinh chế (BSR) / lưu lượng (POW giờ vận hành) |
| inventory turnover | vòng quay tồn kho |
| inventory days | số ngày tồn kho |
| crude oil | dầu thô |
| refined product | sản phẩm tinh chế (xăng A92/A95, dầu DO/FO, nhựa hóa dầu) |
| heating oil | dầu sưởi (ít dùng Việt Nam) |
| gasoline | xăng |
| diesel | dầu diesel (dầu DO) |
| fuel oil | dầu nặng (dầu FO) |
| LPG | khí hoá lỏng (chỉ ghi tắt LPG nếu bài đã giới thiệu lần đầu là "khí hoá lỏng") |
| LNG | khí thiên nhiên hoá lỏng (chỉ ghi tắt LNG nếu bài đã giới thiệu lần đầu) |
| natural gas | khí thiên nhiên |
| condensate | khí ngưng tụ |
| barrel | thùng (1 thùng ≈ 159 lít) |
| oil & gas | dầu khí |
| drilling rig | dàn khoan |
| offshore | ngoài khơi |
| onshore | trên bờ |
| FSO / FPSO | tàu chứa + xử lý dầu nổi (giữ tên đầy đủ nếu công bố từ doanh nghiệp, không viết tắt) |
| capex | chi phí đầu tư (giữ "đầu tư cơ bản" nếu BCTC) |
| opex | chi phí vận hành |
| backwardation | thị trường giá kỳ hạn thấp hơn giao ngay (giữ "đường cong giá kỳ hạn dốc xuống") |
| contango | thị trường giá kỳ hạn cao hơn giao ngay (giữ "đường cong giá kỳ hạn dốc lên") |

## Mapping common (kế thừa từ Bank)

| English | Vietnamese |
|---|---|
| YoY | so cùng kỳ |
| QoQ | so quý trước |
| YTD | lũy kế từ đầu năm |
| LNTT | lợi nhuận trước thuế (giữ tiếng Việt) |
| LNST | lợi nhuận sau thuế (giữ) |
| ROE | tỷ suất sinh lời vốn chủ |
| ROA | tỷ suất sinh lời tài sản |
| EPS | lợi nhuận trên mỗi cổ phiếu |
| ĐHĐCĐ | đại hội đồng cổ đông (viết tắt OK) |
| BCTC | báo cáo tài chính (viết tắt OK) |
| momentum | đà tăng/giảm (tuỳ ngữ cảnh) |
| defensive | phòng thủ |
| catalyst | chất xúc tác / động lực |
| trade-off | đánh đổi |
| anchor | neo (giá) |
| symbolic | mang tính biểu trưng |
| portfolio | danh mục |
| buffer | vùng đệm |
| stress test | kiểm tra sức chịu đựng |
| metric | chỉ số |
| target | mục tiêu / kế hoạch |
| scenario | kịch bản |

## Quy ước viết số trong content

- Giá dầu Brent: `Brent 75 USD/thùng` (KHÔNG `$75/bbl`)
- Biên lọc dầu: `biên lọc dầu 8 USD/thùng` (KHÔNG `refining margin $8/bbl`)
- Sản lượng BSR: `6,5 triệu tấn/năm` (KHÔNG `6.5 MT/year`)
- Giờ vận hành POW: `5.200 giờ` (KHÔNG `5,200 hours`)
- Số ngày tồn kho: `45 ngày` (KHÔNG `45 days`)
- Phần trăm: `tăng 12%` (KHÔNG `+12%` orphan, phải có verb)

## Self-check trước khi persist

Master scan body cuối cùng:
1. Có từ tiếng Anh nào ngoài exception list (OPEC+, Brent, WTI)?
2. Có ký hiệu tiền tệ `$` thay vì `USD`?
3. Có viết tắt tiếng Anh tự phát (như "OG cycle", "refmargin") không có trong mapping?

Bất kỳ hit nào → rewrite trước khi quality_gates check.
