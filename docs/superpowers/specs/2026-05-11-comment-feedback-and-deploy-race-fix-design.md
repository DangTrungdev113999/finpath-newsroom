# Phase H — Comment Feedback + Pipeline Deploy Race Fix Design

**Status:** Spec draft
**Date:** 2026-05-11
**Predecessor:** Phase G (multi-feed + Telegram channel→thread integration)

## 1. Goal

Add 2 features:

**Feature 1 — In-page comment feedback**
User on `/feed` can leave góp ý on each article via inline form at bottom-of-article. Submit caches locally + relays to a private Telegram feedback group via a Cloudflare Worker proxy.

**Feature 2 — Pipeline deploy race fix**
Pipeline `/tin` currently pushes Telegram link to `/article/<slug>` BEFORE GitHub Pages has deployed the new article. User clicking the Telegram link in the race window (potentially hours if human delays git push) hits 404. Fix: pipeline auto-pushes git, polls GitHub Actions for Pages deploy completion, then pushes Telegram with link guaranteed to work.

Both touch the Telegram↔Web flow → bundled in one spec, two phases.

## 2. Scope

**In scope:**
- Frontend comment UI (collapsed CTA, inline form, name capture, local history)
- localStorage schema + utils
- Cloudflare Worker proxy (validation, rate-limit, Telegram relay)
- Worker secrets management via `wrangler`
- Pipeline auto git push with self-heal (behind/lint/network errors)
- Pipeline Pages deploy poll (max 90s timeout, fallback)
- Telegram message format updates (feedback group + race fallback note)
- Pipeline observability log (new step entries)

**Out of scope (defer):**
- Comment moderation UI / admin dashboard
- Replies from admin → user (one-way for MVP)
- Comment edit/delete after submit (only client-local cache modifiable)
- Comment threading (each comment = standalone Telegram message)
- Anonymous mode (name is mandatory per Q6=A)
- Email notifications
- Cross-device sync (localStorage is per-device)

