import { useId, type CSSProperties, type ReactNode } from 'react';
import { cn } from '../shared/lib/cn';

export type ArticleModel = 'claude' | 'gemini' | 'grok';

/**
 * Label visibility mode (responsive — mobile is always icon-only):
 *   'never'  → icon-only at every viewport.
 *   'hover'  → icon-only by default at ≥sm; labels expand on group
 *              hover/keyboard-focus. Use on tight surfaces like the article
 *              header where the toggle sits next to other controls.
 *   'always' → labels persistently visible at ≥sm. Use on roomy surfaces
 *              like the IndexPage filter row.
 */
export type ModelToggleLabelMode = 'never' | 'hover' | 'always';

interface ModelToggleProps {
  selected: ArticleModel;
  onChange: (model: ArticleModel) => void;
  geminiAvailable: boolean;
  grokAvailable: boolean;
  /** V5.1.9 — when false (default) the Claude button is hidden entirely so
   *  the segmented control collapses to 2-way (Gemini + Grok). Set true on
   *  articles that have a claude_body (legacy V5.1.8 + earlier). */
  claudeAvailable?: boolean;
  labelMode?: ModelToggleLabelMode;
}

/**
 * Segmented 3-button toggle to switch the article view between
 * Claude (master), Gemini (Step 4.3), and Grok (Step 4.4). Each button carries
 * a recognizable brand mark — 8-spoke burst for Anthropic / 4-point pinched
 * sparkle for Google Gemini / stylized X for xAI Grok — so the toggle reads
 * at a glance even before the text label is parsed. Gemini and Grok buttons
 * are independently muted + click-blocked when their respective parallel
 * side did not succeed for this article.
 */
export function ModelToggle({
  selected,
  onChange,
  geminiAvailable,
  grokAvailable,
  claudeAvailable = false,
  labelMode = 'never',
}: ModelToggleProps) {
  const handleClaudeClick = () => {
    if (!claudeAvailable) return;
    if (selected !== 'claude') onChange('claude');
  };
  const handleGeminiClick = () => {
    if (!geminiAvailable) return;
    if (selected !== 'gemini') onChange('gemini');
  };
  const handleGrokClick = () => {
    if (!grokAvailable) return;
    if (selected !== 'grok') onChange('grok');
  };

  const claudeActive = selected === 'claude';
  const geminiActive = selected === 'gemini';
  const grokActive = selected === 'grok';

  return (
    <div
      role="radiogroup"
      aria-label="Chọn model viết bài"
      className="group/mtg inline-flex h-7 items-center gap-0.5 rounded-pill border border-fg-3/55 bg-bg-2 px-0.5"
    >
      {claudeAvailable && (
        <ToggleButton
          model="claude"
          active={claudeActive}
          onClick={handleClaudeClick}
          disabled={false}
          ariaLabel="Bài Claude"
          title="Bài Claude"
          labelMode={labelMode}
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
      )}
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
        labelMode={labelMode}
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
      <ToggleButton
        model="grok"
        active={grokActive}
        onClick={handleGrokClick}
        disabled={!grokAvailable}
        ariaLabel={grokAvailable ? 'Bài Grok' : 'Bài Grok không khả dụng'}
        title={
          grokAvailable
            ? 'Bài Grok'
            : 'Bài Grok không khả dụng (Step 4.4 skipped — kiểm tra grok_status trong DB)'
        }
        labelMode={labelMode}
        label="Grok"
        logo={
          <GrokMark
            className={cn(
              'h-3.5 w-3.5 shrink-0 transition-transform duration-fast ease-out-quart',
              'group-hover/mt:scale-110',
              grokActive ? 'text-white' : 'text-fg-0',
            )}
          />
        }
      />
    </div>
  );
}

