# Format: flash_qa (100-150 từ)

> Loaded from `Skill: finpath-newsroom-master-bds`. Apply khi `format_id == "flash_qa"`.

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

≥1 bold `**...**` trong body paragraph. Highlight 1 số key (vd `**doanh số bán trước +28%**`).

## Verdict line

Closing MUST có verdict cho NĐT phân loại (Voice Rule 3):
- Tốt: "Mã phù hợp NĐT giá trị giữ trên 18 tháng, chấp nhận biến động ngắn hạn"
- Xấu: "Cần thêm thông tin để đánh giá" (ba phải, fail Voice Rule 2)

Voice BĐS cẩn trọng — verdict luôn nhắc context chu kỳ (ngành đã trầm 2008/2011-2013/2022), không bull thuần.

## Examples BĐS sector

### Example 1: VHM +5.4% Hot

Title: `VHM tăng 5,4% sau tin bàn giao Ocean City: vì sao thị trường ngả mạnh?`

Body (132 từ):
> Vinhomes tăng 5,4% phiên sáng 12/5 sau khi công bố bàn giao 8.500 căn Ocean City quý 1 với doanh thu ghi nhận **30.200 tỷ**, vì sao thị trường phản ứng mạnh đến vậy?
>
> Lãi quý 1 ghi nhận **5.200 tỷ** tăng 18% so cùng kỳ, lợi nhuận chủ yếu từ phase 2 Ocean City đã pháp lý sạch. Doanh số bán trước Q1 thêm **18.500 tỷ** nhờ phân khúc trung-cao cấp Hà Nội tiếp tục bán tốt. Phía sau con số: VHM đang ăn được phần demand phục hồi của phân khúc pháp lý sạch, nhưng quý 2 doanh thu sẽ trầm do không có dự án bàn giao lớn (mẫu hình doanh thu lồi theo quý).
>
> Mã phù hợp NĐT giá trị giữ trên 18 tháng, chấp nhận quý 2 doanh thu trầm theo chu kỳ bàn giao.

### Example 2: NVL -6.7% Cold panic

Title: `NVL giảm sàn 6,7% sau tin trái phiếu Q2: panic có chính đáng không?`

Body (138 từ):
> Novaland giảm sàn 6,7% phiên sáng nay sau tin 5.800 tỷ trái phiếu doanh nghiệp đáo hạn Q2/2026 chưa rõ phương án, vì sao thị trường panic dù NVL đã rollover 2023-2025?
>
> Phản ứng panic chủ yếu do lo ngại lặp lại pattern 2022. Nhưng dữ liệu thực tế: **dư nợ trái phiếu NVL từ 62.757 tỷ cuối 2022 xuống 38.400 tỷ cuối 2025**, phần lớn đã rollover thoả thuận với trái chủ. 5.800 tỷ Q2 là phần còn lại theo lịch tái cơ cấu hoàn thành cuối 2026. Aqua City vẫn vướng pháp lý — doanh số chờ ghi nhận chuyển đổi chỉ 12%. Phía sau panic: NVL đang trong giai đoạn cuối tái cơ cấu, không phải khủng hoảng mới.
>
> Mã có rủi ro với NĐT short-term FOMO; NĐT giá trị nên đợi proof point pháp lý Aqua City.
