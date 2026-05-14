"""5 quality gates V4.0 — mechanical pass/fail checker for Master Bank articles.

Gates:
  1. no_english_jargon — 0% từ tiếng Anh trong content
  2. word_count — 200-400 hard cap
  3. body_pattern — 1 opening paragraph + 3-7 substantive bullets + 1 closing
  4. title_as_hook — title contains '?' or '—' + tension word
  5. no_metadata_leak — không enum tags trong content
"""
from __future__ import annotations
import os
import re
from functools import lru_cache
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
#
# These gates extend the V4.0 surface but are NOT yet wired into `check_all`
# (which still dispatches the V4.0 5-gate set). B-6 (Task 6) creates
# `check_all_v5(body, format_id, stance)` which wires the new gates +
# per-format gates. Until then, callers must invoke these gates directly.

HEDGING_TERMS = [
    "có thể", "tùy thuộc", "vẫn chờ", "khả năng cao", "đáng theo dõi",
    "nhiều khả năng", "chưa rõ", "có khả năng",
]


def _check_no_hedging_keyword_fallback(body: str) -> dict[str, Any]:
    """V5.0 keyword-based check (B-5). Used when LLM unavailable.

    Active path when ANTHROPIC_API_KEY missing OR anthropic SDK not
    installed OR LLM call raises. Preserves backward compatibility with
    pre-B-30 callers + keeps CI green without API key.
    """
    cleaned = _clean(body).lower()
    found = [t for t in HEDGING_TERMS if t in cleaned]
    if found:
        return {
            "pass": False,
            "reason": f"Hedging terms (keyword fallback): {', '.join(found)}",
        }
    return {"pass": True, "reason": ""}


def _check_no_hedging_llm_judge(body: str) -> dict[str, Any]:
    """V5.1.2 LLM-as-judge implementation.

    Definition: "Ba phải" = câu khẳng định trung tính không cam kết hướng,
    có thể đúng dù sự thật ngược lại.

    Two tests per sentence:
      Test 1 — Reverse-truth: if actual outcome is opposite of what sentence
        implies, does sentence still hold? Yes = hedging.
      Test 2 — Direction: does sentence commit to direction (up/down/strong/
        weak/positive/negative)? No direction = hedging.

    A sentence fails if either test fails.

    Falls back to keyword check on any error (no API key, SDK missing,
    network error, malformed response).
    """
    if not os.getenv("ANTHROPIC_API_KEY"):
        return _check_no_hedging_keyword_fallback(body)

    try:
        import anthropic  # type: ignore
    except ImportError:
        return _check_no_hedging_keyword_fallback(body)

    cleaned = _clean(body).strip()
    sentences = _split_sentences(cleaned)
    countable = [s for s in sentences if not _is_bullet_label(s) and len(s.split()) >= 5]
    if not countable:
        return {"pass": True, "reason": ""}

    prompt_lines = [
        "Apply 2 tests to each Vietnamese stock analysis sentence below.",
        "",
        "Test 1 — Reverse-truth: If actual outcome is OPPOSITE of what the "
        "sentence implies, does the sentence still hold? Yes = hedging.",
        "Test 2 — Direction: Does the sentence commit to a direction "
        "(up/down/strong/weak/positive/negative)? No direction = hedging.",
        "",
        "A sentence FAILS if it fails EITHER test. Return JSON array only, "
        "one entry per sentence:",
        '[{"idx": 0, "fail": true|false, "reason": "..."}]',
        "",
        "Sentences:",
    ]
    for i, s in enumerate(countable):
        prompt_lines.append(f"{i}. {s}")
    prompt = "\n".join(prompt_lines)

    try:
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text if msg.content else "[]"
        if "```json" in text:
            text = text.split("```json", 1)[1].split("```", 1)[0].strip()
        elif "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0].strip()
        import json as _json
        results = _json.loads(text.strip())
        failed = [r for r in results if r.get("fail")]
        if failed:
            reasons = "; ".join(
                f"sent[{r.get('idx', '?')}]: {r.get('reason', 'hedging')}"
                for r in failed[:3]
            )
            return {"pass": False, "reason": f"Hedging (LLM judge): {reasons}"}
        return {"pass": True, "reason": ""}
    except Exception:
        # Any LLM failure → fall back to keyword check.
        return _check_no_hedging_keyword_fallback(body)


