# Phase G — Multi-pipeline + Feed UI + Telegram Design

**Date**: 2026-05-10
**Predecessor**: `2026-05-08-newsroom-v4-redesign.md` (V4.0) → Phase F polish (`v4.0-newsroom-redesign` tag) → Phase G
**Estimated scope**: ~15-18 atomic tasks, 8-10 hours subagent-driven
**Tag end**: `v4.0-phase-g-multi-feed-telegram`

---

## 1. Context

Sau Phase F polish + 3 live runs (MBB, ACB, VPB), pipeline Newsroom V4.0 stable nhưng còn 4 user-facing gaps:

1. **Story Editor cảm thấy bị ép pick 3 briefs** — output ACB + VPB toàn 3 articles dù chất lượng candidates không đồng đều. User feedback: "agent toàn chọn 3, cảm giác bị ép". Cần uncap + reject power preserved.

2. **Pipeline tuần tự bottleneck** — viết 1 ticker chạy ~15-20 phút. Khi muốn viết tin nhiều cổ phiếu cùng ngày (ACB + TPB + VPB) phải chờ tuần tự → user thời gian. Cần multi-pipeline parallel.

3. **UI list cards phân mảnh đọc** — user phải click vào từng card đọc separately. Notion-style feed (scroll dọc continuous, newest top) match mental model "đọc tin báo".

4. **Distribution thiếu** — bài viết xong sit trong localhost output. Không có channel push tin tới reader để comment/feedback. Telegram là kênh nhanh nhất MVP.

---

## 2. Architecture summary

4 streams + 1 prereq (T0). Sequence:

```
T0: SQLite WAL mode (BLOCKER cho Stream 2)
   ↓
Stream 1: Pipeline flow refactor (per-article cycle + Story Editor uncap)
   ↓ (independent)
Streams 2 + 3 + 4 parallel
```

Stream 1 ưu tiên vì refactor `newsroom-pipeline.md` workflow ảnh hưởng tất cả streams khác.

---

## 3. Stream 1 — Pipeline flow refactor

### 3.1. Story Editor uncapped + reject power preserved

**Decision (user)**: cho phép 0 brief (giữ pipeline reject power). Agent tự quyết theo merit, không default về 3.

**Files**:
- `.claude/skills/finpath-newsroom-story-editor/SKILL.md` — xóa hard cap "max 3 briefs", thêm rule "KHÔNG default về số nào — chọn theo merit, không cảm thấy phải fill quota"
- `.claude/agents/newsroom-story-editor.md` — sync agent prompt
- `newsroom-pipeline.md` Step 3 description — update output schema "0-N briefs" thay vì "0-3"

**Behavior**:
- 0 briefs (toàn candidates fail) → orchestrator Step 4 skip + reply "Batch không đủ chất lượng. Reject reasons: ..."
- N briefs (where N ≥ 1) → Step 4 loop N iterations

### 3.2. Per-article cycle (Master 1 → Skeptic 1 → Telegram 1 → Master 2 → ...)

**Current** (Phase F): Step 4 loop ALL briefs → Step 5 loop ALL articles. Batch processing.

**New** (Phase G): outer loop per brief, inner sequence Master → Skeptic → Telegram → next.

**Lợi ích**:
- Skeptic ECHO verification load fresh DB state per article (no race với batch persist)
- Variety guard memory accurate — Skeptic 2 thấy critique 1 đã persist
- Telegram push từng bài thay vì batch (better UX cho readers)
- Failure isolation — bài 1 fail không crash bài 2

**Files**:
- `.claude/agents/newsroom-pipeline.md` — refactor Step 4-5 thành single outer loop:
  ```
  for brief in briefs (1..N):
    Step 4: Task dispatch newsroom-master-bank(brief) → wait → article_id
    Step 5: Task dispatch newsroom-skeptic(article_id) → wait → critique
    Step 7 (NEW): Task dispatch newsroom-telegram-publisher(article_id) → wait → telegram_pushed_at
    log_pipeline_step observability
    next brief
  Step 6: Render markdown all batch articles (mechanical)
  ```

---

## 4. T0 — SQLite WAL mode prereq

**Decision (user)**: enable ngay (Phase G T0 BLOCKER).

**Why**: Stream 2 spawns N parallel pipelines viết cùng `data/pipeline.db`. SQLite default mode = single-writer lock → "database is locked" errors khi concurrent write contention.

