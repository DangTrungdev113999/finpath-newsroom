"""Format Registry V5.0 — loader for data/format_registry.yaml.

Source of truth for 4 Master article formats. Story Editor + Format Director
read this; Master applies per-format pattern + per-format gate check.
"""
from __future__ import annotations
import yaml
from functools import lru_cache
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "data" / "format_registry.yaml"

FORMAT_IDS = ["flash_qa", "standard_qa", "standard_listicle", "standard_narrative"]


@lru_cache(maxsize=1)
def load_registry() -> dict[str, dict[str, Any]]:
    """Load format_registry.yaml. Cached after first call (file is static)."""
    raw = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    return raw["formats"]


def get_format(format_id: str) -> dict[str, Any]:
    """Return single format spec by ID. Raises KeyError if unknown."""
    reg = load_registry()
    if format_id not in reg:
        raise KeyError(f"Unknown format_id: {format_id!r} (valid: {list(reg.keys())})")
    return reg[format_id]


def get_candidates_for_category(category: str) -> list[str]:
    """Filter formats whose `trigger_categories` contains the given category.

    Returns format_ids in catalog order. Empty list if no matches.
    """
    reg = load_registry()
    return [fid for fid, spec in reg.items() if category in spec.get("trigger_categories", [])]
