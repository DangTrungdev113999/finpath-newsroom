# Format: flash_qa (100-150 từ)

> Loaded from `Skill: finpath-newsroom-master-apparel`. Apply khi `format_id == "flash_qa"`.

## Khi nào dùng

Ticker_status = Hot (top tăng/giảm/bùng nổ/cạn cung) + data_richness ∈ {low, medium}. Người đọc cần info nhanh khi mã đang nóng.

## Body pattern

```
[1 câu mở (≥20 từ): nêu question chính]

[1 paragraph trả lời (60-100 từ): answer + verdict]

[1 câu closing (≤20 từ): verdict ngắn cho NĐT cầm]
```

- KHÔNG bullet
- KHÔNG heading "## Cần để ý"
- Max 1 em dash / bài (V5.1.2 PATCH em_dash_density gate)

## Word count

- Total: 100-150 từ HARD CAP. <100 fail word_count. >150 fail word_count.
- Opening: ≥20 từ
- Body paragraph: 60-100 từ
- Closing: ≤20 từ

## Bold highlight

≥1 bold `**...**` trong body paragraph. Highlight 1 số key (VD: `**biên gộp 13%**`, `**đơn chốt 5 tháng**`).

## Verdict line

Closing MUST có verdict cho NĐT phân loại (Voice Rule 3):
- Tốt: "Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động quý theo chu kỳ đơn hàng"
- Xấu: "Cần thêm thông tin để đánh giá" (ba phải, fail Voice Rule 2)

## Examples Apparel sector

### Example 1: MSH +5.8% sau tin đơn hàng Q2

Body (128 từ):
> May Sông Hồng tăng kịch trần 5,8% phiên sáng 12/5 sau khi công bố đã chốt đơn hàng đến hết quý 2/2025, vì sao thị trường phản ứng mạnh đến vậy?
>
> Đơn hàng chốt sớm 5 tháng phía trước phản ánh khách Nike và Columbia tái nhập đơn rõ sau giai đoạn xả tồn kho 2022-2023. **Biên lãi gộp Q4/2024 về 11%** từ đáy 8% năm 2023, doanh thu USD chiếm trên 95% nên USD/VND tăng nhẹ cũng hỗ trợ. Tín hiệu phục hồi đến từ phân khúc khách phổ thông trước, chưa cần chờ phân khúc cao cấp.
>
> Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động quý theo chu kỳ đơn hàng.

### Example 2: TCM -6.2% sau tin tồn kho bán lẻ Mỹ tăng

Body (132 từ):
> Thành Công Textile giảm sàn 6,2% phiên sáng nay sau tin tồn kho bán lẻ Mỹ tháng 3 tăng 12%, vì sao thị trường hoảng loạn dù lãi quý 4 vẫn tăng?
>
> Phản ứng hoảng loạn chủ yếu do lo ngại lặp lại chu kỳ 2022-2023. Dữ liệu thực tế: **tồn kho bán lẻ Mỹ +12% so với tháng 12/2025** đang vượt ngưỡng trung bình 5 năm, áp lực hủy đơn lan đến VN sau 2 quý theo chu kỳ trước. TCM mảng sợi đặc biệt nhạy vì biên gộp đã mỏng, nếu khách Mỹ giãn giao hàng sẽ kéo tỷ lệ chạy máy xuống dưới 70%.
>
> Mã phù hợp NĐT giá trị chấp nhận biến động chu kỳ, không phù hợp NĐT lướt sóng theo cơn hoảng loạn.