**Files**:
- `lib/pipeline_db.py` — `__init__`:
  ```python
  self.conn.execute("PRAGMA journal_mode=WAL")
  self.conn.execute("PRAGMA synchronous=NORMAL")  # safe with WAL
  ```
- `.gitignore` — append `data/pipeline.db-wal` + `data/pipeline.db-shm` (WAL files)
- `tests/test_pipeline_db.py` — add test simulating 3 concurrent writes (threading.Thread × 3) → all succeed
- `data/pipeline.schema.sql` — add comment about WAL mode requirement

**Verification**: simulated parallel test passes. Run /tin-batch (Stream 2) → no lock errors.

---

## 5. Stream 2 — `/tin-batch` command

**Decision (user)**: syntax `/tin-batch ACB,TPB,VPB`.

### 5.1. New command file

**File**: `.claude/commands/tin-batch.md` (NEW)
```markdown
---
description: Viết bài tin chuyên sâu cho NHIỀU mã cổ phiếu Bank cùng lúc
argument-hint: <TICKER1,TICKER2,TICKER3,...>
allowed-tools: Bash, Task, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

Trigger N pipeline 6-step Newsroom V4.0 PARALLEL cho list tickers comma-separated.

Universe MVP Bank: TCB · VCB · MBB · ACB · BID · CTG · VPB.

Parse $ARGUMENTS comma-separated → list tickers. Validate mỗi ticker:
- Thuộc universe → spawn pipeline
- Không thuộc universe → log warn + skip ticker đó

Spawn N newsroom-pipeline agents PARALLEL via single message multiple Task calls.

Output cuối: aggregate báo cáo từ N pipelines.
```

### 5.2. Parallel spawn implementation

Orchestrator (caller of /tin-batch) dispatches N newsroom-pipeline agents trong **single message multiple Task tool calls** — Claude Code sẽ run parallel.

```python
# Pseudocode trong tin-batch handler
tickers = parse_args($ARGUMENTS)  # ["ACB", "TPB", "VPB"]
valid_tickers = [t for t in tickers if t in UNIVERSE]

# Single message với N Task calls → parallel execution
results = parallel_dispatch([
    Task(subagent_type="newsroom-pipeline", prompt=f"ticker={t}")
    for t in valid_tickers
])

# Aggregate
for ticker, result in zip(valid_tickers, results):
    print(f"✅ {ticker}: {result['articles_count']} articles, {result['batch_id']}")
```

### 5.3. Idempotency + collision safety

- **DB row collision**: each pipeline có own `funnel_batch_id` (timestamp-based) → no row_id conflict. Existing `crawl_log.source_url` UNIQUE constraint catches dup URLs across batches.
- **Manifest.json write contention**: 3 pipelines viết `output/compare-feed/manifest.json` cùng lúc → race condition. Fix: file lock (fcntl) hoặc atomic write (temp file + rename). Recommend atomic write.
- **WAL mode** (T0) handles SQLite write serialization automatically.

**Files**:
- `.claude/commands/tin-batch.md` (NEW)
- `lib/render_compare_feed.py` — `update_manifest` add atomic write (temp file + os.rename)

### 5.4. Parallel pipeline observability

Mỗi pipeline log riêng vào pipeline_log của articles trong batch của nó. No cross-contamination — `step_N` per article, not global.

---

## 6. Stream 3 — Feed UI (Cards | Feed toggle)

**Decisions (user)**:
- Cards default, feed là tab thứ 2
- Right column trong feed: full 8 sections
- Mobile responsive: <768px 1-col stacked

### 6.1. Header toggle component

**File**: `web/src/components/Header.tsx` (NEW or extend existing)
- Top bar: logo + 2 tabs `[Cards] [Feed]` + ticker filter chips (optional)
- Active tab highlighted, click route đổi
- Sticky on scroll

### 6.2. New FeedPage

**File**: `web/src/pages/FeedPage.tsx` (NEW)
- Route: `/feed`
- Load manifest.json → sort by `crawled_at` desc (newest top)
- Render ALL articles stacked với `<CompareFeedLayout>` (reuse existing)
- Visual separator: `border-t-4 border-fg/20 pt-12 mt-12` giữa articles
- Newest article auto-scroll-to-top khi mount (optional smooth UX)

### 6.3. Performance — virtualization

