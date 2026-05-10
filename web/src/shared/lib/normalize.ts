/**
 * normalizeSearch — strip Vietnamese diacritics + lowercase for search-token
 * matching. Unlike `slugify`, this does NOT collapse whitespace or drop other
 * characters — it preserves spaces so phrase matches still work.
 *
 *   "Áo dài" → "ao dai"
 *   "Đà Nẵng" → "da nang"
 *
 * Cheap (single normalize pass + regex replace). Safe to call per-keystroke
 * when filtering 1000-item lists.
 */
export function normalizeSearch(raw: string): string {
  return raw
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/g, "d");
}

/** True if `haystack` contains all whitespace-separated tokens from `needle`. */
export function matchesTokens(haystack: string, needle: string): boolean {
  const q = normalizeSearch(needle).trim();
  if (q.length === 0) return true;
  const hay = normalizeSearch(haystack);
  const tokens = q.split(/\s+/);
  for (const tok of tokens) {
    if (!hay.includes(tok)) return false;
  }
  return true;
}
