# Stance Directive Handler — Master BĐS

> Loaded from `Skill: finpath-newsroom-master-bds`. Apply khi parse brief.

Cross-cutting rule áp dụng toàn 4 format. Pair với `voice-layer-rules.md` V1 (Stance required).

## Schema

```yaml
stance_directive:
  direction: "bullish" | "bearish" | "divergent"
  confidence: "high" | "medium" | "low"
  reason: |
    Free-form prose 1-3 câu Vietnamese.
  key_evidence:
    - "..."
    - "..."
```

## Receive

Parse from `brief_json[deep_question_options[chosen_idx][stance_directive]]`. Required object — fail-loud nếu missing keys.

Schema invalid (thiếu direction/confidence/reason/key_evidence) → `master_decision: reject_no_data`, `master_note: invalid_stance_directive_schema`.

## Apply rules

1. **Body MUST follow direction**. Opening + verdict cùng hướng `direction`.
2. **Body MUST cite ≥1 evidence** từ `key_evidence` array (preserve wording where possible).
3. **Caveat permitted in closing** nếu data nuance. Caveat phải có direction (không ba phải, see Voice V2). BĐS đặc biệt cho phép caveat lịch sử chu kỳ trầm (2008/2011-2013/2022) — caveat này KHÔNG phải hedging.
4. **NEVER override stance** — Voice Rule V5 contrarian không apply để override stance_directive. Nếu data conflict stance → push back lên Story Editor (`master_decision: reject_data_conflict`).

## confidence levels

- **high**: write with conviction, no caveats trong closing (BĐS ngoại lệ: vẫn cho phép caveat lịch sử chu kỳ — không tính là hedging)
- **medium**: 1 caveat in closing OK (vd "nếu chưa thấy giấy phép bán hàng phase 1 Aqua City, scenario base case revisit")
- **low**: MUST acknowledge speculation in closing (vd "scenario phụ thuộc pháp lý Aqua City hoàn tất 2026, chưa khẳng định")

## Examples

### Example: bullish (mã giảm sàn nhưng dự án pháp lý sạch)

Brief:
```yaml
stance_directive:
  direction: bullish
  confidence: medium
  reason: "VHM giảm sàn hôm nay nhưng Q1 doanh số bán trước +28% nhờ Ocean City phase 2 pháp lý sạch, không có scandal → panic temporary."
  key_evidence:
    - "Q1 doanh số bán trước +28% so cùng kỳ"
    - "Ocean City phase 2 pháp lý sạch toàn bộ"
    - "Tỷ lệ hấp thụ phân khúc trung-cao cấp Hà Nội Q1 lên 68% từ đáy 32% năm 2023"
```

Body MUST:
- Opening: "Vinhomes giảm sàn hôm nay, nhưng quý 1 doanh số bán trước vẫn tăng 28%..." (bullish direction xuyên opening).
- Body: cite "Doanh số bán trước +28%" + "Ocean City phase 2 pháp lý sạch" trong bullets/paragraphs.
- Closing verdict: "Mã phù hợp NĐT tích lũy giá oversold giữ trên 24 tháng, lưu ý kiểm chứng quý 2 confirm xu hướng, lịch sử ngành 3 chu kỳ trầm có thể lặp nếu lãi suất siết bất ngờ" (bullish + timeframe + holder action + caveat medium + BĐS caveat lịch sử).

Body MUST NOT:
- Mở bằng "tin xấu" / "đáng lo" (lệch direction).
- Closing "chờ xem thêm" (ba phải, violation Voice V2).
- Override sang bearish dù tìm thấy 1 negative datapoint (Voice V5 không apply override).

### Example: bearish (mã tăng nhưng pháp lý vẫn tắc + trái phiếu áp lực)