**Library**: `react-window` (variable size list)
- Add to `web/package.json`: `"react-window": "^1.8.10"` + `@types/react-window`
- Wrap article list in `<VariableSizeList>` — only render articles visible in viewport + buffer
- Lazy load markdown content per article khi enter viewport

**Risk**: variable row height tricky cho dynamic markdown. Fallback: simple infinite scroll (load 5 đầu, IntersectionObserver trigger fetch thêm 5 khi scroll near bottom).

### 6.4. Mobile responsive

**Tailwind breakpoints**:
- `<768px` (mobile/tablet small): 1-col stacked. Left col (article body) trên + right col dưới collapse default.
- `≥768px` (md): 2-col như hiện tại.
- `≥1024px` (lg): wider columns, more breath.

**Files**:
- `web/src/components/CompareFeedLayout.tsx` — flex layout responsive với `md:flex-row` `flex-col` etc.
- `web/src/components/RightColumn.tsx` — wrap content trong `<details>` với `md:open` (default mở trên desktop, đóng trên mobile)

### 6.5. Routing

- `/` → IndexPage (cards) — DEFAULT
- `/feed` → FeedPage (NEW)
- `/article/<slug>` → ArticlePage (single article, deep-link giữ nguyên)

**Files**:
- `web/src/App.tsx` — add `/feed` route
- `web/src/components/Header.tsx` — toggle nav

---

## 7. Stream 4 — Telegram bot publisher (NEW agent + module)

**Decisions (user)**:
- Group destination (2-way comment)
- Format MVP: title + link (sẽ tune sau)
- URL: localhost (sẽ host sau)
- **Tách thành agent riêng** (không inline trong newsroom-pipeline)

### 7.1. New agent: `newsroom-telegram-publisher`

**File**: `.claude/agents/newsroom-telegram-publisher.md` (NEW)
```markdown
---
name: newsroom-telegram-publisher
description: Telegram publisher V4.0 — sau khi 1 article hoàn tất Skeptic critique + render markdown, push title + link tới Telegram group cho readers nhận xét. Idempotent (skip nếu telegram_pushed_at đã set). Use when newsroom-pipeline dispatches Step 7 per article.
tools: Bash, Read
model: sonnet
---

# Telegram Publisher Agent V4.0

Push article notification tới Telegram group sau khi article ready.

## Input
{
  "article_id": "<uuid>",
  "title": "<article title>",
  "public_slug": "<URL slug>"
}

## Workflow

### 1. Idempotency check
Query DB: SELECT telegram_pushed_at FROM generated_news WHERE article_id = ?
Nếu != NULL → SKIP, return {status: "already_pushed"}.

### 2. Load secrets
Read data/secrets.yaml → telegram.bot_token + chat_id + base_url.
Nếu file không tồn tại → SKIP với warning "secrets.yaml missing — Telegram disabled".

### 3. Build message
Plain text format MVP:
<b>{title}</b>

{base_url}/article/{public_slug}

### 4. POST to Telegram Bot API
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d chat_id=<chat_id> \
  -d text=<message> \
  -d parse_mode=HTML \
  -d disable_web_page_preview=false

### 5. Persist telegram_pushed_at
UPDATE generated_news SET telegram_pushed_at = datetime('now') WHERE article_id = ?

## Output
{
  "status": "pushed" | "already_pushed" | "skipped_no_secrets" | "failed",
  "telegram_message_id": <int | null>,
  "error": <string | null>
}

## Hard rules
- KHÔNG retry on failure — log + return failed (orchestrator decides retry policy)
- KHÔNG block pipeline nếu Telegram fail (graceful degrade)
- KHÔNG log secrets ra stdout
- secrets.yaml MUST gitignored
```

### 7.2. Telegram publisher module

