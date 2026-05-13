"""Render V4.0 — multi-article + 8-section right column for Compare Feed.

Each /tin run with N picked briefs produces N markdown files (1 per article).
Each markdown file has frontmatter with all 8 right-column sections data.
"""
from __future__ import annotations
import argparse
import json
import os
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
        "name": anchor_row.get("source_name", ""),
        "url": anchor_row.get("source_url", ""),
        "published": (anchor_row.get("published_time") or "")[:10],
        "raw_title": anchor_row.get("title", ""),
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

    # Section 7: skeptic data trail. Skeptic schema V4.0 key is
    # `skeptic_data_trail` (NOT `data_trail` like Master); read both for
    # backward compat — prefer canonical key.
    skeptic_data_trail = step_5.get("skeptic_data_trail") or step_5.get("data_trail", [])

    # Section 8: raw article URL (link only, NO embed)
    raw_article_url = anchor_row.get("source_url", "")

    # V5.0 — Format Director section (graceful degrade if missing).
    # Read step_3_5_format_director.format_picks[], pick the entry matching
    # Master's chosen_question_idx (fallback first pick).
    step_3_5 = pipeline_log.get("step_3_5_format_director")
    format_director = None
    if step_3_5 and isinstance(step_3_5, dict):
        picks = step_3_5.get("format_picks") or []
        pick = next(
            (p for p in picks if p.get("option_idx") == chosen_question_idx),
            picks[0] if picks else None,
        )
        if pick:
            format_director = {
                "format_id": pick.get("format_id"),
                "format_reason": pick.get("format_reason"),
                "tone_bias": pick.get("tone_bias", "neutral"),
                "length_target": pick.get("length_target"),
                "variety_check": step_3_5.get("variety_check", {}),
            }

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
        "format_director": format_director,
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


