"""Step 3.5 Format Director — pure Python deterministic enrichment.

V5.1.5 (2026-05-13): Converted from LLM agent dispatch to direct Python helper.
Rationale: 5-step format-pick flow is 100% deterministic (lookup table +
regex counts + market_data threshold). Prior agent body forbade Python
shellout → forced sonnet LLM-think → 18min latency for 3 briefs. Python
helper runs the same logic in <1s.

Usage from pipeline orchestrator:
    uv run python lib/stages/run_format_director.py <BATCH_ID> \\
        --market-snapshot-json /tmp/market_snapshot.json \\
        --out /tmp/format-director-<BATCH_ID>.json

Reads brief_json from crawl_log rows where story_editor_decision='accept',
enriches every deep_question_option with format_id + tone_bias +
length_target via `lib.format_picker_logic.pick_format_for_option`, runs
variety check vs 3 most-recent generated_news for ticker, writes back to
crawl_log.brief_json. No article_ids exist yet (Master creates them in
Step 4) — pipeline_log step_3_5_format_director observability is deferred
to orchestrator and merged retroactively after Master persists generated_news.

Returns JSON summary on stdout (and optional --out file).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.format_picker_logic import pick_format_for_option  # noqa: E402
from lib.intra_batch_dedup import merge_briefs_in_batch  # noqa: E402
from lib.pipeline_db import PipelineDB  # noqa: E402


def _variety_check(db: PipelineDB, ticker: str, current_picks: list[str]) -> dict:
    rows = db.recent_generated_news(ticker, limit=3)
    formats = []
    for r in rows:
        pl = json.loads(r.get("pipeline_log") or "{}")
        fid = pl.get("step_4_master", {}).get("format_id_used", "unknown")
        formats.append(fid)
    warning = False
    if len(formats) == 3 and len(set(formats)) == 1 and current_picks and current_picks[0] == formats[0]:
        warning = True
    return {
        "recent_3_formats": formats,
        "current_pick_diversity_warning": warning,
    }


def _load_market_data(market_snapshot_json: str | None) -> dict | None:
    if not market_snapshot_json:
        return None
    p = Path(market_snapshot_json)
    if not p.is_file():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if data is None or not isinstance(data, dict):
        return None
    return data


def enrich_batch(
    batch_id: str,
    db: PipelineDB,
    market_data: dict | None,
) -> dict:
    rows = db.query_by_funnel_batch(batch_id)
    accepted = [
        r for r in rows
        if r.get("story_editor_decision") in ("accept", "write_brief")
        and r.get("brief_json")
    ]

    format_picks: list[dict] = []
    candidates_considered: list[dict] = []
    picks_by_row: dict[str, list[str]] = {}
    enriched_briefs_by_row: dict[str, dict] = {}

    for row in accepted:
        row_id = row["row_id"]
        ticker = row.get("primary_ticker") or row.get("ticker")
        brief_raw = row.get("brief_json")
        if not brief_raw:
            continue
        try:
            brief = json.loads(brief_raw)
        except json.JSONDecodeError:
            continue

        options = brief.get("deep_question_options") or []
        enriched_options = []
        per_option_picks = []
        for idx, opt in enumerate(options):
            picked = pick_format_for_option(opt, market_data)
            enriched_opt = {**opt, **picked}
            enriched_options.append(enriched_opt)
            per_option_picks.append(picked["format_id"])
            format_picks.append(
                {
                    "row_id": row_id,
                    "ticker": ticker,
                    "option_idx": idx,
                    "category": opt.get("category"),
                    "format_id": picked["format_id"],
                    "format_reason": picked["format_reason"],
                    "tone_bias": picked["tone_bias"],
                    "length_target": picked["length_target"],
                }
            )
            candidates_considered.append(
                {
                    "row_id": row_id,
                    "option_idx": idx,
                    "category": opt.get("category"),
                }
            )

        brief["deep_question_options"] = enriched_options
        # ticker is normalized on the brief itself so the dedup helper can
        # group by (ticker, dominant_category) without re-querying the DB.
        brief.setdefault("ticker", ticker)
        brief.setdefault("row_id", row_id)
        enriched_briefs_by_row[row_id] = brief
        picks_by_row[row_id] = per_option_picks

    # Intra-batch thesis MERGE (V5.1.8 — 2026-05-14): when Story Editor produces
    # 2+ briefs with the same dominant deep_question category for the same
    # ticker, ENRICH the strongest brief with the others' options + key_evidence
    # so Master writes 1 article that draws from BOTH sides instead of dropping
    # data (V5.1.6 behavior).
    merged = merge_briefs_in_batch(list(enriched_briefs_by_row.values()))
    merge_summary = {"keep": 0, "merged": 0, "absorbed": 0, "absorbed_rows": []}
    for brief in merged:
        row_id = brief.get("row_id")
        decision = brief.get("merge_decision", "keep")
        if decision.startswith("absorbed_into_"):
            winner_id = decision.removeprefix("absorbed_into_")
            merge_summary["absorbed"] += 1
            merge_summary["absorbed_rows"].append(row_id)
            note = (
                f"Intra-batch MERGE V5.1.8: brief absorbed into winner row_id={winner_id} "
                f"(cùng dominant_category) — Master skip, winner brief đã enrich với "
                f"options + key_evidence từ brief này."
            )
            db.update_crawl_row(
                row_id,
                {
                    "master_decision": "reject_dup_thesis",
                    "master_note": note,
                },
            )
        elif decision == "merged":
            merge_summary["merged"] += 1
        else:
            merge_summary["keep"] += 1
        db.update_crawl_row(
            row_id, {"brief_json": json.dumps(brief, ensure_ascii=False)}
        )

    # Variety check: aggregate across all enriched rows
    unique_tickers = {p["ticker"] for p in format_picks if p.get("ticker")}
    variety = {}
    for tkr in unique_tickers:
        tkr_picks = [p["format_id"] for p in format_picks if p["ticker"] == tkr]
        variety[tkr] = _variety_check(db, tkr, tkr_picks)

    # Batch-level format distribution
    counter = Counter(p["format_id"] for p in format_picks)

    return {
        "schema_version": "5.1.5",
        "batch_id": batch_id,
        "briefs_enriched": len({p["row_id"] for p in format_picks}),
        "options_enriched": len(format_picks),
        "format_picks": format_picks,
        "candidates_considered_per_option": candidates_considered,
        "variety_check": variety,
        "intra_batch_merge": merge_summary,
        "format_distribution": dict(counter),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("batch_id", help="funnel_batch_id (e.g. MSN-20260513-0318)")
    ap.add_argument(
        "--market-snapshot-json",
        help="Path to Step 1.5 market snapshot JSON (optional)",
    )
    ap.add_argument(
        "--out",
        help="Optional path to write full summary JSON",
    )
    ap.add_argument(
        "--db",
        default="data/pipeline.db",
        help="SQLite path (default: data/pipeline.db)",
    )
    args = ap.parse_args()

    t0 = time.time()
    db = PipelineDB(args.db)
    try:
        market_data = _load_market_data(args.market_snapshot_json)
        summary = enrich_batch(args.batch_id, db, market_data)
    finally:
        db.close()
    summary["duration_ms"] = int((time.time() - t0) * 1000)
    summary["ok"] = True

    out_text = json.dumps(summary, ensure_ascii=False)
    print(out_text)
    if args.out:
        Path(args.out).write_text(out_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
