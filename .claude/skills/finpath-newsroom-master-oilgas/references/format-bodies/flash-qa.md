# Format: flash_qa (100-150 từ)

> Loaded from `Skill: finpath-newsroom-master-oilgas`. Apply khi `format_id == "flash_qa"`.

## Khi nào dùng

Ticker_status = Hot (top tăng/giảm, Brent move mạnh, OPEC+ ra quyết định, sự kiện đột biến) + data_richness ∈ {low, medium}. Người đọc cần info nhanh khi mã đang nóng.

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

≥1 bold `**...**` trong body paragraph. Highlight 1 số key (VD: `**biên lọc dầu 12 USD/thùng**`).

## Verdict line

Closing MUST có verdict cho NĐT phân loại (Voice Rule 3):
- Tốt: "Mã phù hợp NĐT chu kỳ giữ trên 12 tháng, chấp nhận biến động giá dầu"
- Xấu: "Cần thêm thông tin để đánh giá" (ba phải, fail Voice Rule 2)

## Examples oilgas sector

### Example 1: BSR +6.5% Hot — biên lọc dầu nới rộng

Body (135 từ):
> BSR tăng kịch trần 6,5% phiên sáng 12/5 sau khi công bố biên lọc dầu quý 1 nới lên 11,8 USD/thùng, cao gấp đôi cùng kỳ, vì sao thị trường phản ứng mạnh đến vậy?
>
> Biên nới chủ yếu nhờ giá Brent giảm chậm hơn giá xăng A95 Singapore, BSR mua dầu thô đầu vào giá trung bình 78 USD/thùng nhưng bán sản phẩm tinh chế ở mặt bằng 90 USD/thùng. **Sản lượng nhà máy Dung Quất đạt 1,7 triệu tấn** quý 1, gần full công suất 96%. Lợi nhuận trước thuế quý ước vượt 2.800 tỷ, tăng 43% so cùng kỳ. Phía sau con số: BSR đang ăn được phần lợi từ chu kỳ chênh lệch dầu thô-sản phẩm mở rộng, không phải tăng nóng nhu cầu.
>
> Mã phù hợp NĐT chu kỳ giữ trên 12 tháng, chấp nhận biến động theo giá Brent.

### Example 2: PVD -6.8% Cold panic — Brent crash

Body (128 từ):
> PVD giảm sàn 6,8% phiên sáng nay sau khi Brent crash 8% trong đêm về 68 USD/thùng, vì sao thị trường panic dù dự án khoan Việt Nam vẫn ổn định?
>
> Phản ứng panic chủ yếu do nỗi nhớ chu kỳ 2020 khi Brent âm giá khiến PVD lỗ nặng cả năm. Nhưng dữ liệu thực tế: **PVD đã ký 3 hợp đồng khoan dài hạn** với giá trị 1.200 tỷ cho 2026, không phụ thuộc giá dầu giao ngay. Số ngày tồn kho dầu thô toàn cầu vẫn ở mức bình thường, OPEC+ chưa quyết định nới sản lượng. Phía sau panic: nỗi sợ lặp lại 2020 đang ép giá xuống vùng oversold so với nội tại doanh nghiệp.
>
> Mã phù hợp NĐT giá trị tích lũy vùng oversold, không phù hợp NĐT short-term theo panic.
