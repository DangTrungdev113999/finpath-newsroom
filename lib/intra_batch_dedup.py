"""Inter-brief thesis dedup within a single /tin batch.

Problem: Story Editor produces N briefs per batch, each with a
`deep_question_options[]` array. For a single ticker, 2+ briefs sometimes
share the SAME dominant deep_question category (e.g., both `paradox` about
re-rating thesis). Master then writes 2 articles with overlapping thesis.

Fix: after Story Editor (Step 3) and before Master (Step 4), group briefs by
(ticker, dominant_category). For groups with >1 brief, pick the strongest
brief and mark the rest as `drop_dup_thesis`. Master reads the flag and
exits early, recording `master_decision='reject_dup_thesis'`.

Pure deterministic — no LLM. Safe to call from Format Director step 3.5.
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from typing import Any


def compute_dominant_category(brief: dict[str, Any]) -> str:
    """Return the dominant deep_question category for a brief.

    Algorithm: most frequent `category` across deep_question_options.
    Tie-break: the category appearing FIRST in the options list (matches the
    Story Editor preference order — option[0] is typically Master's default
    pick).
    Returns '' when options absent or all options lack a category.
    """
    options = brief.get("deep_question_options") or []
    if not isinstance(options, list):
        return ""
    cats: list[str] = []
    for opt in options:
        if isinstance(opt, dict):
            c = opt.get("category")
            if isinstance(c, str) and c:
                cats.append(c)
    if not cats:
        return ""
    counts = Counter(cats)
    max_count = max(counts.values())
    # Preserve insertion order for tie-break (first occurrence wins).
    for c in cats:
        if counts[c] == max_count:
            return c
    return ""  # unreachable but keeps type-checker calm


def _brief_strength_signal(brief: dict[str, Any]) -> tuple[int, int, int]:
    """Stronger brief = more options, more total data_trail_preview entries,
    higher summed key_metric_count. Used to pick the winner inside a group.
    Tuple is ordered for direct max() comparison.
    """
    options = brief.get("deep_question_options") or []
    if not isinstance(options, list):
        return (0, 0, 0)
    n_opts = len(options)
    total_trail = 0
    total_metrics = 0
    for opt in options:
        if not isinstance(opt, dict):
            continue
        trail = opt.get("data_trail_preview") or []
        if isinstance(trail, list):
            total_trail += len(trail)
        metrics = opt.get("key_metric_count")
        if isinstance(metrics, int):
            total_metrics += metrics
    return (n_opts, total_trail, total_metrics)


def dedup_briefs_in_batch(briefs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return a deep-copied list with `dedup_decision` field added per brief.

    Values:
        'keep'              — write this article
        'drop_dup_thesis'   — Master must skip; another brief in the same
                              batch covers the same ticker + dominant_category

    Grouping key: (ticker, dominant_category). Empty dominant_category groups
    are NOT deduped (cannot infer thesis overlap → keep all).
    Tie-break inside a group: highest `_brief_strength_signal`, then earliest
    position in the input list.
    """
    result = [deepcopy(b) for b in briefs]

    groups: dict[tuple[str, str], list[int]] = {}
    for i, b in enumerate(result):
        ticker = b.get("ticker") or ""
        dom = compute_dominant_category(b)
        if not dom:
            b["dedup_decision"] = "keep"
            continue
        groups.setdefault((ticker, dom), []).append(i)

    for (ticker, dom), indexes in groups.items():
        if len(indexes) == 1:
            result[indexes[0]]["dedup_decision"] = "keep"
            continue
        # Pick winner = max (signal, -position). Negative position so earlier
        # wins on full tie (max prefers later by default).
        winner_idx = max(indexes, key=lambda i: (*_brief_strength_signal(result[i]), -i))
        for i in indexes:
            result[i]["dedup_decision"] = "keep" if i == winner_idx else "drop_dup_thesis"

    return result
