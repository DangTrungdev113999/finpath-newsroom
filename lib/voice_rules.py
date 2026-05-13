"""Shared voice rules V1.3 — single source of truth for title + body.

V1.2 (2026-05-12 PM): constants lived in headline_scorer.py — title-only.
V1.3 (2026-05-13): extracted here to enable parallel body voice check
("bình dân xuồng xã nguy hiểm"). Title rules stay verbatim; body adds:
- BAO_CHI_BODY_VERBS — ban formal verbs (bàn giao/ghi nhận/công bố)
- PREFERRED_BODY_VERBS — encourage concrete verbs in body
- METAPHOR_MARKERS — boost sentence_density when present
- CLOSING_VAGUE_BAN — closing reject (cần theo dõi/làm chỉ báo)
- STANCE_VERBS — closing actionable Layer 1
"""
from __future__ import annotations
import re

# ============================================================
# V1.2 TITLE CONSTANTS (extracted from headline_scorer.py)
# Title-only usage — DO NOT apply to body without explicit mapping.
# ============================================================

TITLE_TENSION_WORDS = [
    "hy sinh", "đánh đổi", "nghịch lý", "vì sao", "đổi lấy",
    "không phải", "bù lại", "thay vì", "chấp nhận",
]

DRAMATIC_VERBS = [
    # V1.1 formal/dramatic
    "hy sinh", "đánh đổi", "đặt cược", "lội ngược",
    "rút khỏi", "vượt mặt", "tung đòn", "đặt cọc",
    "chấp nhận thua", "tự chậm lại", "đập cửa", "thoát hiểm",
    "chấp nhận hi sinh", "đánh cược", "đổ vỡ", "vực dậy",
    "tiếp đà", "phá kỷ lục", "soán ngôi", "lấn sang", "rơi vào",
    # V1.2 bình dân additions (concrete, everyday VN)
    "ăn lãi", "ăn ưu đãi", "ăn lời", "ăn được", "ăn ", "ăn,",
    "khoe lãi", "khoe ",
    "dồn tiền", "dồn ", "xén cổ tức", "xén ",
    "gom hàng", "gom ", "bơm vốn", "bơm ",
    "đẻ ra", "ngồi trên tiền", "ngồi trên",
    "chạy đâu", "đi vay", "đi đâu",
    "đổi tên", "đổi hướng", "đổi mô hình",
    "gọi vốn", "gọi tiền",
    "chia cổ tức", "chia kỷ lục",
    "vọt", "tụt", "rớt", "nhảy",
    "bán hàng", "bán ESOP", "bán nội bộ",
    "thật ra", "thực ra", "thật chỉ",
    # V1.3 additions — headcount / restructuring verbs (STB layoff cluster)
    "tống ", "nhồi ", "nhồi thêm",
    "sa thải", "lùa ", "rước ",
    "phân hóa", "ngược chiều",
    "cắt sâu", "cắt mạnh",
]

PR_CLICKBAIT_WORDS = [
    "cú nổ", "bí mật", "sốc", "hot", "thông tin nóng",
    "không thể tin nổi", "cú twist", "kỳ tích", "hé lộ",
    "kỳ tích", "kỷ tích",
]

# V1.2 ban lists — formula/cliché autodetect for title
BAO_CHI_FORMULAIC_PHRASES = [
    # Formula clichés V1.1 over-produced
    "đánh đổi gì", "đánh đổi để", "đánh đổi nào", "đánh đổi để lấy",
    "hy sinh để", "hy sinh nhằm", "hy sinh lợi nhuận",
    "để đổi lấy", "để lấy gì", "đổi lấy gì", "đổi lấy điều gì",
    "đặt cược vào", "đặt cược để",
    # Báo chí formal verbs (thông cáo style)
    "đặt mục tiêu", "đặt kế hoạch", "công bố kế hoạch",
    "đã công bố", "ghi nhận", "thông qua nghị quyết",
    "phấn đấu", "dự kiến đạt",
    # Báo chí buzzwords
    "lao dốc", "bứt phá", "lập kỷ lục",
]

# V1.2 — VN finance terms naturalized (NOT English jargon)
NATURALIZED_FINANCE_TERMS = {
    "esop", "eps", "roe", "roa", "nim", "casa", "npl", "lntt", "lnst",
    "cof", "ldr", "car", "esg", "ipo", "spo", "etf",
    "vix", "ssi", "vnindex", "vn-index", "hose", "hnx", "upcom",
}

