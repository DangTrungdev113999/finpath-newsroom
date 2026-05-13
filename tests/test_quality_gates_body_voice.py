"""Tests for V1.3 body voice gates in lib/quality_gates.

V1.5-lite (2026-05-13 PM): check_bao_chi_body dropped. 3 new gates added:
- check_han_viet_formal — ban ≥2 Hán-Việt formal terms
- check_abbreviation_expanded — 3-4 letter upper must be expanded on first occurrence
- check_price_realistic — closing price target ±50% Finpath current

Kept gates:
- check_bold_density — per-format markdown bold target 3-5%
- check_actionable_closing — closing needs stance + quantified trigger

Tightened gates:
- check_verdict_line — composes check_actionable_closing
- check_sentence_density — bonus for METAPHOR_MARKERS
"""
from __future__ import annotations
import pytest
from lib.quality_gates import (
    check_bold_density,
    check_actionable_closing,
    check_verdict_line,
    check_sentence_density,
)


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


# =====================================================================
# V1.4 check_min_sentence_richness — reject body >20% câu <10 từ
# =====================================================================

def test_min_sentence_richness_rejects_stb_pattern():
    """STB bài 1 audit: 3/11 sentences ≤9 từ (27%) → fail.

    Pattern: opening tail + bullet 1 tail + bullet 3 tail — all 7-9 từ.
    """
    from lib.quality_gates import check_min_sentence_richness
    body = (
        "**Q1/2026: 28 ngân hàng xén 3.026 người**, riêng Sacombank gánh **~85% "
        "tổng cắt giảm ngành bank**. Ngành chia hai phe đi ngược chiều.\n\n"
        "- **STB cắt sâu nhất 10 năm**: ngân hàng mẹ tống **2.570 người**, "
        "hợp nhất bay **2.736** trong Q1 = **16% lực lượng**, kéo xuống "
        "**14.080**, thấp nhất từ 2016. Sau giai đoạn 2017-2024 luôn neo trên 18.000 người.\n"
        "- **Phe cắt nối đuôi STB**: BIDV bớt **279**, TPBank **226**, "
        "Eximbank **222**, VIB **217**. Bộ ba STB + TPB + VIB xén gấp đôi 18 "
        "tháng, gom **4.600 người** rời khỏi hệ thống, tín hiệu tinh gọn mạnh nhất.\n"
        "- **Phe ngược lại nhồi người vào**: VPBank tích **+362** kẻ tuyển "
        "nhiều nhất ngành, Techcombank lấn thêm **176** lên **11.636**, LPBank "
        "gom **142** sau năm thanh lọc. Bộ ba VPB+TCB+LPB nhồi gần **700 người** Q1.\n\n"
        "NĐT đang cầm STB nên giữ qua quý 2 với điều kiện chi phí hoạt động "
        "xén dưới **3.200 tỷ**, nếu không nên cắt 30% vị thế Q3."
    )
    result = check_min_sentence_richness(body)
    assert result["pass"] is False
    assert "27%" in result["reason"] or result["short_count"] >= 3


def test_min_sentence_richness_passes_when_compound_sentences():
    """V1.4 fix: tail fragments merged with main sentence via connector."""
    from lib.quality_gates import check_min_sentence_richness
    body = (
        "Q1/2026: 28 ngân hàng xén 3.026 người, riêng Sacombank gánh ~85% "
        "tổng cắt giảm — ngành chia hai phe đi ngược chiều vì 2 chiến lược trái nhau.\n\n"
        "- STB cắt sâu nhất 10 năm: ngân hàng mẹ tống 2.570 người, hợp nhất "
        "bay 2.736 trong Q1 = 16% lực lượng, kéo xuống 14.080 từ mức 18.000 "
        "của giai đoạn 2017-2024.\n"
        "- Phe cắt nối đuôi STB gồm BIDV bớt 279, TPBank 226, Eximbank 222 "
        "và VIB 217, riêng bộ ba STB + TPB + VIB gom 4.600 người rời hệ thống "
        "trong 18 tháng qua.\n\n"
        "NĐT đang cầm STB nên giữ qua quý 2 với điều kiện chi phí hoạt động "
        "xén dưới 3.200 tỷ, nếu không nên cắt 30% vị thế Q3."
    )
    result = check_min_sentence_richness(body)
    assert result["pass"] is True


