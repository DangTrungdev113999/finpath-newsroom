import { useEffect, useMemo, useState } from 'react';
import { Skeleton } from 'boneyard-js/react';
import type { ArticleSummary } from '../types';
import { loadManifest } from '../lib/articleLoader';
import { ArticleCard } from '../components/ArticleCard';
import { SymbolFilter, useSymbolFilter } from '../components/SymbolFilter';
import { ArticleCardSkeleton } from '../components/skeletons/ArticleCardSkeleton';

const INITIAL_SKELETON_COUNT = 6;

export function IndexPage() {
  const [articles, setArticles] = useState<ArticleSummary[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const { selected, setSelected } = useSymbolFilter();

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

  const filteredArticles = useMemo(
    () =>
      selected.length === 0
        ? articles
        : articles.filter((a) => selected.includes(a.ticker)),
    [articles, selected],
  );

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="mb-8 flex flex-wrap items-center gap-x-4 gap-y-2">
        <h1 className="text-2xl font-semibold tracking-tight text-fg-0">
          {loading
            ? ' '
            : selected.length === 0
              ? `${articles.length} bài`
              : `${filteredArticles.length}/${articles.length} bài`}
        </h1>
        {articles.length > 0 && (
          <SymbolFilter
            items={articles}
            selected={selected}
            onChange={setSelected}
          />
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
          : filteredArticles.map((a) => (
              <ArticleCard key={a.id} article={a} />
            ))}
      </div>
    </div>
  );
}