# Format pattern "Q1/2026 X lãi Y" — báo chí summary lead style
BAO_CHI_QUARTER_PATTERN = re.compile(
    r"^(Q[1-4]/?\d{0,4}|năm \d{4})\s+\w+\s+(lãi|lợi nhuận|doanh thu|công bố|ghi nhận)",
    re.IGNORECASE,
)

# Rubric labels accidentally written to title field
RUBRIC_LABEL_LEAK = {
    "question", "declarative tension", "quote", "contrast verb",
    "lối question", "lối declarative", "lối quote", "lối contrast",
}

# Concrete question subjects (V1.2 rubric bonus + V1.3 additions)
CONCRETE_QUESTION_SUBJECTS = [
    "ai gom", "ai trả", "ai bán", "ai đẩy", "ai chạy", "ai đang",
    "ai vừa", "ai mua", "ai thoát",
    "đi đâu", "chạy đâu", "tiền đâu", "tiền chạy",
    "sợ gì", "đáng sợ", "lo gì", "ngại gì",
    "khôn hay liều", "khôn hay dại", "đúng hay sai",
    "bao giờ", "khi nào", "đến bao giờ",
    "trước ngày", "trước kỳ", "sau tháng",
    " lạ?", " thật?", " thật vậy?",
    # V1.3 — comparison verdict (bank nào sai/đúng, ai thắng, etc)
    "nào sai", "nào đúng", "ai thắng", "ai thua", "bên nào",
    "kẻ nào", "phe nào", "nhóm nào",
]

# ============================================================
# V1.3 BODY CONSTANTS (NEW — for quality_gates body checks)
# ============================================================

# Body-specific báo chí verbs (top 3 from 2026-05-13 body audit:
# bàn giao/ghi nhận 6x · phát hành 5x · công bố/dự kiến 4x).
# These signal báo chí thông cáo style — kill stance + actionability.
BAO_CHI_BODY_VERBS = [
    "bàn giao", "ghi nhận", "công bố", "dự kiến đạt", "dự kiến đạt được",
    "phát hành thành công", "đang tiến hành", "tiếp tục triển khai",
    "đặt mục tiêu", "hoàn thành kế hoạch", "phấn đấu", "phấn đấu đạt",
    "thông qua nghị quyết", "đã được phê duyệt", "đã được thông qua",
    "ban hành", "triển khai đồng bộ", "tích cực triển khai",
]

# Bình dân body verbs preferred — concrete, everyday VN (parallel V1.2 title).
# Master agent should reach for these instead of BAO_CHI_BODY_VERBS.
PREFERRED_BODY_VERBS = [
    "ăn", "khoe", "dồn", "xén", "gom", "bơm", "đẻ", "vọt", "tụt", "rớt",
    "ngồi trên", "lấy", "đốt", "đẩy", "kéo", "ép", "nhồi", "vắt",
    "lùa", "kéo", "đào", "ngấm",
]

# Metaphor/analogy markers — boost sentence_density score (V1.3).
# Encourages Master to ví von thay vì dồn số khô khan.
METAPHOR_MARKERS = [
    "như", "kiểu", "giống", "tựa", "ví như", "nói nôm na",
    "nói cách khác", "thật ra", "thực ra", "kỳ thực",
    "gấp", "bằng", "tương đương", "ngang ngửa", "ngang với",
    "tựa hồ", "chẳng khác", "khác nào",
]

# Closing weak phrases (auto-reject in check_actionable_closing).
# Pattern from audit: VHM-cổ tức closing "theo dõi hấp thụ làm chỉ báo".
CLOSING_VAGUE_BAN = [
    "cần theo dõi", "cần để ý", "đáng theo dõi", "cần thận trọng",
    "tham khảo trước khi", "cân nhắc kỹ", "thận trọng quan sát",
    "làm chỉ báo", "là chỉ báo sớm", "đánh giá thêm",
    "chờ thêm dữ liệu", "chưa rõ", "cần thời gian",
]

# Actionable stance verbs (Layer 1 of check_actionable_closing).
# Closing MUST contain ≥1 of these for direction signal.
STANCE_VERBS = [
    "nên cầm", "nên giữ", "nên giảm", "nên bán", "nên thoát",
    "nên tích lũy", "nên mua thêm", "nên chốt", "nên đợi",
    "giữ", "cắt", "bán", "tích lũy", "thoát",
    "phù hợp NĐT", "không phù hợp NĐT", "phòng thủ",
    "chấp nhận", "ưu tiên", "tránh",
]
