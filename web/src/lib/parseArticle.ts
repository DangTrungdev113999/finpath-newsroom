import matter from 'gray-matter';
import type { Article, ArticleMeta } from '../types';

const LEFT_MARKER = '<!-- left -->';
const RIGHT_MARKER = '<!-- right -->';

export function parseArticle(id: string, raw: string): Article {
  const { data, content } = matter(raw);

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
    meta: data as ArticleMeta,
    leftMarkdown,
    rightMarkdown,
  };
}
