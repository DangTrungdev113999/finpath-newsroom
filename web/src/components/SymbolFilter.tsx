import { useEffect, useMemo, useRef, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { ChevronDown, Search, Tag, X } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuCheckboxItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '../shared/ui/dropdown-menu';
import { cn } from '../shared/lib/cn';

/**
 * URL-persisted multi-select ticker filter. Query: ?t=TCB,VCB,MBB
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

export function getUniqueTickers<T extends { ticker: string }>(
  items: T[],
): string[] {
  const set = new Set<string>();
  for (const it of items) if (it.ticker) set.add(it.ticker);
  return Array.from(set).sort();
}

function countByTicker<T extends { ticker: string }>(
  items: T[],
): Map<string, number> {
  const m = new Map<string, number>();
  for (const it of items) m.set(it.ticker, (m.get(it.ticker) ?? 0) + 1);
  return m;
}

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
  const searchRef = useRef<HTMLInputElement>(null);

  const available = useMemo(() => getUniqueTickers(items), [items]);
  const counts = useMemo(() => countByTicker(items), [items]);

  // Selected first, then alphabetical — selection stays sticky at top
  const ordered = useMemo(() => {
    const sel = new Set(selected);
    return [...available].sort((a, b) => {
      const aSel = sel.has(a);
      const bSel = sel.has(b);
      if (aSel !== bSel) return aSel ? -1 : 1;
      return a.localeCompare(b);
    });
  }, [available, selected]);

  const filtered = useMemo(() => {
    const q = query.trim().toUpperCase();
    if (!q) return ordered;
    return ordered.filter((t) => t.includes(q));
  }, [ordered, query]);

  // Focus search, reset query on open
  useEffect(() => {
    if (!open) return;
    setQuery('');
    const id = requestAnimationFrame(() => searchRef.current?.focus());
    return () => cancelAnimationFrame(id);
  }, [open]);

  const toggle = (ticker: string) => {
    onChange(
      selected.includes(ticker)
        ? selected.filter((t) => t !== ticker)
        : [...selected, ticker],
    );
  };

  const clearAll = () => onChange([]);

  const hasSelection = selected.length > 0;
  const totalItems = items.length;
  const filteredItemCount = hasSelection
    ? items.filter((i) => selected.includes(i.ticker)).length
    : totalItems;

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
          className="w-72 p-0"
        >
          <div className="flex items-center justify-between gap-2 px-2.5 pb-1 pt-2">
            <DropdownMenuLabel className="p-0 text-fg-2">
              Mã cổ phiếu
            </DropdownMenuLabel>
            <span className="font-mono text-[10px] tabular-nums text-fg-3">
              {hasSelection
                ? `${selected.length} chọn · ${filteredItemCount}/${totalItems} bài`
                : `${available.length} mã · ${totalItems} bài`}
            </span>
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
                // Keep typing inside the menu — stop Radix swallowing keys
                if (e.key.length === 1 || e.key === 'Backspace') {
                  e.stopPropagation();
                }
              }}
              placeholder="Tìm mã (TCB, VCB…)"
              className={cn(
                'flex-1 bg-transparent font-mono text-[11px] uppercase tracking-[0.04em] text-fg-0',
                'placeholder:text-fg-3 placeholder:normal-case placeholder:tracking-normal placeholder:font-sans placeholder:text-xs',
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
          <div className="max-h-72 overflow-y-auto px-1 pb-1">
            {filtered.length === 0 ? (
              <div className="px-3 py-4 text-center font-mono text-[11px] text-fg-3">
                Không có mã nào khớp "{query}"
              </div>
            ) : (
              filtered.map((ticker) => {
                const isSelected = selected.includes(ticker);
                const count = counts.get(ticker) ?? 0;
                return (
                  <DropdownMenuCheckboxItem
                    key={ticker}
                    checked={isSelected}
                    onSelect={(e) => {
                      // Prevent menu closing on each toggle
                      e.preventDefault();
                      toggle(ticker);
                    }}
                    className={cn(
                      'flex items-center justify-between gap-2',
                      isSelected && 'bg-brand/8',
                    )}
                  >
                    <span
                      className={cn(
                        'font-mono text-[12px] font-semibold tabular-nums tracking-[0.04em]',
                        isSelected ? 'text-fg-0' : 'text-fg-1',
                      )}
                    >
                      {ticker}
                    </span>
                    <span className="font-mono text-[10px] tabular-nums text-fg-3">
                      {count}
                    </span>
                  </DropdownMenuCheckboxItem>
                );
              })
            )}
          </div>
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Inline removable chips for selected (compact, shows what's active outside the menu) */}
      {hasSelection && (
        <div className="flex flex-wrap items-center gap-1">
          {selected.slice(0, 6).map((ticker) => (
            <button
              type="button"
              key={ticker}
              onClick={() => onChange(selected.filter((t) => t !== ticker))}
              className={cn(
                'group/chip inline-flex items-center gap-1 rounded-pill border border-brand/50 bg-brand/10 px-2 py-[2px]',
                'font-mono text-[10px] font-semibold tabular-nums tracking-[0.04em] text-fg-0',
                'transition-colors duration-fast hover:border-brand hover:bg-brand/20',
              )}
              aria-label={`Bỏ ${ticker}`}
              title={`Bỏ ${ticker}`}
            >
              {ticker}
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

function TriggerSummary({ selected }: { selected: string[] }) {
  if (selected.length === 0) {
    return (
      <span className="truncate font-sans text-[12px] text-fg-2">
        Tất cả
      </span>
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
