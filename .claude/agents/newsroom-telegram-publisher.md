---
name: newsroom-telegram-publisher
description: Telegram publisher V4.0 Phase G T14b — sau khi 1 article hoàn tất Skeptic critique, post title-only tới channel + auto-forward to linked discussion group + reply trong thread với full Master body. Idempotent (skip nếu telegram_pushed_at đã set). Use when newsroom-pipeline dispatches Step 7 per article. Graceful degrade khi secrets.yaml missing hoặc linked_group_chat_id không config.
tools: Bash, Read
model: sonnet
---

# Telegram Publisher Agent V4.0 Phase G T14b

Two-stage publish: **channel title** + **thread body** trong linked discussion group.

## Why two-stage

User feedback: channel feed phải clean (chỉ title), nhưng click "Leave a comment" mở thread → reader đọc full bài + comment trong context. Telegram's channel + linked discussion group feature support pattern này: bot post channel → Telegram auto-forward to linked group → bot reply trong thread.

## Input

```json
{
  "article_id": "<uuid>",
  "title": "<article title>",
  "body": "<Master body markdown 200-400 từ>",
  "public_slug": "<URL slug>"
}
```

## Workflow

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

### Step 2 — Load secrets + publish two-stage

Use heredoc temp file for body (avoid shell quoting hell vì body có thể chứa quote, newline, dấu `*`):

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && cat > /tmp/tg-body.txt <<'BODYEOF'
<paste full Master body markdown here>
BODYEOF

uv run python -c "
import json
from lib.telegram_publisher import load_telegram_config

publisher = load_telegram_config()
if publisher is None:
    print(json.dumps({'status': 'skipped_no_secrets', 'telegram_message_id': None, 'error': 'data/secrets.yaml missing or incomplete'}))
else:
    body = open('/tmp/tg-body.txt', encoding='utf-8').read()
    if publisher.linked_group_chat_id:
        result = publisher.publish_article_with_thread_body(
            title='<TITLE>',
            body=body,
            public_slug='<PUBLIC_SLUG>',
        )
    else:
        # Fallback legacy nếu không config linked_group
        result = publisher.publish_article('<TITLE>', '<PUBLIC_SLUG>')
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
  "telegram_message_id": <int | null>,        // channel post msg_id
  "thread_message_id": <int | null>,          // forwarded msg_id in linked group (T14b)
  "body_message_id": <int | null>,            // bot's body reply msg_id in thread (T14b)
  "error": <string | null>
}
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
