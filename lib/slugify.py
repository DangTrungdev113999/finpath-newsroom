"""Slugify Vietnamese hook titles to URL-safe slugs (max 60 chars)."""
from __future__ import annotations
import re
import unicodedata


def slugify_hook(text: str, max_len: int = 60) -> str:
    """Convert Vietnamese title hook to URL-safe slug.

    Rules:
    - Lowercase
    - Strip Vietnamese diacritics (NFKD + drop combining)
    - Replace non-alphanumeric with hyphen
    - Collapse consecutive hyphens
    - Trim leading/trailing hyphens
    - Truncate to max_len chars
    - Drop trailing partial word after truncate (split by - and drop last fragment if cut mid-word)
    - Empty result → "untitled"
    """
    if not text:
        return "untitled"

    # Strip diacritics via NFKD decomposition
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    # Vietnamese-specific: đ/Đ don't decompose via NFKD, handle explicitly
    text = text.replace("đ", "d").replace("Đ", "d")
    text = text.lower()
    # Replace non-alphanumeric runs with a single hyphen
    text = re.sub(r"[^a-z0-9]+", "-", text)
    # Collapse consecutive hyphens and trim leading/trailing
    text = re.sub(r"-+", "-", text).strip("-")

    if not text:
        return "untitled"

    if len(text) <= max_len:
        return text

    # Truncate + drop partial trailing word
    truncated = text[:max_len]
    # Check if we cut mid-word (next char after cutoff is not a hyphen)
    next_char = text[max_len:max_len + 1]
    if next_char and next_char != "-" and "-" in truncated:
        # Drop the last incomplete word fragment
        truncated = truncated.rsplit("-", 1)[0]
    truncated = truncated.rstrip("-")
    return truncated or "untitled"
