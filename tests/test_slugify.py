"""Tests for lib.slugify — Vietnamese hook → URL-safe slug."""
import pytest
from lib.slugify import slugify_hook


def test_simple_question_hook():
    title = "Vì sao to nhất lại đi chậm nhất?"
    assert slugify_hook(title) == "vi-sao-to-nhat-lai-di-cham-nhat"


def test_declarative_paradox_hook():
    title = "TCB chia cổ tức 67% kỷ lục — nhưng phần lớn không phải tiền mặt"
    result = slugify_hook(title)
    assert result.startswith("tcb-chia-co-tuc-67-ky-luc-nhung-phan-lon")
    assert len(result) <= 60


def test_strips_diacritics():
    assert slugify_hook("Đánh đổi tốc độ lấy độ bền") == "danh-doi-toc-do-lay-do-ben"


def test_truncates_to_60_chars():
    long = "a " * 100
    result = slugify_hook(long)
    assert len(result) <= 60


def test_truncate_strips_trailing_partial_word():
    title = "VCB target 2026 chỉ 5 phần trăm Vì sao ngân hàng to nhất đi chậm"
    result = slugify_hook(title)
    assert len(result) <= 60
    assert not result.endswith("-")
    assert "-" in result
    last_word = result.rsplit("-", 1)[-1]
    assert len(last_word) >= 2


def test_drops_special_chars():
    assert slugify_hook("Đầu tư @ 2026!") == "dau-tu-2026"


def test_consecutive_hyphens_collapsed():
    assert slugify_hook("a   b   —   c") == "a-b-c"


def test_empty_falls_back():
    assert slugify_hook("") == "untitled"
    assert slugify_hook("???") == "untitled"
