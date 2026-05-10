import { useEffect, useState } from 'react';
import type { ArticleSummary } from '../types';
import { loadManifest } from '../lib/articleLoader';
import { ArticleCard } from '../components/ArticleCard';

export function IndexPage() {
  const [articles, setArticles] = useState<ArticleSummary[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

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

  return (
    <div className="max-w-7xl mx-auto px-6 py-10">
      <header className="mb-10 flex items-end justify-between gap-4">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.22em] text-fg-3 mb-2">
            Compare feed
          </p>
          <h1 className="text-3xl font-semibold tracking-tight text-fg-0">
            Newsroom
          </h1>
        </div>
        <p className="font-mono text-xs tabular-nums text-fg-3">
          {loading ? 'Loading…' : `${articles.length} bài`}
        </p>
      </header>

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

      <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
        {articles.map((a) => (
          <ArticleCard key={a.id} article={a} />
        ))}
      </div>
    </div>
  );
}
