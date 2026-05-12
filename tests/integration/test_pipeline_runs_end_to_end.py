"""V1.0 end-to-end smoke — session grouping + manifest build (Plan H Task 9).

These tests exercise insert_crawl_row + build_pipeline_runs_manifest using
the real pipeline schema (not a stub). They are LOCAL DB only — no network.
Marked @pytest.mark.integration to keep them out of the default suite per
pyproject.toml addopts. Run with `pytest -m integration` to execute.
"""
import json
import uuid
from pathlib import Path
import pytest
from lib.pipeline_db import PipelineDB
from lib.render_compare_feed import build_pipeline_runs_manifest


SCHEMA_PATH = Path(__file__).parent.parent.parent / "data" / "pipeline.schema.sql"


def _open_db(tmp_path):
    db = PipelineDB(str(tmp_path / "test.db"))
    db.init_schema(str(SCHEMA_PATH))
    return db


def _insert(db, **kwargs):
    """Insert a complete crawl_log row using REAL schema column names."""
    defaults = {
        "row_id": str(uuid.uuid4()),
        "ticker": "VHM",
        "source_name": "VnEconomy",
        "source_url": f"https://example.com/{uuid.uuid4().hex[:8]}",
        "published_time": "2026-05-12",
        "crawled_at": "2026-05-12T14:30:00Z",
        "title": "title",
        "raw_content": "body",
        "funnel_batch_id": "VHM-20260512-1430",
        "session_id": "session-1",
        "trigger_type": "tin",
        "trigger_args": "VHM",
    }
    defaults.update(kwargs)
    return db.insert_crawl_row(defaults)


@pytest.mark.integration
def test_single_ticker_session_one_batch(tmp_path):
    db = _open_db(tmp_path)
    sid = str(uuid.uuid4())
    _insert(db, session_id=sid)

    output_path = tmp_path / "pipeline-runs.json"
    count = build_pipeline_runs_manifest(db, output_path)
    assert count == 1

    payload = json.loads(output_path.read_text())
    session = payload["sessions"][0]
    assert session["trigger_type"] == "tin"
    assert session["trigger_args"] == "VHM"
    assert len(session["batches"]) == 1
    db.close()


@pytest.mark.integration
def test_tin_hot_3_session_groups_n_batches(tmp_path):
    db = _open_db(tmp_path)
    sid = str(uuid.uuid4())

    for ticker in ["VHM", "FPT", "BSR"]:
        for i in range(3):
            _insert(
                db,
                ticker=ticker,
                funnel_batch_id=f"{ticker}-20260512-1430",
                session_id=sid,
                trigger_type="tin-hot",
                trigger_args="N=3",
            )

    output_path = tmp_path / "pipeline-runs.json"
    count = build_pipeline_runs_manifest(db, output_path)
    assert count == 1

    payload = json.loads(output_path.read_text())
    session = payload["sessions"][0]
    assert session["trigger_type"] == "tin-hot"
    assert len(session["batches"]) == 3
    assert session["fetched_total"] == 9
    db.close()


@pytest.mark.integration
def test_legacy_rows_skipped(tmp_path):
    """Q2 resolution verification — session_id IS NULL rows omitted from manifest."""
    db = _open_db(tmp_path)

    _insert(db, session_id=None, funnel_batch_id="LEGACY-batch")
    _insert(db, session_id="session-1")

    output_path = tmp_path / "pipeline-runs.json"
    count = build_pipeline_runs_manifest(db, output_path)
    assert count == 1
    db.close()
