"""V5.1.9 Step 4.3 Gemini Master orchestrator — free-style with tool access.

Promotion of run_gemini_writer.py: instead of reusing Claude Master's
data_trail, Gemini now does its own research via lib.llm.research_tools.

Flow:
  1. Load article context (raw news + brief deep_question_options + format
     picks) joined from generated_news + crawl_log.
  2. Build prompt by substituting placeholders in prompts/gemini_master.md.
  3. Call lib.llm.gemini_master.generate_article() — SDK auto-handles
     function-calling loop (max 8 remote calls).
  4. Persist:
     - gemini_* columns (title, body, word_count, model, generated_at,
       tokens_in/out, cost_usd, brief_json snapshot, step_log JSON)
     - if no other writer has filled primary fields yet, ALSO update
       title/body/word_count + recompute public_slug (Gemini becomes primary).

Pipeline-safe: NEVER raises. status ∈ {success, skipped_failure,
skipped_disabled}. Pipeline orchestrator (Step 4.3) checks status and moves
on regardless.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.llm import gemini_master, research_tools  # noqa: E402
from lib.pipeline_db import PipelineDB  # noqa: E402
from lib.slugify import slugify_hook  # noqa: E402

DEFAULT_SECRETS_PATH = REPO_ROOT / "data" / "secrets.yaml"
DEFAULT_PROMPT_PATH = REPO_ROOT / "prompts" / "gemini_master.md"
DEFAULT_DB_PATH = REPO_ROOT / "data" / "pipeline.db"

# Placeholder values pipeline orchestrator inserts so the row exists before
# either writer fires. When the row's title still equals this, the first
# writer to complete claims primary slot.
PRIMARY_PLACEHOLDER = "pending-master"


def _load_article_context(db: PipelineDB, article_id: str) -> dict[str, Any] | None:
    cur = db.conn.execute(
        """
        SELECT
            gn.article_id, gn.ticker, gn.sector, gn.row_id,
            gn.title AS current_title, gn.public_slug,
            cl.title AS raw_news_title,
            cl.raw_content AS raw_news_body,
            cl.source_url AS raw_news_url,
            cl.brief_json AS cl_brief_json,
            cl.funnel_batch_id
        FROM generated_news gn
        JOIN crawl_log cl ON cl.row_id = gn.row_id
        WHERE gn.article_id = ?
        """,
        (article_id,),
    )
    row = cur.fetchone()
    return dict(row) if row else None


def _safe_json_loads(value: Any) -> Any:
    if value is None or value == "":
        return None
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return None


def _build_template_vars(article: dict[str, Any]) -> dict[str, str]:
    cl_brief = _safe_json_loads(article.get("cl_brief_json")) or {}
    options = cl_brief.get("deep_question_options") or []
    format_picks = cl_brief.get("format_picks") or []
    angle_label = cl_brief.get("angle_label") or ""
    angle_narrative = cl_brief.get("angle_narrative") or ""

    return {
        "ticker": str(article.get("ticker") or ""),
        "sector": str(article.get("sector") or ""),
        "raw_news_title": str(article.get("raw_news_title") or ""),
        "raw_news_body": str(article.get("raw_news_body") or ""),
        "raw_news_url": str(article.get("raw_news_url") or ""),
        "angle_label": str(angle_label),
        "angle_narrative": str(angle_narrative),
        "deep_question_options_json": json.dumps(options, ensure_ascii=False, indent=2),
        "format_picks_json": json.dumps(format_picks, ensure_ascii=False, indent=2),
    }


def _substitute(template: str, variables: dict[str, str]) -> str:
    result = template
    for key, value in variables.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result


def _build_step_log(result: dict[str, Any], duration_ms: int) -> dict[str, Any]:
    """Build observability payload mirroring legacy step_4_master shape so
    render + UI code paths can read pipeline_log['step_4_3_gemini_master']
    same way they read step_4_master.

    V5.1.9.1: include `tool_history` — SDK ground truth of which tools were
    actually invoked with what args + result summary. Distinct from
    `data_trail` which is the LLM's own self-narrative.
    """
    payload = result.get("payload") or {}
    return {
        "model": result.get("model"),
        "duration_ms": duration_ms,
        "tokens": result.get("usage", {}),
        "chosen_question_idx": payload.get("chosen_question_idx"),
        "chosen_pick_reason": payload.get("chosen_pick_reason"),
        "skip_reasons": payload.get("skip_reasons"),
        "data_trail": payload.get("data_trail") or [],
        "tool_history": result.get("tool_history") or [],
        "gates_passed": payload.get("gates_passed"),
        "format_id_used": payload.get("format_id_used"),
        "format_escalation_reason": payload.get("format_escalation_reason"),
        "insight_final": payload.get("insight_final"),
        "key_view": payload.get("key_view"),
        "variety_guard_angle": payload.get("variety_guard_angle"),
    }


def _promote_to_primary_if_needed(db: PipelineDB, article: dict[str, Any], payload: dict[str, Any], writer: str) -> str | None:
    """If row's current_title is the placeholder, this writer becomes primary:
    fill title/body/word_count/insight_final/key_view/variety_guard_angle +
    recompute public_slug + set primary_writer flag.

    V5.1.9.2: `primary_writer` is written as an explicit column so the
    render/web layer doesn't have to body-string-match. `writer` arg is
    'gemini' or 'grok' from the caller.
    """
    current_title = (article.get("current_title") or "").strip().lower()
    if current_title and PRIMARY_PLACEHOLDER not in current_title:
        return None  # someone else already primary

    title = payload.get("title")
    body = payload.get("body")
    if not isinstance(title, str) or not isinstance(body, str):
        return None

    # Recompute slug from final title
    old_slug = article.get("public_slug") or ""
    hook = slugify_hook(title)
    if PRIMARY_PLACEHOLDER in old_slug:
        new_slug = old_slug.replace(PRIMARY_PLACEHOLDER, hook)
    else:
        ticker = article.get("ticker") or ""
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
        new_slug = f"{ticker}-{stamp}-{hook}"

    db.update_generated_news(article["article_id"], {
        "title": title,
        "body": body,
        "word_count": payload.get("word_count"),
        "insight_final": payload.get("insight_final"),
        "key_view": payload.get("key_view"),
        "variety_guard_angle": payload.get("variety_guard_angle"),
        "public_slug": new_slug,
        "primary_writer": writer,
        # V5.1.9.3: status='published' so cards/feed pages that filter on
        # status surface the article. Pre-V5.1.9 Master skill set this; the
        # writer orchestrators didn't.
        "status": "published",
        "published_at": datetime.now(timezone.utc).isoformat(),
    })
    # V5.1.9.3: render_compare_feed.py filters anchors by
    # crawl_log.master_decision='write_article'. Step 4.0 placeholder leaves
    # this NULL; without the update, render returns no anchors + pipeline
    # halts. Set it when the first writer claims primary so render finds
    # the article.
    row_id = article.get("row_id")
    if row_id:
        db.update_crawl_row(row_id, {
            "master_decision": "write_article",
            "master_note": f"primary_writer={writer} (V5.1.9 free-style)",
        })
    return new_slug


def run_gemini_master(
    article_id: str,
    *,
    db: PipelineDB,
    secrets_path: Path = DEFAULT_SECRETS_PATH,
    prompt_path: Path = DEFAULT_PROMPT_PATH,
    client_factory: Callable[[str], Any] | None = None,
    tavily_api_key: str | None = None,
) -> dict[str, Any]:
    """Run Gemini Master for article_id. NEVER raises."""
    article = _load_article_context(db, article_id)
    if article is None:
        return {
            "ok": False,
            "article_id": article_id,
            "error": "article_not_found",
            "duration_ms": 0,
        }

    variables = _build_template_vars(article)
    template = prompt_path.read_text(encoding="utf-8")
    prompt = _substitute(template, variables)

    tools = research_tools.build_research_tools(
        db=db, secrets_path=secrets_path, tavily_api_key=tavily_api_key
    )
    api_key = gemini_master.load_api_key(secrets_path)
    result = gemini_master.generate_article(
        prompt=prompt,
        tools=tools,
        api_key=api_key,
        _client_factory=client_factory,
    )

    if result["ok"]:
        status = "success"
    elif result["error"] == "missing_api_key":
        status = "skipped_disabled"
    else:
        status = "skipped_failure"

    # Cost
    from lib.llm import pricing as _pricing
    usage = result.get("usage") or {}
    t_in = usage.get("prompt_tokens") if isinstance(usage, dict) else None
    t_out = usage.get("completion_tokens") if isinstance(usage, dict) else None
    cost_usd: float | None = None
    if isinstance(t_in, int) and isinstance(t_out, int):
        cost_usd = _pricing.compute_cost(result["model"], t_in, t_out)

    payload = result.get("payload") or {}
    step_log = _build_step_log(result, result["duration_ms"])

    # V5.1.9.3: persist step_log even on failure so observability surfaces
    # the error + any partial data (e.g. tool_history filled before final
    # JSON parse failed). On disabled/missing-key path step_log captures
    # the skip reason for audit.
    failure_step_log = {
        "model": result.get("model"),
        "duration_ms": result.get("duration_ms"),
        "tokens": result.get("usage") or {},
        "tool_history": result.get("tool_history") or [],
        "error": result.get("error"),
        "skipped_reason": status if not result["ok"] else None,
    }
    db.update_gemini_output(
        article_id=article_id,
        status=status,
        title=payload.get("title") if result["ok"] else None,
        body=payload.get("body") if result["ok"] else None,
        word_count=payload.get("word_count") if result["ok"] else None,
        model=result["model"],
        generated_at=datetime.now(timezone.utc).isoformat() if result["ok"] else None,
        error=result["error"] if not result["ok"] else None,
        tokens_in=t_in if result["ok"] else None,
        tokens_out=t_out if result["ok"] else None,
        cost_usd=cost_usd if result["ok"] else None,
        brief_json=json.dumps({
            "chosen_question_idx": payload.get("chosen_question_idx"),
            "chosen_pick_reason": payload.get("chosen_pick_reason"),
            "skip_reasons": payload.get("skip_reasons"),
            "format_id_used": payload.get("format_id_used"),
        }, ensure_ascii=False) if result["ok"] else None,
        step_log=json.dumps(step_log if result["ok"] else failure_step_log, ensure_ascii=False),
    )

    if result["ok"]:
        # Try to claim primary slot. If already taken (grok finished first), no-op.
        article_refreshed = _load_article_context(db, article_id) or article
        _promote_to_primary_if_needed(db, article_refreshed, payload, writer="gemini")

    return {
        "ok": result["ok"],
        "article_id": article_id,
        "model": result["model"],
        "title": payload.get("title") if result["ok"] else None,
        "word_count": payload.get("word_count") if result["ok"] else None,
        "duration_ms": result["duration_ms"],
        "cost_usd": cost_usd,
        "tool_calls": len(payload.get("data_trail") or []),
        "error": result["error"],
    }


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Step 4.3 Gemini Master (V5.1.9)")
    parser.add_argument("--article-id", required=True)
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--secrets-path", default=str(DEFAULT_SECRETS_PATH))
    parser.add_argument("--prompt-path", default=str(DEFAULT_PROMPT_PATH))
    args = parser.parse_args(argv)

    db = PipelineDB(args.db_path)
    try:
        result = run_gemini_master(
            article_id=args.article_id,
            db=db,
            secrets_path=Path(args.secrets_path),
            prompt_path=Path(args.prompt_path),
        )
    finally:
        db.close()
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
