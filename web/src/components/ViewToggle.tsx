/**
 * Two-pane / one-pane reading mode toggle. "Tập trung" hides the metadata
 * right-column for distraction-free reading; "Đầy đủ" restores both panes.
 *
 * Lives in its own file so ArticlePage and FeedPage can both mount it next
 * to their back-link without duplicating JSX.
 */
export function ViewToggle({
  showRight,
  onChange,
}: {
  showRight: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <div
      role="group"
      aria-label="Chế độ xem"
      className="inline-flex items-center gap-0.5 rounded-pill border border-brand/20 bg-bg-2/60 p-0.5 font-sans text-[12px] font-medium shadow-sm shadow-brand/5"
    >
      <ToggleButton
        active={!showRight}
        onClick={() => onChange(false)}
        label="Tập trung"
        title="Ẩn cột metadata để tập trung đọc"
      >
        <OnePaneIcon />
      </ToggleButton>
      <ToggleButton
        active={showRight}
        onClick={() => onChange(true)}
        label="Đầy đủ"
        title="Đọc bài + cột metadata bên cạnh"
      >
        <TwoPaneIcon />
      </ToggleButton>
    </div>
  );
}

function ToggleButton({
  active,
  onClick,
  label,
  title,
  children,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      title={title}
      className={`inline-flex items-center gap-1.5 rounded-pill px-3 py-1 transition-all duration-med ease-out-quart ${
        active
          ? 'bg-brand text-brand-fg shadow-sm shadow-brand/25 ring-1 ring-brand/40'
          : 'text-fg-2 hover:text-brand hover:bg-brand/5'
      }`}
    >
      {children}
      <span>{label}</span>
    </button>
  );
}

function TwoPaneIcon() {
  return (
    <svg
      viewBox="0 0 16 12"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.4"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-3 w-[16px] shrink-0"
      aria-hidden
    >
      <rect x="1" y="1" width="14" height="10" rx="1.4" />
      <line x1="8" y1="1.5" x2="8" y2="10.5" />
    </svg>
  );
}

function OnePaneIcon() {
  return (
    <svg
      viewBox="0 0 16 12"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.4"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-3 w-[16px] shrink-0"
      aria-hidden
    >
      <rect x="3" y="1" width="10" height="10" rx="1.4" />
    </svg>
  );
}
