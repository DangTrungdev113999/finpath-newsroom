import { useEffect, useMemo, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import type { Article, ArticleSummary } from '../types';
import { loadArticle } from '../lib/articleLoader';
import { extractOpening } from '../lib/extractOpening';
import { useModelPreference } from '../lib/useModelPreference';
import { MissingModelNotice } from './MissingModelNotice';
import { TickerHero } from './TickerHero';
import { cn } from '../shared/lib/cn';

export function ArticleCard({ article }: { article: ArticleSummary }) {
  const { model } = useModelPreference();

  // NO silent fallback to Claude — see MissingModelNotice for editorial copy
  // when the selected side has no title for this article.
  const grokMissing = model === 'grok' && !article.grok_title;
  const geminiMissing = model === 'gemini' && !article.gemini_title;
  const isMissing = grokMissing || geminiMissing;

  const displayTitle =
    model === 'grok' && article.grok_title
      ? article.grok_title
      : model === 'gemini' && article.gemini_title
        ? article.gemini_title
        : article.title;

  // Lazy-load full article body when the card scrolls into view so we can
  // surface a 3-line opening preview under the title. Skipped entirely for
  // missing-side cards (we have no body to preview anyway). The fetched
  // Article is cached in component state — subsequent model toggles
  // re-extract from cache without another network round-trip.
  const cardRef = useRef<HTMLAnchorElement>(null);
  const [full, setFull] = useState<Article | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    if (isMissing || full || failed) return;
    const el = cardRef.current;
    if (!el) return;
    const io = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          io.disconnect();
          loadArticle(article.id)
            .then(setFull)
            .catch(() => setFailed(true));
        }
      },
      { rootMargin: '300px 0px' },
    );
    io.observe(el);
    return () => io.disconnect();
  }, [article.id, isMissing, full, failed]);

  const opening = useMemo(() => {
    if (!full) return null;
    const grokBody = full.meta?.grok?.body;
    const geminiBody = full.meta?.gemini?.body;
    if (model === 'grok' && grokBody) return extractOpening(grokBody);
    if (model === 'gemini' && geminiBody) return extractOpening(geminiBody);
    return extractOpening(full.leftMarkdown ?? '');
  }, [full, model]);

  return (
    <Link
      ref={cardRef}
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
          <TickerHero
            ticker={article.ticker}
            sector={article.sector}
            crawledAt={article.crawled_at}
          />
        </div>
      )}

      <div className="flex flex-1 flex-col p-5">
        {isMissing ? (
          <MissingModelNotice slot="card-title" model={model} />
        ) : (
          <>
            <h3 className="mt-0 mb-3 flex-1 text-[15px] font-semibold leading-snug tracking-tight text-fg-0 transition-colors duration-med ease-out-quart group-hover:text-brand">
              {displayTitle}
            </h3>

            {/* 3-line opening preview — lazy-loaded after the card enters
                viewport, otherwise renders a shimmer placeholder so the card
                height stays stable between visible / loading states. */}
            {opening === null ? (
              <div className="mb-4 space-y-1.5">
                <div className="h-[13px] w-full rounded bg-bg-3/70 animate-pulse" />
                <div className="h-[13px] w-[94%] rounded bg-bg-3/70 animate-pulse" />
                <div className="h-[13px] w-[68%] rounded bg-bg-3/70 animate-pulse" />
              </div>
            ) : opening ? (
              <p className="mb-4 line-clamp-3 text-[13px] leading-[1.55] text-fg-2">
                {opening}
              </p>
            ) : null}
          </>
        )}

        <div
          className={cn(
            'mt-auto flex items-center justify-between border-t pt-3',
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
