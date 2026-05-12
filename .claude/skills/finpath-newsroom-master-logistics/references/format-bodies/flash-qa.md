# Format: flash_qa (100-150 từ)

> Loaded from `Skill: finpath-newsroom-master-logistics`. Apply khi `format_id == "flash_qa"`.

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

≥1 bold `**...**` trong body paragraph. Highlight 1 số key (VD: `**lãi +22%**`, `**sản lượng thông quan 920.000 TEU**`).

## Verdict line

Closing MUST có verdict cho NĐT phân loại (Voice Rule 3):
- Tốt: "Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động cước phí ngắn hạn"
- Xấu: "Cần thêm thông tin để đánh giá" (ba phải, fail Voice Rule 2)

## Examples Logistics sector

### Example 1: GMD +6.5% Hot

Title: `GMD tăng kịch trần 6,5%: vì sao thị trường ngả mạnh sau sản lượng quý?`

Body (135 từ):
> GMD tăng kịch trần 6,5% phiên sáng 12/5 sau khi công bố sản lượng thông quan quý 1 vượt 14% so cùng kỳ, vì sao thị trường phản ứng mạnh đến vậy?
>
> Sản lượng tăng vì xuất khẩu hàng VN sang Mỹ phục hồi 9% so cùng kỳ, kết hợp cụm cảng Nam Đình Vũ Phase 2 chạy full công suất 90% sau khi mở rộng năm 2023. **Sản lượng thông quan Q1/2026 đạt 920.000 TEU** dẫn đầu nhóm cảng phía Bắc, biên lãi gộp khai thác cảng giữ ổn định 38%. Phía sau con số: GMD đang ăn được phần đầu chu kỳ thương mại VN-Mỹ phục hồi, không phải bùng nổ ngắn hạn theo cước phí.
>
> Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động phiên theo đường ống xuất khẩu.

### Example 2: HAH -5.8% Cold panic

Title: `HAH giảm sàn 5,8%: thị trường panic cước phí container có quá đà?`

Body (128 từ):
> Hải An giảm sàn 5,8% phiên sáng nay sau tin cước phí trục Á-Mỹ rơi xuống 2.800 USD/TEU từ mức 3.500 quý trước, vì sao thị trường panic dù đội tàu vẫn đầy?
>
> Phản ứng panic chủ yếu do lo ngại cước phí về vùng đáy 2023. Nhưng dữ liệu thực tế: **đội tàu container HAH chạy 95% công suất** quý 1, hợp đồng dài hạn chiếm 65% doanh thu cố định cước phí mức 3.000 USD/TEU đến hết 2026. Biên lãi gộp Q1 vẫn 18%. Phía sau panic: HAH đang khóa được dòng tiền nhờ hợp đồng dài hạn, không bị ảnh hưởng tức thì khi cước phí giao ngay rơi.
>
> Mã phù hợp NĐT giá trị tin chiến lược hợp đồng dài hạn, không phù hợp NĐT short-term tham gia panic.
