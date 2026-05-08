"""Tests for lib.render_compare_feed V4.0 — multi-article + 8 sections."""
import json
from pathlib import Path

import pytest

from lib.pipeline_db import PipelineDB
from lib.render_compare_feed import (
    render_for_funnel_batch,
    render_article_md_v4,
    build_right_column,
)


@pytest.fixture
def populated_db_v4(tmp_path):
    """Seed 1 batch with 3 articles (multi-article scenario) + 2 rejected."""
    schema = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db_path = tmp_path / "test.db"
    db = PipelineDB(db_path)
    db.init_schema(schema)

    funnel_batch_id = "TCB-20260508-1023"

    # 3 anchor rows (3 picked)
    for i, (rid, src, url, m_note) in enumerate([
        ("anchor-1", "Báo Pháp luật", "https://bpl.vn/a", "Anchor — đầy đủ data"),
        ("anchor-2", "VnEconomy", "https://vne.vn/a", "Anchor — angle so sánh"),
        ("anchor-3", "Vietstock", "https://vst.vn/a", "Anchor — early signal"),
    ]):
        db.insert_crawl_row({
            "row_id": rid, "funnel_batch_id": funnel_batch_id, "ticker": "TCB",
            "source_name": src, "source_url": url, "title": f"Title {i}",
            "crawled_at": "2026-05-08T10:23:00+07:00",
            "published_time": "2026-05-07T10:00:00+07:00",
            "raw_content": "Raw body.",
            "primary_ticker": "TCB", "sector": "Bank",
            "editor_v1_decision": "route_to_story_editor",
            "story_editor_decision": "write_brief",
            "master_decision": "write_article", "master_note": m_note,
            "brief_json": json.dumps({
                "why_chosen_narrative": f"Narrative {i} cho bài chọn này — 3-5 câu giải thích.",
                "angle_label": f"Angle {i}",
                "angle_narrative": f"Narrative angle {i} — 2-3 câu hướng tiếp cận.",
                "source_rationale": f"Rationale {i} — vì sao chọn nguồn.",
                "deep_question_options": [
                    {"question": f"Q1 batch {i}?", "category": "paradox", "pick_hint": "Hint 1"},
                    {"question": f"Q2 batch {i}?", "category": "why_now", "pick_hint": "Hint 2"},
                    {"question": f"Q3 batch {i}?", "category": "hidden_mechanism", "pick_hint": "Hint 3"},
                ],
                "insight_hypothesis": f"Insight {i}",
            }, ensure_ascii=False),
            "status": "published",
        })

    # Reject by editor V1
    db.insert_crawl_row({
        "row_id": "rej-edit", "funnel_batch_id": funnel_batch_id, "ticker": "TCB",
        "source_name": "Random Blog", "source_url": "https://blog/a", "title": "Off-topic",
        "crawled_at": "2026-05-08T10:23:00+07:00",
        "primary_ticker": None, "sector": "rejected",
        "editor_v1_decision": "reject", "editor_v1_note": "Off-topic — không phải Bank",
        "status": "rejected",
    })
    # Reject by story editor
    db.insert_crawl_row({
        "row_id": "rej-story", "funnel_batch_id": funnel_batch_id, "ticker": "TCB",
        "source_name": "Other Source", "source_url": "https://other/a", "title": "Dup story",
        "crawled_at": "2026-05-08T10:23:00+07:00",
        "primary_ticker": "TCB", "sector": "Bank",
        "editor_v1_decision": "route_to_story_editor",
        "story_editor_decision": "reject",
        "story_editor_note": "Cùng story 25/4 với BPL anchor, ít quote CEO hơn",
        "status": "rejected",
    })

    # 3 generated_news for 3 anchors (multi-article)
    for i, (aid, rid, title) in enumerate([
        ("art-1", "anchor-1", "TCB hy sinh 5.000 tỷ — đổi lấy gì?"),
        ("art-2", "anchor-2", "TCB đổi giấy lấy ngôi vương — vốn hóa kém tứ trụ?"),
        ("art-3", "anchor-3", "Phí dịch vụ TCB lập đỉnh — rời mô hình cho vay?"),
    ]):
        slug = f"TCB-20260508-1023-art-{i+1}"
        db.insert_generated_news({
            "article_id": aid, "row_id": rid,
            "ticker": "TCB", "sector": "Bank",
            "title": title,
            "body": "Opening paragraph đầy đủ ba mươi từ trở lên mô tả sự kiện và đặt setup cho thân bài làm rõ tension.\n\n- **Bold 1**: bullet content đầy đủ ít nhất hai mươi từ để pass substantive check trong gate này.\n- **Bold 2**: bullet content cũng đủ hai mươi từ để pass substantive thực sự đấy hôm nay.\n- **Bold 3**: bullet cuối cùng cũng đủ content và bold highlight đầu cho rõ ràng nhé.\n\nClosing.",
            "word_count": 60,
            "key_view": "thận trọng",
            "insight_final": f"Insight final {i}.",
            "skeptic_critique": f"Critique {i}.",
            "skeptic_angle": "alt_interpretation",
            "skeptic_verdict": "pass_with_caveats",
            "accepted_hypothesis": 1,
            "brief_json": "{}",
            "pipeline_log": json.dumps({
                "step_4_master": {
                    "chosen_question_idx": 0,
                    "chosen_pick_reason": f"Pick reason {i}.",
                    "skip_reasons": {"1": "Skip 1", "2": "Skip 2"},
                    "data_trail": [
                        {"source": "Finpath/bankratios", "fetched": "NIM 3.74%", "used_for": "Bullet 1 anchor"},
                        {"source": "KB/frameworks", "fetched": "Pattern X", "used_for": "Closing"},
                    ],
                    "gates_passed": True,
                },
                "step_5_skeptic": {
                    "angle": "alt_interpretation",
                    "verdict": "pass_with_caveats",
                    "data_trail": [
                        {"source": "Finpath/shareholders", "fetched": "Foreign 22%", "used_for": "Counter risk profile"},
                    ],
                },
            }, ensure_ascii=False),
            "status": "published",
            "published_at": "2026-05-08T16:00:00+07:00",
            "public_slug": slug,
        })
    yield db, db_path
    db.close()


