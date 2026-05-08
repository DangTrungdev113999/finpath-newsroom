"""Notion MCP helpers — block tree → markdown conversion.

Pure functions on already-fetched block dicts. No HTTP calls.
The orchestrator (kb_ingest CLI) consumes blocks from a JSON file.
Notion MCP fetches happen in a Claude Code session before the CLI runs.
"""
from __future__ import annotations
from typing import Any


def render_rich_text(rich_text: list[dict]) -> str:
    """Convert Notion rich_text array to markdown inline string."""
    parts = []
    for span in rich_text:
        text = span.get("plain_text", "")
        ann = span.get("annotations", {})
        href = span.get("href")
        if ann.get("code"):
            text = f"`{text}`"
        if ann.get("bold"):
            text = f"**{text}**"
        if ann.get("italic"):
            text = f"*{text}*"
        if href:
            text = f"[{text}]({href})"
        parts.append(text)
    return "".join(parts)


def render_block(block: dict, children_rendered: str = "") -> str:
    """Convert a single Notion block dict to markdown."""
    btype = block.get("type", "")
    payload = block.get(btype, {})

    if btype == "paragraph":
        text = render_rich_text(payload.get("rich_text", []))
        return f"{text}\n\n" + children_rendered

    if btype == "heading_1":
        text = render_rich_text(payload.get("rich_text", []))
        return f"# {text}\n\n" + children_rendered

    if btype == "heading_2":
        text = render_rich_text(payload.get("rich_text", []))
        return f"## {text}\n\n" + children_rendered

    if btype == "heading_3":
        text = render_rich_text(payload.get("rich_text", []))
        return f"### {text}\n\n" + children_rendered

    if btype == "bulleted_list_item":
        text = render_rich_text(payload.get("rich_text", []))
        nested = "\n".join(f"  {line}" for line in children_rendered.splitlines() if line)
        return f"- {text}\n" + (f"{nested}\n" if nested else "")

    if btype == "numbered_list_item":
        text = render_rich_text(payload.get("rich_text", []))
        return f"1. {text}\n"

    if btype == "quote":
        text = render_rich_text(payload.get("rich_text", []))
        return f"> {text}\n\n"

    if btype == "code":
        text = render_rich_text(payload.get("rich_text", []))
        lang = payload.get("language", "")
        return f"```{lang}\n{text}\n```\n\n"

    if btype == "callout":
        text = render_rich_text(payload.get("rich_text", []))
        emoji = payload.get("icon", {}).get("emoji", "")
        return f"> {emoji} {text}\n\n" + children_rendered

    if btype == "toggle":
        summary = render_rich_text(payload.get("rich_text", []))
        return f"<details><summary>{summary}</summary>\n\n{children_rendered}</details>\n\n"

    if btype == "divider":
        return "---\n\n"

    if btype == "child_page":
        title = payload.get("title", "")
        return f"[{title}]\n\n"

    if btype == "column_list" or btype == "column":
        return children_rendered

    return ""


def slugify(text: str, max_len: int = 60) -> str:
    """Convert title to URL-safe slug for filenames."""
    import re
    import unicodedata

    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:max_len] or "untitled"