def _build_gemini_block(article: dict) -> dict | None:
    """Step 4.3 — return frontmatter block when Gemini side succeeded, else None.

    Defensive: requires status='success' AND title AND body all present (avoids
    emitting a half-broken block when only some fields were persisted).
    """
    if article.get("gemini_status") != "success":
        return None
    title = article.get("gemini_title")
    body = article.get("gemini_body")
    if not isinstance(title, str) or not isinstance(body, str) or not title or not body:
        return None
    block: dict = {"title": title, "body": body}
    word_count = article.get("gemini_word_count")
    if isinstance(word_count, int):
        block["word_count"] = word_count
    model = article.get("gemini_model")
    if isinstance(model, str) and model:
        block["model"] = model
    generated_at = article.get("gemini_generated_at")
    if isinstance(generated_at, str) and generated_at:
        block["generated_at"] = generated_at
    return block


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
            "pipeline_version": article.get("pipeline_version") or "V5.0",
        },
        "insight": article.get("insight_final", ""),
        # 8-section right column
        **build_right_column(article, anchor_row, funnel_rows),
    }

    gemini_block = _build_gemini_block(article)
    if gemini_block is not None:
        fm["gemini"] = gemini_block

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

    # NVL run found body also contaminated with <details><summary>Góc nhìn
    # ngược (Skeptic)</summary>...</details> block (orchestrator self-execute
    # inlined Skeptic critique into Master body field). Strip defensively so
    # Skeptic content appears exactly once via the appended "## Góc nhìn
    # ngược" section below.
    body = re.sub(
        r'\n*\s*<details>\s*<summary>\s*G[óo]c\s+nh[iì]n\s+ng[ưu][ợo]?c[^<]*</summary>[\s\S]*?</details>\s*',
        '\n',
        body,
        flags=re.IGNORECASE,
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


def _filter_stale_entries(articles: list[dict], output_dir: Path) -> list[dict]:
    """Drop manifest entries whose `<id>.md` file is missing on disk.

    Master persists with placeholder slug (`<TICKER>-<DATE>-<HHMM>-pending-headline`);
    after Headline (Step 4.5) the slug is regenerated from the final title and the
    new file is rendered. The old placeholder entry stays unless we sweep here,
    causing 404s in the viewer.
    """
    return [a for a in articles if (output_dir / f"{a['id']}.md").exists()]


def clean_manifest(manifest_path: Path) -> dict:
    """Self-heal: drop entries whose .md file no longer exists. Atomic write."""
    if not manifest_path.exists():
        return {"removed": 0, "remaining": 0}
    current = json.loads(manifest_path.read_text(encoding="utf-8"))
    before = len(current.get("articles", []))
    current["articles"] = _filter_stale_entries(
        current.get("articles", []), manifest_path.parent
    )
    after = len(current["articles"])
    tmp_path = manifest_path.with_suffix(".json.tmp")
    tmp_path.write_text(
        json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    os.replace(tmp_path, manifest_path)
    return {"removed": before - after, "remaining": after}


def update_manifest(manifest_path: Path, summary: dict) -> None:
    """Atomic append/update entry in manifest.json. id = public_slug.

    Phase G T6 — atomic via temp file + os.replace. Read-modify-write loop with
    retry on stale read (when 2nd writer races between our read + write).
    macOS/Linux: os.replace is atomic (POSIX rename guarantees).

    Self-heal: every write also sweeps stale entries (file deleted/renamed).
    """
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
        current["articles"] = _filter_stale_entries(
            current["articles"], manifest_path.parent
        )
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


def rebuild_manifest_from_db(db, output_dir: Path) -> dict:
    """Rebuild manifest.json from generated_news as single source of truth.

    Replaces the incremental update flow. Every accepted article whose
    `<public_slug>.md` exists on disk gets an entry; orphan files (placeholder
    leftover after Headline slug rename) and stale entries (file missing) are
    both excluded. Atomic write via temp + os.replace.

    Call at the end of `render_for_funnel_batch` (or as a one-shot reconcile)
    so the manifest always reflects DB truth — render-twice scenarios can no
    longer leak placeholder entries.
    """
    cur = db.conn.execute(
        """
        SELECT gn.public_slug, gn.ticker, gn.sector, gn.title, gn.key_view,
               gn.word_count, gn.pipeline_log, gn.brief_json,
               cl.crawled_at
        FROM generated_news gn
        JOIN crawl_log cl ON cl.row_id = gn.row_id
        WHERE gn.accepted_hypothesis = 1
          AND gn.public_slug IS NOT NULL
        ORDER BY cl.crawled_at DESC
        """
    )
    articles: list[dict] = []
    skipped_no_file = 0
    for row in cur.fetchall():
        public_slug = row["public_slug"]
        if not (output_dir / f"{public_slug}.md").exists():
            skipped_no_file += 1
            continue

        pipeline_log = _parse_json(row["pipeline_log"] or "{}")
        brief = _parse_json(row["brief_json"] or "{}")
        options = brief.get("deep_question_options") or []
        chosen_idx = pipeline_log.get("step_4_master", {}).get("chosen_question_idx", 0)
        chosen_category = None
        if isinstance(chosen_idx, int) and 0 <= chosen_idx < len(options):
            chosen_category = options[chosen_idx].get("category")
        format_id = (
            pipeline_log.get("step_4_master", {}).get("format_id_used")
            or "standard_listicle"
        )

        articles.append({
            "id": public_slug,
            "ticker": row["ticker"],
            "sector": row["sector"] or "Bank",
            "title": row["title"],
            "crawled_at": row["crawled_at"],
            "key_view": row["key_view"] or "trung lập",
            "word_count": row["word_count"] or 0,
            "category": chosen_category,
            "format_id": format_id,
        })

    # Preserve legacy entries (hand-crafted .md files with no DB row) so
    # rebuild doesn't drop pre-pipeline samples like VCB-20260508-1530.md.
    # Filter is still strict on file existence — pure-stale entries (no file
    # AND no DB row) get dropped as intended.
    manifest_path = output_dir / "manifest.json"
    new_ids = {a["id"] for a in articles}
    legacy_carried = 0
    if manifest_path.exists():
        try:
            old = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            old = {"articles": []}
        for entry in old.get("articles", []):
            entry_id = entry.get("id")
            if not entry_id or entry_id in new_ids:
                continue
            if (output_dir / f"{entry_id}.md").exists():
                articles.append(entry)
                legacy_carried += 1

    articles.sort(key=lambda a: a.get("crawled_at") or "", reverse=True)
    tmp_path = manifest_path.with_suffix(".json.tmp")
    tmp_path.write_text(
        json.dumps({"articles": articles}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    os.replace(tmp_path, manifest_path)
    return {
        "total": len(articles),
        "from_db": len(new_ids),
        "legacy_carried": legacy_carried,
        "skipped_no_file": skipped_no_file,
    }


def build_pipeline_runs_manifest(db, output_path: Path) -> int:
    """Build pipeline-runs.json from crawl_log + generated_news.

    Subsystem H V1.0.1 (Plan H Task 3) — aggregates crawl_log rows into a
    session-centric manifest the frontend consumes for pipeline run history.

    - Skip legacy rows: WHERE session_id IS NOT NULL (Q2 resolution).
    - One pipeline trigger = 1 session; one ticker within trigger = 1 batch.
    - Atomic write via .tmp suffix + os.replace (POSIX atomic rename).

    Returns number of sessions written.
    """
    sessions = _query_sessions(db)
    payload = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "sessions": sessions,
    }
    tmp_path = output_path.with_suffix(".json.tmp")
    tmp_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    os.replace(tmp_path, output_path)
    return len(sessions)


def _query_sessions(db) -> list[dict]:
    """Aggregate sessions from crawl_log LEFT JOIN generated_news.

    Schema-adapted from plan template — real crawl_log uses `published_time`
    (not `published_at`), has only `story_editor_note` (no separate
    `_label` / `_reason` columns), and does NOT have `sector_code` /
    `sector_name` / `hot_nhom` / `hot_rank` (those slots stay None pending
    a future Plan H task).
    """
    cur = db.conn.execute(
        """
        SELECT
            cl.row_id,
            cl.session_id,
            cl.trigger_type,
            cl.trigger_args,
            cl.funnel_batch_id,
            cl.ticker,
            cl.sector,
            cl.crawled_at,
            cl.source_name,
            cl.source_url,
            cl.published_time,
            cl.editor_v1_decision,
            cl.editor_v1_note,
            cl.story_editor_decision,
            cl.story_editor_note,
            gn.article_id,
            gn.title AS chosen_title,
            gn.accepted_hypothesis
        FROM crawl_log cl
        LEFT JOIN generated_news gn ON gn.row_id = cl.row_id
        WHERE cl.session_id IS NOT NULL
        ORDER BY cl.crawled_at DESC, cl.session_id, cl.funnel_batch_id
        LIMIT 5000
        """
    )

    sessions_dict: dict[str, dict] = {}

    for row in cur.fetchall():
        session_id = row["session_id"]
        if session_id not in sessions_dict:
            sessions_dict[session_id] = {
                "session_id": session_id,
                "trigger_type": row["trigger_type"] or "tin",
                "trigger_args": row["trigger_args"] or row["ticker"],
                "started_at": row["crawled_at"],
                "ended_at": row["crawled_at"],
                "fetched_total": 0,
                "chosen_total": 0,
                "rejected_total": 0,
                "_batches": {},
            }
        session = sessions_dict[session_id]
        if row["crawled_at"] > session["ended_at"]:
            session["ended_at"] = row["crawled_at"]
        if row["crawled_at"] < session["started_at"]:
            session["started_at"] = row["crawled_at"]

        batch_id = row["funnel_batch_id"]
        if batch_id not in session["_batches"]:
            session["_batches"][batch_id] = {
                "funnel_batch_id": batch_id,
                "ticker": row["ticker"],
                "sector_code": None,  # reserved — Plan H later task
                "sector_name": row["sector"],
                "hot_nhom": None,     # reserved — Plan H later task
                "hot_rank": None,     # reserved — Plan H later task
                "fetched_count": 0,
                "chosen_count": 0,
                "rejected_count": 0,
                "funnel_detail": {"picked": [], "rejected": []},
            }
        batch = session["_batches"][batch_id]
        batch["fetched_count"] += 1
        session["fetched_total"] += 1

        is_chosen = bool(row["article_id"]) and (row["accepted_hypothesis"] in (True, 1))
        if is_chosen:
            batch["chosen_count"] += 1
            session["chosen_total"] += 1
            batch["funnel_detail"]["picked"].append({
                "source": row["source_name"],
                "url": row["source_url"],
                "published": row["published_time"],
                "reason": f"OK — accepted_hypothesis: true. Title: {row['chosen_title'] or 'N/A'}",
            })
        else:
            batch["rejected_count"] += 1
            session["rejected_total"] += 1
            reject_agent, reject_label, reject_reason = _classify_reject(dict(row))
            batch["funnel_detail"]["rejected"].append({
                "source": row["source_name"],
                "url": row["source_url"],
                "published": row["published_time"],
                "reject_agent": reject_agent,
                "reject_label": reject_label,
                "reason": reject_reason,
            })

    sessions: list[dict] = []
    for session in sessions_dict.values():
        # Sort by ticker only — hot_rank slot is reserved for future Plan H task.
        session["batches"] = sorted(
            session["_batches"].values(),
            key=lambda b: b["ticker"],
        )
        del session["_batches"]
        sessions.append(session)
    sessions.sort(key=lambda s: s["started_at"], reverse=True)
    return sessions


def _classify_reject(row: dict) -> tuple[str, str, str]:
    """Return (reject_agent, reject_label, reason) for a non-chosen row.

    Real schema only carries `story_editor_note` for Story Editor rejects —
    both label and reason map to the same field (frontend can split later
    if separate columns get added).
    """
    if row.get("editor_v1_decision") == "reject":
        note = row.get("editor_v1_note") or ""
        return ("editor_v1", note or "unknown", note)
    if row.get("story_editor_decision") == "reject":
        note = row.get("story_editor_note") or ""
        return ("story_editor", note or "unknown", note)
    if not row.get("article_id"):
        return (
            "master",
            "accepted_hypothesis_false",
            "Master rejected — no article persisted",
        )
    return ("unknown", "unclassified", "")


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
        # V1.5-lite fix: render ALL articles per row_id (was LIMIT 1).
        # Some rows produce multiple articles when Master re-runs same brief
        # OR Story Editor picks 2 options for same row. All should render.
        cur = db.conn.execute(
            "SELECT * FROM generated_news WHERE row_id = ? ORDER BY published_at DESC",
            (anchor["row_id"],),
        )
        art_rows = cur.fetchall()
        if not art_rows:
            continue
        for art_row in art_rows:
            article = dict(art_row)
            public_slug = article.get("public_slug") or f"{anchor['ticker']}-{anchor['row_id']}-{article['article_id'][:8]}"
            md_content = render_article_md_v4(article, anchor, rows)
            out_path = output_dir / f"{public_slug}.md"
            out_path.write_text(md_content, encoding="utf-8")
            # Extract chosen deep_question category (1 of 5 Story Editor enums)
            brief = _parse_json(anchor.get("brief_json", "{}"))
            pipeline_log = _parse_json(article.get("pipeline_log", "{}"))
            options = brief.get("deep_question_options") or []
            chosen_idx = pipeline_log.get("step_4_master", {}).get(
                "chosen_question_idx", 0
            )
            chosen_category = None
            if isinstance(chosen_idx, int) and 0 <= chosen_idx < len(options):
                chosen_category = options[chosen_idx].get("category")

            format_id = (
                pipeline_log.get("step_4_master", {}).get("format_id_used")
                or "standard_listicle"
            )

            summary = {
                "id": public_slug,
                "ticker": article["ticker"],
                "sector": article.get("sector", "Bank"),
                "title": article["title"],
                "crawled_at": anchor["crawled_at"],
                "key_view": article.get("key_view", "trung lập"),
                "word_count": article.get("word_count", 0),
                "category": chosen_category,
                "format_id": format_id,
            }
            update_manifest(manifest_path, summary)
            written.append(str(out_path))

    # Final reconcile — rebuild manifest from DB as single source of truth.
    # Drops any orphan entries that lingered from a Headline slug rename or a
    # mid-pipeline render retry. Cheap (one query + atomic write).
    rebuild_summary = rebuild_manifest_from_db(db, output_dir)

    db.close()
    return {
        "count": len(written),
        "files": written,
        "manifest_total": rebuild_summary["total"],
        "manifest_skipped_no_file": rebuild_summary["skipped_no_file"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("funnel_batch_id")
    parser.add_argument("--db", type=Path, default=Path("data/pipeline.db"))
    parser.add_argument("--output-dir", type=Path, default=Path("output/compare-feed/"))
    args = parser.parse_args()
    result = render_for_funnel_batch(args.db, args.funnel_batch_id, args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # Build pipeline runs manifest (Subsystem H V1.0 — Plan H Task 3).
    # render_for_funnel_batch opens+closes its own DB connection, so reopen
    # fresh here for the aggregation pass.
    from lib.pipeline_db import PipelineDB

    runs_path = args.output_dir / "pipeline-runs.json"
    runs_db = PipelineDB(args.db)
    try:
        n_sessions = build_pipeline_runs_manifest(runs_db, runs_path)
    finally:
        runs_db.close()
    print(f"Built {runs_path.name} with {n_sessions} sessions")

    return 0 if "error" not in result else 2


if __name__ == "__main__":
    sys.exit(main())
