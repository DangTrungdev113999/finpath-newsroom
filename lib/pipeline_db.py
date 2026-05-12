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

# V5.1 — Observability fields required across ALL agent-emitted steps for V5.0+.
_OBSERVABILITY_REQUIRED: dict[str, type | tuple] = {
    "model": str,
    "duration_ms": int,
}

# step_4_master V4.0 baseline (NO observability — back-compat).
# `skip_reasons` can be empty dict {} (all options chosen) but key MUST exist.
_STEP_4_REQUIRED_V4: dict[str, type | tuple] = {
    "chosen_question_idx": int,
    "chosen_pick_reason": str,
    "skip_reasons": dict,
    "data_trail": list,
}

# step_4_master V5.0 extension: adds format_id_used + observability.
_STEP_4_REQUIRED_V5: dict[str, type | tuple] = {
    **_STEP_4_REQUIRED_V4,
    **_OBSERVABILITY_REQUIRED,
    "format_id_used": str,
}

# step_5_skeptic V4.0 baseline (key is `skeptic_data_trail`, not `data_trail`).
_STEP_5_REQUIRED_V4: dict[str, type | tuple] = {
    "angle": str,
    "verdict": str,
    "skeptic_data_trail": list,
}

# step_5_skeptic V5.0 (adds observability).
_STEP_5_REQUIRED_V5: dict[str, type | tuple] = {
    **_STEP_5_REQUIRED_V4,
    **_OBSERVABILITY_REQUIRED,
}

# step_3_5_format_director — NEW in V5.0.
_STEP_3_5_REQUIRED: dict[str, type | tuple] = {
    **_OBSERVABILITY_REQUIRED,
    "format_picks": list,
}

# V5.1 — Headline Craft step (Plan C — newsroom-headline-craft agent).
# `hard_criteria_pass` is V1.1 nested dict structure — payload schema enforces
# shape only; fail-loud check on `final_title` against check_hard_criteria
# happens in validate_pipeline_step (V5.1+ gate) so weak titles cannot persist.
_STEP_4_5_REQUIRED: dict[str, type | tuple] = {
    **_OBSERVABILITY_REQUIRED,
    "final_title": str,
    "final_loi": str,
    "picked_score": int,
    "candidates": list,
    "hard_criteria_pass": dict,
}

# Non-empty constraint per step (baseline — V5.0 dynamically adds `model`).
_NON_EMPTY_FIELDS: dict[str, set[str]] = {
    "step_4_master": {"chosen_pick_reason", "data_trail"},
    "step_5_skeptic": {"angle", "verdict", "skeptic_data_trail"},
    "step_3_5_format_director": {"format_picks"},
    "step_4_5_headline_craft": {"final_title", "final_loi"},
}


def _version_ge(a: str, b: str) -> bool:
    """Compare pipeline_version strings like 'V5.0' >= 'V4.0'."""
    def _parse(v: str) -> tuple[int, ...]:
        try:
            return tuple(int(p) for p in v.lstrip("Vv").split("."))
        except (ValueError, AttributeError):
            return (0,)
    return _parse(a) >= _parse(b)