def check_no_hedging(body: str) -> dict[str, Any]:
    """V5.1.2 PATCH (B-30) — LLM-as-judge primary, keyword fallback.

    Definition: "Ba phải" = câu khẳng định trung tính không cam kết hướng,
    có thể đúng dù sự thật ngược lại.

    LLM mode runs 2 tests per sentence (reverse-truth + direction commitment).
    Falls back to V5.0 keyword check when ANTHROPIC_API_KEY missing, the
    anthropic SDK is not installed, or the API call fails for any reason.
    """
    return _check_no_hedging_llm_judge(body)


DIRECTION_KEYWORDS_RE = re.compile(
    r"(tích cực|tiêu cực|cảnh báo|đáng giữ|đáng chú ý|rủi ro|cơ hội|"
    r"tăng trưởng dài hạn|đỉnh ngắn hạn|"
    r"đáng lo|đáng tích lũy|"
    # V1.3 — action-based direction (V1.3 voice uses "nên giữ/giảm/cắt" not "tích cực")
    r"nên giữ|nên cầm|nên giảm|nên cắt|nên bán|nên tích lũy|nên mua|nên thoát|"
    r"phù hợp|không phù hợp|phòng thủ)",
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
    """V5.0 Gate 7 + V1.3 TIGHTEN — closing 3 elements + actionable composition.

    V5.0: direction + timeframe + holder action.
    V1.3: also call check_actionable_closing (stance verb + quantified trigger
    + no vague phrase). Closing pass cũ rule mà fail actionable → verdict fail.
    """
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

    # V1.3 PATCH — compose actionable_closing (stricter actionability check)
    actionable = check_actionable_closing(body)
    if not actionable["pass"]:
        return {"pass": False, "reason": f"Verdict not actionable: {actionable['reason']}"}

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
    "tiêu cực", "bùng phát", "lao dốc", "cẩn thận",
    # Note: "thận trọng" removed — overlaps with HOLDER_ACTION_RE which treats
    # "NĐT thận trọng" as legitimate holder action regardless of stance.
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
# V1.8 (2026-05-13): dropped metaphor marker group (như/kiểu/thật ra/chẳng khác/...).
# AI was gamifying gate by sprinkling decorative phrases without substance —
# user feedback "ưu tiên ví von" prescription caused mannerism. Now sentence
# must contain CONCRETE substance: number, ticker, comparative, time anchor,
# causal verb, or action verb. Metaphor when natural still passes via these
# concrete elements (e.g. "gấp 3 lần" matches comparative group).
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


# ============================================================
# V1.3 BODY VOICE GATES (bình dân xuồng xã nguy hiểm)
# ============================================================

# Per-format bold density thresholds read from data/format_registry.yaml
# (V1.3). flash_qa uses absolute count; others use ratio = bold/word.
# Fallback default if format spec lacks `bold_density_min` field.
_BOLD_DENSITY_FALLBACK = {"mode": "ratio", "value": 0.04}

_BOLD_RE = re.compile(r"\*\*[^*]+\*\*")

# Quantified trigger: number with unit OR conditional pattern with number
# nearby. Catches "12 tháng", "35K tỷ", "vượt 3,5%", "nếu rơi dưới 70".
_QUANTIFIED_TRIGGER_RE = re.compile(
    r"\d+([.,]\d+)?\s*(tỷ|%|nghìn|triệu|đ|/năm|/tháng|/quý|K|nghìn/cp|"
    r"tháng|quý|năm|cp|cổ phiếu|điểm|bps|đồng)",
    re.IGNORECASE,
)



def check_bold_density(body: str, format_id: str) -> dict[str, Any]:
    """V1.3 — per-format markdown bold density target.

    flash_qa: ≥3 bold absolute count (Twitter style short).
    standard_qa: ≥4% density.
    standard_listicle: ≥5% density (densest).
    standard_narrative: ≥3% density (prose flow allowed).

    User feedback 2026-05-13: body audit TB 1.83% — quá thấp, scan-fail.
    """
    cleaned = _clean(body)
    bold_count = len(_BOLD_RE.findall(cleaned))
    # Word count excluding markdown markers
    text_for_words = _BOLD_RE.sub(lambda m: m.group(0)[2:-2], cleaned)
    word_count = len([w for w in re.findall(r"\S+", text_for_words) if w])

    if word_count == 0:
        return {"pass": True, "reason": "", "bold_count": 0, "density": 0.0}

    try:
        fmt = get_format(format_id)
        config = fmt.get("bold_density_min", _BOLD_DENSITY_FALLBACK)
    except KeyError:
        config = _BOLD_DENSITY_FALLBACK
    density = bold_count / word_count

    if config["mode"] == "absolute":
        if bold_count < config["value"]:
            return {
                "pass": False,
                "reason": f"Bold count {bold_count} < {config['value']} (flash_qa absolute min)",
                "bold_count": bold_count,
                "density": density,
            }
    else:
        if density < config["value"]:
            return {
                "pass": False,
                "reason": f"Bold density {density:.1%} < {config['value']:.0%} ({format_id})",
                "bold_count": bold_count,
                "density": density,
            }

    return {"pass": True, "reason": "", "bold_count": bold_count, "density": density}


def check_actionable_closing(body: str) -> dict[str, Any]:
    """V1.3 — closing must be actionable for NĐT.

    3 layers:
    1. Contains ≥1 STANCE_VERB ("nên cầm" / "nên giảm" / "phù hợp NĐT").
    2. Contains ≥1 quantified trigger (price/percent/condition with number).
    3. NOT match CLOSING_VAGUE_BAN ("cần theo dõi" / "làm chỉ báo").

    Audit pattern: VHM-cổ tức "theo dõi hấp thụ làm chỉ báo sớm" → fail.
    SSI-ESOP "giữ 12 tháng nếu margin > 35K tỷ" → pass.
    """
    from lib.voice_rules import STANCE_VERBS, CLOSING_VAGUE_BAN

    cleaned = _clean(body).strip()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", cleaned) if b.strip()]
    # Take last 1-2 blocks as closing (Master closing usually 1 paragraph)
    closing = "\n".join(blocks[-2:]) if len(blocks) >= 2 else cleaned
    closing_lc = closing.lower()

    # Layer 3: vague phrase ban (check first — fail fast on cliché)
    vague_found = [p for p in CLOSING_VAGUE_BAN if p in closing_lc]
    if vague_found:
        return {
            "pass": False,
            "reason": f"Closing vague: {vague_found}",
        }

    # Layer 1: stance verb required
    stance_found = [v for v in STANCE_VERBS if v in closing_lc]
    if not stance_found:
        return {
            "pass": False,
            "reason": "Closing missing stance verb (nên cầm/giảm/giữ/phù hợp NĐT)",
        }

    # Layer 2: quantified trigger required
    if not _QUANTIFIED_TRIGGER_RE.search(closing):
        return {
            "pass": False,
            "reason": "Closing missing quantified trigger (price/percent/condition with number)",
        }

    return {"pass": True, "reason": ""}


# V1.4 — Body sentence richness threshold
_MIN_SENTENCE_WORDS = 10
_MAX_SHORT_RATIO = 0.20


def check_min_sentence_richness(body: str) -> dict[str, Any]:
    """V1.4 — reject body khi >20% câu nội dung <10 từ.

    User feedback STB bài 1 manual: 3/11 sentences ≤9 từ (27%) → feel cụt cụt
    (tail fragments like "Ngành chia hai phe đi ngược chiều." 7 từ standalone).

    Root cause: V1.3 length cap -20% squeeze → Master/writer xé câu thành
    tail fragments để fit budget. V1.4 enforce flow: force compound sentences
    with connectives (vì/khi/khiến/do/nhờ) thay vì split.

    Counting rules:
    - Strip Skeptic + pipeline_log sections (`_clean`)
    - Split by sentence terminators (`_split_sentences`)
    - Exclude bullet-header-only lines (`_is_bullet_label`)
    - Threshold: <10 words = short
    - Fail if short_ratio > 20%

    Edge cases:
    - 0 countable sentences → pass (no division by zero)
    - All bullet headers → pass
    """
    cleaned = _clean(body).strip()
    # V1.5-lite fix: drop bullet header lines (e.g. "- **Foo**:") before
    # sentence splitting. _split_sentences splits on .!? only — won't catch
    # multi-bullet-header bodies. Filter line-by-line first.
    lines_kept = []
    bullet_header_re = re.compile(r"^\s*[-*]\s+\*\*[^*]+\*\*:?\s*$")
    for line in cleaned.split("\n"):
        if bullet_header_re.match(line):
            continue  # skip bullet-header-only line
        lines_kept.append(line)
    cleaned_no_headers = "\n".join(lines_kept).strip()

    if not cleaned_no_headers:
        # All lines were bullet headers → 0 countable
        return {"pass": True, "reason": "", "short_count": 0, "total": 0}

    sentences = _split_sentences(cleaned_no_headers)
    countable = [s for s in sentences if not _is_bullet_label(s)]

    if not countable:
        return {"pass": True, "reason": "", "short_count": 0, "total": 0}

    short = [s for s in countable if len(s.split()) < _MIN_SENTENCE_WORDS]
    ratio = len(short) / len(countable)

    if ratio > _MAX_SHORT_RATIO:
        return {
            "pass": False,
            "reason": (
                f"Sentence richness fail: {len(short)}/{len(countable)} "
                f"câu <{_MIN_SENTENCE_WORDS} từ ({ratio:.0%} > {_MAX_SHORT_RATIO:.0%}). "
                f"Tail fragments: {[s[:60] for s in short[:3]]}"
            ),
            "short_count": len(short),
            "total": len(countable),
        }
    return {
        "pass": True,
        "reason": "",
        "short_count": len(short),
        "total": len(countable),
    }


# === V5.0 Phase 1.6 — per-format gates ===
# Note: check_title_per_format dropped per V5.1 PATCH — title decisions
# belong to V5.1.8 Master self-title (10 master sector prompts inject Title craft block).

from lib.format_registry import get_format


def check_word_count_per_format(body: str, format_id: str) -> dict[str, Any]:
    """V5.0 Gate 2 — word count must be within format's length_range."""
    cleaned = _clean(body).strip()
    n = len(cleaned.split())
    fmt = get_format(format_id)
    lo, hi = fmt["length_range"]
    if n < lo:
        return {"pass": False, "reason": f"Too short: {n} words (need {lo}-{hi} for {format_id})"}
    if n > hi:
        return {"pass": False, "reason": f"Too long: {n} words (need {lo}-{hi} for {format_id})"}
    return {"pass": True, "reason": ""}


def check_body_pattern_per_format(body: str, format_id: str) -> dict[str, Any]:
    """V5.0 Gate 3 — body structure per format spec."""
    cleaned = _clean(body).strip()
    fmt = get_format(format_id)
    structure = fmt["structure"]
    blocks = [b.strip() for b in re.split(r"\n\s*\n", cleaned) if b.strip()]

    # No '## Cần để ý' allowed in any format
    if re.search(r"^#{2,3}\s+C[ầa]n\s+đ[ểe]?\s+ý", cleaned, flags=re.MULTILINE):
        return {"pass": False, "reason": "Contains '## Cần để ý' section — banned"}

    if structure == "paragraph_only":
        for line in cleaned.split("\n"):
            if line.lstrip().startswith(("- ", "* ")):
                return {"pass": False, "reason": "flash_qa: bullet found, format requires paragraph only"}
        return {"pass": True, "reason": ""}

    if structure in ("opening_bullets_closing", "short_opening_dense_bullets"):
        if len(blocks) < 3:
            return {"pass": False, "reason": f"Need ≥3 blocks (opening + bullets + closing), got {len(blocks)}"}
        opening = blocks[0]
        closing = blocks[-1]
        middle = blocks[1:-1]
        if opening.startswith(("- ", "* ")):
            return {"pass": False, "reason": "Opening must be paragraph, not bullet"}

        opening_words = len(opening.split())
        opening_min = fmt.get("opening_min", 0)
        opening_max = fmt.get("opening_max")
        if opening_words < opening_min:
            return {"pass": False, "reason": f"Opening too short: {opening_words} words (need ≥{opening_min} for {format_id})"}
        if opening_max is not None and opening_words > opening_max:
            return {"pass": False, "reason": f"Opening too long: {opening_words} words (need ≤{opening_max} for {format_id})"}

        if closing.startswith(("- ", "* ")) or closing.startswith("#"):
            return {"pass": False, "reason": "Closing must be sentence, not bullet/heading"}

        bullets: list[str] = []
        for block in middle:
            for line in block.split("\n"):
                line = line.strip()
                if line.startswith(("- ", "* ")):
                    bullets.append(line[2:].strip())
                elif line and bullets:
                    bullets[-1] += " " + line
                elif line:
                    return {"pass": False, "reason": f"Non-bullet text in middle: '{line[:60]}'"}

        b_lo, b_hi = fmt["bullets_count"]
        if not (b_lo <= len(bullets) <= b_hi):
            return {"pass": False, "reason": f"Need {b_lo}-{b_hi} bullets, got {len(bullets)}"}
        bullet_min = fmt["bullet_min_length"]
        for i, b in enumerate(bullets, 1):
            words = len(b.split())
            if words < bullet_min:
                return {"pass": False, "reason": f"Bullet {i} too short: {words} words (need ≥{bullet_min} for {format_id})"}
            if "**" not in b:
                return {"pass": False, "reason": f"Bullet {i} missing bold highlight"}
        return {"pass": True, "reason": ""}

    if structure == "flow_paragraphs":
        if len(blocks) < 2:
            return {"pass": False, "reason": "narrative: need ≥2 paragraphs"}
        opening = blocks[0]
        if opening.startswith(("- ", "* ")):
            return {"pass": False, "reason": "Opening must be paragraph"}
        opening_words = len(opening.split())
        if opening_words < fmt.get("opening_min", 40):
            return {"pass": False, "reason": f"Opening too short: {opening_words} words (need ≥40)"}
        bullet_count = sum(1 for line in cleaned.split("\n") if line.lstrip().startswith(("- ", "* ")))
        b_lo, b_hi = fmt["bullets_count"]
        if bullet_count > b_hi:
            return {"pass": False, "reason": f"narrative: {bullet_count} bullets, max {b_hi} highlights allowed"}
        return {"pass": True, "reason": ""}

    return {"pass": False, "reason": f"Unknown structure: {structure}"}


# ============================================================
# V1.5-lite NEW gates (mechanical bans)
# ============================================================

from lib.voice_rules import HAN_VIET_FORMAL_BAN, NATURALIZED_FINANCE_TERMS


def check_han_viet_formal(body: str) -> dict[str, Any]:
    """V1.5-lite — reject body chứa ≥2 Hán-Việt formal terms.

    User feedback 2026-05-13: "độc bản / hội đủ / tái định giá" reads as
    formal/báo chí, not bình dân. 1 occurrence OK (factual context),
    ≥2 = formal pile-on.

    Substring dedup: if "chưa hội đủ" matches, "hội đủ" inside same span
    doesn't double-count.

    Skeptic section + pipeline log stripped before check.
    """
    cleaned = _clean(body).lower()
    # Sort by length desc so longer phrases match first.
    sorted_terms = sorted(HAN_VIET_FORMAL_BAN.keys(), key=len, reverse=True)
    # Track positions already covered by longer matches → skip shorter substrings.
    covered_ranges: list[tuple[int, int]] = []
    found: list[str] = []
    for term in sorted_terms:
        start = 0
        while True:
            idx = cleaned.find(term, start)
            if idx < 0:
                break
            end = idx + len(term)
            # Skip if overlapping with already-found longer term
            if any(idx >= rs and end <= re_ for rs, re_ in covered_ranges):
                start = end
                continue
            found.append(term)
            covered_ranges.append((idx, end))
            start = end
            break  # only count first occurrence per term
    if len(found) >= 2:
        replacements = {t: HAN_VIET_FORMAL_BAN[t] for t in found}
        return {
            "pass": False,
            "reason": f"Hán-Việt formal pile-on: {len(found)} terms — {replacements}",
            "found_terms": found,
        }
    return {"pass": True, "reason": "", "found_terms": found}


_ABBREV_PATTERN = re.compile(r"\b[A-Z]{3,4}\b")
_ABBREV_EXPANSION_PATTERN = re.compile(r"\(([^)]+)\)")


@lru_cache(maxsize=1)
def _get_ticker_set() -> frozenset[str]:
    """Cached Finpath ticker set. Resolved once per process."""
    try:
        from lib.pipeline_db import PipelineDB
        from lib.finpath_sectors import FinpathSectors
        db = PipelineDB("data/pipeline.db")
        fs = FinpathSectors(db)
        cached = fs.get_all_cached_tickers()
        db.close()
        return frozenset(cached)
    except Exception:
        from lib.ticker_universe import ALL_TICKERS
        return frozenset(ALL_TICKERS)


def _is_ticker(token: str) -> bool:
    """Check token có phải Finpath ticker không (cached lookup)."""
    return token in _get_ticker_set()


def check_abbreviation_expanded(body: str) -> dict[str, Any]:
    """V1.5-lite — 3-4 letter uppercase MUST be expanded on first occurrence
    OR in NATURALIZED_FINANCE_TERMS allowlist OR is a ticker.

    User feedback 2026-05-13: BCA / GRDP / SCIC reader bình dân không hiểu.
    Force "Bộ Công An (BCA)" first mention pattern.

    Returns {pass, missing_expansions: [list of unexpanded abbreviations]}
    """
    cleaned = _clean(body)
    tokens = _ABBREV_PATTERN.findall(cleaned)
    if not tokens:
        return {"pass": True, "reason": "", "missing_expansions": []}

    unique_abbrev = []
    seen = set()
    for tok in tokens:
        if tok in seen:
            continue
        seen.add(tok)
        unique_abbrev.append(tok)

    missing = []
    for abbrev in unique_abbrev:
        if abbrev.lower() in NATURALIZED_FINANCE_TERMS:
            continue
        if _is_ticker(abbrev):
            continue
        first_idx = cleaned.find(abbrev)
        if first_idx < 0:
            continue
        # Look ahead 30 chars for "(<expansion>)" pattern
        window = cleaned[first_idx + len(abbrev):first_idx + len(abbrev) + 30]
        if _ABBREV_EXPANSION_PATTERN.search(window):
            continue
        # Also check "<expansion> (ABBREV)" form — look 50 chars before
        before_window = cleaned[max(0, first_idx - 50):first_idx]
        if before_window.rstrip().endswith("("):
            continue
        missing.append(abbrev)

    if missing:
        return {
            "pass": False,
            "reason": f"Abbreviations not expanded on first mention: {missing}",
            "missing_expansions": missing,
        }
    return {"pass": True, "reason": "", "missing_expansions": []}


def _fetch_current_price(ticker: str) -> float:
    """Fetch current stock price from Finpath API. Helper for testability."""
    from lib.finpath_api import FinpathAPI
    api = FinpathAPI()
    overview = api.get_overview()
    if not isinstance(overview, dict):
        raise ConnectionError("Finpath overview returned non-dict")
    stocks = overview.get("stocks", [])
    for s in stocks:
        if s.get("c") == ticker:
            price = s.get("p")
            if price is not None and price > 0:
                return float(price)
    raise ValueError(f"Ticker {ticker} not in Finpath overview")


# V1.5-lite fix: avoid matching K in magnitude expressions like "35K tỷ" / "10K triệu"
# (used for revenue/margin). Negative lookahead excludes those.
_PRICE_TARGET_RE = re.compile(
    r"(\d+(?:[.,]\d+)?)\s*(?:nghìn(?:/cp|\s*đồng)?|nghìn|k(?!\s*(?:tỷ|triệu))\b)",
    re.IGNORECASE,
)


def check_price_realistic(body: str, ticker: str) -> dict[str, Any]:
    """V1.5-lite — closing price target MUST be within ±50% Finpath current.

    User feedback 2026-05-13: FPT bài closing said 145 nghìn/cp khi thực tế
    ~70 nghìn. Master hallucinated price target.

    Extracts price targets from closing paragraph (last block). Fetches
    current price from Finpath API. Asserts each target within ±50% current.

    Degrades gracefully: if Finpath unavailable, return pass with warning.
    """
    try:
        current = _fetch_current_price(ticker)
    except Exception as e:
        return {
            "pass": True,
            "reason": f"warning: Finpath unavailable — skipped price check ({e})",
            "degraded": True,
        }

    cleaned = _clean(body).strip()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", cleaned) if b.strip()]
    closing = "\n".join(blocks[-2:]) if len(blocks) >= 2 else cleaned

    targets = []
    for m in _PRICE_TARGET_RE.finditer(closing):
        raw = m.group(1).replace(",", ".")
        try:
            val = float(raw) * 1000  # nghìn → đồng
            targets.append(val)
        except ValueError:
            continue

    if not targets:
        return {"pass": True, "reason": "", "current_price": current, "targets_found": []}

    out_of_range = []
    lo = current * 0.5
    hi = current * 1.5
    for t in targets:
        if t < lo or t > hi:
            out_of_range.append(t)

    if out_of_range:
        return {
            "pass": False,
            "reason": (
                f"Price target out of ±50% range — current={current:.0f}đ, "
                f"targets={[int(t) for t in targets]}, "
                f"out_of_range={[int(t) for t in out_of_range]}"
            ),
            "current_price": current,
            "targets_found": targets,
            "out_of_range": out_of_range,
        }
    return {
        "pass": True,
        "reason": "",
        "current_price": current,
        "targets_found": targets,
    }


def check_all_v5(body: str, format_id: str, stance: str, ticker: str = "") -> dict[str, dict[str, Any]]:
    """Run V5.0 + V5.1.2 + V1.4 + V1.5-lite gates (13-14 total).

    V1.5-lite (2026-05-13 PM): DROP check_bao_chi_body (replaced Master prompt).
    ADD check_han_viet_formal + check_abbreviation_expanded + check_price_realistic.

    Universal (11): no_english_jargon, no_metadata_leak, no_hedging, verdict_line,
                    stance_consistency, sentence_density, em_dash_density,
                    bold_density, min_sentence_richness (V1.4),
                    han_viet_formal (V1.5 NEW), abbreviation_expanded (V1.5 NEW).
    Conditional (1): price_realistic (V1.5 NEW — requires ticker).
    Per-format (2): word_count, body_pattern.
    """
    result = {
        "no_english_jargon": check_no_english_jargon(body),
        "no_metadata_leak": check_no_metadata_leak(body),
        "no_hedging": check_no_hedging(body),
        "verdict_line": check_verdict_line(body),
        "stance_consistency": check_stance_consistency(body, stance),
        "sentence_density": check_sentence_density(body),
        "em_dash_density": check_em_dash_density(body),
        "bold_density": check_bold_density(body, format_id),
        "min_sentence_richness": check_min_sentence_richness(body),
        "han_viet_formal": check_han_viet_formal(body),
        "abbreviation_expanded": check_abbreviation_expanded(body),
        "word_count": check_word_count_per_format(body, format_id),
        "body_pattern": check_body_pattern_per_format(body, format_id),
    }
    if ticker:
        result["price_realistic"] = check_price_realistic(body, ticker)
    return result
