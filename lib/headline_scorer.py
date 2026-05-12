"""Headline scoring module V1.1 — 5 hard criteria + 8-point rubric.

V1.1 PATCH (2026-05-12): em dash '—' BANNED in title (AI-tell signal).
Hard criteria returns nested dict structure with hook_strong + binh_dan_nguy_hiem
as 2-subtest dicts.

Benchmark: 'TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?' should score ≥6/8.
"""
from __future__ import annotations
import re
from typing import Any

# Tension words (was in V5.0 quality_gates per V5.0 plan, dropped from quality_gates
# per V5.1 PATCH — now lives here in Headline scorer).
TITLE_TENSION_WORDS = [
    "hy sinh", "đánh đổi", "nghịch lý", "vì sao", "đổi lấy",
    "không phải", "bù lại", "thay vì", "chấp nhận",
]

DRAMATIC_VERBS = [
    "hy sinh", "đánh đổi", "đặt cược", "bỏ phiếu", "lội ngược",
    "lao dốc", "rút khỏi", "vượt mặt", "tung đòn", "đặt cọc",
    "chấp nhận thua", "tự chậm lại", "đập cửa", "thoát hiểm",
    "chấp nhận hi sinh", "đánh cược", "đổ vỡ", "vực dậy",
    "tiếp đà", "phá kỷ lục", "soán ngôi", "lấn sang", "rơi vào",
]

PR_CLICKBAIT_WORDS = [
    "cú nổ", "bí mật", "sốc", "hot", "thông tin nóng",
    "không thể tin nổi", "cú twist", "kỳ tích", "hé lộ",
    "kỷ tích",  # Vietnamese variant
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
    """Reuse quality_gates English jargon check on title."""
    try:
        from lib.quality_gates import ENGLISH_JARGON
        tlc = title.lower()
        return any(re.search(rf"\b{re.escape(j.lower())}\b", tlc) for j in ENGLISH_JARGON)
    except ImportError:
        return False


def has_em_dash(title: str) -> bool:
    """V1.1 PATCH: em dash '—' (U+2014) BANNED in title.
    Hyphen '-' (U+002D) + en dash '–' (U+2013) acceptable.
    """
    return "—" in title


def check_hard_criteria(title: str) -> dict[str, Any]:
    """V1.1 — 5 hard criteria check.

    Returns dict with 5 keys + computed 'passed' flag:
    - ticker_present: bool
    - word_count_le_12: bool
    - hook_strong: {tension_present, click_test_pass} dict
    - binh_dan_nguy_hiem: {plain_language, sharp_edge} dict
    - no_em_dash: bool
    - passed: bool (all top-level + nested True)
    """
    ticker_present = has_ticker(title)
    word_count_le_12 = len(title.split()) <= 12

    # Hook strong = 2 sub-tests
    tension_present = (
        has_dramatic_verb(title)
        or has_tension_word(title)
        or has_paradox_pattern(title)
    )
    # Click test heuristic: has number/question/dramatic verb makes reader curious
    click_test_pass = (
        has_specific_number(title)
        or has_open_question(title)
        or has_dramatic_verb(title)
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

    passed = (
        ticker_present
        and word_count_le_12
        and hook_strong["tension_present"]
        and hook_strong["click_test_pass"]
        and binh_dan_nguy_hiem["plain_language"]
        and binh_dan_nguy_hiem["sharp_edge"]
        and no_em_dash
    )

    return {
        "ticker_present": ticker_present,
        "word_count_le_12": word_count_le_12,
        "hook_strong": hook_strong,
        "binh_dan_nguy_hiem": binh_dan_nguy_hiem,
        "no_em_dash": no_em_dash,
        "passed": passed,
    }


def score_title(title: str) -> dict[str, Any]:
    """8-point rubric. Only call after check_hard_criteria passes.

    Returns {score: int, max: 8, elements: dict}.
    """
    elements = {
        "ticker": has_ticker(title),
        "dramatic_verb": has_dramatic_verb(title),
        "specific_number": has_specific_number(title),
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
    if elements["open_question"]:
        score += 1
    if elements["tension_word"]:
        score += 1
    if elements["paradox_pattern"]:
        score += 1
    if elements["extra_concise"]:
        score += 1
    return {"score": score, "max": 8, "elements": elements}


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
