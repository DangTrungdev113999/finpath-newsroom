# Stance Directive Handler — Master Apparel

> Loaded from `Skill: finpath-newsroom-master-apparel`. Apply khi parse brief.

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
- **medium**: 1 caveat in closing OK (vd "nếu USD/VND chững lại nửa cuối năm, biên gộp sẽ revisit")
- **low**: MUST acknowledge speculation in closing (vd "scenario phụ thuộc đơn Q3 từ Costco — chưa khẳng định")

## Examples Apparel sector

### Example: bullish (MSH recovery sau crash 2022-2023)

Brief:
```yaml
stance_directive:
  direction: bullish
  confidence: medium
  reason: "MSH Q4/2024 ghi nhận đơn hàng đã chốt đến Q2/2025, biên lãi gộp về 11% sau đáy 8% năm 2023. Khách Nike/Columbia/GAP tái nhập đơn rõ."
  key_evidence:
    - "Sổ đơn hàng MSH đến Q2/2025 đã chốt"
    - "Biên lãi gộp MSH 11% Q4/2024 (vs đáy 8% năm 2023)"
    - "Đơn từ Nike + Columbia tăng so với 2023"
```

Body MUST:
- Opening: "May Sông Hồng công bố đã chốt đơn hàng đến giữa năm 2025..." (bullish direction xuyên opening).
- Body: cite "đơn hàng đến Q2/2025" + "biên lãi gộp 11% từ đáy 8%" + "đơn Nike/Columbia tái nhập" trong bullets/paragraphs.
- Closing verdict: "Mã phù hợp NĐT giá trị giữ trên 12 tháng, ưu tiên doanh nghiệp có khách hàng phổ thông phục hồi sớm — caveat: nếu USD/VND chững lại nửa cuối năm, biên gộp sẽ revisit" (bullish + timeframe + holder action + caveat medium confidence).

Body MUST NOT:
- Mở bằng "lo ngại" / "thận trọng" (lệch direction).
- Closing "chờ xem thêm tín hiệu" (ba phải, violation Voice V2).
- Override sang bearish dù phát hiện 1 datapoint USD/VND yếu (Voice V5 không apply override).

### Example: bearish (TCM 2022-2023 inventory crash analog hiện tại)

Brief:
```yaml
stance_directive:
  direction: bearish
  confidence: high
  reason: "Tồn kho bán lẻ Mỹ Q1 lại cao bất thường, Macy's/Target báo dư hàng. TCM 2024 biên lãi gộp mới về 14% (vs đỉnh 18% 2021), nay rủi ro lùi tiếp về vùng 10-12% nếu khách hủy đơn."
  key_evidence:
    - "Tồn kho bán lẻ Mỹ tháng 3/2026 tăng 12% so với tháng 12/2025"
    - "TCM biên lãi gộp Q4/2025 ở 14%, chưa về đỉnh chu kỳ"
    - "TCM 2022-2023 đối chiếu: khi tồn kho bán lẻ Mỹ vượt ngưỡng, doanh thu TCM giảm 25% trong 2 quý"
```

Body MUST:
- Opening: acknowledge tin tích cực gần đây (vd Q4 vừa rồi tăng nhẹ) + flag tồn kho bán lẻ Mỹ là rủi ro chính (bearish direction xuyên opening dù sự kiện hiện tại bình thường).
- Body: cite all 3 key_evidence với mechanism reasoning. Đặc biệt cite analog 2022-2023 — chu kỳ trước crash mất 2 quý lan từ tồn kho sang doanh thu.
- Closing: "Mã có rủi ro với NĐT lướt sóng theo số quý 4. NĐT giá trị nên đợi giá hạ 12 tháng để theo dõi tồn kho bán lẻ Mỹ về dưới ngưỡng" (bearish + timeframe + holder action, confidence high → no caveat).

### Example: divergent (Sợi vs may mặc, hoặc TCM tích hợp dọc vs MSH/TNG thuần may)

Brief:
```yaml
stance_directive:
  direction: divergent
  confidence: high
  reason: "Giá bông Cotton A Index quý 1/2026 giảm 18%, mảng sợi TCM bị kẹp giá (sợi tự sản xuất đắt hơn vải Trung Quốc). Ngược lại MSH/TNG mua vải Trung Quốc giá rẻ, biên gộp nới rộng. Phân hoá rõ giữa tích hợp dọc và thuần may."
  key_evidence:
    - "Giá bông Cotton A Index từ 95 USD/kg xuống 78 USD/kg trong Q1"
    - "TCM mảng sợi biên gộp Q1 ước co từ 8% xuống 4-5%"
    - "MSH biên gộp Q1 ước nới từ 11% lên 13% nhờ vải Trung Quốc rẻ"
```

Body MUST explicit 2 sides:
- Phe co (TCM tích hợp dọc): cite mảng sợi bị kẹp giá khi bông giảm vì vải Trung Quốc rẻ hơn vải tự dệt
- Phe nới (MSH/TNG thuần may): cite vải Trung Quốc rẻ làm giảm giá vốn, biên gộp nới rộng

Closing verdict divergent:
- "Mã MSH/TNG phù hợp NĐT giá trị giữ trên 12 tháng chờ biên gộp xác nhận quý 2, mã TCM phù hợp NĐT chấp nhận biến động quý 1 chờ mảng may mặc bù cho mảng sợi."

Verdict MUST phân loại 2 nhóm NĐT theo style — không "tùy lựa chọn" (ba phải).

## Edge cases

- Brief missing `stance_directive` object → `master_decision: reject_no_data`, `master_note: missing_stance_directive`
- `stance_directive.direction` không thuộc {bullish, bearish, divergent} → `master_decision: reject_no_data`, `master_note: invalid_stance_direction_enum`
- Data Master tra được CONFLICT với `stance_directive.direction` rõ ràng → `master_decision: reject_data_conflict`, `master_note: data_contradicts_stance_<direction>` + push back lên Story Editor (discipline 2 chiều).
- `confidence: low` nhưng Master tìm thấy data strong support → vẫn giữ confidence level từ brief, KHÔNG tự nâng (Story Editor là người set confidence dựa trên data foundation broader).
