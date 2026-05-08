# Phase 3 — Pipeline Mechanical Implementation Plan

> **For agentic workers:** Execute via superpowers:subagent-driven-development. Steps use `- [ ]`.

**Goal:** Wire the mechanical pipeline pieces — copy 8 skills to `.claude/skills/`, port crawler logic, build markdown renderer, slash command + main pipeline agent. End-to-end skeleton: `/tin VCB` runs Crawler + writes SQLite + renders empty article placeholder.

**Architecture:** 8 skills extracted from `.skill` zips to `.claude/skills/` (plain dirs). `lib/stages/run_crawler.py` does web search + fetch + dedupe + SQLite write (single file inline-port from skill scripts/). `lib/render_compare_feed.py` reads SQLite + generated_news → writes `output/compare-feed/<id>.md` + appends manifest.json. `.claude/commands/tin.md` slash command invokes `newsroom-pipeline` agent which orchestrates Bash → Python scripts + Task → subagents (Phase 4 will add LLM agents; Phase 3 only mechanical glue).

**Tech Stack:** Python 3.13 + Bash, Claude Code commands/agents/skills.

**Spec ref:** Section 3.3 (pipeline mapping), Section 7 (skills/agents/commands), Phase 3 build order.

**Project root:** `/Users/trungdt/Desktop/Stream Intelligent/`

---

## File Structure

### Created
```
.claude/
├── commands/tin.md
├── agents/newsroom-pipeline.md
└── skills/                          # 8 unzipped skills
    ├── finpath-newsroom-orchestrator/SKILL.md + references/
    ├── finpath-newsroom-crawler/SKILL.md + scripts/
    ├── finpath-newsroom-editor/SKILL.md + scripts/
    ├── finpath-newsroom-story-editor/SKILL.md + references/
    ├── finpath-newsroom-master-bank/SKILL.md + references/
    ├── finpath-newsroom-master-ck/SKILL.md + references/
    ├── finpath-newsroom-master-bds/SKILL.md + references/
    └── finpath-newsroom-skeptic/SKILL.md + references/
lib/stages/__init__.py
lib/stages/run_crawler.py            # Step 1
lib/render_compare_feed.py           # Step 6 — render markdown
tests/test_render_compare_feed.py
```

---

## Tasks

### Task 1: Unzip 8 skills to .claude/skills/

- [ ] **Step 1: Run unzip loop**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && mkdir -p .claude/skills
for f in /Users/trungdt/Desktop/finpath-newsroom-*.skill; do
  name=$(basename "$f" .skill)
  unzip -o -q "$f" -d /tmp/skill-extract-tmp
  # Each .skill zip contains a top-level <name>/ folder
  if [ -d "/tmp/skill-extract-tmp/$name" ]; then
    rm -rf ".claude/skills/$name"
    mv "/tmp/skill-extract-tmp/$name" ".claude/skills/$name"
  fi
  rm -rf /tmp/skill-extract-tmp
done
ls .claude/skills/
```

Expected: 8 directories, each with SKILL.md.

- [ ] **Step 2: Verify integrity**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && for skill in .claude/skills/finpath-newsroom-*; do
  name=$(basename "$skill")
  has_skill_md="❌ no SKILL.md"
  has_refs="❌ no refs"
  if [ -f "$skill/SKILL.md" ]; then has_skill_md="✅"; fi
  if [ -d "$skill/references" ]; then has_refs="✅ refs/"; fi
  echo "$name → $has_skill_md $has_refs"
done
```

Expected: 8 lines, all SKILL.md ✅. 6/8 should have refs (orchestrator, story-editor, master-bank/ck/bds, skeptic).

- [ ] **Step 3: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/skills/ && git commit -m "feat(skills): unzip 8 V3.6 skills to .claude/skills/ (plain dirs)"
```

---

### Task 2: lib/stages/run_crawler.py

- [ ] **Step 1: Write `lib/stages/__init__.py`**

```bash
mkdir -p "/Users/trungdt/Desktop/Stream Intelligent/lib/stages"
touch "/Users/trungdt/Desktop/Stream Intelligent/lib/stages/__init__.py"
```

- [ ] **Step 2: Write `lib/stages/run_crawler.py`**

Inline-port 3 helpers from skill `finpath-newsroom-crawler/scripts/`. Single file. Note: the actual web search + web fetch happens IN A CLAUDE SESSION (which has WebSearch + WebFetch tools). This Python script handles ONLY the SQLite writes + dedupe + funnel_batch_id + URL validation. The search/fetch results are passed via stdin or a JSON file.

```python
"""Crawler stage — Step 1 of pipeline.

Mode A (script-driven): accept JSON of pre-fetched candidates from stdin/file,
                        dedupe + write to SQLite crawl_log.

Mode B (interactive Claude): Claude calls WebSearch + WebFetch, builds the JSON
                             list, then invokes this script.

This script does NOT make HTTP calls itself (no WebSearch in plain Python).
"""
from __future__ import annotations
import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Universe constants (Bank MVP)
BANK_UNIVERSE = ["TCB", "VCB", "MBB", "ACB", "BID", "CTG", "VPB"]

