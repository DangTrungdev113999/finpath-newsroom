"""SQLite ops cho pipeline state — crawl_log + generated_news."""
from __future__ import annotations
import json
import re
import sqlite3
from pathlib import Path
from typing import Any


# Schema validation — V4.0 Phase H2 (after NVL run revealed orchestrator
# self-execute could silently persist pipeline_log missing required fields).
# Fail-loud at the persist layer so prose rules in agent .md files can't be
# bypassed by an over-cautious orchestrator. See:
#   .claude/agents/newsroom-master-{bank,ck,bds}.md V4.0 Step 9 persist
#   .claude/agents/newsroom-skeptic.md V4.0 Step 5 persist

# step_4_master required keys (Master sector agent emits canonical schema).
# `skip_reasons` can be empty dict {} (all options chosen) but key MUST exist.
_STEP_4_REQUIRED: dict[str, type | tuple] = {
    "chosen_question_idx": int,
    "chosen_pick_reason": str,
    "skip_reasons": dict,
    "data_trail": list,
}

# step_5_skeptic required keys (Skeptic agent emits canonical schema). Key is
# `skeptic_data_trail` (NOT `data_trail` like Master) — V4.0 schema explicit.
_STEP_5_REQUIRED: dict[str, type | tuple] = {
    "angle": str,
    "verdict": str,
    "skeptic_data_trail": list,
}

# Non-empty constraint — these fields must have len > 0 after type check.
_NON_EMPTY_FIELDS: dict[str, set[str]] = {
    "step_4_master": {"chosen_pick_reason", "data_trail"},
    "step_5_skeptic": {"angle", "verdict", "skeptic_data_trail"},
}


def validate_pipeline_step(step_key: str, payload: dict) -> None:
    """Raise ValueError if `payload` missing required fields for `step_key`.

    Only enforced for agent-emitted steps (step_4_master, step_5_skeptic);
    observability-only steps (step_1_crawler, step_6_render, …) accept any
    payload shape. Call AFTER merge so partial observability updates from
    orchestrator are checked against the full merged state — this catches
    the orchestrator-self-execute regression where agent never persisted
    the canonical schema in the first place.
    """
    required_map = {
        "step_4_master": _STEP_4_REQUIRED,
        "step_5_skeptic": _STEP_5_REQUIRED,
    }
    required = required_map.get(step_key)
    if not required:
        return  # observability-only step — no schema contract

    missing = []
    wrong_type = []
    empty = []
    for field, expected_type in required.items():
        if field not in payload:
            missing.append(field)
            continue
        value = payload[field]
        if not isinstance(value, expected_type):
            wrong_type.append(f"{field} (got {type(value).__name__}, expected {expected_type.__name__})")
            continue
        if field in _NON_EMPTY_FIELDS.get(step_key, set()) and not value:
            empty.append(field)

    if missing or wrong_type or empty:
        errors = []
        if missing:
            errors.append(f"missing keys: {missing}")
        if wrong_type:
            errors.append(f"wrong type: {wrong_type}")
        if empty:
            errors.append(f"empty (must be non-empty): {empty}")
        raise ValueError(
            f"pipeline_log[{step_key!r}] schema violation — {'; '.join(errors)}. "
            f"This usually means the {step_key} subagent was bypassed (orchestrator "
            f"self-executed inline). MUST dispatch via Task tool to enforce schema."
        )


def parse_task_usage(task_return: str | None) -> int | None:
    """Defensive parse of '<usage>total_tokens: N ...</usage>' block.

    Returns None if block absent or unparseable — never raises.
    Used by orchestrator to capture per-step token counts from Task tool returns
    when available; treat None as expected (orchestrator-self-runs steps cannot
    introspect their own tokens, and Task return format is not contractually
    guaranteed).
    """
    if not task_return:
        return None
    try:
        m = re.search(r"<usage>[^<]*total_tokens:\s*(\d+)", task_return)
        return int(m.group(1)) if m else None
    except (ValueError, AttributeError, TypeError):
        return None


