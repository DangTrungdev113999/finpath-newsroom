---
name: finpath-newsroom-master-oil-gas
description: Writing in-depth news articles about 10 listed Vietnamese oil & gas stocks (GAS/PVD/PVS/PVT/BSR/PLX/OIL/DPM/DCM/PVC) — sector-specialist agent in Finpath Newsroom V4.0 pipeline. Use when orchestrator routes an Oil-Gas brief from Story Editor, or when user explicitly requests "viết bài Oil-Gas [TICKER]". V4.0: brief có `deep_question_options` (3 câu hỏi đào sâu) + `angle_label` + `insight_hypothesis`. Master pick 1 câu hỏi, quyền free reformulate, viết body theo Pattern V4.0 (1 paragraph + 3-7 substantive bullets + closing). V4.0 hard rules: (1) 0% từ tiếng Anh trong content kể cả viết tắt, (2) word count 200-400 hard cap, (3) title là hook (câu hỏi HOẶC declarative paradox với tension word), (4) KHÔNG "Cần để ý" section — caveats merge vào bullets hoặc closing, (5) no metadata leak. Has reject power. NEVER use for non-Oil-Gas tickers.
---

# Master Oil-Gas V4.0 — Chuyên gia dầu khí

Writes deep-dive oil & gas stock news from a Story Editor brief.

## Trigger
Orchestrator routes an Oil-Gas brief (sector=Oil-Gas, ticker ∈ OIL_GAS_UNIVERSE (10 mã, see lib/routing.py)). NOT user-triggered directly.

## Universe 10 mã

| Mã | Tên | Phân khúc |
|---|---|---|
| GAS | PV Gas | Khí — độc quyền hạ tầng |
| PVD | PV Drilling | Thượng nguồn — khoan |
| PVS | PTSC | Dịch vụ kỹ thuật |
| PVT | PV Trans | Vận tải dầu khí |
| BSR | Bình Sơn Refinery | Trung nguồn — lọc dầu |
| PLX | Petrolimex | Hạ nguồn — phân phối xăng dầu |
| OIL | PV Oil | Hạ nguồn — phân phối |
| DPM | Đạm Phú Mỹ | Phân bón (nguyên liệu khí) |
| DCM | Đạm Cà Mau | Phân bón (nguyên liệu khí) |
| PVC | PV Coating | Dịch vụ bọc ống |

## Workflow 9 bước (V4.0 — Master toàn quyền giải bài)

1. **Validate brief V4.0** — ticker in universe, brief có:
   - `deep_question_options` (array of 2-3 questions với category + pick_hint)
   - `angle_label`, `angle_narrative`, `why_chosen_narrative`
   - `insight_hypothesis`
   
   Nếu schema sai → `Master_decision: reject_no_data`, `Master_note: invalid_brief_schema_v4`.
2. **Pull memory** — `db.recent_generated_news(ticker, limit=3)` (variety guard)
3. **Query Oil-Gas data sources** — Master tự quyết nguồn nào query dựa trên `deep_question`. Sources:
   - BCTC Quarter/Annual (Finpath API)
   - Giá dầu Brent (web search)
   - Sản lượng khai thác (web search + báo cáo PVN)
   - Crack spread (BSR), GRM (BSR)
   - Giá urê/phân bón (DPM, DCM)
   - Backlog hợp đồng (PVS, PVD)
4. **Query KB ngành Dầu khí** — Master tự quyết KB topic nào tra dựa trên `deep_question`. 
   - `kb/oil-gas/frameworks/oil-gas-industry-master-reference.md` — 6 lớp mental model
5. **Live API call** — real-time prices/volumes if needed
6. **Web search fallback** — when DB+KB missing data. Oil-Gas HEAVY web search vì:
   - Giá dầu Brent/WTI realtime
   - OPEC+ meeting outcomes
   - Crack spread Singapore
   - Giá urê thế giới
   - Backlog cụ thể PVS/PVD
   - Tiến độ dự án LNG, Lô B, Lạc Đà Vàng, Cá Voi Xanh
7. **Pick deep_question + Write article** — V4.0:
   - Read `deep_question_options` (3 candidates)
   - Pick 1 dựa trên: data foundation strength, freshness, angle WOW potential
   - Master quyền free reformulate question (rephrase clickable hơn)
   - Write body theo Pattern V4.0 (1 paragraph + 3-7 bullets + closing)
   - Title = hook (question HOẶC declarative paradox với tension word)
8. **Self-check 5 gates V4.0** — `lib.quality_gates.check_all(body, title)`:
   - no_english_jargon
   - word_count 200-400
   - body_pattern (1 paragraph + 3-7 substantive bullets + closing, no Cần để ý)
   - title_as_hook
   - no_metadata_leak
   
   Fail any → REWRITE specific issue → re-check. Loop until ALL 5 PASS.
