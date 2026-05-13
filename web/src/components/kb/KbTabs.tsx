import { useEffect, useMemo, useRef, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import Fuse from 'fuse.js';
import { Check, ChevronDown, Layers, Search, X } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
  DialogTrigger,
} from '../../shared/ui/dialog';
import { cn } from '../../shared/lib/cn';
import { SECTOR_LABELS, type Sector } from '../../lib/kbTypes';
import { docsForSector } from '../../lib/kbLoader';

// Category buckets keep the list scannable — 24 sectors land in 8 visual chapters.
const SECTOR_CATEGORIES: { label: string; sectors: Sector[] }[] = [
  { label: 'Tài chính', sectors: ['bank', 'ck', 'insurance'] },
  { label: 'Bất động sản', sectors: ['bds', 'industrial-park', 'construction', 'public-investment'] },
  { label: 'Tiêu dùng', sectors: ['retail', 'food', 'pharma', 'automotive'] },
  { label: 'Xuất khẩu', sectors: ['seafood', 'textile'] },
  { label: 'Năng lượng & Vật liệu', sectors: ['oil-gas', 'utilities', 'chemicals', 'sugar'] },
  { label: 'Vận tải & Du lịch', sectors: ['aviation', 'transport', 'tourism'] },
  { label: 'Công nghệ & Tập đoàn', sectors: ['technology', 'viettel', 'vingroup'] },
  { label: 'Tra cứu', sectors: ['stock-master'] },
];

// Flat index for search — Fuse + accent-insensitive
interface SectorIndexEntry {
  sector: Sector;
  label: string;
  category: string;
  count: number;
  searchKey: string; // ASCII-folded for diacritic-insensitive match
}

function fold(s: string): string {
  return s
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/đ/g, 'd')
    .replace(/Đ/g, 'D')
    .toLowerCase();
}

function buildIndex(): SectorIndexEntry[] {
  const entries: SectorIndexEntry[] = [];
  for (const cat of SECTOR_CATEGORIES) {
    for (const s of cat.sectors) {
      const label = SECTOR_LABELS[s];
      entries.push({
        sector: s,
        label,
        category: cat.label,
        count: docsForSector(s).length,
        searchKey: `${fold(label)} ${fold(cat.label)} ${s}`,
      });
    }
  }
  return entries;
}

