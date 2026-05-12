import { useEffect, useMemo, useRef, useState } from 'react';
import { Skeleton } from 'boneyard-js/react';
import { CompareFeedLayout } from '../components/CompareFeedLayout';
import { loadManifest, loadArticle } from '../lib/articleLoader';
import type { Article, ArticleSummary } from '../types';
import { SymbolFilter, useSymbolFilter } from '../components/SymbolFilter';
import { AngleFilter, useAngleFilter } from '../components/AngleFilter';
import { FormatFilter, useFormatFilter } from '../components/FormatFilter';
import { CompareFeedSkeleton } from '../components/skeletons/CompareFeedSkeleton';

const PAGE_SIZE = 5;

export function FeedPage() {
  const [manifest, setManifest] = useState<ArticleSummary[]>([]);
  const [loaded, setLoaded] = useState<Article[]>([]);
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);
  const [error, setError] = useState<string | null>(null);
  const [showRight, setShowRight] = useState(false);
  const sentinelRef = useRef<HTMLDivElement>(null);
  const { selected, setSelected } = useSymbolFilter();
  const { selected: angleSelected, setSelected: setAngleSelected } =
    useAngleFilter();
  const { selected: formatSelected, setSelected: setFormatSelected } =
    useFormatFilter();

  // Load manifest on mount (already sorted desc by crawled_at in loader)
  useEffect(() => {
    loadManifest()
      .then((list) => setManifest(list))
      .catch((e: Error) => setError(`Lỗi load manifest: ${e.message}`));
  }, []);

  const filteredManifest = useMemo(() => {
    let result = manifest;
    if (selected.length > 0) {
      result = result.filter((a) => selected.includes(a.ticker));
    }
    if (formatSelected.length > 0) {
      result = result.filter(
        (a) => a.format_id && formatSelected.includes(a.format_id),
      );
    }
    if (angleSelected.length > 0) {
      result = result.filter(
        (a) => a.category && angleSelected.includes(a.category as never),
      );
    }
    return result;
  }, [manifest, selected, angleSelected, formatSelected]);

  // AngleFilter hide rule: ẩn khi user pin chỉ flash_qa (format không dùng
  // 5-category enum). Hiện khi không filter format hoặc filter format ∈ standard_*.
  const showAngleFilter = useMemo(() => {
    if (formatSelected.length === 1 && formatSelected[0] === 'flash_qa') {
      return false;
    }
    return true;
  }, [formatSelected]);

  const loadedById = useMemo(() => {
    const m = new Map<string, Article>();
    for (const a of loaded) m.set(a.id, a);
    return m;
  }, [loaded]);

  // Reset loaded + visibleCount when filter changes
  useEffect(() => {
    setLoaded([]);
    setVisibleCount(PAGE_SIZE);
  }, [selected, angleSelected, formatSelected]);

  // Auto-clear angleSelected khi user pin format flash_qa (Angle filter ẩn,
  // tránh state "ẩn nhưng vẫn filter" gây kết quả 0 bài khó hiểu)
  useEffect(() => {
    if (!showAngleFilter && angleSelected.length > 0) {
      setAngleSelected([]);
    }
  }, [showAngleFilter, angleSelected, setAngleSelected]);

  // Load articles up to visibleCount — lookup by id so we don't double-fetch
  // after filter resets and we don't depend on array index ordering.
  useEffect(() => {
    const toLoad = filteredManifest
      .slice(0, visibleCount)
      .filter((e) => !loadedById.has(e.id));
    if (toLoad.length === 0) return;

    Promise.all(toLoad.map((entry) => loadArticle(entry.id)))
      .then((newArticles) => {
        setLoaded((prev) => [...prev, ...newArticles]);
      })
      .catch((e: Error) => setError(`Lỗi load bài: ${e.message}`));
  }, [filteredManifest, visibleCount, loadedById]);

  // IntersectionObserver — trigger load more when sentinel enters viewport
  useEffect(() => {
    if (!sentinelRef.current) return;
    if (visibleCount >= filteredManifest.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          setVisibleCount((c) => Math.min(c + PAGE_SIZE, filteredManifest.length));
        }
      },
      { rootMargin: '200px' },
    );
    observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [filteredManifest.length, visibleCount]);

  if (error) {
    return (
      <main className="mx-auto max-w-7xl px-6 py-8">
        <div className="rounded-md border border-rec/40 bg-rec/10 p-4 text-rec">
          {error}
        </div>
      </main>
    );
  }

  if (manifest.length === 0) {
    return (
      <main className="mx-auto max-w-7xl px-6 py-8">
        <p className="text-fg-3">Đang tải feed...</p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-7xl px-6 py-8">
      <div className="mb-8 flex flex-wrap items-center justify-between gap-x-5 gap-y-3">
        <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
          <h1 className="text-2xl font-semibold tracking-tight text-fg-0">
            {selected.length === 0 &&
            angleSelected.length === 0 &&
            formatSelected.length === 0
              ? `${manifest.length} bài`
              : `${filteredManifest.length}/${manifest.length} bài`}
          </h1>
          {manifest.length > 0 && (
            <>
              <SymbolFilter
                items={manifest}
                selected={selected}
                onChange={setSelected}
              />
              <FormatFilter
                items={manifest}
                selected={formatSelected}
                onChange={setFormatSelected}
              />
              {showAngleFilter && (
                <AngleFilter
                  items={manifest}
                  selected={angleSelected}
                  onChange={setAngleSelected}
                />
              )}
            </>
          )}
        </div>
        <ViewToggle showRight={showRight} onChange={setShowRight} />
      </div>

      {filteredManifest.length === 0 ? (
        <p className="py-8 text-fg-3">Không có bài nào cho bộ lọc đã chọn.</p>
      ) : (
        filteredManifest.slice(0, visibleCount).map((entry, idx) => {
          const article = loadedById.get(entry.id);
          return (
            <div
              key={entry.id}
              className={idx > 0 ? 'mt-12 border-t-4 border-fg-4/40 pt-12' : ''}
            >
              <Skeleton
                name="compare-feed"
                loading={!article}
                fallback={<CompareFeedSkeleton showRight={showRight} />}
              >
                {article ? (
                  <CompareFeedLayout article={article} showRight={showRight} />
                ) : null}
              </Skeleton>
            </div>
          );
        })
      )}
      {visibleCount < filteredManifest.length && (
        <div ref={sentinelRef} aria-hidden className="h-1" />
      )}
      {filteredManifest.length > 0 &&
        visibleCount >= filteredManifest.length &&
        loadedById.size >= filteredManifest.length && (
          <div className="py-8 text-center text-sm text-fg-3">— Hết feed —</div>
        )}
    </main>
  );
}

