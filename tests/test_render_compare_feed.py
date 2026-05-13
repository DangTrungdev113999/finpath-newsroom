"""Tests for lib.render_compare_feed V4.0 — multi-article + 8 sections."""
import json
from pathlib import Path

import pytest

from lib.pipeline_db import PipelineDB
from lib.render_compare_feed import (
    render_for_funnel_batch,
    render_article_md_v4,
    build_right_column,
    clean_manifest,
    rebuild_manifest_from_db,
    update_manifest,
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
        ("art-1", "anchor-1", "Q1 BSR ăn 8.265 tỷ — sếp chỉ hứa 2.162 tỷ?"),
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
                    "skeptic_data_trail": [
                        {"source": "Finpath/shareholders", "fetched": "Foreign 22%", "used_for": "Counter risk profile"},
                    ],
                },
            }, ensure_ascii=False),
            "status": "published",
            "published_at": "2026-05-08T16:00:00+07:00",
            "public_slug": slug,
            # V4.0 baseline for legacy render-output tests. These predate V5.0 schema.
            # Render output structure tested here — schema validation tested separately.
            "pipeline_version": "V4.0",
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


# Bug B6 fix — defensive strip of embedded "## Góc nhìn ngược" heading in skeptic_critique
# ----------------------------------------------------------------------

def _make_minimal_article(skeptic_critique: str | None) -> tuple[dict, dict, list]:
    """Minimal article + anchor + funnel for render_article_md_v4."""
    article = {
        "article_id": "art-test",
        "row_id": "anchor-test",
        "ticker": "MBB",
        "sector": "Bank",
        "title": "Test title — vì sao?",
        "body": "Opening paragraph đầy đủ tối thiểu ba mươi từ để pass setup test bug B6 fix render layer defensive strip skeptic heading.\n\n- **Bold 1**: bullet đủ hai mươi từ để có substance test test test thực sự rồi đó hôm nay nhé.\n\nClosing.",
        "word_count": 50,
        "key_view": "trung lập",
        "insight_final": "Insight test.",
        "skeptic_critique": skeptic_critique,
        "skeptic_angle": "alt_interpretation",
        "skeptic_verdict": "pass_with_caveats",
        "pipeline_log": json.dumps({
            "step_4_master": {
                "chosen_question_idx": 0,
                "chosen_pick_reason": "Test pick",
                "skip_reasons": {},
                "data_trail": [{"source": "test", "fetched": "x", "purpose": "y", "supports_argument": "z"}],
            },
            "step_5_skeptic": {
                "angle": "alt_interpretation",
                "verdict": "pass_with_caveats",
                "skeptic_data_trail": [{"source": "test", "fetched": "x", "purpose": "y", "supports_argument": "z"}],
            },
        }, ensure_ascii=False),
        "public_slug": "MBB-test-slug",
    }
    anchor = {
        "row_id": "anchor-test",
        "funnel_batch_id": "MBB-20260508-1542",
        "ticker": "MBB",
        "source_name": "Source",
        "source_url": "https://src/a",
        "title": "Raw title",
        "crawled_at": "2026-05-08T15:42:00+07:00",
        "published_time": "2026-05-08T10:00:00+07:00",
        "master_decision": "write_article",
        "master_note": "Anchor",
        "brief_json": json.dumps({
            "why_chosen_narrative": "n",
            "angle_label": "a",
            "angle_narrative": "an",
            "deep_question_options": [],
        }, ensure_ascii=False),
    }
    funnel_rows = [anchor]
    return article, anchor, funnel_rows


def test_render_strips_embedded_skeptic_heading():
    """Skeptic critique starts with `## Góc nhìn ngược` → render strips it, output has exactly 1 heading."""
    skeptic_with_heading = "## Góc nhìn ngược\n\nBài Master nêu ba kênh tăng vốn nhưng thiếu data anchor cho kênh thứ ba — đáng nghi ngờ về timing."
    article, anchor, funnel = _make_minimal_article(skeptic_with_heading)
    output = render_article_md_v4(article, anchor, funnel)
    assert output.count("## Góc nhìn ngược") == 1
    # Body content preserved
    assert "Bài Master nêu ba kênh" in output


def test_render_clean_skeptic_no_strip_needed():
    """Skeptic critique without embedded heading — render appends 1 heading."""
    skeptic_clean = "Bài Master nêu ba kênh tăng vốn nhưng thiếu data anchor cho kênh thứ ba."
    article, anchor, funnel = _make_minimal_article(skeptic_clean)
    output = render_article_md_v4(article, anchor, funnel)
    assert output.count("## Góc nhìn ngược") == 1
    assert "Bài Master nêu ba kênh" in output