export function KbTabs({ active }: { active: Sector }) {
  const [params, setParams] = useSearchParams();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const index = useMemo(buildIndex, []);
  const activeEntry = index.find((e) => e.sector === active);
  const totalDocs = useMemo(() => index.reduce((a, e) => a + e.count, 0), [index]);

  const fuse = useMemo(
    () =>
      new Fuse(index, {
        keys: ['searchKey'],
        threshold: 0.35,
        ignoreLocation: true,
        minMatchCharLength: 1,
      }),
    [index],
  );

  const filtered = useMemo(() => {
    const q = query.trim();
    if (!q) return null; // null = show categorized view
    const folded = fold(q);
    return fuse.search(folded).map((r) => r.item);
  }, [query, fuse]);

  // Reset search when dialog opens; focus input
  useEffect(() => {
    if (!open) return;
    setQuery('');
    // Radix DialogContent handles its own focus — small delay lets it settle
    const t = window.setTimeout(() => inputRef.current?.focus(), 30);
    return () => window.clearTimeout(t);
  }, [open]);

  const onSelect = (sector: Sector) => {
    const next = new URLSearchParams(params);
    if (sector === 'bds') next.delete('sector');
    else next.set('sector', sector);
    setParams(next, { replace: true });
    setOpen(false);
  };

  return (
    <div className="border-b border-fg-4/40 p-2.5">
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger
          className={cn(
            'group flex w-full items-center gap-2.5 rounded-lg border px-3 py-2.5 text-left transition-all duration-fast ease-out-quart',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/40',
            'border-fg-4/55 bg-bg-2 hover:border-brand/55 hover:bg-bg-2/70',
          )}
          aria-label="Chọn ngành KB"
        >
          <Layers
            className="h-4 w-4 shrink-0 text-brand"
            strokeWidth={2}
            aria-hidden
          />
          <div className="min-w-0 flex-1">
            <div className="font-sans text-[10px] font-semibold uppercase tracking-[0.18em] text-fg-3">
              Ngành KB
            </div>
            <div className="mt-0.5 flex items-baseline gap-1.5">
              <span className="truncate font-display text-[15px] font-semibold tracking-[-0.005em] text-fg-0">
                {activeEntry ? activeEntry.label : 'Chọn ngành'}
              </span>
              {activeEntry && (
                <span className="font-mono text-[11px] font-medium tabular-nums text-fg-3">
                  {activeEntry.count > 0 ? activeEntry.count : '—'}
                </span>
              )}
            </div>
          </div>
          <ChevronDown
            className="h-4 w-4 shrink-0 text-fg-2 transition-transform duration-fast group-data-[state=open]:rotate-180"
            strokeWidth={2}
            aria-hidden
          />
        </DialogTrigger>

        <DialogContent className="flex h-[min(640px,82vh)] max-w-[520px] flex-col">
          <DialogTitle className="sr-only">Chọn ngành KB</DialogTitle>
          <DialogDescription className="sr-only">
            Chọn một ngành để xem các tài liệu KB tương ứng. Hỗ trợ tìm kiếm theo tên ngành.
          </DialogDescription>

          {/* Header */}
          <div className="flex items-center gap-2.5 border-b border-fg-4/30 bg-bg-2/40 px-4 py-3 pr-11">
            <Layers
              className="h-4 w-4 shrink-0 text-brand"
              strokeWidth={2}
              aria-hidden
            />
            <span className="font-display text-[15px] font-semibold tracking-[-0.01em] text-fg-0">
              Chọn ngành
            </span>
            <span className="ml-auto font-mono text-[11px] tabular-nums">
              <span className="font-semibold text-fg-1">{index.length}</span>
              <span className="text-fg-3"> ngành · </span>
              <span className="font-semibold text-fg-1">{totalDocs}</span>
              <span className="text-fg-3"> tài liệu</span>
            </span>
          </div>

          {/* Search */}
          <div className="border-b border-fg-4/30 px-4 py-3">
            <label
              className={cn(
                'flex h-10 items-center gap-2.5 rounded-lg bg-bg-0 px-3',
                'shadow-[inset_0_0_0_1px_hsl(var(--fg-4)/0.55)]',
                'focus-within:shadow-[inset_0_0_0_1.5px_hsl(var(--brand))]',
                'transition-shadow duration-fast ease-out-quart',
              )}
            >
              <Search
                className="h-4 w-4 shrink-0 text-fg-3"
                strokeWidth={1.75}
                aria-hidden
              />
              <input
                ref={inputRef}
                value={query}
                onChange={(e) => setQuery(e.currentTarget.value)}
                placeholder="Tìm ngành — ngân hàng, bds, chứng khoán…"
                className="flex-1 bg-transparent font-sans text-[14px] text-fg-0 outline-none placeholder:text-fg-3"
                aria-label="Tìm ngành KB"
                spellCheck={false}
                autoComplete="off"
              />
              {query && (
                <button
                  type="button"
                  onClick={() => {
                    setQuery('');
                    inputRef.current?.focus();
                  }}
                  className="text-fg-3 transition-colors hover:text-fg-0"
                  aria-label="Xóa tìm kiếm"
                >
                  <X className="h-4 w-4" strokeWidth={2} />
                </button>
              )}
            </label>
          </div>

          {/* List */}
          <div className="min-h-0 flex-1 overflow-y-auto px-2 py-2">
            {filtered ? (
              filtered.length === 0 ? (
                <div className="flex h-32 items-center justify-center">
                  <p className="text-center font-sans text-[13px] text-fg-3">
                    Không có ngành nào khớp{' '}
                    <span className="font-semibold text-fg-1">"{query}"</span>
                  </p>
                </div>
              ) : (
                <ul role="listbox" aria-label="Kết quả tìm ngành" className="space-y-0.5">
                  {filtered.map((e) => (
                    <SectorRow
                      key={e.sector}
                      entry={e}
                      active={e.sector === active}
                      showCategory
                      onSelect={onSelect}
                    />
                  ))}
                </ul>
              )
            ) : (
              <div className="space-y-3 py-1">
                {SECTOR_CATEGORIES.map((cat) => {
                  const entries = index.filter((e) => e.category === cat.label);
                  if (entries.length === 0) return null;
                  return (
                    <section key={cat.label}>
                      <div className="flex items-baseline justify-between px-2 pb-1.5 pt-1">
                        <h3 className="font-sans text-[10.5px] font-semibold uppercase tracking-[0.2em] text-fg-3">
                          {cat.label}
                        </h3>
                        <span className="font-mono text-[10px] tabular-nums text-fg-4">
                          {entries.reduce((a, e) => a + e.count, 0)}
                        </span>
                      </div>
                      <ul role="listbox" aria-label={cat.label} className="space-y-0.5">
                        {entries.map((e) => (
                          <SectorRow
                            key={e.sector}
                            entry={e}
                            active={e.sector === active}
                            onSelect={onSelect}
                          />
                        ))}
                      </ul>
                    </section>
                  );
                })}
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="flex items-center justify-between gap-3 border-t border-fg-4/30 bg-bg-2/40 px-4 py-2.5">
            <span className="font-mono text-[10.5px] text-fg-3">
              {filtered
                ? `${filtered.length} / ${index.length} ngành`
                : `Đang xem · ${activeEntry?.label ?? '—'}`}
            </span>
            <kbd className="rounded border border-fg-4/40 bg-bg-1 px-1.5 py-0.5 font-mono text-[10px] text-fg-3">
              Esc
            </kbd>
          </div>
        </DialogContent>
      </Dialog>

      <p className="mt-2 px-1 font-sans text-[11.5px] text-fg-3">
        <span className="font-semibold text-fg-1 tabular-nums">{activeEntry?.count ?? 0}</span>{' '}
        tài liệu trong{' '}
        <span className="font-medium text-fg-1">{activeEntry?.label ?? '—'}</span>
      </p>
    </div>
  );
}

function SectorRow({
  entry,
  active,
  showCategory,
  onSelect,
}: {
  entry: SectorIndexEntry;
  active: boolean;
  showCategory?: boolean;
  onSelect: (s: Sector) => void;
}) {
  const empty = entry.count === 0;
  return (
    <li>
      <button
        type="button"
        onClick={() => onSelect(entry.sector)}
        role="option"
        aria-selected={active}
        className={cn(
          'group flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left transition-colors duration-fast',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/40',
          active
            ? 'bg-brand/12 ring-1 ring-inset ring-brand/35'
            : 'hover:bg-bg-2',
        )}
      >
        <span
          className={cn(
            'flex h-5 w-5 shrink-0 items-center justify-center rounded-full transition-colors',
            active
              ? 'bg-brand text-brand-fg'
              : 'border border-fg-4/55 bg-transparent text-transparent group-hover:border-fg-3',
          )}
          aria-hidden
        >
          <Check className="h-3 w-3" strokeWidth={2.75} />
        </span>

        <div className="min-w-0 flex-1">
          <div className="flex items-baseline gap-2">
            <span
              className={cn(
                'truncate font-sans text-[14.5px] font-medium tracking-[-0.005em]',
                active ? 'text-fg-0' : empty ? 'text-fg-2' : 'text-fg-0',
              )}
            >
              {entry.label}
            </span>
            {showCategory && (
              <span className="shrink-0 font-sans text-[10.5px] text-fg-3">
                · {entry.category}
              </span>
            )}
          </div>
        </div>

        <span
          className={cn(
            'shrink-0 rounded-pill px-2 py-0.5 font-mono text-[11px] font-semibold tabular-nums',
            empty
              ? 'bg-bg-2 text-fg-3 italic'
              : active
                ? 'bg-brand text-brand-fg'
                : 'bg-bg-2 text-fg-1',
          )}
        >
          {empty ? 'sắp có' : entry.count}
        </span>
      </button>
    </li>
  );
}
