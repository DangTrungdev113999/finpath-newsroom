import type { Article } from '../types';
import { LeftColumn } from './LeftColumn';
import { RightColumn } from './RightColumn';
import { formatCrawledAt } from '../lib/format';

export function CompareFeedLayout({ article }: { article: Article }) {
  const { meta, leftMarkdown } = article;
  return (
    <article className="max-w-7xl mx-auto px-4 py-6">
      <header>
        <h1 className="leading-tight">
          {meta.sector_icon} {meta.title}
        </h1>
        <p className="text-sm text-gray-500 italic mt-2">
          🕐 Crawled {formatCrawledAt(meta.crawled_at)} · Funnel batch: {meta.funnel_batch_id}
        </p>
      </header>

      <hr className="my-5 border-gray-200" />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-x-10 gap-y-6">
        <LeftColumn
          title={meta.title}
          meta={meta.left_meta}
          insight={meta.insight}
          body={leftMarkdown}
        />
        <RightColumn meta={meta} />
      </div>
    </article>
  );
}
