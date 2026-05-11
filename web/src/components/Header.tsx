import type { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ThemeSwitcher } from '../themes/ThemeSwitcher';

export function Header() {
  const { pathname } = useLocation();
  const isCards = pathname === '/' || pathname.startsWith('/article/');
  const isFeed = pathname === '/feed';

  return (
    <header
      className="sticky top-0 z-30 border-b border-fg-4/40 bg-bg-1/80"
      style={{ backdropFilter: 'saturate(180%) blur(20px)', WebkitBackdropFilter: 'saturate(180%) blur(20px)' }}
    >
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between gap-3 px-3 sm:gap-6 sm:px-6">
        <div className="flex min-w-0 items-center gap-4 sm:gap-7">
          <Logo />

          <span aria-hidden className="hidden h-5 w-px bg-fg-4/60 sm:block" />

          <nav
            aria-label="Điều hướng chính"
            className="flex shrink-0 items-center gap-3 sm:gap-5"
          >
            <NavLink to="/" active={isCards}>
              Bài viết
            </NavLink>
            <span aria-hidden className="h-3 w-px bg-fg-4/60" />
            <NavLink to="/feed" active={isFeed}>
              Dòng tin
            </NavLink>
          </nav>
        </div>

        <div className="w-[6.5rem] shrink-0 sm:w-44">
          <ThemeSwitcher />
        </div>
      </div>
    </header>
  );
}

function Logo() {
  return (
    <Link
      to="/"
      aria-label="TeamChứng — về trang chủ"
      className="group relative flex shrink-0 items-center gap-2 no-underline"
    >
      {/* Monogram mark — Ticker T with live chart pulse */}
      <span
        aria-hidden
        className="relative inline-flex h-9 w-9 items-center justify-center overflow-hidden rounded-[11px] bg-fg-0 text-bg-1 ring-1 ring-fg-0/20 shadow-[0_2px_12px_-3px_hsl(var(--brand)/0.45),inset_0_1px_0_hsl(0_0%_100%/0.08)] transition-all duration-med ease-out-quart group-hover:rotate-[-4deg] group-hover:scale-[1.04] sm:h-10 sm:w-10"
      >
        {/* Diagonal brand glow corner */}
        <span
          className="pointer-events-none absolute -right-3 -top-3 h-6 w-6 rounded-full bg-brand/40 blur-md"
          aria-hidden
        />
        {/* Newsprint micro-grid */}
        <svg
          viewBox="0 0 40 40"
          className="absolute inset-0 h-full w-full opacity-[0.06]"
          aria-hidden
        >
          <defs>
            <pattern id="logo-grid" width="4" height="4" patternUnits="userSpaceOnUse">
              <circle cx="0.5" cy="0.5" r="0.5" fill="currentColor" />
            </pattern>
          </defs>
          <rect width="40" height="40" fill="url(#logo-grid)" />
        </svg>
        <svg
          viewBox="0 0 40 40"
          className="relative h-full w-full"
          aria-hidden
        >
          {/* The T — bold geometric letterform */}
          <rect x="7" y="9" width="22" height="3.2" rx="0.5" fill="currentColor" />
          <rect x="16.4" y="9" width="3.2" height="20" rx="0.5" fill="currentColor" />

          {/* Serif feet — gives editorial slab character */}
          <rect x="14.5" y="27.5" width="7" height="1.6" rx="0.4" fill="currentColor" />

          {/* Rising candle chart — finance signal */}
          <g>
            <rect x="23.5" y="22" width="2.4" height="6.5" rx="0.4" fill="hsl(var(--brand))" opacity="0.45" />
            <rect x="27.4" y="18" width="2.4" height="10.5" rx="0.4" fill="hsl(var(--brand))" opacity="0.7" />
            <rect x="31.3" y="13" width="2.4" height="15.5" rx="0.4" fill="hsl(var(--brand))" />
            {/* Wick on tallest */}
            <line x1="32.5" y1="9.5" x2="32.5" y2="13" stroke="hsl(var(--brand))" strokeWidth="0.9" strokeLinecap="round" />
          </g>

          {/* Ticker rail */}
          <rect x="5" y="32" width="30" height="1.2" rx="0.6" fill="currentColor" opacity="0.18" />
          <rect x="5" y="32" width="11" height="1.2" rx="0.6" fill="hsl(var(--brand))">
            <animate attributeName="x" values="-12;40" dur="3.6s" repeatCount="indefinite" />
          </rect>

          {/* Live pulse dot */}
          <circle cx="33" cy="9" r="2.2" fill="hsl(var(--brand))" opacity="0.55">
            <animate attributeName="r" values="2.2;5.5;2.2" dur="2.2s" repeatCount="indefinite" />
            <animate attributeName="opacity" values="0.55;0;0.55" dur="2.2s" repeatCount="indefinite" />
          </circle>
          <circle cx="33" cy="9" r="2" fill="hsl(var(--brand))" />
        </svg>
      </span>

      {/* Wordmark */}
      <span className="flex items-baseline leading-none tracking-[-0.025em] text-fg-0">
        <span className="font-display text-[18px] font-semibold sm:text-[20px]">
          Team
        </span>
        <span className="font-display text-[18px] font-light italic text-brand sm:text-[20px]">
          Chứng
        </span>
      </span>
    </Link>
  );
}

function NavLink({ to, active, children }: { to: string; active: boolean; children: ReactNode }) {
  return (
    <Link
      to={to}
      aria-current={active ? 'page' : undefined}
      className={`group/nav relative font-sans text-[13px] font-medium tracking-[0.005em] no-underline transition-colors duration-fast ease-out-quart sm:text-[14px] ${
        active ? 'text-fg-0' : 'text-fg-2 hover:text-fg-0'
      }`}
    >
      {children}
      <span
        aria-hidden
        className={`pointer-events-none absolute -bottom-1 left-0 h-[2px] rounded-full bg-brand transition-all duration-med ease-out-quart ${
          active ? 'w-full opacity-100' : 'w-0 opacity-0 group-hover/nav:w-full group-hover/nav:opacity-60'
        }`}
      />
    </Link>
  );
}