function ViewToggle({
  showRight,
  onChange,
}: {
  showRight: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <div
      role="group"
      aria-label="Chế độ xem"
      className="inline-flex items-center gap-0.5 rounded-pill border border-brand/20 bg-bg-2/60 p-0.5 font-sans text-[12px] font-medium shadow-sm shadow-brand/5"
    >
      <ToggleButton
        active={!showRight}
        onClick={() => onChange(false)}
        label="Tập trung"
        title="Ẩn cột metadata để tập trung đọc"
      >
        <OnePaneIcon />
      </ToggleButton>
      <ToggleButton
        active={showRight}
        onClick={() => onChange(true)}
        label="Đầy đủ"
        title="Đọc bài + cột metadata bên cạnh"
      >
        <TwoPaneIcon />
      </ToggleButton>
    </div>
  );
}

function ToggleButton({
  active,
  onClick,
  label,
  title,
  children,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      title={title}
      className={`inline-flex items-center gap-1.5 rounded-pill px-3 py-1 transition-all duration-med ease-out-quart ${
        active
          ? 'bg-brand text-brand-fg shadow-sm shadow-brand/25 ring-1 ring-brand/40'
          : 'text-fg-2 hover:text-brand hover:bg-brand/5'
      }`}
    >
      {children}
      <span>{label}</span>
    </button>
  );
}

function TwoPaneIcon() {
  return (
    <svg
      viewBox="0 0 16 12"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.4"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-3 w-[16px] shrink-0"
      aria-hidden
    >
      <rect x="1" y="1" width="14" height="10" rx="1.4" />
      <line x1="8" y1="1.5" x2="8" y2="10.5" />
    </svg>
  );
}

function OnePaneIcon() {
  return (
    <svg
      viewBox="0 0 16 12"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.4"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-3 w-[16px] shrink-0"
      aria-hidden
    >
      <rect x="3" y="1" width="10" height="10" rx="1.4" />
    </svg>
  );
}
