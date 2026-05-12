"""5 quality gates V4.0 — mechanical pass/fail checker for Master Bank articles.

Gates:
  1. no_english_jargon — 0% từ tiếng Anh trong content
  2. word_count — 200-400 hard cap
  3. body_pattern — 1 opening paragraph + 3-7 substantive bullets + 1 closing
  4. title_as_hook — title contains '?' or '—' + tension word
  5. no_metadata_leak — không enum tags trong content
"""
from __future__ import annotations
import re
from typing import Any

ENGLISH_JARGON = {
    # Bank abbreviations
    "npl", "nim", "casa", "car", "irb", "rwa", "esop", "sme", "nii", "ldr",
    "llr", "cof", "tpdn", "yoy", "qoq", "ytd", "roe", "roa", "eps",
    "basel",
    # Common English finance/news words
    "trade-off", "tradeoff", "anchor", "relevant", "confirm", "pattern",
    "breaking", "momentum", "defensive", "catalyst", "symbolic", "metric",
    "event", "story", "scenario", "target", "portfolio", "buffer",
    "stress test", "arithmetic", "coverage", "opportunity cost",
}

# Narrative-only extras — banned in Story Editor brief narratives but allowed
# in Master body if context warrants (e.g., "Big4" = legit Vietnamese banking
# shorthand for VCB/BID/CTG/AGR). Brief narratives must be 100% Vietnamese
# thuần since they explain editorial intent to user.
ENGLISH_JARGON_NARRATIVE_EXTRA = {
    "funding",
    "big4",
    "forward-looking",
    "cross-check",
}

METADATA_TAGS = [
    "strategic-shift", "risk_highlight", "insight_type", "critique angle",
    "data_skepticism", "historical_analog", "alt_interpretation",
    "insight_wrong", "execution_unfaithful",
    "paradox", "why_now", "hidden_mechanism", "comparison_deep", "early_signal",
    "low_writeability", "low_insight_potential", "dup_event", "dup_angle_recent",
]

TITLE_TENSION_WORDS = [
    "hy sinh", "đánh đổi", "nghịch lý", "vì sao", "đổi lấy",
    "không phải", "bù lại", "thay vì", "chấp nhận",
]


def _strip_skeptic_section(body: str) -> str:
    """Remove Skeptic '## Góc nhìn ngược' section if present."""
    parts = re.split(
        r"^#{2,3}\s+G[óo]c\s+nh[iì]n\s+ng[ưu]?[ợo]?c\s*$",
        body, flags=re.MULTILINE,
    )
    return parts[0]


def _strip_pipeline_log(body: str) -> str:
    return re.sub(r"<details>.*?</details>", "", body, flags=re.DOTALL)


def _clean(body: str) -> str:
    return _strip_skeptic_section(_strip_pipeline_log(body))


def check_no_english_jargon(body: str) -> dict[str, Any]:
    cleaned = _clean(body).lower()
    found = [j for j in ENGLISH_JARGON if re.search(r"\b" + re.escape(j) + r"\b", cleaned)]
    if found:
        return {"pass": False, "reason": f"Banned jargon: {', '.join(found)}"}
    return {"pass": True, "reason": ""}


def _strip_explained_jargon(body: str) -> str:
    """Strip 'JARGON (giải thích)' patterns to allow legitimate explained jargon.

    Example: 'NIM (biên lãi vay)' → '' (allowed pass-through).
    'NIM' alone → not stripped (will fail gate).

    Iterates ENGLISH_JARGON dict — for each term, build pattern that matches
    'TERM <whitespace> ( ... )' and remove. Then remaining text is checked.
    Multi-jargon ('NIM (biên lãi) và CASA (tỷ lệ)') handled by sequential
    iteration; nested parens NOT supported.
    """
    cleaned = body
    for term in ENGLISH_JARGON:
        pattern = rf"\b{re.escape(term)}\b\s*\([^)]+\)"
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    return cleaned


def check_no_english_jargon_skeptic(skeptic_body: str) -> dict[str, Any]:
    """Bug C fix — Skeptic critique 0% từ tiếng Anh.

    Allows pattern 'JARGON (tiếng Việt giải thích)' — strips before check.
    Bare jargon fails. Input IS the skeptic body (do NOT strip skeptic
    section — input is already isolated).
    """
    if not skeptic_body or not skeptic_body.strip():
        return {"pass": True, "reason": ""}
    cleaned = _strip_explained_jargon(skeptic_body).lower()
    found = [j for j in ENGLISH_JARGON if re.search(r"\b" + re.escape(j) + r"\b", cleaned)]
    if found:
        return {"pass": False, "reason": f"Banned jargon trong Skeptic: {', '.join(found)}"}
    return {"pass": True, "reason": ""}


