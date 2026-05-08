import { Link } from 'react-router-dom';
import type { ArticleSummary } from '../types';
import { formatCrawledAt, keyViewBadgeClass } from '../lib/format';

export function ArticleCard({ article }: { article: ArticleSummary }) {
  return (
    <Link
      to={`/article/${article.id}`}
      className="block rounded-lg border border-gray-200 p-4 hover:border-gray-400 hover:shadow-sm transition no-underline"
    >
      <div className="flex items-center gap-2 mb-2">
        <span className="text-xs font-semibold rounded bg-blue-100 text-blue-800 px-2 py-0.5">
          {article.ticker}
        </span>
        <span
          className={`text-xs rounded px-2 py-0.5 ${keyViewBadgeClass(article.key_view)}`}
        >
          {article.key_view}
        </span>
        <span className="text-xs text-gray-500 ml-auto">{article.word_count} từ</span>
      </div>
      <h3 className="text-base font-semibold text-gray-900 leading-snug mb-2 mt-0">
        {article.title}
      </h3>
      <p className="text-xs text-gray-500 m-0">
        🕐 {formatCrawledAt(article.crawled_at)}
      </p>
    </Link>
  );
}
