"""Shared voice rules V1.5-lite — mechanical bans only, no prefer lists.

V1.4 (2026-05-13): DRAMATIC_VERBS / PREFERRED_BODY_VERBS / METAPHOR_MARKERS
caused Pattern A pile-on — AI generalized STYLE từ list → invented
"chấm đích / vọt lãi / xén lợi". V1.5-lite drops these.

V1.5-lite (2026-05-13 PM):
- DROP: DRAMATIC_VERBS, PREFERRED_BODY_VERBS, METAPHOR_MARKERS,
  BAO_CHI_FORMULAIC_PHRASES, BAO_CHI_BODY_VERBS, CONCRETE_QUESTION_SUBJECTS,
  RUBRIC_LABEL_LEAK, BAO_CHI_QUARTER_PATTERN
- KEEP: NATURALIZED_FINANCE_TERMS, CLOSING_VAGUE_BAN, STANCE_VERBS
- ADD: HAN_VIET_FORMAL_BAN (dict term → bình dân replacement)
"""
from __future__ import annotations


# Naturalized finance terms — không count as English jargon trong title/body
NATURALIZED_FINANCE_TERMS = {
    "esop", "eps", "roe", "roa", "nim", "casa", "npl", "lntt", "lnst",
    "cof", "ldr", "car", "esg", "ipo", "spo", "etf",
    "vix", "ssi", "vnindex", "vn-index", "hose", "hnx", "upcom",
}

# Closing weak phrases — reject in check_actionable_closing Layer 3
CLOSING_VAGUE_BAN = [
    "cần theo dõi", "cần để ý", "đáng theo dõi", "cần thận trọng",
    "tham khảo trước khi", "cân nhắc kỹ", "thận trọng quan sát",
    "làm chỉ báo", "là chỉ báo sớm", "đánh giá thêm",
    "chờ thêm dữ liệu", "chưa rõ", "cần thời gian",
]

# Actionable stance verbs — Layer 1 of check_actionable_closing
STANCE_VERBS = [
    "nên cầm", "nên giữ", "nên giảm", "nên bán", "nên thoát",
    "nên tích lũy", "nên mua thêm", "nên chốt", "nên đợi",
    "giữ", "cắt", "bán", "tích lũy", "thoát",
    "phù hợp NĐT", "không phù hợp NĐT", "phòng thủ",
    "chấp nhận", "ưu tiên", "tránh",
]

# V1.5-lite — Hán-Việt formal vocabulary ban (term → bình dân replacement).
# Reader bình dân không hiểu / cảm thấy formal. Master phải dùng bình dân
# equivalent. Mechanical gate check_han_viet_formal rejects body chứa ≥2 terms.
# Consumer: lib.quality_gates.check_han_viet_formal (V1.5-lite Task 2).
HAN_VIET_FORMAL_BAN = {
    "độc bản": "duy nhất",
    "hội đủ": "đủ",
    "chưa hội đủ": "chưa đủ",
    "tái định giá": "định giá lại",
    "cấu trúc vốn": "cơ cấu vốn",
    "cấu trúc sở hữu": "cơ cấu sở hữu",
    "phương án xử lý": "cách xử lý",
    "triển khai đồng bộ": "làm đồng bộ",
    "tích cực triển khai": "đang đẩy",
    "ban hành nghị quyết": "ra nghị quyết",
    "thông qua nghị quyết": "chốt nghị quyết",
    "đã được phê duyệt": "đã duyệt",
    "đã được thông qua": "đã chốt",
    "dự kiến đạt": "nhắm tới",
    "hoàn thành kế hoạch": "đạt kế hoạch",
    "phấn đấu đạt": "cố đạt",
    "thực hiện chiến lược": "làm chiến lược",
    "chế tài xử lý": "chế độ phạt",
    "khả năng huy động": "khả năng gọi vốn",
    "tiến hành triển khai": "đang làm",
}


# V1.6 — Vague action verbs flagged in titles (soft hint, not hard reject).
# Consumer (V5.1.8): 10 master sector prompt Title craft block — agent self-check during title craft.
# self-check during candidate generation. User feedback:
# "FPT mẹ nguy 2.330 tỷ" / "khoản 282 tỷ che gì" / "PVS ăn 44%"
# Reader can't tell WHAT happened — verb mơ hồ. Resolve by following with
# CONCRETE_OBJECT_HINTS within 4 tokens (lãi/doanh thu/kế hoạch/etc).
VAGUE_ACTION_VERBS = {
    "ăn": "verb mơ hồ — chỉ rõ ăn lãi/doanh thu/kế hoạch (vd: 'ăn 1.974 tỷ lãi')",
    "che": "verb mơ hồ — chỉ rõ che cái gì (vd: 'che 282 tỷ trích lập')",
    "nguy": "không phải verb đơn — dùng 'có thể mất X' / 'rủi ro mất X'",
    "mắc": "verb mơ hồ — chỉ rõ mắc kẹt/mắc nợ + nguyên nhân (vd: 'mắc kẹt 14.000 tỷ Lô B')",
    "đẻ": "verb colloquial — dùng 'tạo' / 'phát sinh' + bổ ngữ rõ",
    "đốt": "verb colloquial — dùng 'tiêu' / 'chi' / 'lỗ' + bổ ngữ",
}

# Concrete objects that "rescue" vague verbs — if verb followed by these within
# 4 tokens, treat as concrete enough. Lowercase only (case-insensitive check).
CONCRETE_OBJECT_HINTS = {
    "lãi", "lợi nhuận", "doanh thu", "lỗ", "chi phí", "vốn",
    "cổ tức", "trái phiếu", "tài sản", "nợ",
    "kế hoạch", "trích lập", "dự phòng",
    "nhân viên", "nhân sự",
    "vị thế", "thị phần", "cổ phần",
}
