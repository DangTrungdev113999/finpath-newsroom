"""5 quality gates V3.6 — mechanical pass/fail checker for Master Bank articles.

Each gate returns a dict: {"pass": bool, "reason": str (empty if pass)}.
"""
from __future__ import annotations
import re
from typing import Any

ENGLISH_JARGON = {
    "npl", "nim", "casa", "car", "irb", "rwa", "esop", "sme", "nii", "ldr",
    "llr", "cof", "tpdn", "yoy", "qoq", "ytd", "roe", "roa",
    "basel",
    "trade-off", "tradeoff", "anchor", "relevant", "confirm", "pattern",
    "breaking", "momentum", "defensive", "catalyst", "symbolic", "metric",
    "event", "story", "scenario", "target", "portfolio", "buffer",
    "stress test", "arithmetic", "coverage", "opportunity cost",
}

JARGON_EXCEPTIONS = {
    "vietcombank", "techcombank", "vpbank", "vietinbank", "agribank",
    "bidv", "mb bank", "acb", "shb", "vncb", "gp bank", "oceanbank",
    "vạn thịnh phát", "tân hoàng minh", "lottner", "jens",
    "q1", "q2", "q3", "q4", "nhnn", "đhđcđ", "ndth", "scb",
    "tcb", "vcb", "mbb", "bid", "ctg", "vpb",
}

METADATA_TAGS = [
    "strategic-shift", "risk_highlight", "insight_type", "critique angle",
    "data_skepticism", "historical_analog", "alt_interpretation",
    "insight_wrong", "execution_unfaithful",
    "paradox", "why_now", "hidden_mechanism", "comparison_deep", "early_signal",
    "low_writeability", "low_insight_potential", "dup_event", "dup_angle_recent",
]


def _strip_skeptic_section(body: str) -> str:
    parts = re.split(r"^##\s+G[óo]c\s+nh[iì]n\s+ng[ưu]?[ợo]?c\s*$", body, flags=re.MULTILINE)
    return parts[0]


def _strip_pipeline_log(body: str) -> str:
    return re.sub(r"<details>.*?</details>", "", body, flags=re.DOTALL)


def check_no_english_jargon(body: str) -> dict[str, Any]:
    cleaned = _strip_skeptic_section(_strip_pipeline_log(body))
    cleaned_lc = cleaned.lower()
    found: list[str] = []
    for jargon in ENGLISH_JARGON:
        pattern = r"\b" + re.escape(jargon) + r"\b"
        if re.search(pattern, cleaned_lc):
            found.append(jargon)
    if found:
        return {"pass": False, "reason": f"Banned jargon: {', '.join(found)}"}
    return {"pass": True, "reason": ""}


def check_word_count(body: str) -> dict[str, Any]:
    cleaned = _strip_skeptic_section(_strip_pipeline_log(body)).strip()
    words = cleaned.split()
    n = len(words)
    if n < 200:
        return {"pass": False, "reason": f"Too short: {n} words (need 200-400)"}
    if n > 400:
        return {"pass": False, "reason": f"Too long: {n} words (need 200-400)"}
    return {"pass": True, "reason": ""}


def check_mechanism_count(body: str) -> dict[str, Any]:
    cleaned = _strip_skeptic_section(_strip_pipeline_log(body))
    bullets = re.findall(r"^[-*]\s+\S", cleaned, flags=re.MULTILINE)
    n = len(bullets)
    if n < 3:
        return {"pass": False, "reason": f"Too few mechanisms: {n} bullets (need 3-7)"}
    if n > 7:
        return {"pass": False, "reason": f"Too many mechanisms: {n} bullets (need 3-7)"}
    return {"pass": True, "reason": ""}


def check_can_de_y_narrative(body: str) -> dict[str, Any]:
    cleaned = _strip_skeptic_section(_strip_pipeline_log(body))
    m = re.search(
        r"^##\s+C[ầa]n\s+đ[ểe]?\s+ý\s*$([\s\S]*?)(?=^##\s|\Z)",
        cleaned,
        flags=re.MULTILINE,
    )
    if not m:
        return {"pass": True, "reason": "section missing — optional"}
    section = m.group(1).strip()
    lines = [ln.strip() for ln in section.split("\n") if ln.strip()]
    bullet_lines = [ln for ln in lines if ln.startswith(("- ", "* "))]
    if bullet_lines and len(bullet_lines) == len(lines):
        for bullet in bullet_lines:
            content = bullet[2:].strip()
            if len(content.split()) < 8:
                return {"pass": False, "reason": f"Cần để ý bullet too short (data-point only): '{bullet}'"}
        if 2 <= len(bullet_lines) <= 3:
            return {"pass": True, "reason": ""}
        return {"pass": False, "reason": f"Too many bullets ({len(bullet_lines)}) — narrative or 2-3 caveat only"}
    return {"pass": True, "reason": ""}


def check_no_metadata_leak(body: str) -> dict[str, Any]:
    cleaned = _strip_skeptic_section(_strip_pipeline_log(body))
    cleaned_lc = cleaned.lower()
    found: list[str] = []
    for tag in METADATA_TAGS:
        if tag.lower() in cleaned_lc:
            found.append(tag)
    if found:
        return {"pass": False, "reason": f"Metadata leak: {', '.join(found)}"}
    return {"pass": True, "reason": ""}


def check_all(body: str) -> dict[str, dict[str, Any]]:
    return {
        "no_english_jargon": check_no_english_jargon(body),
        "word_count": check_word_count(body),
        "mechanism_count": check_mechanism_count(body),
        "can_de_y_narrative": check_can_de_y_narrative(body),
        "no_metadata_leak": check_no_metadata_leak(body),
    }
