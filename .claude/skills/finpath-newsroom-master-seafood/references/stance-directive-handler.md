# Stance Directive Handler — Master Thuỷ sản

> Loaded from `Skill: finpath-newsroom-master-seafood`. Apply khi parse brief.

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
- **low**: MUST acknowledge speculation in closing (vd "scenario phụ thuộc room đợt 2 NHNN, chưa khẳng định")

## Examples

### Example: bullish (mã giảm sàn nhưng nội lực OK)

Brief:
```yaml
stance_directive:
  direction: bullish
  confidence: medium
  reason: "Mã giảm sàn hôm nay nhưng Q1 lãi vẫn tăng 17%, ROA stable, không có scandal → panic temporary."
  key_evidence:
    - "Q1 lãi +17%"
    - "Không có scandal cụ thể trên truyền thông tài chính"
    - "Sector cycle vẫn up nhờ NHNN nới lỏng"
```

Body MUST:
- Opening: "Cổ phiếu X giảm sàn hôm nay, nhưng quý 1 lãi vẫn tăng 17%..." (bullish direction xuyên opening).
- Body: cite "Q1 lãi +17%" + "Sector cycle vẫn up" trong bullets/paragraphs.
- Closing verdict: "Mã phù hợp NĐT tích lũy giá oversold trong 12 tháng, lưu ý kiểm chứng quý 2 confirm xu hướng" (bullish + timeframe + holder action + caveat medium confidence).

Body MUST NOT:
- Mở bằng "tin xấu" / "đáng lo" (lệch direction).
- Closing "chờ xem thêm" (ba phải, violation Voice V2).
- Override sang bearish dù tìm thấy 1 negative datapoint (Voice V5 không apply override).

### Example: bearish (mã tăng trần nhưng PE cao + earnings yếu)

Brief:
```yaml
stance_directive:
  direction: bearish
  confidence: high
  reason: "Mã tăng 6% phiên nay nhưng PE forward 18 (Big4 avg 10), NIM co từ 3.5% xuống 2.9% Q1. Đà tăng FOMO."
  key_evidence:
    - "PE forward 18 lần vs Big4 trung bình 10 lần"
    - "Biên lãi vay co từ 3,5% xuống 2,9% quý 1"
    - "Tín dụng quý 1 chỉ 1,8% lũy kế năm"
```

Body MUST:
- Opening: acknowledge tăng 6% + flag PE forward outlier (bearish direction xuyên opening dù sự kiện tăng).
- Body: cite all 3 key_evidence với mechanism reasoning.
- Closing: "Mã có rủi ro với NĐT short-term FOMO. NĐT giữ giá trị nên đợi pullback 12-18 tháng" (bearish + timeframe + holder action, confidence high → no caveat).

### Example: divergent (comparison_deep)

Brief:
```yaml
stance_directive:
  direction: divergent
  confidence: high
  reason: "Big4 vs tư nhân Q1 đi 2 hướng rõ — VCB/CTG/BID growth 4%+ nhờ trial credit. Tư nhân TCB/MBB co lại 1.8% YTD."
  key_evidence:
    - "Big4 tín dụng tăng 4,3% trung bình quý 1"
    - "TCB tăng 1,8% lũy kế năm"
    - "BID room cấp đợt 1 +28%"
```

Body MUST explicit 2 sides:
- Winners (Big4): cite tăng trưởng + room + biên lãi vay nới rộng
- Co-flank (tư nhân lớn): cite room dùng <30% + chiến lược giữ chỗ chờ chất lượng khách hàng

Closing verdict divergent:
- "Mã Big4 phù hợp NĐT giá trị giữ trên 18 tháng ưu tiên ổn định, mã tư nhân top phù hợp NĐT chấp nhận biến động chờ tăng trưởng nửa cuối năm."

Verdict MUST phân loại 2 nhóm NĐT theo style — không "tùy lựa chọn" (ba phải).

## Edge cases

- Brief missing `stance_directive` object → `master_decision: reject_no_data`, `master_note: missing_stance_directive`
- `stance_directive.direction` không thuộc {bullish, bearish, divergent} → `master_decision: reject_no_data`, `master_note: invalid_stance_direction_enum`
- Data Master tra được CONFLICT với `stance_directive.direction` rõ ràng → `master_decision: reject_data_conflict`, `master_note: data_contradicts_stance_<direction>` + push back lên Story Editor (discipline 2 chiều).
- `confidence: low` nhưng Master tìm thấy data strong support → vẫn giữ confidence level từ brief, KHÔNG tự nâng (Story Editor là người set confidence dựa trên data foundation broader).
