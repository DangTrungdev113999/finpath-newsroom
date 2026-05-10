// web/src/components/CommentSection.tsx
import { useState, useMemo } from 'react';
import {
  appendComment,
  getCommentsForArticle,
  getStorage,
  isStorageDisabled,
  saveName,
} from '../lib/feedbackStorage';
import { isFeedbackEnabled, submitFeedback } from '../lib/feedbackClient';

interface Props {
  articleId: string;
  articleTitle: string;
  ticker: string;
}

type FormState = 'idle' | 'submitting' | 'success' | 'error';

const MIN_COMMENT = 5;
const MAX_COMMENT = 1000;
const MIN_NAME = 1;
const MAX_NAME = 50;

export function CommentSection({ articleId, articleTitle, ticker }: Props) {
  // Feature flag — entire section absent in environments without Worker URL
  if (!isFeedbackEnabled()) return null;

  const [expanded, setExpanded] = useState(false);
  const [state, setState] = useState<FormState>('idle');
  const [errMsg, setErrMsg] = useState<string | null>(null);
  const [comment, setComment] = useState('');
  const [nameInput, setNameInput] = useState('');

  // Refresh on each render so badge count + history always live.
  // Cheap (sync read) — fine for low-volume feedback UI.
  const storage = getStorage();
  const savedName = storage.name;
  const history = getCommentsForArticle(articleId);
  const showNameField = !savedName;
  const storageDisabled = useMemo(() => isStorageDisabled(), []);

  const trimmedComment = comment.trim();
  const trimmedName = nameInput.trim();
  const effectiveName = savedName ?? trimmedName;
  const canSubmit =
    trimmedComment.length >= MIN_COMMENT &&
    trimmedComment.length <= MAX_COMMENT &&
    effectiveName.length >= MIN_NAME &&
    effectiveName.length <= MAX_NAME &&
    state !== 'submitting';

  async function onSubmit() {
    if (!canSubmit) return;
    setState('submitting');
    setErrMsg(null);

    // Capture name on first submit
    if (showNameField) saveName(trimmedName);

    const payload = {
      name: effectiveName,
      article_id: articleId,
      article_title: articleTitle,
      ticker,
      comment: trimmedComment,
      timestamp: new Date().toISOString(),
      client_id: storage.client_id,
    };

    const result = await submitFeedback(payload);
    if (result.ok) {
      appendComment(articleId, {
        comment: trimmedComment,
        timestamp: payload.timestamp,
        telegram_message_id: result.telegram_message_id,
      });
      setComment('');
      setState('success');
      setTimeout(() => setState('idle'), 2500);
      return;
    }

    // Error path — KEEP textarea
    let msg = result.message ?? 'Lỗi không xác định';
    if (result.error === 'rate_limited') {
      msg = `Bạn đang góp ý quá nhanh, đợi vài phút (${result.retry_after ?? 240}s)`;
    } else if (result.error === 'validation') {
      msg = `Lỗi nhập liệu (${result.field}): ${result.message ?? 'không hợp lệ'}`;
    } else if (result.error === 'telegram_fail') {
      msg = `Không gửi được tới Telegram: ${result.message ?? ''}`;
    } else if (result.error === 'network') {
      msg = 'Mất kết nối, thử lại nhé';
    } else if (result.error === 'disabled') {
      msg = 'Tính năng góp ý đang tắt (build thiếu Worker URL)';
    }
    setErrMsg(msg);
    setState('error');
  }

  return (
    <section className="mt-8 border-t border-fg-4/40 pt-6">
      <button
        type="button"
        onClick={() => setExpanded((v) => !v)}
        className="flex w-full items-center justify-between rounded-md bg-bg-2 px-4 py-3 text-sm font-semibold text-fg-1 transition-colors hover:bg-bg-3/60"
        aria-expanded={expanded}
      >
        <span>
          💬 Góp ý cho bài này
          {history.length > 0 && (
            <span className="ml-2 rounded-pill bg-bg-3 px-2 py-0.5 text-xs font-normal text-fg-2">
              Đã gửi: {history.length}
            </span>
          )}
        </span>
        <span className="text-fg-3">{expanded ? '▴' : '▾'}</span>
      </button>

      {expanded && (
        <div className="mt-3 rounded-md border border-fg-4/40 bg-bg-1 p-4">
          {storageDisabled && (
            <div className="mb-3 rounded-md bg-warn/10 px-3 py-2 text-xs text-warn">
              ⚠️ Lưu trữ local bị tắt — lịch sử góp ý sẽ mất khi reload.
            </div>
          )}

          {showNameField && (
            <div className="mb-3">
              <label className="mb-1 block text-xs font-semibold text-fg-2">Tên</label>
              <input
                type="text"
                placeholder="Tên (sẽ lưu cho lần sau)"
                value={nameInput}
                onChange={(e) => setNameInput(e.target.value)}
                maxLength={MAX_NAME}
                className="w-full rounded-md border border-fg-4 bg-bg-1 px-3 py-2 text-sm text-fg-0 focus:border-brand focus:outline-none"
              />
            </div>
          )}

          <textarea
            placeholder="Nhập góp ý (5-1000 ký tự)…"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            maxLength={MAX_COMMENT}
            rows={3}
            className="w-full resize-y rounded-md border border-fg-4 bg-bg-1 px-3 py-2 text-sm text-fg-0 focus:border-brand focus:outline-none"
          />
          <div className="mt-1 text-right text-xs text-fg-3">
            {trimmedComment.length}/{MAX_COMMENT} ký tự
          </div>

          <div className="mt-3 flex items-center gap-3">
            <button
              type="button"
              onClick={onSubmit}
              disabled={!canSubmit}
              className="rounded-md bg-brand px-4 py-2 text-sm font-medium text-brand-fg transition-colors hover:bg-brand-hot disabled:cursor-not-allowed disabled:opacity-50"
            >
              {state === 'submitting' ? 'Đang gửi…' : 'Gửi'}
            </button>
            {state === 'success' && (
              <span className="text-sm text-done">✅ Đã gửi</span>
            )}
            {state === 'error' && errMsg && (
              <span className="text-sm text-rec">❌ {errMsg}</span>
            )}
          </div>

          {history.length > 0 && (
            <div className="mt-5 border-t border-fg-4/40 pt-4">
              <h4 className="mb-2 text-xs font-semibold uppercase tracking-wide text-fg-3">
                Lịch sử góp ý của bạn ({history.length})
              </h4>
              <ul className="space-y-2 pl-0 text-sm">
                {history.map((h, i) => (
                  <li key={i} className="border-l-2 border-fg-4/60 pl-3">
                    <div className="text-fg-1">{h.comment}</div>
                    <div className="text-xs text-fg-3">
                      {new Date(h.timestamp).toLocaleString('vi-VN')}
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
