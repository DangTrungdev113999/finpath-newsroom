"""Tests for lib.quality_gates V4.0 — 5 gates."""
import pytest
from lib.quality_gates import (
    check_no_english_jargon,
    check_no_english_jargon_narrative,
    check_no_english_jargon_skeptic,
    check_word_count,
    check_body_pattern,
    check_title_as_hook,
    check_no_metadata_leak,
    check_all,
)


# === Gate 1: 0% English jargon ===

def test_no_english_jargon_passes_clean_vietnamese():
    body = "Lợi nhuận trước thuế đạt **11.803 tỷ đồng**, tăng 9% so cùng kỳ. Nợ xấu 0,62%."
    assert check_no_english_jargon(body)["pass"] is True


def test_no_english_jargon_fails_on_NPL():
    assert check_no_english_jargon("NPL 1,05% tăng nhẹ.")["pass"] is False


def test_no_english_jargon_fails_on_momentum():
    assert check_no_english_jargon("TCB có momentum mạnh.")["pass"] is False


def test_no_english_jargon_allows_proper_nouns():
    body = "Vietcombank và Techcombank công bố KQKD Q1/2026. ĐHĐCĐ ngày 25/4."
    assert check_no_english_jargon(body)["pass"] is True


# === Gate 1b: 0% English jargon trong narrative brief (Bug B fix) ===

def test_narrative_pure_vietnamese_passes():
    assert check_no_english_jargon_narrative(["Bài chọn vì độ mới và sức nặng"])["pass"] is True


def test_narrative_with_english_fails():
    result = check_no_english_jargon_narrative(["Bài này tốt vì có tradeoff hay"])
    assert result["pass"] is False
    assert "tradeoff" in result["reason"].lower()


def test_narrative_multi_field_concat():
    result = check_no_english_jargon_narrative(["OK", "Có Big4 reference", "Bình thường"])
    assert result["pass"] is False


def test_narrative_empty_list_passes():
    assert check_no_english_jargon_narrative([])["pass"] is True


def test_narrative_empty_strings_pass():
    assert check_no_english_jargon_narrative(["", "", ""])["pass"] is True


def test_big4_passes_body_but_fails_narrative():
    """Bug B split fix — `big4` is legit Vietnamese banking shorthand in Master
    body (analog to ĐHĐCĐ) but banned in Story Editor narratives. Body gate
    must NOT silently broaden via narrative-extra dict."""
    body_text = "Big4 đặt cược vào tín dụng doanh nghiệp vừa nhỏ."
    assert check_no_english_jargon(body_text)["pass"] is True
    narrative_result = check_no_english_jargon_narrative([body_text])
    assert narrative_result["pass"] is False
    assert "big4" in narrative_result["reason"].lower()


@pytest.mark.parametrize("term", ["funding", "big4", "forward-looking", "cross-check"])
def test_narrative_extra_jargon_each_term_blocks(term):
    """Guard against silent dict shrinkage — every term in
    ENGLISH_JARGON_NARRATIVE_EXTRA must individually trip the narrative gate."""
    result = check_no_english_jargon_narrative([f"Bài có nhắc tới {term} rất rõ"])
    assert result["pass"] is False
    assert term in result["reason"].lower()


# === Gate 1c: Skeptic English jargon (Bug C fix) ===

def test_skeptic_pure_vietnamese_passes():
    body = "Bài Master sai về biên lãi vay khi không nhắc đến chi phí vốn quý này."
    assert check_no_english_jargon_skeptic(body)["pass"] is True


def test_skeptic_unexplained_jargon_fails():
    # Use NIM (in ENGLISH_JARGON) — bare jargon without explanation must fail.
    result = check_no_english_jargon_skeptic("Bài quên nhắc NIM quý này thấp hơn cùng kỳ.")
    assert result["pass"] is False
    assert "nim" in result["reason"].lower()


def test_skeptic_unexplained_eps_fails():
    result = check_no_english_jargon_skeptic("Bài quên nhắc EPS Q1 chỉ đạt 580 đồng.")
    assert result["pass"] is False
    assert "eps" in result["reason"].lower()


def test_skeptic_explained_eps_passes():
    result = check_no_english_jargon_skeptic("EPS (lợi nhuận trên mỗi cổ phiếu) MB Q1 chỉ 580 đồng.")
    assert result["pass"] is True


