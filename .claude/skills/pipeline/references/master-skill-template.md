# Master Skill Template

Template cho master agent skill khi thêm ngành mới.

Copy và customize các placeholder `<SECTOR>`, `<sector>`, `<N>`, `<TICKER_LIST>`.

---

```markdown
---
name: finpath-newsroom-master-<sector>
description: Writing in-depth news articles about <N> listed Vietnamese <sector> stocks (<TICKER_LIST>) — sector-specialist agent in Finpath Newsroom V4.0 pipeline. Use when orchestrator routes a <Sector> brief from Story Editor, or when user explicitly requests "viết bài <Sector> [TICKER]". V4.0: brief có `deep_question_options` (3 câu hỏi đào sâu) + `angle_label` + `insight_hypothesis`. Master pick 1 câu hỏi, quyền free reformulate, viết body theo Pattern V4.0 (1 paragraph + 3-7 substantive bullets + closing). V4.0 hard rules: (1) 0% từ tiếng Anh trong content kể cả viết tắt, (2) word count 200-400 hard cap, (3) title là hook (câu hỏi HOẶC declarative paradox với tension word), (4) KHÔNG "Cần để ý" section — caveats merge vào bullets hoặc closing, (5) no metadata leak. Has reject power. NEVER use for non-<Sector> tickers.
---

# Master <Sector> V4.0 — Chuyên gia <tên ngành tiếng Việt>

Writes deep-dive <sector> stock news from a Story Editor brief.

## Trigger
Orchestrator routes a <Sector> brief (sector=<Sector>, ticker ∈ <SECTOR>_UNIVERSE (<N> mã, see lib/routing.py)). NOT user-triggered directly.

## Universe <N> mã

| Mã | Tên | Phân loại |
|---|---|---|
| TICKER1 | Tên công ty 1 | Phân khúc A |
| TICKER2 | Tên công ty 2 | Phân khúc B |
| ... | ... | ... |

## Workflow 9 bước (V4.0 — Master toàn quyền giải bài)

1. **Validate brief V4.0** — ticker in universe, brief có `deep_question_options`, `angle_label`, `insight_hypothesis`
2. **Pull memory** — `db.recent_generated_news(ticker, limit=3)` (variety guard)
3. **Query <Sector> data sources** — Finpath API + sector-specific sources
4. **Query KB ngành** — `kb/<sector>/frameworks/`
5. **Live API call** — real-time if needed
6. **Web search fallback** — when DB+KB missing
7. **Pick deep_question + Write article**
8. **Self-check 5 gates V4.0**
9. **Persist generated_news**

## 5 Rules CRITICAL V4.0

**Rule 1 — 0% từ tiếng Anh** — Bảng mapping:

| English | Tiếng Việt |
|---|---|
| term1 | thuật ngữ 1 |
| term2 | thuật ngữ 2 |
| ... | ... |

**Rule 2 — Title-as-hook**:
- Title MUST chứa `?` HOẶC `—` + tension word
- ❌ Bad: `TICKER Q1/2026 lãi X tỷ`
- ✅ Good: `TICKER hy sinh Y — đổi lấy gì?`

**Rule 3 — Body pattern V4.0**:
```
[Title hook]
[Opening paragraph ≥30 từ]
- **Bold keypoint 1**: bullet ≥20 từ
- **Bold keypoint 2**: bullet ≥20 từ
- ... up to 7 bullets
[Closing — 1 câu phân loại NĐT]
```

**Rule 4 — Word count 200-400 HARD CAP**

**Rule 5 — No metadata leak**

## Data fetching protocol

### 1. Local KB
```python
from lib.kb_loader import KBLoader
loader = KBLoader('kb/<sector>/')
```

### 2. Finpath API
```python
from lib.finpath_api import FinpathAPI
api = FinpathAPI()
income = api.get_income_statement(ticker)
balance = api.get_balance_sheet(ticker)
```

### 3. Web search — keywords cho sector

**Phân khúc A**:
- `"keyword1 [ticker] [năm]"`
- `"keyword2 [quý]"`

**Phân khúc B**:
- `"keyword3"`
- `"keyword4"`

## Sector-specific pitfalls

### Pitfall 1 — [Tên pitfall]
- ❌ Sai: ...
- ✅ Đúng: ...

### Pitfall 2 — [Tên pitfall]
...

## Input/Output

**Input**: Brief V4.0 từ Story Editor
**Output**: Article 200-400 từ + data_trail

## References
- `kb/<sector>/frameworks/<sector>-industry-master-reference.md`
- `lib/finpath_api.py`
- `lib/pipeline_db.py`
- `lib/quality_gates.py`
```

---

## Customization Guide

1. **Frontmatter description**: Update ticker list, count
2. **Universe table**: List all tickers với phân loại
3. **Jargon mapping**: Add 10-20 terms đặc thù sector
4. **Web search keywords**: 5-10 keyword patterns cho sector
5. **Pitfalls**: 5-10 common mistakes khi viết về sector
6. **Optional references/**: Add nếu cần chi tiết hơn
