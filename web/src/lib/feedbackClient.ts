// web/src/lib/feedbackClient.ts
/**
 * POST feedback to Cloudflare Worker proxy.
 * Worker URL injected at build time via VITE_FEEDBACK_WORKER_URL.
 * If env var missing → isFeedbackEnabled() returns false; UI hides.
 */

const WORKER_URL = import.meta.env.VITE_FEEDBACK_WORKER_URL as string | undefined;

export const isFeedbackEnabled = (): boolean => Boolean(WORKER_URL && WORKER_URL.startsWith('http'));

export interface FeedbackPayload {
  name: string;
  article_id: string;
  article_title: string;
  ticker: string;
  comment: string;
  timestamp: string;
  client_id: string;
}

export interface FeedbackOk {
  ok: true;
  telegram_message_id: number;
}

export interface FeedbackErr {
  ok: false;
  error: 'validation' | 'rate_limited' | 'telegram_fail' | 'network' | 'disabled';
  message?: string;
  field?: string;
  retry_after?: number;
}

export type FeedbackResult = FeedbackOk | FeedbackErr;

export async function submitFeedback(payload: FeedbackPayload): Promise<FeedbackResult> {
  if (!isFeedbackEnabled()) {
    return { ok: false, error: 'disabled', message: 'Feature flag off (no Worker URL)' };
  }
  try {
    const resp = await fetch(`${WORKER_URL}/api/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const json = (await resp.json()) as FeedbackResult;
    return json;
  } catch (e) {
    return {
      ok: false,
      error: 'network',
      message: e instanceof Error ? e.message : 'unknown network error',
    };
  }
}
