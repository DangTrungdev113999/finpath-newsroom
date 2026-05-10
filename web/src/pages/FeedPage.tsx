import { useEffect, useRef, useState } from 'react';
import { CompareFeedLayout } from '../components/CompareFeedLayout';
import { loadManifest, loadArticle } from '../lib/articleLoader';
import type { Article, ArticleSummary } from '../types';

const PAGE_SIZE = 5;

export function FeedPage() {
  const [manifest, setManifest] = useState<ArticleSummary[]>([]);
  const [loaded, setLoaded] = useState<Article[]>([]);
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);
  const [error, setError] = useState<string | null>(null);
  const [showRight, setShowRight] = useState(true);
  const sentinelRef = useRef<HTMLDivElement>(null);

  // Load manifest on mount (already sorted desc by crawled_at in loader)
  useEffect(() => {
    loadManifest()
      .then((list) => setManifest(list))
      .catch((e: Error) => setError(`Lỗi load manifest: ${e.message}`));
  }, []);

  // Load articles up to visibleCount
  useEffect(() => {
    const toLoad = manifest.slice(loaded.length, visibleCount);
    if (toLoad.length === 0) return;

    Promise.all(toLoad.map((entry) => loadArticle(entry.id)))
      .then((newArticles) => {
        setLoaded((prev) => [...prev, ...newArticles]);
      })
      .catch((e: Error) => setError(`Lỗi load bài: ${e.message}`));
  }, [manifest, visibleCount, loaded.length]);

  // IntersectionObserver — trigger load more when sentinel enters viewport
  useEffect(() => {
    if (!sentinelRef.current) return;
    if (visibleCount >= manifest.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          setVisibleCount((c) => Math.min(c + PAGE_SIZE, manifest.length));
        }
      },
      { rootMargin: '200px' },
    );
    observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [manifest.length, visibleCount]);

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
      <div className="mb-8 flex items-end justify-between gap-4">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.22em] text-fg-3 mb-1.5">
            Feed
          </p>
          <h1 className="text-2xl font-semibold tracking-tight text-fg-0">
            {manifest.length} bài
          </h1>
        </div>
        <ViewToggle showRight={showRight} onChange={setShowRight} />
      </div>
      {loaded.map((article, idx) => (
        <article
          key={article.id}
          className={idx > 0 ? 'mt-12 border-t-4 border-fg-4/40 pt-12' : ''}
        >
          <CompareFeedLayout article={article} showRight={showRight} />
        </article>
      ))}
      {visibleCount < manifest.length && (
        <div ref={sentinelRef} className="py-8 text-center text-sm text-fg-3">
          Đang tải thêm...
        </div>
      )}
      {visibleCount >= manifest.length && loaded.length === manifest.length && (
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
      className="inline-flex items-center gap-0.5 rounded-pill border border-fg-4/40 bg-bg-2/60 p-0.5 font-sans text-[12px] font-medium"
    >
      <ToggleButton
        active={showRight}
        onClick={() => onChange(true)}
        label="Đầy đủ"
        title="Đọc bài + cột metadata bên cạnh"
      >
        <TwoPaneIcon />
      </ToggleButton>
      <ToggleButton
        active={!showRight}
        onClick={() => onChange(false)}
        label="Tập trung"
        title="Ẩn cột metadata để tập trung đọc"
      >
        <OnePaneIcon />
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
          ? 'bg-bg-1 text-fg-0 shadow-sm ring-1 ring-fg-4/40'
          : 'text-fg-2 hover:text-fg-0'
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
