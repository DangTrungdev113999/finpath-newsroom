"""Extract central thesis from Story Editor brief — V4.0/V5.0/empty handler.

Headline Craft V1.6 anchor source. Returns semantic seed for the Headline
agent to craft a title around, not a literal template.

Priority order:
1. V5.0 brief.deep_question_options[picked_idx].(question|deep_question)
2. V4.0 brief.insight_hypothesis (first sentence ≤200 chars)
3. body opening (until first period or newline) — markdown stripped
4. empty
"""
from __future__ import annotations

import json
import re
from typing import Any

_MAX_INSIGHT_LEN = 200
_MAX_BODY_LEN = 200

# Strip markdown bold/italic/links and bullet markers from body opening
_MD_STRIP_RE = re.compile(r"(\*{1,3}|_{1,3}|`+|\[|\]\([^)]+\))")
_BULLET_RE = re.compile(r"^\s*[-*]\s*")


def extract_central_thesis(
    brief_json: str | dict | None,
    body: str = "",
    picked_idx: int = 0,
) -> dict[str, str]:
    """Return central thesis with source provenance.

    Args:
        brief_json: Story Editor brief — JSON string OR dict OR empty.
        body: Master final body (markdown). Used as fallback when brief absent.
        picked_idx: Which deep_question option Master selected (V5.0 schema).

    Returns:
        {"thesis": str, "source": "v5_deep_question"|"v4_insight"|"body_opening"|"empty"}
    """
    brief = _coerce_brief(brief_json)

    v5_thesis = _try_v5(brief, picked_idx)
    if v5_thesis:
        return {"thesis": v5_thesis, "source": "v5_deep_question"}

    v4_thesis = _try_v4(brief)
    if v4_thesis:
        return {"thesis": v4_thesis, "source": "v4_insight"}

    body_thesis = _try_body_opening(body)
    if body_thesis:
        return {"thesis": body_thesis, "source": "body_opening"}

    return {"thesis": "", "source": "empty"}


def _coerce_brief(brief_json: str | dict | None) -> dict[str, Any]:
    if brief_json is None:
        return {}
    if isinstance(brief_json, dict):
        return brief_json
    if isinstance(brief_json, str):
        s = brief_json.strip()
        if not s:
            return {}
        try:
            parsed = json.loads(s)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _try_v5(brief: dict[str, Any], picked_idx: int) -> str:
    opts = brief.get("deep_question_options")
    if not isinstance(opts, list) or not opts:
        return ""
    # Out-of-range → fall back to idx 0; if still bad, return empty.
    if picked_idx < 0 or picked_idx >= len(opts):
        picked_idx = 0
    opt = opts[picked_idx]
    if not isinstance(opt, dict):
        return ""
    return str(opt.get("question") or opt.get("deep_question") or "").strip()


def _try_v4(brief: dict[str, Any]) -> str:
    raw = brief.get("insight_hypothesis")
    if not isinstance(raw, str) or not raw.strip():
        return ""
    first = _first_sentence(raw)
    return first[:_MAX_INSIGHT_LEN].rstrip()


def _try_body_opening(body: str) -> str:
    if not body or not body.strip():
        return ""
    # First non-empty, non-bullet line
    for line in body.split("\n"):
        line = _BULLET_RE.sub("", line).strip()
        if not line:
            continue
        first = _first_sentence(line)
        cleaned = _strip_markdown(first)
        if cleaned:
            return cleaned[:_MAX_BODY_LEN].rstrip()
    return ""


def _first_sentence(text: str) -> str:
    # Split on period/exclaim/question (with optional space)
    parts = re.split(r"(?<=[.?!])\s+", text.strip(), maxsplit=1)
    return parts[0] if parts else text


def _strip_markdown(text: str) -> str:
    cleaned = _MD_STRIP_RE.sub("", text)
    # Collapse leftover whitespace
    return re.sub(r"\s+", " ", cleaned).strip()
