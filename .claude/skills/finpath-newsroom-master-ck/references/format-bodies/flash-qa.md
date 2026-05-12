# Format: flash_qa (100-150 từ)

> Loaded from `Skill: finpath-newsroom-master-ck`. Apply khi `format_id == "flash_qa"`.

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

≥1 bold `**...**` trong body paragraph. Highlight 1 số key (vd `**lãi +24%**`).

## Verdict line

Closing MUST có verdict cho NĐT phân loại (Voice Rule 3):
- Tốt: "Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động ngắn hạn"
- Xấu: "Cần thêm thông tin để đánh giá" (ba phải, fail Voice Rule 2)

## Examples CK sector

### Example 1: SSI +6.2% Hot

Title: `SSI tăng kịch trần 6,2%: vì sao thị trường ngả mạnh sau lãi quý?`

Body (135 từ):
> SSI tăng kịch trần 6,2% phiên sáng 12/5 sau khi công bố lãi quý 1 vượt 24% so cùng kỳ, vì sao thị trường phản ứng mạnh đến vậy?
>
> Lãi tăng vì doanh thu cho vay ký quỹ nới rộng 18% nhờ dư nợ ký quỹ trung bình tăng từ 12.500 tỷ lên 14.800 tỷ, kết hợp doanh thu môi giới +9% nhờ thanh khoản HOSE quý 1 cải thiện. **Thị phần môi giới SSI Q1/2026 đạt 9,8%** vẫn dẫn đầu HOSE, tự doanh ghi nhận lãi 380 tỷ chủ yếu từ danh mục ghi nhận theo giá thị trường vào lợi nhuận quý. Phía sau con số: SSI đang ăn được phần đầu chu kỳ thanh khoản cải thiện, không phải bùng nổ ngắn hạn.
>
> Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động phiên theo thanh khoản.

### Example 2: VCI -5.8% Cold panic

Title: `VCI giảm sàn 5,8%: thị trường panic biên lãi co có quá đà?`

Body (128 từ):
> Bản Việt giảm sàn 5,8% phiên sáng nay sau tin biên lãi gộp môi giới co từ 38% xuống 32% quý 1, vì sao thị trường panic dù lãi vẫn dương?
>
> Phản ứng panic chủ yếu do lo ngại VCI mất thị phần vào nhóm miễn phí. Nhưng dữ liệu thực tế: **thị phần môi giới VCI Q1 vẫn 8,4%** giảm nhẹ 0,3 điểm so với quý trước, biên co chủ yếu do VCI chủ động giảm phí 2 gói khách hàng mới để bảo vệ tệp. Doanh thu ngân hàng đầu tư +42% bù lại. Phía sau panic: VCI đang chấp nhận hy sinh biên ngắn hạn để giữ thị phần trước chu kỳ FTSE nâng hạng 9/2026.
>
> Mã phù hợp NĐT giá trị tin chiến lược giữ thị phần, không phù hợp NĐT short-term tham gia panic.
