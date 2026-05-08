# Compare Feed Prepend — Layout V2.4

Compare Feed output: `output/compare-feed/<batch>.md` — Phase 6 DEFER (currently rendered to local file, NOT Notion page)

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

[Body bullet/đoạn ngắn 150-250 từ]
- **Bold số key** trong bullet
- ...

## Cần để ý
[optional 25-30 từ — Mốc cần theo dõi]

[Chốt insight tự nhiên — không nhãn "Tóm lại"]

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

**Funnel batch**: `[ticker]-[YYYYMMDD]-[HHMM]` · **Sort**: by Published_time desc

✅ **Picked (1)**
- [**Nguồn**](https://full-url.com) (DD/MM/YYYY) → **Editor V1: pass** → **Story Editor: write_brief** → **Master: write_article** → **published**. Anchor vì [≤1 câu lý do].

❌ **Rejected by Editor V1 (Y bài, nếu có)**
- [Nguồn](https://full-url.com) (DD/MM/YYYY) — **out_of_universe**: [reason ≤1 câu, dễ hiểu]
- [Nguồn](https://full-url.com) (DD/MM/YYYY) — **low_quality_source**: [reason]
- [Nguồn](https://full-url.com) (DD/MM/YYYY) — **dup_url**: [reason]

❌ **Rejected by Story Editor (Z bài)**
- [Nguồn](https://full-url.com) (DD/MM/YYYY) — **dup_event**: [reason ≤1 câu — vd "Cùng story ĐHĐCĐ 25/4 với BPL anchor, thiếu 2 quote CEO/Chủ tịch"]
- [Nguồn](https://full-url.com) (DD/MM/YYYY) — **low_writeability**: [reason — vd "PR-friendly title, không decode strategic-shift"]
- [Nguồn](https://full-url.com) (DD/MM/YYYY) — **wait_more_data**: [reason — vd "Tin sau ĐHĐCĐ chỉ là update thanh toán, không có angle mới"]
- [Nguồn](https://full-url.com) (DD/MM/YYYY) — **duplicate**: [reason — vd "Trùng story đã viết tuần trước"]

❌ **Rejected by Master (0-1 bài)**
- [Nguồn](https://full-url.com) (DD/MM/YYYY) — **reject_no_data**: [Master_note — vd "data anchor missing — 50%+ keys null"]
- [Nguồn](https://full-url.com) (DD/MM/YYYY) — **reject_data_conflict**: [Master_note — vd "insight nói X nhưng data show Y"]

</details>

<details>
<summary>📖 Click đọc full bài viết gốc</summary>

[Raw text full — từ web_fetch primary URL token_limit ≥3500]

</details>
```

## Render order (orchestrator Step 6)

1. Query `crawl_log` filter by `funnel_batch_id` của primary: `db.query_by_funnel_batch(batch_id)`
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

## V2.4 CRITICAL — Crawl Funnel + Raw expand

**1. Crawl Funnel: list TẤT CẢ candidates trong batch (không pick + 2 reject như cũ)**
- Mỗi candidate phải có: link click ra được (Markdown format `[Nguồn](URL)`), Published_time, agent reject rõ (Editor V1 / Story Editor / Master), reject_reason ≤1 câu dễ hiểu
- Group by agent reject (Editor V1 / Story Editor / Master) + Picked tách riêng đầu
- Sort within group: by Published_time desc

**2. Link nguồn click ra được**
- ❌ KHÔNG: `Báo Pháp luật (05/05) → write_brief` (text plain, click không ra)
- ✅ ĐÚNG: `[Báo Pháp luật](https://doanhnhan.baophapluat.vn/dhdcd-techcombank...) (05/05/2026)` (Markdown link)
- Lý do: user verify nguồn bằng cách click trực tiếp, không phải copy URL từ DB

**3. Reject reason ngắn + dễ hiểu**
- Mỗi reason ≤1 câu, dùng từ thông thường (KHÔNG jargon nội bộ)
- ❌ "low_writeability score 2/5 below threshold"
- ✅ "low_writeability: PR-friendly title, không decode strategic-shift"
- ❌ "dup_event hash collision với row#abc"
- ✅ "dup_event: Cùng story ĐHĐCĐ 25/4 với BPL anchor, thiếu 2 quote CEO/Chủ tịch"

**4. Raw text gốc full content**
- Bắt buộc full body từ web_fetch primary URL (token_limit ≥3500), KHÔNG phải tóm tắt 600 chars từ Crawler snippet
- Master Bank Bước 9c overwrite `Nội dung thô` của row anchor với full body sau khi pick
- 6 section đúng article gốc (giữ original heading), không tóm tắt
- Quote CEO/Chủ tịch để nguyên trong italic + dấu ngoặc kép, không paraphrase

**Quy ước escalation**: Nếu Crawler shortcut chỉ fetch 3 candidates thay vì 10+ nguồn whitelist → flag `broadcast_search_used: true` trong row Ghi chú pipeline → Compare Feed render warning ⚠️ ở đầu Crawl Funnel section: "Crawl batch dùng broadcast search, có thể miss tin từ nguồn ít rank cao".