class PipelineDB:
    """SQLite handle for crawl_log + generated_news."""

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        self.conn = sqlite3.connect(self.path, timeout=30.0)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        # Phase G T1 — WAL mode for concurrent multi-pipeline writes.
        # synchronous=NORMAL is safe with WAL (durability preserved per checkpoint).
        # Skip pragmas for in-memory DBs (WAL not applicable, raises error).
        if self.path != ":memory:":
            self.conn.execute("PRAGMA journal_mode=WAL")
            self.conn.execute("PRAGMA synchronous=NORMAL")

    def init_schema(self, schema_path: str | Path) -> None:
        sql = Path(schema_path).read_text(encoding="utf-8")
        self.conn.executescript(sql)
        self.conn.commit()

    def list_tables(self) -> list[str]:
        cur = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        return [r["name"] for r in cur.fetchall()]

    def insert_crawl_row(self, data: dict[str, Any]) -> str:
        cols = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        sql = f"INSERT INTO crawl_log ({cols}) VALUES ({placeholders})"
        self.conn.execute(sql, list(data.values()))
        self.conn.commit()
        return data["row_id"]

    def get_crawl_row(self, row_id: str) -> dict[str, Any] | None:
        cur = self.conn.execute("SELECT * FROM crawl_log WHERE row_id = ?", (row_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def update_crawl_row(self, row_id: str, updates: dict[str, Any]) -> None:
        if not updates:
            return
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        sql = f"UPDATE crawl_log SET {set_clause} WHERE row_id = ?"
        self.conn.execute(sql, [*updates.values(), row_id])
        self.conn.commit()

    def query_by_funnel_batch(self, batch_id: str) -> list[dict[str, Any]]:
        cur = self.conn.execute(
            "SELECT * FROM crawl_log WHERE funnel_batch_id = ? ORDER BY crawled_at DESC",
            (batch_id,),
        )
        return [dict(r) for r in cur.fetchall()]

    def query_pending_for_editor(self) -> list[dict[str, Any]]:
        cur = self.conn.execute(
            "SELECT * FROM crawl_log WHERE status = 'pending' AND editor_v1_decision IS NULL"
        )
        return [dict(r) for r in cur.fetchall()]

    def insert_generated_news(self, data: dict[str, Any]) -> str:
        # V4.0 Phase H2 — validate pipeline_log schema BEFORE insert. Master
        # agents persist via this method with full step_4_master payload; if
        # the payload is missing required fields (skip_reasons / data_trail /
        # chosen_pick_reason / chosen_question_idx), refuse the write so
        # the bug surfaces immediately instead of polluting DB + viewer.
        raw_log = data.get("pipeline_log")
        if raw_log:
            try:
                log = json.loads(raw_log) if isinstance(raw_log, str) else raw_log
            except (json.JSONDecodeError, TypeError):
                log = {}
            for step_key in ("step_4_master", "step_5_skeptic"):
                if step_key in log:
                    validate_pipeline_step(step_key, log[step_key])

        cols = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        sql = f"INSERT INTO generated_news ({cols}) VALUES ({placeholders})"
        self.conn.execute(sql, list(data.values()))
        self.conn.commit()
        return data["article_id"]

    def update_generated_news(self, article_id: str, updates: dict[str, Any]) -> None:
        if not updates:
            return
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        sql = f"UPDATE generated_news SET {set_clause} WHERE article_id = ?"
        self.conn.execute(sql, [*updates.values(), article_id])
        self.conn.commit()

    def log_pipeline_step(self, article_id: str, step_key: str, payload: dict) -> None:
        """Shallow-MERGE payload into pipeline_log[step_key]. Existing keys
        preserved; payload keys override on conflict.

        Phase G hotfix (2026-05-10): previous overwrite semantics caused agent-
        persisted fields (Master `data_trail`, Skeptic `skeptic_data_trail`)
        to be wiped when orchestrator subsequently logged observability
        payload (model + duration + tokens + count). Merge preserves both:
        - Master persists step_4_master = {data_trail, gates_passed, ...}
        - Orchestrator merges step_4_master += {model, duration_ms, tokens, count}
        - Result: step_4_master has data_trail + observability together.

        Schema convention:
        - step_1_crawler / step_6_render: orchestrator self-runs, tokens=None
        - step_2_editor / step_3_story_editor / step_4_master / step_5_skeptic:
          Task-dispatched, tokens parsed from <usage> if available else None

        Batch-level steps (1, 2, 3, 6) duplicate across N articles in same
        batch by design — each article's pipeline_log is self-contained.

        No-op if article_id does not exist (graceful — agent retry safe).
        """
        cur = self.conn.execute(
            "SELECT pipeline_log FROM generated_news WHERE article_id = ?",
            (article_id,),
        )
        row = cur.fetchone()
        if not row:
            return
        log = json.loads(row["pipeline_log"]) if row["pipeline_log"] else {}
        # Phase G hotfix: shallow merge preserves agent-persisted fields
        log[step_key] = {**log.get(step_key, {}), **payload}
        # V4.0 Phase H2 — validate merged state against canonical schema for
        # agent-emitted steps. Catches orchestrator-self-execute regression:
        # if agent never persisted the canonical schema first, orchestrator
        # observability merge (model + duration_ms) leaves step_4/step_5
        # missing required fields → ValueError → cannot silently proceed.
        validate_pipeline_step(step_key, log[step_key])
        self.conn.execute(
            "UPDATE generated_news SET pipeline_log = ? WHERE article_id = ?",
            (json.dumps(log, ensure_ascii=False), article_id),
        )
        self.conn.commit()

    def recent_generated_news(self, ticker: str, limit: int = 3) -> list[dict[str, Any]]:
        cur = self.conn.execute(
            "SELECT * FROM generated_news WHERE ticker = ? AND status = 'published' "
            "ORDER BY published_at DESC LIMIT ?",
            (ticker, limit),
        )
        return [dict(r) for r in cur.fetchall()]

    def close(self) -> None:
        self.conn.close()
