# Feedback Worker — Cloudflare deploy guide

Comment feedback proxy: receives POST from `/feed` page, validates, rate-limits, forwards to Telegram.

## One-time setup (USER must do, subagent cannot)

1. Install wrangler if not present:
   ```bash
   npm i -g wrangler
   ```

2. Login to Cloudflare:
   ```bash
   wrangler login
   ```

3. Create KV namespace for rate-limiting:
   ```bash
   cd worker
   wrangler kv:namespace create FEEDBACK_RL
   # Copy the printed `id` into wrangler.toml replacing REPLACE_WITH_KV_ID_FROM_WRANGLER_OUTPUT
   ```

4. Set secrets:
   ```bash
   wrangler secret put TELEGRAM_BOT_TOKEN
   # Paste bot token from data/secrets.yaml `telegram.bot_token`

   wrangler secret put TELEGRAM_FEEDBACK_GROUP_ID
   # Paste the FEEDBACK group chat id (NOT the article channel chat id)
   # Format: -100xxxxxxxxxx (with -100 prefix for supergroup)
   ```

5. Deploy:
   ```bash
   wrangler deploy
   # Output prints Worker URL: https://feedback-finpath.<account>.workers.dev
   ```

6. Add Worker URL to GitHub Actions secrets:
   - GitHub repo → Settings → Secrets and variables → Actions
   - Add new secret: `VITE_FEEDBACK_WORKER_URL` = `https://feedback-finpath.<account>.workers.dev`

7. Trigger Pages rebuild so new env var is baked in:
   ```bash
   git commit --allow-empty -m "trigger pages rebuild for VITE_FEEDBACK_WORKER_URL"
   git push
   ```

8. Verify: open production `/feed`, check that "💬 Góp ý cho bài này" CTA appears under each article.

## Local dev

```bash
cd worker
wrangler dev
# Hits http://localhost:8787/api/feedback
```

In `web/.env.local`:
```
VITE_FEEDBACK_WORKER_URL=http://localhost:8787
```

Then `cd web && npm run dev` → comment section uses local Worker.

## CORS

Worker allows: `https://dangtrungdev113999.github.io`, `http://localhost:5174`, `http://localhost:5175`. Other origins → 403.

## Rate limit

Per `client_id` (uuid in browser localStorage): max 10 requests/hour.
Stored in KV bucket key `rl:<client_id>:<hour_bucket>` with 1h TTL.