## 3. High-level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│ FEATURE 1 — Comment relay                                    │
│                                                              │
│  Browser (GitHub Pages static)                               │
│   │  POST /api/feedback {name, article_id, comment, ...}    │
│   ▼                                                          │
│  Cloudflare Worker (feedback-finpath.<sub>.workers.dev)     │
│   │  - CORS check (allow GH Pages origin)                   │
│   │  - Schema validate                                       │
│   │  - Rate-limit via KV (max 10/hour per client_id)        │
│   │  POST sendMessage                                        │
│   ▼                                                          │
│  Telegram bot → Group feedback (separate from channel)      │
│                                                              │
│  Side effects:                                               │
│   - localStorage: name, client_id, comment history per art. │
│   - KV namespace FEEDBACK_RL: rate-limit buckets             │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ FEATURE 2 — Race fix                                         │
│                                                              │
│  Current flow (race exists):                                 │
│    1-3. Crawler → Editor → Story Editor                      │
│    4. Master generate                                        │
│    5. Skeptic critique                                       │
│    6. Telegram push  ← link 404 risk                         │
│    7. Render markdown                                        │
│                                                              │
│  New flow (race-free):                                       │
│    1-3. (unchanged)                                          │
│    4-5. (unchanged) — per article                            │
│    6. Render markdown — per article (move earlier)          │
│    [Per-article loop ends, no Telegram yet]                 │
│    7. Auto git publish — single commit + push for batch     │
│    8. Wait Pages deploy — poll GH Actions API               │
│    9. Per article: Telegram push (link guaranteed)          │
└──────────────────────────────────────────────────────────────┘
```

## 4. Feature 1 — Comment Feedback

### 4.1 UI placement

`web/src/components/CompareFeedLayout.tsx` — render `<CommentSection>` at bottom of article, AFTER 2-col grid AND BEFORE next article's top border in `FeedPage.tsx`.

```
[ article header ]
[ 2-col grid: LeftColumn | RightColumn ]
[ ─── hr ─── ]
[ <CommentSection articleId articleTitle ticker /> ]
```

When `showRight=false` (focus mode), CommentSection still renders (constrained to `max-w-3xl mx-auto` matching LeftColumn width).

### 4.2 CommentSection component states

**Collapsed (default):**
```
┌──────────────────────────────────────────┐
│ 💬 Góp ý cho bài này  [Đã gửi: 3]       │  ← clickable
└──────────────────────────────────────────┘
```
- Badge `[Đã gửi: N]` only shown if `N > 0` (from localStorage)
- Click → expand

**Expanded (form):**
```
┌──────────────────────────────────────────┐
│ 💬 Góp ý cho bài này              [▴]   │
│ ─────────────────────────────────────── │
│ Tên: [_______________]   ← only first   │
│      "Tên sẽ lưu cho lần sau"           │
│                                          │
│ ┌──────────────────────────────────┐    │
│ │ (textarea autoresize 3-8 rows)   │    │
│ └──────────────────────────────────┘    │
│ {N}/1000 ký tự                          │
│                                          │
│ [Gửi]                                    │
│                                          │
│ ─────────────────────────────────────── │
│ Lịch sử góp ý của bạn (3):              │  ← Q4B read-back
│  • "câu opening hơi lủng"                │
│       2026-05-10 14:23                   │
│  • "thiếu context Vạn Thịnh Phát"        │
│       2026-05-10 15:01                   │
│  • "title hook đỉnh"                     │
│       2026-05-11 08:12                   │
└──────────────────────────────────────────┘
```

**Submit states:**
- `idle` → `submitting` (button "Đang gửi…", disabled, spinner)
- `submitting` → `success` → toast "✅ Đã gửi" + clear textarea + append history + badge +1
- `submitting` → `error` → toast "❌ Lỗi: <msg>" + KEEP textarea + NO history append

### 4.3 Validation rules (client-side)

| Field | Rule | Error message |
|---|---|---|
| name | required first time, 1-50 chars, strip control chars (allow Unicode/Vietnamese) | "Tên 1-50 ký tự" |
| comment | required, 5-1000 chars after trim | "Tối thiểu 5 ký tự" / "Tối đa 1000 ký tự" |
| dup check | same comment text within last 60s on same article → reject | "Bạn vừa gửi nội dung này, đợi 1 phút" |

### 4.4 localStorage schema

Key: `finpath-newsroom-feedback`

```typescript
interface FeedbackStorage {
  name: string | null;           // captured first submit
  client_id: string;             // uuid v4, generated once
  comments: {
    [article_id: string]: Array<{
      comment: string;
      timestamp: string;         // ISO 8601
      telegram_message_id?: number;  // null if Worker returned without msg id
    }>;
  };
}
```

Default initialization on first read:
```typescript
{
  name: null,
  client_id: crypto.randomUUID(),
  comments: {}
}
```

**Disabled localStorage handling:**
Wrap `localStorage.getItem/setItem` in try/catch. On failure → fallback to in-memory state (lost on reload). Show banner: "⚠️ Lưu trữ local bị tắt — lịch sử góp ý sẽ mất khi reload."

### 4.5 Cloudflare Worker contract

**Endpoint:** `POST https://feedback-finpath.<sub>.workers.dev/api/feedback`

**Request:**
```jsonc
{
  "name": "Trung",                          // required, 1-50 chars
  "article_id": "vcb-q1-lai-tang-9-...",    // public_slug
  "article_title": "VCB quý I: lãi vẫn tăng 9%...",
  "ticker": "VCB",                          // /^[A-Z]{3,4}$/
  "comment": "câu opening hơi lủng",        // 5-1000 chars
  "timestamp": "2026-05-11T08:12:34.567Z",  // ISO 8601 client time
  "client_id": "uuid-v4-string"             // for rate-limit bucket
}
```

