import { useState } from 'react';
import { Link } from 'react-router-dom';
import type { Article } from '../types';
import { LeftColumn } from './LeftColumn';
import { RightColumn } from './RightColumn';
import { CommentSection } from './CommentSection';
import { TTSButton } from './TTSButton';
import { ModelToggle, type ArticleModel } from './ModelToggle';
import { MissingModelNotice } from './MissingModelNotice';
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
  // V5.1.9 — Claude side is only available on legacy articles where the
  // primary `title`/`body` fields came from Claude Master (not from a
  // promoted-to-primary Gemini/Grok output). Heuristic: when both parallel
  // sides are present AND the primary title equals one of them, no Claude.
  // Simpler: read meta.left_meta.author — Master sets a sector-specific
  // author string; if author starts with "Gemini" or "Grok" then primary
  // is a parallel writer, no Claude side exists.
  const authorPrefix = (meta.left_meta?.author || '').toLowerCase();
  const claudeAvailable = !authorPrefix.startsWith('gemini') && !authorPrefix.startsWith('grok');

  // Always read the global hook so 'local' mode can seed its useState from
  // the current global value on mount (without subscribing further).
  const globalPref = useModelPreference();
  const [localModel, setLocalModel] = useState<ArticleModel>(globalPref.model);
  const model = modelScope === 'local' ? localModel : globalPref.model;
  const setModel = modelScope === 'local' ? setLocalModel : globalPref.setModel;
  const showGemini = model === 'gemini' && geminiAvailable;
  const showGrok = model === 'grok' && grokAvailable;
  // NO silent fallback: when the user picked a side that didn't run for this
  // article, render an editorial "missing" notice instead of Claude's text.
  const isMissing =
    (model === 'gemini' && !geminiAvailable) ||
    (model === 'grok' && !grokAvailable);
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
        {isMissing ? (
          <MissingModelNotice slot="article-title" model={model} />
        ) : (
          <h1 className="leading-tight">{displayTitle}</h1>
        )}
        <div className="mt-2 flex flex-col gap-2 sm:flex-row sm:flex-wrap sm:items-center sm:justify-between sm:gap-x-4">
          <p className="!m-0 min-w-0 text-sm italic text-fg-3 sm:flex-1">
            {formatCrawledAt(meta.crawled_at)}
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
              claudeAvailable={claudeAvailable}
              labelMode="hover"
            />
            {!isMissing && <TTSButton text={displayBody} />}
          </div>
        </div>
      </header>

      {/* V5.1.8 — Imagen 4 hero thumb (1024×576). Renders only when
          /tin --image was used AND Imagen succeeded. Falls back to nothing
          (no broken layout) on older articles. */}
      {meta.thumb_url && (
        <figure
          className={`mt-4 mb-2 overflow-hidden rounded-lg border border-fg-4/30 bg-fg-4/10 aspect-video ${
            showRight ? '' : 'max-w-3xl mx-auto'
          }`}
        >
          <img
            src={meta.thumb_url}
            alt=""
            loading="lazy"
            className="h-full w-full object-cover"
          />
        </figure>
      )}

      <hr className={`my-5 border-fg-4/40 ${showRight ? '' : 'max-w-3xl mx-auto'}`} />

      {isMissing ? (
        showRight ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-6">
            <MissingModelNotice
              slot="article-body"
              model={model}
              ticker={meta.ticker}
            />
            <RightColumn meta={meta} />
          </div>
        ) : (
          <div className="max-w-3xl mx-auto">
            <MissingModelNotice
              slot="article-body"
              model={model}
              ticker={meta.ticker}
            />
          </div>
        )
      ) : showRight ? (
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
