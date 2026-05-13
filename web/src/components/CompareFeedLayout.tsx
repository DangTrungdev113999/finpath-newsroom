import { Link } from 'react-router-dom';
import type { Article } from '../types';
import { LeftColumn } from './LeftColumn';
import { RightColumn } from './RightColumn';
import { CommentSection } from './CommentSection';
import { TTSButton } from './TTSButton';
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
        <div className="mt-2 flex flex-wrap items-center justify-between gap-x-4 gap-y-2">
          <p className="!m-0 hidden min-w-0 flex-1 text-sm italic text-fg-3 sm:block">
            🕐 Crawled {formatCrawledAt(meta.crawled_at)} · Funnel batch:{' '}
            <Link
              to={`/pipeline-runs?batch_id=${meta.funnel_batch_id}`}
              className="whitespace-nowrap text-brand hover:underline"
            >
              {meta.funnel_batch_id}
            </Link>
          </p>
          <TTSButton text={leftMarkdown} />
        </div>
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

      {/* Phase H2 — comment feedback (article.id == public_slug per CLAUDE.md) */}
      <div className={showRight ? '' : 'max-w-3xl mx-auto'}>
        <CommentSection
          articleId={article.id}
          articleTitle={meta.title}
          ticker={meta.ticker ?? ''}
        />
      </div>
    </article>
  );
}
