# Expert Closing Examples — Quality bar, NOT template

> 6 expert closings từ chuyên gia in-house. ĐỌC để cảm nhận quality bar, KHÔNG copy structure, KHÔNG pick phrases.

## Intent (1 paragraph)

Closing không tóm tắt bài — closing CHUYỂN THESIS THÀNH QUYẾT ĐỊNH ĐẦU TƯ. Agent đọc body xong tự hỏi: cược thực sự là gì? Cho ai là buy? Cho ai là wait? Cho ai là giữ? Identity của cổ phiếu chuyển nếu thesis đúng/sai? Closing có thể 1-3 câu, conditional bet ("nếu... thì...") OK, investor segmentation ("ai tin X thì... ai chỉ nhìn Y thì...") OK, identity transformation ("không còn là gia công — sẽ là AI hạ tầng") OK. Mỗi bài tự pick form phù hợp — KHÔNG dập khuôn.

## 6 expert benchmark

### PVS — investor segmentation + identity warning
> PVS không rẻ vì có nhiều tiền mặt; PVS chỉ rẻ nếu Lô B – Ô Môn thật sự biến 100.000 tỷ backlog thành lợi nhuận. Ai tin chu kỳ dầu khí 2026–2028 đang mở ra thì nên tích lũy khi thị trường còn nghi ngờ. Ai chỉ nhìn 16.000 tỷ tiền mặt để mua thì rất dễ mua nhầm một cái két không thuộc về cổ đông.

### GAS — defensive thesis qualified
> PV GAS vẫn là cổ phiếu phòng thủ, nhưng không còn là cỗ máy in tiền dễ dàng như thời khí nội địa biên cao. Khi LNG bắt đầu ăn vào biên lợi nhuận, nhà đầu tư không nên mua GAS vì doanh thu tăng, mà chỉ nên mua khi giá đủ rẻ để bù cho giai đoạn lợi nhuận mỏng hơn.

### FPT/FOX — risk relocation + conditional outcome
> Rủi ro của FPT không nằm ở tăng trưởng, mà nằm ở cách xử lý nút thắt sở hữu tại FOX. Nếu bài toán free-float được gỡ gọn, đây chỉ là nhiễu ngắn hạn để gom thêm. Nhưng nếu phải pha loãng mạnh hoặc kéo dài quá lâu, cổ đông FPT sẽ phải trả giá cho một vấn đề không đến từ kinh doanh.

### FPT Huế — identity transformation
> FPT không chọn Huế vì Huế lớn, mà vì Huế có thứ không thể sao chép: dữ liệu văn hóa bản địa. Nếu FPT biến được di sản thành tài sản dữ liệu, cổ phiếu này sẽ được định giá như một doanh nghiệp AI hạ tầng địa phương, không còn là công ty gia công phần mềm. Đây là câu chuyện nên mua khi thị trường còn chưa hiểu hết.

### PLX kế hoạch 2026 — defensive caveat + price wait
> PLX đang bán nhiều hơn nhưng kiếm ít hơn trên mỗi lít xăng. Với biên lợi nhuận bị khóa bởi cơ chế giá và xe điện bắt đầu gặm dần nhu cầu, đây không phải cổ phiếu để mua đuổi. Nhà đầu tư đang cầm có thể giữ vì phòng thủ, nhưng muốn mua thêm thì phải đợi giá đủ rẻ.

### PLX VGX — bipolar conditional bet
> VGX không phải canh bạc 35 tỷ, mà là phép thử xem Petrolimex có biến 3.000 cây xăng thành mạng lưới năng lượng mới hay không. Nếu làm nhanh, PLX có cửa đổi vai từ người bán xăng sang chủ hạ tầng sạc và đổi pin. Nếu chậm, 35 tỷ này chỉ là một tấm vé tượng trưng để đứng nhìn xe điện lấy mất khách hàng.

## Observation (KHÔNG rule)

Đọc 6 closing trên, cảm nhận chung:
- Mỗi closing ÉP NĐT phải đối diện một quyết định cụ thể (mua / giữ / chờ / không mua) — không vague
- Khi có 2 path khả thi → spell out cả 2 (nếu A → outcome X, nếu B → outcome Y)
- Khi có investor segmentation → tách rõ (ai cầm vs ai chưa cầm vs ai tin thesis vs ai chỉ nhìn fact)
- Concrete metaphor xuất hiện tự nhiên khi cần (cái két không thuộc về cổ đông, cỗ máy in tiền, tấm vé tượng trưng, mua đuổi, gặm dần)
- Verb "nên tích lũy / nên mua / không nên mua / có thể giữ / phải đợi" rõ ràng — không hedging

Bài khác sẽ cần form khác. KHÔNG dập khuôn 6 example trên. Đọc bài → judge form phù hợp.

## Safety net (objective, không craft)

- Stance verb có mặt — `lib.voice_rules.STANCE_VERBS` (nên cầm/giữ/bán/tích lũy/phù hợp NĐT/...)
- KHÔNG vague phrase — `CLOSING_VAGUE_BAN` (cần theo dõi/đáng theo dõi/làm chỉ báo/...)
- ≥1 number trong closing (price target / threshold / timeframe có năm)

3 safety check above pass = OK. KHÔNG enforce structure/phrase/length cụ thể.
