// web/src/components/CommentSection.tsx
import { useState, useMemo, useRef } from 'react';
import { Feather, Send, ChevronDown, Check, AlertCircle, Loader2, Sprout, Plus } from 'lucide-react';
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

// Pre-fill templates — chip label + leading sentence the user continues writing from.
// Each template targets a real reader pain mapped to V4.0 quality gates (CLAUDE.md).
const PROMPT_TEMPLATES: Array<{ label: string; prefill: string }> = [
  {
    label: 'Title chưa đủ hấp dẫn',
    prefill: 'Title (hook) chưa đủ hấp dẫn. Với mình, title hợp hơn với bài này nên là: ',
  },
  {
    label: 'Bài dài quá',
    prefill: 'Bài này dài quá, theo mình nên gọn lại còn khoảng … từ. Lý do: ',
  },
  {
    label: 'Đọc xong không đọng insight',
    prefill: 'Mình đọc xong không đọng lại insight gì trong đầu. Phần làm mình hụt nhất là: ',
  },
  {
    label: 'Bài thiếu mặt rủi ro',
    prefill: 'Bài đang nhìn hơi một chiều, mình thấy phần rủi ro chưa rõ. Cụ thể: ',
  },
  {
    label: 'Có từ tiếng Anh khó hiểu',
    prefill: 'Bài có từ tiếng Anh / chuyên ngành mình thấy khó hiểu, nên được dịch hoặc giải thích: ',
  },
  {
    label: 'Số liệu thiếu so sánh',
    prefill: 'Có vài số liệu trong bài đứng một mình, chưa rõ so cùng kỳ / quý trước / peer thế nào. Ví dụ: ',
  },
  {
    label: 'Không rõ dành cho NĐT loại nào',
    prefill: 'Đọc xong mình chưa thấy rõ bài phù hợp NĐT loại nào (ngắn hạn / giá trị / cổ tức / dài hạn). Theo mình bài nên nói rõ: ',
  },
  {
    label: 'Nội dung sai so với thực tế',
    prefill: 'Mình thấy có chỗ trong bài chưa khớp với thực tế. Cụ thể chỗ sai là: ',
  },
  {
    label: 'Văn cần bình dân + "nguy hiểm" hơn',
    prefill: 'Giọng văn bài này cần bình dân hơn (gần với NĐT retail thật) và "nguy hiểm" hơn (sắc bén, không an toàn). Cụ thể: ',
  },
];

