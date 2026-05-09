"""Tests for lib.kb_loader."""
from datetime import datetime, timezone

import pytest

from lib.kb_loader import KBLoader, freshness_warning


# Anchor "now" so tests don't depend on real wall clock.
NOW = datetime(2026, 5, 8, tzinfo=timezone.utc)


@pytest.fixture
def kb_dir(tmp_path):
    """Create a fake kb/ tree with 2 files in frameworks/."""
    fw = tmp_path / "frameworks"
    fw.mkdir()
    (fw / "big4-pattern.md").write_text(
        "---\ntitle: \"Big4 vs tư nhân pattern\"\ncategory: frameworks\n---\n\n"
        "Big4 (VCB BID CTG VietinBank) under-promise hơn tư nhân.",
        encoding="utf-8",
    )
    (fw / "casa-evolution.md").write_text(
        "---\ntitle: \"CASA evolution\"\ncategory: frameworks\n---\n\n"
        "Tỷ lệ CASA tăng trend 2020-2025.",
        encoding="utf-8",
    )
    return tmp_path


def test_search_returns_matching_files(kb_dir):
    loader = KBLoader(kb_dir)
    results = loader.search(["Big4"])
    assert len(results) == 1
    assert "big4-pattern.md" in results[0]["path"]


def test_search_multiple_keywords_AND(kb_dir):
    loader = KBLoader(kb_dir)
    results = loader.search(["Big4", "VCB"])
    assert len(results) == 1


def test_search_no_match(kb_dir):
    loader = KBLoader(kb_dir)
    results = loader.search(["NoSuchTopic"])
    assert results == []


def test_load_topic_returns_full_content(kb_dir):
    loader = KBLoader(kb_dir)
    content = loader.load_topic("frameworks/big4-pattern.md")
    assert "under-promise" in content


def test_load_topic_missing_raises(kb_dir):
    loader = KBLoader(kb_dir)
    with pytest.raises(FileNotFoundError):
        loader.load_topic("frameworks/missing.md")


def test_search_by_category(kb_dir):
    loader = KBLoader(kb_dir)
    results = loader.search(["CASA"], category="frameworks")
    assert len(results) == 1
    assert results[0]["category"] == "frameworks"


# ---- freshness_warning() — Bug E fix (Phase F T4) ----------------------------


def test_freshness_recent_returns_none():
    """Row verified 3 ngày trước (within default 30d) → no warning."""
    row = {"last_verified": "2026-05-05"}
    assert freshness_warning(row, now=NOW) is None


def test_freshness_stale_returns_warning():
    """Row verified >30d (Jan 2026 vs now=May 2026) → warning."""
    row = {"last_verified": "2026-01-01"}
    warn = freshness_warning(row, now=NOW)
    assert warn is not None
    assert "stale" in warn
    assert "ngày" in warn


def test_freshness_missing_returns_warning():
    """Row without last_verified field → warning."""
    row = {"target_lntt_ty": 39400}
    warn = freshness_warning(row, now=NOW)
    assert warn is not None
    assert "chưa verified" in warn


def test_freshness_unknown_returns_warning():
    """Row with last_verified='unknown' (legacy marker) → warning."""
    row = {"last_verified": "unknown"}
    warn = freshness_warning(row, now=NOW)
    assert warn is not None
    assert "chưa verified" in warn


def test_freshness_invalid_format_returns_warning():
    """Row with garbage date string → warning (defensive)."""
    row = {"last_verified": "not-a-date"}
    warn = freshness_warning(row, now=NOW)
    assert warn is not None
    assert "không parse được" in warn


def test_freshness_custom_max_days():
    """Row 10 days old with max_days=5 → warning (custom threshold)."""
    row = {"last_verified": "2026-04-28"}  # 10 ngày trước NOW=2026-05-08
    warn = freshness_warning(row, max_days=5, now=NOW)
    assert warn is not None
    assert "stale" in warn
    # Same row with default 30d → no warning
    assert freshness_warning(row, now=NOW) is None
