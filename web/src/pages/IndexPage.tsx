import { useEffect, useMemo, useRef, useState } from 'react';
import { Skeleton } from 'boneyard-js/react';
import { ChevronDown, Loader2 } from 'lucide-react';
import type { ArticleSummary } from '../types';
import { loadManifest } from '../lib/articleLoader';
import { ArticleCard } from '../components/ArticleCard';
import { SymbolFilter, useSymbolFilter } from '../components/SymbolFilter';
import { AngleFilter, useAngleFilter } from '../components/AngleFilter';
import { ModelToggle } from '../components/ModelToggle';
import { ArticleCardSkeleton } from '../components/skeletons/ArticleCardSkeleton';
import { useModelPreference } from '../lib/useModelPreference';

const INITIAL_SKELETON_COUNT = 6;
const PAGE_SIZE = 12; // bài mỗi lần load thêm

export function IndexPage() {
  const [articles, setArticles] = useState<ArticleSummary[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);
  const sentinelRef = useRef<HTMLDivElement | null>(null);
  const { selected, setSelected } = useSymbolFilter();
  const { selected: angleSelected, setSelected: setAngleSelected } =
    useAngleFilter();
  const { model, setModel } = useModelPreference();
  const geminiAvailable = useMemo(
    () => articles.some((a) => !!a.gemini_title),
    [articles],
  );
  const grokAvailable = useMemo(
    () => articles.some((a) => !!a.grok_title),
    [articles],
  );

  useEffect(() => {
    loadManifest()
      .then((list) => {
        setArticles(list);
        setLoading(false);
      })
      .catch((e: Error) => {
        setError(e.message);
        setLoading(false);
      });
  }, []);

  const filteredArticles = useMemo(() => {
    let result = articles;
    if (selected.length > 0) {
      result = result.filter((a) => selected.includes(a.ticker));
    }
    if (angleSelected.length > 0) {
      result = result.filter(
        (a) => a.category && angleSelected.includes(a.category as never),
      );
    }
    return result;
  }, [articles, selected, angleSelected]);

  // Reset paging window mỗi khi filter đổi — tránh tình trạng filter narrow xuống vài bài
  // nhưng visibleCount đang giữ giá trị cũ to gây render thừa.
  useEffect(() => {
    setVisibleCount(PAGE_SIZE);
  }, [selected, angleSelected]);

  const visibleArticles = useMemo(
    () => filteredArticles.slice(0, visibleCount),
    [filteredArticles, visibleCount],
  );
  const hasMore = visibleCount < filteredArticles.length;
  const remaining = filteredArticles.length - visibleCount;

  // Auto-load thêm khi sentinel chạm viewport — UX mượt, không bắt user click mỗi lần
  useEffect(() => {
    if (!hasMore || loading) return;
    const el = sentinelRef.current;
    if (!el) return;
    const io = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          setVisibleCount((c) => Math.min(c + PAGE_SIZE, filteredArticles.length));
        }
      },
      { rootMargin: '400px 0px' }, // pre-trigger trước khi user thật sự thấy
    );
    io.observe(el);
    return () => io.disconnect();
  }, [hasMore, loading, filteredArticles.length]);

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="mb-8 flex flex-wrap items-center gap-x-4 gap-y-2">
        <h1 className="text-2xl font-semibold tracking-tight text-fg-0">
          {loading
            ? ' '
            : selected.length === 0 && angleSelected.length === 0
              ? `${articles.length} bài`
              : `${filteredArticles.length}/${articles.length} bài`}
        </h1>
        {articles.length > 0 && (
          <>
            <SymbolFilter
              items={articles}
              selected={selected}
              onChange={setSelected}
            />
            <AngleFilter
              items={articles}
              selected={angleSelected}
              onChange={setAngleSelected}
            />
            <ModelToggle
              selected={model}
              onChange={setModel}
              geminiAvailable={geminiAvailable}
              grokAvailable={grokAvailable}
              labelMode="always"
            />
          </>
        )}
      </div>

      {error && (
        <div className="mb-6 rounded-lg border border-rec/40 bg-rec/10 p-3 text-sm text-rec">
          Lỗi load manifest: {error}
        </div>
      )}

      {!loading && !error && articles.length === 0 && (
        <p className="text-fg-3">
          Chưa có bài nào. Chạy pipeline (Phase 3+) để generate bài mới.
        </p>
      )}

      {!loading && !error && articles.length > 0 && filteredArticles.length === 0 && (
        <p className="text-fg-3">
          Không có bài nào cho mã đã chọn.
        </p>
      )}

      <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
        {loading
          ? Array.from({ length: INITIAL_SKELETON_COUNT }).map((_, i) => (
              <Skeleton
                key={`sk-${i}`}
                name="article-card"
                loading={true}
                fallback={<ArticleCardSkeleton />}
              >
                <ArticleCardSkeleton />
              </Skeleton>
            ))
          : visibleArticles.map((a) => (
              <ArticleCard key={a.id} article={a} />
            ))}
      </div>

      {/* Load-more zone — sentinel auto-trigger + explicit button fallback */}
      {!loading && !error && hasMore && (
        <div
          ref={sentinelRef}
          className="mt-10 flex flex-col items-center gap-3"
        >
          <button
            type="button"
            onClick={() =>
              setVisibleCount((c) =>
                Math.min(c + PAGE_SIZE, filteredArticles.length),
              )
            }
            className="group inline-flex items-center gap-2 rounded-full border border-fg-4/40 bg-bg-1 px-5 py-2 font-sans text-[13px] font-medium text-fg-1 transition-all duration-fast ease-out-quart hover:-translate-y-px hover:border-brand/50 hover:bg-bg-2 hover:text-fg-0 hover:shadow-[0_8px_20px_-12px_hsl(var(--brand)/0.5)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35"
          >
            <Loader2
              size={14}
              strokeWidth={2}
              className="text-fg-3 transition-colors duration-fast group-hover:text-brand"
              aria-hidden
            />
            <span>Xem thêm</span>
            <span className="font-mono text-[11px] tabular-nums text-fg-3">
              +{Math.min(PAGE_SIZE, remaining)}
            </span>
            <ChevronDown
              size={13}
              strokeWidth={2.25}
              className="text-fg-3 transition-transform duration-fast group-hover:translate-y-0.5 group-hover:text-brand"
              aria-hidden
            />
          </button>
          <p className="font-mono text-[11px] tabular-nums text-fg-3">
            Đang hiện{' '}
            <span className="text-fg-1">{visibleArticles.length}</span> /{' '}
            <span className="text-fg-1">{filteredArticles.length}</span> bài
          </p>
        </div>
      )}

      {/* Tail marker — đã load hết */}
      {!loading && !error && !hasMore && filteredArticles.length > PAGE_SIZE && (
        <div className="mt-10 flex items-center justify-center gap-3">
          <span aria-hidden className="h-px w-12 bg-fg-4/40" />
          <p className="font-mono text-[11px] uppercase tracking-[0.18em] text-fg-3">
            Đã hết · {filteredArticles.length} bài
          </p>
          <span aria-hidden className="h-px w-12 bg-fg-4/40" />
        </div>
      )}
    </div>
  );
}
