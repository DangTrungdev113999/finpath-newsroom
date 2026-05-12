# Format: standard_qa (200-300 từ)

> Loaded from `Skill: finpath-newsroom-master-bank`. Apply khi `format_id == "standard_qa"`.

## Khi nào dùng

Deep question category ∈ {paradox, why_now, hidden_mechanism} + data_richness ≥ medium. Người đọc cần mechanism reasoning nhưng không cần liệt kê chi tiết.

## Body pattern

```
[Opening paragraph 30-80 từ — sự kiện + tension/setup, có thể end với câu hỏi]

- **Bold highlight 1**: substantive bullet ≥20 từ với connector + mechanism reasoning
- **Bold highlight 2**: bullet ≥20 từ
- **Bold highlight 3**: bullet ≥20 từ
- ... up to 6 bullets

[Closing — 1 câu phân loại NĐT phù hợp]
```

- KHÔNG heading "## Cần để ý"
- 3-6 bullets (substantive, mechanism + bold number)
- Max 1 em dash / 100 từ (V5.1.2 PATCH em_dash_density)

## Word count

- Total: 200-300 từ HARD CAP. <200 fail word_count. >300 fail word_count.
- Opening: 30-80 từ
- Each bullet: ≥20 từ
- Closing: 1 câu (≤30 từ), không bullet, không heading

## Bold highlight

Mỗi bullet MUST có ≥1 bold `**...**`. Bold số (vd `**ROE 24,5%**`) hoặc verdict word (vd `**hy sinh**`, `**đánh đổi**`).

## Verdict line

Closing MUST có verdict cho NĐT phân loại (Voice Rule 3):
- 3 elements: direction + timeframe + holder action
- Tốt: "Mã phù hợp NĐT giá trị giữ trên 12 tháng, ưu tiên buffer phòng thủ"
- Xấu: "Tùy quan điểm NĐT đánh giá" (ba phải, fail Voice V2)

## Examples Bank sector

### Example 1: paradox — VCB hy sinh tăng trưởng (220 từ)

Title: `VCB hy sinh tăng trưởng để đánh đổi cho điều gì?`

Body:
> Vietcombank công bố tín dụng quý 1 chỉ tăng 1,8% trong khi cả nhóm tư nhân đua tăng 4-5%, nhưng giá cổ phiếu vẫn vững trên 95.000 đồng. Vì sao to nhất lại đi chậm nhất, và cổ đông trả tiền cho điều gì?
>
> - **Tín dụng 1,8%** thấp hơn trung bình ngành 3,1% phản ánh VCB chọn giữ chất lượng khách hàng top, không chạy doanh số quý đầu năm.
> - **Nợ xấu 0,9%** thấp nhất 27 mã niêm yết, giảm 12 điểm cơ bản so với cùng kỳ — kết quả trực tiếp của chiến lược screen khắt khe trong 18 tháng qua.
> - **Tỷ suất sinh lời vốn chủ 22,3%** vẫn dẫn đầu Big4 dù tăng trưởng thấp, chứng minh quy mô cộng với giá vốn rẻ đang bù cho tốc độ.
> - **Vùng đệm dự phòng 226%** cao gấp 1,8 lần ngưỡng NHNN, sẵn sàng hấp thụ shock TPDN BĐS nếu chu kỳ tái cơ cấu kéo dài sang 2027.
>
> Mã phù hợp NĐT giá trị giữ trên 18 tháng, ưu tiên chất lượng tài sản hơn tốc độ tăng trưởng quý.

### Example 2: why_now — TCB rút BĐS 2026 (260 từ)

Title: `Vì sao TCB chọn rút BĐS năm 2026, không phải 2023?`

Body:
> Techcombank vừa công bố giảm tỷ trọng cho vay BĐS từ 31% xuống dưới 25% trong kế hoạch 2026, sau gần 3 năm vẫn neo tỷ trọng cao bất chấp khủng hoảng 2022-2023. Vì sao timing là bây giờ, không phải đỉnh khủng hoảng?
>
> - **Tỷ trọng BĐS 31%** năm 2022 không giảm vì TCB chấp nhận chịu nợ xấu nhóm 2 tăng để giữ khách hàng phát triển dự án qua chu kỳ, đặt cược ngành sẽ hồi.
> - **Lãi quý 1/2026 vẫn tăng 22%** chứng minh buffer dự phòng đã đủ dày để rút mà không tổn thương thu nhập — điều kiện không có trong 2023.
> - **Tín dụng tiêu dùng tăng 28%** trong 18 tháng qua đã tạo nguồn thay thế, TCB không còn phụ thuộc BĐS cho tăng trưởng.
> - **NHNN siết Thông tư 22** áp dụng đầy đủ từ 2027 buộc giảm hệ số rủi ro BĐS, TCB rút sớm 12 tháng để chuẩn bị vốn cấp 1.
> - **Định giá P/B 1,3 lần** thấp hơn trung bình 5 năm 1,7 lần, ban điều hành muốn re-rate khi thị trường nhìn TCB như bank cân bằng, không phải BĐS bank.
>
> Mã phù hợp NĐT giá trị tin chiến lược chuyển hướng 24-36 tháng, chấp nhận P/B chưa re-rate ngay.
