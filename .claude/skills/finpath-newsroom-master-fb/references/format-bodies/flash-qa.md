# Format: flash_qa (100-150 từ)

> Loaded from `Skill: finpath-newsroom-master-fb`. Apply khi `format_id == "flash_qa"`.

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
- Max 1 em dash / bài (V5.1.2 em_dash_density)

## Word count

- Total: 100-150 từ HARD CAP. <100 fail word_count. >150 fail word_count.
- Opening: ≥20 từ
- Body paragraph: 60-100 từ
- Closing: ≤20 từ

## Bold highlight

≥1 bold `**...**` trong body paragraph. Highlight 1 số key (vd `**sản lượng sữa +8%**`, `**biên lợi nhuận gộp 42%**`).

## Verdict line

Closing MUST có verdict cho NĐT phân loại (Voice Rule 3):
- Tốt: "Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động ngắn hạn"
- Xấu: "Cần thêm thông tin để đánh giá" (ba phải, fail Voice Rule 2)

## Examples sector fb

### Example 1: VNM +6.2% Hot

Body (135 từ):
> Vinamilk tăng kịch trần 6,2% phiên sáng 12/5 sau khi công bố lãi quý 1 vượt 9% so cùng kỳ và sản lượng sữa nội địa tăng trở lại sau 4 năm đi ngang, vì sao thị trường phản ứng mạnh?
>
> Lãi tăng nhờ kết hợp hai chiều: **sản lượng sữa nước nội địa tăng 4,5%** đảo chiều khỏi vùng đáy 2018-2022, đồng thời giá bán trung bình nhích thêm 2,8% nhờ đẩy dòng sữa hữu cơ. Biên lợi nhuận gộp lên 42,5%, hồi từ vùng 40,2% quý 4/2025. Phía sau con số: VNM đang gặp đà mở rộng nông thôn cộng với chu kỳ giá sữa bột nguyên liệu thế giới giảm, không phải tăng giá khuyến mại ngắn hạn.
>
> Mã phù hợp NĐT giá trị giữ trên 18 tháng, chấp nhận biến động ngắn hạn theo phiên.

### Example 2: SAB -5.8% Cold panic

Body (130 từ):
> Sabeco giảm sàn 5,8% phiên sáng nay sau tin Bộ Tài chính đề xuất tăng thuế tiêu thụ đặc biệt rượu bia từ 65% lên 80% giai đoạn 2027-2030, vì sao thị trường panic dù chính sách chưa thông qua?
>
> Phản ứng panic chủ yếu do lo ngại đè kéo dài đỉnh phục hồi vốn đã chậm sau Nghị định 100. Nhưng dữ liệu thực tế: **doanh thu quý 1 vẫn tăng 6,3%** so cùng kỳ nhờ tiêu dùng mang về phát triển, và lộ trình thuế giãn 4 năm cho phép SAB điều chỉnh giá bán dần. Buffer biên lợi nhuận gộp 38% vẫn dày hơn BHN. Phía sau panic: SAB đang chấp nhận hy sinh dư địa tăng giá để giữ thị phần miền Nam.
>
> Mã phù hợp NĐT giá trị chấp nhận chu kỳ phục hồi chậm 24-36 tháng, không phù hợp NĐT short-term tham gia panic.
