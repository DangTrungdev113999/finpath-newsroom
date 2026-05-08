"""Render a published article from SQLite generated_news + crawl_log into
markdown frontmatter format at output/compare-feed/<id>.md, plus update manifest.json.
"""
from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow running as `python lib/render_compare_feed.py ...` from project root
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml


def render_article_md(article: dict, anchor_row: dict, funnel_rows: list[dict]) -> str:
    ticker = article["ticker"]
    sector = article.get("sector", "Bank")
    funnel_batch_id = anchor_row["funnel_batch_id"]
    crawled_at = anchor_row["crawled_at"]

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
    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        data = {"articles": []}
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

    anchor = next((r for r in rows if r.get("master_decision") == "write_article"), None)
    if not anchor:
        db.close()
        return {"error": f"No anchor row (no master_decision=write_article) in batch {funnel_batch_id}"}

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
