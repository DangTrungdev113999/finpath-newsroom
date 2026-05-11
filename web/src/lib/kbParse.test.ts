import { describe, expect, it } from 'vitest';
import { parseFrontmatter, extractHeadings, slugify } from './kbParse';

describe('parseFrontmatter', () => {
  it('parses flat key:value frontmatter', () => {
    const raw = `---
category: frameworks
title: "Bank-NIM-Cycle"
last_updated: 2026-05-11
---
# Body heading

Body content here.`;
    const { meta, body } = parseFrontmatter(raw);
    expect(meta.category).toBe('frameworks');
    expect(meta.title).toBe('Bank-NIM-Cycle');
    expect(meta.last_updated).toBe('2026-05-11');
    expect(body).toBe('# Body heading\n\nBody content here.');
  });

  it('parses array values via JSON.parse', () => {
    const raw = `---
applies_to: ["VHM", "NVL", "KDH"]
---
body`;
    const { meta } = parseFrontmatter(raw);
    expect(meta.applies_to).toEqual(['VHM', 'NVL', 'KDH']);
  });

  it('handles ["all"] special array', () => {
    const raw = `---
applies_to: ["all"]
---
body`;
    const { meta } = parseFrontmatter(raw);
    expect(meta.applies_to).toEqual(['all']);
  });

  it('strips quotes from string values', () => {
    const raw = `---
title: 'single quoted'
notion_page_id: "abc-123"
---
body`;
    const { meta } = parseFrontmatter(raw);
    expect(meta.title).toBe('single quoted');
    expect(meta.notion_page_id).toBe('abc-123');
  });

  it('returns empty meta + full body when no frontmatter', () => {
    const raw = 'no frontmatter\n\njust body';
    const { meta, body } = parseFrontmatter(raw);
    expect(meta).toEqual({});
    expect(body).toBe(raw);
  });
});

describe('extractHeadings', () => {
  it('extracts H2 and H3 with level + text + slug', () => {
    const body = `# Top H1 ignored

## Section A

### A.1 Sub

## Section B`;
    const headings = extractHeadings(body);
    expect(headings.length).toBe(3);
    expect(headings[0]).toMatchObject({ level: 2, text: 'Section A' });
    expect(headings[1]).toMatchObject({ level: 3, text: 'A.1 Sub' });
    expect(headings[2]).toMatchObject({ level: 2, text: 'Section B' });
    expect(headings[0].slug).toBeTruthy();
  });

  it('skips H1 and H4+', () => {
    const body = `# H1
## H2 only
#### H4 skipped`;
    const headings = extractHeadings(body);
    expect(headings.length).toBe(1);
    expect(headings[0].text).toBe('H2 only');
  });

  it('returns empty array when no H2/H3', () => {
    expect(extractHeadings('plain text only')).toEqual([]);
  });
});

describe('slugify — same output as github-slugger', () => {
  it('produces lowercase hyphen-separated slugs', () => {
    expect(slugify('Plain English')).toBe('plain-english');
    expect(slugify('Multiple  Spaces')).toBe('multiple--spaces');
    const viet = slugify('Lớp 1: Hiểu ngành');
    expect(viet.length).toBeGreaterThan(0);
    expect(viet).toBe(viet.toLowerCase());
    expect(viet).not.toMatch(/\s/);
  });
});
