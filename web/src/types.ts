export interface SourceMeta {
  name: string;
  url: string;
  published: string; // ISO date YYYY-MM-DD
  raw_title: string;
}

export interface LeftMeta {
  author: string;
  word_count: number;
  key_view: 'lạc quan' | 'thận trọng' | 'trung lập';
  skeptic_verdict: string;
  pipeline_version: string;
  format_check: string;
}

export interface WhyChosenItem {
  label: string;
  content: string;
}

export interface FunnelItem {
  source: string;
  url: string;
  published: string;
  reason: string;
}

export interface CrawlFunnelData {
  picked: FunnelItem[];
  rejected_editor_v1: FunnelItem[];
  rejected_story_editor: FunnelItem[];
  rejected_master: FunnelItem[];
}

export interface ArticleMeta {
  title: string;
  ticker: string;
  sector: string;
  sector_icon: string;
  crawled_at: string;
  funnel_batch_id: string;
  left_meta: LeftMeta;
  right_source: SourceMeta;
  insight: string;
  why_chosen: WhyChosenItem[];
  crawl_funnel: CrawlFunnelData;
  pipeline_log: Record<string, unknown>;
}

export interface Article {
  id: string;
  meta: ArticleMeta;
  leftMarkdown: string;
  rightMarkdown: string;
}

export interface ArticleSummary {
  id: string;
  ticker: string;
  sector: string;
  title: string;
  crawled_at: string;
  key_view: string;
  word_count: number;
}

export interface Manifest {
  articles: ArticleSummary[];
}