def validate_pipeline_step(step_key: str, payload: dict, pipeline_version: str = "V4.0") -> None:
    """Raise ValueError if `payload` missing required fields for `step_key`.

    Version-aware (V5.0 Phase 1.4 + V5.1 observability):
    - V4.0 and earlier: enforce step_4 + step_5 baselines (no observability).
    - V5.0+: + step_3_5_format_director, step_4.format_id_used required,
      AND observability fields across step_3_5/4/5.

    Only enforced for agent-emitted steps; observability-only steps
    (step_1_crawler, step_6_render, …) accept any payload shape. Call AFTER
    merge so partial observability updates from orchestrator are checked
    against the full merged state — this catches the orchestrator-
    self-execute regression where agent never persisted the canonical
    schema in the first place.
    """
    is_v5_plus = _version_ge(pipeline_version, "V5.0")
    is_v5_1_plus = _version_ge(pipeline_version, "V5.1")

    required_map: dict[str, dict[str, type | tuple]] = {
        "step_4_master": _STEP_4_REQUIRED_V5 if is_v5_plus else _STEP_4_REQUIRED_V4,
        "step_5_skeptic": _STEP_5_REQUIRED_V5 if is_v5_plus else _STEP_5_REQUIRED_V4,
    }
    if is_v5_plus:
        required_map["step_3_5_format_director"] = _STEP_3_5_REQUIRED
    if is_v5_1_plus:
        required_map["step_4_5_headline_craft"] = _STEP_4_5_REQUIRED

    non_empty_fields = dict(_NON_EMPTY_FIELDS)
    if is_v5_plus:
        for step in ("step_4_master", "step_5_skeptic", "step_3_5_format_director"):
            non_empty_fields[step] = non_empty_fields.get(step, set()) | {"model"}
    if is_v5_1_plus:
        non_empty_fields["step_4_5_headline_craft"] = (
            non_empty_fields.get("step_4_5_headline_craft", set()) | {"model"}
        )

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
        if field in non_empty_fields.get(step_key, set()) and not value:
            empty.append(field)

    # Entry-level checks for data_trail arrays — each entry MUST be dict with
    # at least `source` key (V4.0 canonical). VHM run 2026-05-11 caught a
    # Master BĐS dispatch that emitted legacy V3.6 string entries like
    # "KB:bds-... — mechanism description" → frontend DataTrail.tsx crashed
    # on `source.startsWith()` because entry was string not dict.
    bad_entries: list[str] = []
    entry_field_map = {
        "step_4_master": "data_trail",
        "step_5_skeptic": "skeptic_data_trail",
    }
    entry_field = entry_field_map.get(step_key)
    if entry_field and entry_field in payload and isinstance(payload[entry_field], list):
        for idx, entry in enumerate(payload[entry_field]):
            if not isinstance(entry, dict):
                bad_entries.append(f"{entry_field}[{idx}] is {type(entry).__name__} (must be dict)")
            elif "source" not in entry or not entry.get("source"):
                bad_entries.append(f"{entry_field}[{idx}] missing/empty 'source' key")

    if missing or wrong_type or empty or bad_entries:
        errors = []
        if missing:
            errors.append(f"missing keys: {missing}")
        if wrong_type:
            errors.append(f"wrong type: {wrong_type}")
        if empty:
            errors.append(f"empty (must be non-empty): {empty}")
        if bad_entries:
            errors.append(f"bad entries: {bad_entries}")
        raise ValueError(
            f"pipeline_log[{step_key!r}] schema violation (version={pipeline_version}) — "
            f"{'; '.join(errors)}. This usually means the {step_key} subagent was bypassed "
            f"(orchestrator self-executed inline) or emitted legacy schema. "
            f"V4.0 canonical: data_trail entries MUST be dicts with `source` key. "
            f"V5.0+ requires observability (model + duration_ms). "
            f"MUST dispatch via Task tool to enforce schema."
        )

    # V5.1 — step_4_5_headline_craft fail-loud: final_title MUST pass 5 V1.1
    # hard criteria (ticker_present + word_count_le_12 + hook_strong{tension,
    # click_test} + binh_dan_nguy_hiem{plain_language, sharp_edge} + no_em_dash).
    # Orchestrator cannot silently persist a weak title; Headline agent MUST
    # regenerate (max 2 retry) before this validate succeeds.
    if step_key == "step_4_5_headline_craft" and is_v5_1_plus:
        from lib.headline_scorer import check_hard_criteria
        title = payload.get("final_title", "")
        if title:  # basic non-empty already enforced above; defensive
            hc = check_hard_criteria(title)
            if not hc.get("passed", False):
                failed_keys: list[str] = []
                if not hc.get("ticker_present"):
                    failed_keys.append("ticker_present")
                if not hc.get("word_count_le_12"):
                    failed_keys.append("word_count_le_12")
                hook = hc.get("hook_strong", {})
                if not (hook.get("tension_present") and hook.get("click_test_pass")):
                    failed_keys.append("hook_strong")
                bd = hc.get("binh_dan_nguy_hiem", {})
                if not (bd.get("plain_language") and bd.get("sharp_edge")):
                    failed_keys.append("binh_dan_nguy_hiem")
                if not hc.get("no_em_dash"):
                    failed_keys.append("no_em_dash")
                raise ValueError(
                    f"pipeline_log[step_4_5_headline_craft].final_title fails hard criteria: "
                    f"{failed_keys} — title={title!r}. Headline agent emitted weak title; "
                    f"MUST regenerate (max 2 retry) before persist."
                )


# V5.1.3 (F-5) — crawl_log schema validation after Editor V1 routes a row.
# Routed rows (editor_v1_decision = "route_to_story_editor") MUST carry the
# 4 Finpath-driven fields: sector_code, sector_name, sector_parent, master_route.
# sector_parent may be empty string (top-level sectors like oilGas have pn="").
# master_route MUST belong to _MASTER_ROUTE_VALID — fail-loud if Finpath returns
# a sector_code not in data/sector_routing.yaml or if Editor V1 forgets to
# call get_master_route(). Rejected rows skip validation entirely.
_CRAWL_LOG_V5_1_3_FIELDS: dict[str, type] = {
    "sector_code": str,
    "sector_name": str,
    "sector_parent": str,
    "master_route": str,
}

