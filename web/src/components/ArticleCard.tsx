import { useEffect, useMemo, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import type { Article, ArticleSummary } from '../types';
import { loadArticle } from '../lib/articleLoader';
import { extractOpening } from '../lib/extractOpening';
import { useModelPreference } from '../lib/useModelPreference';
import { TickerHero } from './TickerHero';

export function ArticleCard({ article }: { article: ArticleSummary }) {
  const { model } = useModelPreference();

  // Silent fallback chain: user preference → other available side → Claude
  // default (always present). When user has Gemini selected but the article
  // only has Grok / Claude, surface the existing one instead of a "missing"
  // notice — readers care about content, not which AI wrote it.
  const displayTitle =
    model === 'grok'
      ? article.grok_title ?? article.gemini_title ?? article.title
      : model === 'gemini'
        ? article.gemini_title ?? article.grok_title ?? article.title
        : article.title;

  // Lazy-load full article body when the card scrolls into view so we can
  // surface a 3-line opening preview under the title. The fetched Article
  // is cached in component state — subsequent model toggles re-extract from
  // cache without another network round-trip.
  const cardRef = useRef<HTMLAnchorElement>(null);
  const [full, setFull] = useState<Article | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    if (full || failed) return;
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
  }, [article.id, full, failed]);

  const opening = useMemo(() => {
    if (!full) return null;
    const claudeBody = full.leftMarkdown ?? '';
    const grokBody = full.meta?.grok?.body ?? '';
    const geminiBody = full.meta?.gemini?.body ?? '';
    // Same fallback chain as title — keep card title + preview in sync.
    if (model === 'grok')
      return extractOpening(grokBody || geminiBody || claudeBody);
    if (model === 'gemini')
      return extractOpening(geminiBody || grokBody || claudeBody);
    return extractOpening(claudeBody);
  }, [full, model]);

  return (
    <Link
      ref={cardRef}
      to={`/article/${article.id}`}
      className="group relative flex flex-col overflow-hidden rounded-xl border border-fg-4/40 bg-bg-1 no-underline transition-all duration-med ease-out-quart hover:-translate-y-0.5 hover:border-brand/40 hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35"
    >
      <span
        aria-hidden
        className="pointer-events-none absolute inset-x-5 top-0 h-px origin-left scale-x-0 bg-gradient-to-r from-brand via-brand/60 to-transparent transition-transform duration-med ease-out-quart group-hover:scale-x-100"
      />

      {article.thumb_url ? (
        <div className="relative aspect-video w-full overflow-hidden border-b border-fg-4/30 bg-fg-4/10">
          <img
            src={article.thumb_url}
            alt=""
            loading="lazy"
            className="h-full w-full object-cover transition-transform duration-slow ease-out-quart group-hover:scale-[1.03]"
          />
        </div>
      ) : (
        <TickerHero
          ticker={article.ticker}
          sector={article.sector}
          crawledAt={article.crawled_at}
        />
      )}

      <div className="flex flex-1 flex-col p-5">
        <h3 className="mt-0 mb-3 flex-1 text-[15px] font-semibold leading-snug tracking-tight text-fg-0 transition-colors duration-med ease-out-quart group-hover:text-brand">
          {displayTitle}
        </h3>

        {/* 3-line opening preview — lazy-loaded after the card enters
            viewport, otherwise renders a shimmer placeholder so the card
            height stays stable between visible / loading states. */}
        {opening === null ? (
          <div className="space-y-1.5">
            <div className="h-[13px] w-full rounded bg-bg-3/70 animate-pulse" />
            <div className="h-[13px] w-[94%] rounded bg-bg-3/70 animate-pulse" />
            <div className="h-[13px] w-[68%] rounded bg-bg-3/70 animate-pulse" />
          </div>
        ) : opening ? (
          <p className="m-0 line-clamp-3 text-[13px] leading-[1.55] text-fg-2">
            {opening}
          </p>
        ) : null}
      </div>
    </Link>
  );
}
