"""Tests for lib.render_compare_feed — markdown rendering."""
import json
from pathlib import Path

import pytest

from lib.pipeline_db import PipelineDB
from lib.render_compare_feed import render_for_funnel_batch


@pytest.fixture
def populated_db(tmp_path):
    schema = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db_path = tmp_path / "test.db"
    db = PipelineDB(db_path)
    db.init_schema(schema)
    db.insert_crawl_row({
        "row_id": "anchor-1",
        "funnel_batch_id": "VCB-20260508-1530",
        "ticker": "VCB",
        "source_name": "Báo Pháp luật",
        "source_url": "https://example.com/anchor",
        "title": "VCB Q1/2026 lãi 11.803 tỷ",
        "crawled_at": "2026-05-08T15:30:00+07:00",
        "published_time": "2026-05-07T10:00:00+07:00",
        "raw_content": "Raw body of anchor.",
        "primary_ticker": "VCB",
        "sector": "Bank",
        "editor_v1_decision": "route_to_story_editor",
        "story_editor_decision": "write_brief",
        "master_decision": "write_article",
        "master_note": "Anchor — đầy đủ 4 con số decode mechanism",
        "status": "published",
    })
    db.insert_crawl_row({
        "row_id": "rej-1",
        "funnel_batch_id": "VCB-20260508-1530",
        "ticker": "VCB",
        "source_name": "VnEconomy",
        "source_url": "https://example.com/rej",
        "title": "VCB rej article",
        "crawled_at": "2026-05-08T14:30:00+07:00",
        "published_time": "2026-05-06T10:00:00+07:00",
        "primary_ticker": "VCB",
        "sector": "Bank",
        "editor_v1_decision": "route_to_story_editor",
        "story_editor_decision": "reject",
        "story_editor_note": "dup_event: cùng story KQKD Q1",
        "status": "rejected",
    })
    db.insert_generated_news({
        "article_id": "art-1",
        "row_id": "anchor-1",
        "ticker": "VCB",
        "sector": "Bank",
        "title": "VCB quý I: lãi vẫn tăng 9% dù bỏ thêm 1.700 tỷ vào quỹ phòng nợ xấu",
        "body": "Lợi nhuận trước thuế **11.803 tỷ đồng**, tăng 9%.\n\n## Cần để ý\n\nLần đầu sau...",
        "word_count": 354,
        "key_view": "thận trọng",
        "insight_final": "Phù hợp NĐT giá trị giữ trên 12 tháng.",
        "skeptic_critique": "Số trên có context unclear...",
        "skeptic_angle": "data_skepticism",
        "skeptic_verdict": "pass_with_caveats",
        "accepted_hypothesis": 1,
        "brief_json": json.dumps({
            "why_chosen": "Tin Q1/2026 mới, paradox mạnh.",
            "angle_label": "Chủ động xây bộ đệm — đánh đổi tốc độ lấy độ bền",
            "data_anchor": "DB BCTC Quarter VCB-2026-Q1.",
        }),
        "pipeline_log": json.dumps({"step_1_crawler": {"sources": 20}}),
        "status": "published",
        "published_at": "2026-05-08T16:00:00+07:00",
    })
    yield db, db_path
    db.close()


def test_render_writes_md_file(populated_db, tmp_path):
    _, db_path = populated_db
    out_dir = tmp_path / "out"
    result = render_for_funnel_batch(db_path, "VCB-20260508-1530", out_dir)
    assert "error" not in result
    md_path = out_dir / "VCB-20260508-1530.md"
    assert md_path.exists()
    content = md_path.read_text(encoding="utf-8")
    assert content.startswith("---\n")
    assert "<!-- left -->" in content
    assert "<!-- right -->" in content
    assert "VCB" in content
    assert "## Góc nhìn ngược" in content


def test_render_updates_manifest(populated_db, tmp_path):
    _, db_path = populated_db
    out_dir = tmp_path / "out"
    render_for_funnel_batch(db_path, "VCB-20260508-1530", out_dir)
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert len(manifest["articles"]) == 1
    assert manifest["articles"][0]["ticker"] == "VCB"
    assert manifest["articles"][0]["word_count"] == 354


def test_render_funnel_includes_rejected(populated_db, tmp_path):
    _, db_path = populated_db
    out_dir = tmp_path / "out"
    render_for_funnel_batch(db_path, "VCB-20260508-1530", out_dir)
    content = (out_dir / "VCB-20260508-1530.md").read_text()
    assert "VnEconomy" in content
    assert "dup_event" in content


def test_render_missing_anchor_returns_error(tmp_path):
    schema = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db = PipelineDB(tmp_path / "empty.db")
    db.init_schema(schema)
    db.close()
    out_dir = tmp_path / "out"
    result = render_for_funnel_batch(tmp_path / "empty.db", "MISSING-BATCH", out_dir)
    assert "error" in result
