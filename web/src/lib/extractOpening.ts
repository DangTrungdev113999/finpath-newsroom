/**
 * Extract a 3-line opening preview from a raw markdown body for use in
 * ArticleCard underneath the title. The body comes in 4 format-pattern
 * shapes (flash_qa / standard_qa / standard_listicle / standard_narrative)
 * — in all four the opening is the FIRST non-empty prose paragraph before
 * the bullets begin (or the whole body for flash_qa). We walk lines until
 * we hit a bullet, strip inline markdown syntax (bold / italic / code /
 * link), and cap at `maxChars`. `line-clamp-3` on the receiving element
 * handles the visible 3-line truncation + ellipsis.
 *
 * Edge case: V5.0 Skeptic section "## Góc nhìn ngược" is appended after
 * the master body — we cut at the first level-2 heading so it never bleeds
 * into the preview.
 */
export function extractOpening(markdown: string, maxChars = 260): string {
  if (!markdown) return '';

  // Drop everything from the first `##` (Skeptic appendix etc.) onward.
  const beforeAppendix = markdown.split(/^##\s/m)[0] ?? markdown;

  const lines = beforeAppendix.trim().split('\n');
  const prose: string[] = [];
  for (const raw of lines) {
    const t = raw.trim();
    if (!t) {
      if (prose.length > 0) break; // blank line ends the opening paragraph
      continue;
    }
    if (/^#+\s/.test(t)) continue; // heading — skip
    if (/^[-*+]\s/.test(t)) break; // bullet — opening over
    if (/^>\s/.test(t)) continue; // blockquote — skip
    prose.push(t);
    if (prose.join(' ').length >= maxChars) break;
  }

  let combined = prose.join(' ');

  // Strip inline markdown syntax — keep the visible text only.
  combined = combined
    .replace(/!\[[^\]]*\]\([^)]+\)/g, '') // images
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // links
    .replace(/\*\*([^*]+)\*\*/g, '$1') // bold
    .replace(/__([^_]+)__/g, '$1') // bold alt
    .replace(/(?<!\*)\*([^*\n]+)\*(?!\*)/g, '$1') // italic
    .replace(/_([^_\n]+)_/g, '$1') // italic alt
    .replace(/`([^`]+)`/g, '$1') // inline code
    .replace(/\s{2,}/g, ' ')
    .trim();

  return combined.slice(0, maxChars).trim();
}
