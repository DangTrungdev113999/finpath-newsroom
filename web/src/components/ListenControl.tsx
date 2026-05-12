import { useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { ChevronDown, Headphones, Play, Square, SkipForward } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '../shared/ui/dropdown-menu';
import { cn } from '../shared/lib/cn';
import { EqualizerBars } from './EqualizerBars';
import type { ListenState } from '../lib/useArticleListener';

/**
 * Cửa sổ thời gian + nút nghe đọc TTS. URL ?w=today|1h|2h|3h|6h|12h|24h.
 * 'all' = đọc toàn bộ feed (không khuyến nghị — dài).
 * Time window vừa filter feed visual vừa quyết định queue đọc.
 */

export type TimeWindow = 'all' | 'today' | '1h' | '2h' | '3h' | '6h' | '12h' | '24h';

const OPTIONS: ReadonlyArray<{ id: TimeWindow; label: string; short: string }> = [
  { id: 'today', label: 'Hôm nay', short: 'hôm nay' },
  { id: '1h', label: '1 giờ qua', short: '1 giờ qua' },
  { id: '2h', label: '2 giờ qua', short: '2 giờ qua' },
  { id: '3h', label: '3 giờ qua', short: '3 giờ qua' },
  { id: '6h', label: '6 giờ qua', short: '6 giờ qua' },
  { id: '12h', label: '12 giờ qua', short: '12 giờ qua' },
  { id: '24h', label: '24 giờ qua', short: '24 giờ qua' },
];

const VALID = new Set<TimeWindow>(OPTIONS.map((o) => o.id));

export function useTimeWindowFilter() {
  const [params, setParams] = useSearchParams();
  const raw = params.get('w');
  const selected: TimeWindow = useMemo(
    () => (raw && VALID.has(raw as TimeWindow) ? (raw as TimeWindow) : 'today'),
    [raw],
  );

  const setSelected = (next: TimeWindow) => {
    const newParams = new URLSearchParams(params);
    if (next === 'today') newParams.delete('w');
    else newParams.set('w', next);
    setParams(newParams, { replace: true });
  };

  return { selected, setSelected };
}

function vnTodayStartMs(): number {
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Ho_Chi_Minh',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).formatToParts(new Date());
  const get = (t: string) => parts.find((p) => p.type === t)!.value;
  return Date.parse(`${get('year')}-${get('month')}-${get('day')}T00:00:00+07:00`);
}

export function filterByTimeWindow<T extends { crawled_at: string }>(
  items: T[],
  window: TimeWindow,
): T[] {
  if (window === 'all') return items;
  const now = Date.now();
  let cutoff: number;
  if (window === 'today') {
    cutoff = vnTodayStartMs();
  } else {
    const hours = parseInt(window, 10);
    cutoff = now - hours * 60 * 60 * 1000;
  }
  return items.filter((a) => {
    const t = Date.parse(a.crawled_at);
    return Number.isFinite(t) && t >= cutoff;
  });
}

interface Props {
  window: TimeWindow;
  onChangeWindow: (v: TimeWindow) => void;
  filteredCount: number;
  state: ListenState;
  currentIdx: number;
  total: number;
  supported: boolean;
  onPlay: () => void;
  onPause: () => void;
  onStop: () => void;
  onNext: () => void;
}

export function ListenControl({
  window,
  onChangeWindow,
  filteredCount,
  state,
  currentIdx,
  total,
  supported,
  onPlay,
  onPause,
  onStop,
  onNext,
}: Props) {
  const [open, setOpen] = useState(false);
  const opt = OPTIONS.find((o) => o.id === window) ?? OPTIONS[0];
  const isPlaying = state === 'playing';
  const isPaused = state === 'paused';
  const isActive = isPlaying || isPaused;

  const canPlay = supported && filteredCount > 0 && state === 'idle';
  const handleMainAction = () => {
    if (!supported) return;
    if (isPlaying) onPause();
    else if (isPaused) onPlay();
    else if (canPlay) onPlay();
  };

  let title: string;
  if (!supported) title = 'Trình duyệt không hỗ trợ đọc TTS';
  else if (isPlaying) title = `Đang đọc bài ${currentIdx + 1}/${total} — click để tạm dừng`;
  else if (isPaused) title = `Tạm dừng ${currentIdx + 1}/${total} — click để tiếp tục`;
  else if (filteredCount === 0) title = 'Không có bài để đọc với cửa sổ này';
  else title = `Đọc ${filteredCount} bài ${opt.short}`;

  return (
    <div
      className={cn(
        'inline-flex items-center rounded-pill border transition-all duration-300',
        isActive
          ? 'border-brand/60 bg-brand/10 shadow-[0_2px_0_rgba(0,0,0,0.02),0_10px_24px_-12px_hsl(var(--brand)/0.45)]'
          : 'border-fg-4/50 bg-bg-2',
        !supported && 'opacity-50',
      )}
    >
      {/* Main play / pause action */}
      <button
        type="button"
        onClick={handleMainAction}
        disabled={!supported || (state === 'idle' && filteredCount === 0)}
        title={title}
        aria-label={title}
        className={cn(
          'group inline-flex h-9 items-center gap-2.5 rounded-pill pl-3.5 pr-2.5 font-sans text-[13px] transition-colors',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35',
          isActive
            ? 'text-fg-0 hover:bg-brand/15'
            : 'text-fg-0 hover:bg-bg-3',
          'disabled:cursor-not-allowed disabled:opacity-50',
        )}
      >
        {/* State icon — left side of pill */}
        {isPlaying ? (
          <EqualizerBars active />
        ) : isPaused ? (
          <Play
            className="h-3.5 w-3.5 shrink-0 text-brand"
            strokeWidth={2}
            fill="currentColor"
            aria-hidden
          />
        ) : (
          <Headphones
            className={cn(
              'h-4 w-4 shrink-0 transition-colors',
              filteredCount === 0
                ? 'text-fg-3'
                : 'text-brand group-hover:scale-110',
            )}
            strokeWidth={1.85}
            aria-hidden
          />
        )}

        {isActive ? (
          <span className="inline-flex items-baseline gap-1.5 font-semibold">
            <span className="font-mono tabular-nums text-brand">
              {String(currentIdx + 1).padStart(2, '0')}
              <span className="text-fg-3/70">/</span>
              <span className="text-fg-2">{String(total).padStart(2, '0')}</span>
            </span>
            <span className="text-fg-3" aria-hidden>
              ·
            </span>
            <span className="font-medium text-fg-1">{opt.short}</span>
          </span>
        ) : (
          <span className="inline-flex items-baseline gap-1.5">
            <span className="font-semibold text-fg-0">Nghe</span>
            <span
              className={cn(
                'font-mono text-[14px] font-bold tabular-nums',
                filteredCount === 0 ? 'text-fg-3' : 'text-brand',
              )}
            >
              {filteredCount}
            </span>
            <span className="font-medium text-fg-1">bài</span>
            <span className="font-medium italic text-fg-2">{opt.short}</span>
          </span>
        )}
      </button>

      {/* Skip + Stop buttons while playing/paused */}
      {isActive && (
        <>
          <span className="h-5 w-px bg-fg-4/40" aria-hidden />
          <button
            type="button"
            onClick={onNext}
            title="Bài tiếp theo"
            aria-label="Bài tiếp theo"
            className="inline-flex h-9 w-8 items-center justify-center text-fg-2 transition-colors hover:text-brand focus-visible:outline-none"
          >
            <SkipForward className="h-3.5 w-3.5" strokeWidth={2} aria-hidden />
          </button>
          <button
            type="button"
            onClick={onStop}
            title="Dừng đọc"
            aria-label="Dừng đọc"
            className="inline-flex h-9 w-8 items-center justify-center text-fg-2 transition-colors hover:text-rec focus-visible:outline-none"
          >
            <Square className="h-3 w-3" strokeWidth={2} fill="currentColor" aria-hidden />
          </button>
        </>
      )}

      {/* Window setting dropdown — disabled while playing to avoid mid-read change */}
      <span className="h-4 w-px bg-fg-4/40" aria-hidden />
      <DropdownMenu open={open} onOpenChange={setOpen}>
        <DropdownMenuTrigger
          disabled={isActive}
          title={isActive ? 'Đang đọc — dừng để đổi cửa sổ' : 'Đổi cửa sổ thời gian'}
          className={cn(
            'group inline-flex h-9 items-center gap-1 rounded-r-pill pl-1.5 pr-2.5 text-fg-2 transition-colors',
            'hover:text-brand focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35',
            'disabled:cursor-not-allowed disabled:opacity-50',
          )}
          aria-label="Đổi cửa sổ thời gian"
        >
          <ChevronDown
            className="h-3 w-3 shrink-0 transition-transform duration-fast group-data-[state=open]:rotate-180"
            strokeWidth={2}
            aria-hidden
          />
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" side="bottom" sideOffset={6} className="w-[220px] p-0">
          <div className="px-3 pb-1.5 pt-2.5">
            <DropdownMenuLabel className="!p-0 text-fg-2">
              Đọc bài trong cửa sổ
            </DropdownMenuLabel>
          </div>
          <DropdownMenuSeparator className="mx-2 my-1" />
          <DropdownMenuRadioGroup
            value={window}
            onValueChange={(v) => onChangeWindow(v as TimeWindow)}
          >
            <div className="space-y-0.5 px-1 pb-2">
              {OPTIONS.map((o) => (
                <DropdownMenuRadioItem
                  key={o.id}
                  value={o.id}
                  className="text-[12.5px] text-fg-1"
                >
                  {o.label}
                </DropdownMenuRadioItem>
              ))}
            </div>
          </DropdownMenuRadioGroup>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}

