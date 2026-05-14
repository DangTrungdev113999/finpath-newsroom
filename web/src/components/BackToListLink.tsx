import { Link } from 'react-router-dom';

/**
 * Editorial back-to-list pill chip used by ArticlePage and FeedPage. Glass
 * blur surface, hairline border that warms to brand on hover, chevron
 * slides left and a trailing ↩ glyph tints brand for tactile feedback.
 */
export function BackToListLink({
  to = '/',
  label = 'Quay lại danh sách',
  ariaLabel,
}: {
  to?: string;
  label?: string;
  ariaLabel?: string;
}) {
  return (
    <Link
      to={to}
      aria-label={ariaLabel ?? `${label} bài viết`}
      className="group/back inline-flex h-8 items-center gap-2 rounded-pill border border-fg-4/40 bg-bg-1/70 px-3.5 font-sans text-[12px] font-medium text-fg-2 no-underline backdrop-blur transition-all duration-med ease-out-quart hover:-translate-y-px hover:border-brand/45 hover:bg-bg-2 hover:text-brand hover:shadow-[0_4px_14px_-6px_hsl(var(--brand)/0.45)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35"
    >
      <svg
        viewBox="0 0 16 16"
        aria-hidden
        className="h-3 w-3 shrink-0 transition-transform duration-med ease-out-quart group-hover/back:-translate-x-1"
      >
        <path
          d="M9.75 3 L4.5 8 L9.75 13"
          stroke="currentColor"
          strokeWidth="1.7"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
      </svg>
      <span className="tracking-[0.01em]">{label}</span>
      <span
        aria-hidden
        className="font-mono text-[10px] tracking-[0.18em] text-fg-3 transition-colors duration-med ease-out-quart group-hover/back:text-brand/70"
      >
        ↩
      </span>
    </Link>
  );
}
