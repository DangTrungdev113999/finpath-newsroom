// worker/feedback.ts
/**
 * Cloudflare Worker — comment feedback proxy.
 *
 * Endpoint: POST /api/feedback
 * Validates payload, rate-limits per client_id (KV), forwards to Telegram
 * group as a flat text message.
 *
 * Secrets (set via `wrangler secret put`):
 *   TELEGRAM_BOT_TOKEN
 *   TELEGRAM_FEEDBACK_GROUP_ID
 *
 * KV binding (in wrangler.toml):
 *   FEEDBACK_RL — rate-limit buckets (key: rl:<client_id>:<hour>)
 */

interface Env {
  TELEGRAM_BOT_TOKEN: string;
  TELEGRAM_FEEDBACK_GROUP_ID: string;
  FEEDBACK_RL: KVNamespace;
}

const ALLOWED_ORIGINS = [
  'https://dangtrungdev113999.github.io',
  'http://localhost:5174',
  'http://localhost:5175',
];

const MAX_REQS_PER_HOUR = 10;
const SECONDS_PER_HOUR = 3600;

const TICKER_RE = /^[A-Z]{3,4}$/;
const SLUG_RE = /^[a-z0-9-]+$/;
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

interface FeedbackPayload {
  name: string;
  article_id: string;
  article_title: string;
  ticker: string;
  comment: string;
  timestamp: string;
  client_id: string;
}

function corsHeaders(origin: string | null): Record<string, string> {
  const allowed = origin && ALLOWED_ORIGINS.includes(origin) ? origin : '';
  return {
    'Access-Control-Allow-Origin': allowed,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Vary': 'Origin',
  };
}

function jsonResponse(body: unknown, status: number, origin: string | null): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) },
  });
}

function htmlEscape(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function validate(p: Partial<FeedbackPayload>): { ok: true; v: FeedbackPayload } | { ok: false; field: string; message: string } {
  if (!p.name || typeof p.name !== 'string') return { ok: false, field: 'name', message: 'thiếu' };
  const name = p.name.trim().replace(/[\x00-\x1f]/g, '');
  if (name.length < 1 || name.length > 50) return { ok: false, field: 'name', message: '1-50 ký tự' };

  if (!p.comment || typeof p.comment !== 'string') return { ok: false, field: 'comment', message: 'thiếu' };
  const comment = p.comment.trim();
  if (comment.length < 5 || comment.length > 1000) return { ok: false, field: 'comment', message: '5-1000 ký tự' };

  if (!p.ticker || !TICKER_RE.test(p.ticker)) return { ok: false, field: 'ticker', message: 'invalid ticker' };
  if (!p.article_id || !SLUG_RE.test(p.article_id) || p.article_id.length > 200) {
    return { ok: false, field: 'article_id', message: 'invalid slug' };
  }
  if (!p.article_title || typeof p.article_title !== 'string' || p.article_title.length > 500) {
    return { ok: false, field: 'article_title', message: 'invalid title' };
  }
  if (!p.client_id || !UUID_RE.test(p.client_id)) return { ok: false, field: 'client_id', message: 'invalid uuid' };

  if (!p.timestamp || typeof p.timestamp !== 'string') return { ok: false, field: 'timestamp', message: 'thiếu' };
  const ts = Date.parse(p.timestamp);
  if (isNaN(ts)) return { ok: false, field: 'timestamp', message: 'invalid ISO' };
  const nowMs = Date.now();
  if (ts > nowMs + 5 * 60 * 1000) return { ok: false, field: 'timestamp', message: 'in future' };
  if (ts < nowMs - 24 * 60 * 60 * 1000) return { ok: false, field: 'timestamp', message: 'too old' };

  return {
    ok: true,
    v: {
      name,
      article_id: p.article_id,
      article_title: p.article_title,
      ticker: p.ticker,
      comment,
      timestamp: p.timestamp,
      client_id: p.client_id,
    },
  };
}

async function rateLimitCheck(kv: KVNamespace, client_id: string): Promise<{ ok: true } | { ok: false; retry_after: number }> {
  const nowSec = Math.floor(Date.now() / 1000);
  const hourBucket = Math.floor(nowSec / SECONDS_PER_HOUR);
  const key = `rl:${client_id}:${hourBucket}`;
  const current = parseInt((await kv.get(key)) ?? '0', 10);
  if (current >= MAX_REQS_PER_HOUR) {
    const retry_after = SECONDS_PER_HOUR - (nowSec % SECONDS_PER_HOUR);
    return { ok: false, retry_after };
  }
  await kv.put(key, String(current + 1), { expirationTtl: SECONDS_PER_HOUR });
  return { ok: true };
}

function buildTelegramMessage(p: FeedbackPayload, baseUrl: string): string {
  const url = `${baseUrl}/article/${p.article_id}`;
  const tsLocal = new Date(p.timestamp).toLocaleString('vi-VN', {
    timeZone: 'Asia/Ho_Chi_Minh',
    hour12: false,
  });
  return [
    `💬 <b>Góp ý cho bài [${htmlEscape(p.ticker)}]</b>`,
    `<b>${htmlEscape(p.article_title)}</b>`,
    ``,
    `<b>${htmlEscape(p.name)}</b>: ${htmlEscape(p.comment)}`,
    ``,
    `🔗 ${url}`,
    `🕐 ${tsLocal}`,
  ].join('\n');
}

async function postTelegram(env: Env, text: string): Promise<{ ok: true; message_id: number } | { ok: false; message: string }> {
  const url = `https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`;
  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: env.TELEGRAM_FEEDBACK_GROUP_ID,
      text,
      parse_mode: 'HTML',
      disable_web_page_preview: false,
    }),
  });
  const data = (await resp.json()) as { ok: boolean; result?: { message_id: number }; description?: string };
  if (data.ok && data.result) {
    return { ok: true, message_id: data.result.message_id };
  }
  return { ok: false, message: data.description ?? 'unknown telegram error' };
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const origin = req.headers.get('Origin');
    const url = new URL(req.url);

    if (req.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }

    if (url.pathname !== '/api/feedback' || req.method !== 'POST') {
      return jsonResponse({ ok: false, error: 'not_found' }, 404, origin);
    }

    if (!origin || !ALLOWED_ORIGINS.includes(origin)) {
      return jsonResponse({ ok: false, error: 'origin_not_allowed' }, 403, origin);
    }

    let payload: Partial<FeedbackPayload>;
    try {
      payload = (await req.json()) as Partial<FeedbackPayload>;
    } catch {
      return jsonResponse({ ok: false, error: 'validation', message: 'invalid json' }, 400, origin);
    }

    const v = validate(payload);
    if (!v.ok) {
      return jsonResponse({ ok: false, error: 'validation', field: v.field, message: v.message }, 400, origin);
    }

    const rl = await rateLimitCheck(env.FEEDBACK_RL, v.v.client_id);
    if (!rl.ok) {
      return jsonResponse({ ok: false, error: 'rate_limited', retry_after: rl.retry_after }, 429, origin);
    }

    const baseUrl = origin.replace(/\/$/, '') + (origin.endsWith('github.io') ? '/finpath-newsroom' : '');
    const text = buildTelegramMessage(v.v, baseUrl);

    const tg = await postTelegram(env, text);
    if (!tg.ok) {
      return jsonResponse({ ok: false, error: 'telegram_fail', message: tg.message }, 502, origin);
    }

    return jsonResponse({ ok: true, telegram_message_id: tg.message_id }, 200, origin);
  },
};
