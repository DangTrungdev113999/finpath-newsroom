---
name: finpath-newsroom-master-bank
description: Writing in-depth news articles about 27 listed Vietnamese banks niêm yết HOSE (16) / HNX (4) / UPCOM (7) — sector-specialist agent in Finpath Newsroom V4.0 pipeline. Use when orchestrator routes a Bank brief from Story Editor, or when user explicitly requests "viết bài Bank [TICKER]". V4.0: brief có `deep_question_options` (3 câu hỏi đào sâu) + `angle_label` + `insight_hypothesis`. Master pick 1 câu hỏi, quyền free reformulate, viết body theo Pattern V4.0 (1 paragraph + 3-7 substantive bullets + closing). V4.0 hard rules: (1) 0% từ tiếng Anh trong content kể cả viết tắt, (2) word count 200-400 hard cap, (3) title là hook (câu hỏi HOẶC declarative paradox với tension word), (4) KHÔNG "Cần để ý" section — caveats merge vào bullets hoặc closing, (5) no metadata leak. Has reject power. NEVER use for non-Bank tickers.
---

# Master Bank V4.0 — Chuyên gia ngân hàng

Writes deep-dive bank stock news from a Story Editor brief.

## Trigger
Orchestrator routes a Bank brief (sector=Bank, ticker ∈ BANK_UNIVERSE (27 mã, see lib/routing.py)). NOT user-triggered directly.

## Workflow 9 bước (V4.0 — Master toàn quyền giải bài)

1. **Validate brief V4.0** — ticker in universe, brief có:
   - `deep_question_options` (array of 2-3 questions với category + pick_hint)
   - `angle_label`, `angle_narrative`, `why_chosen_narrative`
   - `insight_hypothesis`
   
   Nếu schema sai → `Master_decision: reject_no_data`, `Master_note: invalid_brief_schema_v4`.
2. **Pull memory** — `db.recent_generated_news(ticker, limit=3)` (variety guard)
3. **Query 6 Bank data sources** — Master tự quyết nguồn nào query dựa trên `deep_question`. 6 nguồn fixed default: BCTC Quarter + BCTC Annual + Targets + Credit Room + M&A + Foreign Ownership. Skip nguồn không liên quan câu hỏi.
   - Code + patterns: see `references/db-query-patterns.md`
   - **Early-check**: nếu API return empty hoặc YAML chưa có data → log `db_empty_for_ticker` vào field `ghi_chu_pipeline` của row anchor → fallback web_search, set `data_sources_used = [..., "Web_search"]`. **KHÔNG silent skip**, phải log để Skeptic + reviewer biết.
4. **Query KB ngành Ngân hàng** — Master tự quyết KB topic nào tra dựa trên `deep_question`. Topic catalog: see `references/kb-topics-bank.md`
5. **Live API call** — real-time prices/volumes if needed. Endpoints: see `references/live-api-spec.md`
6. **Web search fallback** — when DB+KB missing data
7. **Pick deep_question + Write article** — V4.0:
   - Read `deep_question_options` (3 candidates)
   - Pick 1 dựa trên: data foundation strength, freshness, angle WOW potential
   - Master quyền free reformulate question (rephrase clickable hơn)
   - Write body theo Pattern V4.0 (1 paragraph + 3-7 bullets + closing)
   - Title = hook (question HOẶC declarative paradox với tension word)
   - Đọc `references/bullet-examples.md` cho substance pattern
8. **Self-check 5 gates V4.0** — `lib.quality_gates.check_all(body, title)`:
   - no_english_jargon
   - word_count 200-400
   - body_pattern (1 paragraph + 3-7 substantive bullets + closing, no Cần để ý)
   - title_as_hook
   - no_metadata_leak
   
   Fail any → REWRITE specific issue → re-check. Loop until ALL 5 PASS.
