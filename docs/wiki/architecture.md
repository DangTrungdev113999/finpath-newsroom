# Architecture - Finpath Newsroom

## Overview

Finpath Newsroom V3.6 - Hệ thống tạo bài tin chuyên sâu về cổ phiếu Việt Nam (71 mã thuộc 4 sector: Bank/CK/BĐS/Oil-Gas).

## Tech Stack

- **Python 3.13+** - Core pipeline, libs, scripts
- **SQLite** - Pipeline database (`data/pipeline.db`)
- **React + Vite + Tailwind** - Web viewer (`web/`)
- **Cloudflare Workers** - Feedback worker (`worker/`)
- **Claude Code CLI** - LLM agents và skills

## Directory Structure

```
.
├── .claude/
│   ├── agents/           # 4 LLM agents (pipeline, editor, story-editor, master-*, skeptic)
│   ├── commands/         # /tin <TICKER> entry point
│   └── skills/           # 12 skill V3.6 (knowledge modules)
│
├── data/
│   ├── manual/           # Curated YAML (targets, credit_room, nhnn_circulars)
│   ├── pipeline.db       # SQLite (crawl_log + generated_news)
│   └── secrets.yaml      # API keys (gitignored)
│
├── docs/
│   ├── superpowers/      # Specs + Plans
│   │   ├── specs/        # Design specs
│   │   └── plans/        # Implementation plans
│   └── wiki/             # Project documentation
│
├── kb/                   # Markdown Knowledge Base
│   ├── bank/             # 27 mã ngân hàng
│   ├── ck/               # 30 mã chứng khoán
│   ├── bds/              # 4 mã BĐS dân cư
│   └── oil-gas/          # 10 mã dầu khí
│
├── lib/                  # Python helpers
│   ├── finpath_api.py    # Finpath API client
│   ├── pipeline_db.py    # SQLite operations
│   ├── kb_ingest.py      # KB ingestion
│   ├── kb_loader.py      # KB loading
│   ├── quality_gates.py  # 5 quality gates V4.0
│   ├── render_compare_feed.py  # Markdown rendering
│   └── stages/           # Pipeline stages
│       ├── run_crawler.py
│       ├── run_git_publish.py
│       └── run_pages_wait.py
│
├── output/
│   └── compare-feed/     # Generated articles + manifest.json
│
├── scripts/              # One-off scripts
│
├── tests/                # Pytest tests
│
├── web/                  # Vite + React viewer
│   └── src/
│       ├── components/   # React components
│       ├── pages/        # Page components
│       └── lib/          # Frontend helpers
│
└── worker/               # Cloudflare Workers
    └── feedback.ts       # Feedback collection
```

## Data Flow

```
User Input (/tin <TICKER>)
    │
    ▼
Orchestrator
    │
    ├──► Crawler ──► crawl_log (SQLite)
    │
    ├──► Editor V1 ──► Filter + Route
    │
    ├──► Story Editor ──► Brief generation
    │
    ├──► Master (Bank/CK/BĐS/Oil-Gas) ──► Article generation
    │
    ├──► Skeptic ──► Critique append
    │
    └──► Publish ──► output/compare-feed/*.md
```

## Pipeline Database Schema

```sql
-- crawl_log: Raw crawled articles
CREATE TABLE crawl_log (
    id INTEGER PRIMARY KEY,
    source_url TEXT UNIQUE,
    ticker TEXT,
    published_time TEXT,
    funnel_batch_id TEXT,
    editor_v1_decision TEXT,
    story_editor_decision TEXT
);

-- generated_news: Final articles
CREATE TABLE generated_news (
    id INTEGER PRIMARY KEY,
    public_slug TEXT UNIQUE,
    ticker TEXT,
    title TEXT,
    body TEXT,
    created_at TEXT
);
```

## 5 Quality Gates V4.0

1. **0% English words** - Kể cả viết tắt (NPL -> nợ xấu, NIM -> biên lãi vay)
2. **Word count 200-400** - Hard cap
3. **Body pattern** - 1 opening + 3-7 bullets + 1 closing
4. **Title-as-hook** - Chứa `?` hoặc `—` + tension word
5. **No metadata leak** - Không lộ internal enum/category

## Universe - 71 Mã

- **Bank (27)**: HOSE 16 + HNX 4 + UPCOM 7
- **CK (30)**: HOSE 5 + HNX 15 + UPCOM 10
- **BĐS (4)**: VHM, NVL, KDH, DXG
- **Oil-Gas (10)**: GAS, PVD, PVS, PVT, BSR, PLX, OIL, DPM, DCM, PVC

## Related Files

- Spec: `docs/superpowers/specs/2026-05-08-newsroom-cli-migration-design.md`
- CLAUDE.md: `/data/finpath/finpath-newsroom/CLAUDE.md`