def check_no_english_jargon_narrative(narratives: list[str]) -> dict[str, Any]:
    """Bug B fix — 0% từ tiếng Anh trong narrative fields của Story Editor brief.

    Checks ENGLISH_JARGON ∪ ENGLISH_JARGON_NARRATIVE_EXTRA. The extra set
    contains terms (e.g. "big4") that are legit in Master body but must NOT
    leak into editorial narrative explanations. Concat narratives →
    case-insensitive word-boundary regex. Does NOT apply `_clean()` —
    narratives là raw string, không có Skeptic section / pipeline-log block markup.
    """
    if not narratives:
        return {"pass": True, "reason": ""}
    concatenated = " ".join(n for n in narratives if n).lower()
    if not concatenated.strip():
        return {"pass": True, "reason": ""}
    all_jargon = list(ENGLISH_JARGON) + list(ENGLISH_JARGON_NARRATIVE_EXTRA)
    found = [j for j in all_jargon if re.search(r"\b" + re.escape(j) + r"\b", concatenated)]
    if found:
        return {"pass": False, "reason": f"Banned jargon: {', '.join(found)}"}
    return {"pass": True, "reason": ""}


def check_word_count(body: str) -> dict[str, Any]:
    cleaned = _clean(body).strip()
    n = len(cleaned.split())
    if n < 200:
        return {"pass": False, "reason": f"Too short: {n} words (need 200-400)"}
    if n > 400:
        return {"pass": False, "reason": f"Too long: {n} words (need 200-400)"}
    return {"pass": True, "reason": ""}


def check_body_pattern(body: str) -> dict[str, Any]:
    """Gate 3 — body structure: 1 opening paragraph + 3-7 substantive bullets + 1 closing.

    NO '## Cần để ý' section allowed. Bullets must be ≥20 words with ≥1 bold.
    """
    cleaned = _clean(body).strip()

    # Check no `## Cần để ý` heading
    if re.search(r"^#{2,3}\s+C[ầa]n\s+đ[ểe]?\s+ý", cleaned, flags=re.MULTILINE):
        return {"pass": False, "reason": "Contains '## Cần để ý' section — drop it in V4.0"}

    # Split into blocks separated by blank lines
    blocks = [b.strip() for b in re.split(r"\n\s*\n", cleaned) if b.strip()]
    if len(blocks) < 3:
        return {"pass": False, "reason": f"Need ≥3 blocks (opening + bullets + closing), got {len(blocks)}"}

    opening = blocks[0]
    closing = blocks[-1]
    middle = blocks[1:-1]

    # Opening: must be paragraph (not bullet), ≥30 words
    if opening.startswith(("- ", "* ")):
        return {"pass": False, "reason": "Opening block must be paragraph, not bullet"}
    if len(opening.split()) < 30:
        return {"pass": False, "reason": f"Opening paragraph too short: {len(opening.split())} words (need ≥30)"}

    # Closing: 1 sentence, not bullet, not heading
    if closing.startswith(("- ", "* ")):
        return {"pass": False, "reason": "Closing must be sentence, not bullet"}
    if closing.startswith("#"):
        return {"pass": False, "reason": "Closing must not be heading"}

    # Middle: collect all bullets from middle blocks
    bullets: list[str] = []
    for block in middle:
        for line in block.split("\n"):
            line = line.strip()
            if line.startswith(("- ", "* ")):
                bullets.append(line[2:].strip())
            elif line:
                # Non-bullet line in middle = continuation of previous bullet (multi-line) — append
                if bullets:
                    bullets[-1] += " " + line
                else:
                    return {"pass": False, "reason": f"Non-bullet, non-opening text in middle: '{line[:60]}'"}

    if len(bullets) < 3:
        return {"pass": False, "reason": f"Need 3-7 bullets, got {len(bullets)}"}
    if len(bullets) > 7:
        return {"pass": False, "reason": f"Need 3-7 bullets, got {len(bullets)}"}

    # Each bullet: ≥20 words AND ≥1 bold (`**...**`)
    for i, b in enumerate(bullets, start=1):
        words = len(b.split())
        if words < 20:
            return {"pass": False, "reason": f"Bullet {i} too short: {words} words (need ≥20)"}
        if "**" not in b:
            return {"pass": False, "reason": f"Bullet {i} missing bold (**...**) highlight"}

    return {"pass": True, "reason": ""}


