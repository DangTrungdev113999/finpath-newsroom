"""Tests for lib.quality_gates V4.0 — 5 gates."""
import pytest
from lib.quality_gates import (
    check_no_english_jargon,
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