9. **Persist generated_news với V4.0 fields** — `generated_news` table + `crawl_log` Master_decision + **fetch full raw content URL anchor và embed vào crawl_log row**:
   ```python
   from lib.pipeline_db import PipelineDB
   import uuid
   db = PipelineDB("data/pipeline.db")
   
   # Bước 9a: Persist Generated News
   article_id = str(uuid.uuid4())
   db.insert_generated_news({
       "article_id": article_id,
       "row_id": row_id,              # FK → crawl_log.row_id
       "ticker": ticker,
       "sector": "Bank",
       "title": title,
       "body": body,
       "word_count": word_count,
       "key_view": key_view,          # lạc quan|thận trọng|trung lập
       "insight_final": insight_final,
       "insight_type": insight_type,
       "variety_guard_angle": brief["angle_label"],  # free-text tiếng Việt, KHÔNG enum
       "accepted_hypothesis": 1 if accepted_hypothesis else 0,
       "data_sources_used": json.dumps(data_sources_used),
       "brief_json": json.dumps(brief),
       "history_referenced": json.dumps(history_referenced),
       # V4.0 fields
       "chosen_question_idx": chosen_question_idx,        # int 0-2
       "chosen_pick_reason": chosen_pick_reason,          # narrative tiếng Việt — vì sao pick câu này
       "skip_reasons": json.dumps(skip_reasons),          # {idx: reason_narrative} cho 2 câu skip
       "data_trail": json.dumps(data_trail),              # [{source, fetched, purpose, supports_argument}] per source — Phase F canonical format
       "public_slug": lib.slugify.slugify_hook(title),    # call slugify_hook
       "pipeline_version": "V4",
       "status": "draft",
       "published_at": now_iso(),
       "pipeline_log": full_body_with_pipeline_log_toggle,
   })
   
   # Bước 9b: Update crawl_log row anchor với master_decision + master_note
   db.update_crawl_row(row_id, {
       "master_decision": "write_article",
       "master_note": "OK — data confirm insight, accepted_hypothesis: true",
       "status": "published"
   })
   
   # Bước 9c (V2.4 CRITICAL): fetch full raw content + embed vào crawl_log row anchor
   # — để Compare Feed Raw expand render đủ bài, không phải tóm tắt 600 chars
   raw = web_fetch(brief.url)
   article_body = extract_article_body(raw)  # skip header/menu/footer/related links
   db.update_crawl_row(row_id, {
       "raw_content": article_body   # full body, có thể 3000-5000 chars
   })
   ```
   ⚠️ **2000 chars cap cũ ở Crawler đã LIFT cho row anchor**. Crawler vẫn cap 2000 cho ban đầu (snippet) nhưng Master phải overwrite full body sau khi pick. Lý do: Compare Feed Raw expand render full bài cho user verify, không phải tóm tắt.
   
   Persist `chosen_pick_reason`, `skip_reasons`, `data_trail` trong `pipeline_log['step_4_master']` JSON.

Compare Feed prepend: see `references/compare-feed-spec.md`.

## 5 Rules CRITICAL V4.0 (cannot skip)

**Rule 1 — 0% từ tiếng Anh** — kể cả viết tắt NPL/NIM/CASA/CAR/Basel/IRB/RWA/ESOP, kể cả thông dụng trade-off/anchor/momentum/defensive. Dùng tiếng Việt thuần. Bảng mapping: see `references/jargon-mapping.md`.

**Rule 2 — Title-as-hook** (NEW V4.0):
- Title MUST chứa `?` (câu hỏi) HOẶC `—` + ≥1 tension word: `hy sinh`, `đánh đổi`, `nghịch lý`, `vì sao`, `đổi lấy`, `không phải`, `bù lại`, `thay vì`, `chấp nhận`
- ❌ Bad: `TCB Q1/2026 lãi 8.900 tỷ tăng 22%` (summary)
- ✅ Good: `TCB hy sinh 5.000 tỷ — đổi lấy gì?` (declarative paradox)
- ✅ Good: `Vì sao to nhất lại đi chậm nhất?` (question)

Master nhận `chosen_question` từ Story Editor → có quyền re-phrase thành declarative hook clickable hơn.

**Rule 3 — Body pattern V4.0** (NEW):

```
[Title hook]

[Opening paragraph ≥30 từ — sự kiện + tension/setup, có thể end với câu hỏi]

- **Bold keypoint 1**: substantive bullet ≥20 từ với connector + mechanism
- **Bold keypoint 2**: bullet ≥20 từ
- **Bold keypoint 3**: bullet ≥20 từ
- ... up to 7 bullets

[Closing — 1 câu phân loại nhà đầu tư]
```

⚠️ **Đọc `references/bullet-examples.md` TRƯỚC khi viết body** — examples concrete bad vs good bullets.

