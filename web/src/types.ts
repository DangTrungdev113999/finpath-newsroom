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

export interface StepLog {
  model: string;
  started_at?: string;
  duration_ms: number;
  tokens: number | null;
  // step-specific extras (optional, varies by step)
  candidates_count?: number;
  rows_processed?: number;
  briefs_count?: number;
  files_written?: number;
  // step_4_master / step_5_skeptic extras
  data_trail?: DataTrailEntry[];
  gates_passed?: boolean;
  angle?: string;
  // allow other step-specific keys without typing each one
  [extra: string]: unknown;
}

export interface PipelineLog {
  step_1_crawler?: StepLog;
  step_2_editor?: StepLog;
  step_3_story_editor?: StepLog;
  step_4_master?: StepLog;
  step_5_skeptic?: StepLog;
  step_6_render?: StepLog;
  // Phase H1 — race fix
  step_7_git_publish?: {
    ok: boolean;
    commit_sha?: string;
    duration_ms: number;
    self_heal_actions?: string[];
    error?: string;
    stage?: string;
  };
  step_8_pages_wait?: {
    ok: boolean;
    elapsed_s: number;
    workflow_run_url?: string;
    error?: string;
    run_url?: string;
    fallback?: string;
  };
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
  // Phase F T11 — observability per pipeline step
  pipeline_log?: PipelineLog;
}

export interface Article {
  id: string;
  meta: ArticleMeta;
  leftMarkdown: string;
  rightMarkdown: string;
}

export type FormatId =
  | 'flash_qa'
  | 'standard_qa'
  | 'standard_listicle'
  | 'standard_narrative';

export interface ArticleSummary {
  id: string;
  ticker: string;
  sector: string;
  title: string;
  crawled_at: string;
  key_view: string;
  word_count: number;
  /** One of 5 deep_question categories (Story Editor). Optional for back-compat. */
  category?: string;
  /** V5.1 article format (Format Director step 3.5). Optional for back-compat —
   *  pre-V5.1 articles backfilled as standard_listicle in render_compare_feed.py. */
  format_id?: FormatId;
}

export interface Manifest {
  articles: ArticleSummary[];
}
