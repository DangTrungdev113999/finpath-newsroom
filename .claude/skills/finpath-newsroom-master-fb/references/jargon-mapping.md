# Jargon Mapping — Sector Tiêu dùng Thực phẩm (fb)

> Loaded from `Skill: finpath-newsroom-master-fb`. Anh → Việt strict mapping cho gate `no_english_jargon`. 0% từ tiếng Anh trong body Master + insight_final + closing.

## QUY TẮC CỨNG — 0% TỪ TIẾNG ANH

Bài Master + insight_final = KHÔNG được có 1 từ tiếng Anh nào (kể cả viết tắt thông dụng ASP / SKU / FMCG / MT / GT). Rule binary: hoặc 0% Anh, hoặc fail gate, KHÔNG persist.

## Industry-specific (fb sector)

| Anh | Việt thuần | Note |
|---|---|---|
| ASP (average selling price) | giá bán trung bình | KHÔNG dùng viết tắt ASP trong body |
| volume | sản lượng | (tấn / lít / hộp) |
| volume growth | tăng trưởng sản lượng | |
| gross margin | biên lợi nhuận gộp | |
| gross profit | lợi nhuận gộp | |
| COGS | giá vốn hàng bán | |
| SKU | mã sản phẩm | |
| FMCG | hàng tiêu dùng nhanh | |
| modern trade (MT) | kênh hiện đại (siêu thị + minimart + cửa hàng tiện lợi) | KHÔNG dùng MT |
| general trade (GT) | kênh truyền thống (chợ + tạp hóa) | KHÔNG dùng GT |
| on-trade | tiêu dùng tại chỗ (quán + nhà hàng) | dành cho rượu bia |
| off-trade | tiêu dùng mang về | dành cho rượu bia |
| HORECA | kênh khách sạn nhà hàng quán | giải thích đầy đủ |
| distribution coverage | phủ điểm bán | |
| point of sale | điểm bán hàng | |
| premiumization | đẩy lên phân khúc cao cấp / nâng dòng sản phẩm | |
| premium segment | phân khúc cao cấp | |
| mass market | thị trường đại chúng / phân khúc phổ thông | |
| private label | nhãn riêng | |
| route to market | tuyến phân phối | |
| direct-to-consumer | bán thẳng đến người tiêu dùng | |
| trade marketing | tiếp thị tại điểm bán | |
| brand power | sức mạnh thương hiệu | |
| market share | thị phần | |
| same-store sales (SSS) | doanh số cửa hàng cũ | dành cho chuỗi bán lẻ (WinMart) |
| inventory turnover | vòng quay tồn kho | |
| inventory days | số ngày tồn kho | |
| working capital | vốn lưu động | |

## Nguyên liệu đầu vào (raw material)

| Anh | Việt thuần | Note |
|---|---|---|
| dairy commodity | nguyên liệu sữa thế giới | giá Fonterra GDT |
| milk powder | sữa bột nguyên liệu | nhập từ New Zealand, Úc, EU |
| WMP / SMP | sữa bột nguyên kem / sữa bột gầy | dùng "sữa bột nguyên kem" |
| malt | mạch nha | nguyên liệu bia |
| barley | lúa mạch | |
| sugar (raw) | đường thô | giá ICE No.11 |
| palm oil | dầu cọ | nguyên liệu dầu ăn, giá Bursa Malaysia |
| sugarcane | mía nguyên liệu | |

## Tài chính chuẩn

| Anh | Việt thuần |
|---|---|
| revenue | doanh thu thuần |
| net profit | lợi nhuận sau thuế |
| EBITDA | lợi nhuận trước thuế lãi vay khấu hao (giải thích nguyên câu, KHÔNG dùng viết tắt) |
| LNTT | lãi trước thuế / lợi nhuận trước thuế (Việt) |
| LNST | lãi sau thuế / lợi nhuận sau thuế (Việt) |
| ROA | tỷ suất sinh lời tài sản |
| ROE | tỷ suất sinh lời vốn chủ |
| EPS | lợi nhuận trên mỗi cổ phiếu |
| PE | hệ số PE (Vietnam dùng "PE" trực tiếp acceptable trong context giá) |
| PB | hệ số PB |
| dividend yield | tỷ suất cổ tức |
| payout ratio | tỷ lệ chi trả cổ tức |

## Trading / thời gian

| Anh | Việt thuần |
|---|---|
| YoY | so cùng kỳ |
| QoQ | so quý trước |
| YTD | lũy kế từ đầu năm |
| HoH | so nửa năm trước |
| MoM | so tháng trước |

## Quản trị / chiến lược

| Anh | Việt thuần |
|---|---|
| portfolio (sản phẩm) | danh mục sản phẩm |
| portfolio (đầu tư) | danh mục đầu tư |
| transformation | chuyển đổi / chuyển hướng |
| divestment | thoái vốn |
| M&A | mua bán sáp nhập |
| spin-off | tách niêm yết / tách công ty con |
| joint venture | liên doanh |
| trade-off | đánh đổi |
| catalyst | yếu tố thúc đẩy / động lực |
| anchor | nguồn chính / căn cứ chính |
| momentum | đà tăng / đà giảm |
| defensive | thận trọng / phòng thủ |
| pattern | mô hình / khuôn mẫu lặp lại |
| target | mục tiêu / kế hoạch |
| scenario | kịch bản |
| story | câu chuyện |
| outlook | triển vọng |

## Anti-pattern (must reject)

- "ASP của VNM tăng 5%" → "giá bán trung bình của VNM tăng 5%"
- "FMCG sector cycle" → "chu kỳ ngành hàng tiêu dùng nhanh"
- "MT channel của Masan" → "kênh hiện đại (siêu thị) của Masan"
- "on-trade giảm vì NĐ100" → "tiêu dùng tại chỗ giảm vì Nghị định 100"
- "SAB premium segment" → "phân khúc cao cấp của Sabeco"
- "Volume growth Q1 +8%" → "sản lượng quý 1 tăng 8% so cùng kỳ"
- "Same-store sales WinMart +12%" → "doanh số cửa hàng cũ của WinMart tăng 12%"
- "Gross margin 42% YoY" → "biên lợi nhuận gộp 42%, tăng so cùng kỳ"
- "Private label tăng share" → "nhãn riêng tăng thị phần"
- "Premiumization strategy" → "chiến lược đẩy lên phân khúc cao cấp"

## Exception (cho phép giữ tiếng Anh hoặc tên riêng)

- Tên thương hiệu / công ty: Vinamilk, Masan, Sabeco, Heineken, TH True Milk, WinMart, WinCommerce, Mondelez, Vinasoy, Tường An, Vocarimex, Wall's, Chinsu, Omachi, Kokomi, Vinacafé, Biscafun
- Tên đơn vị tiền: USD, VND, EUR
- Ký hiệu sản phẩm cố định: Coca-Cola, Pepsi (tên riêng)
- Số thông dụng: Q1/Q2/Q3/Q4 (giữ — viết tắt quý chuẩn Việt)
- Nghị định 100 (giữ nguyên tên văn bản pháp lý)

## Note đặc biệt

Khi đề cập SK Group (nhà đầu tư Hàn Quốc của Masan Consumer), Thaibev (chủ sở hữu Sabeco), Fonterra (nhà cung cấp sữa bột nguyên liệu) — giữ nguyên tên riêng, không cần dịch.
