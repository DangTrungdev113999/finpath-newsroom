import { cn } from '../shared/lib/cn';

export type ArticleModel = 'claude' | 'gemini';

interface ModelToggleProps {
  selected: ArticleModel;
  onChange: (model: ArticleModel) => void;
  geminiAvailable: boolean;
}

/**
 * Segmented 2-button toggle to switch the LeftColumn article view between
 * Claude (default) and Gemini (Step 4.3 parallel writer). Gemini button is
 * visually muted + click-blocked when no successful Gemini side exists
 * (gemini_status != 'success' in DB / frontmatter block absent).
 */
export function ModelToggle({
  selected,
  onChange,
  geminiAvailable,
}: ModelToggleProps) {
  const handleGeminiClick = () => {
    if (!geminiAvailable) return;
    if (selected !== 'gemini') onChange('gemini');
  };
  const handleClaudeClick = () => {
    if (selected !== 'claude') onChange('claude');
  };

  return (
    <div
      role="radiogroup"
      aria-label="Chọn model viết bài"
      className="inline-flex items-center rounded-pill border border-fg-3/55 bg-bg-2 p-0.5 font-sans text-[11.5px] font-medium"
    >
      <ToggleButton
        active={selected === 'claude'}
        onClick={handleClaudeClick}
        disabled={false}
        ariaLabel="Bài Claude"
      >
        Claude
      </ToggleButton>
      <ToggleButton
        active={selected === 'gemini'}
        onClick={handleGeminiClick}
        disabled={!geminiAvailable}
        ariaLabel={
          geminiAvailable ? 'Bài Gemini' : 'Bài Gemini không khả dụng'
        }
        title={
          geminiAvailable
            ? undefined
            : 'Bài Gemini không khả dụng (Step 4.3 skipped — kiểm tra gemini_status trong DB)'
        }
      >
        Gemini
      </ToggleButton>
    </div>
  );
}

function ToggleButton({
  active,
  onClick,
  disabled,
  ariaLabel,
  title,
  children,
}: {
  active: boolean;
  onClick: () => void;
  disabled: boolean;
  ariaLabel: string;
  title?: string;
  children: React.ReactNode;
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
        'h-6 rounded-full px-3 transition-all duration-fast ease-out-quart',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35',
        active
          ? 'bg-brand text-brand-fg shadow-sm shadow-brand/15'
          : 'text-fg-1 hover:text-fg-0',
        disabled && 'cursor-not-allowed opacity-50 hover:text-fg-1',
      )}
    >
      {children}
    </button>
  );
}
