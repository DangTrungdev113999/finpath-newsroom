"""Tests for lib.kb_loader."""
import pytest
from pathlib import Path

from lib.kb_loader import KBLoader


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