# Whitelist 20 Vietnamese financial news sources
SOURCES_WHITELIST = {
    "CafeF": "cafef.vn",
    "VnEconomy": "vneconomy.vn",
    "Vietstock": "vietstock.vn",
    "Báo Pháp luật": "doanhnhan.baophapluat.vn",
    "Tin nhanh chứng khoán": "tinnhanhchungkhoan.vn",
    "VnExpress": "vnexpress.net",
    "Báo Đầu tư": "baodautu.vn",
    "Diễn đàn Doanh nghiệp": "diendandoanhnghiep.vn",
    "Nhịp sống Kinh tế": "nhipsongkinhdoanh.vn",
    "Thời báo Tài chính": "thoibaotaichinhvietnam.vn",
    "Người Lao động": "nld.com.vn",
    "Thanh Niên": "thanhnien.vn",
    "Tuổi Trẻ": "tuoitre.vn",
    "Lao Động": "laodong.vn",
    "Saigon Times": "saigontimes.vn",
    "VietnamNet": "vietnamnet.vn",
    "Báo Tin tức": "baotintuc.vn",
    "VietnamFinance": "vietnamfinance.vn",
    "Bizlive": "bizlive.vn",
    "Reatimes": "reatimes.vn",
}


def build_queries(ticker: str, sector: str = "Bank") -> list[str]:
    """Return list of search queries for a ticker."""
    company_name = {
        "TCB": "Techcombank", "VCB": "Vietcombank", "MBB": "MB Bank",
        "ACB": "ACB", "BID": "BIDV", "CTG": "VietinBank", "VPB": "VPBank",
    }.get(ticker, ticker)
    return [
        f"{ticker} {company_name}",
        f"{ticker} kết quả kinh doanh",
        f"{ticker} cổ phiếu tin tức",
        f"{ticker} ngân hàng",
    ]


def make_funnel_batch_id(ticker: str) -> str:
    """Generate funnel_batch_id like VCB-20260508-1530."""
    return f"{ticker}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')}"