export function CommentSection({ articleId, articleTitle, ticker }: Props) {
  // Feature flag — entire section absent in environments without Worker URL
  if (!isFeedbackEnabled()) return null;

  const [expanded, setExpanded] = useState(false);
  const [state, setState] = useState<FormState>('idle');
  const [errMsg, setErrMsg] = useState<string | null>(null);
  const [comment, setComment] = useState('');
  const [nameInput, setNameInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  function applyTemplate(prefill: string) {
    // If user already has substantial text, append on a fresh line instead of overwriting.
    const next = comment.trim().length >= MIN_COMMENT ? `${comment.trimEnd()}\n\n${prefill}` : prefill;
    setComment(next);
    // Focus + jump cursor to end on next tick (after React commits)
    requestAnimationFrame(() => {
      const el = textareaRef.current;
      if (!el) return;
      el.focus();
      const pos = next.length;
      el.setSelectionRange(pos, pos);
    });
  }

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
    <section className="mt-10">
      <button
        type="button"
        onClick={() => setExpanded((v) => !v)}
        className={`group flex w-full items-center gap-4 rounded-xl border border-fg-4/40 bg-bg-1 px-4 py-3 text-left shadow-[0_1px_0_rgba(0,0,0,0.02)] transition-all duration-200 ease-out hover:border-brand/50 hover:bg-bg-1 hover:shadow-[0_1px_0_rgba(0,0,0,0.02),0_10px_24px_-18px_hsl(var(--brand)/0.45)] ${
          expanded ? 'border-brand/50 shadow-[0_1px_0_rgba(0,0,0,0.02),0_10px_24px_-18px_hsl(var(--brand)/0.45)]' : ''
        }`}
        aria-expanded={expanded}
      >
        <span
          className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-brand/10 text-brand transition-transform duration-300 ease-out group-hover:rotate-[-6deg] ${
            expanded ? 'rotate-[-10deg] bg-brand/15' : ''
          }`}
        >
          <Feather size={15} strokeWidth={1.75} />
        </span>

        <span className="min-w-0 flex-1 font-serif text-[1.15rem] italic text-fg-0">
          Góp ý cho bài này
        </span>

        {history.length > 0 && (
          <span className="hidden shrink-0 items-center gap-1 rounded-full bg-brand/10 px-2.5 py-1 text-[0.72rem] font-medium text-brand sm:inline-flex">
            <span className="tabular-nums">{history.length}</span>
            <span className="text-fg-3/70">·</span>
            <span className="text-fg-2">đã gửi</span>
          </span>
        )}

        <ChevronDown
          size={16}
          strokeWidth={2}
          className={`shrink-0 text-fg-3 transition-transform duration-300 ease-out ${
            expanded ? 'rotate-180 text-brand' : 'group-hover:translate-y-0.5'
          }`}
        />
      </button>

      {expanded && (
        <div className="mt-3 rounded-2xl bg-bg-1 px-6 py-6 shadow-[0_1px_0_rgba(0,0,0,0.02),0_10px_40px_-20px_rgba(0,0,0,0.10)] animate-[commentReveal_400ms_ease-out] sm:px-8 sm:py-7">
          {storageDisabled && (
            <p className="mb-5 flex items-start gap-2 text-xs italic text-warn">
              <AlertCircle size={13} className="mt-0.5 shrink-0" strokeWidth={1.75} />
              <span>Lưu trữ local bị tắt — lịch sử góp ý sẽ mất khi reload trang.</span>
            </p>
          )}

          {/* Inline editor's note — không phải alert box, chỉ là một dòng prose ấm */}
          <p className="mb-6 flex items-start gap-2.5 text-[1.08rem] font-semibold leading-relaxed text-done">
            <Sprout size={18} strokeWidth={2} className="mt-[5px] shrink-0 text-done" />
            <span>Cảm ơn sự góp ý của bạn.</span>
          </p>

          {showNameField && (
            <label className="mb-7 block">
              <span className="sr-only">Tên của bạn</span>
              <input
                type="text"
                placeholder="Ký tên bạn ở đây…"
                value={nameInput}
                onChange={(e) => setNameInput(e.target.value)}
                maxLength={MAX_NAME}
                className="w-full border-b border-fg-4/50 bg-transparent px-0 py-2 font-serif text-[1.05rem] italic text-fg-0 placeholder:text-fg-3/55 placeholder:italic focus:border-brand focus:outline-none transition-colors"
              />
              <span className="mt-1.5 block font-serif text-[0.85rem] italic text-fg-3">
                Chỉ cần nhập lần đầu — lần sau trình duyệt của bạn sẽ tự nhớ.
              </span>
            </label>
          )}

          <div className="mb-4 flex flex-wrap gap-x-2.5 gap-y-2">
            {PROMPT_TEMPLATES.map((t) => (
              <button
                key={t.label}
                type="button"
                onClick={() => applyTemplate(t.prefill)}
                className="group/chip inline-flex items-center gap-1.5 rounded-full bg-bg-3/70 px-3.5 py-1.5 text-[0.92rem] font-medium text-fg-1 transition-colors duration-150 hover:bg-brand/[0.10] hover:text-brand focus-visible:bg-brand/[0.10] focus-visible:text-brand focus-visible:outline-none active:scale-[0.97]"
              >
                <Plus
                  size={13}
                  strokeWidth={2.25}
                  className="text-fg-3 transition-colors group-hover/chip:text-brand"
                />
                {t.label}
              </button>
            ))}
          </div>

          <label className="block">
            <span className="sr-only">Góp ý của bạn</span>
            <textarea
              ref={textareaRef}
              placeholder="Viết ở đây — không cần dài, càng cụ thể càng tốt…"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              maxLength={MAX_COMMENT}
              rows={5}
              className="w-full resize-y rounded-xl bg-bg-0/50 px-4 py-3.5 font-serif text-[1.05rem] leading-relaxed text-fg-0 placeholder:italic placeholder:text-fg-3/55 focus:bg-bg-0/80 focus:outline-none focus:ring-2 focus:ring-brand/35 transition-all"
            />
            <div className="mt-1.5 pr-1 text-right text-[0.72rem]">
              <span
                className={`tabular-nums ${
                  trimmedComment.length > MAX_COMMENT * 0.9 ? 'text-brand' : 'text-fg-3/70'
                }`}
              >
                {trimmedComment.length}/{MAX_COMMENT}
              </span>
            </div>
          </label>

          <div className="mt-6 flex flex-wrap items-center gap-x-4 gap-y-2">
            <button
              type="button"
              onClick={onSubmit}
              disabled={!canSubmit}
              className="group/btn inline-flex items-center gap-2 rounded-full bg-brand px-6 py-2.5 font-serif text-[0.98rem] italic text-brand-fg shadow-[0_1px_0_rgba(0,0,0,0.04),0_8px_22px_-12px_hsl(var(--brand)/0.65)] transition-all duration-200 hover:bg-brand-hot hover:-translate-y-0.5 hover:shadow-[0_1px_0_rgba(0,0,0,0.06),0_14px_28px_-12px_hsl(var(--brand)/0.75)] active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:translate-y-0 disabled:hover:shadow-[0_1px_0_rgba(0,0,0,0.04),0_8px_22px_-12px_hsl(var(--brand)/0.65)]"
            >
              {state === 'submitting' ? (
                <>
                  <Loader2 size={14} strokeWidth={2.25} className="animate-spin" />
                  <span>Đang gửi…</span>
                </>
              ) : (
                <>
                  <Send
                    size={13}
                    strokeWidth={2.25}
                    className="transition-transform duration-300 group-hover/btn:translate-x-0.5 group-hover/btn:-translate-y-0.5"
                  />
                  <span>Gửi góp ý</span>
                </>
              )}
            </button>

            {state === 'success' && (
              <span className="inline-flex items-center gap-1.5 text-sm text-done animate-[fadeSlide_300ms_ease-out]">
                <Check size={14} strokeWidth={2.25} />
                Đã ghi nhận — cảm ơn bạn.
              </span>
            )}
            {state === 'error' && errMsg && (
              <span className="inline-flex max-w-md items-start gap-1.5 text-sm text-rec">
                <AlertCircle size={14} strokeWidth={2} className="mt-0.5 shrink-0" />
                <span>{errMsg}</span>
              </span>
            )}
          </div>

          {history.length > 0 && (
            <div className="mt-6 border-t border-fg-4/40 pt-4">
              <div className="mb-3 text-[0.78rem] font-medium text-fg-2">
                Bạn đã gửi{' '}
                <span className="tabular-nums text-brand">{history.length}</span>{' '}
                góp ý cho bài này
              </div>
              <ol className="space-y-3 pl-0">
                {history
                  .slice()
                  .reverse()
                  .map((h, i) => (
                    <li
                      key={`${h.timestamp}-${i}`}
                      className="border-l-2 border-brand/25 pl-3"
                    >
                      <p className="text-[0.92rem] leading-relaxed text-fg-1">
                        {h.comment}
                      </p>
                      <p className="mt-0.5 text-[0.72rem] tabular-nums text-fg-3">
                        {new Date(h.timestamp).toLocaleString('vi-VN', {
                          year: 'numeric',
                          month: '2-digit',
                          day: '2-digit',
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </p>
                    </li>
                  ))}
              </ol>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
