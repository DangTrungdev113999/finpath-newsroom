# Format Examples — Good vs Bad (V4.0)

Examples illustrating 5 Rules V4.0 from SKILL.md. V4.0 rules: (1) 0% từ tiếng Anh, (2) title-as-hook, (3) body pattern (opening + bullets + closing, KHÔNG "Cần để ý" section), (4) word count 200-400 hard cap, (5) no metadata leak.

## Rule 1 — 0% từ tiếng Anh (V4.0 stricter — kể cả viết tắt)

❌ **BAD** (jargon Anh, kể cả viết tắt + parens không cứu được):
> SSI Q1/2026 margin outstanding 28.000 tỷ, market share HOSE 9,2%, AUM 180.000 tỷ. ROA 4,5%, ROE 18%.

❌ **BAD** (V3.6 style — V4.0 cấm cả parens giải thích):
> Q1/2026 SSI ghi nhận dư nợ cho vay ký quỹ (margin) 28.000 tỷ, thị phần (market share) HOSE 9,2%, tài sản quản lý (AUM) 180.000 tỷ.

✅ **GOOD** V4.0 (0% Anh, không parens):
> Q1/2026 SSI ghi nhận dư nợ cho vay ký quỹ 28.000 tỷ đồng, thị phần môi giới HOSE 9,2%, tài sản quản lý 180.000 tỷ đồng. Cùng kỳ năm trước dư nợ chỉ 22.500 tỷ — tăng 24% trong 12 tháng.

## Rule 2 — Impact-driven, bold số key

❌ **BAD** (số mồ côi, không context):
> Lợi nhuận trước thuế đạt 1.200 tỷ đồng, tăng 18% so với cùng kỳ.

✅ **GOOD** (số có context + bold):
> Lợi nhuận trước thuế SSI Q1/2026 đạt **1.200 tỷ đồng** (+18% so cùng kỳ) — vượt 22% kế hoạch quý của ban điều hành đặt ra hồi đầu năm, cho thấy đà tăng mạnh hơn dự kiến.

❌ **BAD** (bullet không bold):
> - Vốn chủ tăng từ 12.345 tỷ lên 16.500 tỷ đồng.

✅ **GOOD** (bold số key):
> - Vốn chủ sở hữu tăng từ 12.345 tỷ lên **16.500 tỷ đồng** (+34%) — SSI vượt VND 14.200 tỷ và HCM 13.800 tỷ, giành lại ngôi vốn chủ lớn nhất ngành.

## Rule 3 — Voice mạnh, không nước đôi

❌ **BAD** (nước đôi):
> Có thể SSI phù hợp NĐT giá trị, nhưng tùy thuộc thị trường. Nhà đầu tư nên cân nhắc.

❌ **BAD** (khuyến nghị cụ thể — pháp lý):
> Khuyến nghị MUA SSI mục tiêu giá 35.000 đồng.

✅ **GOOD** (insight rõ + không action):
> SSI phù hợp NĐT giá trị giữ trên 12 tháng — chấp nhận biên lãi môi giới co dần để đổi lấy vị thế đón sóng FTSE nâng hạng. KHÔNG phù hợp NĐT lướt sóng tìm đà tăng ngắn hạn.

## Rule 4 — Format V4.0 (KHÔNG nhãn, KHÔNG "Cần để ý" section)

❌ **BAD** (nhãn AI xào):
> ## Key takeaway
> SSI thận trọng
> ## Tóm lại
> NĐT giá trị nên giữ.

❌ **BAD** (V4.0 BAN heading `## Cần để ý` — caveat phải merge vào bullets hoặc closing):
> ## Cần để ý
> Q2/2026 BCTC chính thức ra giữa tháng 7 — số thị phần thực tế sẽ xác nhận hay phản bác đà tăng đang thấy.

✅ **GOOD** (closing sentence chứa caveat, không heading):
> SSI phù hợp NĐT giá trị giữ trên 12 tháng — chấp nhận biên lãi môi giới co dần để đổi lấy vị thế đón sóng FTSE nâng hạng tháng 9/2026, miễn dư nợ cho vay ký quỹ chưa chạm trần 200% vốn chủ.

✅ **GOOD** (caveat merge vào bullet substantive):
> - **Q2/2026 là điểm kiểm chứng then chốt**: báo cáo tài chính chính thức công bố giữa tháng 7 sẽ cho biết thị phần môi giới HOSE giữ được 9,2% hay tiếp tục lùi — nếu lùi dưới 9%, áp lực phát hành thêm cổ phiếu tăng vốn chủ sẽ rõ trong nửa cuối năm.

V4.0 body pattern: opening paragraph + 3-7 substantive bullets + 1 closing sentence. KHÔNG heading nào trong body Master. Skeptic append `## Góc nhìn ngược` riêng (không tính vào gates Master).

## Rule 5 — Final gate examples (CK)

✅ **Trường hợp REJECT_NO_DATA**:
- Brief: "phân tích cấu trúc danh mục tự doanh SHS Q1/2026"
- Fetch: Finpath API không có breakdown danh mục tự doanh per loại tài sản. Web search 4 keyword khác nhau ("SHS thuyết minh BCTC Q1 2026 tự doanh", "SHS danh mục cổ phiếu tự doanh Q1", "SHS báo cáo Q1 2026 FVTPL", "SHS tự doanh trái phiếu Q1") → không ra số chi tiết.
- Action: `accepted_hypothesis: false`, `Master_decision: reject_no_data`, `Master_note: data_anchor_missing — SHS chưa công bố thuyết minh BCTC Q1, không đủ neo viết bài cấu trúc tự doanh`

✅ **Trường hợp REJECT_DATA_CONFLICT**:
- Brief: "VCI mất thị phần môi giới — bị TCBS vượt mặt Q1/2026"
- Fetch dữ liệu HOSE Q1/2026: VCI 7,5% (lên từ 7,1%) > TCBS 6,8%, VCI không mất thị phần, mà tăng
- Action: `accepted_hypothesis: false`, `Master_decision: reject_data_conflict`, `Master_note: insight_data_conflict — brief nói VCI mất thị phần nhưng dữ liệu HOSE Q1 cho thấy VCI thị phần tăng từ 7,1% lên 7,5%. Cần Story Editor đổi angle khác.`

✅ **Trường hợp ACCEPT + adjust insight**:
- Brief insight_hypothesis: "SSI tăng vốn 5.000 tỷ — quy mô phát hành lớn nhất ngành 2026"
- Data confirm SSI phát hành 4.155 tỷ (không phải 5.000) nhưng vẫn là lớn nhất ngành 5 công ty đầu (peer VND 3.000 tỷ, HCM 2.500 tỷ)
- Action: `accepted_hypothesis: true`, insight_final = "SSI phát hành 4.155 tỷ — quy mô lớn nhất nhóm 5 công ty chứng khoán đầu ngành 2026 — chuẩn bị dòng vốn đón sóng FTSE nâng hạng tháng 9/2026"
