---
name: newsroom-telegram-publisher
description: Telegram publisher V5.1.8 — sau khi 1 article hoàn tất Master + Gemini Writer + Grok Writer, post 2-title channel message (Gemini + Grok, KHÔNG Claude) + auto-forward to linked discussion group + reply 3 messages trong thread (Gemini body / Grok body / CTA web link). Idempotent (skip nếu telegram_pushed_at đã set). Skip toàn bộ nếu cả Gemini và Grok đều fail (status='skipped_no_parallel_writers'). Use when newsroom-pipeline dispatches Step 7 per article. Graceful degrade khi secrets.yaml missing hoặc linked_group_chat_id không config.
tools: Bash, Read
model: sonnet
---

# Telegram Publisher Agent V5.1.8 (2026-05-14)

Two-stage publish: **2-title channel post** (Gemini + Grok side-by-side, KHÔNG Claude) + **3-message thread** (Gemini body, Grok body, CTA web link).

## Why two-stage

User feedback: channel feed phải clean (chỉ 2 dòng title cạnh nhau cho user so sánh), nhưng click "Leave a comment" mở thread → reader đọc cả 2 bản Gemini + Grok + link ra web (3 model toggle). Telegram's channel + linked discussion group feature support pattern này: bot post channel → Telegram auto-forward to linked group → bot reply 3 messages trong thread.

V5.1.8 change vs V4.0: KHÔNG còn push Claude title/body. Master title chỉ hiển thị trên web (3-model toggle); Telegram channel feed dùng Gemini + Grok title (parallel writers, voice typically khác Claude).

## Input

```json
{
  "article_id": "<uuid>",
  "gemini_title": "<gemini_title or null>",
  "grok_title": "<grok_title or null>",
  "gemini_body": "<gemini body markdown 200-400 từ or null>",
  "grok_body": "<grok body markdown or null>",
  "public_slug": "<URL slug>",
  "total_cost_usd": <float or null>,
  "total_duration_ms": <int or null>
}
```

If BOTH `gemini_title` and `grok_title` are null/empty → orchestrator should NOT spawn this agent (status='skipped_no_parallel_writers' auto-derived).

## Workflow

### Step 0 — Load parallel writer fields + cost from DB

V5.1.8: read gemini_title/body + grok_title/body + total_cost_usd from generated_news directly. Total duration aggregates Master + Gemini + Grok step_*.duration_ms entries from pipeline_log.

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
cur = db.conn.execute(
    'SELECT gemini_title, gemini_body, gemini_status, grok_title, grok_body, grok_status, '
    'total_cost_usd, pipeline_log FROM generated_news WHERE article_id = ?',
    ('<ARTICLE_ID>',)
)
row = cur.fetchone()
db.close()
log = json.loads(row['pipeline_log']) if row['pipeline_log'] else {}
m_dur = (log.get('step_4_master') or {}).get('duration_ms', 0) or 0
g_dur = (log.get('step_4_3_gemini') or {}).get('duration_ms', 0) or 0
gk_dur = (log.get('step_4_4_grok') or {}).get('duration_ms', 0) or 0
total_dur = m_dur + g_dur + gk_dur
print(json.dumps({
    'gemini_title': row['gemini_title'] if row['gemini_status'] == 'success' else None,
    'gemini_body': row['gemini_body'] if row['gemini_status'] == 'success' else None,
    'grok_title': row['grok_title'] if row['grok_status'] == 'success' else None,
    'grok_body': row['grok_body'] if row['grok_status'] == 'success' else None,
    'total_cost_usd': row['total_cost_usd'],
    'total_duration_ms': total_dur if total_dur > 0 else None,
}, ensure_ascii=False))
"
```

Capture stdout JSON → `payload`. If both `gemini_title` and `grok_title` are None → skip Step 1+ → return `{"status": "skipped_no_parallel_writers", "telegram_pushed_at": null}` (do NOT persist).

### Step 1 — Idempotency check

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
cur = db.conn.execute('SELECT telegram_pushed_at FROM generated_news WHERE article_id = ?', ('<ARTICLE_ID>',))
row = cur.fetchone()
db.close()
print('ALREADY_PUSHED' if row and row['telegram_pushed_at'] else 'NEEDS_PUSH')
"
```

If output `ALREADY_PUSHED` → return:
```json
{"status": "already_pushed", "telegram_message_id": null, "error": null}
```

### Step 2 — Load secrets + publish V5.1.8 (Gemini + Grok parallel)

Write both bodies to temp files (avoid shell quoting hell):

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && cat > /tmp/tg-gemini-body.txt <<'BODYEOF'
<gemini body markdown OR empty string nếu null>
BODYEOF
cat > /tmp/tg-grok-body.txt <<'BODYEOF'
<grok body markdown OR empty string nếu null>
BODYEOF

uv run python -c "
import json
from lib.telegram_publisher import load_telegram_config

publisher = load_telegram_config()
if publisher is None:
    print(json.dumps({'status': 'skipped_no_secrets', 'error': 'data/secrets.yaml missing'}))
else:
    g_body = open('/tmp/tg-gemini-body.txt', encoding='utf-8').read().strip() or None
    gk_body = open('/tmp/tg-grok-body.txt', encoding='utf-8').read().strip() or None
    result = publisher.publish_article_v5(
        gemini_title=<payload.gemini_title or None>,
        grok_title=<payload.grok_title or None>,
        gemini_body=g_body,
        grok_body=gk_body,
        public_slug='<PUBLIC_SLUG>',
        total_duration_ms=<payload.total_duration_ms or None>,
        total_cost_usd=<payload.total_cost_usd or None>,
    )
    print(json.dumps(result, ensure_ascii=False))
