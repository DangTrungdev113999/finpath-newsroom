import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import type { Article } from '../types';
import { loadArticle } from '../lib/articleLoader';
import { CompareFeedLayout } from '../components/CompareFeedLayout';
import { BackToListLink } from '../components/BackToListLink';
import { ViewToggle } from '../components/ViewToggle';

export function ArticlePage() {
  const { id } = useParams<{ id: string }>();
  const [article, setArticle] = useState<Article | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showRight, setShowRight] = useState(false);

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
      <nav className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3 px-4 pt-4">
        <BackToListLink />
        <ViewToggle showRight={showRight} onChange={setShowRight} />
      </nav>
      {error && (
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="rounded border border-rec/40 bg-rec/10 p-3 text-sm text-rec">
            Lỗi load bài: {error}
          </div>
        </div>
      )}
      {!article && !error && (
        <p className="max-w-7xl mx-auto px-4 py-6 text-fg-3">Loading…</p>
      )}
      {article && <CompareFeedLayout article={article} showRight={showRight} />}
    </div>
  );
}
