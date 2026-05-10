import { Link } from 'react-router-dom';
import type { ArticleSummary } from '../types';
import { formatCrawledAt } from '../lib/format';

export function ArticleCard({ article }: { article: ArticleSummary }) {
  return (
    <Link
      to={`/article/${article.id}`}
      className="group relative flex flex-col rounded-xl border border-fg-4/40 bg-bg-1 p-5 no-underline transition-all duration-med ease-out-quart hover:-translate-y-0.5 hover:border-brand/40 hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35"
    >
      <span
        aria-hidden
        className="pointer-events-none absolute inset-x-5 top-0 h-px origin-left scale-x-0 bg-gradient-to-r from-brand via-brand/60 to-transparent transition-transform duration-med ease-out-quart group-hover:scale-x-100"
      />

      <div className="mb-5 flex items-center justify-between">
        <span className="rounded-md bg-fg-0 px-2.5 py-1 font-sans text-[12px] font-bold tracking-[0.02em] text-bg-1">
          {article.ticker}
        </span>
        <time className="font-mono text-[10px] tabular-nums text-fg-3">
          {formatCrawledAt(article.crawled_at)}
        </time>
      </div>

      <h3 className="mt-0 mb-5 flex-1 text-[15px] font-semibold leading-snug tracking-tight text-fg-0 transition-colors duration-med ease-out-quart group-hover:text-brand">
        {article.title}
      </h3>

      <div className="flex items-center justify-between border-t border-fg-4/30 pt-3">
        <span className="font-mono text-[10px] tabular-nums text-fg-3">
          {article.word_count} từ
        </span>
        <span
          aria-hidden
          className="font-mono text-[11px] text-fg-3 transition-all duration-med ease-out-quart group-hover:translate-x-0.5 group-hover:text-brand"
        >
          →
        </span>
      </div>
    </Link>
  );
}