def check_title_as_hook(title: str) -> dict[str, Any]:
    """Gate 4 — title contains '?' OR '—' + tension word."""
    if not title:
        return {"pass": False, "reason": "Title empty"}
    title_lc = title.lower()
    if "?" in title:
        return {"pass": True, "reason": ""}
    if "—" in title:
        for word in TITLE_TENSION_WORDS:
            if word in title_lc:
                return {"pass": True, "reason": ""}
        return {"pass": False, "reason": "Title has '—' but no tension word"}
    return {"pass": False, "reason": "Title is summary — needs '?' or '—' + tension word"}


def check_no_metadata_leak(body: str) -> dict[str, Any]:
    cleaned = _clean(body).lower()
    found = [t for t in METADATA_TAGS if t.lower() in cleaned]
    if found:
        return {"pass": False, "reason": f"Metadata leak: {', '.join(found)}"}
    return {"pass": True, "reason": ""}


def check_all(body: str, title: str = "") -> dict[str, dict[str, Any]]:
    """Run all 5 V4.0 gates. Pass title for Gate 4."""
    return {
        "no_english_jargon": check_no_english_jargon(body),
        "word_count": check_word_count(body),
        "body_pattern": check_body_pattern(body),
        "title_as_hook": check_title_as_hook(title),
        "no_metadata_leak": check_no_metadata_leak(body),
    }


# === V5.0 Phase 1.5 — Voice Layer gates ===

HEDGING_TERMS = [
    "có thể", "tùy thuộc", "vẫn chờ", "khả năng cao", "đáng theo dõi",
    "nhiều khả năng", "chưa rõ", "có khả năng",
]


def check_no_hedging(body: str) -> dict[str, Any]:
    """V5.0 Gate 6 — reject hedging terms in body (no nước đôi).

    Keyword-based initial impl. B-30 will redefine via LLM-as-judge
    (V5.1.2 patch) to handle nuanced cases keyword regex can't catch.
    """
    cleaned = _clean(body).lower()
    found = [t for t in HEDGING_TERMS if t in cleaned]
    if found:
        return {"pass": False, "reason": f"Hedging terms: {', '.join(found)}"}
    return {"pass": True, "reason": ""}


DIRECTION_KEYWORDS_RE = re.compile(
    r"(tích cực|tiêu cực|cảnh báo|đáng giữ|đáng chú ý|rủi ro|cơ hội|"
    r"tăng trưởng dài hạn|đỉnh ngắn hạn|"
    r"đáng lo|đáng tích lũy)",
    re.IGNORECASE,
)
TIMEFRAME_KEYWORDS_RE = re.compile(
    r"(12 tháng|18 tháng|6 tháng|3 tháng|Q[1-4](/\d{4})?|năm \d{4}|"
    r"ngắn hạn|trung hạn|dài hạn|trung-dài hạn|quý tới)",
    re.IGNORECASE,
)
HOLDER_ACTION_RE = re.compile(
    r"(NĐT|nhà đầu tư|người (giữ|cầm)|đang (cầm|giữ)|holder|"
    r"khớp NĐT)[^.]*?(giữ|chờ|tích lũy|thận trọng|cắt|không nên|nên)",
    re.IGNORECASE,
)


def check_verdict_line(body: str) -> dict[str, Any]:
    """V5.0 Gate 7 — closing must contain 3 elements: direction + timeframe + holder action."""
    cleaned = _clean(body).strip()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", cleaned) if b.strip()]
    closing_text = "\n".join(blocks[-2:]) if len(blocks) >= 2 else cleaned

    has_direction = bool(DIRECTION_KEYWORDS_RE.search(closing_text))
    has_timeframe = bool(TIMEFRAME_KEYWORDS_RE.search(closing_text))
    has_holder_action = bool(HOLDER_ACTION_RE.search(closing_text))

    missing = []
    if not has_direction:
        missing.append("direction")
    if not has_timeframe:
        missing.append("timeframe")
    if not has_holder_action:
        missing.append("action_for_holder")

    if missing:
        return {"pass": False, "reason": f"Verdict missing: {missing}"}
    return {"pass": True, "reason": ""}


BULLISH_TERMS = [
    "tăng trưởng", "tích cực", "đáng giữ", "đáng chú ý", "cơ hội",
    "mạnh", "ổn định", "lợi thế", "phòng thủ thành công",
    "buffer tích lũy", "cao hơn", "vượt", "lấn", "ngon", "tăng mua",
    "đáng tích lũy",
]
BEARISH_TERMS = [
    "rủi ro", "cảnh báo", "yếu", "lỗ", "giảm",
    "đỉnh ngắn hạn", "không nên", "đáng lo", "đe dọa", "căng thẳng",
    "tiêu cực", "bùng phát", "lao dốc", "cẩn thận", "thận trọng",
]


