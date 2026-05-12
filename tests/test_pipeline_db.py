"""Tests for lib.pipeline_db — SQLite ops on crawl_log + generated_news."""
import json
import pytest
from pathlib import Path

from lib.pipeline_db import PipelineDB, parse_task_usage, validate_pipeline_step


@pytest.fixture
def db():
    """Fresh in-memory DB initialized with schema."""
    schema_path = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db = PipelineDB(":memory:")
    db.init_schema(schema_path)
    yield db
    db.close()


def test_init_schema_creates_tables(db):
    """Schema init creates crawl_log + generated_news tables."""
    tables = db.list_tables()
    assert "crawl_log" in tables
    assert "generated_news" in tables


def test_insert_crawl_row_returns_row_id(db):
    """insert_crawl_row returns the row_id used."""
    row_id = db.insert_crawl_row({
        "row_id": "uuid-1",
        "funnel_batch_id": "VCB-20260508-1530",
        "ticker": "VCB",
        "source_name": "Báo Pháp luật",
        "source_url": "https://example.com/a1",
        "title": "Test article",
        "crawled_at": "2026-05-08T15:30:00+07:00",
    })
    assert row_id == "uuid-1"


def test_insert_duplicate_url_raises(db):
    """Inserting same source_url twice raises (UNIQUE constraint)."""
    base = {
        "funnel_batch_id": "VCB-20260508-1530",
        "ticker": "VCB",
        "source_name": "X",
        "source_url": "https://example.com/dup",
        "title": "T",
        "crawled_at": "2026-05-08T00:00:00+07:00",
    }
    db.insert_crawl_row({"row_id": "u1", **base})
    with pytest.raises(Exception):
        db.insert_crawl_row({"row_id": "u2", **base})


def test_get_crawl_row_returns_dict(db):
    """get_crawl_row returns dict with all fields, None for unset."""
    db.insert_crawl_row({
        "row_id": "uuid-2",
        "funnel_batch_id": "TCB-20260508-1530",
        "ticker": "TCB",
        "source_name": "VnEconomy",
        "source_url": "https://example.com/a2",
        "title": "T2",
        "crawled_at": "2026-05-08T00:00:00+07:00",
    })
    row = db.get_crawl_row("uuid-2")
    assert row["ticker"] == "TCB"
    assert row["status"] == "pending"
    assert row["editor_v1_decision"] is None


def test_update_crawl_row_partial(db):
    """update_crawl_row updates only the keys passed."""
    db.insert_crawl_row({
        "row_id": "uuid-3",
        "funnel_batch_id": "B",
        "ticker": "VCB",
        "source_name": "X",
        "source_url": "https://example.com/a3",
        "title": "T",
        "crawled_at": "2026-05-08T00:00:00+07:00",
    })
    db.update_crawl_row("uuid-3", {
        "editor_v1_decision": "route_to_story_editor",
        "primary_ticker": "VCB",
        "sector": "Bank",
    })
    row = db.get_crawl_row("uuid-3")
    assert row["editor_v1_decision"] == "route_to_story_editor"
    assert row["sector"] == "Bank"
    assert row["title"] == "T"


def test_query_by_funnel_batch(db):
    """query_by_funnel_batch returns all rows for batch_id, sorted by crawled_at desc."""
    for i, ts in enumerate(["2026-05-08T10:00:00+07:00", "2026-05-08T12:00:00+07:00"]):
        db.insert_crawl_row({
            "row_id": f"u{i}",
            "funnel_batch_id": "VCB-20260508-1530",
            "ticker": "VCB",
            "source_name": f"S{i}",
            "source_url": f"https://example.com/{i}",
            "title": "T",
            "crawled_at": ts,
        })
    rows = db.query_by_funnel_batch("VCB-20260508-1530")
    assert len(rows) == 2
    assert rows[0]["crawled_at"] == "2026-05-08T12:00:00+07:00"


