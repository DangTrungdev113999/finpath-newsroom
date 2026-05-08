# Insight Finalization — Bước 7.5 (V2.2)

After data fetch (Bước 3-6), Master tự verify brief.insight_hypothesis với data thực tế. 3 cases.

## Case 1 — Data CONFIRM insight (giữ nguyên)

Data fetch khớp với insight_hypothesis → giữ nguyên wording (có thể chỉnh nhẹ ngữ điệu cho tự nhiên).

**Example**:
- Brief insight_hypothesis: "VCB target 2026 +5% — defensive nhất Big 4"
- Data fetch: VCB target +5% (DB Targets), peer VPB +25%, BID +10%, CTG +12% → VCB chậm thật
- → `insight_final` = "VCB chọn defensive 2026 với target +5% — chậm nhất Big 4 — lựa chọn ưu tiên chất lượng tài sản hơn tăng trưởng"
- → `accepted_hypothesis: true`

## Case 2 — Data LỆCH NHẸ (chỉnh wording)

Data confirm core idea nhưng số/peer compare không khớp 100% → chỉnh insight cho match data thật, vẫn accept.

**Example**:
- Brief insight_hypothesis: "TCB Q1 LNTT +30% — momentum mạnh"
- Data fetch: TCB Q1 LNTT 8.900 tỷ, +22.6% YoY (không phải +30%)
- → Chỉnh: `insight_final` = "TCB Q1 LNTT 8.900 tỷ +22.6% — momentum khá tốt, vượt 25% kế hoạch quý ban điều hành đặt"
- → `accepted_hypothesis: true` (vì core idea momentum vẫn đúng)

## Case 3 — Data CONFLICT MẠNH (reject)

Data conflict fundamental với insight_hypothesis → KHÔNG viết bài, set reject.

**Example 1 — Wrong direction**:
- Brief insight_hypothesis: "VCB defensive — tăng trưởng tín dụng chậm nhất Big 4"
- Data fetch: VCB tín dụng Q1/2026 +4.1% > VPB +3.8% > BID +3.5% → VCB không phải chậm nhất
- → `accepted_hypothesis: false`
- → `Master_decision: reject_data_conflict`
- → `Master_note: "insight_data_conflict — brief nói VCB chậm nhất nhưng data Q1 cho thấy VCB +4.1% nhanh hơn VPB và BID. Cần Story Editor reframe lại angle."`

**Example 2 — Wrong magnitude**:
- Brief insight_hypothesis: "TCB tăng vốn 60% — biggest VN bank capital raise"
- Data fetch: TCB tăng vốn từ 70.862 → 113.738 tỷ (+60% đúng), nhưng peer VPB tháng 3/2026 đã tăng vốn 80%
- → `accepted_hypothesis: false`
- → `Master_decision: reject_data_conflict`
- → `Master_note: "insight_data_conflict — brief nói TCB biggest nhưng VPB +80% lớn hơn. Cần reframe angle khác."`

## Quyết định cuối

After classify into 1 of 3 cases:

```python
if case == 1 or case == 2:
    accepted_hypothesis = True
    insight_final = adjusted_or_kept_insight  # 1 câu
    proceed_to_write_article()
elif case == 3:
    accepted_hypothesis = False
    insight_final = None  # không có
    persist_master_reject_to_crawl_log(decision, note)
    return  # KHÔNG viết bài
```

## Output insight_final format

- **1 CÂU** — không 2-3 câu
- Specific (có số/tên cụ thể), không generic
- Insight type bias mua/bán nhưng không khuyến nghị (xem Rule 3)

✅ GOOD: "VCB chọn defensive 2026 với target +5% — chậm nhất Big 4 — phù hợp NĐT giá trị giữ trên 12 tháng"
❌ BAD: "VCB Q1 ổn, NĐT cân nhắc" (generic, không impact)

## Persist insight_final

- DB Generated News property `Insight_line` (text)
- Hiển thị Compare Feed cột trái header dòng `> 💡 **Insight**: ...`
