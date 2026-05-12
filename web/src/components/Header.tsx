import type { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ThemeSwitcher } from '../themes/ThemeSwitcher';

export function Header() {
  const { pathname } = useLocation();
  const isCards = pathname === '/' || pathname.startsWith('/article/');
  const isFeed = pathname === '/feed';
  const isKb = pathname === '/tai-lieu' || pathname.startsWith('/tai-lieu/');

  return (
    <header
      className="sticky top-0 z-30 border-b border-fg-4/30 bg-bg-1/70"
      style={{ backdropFilter: 'saturate(180%) blur(20px)', WebkitBackdropFilter: 'saturate(180%) blur(20px)' }}
    >
      {/* Subtle ambient gradient — hairline glow under brand pulse, only visible on active page */}
      <span
        aria-hidden
        className="pointer-events-none absolute inset-x-0 -bottom-px h-px"
        style={{
          background:
            'linear-gradient(90deg, transparent 0%, hsl(var(--brand) / 0.35) 30%, hsl(var(--brand) / 0.5) 50%, hsl(var(--brand) / 0.35) 70%, transparent 100%)',
          opacity: 0.55,
        }}
      />

      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between gap-3 px-3 sm:gap-8 sm:px-6">
        <div className="flex min-w-0 items-center gap-5 sm:gap-8">
          <Logo />

          <nav
            aria-label="Điều hướng chính"
            className="flex shrink-0 items-center gap-1 rounded-full border border-fg-4/35 bg-bg-2/50 p-1 shadow-[inset_0_1px_0_hsl(var(--fg-0)/0.04)] sm:gap-1.5"
          >
            <NavLink to="/" active={isCards}>
              Bài viết
            </NavLink>
            <NavLink to="/feed" active={isFeed}>
              Dòng tin
            </NavLink>
            <NavLink to="/tai-lieu" active={isKb}>
              Tài liệu
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
      className="group relative flex shrink-0 items-center gap-2.5 no-underline"
    >
      {/* Mark — "Sắc": the Vietnamese rising-tone diacritic doubles as a
          chart uptick. One symbol, two readings — cultural + financial.
          Three elements only: stamp, sắc stroke, apex node. */}
      <span
        aria-hidden
        className="relative inline-flex h-9 w-9 items-center justify-center rounded-[9px] bg-fg-0 ring-1 ring-fg-0/[0.12] transition-all duration-med ease-out-quart group-hover:-translate-y-px sm:h-10 sm:w-10"
        style={{
          boxShadow:
            'inset 0 1px 0 hsl(0 0% 100% / 0.06), 0 1px 0 hsl(var(--fg-0) / 0.06), 0 6px 20px -14px hsl(var(--brand) / 0.55), 0 2px 4px -2px rgb(0 0 0 / 0.18)',
        }}
      >
        <svg viewBox="0 0 40 40" className="h-full w-full" aria-hidden>
          {/* Faint axis baseline — anchors the tick in chart space without
              committing to literal bars */}
          <line
            x1="9.5"
            y1="29.4"
            x2="30.5"
            y2="29.4"
            stroke="hsl(var(--bg-1))"
            strokeWidth="0.9"
            strokeLinecap="round"
            opacity="0.22"
          />

          {/* The dấu sắc — single confident upstroke, brand color.
              Angled at ~42° (true to Vietnamese diacritic geometry). */}
          <path
            d="M 12.8 26.4 L 27.2 12.8"
            stroke="hsl(var(--brand))"
            strokeWidth="4.6"
            strokeLinecap="round"
            className="transition-transform duration-med ease-out-quart group-hover:[transform:translate(0.6px,-0.6px)]"
          />

          {/* Apex node — reads as candle-wick endpoint / signal source */}
          <circle
            cx="27.2"
            cy="12.8"
            r="2.2"
            fill="hsl(var(--brand))"
            className="transition-transform duration-med ease-out-quart group-hover:[transform:translate(0.6px,-0.6px)]"
          />
        </svg>
      </span>

      {/* Wordmark — single weight serif, no italic, no brand-color split.
          Restraint: the mark carries 100% of the brand signature. */}
      <span className="font-display text-[19px] font-semibold leading-none tracking-[-0.028em] text-fg-0 sm:text-[21px]">
        Team<span className="text-fg-1">Chứng</span>
      </span>
    </Link>
  );
}

function NavLink({ to, active, children }: { to: string; active: boolean; children: ReactNode }) {
  return (
    <Link
      to={to}
      aria-current={active ? 'page' : undefined}
      className={`group/nav relative inline-flex items-center rounded-full px-3.5 py-1.5 font-sans text-[13px] font-semibold tracking-[0.005em] no-underline transition-all duration-med ease-out-quart sm:px-4 sm:text-[13.5px] ${
        active
          ? 'text-brand'
          : 'text-fg-2 hover:text-fg-0'
      }`}
      style={
        active
          ? {
              backgroundImage:
                'linear-gradient(180deg, hsl(var(--brand) / 0.22) 0%, hsl(var(--brand) / 0.10) 45%, hsl(var(--brand) / 0.04) 100%)',
              boxShadow:
                'inset 0 0 0 1px hsl(var(--brand) / 0.35), inset 0 1px 0 hsl(var(--brand) / 0.45), 0 6px 22px -10px hsl(var(--brand) / 0.55), 0 1px 0 hsl(var(--bg-1) / 0.4)',
            }
          : undefined
      }
    >
      {/* Hover wash — only on inactive pills */}
      {!active && (
        <span
          aria-hidden
          className="pointer-events-none absolute inset-0 rounded-full bg-fg-0/0 transition-colors duration-fast group-hover/nav:bg-fg-0/[0.04]"
        />
      )}

      {/* Active accent — luminous hairline crowning the pill */}
      {active && (
        <span
          aria-hidden
          className="pointer-events-none absolute inset-x-3 top-0 h-[1.5px] rounded-full"
          style={{
            background:
              'linear-gradient(90deg, transparent 0%, hsl(var(--brand)) 50%, transparent 100%)',
            filter: 'blur(0.3px)',
          }}
        />
      )}

      <span className="relative whitespace-nowrap">{children}</span>
    </Link>
  );
}
