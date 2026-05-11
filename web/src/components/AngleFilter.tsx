import { useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { ChevronDown, Compass, X } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '../shared/ui/dropdown-menu';
import { cn } from '../shared/lib/cn';
import {
  ANGLE_CATEGORIES,
  getAngleCategory,
  type AngleCategoryId,
} from '../lib/angleCategories';

/**
 * URL-persisted multi-select angle filter. Query: ?c=paradox,why_now
 */
export function useAngleFilter() {
  const [params, setParams] = useSearchParams();
  const raw = params.get('c');

  const selected = useMemo<AngleCategoryId[]>(
    () =>
      raw
        ? (raw
            .split(',')
            .map((s) => s.trim())
            .filter(Boolean) as AngleCategoryId[])
        : [],
    [raw],
  );

  const setSelected = (next: AngleCategoryId[]) => {
    const newParams = new URLSearchParams(params);
    if (next.length === 0) newParams.delete('c');
    else newParams.set('c', next.join(','));
    setParams(newParams, { replace: true });
  };

  return { selected, setSelected };
}

export function AngleFilter<T extends { category?: string }>({
  items,
  selected,
  onChange,
}: {
  items: T[];
  selected: AngleCategoryId[];
  onChange: (next: AngleCategoryId[]) => void;
}) {
  const [open, setOpen] = useState(false);

  // Article count per category
  const counts = useMemo(() => {
    const m = new Map<string, number>();
    for (const it of items) {
      if (it.category) m.set(it.category, (m.get(it.category) ?? 0) + 1);
    }
    return m;
  }, [items]);

  const toggle = (id: AngleCategoryId) => {
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
            : 'border-fg-4/40 bg-bg-2/60 text-fg-2 hover:border-fg-0/40 hover:text-fg-0',
        )}
        aria-label="Lọc theo hướng tiếp cận"
      >
        <Compass
          className={cn(
            'h-3.5 w-3.5 shrink-0',
            hasSelection ? 'text-brand' : 'text-fg-3',
          )}
          strokeWidth={1.85}
          aria-hidden
        />
        <span className="font-sans text-[11px] uppercase tracking-[0.18em] text-fg-3">
          Hướng
        </span>
        <AngleTriggerSummary selected={selected} />
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
        <div className="flex items-center justify-between gap-2 px-3 pb-1.5 pt-2.5">
          <DropdownMenuLabel className="!p-0 text-fg-2">
            Hướng tiếp cận
          </DropdownMenuLabel>
          <span className="font-mono text-[10px] tabular-nums text-fg-3">
            {hasSelection
              ? `${selected.length}/${ANGLE_CATEGORIES.length}`
              : `${ANGLE_CATEGORIES.length} loại`}
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
          {ANGLE_CATEGORIES.map((cat) => {
            const isSelected = selected.includes(cat.id);
            const count = counts.get(cat.id) ?? 0;
            const dim = count === 0 && !isSelected;
            return (
              <button
                type="button"
                key={cat.id}
                onClick={() => toggle(cat.id)}
                aria-pressed={isSelected}
                className={cn(
                  'group/row relative flex w-full items-center gap-2.5 rounded-md px-2 py-1.5 text-left transition-all duration-fast',
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

                {/* Label + description */}
                <span className="flex min-w-0 flex-1 flex-col">
                  <span className="font-sans text-[12px] font-medium text-fg-0">
                    {cat.label}
                  </span>
                  <span className="truncate font-sans text-[10px] text-fg-3">
                    {cat.description}
                  </span>
                </span>

                {/* Count */}
                <span
                  className={cn(
                    'shrink-0 font-mono text-[10.5px] tabular-nums',
                    count > 0 ? 'font-semibold text-fg-1' : 'text-fg-3',
                  )}
                >
                  {count > 0 ? count : '–'}
                </span>
              </button>
            );
          })}
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

function AngleTriggerSummary({ selected }: { selected: AngleCategoryId[] }) {
  if (selected.length === 0) {
    return (
      <span className="truncate font-sans text-[12px] text-fg-2">Tất cả</span>
    );
  }
  if (selected.length === 1) {
    const c = getAngleCategory(selected[0]);
    return (
      <span className="truncate font-sans text-[12px] font-semibold text-fg-0">
        {c?.short ?? selected[0]}
      </span>
    );
  }
  return (
    <span className="flex items-center gap-1 truncate">
      <span className="font-sans text-[12px] font-semibold text-fg-0">
        {getAngleCategory(selected[0])?.short ?? selected[0]}
      </span>
      <span className="inline-flex h-4 min-w-4 items-center justify-center rounded-full bg-brand px-1 font-sans text-[10px] font-bold tabular-nums text-brand-fg">
        +{selected.length - 1}
      </span>
    </span>
  );
}
