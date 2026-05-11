# Compare Feed Prepend — Layout V2.4

Compare Feed page: `https://www.notion.so/359273c7a9a181bd88f6ebf0d954551d`

## Position
**Newest-first**: section bài mới prepend vào TOP page, trên section bài cũ.

## Header (full width, 2 dòng)

```markdown
# 🏦 [Tiêu đề bài full]
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

## Cột TRÁI — bài AI viết lại

```markdown
## ✍️ Bài AI viết lại · [N từ]

> 💡 **Insight**: [insight_final 1 câu — copy từ row.Insight_line]

[Mở đầu 25-30 từ — không heading]

[Opening paragraph 30-60 từ — sự kiện + tension/setup, không heading]

- **Bold keypoint 1**: substantive bullet ≥20 từ với connector + mechanism
- **Bold keypoint 2**: bullet ≥20 từ
- **Bold keypoint 3**: bullet ≥20 từ
- ... up to 7 bullets

⚠️ **V4.0 BAN heading `## Cần để ý`** — caveat phải merge vào bullet substantive HOẶC closing sentence. Body Master KHÔNG được có bất kỳ heading nào ngoài body chính (opening + bullets + closing). Skeptic append `## Góc nhìn ngược` riêng (không tính vào gates Master).

[Closing 1 câu — phân loại NĐT phù hợp, không nhãn "Tóm lại". Caveat merge ở đây nếu cần.]

## Góc nhìn ngược
[Skeptic append sau publish — 100-300 từ bullet]

<details>
<summary>📋 Pipeline log</summary>
[Step 1-6 chi tiết — see references/pipeline-log-format.md]
</details>
```

## Cột PHẢI — raw text + meta

```markdown
## 📰 Raw text gốc · [M từ]

**[Title gốc full]**
*Nguồn: domain.vn — DD/MM/YYYY*

### 🎯 Cách viết & lý do chọn
- **Vì sao chọn bài này**: [brief.why_chosen — Story Editor judgment]
- **Hướng đi**: [brief.angle — vd "Nghịch lý kết hợp strategic shift"]
- **Vì sao chọn hướng này**: [brief.angle_rationale]
- **Vì sao chọn nguồn này**: [brief.source_rationale]

<details>
<summary>📊 Crawl funnel — đã search N nguồn, tìm M tin, chọn 1 published, X rejected (click để xem)</summary>

✅ **Published (1 bài)**
- **[Nguồn]** — [DD/MM/YYYY HH:MM] — "[Title]" (PRIMARY source)

❌ **Editor V1 reject (Y bài)**
- **[Nguồn]** — [DD/MM/YYYY] — "[Title]" — `[reject_reason]`: [Editor_V1_note]

❌ **Story Editor V2.4 reject (Z bài)**
- **[Nguồn]** — [DD/MM/YYYY] — "[Title]" — `[reject_reason]`: [Story_Editor_note]

❌ **Master reject (0-1 bài)**
- **[Nguồn]** — "[Title]" — `[reject_reason]`: [Master_note]

</details>

<details>
<summary>📖 Click đọc full bài viết gốc</summary>

[Raw text full — từ web_fetch primary URL token_limit ≥3500]

</details>
```

## Render order (orchestrator Step 6)

1. Query DB Crawl Log filter by Funnel_batch_id của primary
2. Group rows: published / Editor V1 reject / Story Editor reject / Master reject
3. Sort within group: by Published_time desc
4. Render Crawl funnel section LIST format (KHÔNG table — mobile-friendly)
5. Default COLLAPSE both `<details>` (sếp click mới mở)
6. Crawl funnel section đặt **TRƯỚC** raw text expand

## Critical rules

- **Cột trái sạch** — chỉ insight + bài + góc nhìn ngược + pipeline log toggle. KHÔNG nhãn "Key takeaway"/"Tóm lại"
- **Cột phải đầy đủ meta** — 4 bullet "Cách viết" + Crawl Funnel + Raw text expand
- **Funnel section default collapse** — không mở sẵn (clean look)
- **Insight callout dùng `>`** (blockquote markdown) — nổi bật vs body
