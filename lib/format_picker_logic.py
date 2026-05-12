"""Format picker logic — 5-step deterministic flow.

Exposed as Python helper so Format Director agent can reference + so logic
is testable independently. Agent prompt mirrors this logic but Python
exposes it for code-level fallback / testing / future Format Director swap.
"""
from __future__ import annotations
import re
from typing import Any

from lib.format_registry import load_registry, get_candidates_for_category, FORMAT_IDS

TIMELINE_MARKER_RE = re.compile(
    r"(Q[1-4]/?\d{0,4}|năm \d{4}|tháng \d{1,2}|cuối năm|đầu năm|"
    r"\d{4}|hồi \d{4})",
    re.IGNORECASE,
)


def _count_timeline_markers(text: str) -> int:
    return len(TIMELINE_MARKER_RE.findall(text or ""))


def _format_reason_template(category: str, candidates: list[str], chosen: str, extra: str = "") -> str:
    base = f"Category={category} → candidates={candidates}. Picked={chosen}."
    if extra:
        return f"{base} {extra}"
    return base


def pick_format_for_option(option: dict, market_data: dict | None) -> dict[str, Any]:
    """Run 5-step flow on 1 deep_question_option.

    Args:
      option: {category, narrative_setup, data_trail_preview, key_metric_count}
      market_data: {pct_change_today, ...} or None

    Returns:
      {format_id, format_reason, tone_bias, length_target}
    """
    category = option.get("category", "")
    narrative = option.get("narrative_setup", "")
    data_preview = option.get("data_trail_preview") or []
    key_metric_count = option.get("key_metric_count", 0)

    # Step 1 — category → candidates
    candidates = get_candidates_for_category(category)
    if not candidates:
        chosen = "flash_qa"
        extra = f"No candidates for category={category!r}, fallback flash_qa."
    elif len(candidates) == 1:
        chosen = candidates[0]
        extra = ""
    else:
        # Step 2 — tie-break (hidden_mechanism: 2 candidates)
        n_markers = _count_timeline_markers(narrative)
        if n_markers >= 3 and "standard_narrative" in candidates:
            chosen = "standard_narrative"
            extra = f"Tie-break: {n_markers} timeline markers → narrative."
        else:
            chosen = "standard_qa"
            extra = f"Tie-break: {n_markers} timeline markers (<3) → qa."

    # Step 3 — length downgrade for shallow data
    n_sources = len(data_preview)
    if n_sources <= 2 and key_metric_count <= 1 and chosen.startswith("standard_"):
        chosen_old = chosen
        chosen = "flash_qa"
        extra += f" Downgrade {chosen_old}→flash_qa (sources={n_sources}, metrics={key_metric_count})."

    # Step 4 — tone bias from market mood
    tone_bias = "neutral"
    if market_data:
        pct = market_data.get("pct_change_today", 0)
        if pct <= -3.0:
            tone_bias = "acknowledge_market_red"
        elif pct >= 3.0:
            tone_bias = "acknowledge_market_green"

    # Step 5 — length target from registry
    reg = load_registry()
    length_target = reg[chosen]["length_target"]

    format_reason = _format_reason_template(category, candidates or ["fallback"], chosen, extra=extra.strip())

    return {
        "format_id": chosen,
        "format_reason": format_reason,
        "tone_bias": tone_bias,
        "length_target": length_target,
    }