def test_render_strips_h3_heading_too():
    """Skeptic critique with `### Góc nhìn ngược` (h3) → also stripped (regex matches h2 OR h3)."""
    skeptic_h3 = "### Góc nhìn ngược\n\nBài Master nêu vấn đề về timing."
    article, anchor, funnel = _make_minimal_article(skeptic_h3)
    output = render_article_md_v4(article, anchor, funnel)
    assert output.count("## Góc nhìn ngược") == 1
    # h3 form should be gone (only h2 remains)
    assert output.count("### Góc nhìn ngược") == 0
    assert "Bài Master nêu vấn đề" in output


def test_render_no_skeptic_no_heading():
    """No skeptic critique → no heading appended."""
    for empty in ("", None):
        article, anchor, funnel = _make_minimal_article(empty)
        output = render_article_md_v4(article, anchor, funnel)
        assert output.count("## Góc nhìn ngược") == 0


def test_render_skeptic_with_extra_blank_lines():
    """Leading whitespace + blank lines before heading → still stripped."""
    skeptic_padded = "\n\n\n## Góc nhìn ngược\n\n\n\nBài Master nêu vấn đề về timing."
    article, anchor, funnel = _make_minimal_article(skeptic_padded)
    output = render_article_md_v4(article, anchor, funnel)
    assert output.count("## Góc nhìn ngược") == 1
    assert "Bài Master nêu vấn đề" in output


def test_render_strips_details_block_from_body():
    """NVL run regression: orchestrator inline contaminated body field with
    <details><summary>Góc nhìn ngược (Skeptic)</summary>...</details> block.
    Render must strip defensively so Skeptic appears exactly once via the
    appended `## Góc nhìn ngược` section."""
    article, anchor, funnel = _make_minimal_article("Critique content.")
    article["body"] = (
        "Opening paragraph rộng đủ ba mươi từ với tension setup cho thân bài.\n\n"
        "- **Bold 1**: bullet đủ hai mươi từ pass substantive gate one with anchor.\n"
        "- **Bold 2**: bullet đủ hai mươi từ pass substantive gate two with anchor.\n\n"
        "Closing line.\n\n"
        "<details>\n<summary>Góc nhìn ngược (Skeptic)</summary>\n"
        "Critique duplicated inside details block — must be stripped.\n"
        "</details>"
    )
    output = render_article_md_v4(article, anchor, funnel)
    # <details> block stripped from body
    assert "<details>" not in output
    assert "</details>" not in output
    assert "Critique duplicated inside details block" not in output
    # Skeptic critique appears exactly once (via appended ## heading)
    assert output.count("## Góc nhìn ngược") == 1
    assert "Critique content." in output


def test_build_right_column_reads_skeptic_data_trail_key():
    """Render reads canonical `skeptic_data_trail` key from step_5_skeptic
    (NVL viewer regression — old code read `data_trail` and got [])."""
    article = {
        "pipeline_log": json.dumps({
            "step_4_master": {
                "chosen_question_idx": 0,
                "chosen_pick_reason": "x",
                "skip_reasons": {},
                "data_trail": [{"source": "Finpath", "fetched": "y", "purpose": "z", "supports_argument": "w"}],
            },
            "step_5_skeptic": {
                "angle": "data_skepticism",
                "verdict": "pass",
                "skeptic_data_trail": [
                    {"source": "DB/generated_news", "fetched": "echo", "purpose": "verify", "supports_argument": True},
                    {"source": "KB/bds-res-presales", "fetched": "lifecycle", "purpose": "check", "supports_argument": True},
                ],
            },
        }),
        "ticker": "NVL",
        "title": "T",
    }
    anchor = {
        "source_name": "X", "source_url": "https://x", "title": "T",
        "published_time": None, "brief_json": "{}", "row_id": "r1",
        "ticker": "NVL", "funnel_batch_id": "NVL-x",
        "crawled_at": "2026-05-11T00:00:00+00:00",
    }
    result = build_right_column(article, anchor, [anchor])
    assert len(result["skeptic_data_trail"]) == 2
    assert result["skeptic_data_trail"][0]["source"] == "DB/generated_news"


