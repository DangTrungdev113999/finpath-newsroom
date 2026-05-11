"""Integration test — kb_loader can find BĐS topics."""
from pathlib import Path

from lib.kb_loader import KBLoader


def test_loader_finds_bds_residential_topics():
    loader = KBLoader(Path("kb/bds"))
    results = loader.search(["doanh số bán trước"])
    assert len(results) >= 1
    assert any("res-presales-backlog" in r["path"] for r in results)


def test_loader_finds_bds_legal_topics():
    loader = KBLoader(Path("kb/bds"))
    results = loader.search(["Luật Kinh doanh"])
    assert len(results) >= 1


def test_loader_finds_bds_master_reference():
    loader = KBLoader(Path("kb/bds"))
    results = loader.search(["6 lớp"])  # 6-layer mental model
    assert len(results) >= 1
    assert any("industry-master-reference" in r["path"] for r in results)


def test_loader_returns_all_21_files():
    loader = KBLoader(Path("kb/bds"))
    all_files = loader._all_files()
    md_files = [f for f in all_files if f.suffix == ".md"]
    assert len(md_files) == 21
