import { useId, type ReactNode } from 'react';
import { cn } from '../shared/lib/cn';

export type ArticleModel = 'claude' | 'gemini';

interface ModelToggleProps {
  selected: ArticleModel;
  onChange: (model: ArticleModel) => void;
  geminiAvailable: boolean;
  /** When true, render text label next to each logo (use on roomy surfaces
   *  like IndexPage filter row). Default false — icon-only, compact for the
   *  article header next to TTSButton. */
  withLabel?: boolean;
}

/**
 * Segmented 2-button toggle to switch the LeftColumn article view between
 * Claude (default) and Gemini (Step 4.3 parallel writer). Each button carries
 * a recognizable brand mark — 8-spoke burst for Anthropic / 4-point pinched
 * sparkle for Google Gemini — so the toggle reads at a glance even before the
 * text label is parsed. Gemini button is muted + click-blocked when no
 * successful Gemini side exists (gemini_status != 'success' in DB).
 */
export function ModelToggle({
  selected,
  onChange,
  geminiAvailable,
  withLabel = false,
}: ModelToggleProps) {
  const handleGeminiClick = () => {
    if (!geminiAvailable) return;
    if (selected !== 'gemini') onChange('gemini');
  };
  const handleClaudeClick = () => {
    if (selected !== 'claude') onChange('claude');
  };

  const claudeActive = selected === 'claude';
  const geminiActive = selected === 'gemini';

  return (
    <div
      role="radiogroup"
      aria-label="Chọn model viết bài"
      className="inline-flex h-7 items-center gap-0.5 rounded-pill border border-fg-3/55 bg-bg-2 px-0.5"
    >
      <ToggleButton
        model="claude"
        active={claudeActive}
        onClick={handleClaudeClick}
        disabled={false}
        ariaLabel="Bài Claude"
        title="Bài Claude"
        withLabel={withLabel}
        label="Claude"
        logo={
          <ClaudeMark
            className={cn(
              'h-3.5 w-3.5 shrink-0 transition-transform duration-fast ease-out-quart',
              'group-hover/mt:scale-110',
              claudeActive ? 'text-white' : 'text-[#D97757]',
            )}
          />
        }
      />
      <ToggleButton
        model="gemini"
        active={geminiActive}
        onClick={handleGeminiClick}
        disabled={!geminiAvailable}
        ariaLabel={
          geminiAvailable ? 'Bài Gemini' : 'Bài Gemini không khả dụng'
        }
        title={
          geminiAvailable
            ? 'Bài Gemini'
            : 'Bài Gemini không khả dụng (Step 4.3 skipped — kiểm tra gemini_status trong DB)'
        }
        withLabel={withLabel}
        label="Gemini"
        logo={
          <GeminiMark
            className={cn(
              'h-3.5 w-3.5 shrink-0 transition-transform duration-fast ease-out-quart',
              'group-hover/mt:scale-110',
              geminiActive && 'text-white',
            )}
            monochrome={geminiActive}
          />
        }
      />
    </div>
  );
}

// Brand-locked active styles — do NOT inherit from theme tokens.
// Claude: Anthropic clay #D97757. Gemini: Google sparkle gradient blue→violet→red.
const ACTIVE_STYLES: Record<ArticleModel, string> = {
  claude:
    'bg-[#D97757] shadow-[0_1px_8px_-2px_rgba(217,119,87,0.55)] focus-visible:ring-[#D97757]/40',
  gemini:
    'bg-gradient-to-br from-[#4285F4] via-[#9B72CB] to-[#D96570] shadow-[0_1px_8px_-2px_rgba(155,114,203,0.6)] focus-visible:ring-[#9B72CB]/45',
};

function ToggleButton({
  model,
  active,
  onClick,
  disabled,
  ariaLabel,
  title,
  logo,
  withLabel,
  label,
}: {
  model: ArticleModel;
  active: boolean;
  onClick: () => void;
  disabled: boolean;
  ariaLabel: string;
  title: string;
  logo: ReactNode;
  withLabel: boolean;
  label: string;
}) {
  return (
    <button
      type="button"
      role="radio"
      aria-checked={active}
      aria-label={ariaLabel}
      aria-disabled={disabled || undefined}
      title={title}
      onClick={onClick}
      className={cn(
        'group/mt inline-flex h-6 items-center justify-center rounded-full',
        'transition-[background,box-shadow,color] duration-med ease-out-quart',
        'focus-visible:outline-none focus-visible:ring-2',
        withLabel ? 'gap-1.5 px-2.5 font-sans text-[12px] font-medium' : 'w-6',
        active
          ? cn(ACTIVE_STYLES[model], withLabel && 'text-white')
          : cn(
              'hover:bg-bg-3/60 focus-visible:ring-fg-3/40',
              withLabel ? 'text-fg-1' : 'text-fg-1',
            ),
        disabled && 'cursor-not-allowed opacity-40 hover:bg-transparent',
      )}
    >
      {logo}
      {withLabel && <span>{label}</span>}
    </button>
  );
}

/**
 * Anthropic-style 8-spoke burst: four overlapping thin ellipses rotated
 * 0° / 45° / 90° / 135°. Uses currentColor so the active state inherits the
 * pill's text color (brand-fg) and inactive can be tinted via Tailwind text-*.
 */
function ClaudeMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden className={className}>
      <g fill="currentColor">
        <ellipse cx="12" cy="12" rx="1.4" ry="11" />
        <ellipse cx="12" cy="12" rx="11" ry="1.4" />
        <ellipse cx="12" cy="12" rx="1.4" ry="11" transform="rotate(45 12 12)" />
        <ellipse cx="12" cy="12" rx="1.4" ry="11" transform="rotate(-45 12 12)" />
      </g>
    </svg>
  );
}

/**
 * Google Gemini-style 4-point pinched sparkle. Inactive uses the trademark
 * blue → violet → red gradient; active switches to monochrome currentColor so
 * the gradient does not clash with the warm brand-orange pill background.
 */
function GeminiMark({
  className,
  monochrome = false,
}: {
  className?: string;
  monochrome?: boolean;
}) {
  const gradId = useId();
  return (
    <svg viewBox="0 0 24 24" aria-hidden className={className}>
      {!monochrome && (
        <defs>
          <linearGradient id={gradId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#4285F4" />
            <stop offset="50%" stopColor="#9B72CB" />
            <stop offset="100%" stopColor="#D96570" />
          </linearGradient>
        </defs>
      )}
      <path
        d="M12 0 C12 6 14 10 24 12 C14 14 12 18 12 24 C12 18 10 14 0 12 C10 10 12 6 12 0 Z"
        fill={monochrome ? 'currentColor' : `url(#${gradId})`}
      />
    </svg>
  );
}
