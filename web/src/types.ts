export interface SourceMeta {
  name: string;
  url: string;
  published: string;
  raw_title: string;
}

export interface LeftMeta {
  author: string;
  word_count: number;
  key_view: 'lạc quan' | 'thận trọng' | 'trung lập';
  skeptic_verdict: string;
  pipeline_version: string;
}

export interface DeepQuestionOption {
  question: string;
  category: string;
  pick_hint: string;
}

export interface FunnelItem {
  source: string;
  url: string;
  published: string;
  reason: string;
  reject_agent?: 'editor_v1' | 'story_editor' | 'master';
  reject_label?: string;
}

export interface CrawlFunnelData {
  picked: FunnelItem[];
  rejected: FunnelItem[];
  total_candidates: number;
}

export interface DataTrailEntry {
  source: string;             // Canonical: Full URL | WebSearch:"query" | Finpath_API/<endpoint> | KB/<path> | Manual_YAML/<file>:<row_key> | "Lập luận tự"
  fetched: string;            // What was retrieved
  purpose?: string;           // V4.0 Phase F: vì sao tra (e.g. "kiểm chéo claim ROE Q1")
  supports_argument?: string; // V4.0 Phase F: bổ sung cho ("Bullet 2 (luận điểm chính)", "Opening (tension)")
  used_for?: string;          // LEGACY (pre-Phase F): backward compat — old entries have this; render maps to supports_argument
}

export interface ArticleMeta {
  title: string;
  ticker: string;
  sector: string;
  sector_icon: string;
  crawled_at: string;
  funnel_batch_id: string;
  left_meta: LeftMeta;
  insight: string;
  // V4.0 right-column 8 sections
  right_source: SourceMeta;
  why_chosen_narrative: string;
  angle_label: string;
  angle_narrative: string;
  deep_question_options: DeepQuestionOption[];
  chosen_question_idx: number;
  chosen_pick_reason: string;
  skip_reasons: Record<string, string>;
  crawl_funnel: CrawlFunnelData;
  master_data_trail: DataTrailEntry[];
  skeptic_data_trail: DataTrailEntry[];
  raw_article_url: string;
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
