"""Headline scoring module V1.5-lite — 8 hard criteria + 6-point rubric.

V1.1 (2026-05-12 AM): em dash '—' BANNED in title (AI-tell signal).
V1.2 (2026-05-12 PM): added bao_chi reject + label_leak reject + concrete_question bonus.
V1.3 (2026-05-13 AM): orphan number detector + word_count relaxed ≤12 → ≤16.
V1.5-lite (2026-05-13 PM): drop V1.2-V1.4 word bonus scorer (caused Pattern A
pile-on per audit). Add Hán-Việt + abbreviation hard criteria. Simplified rubric.

Dropped in V1.5-lite:
- is_bao_chi / BAO_CHI_FORMULAIC_PHRASES / BAO_CHI_QUARTER_PATTERN
- has_concrete_question_subject / CONCRETE_QUESTION_SUBJECTS
- has_dramatic_verb / DRAMATIC_VERBS
- has_tension_word / TITLE_TENSION_WORDS
- RUBRIC_LABEL_LEAK (replaced by inline set in is_label_leak)
- hook_strong / binh_dan_nguy_hiem nested dicts in check_hard_criteria
- 8-point rubric → 6-point rubric

Added in V1.5-lite:
- no_han_viet_formal hard criterion (via HAN_VIET_FORMAL_BAN)
- abbreviation_expanded hard criterion (via check_abbreviation_expanded)
- has_concrete_number info field
- plain_language flat key (was nested in binh_dan_nguy_hiem)
"""
from __future__ import annotations
import re
from typing import Any

# V1.5-lite: only naturalized terms needed (exception for has_english check).
from lib.voice_rules import NATURALIZED_FINANCE_TERMS

