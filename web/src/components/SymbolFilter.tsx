import { useEffect, useMemo, useRef, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import Fuse from 'fuse.js';
import { ChevronDown, Search, Tag, X } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '../shared/ui/dropdown-menu';
import { cn } from '../shared/lib/cn';
import {
  SECTORS,
  TICKER_UNIVERSE,
  type Sector,
  type TickerInfo,
} from '../lib/tickerUniverse';

/**
 * URL-persisted multi-select ticker filter. Query: ?t=TCB,VCB
 */
export function useSymbolFilter() {
  const [params, setParams] = useSearchParams();
  const raw = params.get('t');

  const selected = useMemo(
    () =>
      raw
        ? raw
            .split(',')
            .map((s) => s.trim().toUpperCase())
            .filter(Boolean)
        : [],
    [raw],
  );

  const setSelected = (next: string[]) => {
    const newParams = new URLSearchParams(params);
    if (next.length === 0) newParams.delete('t');
    else newParams.set('t', next.join(','));
    setParams(newParams, { replace: true });
  };

  return { selected, setSelected };
}

// Build Fuse index once at module load — universe is static
const fuse = new Fuse<TickerInfo>(TICKER_UNIVERSE, {
  keys: [
    { name: 'code', weight: 3 },
    { name: 'name', weight: 2 },
    { name: 'aliases', weight: 1 },
  ],
  threshold: 0.4,
  ignoreLocation: true,
  minMatchCharLength: 1,
});

function countByTicker<T extends { ticker: string }>(
  items: T[],
): Map<string, number> {
  const m = new Map<string, number>();
  for (const it of items) m.set(it.ticker, (m.get(it.ticker) ?? 0) + 1);
  return m;
}

type SectorFilter = 'all' | Sector;

export function SymbolFilter<T extends { ticker: string }>({
  items,
  selected,
  onChange,
}: {
  items: T[];
  selected: string[];
  onChange: (next: string[]) => void;
}) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [sectorTab, setSectorTab] = useState<SectorFilter>('all');
  const searchRef = useRef<HTMLInputElement>(null);

  const counts = useMemo(() => countByTicker(items), [items]);

  // Apply sector tab + Fuse search + selected-first ordering
  const visible = useMemo(() => {
    const sectorPool =
      sectorTab === 'all'
        ? TICKER_UNIVERSE
        : TICKER_UNIVERSE.filter((t) => t.sector === sectorTab);

    const q = query.trim();
    const searched: TickerInfo[] = q
      ? fuse.search(q).map((r) => r.item).filter((t) =>
          sectorTab === 'all' ? true : t.sector === sectorTab,
        )
      : sectorPool;

    if (q) return searched;

    // No query — sort: selected first, then alphabetical within sector groups
    const sel = new Set(selected);
    return [...searched].sort((a, b) => {
      const aSel = sel.has(a.code);
      const bSel = sel.has(b.code);
      if (aSel !== bSel) return aSel ? -1 : 1;
      return a.code.localeCompare(b.code);
    });
  }, [query, sectorTab, selected]);

  // Section count per sector tab — uses CURRENT counts map
  const sectorCounts = useMemo(() => {
    const m: Record<SectorFilter, number> = { all: 0, bank: 0, ck: 0, bds: 0 };
    for (const t of TICKER_UNIVERSE) {
      const n = counts.get(t.code) ?? 0;
      m.all += n;
      m[t.sector] += n;
    }
    return m;
  }, [counts]);

  // Reset query + focus search on open
  useEffect(() => {
    if (!open) return;
    setQuery('');
    const id = requestAnimationFrame(() => searchRef.current?.focus());
    return () => cancelAnimationFrame(id);
  }, [open]);

  const toggle = (code: string) => {
    onChange(
      selected.includes(code)
        ? selected.filter((c) => c !== code)
        : [...selected, code],
    );
  };

  const clearAll = () => onChange([]);

  const hasSelection = selected.length > 0;
  const totalArticles = items.length;
  const filteredArticleCount = hasSelection
    ? items.filter((i) => selected.includes(i.ticker)).length
    : totalArticles;

  return (
    <div className="flex flex-wrap items-center gap-2">
      <DropdownMenu open={open} onOpenChange={setOpen}>
        <DropdownMenuTrigger
          className={cn(
            'group inline-flex h-8 max-w-full items-center gap-2 rounded-pill border px-3 font-sans text-[12px] font-medium transition-all duration-fast ease-out-quart',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35',
            hasSelection
              ? 'border-brand/60 bg-brand/10 text-fg-0 shadow-sm shadow-brand/15'
              : 'border-fg-4/40 bg-bg-2/60 text-fg-2 hover:border-fg-0/40 hover:text-fg-0',
          )}
          aria-label="Lọc theo mã cổ phiếu"
        >
          <Tag
            className={cn(
              'h-3.5 w-3.5 shrink-0',
              hasSelection ? 'text-brand' : 'text-fg-3',
            )}
            strokeWidth={1.85}
            aria-hidden
          />
          <span className="font-sans text-[11px] uppercase tracking-[0.18em] text-fg-3">
            Mã
          </span>
          <TriggerSummary selected={selected} />
          <ChevronDown
            className="h-3 w-3 shrink-0 text-fg-3 transition-transform duration-fast group-data-[state=open]:rotate-180"
            strokeWidth={2}
            aria-hidden
          />
        </DropdownMenuTrigger>

        <DropdownMenuContent
          align="start"
          side="bottom"
          sideOffset={6}
          className="w-[336px] p-0"
        >
          {/* Header */}
          <div className="flex items-center justify-between gap-2 px-3 pb-1 pt-2.5">
            <DropdownMenuLabel className="!p-0 text-fg-2">
              Mã cổ phiếu
            </DropdownMenuLabel>
            <span className="font-mono text-[10px] tabular-nums text-fg-3">
              {hasSelection
                ? `${selected.length} chọn · ${filteredArticleCount}/${totalArticles} bài`
                : `${TICKER_UNIVERSE.length} mã · ${totalArticles} bài`}
            </span>
          </div>

          {/* Sector tabs */}
          <div className="mx-2 mb-1.5 flex items-center gap-0.5 rounded-pill bg-bg-2/60 p-0.5">
            <SectorTab
              active={sectorTab === 'all'}
              onClick={() => setSectorTab('all')}
              label="Tất cả"
              count={sectorCounts.all}
              total={TICKER_UNIVERSE.length}
            />
            {SECTORS.map((s) => (
              <SectorTab
                key={s.id}
                active={sectorTab === s.id}
                onClick={() => setSectorTab(s.id)}
                label={s.short}
                title={s.label}
                count={sectorCounts[s.id]}
                total={TICKER_UNIVERSE.filter((t) => t.sector === s.id).length}
              />
            ))}
          </div>

          {/* Search */}
          <label
            className={cn(
              'mx-2 mb-1.5 flex h-7 items-center gap-1.5 rounded-md bg-bg-0 px-2',
              'shadow-[inset_0_0_0_1px_hsl(var(--fg-4)/0.55)]',
              'focus-within:shadow-[inset_0_0_0_1.5px_hsl(var(--focus-ring))]',
              'transition-shadow duration-fast ease-out-quart',
            )}
          >
            <Search
              className="h-3 w-3 shrink-0 text-fg-3"
              strokeWidth={1.75}
              aria-hidden
            />
            <input
              ref={searchRef}
              value={query}
              onChange={(e) => setQuery(e.currentTarget.value)}
              onKeyDown={(e) => {
                if (e.key.length === 1 || e.key === 'Backspace') {
                  e.stopPropagation();
                }
              }}
              placeholder="Tìm mã hoặc tên (VCB, Vietcombank, Techcom…)"
              className={cn(
                'flex-1 bg-transparent font-sans text-[11px] text-fg-0',
                'placeholder:text-fg-3 placeholder:font-sans placeholder:text-[11px]',
                'outline-none',
              )}
              aria-label="Tìm mã cổ phiếu"
              spellCheck={false}
              autoComplete="off"
            />
            {query && (
              <button
                type="button"
                onClick={() => {
                  setQuery('');
                  searchRef.current?.focus();
                }}
                className="text-fg-3 transition-colors hover:text-fg-0"
                aria-label="Xóa tìm kiếm"
              >
                <X className="h-3 w-3" strokeWidth={2} />
              </button>
            )}
          </label>

          {/* Clear-all action */}
          {hasSelection && (
            <button
              type="button"
              onClick={clearAll}
              className={cn(
                'mx-2 mb-1 flex h-6 w-[calc(100%-1rem)] items-center justify-between rounded-md px-2',
                'font-sans text-[11px] text-fg-2',
                'hover:bg-bg-2 hover:text-fg-0',
                'transition-colors duration-fast',
              )}
            >
              <span className="flex items-center gap-1.5">
                <X className="h-3 w-3" strokeWidth={2} />
                Bỏ chọn tất cả
              </span>
              <span className="font-mono text-[10px] tabular-nums text-fg-3">
                {selected.length}
              </span>
            </button>
          )}

          <DropdownMenuSeparator className="mx-2 my-1" />

          {/* List */}
          <div className="max-h-[280px] overflow-y-auto px-1 pb-1.5">
            {visible.length === 0 ? (
              <div className="px-3 py-6 text-center font-mono text-[11px] text-fg-3">
                {query
                  ? `Không có mã nào khớp "${query}"`
                  : 'Không có mã nào trong ngành này'}
              </div>
            ) : (
              visible.map((t) => {
                const isSelected = selected.includes(t.code);
                const count = counts.get(t.code) ?? 0;
                const dim = count === 0;
                return (
                  <button
                    type="button"
                    key={t.code}
                    onClick={() => toggle(t.code)}
                    className={cn(
                      'group/row relative flex w-full items-center gap-2.5 rounded-md px-2 py-1.5 text-left transition-all duration-fast',
                      isSelected
                        ? 'bg-brand/[0.09] ring-1 ring-brand/40'
                        : 'hover:bg-bg-2',
                      dim && !isSelected && 'opacity-60',
                    )}
                  >
                    {isSelected && (
                      <span
                        aria-hidden
                        className="absolute inset-y-1.5 left-0 w-[2px] rounded-r-full bg-brand"
                      />
                    )}
                    {/* Checkbox indicator */}
                    <span
                      aria-hidden
                      className={cn(
                        'flex h-4 w-4 shrink-0 items-center justify-center rounded-[5px] border transition-colors duration-fast',
                        isSelected
                          ? 'border-brand bg-brand text-brand-fg'
                          : 'border-fg-4/60 bg-bg-1',
                      )}
                    >
                      {isSelected && (
                        <svg
                          viewBox="0 0 12 12"
                          className="h-2.5 w-2.5"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2.5"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        >
                          <path d="M2.5 6.5l2.5 2.5 4.5-5" />
                        </svg>
                      )}
                    </span>
                    {/* Code */}
                    <span
                      className={cn(
                        'shrink-0 font-mono text-[12px] font-bold tabular-nums tracking-[0.04em]',
                        isSelected ? 'text-fg-0' : 'text-fg-0',
                      )}
                    >
                      {t.code}
                    </span>
                    {/* Name */}
                    <span className="min-w-0 flex-1 truncate font-sans text-[11px] text-fg-2">
                      {t.name}
                    </span>
                    {/* Sector chip */}
                    <span
                      className={cn(
                        'shrink-0 rounded-pill px-1.5 py-[1px] font-mono text-[9px] uppercase tracking-wider',
                        t.sector === 'bank' && 'bg-fg-4/30 text-fg-2',
                        t.sector === 'ck' && 'bg-fg-4/30 text-fg-2',
                        t.sector === 'bds' && 'bg-fg-4/30 text-fg-2',
                      )}
                    >
                      {t.sector === 'bank'
                        ? 'NH'
                        : t.sector === 'ck'
                          ? 'CK'
                          : 'BĐS'}
                    </span>
                    {/* Article count */}
                    <span
                      className={cn(
                        'shrink-0 font-mono text-[10px] tabular-nums',
                        count > 0 ? 'text-fg-1' : 'text-fg-3',
                      )}
                    >
                      {count}
                    </span>
                  </button>
                );
              })
            )}
          </div>

          {/* Footer hint */}
          <div className="border-t border-fg-4/30 bg-bg-2/40 px-3 py-1.5">
            <p className="font-sans text-[10px] text-fg-3">
              {visible.length} mã · {hasSelection ? 'chọn nhiều' : 'click để lọc'}
            </p>
          </div>
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Inline removable chips */}
      {hasSelection && (
        <div className="flex flex-wrap items-center gap-1">
          {selected.slice(0, 6).map((code) => (
            <button
              type="button"
              key={code}
              onClick={() => onChange(selected.filter((c) => c !== code))}
              className={cn(
                'group/chip inline-flex items-center gap-1 rounded-pill border border-brand/50 bg-brand/10 px-2 py-[2px]',
                'font-mono text-[10px] font-semibold tabular-nums tracking-[0.04em] text-fg-0',
                'transition-colors duration-fast hover:border-brand hover:bg-brand/20',
              )}
              aria-label={`Bỏ ${code}`}
              title={`Bỏ ${code}`}
            >
              {code}
              <X
                className="h-2.5 w-2.5 text-fg-3 group-hover/chip:text-fg-0"
                strokeWidth={2.5}
              />
            </button>
          ))}
          {selected.length > 6 && (
            <span className="font-mono text-[10px] tabular-nums text-fg-3">
              +{selected.length - 6}
            </span>
          )}
        </div>
      )}
    </div>
  );
}

