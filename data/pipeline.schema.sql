-- Pipeline DB schema (Phase G+ requires WAL mode — see lib/pipeline_db.py:__init__)
-- Backup process MUST include all 3 files: pipeline.db + pipeline.db-wal + pipeline.db-shm
-- Finpath Newsroom Pipeline State Schema
-- Version: V3.6
-- Tables: crawl_log + generated_news

CREATE TABLE IF NOT EXISTS crawl_log (
  row_id              TEXT PRIMARY KEY,
  funnel_batch_id     TEXT NOT NULL,
  ticker              TEXT NOT NULL,
  source_name         TEXT NOT NULL,
  source_url          TEXT NOT NULL,
  title               TEXT NOT NULL,
  raw_content         TEXT,
  published_time      TEXT,
  crawled_at          TEXT NOT NULL,
  detected_tickers    TEXT,
  primary_ticker      TEXT,
  sector              TEXT,
  editor_v1_decision  TEXT,
  editor_v1_note      TEXT,
  story_editor_decision TEXT,
  story_editor_note   TEXT,
  brief_json          TEXT,
  master_decision     TEXT,
  master_note         TEXT,
  status              TEXT NOT NULL DEFAULT 'pending',
  pipeline_version    TEXT NOT NULL DEFAULT 'V3.6',
  pipeline_log        TEXT,
  notes               TEXT
);

CREATE INDEX IF NOT EXISTS idx_crawl_log_funnel ON crawl_log(funnel_batch_id);
CREATE INDEX IF NOT EXISTS idx_crawl_log_ticker_status ON crawl_log(ticker, status);
CREATE UNIQUE INDEX IF NOT EXISTS idx_crawl_log_url ON crawl_log(source_url);

CREATE TABLE IF NOT EXISTS generated_news (
  article_id          TEXT PRIMARY KEY,
  row_id              TEXT NOT NULL,
  ticker              TEXT NOT NULL,
  sector              TEXT NOT NULL,
  title               TEXT NOT NULL,
  body                TEXT NOT NULL,
  word_count          INTEGER,
  key_view            TEXT,
  insight_final       TEXT,
  insight_type        TEXT,
  variety_guard_angle TEXT,
  accepted_hypothesis INTEGER NOT NULL,
  data_sources_used   TEXT,
  brief_json          TEXT,
  history_referenced  TEXT,
  skeptic_critique    TEXT,
  skeptic_angle       TEXT,
  skeptic_verdict     TEXT,
  status              TEXT NOT NULL DEFAULT 'draft',
  published_at        TEXT,
  pipeline_version    TEXT NOT NULL DEFAULT 'V3.6',
  pipeline_log        TEXT,
  public_slug         TEXT,
  telegram_pushed_at  TIMESTAMP NULL,
  -- Step 4.3 Gemini Writer (parallel to Claude Master): success/skipped_failure/skipped_disabled
  gemini_title        TEXT,
  gemini_body         TEXT,
  gemini_word_count   INTEGER,
  gemini_model        TEXT,
  gemini_generated_at TIMESTAMP NULL,
  gemini_status       TEXT,
  gemini_error        TEXT,
  -- Step 4.4 Grok Writer (xAI, parallel to Gemini): same status enum
  grok_title          TEXT,
  grok_body           TEXT,
  grok_word_count     INTEGER,
  grok_model          TEXT,
  grok_generated_at   TIMESTAMP NULL,
  grok_status         TEXT,
  grok_error          TEXT,
  FOREIGN KEY (row_id) REFERENCES crawl_log(row_id)
);

CREATE INDEX IF NOT EXISTS idx_generated_ticker_published ON generated_news(ticker, published_at DESC);
CREATE UNIQUE INDEX IF NOT EXISTS idx_generated_public_slug ON generated_news(public_slug);
-- Phase G T11 — Telegram publish idempotency tracking
CREATE INDEX IF NOT EXISTS idx_generated_telegram_pushed ON generated_news(telegram_pushed_at);