def test_skeptic_multi_jargon_explained_passes():
    body = "NIM (biên lãi vay) và CASA (tỷ lệ tiền gửi không kỳ hạn) đều giảm trong quý."
    assert check_no_english_jargon_skeptic(body)["pass"] is True


def test_skeptic_one_explained_one_unexplained_fails():
    body = "NIM (biên lãi vay) ổn nhưng CASA không nhắc — thiếu sót lớn."
    result = check_no_english_jargon_skeptic(body)
    assert result["pass"] is False
    assert "casa" in result["reason"].lower()


def test_skeptic_case_insensitive():
    # Lowercase explained → pass
    assert check_no_english_jargon_skeptic("Nim (biên lãi vay) thấp.")["pass"] is True
    # Lowercase unexplained → fail
    assert check_no_english_jargon_skeptic("nim không giải thích.")["pass"] is False


def test_skeptic_jargon_at_sentence_start():
    # Bare jargon at sentence start, no explanation → fail
    result = check_no_english_jargon_skeptic("NIM thấp.")
    assert result["pass"] is False
    assert "nim" in result["reason"].lower()


def test_skeptic_empty_passes():
    assert check_no_english_jargon_skeptic("")["pass"] is True
    assert check_no_english_jargon_skeptic("   ")["pass"] is True


# === Gate 2: Word count 200-400 ===

def test_word_count_in_range_passes():
    assert check_word_count(" ".join(["w"] * 300))["pass"] is True


def test_word_count_too_long_fails():
    assert check_word_count(" ".join(["w"] * 450))["pass"] is False


def test_word_count_too_short_fails():
    assert check_word_count(" ".join(["w"] * 100))["pass"] is False


# === Gate 3: Body pattern — 1 paragraph + 3-7 bullets + closing ===

VALID_BODY = """Đại hội cổ đông Techcombank 25/4 thông qua chia cổ tức tổng 67% — nhưng câu chuyện thật là chiến lược ngược chiều thị trường, ngân hàng đang đánh đổi.

- **Cổ tức 67% tách thành hai phần khác bản chất**: 7% tiền mặt tương đương 4.960 tỷ đồng, còn 60% là cổ phiếu thưởng phát hành từ lợi nhuận giữ lại — không rút đồng tiền mặt nào khỏi ngân hàng.

- **Lần đầu lịch sử BĐS giảm xuống 28,9%**: bán lẻ và doanh nghiệp vừa nhỏ tăng 33% so cùng kỳ, đạt 395 nghìn tỷ — bù vào chỗ trống bằng phân khúc rủi ro thấp hơn.

- **CEO thừa nhận hy sinh 5.000 tỷ lợi nhuận tiềm năng mỗi năm**: đánh đổi này nhằm duy trì 3 lớp phòng thủ thanh khoản theo chuẩn quốc tế mới — chiến lược dài hạn không phải phản xạ chu kỳ.

TCB phù hợp nhà đầu tư giá trị nắm trên 12 tháng — không phù hợp lướt sóng kỳ vọng đà ngắn hạn.
"""


def test_body_pattern_valid_passes():
    assert check_body_pattern(VALID_BODY)["pass"] is True


def test_body_pattern_no_opening_paragraph_fails():
    body = """- **Bullet 1**: opening missing này phải là paragraph mới đúng pattern V4.0 thật sự.
- **Bullet 2**: another bullet với content đầy đủ ít nhất hai mươi từ để qua check substantive.
- **Bullet 3**: third bullet cũng đầy đủ content và bold highlight đặt đầu cho rõ.

Closing sentence here."""
    result = check_body_pattern(body)
    assert result["pass"] is False
    assert "opening" in result["reason"].lower()


def test_body_pattern_too_few_bullets_fails():
    body = """Opening paragraph đầy đủ ba mươi từ trở lên mô tả sự kiện và đặt setup cho phần thân bài, làm rõ tension.

- **Bullet 1**: chỉ có một bullet không đủ pattern V4.0 cần ba bullet trở lên cho mechanism.

Closing.
"""
    assert check_body_pattern(body)["pass"] is False


