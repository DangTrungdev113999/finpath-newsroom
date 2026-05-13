"""Headline scoring module V1.2 — 7 hard criteria + 8-point rubric.

V1.1 (2026-05-12 AM): em dash '—' BANNED in title (AI-tell signal).
V1.2 (2026-05-12 PM): added bao_chi reject + label_leak reject + concrete_question
bonus. Reason — V1.1 generated 7/10 titles using formula 'X đánh đổi/hy sinh Y
để Z?'. User feedback: pattern formulaic, không 'bình dân nguy hiểm'.

V1.2 bans (hard criteria additions):
- BAO_CHI_FORMULAIC_PHRASES: 'đánh đổi gì', 'để đổi lấy', 'hy sinh để',
  'đặt cược vào', 'đặt mục tiêu', 'lao dốc', 'bứt phá', 'Q1/2026 X lãi Y'
- RUBRIC_LABEL_LEAK: title field = bare 'Question'/'Declarative tension'

V1.2 bonuses (rubric):
- concrete_question_subject: 'ai gom?', 'đi đâu?', 'sợ gì?', 'khôn hay liều?'

Benchmark V1.2: 'Q1 BSR ăn 8.265 tỷ, sếp chỉ hứa 2.162 tỷ cả năm?' score ≥6/8.
"""
from __future__ import annotations
import re
from typing import Any

# V1.5-lite: dropped V1.2 word lists. Keep only naturalized terms allowlist
# (used by has_english for jargon check exception).
from lib.voice_rules import NATURALIZED_FINANCE_TERMS

# V1.5-lite local copies — these were removed from voice_rules because they
# caused Pattern A pile-on in Master body. Kept here ONLY for headline scoring
# functions until Task 3 refactors headline_scorer fully.
# TODO Task 3: replace/remove these local copies.
TITLE_TENSION_WORDS = [
    "hy sinh", "đánh đổi", "nghịch lý", "vì sao", "đổi lấy",
    "không phải", "bù lại", "thay vì", "chấp nhận",
]