def test_min_sentence_richness_excludes_bullet_header_only():
    """Bullet header `**Foo**:` lines KHÔNG count as countable sentence."""
    from lib.quality_gates import check_min_sentence_richness
    # 4 long content sentences + bullet headers stripped
    body = (
        "Opening paragraph with enough words to count as full sentence in body voice.\n\n"
        "- **Header 1**: Bullet content has at least ten words explaining mechanism clearly here.\n"
        "- **Header 2**: Another bullet with sufficient words to count properly above threshold.\n\n"
        "Closing sentence is also long enough to count toward sentence richness density check."
    )
    result = check_min_sentence_richness(body)
    assert result["pass"] is True


def test_min_sentence_richness_handles_zero_countable():
    """Edge case: body empty or only bullet headers — pass (no division by zero)."""
    from lib.quality_gates import check_min_sentence_richness
    result = check_min_sentence_richness("")
    assert result["pass"] is True

    body_only_headers = "- **Foo**:\n- **Bar**:"
    result = check_min_sentence_richness(body_only_headers)
    assert result["pass"] is True


def test_min_sentence_richness_strips_skeptic_section():
    """Skeptic '## Góc nhìn ngược' section excluded from count."""
    from lib.quality_gates import check_min_sentence_richness
    body_with_skeptic = (
        "Opening paragraph with sufficient words to count toward density check.\n\n"
        "- **Bullet**: Long bullet with at least ten words explaining mechanism clearly.\n\n"
        "Closing sentence long enough to count toward sentence richness check.\n\n"
        "## Góc nhìn ngược\n\nNgắn cụt. Ngắn cụt nữa. Quá ngắn."
    )
    result = check_min_sentence_richness(body_with_skeptic)
    # Body proper (skeptic stripped) has 3 long sentences → pass
    assert result["pass"] is True


# =====================================================================
# V1.5-lite check_han_viet_formal — reject body ≥2 Hán-Việt formal terms
# =====================================================================

def test_han_viet_formal_rejects_two_terms():
    """Body với 2 terms từ HAN_VIET_FORMAL_BAN → fail."""
    from lib.quality_gates import check_han_viet_formal
    body = (
        "VHM phát hành 11.000 tỷ cấu trúc vốn mới. "
        "Tái định giá toàn danh mục sau Q1/2026."
    )
    result = check_han_viet_formal(body)
    assert result["pass"] is False


def test_han_viet_formal_allows_one_term():
    """1 occurrence OK (factual context)."""
    from lib.quality_gates import check_han_viet_formal
    body = "VHM ăn 25.625 tỷ Q1. Tái định giá dự án Hải Vân Bay sau bàn giao."
    result = check_han_viet_formal(body)
    assert result["pass"] is True


def test_han_viet_formal_zero_terms_passes():
    """Pure bình dân → pass."""
    from lib.quality_gates import check_han_viet_formal
    body = (
        "VHM ăn 25.625 tỷ Q1, gấp 3 lần Vietcombank cùng kỳ. "
        "Định giá lại danh mục sau Q1/2026."
    )
    result = check_han_viet_formal(body)
    assert result["pass"] is True


def test_han_viet_formal_strips_skeptic_section():
    """Skeptic '## Góc nhìn ngược' section stripped before check."""
    from lib.quality_gates import check_han_viet_formal
    body = (
        "VHM ăn 25.625 tỷ Q1.\n\n## Góc nhìn ngược\n"
        "Master độc bản hội đủ tái định giá phương án xử lý."
    )
    result = check_han_viet_formal(body)
    assert result["pass"] is True


# =====================================================================
# V1.5-lite check_abbreviation_expanded — 3-4 letter upper must be expanded
# =====================================================================