def test_body_pattern_too_many_bullets_fails():
    bullets = "\n".join(
        [f"- **Bold {i}**: bullet content đầy đủ ít nhất hai mươi từ để pass substantive check trong gate này." for i in range(1, 9)]
    )
    body = f"Opening paragraph đầy đủ ba mươi từ mô tả sự kiện và đặt setup cho thân bài rõ ràng tension.\n\n{bullets}\n\nClosing.\n"
    assert check_body_pattern(body)["pass"] is False


def test_body_pattern_bullet_too_short_fails():
    body = """Opening paragraph đầy đủ ba mươi từ trở lên mô tả sự kiện và đặt setup cho thân bài làm rõ tension.

- **Bold**: short.
- **Bold 2**: cũng ngắn.
- **Bold 3**: vẫn ngắn.

Closing.
"""
    assert check_body_pattern(body)["pass"] is False


def test_body_pattern_bullet_no_bold_fails():
    body = """Opening paragraph đầy đủ ba mươi từ trở lên mô tả sự kiện và đặt setup cho thân bài làm rõ tension đó.

- Plain bullet content đầy đủ hai mươi từ nhưng không có bold highlight cần thiết theo V4.0 pattern.
- Plain bullet 2 cũng không có bold highlight nên fail check substantive vì không emphasis keypoint.
- Plain bullet 3 tương tự thiếu bold tag.

Closing.
"""
    assert check_body_pattern(body)["pass"] is False


def test_body_pattern_can_de_y_section_fails():
    body = """Opening paragraph đầy đủ ba mươi từ trở lên mô tả sự kiện và đặt setup cho thân bài làm rõ tension.

- **Bold 1**: bullet content đầy đủ ít nhất hai mươi từ để pass substantive check trong gate này.
- **Bold 2**: bullet content cũng đủ hai mươi từ để pass substantive check thực sự đấy.
- **Bold 3**: bullet cuối cùng cũng đủ content và bold highlight đầu cho rõ ràng.

## Cần để ý

Caveat narrative.

Closing.
"""
    result = check_body_pattern(body)
    assert result["pass"] is False
    assert "cần để ý" in result["reason"].lower() or "can de y" in result["reason"].lower()


# === Gate 4: Title-as-hook ===

def test_title_question_passes():
    assert check_title_as_hook("Vì sao ngân hàng to nhất đi chậm nhất?")["pass"] is True


def test_title_paradox_dash_passes():
    assert check_title_as_hook("TCB hy sinh 5.000 tỷ — đổi lấy gì?")["pass"] is True


def test_title_summary_fails():
    assert check_title_as_hook("TCB Q1/2026 lãi 8.900 tỷ tăng 22%")["pass"] is False


def test_title_with_tension_word_passes():
    assert check_title_as_hook("VCB chấp nhận tăng trưởng chậm — đánh đổi rủi ro")["pass"] is True


def test_title_dash_no_tension_fails():
    assert check_title_as_hook("TCB Q1/2026 — kết quả mới nhất")["pass"] is False


# === Gate 5: No metadata leak ===

def test_no_metadata_leak_fails_on_strategic_shift():
    assert check_no_metadata_leak("Đây là tin strategic-shift quan trọng.")["pass"] is False


def test_no_metadata_leak_passes_clean():
    assert check_no_metadata_leak("Đây là tin chuyển hướng chiến lược.")["pass"] is True


# === check_all ===

def test_check_all_returns_5_gates():
    result = check_all("Test body.", title="Test?")
    assert set(result.keys()) == {
        "no_english_jargon", "word_count", "body_pattern",
        "title_as_hook", "no_metadata_leak"
    }


# === V5.0 Phase 1.5 / B-30 — no_hedging gate ===
# B-30 (V5.1.2): primary path = LLM-as-judge. Fallback = keyword (V5.0).
# These tests force the fallback path via `monkeypatch.delenv` so they remain
# deterministic + free regardless of whether ANTHROPIC_API_KEY is set in the
# host environment. LLM-mode coverage lives in the B-30 block at end of file.