**File**: `lib/telegram_publisher.py` (NEW)
```python
import json
import urllib.request
import urllib.parse
import yaml
from pathlib import Path

class TelegramPublisher:
    def __init__(self, bot_token: str, chat_id: str, base_url: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = base_url.rstrip("/")
    
    def publish_article(self, title: str, public_slug: str) -> dict:
        """Push article notification. Returns {status, telegram_message_id, error}."""
        message = f"<b>{self._escape_html(title)}</b>\n\n{self.base_url}/article/{public_slug}"
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": "false",
        }).encode("utf-8")
        try:
            with urllib.request.urlopen(url, data=data, timeout=10) as resp:
                result = json.loads(resp.read())
                if result.get("ok"):
                    return {"status": "pushed", "telegram_message_id": result["result"]["message_id"], "error": None}
                return {"status": "failed", "telegram_message_id": None, "error": result.get("description", "Unknown")}
        except Exception as e:
            return {"status": "failed", "telegram_message_id": None, "error": str(e)}
    
    @staticmethod
    def _escape_html(text: str) -> str:
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def load_telegram_config(secrets_path: Path = Path("data/secrets.yaml")) -> TelegramPublisher | None:
    """Load TG config from secrets.yaml. Returns None if file missing or telegram section absent."""
    if not secrets_path.exists():
        return None
    config = yaml.safe_load(secrets_path.read_text())
    tg = config.get("telegram") if config else None
    if not tg or not all(k in tg for k in ("bot_token", "chat_id", "base_url")):
        return None
    return TelegramPublisher(tg["bot_token"], tg["chat_id"], tg["base_url"])
```

### 7.3. Secrets file template

**File**: `data/secrets.yaml.example` (committed — template)
```yaml
# Copy this file to data/secrets.yaml and fill in values.
# data/secrets.yaml MUST be gitignored (already in .gitignore).
telegram:
  bot_token: "1234567890:ABCdef..."  # Get from @BotFather
  chat_id: "-1001234567890"           # Group chat_id (get via Telegram getUpdates API)
  base_url: "http://localhost:5174"   # Update to public URL when hosted
```

**File**: `.gitignore` — add `data/secrets.yaml`

### 7.4. DB schema migration

**File**: `data/pipeline.schema.sql`
```sql
ALTER TABLE generated_news ADD COLUMN telegram_pushed_at TIMESTAMP NULL;
CREATE INDEX idx_generated_telegram_pushed ON generated_news(telegram_pushed_at);
```

### 7.5. Pipeline integration

`newsroom-pipeline.md` Step 7 (NEW intra-cycle):
```
For each brief in briefs:
  Step 4: Master Bank → article_id
  Step 5: Skeptic → critique
  Step 7 (NEW): Task dispatch newsroom-telegram-publisher(article_id, title, public_slug)
                Wait → log telegram_message_id + status
  log_pipeline_step("step_7_telegram", payload)
```

### 7.6. Tests

**File**: `tests/test_telegram_publisher.py` (NEW)
- `test_publisher_init_with_config`
- `test_publisher_html_escape` (title chứa "<b>" → escape)
- `test_publisher_push_success` (mock urlopen)
- `test_publisher_push_failure_returns_error` (mock 400 response)
- `test_load_config_missing_file_returns_none`
- `test_load_config_missing_telegram_section_returns_none`
- `test_load_config_full_returns_publisher`

### 7.7. User setup steps

After Phase G ship, user phải:
1. Tạo Telegram bot qua @BotFather → copy bot_token
2. Tạo Telegram group → add bot vào group
3. Send message "/start" trong group
4. Get chat_id qua: `curl https://api.telegram.org/bot<TOKEN>/getUpdates` → tìm `chat.id` (negative number cho group)
5. `cp data/secrets.yaml.example data/secrets.yaml` + fill values
6. Run `/tin <TICKER>` → verify message landed in group

---

## 8. Files to modify (overview)

**Backend Python (~6 files)**:
- `lib/pipeline_db.py` (T0 WAL)
- `lib/render_compare_feed.py` (manifest atomic write)
- `lib/telegram_publisher.py` (NEW)
- `data/pipeline.schema.sql` (telegram_pushed_at + WAL note)
- `data/secrets.yaml.example` (NEW template)
- `.gitignore` (WAL files + secrets.yaml)

**Tests (~3 files)**:
- `tests/test_pipeline_db.py` (concurrent write test)
- `tests/test_telegram_publisher.py` (NEW)
- `tests/test_render_compare_feed.py` (atomic manifest write)

**Skills + agents (~5 files)**:
- `.claude/skills/finpath-newsroom-story-editor/SKILL.md` (uncap rule)
- `.claude/agents/newsroom-story-editor.md` (sync uncap)
- `.claude/agents/newsroom-pipeline.md` (per-article cycle + Step 7 Telegram + uncap N briefs)
- `.claude/agents/newsroom-telegram-publisher.md` (NEW)
- `.claude/commands/tin-batch.md` (NEW)

**React (~5 files)**:
- `web/package.json` (+ react-window)
- `web/src/App.tsx` (/feed route + Header)
- `web/src/components/Header.tsx` (NEW or extend)
- `web/src/pages/FeedPage.tsx` (NEW)
- `web/src/components/CompareFeedLayout.tsx` (mobile responsive)
- `web/src/components/RightColumn.tsx` (mobile collapse default)

