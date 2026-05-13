import { useState } from 'react';
import { Link } from 'react-router-dom';
import type { Article } from '../types';
import { LeftColumn } from './LeftColumn';
import { RightColumn } from './RightColumn';
import { CommentSection } from './CommentSection';
import { TTSButton } from './TTSButton';
import { ModelToggle, type ArticleModel } from './ModelToggle';
import { formatCrawledAt } from '../lib/format';

export function CompareFeedLayout({
  article,
  showRight = true,
}: {
  article: Article;
  showRight?: boolean;
}) {
  const { meta, leftMarkdown } = article;
  const [model, setModel] = useState<ArticleModel>('claude');
  const geminiAvailable = !!(meta.gemini?.title && meta.gemini?.body);
  const showGemini = model === 'gemini' && geminiAvailable;
  const displayTitle = showGemini ? meta.gemini!.title : meta.title;
  const displayBody = showGemini ? meta.gemini!.body : leftMarkdown;
  const displayLeftMeta = showGemini
    ? {
        ...meta.left_meta,
        author: meta.gemini?.model ? `Gemini · ${meta.gemini.model}` : 'Gemini',
        word_count: meta.gemini?.word_count ?? meta.left_meta.word_count,
        // Skeptic critique is Claude-side only — clear verdict marker in Gemini view
        skeptic_verdict: '',
      }
    : meta.left_meta;

  return (
    <article className="max-w-7xl mx-auto px-4 py-6">
      <header className={showRight ? '' : 'max-w-3xl mx-auto'}>
        <h1 className="leading-tight">
          {meta.sector_icon} {displayTitle}
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
          <div className="flex items-center gap-3">
            <ModelToggle
              selected={model}
              onChange={setModel}
              geminiAvailable={geminiAvailable}
            />
            <TTSButton text={displayBody} />
          </div>
        </div>
      </header>

      <hr className={`my-5 border-fg-4/40 ${showRight ? '' : 'max-w-3xl mx-auto'}`} />

      {showRight ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-6">
          <LeftColumn meta={displayLeftMeta} body={displayBody} />
          <RightColumn meta={meta} />
        </div>
      ) : (
        <div className="max-w-3xl mx-auto">
          <LeftColumn meta={displayLeftMeta} body={displayBody} />
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
