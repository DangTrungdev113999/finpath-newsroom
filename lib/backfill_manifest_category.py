"""Backfill `category` (5 deep_question categories) into manifest entries.

Reads `output/compare-feed/<id>.md` frontmatter for each article in
`output/compare-feed/manifest.json` and writes back the chosen question's
category into the entry. Idempotent — safe to re-run.

Run: python lib/backfill_manifest_category.py
"""

from __future__ import annotations
import json
from pathlib import Path

import yaml


COMPARE_FEED = Path(__file__).resolve().parent.parent / "output" / "compare-feed"
MANIFEST = COMPARE_FEED / "manifest.json"


def _extract_category(md_path: Path) -> str | None:
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    fm_end = text.find("\n---\n", 4)
    if fm_end == -1:
        return None
    try:
        fm = yaml.safe_load(text[4:fm_end])
    except yaml.YAMLError:
        return None
    options = fm.get("deep_question_options") or []
    idx = fm.get("chosen_question_idx", 0)
    if isinstance(idx, int) and 0 <= idx < len(options):
        cat = options[idx].get("category")
        return str(cat) if cat else None
    return None


def main() -> int:
    if not MANIFEST.exists():
        print(f"Manifest not found: {MANIFEST}")
        return 1

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    articles = data.get("articles") or []
    updated = 0
    missing_md = 0
    for entry in articles:
        md_path = COMPARE_FEED / f"{entry['id']}.md"
        if not md_path.exists():
            missing_md += 1
            continue
        category = _extract_category(md_path)
        if category and entry.get("category") != category:
            entry["category"] = category
            updated += 1

    MANIFEST.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Total: {len(articles)} · updated: {updated} · missing .md: {missing_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
