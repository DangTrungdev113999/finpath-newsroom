import type { Article, ArticleSummary, Manifest } from '../types';
import { parseArticle } from './parseArticle';

const ARTICLES_BASE = '/articles';

export async function loadManifest(): Promise<ArticleSummary[]> {
  const res = await fetch(`${ARTICLES_BASE}/manifest.json`, { cache: 'no-store' });
  if (!res.ok) {
    throw new Error(`Manifest fetch failed: ${res.status}`);
  }
  const data = (await res.json()) as Manifest;
  return [...data.articles].sort((a, b) =>
    b.crawled_at.localeCompare(a.crawled_at),
  );
}

export async function loadArticle(id: string): Promise<Article> {
  const res = await fetch(`${ARTICLES_BASE}/${id}.md`, { cache: 'no-store' });
  if (!res.ok) {
    throw new Error(`Article ${id} fetch failed: ${res.status}`);
  }
  const raw = await res.text();
  return parseArticle(id, raw);
}