def test_render_writes_n_files_for_n_anchors(populated_db_v4, tmp_path):
    """V4.0 multi-article: 3 anchors → 3 files (not 1)."""
    _, db_path = populated_db_v4
    out_dir = tmp_path / "out"
    result = render_for_funnel_batch(db_path, "TCB-20260508-1023", out_dir)
    assert result["count"] == 3
    md_files = list(out_dir.glob("*.md"))
    assert len(md_files) == 3


def test_render_uses_public_slug_in_filename(populated_db_v4, tmp_path):
    _, db_path = populated_db_v4
    out_dir = tmp_path / "out"
    render_for_funnel_batch(db_path, "TCB-20260508-1023", out_dir)
    md_filenames = sorted(p.name for p in out_dir.glob("*.md"))
    assert md_filenames == [
        "TCB-20260508-1023-art-1.md",
        "TCB-20260508-1023-art-2.md",
        "TCB-20260508-1023-art-3.md",
    ]


def test_manifest_has_n_entries(populated_db_v4, tmp_path):
    _, db_path = populated_db_v4
    out_dir = tmp_path / "out"
    render_for_funnel_batch(db_path, "TCB-20260508-1023", out_dir)
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert len(manifest["articles"]) == 3
    assert all(a["ticker"] == "TCB" for a in manifest["articles"])


def test_manifest_id_is_public_slug(populated_db_v4, tmp_path):
    _, db_path = populated_db_v4
    out_dir = tmp_path / "out"
    render_for_funnel_batch(db_path, "TCB-20260508-1023", out_dir)
    manifest = json.loads((out_dir / "manifest.json").read_text())
    ids = {a["id"] for a in manifest["articles"]}
    assert "TCB-20260508-1023-art-1" in ids
    assert "TCB-20260508-1023-art-2" in ids
    assert "TCB-20260508-1023-art-3" in ids


def test_render_includes_8_sections_in_right_column(populated_db_v4, tmp_path):
    """Frontmatter contains all 8 sections data for cột phải."""
    _, db_path = populated_db_v4
    out_dir = tmp_path / "out"
    render_for_funnel_batch(db_path, "TCB-20260508-1023", out_dir)
    md_path = out_dir / "TCB-20260508-1023-art-1.md"
    content = md_path.read_text()
    # Section 1: original article info
    assert "right_source:" in content
    # Section 2: why_chosen_narrative
    assert "why_chosen_narrative:" in content
    # Section 3: angle_narrative
    assert "angle_narrative:" in content
    # Section 4: deep_question_options + master pick
    assert "deep_question_options" in content
    assert "chosen_question_idx" in content
    # Section 5: crawl_funnel + reject reasons + agent labels
    assert "crawl_funnel:" in content
    # Section 6: master_data_trail
    assert "master_data_trail:" in content
    # Section 7: skeptic_data_trail
    assert "skeptic_data_trail:" in content
    # Section 8: external link (raw_url, NOT raw_content)
    assert "raw_article_url:" in content
    assert "Raw body." not in content  # raw content NOT embedded


def test_funnel_groups_rejects_with_agent_labels(populated_db_v4, tmp_path):
    _, db_path = populated_db_v4
    out_dir = tmp_path / "out"
    render_for_funnel_batch(db_path, "TCB-20260508-1023", out_dir)
    content = (out_dir / "TCB-20260508-1023-art-1.md").read_text()
    # editor_v1 reject narrative + agent label
    assert "Off-topic" in content
    assert "editor_v1" in content or "Gác cổng" in content
    # story_editor reject narrative + agent label
    assert "Cùng story 25/4" in content
    assert "story_editor" in content or "Tổng biên tập" in content
