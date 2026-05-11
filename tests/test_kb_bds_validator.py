"""Tests for lib.kb_bds_validator — enforces 5 KB BĐS principles."""
from pathlib import Path

import pytest

from lib.kb_bds_validator import validate_kb_file, VALID_APPLIES_TO


VALID_FILE_CONTENT = """---
category: frameworks
title: "BDS-Test-Topic"
last_updated: 2026-05-11
notion_page_id: "abc-123"
source_url: "https://notion.so/abc"
applies_to: ["residential"]
---

# Test Topic

Intro paragraph.

## Khái niệm & cơ chế

Một số định nghĩa.

## Pitfalls (đọc số dễ sai)

- **Bẫy 1**: mô tả bẫy thứ nhất với độ dài đủ thông tin.
- **Bẫy 2**: mô tả bẫy thứ hai với ví dụ lịch sử minh họa.

## Case study lịch sử

> **2024 — Residential — Lag P&L**:
> Mô tả case study.
>
> **Không analogize sang**: KCN (xem `bds-kcn-lease-structure.md`).

## Source log

- https://notion.so/abc
- Stamp: build 2026-05-11. Review every 3 years.
"""


@pytest.fixture
def valid_file(tmp_path):
    f = tmp_path / "bds-test.md"
    f.write_text(VALID_FILE_CONTENT, encoding="utf-8")
    return f


def test_valid_file_passes(valid_file):
    assert validate_kb_file(valid_file) == []


def test_missing_applies_to_fails(tmp_path):
    f = tmp_path / "bad.md"
    bad = VALID_FILE_CONTENT.replace('applies_to: ["residential"]\n', "")
    f.write_text(bad, encoding="utf-8")
    violations = validate_kb_file(f)
    assert any("applies_to" in v for v in violations)


def test_invalid_applies_to_value_fails(tmp_path):
    f = tmp_path / "bad.md"
    bad = VALID_FILE_CONTENT.replace('["residential"]', '["bogus_category"]')
    f.write_text(bad, encoding="utf-8")
    violations = validate_kb_file(f)
    assert any("invalid" in v.lower() for v in violations)


def test_missing_khai_niem_section_fails(tmp_path):
    f = tmp_path / "bad.md"
    bad = VALID_FILE_CONTENT.replace("## Khái niệm & cơ chế", "## Random Section")
    f.write_text(bad, encoding="utf-8")
    violations = validate_kb_file(f)
    assert any("Khái niệm" in v for v in violations)


def test_missing_pitfalls_section_fails(tmp_path):
    f = tmp_path / "bad.md"
    bad = VALID_FILE_CONTENT.replace("## Pitfalls (đọc số dễ sai)", "## Random")
    f.write_text(bad, encoding="utf-8")
    violations = validate_kb_file(f)
    assert any("Pitfalls" in v for v in violations)


def test_pitfall_count_below_2_fails(tmp_path):
    f = tmp_path / "bad.md"
    bad = VALID_FILE_CONTENT.replace(
        "- **Bẫy 2**: mô tả bẫy thứ hai với ví dụ lịch sử minh họa.\n",
        "",
    )
    f.write_text(bad, encoding="utf-8")
    violations = validate_kb_file(f)
    assert any("pitfall" in v.lower() and "2" in v for v in violations)


def test_missing_source_log_fails(tmp_path):
    f = tmp_path / "bad.md"
    bad = VALID_FILE_CONTENT.split("## Source log")[0]
    f.write_text(bad, encoding="utf-8")
    violations = validate_kb_file(f)
    assert any("Source log" in v for v in violations)


def test_valid_applies_to_enum_values():
    expected = {"residential", "kcn", "retail", "office", "resort", "data_center", "all"}
    assert VALID_APPLIES_TO == expected
