import { Link } from 'react-router-dom';
import type { ArticleSummary } from '../types';
import { formatCrawledAt } from '../lib/format';

export function ArticleCard({ article }: { article: ArticleSummary }) {
  return (
    <Link
      to={`/article/${article.id}`}
      className="block rounded-lg border border-gray-200 p-4 hover:border-gray-400 hover:shadow-sm transition no-underline"
    >
      <div className="flex items-center justify-between mb-3 text-xs text-gray-500">
        <span className="font-semibold rounded bg-blue-100 text-blue-800 px-2 py-0.5">
          {article.ticker}
        </span>
        <span>
          {article.word_count} từ · 🕐 {formatCrawledAt(article.crawled_at)}
        </span>
      </div>
      <h3 className="text-base font-semibold text-gray-900 leading-snug mt-0">
        {article.title}
      </h3>
    </Link>
  );
}
