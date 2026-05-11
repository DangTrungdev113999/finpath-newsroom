"""KB BĐS validator — enforces 5 hard rules per design spec 2026-05-11.

Usage:
  from lib.kb_bds_validator import validate_kb_file
  violations = validate_kb_file(Path("kb/bds/frameworks/bds-res-presales-backlog.md"))
  if violations:
      for v in violations:
          print(f"  ✗ {v}")

Rules enforced (machine-checkable subset of design Section 5):
  - 5.5 Pitfall section has ≥ 2 bullet items
  - Structural: required sections present (Khái niệm, Pitfalls, Source log)
  - Frontmatter: applies_to field with valid enum values

Rules NOT machine-checked (require manual review):
  - 5.1 Static-only (no anchor data Q1/2026) — too fuzzy, manual review
  - 5.2 0% English jargon — too many edge cases (proper nouns, code blocks), manual grep
  - 5.3 Case study 3-label format — varies by file, manual verify
  - 5.4 Source log URL validity — manual verify
"""
from __future__ import annotations

import re
from pathlib import Path

VALID_APPLIES_TO = {
    "residential",
    "kcn",
    "retail",
    "office",
    "resort",
    "data_center",
    "all",
}

REQUIRED_SECTIONS = [
    "## Khái niệm",
    "## Pitfalls",
    "## Source log",
]


def _extract_frontmatter(text: str) -> str | None:
    m = re.match(r"^---\n([\s\S]*?)\n---\n", text)
    return m.group(1) if m else None


def _extract_applies_to(fm: str) -> list[str] | None:
    """Parse applies_to: ["x", "y"] line from frontmatter."""
    m = re.search(r'^applies_to:\s*\[(.*?)\]\s*$', fm, re.MULTILINE)
    if not m:
        return None
    raw = m.group(1)
    values = [v.strip().strip('"').strip("'") for v in raw.split(",")]
    return [v for v in values if v]


def _count_pitfall_items(text: str) -> int:
    """Count bullet items inside ## Pitfalls section (until next ## heading)."""
    m = re.search(r"## Pitfalls[^\n]*\n([\s\S]*?)(?=\n## |\Z)", text)
    if not m:
        return 0
    section = m.group(1)
    bullets = re.findall(r"^\s*[-*]\s+", section, re.MULTILINE)
    numbered = re.findall(r"^\s*\d+\.\s+", section, re.MULTILINE)
    return len(bullets) + len(numbered)


def validate_kb_file(path: Path) -> list[str]:
    """Return list of violation strings. Empty list = file passes validator.

    Raises FileNotFoundError if path does not exist.
    """
    text = path.read_text(encoding="utf-8")
    violations: list[str] = []

    fm = _extract_frontmatter(text)
    if fm is None:
        violations.append("Missing frontmatter block")
    else:
        applies = _extract_applies_to(fm)
        if applies is None:
            violations.append("Missing applies_to field in frontmatter")
        elif not applies:
            violations.append("applies_to is empty list")
        else:
            for v in applies:
                if v not in VALID_APPLIES_TO:
                    violations.append(
                        f"applies_to has invalid value '{v}' "
                        f"(allowed: {sorted(VALID_APPLIES_TO)})"
                    )

    for section in REQUIRED_SECTIONS:
        if section not in text:
            violations.append(f"Missing required section: {section}")

    pitfall_count = _count_pitfall_items(text)
    if pitfall_count < 2:
        violations.append(
            f"Pitfall section has {pitfall_count} bullets (require ≥ 2)"
        )

    return violations
