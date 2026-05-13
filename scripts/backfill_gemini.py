"""Backfill Gemini side for articles missing gemini_status='success'.

Usage:
    uv run python scripts/backfill_gemini.py [--dates YYYY-MM-DD,YYYY-MM-DD] [--dry-run]

Default dates: 2026-05-12,2026-05-13 (Phase A-C ship window).
Iterates articles sequentially (Gemini free tier = 10 RPM safety margin).
Logs each call result. Final summary at end.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.pipeline_db import PipelineDB  # noqa: E402
from lib.stages.run_gemini_writer import run_gemini_writer  # noqa: E402


def find_targets(db: PipelineDB, dates: list[str]) -> list[dict]:
    """Backfill targets — filter by crawl_log.crawled_at because feed sort uses
    crawled_at and many articles have generated_news.published_at = NULL (Skeptic
    step paused → never sets published_at). Joining keeps the cohort aligned with
    what users actually see in /feed.
    """
    placeholders = ",".join("?" for _ in dates)
    cur = db.conn.execute(
        f"""
        SELECT gn.article_id, gn.ticker, gn.title, gn.gemini_status,
               date(cl.crawled_at) AS pub_date,
               cl.funnel_batch_id AS batch_id
        FROM generated_news gn
        JOIN crawl_log cl ON cl.row_id = gn.row_id
        WHERE date(cl.crawled_at) IN ({placeholders})
          AND (gn.gemini_status IS NULL OR gn.gemini_status != 'success')
        ORDER BY cl.crawled_at ASC
        """,
        dates,
    )
    return [dict(r) for r in cur.fetchall()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dates",
        default="2026-05-12,2026-05-13",
        help="Comma-separated dates (YYYY-MM-DD)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    dates = [d.strip() for d in args.dates.split(",") if d.strip()]
    db = PipelineDB(str(REPO_ROOT / "data" / "pipeline.db"))
    targets = find_targets(db, dates)

    print(f"[backfill] {len(targets)} targets across dates {dates}")
    for t in targets:
        print(f"  {t['article_id'][:8]} | {t['pub_date']} | {t['ticker']:4} | batch={t['batch_id']}")

    if args.dry_run:
        print("[backfill] dry-run — no calls made")
        db.close()
        return 0

    results = {"success": 0, "skipped_failure": 0, "skipped_disabled": 0, "errors": []}
    batches: set[str] = set()
    started = time.monotonic()

    for i, t in enumerate(targets, start=1):
        article_id = t["article_id"]
        ticker = t["ticker"]
        print(
            f"[backfill] {i}/{len(targets)} {ticker} {article_id[:8]} … ",
            end="",
            flush=True,
        )
        call_start = time.monotonic()
        try:
            res = run_gemini_writer(article_id=article_id, db=db)
            elapsed = int((time.monotonic() - call_start) * 1000)
            if res["ok"]:
                results["success"] += 1
                batches.add(t["batch_id"])
                print(
                    f"ok ({elapsed}ms, {res['word_count']} từ) — {res['title'][:60]}",
                    flush=True,
                )
            elif res["error"] == "missing_api_key":
                results["skipped_disabled"] += 1
                print(f"skipped_disabled — {res['error']}", flush=True)
                # Don't continue trying without key
                results["errors"].append(
                    {"article_id": article_id, "error": "missing_api_key"}
                )
                break
            else:
                results["skipped_failure"] += 1
                results["errors"].append(
                    {"article_id": article_id, "error": res["error"]}
                )
                print(f"FAIL — {res['error']}", flush=True)
        except Exception as exc:  # noqa: BLE001
            results["skipped_failure"] += 1
            results["errors"].append(
                {"article_id": article_id, "error": f"exception: {exc}"}
            )
            print(f"EXCEPTION — {exc}", flush=True)

    total = int(time.monotonic() - started)
    db.close()

    summary = {
        "total_targets": len(targets),
        "success": results["success"],
        "skipped_failure": results["skipped_failure"],
        "skipped_disabled": results["skipped_disabled"],
        "elapsed_s": total,
        "batches_to_rerender": sorted(batches),
        "errors": results["errors"],
    }
    print("\n[backfill] summary:")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    # Write summary JSON for downstream re-render step (ephemeral)
    summary_path = Path("/tmp/backfill-gemini-summary.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[backfill] summary written: {summary_path}")
    return 0 if results["skipped_disabled"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
