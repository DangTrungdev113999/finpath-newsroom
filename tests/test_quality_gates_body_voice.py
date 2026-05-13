"""Tests for V1.3 body voice gates in lib/quality_gates.

3 new gates:
- check_bao_chi_body — ban ≥2 báo chí verb occurrences (parallel title is_bao_chi)
- check_bold_density — per-format markdown bold target 3-5%
- check_actionable_closing — closing needs stance + quantified trigger

2 tightened gates:
- check_verdict_line — composes check_actionable_closing
- check_sentence_density — bonus for METAPHOR_MARKERS
"""
from __future__ import annotations
import pytest
from lib.quality_gates import (
    check_bao_chi_body,
    check_bold_density,
    check_actionable_closing,
    check_verdict_line,
    check_sentence_density,
)


# =====================================================================
# check_bao_chi_body — ≥2 BAO_CHI_BODY_VERBS occurrences in body → fail
# =====================================================================

def test_bao_chi_body_rejects_three_verbs():
    """Audit pattern: 'bàn giao + ghi nhận + công bố' → fail."""
    body = (
        "VHM Q1/2026 ghi nhận lợi nhuận 25.625 tỷ. Công ty công bố kế hoạch "
        "60.000 tỷ cho 2026, đã bàn giao 4.000 căn cho khách hàng."
    )
    result = check_bao_chi_body(body)
    assert result["pass"] is False
    assert "ghi nhận" in result["reason"] or "ghi nhận" in result.get("leaked_verbs", [])


def test_bao_chi_body_allows_one_verb():
    """1 occurrence (factual reporting) → pass."""
    body = (
        "VHM ăn 25.625 tỷ Q1, gấp 3 lần Vietcombank cùng kỳ. Lợi nhuận này "
        "được ghi nhận từ bàn giao Royal Island. Vốn 11.000 tỷ trái phiếu "
        "đi vào dự án Hải Vân Bay quý 2."
    )
    result = check_bao_chi_body(body)
    # Has "ghi nhận" + "bàn giao" — that's 2 → fail
    # Adjust: only 1 "ghi nhận"
    body_one = (
        "VHM ăn 25.625 tỷ Q1, gấp 3 lần Vietcombank cùng kỳ. Lợi nhuận này "
        "được ghi nhận từ Royal Island bàn lại quý sau."
    )
    result = check_bao_chi_body(body_one)
    assert result["pass"] is True


def test_bao_chi_body_allows_zero_verbs():
    """Pure bình dân body → pass."""
    body = (
        "VHM ăn 25.625 tỷ Q1, gấp 3 lần Vietcombank cùng kỳ. Vốn 11.000 tỷ "
        "trái phiếu bơm vào Hải Vân Bay quý 2/2026."
    )
    result = check_bao_chi_body(body)
    assert result["pass"] is True


def test_bao_chi_body_strips_skeptic_section():
    """Skeptic '## Góc nhìn ngược' section excluded."""
    body = (
        "VHM ăn 25.625 tỷ Q1.\n\n## Góc nhìn ngược\n"
        "Master ghi nhận công bố đặt mục tiêu phấn đấu hoàn thành kế hoạch."
    )
    result = check_bao_chi_body(body)
    # Skeptic section stripped before check → no báo chí in body proper
    assert result["pass"] is True


def test_bao_chi_body_returns_leaked_verbs_list():
    """Result includes which verbs leaked."""
    body = (
        "VHM ghi nhận 25.625 tỷ Q1. Công ty công bố kế hoạch mới. "
        "Đã bàn giao 4.000 căn cho khách."
    )
    result = check_bao_chi_body(body)
    assert result["pass"] is False
    assert "leaked_verbs" in result
    assert len(result["leaked_verbs"]) >= 2


# =====================================================================
# check_bold_density — per-format markdown bold target
# =====================================================================

def test_bold_density_flash_qa_min_3_absolute():
    """flash_qa: ≥3 bold absolute count (Twitter style short)."""
    body_pass = (
        "VHM **ăn 25.625 tỷ** Q1, **gấp 3 lần Vietcombank**. "
        "Trái phiếu **11.000 tỷ** bơm Hải Vân Bay Q2/2026. NĐT giữ 12 tháng."
    )
    result = check_bold_density(body_pass, "flash_qa")
    assert result["pass"] is True

    body_fail = "VHM ăn 25.625 tỷ Q1, gấp 3 lần Vietcombank. **1 bold thôi**."
    result = check_bold_density(body_fail, "flash_qa")
    assert result["pass"] is False


def test_bold_density_standard_qa_min_4_percent():
    """standard_qa: ≥4% density (1 bold per 25 words)."""
    # ~200 words → need ≥8 bold for 4%
    body_pass = " ".join(
        ["**bold**"] * 10 + ["word"] * 190
    )
    result = check_bold_density(body_pass, "standard_qa")
    assert result["pass"] is True

    body_fail = " ".join(["**bold**"] * 3 + ["word"] * 197)
    result = check_bold_density(body_fail, "standard_qa")
    assert result["pass"] is False


