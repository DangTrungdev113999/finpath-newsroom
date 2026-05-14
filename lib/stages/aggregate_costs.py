"""V5.1.8 cost aggregator — runs AFTER Master + Gemini + Grok + Image steps.

Reads each generated_news row's pipeline_log JSON to extract Claude Master
usage (input/output tokens + total_cost_usd surfaced by spawn_step_agent),
computes claude_cost_usd via lib.llm.pricing.compute_cost(), then sums all
4 per-model costs (claude / gemini / grok / image) into total_cost_usd.

Idempotent: re-running on a row that already has costs is safe — values
overwrite. NULL-safe: missing component → contributes 0 to total. When all
4 components are NULL/0, total_cost_usd stays NULL (signals "no cost data
yet" rather than fabricated zero).

Pipeline.md Step 6 (Render) invokes this BEFORE render so the frontmatter
costs: block carries final aggregated values.

Usage:
    uv run python -m lib.stages.aggregate_costs --article-id <uuid>
    uv run python -m lib.stages.aggregate_costs --batch-id <batch>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.llm import pricing  # noqa: E402
from lib.pipeline_db import PipelineDB  # noqa: E402

DEFAULT_DB_PATH = REPO_ROOT / "data" / "pipeline.db"

# Master spawn_step_agent default model — used when pipeline_log doesn't
# record `model` explicitly. Aligned with .claude/skills/finpath-newsroom-
# orchestrator/references/spawn-step-agent.md Step 4 model preset.
DEFAULT_MASTER_MODEL = "claude-opus-4-7"


def extract_claude_usage(pipeline_log: dict[str, Any]) -> dict[str, Any]:
    """Pull Claude Master input/output tokens + model from pipeline_log.

    Handles both shapes:
        - V5.1.5+: `tokens` is a dict {input, output, cache_creation, cache_read}
          (spawn_step_agent canonical shape)
        - Legacy: `tokens` is an int total_tokens (from parse_task_usage)

    Returns dict with keys: tokens_in, tokens_out, model (any may be None).
    """
    step = pipeline_log.get("step_4_master") or {}
    if not isinstance(step, dict):
        return {"tokens_in": None, "tokens_out": None, "model": None}

    raw_tokens = step.get("tokens")
    tokens_in: int | None = None
    tokens_out: int | None = None
    if isinstance(raw_tokens, dict):
        # Cache reads + cache creation count toward input; do not double-count.
        in_tok = raw_tokens.get("input") or 0
        cache_creation = raw_tokens.get("cache_creation") or 0
        cache_read = raw_tokens.get("cache_read") or 0
        out_tok = raw_tokens.get("output") or 0
        if isinstance(in_tok, int) or isinstance(cache_creation, int) or isinstance(cache_read, int):
            tokens_in = (in_tok or 0) + (cache_creation or 0) + (cache_read or 0)
        if isinstance(out_tok, int):
            tokens_out = out_tok
    elif isinstance(raw_tokens, int) and raw_tokens > 0:
        # Legacy total-only: attribute conservatively as 80% input / 20% output
        # (typical chat ratio). Cost shape biased slightly low; sufficient for
        # aggregate audit, not for billing reconciliation.
        tokens_in = int(raw_tokens * 0.8)
        tokens_out = raw_tokens - tokens_in

    # Only attach a model when we actually have tokens to price. No tokens
    # → return all-None so caller knows "no Claude usage recorded yet" and
    # leaves claude_cost_usd NULL.
    if tokens_in is None and tokens_out is None:
        return {"tokens_in": None, "tokens_out": None, "model": None}

    model = step.get("model")
    if not isinstance(model, str) or not model:
        model = DEFAULT_MASTER_MODEL

    return {"tokens_in": tokens_in, "tokens_out": tokens_out, "model": model}


def aggregate_article_costs(db: PipelineDB, article_id: str) -> dict[str, Any]:
    """Compute + persist cost breakdown for one article. Returns final values.

    Pulls existing gemini_cost_usd / grok_cost_usd / image_cost_usd from DB
    (already populated by their respective writers), computes claude_cost_usd
    from pipeline_log, sums to total_cost_usd. Writes via update_cost_breakdown.

    Returns dict {claude_cost_usd, gemini_cost_usd, grok_cost_usd,
    image_cost_usd, total_cost_usd, claude_tokens_in, claude_tokens_out}.
    Returns empty dict when article_id not found.
    """
    cur = db.conn.execute(
        """
        SELECT pipeline_log, gemini_cost_usd, grok_cost_usd, image_cost_usd,
               claude_tokens_in, claude_tokens_out, claude_cost_usd
        FROM generated_news WHERE article_id = ?
        """,
        (article_id,),
    )
    row = cur.fetchone()
    if row is None:
        return {}

    pipeline_log = json.loads(row["pipeline_log"]) if row["pipeline_log"] else {}
    claude_usage = extract_claude_usage(pipeline_log)
    claude_in = claude_usage["tokens_in"]
    claude_out = claude_usage["tokens_out"]
    claude_model = claude_usage["model"]

    claude_cost: float | None = None
    if isinstance(claude_in, int) and isinstance(claude_out, int):
        claude_cost = pricing.compute_cost(claude_model, claude_in, claude_out)

    # Gemini / Grok / Image costs come straight from their writer columns.
    gemini_cost = row["gemini_cost_usd"]
    grok_cost = row["grok_cost_usd"]
    image_cost = row["image_cost_usd"]

    components = [claude_cost, gemini_cost, grok_cost, image_cost]
    total = sum(c for c in components if isinstance(c, (int, float)))
    total_cost: float | None = round(total, 6) if any(
        isinstance(c, (int, float)) for c in components
    ) else None

    db.update_cost_breakdown(
        article_id,
        claude_tokens_in=claude_in,
        claude_tokens_out=claude_out,
        claude_cost_usd=claude_cost,
        total_cost_usd=total_cost,
    )

    return {
        "article_id": article_id,
        "claude_tokens_in": claude_in,
        "claude_tokens_out": claude_out,
        "claude_cost_usd": claude_cost,
        "gemini_cost_usd": gemini_cost,
        "grok_cost_usd": grok_cost,
        "image_cost_usd": image_cost,
        "total_cost_usd": total_cost,
    }


def aggregate_batch_costs(db: PipelineDB, batch_id: str) -> list[dict[str, Any]]:
    """Aggregate costs for every article in a funnel batch. Returns list of
    per-article result dicts; empty list when no articles match.
    """
    cur = db.conn.execute(
        """
        SELECT gn.article_id
        FROM generated_news gn
        JOIN crawl_log cl ON cl.row_id = gn.row_id
        WHERE cl.funnel_batch_id = ?
          AND gn.accepted_hypothesis = 1
        """,
        (batch_id,),
    )
    article_ids = [r["article_id"] for r in cur.fetchall()]
    return [aggregate_article_costs(db, aid) for aid in article_ids]


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="V5.1.8 cost aggregator")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--article-id", help="Aggregate one article")
    g.add_argument("--batch-id", help="Aggregate all articles in a funnel batch")
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    args = parser.parse_args(argv)

    db = PipelineDB(args.db_path)
    try:
        if args.article_id:
            result = aggregate_article_costs(db, args.article_id)
            print(json.dumps(result, ensure_ascii=False))
        else:
            results = aggregate_batch_costs(db, args.batch_id)
            print(json.dumps({"count": len(results), "rows": results}, ensure_ascii=False))
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(_main())