def test_insert_generated_news_links_to_crawl_row(db):
    """generated_news insert with row_id FK works + recent_generated_news queries it."""
    db.insert_crawl_row({
        "row_id": "u-anchor",
        "funnel_batch_id": "B",
        "ticker": "VCB",
        "source_name": "X",
        "source_url": "https://example.com/anchor",
        "title": "T",
        "crawled_at": "2026-05-08T00:00:00+07:00",
    })
    aid = db.insert_generated_news({
        "article_id": "art-1",
        "row_id": "u-anchor",
        "ticker": "VCB",
        "sector": "Bank",
        "title": "Article title",
        "body": "Body...",
        "word_count": 354,
        "accepted_hypothesis": 1,
        "status": "published",
        "published_at": "2026-05-08T16:00:00+07:00",
    })
    assert aid == "art-1"
    arts = db.recent_generated_news("VCB", limit=3)
    assert len(arts) == 1
    assert arts[0]["title"] == "Article title"


# ---------------------------------------------------------------------------
# Phase F T10 — per-step observability (log_pipeline_step + parse_task_usage)
# ---------------------------------------------------------------------------


def _seed_article(db, article_id: str = "art-obs", pipeline_log: str | None = None):
    """Helper: insert a minimal crawl_log + generated_news row for obs tests."""
    db.insert_crawl_row({
        "row_id": f"row-{article_id}",
        "funnel_batch_id": "VCB-20260508-1530",
        "ticker": "VCB",
        "source_name": "X",
        "source_url": f"https://example.com/{article_id}",
        "title": "T",
        "crawled_at": "2026-05-08T00:00:00+07:00",
    })
    payload = {
        "article_id": article_id,
        "row_id": f"row-{article_id}",
        "ticker": "VCB",
        "sector": "Bank",
        "title": "Article",
        "body": "Body...",
        "word_count": 300,
        "accepted_hypothesis": 1,
        "status": "draft",
        # V4.0 baseline for legacy merge-behavior tests. New V5.0 tests must
        # override by passing pipeline_version="V5.0" + full V5.0 schema fields.
        "pipeline_version": "V4.0",
    }
    if pipeline_log is not None:
        payload["pipeline_log"] = pipeline_log
    db.insert_generated_news(payload)


def test_log_pipeline_step_creates_entry(db):
    """Empty pipeline_log → log_pipeline_step writes step_1 entry."""
    _seed_article(db, "art-1")
    db.log_pipeline_step("art-1", "step_1_crawler", {
        "model": "sonnet",
        "duration_ms": 1234,
        "tokens": None,
        "candidates_count": 10,
    })
    row = db.conn.execute(
        "SELECT pipeline_log FROM generated_news WHERE article_id = 'art-1'"
    ).fetchone()
    log = json.loads(row["pipeline_log"])
    assert "step_1_crawler" in log
    assert log["step_1_crawler"]["model"] == "sonnet"
    assert log["step_1_crawler"]["duration_ms"] == 1234
    assert log["step_1_crawler"]["tokens"] is None
    assert log["step_1_crawler"]["candidates_count"] == 10


_VALID_STEP_4 = {
    "chosen_question_idx": 0,
    "chosen_pick_reason": "Tension paradox đáng đào sâu",
    "skip_reasons": {},
    "data_trail": [{"source": "Finpath_API/income", "fetched": "Q1 ROE", "purpose": "verify", "supports_argument": "B1"}],
}


def test_log_pipeline_step_merges_existing(db):
    """log_pipeline_step adds step_4 to existing pipeline_log with step_3 → both present.

    Step_4 first persisted with canonical schema (agent), then orchestrator
    merges observability — final state has both halves.
    """
    existing = json.dumps({"step_3_story_editor": {"model": "opus", "duration_ms": 5000, "tokens": 12000}})
    _seed_article(db, "art-2", pipeline_log=existing)
    # Agent persists canonical schema first
    db.log_pipeline_step("art-2", "step_4_master", _VALID_STEP_4)
    # Orchestrator merges observability
    db.log_pipeline_step("art-2", "step_4_master", {
        "model": "opus",
        "duration_ms": 8000,
        "tokens": 25000,
    })
    row = db.conn.execute(
        "SELECT pipeline_log FROM generated_news WHERE article_id = 'art-2'"
    ).fetchone()
    log = json.loads(row["pipeline_log"])
    assert "step_3_story_editor" in log
    assert "step_4_master" in log
    assert log["step_3_story_editor"]["tokens"] == 12000
    assert log["step_4_master"]["tokens"] == 25000
    # Canonical schema preserved by merge
    assert log["step_4_master"]["chosen_question_idx"] == 0


