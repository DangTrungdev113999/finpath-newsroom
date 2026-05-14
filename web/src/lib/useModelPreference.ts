import { useCallback, useEffect, useState } from 'react';

import type { ArticleModel } from '../components/ModelToggle';

const STORAGE_KEY = 'article.model';
const CHANGE_EVENT = 'article-model:change';
const DEFAULT_MODEL: ArticleModel = 'gemini';

function readStoredModel(): ArticleModel {
  if (typeof window === 'undefined') return DEFAULT_MODEL;
  const raw = window.localStorage.getItem(STORAGE_KEY);
  return raw === 'claude' || raw === 'gemini' || raw === 'grok'
    ? raw
    : DEFAULT_MODEL;
}

/**
 * App-wide model preference (Claude / Gemini). Backed by localStorage so the
 * choice survives navigation between list ↔ detail and a full reload. Default
 * is Gemini — list cards + detail page both honor it when the article has a
 * Gemini side; cards/detail fall back to Claude automatically when not.
 *
 * Same-window sync: setModel dispatches a custom `article-model:change` event,
 * every mounted hook instance subscribes to it. Without this, the `storage`
 * event alone would only fire in OTHER tabs — so clicking the toggle on
 * IndexPage would update its own local state but leave each ArticleCard's
 * independent hook stale until next navigation.
 *
 * Cross-tab sync: `storage` event handles propagation across browser tabs.
 */
export function useModelPreference(): {
  model: ArticleModel;
  setModel: (next: ArticleModel) => void;
} {
  const [model, setModelState] = useState<ArticleModel>(() => readStoredModel());

  useEffect(() => {
    const sync = () => setModelState(readStoredModel());
    const onStorage = (e: StorageEvent) => {
      if (e.key === STORAGE_KEY) sync();
    };
    window.addEventListener(CHANGE_EVENT, sync);
    window.addEventListener('storage', onStorage);
    return () => {
      window.removeEventListener(CHANGE_EVENT, sync);
      window.removeEventListener('storage', onStorage);
    };
  }, []);

  const setModel = useCallback((next: ArticleModel) => {
    window.localStorage.setItem(STORAGE_KEY, next);
    window.dispatchEvent(new Event(CHANGE_EVENT));
  }, []);

  return { model, setModel };
}
