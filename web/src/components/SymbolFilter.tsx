import { useEffect, useMemo, useRef, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import Fuse from 'fuse.js';
import { useVirtualizer } from '@tanstack/react-virtual';
import { ChevronDown, Search, Tag, X } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
  DialogTrigger,
} from '../shared/ui/dialog';
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

// Fuse index — rebuilt once at module load
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

const ROW_HEIGHT = 40;

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
  const scrollRef = useRef<HTMLDivElement>(null);

  const counts = useMemo(() => countByTicker(items), [items]);

  const visible = useMemo(() => {
    const sectorPool =
      sectorTab === 'all'
        ? TICKER_UNIVERSE
        : TICKER_UNIVERSE.filter((t) => t.sector === sectorTab);

    const q = query.trim();
    if (q) {
      return fuse
        .search(q)
        .map((r) => r.item)
        .filter((t) => (sectorTab === 'all' ? true : t.sector === sectorTab));
    }

    const sel = new Set(selected);
    return [...sectorPool].sort((a, b) => {
      const aSel = sel.has(a.code);
      const bSel = sel.has(b.code);
      if (aSel !== bSel) return aSel ? -1 : 1;
      if (a.sector !== b.sector) {
        return (
          SECTORS.findIndex((s) => s.id === a.sector) -
          SECTORS.findIndex((s) => s.id === b.sector)
        );
      }
      return a.code.localeCompare(b.code);
    });
  }, [query, sectorTab, selected]);

  // Ticker count per sector (universe size) — distinct from article counts
  const sectorTickerCounts = useMemo(() => {
    const m: Record<SectorFilter, number> = {
      all: TICKER_UNIVERSE.length,
      bank: 0,
      ck: 0,
      bds: 0,
    };
    for (const t of TICKER_UNIVERSE) m[t.sector] += 1;
    return m;
  }, []);

  // Virtualizer
  const virtualizer = useVirtualizer({
    count: visible.length,
    getScrollElement: () => scrollRef.current,
    estimateSize: () => ROW_HEIGHT,
    overscan: 10,
  });

  useEffect(() => {
    if (!open) return;
    setQuery('');
    setSectorTab('all');
    const id = requestAnimationFrame(() => searchRef.current?.focus());
    return () => cancelAnimationFrame(id);
  }, [open]);

  // Reset scroll to top when filter changes
  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = 0;
  }, [query, sectorTab]);

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
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger
          className={cn(
            'group inline-flex h-8 max-w-full items-center gap-2 rounded-pill border px-3 font-sans text-[12px] font-medium transition-all duration-fast ease-out-quart',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35',
            hasSelection
              ? 'border-brand/60 bg-brand/10 text-fg-0 shadow-sm shadow-brand/15'
              : 'border-fg-4/40 bg-bg-2/60 text-fg-2 hover:border-fg-0/40 hover:text-fg-0',
          )}
          aria-label="Mở bộ lọc mã cổ phiếu"
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
            className="h-3 w-3 shrink-0 text-fg-3"
            strokeWidth={2}
            aria-hidden
          />
        </DialogTrigger>

        <DialogContent className="flex h-[min(720px,85vh)] flex-col">
          {/* SR-only accessibility labels — visual header below is hand-laid */}
          <DialogTitle className="sr-only">Lọc cổ phiếu</DialogTitle>
          <DialogDescription className="sr-only">
            Chọn các mã cổ phiếu để lọc danh sách bài viết
          </DialogDescription>

          {/* ── Header (compact single row) ────────────────────────── */}
          <div className="flex items-center gap-2.5 border-b border-fg-4/30 bg-bg-2/40 px-4 py-2.5 pr-11">
            <Tag
              className="h-3.5 w-3.5 shrink-0 text-brand"
              strokeWidth={2}
              aria-hidden
            />
            <span className="font-display text-[14px] font-semibold tracking-[-0.01em] text-fg-0">
              Lọc cổ phiếu
            </span>
            <span className="ml-auto font-mono text-[11px] tabular-nums">
              {hasSelection ? (
                <>
                  <span className="font-semibold text-brand">{selected.length}</span>
                  <span className="text-fg-3"> chọn · </span>
                  <span className="font-semibold text-fg-1">{filteredArticleCount}</span>
                  <span className="text-fg-3">/{totalArticles} bài</span>
                </>
              ) : (
                <>
                  <span className="font-semibold text-fg-1">{TICKER_UNIVERSE.length}</span>
                  <span className="text-fg-3"> mã · </span>
                  <span className="font-semibold text-fg-1">{totalArticles}</span>
                  <span className="text-fg-3"> bài</span>
                </>
              )}
            </span>
          </div>

          {/* ── Controls ───────────────────────────────────────────── */}
          <div className="space-y-2 border-b border-fg-4/30 px-4 py-2.5">
            {/* Search */}
            <label
              className={cn(
                'flex h-9 items-center gap-2 rounded-lg bg-bg-0 px-2.5',
                'shadow-[inset_0_0_0_1px_hsl(var(--fg-4)/0.55)]',
                'focus-within:shadow-[inset_0_0_0_1.5px_hsl(var(--brand))]',
                'transition-shadow duration-fast ease-out-quart',
              )}
            >
              <Search
                className="h-3.5 w-3.5 shrink-0 text-fg-3"
                strokeWidth={1.75}
                aria-hidden
              />
              <input
                ref={searchRef}
                value={query}
                onChange={(e) => setQuery(e.currentTarget.value)}
                placeholder="Tìm mã hoặc tên — VCB, Vietcombank, Techcom…"
                className="flex-1 bg-transparent font-sans text-[12.5px] text-fg-0 outline-none placeholder:text-fg-3"
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
                  <X className="h-3.5 w-3.5" strokeWidth={2} />
                </button>
              )}
            </label>

            {/* Sector tabs */}
            <div className="flex items-center gap-0.5 rounded-pill bg-bg-2/60 p-0.5">
              <SectorTab
                active={sectorTab === 'all'}
                onClick={() => setSectorTab('all')}
                label="Tất cả"
                count={sectorTickerCounts.all}
              />
              {SECTORS.map((s) => (
                <SectorTab
                  key={s.id}
                  active={sectorTab === s.id}
                  onClick={() => setSectorTab(s.id)}
                  label={s.label}
                  count={sectorTickerCounts[s.id]}
                />
              ))}
            </div>

            {/* Selected chips */}
            {hasSelection && (
              <div className="flex flex-wrap items-center gap-1">
                {selected.slice(0, 10).map((code) => (
                  <button
                    type="button"
                    key={code}
                    onClick={() => toggle(code)}
                    className="group/chip inline-flex items-center gap-1 rounded-pill border border-brand/50 bg-brand/10 px-1.5 py-[1px] font-mono text-[10px] font-semibold tabular-nums text-fg-0 transition-colors duration-fast hover:border-brand hover:bg-brand/20"
                    aria-label={`Bỏ ${code}`}
                  >
                    {code}
                    <X
                      className="h-2.5 w-2.5 text-fg-3 group-hover/chip:text-fg-0"
                      strokeWidth={2.5}
                    />
                  </button>
                ))}
                {selected.length > 10 && (
                  <span className="font-mono text-[10px] tabular-nums text-fg-3">
                    +{selected.length - 10}
                  </span>
                )}
                <button
                  type="button"
                  onClick={clearAll}
                  className="ml-auto rounded-md px-1.5 py-0.5 font-sans text-[10.5px] font-medium text-fg-3 transition-colors hover:bg-bg-2 hover:text-fg-0"
                >
                  Bỏ chọn
                </button>
              </div>
            )}
          </div>

          {/* ── Virtualized list ──────────────────────────────────── */}
          <div
            ref={scrollRef}
            className="min-h-0 flex-1 overflow-y-auto"
          >
            {visible.length === 0 ? (
              <div className="flex h-32 items-center justify-center">
                <p className="text-center font-mono text-[12px] text-fg-3">
                  {query ? (
                    <>
                      Không có mã nào khớp{' '}
                      <span className="font-semibold text-fg-1">"{query}"</span>
                    </>
                  ) : (
                    'Không có mã nào trong ngành này'
                  )}
                </p>
              </div>
            ) : (
              <div
                style={{
                  height: virtualizer.getTotalSize(),
                  position: 'relative',
                }}
              >
                {virtualizer.getVirtualItems().map((vRow) => {
                  const t = visible[vRow.index];
                  if (!t) return null;
                  return (
                    <div
                      key={t.code}
                      style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        transform: `translateY(${vRow.start}px)`,
                        height: vRow.size,
                      }}
                    >
                      <TickerRow
                        ticker={t}
                        count={counts.get(t.code) ?? 0}
                        selected={selected.includes(t.code)}
                        onToggle={() => toggle(t.code)}
                      />
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* ── Footer ─────────────────────────────────────────────── */}
          <div className="flex items-center justify-between gap-3 border-t border-fg-4/30 bg-bg-2/40 px-4 py-2">
            <span className="font-mono text-[10.5px] text-fg-3">
              {visible.length} / {TICKER_UNIVERSE.length} mã
              {query && (
                <>
                  {' '}
                  · "<span className="font-semibold text-fg-1">{query}</span>"
                </>
              )}
            </span>
            <button
              type="button"
              onClick={() => setOpen(false)}
              className={cn(
                'inline-flex h-7 items-center gap-1.5 rounded-pill px-3.5 font-sans text-[12px] font-semibold transition-all duration-fast',
                'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35',
                hasSelection
                  ? 'bg-brand text-brand-fg shadow-sm shadow-brand/25'
                  : 'bg-fg-0 text-bg-1 hover:opacity-90',
              )}
            >
              {hasSelection ? (
                <>
                  Áp dụng
                  <span className="rounded-full bg-brand-fg/20 px-1.5 py-[1px] font-mono text-[10px]">
                    {selected.length}
                  </span>
                </>
              ) : (
                'Đóng'
              )}
            </button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Inline removable chips outside dialog */}
      {hasSelection && (
        <div className="flex flex-wrap items-center gap-1">
          {selected.slice(0, 6).map((code) => (
            <button
              type="button"
              key={code}
              onClick={() => onChange(selected.filter((c) => c !== code))}
              className="group/chip inline-flex items-center gap-1 rounded-pill border border-brand/50 bg-brand/10 px-2 py-[2px] font-mono text-[10px] font-semibold tabular-nums tracking-[0.04em] text-fg-0 transition-colors duration-fast hover:border-brand hover:bg-brand/20"
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

function TickerRow({
  ticker,
  count,
  selected,
  onToggle,
}: {
  ticker: TickerInfo;
  count: number;
  selected: boolean;
  onToggle: () => void;
}) {
  const hasArticles = count > 0;
  const sectorShort =
    ticker.sector === 'bank' ? 'NH' : ticker.sector === 'ck' ? 'CK' : 'BĐS';

  return (
    <button
      type="button"
      onClick={onToggle}
      aria-pressed={selected}
      className={cn(
        'group/row flex h-full w-full items-center gap-2.5 px-4 text-left transition-colors duration-fast',
        'border-b border-fg-4/15',
        selected
          ? 'bg-brand/[0.09] hover:bg-brand/[0.12]'
          : 'hover:bg-bg-2/70',
        !hasArticles && !selected && 'opacity-65',
      )}
    >
      {/* Checkbox indicator */}
      <span
        aria-hidden
        className={cn(
          'flex h-4 w-4 shrink-0 items-center justify-center rounded-[5px] border transition-colors duration-fast',
          selected
            ? 'border-brand bg-brand text-brand-fg'
            : 'border-fg-4/60 bg-bg-1',
        )}
      >
        {selected && (
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
      <span className="w-12 shrink-0 font-mono text-[12.5px] font-bold tabular-nums tracking-[0.03em] text-fg-0">
        {ticker.code}
      </span>

      {/* Name */}
      <span className="min-w-0 flex-1 truncate font-sans text-[12px] text-fg-1">
        {ticker.name}
      </span>

      {/* Exchange */}
      <span className="hidden shrink-0 font-mono text-[9px] uppercase tracking-wider text-fg-3 sm:inline">
        {ticker.exchange}
      </span>

      {/* Sector chip */}
      <span
        className={cn(
          'shrink-0 rounded-pill px-1.5 py-[1px] font-mono text-[9px] uppercase tracking-wider',
          selected ? 'bg-brand/20 text-brand' : 'bg-fg-4/25 text-fg-2',
        )}
      >
        {sectorShort}
      </span>

      {/* Count */}
      <span className="flex w-14 shrink-0 items-center justify-end gap-1 font-mono text-[10.5px] tabular-nums">
        <span
          className={cn(
            'inline-block h-1.5 w-1.5 rounded-full',
            hasArticles ? 'bg-brand' : 'bg-fg-4',
          )}
        />
        <span className={hasArticles ? 'text-fg-1' : 'text-fg-3'}>
          {hasArticles ? `${count}` : '·'}
        </span>
      </span>
    </button>
  );
}

function SectorTab({
  active,
  onClick,
  label,
  count,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
  count: number;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        'flex flex-1 items-center justify-center gap-1.5 rounded-pill px-2.5 py-1 font-sans text-[11.5px] font-medium transition-all duration-fast',
        active
          ? 'bg-brand text-brand-fg shadow-sm shadow-brand/20'
          : 'text-fg-2 hover:text-fg-0',
      )}
    >
      <span className={active ? 'font-semibold' : ''}>{label}</span>
      <span
        className={cn(
          'rounded-full px-1.5 py-[1px] font-mono text-[9px] font-bold tabular-nums',
          active ? 'bg-brand-fg/25 text-brand-fg' : 'bg-fg-4/30 text-fg-2',
        )}
      >
        {count}
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
      <span className="inline-flex h-4 min-w-4 items-center justify-center rounded-full bg-brand px-1 font-sans text-[10px] font-bold tabular-nums text-brand-fg">
        +{selected.length - 1}
      </span>
    </span>
  );
}
