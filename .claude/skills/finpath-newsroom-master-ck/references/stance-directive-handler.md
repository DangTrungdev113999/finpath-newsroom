# Stance Directive Handler — Master CK

> Loaded from `Skill: finpath-newsroom-master-ck`. Apply khi parse brief.

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
3. **Caveat permitted in closing** nếu data nuance. Caveat phải có direction (không ba phải, see Voice V2).
4. **NEVER override stance** — Voice Rule V5 contrarian không apply để override stance_directive. Nếu data conflict stance → push back lên Story Editor (`master_decision: reject_data_conflict`).

## confidence levels

- **high**: write with conviction, no caveats trong closing
- **medium**: 1 caveat in closing OK (vd "nếu chưa thấy proof point quý 2, scenario base case revisit")
- **low**: MUST acknowledge speculation in closing (vd "scenario phụ thuộc FTSE nâng hạng đúng lịch 9/2026, chưa khẳng định")

## Examples

### Example: bullish (mã giảm sàn nhưng nội lực OK)

Brief:
```yaml
stance_directive:
  direction: bullish
  confidence: medium
  reason: "SSI giảm sàn hôm nay nhưng Q1 lãi vẫn tăng 24%, thị phần môi giới HOSE giữ top 1 ở 9,8%, không có scandal → panic temporary."
  key_evidence:
    - "Q1 lãi +24%"
    - "Thị phần HOSE Q1/2026 đạt 9,8% giữ top 1"
    - "Doanh thu ngân hàng đầu tư +35% đón FTSE 9/2026"
```

Body MUST:
- Opening: "SSI giảm sàn hôm nay, nhưng quý 1 lãi vẫn tăng 24%..." (bullish direction xuyên opening).
- Body: cite "Q1 lãi +24%" + "Doanh thu ngân hàng đầu tư +35%" trong bullets/paragraphs.
- Closing verdict: "Mã phù hợp NĐT tích lũy giá oversold trong 12 tháng, lưu ý kiểm chứng quý 2 confirm xu hướng" (bullish + timeframe + holder action + caveat medium confidence).

Body MUST NOT:
- Mở bằng "tin xấu" / "đáng lo" (lệch direction).
- Closing "chờ xem thêm" (ba phải, violation Voice V2).
- Override sang bearish dù tìm thấy 1 negative datapoint (Voice V5 không apply override).

### Example: bearish (mã tăng trần nhưng PE cao + biên co)

Brief:
```yaml
stance_directive:
  direction: bearish
  confidence: high
  reason: "VCI tăng 6% phiên nay nhưng P/E forward 22 (Big5 avg 14), biên lãi gộp môi giới co từ 38% xuống 32% Q1. Đà tăng FOMO."
  key_evidence:
    - "P/E forward 22 lần vs Big5 trung bình 14 lần"
    - "Biên lãi gộp môi giới co từ 38% xuống 32% quý 1"
    - "Thị phần HOSE giảm 0,3 điểm so quý trước"
```

Body MUST:
- Opening: acknowledge tăng 6% + flag P/E forward outlier (bearish direction xuyên opening dù sự kiện tăng).
- Body: cite all 3 key_evidence với mechanism reasoning.
- Closing: "Mã có rủi ro với NĐT short-term FOMO. NĐT giữ giá trị nên đợi pullback 12-18 tháng" (bearish + timeframe + holder action, confidence high → no caveat).

### Example: divergent (comparison_deep)

Brief:
```yaml
stance_directive:
  direction: divergent
  confidence: high
  reason: "Big5 vs nhóm nhỏ Q1 đi 2 hướng rõ — SSI/VND/VCI doanh thu ngân hàng đầu tư +35% nhờ đón FTSE 9/2026. MBS/SHS/BVS chỉ +12% YoY, phụ thuộc môi giới cá nhân biên co."
  key_evidence:
    - "Big5 doanh thu ngân hàng đầu tư +35% trung bình quý 1"
    - "MBS SHS BVS doanh thu +12% so cùng kỳ"
    - "Big5 thị phần HOSE 52,4% tăng 0,8 điểm"
```

Body MUST explicit 2 sides:
- Winners (Big5): cite tăng trưởng ngân hàng đầu tư + đường ống FTSE + năng lực bảo lãnh phát hành
- Co-flank (nhóm nhỏ): cite phụ thuộc môi giới cá nhân + biên co + thiếu vốn chủ mở rộng cho vay ký quỹ

Closing verdict divergent:
- "Mã Big5 phù hợp NĐT giá trị giữ trên 18 tháng đón FTSE nâng hạng, mã nhóm nhỏ phù hợp NĐT chấp nhận biến động chờ ngành tái hợp nhất."

Verdict MUST phân loại 2 nhóm NĐT theo style — không "tùy lựa chọn" (ba phải).

## Edge cases

- Brief missing `stance_directive` object → `master_decision: reject_no_data`, `master_note: missing_stance_directive`
- `stance_directive.direction` không thuộc {bullish, bearish, divergent} → `master_decision: reject_no_data`, `master_note: invalid_stance_direction_enum`
- Data Master tra được CONFLICT với `stance_directive.direction` rõ ràng → `master_decision: reject_data_conflict`, `master_note: data_contradicts_stance_<direction>` + push back lên Story Editor (discipline 2 chiều).
- `confidence: low` nhưng Master tìm thấy data strong support → vẫn giữ confidence level từ brief, KHÔNG tự nâng (Story Editor là người set confidence dựa trên data foundation broader).
