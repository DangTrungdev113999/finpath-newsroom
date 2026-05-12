# Format: flash_qa (100-150 từ)

> Loaded from `Skill: finpath-newsroom-master-retail`. Apply khi `format_id == "flash_qa"`.

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

≥1 bold `**...**` trong body paragraph. Highlight 1 số key (VD: `**tăng trưởng doanh thu cùng cửa hàng +12%**`).

## Verdict line

Closing MUST có verdict cho NĐT phân loại (Voice Rule 3):
- Tốt: "Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động ngắn hạn"
- Xấu: "Cần thêm thông tin để đánh giá" (ba phải, fail Voice Rule 2)

## Examples Retail sector

### Example 1: MWG +6.5% Hot — Bách Hoá Xanh có lãi

Body (135 từ):
> Thế Giới Di Động tăng kịch trần 6,5% phiên sáng 12/5 sau khi công bố Bách Hoá Xanh chính thức có lãi quý đầu tiên, vì sao thị trường phản ứng mạnh?
>
> Bách Hoá Xanh đóng góp 245 tỷ lãi sau thuế quý 1 sau 6 năm lỗ liên tiếp, biên lợi nhuận gộp nâng từ 22% lên 25,5%. Chuỗi cửa hàng giảm từ 2.140 xuống 1.700 sau đợt tinh giản 2023, **doanh thu trung bình mỗi cửa hàng tăng 28%** so cùng kỳ. Mảng điện thoại Thế Giới Di Động vẫn co 4% do thị trường thay máy chậm, nhưng cả tập đoàn lãi tăng 52% nhờ đòn bẩy lưu lượng khách rổ thực phẩm cao hơn rổ hàng điện máy.
>
> Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động khi chu kỳ điện thoại còn yếu.

### Example 2: PNJ -5.2% Cold — giá vàng quá cao

Body (128 từ):
> Phú Nhuận giảm 5,2% phiên sáng 12/5 sau tin giá vàng SJC chạm 92 triệu đồng mỗi lượng, vì sao thị trường lo dù lãi quý 1 vẫn tăng?
>
> Lo ngại tập trung ở sản lượng trang sức quý 2 khi giá vàng nguyên liệu vượt vùng kháng cự, nhưng dữ liệu thực: **doanh thu trang sức quý 1 vẫn tăng 18%** so cùng kỳ, lưu lượng khách Phú Nhuận giữ ổn định, biên lợi nhuận gộp 18,4% chỉ co nhẹ 30 điểm cơ bản. Phú Nhuận đã giảm tỷ trọng vàng miếng từ 32% xuống 24% trong 12 tháng để giảm phụ thuộc chu kỳ giá vàng, đẩy mạnh trang sức cao cấp tỷ suất sinh lời tốt hơn.
>
> Mã phù hợp NĐT giá trị tin chiến lược tái cấu trúc, không phù hợp NĐT ngắn hạn tham gia panic.