**Responses:**
| Status | Body | Cause |
|---|---|---|
| 200 | `{"ok": true, "telegram_message_id": 123}` | Sent OK |
| 400 | `{"ok": false, "error": "validation", "field": "<f>", "message": "<m>"}` | Schema fail |
| 429 | `{"ok": false, "error": "rate_limited", "retry_after": 240}` | KV bucket exceeded |
| 502 | `{"ok": false, "error": "telegram_fail", "message": "<TG err>"}` | Telegram API rejected |

**CORS:**
- `Access-Control-Allow-Origin: https://dangtrungdev113999.github.io`
- `Access-Control-Allow-Methods: POST, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type`
- Preflight `OPTIONS` returns 204

**Rate-limit (KV):**
- Key: `rl:<client_id>:<hour_bucket>` where `hour_bucket = floor(unix_ts / 3600)`
- Value: count (incremented per request, TTL 3600s)
- Cap: 10/hour. Exceeded → 429 with `retry_after = 3600 - (now % 3600)` seconds.

**Validation logic** (inline, no Zod dep needed for ~5 fields):
- `name` 1-50 chars after trim, strip `/[\x00-\x1f]/g`
- `comment` 5-1000 chars after trim
- `ticker` matches `/^[A-Z]{3,4}$/`
- `article_id` 1-200 chars, slug pattern `/^[a-z0-9-]+$/`
- `client_id` valid UUID v4 pattern
- `timestamp` valid ISO date, not in future > 5min, not older > 1day

### 4.6 Telegram message format (feedback group)

Q5A flat — each comment = new message in group:

```html
💬 <b>Góp ý cho bài [VCB]</b>
<b>VCB quý I: lãi vẫn tăng 9% dù bỏ thêm 1.700 tỷ vào quỹ phòng nợ xấu</b>

<b>Trung</b>: câu opening hơi lủng

🔗 https://dangtrungdev113999.github.io/finpath-newsroom/article/vcb-q1-lai-tang-9-du-bo-them-1-700-ty-vao-quy-phong-no-xau
🕐 11/05/2026 08:12:34
```

Sent with `parse_mode=HTML`, `disable_web_page_preview=false` (preview useful for context).

**HTML escape:** Worker MUST escape `<`, `>`, `&` in `name`, `comment`, `article_title` before interpolating into HTML template.

## 5. Feature 2 — Race Condition Fix

### 5.1 Pipeline flow modification

**File:** `.claude/agents/newsroom-pipeline.md` Step 7 section

**Old per-article loop:**
```
For each picked brief:
  4. Master
  5. Skeptic
  6. Telegram push      ← race risk
  7. Render
```

**New per-article loop + batch tail:**
```
For each picked brief:
  4. Master
  5. Skeptic
  6. Render markdown    ← moved earlier (file ready before any Telegram)

After all articles done (BATCH-LEVEL, single execution):
  7. Auto git publish    ← lib/stages/run_git_publish.py
  8. Wait Pages deploy   ← lib/stages/run_pages_wait.py
  9. For each article: Telegram push (link guaranteed)
```

### 5.2 Auto git publish — `lib/stages/run_git_publish.py` (NEW)

**Purpose:** Single batch commit + push, self-heal common errors.

**Function signature:**
```python
def auto_git_publish(batch_id: str, article_count: int) -> dict:
    """
    Returns:
      {"ok": True, "commit_sha": "<sha>", "duration_ms": int, "self_heal_actions": []}
      OR
      {"ok": False, "error": "<reason>", "stage": "git_<step>", "stderr": "<truncated>"}
    """
```

**Algorithm:**
1. `git add output/compare-feed/ data/pipeline.db` (only output files + state DB)
2. `git commit -m "feat(content): auto-publish batch <batch_id> (<N> articles)"`
3. Try `git push` up to 3 attempts with self-heal:

   | Detected stderr signal | Self-heal action | Retry |
   |---|---|---|
   | `Your branch is behind` | `git pull --rebase` | yes |
   | `pre-commit hook failed` + `lint`/`format` | `cd web && npm run lint -- --fix; cd ..; git add -u` | yes |
   | `network` / `timeout` / `connection` | `time.sleep(2 ** attempt)` exponential backoff | yes |
   | Conflict in non-output files | `git rebase --abort`; FAIL with stage=git_conflict | no |
   | Auth fail / permission denied | FAIL with stage=git_auth | no |
   | Anything else | FAIL with stage=git_unknown | no |