Brief:
```yaml
stance_directive:
  direction: bearish
  confidence: high
  reason: "NVL tăng 7% phiên nay nhưng doanh số chờ ghi nhận 60.000 tỷ giấy chỉ chuyển đổi 12% do Aqua City pháp lý tắc, 5.800 tỷ trái phiếu Q2/2026 chưa rõ phương án. Đà tăng FOMO."
  key_evidence:
    - "Doanh số chờ ghi nhận 60.000 tỷ chuyển đổi thực chỉ 12%"
    - "5.800 tỷ trái phiếu doanh nghiệp đáo hạn Q2/2026 chưa rõ phương án"
    - "Ban điều hành cam kết Aqua City pháp lý sắp xong từ 2022, 4 năm chưa thành"
```

Body MUST:
- Opening: acknowledge tăng 7% + flag rủi ro Aqua City (bearish direction xuyên opening dù sự kiện tăng).
- Body: cite all 3 key_evidence với mechanism reasoning, neo lịch sử "pháp lý sắp xong" cam kết không đúng hẹn.
- Closing: "Mã có rủi ro với NĐT short-term FOMO. NĐT giá trị nên đợi proof point giấy phép bán hàng phase 1 Aqua City 2026, lịch sử ngành 2008-2011 và 2022-2023 từng vỡ nợ chu kỳ" (bearish + timeframe + holder action, confidence high → BĐS caveat lịch sử OK).

### Example: divergent (comparison_deep 4 mã VHM/KDH/DXG/NVL)

Brief:
```yaml
stance_directive:
  direction: divergent
  confidence: high
  reason: "VHM/KDH pháp lý sạch + biên lợi nhuận cao, NVL/DXG còn vướng tái cơ cấu trái phiếu doanh nghiệp. Phân hóa rõ rệt 2026."
  key_evidence:
    - "VHM doanh số bán trước Q1 18.500 tỷ + KDH biên lợi nhuận gộp 56% dẫn đầu"
    - "DXG hoàn tất tái cơ cấu cuối 2025, dư nợ trái phiếu xuống 1.800 tỷ"
    - "NVL doanh số chờ ghi nhận 60.000 tỷ chuyển đổi thực chỉ 12% do Aqua City"
```

Body MUST explicit 2 sides:
- Winners (VHM/KDH): cite doanh số bán trước + biên lợi nhuận + quỹ đất pháp lý sạch + tỷ lệ tổng nợ trên vốn chủ thấp
- Co-flank (NVL/DXG): cite doanh số chờ ghi nhận chuyển đổi thấp + dư nợ trái phiếu doanh nghiệp còn căng + lịch sử cam kết pháp lý không đúng hẹn

Closing verdict divergent:
- "Mã VHM/KDH phù hợp NĐT giá trị giữ trên 24 tháng đón chu kỳ phục hồi, mã DXG phù hợp NĐT chấp nhận biến động chờ chu kỳ rõ ràng, NVL chỉ phù hợp NĐT tin tái cơ cấu hoàn tất cuối 2026 + chấp nhận lịch sử ngành 3 chu kỳ trầm có thể lặp."

Verdict MUST phân loại 2 (hoặc nhiều) nhóm NĐT theo style — không "tùy lựa chọn" (ba phải).

## Edge cases

- Brief missing `stance_directive` object → `master_decision: reject_no_data`, `master_note: missing_stance_directive`
- `stance_directive.direction` không thuộc {bullish, bearish, divergent} → `master_decision: reject_no_data`, `master_note: invalid_stance_direction_enum`
- Data Master tra được CONFLICT với `stance_directive.direction` rõ ràng (vd brief bullish NVL nhưng Aqua City vẫn tắc pháp lý) → `master_decision: reject_data_conflict`, `master_note: data_contradicts_stance_<direction>` + push back lên Story Editor (discipline 2 chiều).
- `confidence: low` nhưng Master tìm thấy data strong support → vẫn giữ confidence level từ brief, KHÔNG tự nâng (Story Editor là người set confidence dựa trên data foundation broader).
