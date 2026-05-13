import { Fragment, type ComponentType, type ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  BookOpen,
  ChevronDown,
  History,
  Newspaper,
  Rss,
} from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from '../shared/ui/dropdown-menu';
import { cn } from '../shared/lib/cn';
import { ThemeSwitcher } from '../themes/ThemeSwitcher';

type IconType = ComponentType<{ className?: string; strokeWidth?: number | string }>;

type NavItem = {
  to: string;
  label: string;
  icon: IconType;
  match: (pathname: string) => boolean;
};

const NAV_ITEMS: ReadonlyArray<NavItem> = [
  {
    to: '/',
    label: 'Bài viết',
    icon: Newspaper,
    match: (p) => p === '/' || p.startsWith('/article/'),
  },
  {
    to: '/feed',
    label: 'Dòng tin',
    icon: Rss,
    match: (p) => p === '/feed',
  },
  {
    to: '/tai-lieu',
    label: 'Tài liệu',
    icon: BookOpen,
    match: (p) => p === '/tai-lieu' || p.startsWith('/tai-lieu/'),
  },
  {
    to: '/pipeline-runs',
    label: 'Lịch sử pipeline',
    icon: History,
    match: (p) => p === '/pipeline-runs' || p.startsWith('/pipeline-runs'),
  },
];

export function Header() {
  const { pathname } = useLocation();
  const activeItem = NAV_ITEMS.find((item) => item.match(pathname)) ?? NAV_ITEMS[0];

  return (
    <header
      className="sticky top-0 z-30 border-b border-fg-4/40 bg-bg-1/80"
      style={{
        backdropFilter: 'saturate(180%) blur(20px)',
        WebkitBackdropFilter: 'saturate(180%) blur(20px)',
      }}
    >
      <div className="mx-auto max-w-7xl">
        <div className="flex h-14 items-center justify-between gap-2 px-3 sm:gap-4 sm:px-6">
          {/* Brand + desktop inline nav */}
          <div className="flex min-w-0 items-center gap-3 lg:gap-7">
            <Logo />

            <span aria-hidden className="hidden h-5 w-px bg-fg-4/60 lg:block" />

            <nav
              aria-label="Điều hướng chính"
              className="hidden shrink-0 items-center gap-3 lg:flex lg:gap-5"
            >
              {NAV_ITEMS.map((item, idx) => (
                <Fragment key={item.to}>
                  {idx > 0 && <span aria-hidden className="h-3 w-px bg-fg-4/60" />}
                  <NavLink to={item.to} active={item.match(pathname)}>
                    {item.label}
                  </NavLink>
                </Fragment>
              ))}
            </nav>
          </div>

          {/* Right cluster — nav dropdown (mobile+tablet) + theme switcher */}
          <div className="flex shrink-0 items-center gap-2">
            <MobileNavMenu activeItem={activeItem} pathname={pathname} />
            <ThemeSwitcher />
          </div>
        </div>
      </div>
    </header>
  );
}

function MobileNavMenu({
  activeItem,
  pathname,
}: {
  activeItem: NavItem;
  pathname: string;
}) {
  const ActiveIcon = activeItem.icon;

  return (
    <div className="lg:hidden">
      <DropdownMenu>
        <DropdownMenuTrigger
          className={cn(
            'group flex items-center rounded-pill',
            'border border-fg-4/40 bg-bg-2/60 text-fg-1',
            'hover:border-fg-4/70 hover:bg-bg-2 hover:text-fg-0',
            'transition-[background-color,border-color,color] duration-med ease-out-quart',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35',
            'data-[state=open]:border-fg-4/70 data-[state=open]:bg-bg-2 data-[state=open]:text-fg-0',
            // < sm: square icon-only button (40×40)
            // ≥ sm: pill with current section label
            'h-10 w-10 justify-center sm:h-9 sm:w-auto sm:gap-2 sm:px-3',
          )}
          aria-label={`Điều hướng — đang xem ${activeItem.label}`}
        >
          <ActiveIcon
            className="h-4 w-4 shrink-0 text-brand sm:h-3.5 sm:w-3.5"
            strokeWidth={2}
          />
          <span className="hidden max-w-[10rem] truncate text-left font-sans text-[13px] font-medium tracking-[0.005em] text-fg-1 sm:inline">
            {activeItem.label}
          </span>
          <ChevronDown
            className="hidden h-3 w-3 shrink-0 text-fg-3 transition-transform duration-med ease-out-quart group-hover:text-fg-1 group-data-[state=open]:rotate-180 sm:block"
            strokeWidth={2}
          />
        </DropdownMenuTrigger>

        <DropdownMenuContent side="bottom" align="end" className="w-56 p-1">
          <DropdownMenuLabel>Điều hướng</DropdownMenuLabel>
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = item.match(pathname);
            return (
              <DropdownMenuItem
                key={item.to}
                asChild
                className={cn(
                  'relative h-auto gap-2.5 py-2 pl-3 pr-2',
                  '[&_svg]:h-4 [&_svg]:w-4',
                  isActive && 'bg-brand/10 text-fg-0',
                )}
              >
                <Link
                  to={item.to}
                  aria-current={isActive ? 'page' : undefined}
                  className="no-underline"
                >
                  {isActive && (
                    <span
                      aria-hidden
                      className="pointer-events-none absolute inset-y-1 left-0 w-[2px] rounded-r-full bg-brand"
                    />
                  )}
                  <Icon
                    className={cn(
                      'shrink-0',
                      isActive ? 'text-brand' : 'text-fg-2',
                    )}
                    strokeWidth={1.75}
                  />
                  <span
                    className={cn(
                      'flex-1 truncate font-sans text-[13px]',
                      isActive ? 'font-semibold text-fg-0' : 'font-medium text-fg-1',
                    )}
                  >
                    {item.label}
                  </span>
                </Link>
              </DropdownMenuItem>
            );
          })}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}

