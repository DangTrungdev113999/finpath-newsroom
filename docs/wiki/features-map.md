# Features Map

Auto-generated feature index. Run `bash .claude/skills/guide/scripts/scan-all.sh` to refresh.

## Lib Modules (`lib/`)

| Module | Description |
|--------|-------------|
| `backfill_manifest_category` | Backfill `category` (5 deep_question categories) into manifest entries. |
| `finpath_api` | Finpath API wrapper — public Bank endpoints. |
| `kb_bds_validator` | KB BĐS validator — enforces 5 hard rules per design spec 2026-05-11. |
| `kb_ingest` | KB ingest — convert Notion Bank Sector page tree (JSON dump) to markdown files |
| `kb_loader` | KB runtime loader — read kb/bank/ markdown files (no Notion calls). |
| `notion_fetch` | Notion MCP helpers — block tree → markdown conversion. |
| `pipeline_db` | SQLite ops cho pipeline state — crawl_log + generated_news. |
| `quality_gates` | 5 quality gates V4.0 — mechanical pass/fail checker for Master Bank articles. |
| `render_compare_feed` | Render V4.0 — multi-article + 8-section right column for Compare Feed. |
| `slugify` | Slugify Vietnamese hook titles to URL-safe slugs (max 60 chars). |
| `telegram_publisher` | Telegram Bot API publisher (Phase G T12 + T14b). |

## Pipeline Stages (`lib/stages/`)

| Stage | Description |
|-------|-------------|
| `run_crawler` | Crawler stage — Step 1 of pipeline. |
| `run_git_publish` | Auto git publish with self-heal for common errors. |
| `run_pages_wait` | Poll GitHub Actions API until Pages deploy workflow completes. |

## Workers (`worker/`)

| Worker | Description |
|--------|-------------|
| `feedback.ts` |  worker/feedback.ts |

## Knowledge Base Domains (`kb/`)

| Domain | Files | Description |
|--------|-------|-------------|
| `bank` | 4 files | 27 mã ngân hàng (Big4 + tư nhân + hợp tác xã) |
| `bds` | 21 files | BĐS dân cư (VHM/NVL/KDH/DXG) |
| `ck` | 6 files | 30 mã chứng khoán (HOSE/HNX/UPCOM) |
| `oil-gas` | 1 files | 10 mã dầu khí + phân bón |