def test_abbreviation_expanded_rejects_bare_bca():
    """BCA without expansion first mention → fail."""
    from lib.quality_gates import check_abbreviation_expanded
    body = "BCA nhận 50% vốn FPT từ tháng 7/2025."
    result = check_abbreviation_expanded(body)
    assert result["pass"] is False
    assert "BCA" in result["missing_expansions"]


def test_abbreviation_expanded_accepts_first_expansion():
    """'Bộ Công An (BCA)' first mention → pass."""
    from lib.quality_gates import check_abbreviation_expanded
    body = "Bộ Công An (BCA) nhận 50% vốn FPT. BCA nắm đa số."
    result = check_abbreviation_expanded(body)
    assert result["pass"] is True


def test_abbreviation_expanded_naturalized_skipped():
    """ESOP / NIM / ROE / IPO trong NATURALIZED allowlist → skip."""
    from lib.quality_gates import check_abbreviation_expanded
    body = "SSI bán ESOP 100 tỷ. NIM ngân hàng tăng 30bps."
    result = check_abbreviation_expanded(body)
    assert result["pass"] is True


def test_abbreviation_expanded_tickers_skipped():
    """Ticker uppercase (FPT/VHM/STB) → skip even không expand."""
    from lib.quality_gates import check_abbreviation_expanded
    body = "FPT Q1 lãi 5.000 tỷ. VHM ăn 25.625 tỷ. STB cắt 2.700 người."
    result = check_abbreviation_expanded(body)
    assert result["pass"] is True


def test_abbreviation_expanded_multi_unknown_fails():
    """Multiple unknown abbreviations not expanded → fail."""
    from lib.quality_gates import check_abbreviation_expanded
    body = "GRDP Huế tăng 8%. SCIC chuyển 50% cho BCA tháng 7/2025."
    result = check_abbreviation_expanded(body)
    assert result["pass"] is False
    assert "GRDP" in result["missing_expansions"]
    assert "SCIC" in result["missing_expansions"]
    assert "BCA" in result["missing_expansions"]


# =====================================================================
# V1.5-lite check_price_realistic — Finpath ±50% current
# =====================================================================

def test_price_realistic_pass_when_within_range(monkeypatch):
    """Price target trong ±50% current → pass."""
    from lib.quality_gates import check_price_realistic
    def fake_get_price(ticker):
        return 70_000
    monkeypatch.setattr("lib.quality_gates._fetch_current_price", fake_get_price)
    body = "NĐT nên tích lũy FPT vùng dưới 85 nghìn/cp trong 18 tháng."
    result = check_price_realistic(body, ticker="FPT")
    assert result["pass"] is True


def test_price_realistic_fail_when_out_of_range(monkeypatch):
    """Price target ngoài ±50% current → fail (FPT 145 nghìn khi thực tế 70)."""
    from lib.quality_gates import check_price_realistic
    def fake_get_price(ticker):
        return 70_000
    monkeypatch.setattr("lib.quality_gates._fetch_current_price", fake_get_price)
    body = "NĐT nên tích lũy FPT dưới 145 nghìn/cp trong 18-24 tháng."
    result = check_price_realistic(body, ticker="FPT")
    assert result["pass"] is False


def test_price_realistic_degrades_when_api_unavailable(monkeypatch):
    """Finpath API fail → pass with warning (don't block pipeline)."""
    from lib.quality_gates import check_price_realistic
    def fake_get_price(ticker):
        raise ConnectionError("Finpath unavailable")
    monkeypatch.setattr("lib.quality_gates._fetch_current_price", fake_get_price)
    body = "NĐT nên tích lũy FPT dưới 145 nghìn/cp."
    result = check_price_realistic(body, ticker="FPT")
    assert result["pass"] is True


def test_price_realistic_no_price_in_closing_passes(monkeypatch):
    """Body without price target → pass."""
    from lib.quality_gates import check_price_realistic
    def fake_get_price(ticker):
        return 70_000
    monkeypatch.setattr("lib.quality_gates._fetch_current_price", fake_get_price)
    body = "NĐT nên cầm FPT 12 tháng nếu margin >35K tỷ Q3/2026."
    result = check_price_realistic(body, ticker="FPT")
    assert result["pass"] is True