DRAMATIC_VERBS = [
    "hy sinh", "đánh đổi", "đặt cược", "lội ngược",
    "rút khỏi", "vượt mặt", "tung đòn", "đặt cọc",
    "chấp nhận thua", "tự chậm lại", "đập cửa", "thoát hiểm",
    "chấp nhận hi sinh", "đánh cược", "đổ vỡ", "vực dậy",
    "tiếp đà", "phá kỷ lục", "soán ngôi", "lấn sang", "rơi vào",
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

BAO_CHI_FORMULAIC_PHRASES = [
    "đánh đổi gì", "đánh đổi để", "đánh đổi nào", "đánh đổi để lấy",
    "hy sinh để", "hy sinh nhằm", "hy sinh lợi nhuận",
    "để đổi lấy", "để lấy gì", "đổi lấy gì", "đổi lấy điều gì",
    "đặt cược vào", "đặt cược để",
    "đặt mục tiêu", "đặt kế hoạch", "công bố kế hoạch",
    "đã công bố", "ghi nhận", "thông qua nghị quyết",
    "phấn đấu", "dự kiến đạt",
    "lao dốc", "bứt phá", "lập kỷ lục",
]

BAO_CHI_QUARTER_PATTERN = re.compile(
    r"^(Q[1-4]/?\d{0,4}|năm \d{4})\s+\w+\s+(lãi|lợi nhuận|doanh thu|công bố|ghi nhận)",
    re.IGNORECASE,
)

RUBRIC_LABEL_LEAK = {
    "question", "declarative tension", "quote", "contrast verb",
    "lối question", "lối declarative", "lối quote", "lối contrast",
}

CONCRETE_QUESTION_SUBJECTS = [
    "ai gom", "ai trả", "ai bán", "ai đẩy", "ai chạy", "ai đang",
    "ai vừa", "ai mua", "ai thoát",
    "đi đâu", "chạy đâu", "tiền đâu", "tiền chạy",
    "sợ gì", "đáng sợ", "lo gì", "ngại gì",
    "khôn hay liều", "khôn hay dại", "đúng hay sai",
    "bao giờ", "khi nào", "đến bao giờ",
    "trước ngày", "trước kỳ", "sau tháng",
    " lạ?", " thật?", " thật vậy?",
    "nào sai", "nào đúng", "ai thắng", "ai thua", "bên nào",
    "kẻ nào", "phe nào", "nhóm nào",
]

# Universe — synced with lib/finpath_sectors (139 tickers V5.1.3 cached).
# Hardcoded subset for hot-path Headline detection (fallback if cache miss).
ALL_TICKERS = [
    # Bank 27
    "VCB", "CTG", "BID", "TCB", "MBB", "ACB", "VPB", "HDB",
    "STB", "SHB", "EIB", "TPB", "MSB", "LPB", "OCB", "VIB",
    "NAB", "BAB", "NVB", "SGB",
    "VAB", "BVB", "ABB", "KLB", "VBB", "PGB", "HDF",
    # CK 30
    "SSI", "VND", "HCM", "VCI", "VIX",
    "SHS", "MBS", "BVS", "BSI", "AGR", "CTS", "APG", "EVS",
    "IVS", "PSI", "TVS", "WSS", "ORS", "VFS", "TCI",
    "DSC", "FTS", "CSI", "SBS", "PHS", "ART", "APS", "BMS", "AAS", "VTS",
    # BĐS 4
    "VHM", "NVL", "KDH", "DXG",
    # V5.1.3 expansion — 7 new sectors
    "BSR", "PVS", "GAS", "POW", "PLX", "OIL", "PVD", "PVT",  # oilgas
    "GMD", "HAH", "VOS", "VSC", "PHP", "CDN", "HAX",  # logistics
    "VNM", "MSN", "SAB", "BHN", "KDC", "MCM", "QNS",  # fb
    "TCM", "MSH", "TNG",  # apparel
    "MWG", "FRT", "DGW", "PNJ", "AST",  # retail
    "VHC", "ANV", "MPC", "FMC", "IDI", "CMX",  # seafood
    "FPT", "REE", "PC1", "GEX", "ITD", "TRA", "DBD", "IMP", "ELC",  # defensive
    # materialContractor + bds expanded (V5.1.3 — HPG cluster)
    "HPG", "HSG", "NKG", "HBC", "CTD", "VCG", "HT1", "BCC", "BCM", "BMP",
    "CII", "DIG", "DPG", "GEG", "HQC", "HPX", "HUT", "IDC", "IJC", "ITA",
    "KBC", "KBS", "KHG", "KSB", "L14", "LCG", "LDG", "NLG", "NTC", "NTL",
    "PDR", "PTB", "SCR", "SIP", "SZC", "SZK", "TCH", "VGC", "VIC", "VIP", "VPI", "VRE",
    # other sectors missing
    "BWE", "CEO", "DBC", "DXS", "GVR", "HDC", "HDG", "HVN", "NCB", "NGK",
    "NT2", "PAN", "PET", "PGS", "PHR", "PPC", "PVC", "QTP", "SBT", "SCS",
    "SKG", "SMC", "SSB", "TDM", "VCS", "VGT", "VJC", "VTP",
]

GROUP_REFS = ["Big4", "Big 4", "tư nhân top", "tư nhân", "Big5", "Big3"]


def has_ticker(title: str) -> bool:
    """Check title contains at least 1 ticker OR group reference."""
    for t in ALL_TICKERS:
        if re.search(rf"\b{t}\b", title):
            return True
    for g in GROUP_REFS:
        if g in title:
            return True
    return False


def has_specific_number(title: str) -> bool:
    """Number with financial unit OR headcount unit OR bare ≥4-digit number.

    V1.3 PATCH (2026-05-13): also accept "X người / X nhân viên / X nhân sự"
    and bare numbers ≥1.000 (e.g. "2.700, VPB+TCB+LPB nhồi 700"). Headlines
    về layoff / corp action have bare counts without financial unit.
    """
    # Financial unit (original V1.1)
    if re.search(
        r"\d+([.,]\d+)?\s*(tỷ|triệu|nghìn|%|đ|/năm|/tháng|/quý|đ/tháng|bps|điểm)",
        title, re.IGNORECASE,
    ):
        return True
    # V1.3 — headcount unit
    if re.search(
        r"\d+([.,]\d+)?\s*(người|nhân viên|nhân sự|lao động|cổ phiếu|cp)",
        title, re.IGNORECASE,
    ):
        return True
    # V1.3 — bare ≥4-digit number (vd "2.700" / "11.026" — concrete count without unit)
    if re.search(r"\b\d{1,3}[.,]\d{3,}\b", title):
        return True
    return False


def has_dramatic_verb(title: str) -> bool:
    tlc = title.lower()
    return any(v in tlc for v in DRAMATIC_VERBS)


def has_tension_word(title: str) -> bool:
    tlc = title.lower()
    return any(w in tlc for w in TITLE_TENSION_WORDS)


def has_paradox_pattern(title: str) -> bool:
    return bool(re.search(
        r"\bmà\b|\bnhưng\b|\bthật ra\b|\bthực ra\b|\bkỳ thực\b",
        title.lower()
    ))


def has_open_question(title: str) -> bool:
    return title.rstrip().endswith("?")


def has_pr_clickbait(title: str) -> bool:
    tlc = title.lower()
    return any(w in tlc for w in PR_CLICKBAIT_WORDS)


def has_english(title: str) -> bool:
    """Reuse quality_gates English jargon check on title.

    V1.2: NATURALIZED_FINANCE_TERMS (ESOP / EPS / ROE / NIM / etc.) are
    accepted as Vietnamese usage — universal in VN finance media + retail
    investor talk. Banning forces verbose VN equivalents nobody says.
    """
    try:
        from lib.quality_gates import ENGLISH_JARGON
        tlc = title.lower()
        # Filter out naturalized terms before check
        filtered_jargon = [j for j in ENGLISH_JARGON if j.lower() not in NATURALIZED_FINANCE_TERMS]
        return any(re.search(rf"\b{re.escape(j.lower())}\b", tlc) for j in filtered_jargon)
    except ImportError:
        return False


def has_em_dash(title: str) -> bool:
    """V1.1 PATCH: em dash '—' (U+2014) BANNED in title.
    Hyphen '-' (U+002D) + en dash '–' (U+2013) acceptable.
    """
    return "—" in title


def is_bao_chi(title: str) -> bool:
    """V1.2 — detect báo chí formula/cliché. Reject hard criteria.

    Catches:
    - Formula 'X đánh đổi/hy sinh Y để Z' (V1.1 over-generated)
    - Báo chí formal verbs (đặt mục tiêu / ghi nhận / công bố)
    - Buzzwords (lao dốc / bứt phá / lập kỷ lục)
    - Format 'Q1/2026 X lãi Y' summary lead
    """
    tlc = title.lower()
    if any(phrase in tlc for phrase in BAO_CHI_FORMULAIC_PHRASES):
        return True
    if BAO_CHI_QUARTER_PATTERN.match(title):
        return True
    return False


def is_label_leak(title: str) -> bool:
    """V1.2 — detect rubric label accidentally written as title.

    Catches:
    - Bare 'Question' / 'Declarative tension' / 'Quote'
    - 'Question — explanation:' meta-prefix
    - 'Lối X:' prefix
    """
    tlc = title.lower().strip().rstrip("?.!")
    # Bare label or short title that IS just the label
    if len(title.split()) <= 4 and tlc in RUBRIC_LABEL_LEAK:
        return True
    # Common leak patterns observed in production V1.1
    if tlc.startswith("question") and ":" in title:
        return True
    if tlc.startswith("declarative tension"):
        return True
    if tlc.startswith("lối "):
        return True
    if tlc.startswith("contrast verb"):
        return True
    return False


def has_concrete_question_subject(title: str) -> bool:
    """V1.2 — concrete question subject ('ai gom?' / 'đi đâu?').

    Vs generic abstract ('để đổi lấy gì?'). Earns +1 rubric bonus.
    """
    if not has_open_question(title):
        return False
    tlc = title.lower()
    return any(s in tlc for s in CONCRETE_QUESTION_SUBJECTS)


# V1.3 — generic reference words that need specifier nearby ("ngành" alone fails,
# "ngành bank" passes). Used by has_orphan_number to catch vague references.
GENERIC_REFERENCES = {"ngành", "nhóm", "khu vực", "ngành nghề", "lĩnh vực", "khối"}

# V1.3 — specifiers that can resolve a generic reference (must appear within 3 words)
REFERENCE_SPECIFIERS = {
    "bank", "ngân hàng", "tư nhân", "big4", "bds", "bđs", "ck", "chứng khoán",
    "oilgas", "dầu khí", "logistics", "fb", "retail", "bán lẻ", "seafood",
    "thuỷ sản", "thủy sản", "apparel", "dệt may", "defensive", "phòng thủ",
    "tài chính", "công nghệ", "điện",
}


def has_orphan_number(title: str) -> bool:
    """V1.3 — detect orphan number/percent (no subject) or vague reference.

    Reader test 5 giây: title đứng độc lập, mọi number/percent phải có
    subject explicit (vd "85% nhân sự" OK, "85%" alone fail).

    Catches:
    - Lone percentage without noun within 4 next tokens
      ("STB xén 85% mà ngành còn lại..." → 85% no subject within "mà ngành")
    - Generic reference "ngành" / "nhóm" without specifier within 3 tokens
      ("ngành còn lại vẫn tuyển" → "ngành" without bank/CK/BĐS specifier)

    Returns True if orphan (BAD), False if all numbers/refs have subject (GOOD).
    """
    tlc = title.lower()
    tokens = re.findall(r"\S+", tlc)

    # Check 1: Lone percentage. After every "<N>%" token, scan next 4 tokens
    # for a Vietnamese noun. Accept if noun present.
    NOUN_HINTS = {
        # Headcount / personnel
        "người", "nhân", "viên", "sự", "lao", "động",
        # Money units
        "tỷ", "tỉ", "triệu", "nghìn", "đồng", "đ", "vnđ",
        # Business nouns
        "lợi", "nhuận", "doanh", "thu", "vốn", "cổ", "phiếu", "tiền",
        "tài", "sản", "nợ", "lãi", "biên", "giá", "chi", "phí", "dự",
        "phòng", "tăng", "giảm", "trưởng", "thị", "phần", "quỹ",
        "trái", "phiếu", "tín", "dụng", "huy", "động", "ký", "quỹ",
        # Time
        "năm", "tháng", "quý", "ngày", "kỳ", "q1", "q2", "q3", "q4",
        # Direction adjectives
        "cùng", "trên", "dưới", "vượt", "thấp", "cao",
    }
    for i, tok in enumerate(tokens):
        if re.search(r"\d+([.,]\d+)?%", tok):
            window = tokens[i + 1: i + 5]
            window_text = " ".join(window)
            # Skip if percent token itself contains noun (vd "85%vốn")
            if any(noun in tok for noun in NOUN_HINTS):
                continue
            # Accept if any noun hint in next 4 tokens
            if any(any(noun in w for noun in NOUN_HINTS) for w in window):
                continue
            # Orphan
            return True

    # Check 2: Generic reference without specifier nearby.
    for i, tok in enumerate(tokens):
        clean_tok = re.sub(r"[^\w]", "", tok)
        if clean_tok in GENERIC_REFERENCES:
            window = tokens[max(0, i - 2): i + 4]
            window_text = " ".join(window)
            if any(spec in window_text for spec in REFERENCE_SPECIFIERS):
                continue
            return True

    return False


def check_hard_criteria(title: str) -> dict[str, Any]:
    """V1.2 — 7 hard criteria check.

    Returns dict with 8 keys + computed 'passed' flag:
    - ticker_present: bool
    - word_count_le_16: bool (V1.3: relaxed from 12 — clarity > conciseness)
    - hook_strong: {tension_present, click_test_pass} dict
    - binh_dan_nguy_hiem: {plain_language, sharp_edge} dict
    - no_em_dash: bool
    - not_bao_chi: bool (V1.2 NEW — ban formula clichés + báo chí buzzwords)
    - not_label_leak: bool (V1.2 NEW — title KHÔNG được = rubric label)
    - not_orphan_number: bool (V1.3 NEW — số/percent phải có subject, ngành phải có specifier)
    - passed: bool (all top-level + nested True)
    """
    ticker_present = has_ticker(title)
    # V1.3 relaxed from ≤12 → ≤16 (clarity > conciseness per user feedback 2026-05-13)
    word_count_le_16 = len(title.split()) <= 16

    # Hook strong = 2 sub-tests (V1.2: also accept concrete_question_subject
    # as tension signal — 'Tiền chạy đâu?', 'Khôn hay liều?')
    tension_present = (
        has_dramatic_verb(title)
        or has_tension_word(title)
        or has_paradox_pattern(title)
        or has_concrete_question_subject(title)
    )
    # Click test heuristic (V1.2): has number/question/dramatic/concrete-Q-subject
    click_test_pass = (
        has_specific_number(title)
        or has_open_question(title)
        or has_dramatic_verb(title)
        or has_concrete_question_subject(title)
    )
    hook_strong = {
        "tension_present": tension_present,
        "click_test_pass": click_test_pass,
    }

    # Bình dân nguy hiểm = 2 sub-tests
    # plain_language: no English jargon + no PR clickbait
    plain_language = not has_english(title) and not has_pr_clickbait(title)
    # sharp_edge: has tension/dramatic/specific (i.e. not bland)
    sharp_edge = (
        has_dramatic_verb(title)
        or has_specific_number(title)
        or has_tension_word(title)
        or has_paradox_pattern(title)
    )
    binh_dan_nguy_hiem = {
        "plain_language": plain_language,
        "sharp_edge": sharp_edge,
    }

    no_em_dash = not has_em_dash(title)
    not_bao_chi = not is_bao_chi(title)
    not_label_leak = not is_label_leak(title)
    not_orphan_number = not has_orphan_number(title)

    passed = (
        ticker_present
        and word_count_le_16
        and hook_strong["tension_present"]
        and hook_strong["click_test_pass"]
        and binh_dan_nguy_hiem["plain_language"]
        and binh_dan_nguy_hiem["sharp_edge"]
        and no_em_dash
        and not_bao_chi
        and not_label_leak
        and not_orphan_number
    )

    return {
        "ticker_present": ticker_present,
        "word_count_le_16": word_count_le_16,
        "hook_strong": hook_strong,
        "binh_dan_nguy_hiem": binh_dan_nguy_hiem,
        "no_em_dash": no_em_dash,
        "not_bao_chi": not_bao_chi,
        "not_label_leak": not_label_leak,
        "not_orphan_number": not_orphan_number,
        "passed": passed,
    }


def score_title(title: str) -> dict[str, Any]:
    """V1.3 — 8-point rubric. Only call after check_hard_criteria passes.

    Returns {score: int, max: 8, elements: dict}.

    Scoring (max 8, weighted by impact on reader curiosity):
    - dramatic_verb: +2
    - specific_number: +2
    - concrete_question_subject (V1.2): +1 (bonus for 'ai gom?' vs 'đổi lấy gì?')
    - open_question: +1
    - tension_word: +1
    - paradox_pattern: +1
    - self_explanatory (V1.3): +1 (≤14 từ AND no orphan number — sweet spot)

    V1.3 PATCH: replaced extra_concise (≤10 từ) — pushed hook quá ngắn → mất
    subject. Now reward "≤14 từ AND không orphan number" — balance concise + clear.
    """
    elements = {
        "ticker": has_ticker(title),
        "dramatic_verb": has_dramatic_verb(title),
        "specific_number": has_specific_number(title),
        "concrete_question_subject": has_concrete_question_subject(title),
        "open_question": has_open_question(title),
        "tension_word": has_tension_word(title),
        "paradox_pattern": has_paradox_pattern(title),
        "self_explanatory": len(title.split()) <= 14 and not has_orphan_number(title),
    }
    score = 0
    if elements["dramatic_verb"]:
        score += 2
    if elements["specific_number"]:
        score += 2
    if elements["concrete_question_subject"]:
        score += 1
    if elements["open_question"]:
        score += 1
    if elements["tension_word"]:
        score += 1
    if elements["paradox_pattern"]:
        score += 1
    if elements["self_explanatory"]:
        score += 1
    # Cap at 8 (open_question + concrete_question may both fire, +1 each but
    # concrete already implies open, so cap)
    return {"score": min(score, 8), "max": 8, "elements": elements}


def pick_best_candidate(candidates: list[str]) -> dict[str, Any]:
    """Apply 5 hard criteria filter + score → return best.

    Returns: {final_title, picked_score, all_scored}
    Raises ValueError if 0 candidates pass hard criteria.
    """
    scored = []
    for c in candidates:
        hard = check_hard_criteria(c)
        entry = {
            "text": c,
            "hard_pass": hard["passed"],
            "hard_detail": hard,
        }
        if hard["passed"]:
            entry.update(score_title(c))
        scored.append(entry)

    passing = [s for s in scored if s["hard_pass"]]
    if not passing:
        raise ValueError(
            f"All {len(candidates)} candidates failed hard criteria. "
            f"Headline agent must regenerate."
        )
    # Sort by score DESC, tie-break by length ASC
    passing.sort(key=lambda x: (-x["score"], len(x["text"])))
    best = passing[0]
    return {
        "final_title": best["text"],
        "picked_score": best["score"],
        "all_scored": scored,
    }
