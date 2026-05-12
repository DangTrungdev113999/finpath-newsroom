# Format: flash_qa (100-150 từ)

> Loaded from `Skill: finpath-newsroom-master-seafood`. Apply khi `format_id == "flash_qa"`.

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

≥1 bold `**...**` trong body paragraph. Highlight 1 số key (vd `**doanh thu tăng 18%**`, `**biên lợi nhuận gộp 22%**`).

## Verdict line

Closing MUST có verdict cho NĐT phân loại (Voice Rule 3):
- Tốt: "Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động ngắn hạn"
- Xấu: "Cần thêm thông tin để đánh giá" (ba phải, fail Voice Rule 2)

## Examples Thuỷ sản sector

### Example 1: VHC +6.5% Hot

Body (132 từ):
> Vĩnh Hoàn tăng kịch trần 6,5% trong phiên 12/5 sau khi công bố sản lượng xuất khẩu cá tra sang Mỹ tháng 4 vượt 18% so cùng kỳ, vì sao thị trường phản ứng mạnh đến vậy?
>
> Sản lượng tăng vì khách hàng Mỹ kênh hiện đại bắt đầu đặt hàng lại sau giai đoạn giải phóng tồn kho 2024. **Giá bán trung bình đạt 3,4 đô-la mỗi kg**, nhích nhẹ so quý 1 nhờ hợp đồng mới ký từ mùa Chay châu Âu. Biên lợi nhuận gộp ước tính nới rộng 2 điểm phần trăm so quý trước. Phía sau con số: VHC đang ăn được phần ưu thế thuế chống bán phá giá Mỹ kỳ rà soát mới hạ mức.
>
> Mã phù hợp NĐT giá trị giữ trên 12 tháng, chấp nhận biến động theo chu kỳ xuất khẩu Mỹ.

### Example 2: MPC -6.8% Cold panic

Body (128 từ):
> Minh Phú giảm sàn 6,8% phiên sáng nay sau tin Ecuador nâng sản lượng tôm xuất Mỹ thêm 22% so cùng kỳ, vì sao thị trường panic dù doanh thu MPC quý 1 vẫn tăng?
>
> Phản ứng panic do lo ngại Ecuador đẩy giá tôm thẻ Mỹ xuống thêm. Nhưng dữ liệu thực tế: **giá tôm nguyên liệu khu vực Đông Nam Á đã giảm 12%** từ đầu năm, biên lợi nhuận gộp MPC quý 1 nới từ 4,5% lên 6,8%. Hợp đồng Nhật Bản kênh cao cấp giữ giá tốt. Phía sau panic: MPC đang chấp nhận hy sinh thị phần Mỹ tầm trung để giữ mảng Nhật giá tốt hơn.
>
> Mã phù hợp NĐT giá trị tin chiến lược đa thị trường, không phù hợp NĐT ngắn hạn lo ngại cạnh tranh khu vực.