4. After max attempts → fallback to FAIL.
5. On success → return commit SHA from `git rev-parse HEAD`.

**Self-heal log:** `self_heal_actions: ["git pull --rebase", "npm lint --fix"]` — for observability.

### 5.3 Pages deploy poll — `lib/stages/run_pages_wait.py` (NEW)

**Purpose:** Block until Pages deployment for the new commit succeeds.

**Function signature:**
```python
def wait_pages_deployed(commit_sha: str, timeout_s: int = 90) -> dict:
    """
    Returns:
      {"ok": True, "elapsed_s": int, "workflow_run_url": "<url>"}
      OR
      {"ok": False, "error": "<reason>", "elapsed_s": int, "fallback": "push_telegram_anyway"}
    """
```

**Algorithm:**
1. Loop until `time.time() - start > timeout_s` (default 90s):
   - GET `https://api.github.com/repos/<owner>/finpath-newsroom/actions/runs?head_sha={commit_sha}&event=push`
   - Auth header: `Authorization: Bearer <secrets.github.token>`
   - Find first `workflow_runs` matching deploy workflow (name="deploy")
   - If `status == "completed"`:
     - `conclusion == "success"` → return ok
     - `conclusion == "failure"` → return fail with run url
   - If still running → `time.sleep(5)` and continue
2. On timeout → return ok=False, fallback flag for caller.

**Caller behavior on timeout fallback:**
- Pipeline still proceeds to Step 9 (Telegram push) — body in thread is the primary content (T14b)
- Channel post format gets 1 extra line appended:
  ```
  ⚠️ Đang deploy, link có thể chưa work trong 30s
  ```
- Pipeline log records `pages_wait: {ok: false, fallback: "push_telegram_anyway"}` for observability.

