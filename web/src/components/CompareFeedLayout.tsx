import type { Article } from '../types';
import { LeftColumn } from './LeftColumn';
import { RightColumn } from './RightColumn';
import { formatCrawledAt } from '../lib/format';

export function CompareFeedLayout({
  article,
  showRight = true,
}: {
  article: Article;
  showRight?: boolean;
}) {
  const { meta, leftMarkdown } = article;
  return (
    <article className="max-w-7xl mx-auto px-4 py-6">
      <header className={showRight ? '' : 'max-w-3xl mx-auto'}>
        <h1 className="leading-tight">
          {meta.sector_icon} {meta.title}
        </h1>
        <p className="text-sm text-fg-3 italic mt-2">
          🕐 Crawled {formatCrawledAt(meta.crawled_at)} · Funnel batch: {meta.funnel_batch_id}
        </p>
      </header>

      <hr className={`my-5 border-fg-4/40 ${showRight ? '' : 'max-w-3xl mx-auto'}`} />

      {showRight ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-6">
          <LeftColumn meta={meta.left_meta} body={leftMarkdown} />
          <RightColumn meta={meta} />
        </div>
      ) : (
        <div className="max-w-3xl mx-auto">
          <LeftColumn meta={meta.left_meta} body={leftMarkdown} />
        </div>
      )}
    </article>
  );
}
