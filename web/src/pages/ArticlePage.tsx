import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import type { Article } from '../types';
import { loadArticle } from '../lib/articleLoader';
import { CompareFeedLayout } from '../components/CompareFeedLayout';

export function ArticlePage() {
  const { id } = useParams<{ id: string }>();
  const [article, setArticle] = useState<Article | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    setArticle(null);
    setError(null);
    loadArticle(id)
      .then(setArticle)
      .catch((e: Error) => setError(e.message));
  }, [id]);

  return (
    <div>
      <nav className="max-w-7xl mx-auto px-4 pt-4">
        <Link to="/" className="text-sm">
          ← Quay lại danh sách
        </Link>
      </nav>
      {error && (
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="rounded border border-red-200 bg-red-50 p-3 text-sm text-red-800">
            Lỗi load bài: {error}
          </div>
        </div>
      )}
      {!article && !error && (
        <p className="max-w-7xl mx-auto px-4 py-6 text-gray-500">Loading…</p>
      )}
      {article && <CompareFeedLayout article={article} />}
    </div>
  );
}
