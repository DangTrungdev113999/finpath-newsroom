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
      <div className="mx-auto flex h-12 max-w-7xl items-center justify-between gap-4 px-6">
        <Link
          to="/"
          className="font-sans text-[17px] tracking-[-0.015em] text-fg-0 no-underline transition-opacity duration-fast hover:opacity-70"
        >
          <span className="font-semibold">Team</span>
          <span className="ml-1.5 font-normal text-fg-3">Chứng</span>
        </Link>

        <div className="flex items-center gap-2">
          <nav className="flex items-center gap-0.5 rounded-pill bg-bg-2/80 p-0.5 font-sans text-xs font-medium">
            <NavTab to="/" active={isCards}>
              Cards
            </NavTab>
            <NavTab to="/feed" active={isFeed}>
              Feed
            </NavTab>
          </nav>

          <div className="ml-1 w-44">
            <ThemeSwitcher />
          </div>
        </div>
      </div>
    </header>
  );
}

function NavTab({ to, active, children }: { to: string; active: boolean; children: ReactNode }) {
  return (
    <Link
      to={to}
      aria-current={active ? 'page' : undefined}
      className={`rounded-pill px-3.5 py-1 no-underline transition-all duration-med ease-out-quart ${
        active
          ? 'bg-bg-1 text-fg-0 shadow-sm'
          : 'text-fg-2 hover:text-fg-0'
      }`}
    >
      {children}
    </Link>
  );
}