def check_stance_consistency(body: str, stance: str) -> dict[str, Any]:
    """V5.0 Gate 8 — Master article tone matches brief stance."""
    cleaned = _clean(body).lower()
    bullish = sum(1 for t in BULLISH_TERMS if t in cleaned)
    bearish = sum(1 for t in BEARISH_TERMS if t in cleaned)
    total = bullish + bearish

    if total == 0:
        return {"pass": False, "reason": "Article has no stance keywords (lifeless)"}

    bull_ratio = bullish / total

    if stance == "bullish" and bull_ratio < 0.5:
        return {"pass": False, "reason": f"Brief=bullish but body tone bearish ({bullish} bull vs {bearish} bear)"}
    if stance == "bearish" and bull_ratio > 0.5:
        return {"pass": False, "reason": f"Brief=bearish but body tone bullish ({bullish} bull vs {bearish} bear)"}
    if stance == "divergent" and (bull_ratio < 0.3 or bull_ratio > 0.7):
        return {"pass": False, "reason": f"Brief=divergent but body one-sided ({bull_ratio:.0%} bullish)"}

    return {"pass": True, "reason": ""}


# Sentence density: each sentence must contain ≥1 specific element.
SPECIFIC_ELEMENT_RE = re.compile(
    r"(\d+([.,]\d+)?(%|đ|tỷ|nghìn|triệu)?|"
    r"\b(VCB|TCB|MBB|CTG|BID|VPB|HDB|STB|SHB|EIB|TPB|MSB|LPB|OCB|VIB|ACB|"
    r"SSI|VND|HCM|VCI|VIX|SHS|MBS|BVS|"
    r"VHM|NVL|KDH|DXG|"
    r"Big4|HOSE|HNX|UPCOM|NHNN|ĐHĐCĐ)\b|"
    r"(cao hơn|thấp hơn|gấp|vượt|hơn|thấp nhất|cao nhất|so với|so cùng kỳ)|"
    r"(Q[1-4]|năm \d{4}|tháng \d|quý|tuần|YTD|YoY|QoQ|hôm nay)|"
    r"(do|vì|nhờ|khiến|dẫn đến|kéo theo|bổ sung|trở thành|chuyển|tích lũy|đánh đổi)|"
    r"(rút|chuyển|duy trì|phòng thủ|lấn sang|tăng|giảm|đi chậm|nới|co))",
    re.IGNORECASE,
)


def _split_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]


def _is_bullet_label(sentence: str) -> bool:
    s = sentence.lstrip("- *").strip()
    return bool(re.match(r"^\*\*[^*]+\*\*:?\s*$", s))


def check_sentence_density(body: str) -> dict[str, Any]:
    """V5.0 Gate 9 — ≥80% sentences in body contain ≥1 specific element."""
    cleaned = _clean(body).strip()
    sentences = _split_sentences(cleaned)
    countable = [s for s in sentences if not _is_bullet_label(s)]
    if not countable:
        return {"pass": True, "reason": ""}
    has_element = [bool(SPECIFIC_ELEMENT_RE.search(s)) for s in countable]
    pass_count = sum(has_element)
    ratio = pass_count / len(countable)
    if ratio < 0.8:
        fluff = [s for s, ok in zip(countable, has_element) if not ok]
        return {
            "pass": False,
            "reason": f"Density {ratio:.0%} (<80%) — {len(fluff)} fluff sentences: {fluff[:3]}",
        }
    return {"pass": True, "reason": ""}


def check_em_dash_density(body: str) -> dict[str, Any]:
    """V5.1.2 PATCH Gate — max 1 em dash (U+2014) per 100 words.

    User feedback: em dash is AI-tell. Banned in title, minimized in body.
    """
    cleaned = _clean(body)
    em_dash_count = cleaned.count("—")
    word_count = len([w for w in re.findall(r"\S+", cleaned) if w])
    if word_count == 0:
        return {"pass": True, "reason": ""}
    threshold = max(1.0, word_count / 100.0)
    if em_dash_count > threshold:
        return {
            "pass": False,
            "reason": f"Em dash overused: {em_dash_count} em dashes in {word_count} words (max {threshold:.1f})",
        }
    return {"pass": True, "reason": ""}
