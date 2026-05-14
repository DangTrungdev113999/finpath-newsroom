import { useState } from 'react';
import { Link } from 'react-router-dom';
import type { Article } from '../types';
import { LeftColumn } from './LeftColumn';
import { RightColumn } from './RightColumn';
import { CommentSection } from './CommentSection';
import { TTSButton } from './TTSButton';
import { ModelToggle, type ArticleModel } from './ModelToggle';
import { formatCrawledAt } from '../lib/format';
import { useModelPreference } from '../lib/useModelPreference';

export function CompareFeedLayout({
  article,
  showRight = true,
  modelScope = 'global',
}: {
  article: Article;
  showRight?: boolean;
  /** 'global' (default) — Model toggle reads/writes the app-wide preference
   *  via useModelPreference (article cards + ArticlePage stay in sync).
   *  'local'  — each layout instance owns its own state, seeded from the
   *  current global preference on mount. Used by FeedPage so toggling on one
   *  article does not change every other article in the feed. */
  modelScope?: 'global' | 'local';
}) {
  const { meta, leftMarkdown } = article;
  const geminiAvailable = !!(meta.gemini?.title && meta.gemini?.body);
  const grokAvailable = !!(meta.grok?.title && meta.grok?.body);

  // Always read the global hook so 'local' mode can seed its useState from
  // the current global value on mount (without subscribing further).
  const globalPref = useModelPreference();
  const [localModel, setLocalModel] = useState<ArticleModel>(globalPref.model);
  const model = modelScope === 'local' ? localModel : globalPref.model;
  const setModel = modelScope === 'local' ? setLocalModel : globalPref.setModel;
  const showGemini = model === 'gemini' && geminiAvailable;
  const showGrok = model === 'grok' && grokAvailable;
  const displayTitle = showGrok
    ? meta.grok!.title
    : showGemini
      ? meta.gemini!.title
      : meta.title;
  const displayBody = showGrok
    ? meta.grok!.body
    : showGemini
      ? meta.gemini!.body
      : leftMarkdown;
  const displayLeftMeta = showGrok
    ? {
        ...meta.left_meta,
        author: meta.grok?.model ? `Grok · ${meta.grok.model}` : 'Grok',
        word_count: meta.grok?.word_count ?? meta.left_meta.word_count,
        // Skeptic critique is Claude-side only — clear verdict marker in Grok view
        skeptic_verdict: '',
      }
    : showGemini
      ? {
          ...meta.left_meta,
          author: meta.gemini?.model
            ? `Gemini · ${meta.gemini.model}`
            : 'Gemini',
          word_count: meta.gemini?.word_count ?? meta.left_meta.word_count,
          skeptic_verdict: '',
        }
      : meta.left_meta;

  return (
    <article className="max-w-7xl mx-auto px-4 py-6">
      <header className={showRight ? '' : 'max-w-3xl mx-auto'}>
        <h1 className="leading-tight">
          {meta.sector_icon} {displayTitle}
        </h1>
        <div className="mt-2 flex flex-col gap-2 sm:flex-row sm:flex-wrap sm:items-center sm:justify-between sm:gap-x-4">
          <p className="!m-0 min-w-0 text-sm italic text-fg-3 sm:flex-1">
            🕐 Crawled {formatCrawledAt(meta.crawled_at)}
            <span className="hidden sm:inline">
              {' '}·{' '}
              <Link
                to={`/pipeline-runs?batch_id=${meta.funnel_batch_id}`}
                className="whitespace-nowrap text-brand hover:underline"
              >
                {meta.funnel_batch_id}
              </Link>
            </span>
          </p>
          <div className="flex items-center gap-3">
            <ModelToggle
              selected={model}
              onChange={setModel}
              geminiAvailable={geminiAvailable}
              grokAvailable={grokAvailable}
              labelMode="hover"
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
