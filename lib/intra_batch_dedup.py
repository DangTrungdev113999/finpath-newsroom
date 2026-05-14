"""Intra-batch thesis MERGE within a single /tin batch (V5.1.8 — 2026-05-14).

Problem: Story Editor produces N briefs per batch, each with a
`deep_question_options[]` array. For a single ticker, 2+ briefs sometimes
share the SAME dominant deep_question category (e.g., both `paradox` about
re-rating thesis). Master then writes 2 articles with overlapping thesis.

V5.1.8 fix: instead of dropping losers, MERGE their content into the
strongest winner brief so Master writes 1 enriched article that covers BOTH
sides. Loser briefs marked `absorbed_into_<winner_row_id>` so pipeline
orchestrator skips dispatching them to Master.

Old behavior (V5.1.6, kept as wrapper for backward compat):
`dedup_briefs_in_batch` returns briefs with `dedup_decision ∈ {keep,
drop_dup_thesis}`.

New behavior (V5.1.8):
`merge_briefs_in_batch` returns briefs with `merge_decision ∈ {keep,
merged, absorbed_into_<row_id>}`. Winner brief in a merged group gets
`merged_from_briefs[]` field listing absorbed row_ids + concatenated
`deep_question_options[]` (deduped by question text) + union of
`stance_directive.key_evidence` arrays. Master reads enriched brief and
writes 1 article that uses content from BOTH original briefs.

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
    for c in cats:
        if counts[c] == max_count:
            return c
    return ""  # unreachable


def _brief_strength_signal(brief: dict[str, Any]) -> tuple[int, int, int]:
    """Stronger brief = more options, more total data_trail_preview entries,
    higher summed key_metric_count.
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


def _merge_options_into_winner(
    winner_options: list[dict[str, Any]],
    loser_options: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Concat loser options into winner, dedupe by question text."""
    seen_questions: set[str] = set()
    merged: list[dict[str, Any]] = []
    for opt in winner_options + loser_options:
        if not isinstance(opt, dict):
            continue
        q = (opt.get("question") or opt.get("deep_question") or "").strip()
        if not q:
            merged.append(opt)
            continue
        if q in seen_questions:
            continue
        seen_questions.add(q)
        merged.append(opt)
    return merged


def _union_key_evidence(winner: dict[str, Any], losers: list[dict[str, Any]]) -> list[str]:
    """Collect stance_directive.key_evidence strings from winner + losers, deduped
    preserving first-seen order."""
    out: list[str] = []
    seen: set[str] = set()

    def _collect(brief: dict[str, Any]) -> None:
        # Brief-level stance_directive (V5.0 fallback when picked option lacks it)
        sd = brief.get("stance_directive")
        if isinstance(sd, dict):
            ev = sd.get("key_evidence")
            if isinstance(ev, list):
                for item in ev:
                    s = str(item).strip()
                    if s and s not in seen:
                        out.append(s)
                        seen.add(s)
        # Per-option stance_directive (V5.1.2 — preferred)
        for opt in brief.get("deep_question_options") or []:
            if not isinstance(opt, dict):
                continue
            sd_opt = opt.get("stance_directive")
            if isinstance(sd_opt, dict):
                ev = sd_opt.get("key_evidence")
                if isinstance(ev, list):
                    for item in ev:
                        s = str(item).strip()
                        if s and s not in seen:
                            out.append(s)
                            seen.add(s)

    _collect(winner)
    for loser in losers:
        _collect(loser)
    return out


def merge_briefs_in_batch(briefs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return a deep-copied list with `merge_decision` field added per brief.

    Decisions:
        'keep'                      — singleton, write this article
        'merged'                    — winner of a group; brief enriched with
                                       losers' options + key_evidence; Master
                                       writes 1 article using both
        'absorbed_into_<row_id>'    — loser; Master skips. Pipeline orchestrator
                                       MUST filter rows with master_decision
                                       'reject_dup_thesis' set by Format Director.

    Grouping key: (ticker, dominant_category). Empty dominant_category groups
    are NOT merged (cannot infer thesis overlap → keep all).

    Tie-break inside a group: highest `_brief_strength_signal`, then earliest
    position in the input list.
    """
    result = [deepcopy(b) for b in briefs]

    groups: dict[tuple[str, str], list[int]] = {}
    for i, b in enumerate(result):
        ticker = b.get("ticker") or ""
        dom = compute_dominant_category(b)
        if not dom:
            b["merge_decision"] = "keep"
            continue
        groups.setdefault((ticker, dom), []).append(i)

    for (ticker, dom), indexes in groups.items():
        if len(indexes) == 1:
            result[indexes[0]]["merge_decision"] = "keep"
            continue

        # Pick winner = max strength, tie → earliest position
        winner_idx = max(
            indexes, key=lambda i: (*_brief_strength_signal(result[i]), -i)
        )
        loser_indexes = [i for i in indexes if i != winner_idx]
        loser_briefs = [result[i] for i in loser_indexes]
        winner = result[winner_idx]

        # Enrich winner with loser content
        winner_opts = list(winner.get("deep_question_options") or [])
        loser_opts: list[dict[str, Any]] = []
        for loser in loser_briefs:
            loser_opts.extend(loser.get("deep_question_options") or [])
        merged_opts = _merge_options_into_winner(winner_opts, loser_opts)
        # Cap at 5 to prevent context bloat (V5.1.8 — Master picks 1 anyway)
        winner["deep_question_options"] = merged_opts[:5]

        # Union key_evidence
        winner_evidence = _union_key_evidence(winner, loser_briefs)
        if winner_evidence:
            # Stash into brief-level summary (Master reads from picked option's
            # stance_directive.key_evidence first; this is supplementary).
            winner["merged_key_evidence"] = winner_evidence

        # Audit trail
        winner["merge_decision"] = "merged"
        winner["merged_from_briefs"] = [
            {
                "row_id": result[i].get("row_id") or "",
                "angle_label": result[i].get("angle_label") or "",
                "n_options": len(result[i].get("deep_question_options") or []),
            }
            for i in loser_indexes
        ]

        # Losers: marked absorbed, will be filtered at pipeline Step 4
        winner_row_id = str(winner.get("row_id") or "")
        for i in loser_indexes:
            result[i]["merge_decision"] = f"absorbed_into_{winner_row_id}"

    return result


def dedup_briefs_in_batch(briefs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """V5.1.6 backward-compat wrapper: returns briefs with `dedup_decision` field.

    V5.1.8 behavior change: under the hood this now calls `merge_briefs_in_batch`
    so winners are ENRICHED with loser content. The legacy `dedup_decision` field
    is set to:
        'keep'              — for singletons AND merged winners
        'drop_dup_thesis'   — for losers (absorbed into a winner)

    Callers using the old field name will continue to work; the merge fields
    (`merge_decision`, `merged_from_briefs`, `merged_key_evidence`) are
    additionally available for new callers.
    """
    out = merge_briefs_in_batch(briefs)
    for b in out:
        md = b.get("merge_decision", "keep")
        if md == "keep" or md == "merged":
            b["dedup_decision"] = "keep"
        else:  # absorbed_into_*
            b["dedup_decision"] = "drop_dup_thesis"
    return out