def test_log_pipeline_step_same_key_merges_with_collision_override(db):
    """Twice with same step_key: keys conflict → latest payload wins; non-conflicting keys preserved.

    Uses step_1_crawler (no schema contract) to isolate collision logic from
    schema validation — Phase H2 step_4_master would reject incomplete payloads.
    """
    _seed_article(db, "art-3")
    db.log_pipeline_step("art-3", "step_1_crawler", {"duration_ms": 1000, "tokens": 5000})
    db.log_pipeline_step("art-3", "step_1_crawler", {"duration_ms": 2000, "tokens": 10000})
    row = db.conn.execute(
        "SELECT pipeline_log FROM generated_news WHERE article_id = 'art-3'"
    ).fetchone()
    log = json.loads(row["pipeline_log"])
    assert log["step_1_crawler"]["duration_ms"] == 2000
    assert log["step_1_crawler"]["tokens"] == 10000
    # Only one entry for step_1_crawler
    assert list(log.keys()) == ["step_1_crawler"]


def test_log_pipeline_step_merges_preserve_existing_subkeys(db):
    """Phase G hotfix — Master agent persists data_trail first, orchestrator
    later logs observability payload. MERGE semantic preserves data_trail
    even though orchestrator payload doesn't include it.
    """
    _seed_article(db, "art-merge")
    # Step 1: Master agent persists step_4_master with full canonical schema
    db.log_pipeline_step("art-merge", "step_4_master", {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "Pick because Q1 paradox cot loi",
        "skip_reasons": {},
        "data_trail": [
            {"source": "https://x", "fetched": "Q1 ROE 21,2%", "purpose": "verify", "supports_argument": "Bullet 1"}
        ],
        "gates_passed": True,
    })
    # Step 2: Orchestrator logs observability — does NOT include data_trail
    db.log_pipeline_step("art-merge", "step_4_master", {
        "model": "opus",
        "duration_ms": 60000,
        "tokens": None,
        "data_trail_count": 1,
    })
    row = db.conn.execute(
        "SELECT pipeline_log FROM generated_news WHERE article_id = 'art-merge'"
    ).fetchone()
    log = json.loads(row["pipeline_log"])
    s4 = log["step_4_master"]
    # data_trail array PRESERVED (was wiped by old overwrite logic)
    assert "data_trail" in s4
    assert len(s4["data_trail"]) == 1
    assert s4["data_trail"][0]["purpose"] == "verify"
    # Master fields preserved
    assert s4["gates_passed"] is True
    assert s4["chosen_question_idx"] == 0
    # Orchestrator fields added
    assert s4["model"] == "opus"
    assert s4["duration_ms"] == 60000
    assert s4["data_trail_count"] == 1


def test_log_pipeline_step_missing_article_id_noop(db):
    """Non-existent article_id → no error, no insert."""
    # Should not raise
    db.log_pipeline_step("does-not-exist", "step_1_crawler", {"model": "sonnet"})
    # Verify no row was inserted
    row = db.conn.execute(
        "SELECT * FROM generated_news WHERE article_id = 'does-not-exist'"
    ).fetchone()
    assert row is None


def test_parse_task_usage_present():
    """Input with <usage>total_tokens: N ...</usage> → returns N."""
    text = "Result text\n<usage>total_tokens: 5000 tool_uses: 10</usage>"
    assert parse_task_usage(text) == 5000