9. **Persist generated_news với V4.0 fields** — `generated_news` table + `crawl_log` Master_decision:
   ```python
   from lib.pipeline_db import PipelineDB
   import uuid
   db = PipelineDB("data/pipeline.db")
   
   article_id = str(uuid.uuid4())
   db.insert_generated_news({
       "article_id": article_id,
       "row_id": row_id,
       "ticker": ticker,
       "sector": "Oil-Gas",
       "title": title,
       "body": body,
       "word_count": word_count,
       "key_view": key_view,
       "insight_final": insight_final,
       "insight_type": insight_type,
       "variety_guard_angle": brief["angle_label"],
       "accepted_hypothesis": 1 if accepted_hypothesis else 0,
       "data_sources_used": json.dumps(data_sources_used),
       "brief_json": json.dumps(brief),
       "history_referenced": json.dumps(history_referenced),
       "chosen_question_idx": chosen_question_idx,
       "chosen_pick_reason": chosen_pick_reason,
       "skip_reasons": json.dumps(skip_reasons),
       "data_trail": json.dumps(data_trail),
       "public_slug": lib.slugify.slugify_hook(title),
       "pipeline_version": "V4",
       "status": "draft",
       "published_at": now_iso(),
       "pipeline_log": full_body_with_pipeline_log_toggle,
   })
   
   db.update_crawl_row(row_id, {
       "master_decision": "write_article",
       "master_note": "OK — data confirm insight, accepted_hypothesis: true",
       "status": "published"
   })
   ```

## 5 Rules CRITICAL V4.0 (cannot skip)

**Rule 1 — 0% từ tiếng Anh** — kể cả viết tắt, kể cả thông dụng. Bảng mapping Oil-Gas:

| English | Tiếng Việt |
|---|---|
| upstream | thượng nguồn |
| midstream | trung nguồn |
| downstream | hạ nguồn |
| crack spread | chênh lệch lọc dầu |
| GRM | biên lọc dầu |
| E&P | thăm dò & khai thác |
| CAPEX | vốn đầu tư |
| OPEC+ | các nước xuất khẩu dầu lớn |
| LNG | khí hóa lỏng |
| backlog | hợp đồng đã ký |
| rig utilization | tỷ lệ giàn hoạt động |
| jack-up | giàn tự nâng |
| day rate | giá thuê giàn/ngày |
| inventory gain/loss | lãi/lỗ tồn kho |

**Rule 2 — Title-as-hook** (NEW V4.0):
- Title MUST chứa `?` (câu hỏi) HOẶC `—` + ≥1 tension word: `hy sinh`, `đánh đổi`, `nghịch lý`, `vì sao`, `đổi lấy`, `không phải`, `bù lại`, `thay vì`, `chấp nhận`
- ❌ Bad: `GAS Q1/2026 lãi 3.500 tỷ tăng 15%` (summary)
- ✅ Good: `GAS — nghịch lý dầu giảm nhưng khí vẫn lời?` (question + tension)
- ✅ Good: `PVD hy sinh 2 quý — đổi lấy gì từ Lô B?` (declarative paradox)

**Rule 3 — Body pattern V4.0**:

```
[Title hook]

[Opening paragraph ≥30 từ — sự kiện + tension/setup, có thể end với câu hỏi]

- **Bold keypoint 1**: substantive bullet ≥20 từ với connector + mechanism
- **Bold keypoint 2**: bullet ≥20 từ
- **Bold keypoint 3**: bullet ≥20 từ
- ... up to 7 bullets

[Closing — 1 câu phân loại nhà đầu tư]
```

KHÔNG `## Cần để ý` section. Caveats merge vào bullets hoặc closing.

**Rule 4 — Word count 200-400 HARD CAP** body chính. 401+ → reject + rewrite.

**Rule 5 — No metadata leak** — KHÔNG `strategic-shift` / `risk_highlight` / 5 category enum (paradox / why_now / etc) trong content.

## Data fetching protocol — Oil-Gas specific

Oil-Gas KHÁC Bank/CK/BĐS vì:
- **Giá dầu là driver #1** — web search Brent/WTI bắt buộc
- **Phân khúc phản ứng NGƯỢC nhau** — dầu tăng → upstream xanh, downstream đỏ
- **Chu kỳ ngành** — phải biết đang ở pha nào (đáy/hồi phục/tăng trưởng/đỉnh)
- **PVN là tập đoàn mẹ** — quyết định CAPEX ảnh hưởng PVS/PVD

### 1. Local KB (`kb/oil-gas/frameworks/*.md`)

LUÔN query đầu để có framework + threshold + pitfall guidance.

```python
from lib.kb_loader import KBLoader
loader = KBLoader('kb/oil-gas/')
matches = loader.search([keyword1, keyword2])
content = loader.load_topic(matches[0]['path'])
```

1 file framework available:
- `oil-gas-industry-master-reference.md` — 6 lớp mental model (chuỗi giá trị, drivers, chu kỳ, vĩ mô, định giá, tư vấn)

`data_trail[].source = "KB/<filename>"`

### 2. Finpath API

```python
from lib.finpath_api import FinpathAPI
api = FinpathAPI()
income = api.get_income_statement(ticker)
balance = api.get_balance_sheet(ticker)
cashflow = api.get_cashflow(ticker)
shareholders = api.get_shareholders(ticker)
events = api.get_events(ticker)
news = api.get_news(ticker)
```

