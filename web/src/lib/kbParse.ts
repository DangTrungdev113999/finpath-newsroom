import GithubSlugger from 'github-slugger';
import type { KbHeading, KbMeta } from './kbTypes';

// Parse YAML frontmatter from a raw markdown string. Handles flat key:value
// pairs and JSON array values like `applies_to: ["VHM", "NVL"]`.
// KB frontmatter is intentionally flat — no nesting needed, so no js-yaml dep.
export function parseFrontmatter(raw: string): { meta: KbMeta; body: string } {
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!m) return { meta: {}, body: raw };

  const meta: KbMeta = {};
  for (const rawLine of m[1].split(/\r?\n/)) {
    const kv = rawLine.match(/^(\w+):\s*(.*)$/);
    if (!kv) continue;
    const [, key, val] = kv;
    if (val.startsWith('[') && val.endsWith(']')) {
      try {
        meta[key] = JSON.parse(val);
        continue;
      } catch {
        // fall through to string assign
      }
    }
    meta[key] = val.replace(/^["']|["']$/g, '');
  }
  return { meta, body: m[2] };
}

// Extract H2 and H3 headings from a markdown body. Each heading gets the
// same slug that rehype-slug will emit as id="..." on the rendered DOM,
// so search results can scroll to anchors reliably.
export function extractHeadings(body: string): KbHeading[] {
  const slugger = new GithubSlugger();
  const headings: KbHeading[] = [];
  const re = /^(#{2,3})\s+(.+)$/gm;
  let match: RegExpExecArray | null;
  while ((match = re.exec(body)) !== null) {
    const level = match[1].length as 2 | 3;
    const text = match[2].trim();
    headings.push({ level, text, slug: slugger.slug(text) });
  }
  return headings;
}

// Slugify a single heading text using github-slugger. Fresh slugger per call
// so dup-text suffix counters do not leak across calls.
export function slugify(text: string): string {
  const slugger = new GithubSlugger();
  return slugger.slug(text);
}
