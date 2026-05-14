import { useState } from 'react';
import { useId } from 'react';
import { Check, Loader2 } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogDescription,
} from '../shared/ui/dialog';
import { signInPuter } from '../lib/puterTTS';
import { cn } from '../shared/lib/cn';

interface Props {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  /** Called after a successful Puter sign-in — caller resumes the gated
   *  action (e.g. starts TTS playback). */
  onAuthenticated: () => void;
}

/**
 * Auth-gate dialog shown when a visitor clicks "Nghe bài" without a Puter
 * session. Visual metaphor: a press-pass / concert-ticket invitation
 * printed on cream paper — perforated stub footer, brand-amber wax-seal
 * primary CTA. Frames the third-party login as an inviting one-step ritual
 * rather than a paywall.
 *
 * Wraps the Radix Dialog primitive at `shared/ui/dialog.tsx`.
 */
export function LoginPromptDialog({ open, onOpenChange, onAuthenticated }: Props) {
  const grainId = useId();
  const [status, setStatus] = useState<'idle' | 'loading' | 'error'>('idle');

  async function handleSignIn() {
    setStatus('loading');
    const ok = await signInPuter();
    if (ok) {
      setStatus('idle');
      onOpenChange(false);
      onAuthenticated();
    } else {
      setStatus('error');
    }
  }

  return (
    <Dialog
      open={open}
      onOpenChange={(next) => {
        if (!next) setStatus('idle');
        onOpenChange(next);
      }}
    >
      <DialogContent className="!max-w-[420px] !rounded-2xl !border-fg-4/35 !bg-[#f7eedb]">
        {/* paper grain — fractal noise tinted warm sepia */}
        <svg
          aria-hidden
          className="pointer-events-none absolute inset-0 h-full w-full mix-blend-multiply opacity-[0.14]"
        >
          <filter id={grainId}>
            <feTurbulence
              type="fractalNoise"
              baseFrequency="0.92"
              numOctaves="2"
              stitchTiles="stitch"
            />
            <feColorMatrix values="0 0 0 0 0.35  0 0 0 0 0.22  0 0 0 0 0.12  0 0 0 0.9 0" />
          </filter>
          <rect width="100%" height="100%" filter={`url(#${grainId})`} />
        </svg>

        <div className="relative px-6 pb-5 pt-7">
          {/* press-pass header chip */}
          <div className="mb-4 inline-flex items-center gap-2 rounded-sm border border-[#3a2618]/45 bg-[#ede1c2] px-2.5 py-1">
            <span aria-hidden className="flex items-end gap-[2px]">
              {[3, 6, 4, 8, 5].map((h, i) => (
                <span
                  key={i}
                  style={{ height: `${h * 1.5}px`, width: '2px' }}
                  className="bg-[#3a2618]"
                />
              ))}
            </span>
            <span className="font-mono text-[9.5px] font-bold uppercase tracking-[0.28em] text-[#3a2618]">
              Audio · Press-pass
            </span>
          </div>

          {/* headline */}
          <DialogTitle className="!font-display !text-[24px] !leading-[1.15] !font-bold !text-[#1d130a] !tracking-tight">
            Ghé Puter một lần,
            <br />
            <em className="not-italic text-[#6b1a1a]">mở giọng đọc miễn phí.</em>
          </DialogTitle>

          <DialogDescription className="!mt-3 !font-sans !text-[13px] !leading-relaxed !text-[#3a2618]">
            Giọng tiếng Việt do Puter cung cấp — nền tảng AI bên thứ 3, hoàn
            toàn miễn phí, không cần thẻ. Một cửa sổ đăng nhập mở ra, xong
            việc thì quay về đây — bài tin vẫn nguyên vị trí.
          </DialogDescription>

          {/* trust checks — 3 lines, ink check + sepia text */}
          <ul className="mt-5 space-y-2">
            {[
              ['Miễn phí', 'không thẻ tín dụng, không gia hạn'],
              ['Mở popup, không refresh', 'bài đang đọc giữ nguyên vị trí'],
              ['Một tài khoản dùng tất cả', 'TTS / chat / storage của Puter'],
            ].map(([head, tail]) => (
              <li key={head} className="flex items-start gap-2.5">
                <span
                  aria-hidden
                  className="mt-[3px] flex h-4 w-4 shrink-0 items-center justify-center rounded-full"
                  style={{
                    backgroundColor: '#3a2618',
                  }}
                >
                  <Check
                    className="h-2.5 w-2.5 text-[#f7eedb]"
                    strokeWidth={3.5}
                  />
                </span>
                <span className="font-sans text-[12.5px] leading-snug text-[#1d130a]">
                  <span className="font-semibold">{head}</span>
                  <span className="text-[#3a2618]/75"> — {tail}</span>
                </span>
              </li>
            ))}
          </ul>

          {/* inline error */}
          {status === 'error' && (
            <p className="mt-4 rounded-sm border border-[#6b1a1a]/40 bg-[#6b1a1a]/10 px-2.5 py-1.5 font-sans text-[11.5px] text-[#6b1a1a]">
              Đăng nhập không hoàn tất. Cửa sổ Puter có thể đã bị chặn
              popup — cho phép rồi thử lại.
            </p>
          )}

          {/* CTAs */}
          <div className="mt-6 flex items-center justify-between gap-3">
            <button
              type="button"
              onClick={() => onOpenChange(false)}
              className="font-sans text-[12px] font-medium text-[#3a2618]/75 underline-offset-2 transition-colors hover:text-[#1d130a] hover:underline focus-visible:outline-none focus-visible:underline"
            >
              Để sau
            </button>

            <button
              type="button"
              onClick={handleSignIn}
              disabled={status === 'loading'}
              className={cn(
                'group/cta inline-flex items-center gap-2 rounded-sm px-4 py-2.5 font-sans text-[12.5px] font-bold uppercase tracking-[0.08em] transition-all duration-fast ease-out-quart',
                'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#6b1a1a]/40',
                'disabled:cursor-wait',
              )}
              style={{
                backgroundColor: '#1d130a',
                color: '#f5dfa0',
                boxShadow:
                  'inset 0 0 0 1px rgba(217, 184, 108, 0.85), inset 0 0 0 2px rgba(29, 19, 10, 1), inset 0 0 0 3px rgba(217, 184, 108, 0.4), 0 2px 0 0 rgba(29, 19, 10, 0.25)',
              }}
            >
              {status === 'loading' ? (
                <>
                  <Loader2
                    className="h-3 w-3 animate-spin"
                    strokeWidth={3}
                    aria-hidden
                  />
                  Đang mở Puter
                </>
              ) : (
                <>
                  Tiếp tục với Puter
                  <span
                    aria-hidden
                    className="font-mono text-[14px] transition-transform duration-fast group-hover/cta:translate-x-0.5"
                  >
                    →
                  </span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* perforated ticket-stub footer */}
        <div className="relative">
          {/* perforation line — alternating notch dots */}
          <div
            aria-hidden
            className="h-3"
            style={{
              backgroundImage:
                'radial-gradient(circle at 6px 6px, transparent 3px, transparent 3px), repeating-linear-gradient(90deg, transparent 0 6px, rgba(58, 38, 24, 0.45) 6px 10px)',
              backgroundSize: '12px 12px',
              backgroundPosition: 'center',
            }}
          />
          <div className="flex items-center justify-between bg-[#ede1c2] px-6 py-2.5">
            <span className="font-mono text-[9.5px] font-bold uppercase tracking-[0.24em] text-[#3a2618]/85">
              Puter.com · bên thứ 3
            </span>
            <span className="font-mono text-[9.5px] uppercase tracking-[0.24em] text-[#3a2618]/65">
              Free tier · vô thời hạn
            </span>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
