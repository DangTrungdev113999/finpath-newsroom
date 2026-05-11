# Compare Feed Prepend — Layout V4.0 (BĐS)

Compare Feed page render từ SQLite `data/pipeline.db` → output `output/compare-feed/<TICKER>-<batch_id>.md` + web React render.

## Position
**Newest-first**: section bài mới prepend vào TOP page, trên section bài cũ.

## Header (full width, 2 dòng)

```markdown
# 🏠 [Tiêu đề bài full]
*🕐 Crawled DD/MM/YYYY HH:MM*
```

Icon sector: 🏦 Bank | 📈 CK | 🏠 BĐS

## Layout 2 cột

```markdown
<columns>
<column>
[Cột TRÁI — bài AI viết lại]
</column>
<column>
[Cột PHẢI — raw + meta]
</column>
</columns>
```

## Cột TRÁI — bài AI viết lại (V4.0 pattern)

```markdown
## ✍️ Bài AI viết lại · [N từ]

> 💡 **Insight**: [insight_final 1 câu — copy từ row.Insight_line]

[Opening paragraph ≥30 từ — sự kiện + tension/setup, có thể end với câu hỏi]

- **Bold keypoint 1**: substantive bullet ≥20 từ với connector + mechanism
- **Bold keypoint 2**: bullet ≥20 từ
- **Bold keypoint 3**: bullet ≥20 từ
- ... up to 7 bullets

[Closing — 1 câu phân loại nhà đầu tư, caveat merge vào nếu có]

## Góc nhìn ngược
[Skeptic append sau publish — 100-300 từ bullet]

<details>
<summary>📋 Pipeline log</summary>
[Step 1-6 chi tiết — see references/pipeline-log-format.md]
</details>
```

⚠️ **V4.0 BAN heading `## Cần để ý`** — caveat phải merge vào bullet substantive HOẶC closing sentence. Body Master KHÔNG được có bất kỳ heading nào ngoài body chính (opening + bullets + closing). Skeptic append `## Góc nhìn ngược` riêng (không tính vào gates Master).

## Cột PHẢI — raw text + meta

```markdown
## 📰 Raw text gốc · [M từ]

**[Title gốc full]**
*Nguồn: domain.vn — DD/MM/YYYY*

### 🎯 Cách viết & lý do chọn
- **Vì sao chọn bài này**: [brief.why_chosen_narrative — Story Editor judgment]
- **Hướng đi**: [brief.angle_label + angle_narrative]
- **Vì sao chọn hướng này**: [brief.why_chosen_narrative]
- **Vì sao chọn nguồn này**: [brief.source_rationale]
- **Câu hỏi đào sâu đã pick**: [deep_question_options[chosen_question_idx].question]
- **Vì sao pick câu này**: [chosen_pick_reason narrative tiếng Việt]

<details>
<summary>📊 Crawl funnel — đã search N nguồn, tìm M tin, chọn 1 published, X rejected (click để xem)</summary>

✅ **Published (1 bài)**
- **[Nguồn]** — [DD/MM/YYYY HH:MM] — "[Title]" (PRIMARY source)

❌ **Editor V1 reject (Y bài)**
- **[Nguồn]** — [DD/MM/YYYY] — "[Title]" — `[reject_reason]`: [Editor_V1_note]

❌ **Story Editor V4 reject (Z bài)**
- **[Nguồn]** — [DD/MM/YYYY] — "[Title]" — `[reject_reason]`: [Story_Editor_note]

❌ **Master reject (0-1 bài)**
- **[Nguồn]** — "[Title]" — `[reject_reason]`: [Master_note]

</details>

<details>
<summary>📖 Click đọc full bài viết gốc</summary>

[Raw text full — từ web_fetch primary URL, Master persist vào crawl_log.raw_content sau khi pick]

</details>

<details>
<summary>🔍 Data trail (V4.0)</summary>

[Render data_trail array — mỗi entry gồm source (URL/WebSearch/Finpath_API/KB/Manual_YAML/Lập luận tự) + fetched + purpose + supports_argument]

</details>
```

## Render order (orchestrator Step 6)

1. Query SQLite `crawl_log` filter by `funnel_batch_id` của primary
2. Group rows: published / Editor V1 reject / Story Editor reject / Master reject
3. Sort within group: by `published_time` desc
4. Render Crawl funnel section LIST format (KHÔNG table — mobile-friendly)
5. Default COLLAPSE 3 `<details>` (sếp click mới mở)
6. Crawl funnel section đặt **TRƯỚC** raw text expand

## Critical rules

- **Cột trái sạch V4.0** — chỉ insight callout + opening paragraph + 3-7 bullets + closing + góc nhìn ngược + pipeline log toggle. KHÔNG heading `## Cần để ý`, KHÔNG nhãn "Key takeaway"/"Tóm lại"/"Tin chính"/"Điểm cốt lõi".
- **Cột phải đầy đủ meta V4.0** — 6 bullet "Cách viết" (thêm 2 bullet V4.0 về câu hỏi đã pick + reason) + Crawl Funnel + Raw text expand + Data trail expand
- **Funnel section default collapse** — không mở sẵn (clean look)
- **Insight callout dùng `>`** (blockquote markdown) — nổi bật vs body
- **V4.0 enum không leak** — `chosen_question_idx` numeric OK render, nhưng `category` (paradox/why_now/hidden_mechanism/comparison_deep/early_signal) chỉ render trong pipeline_log internal toggle (code style backtick), KHÔNG render trong "Cách viết" narrative section
