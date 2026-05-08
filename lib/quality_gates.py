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
    "llr", "cof", "tpdn", "yoy", "qoq", "ytd", "roe", "roa",
    "basel",
    # Common English finance/news words
    "trade-off", "tradeoff", "anchor", "relevant", "confirm", "pattern",
    "breaking", "momentum", "defensive", "catalyst", "symbolic", "metric",
    "event", "story", "scenario", "target", "portfolio", "buffer",
    "stress test", "arithmetic", "coverage", "opportunity cost",
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