function Logo() {
  return (
    <Link
      to="/"
      aria-label="TeamChứng — về trang chủ"
      className="group relative flex shrink-0 items-center gap-2 no-underline"
    >
      {/* Logo mark — Live Crescendo: breathing market bars + sắc accent */}
      <span
        aria-hidden
        className="relative inline-flex h-9 w-9 items-center justify-center overflow-hidden rounded-tl-[14px] rounded-br-[14px] rounded-tr-[5px] rounded-bl-[5px] bg-fg-0 text-bg-1 ring-1 ring-fg-0/15 shadow-[0_6px_20px_-6px_hsl(var(--brand)/0.55),0_2px_6px_-2px_rgb(0_0_0_/_0.25),inset_0_1px_0_hsl(0_0%_100%/0.1)] transition-all duration-med ease-out-quart group-hover:rotate-[3deg] group-hover:scale-[1.06] sm:h-10 sm:w-10"
      >
        {/* Background gradient mesh */}
        <span
          aria-hidden
          className="pointer-events-none absolute inset-0"
          style={{
            background:
              'radial-gradient(120% 80% at 100% 0%, hsl(var(--brand) / 0.35) 0%, transparent 55%), radial-gradient(80% 100% at 0% 100%, hsl(var(--brand) / 0.12) 0%, transparent 60%)',
          }}
        />
        {/* Newsprint micro-grid */}
        <svg
          viewBox="0 0 40 40"
          className="absolute inset-0 h-full w-full opacity-[0.07]"
          aria-hidden
        >
          <defs>
            <pattern id="logo-grid" width="4" height="4" patternUnits="userSpaceOnUse">
              <circle cx="0.6" cy="0.6" r="0.45" fill="currentColor" />
            </pattern>
          </defs>
          <rect width="40" height="40" fill="url(#logo-grid)" />
        </svg>

        <svg
          viewBox="0 0 40 40"
          className="relative h-full w-full"
          aria-hidden
        >
          {/* Soft glow under apex bar */}
          <ellipse
            cx="27.5"
            cy="34"
            rx="9"
            ry="2"
            fill="hsl(var(--brand))"
            opacity="0.18"
          />

          {/* 5 ascending market bars — anchored at baseline y=34, breathe in wave */}
          <g>
            <rect x="7"  y="25" width="3" height="9"  rx="1" fill="currentColor" opacity="0.32">
              <animate attributeName="y"      values="25;28;25" dur="2.2s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" />
              <animate attributeName="height" values="9;6;9"    dur="2.2s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" />
            </rect>
            <rect x="12" y="21" width="3" height="13" rx="1" fill="currentColor" opacity="0.48">
              <animate attributeName="y"      values="21;24;21" dur="2.2s" begin="-0.18s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" />
              <animate attributeName="height" values="13;10;13" dur="2.2s" begin="-0.18s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" />
            </rect>
            <rect x="17" y="16" width="3" height="18" rx="1" fill="currentColor" opacity="0.65">
              <animate attributeName="y"      values="16;19;16" dur="2.2s" begin="-0.36s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" />
              <animate attributeName="height" values="18;15;18" dur="2.2s" begin="-0.36s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" />
            </rect>
            <rect x="22" y="12" width="3" height="22" rx="1" fill="currentColor" opacity="0.85">
              <animate attributeName="y"      values="12;15;12" dur="2.2s" begin="-0.54s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" />
              <animate attributeName="height" values="22;19;22" dur="2.2s" begin="-0.54s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" />
            </rect>
            {/* Apex bar — brand color */}
            <rect x="27" y="8"  width="3" height="26" rx="1.4" fill="hsl(var(--brand))">
              <animate attributeName="y"      values="8;11;8"   dur="2.2s" begin="-0.72s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" />
              <animate attributeName="height" values="26;23;26" dur="2.2s" begin="-0.72s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" />
            </rect>
          </g>

          {/* Dấu sắc — Vietnamese rising-tone accent (cultural cue) */}
          <line
            x1="32"
            y1="9"
            x2="36"
            y2="4.5"
            stroke="hsl(var(--brand))"
            strokeWidth="1.6"
            strokeLinecap="round"
            opacity="0.95"
          />

          {/* Live pulse beacon crowning the apex bar */}
          <circle cx="28.5" cy="6" r="2.2" fill="hsl(var(--brand))" opacity="0.55">
            <animate attributeName="r"       values="2.2;6;2.2"   dur="2s" repeatCount="indefinite" />
            <animate attributeName="opacity" values="0.55;0;0.55" dur="2s" repeatCount="indefinite" />
          </circle>
          <circle cx="28.5" cy="6" r="1.9" fill="hsl(var(--brand))" />
          <circle cx="28.5" cy="6" r="0.6" fill="hsl(var(--bg-1))" opacity="0.55" />

          {/* Baseline rule — ticker tape */}
          <line
            x1="5"
            y1="35"
            x2="35"
            y2="35"
            stroke="currentColor"
            strokeWidth="0.7"
            opacity="0.22"
            strokeLinecap="round"
          />
        </svg>
      </span>

      {/* Wordmark */}
      <span className="flex min-w-0 items-baseline leading-none tracking-[-0.025em] text-fg-0">
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