function SectorTab({
  active,
  onClick,
  label,
  title,
  count,
  total,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
  title?: string;
  count: number;
  total: number;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      title={title ?? label}
      className={cn(
        'flex flex-1 items-center justify-center gap-1 rounded-pill px-2 py-1 font-sans text-[10.5px] font-medium transition-all duration-fast',
        active
          ? 'bg-brand text-brand-fg shadow-sm shadow-brand/20'
          : 'text-fg-2 hover:text-fg-0',
      )}
    >
      <span className={active ? 'font-semibold' : ''}>{label}</span>
      <span
        className={cn(
          'font-mono text-[9px] tabular-nums',
          active ? 'text-brand-fg/85' : 'text-fg-3',
        )}
      >
        {count}/{total > 0 ? total : 0}
      </span>
    </button>
  );
}

function TriggerSummary({ selected }: { selected: string[] }) {
  if (selected.length === 0) {
    return (
      <span className="truncate font-sans text-[12px] text-fg-2">Tất cả</span>
    );
  }
  if (selected.length === 1) {
    return (
      <span className="truncate font-mono text-[12px] font-semibold tabular-nums tracking-[0.04em] text-fg-0">
        {selected[0]}
      </span>
    );
  }
  return (
    <span className="flex items-center gap-1 truncate">
      <span className="font-mono text-[12px] font-semibold tabular-nums tracking-[0.04em] text-fg-0">
        {selected[0]}
      </span>
      <span
        className={cn(
          'inline-flex h-4 min-w-4 items-center justify-center rounded-full bg-brand px-1',
          'font-sans text-[10px] font-bold tabular-nums text-brand-fg',
        )}
      >
        +{selected.length - 1}
      </span>
    </span>
  );
}