def test_render_includes_format_director_section(tmp_path):
    """V5.0: right column markdown includes format pick reasoning."""
    from lib.render_compare_feed import build_right_column

    article = {
        "article_id": "a1",
        "ticker": "VCB",
        "title": "Vì sao to nhất lại đi chậm?",
        "body": "...",
        "pipeline_version": "V5.0",
        "pipeline_log": '{"step_3_5_format_director": {"format_picks": [{"option_idx": 0, "format_id": "standard_qa", "format_reason": "Category=paradox → candidates=[standard_qa]. Picked=standard_qa.", "tone_bias": "neutral", "length_target": 250}], "candidates_considered_per_option": [{"option_idx": 0, "category": "paradox", "candidates": ["standard_qa"]}], "variety_check": {"recent_3_articles_same_ticker_formats": ["standard_qa", "standard_listicle", "standard_qa"], "current_pick_diversity_warning": false}, "model": "claude-sonnet-4-6", "duration_ms": 8400, "tokens": 1240}, "step_4_master": {"chosen_question_idx": 0, "chosen_pick_reason": "test", "skip_reasons": {}, "data_trail": [{"source": "x", "fetched": "y"}], "format_id_used": "standard_qa"}}',
    }
    anchor_row = {"row_id": "r1", "ticker": "VCB"}
    funnel_rows = []

    rc = build_right_column(article, anchor_row, funnel_rows)
    assert "format_director" in rc
    assert rc["format_director"]["format_id"] == "standard_qa"
    assert rc["format_director"]["format_reason"]
    assert rc["format_director"]["tone_bias"] == "neutral"


def test_render_v4_article_no_format_director_section(tmp_path):
    """V3.6/V4.0 legacy articles: format_director field absent (graceful)."""
    from lib.render_compare_feed import build_right_column
    article = {
        "article_id": "a1",
        "ticker": "VCB",
        "title": "Test",
        "body": "...",
        "pipeline_version": "V4.0",
        "pipeline_log": '{"step_4_master": {"chosen_question_idx": 0, "chosen_pick_reason": "x", "skip_reasons": {}, "data_trail": [{"source": "x", "fetched": "y"}]}}',
    }
    rc = build_right_column(article, {"row_id": "r1", "ticker": "VCB"}, [])
    assert rc.get("format_director") in (None, {})


