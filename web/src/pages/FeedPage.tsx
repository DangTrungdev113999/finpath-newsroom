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
        <div className="rounded-md border border-red-300 bg-red-50 p-4 text-red-700">
          {error}
        </div>
      </main>
    );
  }

  if (manifest.length === 0) {
    return (
      <main className="mx-auto max-w-7xl px-6 py-8">
        <p className="text-gray-500">Đang tải feed...</p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-7xl px-6 py-8">
      <h1 className="mb-6 text-xl font-semibold text-gray-900">
        Feed — {manifest.length} bài
      </h1>
      {loaded.map((article, idx) => (
        <article
          key={article.id}
          className={idx > 0 ? 'mt-12 border-t-4 border-gray-200 pt-12' : ''}
        >
          <CompareFeedLayout article={article} />
        </article>
      ))}
      {visibleCount < manifest.length && (
        <div ref={sentinelRef} className="py-8 text-center text-sm text-gray-400">
          Đang tải thêm...
        </div>
      )}
      {visibleCount >= manifest.length && loaded.length === manifest.length && (
        <div className="py-8 text-center text-sm text-gray-400">— Hết feed —</div>
      )}
    </main>
  );
}