def test_bold_density_standard_listicle_min_5_percent():
    """standard_listicle: densest at ≥5% (1 bold per 20 words)."""
    body_pass = " ".join(["**b**"] * 15 + ["word"] * 235)  # 6%
    result = check_bold_density(body_pass, "standard_listicle")
    assert result["pass"] is True

    body_fail = " ".join(["**b**"] * 10 + ["word"] * 240)  # 4%
    result = check_bold_density(body_fail, "standard_listicle")
    assert result["pass"] is False


def test_bold_density_standard_narrative_min_3_percent():
    """standard_narrative: lower 3% (some prose flow OK)."""
    body_pass = " ".join(["**b**"] * 8 + ["word"] * 242)  # 3.2%
    result = check_bold_density(body_pass, "standard_narrative")
    assert result["pass"] is True


def test_bold_density_handles_zero_words():
    result = check_bold_density("", "flash_qa")
    assert result["pass"] is True  # no body to fail


# =====================================================================
# check_actionable_closing — stance + quantified trigger + no vague
# =====================================================================

def test_actionable_closing_passes_with_stance_and_trigger():
    """SSI-ESOP pattern: 'giữ 12 tháng nếu margin > 35K tỷ'."""
    body = (
        "SSI Q1 lãi 1.500 tỷ. **ESOP** thưởng nội bộ 180 tỷ.\n\n"
        "NĐT nên giữ 12 tháng nếu dư nợ margin vượt 35.000 tỷ Q2; "
        "cắt 30% nếu thị phần tụt dưới 8% Q3/2026."
    )
    result = check_actionable_closing(body)
    assert result["pass"] is True


def test_actionable_closing_rejects_vague_theo_doi():
    """VHM-cổ tức pattern: 'theo dõi hấp thụ làm chỉ báo sớm' → fail."""
    body = (
        "VHM chia cổ tức 60% kỷ lục.\n\n"
        "NĐT cần theo dõi tốc độ hấp thụ Hải Vân Bay Q2/2026 làm chỉ báo "
        "sớm cho năm 2027-2028."
    )
    result = check_actionable_closing(body)
    assert result["pass"] is False


def test_actionable_closing_rejects_no_stance_verb():
    """Closing có số nhưng thiếu stance verb → fail."""
    body = (
        "VHM Q1 ăn 25.625 tỷ.\n\n"
        "Hải Vân Bay Q2/2026 mục tiêu hấp thụ 40% trong 6 tháng."
    )
    result = check_actionable_closing(body)
    assert result["pass"] is False


def test_actionable_closing_rejects_no_quantified_trigger():
    """Closing có stance nhưng thiếu quantified trigger → fail."""
    body = (
        "ACB Q1 ăn lớn.\n\n"
        "NĐT nên giữ ACB dài hạn vì nền tảng vững chắc và quản trị tốt."
    )
    result = check_actionable_closing(body)
    assert result["pass"] is False


def test_actionable_closing_accepts_price_range_trigger():
    """Price range as quantified trigger → pass."""
    body = (
        "VHM phát hành trái phiếu lớn.\n\n"
        "NĐT nên cầm vùng 75-80 nghìn/cổ phiếu, cắt 30% nếu rơi dưới 70."
    )
    result = check_actionable_closing(body)
    assert result["pass"] is True


# =====================================================================
# check_verdict_line — composes actionable_closing (TIGHTEN)
# =====================================================================

def test_verdict_line_passes_with_actionable_closing():
    """Strong closing with all 3 elements + quantified."""
    body = (
        "ACB Q1 ăn 5.200 tỷ.\n\n"
        "NĐT đang cầm nên giữ 12-18 tháng nếu NIM duy trì trên 3,5% Q3/2026; "
        "giảm 30% vị thế nếu CASA tụt dưới 22%."
    )
    result = check_verdict_line(body)
    assert result["pass"] is True


def test_verdict_line_fails_when_actionable_closing_fails():
    """Closing vague → verdict_line fail via composed check."""
    body = (
        "VHM chia cổ tức 60%.\n\n"
        "NĐT cần theo dõi hấp thụ Hải Vân Bay làm chỉ báo sớm 2027."
    )
    result = check_verdict_line(body)
    assert result["pass"] is False


# =====================================================================
# check_sentence_density — METAPHOR_MARKERS bonus (TIGHTEN)
# =====================================================================

def test_sentence_density_accepts_metaphor_as_specific_element():
    """Sentence with 'gấp X lần' or 'như Y' counts toward density."""
    body = (
        "VHM Q1 ăn 25.625 tỷ, gấp 3 lần Vietcombank cùng kỳ. "
        "Cách viết này như một cú đập trực diện vào nhóm tài chính. "
        "Thật ra nhóm BĐS dẫn đầu cả index năm nay. "
        "Trái phiếu 11.000 tỷ bơm Hải Vân Bay Q2/2026."
    )
    result = check_sentence_density(body)
    assert result["pass"] is True
