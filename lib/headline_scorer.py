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

# V1.3: voice constants moved to lib/voice_rules.py for title + body sharing.
# Re-export at module level for backward compat (existing tests + downstream
# code import these names from headline_scorer).
from lib.voice_rules import (
    TITLE_TENSION_WORDS,
    DRAMATIC_VERBS,
    PR_CLICKBAIT_WORDS,
    BAO_CHI_FORMULAIC_PHRASES,
    NATURALIZED_FINANCE_TERMS,
    BAO_CHI_QUARTER_PATTERN,
    RUBRIC_LABEL_LEAK,
    CONCRETE_QUESTION_SUBJECTS,
)

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
    """Number with financial unit (vd 5.000 tỷ, 30%, 250 đ)."""
    return bool(re.search(
        r"\d+([.,]\d+)?\s*(tỷ|triệu|nghìn|%|đ|/năm|/tháng|/quý|đ/tháng|bps|điểm)",
        title, re.IGNORECASE
    ))


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


def check_hard_criteria(title: str) -> dict[str, Any]:
    """V1.2 — 7 hard criteria check.

    Returns dict with 7 keys + computed 'passed' flag:
    - ticker_present: bool
    - word_count_le_12: bool
    - hook_strong: {tension_present, click_test_pass} dict
    - binh_dan_nguy_hiem: {plain_language, sharp_edge} dict
    - no_em_dash: bool
    - not_bao_chi: bool (V1.2 NEW — ban formula clichés + báo chí buzzwords)
    - not_label_leak: bool (V1.2 NEW — title KHÔNG được = rubric label)
    - passed: bool (all top-level + nested True)
    """
    ticker_present = has_ticker(title)
    word_count_le_12 = len(title.split()) <= 12

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

    passed = (
        ticker_present
        and word_count_le_12
        and hook_strong["tension_present"]
        and hook_strong["click_test_pass"]
        and binh_dan_nguy_hiem["plain_language"]
        and binh_dan_nguy_hiem["sharp_edge"]
        and no_em_dash
        and not_bao_chi
        and not_label_leak
    )

    return {
        "ticker_present": ticker_present,
        "word_count_le_12": word_count_le_12,
        "hook_strong": hook_strong,
        "binh_dan_nguy_hiem": binh_dan_nguy_hiem,
        "no_em_dash": no_em_dash,
        "not_bao_chi": not_bao_chi,
        "not_label_leak": not_label_leak,
        "passed": passed,
    }


def score_title(title: str) -> dict[str, Any]:
    """V1.2 — 8-point rubric. Only call after check_hard_criteria passes.

    Returns {score: int, max: 8, elements: dict}.

    Scoring (max 8, weighted by impact on reader curiosity):
    - dramatic_verb: +2
    - specific_number: +2
    - concrete_question_subject (V1.2): +1 (bonus for 'ai gom?' vs 'đổi lấy gì?')
    - open_question: +1
    - tension_word: +1
    - paradox_pattern: +1
    - extra_concise (≤10 từ): +1
    """
    elements = {
        "ticker": has_ticker(title),
        "dramatic_verb": has_dramatic_verb(title),
        "specific_number": has_specific_number(title),
        "concrete_question_subject": has_concrete_question_subject(title),
        "open_question": has_open_question(title),
        "tension_word": has_tension_word(title),
        "paradox_pattern": has_paradox_pattern(title),
        "extra_concise": len(title.split()) <= 10,
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
    if elements["extra_concise"]:
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