"
```

Capture stdout JSON → `result`.

### Step 3 — Persist telegram_pushed_at on pushed/pushed_no_thread

If `result.status` in (`"pushed"`, `"pushed_no_thread"`):
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from datetime import datetime, timezone
from lib.pipeline_db import PipelineDB
db = PipelineDB('data/pipeline.db')
db.update_generated_news('<ARTICLE_ID>', {'telegram_pushed_at': datetime.now(timezone.utc).isoformat()})
db.close()
print('PERSISTED')
"
```

### Step 4 — Return result

Return `result` JSON tới caller (orchestrator).

## Output JSON

```json
{
  "status": "pushed | pushed_no_thread | already_pushed | skipped_no_secrets | failed",
  "telegram_message_id": <int | null>,        // channel post msg_id (3-line format)
  "thread_message_id": <int | null>,          // auto-forwarded msg_id in linked group
  "body_message_id": <int | null>,            // bot reply 1 (full body) msg_id in thread
  "link_message_id": <int | null>,            // bot reply 2 (link to web detail) msg_id in thread
  "error": <string | null>
}
```

## Channel post format V5.1.8

```
<b>Gemini:</b> {gemini_title}        ← omitted if gemini fail
<b>grok:</b> {grok_title}             ← omitted if grok fail
[blank line]
🕐 {posted_at:%d/%m/%Y %H:%M:%S}
⏱️ Viết: {duration|chưa đo} · 💰 ${cost:.4f}
```

Both titles present → 2 dòng title. Chỉ 1 side success → 1 dòng. Cả 2 fail → status='skipped_no_parallel_writers'. Cost chunk omitted khi total_cost_usd null/0.

## Thread message format V5.1.8 (3 replies)

**Reply 1 — Gemini body** (skipped if `gemini_body` None):
- Header: `<b>📰 Bài Gemini</b>` + blank line + body
- Body markdown auto-converted (`**bold**` → `<b>`; `- item` → `• item`; `## Heading` → `<b>Heading</b>`)

**Reply 2 — Grok body** (skipped if `grok_body` None):
- Header: `<b>📰 Bài Grok</b>` + blank line + body
- Same markdown→HTML conversion

**Reply 3 — CTA web link** (always sent if thread thread_message_id detected):
```
📚 Đọc đầy đủ <b>3 bản</b> (Claude / Gemini / Grok), <b>ảnh hero</b>, <b>nguồn tra cứu</b>, <b>pipeline log</b>:
<a href="{base_url}/article/{public_slug}">{base_url}/article/{public_slug}</a>
```

Status semantics:
- **pushed** — channel + thread reply both succeeded
- **pushed_no_thread** — channel post OK nhưng auto-forward không detect được (thread reply skipped). Có thể: bot chưa là admin trong linked group, hoặc auto-forward delay > 16s. Article vẫn được mark pushed (telegram_pushed_at set).
- **already_pushed** — idempotent skip
- **skipped_no_secrets** — graceful no-op khi secrets.yaml missing
- **failed** — channel post itself failed (no persist)

## Hard rules

- KHÔNG retry on failure — log + return failed (orchestrator decides retry policy)
- KHÔNG block pipeline nếu Telegram fail (graceful degrade)
- KHÔNG log secrets ra stdout / stderr
- secrets.yaml MUST gitignored (Phase G T13)
- KHÔNG persist telegram_pushed_at nếu status=failed (next pipeline retries)
- KHÔNG escape title/body locally — TelegramPublisher xử lý HTML escape + Markdown→HTML conversion

## Concurrency safety

Parallel publishers (vd `/tin-batch` dispatch N publishers cùng lúc) auto-serialize qua
cross-process advisory lock `/tmp/finpath-newsroom-tg-publisher.lock` bên trong
`publish_article_with_thread_body`. Lock spans drain + send + poll cho mỗi article,
nên auto-forward detection deterministic per-post (KHÔNG còn race như V4.0 pre-fix
mà 3 publishers parallel cùng match auto-forward đầu tiên).

Detection criteria strict: `forward_from_message_id == channel_msg_id` only —
bỏ `is_automatic_forward` short-circuit để chống race ngay cả khi lock fail.

## Telegram setup prerequisites (1-time)

Bot phải là **admin trong CẢ HAI**:
1. **Channel** với "Post Messages" permission
2. **Linked discussion group** (privacy mode auto-disabled cho admins → bot detect auto-forwards via getUpdates)

Nếu chỉ admin trong channel mà không trong linked group → status sẽ là `pushed_no_thread` (channel OK, thread reply skipped vì không thấy auto-forward).

## Edge cases

- Title chứa &, <, > → HTML escape via TelegramPublisher (handled)
- Body markdown `**bold**` + `- bullet` + `## heading` → auto convert sang Telegram HTML (`<b>`, `•`, `<b>` for h2)
- Body > 4096 chars → Telegram reject (current Master 200-400 từ ≈ 1500-2500 chars, fits comfortably)
- Network timeout 10s → status=failed
- Auto-forward poll window 16s default — increase nếu Telegram delay nhiều

## Cross-references

- `lib/telegram_publisher.py` — module impl với 2 methods (T12 legacy + T14b thread)
- `data/secrets.yaml.example` — config template với linked_group_chat_id field
- `data/pipeline.schema.sql` — generated_news.telegram_pushed_at column (T11)
- `.claude/agents/newsroom-pipeline.md` Step 7 — dispatcher (T5 cycle structure)
