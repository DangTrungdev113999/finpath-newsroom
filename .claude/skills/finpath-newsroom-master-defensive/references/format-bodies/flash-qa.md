# Format: flash_qa (100-150 từ)

> Loaded from `Skill: finpath-newsroom-master-defensive`. Apply khi `format_id == "flash_qa"`.

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

≥1 bold `**...**` trong body paragraph. Highlight 1 số key (VD: `**doanh thu định kỳ +18%**`).

## Verdict line

Closing MUST có verdict cho NĐT phân loại (Voice Rule 3):
- Tốt: "Mã phù hợp NĐT giá trị giữ trên 12 tháng, ưu tiên dòng tiền ổn định"
- Xấu: "Cần thêm thông tin để đánh giá" (ba phải, fail Voice Rule 2)

## Examples Defensive sector (Tech / Utility / Pharma mixed)

### Example 1: FPT +5.2% Hot — Tech subsector

Body (135 từ):
> FPT tăng kịch trần 5,2% phiên sáng 12/5 sau khi công bố ký hợp đồng gia công công nghệ với khách hàng Mỹ trị giá 180 triệu USD trong 5 năm, vì sao thị trường phản ứng mạnh đến vậy?
>
> Hợp đồng đẩy đơn hàng tồn đọng của FPT Software lên **2,4 tỷ USD**, tương đương 14 tháng doanh thu chạy. Biên lợi nhuận mảng gia công Mỹ trung bình **22%** cao hơn Nhật **18%**, đẩy biên hợp nhất tăng 50 điểm cơ bản. Phía sau con số: FPT đang ăn được làn sóng thuê nước ngoài AI từ ngân hàng Mỹ chuyển từ Ấn Độ sang Đông Nam Á, không phải sự kiện một lần.
>
> Mã phù hợp NĐT giá trị giữ trên 24 tháng, ưu tiên dòng tiền định kỳ ổn định từ outsourcing.

### Example 2: REE -4.8% Cold — Utility subsector

Body (130 từ):
> REE giảm sàn 4,8% sáng nay sau khi công bố cổ tức 2026 chỉ 16% so với 22% năm trước, vì sao thị trường panic dù lãi quý 1 vẫn tăng?
>
> Phản ứng tiêu cực chủ yếu vì lợi suất trái phiếu chính phủ 10 năm vừa nhảy lên 5,8%, tỷ suất cổ tức REE giảm xuống **2,1%** kém hấp dẫn hơn. Thực tế dữ liệu: cắt cổ tức để giữ tiền đầu tư mảng năng lượng tái tạo 1.800 MW giai đoạn 2026-2028. Phía sau panic: REE đang đánh đổi cổ tức ngắn hạn lấy tăng trưởng tài sản dài hạn, không phải kinh doanh xấu đi.
>
> Mã phù hợp NĐT giá trị giữ 24-36 tháng tin chu kỳ năng lượng tái tạo, không phù hợp NĐT thu nhập cổ tức ngắn hạn.
