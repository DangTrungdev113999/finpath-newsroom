import { Link } from 'react-router-dom';
import type { ArticleSummary } from '../types';
import { formatCrawledAt } from '../lib/format';
import { useModelPreference } from '../lib/useModelPreference';
import { MissingModelNotice } from './MissingModelNotice';
import { TickerHero } from './TickerHero';
import { cn } from '../shared/lib/cn';

export function ArticleCard({ article }: { article: ArticleSummary }) {
  const stamp = formatCrawledAt(article.crawled_at);
  const [datePart, timePart] = stamp.split(' '); // "11/05/2026" + "16:55"
  const { model } = useModelPreference();

  // NO silent fallback to Claude — when the selected side has no title we
  // surface the gap so the reader knows which model actually wrote (or didn't
  // write) what they are looking at.
  const grokMissing = model === 'grok' && !article.grok_title;
  const geminiMissing = model === 'gemini' && !article.gemini_title;
  const isMissing = grokMissing || geminiMissing;

  const displayTitle =
    model === 'grok' && article.grok_title
      ? article.grok_title
      : model === 'gemini' && article.gemini_title
        ? article.gemini_title
        : article.title;

  return (
    <Link
      to={`/article/${article.id}`}
      className={cn(
        'group relative flex flex-col overflow-hidden rounded-xl border bg-bg-1 no-underline transition-all duration-med ease-out-quart focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35',
        isMissing
          ? 'border-fg-4/30 hover:border-fg-3/40'
          : 'border-fg-4/40 hover:-translate-y-0.5 hover:border-brand/40 hover:shadow-md',
      )}
    >
      {!isMissing && (
        <span
          aria-hidden
          className="pointer-events-none absolute inset-x-5 top-0 h-px origin-left scale-x-0 bg-gradient-to-r from-brand via-brand/60 to-transparent transition-transform duration-med ease-out-quart group-hover:scale-x-100"
        />
      )}

      {article.thumb_url ? (
        <div
          className={cn(
            'relative aspect-video w-full overflow-hidden border-b border-fg-4/30 bg-fg-4/10',
            isMissing && 'opacity-50 saturate-50',
          )}
        >
          <img
            src={article.thumb_url}
            alt=""
            loading="lazy"
            className={cn(
              'h-full w-full object-cover transition-transform duration-slow ease-out-quart',
              !isMissing && 'group-hover:scale-[1.03]',
            )}
          />
        </div>
      ) : (
        <div className={cn(isMissing && 'opacity-55 saturate-[0.6]')}>
          <TickerHero ticker={article.ticker} sector={article.sector} />
        </div>
      )}

      <div className="flex flex-1 flex-col p-5">
        <div className="mb-5 flex items-center justify-between gap-3">
          <span
            className={cn(
              'rounded-md px-2.5 py-1 font-sans text-[12px] font-bold tracking-[0.02em]',
              isMissing
                ? 'bg-fg-3 text-bg-1'
                : 'bg-fg-0 text-bg-1',
            )}
          >
            {article.ticker}
          </span>
          {/* Byline timestamp — editorial "date · time" split, mono semibold */}
          <time
            dateTime={article.crawled_at}
            className="inline-flex items-baseline gap-1.5 font-mono tabular-nums"
          >
            <span className="text-[11px] font-semibold tracking-[0.02em] text-fg-1">
              {datePart}
            </span>
            <span aria-hidden className="text-fg-4">
              ·
            </span>
            <span className="text-[10.5px] tracking-[0.02em] text-fg-2">
              {timePart}
            </span>
          </time>
        </div>

        {isMissing ? (
          <MissingModelNotice slot="card-title" model={model} />
        ) : (
          <h3 className="mt-0 mb-5 flex-1 text-[15px] font-semibold leading-snug tracking-tight text-fg-0 transition-colors duration-med ease-out-quart group-hover:text-brand">
            {displayTitle}
          </h3>
        )}

        <div
          className={cn(
            'flex items-center justify-between border-t pt-3',
            isMissing ? 'border-fg-4/20' : 'border-fg-4/30',
          )}
        >
          {isMissing ? (
            <span className="font-mono text-[10px] font-medium uppercase tracking-[0.18em] text-fg-3">
              — chưa generate
            </span>
          ) : (
            // Word count — number emphasized, unit demoted to caption
            <span className="inline-flex items-baseline gap-1 font-mono tabular-nums">
              <span className="text-[12.5px] font-bold text-fg-1">
                {article.word_count}
              </span>
              <span className="text-[9.5px] font-medium uppercase tracking-[0.14em] text-fg-3">
                từ
              </span>
            </span>
          )}
          <span
            aria-hidden
            className={cn(
              'font-mono text-[12px] transition-all duration-med ease-out-quart',
              isMissing
                ? 'text-fg-4'
                : 'text-fg-3 group-hover:translate-x-0.5 group-hover:text-brand',
            )}
          >
            →
          </span>
        </div>
      </div>
    </Link>
  );
}