**On `conclusion == "failure"`:**
- Pipeline FAILS the whole batch (deploy broken = link will never work, don't pollute Telegram with bad link).
- Log `pages_wait: {ok: false, error: "deploy failed", run_url: "..."}` so user can investigate.

### 5.4 Pipeline observability — new log entries

`pipeline_log` JSON gets 2 new keys per batch (not per article):

```json
{
  "step_7_git_publish": {
    "ok": true,
    "commit_sha": "abc123",
    "duration_ms": 4500,
    "self_heal_actions": ["git pull --rebase"]
  },
  "step_8_pages_wait": {
    "ok": true,
    "elapsed_s": 42,
    "workflow_run_url": "https://github.com/.../actions/runs/12345"
  }
}
```

Per-article `step_9_telegram` keeps existing schema from T14b.

`web/src/components/PipelineObservability.tsx` — extend STEP_LABELS array to include `step_7_git_publish` and `step_8_pages_wait` rendered as bonus rows below existing 6 steps.

## 6. Files

### Create

| Path | Purpose |
|---|---|
| `web/src/components/CommentSection.tsx` | Collapsed CTA + expanded form + history list |
| `web/src/lib/feedbackStorage.ts` | localStorage utils (get/set/append, fallback in-memory) |
| `web/src/lib/feedbackClient.ts` | POST to Worker, error handling |
| `worker/feedback.ts` | Cloudflare Worker entry |
| `worker/wrangler.toml` | Worker config (KV binding, env vars list) |
| `worker/README.md` | Setup instructions (wrangler login, secret put, deploy) |
| `lib/stages/run_git_publish.py` | Auto git push with self-heal |
| `lib/stages/run_pages_wait.py` | Poll GH Actions API for deploy |
| `tests/test_run_git_publish.py` | Unit tests for self-heal cases (mock subprocess) |
| `tests/test_run_pages_wait.py` | Unit tests for poll logic (mock GH API) |
| `web/src/components/__tests__/CommentSection.test.tsx` | Component tests (form states, validation, submit) |
| `web/src/lib/__tests__/feedbackStorage.test.ts` | localStorage utility tests |

### Modify

| Path | Change |
|---|---|
| `web/src/components/CompareFeedLayout.tsx` | Render `<CommentSection>` after grid, respect showRight constraint |
| `web/src/components/PipelineObservability.tsx` | Add `step_7_git_publish` + `step_8_pages_wait` rows |
| `web/src/types.ts` | Extend `PipelineLog` interface with new step keys |
| `.claude/agents/newsroom-pipeline.md` | Step 7 flow restructure (move render earlier, add 7-9 batch tail) |
| `data/secrets.yaml.example` | Add `feedback_group_chat_id` + `github.token` placeholders |
| `data/secrets.yaml` (gitignored) | User adds real values |

## 7. Secrets Management

### 7.1 Local pipeline secrets — `data/secrets.yaml`

Add to existing file (already has telegram bot_token + chat_id):

```yaml
telegram:
  bot_token: "<existing>"
  chat_id: "<existing>"
  linked_group_chat_id: "<existing>"
  feedback_group_chat_id: "<NEW — user provides after creating private group>"
  base_url: "<existing>"

github:
  token: "<NEW — Personal Access Token, scope: repo:read>"
  owner: "dangtrungdev113999"
  repo: "finpath-newsroom"
```

### 7.2 Cloudflare Worker secrets

Set via wrangler CLI (NOT in repo):

```bash
cd worker
wrangler secret put TELEGRAM_BOT_TOKEN
wrangler secret put TELEGRAM_FEEDBACK_GROUP_ID
```

KV namespace bind in `wrangler.toml`:

```toml
[[kv_namespaces]]
binding = "FEEDBACK_RL"
id = "<created via: wrangler kv:namespace create FEEDBACK_RL>"
```

Worker code reads `env.TELEGRAM_BOT_TOKEN`, `env.TELEGRAM_FEEDBACK_GROUP_ID`, `env.FEEDBACK_RL`.

## 8. Error Handling Summary

| Failure | Layer | Behavior |
|---|---|---|
| User submits empty comment | Frontend | Inline validation, button disabled |
| Worker 429 rate-limit | Frontend | Toast "⏰ Đợi vài phút", textarea kept |
| Worker 502 Telegram fail | Frontend | Toast "❌ Lỗi gửi", textarea kept, NO localStorage append |
| Network fail (Worker unreachable) | Frontend | Toast "❌ Mất kết nối, thử lại", textarea kept |
| localStorage disabled | Frontend | Banner warning, fallback in-memory |
| Telegram bot rate-limit (30/sec) | Worker | Forward 429 to client, log warning |
| Pipeline git push fail (auth) | Pipeline | FAIL batch, log stage=git_auth, pipeline_log records error |
| Pipeline git push fail (conflict) | Pipeline | FAIL batch, log stage=git_conflict |
| Pipeline Pages deploy timeout (90s) | Pipeline | Proceed to Telegram with fallback note in channel post |
| Pipeline Pages deploy failure | Pipeline | FAIL batch, do NOT push Telegram (avoid bad link) |

## 9. Testing Strategy

### Unit tests
- `tests/test_run_git_publish.py` — mock subprocess, verify self-heal triggers correct retry actions for each stderr signal
- `tests/test_run_pages_wait.py` — mock requests, verify poll loop, timeout, success/failure detection
- `web/src/lib/__tests__/feedbackStorage.test.ts` — verify get/set/append, fallback when localStorage throws
- `web/src/components/__tests__/CommentSection.test.tsx` — verify states (collapsed/expanded/submitting/success/error), validation messages, name capture flow

### Integration
- Worker local dev: `wrangler dev` + curl POST → verify CORS, validation, KV rate-limit (force 11 requests)
- Manual E2E: deploy Worker → submit feedback from `/feed` → verify message arrives in feedback Telegram group with correct format

### Pipeline E2E
- `/tin VCB` after fix → verify pipeline_log shows step 7 + 8 entries with self_heal_actions populated if any rebase happened
- Force race: delete remote main, run /tin → expect git_publish self-heal `git pull --rebase` triggered, eventually succeeds
- Force timeout: temporarily set `timeout_s=2` → verify Telegram fallback note appears in channel post

## 10. Phases

**Phase H1 — Race condition fix** (smaller, test fast)
- T1: Create `lib/stages/run_git_publish.py` + tests
- T2: Create `lib/stages/run_pages_wait.py` + tests
- T3: Modify `.claude/agents/newsroom-pipeline.md` Step 7 (move render earlier, add 7-9 batch tail)
- T4: Update `data/secrets.yaml.example` (add github.token + feedback_group_chat_id)
- T5: Extend `web/src/types.ts` PipelineLog + `PipelineObservability.tsx` rows
- T6: E2E `/tin VCB` verify pipeline_log structure + Telegram link works

**Phase H2 — Comment feature** (frontend + Worker)
- T7: Create `worker/feedback.ts` + `wrangler.toml` + setup docs
- T8: Deploy Worker (manual: `wrangler deploy`), set secrets, create KV namespace
- T9: Create `web/src/lib/feedbackStorage.ts` + tests
- T10: Create `web/src/lib/feedbackClient.ts`
- T11: Create `web/src/components/CommentSection.tsx` + tests
- T12: Wire into `CompareFeedLayout.tsx` (respect showRight constraint)
- T13: E2E manual — submit feedback from production `/feed`, verify message in Telegram group, verify localStorage history persists

**Tag end:** `v4.0-phase-h-feedback-and-deploy-race-fix`

## 11. Decisions Log

| # | Question | Choice | Rationale |
|---|---|---|---|
| 1 | Comment delivery architecture | B (Cloudflare Worker proxy) | Token safe server-side, free tier KV for rate-limit, independent of frontend deploy |
| 2 | Proxy host | Cloudflare Worker | No need to migrate from GitHub Pages, standalone subdomain free, KV included |
| 3 | Comment UI placement | B (collapsed CTA inline) | Avoids bloat in infinite scroll feed, expandable on demand |
| 4 | Read-back model | B (show local history) | User knows "đã gửi", avoids double-submit, no server read needed |
| 5 | Telegram threading in feedback group | A (flat with article header prefix) | Simplest, easy to migrate to forum topics if volume grows |
| 6 | Identity model | A (just name, mandatory) | Simplest, lower friction; admin reply via group is fine for MVP |
| 7 | Race condition fix | B (auto git push + poll deploy + Telegram) | Robust without major architecture change; ~30-60s pipeline penalty acceptable |
| 7b | Git push automation | Auto + self-heal common errors | User explicit: "tự động fix luôn nhé, rồi push lại" |

## 12. Open Questions / Risks

1. **GitHub Personal Access Token scope** — `repo:read` should suffice for Actions API GET. If GitHub adds finer-grained tokens for Actions, prefer that.
2. **Cloudflare Worker subdomain naming** — user must pick a Worker name when first running `wrangler deploy`. Default: `feedback-finpath`. URL becomes `feedback-finpath.<account-sub>.workers.dev`.
3. **Worker custom domain** — defer (use default workers.dev URL for MVP). Custom domain requires Cloudflare-managed DNS.
4. **Spam risk if Worker URL leaked** — KV rate-limit caps abuse to 10/hour per client_id. If client_id rotated maliciously → could grow. Add IP-based secondary limit if abuse seen.
5. **GH Actions polling cost** — each `/tin` adds 6-18 GH API calls (poll every 5s for 30-90s). Free tier limit 5000/hour, fine.
6. **Pre-commit hook auto-fix scope** — currently only handles `npm run lint --fix`. Other hooks (Python ruff, etc.) might need their own fixers; track in self_heal_actions and re-evaluate after first failures.
7. **Pages workflow name lookup** — `wait_pages_deployed` filters runs by workflow name="deploy". If workflow name changes in `.github/workflows/deploy.yml`, hardcoded string breaks. Consider passing workflow file name as parameter.
