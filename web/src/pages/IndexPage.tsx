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
    <div className="max-w-7xl mx-auto px-4 py-6">
      <header className="mb-6">
        <h1>📰 Newsroom Compare Feed</h1>
        <p className="text-sm text-gray-500 mt-2">
          {loading ? 'Loading…' : `${articles.length} bài`}
        </p>
      </header>

      {error && (
        <div className="rounded border border-red-200 bg-red-50 p-3 text-sm text-red-800">
          Lỗi load manifest: {error}
        </div>
      )}

      {!loading && !error && articles.length === 0 && (
        <p className="text-gray-500">
          Chưa có bài nào. Chạy pipeline (Phase 3+) để generate bài mới.
        </p>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {articles.map((a) => (
          <ArticleCard key={a.id} article={a} />
        ))}
      </div>
    </div>
  );
}
