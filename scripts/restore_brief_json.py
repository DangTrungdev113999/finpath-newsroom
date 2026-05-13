"""Forensic restore — copy crawl_log.brief_json → generated_news.brief_json for empty rows.

Headline Craft V1.6 needs brief_json on generated_news (where Step 4.5 reads from).
Today's Master rewrite batch left some rows with empty brief_json even though the
parent crawl_log row preserved it.

Usage:
    uv run python scripts/restore_brief_json.py            # report only (dry-run)
    uv run python scripts/restore_brief_json.py --apply    # actually UPDATE
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "pipeline.db"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Execute UPDATE (otherwise dry-run)")
    args = parser.parse_args()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cur = conn.execute(
        """
        SELECT
            gn.article_id,
            gn.ticker,
            gn.row_id,
            length(coalesce(gn.brief_json, '')) AS gn_len,
            length(coalesce(cl.brief_json, '')) AS cl_len,
            cl.brief_json AS source_brief
        FROM generated_news gn
        JOIN crawl_log cl ON cl.row_id = gn.row_id
        WHERE coalesce(length(gn.brief_json), 0) = 0
          AND coalesce(length(cl.brief_json), 0) > 0
        ORDER BY gn.ticker, gn.article_id
        """
    )
    rows = cur.fetchall()

    if not rows:
        print("Nothing to restore — generated_news.brief_json already populated where crawl_log has data.")
        return 0

    print(f"Found {len(rows)} articles with empty brief_json but populated crawl_log.brief_json:\n")
    for r in rows:
        try:
            brief = json.loads(r["source_brief"])
        except json.JSONDecodeError:
            preview = "JSON parse error"
        else:
            opts = brief.get("deep_question_options")
            if isinstance(opts, list) and opts:
                q = ""
                for k in ("question", "deep_question", "angle", "hypothesis"):
                    v = opts[0].get(k) if isinstance(opts[0], dict) else None
                    if isinstance(v, str) and v.strip():
                        q = v.strip()
                        break
                preview = f"V5({len(opts)} opts): {q[:80]}"
            elif "insight_hypothesis" in brief:
                preview = f"V4 insight: {brief['insight_hypothesis'][:80]}"
            else:
                preview = f"keys={list(brief.keys())[:5]}"
        print(f"  {r['article_id'][:8]}  {r['ticker']:5s}  cl_len={r['cl_len']:5d}  {preview}")

    if not args.apply:
        print("\nDry-run mode — re-run with --apply to UPDATE generated_news.brief_json")
        return 0

    print("\nApplying UPDATE...")
    updated = 0
    for r in rows:
        conn.execute(
            "UPDATE generated_news SET brief_json = ? WHERE article_id = ?",
            (r["source_brief"], r["article_id"]),
        )
        updated += 1
    conn.commit()
    print(f"Updated {updated} rows.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
