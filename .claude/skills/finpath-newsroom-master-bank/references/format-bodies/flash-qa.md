# Format: flash_qa (100-150 từ)

> Loaded from `Skill: finpath-newsroom-master-bank`. Apply khi `format_id == "flash_qa"`.

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

≥1 bold `**...**` trong body paragraph. Highlight 1 số key (VD: `**lãi +17%**`).

## Verdict line

Closing MUST có verdict cho NĐT phân loại (Voice Rule 3):
- Tốt: "Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động ngắn hạn"
- Xấu: "Cần thêm thông tin để đánh giá" (ba phải, fail Voice Rule 2)

## Examples Bank sector

### Example 1: VCB +6.8% Hot

Body (130 từ):
> Vietcombank tăng kịch trần 6,8% trong phiên sáng 12/5 sau khi công bố lãi quý 1 vượt 11% so cùng kỳ, vì sao thị trường phản ứng mạnh đến vậy?
>
> Lãi tăng vì biên lãi vay nới rộng từ 3,1% lên 3,3% nhờ huy động giá rẻ tăng. Nợ xấu vẫn ở mức an toàn 0,9%, tỷ suất sinh lời tài sản giữ ổn định 1,8%. **Tín dụng quý 1 tăng 3,5%** cao hơn trung bình ngành 2,1%. Phía sau con số: VCB đang ăn được phần lợi từ chu kỳ NHNN nới lỏng, không phải tăng nóng tín dụng.
>
> Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động ngắn hạn theo phiên.

### Example 2: TCB -6.5% Cold panic

Body (125 từ):
> Techcombank giảm sàn 6,5% phiên sáng nay sau tin nợ xấu nhóm 2 nhảy lên 2,4%, vì sao thị trường panic dù lãi quý vẫn tăng?
>
> Phản ứng panic chủ yếu do lo ngại lan ra nhóm 3-4. Nhưng dữ liệu thực tế: **nợ xấu nhóm 2 tăng từ 1,8% lên 2,4%** chủ yếu là khoản BĐS tái cơ cấu, không phải tín dụng tiêu dùng mới. Buffer dự phòng đã +28% Q1. Phía sau panic: TCB đang chấp nhận hy sinh LNTT ngắn hạn để gia cố vùng đệm trước rủi ro chu kỳ.
>
> Mã phù hợp NĐT giá trị tin chiến lược phòng thủ, không phù hợp NĐT short-term tham gia panic.
