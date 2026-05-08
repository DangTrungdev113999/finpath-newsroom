# Format Examples — Good vs Bad

Examples illustrating 5 Rules from SKILL.md.

## Rule 1 — Tiếng Việt đọc-cái-hiểu-luôn

❌ **BAD** (jargon không giải thích):
> VCB Q1/2026 NIM 3.2%, NPL 1.05%, CASA 31%, LDR 80%. ROA 1.8%, ROE 22%.

✅ **GOOD** (jargon giải thích lần đầu):
> Q1/2026 VCB ghi nhận biên lợi nhuận lãi vay (NIM — chênh lệch giữa lãi suất cho vay và chi phí huy động) 3.2%, tỷ lệ nợ xấu (NPL) 1.05%, tỷ lệ tiền gửi không kỳ hạn (CASA) 31%. Cùng kỳ năm trước NIM chỉ 2.9% — đà cải thiện rõ.

## Rule 2 — Impact-driven, bold số key

❌ **BAD** (orphan number):
> LNTT đạt 8.900 tỷ đồng, tăng 22.6% so với cùng kỳ.

✅ **GOOD** (số có context + bold):
> LNTT TCB Q1/2026 đạt **8.900 tỷ đồng** (+22.6% YoY) — vượt 25% kế hoạch quý của ban điều hành đặt ra hồi đầu năm, cho thấy momentum mạnh hơn dự kiến.

❌ **BAD** (bullet không bold):
> - Vốn điều lệ tăng từ 70.862 tỷ lên 113.738 tỷ đồng.

✅ **GOOD** (bold số key):
> - Vốn điều lệ tăng từ 70.862 tỷ lên **113.738 tỷ đồng** (+60%) — TCB bây giờ là ngân hàng tư nhân vốn lớn nhất.

## Rule 3 — Voice mạnh, không nước đôi

❌ **BAD** (nước đôi):
> Có thể VCB phù hợp NĐT giá trị, nhưng tùy thuộc thị trường. Nhà đầu tư nên cân nhắc.

❌ **BAD** (khuyến nghị cụ thể — pháp lý):
> Khuyến nghị MUA VCB target giá 110.000 đồng.

✅ **GOOD** (insight rõ + không action):
> VCB phù hợp NĐT giá trị giữ trên 12 tháng — chấp nhận tăng trưởng chậm để đổi lấy chất lượng tài sản. KHÔNG phù hợp NĐT lướt sóng tìm momentum.

## Rule 4 — Format ngắn, không nhãn

❌ **BAD** (nhãn AI xào):
> ## Key takeaway
> VCB defensive
> ## Tóm lại
> NĐT giá trị nên giữ.

✅ **GOOD** (chốt insight tự nhiên):
> Tín hiệu rõ: VCB chọn defensive thay vì momentum. Đây là lựa chọn của ngân hàng to nhất ưu tiên chất lượng tài sản — phù hợp NĐT giá trị giữ dài, không phù hợp NĐT lướt sóng.

✅ **GOOD** với "Cần để ý" optional:
> ## Cần để ý
> Q2/2026 BCTC chính thức ra giữa tháng 7 — số NIM thực tế sẽ confirm hay reject momentum đang thấy. Nếu NIM Q2 < Q1 → flag tín hiệu suy yếu.

## Rule 5 — Final gate examples

✅ **Trường hợp REJECT_NO_DATA**:
- Brief: "phân tích CFS TCB Q1/2026"
- Fetch DB: TCB Quarter row Q1/2026 có 5/6 CFS fields NULL
- Action: `accepted_hypothesis: false`, `Master_decision: reject_no_data`, `Master_note: data_anchor_missing — 5/6 CFS keys null cho TCB Q1/2026, không đủ anchor viết bài CFS`

✅ **Trường hợp REJECT_DATA_CONFLICT**:
- Brief: "VCB defensive — tăng trưởng chậm nhất Big 4"
- Fetch DB: VCB tín dụng Q1/2026 +4.1% > VPB +3.8% > BID +3.5% → VCB không phải chậm nhất
- Action: `accepted_hypothesis: false`, `Master_decision: reject_data_conflict`, `Master_note: insight_data_conflict — brief nói VCB chậm nhất nhưng data Q1 cho thấy VCB +4.1% nhanh hơn VPB và BID`

✅ **Trường hợp ACCEPT + adjust insight (Bước 7.5 case 2)**:
- Brief insight_hypothesis: "VCB target 2026 +5%, dự báo cẩn trọng"
- Data confirm target 5% nhưng peer Big 4 trung bình 12% → VCB conservative thật
- Action: `accepted_hypothesis: true`, insight_final = "VCB chọn defensive 2026 với target +5% — chậm nhất Big 4 — lựa chọn ưu tiên chất lượng hơn tăng trưởng"