**Total**: ~17 files modified, 6 new modules/files.

---

## 9. Verification approach

### 9.1. Unit tests
- `pytest tests/` — all pre-existing 110 + new tests pass
- Concurrent write test (3 threads × 3 writes) → all succeed under WAL
- Telegram publisher mock tests cover happy path + failure modes

### 9.2. E2E
- `/tin-batch ACB,TPB,VPB` from Claude Code CLI → 3 pipelines parallel → no SQLite lock errors → 3-9 articles output
- Telegram messages received in group (1 per article)
- pipeline_log có step_7_telegram entry per article
- Re-run /tin VPB → telegram NOT re-pushed (idempotency)

### 9.3. Visual
- `cd web && npm run dev` → localhost:5174
- Click [Cards] tab → IndexPage with cards
- Click [Feed] tab → FeedPage with stacked articles
- Resize browser <768px → 1-col stacked, right col collapse default
- Newest article on top
- Scroll fast → no janky rendering (virtualization works)

### 9.4. Cost benchmark (close out Phase F T12)
- Run /tin-batch ACB,TPB (2 pipelines parallel, real Task dispatch)
- Query pipeline_log per article → confirm:
  - step_2_editor.model == "sonnet"
  - step_3_story_editor.model == "opus"
  - At least 1 step has tokens != null
- Compare total tokens vs MBB pre-Phase F baseline → ~30-40% reduction expected

---

## 10. Risks / open issues

1. **WAL .wal/.shm files** — must gitignore properly. Backup process must include all 3 files (db + wal + shm).
2. **Manifest atomic write** — fcntl on macOS works, on Windows needs different lock. MVP target macOS only.
3. **react-window variable height** — known tricky cho dynamic markdown content. Fallback: IntersectionObserver simple infinite scroll.
4. **Telegram rate limit** — 30 msg/sec. Per-article publish OK; nếu 5 pipelines × 3 articles parallel = 15 msg burst → may need throttle (sleep between pushes).
5. **Telegram chat_id leak** — if user shares secrets.yaml accidentally. Documentation hard-call: NEVER commit secrets.yaml.
6. **Multi-pipeline output collision** — 3 pipelines viết cùng `output/compare-feed/`. Filename uses public_slug (unique per article), no collision. Manifest needs atomic write.
7. **Browser autoscroll mobile** — newest article auto-scroll-to-top có thể annoy user reading. Default off, opt-in via setting.
8. **Telegram message_id persisted but no use yet** — phase H sẽ dùng để edit/delete message khi article rewritten. Ship now, use later.

---

## 11. Open questions (defer to Phase G2 / G3)

- Telegram message rich format (markdown bold + bullets + image) — user prefer plain MVP first
- Telegram thread/topic per ticker (Telegram Forum feature) — defer
- Web public hosting (Vercel/Netlify deploy) — user sẽ làm sau
- Multi-language support (English version cho international readers) — out of scope MVP
- Webhook integration (Telegram → callback when user comments) — Phase H
- Pipeline scheduling (cron auto /tin daily) — Phase H

---

## 12. Success criteria

Phase G ship khi:
- [ ] Story Editor uncap verified — 1 run output 1-2 briefs (not forced 3)
- [ ] /tin-batch ACB,TPB ran parallel without SQLite lock errors
- [ ] Per-article cycle: Master 1 → Skeptic 1 → Telegram 1 sequential per brief
- [ ] Feed UI: Cards|Feed toggle works, stacked articles scrollable, mobile 1-col
- [ ] Telegram messages land in group (1 per article)
- [ ] Idempotency: re-run /tin same ticker không push Telegram lại
- [ ] All tests green (110 + new tests)
- [ ] Phase F T12 cost benchmark closed out (real Task dispatch validated)

---

## 13. Out of scope

- Edit/delete Telegram messages on article rewrite
- Web hosting deployment
- Multi-language
- Comment ingestion từ Telegram (1-way push only MVP)
- Pipeline cron scheduling
- Master factual citation gate (Phase F2 backlog from MBB run finding)

---

## 14. Changelog

- 2026-05-10: Initial spec — 9 user clarifications confirmed via brainstorming skill, Stream 4 Telegram tách thành agent riêng per user feedback
