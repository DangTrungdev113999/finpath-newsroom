"""KB ingest — convert Notion Bank Sector page tree (JSON dump) to markdown files.

Workflow:
  1. Claude session fetches Notion blocks via mcp__notion__API-get-block-children
     (recursive), saves the tree as JSON.
  2. Run: python lib/kb_ingest.py <tree.json> <output_dir>
  3. Script renders each KB topic as a markdown file with frontmatter.

Tree JSON format:
  {
    "pages": [
      {
        "id": "<uuid>",
        "title": "<title>",
        "url": "<notion url>",
        "category": "frameworks|trends|history|per-ticker|uncategorized",
        "blocks": [<block dict with optional 'children' key>, ...]
      }
    ]
  }
"""
from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from lib.notion_fetch import render_block, slugify
except ModuleNotFoundError:
    import sys as _sys
    from pathlib import Path as _Path
    _sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))
    from lib.notion_fetch import render_block, slugify


def render_blocks_recursive(blocks: list[dict]) -> str:
    """Render a flat list of blocks (with optional 'children' key) into markdown."""
    out = []
    for blk in blocks:
        children = blk.get("children", [])
        children_md = render_blocks_recursive(children) if children else ""
        out.append(render_block(blk, children_md))
    return "".join(out)


def write_kb_page(page: dict, output_dir: Path) -> Path:
    """Write a single KB page to output_dir/<category>/<slug>.md."""
    category = page.get("category", "uncategorized")
    title = page.get("title", "Untitled")
    slug = slugify(title)
    cat_dir = output_dir / category
    cat_dir.mkdir(parents=True, exist_ok=True)
    file_path = cat_dir / f"{slug}.md"

    body_md = render_blocks_recursive(page.get("blocks", []))

    fm_lines = [
        "---",
        f'notion_page_id: "{page["id"]}"',
        f'source_url: "{page.get("url", "")}"',
        f'last_synced: {datetime.now(timezone.utc).isoformat()}',
        f'category: {category}',
        f'title: "{title.replace(chr(34), chr(92) + chr(34))}"',
        "---",
        "",
    ]
    file_path.write_text("\n".join(fm_lines) + body_md, encoding="utf-8")
    return file_path


def ingest(tree_json_path: Path, output_dir: Path) -> dict:
    data = json.loads(tree_json_path.read_text(encoding="utf-8"))
    pages = data.get("pages", [])
    written = []
    errors = []
    for page in pages:
        try:
            path = write_kb_page(page, output_dir)
            written.append(str(path))
        except Exception as e:
            errors.append({"page_id": page.get("id"), "error": str(e)})
    return {"written": written, "errors": errors, "count": len(written)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tree_json", type=Path, help="Path to JSON file with Notion block tree")
    parser.add_argument("output_dir", type=Path, default=Path("kb/bank/"), nargs="?")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    if not args.tree_json.exists():
        print(f"Error: {args.tree_json} not found", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)
    result = ingest(args.tree_json, args.output_dir)
    print(json.dumps(result, indent=2))
    return 0 if not result["errors"] else 2


if __name__ == "__main__":
    sys.exit(main())