_MASTER_ROUTE_VALID: set[str] = {
    "bank", "ck", "bds",
    "oilgas", "logistics", "fb", "apparel", "retail", "seafood", "defensive",
}


def validate_crawl_log_v5_1_3(row: dict) -> None:
    """Validate V5.1.3 crawl_log fields after Editor V1.

    Routed rows MUST have 4 fields: sector_code, sector_name, sector_parent,
    master_route. sector_parent may be empty string. master_route MUST belong
    to _MASTER_ROUTE_VALID. Rejected rows skip validation.
    """
    if row.get("editor_v1_decision") != "route_to_story_editor":
        return
    for field, expected_type in _CRAWL_LOG_V5_1_3_FIELDS.items():
        if field not in row or row[field] is None:
            raise ValueError(f"crawl_log V5.1.3 missing field: {field}")
        if not isinstance(row[field], expected_type):
            raise ValueError(
                f"crawl_log {field} must be {expected_type.__name__}, "
                f"got {type(row[field]).__name__}"
            )
    if row["master_route"] not in _MASTER_ROUTE_VALID:
        raise ValueError(
            f"master_route '{row['master_route']}' invalid. "
            f"Valid: {sorted(_MASTER_ROUTE_VALID)}"
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
        # V5.1.3 (F-1) — apply additive migrations from lib/migrations/*.sql.
        # Idempotent via CREATE TABLE IF NOT EXISTS; runs before init_schema so
        # any legacy schema load still works. Tables created here are
        # independent of the canonical crawl_log + generated_news schema.
        self._apply_migrations()
        # V5.1.4 (H-1) — conditional ALTER TABLE for crawl_log session grouping
        # + V5.1.3 sector fields. Idempotent (PRAGMA table_info check) but
        # `ALTER TABLE ADD COLUMN` is NOT, so a Python helper is required
        # instead of a .sql migration. No-op on fresh DBs (tables don't exist
        # yet — caller will run init_schema next, which re-invokes these).
        # Safe on reopen.
        self._upgrade_crawl_log_schema()
        self._upgrade_generated_news_schema()

    def _apply_migrations(self) -> None:
        """Apply migration SQL files from lib/migrations/ in alphabetical order.

        Idempotent — each migration MUST use CREATE TABLE IF NOT EXISTS /
        CREATE INDEX IF NOT EXISTS so re-running on an existing DB is safe.
        Naming convention: YYYY-MM-DD-<slug>.sql so sorted() = chronological.
        """
        migrations_dir = Path(__file__).parent / "migrations"
        if not migrations_dir.exists():
            return
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            sql = migration_file.read_text(encoding="utf-8")
            self.conn.executescript(sql)
        self.conn.commit()

    def _upgrade_crawl_log_schema(self) -> None:
        """Conditional ALTER TABLE for non-idempotent column additions (V5.1.4 H-1).

        SQLite doesn't support `ADD COLUMN IF NOT EXISTS`, so we check
        PRAGMA table_info first. Indexes use IF NOT EXISTS so they're
        safe to re-run.

        Plan H session grouping fields: session_id, trigger_type, trigger_args.

        No-op when `crawl_log` table doesn't exist yet (fresh DB before
        init_schema has run). Called from both __init__ (handles reopens)
        AND init_schema (handles fresh bootstrap). Both call sites are
        idempotent thanks to the table-exists guard + per-column check.
        """
        cur = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='crawl_log'"
        )
        if cur.fetchone() is None:
            return  # crawl_log not bootstrapped yet — init_schema will retry.
        cur = self.conn.execute("PRAGMA table_info(crawl_log)")
        existing = {row["name"] for row in cur.fetchall()}
        # V5.1.4 H-1 (session grouping) + V5.1.3 (Finpath sectors routing).
        # NOTE: legacy `sector` column (kept as alias for sector_name) already
        # exists in canonical schema.sql, so it's NOT in this list.
        for col in (
            "session_id", "trigger_type", "trigger_args",
            "sector_code", "sector_name", "sector_parent", "master_route",
        ):
            if col not in existing:
                self.conn.execute(f"ALTER TABLE crawl_log ADD COLUMN {col} TEXT")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_crawl_log_session ON crawl_log(session_id)"
        )
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_crawl_log_crawled_desc ON crawl_log(crawled_at DESC)"
        )
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_crawl_log_master_route ON crawl_log(master_route)"
        )
        self.conn.commit()

    def _upgrade_generated_news_schema(self) -> None:
        """Conditional ALTER TABLE for generated_news V1.1 Headline Craft +
        V5.1.3 sector fields. Same idempotency pattern as crawl_log upgrade.
        """
        cur = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='generated_news'"
        )
        if cur.fetchone() is None:
            return
        cur = self.conn.execute("PRAGMA table_info(generated_news)")
        existing = {row["name"] for row in cur.fetchall()}
        # V1.1 Headline Craft (Plan C C-6) — final crafted title from Step 4.5
        # V5.1.3 sector fields — denormalized from crawl_log for downstream consumers
        for col in (
            "headline_final",
            "sector_code", "master_route",
        ):
            if col not in existing:
                self.conn.execute(f"ALTER TABLE generated_news ADD COLUMN {col} TEXT")
        self.conn.commit()

    def init_schema(self, schema_path: str | Path) -> None:
        sql = Path(schema_path).read_text(encoding="utf-8")
        self.conn.executescript(sql)
        self.conn.commit()
        # V5.1.4 (H-1) — re-run crawl_log upgrade so fresh-bootstrap callers
        # (canonical pattern: PipelineDB() + init_schema()) get the session
        # grouping columns + V5.1.3 sector fields. On reopen the __init__ call
        # already handled it and this is a no-op via per-column existence check.
        self._upgrade_crawl_log_schema()
        self._upgrade_generated_news_schema()

    def list_tables(self) -> list[str]:
        cur = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        return [r["name"] for r in cur.fetchall()]

    def insert_crawl_row(self, data: dict[str, Any]) -> str:
        """Insert a crawl_log row. Generic dict-driven INSERT — any subset of
        existing columns is accepted (column names must match schema).

        V5.1.4 / Plan H Task 2 — session grouping fields are optional:
            session_id (TEXT, nullable)   — UUID shared across all crawl_log
                                            rows in one pipeline trigger.
            trigger_type (TEXT, nullable) — 'tin' | 'tin-hot' | 'tin-batch'.
            trigger_args (TEXT, nullable) — ticker for 'tin', 'N=3' for
                                            'tin-hot', etc.
        Legacy callers omitting these keys still work — columns default to
        NULL by the H-1 ALTER TABLE migration.

        Returns the row_id supplied by the caller (caller manages UUID
        generation — see lib/stages/run_crawler.py::write_candidate_to_db).
        """
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
        # V5.0 Phase 1.3 (B-3) — default pipeline_version to V5.0 unless caller
        # specifies. Existing rows (V3.6/V4.0) preserved via schema DEFAULT;
        # only NEW inserts via this method get V5.0 → enables version-gate
        # validation downstream (B-4 adds pipeline_version kwarg to
        # validate_pipeline_step). Mutation guard: don't mutate caller's dict.
        data = {**data}
        if "pipeline_version" not in data:
            data["pipeline_version"] = "V5.0"

        # V4.0 Phase H2 — validate pipeline_log schema BEFORE insert. Master
        # agents persist via this method with full step_4_master payload; if
        # the payload is missing required fields (skip_reasons / data_trail /
        # chosen_pick_reason / chosen_question_idx), refuse the write so
        # the bug surfaces immediately instead of polluting DB + viewer.
        # V5.0 Phase 1.4 (B-4) — passes pipeline_version from data so
        # version-gated checks (V5.0 observability + format_id_used + step_3_5)
        # only apply to V5.0+ rows.
        raw_log = data.get("pipeline_log")
        if raw_log:
            try:
                log = json.loads(raw_log) if isinstance(raw_log, str) else raw_log
            except (json.JSONDecodeError, TypeError):
                log = {}
            for step_key in ("step_3_5_format_director", "step_4_master", "step_5_skeptic"):
                if step_key in log:
                    validate_pipeline_step(
                        step_key, log[step_key], pipeline_version=data["pipeline_version"]
                    )

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
            "SELECT pipeline_log, pipeline_version FROM generated_news WHERE article_id = ?",
            (article_id,),
        )
        row = cur.fetchone()
        if not row:
            return
        # V5.0 Phase 1.4 (B-4) — read row's pipeline_version to apply
        # version-aware schema validation. V3.6/V4.0 rows skip V5.0-only
        # checks (format_id_used, observability, step_3_5_format_director).
        pipeline_version = (
            row["pipeline_version"] if "pipeline_version" in row.keys() else "V4.0"
        )
        log = json.loads(row["pipeline_log"]) if row["pipeline_log"] else {}
        # Phase G hotfix: shallow merge preserves agent-persisted fields
        log[step_key] = {**log.get(step_key, {}), **payload}
        # V4.0 Phase H2 — validate merged state against canonical schema for
        # agent-emitted steps. Catches orchestrator-self-execute regression:
        # if agent never persisted the canonical schema first, orchestrator
        # observability merge (model + duration_ms) leaves step_4/step_5
        # missing required fields → ValueError → cannot silently proceed.
        validate_pipeline_step(step_key, log[step_key], pipeline_version=pipeline_version)
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
