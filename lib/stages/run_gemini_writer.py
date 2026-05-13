"""Step 4.3 Gemini Writer — generate parallel article via Gemini 2.5 Pro.

Runs AFTER Claude Master Step 4 has persisted body + data_trail. Reads brief
(from crawl_log.brief_json), master pick + data_trail (from generated_news),
and raw news (from crawl_log) → substitutes prompts/gemini_writer.md → calls
google-genai → persists generated_news.gemini_* columns.

Pipeline-safety: ALWAYS exits 0 even when Gemini fails. Result statuses:
  - success          : generated_news.gemini_* fully populated
  - skipped_failure  : status + error set; body/title NULL (Gemini API failed)
  - skipped_disabled : status + error set; body/title NULL (missing api_key)

Usage:
    uv run python -m lib.stages.run_gemini_writer --article-id <uuid>
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

from lib.llm import gemini_client  # noqa: E402
from lib.pipeline_db import PipelineDB  # noqa: E402

DEFAULT_SECRETS_PATH = REPO_ROOT / "data" / "secrets.yaml"
DEFAULT_PROMPT_PATH = REPO_ROOT / "prompts" / "gemini_writer.md"
DEFAULT_DB_PATH = REPO_ROOT / "data" / "pipeline.db"


def _load_article_context(db: PipelineDB, article_id: str) -> dict[str, Any] | None:
    """Join generated_news + crawl_log for the article. Returns None when missing."""
    cur = db.conn.execute(
        """
        SELECT
            gn.article_id,
            gn.ticker,
            gn.sector,
            gn.brief_json   AS gn_brief_json,
            gn.pipeline_log AS gn_pipeline_log,
            cl.title        AS raw_news_title,
            cl.raw_content  AS raw_news_body,
            cl.source_url   AS raw_news_url,
            cl.brief_json   AS cl_brief_json
        FROM generated_news gn
        JOIN crawl_log cl ON cl.row_id = gn.row_id
        WHERE gn.article_id = ?
        """,
        (article_id,),
    )
    row = cur.fetchone()
    if not row:
        return None
    return dict(row)


def _build_template_vars(article: dict[str, Any]) -> dict[str, str]:
    """Extract placeholder values for prompts/gemini_writer.md."""
    gn_brief = _safe_json_loads(article.get("gn_brief_json")) or {}
    cl_brief = _safe_json_loads(article.get("cl_brief_json")) or {}
    pipeline_log = _safe_json_loads(article.get("gn_pipeline_log")) or {}

    chosen_idx = gn_brief.get("chosen_question_idx", 0)
    if not isinstance(chosen_idx, int):
        chosen_idx = 0

    # Master picked-option summary in generated_news.brief_json
    stance = gn_brief.get("stance_directive") or {}
    format_id = gn_brief.get("format_id") or "standard_qa"

    # Full option text + tone/length from Story Editor brief in crawl_log.brief_json
    options = cl_brief.get("deep_question_options")
    picked_option = {}
    if isinstance(options, list) and 0 <= chosen_idx < len(options):
        picked_option = options[chosen_idx] or {}

    deep_question = picked_option.get("question") or picked_option.get("deep_question") or ""
    tone_bias = picked_option.get("tone_bias") or "neutral"
    # length_target may arrive as int (Story Editor stores word count target, e.g. 250)
    # or string ("compact"/"standard"/"detailed"). Always coerce to str for substitution.
    length_target = picked_option.get("length_target")
    if length_target is None or length_target == "":
        length_target = "standard"

    key_evidence = stance.get("key_evidence") if isinstance(stance, dict) else None
    if isinstance(key_evidence, list):
        key_evidence_text = ", ".join(str(e) for e in key_evidence)
    else:
        key_evidence_text = ""

    data_trail = (
        pipeline_log.get("step_4_master", {}).get("data_trail")
        if isinstance(pipeline_log, dict)
        else None
    )
    if not isinstance(data_trail, list):
        data_trail = []

    return {
        "ticker": str(article.get("ticker") or ""),
        "sector": str(article.get("sector") or ""),
        "raw_news_title": str(article.get("raw_news_title") or ""),
        "raw_news_body": str(article.get("raw_news_body") or ""),
        "raw_news_url": str(article.get("raw_news_url") or ""),
        "brief_deep_question": str(deep_question),
        "brief_stance_direction": str(stance.get("direction", "")) if isinstance(stance, dict) else "",
        "brief_stance_confidence": str(stance.get("confidence", "")) if isinstance(stance, dict) else "",
        "brief_stance_reason": str(stance.get("reason", "")) if isinstance(stance, dict) else "",
        "brief_key_evidence": key_evidence_text,
        "format_id": str(format_id),
        "tone_bias": str(tone_bias),
        "length_target": str(length_target),
        "data_trail_json": json.dumps(data_trail, ensure_ascii=False, indent=2),
    }


def _safe_json_loads(value: Any) -> Any:
    if value is None or value == "":
        return None
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return None
    return None


def _substitute(template: str, variables: dict[str, str]) -> str:
    """Replace `{{var}}` placeholders. Unknown placeholders are left as-is so prompt
    authors notice missing context instead of silently dropping it."""
    result = template
    for key, value in variables.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result


def run_gemini_writer(
    article_id: str,
    *,
    db: PipelineDB,
    secrets_path: Path = DEFAULT_SECRETS_PATH,
    prompt_path: Path = DEFAULT_PROMPT_PATH,
    client_factory: Callable[[str], Any] | None = None,
) -> dict[str, Any]:
    """Generate Gemini side for the article. NEVER raises — returns result dict.

    Result dict mirrors `lib.llm.gemini_client.generate_article` shape; additionally
    `error == "article_not_found"` when the article_id has no row.
    """
    article = _load_article_context(db, article_id)
    if article is None:
        return {
            "ok": False,
            "title": None,
            "body": None,
            "word_count": None,
            "model": gemini_client.DEFAULT_MODEL,
            "error": "article_not_found",
            "duration_ms": 0,
        }

    variables = _build_template_vars(article)
    template = prompt_path.read_text(encoding="utf-8")
    prompt = _substitute(template, variables)

    api_key = gemini_client.load_api_key(secrets_path)
    result = gemini_client.generate_article(
        prompt=prompt,
        api_key=api_key,
        _client_factory=client_factory,
    )

    if result["ok"]:
        status = "success"
    elif result["error"] == "missing_api_key":
        status = "skipped_disabled"
    else:
        status = "skipped_failure"

    db.update_gemini_output(
        article_id=article_id,
        status=status,
        title=result["title"] if result["ok"] else None,
        body=result["body"] if result["ok"] else None,
        word_count=result["word_count"] if result["ok"] else None,
        model=result["model"],
        generated_at=datetime.now(timezone.utc).isoformat() if result["ok"] else None,
        error=result["error"] if not result["ok"] else None,
    )
    return result


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Step 4.3 Gemini Writer")
    parser.add_argument("--article-id", required=True, help="generated_news.article_id")
    parser.add_argument(
        "--db-path",
        default=str(DEFAULT_DB_PATH),
        help="Path to pipeline.db (default data/pipeline.db)",
    )
    parser.add_argument(
        "--secrets-path",
        default=str(DEFAULT_SECRETS_PATH),
        help="Path to secrets.yaml",
    )
    parser.add_argument(
        "--prompt-path",
        default=str(DEFAULT_PROMPT_PATH),
        help="Path to gemini_writer.md prompt template",
    )
    args = parser.parse_args(argv)

    db = PipelineDB(args.db_path)
    try:
        result = run_gemini_writer(
            article_id=args.article_id,
            db=db,
            secrets_path=Path(args.secrets_path),
            prompt_path=Path(args.prompt_path),
        )
    finally:
        db.close()

    summary = {
        "ok": result["ok"],
        "article_id": args.article_id,
        "model": result["model"],
        "title": result["title"],
        "word_count": result["word_count"],
        "duration_ms": result["duration_ms"],
        "error": result["error"],
    }
    print(json.dumps(summary, ensure_ascii=False))
    # Exit 0 even on failure — pipeline MUST NOT block on Gemini failure
    return 0


if __name__ == "__main__":
    sys.exit(_main())