PR_CLICKBAIT_WORDS = [
    "cú nổ", "bí mật", "sốc", "hot", "thông tin nóng",
    "không thể tin nổi", "cú twist", "kỳ tích", "hé lộ",
    "kỳ tích", "kỷ tích",
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


def is_label_leak(title: str) -> bool:
    """V1.2 — detect rubric label accidentally written as title.

    Catches:
    - Bare 'Question' / 'Declarative tension' / 'Quote'
    - 'Question — explanation:' meta-prefix
    - 'Lối X:' prefix
    """
    _RUBRIC_LABEL_LEAK = {
        "question", "declarative tension", "quote", "contrast verb",
        "lối question", "lối declarative", "lối quote", "lối contrast",
    }
    tlc = title.lower().strip().rstrip("?.!")
    # Bare label or short title that IS just the label
    if len(title.split()) <= 4 and tlc in _RUBRIC_LABEL_LEAK:
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


def detect_vague_action_verb(title: str) -> list[dict[str, str]]:
    """V1.6 — soft hint detector for vague action verbs in titles.

    Reads title token-by-token. For each verb in VAGUE_ACTION_VERBS:
    - If followed within 4 tokens by any CONCRETE_OBJECT_HINTS → NOT flagged
      ("PVS ăn 1.974 tỷ lãi" → 'lãi' present → OK)
    - Otherwise → flagged with suggestion text
      ("PVS ăn 44%" → no concrete object → flagged)
      ("FPT nguy 2.330 tỷ" → 'nguy' not a verb → flagged regardless)

    'nguy' / 'mắc' are flagged ALWAYS (no valid concrete bổ ngữ in title context).
    Returns list of {verb, position, suggestion}. Empty list = no hints.
    NOT in `passed` flag — agent self-check + audit log only.
    """
    from lib.voice_rules import VAGUE_ACTION_VERBS, CONCRETE_OBJECT_HINTS

    tlc = title.lower()
    tokens = re.findall(r"\S+", tlc)
    hints: list[dict[str, str]] = []

    # 'nguy' and 'mắc' are always-flagged (no resolution via concrete object in title length)
    ALWAYS_FLAG = {"nguy", "mắc"}

    for i, tok in enumerate(tokens):
        clean = re.sub(r"[^\w]", "", tok)
        if clean in VAGUE_ACTION_VERBS:
            if clean in ALWAYS_FLAG:
                hints.append({
                    "verb": clean,
                    "position": str(i),
                    "suggestion": VAGUE_ACTION_VERBS[clean],
                })
                continue
            # Look ahead 4 tokens for concrete object
            window = tokens[i + 1: i + 5]
            has_concrete = any(
                any(obj in re.sub(r"[^\w\s]", "", w) for obj in CONCRETE_OBJECT_HINTS)
                for w in window
            )
            if not has_concrete:
                hints.append({
                    "verb": clean,
                    "position": str(i),
                    "suggestion": VAGUE_ACTION_VERBS[clean],
                })
    return hints


def check_hard_criteria(title: str) -> dict[str, Any]:
    """V1.6 — 7 hard criteria + 2 soft info hints.

    Drops `not_orphan_number` from MUST-pass list (was V1.5-lite hard criterion).
    Reason: orphan-number gate is too rigid — production data shows agent-crafted
    titles that ARE clear ("PVS dồn 282 tỷ trích lập") sometimes fail; titles
    that PASS still feel "AI cụt nghĩa" ("FPT mẹ nguy 2.330 tỷ"). User explicit:
    "không thích dập khuôn — phải tùy từng bài". Detector kept as soft hint —
    agent reads as self-check, scorer logs but does not halt pipeline.

    7 V1.6 hard criteria (MUST pass for `passed`):
    - ticker_present
    - word_count_le_16
    - no_em_dash
    - not_label_leak
    - no_han_viet_formal
    - abbreviation_expanded
    - plain_language

    Info-only (logged, NOT in `passed` flag):
    - not_orphan_number (V1.3 detector — soft hint, agent self-check)
    - has_concrete_number (V1.5 detector — soft hint)
    - vague_action_verbs (V1.6 NEW — list of vague verbs flagged)
    """
    ticker_present = has_ticker(title)
    word_count_le_16 = len(title.split()) <= 16
    no_em_dash = not has_em_dash(title)
    not_label_leak = not is_label_leak(title)
    not_orphan_number = not has_orphan_number(title)  # V1.6: info only

    # Hán-Việt formal check
    from lib.voice_rules import HAN_VIET_FORMAL_BAN
    tlc = title.lower()
    han_viet_found = [t for t in HAN_VIET_FORMAL_BAN if t in tlc]
    no_han_viet_formal = len(han_viet_found) == 0

    # Abbreviation expansion
    from lib.quality_gates import check_abbreviation_expanded
    abbrev_result = check_abbreviation_expanded(title)
    abbreviation_expanded = abbrev_result["pass"]

    # Info-only: concrete number presence
    has_concrete_number = has_specific_number(title) and not_orphan_number

    # V1.6 NEW: vague action verbs soft hint
    vague_hints = detect_vague_action_verb(title)

    # plain_language preserved
    plain_language = not has_english(title) and not has_pr_clickbait(title)

    # V1.6: passed = 7 hard criteria only (orphan_number + vague_verbs are soft)
    passed = (
        ticker_present
        and word_count_le_16
        and no_em_dash
        and not_label_leak
        and no_han_viet_formal
        and abbreviation_expanded
        and plain_language
    )

    return {
        "ticker_present": ticker_present,
        "word_count_le_16": word_count_le_16,
        "no_em_dash": no_em_dash,
        "not_label_leak": not_label_leak,
        "no_han_viet_formal": no_han_viet_formal,
        "abbreviation_expanded": abbreviation_expanded,
        "plain_language": plain_language,
        # Info-only (soft hints, not in passed)
        "not_orphan_number": not_orphan_number,
        "has_concrete_number": has_concrete_number,
        "vague_action_verbs": vague_hints,
        "passed": passed,
    }


def score_title(title: str) -> dict[str, Any]:
    """V1.5-lite — 6-point rubric (simplified from V1.3 8-point).

    Drops scorer word bonuses (caused Pattern A pile-on):
    - dramatic_verb +2 (DRAMATIC_VERBS list)
    - concrete_question_subject +1 (CONCRETE_QUESTION_SUBJECTS list)
    - self_explanatory +1 (V1.3)
    - tension_word +1 (TITLE_TENSION_WORDS list)

    Keeps mechanical signals:
    - has_concrete_number: +2 (number with subject, no orphan)
    - open_question (?): +1
    - paradox pattern (mà / nhưng / thật ra): +1
    - extra_concise (≤10 từ): +1
    - has_ticker (bonus for prominence): +1

    Returns {score: int, max: 6, elements: dict}.
    """
    elements = {
        "ticker": has_ticker(title),
        "has_concrete_number": has_specific_number(title) and not has_orphan_number(title),
        "open_question": has_open_question(title),
        "paradox_pattern": has_paradox_pattern(title),
        "extra_concise": len(title.split()) <= 10,
    }
    score = 0
    if elements["has_concrete_number"]:
        score += 2
    if elements["open_question"]:
        score += 1
    if elements["paradox_pattern"]:
        score += 1
    if elements["extra_concise"]:
        score += 1
    if elements["ticker"]:
        score += 1
    return {"score": min(score, 6), "max": 6, "elements": elements}


def pick_best_candidate(candidates: list[str]) -> dict[str, Any]:
    """Apply hard criteria filter + score → return best.

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