def write_candidate_to_db(db, candidate: dict, funnel_batch_id: str) -> str | None:
    """Insert a candidate into crawl_log. Returns row_id, or None if dup-skipped."""
    row_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()
    try:
        db.insert_crawl_row({
            "row_id": row_id,
            "funnel_batch_id": funnel_batch_id,
            "ticker": candidate["ticker"],
            "source_name": candidate["source_name"],
            "source_url": candidate["url"],
            "title": candidate.get("title", "(no title)"),
            "raw_content": (candidate.get("content") or "")[:2000],
            "published_time": candidate.get("published_time"),
            "crawled_at": now_iso,
        })
        return row_id
    except Exception:
        # likely UNIQUE source_url — skip
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Crawler stage — write candidates to SQLite")
    parser.add_argument("ticker", help="Bank ticker (e.g. VCB)")
    parser.add_argument("--candidates-json", type=Path, required=True,
                        help="Path to JSON file with array of candidate dicts")
    parser.add_argument("--db", type=Path, default=Path("data/pipeline.db"))
    parser.add_argument("--schema", type=Path, default=Path("data/pipeline.schema.sql"))
    args = parser.parse_args()

    ticker = args.ticker.upper()
    if ticker not in BANK_UNIVERSE:
        print(json.dumps({"error": f"{ticker} not in MVP Bank universe", "universe": BANK_UNIVERSE}))
        return 1

    # Lazy import to allow tests to monkeypatch
    from lib.pipeline_db import PipelineDB

    args.db.parent.mkdir(parents=True, exist_ok=True)
    db = PipelineDB(args.db)
    if not args.db.exists() or args.db.stat().st_size == 0:
        db.init_schema(args.schema)

    candidates = json.loads(args.candidates_json.read_text(encoding="utf-8"))
    if not isinstance(candidates, list):
        print(json.dumps({"error": "candidates JSON must be a list"}))
        return 1

    funnel_batch_id = make_funnel_batch_id(ticker)
    rows_written = []
    rows_skipped = 0
    errors = []

    for c in candidates:
        c.setdefault("ticker", ticker)
        if "url" not in c or "source_name" not in c:
            errors.append({"candidate": c, "error": "missing url or source_name"})
            continue
        rid = write_candidate_to_db(db, c, funnel_batch_id)
        if rid:
            rows_written.append({"row_id": rid, "url": c["url"], "source_name": c["source_name"]})
        else:
            rows_skipped += 1

    db.close()
    print(json.dumps({
        "ticker": ticker,
        "funnel_batch_id": funnel_batch_id,
        "rows_written": rows_written,
        "rows_skipped_dedupe": rows_skipped,
        "errors": errors,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Smoke test**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && cat > /tmp/cands.json <<'EOF'
[
  {"source_name": "Báo Pháp luật", "url": "https://example.com/vcb-test-1", "title": "VCB test 1", "published_time": "2026-05-07T10:00:00+07:00", "content": "Body 1"},
  {"source_name": "VnEconomy", "url": "https://example.com/vcb-test-2", "title": "VCB test 2", "published_time": "2026-05-06T10:00:00+07:00", "content": "Body 2"}
]
EOF
rm -f /tmp/test-pipeline.db
uv run python lib/stages/run_crawler.py VCB --candidates-json /tmp/cands.json --db /tmp/test-pipeline.db
echo "---"
uv run python -c "
from lib.pipeline_db import PipelineDB
db = PipelineDB('/tmp/test-pipeline.db')
rows = db.query_by_funnel_batch([r for r in db.list_tables() if r=='crawl_log'][0:0] or db.conn.execute('SELECT funnel_batch_id FROM crawl_log LIMIT 1').fetchone()[0])
print(f'Rows in DB: {len(rows)}')
"
```

Expected: rows_written has 2 entries, error count 0, DB has 2 rows.

- [ ] **Step 4: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add lib/stages/ && git commit -m "feat(lib): run_crawler stage — SQLite write candidates with funnel_batch_id + dedupe"
```

---

### Task 3: lib/render_compare_feed.py

- [ ] **Step 1: Write `lib/render_compare_feed.py`**

```python
"""Render a published article from SQLite generated_news + crawl_log into
markdown frontmatter format at output/compare-feed/<id>.md, plus update manifest.json.
"""
from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


def render_article_md(article: dict, anchor_row: dict, funnel_rows: list[dict]) -> str:
    """Build the markdown file content (frontmatter + 2 sections).

    article: row from generated_news
    anchor_row: row from crawl_log (the picked source)
    funnel_rows: all rows in same funnel_batch_id (for crawl_funnel section)
    """
    ticker = article["ticker"]
    sector = article.get("sector", "Bank")
    funnel_batch_id = anchor_row["funnel_batch_id"]
    crawled_at = anchor_row["crawled_at"]

    # Categorize funnel rows by decision
    picked = []
    rejected_v1 = []
    rejected_story = []
    rejected_master = []
    for r in funnel_rows:
        item = {
            "source": r["source_name"],
            "url": r["source_url"],
            "published": (r.get("published_time") or "")[:10],
            "reason": r.get("editor_v1_note") or r.get("story_editor_note") or r.get("master_note") or "",
        }
        if r.get("master_decision") == "write_article":
            item["reason"] = r.get("master_note") or "Anchor — đầy đủ data decode mechanism"
            picked.append(item)
        elif r.get("master_decision") in ("reject_no_data", "reject_data_conflict"):
            rejected_master.append(item)
        elif r.get("story_editor_decision") == "reject":
            rejected_story.append(item)
        elif r.get("editor_v1_decision") == "reject":
            rejected_v1.append(item)

    # Build frontmatter
    fm = {
        "title": article["title"],
        "ticker": ticker,
        "sector": sector,
        "sector_icon": _sector_icon(sector),
        "crawled_at": crawled_at,
        "funnel_batch_id": funnel_batch_id,
        "left_meta": {
            "author": _author_for_sector(sector),
            "word_count": article.get("word_count", 0),
            "key_view": article.get("key_view", "trung lập"),
            "skeptic_verdict": article.get("skeptic_verdict", "pass"),
            "pipeline_version": article.get("pipeline_version", "V3.6"),
            "format_check": "0% Anh + 400 hard cap",
        },
        "right_source": {
            "name": anchor_row["source_name"],
            "url": anchor_row["source_url"],
            "published": (anchor_row.get("published_time") or "")[:10],
            "raw_title": anchor_row["title"],
        },
        "insight": article.get("insight_final", ""),
        "why_chosen": _parse_why_chosen(article.get("brief_json")),
        "crawl_funnel": {
            "picked": picked or [{"source": anchor_row["source_name"], "url": anchor_row["source_url"],
                                  "published": (anchor_row.get("published_time") or "")[:10],
                                  "reason": "Anchor"}],
            "rejected_editor_v1": rejected_v1,
            "rejected_story_editor": rejected_story,
            "rejected_master": rejected_master,
        },
        "pipeline_log": _parse_pipeline_log(article.get("pipeline_log")),
    }

    fm_yaml = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).strip()

    body = (article.get("body") or "").strip()
    skeptic = (article.get("skeptic_critique") or "").strip()
    raw_content = (anchor_row.get("raw_content") or "").strip()

    left_section = body
    if skeptic:
        left_section += f"\n\n## Góc nhìn ngược\n\n{skeptic}"

    return (
        f"---\n{fm_yaml}\n---\n\n"
        f"<!-- left -->\n\n{left_section}\n\n"
        f"<!-- right -->\n\n{raw_content}\n"
    )


def _sector_icon(sector: str) -> str:
    return {"Bank": "🏦", "CK": "📈", "BĐS": "🏠"}.get(sector, "📰")


def _author_for_sector(sector: str) -> str:
    return {
        "Bank": "Chuyên gia ngân hàng",
        "CK": "Chuyên gia chứng khoán",
        "BĐS": "Chuyên gia bất động sản",
    }.get(sector, "Chuyên gia")


def _parse_why_chosen(brief_json_str: str | None) -> list[dict]:
    if not brief_json_str:
        return []
    try:
        brief = json.loads(brief_json_str)
    except json.JSONDecodeError:
        return []
    items = []
    if "why_chosen" in brief:
        items.append({"label": "Vì sao chọn bài này", "content": brief["why_chosen"]})
    if "angle_label" in brief:
        items.append({"label": "Angle chọn", "content": brief["angle_label"]})
    if "data_anchor" in brief:
        items.append({"label": "Data anchor", "content": brief["data_anchor"]})
    return items


def _parse_pipeline_log(log_str: str | None) -> dict:
    if not log_str:
        return {}
    try:
        return json.loads(log_str)
    except json.JSONDecodeError:
        return {}


def update_manifest(manifest_path: Path, summary: dict) -> None:
    """Append/update entry in manifest.json. Sort by crawled_at desc."""
    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        data = {"articles": []}
    # Replace existing entry with same id
    data["articles"] = [a for a in data["articles"] if a["id"] != summary["id"]]
    data["articles"].append(summary)
    data["articles"].sort(key=lambda a: a["crawled_at"], reverse=True)
    manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def render_for_funnel_batch(db_path: Path, funnel_batch_id: str, output_dir: Path) -> dict:
    from lib.pipeline_db import PipelineDB

    db = PipelineDB(db_path)
    rows = db.query_by_funnel_batch(funnel_batch_id)
    if not rows:
        db.close()
        return {"error": f"No rows for funnel_batch {funnel_batch_id}"}

    # Find anchor row (master_decision == write_article)
    anchor = next((r for r in rows if r.get("master_decision") == "write_article"), None)
    if not anchor:
        db.close()
        return {"error": f"No anchor row (no master_decision=write_article) in batch {funnel_batch_id}"}

    # Find generated_news article for this row_id
    cur = db.conn.execute(
        "SELECT * FROM generated_news WHERE row_id = ? ORDER BY published_at DESC LIMIT 1",
        (anchor["row_id"],),
    )
    art_row = cur.fetchone()
    if not art_row:
        db.close()
        return {"error": f"No generated_news for row_id {anchor['row_id']}"}
    article = dict(art_row)

    md_content = render_article_md(article, anchor, rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{funnel_batch_id}.md"
    out_path.write_text(md_content, encoding="utf-8")

    summary = {
        "id": funnel_batch_id,
        "ticker": article["ticker"],
        "sector": article.get("sector", "Bank"),
        "title": article["title"],
        "crawled_at": anchor["crawled_at"],
        "key_view": article.get("key_view", "trung lập"),
        "word_count": article.get("word_count", 0),
    }
    update_manifest(output_dir / "manifest.json", summary)
    db.close()
    return {"written": str(out_path), "summary": summary}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("funnel_batch_id", help="e.g. VCB-20260508-1530")
    parser.add_argument("--db", type=Path, default=Path("data/pipeline.db"))
    parser.add_argument("--output-dir", type=Path, default=Path("output/compare-feed/"))
    args = parser.parse_args()
    result = render_for_funnel_batch(args.db, args.funnel_batch_id, args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if "error" not in result else 2


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Write test `tests/test_render_compare_feed.py`**

```python
"""Tests for lib.render_compare_feed — markdown rendering."""
import json
from pathlib import Path

import pytest

from lib.pipeline_db import PipelineDB
from lib.render_compare_feed import render_for_funnel_batch, render_article_md


@pytest.fixture
def populated_db(tmp_path):
    schema = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db_path = tmp_path / "test.db"
    db = PipelineDB(db_path)
    db.init_schema(schema)
    # Seed: 1 picked + 1 rejected_story
    db.insert_crawl_row({
        "row_id": "anchor-1",
        "funnel_batch_id": "VCB-20260508-1530",
        "ticker": "VCB",
        "source_name": "Báo Pháp luật",
        "source_url": "https://example.com/anchor",
        "title": "VCB Q1/2026 lãi 11.803 tỷ",
        "crawled_at": "2026-05-08T15:30:00+07:00",
        "published_time": "2026-05-07T10:00:00+07:00",
        "raw_content": "Raw body of anchor.",
        "primary_ticker": "VCB",
        "sector": "Bank",
        "editor_v1_decision": "route_to_story_editor",
        "story_editor_decision": "write_brief",
        "master_decision": "write_article",
        "master_note": "Anchor — đầy đủ 4 con số decode mechanism",
        "status": "published",
    })
    db.insert_crawl_row({
        "row_id": "rej-1",
        "funnel_batch_id": "VCB-20260508-1530",
        "ticker": "VCB",
        "source_name": "VnEconomy",
        "source_url": "https://example.com/rej",
        "title": "VCB rej article",
        "crawled_at": "2026-05-08T14:30:00+07:00",
        "published_time": "2026-05-06T10:00:00+07:00",
        "primary_ticker": "VCB",
        "sector": "Bank",
        "editor_v1_decision": "route_to_story_editor",
        "story_editor_decision": "reject",
        "story_editor_note": "dup_event: cùng story KQKD Q1",
        "status": "rejected",
    })
    db.insert_generated_news({
        "article_id": "art-1",
        "row_id": "anchor-1",
        "ticker": "VCB",
        "sector": "Bank",
        "title": "VCB quý I: lãi vẫn tăng 9% dù bỏ thêm 1.700 tỷ vào quỹ phòng nợ xấu",
        "body": "Lợi nhuận trước thuế **11.803 tỷ đồng**, tăng 9%.\n\n## Cần để ý\n\nLần đầu sau...",
        "word_count": 354,
        "key_view": "thận trọng",
        "insight_final": "Phù hợp NĐT giá trị giữ trên 12 tháng.",
        "skeptic_critique": "Số trên có context unclear...",
        "skeptic_angle": "data_skepticism",
        "skeptic_verdict": "pass_with_caveats",
        "accepted_hypothesis": 1,
        "brief_json": json.dumps({
            "why_chosen": "Tin Q1/2026 mới, paradox mạnh.",
            "angle_label": "Chủ động xây bộ đệm — đánh đổi tốc độ lấy độ bền",
            "data_anchor": "DB BCTC Quarter VCB-2026-Q1.",
        }),
        "pipeline_log": json.dumps({"step_1_crawler": {"sources": 20}}),
        "status": "published",
        "published_at": "2026-05-08T16:00:00+07:00",
    })
    yield db, db_path
    db.close()


def test_render_writes_md_file(populated_db, tmp_path):
    _, db_path = populated_db
    out_dir = tmp_path / "out"
    result = render_for_funnel_batch(db_path, "VCB-20260508-1530", out_dir)
    assert "error" not in result
    md_path = out_dir / "VCB-20260508-1530.md"
    assert md_path.exists()
    content = md_path.read_text(encoding="utf-8")
    assert content.startswith("---\n")
    assert "<!-- left -->" in content
    assert "<!-- right -->" in content
    assert "VCB" in content
    assert "## Góc nhìn ngược" in content


def test_render_updates_manifest(populated_db, tmp_path):
    _, db_path = populated_db
    out_dir = tmp_path / "out"
    render_for_funnel_batch(db_path, "VCB-20260508-1530", out_dir)
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert len(manifest["articles"]) == 1
    assert manifest["articles"][0]["ticker"] == "VCB"
    assert manifest["articles"][0]["word_count"] == 354


def test_render_funnel_includes_rejected(populated_db, tmp_path):
    _, db_path = populated_db
    out_dir = tmp_path / "out"
    render_for_funnel_batch(db_path, "VCB-20260508-1530", out_dir)
    content = (out_dir / "VCB-20260508-1530.md").read_text()
    # frontmatter has rejected_story_editor with VnEconomy entry
    assert "VnEconomy" in content
    assert "dup_event" in content


def test_render_missing_anchor_returns_error(tmp_path):
    schema = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db = PipelineDB(tmp_path / "empty.db")
    db.init_schema(schema)
    db.close()
    out_dir = tmp_path / "out"
    result = render_for_funnel_batch(tmp_path / "empty.db", "MISSING-BATCH", out_dir)
    assert "error" in result
```

- [ ] **Step 3: Run tests**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_render_compare_feed.py -v
```

Expected: 4 PASS.

- [ ] **Step 4: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add lib/render_compare_feed.py tests/test_render_compare_feed.py && git commit -m "feat(lib): render_compare_feed — SQLite → markdown frontmatter + manifest"
```

---

### Task 4: Slash command + main pipeline agent

- [ ] **Step 1: Write `.claude/commands/tin.md`**

```markdown
---
description: Viết bài tin chuyên sâu về 1 mã cổ phiếu Việt Nam (Bank universe MVP)
argument-hint: <TICKER>
allowed-tools: Bash, Task, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

Trigger pipeline 6-step Newsroom V3.6 cho ticker **$1**.

Universe MVP Bank: TCB · VCB · MBB · ACB · BID · CTG · VPB.

Nếu $1 không thuộc universe → reply "Ticker $1 không thuộc MVP Bank universe. CK + BĐS sẽ thêm sau." và dừng.

Nếu $1 hợp lệ → dispatch agent `newsroom-pipeline` với input ticker = $1, để chạy 6-step:
1. Crawler (Python script)
2. Editor V1 (subagent newsroom-editor — Phase 4)
3. Story Editor (subagent newsroom-story-editor — Phase 4)
4. Master Bank (subagent newsroom-master-bank — Phase 4)
5. Skeptic (subagent newsroom-skeptic — Phase 4)
6. Render markdown (Python script)

Trong Phase 3 mechanical: Step 1 + 6 chạy thật, Step 2-5 stub (chỉ log "phase 4 implements"). Output sẽ là 1 file markdown ở `output/compare-feed/$1-<batch_id>.md` với content placeholder.
```

- [ ] **Step 2: Write `.claude/agents/newsroom-pipeline.md`**

```markdown
---
name: newsroom-pipeline
description: Top-level orchestrator for Finpath Newsroom 6-step pipeline. Use when /tin command dispatches with a ticker. Runs Crawler (Python script) → Editor V1 → Story Editor → Master sector → Skeptic → Render. Phase 3 stubs Step 2-5 (LLM agents in Phase 4).
tools: Bash, Task, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

# Newsroom Pipeline Agent

You orchestrate 6-step pipeline for 1 ticker. Reference skill `finpath-newsroom-orchestrator` for full spec (use `Skill: finpath-newsroom-orchestrator` to load).

## Input

Ticker (string, e.g. "VCB"). Validate against MVP Bank universe: `TCB|VCB|MBB|ACB|BID|CTG|VPB`. Reject if not in universe.

## Phase 3 mechanical workflow (current)

### Step 1 — Crawler

Use WebSearch + WebFetch to find 5-10 recent (≤30 days) news articles about the ticker from Vietnamese financial news sources (CafeF / VnEconomy / Vietstock / Báo Pháp luật / Tin nhanh chứng khoán etc.). Build a JSON array of candidates:

```json
[
  {
    "source_name": "<from URL → match SOURCES_WHITELIST in run_crawler.py>",
    "url": "<full URL>",
    "title": "<article title>",
    "published_time": "<ISO datetime if available, else null>",
    "content": "<first 2000 chars of body>"
  }
]
```

Save JSON to `/tmp/crawler-input-<ticker>.json`. Then run:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python lib/stages/run_crawler.py <TICKER> --candidates-json /tmp/crawler-input-<ticker>.json
```

Capture the `funnel_batch_id` from the output JSON.

### Step 2-5 — STUB in Phase 3

Phase 3 mechanical: do NOT dispatch LLM agents. Instead, write a stub article directly to SQLite generated_news so Step 6 can render it:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import sqlite3, uuid, json
from datetime import datetime, timezone
conn = sqlite3.connect('data/pipeline.db')
# Pick first row of batch as anchor
cur = conn.execute('SELECT row_id, source_url FROM crawl_log WHERE funnel_batch_id = ? LIMIT 1', ('<batch>',))
row = cur.fetchone()
if not row:
    print('No rows in batch'); exit(1)
row_id, _url = row
# Mark anchor + write stub article
conn.execute('UPDATE crawl_log SET master_decision=?, story_editor_decision=?, editor_v1_decision=?, status=? WHERE row_id=?',
             ('write_article','write_brief','route_to_story_editor','published', row_id))
conn.execute('INSERT INTO generated_news (article_id, row_id, ticker, sector, title, body, word_count, key_view, insight_final, accepted_hypothesis, status, published_at, pipeline_version) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
             (str(uuid.uuid4()), row_id, '<TICKER>', 'Bank',
              '[Phase 3 stub] <TICKER> bài tự động từ pipeline mechanical',
              'Body placeholder. Phase 4 agents sẽ generate bài thật từ brief Story Editor.',
              50, 'trung lập', 'Phase 3 stub — Phase 4 sẽ thay.', 1,
              'published', datetime.now(timezone.utc).isoformat(), 'V3.6'))
conn.commit()
conn.close()
print('Stub article created')
"
```

Replace `<batch>` with actual funnel_batch_id, `<TICKER>` with the ticker.

### Step 6 — Render

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python lib/render_compare_feed.py <funnel_batch_id>
```

This writes `output/compare-feed/<batch>.md` and updates `output/compare-feed/manifest.json`.

## Output to user

Confirm:
- Funnel batch id
- Number of crawled rows in SQLite
- File path of rendered markdown
- Suggest user run `cd web && npm run dev` to view at localhost:5173

## Phase 4 will replace stubs

When LLM agents (newsroom-editor, newsroom-story-editor, newsroom-master-bank, newsroom-skeptic) are built in Phase 4, replace the stub block with real subagent dispatches.
```

- [ ] **Step 3: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/commands/ .claude/agents/ && git commit -m "feat(claude): /tin command + newsroom-pipeline agent (Phase 3 stub Step 2-5)"
```

---

### Task 5: End-to-end smoke + final tag

- [ ] **Step 1: Run all pytest**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest -v 2>&1 | tail -5
```

Expected: 23 PASS (19 from Phase 2 + 4 from Phase 3 render tests).

- [ ] **Step 2: End-to-end smoke — invoke `/tin VCB` simulation manually**

Since `/tin` slash command is invoked from Claude Code session (not Bash), we simulate the pipeline orchestration manually:

a. Build minimal candidates JSON for VCB:

```bash
cat > /tmp/cands-smoke.json <<'EOF'
[
  {
    "source_name": "Báo Pháp luật",
    "url": "https://doanhnhan.baophapluat.vn/vcb-smoke-test-phase3",
    "title": "VCB smoke phase 3",
    "published_time": "2026-05-08T10:00:00+07:00",
    "content": "Smoke test body for Phase 3 pipeline mechanical."
  }
]
EOF
```

b. Run Step 1 (Crawler):

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python lib/stages/run_crawler.py VCB --candidates-json /tmp/cands-smoke.json --db data/pipeline.db
```

Capture funnel_batch_id from output (e.g. `VCB-20260508-1530`).

c. Simulate Step 2-5 stub (mark anchor + insert generated_news):

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && BATCH=$(uv run python -c "
import sqlite3
conn = sqlite3.connect('data/pipeline.db')
cur = conn.execute('SELECT funnel_batch_id FROM crawl_log WHERE ticker=? ORDER BY crawled_at DESC LIMIT 1', ('VCB',))
print(cur.fetchone()[0])
conn.close()
")
echo "Batch: $BATCH"
uv run python -c "
import sqlite3, uuid
from datetime import datetime, timezone
conn = sqlite3.connect('data/pipeline.db')
cur = conn.execute('SELECT row_id FROM crawl_log WHERE funnel_batch_id = ? LIMIT 1', ('$BATCH',))
row_id = cur.fetchone()[0]
conn.execute('UPDATE crawl_log SET master_decision=?, story_editor_decision=?, editor_v1_decision=?, status=? WHERE row_id=?',
             ('write_article','write_brief','route_to_story_editor','published', row_id))
conn.execute('INSERT INTO generated_news (article_id, row_id, ticker, sector, title, body, word_count, key_view, insight_final, accepted_hypothesis, status, published_at, pipeline_version) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
             (str(uuid.uuid4()), row_id, 'VCB', 'Bank',
              '[Phase 3 stub] VCB smoke test — pipeline mechanical wiring verified',
              'Phase 3 stub body. Phase 4 LLM agents sẽ generate bài thật.',
              50, 'trung lập', 'Phase 3 mechanical smoke OK.', 1,
              'published', datetime.now(timezone.utc).isoformat(), 'V3.6'))
conn.commit()
conn.close()
print('Stub article inserted')
"
```

d. Run Step 6 (Render):

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python lib/render_compare_feed.py "$BATCH"
```

e. Verify output file + manifest:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && ls -la output/compare-feed/ && cat output/compare-feed/manifest.json
```

Expected: new `output/compare-feed/$BATCH.md` exists, manifest has 2 entries (the existing VCB-20260508-1530 from Phase 1 + the new smoke batch).

f. Cleanup smoke data (DON'T commit it — leave only the VCB-20260508-1530 sample from Phase 1):

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import sqlite3
conn = sqlite3.connect('data/pipeline.db')
conn.execute('DELETE FROM generated_news WHERE title LIKE ?', ('[Phase 3 stub]%',))
conn.execute('DELETE FROM crawl_log WHERE source_url = ?', ('https://doanhnhan.baophapluat.vn/vcb-smoke-test-phase3',))
conn.commit(); conn.close()
print('Smoke data cleaned')
"
# Remove smoke .md and revert manifest if it changed
rm -f output/compare-feed/VCB-*.md.smoke
# Manually edit manifest.json to remove the smoke entry, keeping only VCB-20260508-1530
uv run python -c "
import json
from pathlib import Path
p = Path('output/compare-feed/manifest.json')
data = json.loads(p.read_text())
data['articles'] = [a for a in data['articles'] if not a['title'].startswith('[Phase 3 stub]')]
p.write_text(json.dumps(data, ensure_ascii=False, indent=2))
print('Manifest cleaned')
"
# Remove any stub markdown file in output (keep only VCB-20260508-1530.md)
ls output/compare-feed/*.md | grep -v 'VCB-20260508-1530.md' | xargs rm -f 2>/dev/null
ls output/compare-feed/
```

- [ ] **Step 3: Tag (after Task 6 finishes)**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git tag phase-3-pipeline-mechanical && git tag
```

---

### Task 6: KB completion ingest (advisor-recommended before Phase 4)

Phase 2 Task 6 only ingested 4 framework pages. Master Bank (Phase 4) needs per-ticker KB. Run targeted sweeps:

- [ ] **Step 1: Sweep `📚 KB ngành Ngân hàng` sub-page (find page id from hub)**

Use MCP to locate the "📚 KB ngành Ngân hàng" sub-page id. Likely a child_page block in Bank Sector hub root (already explored — 6 category sub-pages: Annual Reports, ĐHĐCĐ Resolutions, CEO/CFO Statements, Research Reports, M&A Cases, others).

For EACH category sub-page, fetch its child pages (the per-ticker pages). For each per-ticker page:
- Get all blocks recursively (depth 3)
- Categorize: page title contains specific ticker (VCB/TCB/MBB/ACB/BID/CTG/VPB) → `category: per-ticker`. Title pattern from category: "Annual Report" → `per-ticker`, "ĐHĐCĐ" → `per-ticker`, "CEO statement" → `per-ticker`, "Research" → `per-ticker`, "M&A" → `history`. Master references → `frameworks`.

Build JSON tree (incremental — append to /tmp/bank-sector-tree-extra.json), run `lib/kb_ingest.py`.

- [ ] **Step 2: Run incremental ingest**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python lib/kb_ingest.py /tmp/bank-sector-tree-extra.json kb/bank/
```

- [ ] **Step 3: Verify counts**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && find kb/bank -name "*.md" | wc -l && find kb/bank -name "*.md" | sed 's|/.*||' | sort | uniq -c
```

Expected: ~30+ markdown files, distributed across `frameworks/`, `per-ticker/`, possibly `history/` + `trends/`.

- [ ] **Step 4: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add kb/ && git commit -m "feat(kb): complete Bank KB ingest — per-ticker + history pages from Notion"
```

If the additional sub-pages aren't accessible (404) or the ingest budget is too tight, log it and proceed to Phase 4 with the 4 frameworks pages — agents will lean on web search per CLAUDE.md.

---

## Acceptance for Phase 3

1. ✅ 8 skills under `.claude/skills/`
2. ✅ `lib/stages/run_crawler.py` accepts JSON candidates → SQLite
3. ✅ `lib/render_compare_feed.py` reads SQLite → markdown
4. ✅ 4 render tests pass
5. ✅ `/tin VCB` slash command + `newsroom-pipeline` agent files exist
6. ✅ tag `phase-3-pipeline-mechanical`

---

## Out of scope Phase 3

- ❌ LLM agents Editor V1 / Story Editor / Master / Skeptic (Phase 4)
- ❌ Real article generation (Phase 4)
