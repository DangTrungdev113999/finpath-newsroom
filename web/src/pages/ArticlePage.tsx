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
        <Link
          to="/"
          aria-label="Quay lại danh sách bài viết"
          className="group/back inline-flex items-center gap-2 rounded-pill border border-fg-4/40 bg-bg-1/70 px-3 py-1.5 font-sans text-[12px] font-medium text-fg-2 no-underline backdrop-blur transition-all duration-med ease-out-quart hover:-translate-y-px hover:border-brand/45 hover:bg-bg-2 hover:text-brand hover:shadow-[0_4px_14px_-6px_hsl(var(--brand)/0.45)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35"
        >
          <svg
            viewBox="0 0 16 16"
            aria-hidden
            className="h-3 w-3 shrink-0 transition-transform duration-med ease-out-quart group-hover/back:-translate-x-1"
          >
            <path
              d="M9.75 3 L4.5 8 L9.75 13"
              stroke="currentColor"
              strokeWidth="1.7"
              strokeLinecap="round"
              strokeLinejoin="round"
              fill="none"
            />
          </svg>
          <span className="tracking-[0.01em]">Quay lại danh sách</span>
          <span
            aria-hidden
            className="font-mono text-[10px] tracking-[0.18em] text-fg-3 transition-colors duration-med ease-out-quart group-hover/back:text-brand/70"
          >
            ↩
          </span>
        </Link>
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
      {article && <CompareFeedLayout article={article} />}
    </div>
  );
}
