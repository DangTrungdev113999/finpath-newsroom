import yaml from 'js-yaml';
import type { Article, ArticleMeta, FunnelItem } from '../types';

const LEFT_MARKER = '<!-- left -->';
const RIGHT_MARKER = '<!-- right -->';
const FRONTMATTER_RE = /^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/;

type LegacyFunnel = {
  picked?: FunnelItem[];
  rejected?: FunnelItem[];
  rejected_editor_v1?: FunnelItem[];
  rejected_story_editor?: FunnelItem[];
  rejected_master?: FunnelItem[];
  total_candidates?: number;
};

function normalizeCrawlFunnel(funnel: LegacyFunnel | undefined) {
  if (!funnel) return funnel;
  const picked = funnel.picked ?? [];
  const tagAgent = (items: FunnelItem[] | undefined, agent: FunnelItem['reject_agent']): FunnelItem[] =>
    (items ?? []).map((it) => ({ ...it, reject_agent: it.reject_agent ?? agent }));
  const rejected =
    funnel.rejected ?? [
      ...tagAgent(funnel.rejected_editor_v1, 'editor_v1'),
      ...tagAgent(funnel.rejected_story_editor, 'story_editor'),
      ...tagAgent(funnel.rejected_master, 'master'),
    ];
  const total_candidates = funnel.total_candidates ?? picked.length + rejected.length;
  return { picked, rejected, total_candidates };
}

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

  if (data?.crawl_funnel) {
    data.crawl_funnel = normalizeCrawlFunnel(data.crawl_funnel as LegacyFunnel)!;
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