def test_parse_task_usage_absent():
    """Input without <usage> block → None."""
    assert parse_task_usage("No usage block here") is None


def test_parse_task_usage_empty():
    """Empty string or None → None."""
    assert parse_task_usage("") is None
    assert parse_task_usage(None) is None


def test_parse_task_usage_malformed():
    """Malformed <usage> block (no total_tokens) → None, no exception."""
    assert parse_task_usage("<usage>broken format</usage>") is None
    assert parse_task_usage("<usage>total_tokens: not_a_number</usage>") is None
    assert parse_task_usage("<usage>") is None


# ---------------------------------------------------------------------------
# Phase G T1 — WAL mode + concurrent multi-pipeline writes
# ---------------------------------------------------------------------------


def test_wal_mode_concurrent_writes_succeed(tmp_path):
    """3 subprocess writers concurrent writes via WAL mode → all succeed.

    Phase G T1 — verifies WAL mode permits concurrent multi-pipeline writes
    without 'database is locked' errors. Subprocess based (not threading)
    because real /tin-batch spawns separate Claude Code workers.
    """
    import subprocess
    from pathlib import Path

    # Setup: real disk DB initialized with schema (WAL doesn't work :memory:)
    db_path = tmp_path / "concurrent.db"
    schema_path = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db = PipelineDB(str(db_path))
    db.init_schema(schema_path)
    db.close()

    helper = Path(__file__).parent / "helpers" / "concurrent_writer.py"
    batch_id = "CONCURRENT-TEST-001"

    # Spawn 3 concurrent writers, each inserts 1 row with unique source_url
    procs = [
        subprocess.Popen(
            ["uv", "run", "python", str(helper), str(db_path), batch_id, f"https://test.example/{i}"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        for i in range(3)
    ]
    results = [p.wait(timeout=60) for p in procs]
    assert all(rc == 0 for rc in results), \
        f"Subprocess failed: {[(p.returncode, p.stderr.read().decode()) for p in procs]}"

    # Verify all 3 rows persisted
    db = PipelineDB(str(db_path))
    rows = db.query_by_funnel_batch(batch_id)
    db.close()
    assert len(rows) == 3, f"Expected 3 rows, got {len(rows)}"


# ---------------------------------------------------------------------------
# Phase G T11 — Telegram publish idempotency tracking
# ---------------------------------------------------------------------------


def test_generated_news_has_telegram_pushed_at_column(db):
    """Phase G T11 — schema includes telegram_pushed_at column."""
    cur = db.conn.execute("PRAGMA table_info(generated_news)")
    cols = {row["name"] for row in cur.fetchall()}
    assert "telegram_pushed_at" in cols, f"Missing column. Found: {sorted(cols)}"


def test_telegram_pushed_at_default_null(db):
    """Phase G T11 — telegram_pushed_at defaults to NULL on new article."""
    db.insert_crawl_row({
        "row_id": "r1",
        "funnel_batch_id": "b1",
        "source_name": "test",
        "source_url": "https://t/1",
        "title": "t",
        "ticker": "TST",
        "raw_content": "c",
        "crawled_at": "2026-05-10T00:00:00Z",
    })
    db.insert_generated_news({
        "article_id": "a1",
        "row_id": "r1",
        "ticker": "TST",
        "sector": "Bank",
        "title": "Test",
        "body": "body",
        "word_count": 100,
        "key_view": "trung lập",
        "insight_final": "i",
        "accepted_hypothesis": 1,
        "status": "draft",
        "pipeline_version": "V4.0",
    })
    cur = db.conn.execute(
        "SELECT telegram_pushed_at FROM generated_news WHERE article_id = ?",
        ("a1",),
    )
    row = cur.fetchone()
    assert row["telegram_pushed_at"] is None


# ---------------------------------------------------------------------------
# Phase H2 — pipeline_log schema validation (validate_pipeline_step)
# ---------------------------------------------------------------------------


_VALID_STEP_4_FULL = {
    "chosen_question_idx": 0,
    "chosen_pick_reason": "Tension paradox đáng đào sâu",
    "skip_reasons": {"1": "Yếu hơn", "2": "Cần data web search"},
    "data_trail": [{"source": "Finpath", "fetched": "ROE", "purpose": "verify", "supports_argument": "B1"}],
}

_VALID_STEP_5_FULL = {
    "angle": "data_skepticism",
    "verdict": "pass_with_caveats",
    "skeptic_data_trail": [{"source": "DB", "fetched": "echo", "purpose": "verify", "supports_argument": True}],
}


def test_validate_pipeline_step_accepts_full_step_4():
    """Full canonical schema → no error."""
    validate_pipeline_step("step_4_master", _VALID_STEP_4_FULL)


def test_validate_pipeline_step_accepts_full_step_5():
    """Full canonical schema → no error."""
    validate_pipeline_step("step_5_skeptic", _VALID_STEP_5_FULL)


def test_validate_pipeline_step_rejects_missing_skip_reasons():
    """skip_reasons key required even if empty dict {}."""
    payload = {**_VALID_STEP_4_FULL}
    del payload["skip_reasons"]
    with pytest.raises(ValueError, match="skip_reasons"):
        validate_pipeline_step("step_4_master", payload)


def test_validate_pipeline_step_rejects_orchestrator_observability_only():
    """Catches orchestrator inline regression: only observability fields,
    no canonical schema. ValueError must mention Task tool dispatch."""
    with pytest.raises(ValueError, match="Task tool"):
        validate_pipeline_step("step_4_master", {"model": "opus", "duration_ms": 1234})


def test_validate_pipeline_step_rejects_empty_skeptic_data_trail():
    """Skeptic data_trail must be non-empty list (V4.0 mandate)."""
    payload = {**_VALID_STEP_5_FULL, "skeptic_data_trail": []}
    with pytest.raises(ValueError, match="empty"):
        validate_pipeline_step("step_5_skeptic", payload)


def test_validate_pipeline_step_wrong_type_caught():
    """skip_reasons must be dict (not list/str/None)."""
    payload = {**_VALID_STEP_4_FULL, "skip_reasons": ["bad"]}
    with pytest.raises(ValueError, match="wrong type"):
        validate_pipeline_step("step_4_master", payload)


def test_validate_pipeline_step_unknown_step_passes():
    """Observability-only steps (step_1_crawler, step_6_render, etc.)
    have no schema contract — any payload accepted."""
    validate_pipeline_step("step_1_crawler", {})
    validate_pipeline_step("step_6_render", {"model": "python"})
    validate_pipeline_step("step_7_git_publish", {"ok": True})


def test_validate_pipeline_step_rejects_legacy_string_data_trail_entries():
    """VHM run regression: Master BĐS emitted master_data_trail as ARRAY OF
    STRINGS (V3.6 legacy) → frontend crash on source.startsWith().
    V4.0 canonical: each entry must be dict with `source` key."""
    payload = {
        **_VALID_STEP_4_FULL,
        "data_trail": [
            "KB:bds-res-presales-backlog.md — backlog mechanism, conversion 90%",
            "WebSearch:vietstock.vn — Kế hoạch 2026",
        ],
    }
    with pytest.raises(ValueError, match="bad entries"):
        validate_pipeline_step("step_4_master", payload)


def test_validate_pipeline_step_rejects_data_trail_entries_without_source():
    """data_trail dict entries must have non-empty `source` key."""
    payload = {
        **_VALID_STEP_4_FULL,
        "data_trail": [{"fetched": "x", "purpose": "y"}],  # source missing
    }
    with pytest.raises(ValueError, match="bad entries"):
        validate_pipeline_step("step_4_master", payload)


def test_validate_pipeline_step_rejects_legacy_skeptic_string_entries():
    """Same check for step_5_skeptic.skeptic_data_trail."""
    payload = {
        **_VALID_STEP_5_FULL,
        "skeptic_data_trail": ["DB/generated_news — echo verify"],
    }
    with pytest.raises(ValueError, match="bad entries"):
        validate_pipeline_step("step_5_skeptic", payload)


def test_insert_generated_news_validates_pipeline_log(db):
    """insert_generated_news enforces schema on pipeline_log JSON."""
    bad_payload = {
        "article_id": "art-bad",
        "row_id": "row-bad",
        "ticker": "VCB",
        "sector": "Bank",
        "title": "T",
        "body": "B",
        "word_count": 100,
        "status": "draft",
        # step_4 missing skip_reasons + data_trail
        "pipeline_log": json.dumps({
            "step_4_master": {"chosen_question_idx": 0, "chosen_pick_reason": "x"},
        }),
    }
    # Seed crawl_log first to satisfy FK if any
    db.insert_crawl_row({
        "row_id": "row-bad",
        "funnel_batch_id": "VCB-x",
        "ticker": "VCB",
        "source_name": "S",
        "source_url": "https://example.com/bad",
        "title": "T",
        "crawled_at": "2026-05-11T00:00:00+07:00",
    })
    with pytest.raises(ValueError, match="step_4_master"):
        db.insert_generated_news(bad_payload)


# ---------------------------------------------------------------------------
# V5.0 Phase 1.3 (B-3) — pipeline_version default bump to V5.0
# ---------------------------------------------------------------------------


def test_insert_generated_news_defaults_pipeline_version_v5(tmp_path):
    """V5.0: new rows get pipeline_version=V5.0 unless caller specifies."""
    from lib.pipeline_db import PipelineDB
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    db.init_schema("data/pipeline.schema.sql")
    # Seed a crawl_log row first (FK)
    db.insert_crawl_row({
        "row_id": "r1", "funnel_batch_id": "b1", "ticker": "VCB",
        "source_name": "CafeF", "source_url": "http://example.com/1",
        "title": "T", "crawled_at": "2026-05-11T00:00:00Z",
    })
    # Insert WITHOUT pipeline_version → should default to V5.0 (not V3.6)
    article_data = {
        "article_id": "a1", "row_id": "r1", "ticker": "VCB", "sector": "Bank",
        "title": "Test", "body": "...", "accepted_hypothesis": 1, "status": "draft",
    }
    db.insert_generated_news(article_data)
    row = db.conn.execute("SELECT pipeline_version FROM generated_news WHERE article_id='a1'").fetchone()
    assert row["pipeline_version"] == "V5.0"
    db.close()


def test_insert_generated_news_explicit_version_preserved(tmp_path):
    """Caller can override default (e.g. test fixtures simulating legacy V4.0)."""
    from lib.pipeline_db import PipelineDB
    db_path = tmp_path / "test.db"
    db = PipelineDB(str(db_path))
    db.init_schema("data/pipeline.schema.sql")
    db.insert_crawl_row({
        "row_id": "r2", "funnel_batch_id": "b2", "ticker": "VCB",
        "source_name": "CafeF", "source_url": "http://example.com/2",
        "title": "T", "crawled_at": "2026-05-11T00:00:00Z",
    })
    db.insert_generated_news({
        "article_id": "a2", "row_id": "r2", "ticker": "VCB", "sector": "Bank",
        "title": "Test", "body": "...", "accepted_hypothesis": 1, "status": "draft",
        "pipeline_version": "V4.0",  # explicit override
    })
    row = db.conn.execute("SELECT pipeline_version FROM generated_news WHERE article_id='a2'").fetchone()
    assert row["pipeline_version"] == "V4.0"
    db.close()


# ---------------------------------------------------------------------------
# V5.0 Phase 1.4 (B-4) — Version-gate validation in validate_pipeline_step
# ---------------------------------------------------------------------------


def test_validate_v5_step_4_requires_observability():
    """V5.1: step_4_master MUST emit model + duration_ms (observability)."""
    from lib.pipeline_db import validate_pipeline_step
    import pytest
    payload = {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "ok",
        "skip_reasons": {},
        "data_trail": [{"source": "x", "fetched": "y"}],
        "format_id_used": "standard_qa",
    }
    with pytest.raises(ValueError, match="model|duration_ms"):
        validate_pipeline_step("step_4_master", payload, pipeline_version="V5.0")


def test_validate_v5_step_4_observability_complete_passes():
    from lib.pipeline_db import validate_pipeline_step
    payload = {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "ok",
        "skip_reasons": {},
        "data_trail": [{"source": "x", "fetched": "y"}],
        "format_id_used": "standard_qa",
        "model": "claude-opus-4-7",
        "duration_ms": 12500,
    }
    validate_pipeline_step("step_4_master", payload, pipeline_version="V5.0")


def test_validate_v5_step_4_empty_model_rejects():
    """model must be non-empty string."""
    from lib.pipeline_db import validate_pipeline_step
    import pytest
    payload = {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "ok",
        "skip_reasons": {},
        "data_trail": [{"source": "x"}],
        "format_id_used": "standard_qa",
        "model": "",
        "duration_ms": 12500,
    }
    with pytest.raises(ValueError, match="empty"):
        validate_pipeline_step("step_4_master", payload, pipeline_version="V5.0")


def test_validate_v4_step_4_no_observability_required():
    """V4.0 back-compat: observability NOT required."""
    from lib.pipeline_db import validate_pipeline_step
    payload = {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "ok",
        "skip_reasons": {},
        "data_trail": [{"source": "x", "fetched": "y"}],
    }
    validate_pipeline_step("step_4_master", payload, pipeline_version="V4.0")


def test_validate_v3_skips_step_3_5_check():
    """V3.6 rows: no step_3_5_format_director schema enforcement."""
    from lib.pipeline_db import validate_pipeline_step
    validate_pipeline_step("step_3_5_format_director", {}, pipeline_version="V3.6")


def test_validate_v4_skips_step_3_5_check():
    """V4.0 rows: also skip step_3_5."""
    from lib.pipeline_db import validate_pipeline_step
    validate_pipeline_step("step_3_5_format_director", {}, pipeline_version="V4.0")


def test_validate_v5_enforces_step_3_5():
    """V5.0 rows: step_3_5_format_director MUST have format_picks."""
    from lib.pipeline_db import validate_pipeline_step
    import pytest
    with pytest.raises(ValueError, match="step_3_5_format_director"):
        validate_pipeline_step("step_3_5_format_director", {}, pipeline_version="V5.0")


def test_validate_v5_step_4_requires_format_id_used():
    """V5.0 step_4_master gets format_id_used required field added."""
    from lib.pipeline_db import validate_pipeline_step
    import pytest
    payload = {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "Test reason",
        "skip_reasons": {},
        "data_trail": [{"source": "Finpath_API/test", "fetched": "data"}],
    }
    with pytest.raises(ValueError, match="format_id_used"):
        validate_pipeline_step("step_4_master", payload, pipeline_version="V5.0")


def test_validate_v4_step_4_no_format_id_used_required():
    """V4.0 step_4_master: format_id_used NOT required (back-compat)."""
    from lib.pipeline_db import validate_pipeline_step
    payload = {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "Test reason",
        "skip_reasons": {},
        "data_trail": [{"source": "Finpath_API/test", "fetched": "data"}],
    }
    validate_pipeline_step("step_4_master", payload, pipeline_version="V4.0")


def test_validate_v5_step_4_valid_passes():
    """V5.0 step_4_master with format_id_used present + observability passes."""
    from lib.pipeline_db import validate_pipeline_step
    payload = {
        "chosen_question_idx": 0,
        "chosen_pick_reason": "Test reason",
        "skip_reasons": {},
        "data_trail": [{"source": "Finpath_API/test", "fetched": "data"}],
        "format_id_used": "standard_qa",
        "model": "claude-opus-4-7",
        "duration_ms": 12500,
    }
    validate_pipeline_step("step_4_master", payload, pipeline_version="V5.0")
