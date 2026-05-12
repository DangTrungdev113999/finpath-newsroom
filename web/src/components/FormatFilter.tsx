import { useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { ChevronDown, LayoutTemplate, X } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '../shared/ui/dropdown-menu';
import { cn } from '../shared/lib/cn';
import {
  FORMAT_CATEGORIES,
  getFormatCategory,
  type FormatCategory,
} from '../lib/formatCategories';
import type { FormatId } from '../types';

/**
 * URL-persisted multi-select format filter. Query: ?f=standard_listicle,flash_qa
 */
export function useFormatFilter() {
  const [params, setParams] = useSearchParams();
  const raw = params.get('f');

  const selected = useMemo<FormatId[]>(
    () =>
      raw
        ? (raw
            .split(',')
            .map((s) => s.trim())
            .filter(Boolean) as FormatId[])
        : [],
    [raw],
  );

  const setSelected = (next: FormatId[]) => {
    const newParams = new URLSearchParams(params);
    if (next.length === 0) newParams.delete('f');
    else newParams.set('f', next.join(','));
    setParams(newParams, { replace: true });
  };

  return { selected, setSelected };
}

export function FormatFilter<T extends { format_id?: string }>({
  items,
  selected,
  onChange,
}: {
  items: T[];
  selected: FormatId[];
  onChange: (next: FormatId[]) => void;
}) {
  const [open, setOpen] = useState(false);

  // Article count per format
  const counts = useMemo(() => {
    const m = new Map<string, number>();
    for (const it of items) {
      if (it.format_id) m.set(it.format_id, (m.get(it.format_id) ?? 0) + 1);
    }
    return m;
  }, [items]);

  const toggle = (id: FormatId) => {
    onChange(
      selected.includes(id)
        ? selected.filter((c) => c !== id)
        : [...selected, id],
    );
  };

  const clearAll = () => onChange([]);
  const hasSelection = selected.length > 0;

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger
        className={cn(
          'group inline-flex h-8 max-w-full items-center gap-2 rounded-pill border px-3 font-sans text-[12px] font-medium transition-all duration-fast ease-out-quart',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35',
          hasSelection
            ? 'border-brand/60 bg-brand/10 text-fg-0 shadow-sm shadow-brand/15'
            : 'border-fg-3/55 bg-bg-2 text-fg-1 hover:border-fg-0/60 hover:text-fg-0',
        )}
        aria-label="Lọc theo định dạng bài"
      >
        <LayoutTemplate
          className={cn(
            'h-3.5 w-3.5 shrink-0',
            hasSelection ? 'text-brand' : 'text-fg-1',
          )}
          strokeWidth={2}
          aria-hidden
        />
        <span className="font-sans text-[10.5px] font-semibold uppercase tracking-[0.14em] text-fg-2">
          Định dạng
        </span>
        <FormatTriggerSummary selected={selected} />
        <ChevronDown
          className="h-3 w-3 shrink-0 text-fg-2 transition-transform duration-fast group-data-[state=open]:rotate-180"
          strokeWidth={2.25}
          aria-hidden
        />
      </DropdownMenuTrigger>

      <DropdownMenuContent
        align="start"
        side="bottom"
        sideOffset={6}
        className="w-[340px] p-0"
      >
        <div className="flex items-center justify-between gap-2 px-3 pb-1.5 pt-2.5">
          <DropdownMenuLabel className="!p-0 text-fg-2">
            Định dạng bài
          </DropdownMenuLabel>
          <span className="font-mono text-[10px] tabular-nums text-fg-3">
            {hasSelection
              ? `${selected.length}/${FORMAT_CATEGORIES.length}`
              : `${FORMAT_CATEGORIES.length} loại`}
          </span>
        </div>

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

        <div className="space-y-0.5 px-1 pb-2">
          {FORMAT_CATEGORIES.map((fmt) => (
            <FormatRow
              key={fmt.id}
              fmt={fmt}
              isSelected={selected.includes(fmt.id)}
              count={counts.get(fmt.id) ?? 0}
              onToggle={() => toggle(fmt.id)}
            />
          ))}
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

function FormatRow({
  fmt,
  isSelected,
  count,
  onToggle,
}: {
  fmt: FormatCategory;
  isSelected: boolean;
  count: number;
  onToggle: () => void;
}) {
  const dim = count === 0 && !isSelected;
  return (
    <button
      type="button"
      onClick={onToggle}
      aria-pressed={isSelected}
      className={cn(
        'group/row relative flex w-full items-start gap-2.5 rounded-md px-2 py-2 text-left transition-all duration-fast',
        isSelected
          ? 'bg-brand/[0.09] ring-1 ring-brand/40'
          : 'hover:bg-bg-2',
        dim && 'opacity-55',
      )}
    >
      {/* Checkbox */}
      <span
        aria-hidden
        className={cn(
          'mt-0.5 flex h-4 w-4 shrink-0 items-center justify-center rounded-[5px] border transition-colors duration-fast',
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

      {/* Label + description + word range + count */}
      <span className="flex min-w-0 flex-1 flex-col gap-0.5">
        <span className="flex items-baseline justify-between gap-2">
          <span className="font-sans text-[12.5px] font-semibold text-fg-0">
            {fmt.label}
          </span>
          <span className="font-mono text-[10px] tabular-nums text-fg-3">
            {fmt.wordRange} · {count} bài
          </span>
        </span>
        <span className="font-sans text-[11px] leading-snug text-fg-2">
          {fmt.description}
        </span>
      </span>
    </button>
  );
}

function FormatTriggerSummary({ selected }: { selected: FormatId[] }) {
  if (selected.length === 0) {
    return (
      <span className="truncate font-sans text-[12px] font-semibold text-fg-0">Tất cả</span>
    );
  }
  if (selected.length === 1) {
    const c = getFormatCategory(selected[0]);
    return (
      <span className="truncate font-sans text-[12px] font-semibold text-fg-0">
        {c?.short ?? selected[0]}
      </span>
    );
  }
  return (
    <span className="flex items-center gap-1 truncate">
      <span className="font-sans text-[12px] font-semibold text-fg-0">
        {getFormatCategory(selected[0])?.short ?? selected[0]}
      </span>
      <span className="inline-flex h-4 min-w-4 items-center justify-center rounded-full bg-brand px-1 font-sans text-[10px] font-bold tabular-nums text-brand-fg">
        +{selected.length - 1}
      </span>
    </span>
  );
}
