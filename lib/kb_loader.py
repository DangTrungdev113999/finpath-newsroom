"""KB runtime loader — read kb/bank/ markdown files (no Notion calls).

Usage:
  loader = KBLoader(Path("kb/bank/"))
  matches = loader.search(["NPL", "Basel"])
  body = loader.load_topic(matches[0]["path"])
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Any


class KBLoader:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def _all_files(self) -> list[Path]:
        if not self.root.exists():
            return []
        return list(self.root.rglob("*.md"))

    @staticmethod
    def _extract_frontmatter(text: str) -> dict[str, str]:
        m = re.match(r"^---\n([\s\S]*?)\n---\n", text)
        if not m:
            return {}
        fm: dict[str, str] = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip().strip('"')
        return fm

    def search(self, keywords: list[str], category: str | None = None) -> list[dict[str, Any]]:
        """Return KB files matching ALL keywords (case-insensitive).

        Optionally filter by category. Sorted by total keyword hit count desc.
        """
        if not keywords:
            return []
        keywords_lc = [k.lower() for k in keywords]
        results: list[dict[str, Any]] = []
        for path in self._all_files():
            text = path.read_text(encoding="utf-8")
            text_lc = text.lower()
            if not all(k in text_lc for k in keywords_lc):
                continue
            fm = self._extract_frontmatter(text)
            cat = fm.get("category", path.parent.name)
            if category and cat != category:
                continue
            relpath = str(path.relative_to(self.root))
            score = sum(text_lc.count(k) for k in keywords_lc)
            # Snippet = first paragraph after frontmatter (best effort)
            body = re.sub(r"^---\n[\s\S]*?\n---\n", "", text, count=1).lstrip()
            snippet_end = body.find("\n\n")
            snippet = body[:snippet_end if snippet_end != -1 else 200][:200]
            results.append({
                "path": relpath,
                "title": fm.get("title", path.stem),
                "category": cat,
                "score": score,
                "snippet": snippet,
            })
        results.sort(key=lambda r: r["score"], reverse=True)
        return results

    def load_topic(self, relative_path: str) -> str:
        full = self.root / relative_path
        if not full.exists():
            raise FileNotFoundError(f"KB topic not found: {relative_path}")
        return full.read_text(encoding="utf-8")
