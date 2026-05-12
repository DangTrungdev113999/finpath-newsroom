# Stance Directive Handler — Master Logistics

> Loaded from `Skill: finpath-newsroom-master-logistics`. Apply khi parse brief.

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
- **medium**: 1 caveat in closing OK (vd "nếu chưa thấy sản lượng thông quan quý 2 cải thiện, scenario base case revisit")
- **low**: MUST acknowledge speculation in closing (vd "scenario phụ thuộc đường ống vận chuyển hàng xuất khẩu Mỹ duy trì sau thuế quan, chưa khẳng định")

## Examples

### Example: bullish (HAH giảm sàn nhưng nội lực OK)

Brief:
```yaml
stance_directive:
  direction: bullish
  confidence: medium
  reason: "HAH giảm sàn hôm nay nhưng Q1 lãi vẫn tăng 22%, đội tàu container hoạt động full 95% công suất, cước phí trục Á-Mỹ vẫn giữ mức 3.200 USD/TEU → panic temporary."
  key_evidence:
    - "Q1 lãi +22%"
    - "Đội tàu container chạy 95% công suất quý 1"
    - "Cước phí trục Á-Mỹ giữ 3.200 USD/TEU"
```

Body MUST:
- Opening: "Cổ phiếu HAH giảm sàn hôm nay, nhưng quý 1 lãi vẫn tăng 22%..." (bullish direction xuyên opening).
- Body: cite "Q1 lãi +22%" + "Đội tàu chạy 95% công suất" trong bullets/paragraphs.
- Closing verdict: "Mã phù hợp NĐT tích lũy giá oversold trong 12 tháng, lưu ý kiểm chứng quý 2 confirm cước phí giữ mức nền cao" (bullish + timeframe + holder action + caveat medium confidence).

Body MUST NOT:
- Mở bằng "tin xấu" / "đáng lo" (lệch direction).
- Closing "chờ xem thêm" (ba phải, violation Voice V2).
- Override sang bearish dù tìm thấy 1 negative datapoint (Voice V5 không apply override).

### Example: bearish (VOS tăng trần nhưng cước phí về vùng đáy)

Brief:
```yaml
stance_directive:
  direction: bearish
  confidence: high
  reason: "VOS tăng 6% phiên nay nhưng cước phí vận tải hàng rời (BDI) đã rơi từ 2.800 xuống 1.450 trong 3 tháng, biên lãi gộp vận tải Q1 co từ 18% xuống 9%. Đà tăng FOMO theo tin đồn hợp đồng dài hạn."
  key_evidence:
    - "Cước phí hàng rời (BDI) rơi từ 2.800 xuống 1.450 trong 3 tháng"
    - "Biên lãi gộp vận tải co từ 18% xuống 9% quý 1"
    - "Hệ số sử dụng đội tàu giảm xuống 72% quý 1"
```

Body MUST:
- Opening: acknowledge tăng 6% + flag BDI rơi (bearish direction xuyên opening dù sự kiện tăng).
- Body: cite all 3 key_evidence với mechanism reasoning.
- Closing: "Mã có rủi ro với NĐT short-term FOMO. NĐT giữ giá trị nên đợi pullback 12-18 tháng" (bearish + timeframe + holder action, confidence high → no caveat).

### Example: divergent (comparison_deep — Cảng vs Vận tải biển)

Brief:
```yaml
stance_directive:
  direction: divergent
  confidence: high
  reason: "Cảng vs vận tải biển Q1 đi 2 hướng rõ — GMD/VSC/PHP sản lượng thông quan +12% nhờ xuất khẩu VN sang Mỹ phục hồi. HAH/VOS phụ thuộc cước phí thế giới đang co theo BDI yếu."
  key_evidence:
    - "GMD sản lượng thông quan Q1 đạt 920.000 TEU, +12% so cùng kỳ"
    - "HAH biên lãi gộp Q1 co từ 22% xuống 14% theo cước phí"
    - "Xuất khẩu VN Q1 sang Mỹ +9% so cùng kỳ"
```

Body MUST explicit 2 sides:
- Winners (Cảng): cite sản lượng thông quan tăng + đường ống xuất khẩu phục hồi + biên lãi cảng ổn định
- Co-flank (Vận tải biển): cite cước phí thế giới co + biên lãi gộp co + hệ số sử dụng đội tàu giảm

Closing verdict divergent:
- "Mã cảng phù hợp NĐT giá trị giữ trên 18 tháng ưu tiên ổn định theo đường ống xuất khẩu, mã vận tải biển phù hợp NĐT chấp nhận biến động chờ chu kỳ cước phí toàn cầu phục hồi."

Verdict MUST phân loại 2 nhóm NĐT theo style — không "tùy lựa chọn" (ba phải).

## Edge cases

- Brief missing `stance_directive` object → `master_decision: reject_no_data`, `master_note: missing_stance_directive`
- `stance_directive.direction` không thuộc {bullish, bearish, divergent} → `master_decision: reject_no_data`, `master_note: invalid_stance_direction_enum`
- Data Master tra được CONFLICT với `stance_directive.direction` rõ ràng → `master_decision: reject_data_conflict`, `master_note: data_contradicts_stance_<direction>` + push back lên Story Editor (discipline 2 chiều).
- `confidence: low` nhưng Master tìm thấy data strong support → vẫn giữ confidence level từ brief, KHÔNG tự nâng (Story Editor là người set confidence dựa trên data foundation broader).
