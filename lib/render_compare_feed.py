"""Render V4.0 — multi-article + 8-section right column for Compare Feed.

Each /tin run with N picked briefs produces N markdown files (1 per article).
Each markdown file has frontmatter with all 8 right-column sections data.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow running as `python lib/render_compare_feed.py ...` from project root
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml


REJECT_AGENT_LABELS = {
    "editor_v1": "Gác cổng bỏ",
    "story_editor": "Tổng biên tập bỏ",
    "master": "Phóng viên bỏ",
}


def build_right_column(article: dict, anchor_row: dict, funnel_rows: list[dict]) -> dict:
    """Build the 8-section right-column data structure as frontmatter dict."""
    pipeline_log = _parse_json(article.get("pipeline_log", "{}"))
    brief = _parse_json(anchor_row.get("brief_json", "{}"))
    step_4 = pipeline_log.get("step_4_master", {})
    step_5 = pipeline_log.get("step_5_skeptic", {})

    # Section 1: original article info (raw_source)
    right_source = {
        "name": anchor_row["source_name"],
        "url": anchor_row["source_url"],
        "published": (anchor_row.get("published_time") or "")[:10],
        "raw_title": anchor_row["title"],
    }

    # Section 2: why_chosen_narrative (Story Editor)
    why_chosen_narrative = brief.get("why_chosen_narrative", "")

    # Section 3: angle (Story Editor)
    angle_label = brief.get("angle_label", "")
    angle_narrative = brief.get("angle_narrative", "")

    # Section 4: question options + Master pick
    deep_question_options = brief.get("deep_question_options", [])
    chosen_question_idx = step_4.get("chosen_question_idx", 0)
    chosen_pick_reason = step_4.get("chosen_pick_reason", "")
    skip_reasons = step_4.get("skip_reasons", {})

    # Section 5: crawl funnel — picked + rejected (with agent labels)
    crawl_funnel = _build_funnel(funnel_rows)

    # Section 6: master data trail
    master_data_trail = step_4.get("data_trail", [])

    # Section 7: skeptic data trail
    skeptic_data_trail = step_5.get("data_trail", [])

    # Section 8: raw article URL (link only, NO embed)
    raw_article_url = anchor_row["source_url"]

    return {
        "right_source": right_source,
        "why_chosen_narrative": why_chosen_narrative,
        "angle_label": angle_label,
        "angle_narrative": angle_narrative,
        "deep_question_options": deep_question_options,
        "chosen_question_idx": chosen_question_idx,
        "chosen_pick_reason": chosen_pick_reason,
        "skip_reasons": skip_reasons,
        "crawl_funnel": crawl_funnel,
        "master_data_trail": master_data_trail,
        "skeptic_data_trail": skeptic_data_trail,
        "raw_article_url": raw_article_url,
    }


def _build_funnel(rows: list[dict]) -> dict:
    """Group rows: picked + rejected_by_agent. Each rejected has agent label + narrative reason."""
    picked = []
    rejected = []
    for r in rows:
        item_base = {
            "source": r["source_name"],
            "url": r["source_url"],
            "published": (r.get("published_time") or "")[:10],
        }
        if r.get("master_decision") == "write_article":
            picked.append({**item_base, "reason": r.get("master_note") or "Anchor"})
        elif r.get("master_decision") in ("reject_no_data", "reject_data_conflict"):
            rejected.append({
                **item_base,
                "reject_agent": "master",
                "reject_label": REJECT_AGENT_LABELS["master"],
                "reason": r.get("master_note", "Master reject"),
            })
        elif r.get("story_editor_decision") == "reject":
            rejected.append({
                **item_base,
                "reject_agent": "story_editor",
                "reject_label": REJECT_AGENT_LABELS["story_editor"],
                "reason": r.get("story_editor_note", "Story Editor reject"),
            })
        elif r.get("editor_v1_decision") == "reject":
            rejected.append({
                **item_base,
                "reject_agent": "editor_v1",
                "reject_label": REJECT_AGENT_LABELS["editor_v1"],
                "reason": r.get("editor_v1_note", "Editor V1 reject"),
            })
    return {"picked": picked, "rejected": rejected, "total_candidates": len(rows)}


def _parse_json(s: str) -> dict:
    if not s:
        return {}
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return {}


def render_article_md_v4(article: dict, anchor_row: dict, funnel_rows: list[dict]) -> str:
    """Build the V4.0 markdown file content (frontmatter + 2 sections).

    Body = Master output as-is. Skeptic critique appended in left column section
    via '## Góc nhìn ngược' heading.
    """
    sector = article.get("sector", "Bank")
    sector_icon = {"Bank": "🏦", "CK": "📈", "BĐS": "🏠"}.get(sector, "📰")

    fm = {
        "title": article["title"],
        "ticker": article["ticker"],
        "sector": sector,
        "sector_icon": sector_icon,
        "crawled_at": anchor_row["crawled_at"],
        "funnel_batch_id": anchor_row["funnel_batch_id"],
        "left_meta": {
            "author": _author_for_sector(sector),
            "word_count": article.get("word_count", 0),
            "key_view": article.get("key_view", "trung lập"),
            "skeptic_verdict": article.get("skeptic_verdict", "pass"),
            "pipeline_version": article.get("pipeline_version", "V4.0"),
        },
        "insight": article.get("insight_final", ""),
        # 8-section right column
        **build_right_column(article, anchor_row, funnel_rows),
    }

    fm_yaml = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).strip()
    body = (article.get("body") or "").strip()
    skeptic = (article.get("skeptic_critique") or "").strip()

    # Bug B6 hotfix v2 (Phase G prep) — defensive strip embedded skeptic block
    # from BODY field too. VPB run found body field contaminated with full
    # skeptic critique (Master/orchestrator merged Skeptic content into body
    # before persist). Strip "## Góc nhìn ngược" + everything after — Skeptic
    # content lives in skeptic_critique field, render appends it once below.
    body = re.sub(
        r'\n*\s*#{2,3}\s+G[óo]c\s+nh[iì]n\s+ng[ưu][ợo]?c\s*\n[\s\S]*$',
        '',
        body,
        flags=re.MULTILINE,
    ).strip()

    left_section = body
    if skeptic:
        # Bug B6 fix — defensive strip leading "## Góc nhìn ngược" heading from
        # skeptic_critique. Skeptic skill V4.0 persists critique without heading,
        # but legacy data + agent regression handled here. Allows extra blank lines.
        skeptic_clean = re.sub(
            r'^\s*#{2,3}\s+G[óo]c\s+nh[iì]n\s+ng[ưu][ợo]?c\s*\n+',
            '',
            skeptic,
            count=1,
            flags=re.MULTILINE,
        )
        left_section += f"\n\n## Góc nhìn ngược\n\n{skeptic_clean}"

    # Right column markdown body — empty since frontmatter has all data
    # React component renders sections from frontmatter directly.
    right_section = ""

    return (
        f"---\n{fm_yaml}\n---\n\n"
        f"<!-- left -->\n\n{left_section}\n\n"
        f"<!-- right -->\n\n{right_section}\n"
    )


def _author_for_sector(sector: str) -> str:
    return {"Bank": "Chuyên gia ngân hàng", "CK": "Chuyên gia chứng khoán", "BĐS": "Chuyên gia bất động sản"}.get(sector, "Chuyên gia")


def update_manifest(manifest_path: Path, summary: dict) -> None:
    """Atomic append/update entry in manifest.json. id = public_slug.

    Phase G T6 — atomic via temp file + os.replace. Read-modify-write loop with
    retry on stale read (when 2nd writer races between our read + write).
    macOS/Linux: os.replace is atomic (POSIX rename guarantees).
    """
    import os
    import tempfile
    import time

    max_retries = 5
    for attempt in range(max_retries):
        # Read latest state
        if manifest_path.exists():
            try:
                current = json.loads(manifest_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                # Concurrent writer mid-write — back off + retry
                time.sleep(0.05 * (attempt + 1))
                continue
        else:
            current = {"articles": []}

        # Apply update
        current["articles"] = [a for a in current["articles"] if a["id"] != summary["id"]]
        current["articles"].append(summary)
        current["articles"].sort(key=lambda a: a["crawled_at"], reverse=True)

        # Atomic write via temp file in same dir + replace
        fd, tmp_path = tempfile.mkstemp(
            dir=manifest_path.parent, prefix=".manifest-", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(current, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, manifest_path)  # POSIX atomic rename
            return
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

    raise RuntimeError(f"Failed to atomically update {manifest_path} after {max_retries} retries")


def render_for_funnel_batch(db_path: Path, funnel_batch_id: str, output_dir: Path) -> dict:
    """V4.0: Loop ALL anchor rows in batch, render 1 file per article."""
    from lib.pipeline_db import PipelineDB

    db = PipelineDB(db_path)
    rows = db.query_by_funnel_batch(funnel_batch_id)
    if not rows:
        db.close()
        return {"error": f"No rows for batch {funnel_batch_id}"}

    anchors = [r for r in rows if r.get("master_decision") == "write_article"]
    if not anchors:
        db.close()
        return {"error": f"No anchors in batch {funnel_batch_id}"}

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    written = []

    for anchor in anchors:
        cur = db.conn.execute(
            "SELECT * FROM generated_news WHERE row_id = ? ORDER BY published_at DESC LIMIT 1",
            (anchor["row_id"],),
        )
        art_row = cur.fetchone()
        if not art_row:
            continue
        article = dict(art_row)
        public_slug = article.get("public_slug") or f"{anchor['ticker']}-{anchor['row_id']}"
        md_content = render_article_md_v4(article, anchor, rows)
        out_path = output_dir / f"{public_slug}.md"
        out_path.write_text(md_content, encoding="utf-8")
        summary = {
            "id": public_slug,
            "ticker": article["ticker"],
            "sector": article.get("sector", "Bank"),
            "title": article["title"],
            "crawled_at": anchor["crawled_at"],
            "key_view": article.get("key_view", "trung lập"),
            "word_count": article.get("word_count", 0),
        }
        update_manifest(manifest_path, summary)
        written.append(str(out_path))

    db.close()
    return {"count": len(written), "files": written}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("funnel_batch_id")
    parser.add_argument("--db", type=Path, default=Path("data/pipeline.db"))
    parser.add_argument("--output-dir", type=Path, default=Path("output/compare-feed/"))
    args = parser.parse_args()
    result = render_for_funnel_batch(args.db, args.funnel_batch_id, args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if "error" not in result else 2


if __name__ == "__main__":
    sys.exit(main())