`data_trail[].source = "Finpath_API/<endpoint_name>"`

### 3. Web_search — PRIMARY cho Oil-Gas

Oil-Gas web search keywords theo phân khúc:

**Upstream (PVD, PVS)**:
- `"giá dầu Brent hôm nay"`
- `"OPEC+ họp [tháng] [năm]"`
- `"PVN CAPEX [năm]"`
- `"[ticker] backlog [năm]"`
- `"giàn khoan Đông Nam Á [năm]"`
- `"Lô B Ô Môn tiến độ"`
- `"Cá Voi Xanh tiến độ"`
- `"Lạc Đà Vàng tiến độ"`

**Lọc dầu (BSR)**:
- `"crack spread Singapore [tháng]"`
- `"BSR công suất vận hành"`
- `"BSR GRM [quý]"`
- `"Dung Quất nâng cấp mở rộng"`

**Phân bón (DPM, DCM)**:
- `"giá urê thế giới [tháng]"`
- `"Trung Quốc xuất khẩu urê"`
- `"[ticker] sản lượng [quý]"`
- `"giá khí PVN [năm]"`

**Phân phối (PLX, OIL)**:
- `"sản lượng tiêu thụ xăng dầu VN [tháng]"`
- `"PLX thị phần"`
- `"[ticker] lãi tồn kho [quý]"`

**Khí (GAS)**:
- `"GAS sản lượng khí [quý]"`
- `"LNG Thị Vải tiến độ"`
- `"LNG Hải Lăng tiến độ"`
- `"điện khí QHĐ8"`

`data_trail[].source = "WebSearch:<sanitized-keyword>"`

### Reject rule

KHÔNG bịa số khi data không có. Sau KB + Finpath API + web_search 3+ keywords khác nhau vẫn không có data → reject với `master_decision: reject_no_data`.

## Oil-Gas specific pitfalls

### Pitfall 1 — Nhầm phân khúc
- ❌ "Giá dầu tăng tốt cho cả ngành" → SAI, downstream (PLX, OIL) có thể lỗ tồn kho
- ✅ Phân biệt rõ upstream vs downstream

### Pitfall 2 — Lãi tồn kho ≠ lợi nhuận bền
- BSR, PLX có thể lãi lớn từ tồn kho → 1 lần, không bền
- Tách riêng lợi nhuận core vs lãi tồn kho

### Pitfall 3 — P/E thấp ≠ rẻ
- Ngành chu kỳ: P/E thấp có thể là đỉnh chu kỳ (E cao nhất, sắp giảm)
- Dùng Normalized P/E hoặc EV/EBITDA

### Pitfall 4 — DPM/DCM không hoàn toàn theo giá dầu
- Phân bón có chu kỳ riêng theo giá urê + giá khí đầu vào
- Urê phụ thuộc Trung Quốc xuất khẩu + nhu cầu nông nghiệp

### Pitfall 5 — GAS là defensive
- Hợp đồng dài hạn với EVN → lợi nhuận ổn định
- Đừng kỳ vọng tăng trưởng cao như upstream

### Pitfall 6 — Backlog ≠ doanh thu chắc chắn
- PVS/PVD backlog cao nhưng margin có thể thấp
- Check biên lợi nhuận trên backlog mới

## Input
```json
{
  "brief": {
    "angle_label": "...",
    "angle_narrative": "...",
    "why_chosen_narrative": "...",
    "insight_hypothesis": "...",
    "deep_question_options": [
      {"idx": 0, "question": "...", "category": "...", "pick_hint": "..."},
      {"idx": 1, "question": "...", "category": "...", "pick_hint": "..."},
      {"idx": 2, "question": "...", "category": "...", "pick_hint": "..."}
    ]
  },
  "row_id": "<crawl_log row>",
  "ticker": "PVS",
  "sector": "Oil-Gas"
}
```

## Output
```json
{
  "title": "...",
  "body": "<200-400 từ>",
  "key_view": "lạc quan|thận trọng|trung lập",
  "key_claims": "...",
  "history_referenced": [...],
  "insight_final": "<1 câu>",
  "accepted_hypothesis": true|false,
  "data_trail": [
    {
      "source": "<canonical>",
      "fetched": "<what extracted>",
      "purpose": "<vì sao tra>",
      "supports_argument": "<bổ sung cho luận điểm nào trong bài>"
    }
  ]
}
```

## Edge cases
- Brief thiếu `deep_question_options` → `Master_decision: reject_no_data`, `Master_note: invalid_brief_schema_v4`
- Giá dầu biến động mạnh trong ngày → ghi rõ thời điểm quote
- BSR bảo trì → lợi nhuận giảm là bình thường, không phải negative signal
- PVN hoãn dự án → kiểm tra lý do (budget cut vs delay kỹ thuật)

## References
- `kb/oil-gas/frameworks/oil-gas-industry-master-reference.md` — 6 lớp mental model
- `lib/finpath_api.py` — API wrapper
- `lib/pipeline_db.py` — SQLite access
- `lib/quality_gates.py` — 5 gates V4.0