def test_update_manifest_atomic_concurrent(tmp_path):
    """3 concurrent update_manifest calls all entries persist (no last-writer-wins).

    Phase G T6 — atomic write via temp file + os.replace. Tests subprocess
    invocations because multi-pipeline parallel calls update_manifest from
    different Python processes.
    """
    import subprocess
    from pathlib import Path

    manifest = tmp_path / "manifest.json"
    helper = Path(__file__).parent / "helpers" / "manifest_writer.py"

    # Spawn 3 concurrent writers, each adds 1 unique article
    procs = [
        subprocess.Popen(
            ["uv", "run", "python", str(helper), str(manifest), f"article-{i}", f"2026-05-10T00:00:0{i}Z"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        for i in range(3)
    ]
    results = [p.wait(timeout=30) for p in procs]
    assert all(rc == 0 for rc in results)

    # All 3 entries should be present
    import json
    data = json.loads(manifest.read_text())
    ids = {a["id"] for a in data["articles"]}
    assert ids == {"article-0", "article-1", "article-2"}, \
        f"Lost entries — got {ids}"


def test_update_manifest_sweeps_stale_entries(tmp_path):
    """Headline (Step 4.5) regenerates slug from final title — old placeholder
    entry must NOT linger pointing to a non-existent .md file (causes 404 in
    viewer). update_manifest sweeps any entry whose .md file is missing.
    """
    manifest = tmp_path / "manifest.json"

    # Pre-seed manifest with a stale entry whose .md file does NOT exist —
    # simulates the Master-persists-placeholder → Headline-renames-slug case.
    stale = {
        "articles": [
            {
                "id": "STB-20260513-1900-pending-headline",
                "ticker": "STB",
                "sector": "Bank",
                "title": "placeholder",
                "crawled_at": "2026-05-13T03:00:00Z",
                "key_view": "trung lập",
                "word_count": 0,
            }
        ]
    }
    manifest.write_text(json.dumps(stale), encoding="utf-8")

    # New render writes the .md file then calls update_manifest with final slug.
    final_id = "STB-20260513-1900-stb-gom-dna-lpbank"
    (tmp_path / f"{final_id}.md").touch()
    update_manifest(
        manifest,
        {
            "id": final_id,
            "ticker": "STB",
            "sector": "Bank",
            "title": "STB gom DNA LPBank",
            "crawled_at": "2026-05-13T03:00:00Z",
            "key_view": "lạc quan",
            "word_count": 276,
        },
    )

    data = json.loads(manifest.read_text(encoding="utf-8"))
    ids = {a["id"] for a in data["articles"]}
    assert ids == {final_id}, f"stale placeholder leaked → {ids}"


def test_clean_manifest_drops_orphans(tmp_path):
    """clean_manifest is the one-shot equivalent for the same sweep."""
    manifest = tmp_path / "manifest.json"
    (tmp_path / "live.md").touch()
    manifest.write_text(
        json.dumps({
            "articles": [
                {"id": "live", "crawled_at": "2026-05-13T00:00:00Z"},
                {"id": "orphan", "crawled_at": "2026-05-13T00:00:00Z"},
            ]
        }),
        encoding="utf-8",
    )
    result = clean_manifest(manifest)
    assert result == {"removed": 1, "remaining": 1}
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert [a["id"] for a in data["articles"]] == ["live"]


def test_rebuild_manifest_excludes_orphan_placeholder_file(tmp_path):
    """Even if BOTH placeholder.md AND final.md exist on disk (render-twice
    scenario), rebuild_manifest_from_db only links the DB-current public_slug.
    The orphan file is left on disk but unlisted — no 404 path for users.
    """
    schema = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db_path = tmp_path / "test.db"
    db = PipelineDB(db_path)
    db.init_schema(schema)

    db.insert_crawl_row({
        "row_id": "anchor-1",
        "funnel_batch_id": "STB-20260513-1900",
        "ticker": "STB",
        "source_name": "X",
        "source_url": "https://x/a",
        "title": "raw",
        "crawled_at": "2026-05-13T03:00:00+07:00",
        "primary_ticker": "STB",
        "sector": "Bank",
        "editor_v1_decision": "route_to_story_editor",
        "story_editor_decision": "write_brief",
        "master_decision": "write_article",
        "brief_json": json.dumps({"deep_question_options": []}),
        "status": "published",
    })
    final_slug = "STB-20260513-1900-stb-gom-dna-lpbank"
    db.insert_generated_news({
        "article_id": "art-1",
        "row_id": "anchor-1",
        "ticker": "STB",
        "sector": "Bank",
        "title": "STB gom DNA LPBank",
        "body": "x",
        "word_count": 276,
        "key_view": "lạc quan",
        "insight_final": "ok",
        "accepted_hypothesis": 1,
        "public_slug": final_slug,
        "pipeline_version": "V4.0",
        "pipeline_log": json.dumps({
            "step_4_master": {
                "chosen_question_idx": 0,
                "chosen_pick_reason": "x",
                "skip_reasons": {},
                "data_trail": [{"source": "x", "fetched": "y"}],
            }
        }),
    })

    # Both files exist on disk — simulating render-twice race.
    (tmp_path / "STB-20260513-1900-pending-headline.md").touch()
    (tmp_path / f"{final_slug}.md").touch()

    result = rebuild_manifest_from_db(db, tmp_path)
    db.close()
    assert result["total"] == 1
    assert result["from_db"] == 1
    data = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert [a["id"] for a in data["articles"]] == [final_slug]


def test_rebuild_manifest_preserves_legacy_hand_crafted_entry(tmp_path):
    """Legacy/pre-pipeline .md files (e.g. hand-crafted sample) with no DB
    row but existing on disk + listed in old manifest should survive rebuild.
    """
    schema = Path(__file__).parent.parent / "data" / "pipeline.schema.sql"
    db_path = tmp_path / "test.db"
    db = PipelineDB(db_path)
    db.init_schema(schema)

    # Hand-crafted file on disk + listed in old manifest, no DB row.
    legacy_id = "VCB-20260508-1530"
    (tmp_path / f"{legacy_id}.md").touch()
    (tmp_path / "manifest.json").write_text(
        json.dumps({"articles": [{
            "id": legacy_id,
            "ticker": "VCB",
            "sector": "Bank",
            "title": "Sample",
            "crawled_at": "2026-05-08T15:30:00Z",
        }]}),
        encoding="utf-8",
    )

    result = rebuild_manifest_from_db(db, tmp_path)
    db.close()
    assert result == {
        "total": 1,
        "from_db": 0,
        "legacy_carried": 1,
        "skipped_no_file": 0,
    }
    data = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert [a["id"] for a in data["articles"]] == [legacy_id]