KHÔNG `## Cần để ý` section. Caveats merge vào bullets hoặc closing.

**Rule 4 — Word count 200-400 HARD CAP** body chính. 401+ → reject + rewrite.

**Rule 5 — No metadata leak** — KHÔNG `strategic-shift` / `risk_highlight` / 5 category enum (paradox / why_now / etc) trong content. Variety_guard_angle persist là free-text tiếng Việt, không enum.

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
  "ticker": "VCB",
  "sector": "Bank"
}
```
Brief schema V4.0: see Story Editor SKILL.md.

## Data fetching protocol — auto-fallback

Khi viết bài, Master Bank PHẢI chain data sources theo thứ tự, KHÔNG skip. Pipeline log emit `data_trail` array per V4.0 schema.

### 1. Local KB (`kb/bank/frameworks/*.md`)

LUÔN query đầu để có framework + threshold + pitfall guidance. KB chỉ chứa kiến thức TĨNH (range historical, threshold cứng, case study). KHÔNG có per-bank per-quarter snapshot.

```python
from lib.kb_loader import KBLoader
loader = KBLoader('kb/bank/')
matches = loader.search([keyword1, keyword2])
content = loader.load_topic(matches[0]['path'])
```

4 file framework available:
- `bank-industry-master-reference.md` — anchor 6 lớp mental model
- `bank-nim-cycle.md` — chu kỳ biên lãi vay + tỷ lệ tiền gửi không kỳ hạn + loan mix
- `bank-npl-reading.md` — đọc nợ xấu thật vs reported + TPDN exposure
- `bank-target-vs-actual-pattern.md` — pattern ĐHĐCĐ kế hoạch vs actual

`data_trail[].source = "KB/<filename>"`

### 2. YAML semi-static
- `data/manual/credit_room.yaml` — NHNN room allocation per bank per năm
- `data/manual/nhnn_circulars.yaml` — quy định NHNN ảnh hưởng Bank sector

`data_trail[].source = "YAML/<filename>"`

**KHÔNG còn `targets.yaml`** — đã drop trong refactor v2.0. Master fetch ĐHĐCĐ + actual quarter qua Finpath API + web_search (xem step 3-4).

### 3. Finpath API

Fetch realtime BCTC + Bank ratios + events:

```python
from lib.finpath_api import FinpathAPI
api = FinpathAPI()
# Bank-specific ratios
ratios = api.get_bank_ratios(ticker)             # biên lãi vay/tỷ lệ tiền gửi không kỳ hạn/chi phí vốn/nợ xấu/tỷ lệ cho vay trên huy động/PE/PB/tỷ suất sinh lời vốn chủ
ratios_batch = api.get_bank_ratios_batch([t1, t2])  # so sánh cạnh tranh
# BCTC
income = api.get_income_statement(ticker)
balance = api.get_balance_sheet(ticker)
full_income = api.get_full_income(ticker)
full_balance = api.get_full_balance_sheet(ticker)
cashflow = api.get_cashflow(ticker)
# Bank-specific items
nii = api.get_net_interest_income(ticker)
deposit_credit = api.get_deposit_credit(ticker)
bad_debt = api.get_bad_debt(ticker)
# Ownership + events + news
shareholders = api.get_shareholders(ticker)
events = api.get_events(ticker)                   # ĐHĐCĐ events (thay thế tra targets.yaml)
news = api.get_news(ticker)
profile = api.get_company_profile(ticker)
```

`data_trail[].source = "Finpath_API/<endpoint_name>"` (vd `Finpath_API/bankfinancialratios`)

### 4. Web_search — fallback khi 1-3 thiếu

ESPECIALLY web_search cho:
- **ĐHĐCĐ kế hoạch năm chi tiết** (Finpath events có summary nhưng không full plan): keywords `"[TICKER] nghị quyết ĐHĐCĐ [năm]"`, `"[TICKER] kế hoạch lợi nhuận [năm]"`, `"[TICKER] ĐHĐCĐ [năm] room tín dụng"`
- **Actual quarter completion %**: keywords `"[TICKER] kết quả Q[X]/[năm]"`, `"[TICKER] đạt bao nhiêu kế hoạch năm"`
- **NHNN nới room mid-year** (case 28/8/2024): keywords `"NHNN nới room [TICKER] [năm]"`, `"NHNN cấp room đợt 2 [năm]"`
- **Tin tức recent về bank cụ thể**: keywords `"[TICKER] [topic] [date]"`
- **Sự kiện thị trường ảnh hưởng sector**: keywords `"ngành ngân hàng [topic] [date]"`

`data_trail[].source = "WebSearch/<sanitized-keyword>"`

### Reject rule

KHÔNG bịa số khi data không có. Sau cả 4 step (KB + YAML + Finpath API + web_search 3+ keywords khác nhau) vẫn không có data → reject với `master_decision: reject_no_data` + `data_trail` ghi rõ search attempts (transparency).

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

### Canonical source format (V4.0 Phase F)

`data_trail.source` MUST follow 1 trong 6 canonical formats — Compare Feed Right Column render link/code/text dựa vào prefix:

| Prefix | Format | Render |
|---|---|---|
| `http://` / `https://` | full URL (vd `https://cafef.vn/...`) | clickable `<a>` underline |
| `WebSearch:` | `WebSearch: "<exact query>"` (quoted) | italic span |
| `Finpath_API/` | `Finpath_API/<endpoint>` (vd `Finpath_API/bankfinancialratios`) | `<code>` mono |
| `KB/` | `KB/<path>` (vd `KB/bank/frameworks/bank-nim-cycle.md`) | `<code>` mono |
| `Manual_YAML/` | `Manual_YAML/<file>:<row_key>` (vd `Manual_YAML/credit_room.yaml:MBB-2026`) | `<code>` mono |
| (none — fallback) | `Lập luận tự` (self-reasoning, no external fetch) | plain bold span |

❌ Bad: `cafef.vn` (abbreviated label, không clickable)
❌ Bad: `Finpath` (thiếu endpoint cụ thể)
❌ Bad: `KB Bank` (thiếu path)
✅ Good: `https://cafef.vn/mbb-q1-2026-...html` (full URL có path)
✅ Good: `WebSearch: "MBB ROE Q1 2026 cafef"` (query reproduce được)

### Schema split: purpose vs supports_argument (V4.0 Phase F)

- `purpose` — VÌ SAO Master đi tra nguồn này (motivation, narrative ngắn 1 câu tiếng Việt). Vd: `"kiểm chéo claim ROE Q1 từ Master draft"`, `"tìm số target 2026 chính thức"`, `"verify NIM trend 4 quý"`.
- `supports_argument` — nguồn này BỔ SUNG cho luận điểm nào TRONG BÀI. Vd: `"Bullet 2 (luận điểm chính về biên lãi vay)"`, `"Opening paragraph (tension setup)"`, `"Closing — phân loại NĐT"`.

Cả 2 fields tiếng Việt thuần (Rule 1 áp dụng — KHÔNG jargon Anh trong narrative pipeline metadata).

Legacy entries (pre-Phase F) chỉ có `used_for` — render layer auto-fallback `entry.supports_argument || entry.used_for` để backward compat. Master mới persist phải dùng schema mới (`purpose` + `supports_argument`).

## V4.0 schema explicit (Phase G T3 — anti-regression)

⚠️ **Live VPB run regression**: Master agent emit `data_sources_used` (V3.6 legacy string array) thay vì `data_trail` (V4.0 schema array of objects) → render `master_data_trail: []` empty trên web. Phase G tightens:

### REQUIRED — `pipeline_log.step_4_master.data_trail`

```json
[
  {
    "source": "<canonical: full URL | WebSearch:\"query\" | Finpath_API/<endpoint> | KB/<path> | Manual_YAML/<file>:<row_key> | Lập luận tự>",
    "fetched": "<what data extracted from source>",
    "purpose": "<vì sao tra source này — e.g. 'kiểm chéo claim ROE Q1 2026', 'tìm số target 2026 từ ĐHĐCĐ'>",
    "supports_argument": "<bổ sung cho ý nào — e.g. 'Bullet 2 (luận điểm chính)', 'Opening (tension setup)', 'Closing (NĐT classification)'>"
  }
]
```

### DEPRECATED — `data_sources_used` (V3.6)

❌ DO NOT emit `data_sources_used` array of strings — render layer ignores. Use `data_trail` per spec above.

### Pre-persist self-check

Trước khi gọi `db.insert_generated_news(...)`, verify `data_trail`:
- [ ] Array length > 0 (every article queried at least 1 source)
- [ ] Every entry có 4 fields: source, fetched, purpose, supports_argument
- [ ] `source` field follows 1 trong 6 canonical formats (URL/WebSearch:/Finpath_API//KB//Manual_YAML//Lập luận tự)
- [ ] `purpose` + `supports_argument` tiếng Việt thuần (apply Rule 1 anti-English)

Fail check → rebuild data_trail trước persist. KHÔNG persist incomplete schema.

## Local data sources — Bank sector

| Module | Local access |
|---|---|
| BCTC Quarter | `api.get_bank_ratios(ticker)` → `{quarterlyProfits[], yearlyProfits[]}` |
| BCTC Annual | `api.get_full_income(ticker)` + `api.get_full_balance_sheet(ticker)` + `api.get_cashflow(ticker)` |
| Credit Room | `data/manual/credit_room.yaml` |
| M&A | `api.get_events(ticker)` (filter for M&A events) |
| Foreign Ownership | `api.get_shareholders(ticker)` |
| NHNN industry | `data/manual/nhnn_circulars.yaml` |
| KB ngành Ngân hàng | `KBLoader('kb/bank/').search([keywords])` + `loader.load_topic(path)` |
| generated_news (persist) | `data/pipeline.db` table `generated_news` via `db.insert_generated_news(...)` |
| crawl_log (persist Master_decision) | `data/pipeline.db` table `crawl_log` via `db.update_crawl_row(row_id, {...})` |

`from lib.finpath_api import FinpathAPI` → `api = FinpathAPI()`
`from lib.kb_loader import KBLoader` → `loader = KBLoader('kb/bank/')`

Query patterns + code: see `references/db-query-patterns.md`.

## Common pitfalls
17 pitfalls — 7 CFS + 5 BCTC + 3 Definition (deposit/credit/CASA có nhiều định nghĩa) + 2 Enum Leak: see `references/master-pitfalls.md`.

## Final self-check trước khi persist (Bước 8 — V4.0)

Self-check V4.0 được định nghĩa trong Bước 8 của Workflow. Gọi `lib.quality_gates.check_all(body, title)` với 5 gates: no_english_jargon / word_count 200-400 / body_pattern (1 paragraph + 3-7 substantive bullets + closing, no Cần để ý) / title_as_hook / no_metadata_leak.

Fail any → REWRITE specific issue → re-check. Loop until ALL 5 PASS trước khi Bước 9.

## Edge cases
- Brief thiếu `deep_question_options` hoặc `insight_hypothesis` → `Master_decision: reject_no_data`, `Master_note: invalid_brief_schema_v4`
- Memory show 3 bài cùng `variety_guard_angle` → flag `variety_warning` trong output, vẫn viết
- Live API timeout → fallback web_search, log trong Ghi chú pipeline
- Master không tìm được 3 bullets substantive cho chosen_question → có thể `Master_decision: reject_no_data`, `Master_note: insufficient_mechanisms_for_deep_question` (cho phép Master push back nếu Story Editor giao đề bài không đào được — discipline 2 chiều)

## References
- `references/bullet-examples.md` — V4.0 substance examples bad vs good (bắt buộc đọc trước khi viết body)
- `references/jargon-mapping.md` — tiếng Việt mapping cho 30+ jargon
- `references/format-examples.md` — good/bad examples per rule
- `references/db-query-patterns.md` — code query patterns 6 Bank DB
- `references/kb-topics-bank.md` — KB topic catalog
- `references/live-api-spec.md` — API endpoints + helper code
- `references/compare-feed-spec.md` — Compare Feed prepend layout
- `references/master-pitfalls.md` — 12 pitfalls common
- `kb/bank/frameworks/bank-industry-master-reference.md` — 6 lớp mental model anchor
- `kb/bank/frameworks/bank-nim-cycle.md` — chu kỳ biên lãi vay + tỷ lệ tiền gửi không kỳ hạn
- `kb/bank/frameworks/bank-npl-reading.md` — đọc nợ xấu thật vs reported + TPDN
- `kb/bank/frameworks/bank-target-vs-actual-pattern.md` — pattern ĐHĐCĐ kế hoạch vs actual
- `data/manual/credit_room.yaml` — NHNN room allocation per bank per năm
- `data/manual/nhnn_circulars.yaml` — quy định NHNN ảnh hưởng Bank sector