def test_no_hedging_pass(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from lib.quality_gates import check_no_hedging
    body = "VCB sẽ tăng trưởng. NĐT nên giữ. Q1 đang mạnh."
    assert check_no_hedging(body)["pass"] is True


def test_no_hedging_rejects_co_the(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from lib.quality_gates import check_no_hedging
    body = "VCB có thể tăng trưởng. NĐT nên giữ."
    result = check_no_hedging(body)
    assert result["pass"] is False
    assert "có thể" in result["reason"]


def test_no_hedging_rejects_tuy_thuoc(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from lib.quality_gates import check_no_hedging
    body = "Tăng trưởng tùy thuộc thị trường."
    assert check_no_hedging(body)["pass"] is False


def test_no_hedging_rejects_dang_theo_doi(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from lib.quality_gates import check_no_hedging
    body = "Đây là sự kiện đáng theo dõi trong tương lai."
    assert check_no_hedging(body)["pass"] is False


def test_no_hedging_rejects_kha_nang_cao(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from lib.quality_gates import check_no_hedging
    body = "Khả năng cao sẽ tăng. Nhưng chưa rõ."
    result = check_no_hedging(body)
    assert result["pass"] is False


# === V5.0 Phase 1.5 — verdict_line gate ===

VERDICT_OK = """
Tích cực dài hạn cho VCB. NĐT đang cầm nên giữ 12 tháng — chiến lược phòng thủ Q1 sẽ thành lợi thế.
"""

VERDICT_MISSING_DIRECTION = """
NĐT đang cầm nên giữ 12 tháng — chiến lược phòng thủ Q1 sẽ thành lợi thế.
"""

VERDICT_MISSING_TIMEFRAME = """
Tích cực cho VCB. NĐT đang cầm nên giữ — chiến lược phòng thủ sẽ thành lợi thế.
"""

VERDICT_MISSING_HOLDER_ACTION = """
Tích cực dài hạn cho VCB trong 12 tháng tới.
"""


def test_verdict_line_pass():
    from lib.quality_gates import check_verdict_line
    body = "Opening paragraph here.\n\n- bullet\n\n" + VERDICT_OK
    assert check_verdict_line(body)["pass"] is True


def test_verdict_line_rejects_missing_direction():
    from lib.quality_gates import check_verdict_line
    body = "Opening here.\n\n- bullet\n\n" + VERDICT_MISSING_DIRECTION
    result = check_verdict_line(body)
    assert result["pass"] is False
    assert "direction" in result["reason"]


def test_verdict_line_rejects_missing_timeframe():
    from lib.quality_gates import check_verdict_line
    body = "Opening here.\n\n- bullet\n\n" + VERDICT_MISSING_TIMEFRAME
    result = check_verdict_line(body)
    assert result["pass"] is False
    assert "timeframe" in result["reason"]


def test_verdict_line_rejects_missing_holder_action():
    from lib.quality_gates import check_verdict_line
    body = "Opening here.\n\n- bullet\n\n" + VERDICT_MISSING_HOLDER_ACTION
    result = check_verdict_line(body)
    assert result["pass"] is False
    assert "action_for_holder" in result["reason"]


# === V5.0 Phase 1.5 — stance_consistency gate ===

BULLISH_BODY = "VCB tăng trưởng tích cực, đáng giữ. Cơ hội mạnh, ổn định lợi thế."
BEARISH_BODY = "VCB có rủi ro yếu. Cảnh báo căng thẳng. Đỉnh ngắn hạn đáng lo."
MIXED_BODY = "VCB tăng trưởng tích cực nhưng rủi ro cũng cao. Cảnh báo cần lưu ý."


def test_stance_bullish_matches():
    from lib.quality_gates import check_stance_consistency
    assert check_stance_consistency(BULLISH_BODY, "bullish")["pass"] is True


def test_stance_bearish_matches():
    from lib.quality_gates import check_stance_consistency
    assert check_stance_consistency(BEARISH_BODY, "bearish")["pass"] is True


def test_stance_bullish_brief_bearish_body_rejects():
    from lib.quality_gates import check_stance_consistency
    result = check_stance_consistency(BEARISH_BODY, "bullish")
    assert result["pass"] is False
    assert "tone bearish" in result["reason"]


def test_stance_bearish_brief_bullish_body_rejects():
    from lib.quality_gates import check_stance_consistency
    result = check_stance_consistency(BULLISH_BODY, "bearish")
    assert result["pass"] is False


def test_stance_divergent_balanced_passes():
    from lib.quality_gates import check_stance_consistency
    assert check_stance_consistency(MIXED_BODY, "divergent")["pass"] is True


def test_stance_no_keywords_rejects():
    from lib.quality_gates import check_stance_consistency
    body = "VCB là ngân hàng. Q1 ra báo cáo."  # No stance words
    result = check_stance_consistency(body, "bullish")
    assert result["pass"] is False
    assert "lifeless" in result["reason"].lower()


# === V5.0 Phase 1.5 — sentence_density gate ===

DENSE_BODY = (
    "VCB Q1/2026 LNTT đạt 11.218 tỷ — chỉ tăng 1,3% so cùng kỳ. "
    "Chi phí dự phòng tăng 38% do tích lũy buffer. "
    "Tăng trưởng tín dụng VCB 1,8% YTD thấp hơn CTG. "
    "Đây là chiến lược phòng thủ cho 2027. "
    "NĐT giữ VCB 12 tháng nhờ ổn định."
)

FLUFF_BODY = (
    "Đây là điều cần lưu ý. "
    "Cần theo dõi sát sao xu hướng này. "
    "Tình hình có nhiều biến động trong thời gian tới. "
    "Diễn biến đang theo chiều hướng tích cực. "
    "Điều này rất quan trọng với nhà đầu tư."
)


def test_sentence_density_dense_body_passes():
    from lib.quality_gates import check_sentence_density
    assert check_sentence_density(DENSE_BODY)["pass"] is True


def test_sentence_density_fluff_body_rejects():
    from lib.quality_gates import check_sentence_density
    result = check_sentence_density(FLUFF_BODY)
    assert result["pass"] is False
    assert "density" in result["reason"].lower()


def test_sentence_density_mixed_at_threshold():
    """80% threshold: 4/5 sentences dense → pass."""
    from lib.quality_gates import check_sentence_density
    body = (
        "VCB Q1 LNTT 11.218 tỷ. "
        "Chi phí dự phòng tăng 38% YoY. "
        "CTG tăng 11,4% so cùng kỳ. "
        "Tín dụng 1,8% YTD. "
        "Điều này cần lưu ý."  # only fluff (1 of 5)
    )
    assert check_sentence_density(body)["pass"] is True


def test_sentence_density_bullet_labels_excluded():
    """Bullet labels like '**X:**' not counted as sentences."""
    from lib.quality_gates import check_sentence_density
    body = (
        "VCB tăng 11,4% so cùng kỳ Q1/2026. "
        "**Chi phí dự phòng tăng 38%:** buffer tích lũy do rủi ro BĐS."
    )
    assert check_sentence_density(body)["pass"] is True


# === V5.1.2 PATCH — em_dash_density gate (max 1 per 100 words) ===

def test_em_dash_density_clean_body_passes():
    from lib.quality_gates import check_em_dash_density
    body = "VCB tăng 1,3% Q1. " * 30  # 120 words, 0 em dash
    assert check_em_dash_density(body)["pass"] is True


def test_em_dash_density_one_per_hundred_passes():
    from lib.quality_gates import check_em_dash_density
    # 100 words, 1 em dash → ratio 1.0% = exactly at threshold (pass)
    body = "VCB tăng — đáng chú ý. " + ("Q1 manh. " * 95)  # ~100 words, 1 em dash
    assert check_em_dash_density(body)["pass"] is True


def test_em_dash_density_too_many_rejects():
    from lib.quality_gates import check_em_dash_density
    # 50 words, 3 em dashes → ratio 6%, fails
    body = "VCB — đáng — chú — ý. Q1 manh. " * 5
    result = check_em_dash_density(body)
    assert result["pass"] is False
    assert "em dash" in result["reason"].lower()


def test_em_dash_density_no_em_dash_in_empty_body():
    from lib.quality_gates import check_em_dash_density
    assert check_em_dash_density("")["pass"] is True


# === V5.0 Phase 1.6 — per-format gates + dispatch (V5.1 PATCH: title gates removed) ===

def test_per_format_flash_qa_word_count():
    from lib.quality_gates import check_word_count_per_format
    body_100w = " ".join(["word"] * 100)
    assert check_word_count_per_format(body_100w, "flash_qa")["pass"] is True
    body_200w = " ".join(["word"] * 200)
    assert check_word_count_per_format(body_200w, "flash_qa")["pass"] is False


def test_per_format_standard_qa_word_count_unchanged():
    from lib.quality_gates import check_word_count_per_format
    body_250w = " ".join(["word"] * 250)
    assert check_word_count_per_format(body_250w, "standard_qa")["pass"] is True
    body_100w = " ".join(["word"] * 100)
    assert check_word_count_per_format(body_100w, "standard_qa")["pass"] is False


def test_per_format_flash_qa_body_pattern_no_bullets():
    from lib.quality_gates import check_body_pattern_per_format
    body_with_bullet = (
        "Opening paragraph of about thirty words flash qa minimum length minimum "
        "test test test test test test test test test.\n\n- bullet violation here\n\nClosing."
    )
    result = check_body_pattern_per_format(body_with_bullet, "flash_qa")
    assert result["pass"] is False
    assert "bullet" in result["reason"].lower()


def test_per_format_flash_qa_body_paragraph_only_passes():
    from lib.quality_gates import check_body_pattern_per_format
    body = (
        "VCB chia cổ tức 21% bằng cổ phiếu chốt phương án phát hành 21:1 vốn điều "
        "lệ tăng từ 83.557 lên 101.124 tỷ pha loãng EPS giấy tờ khoảng 17% nhưng "
        "P/E forward thực tế không đổi vì cổ tức cổ phiếu chuyển hạch toán LNCPS "
        "vốn cổ phần không đổi giá trị doanh nghiệp NĐT giữ dài hạn theo cốt lõi."
    )
    assert check_body_pattern_per_format(body, "flash_qa")["pass"] is True


def test_per_format_standard_listicle_min_4_bullets():
    """Listicle requires 4-7 bullets, each ≥25 words."""
    from lib.quality_gates import check_body_pattern_per_format
    body_3bullets = (
        "Opening ngắn 20 từ test test test test test test test test test test test "
        "test test test test test test test.\n\n"
        "- **Bullet 1**: " + " ".join(["word"] * 25) + "\n"
        "- **Bullet 2**: " + " ".join(["word"] * 25) + "\n"
        "- **Bullet 3**: " + " ".join(["word"] * 25) + "\n\n"
        "Closing."
    )
    result = check_body_pattern_per_format(body_3bullets, "standard_listicle")
    assert result["pass"] is False
    assert "4" in result["reason"] or "bullet" in result["reason"].lower()


def test_check_all_v5_dispatches_per_format(monkeypatch):
    """check_all_v5 runs universal + per-format. 9 keys (B-30 wires em_dash_density).

    Forces the no_hedging keyword fallback path via monkeypatch.delenv so the
    test stays deterministic + free regardless of ANTHROPIC_API_KEY presence.
    """
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from lib.quality_gates import check_all_v5
    body = (
        "VCB Q1/2026 LNTT đạt 11.218 tỷ đồng chỉ tăng 1,3% so cùng kỳ "
        "trong khi CTG tăng 11,4% và BID 8,2% nhờ tăng tín dụng nhanh hơn — "
        "VCB to nhất sàn lại đi chậm nhất Q1/2026 do chiến lược ngược chiều thị trường.\n\n"
        "- **Chi phí dự phòng VCB tăng 38% so cùng kỳ**: ngân hàng tích lũy vùng đệm trước rủi ro nợ xấu nhóm BĐS lấn từ 0,82% lên 1,03% nhờ tiếp tục đặt cược dài hạn vào tăng trưởng ổn định.\n"
        "- **Biên lãi vay VCB co từ 3,06% xuống 2,71%**: nhờ ưu tiên giữ khách hàng tốt thay vì đẩy lãi suất cho vay lên cao, chiến lược phòng thủ dài hạn đáng chú ý cho tăng trưởng ổn định.\n"
        "- **Tăng trưởng tín dụng VCB chỉ 1,8% lũy kế từ đầu năm**: trong khi CTG đạt 4,3% và BID 3,8% so cùng kỳ, VCB tự chậm có chủ đích nhờ ưu tiên chất lượng tài sản tích lũy lợi thế dài hạn.\n\n"
        "Tích cực dài hạn cho VCB nhờ chiến lược ổn định nhờ kỷ luật rủi ro. NĐT đang cầm nên giữ 12 tháng vì chiến lược phòng thủ Q1 sẽ thành lợi thế tăng trưởng."
    )
    results = check_all_v5(body, format_id="standard_qa", stance="bullish")
    # 9 keys expected (B-30 added em_dash_density)
    assert set(results.keys()) == {
        "no_english_jargon", "no_metadata_leak", "no_hedging",
        "verdict_line", "stance_consistency", "sentence_density",
        "em_dash_density",
        "word_count", "body_pattern",
    }
    # title_pattern NOT in results
    assert "title_pattern" not in results
    failed = [(k, v) for k, v in results.items() if not v["pass"]]
    assert not failed, f"Unexpected failures: {failed}"


# === B-30 (V5.1.2 PATCH) — LLM-as-judge no-hedging + em_dash wiring ===

def test_no_hedging_falls_back_when_no_api_key(monkeypatch):
    """No ANTHROPIC_API_KEY → keyword fallback path catches hedging keyword."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from lib.quality_gates import check_no_hedging
    body = "Cổ phiếu có thể tăng tùy thuộc thị trường."
    result = check_no_hedging(body)
    assert result["pass"] is False
    # Fallback emits the explicit "keyword fallback" marker.
    assert "keyword fallback" in result["reason"]
    assert "có thể" in result["reason"]


def test_no_hedging_falls_back_to_keyword_when_sdk_missing(monkeypatch):
    """API key set but anthropic SDK unimportable → fallback path used.

    Simulates SDK-missing by stubbing `__import__("anthropic")` to raise
    ImportError. Verifies the LLM branch swallows ImportError and degrades
    to keyword check (clean body passes).
    """
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-fake-key")
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "anthropic":
            raise ImportError("anthropic not installed (test)")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    from lib.quality_gates import check_no_hedging
    # Clean body — keyword fallback should pass it.
    body = "VCB sẽ tăng. NĐT nên giữ. Q1 đang mạnh."
    result = check_no_hedging(body)
    assert result["pass"] is True


def test_check_all_v5_includes_em_dash_density(monkeypatch):
    """check_all_v5 now returns 9 keys including em_dash_density (B-30 wiring)."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from lib.quality_gates import check_all_v5
    body = (
        "VCB Q1/2026 LNTT đạt 11.218 tỷ đồng chỉ tăng 1,3% so cùng kỳ "
        "trong khi CTG tăng 11,4% và BID 8,2% nhờ tăng tín dụng nhanh hơn — "
        "VCB to nhất sàn lại đi chậm nhất Q1/2026 do chiến lược ngược chiều thị trường.\n\n"
        "- **Chi phí dự phòng VCB tăng 38% so cùng kỳ**: ngân hàng tích lũy vùng đệm trước rủi ro nợ xấu nhóm BĐS lấn từ 0,82% lên 1,03% nhờ tiếp tục đặt cược dài hạn vào tăng trưởng ổn định.\n"
        "- **Biên lãi vay VCB co từ 3,06% xuống 2,71%**: nhờ ưu tiên giữ khách hàng tốt thay vì đẩy lãi suất cho vay lên cao, chiến lược phòng thủ dài hạn đáng chú ý cho tăng trưởng ổn định.\n"
        "- **Tăng trưởng tín dụng VCB chỉ 1,8% lũy kế từ đầu năm**: trong khi CTG đạt 4,3% và BID 3,8% so cùng kỳ, VCB tự chậm có chủ đích nhờ ưu tiên chất lượng tài sản tích lũy lợi thế dài hạn.\n\n"
        "Tích cực dài hạn cho VCB nhờ chiến lược ổn định nhờ kỷ luật rủi ro. NĐT đang cầm nên giữ 12 tháng vì chiến lược phòng thủ Q1 sẽ thành lợi thế tăng trưởng."
    )
    results = check_all_v5(body, format_id="standard_qa", stance="bullish")
    assert "em_dash_density" in results
    assert len(results) == 9  # 7 universal + 2 per-format
    # All gates should pass for a clean body.
    failed = [(k, v) for k, v in results.items() if not v["pass"]]
    assert not failed, f"Unexpected failures: {failed}"