// Brand-locked active styles — moved to inline style so brand fills are
// guaranteed to render regardless of Tailwind JIT scan or content path
// configuration. Pair with a small Tailwind class for shared ring/text/shadow
// utilities. Each brand also gets a high-contrast white inner ring so the
// active button reads as "ticket-punched" against any theme.
const ACTIVE_INLINE: Record<ArticleModel, CSSProperties> = {
  claude: {
    background: '#D97757',
    boxShadow:
      'inset 0 0 0 1px rgba(255, 255, 255, 0.28), 0 2px 10px -2px rgba(217, 119, 87, 0.7)',
  },
  gemini: {
    background:
      'linear-gradient(135deg, #4285F4 0%, #9B72CB 50%, #D96570 100%)',
    boxShadow:
      'inset 0 0 0 1px rgba(255, 255, 255, 0.3), 0 2px 12px -2px rgba(155, 114, 203, 0.75)',
  },
  grok: {
    background: '#0B0B0B',
    boxShadow:
      'inset 0 0 0 1px rgba(255, 255, 255, 0.22), 0 2px 10px -2px rgba(0, 0, 0, 0.75)',
  },
};

function ToggleButton({
  model,
  active,
  onClick,
  disabled,
  ariaLabel,
  title,
  logo,
  labelMode,
  label,
}: {
  model: ArticleModel;
  active: boolean;
  onClick: () => void;
  disabled: boolean;
  ariaLabel: string;
  title: string;
  logo: ReactNode;
  labelMode: ModelToggleLabelMode;
  label: string;
}) {
  const showLabelOnDesktop = labelMode !== 'never';
  const persistentLabel = labelMode === 'always';

  return (
    <button
      type="button"
      role="radio"
      aria-checked={active}
      aria-label={ariaLabel}
      aria-disabled={disabled || undefined}
      title={title}
      onClick={onClick}
      style={active ? ACTIVE_INLINE[model] : undefined}
      className={cn(
        'group/mt inline-flex h-6 items-center justify-center rounded-full',
        'transition-[width,gap,padding,background,box-shadow,color] duration-med ease-out-quart',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-fg-0/40',
        showLabelOnDesktop
          ? persistentLabel
            ? 'w-6 sm:w-auto sm:gap-1.5 sm:px-2.5 sm:font-sans sm:text-[12px] sm:font-medium'
            : cn(
                'w-6',
                'sm:group-hover/mtg:w-auto sm:group-hover/mtg:gap-1.5 sm:group-hover/mtg:px-2.5',
                'sm:group-focus-within/mtg:w-auto sm:group-focus-within/mtg:gap-1.5 sm:group-focus-within/mtg:px-2.5',
                'sm:font-sans sm:text-[12px] sm:font-medium',
              )
          : 'w-6',
        active
          ? 'text-white font-semibold'
          : 'text-fg-1 hover:bg-bg-3/60',
        disabled && 'cursor-not-allowed opacity-40 hover:bg-transparent',
      )}
    >
      {logo}
      {showLabelOnDesktop && (
        <span
          className={cn(
            persistentLabel
              ? 'hidden sm:inline'
              : 'hidden sm:group-hover/mtg:inline sm:group-focus-within/mtg:inline',
          )}
        >
          {label}
        </span>
      )}
    </button>
  );
}

/**
 * Anthropic-style 8-spoke burst: four overlapping thin ellipses rotated
 * 0° / 45° / 90° / 135°. Uses currentColor so the active state inherits the
 * pill's text color (brand-fg) and inactive can be tinted via Tailwind text-*.
 */
export function ClaudeMark({ className }: { className?: string }) {
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
export function GeminiMark({
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

/**
 * xAI Grok mark — slashed circle (Ø-glyph): a circle outline cut by a
 * diagonal stroke that extends past the bottom-left as a comet-like tail.
 * Stroke uses currentColor so active state renders white inside the matte
 * black pill while inactive inherits text-fg-0.
 */
export function GrokMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden className={className}>
      <g
        stroke="currentColor"
        strokeWidth="2"
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <circle cx="12" cy="12" r="8" />
        <path d="M19 5 L3 21" />
      </g>
    </svg>
  );
}
