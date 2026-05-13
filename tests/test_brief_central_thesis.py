"""Tests for lib.brief_central_thesis — schema normalizer V4/V5/empty."""
from __future__ import annotations

import pytest

from lib.brief_central_thesis import extract_central_thesis


class TestV5Schema:
    def test_picks_question_at_idx_zero(self) -> None:
        brief = {
            "ticker": "PVS",
            "deep_question_options": [
                {
                    "question": "Tiền mặt bằng 82% vốn hoá, vì sao thị trường định giá phần kinh doanh lõi của PVS gần bằng 0?",
                    "category": "comparison_deep",
                },
                {"question": "Câu hỏi khác?", "category": "paradox"},
            ],
        }
        result = extract_central_thesis(brief, body="", picked_idx=0)
        assert result["source"] == "v5_deep_question"
        assert "82% vốn hoá" in result["thesis"]
        assert "định giá" in result["thesis"]

    def test_picks_question_at_idx_one(self) -> None:
        brief = {
            "deep_question_options": [
                {"question": "Q0?", "category": "paradox"},
                {"question": "Q1 chính được pick?", "category": "why_now"},
            ],
        }
        result = extract_central_thesis(brief, body="", picked_idx=1)
        assert result["thesis"] == "Q1 chính được pick?"
        assert result["source"] == "v5_deep_question"

    def test_deep_question_field_alias(self) -> None:
        """Some briefs use deep_question instead of question key."""
        brief = {
            "deep_question_options": [
                {"deep_question": "Lý do FPT đổ 89 triệu USD vào Huế?", "category": "why_now"},
            ],
        }
        result = extract_central_thesis(brief, body="")
        assert result["source"] == "v5_deep_question"
        assert "FPT đổ 89 triệu USD" in result["thesis"]

    def test_angle_field_alias(self) -> None:
        """DXG-style briefs use angle field instead of question."""
        brief = {
            "deep_question_options": [
                {
                    "option_id": "A",
                    "angle": "Nghịch lý tăng trưởng: doanh thu +46% nhưng cổ đông mẹ thực nhận ít hơn năm trước?",
                    "stance_directive": {"direction": "bearish_neutral"},
                }
            ],
        }
        result = extract_central_thesis(brief, body="")
        assert result["source"] == "v5_deep_question"
        assert "doanh thu +46%" in result["thesis"]

    def test_hypothesis_field_alias(self) -> None:
        """Older briefs may use hypothesis instead of question."""
        brief = {
            "deep_question_options": [
                {"hypothesis": "STB nén chi phí nhân sự để giữ lợi nhuận?"}
            ],
        }
        result = extract_central_thesis(brief, body="")
        assert result["source"] == "v5_deep_question"
        assert "STB" in result["thesis"]


class TestV4Schema:
    def test_picks_insight_hypothesis_first_sentence(self) -> None:
        brief = {
            "ticker": "PVS",
            "angle_label": "Lãi gộp gấp ba, dự phòng gấp mười hai",
            "insight_hypothesis": (
                "PVS chủ động dồn 282 tỷ trích lập bảo hành vào Q1/2026 để giữ lợi nhuận thấp. "
                "Đây là cách quản lý kỳ vọng thận trọng của tổng công ty thuộc PVN."
            ),
        }
        result = extract_central_thesis(brief, body="")
        assert result["source"] == "v4_insight"
        assert "282 tỷ trích lập bảo hành" in result["thesis"]
        # First sentence only (≤200 chars)
        assert "quản lý kỳ vọng" not in result["thesis"]

    def test_insight_hypothesis_truncates_at_200_chars(self) -> None:
        brief = {
            "insight_hypothesis": "A" * 250 + ". Second sentence here.",
        }
        result = extract_central_thesis(brief, body="")
        assert len(result["thesis"]) <= 200


class TestEmptyFallback:
    def test_empty_brief_uses_body_opening(self) -> None:
        body = (
            "FPT Telecom (FOX) vừa thừa nhận không đủ tỷ lệ tự do giao dịch tối thiểu **10%** "
            "để giữ tư cách công ty đại chúng.\n\n- Bullet 1\n- Bullet 2"
        )
        result = extract_central_thesis("", body=body)
        assert result["source"] == "body_opening"
        assert "FPT Telecom" in result["thesis"]
        assert "công ty đại chúng" in result["thesis"]
        # No markdown leak
        assert "**" not in result["thesis"]

    def test_empty_brief_dict_uses_body(self) -> None:
        result = extract_central_thesis({}, body="Body line 1. Body line 2.")
        assert result["source"] == "body_opening"
        assert "Body line 1" in result["thesis"]

    def test_brief_string_json(self) -> None:
        result = extract_central_thesis(
            '{"deep_question_options": [{"question": "Test?"}]}',
            body="",
        )
        assert result["thesis"] == "Test?"


class TestEdgeCases:
    def test_no_brief_no_body_returns_empty(self) -> None:
        result = extract_central_thesis("", body="")
        assert result["thesis"] == ""
        assert result["source"] == "empty"

    def test_invalid_json_brief_falls_back_to_body(self) -> None:
        result = extract_central_thesis("{not valid json", body="Body opening here. Rest.")
        assert result["source"] == "body_opening"
        assert "Body opening here" in result["thesis"]

    def test_v5_picked_idx_out_of_range_falls_back(self) -> None:
        brief = {"deep_question_options": [{"question": "Only one"}]}
        result = extract_central_thesis(brief, body="Fallback body.", picked_idx=5)
        # Out-of-range should not crash; fallback to body opening
        assert result["source"] in ("body_opening", "v5_deep_question")

    def test_strips_markdown_bold_from_body(self) -> None:
        body = "**FPT** Telecom thừa nhận không đủ tỷ lệ **10%** tự do."
        result = extract_central_thesis("", body=body)
        assert "**" not in result["thesis"]
        assert "FPT" in result["thesis"]
