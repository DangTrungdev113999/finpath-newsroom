import yaml from 'js-yaml';
import type { Article, ArticleMeta } from '../types';

const LEFT_MARKER = '<!-- left -->';
const RIGHT_MARKER = '<!-- right -->';
const FRONTMATTER_RE = /^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/;

export function parseArticle(id: string, raw: string): Article {
  const match = raw.match(FRONTMATTER_RE);
  if (!match) {
    throw new Error(`Article ${id}: missing frontmatter (--- ... ---)`);
  }
  const [, frontmatterText, content] = match;

  let data: ArticleMeta;
  try {
    data = yaml.load(frontmatterText) as ArticleMeta;
  } catch (e) {
    throw new Error(`Article ${id}: invalid YAML frontmatter — ${(e as Error).message}`);
  }

  const leftIdx = content.indexOf(LEFT_MARKER);
  const rightIdx = content.indexOf(RIGHT_MARKER);

  if (leftIdx === -1) {
    throw new Error(`Article ${id}: missing <!-- left --> marker`);
  }
  if (rightIdx === -1) {
    throw new Error(`Article ${id}: missing <!-- right --> marker`);
  }

  const leftMarkdown = content.slice(leftIdx + LEFT_MARKER.length, rightIdx).trim();
  const rightMarkdown = content.slice(rightIdx + RIGHT_MARKER.length).trim();

  return {
    id,
    meta: data,
    leftMarkdown,
    rightMarkdown,
  };
}
