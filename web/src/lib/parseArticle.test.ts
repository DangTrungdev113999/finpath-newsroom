import { describe, it, expect } from 'vitest';
import { parseArticle } from './parseArticle';

const SAMPLE = `---
title: "VCB quý I"
ticker: VCB
sector: Bank
sector_icon: "🏦"
crawled_at: 2026-05-08T15:30:00+07:00
funnel_batch_id: VCB-20260508-1530
left_meta:
  author: "Chuyên gia ngân hàng"
  word_count: 354
  key_view: "thận trọng"
  skeptic_verdict: "pass_with_caveats"
  pipeline_version: "V3.6"
  format_check: "0% Anh + 400 hard cap"
right_source:
  name: "Báo Pháp luật"
  url: "https://example.com/article"
  published: 2026-05-07
  raw_title: "Vietcombank Q1"
insight: "Phù hợp NĐT giá trị giữ trên 12 tháng."
why_chosen: []
crawl_funnel:
  picked: []
  rejected_editor_v1: []
  rejected_story_editor: []
  rejected_master: []
pipeline_log: {}
---

<!-- left -->

Lợi nhuận quý I/2026 đạt **11.803 tỷ đồng**.

## Cần để ý

caveat narrative.

<!-- right -->

Raw text gốc full body.
`;

describe('parseArticle', () => {
  it('extracts frontmatter into meta', () => {
    const article = parseArticle('VCB-20260508-1530', SAMPLE);
    expect(article.id).toBe('VCB-20260508-1530');
    expect(article.meta.ticker).toBe('VCB');
    expect(article.meta.sector_icon).toBe('🏦');
    expect(article.meta.left_meta.word_count).toBe(354);
    expect(article.meta.right_source.name).toBe('Báo Pháp luật');
  });

  it('splits left markdown ending at <!-- right --> marker', () => {
    const article = parseArticle('id', SAMPLE);
    expect(article.leftMarkdown).toContain('Lợi nhuận quý I/2026');
    expect(article.leftMarkdown).toContain('## Cần để ý');
    expect(article.leftMarkdown).not.toContain('Raw text gốc');
    expect(article.leftMarkdown).not.toContain('<!-- right -->');
  });

  it('extracts right markdown after <!-- right --> marker', () => {
    const article = parseArticle('id', SAMPLE);
    expect(article.rightMarkdown).toContain('Raw text gốc full body');
    expect(article.rightMarkdown).not.toContain('<!-- right -->');
    expect(article.rightMarkdown).not.toContain('Lợi nhuận');
  });

  it('throws when <!-- left --> marker missing', () => {
    const bad = `---\ntitle: x\n---\n\nno markers here`;
    expect(() => parseArticle('id', bad)).toThrow(/left.*marker/i);
  });

  it('throws when <!-- right --> marker missing', () => {
    const bad = `---\ntitle: x\n---\n\n<!-- left -->\nonly left`;
    expect(() => parseArticle('id', bad)).toThrow(/right.*marker/i);
  });

  it('parses gemini block when present in frontmatter', () => {
    const withGemini = `---
title: T
ticker: ACB
sector: Bank
sector_icon: 🏦
crawled_at: 2026-05-13T10:00:00+07:00
funnel_batch_id: ACB-x
left_meta: { author: x, word_count: 1, key_view: lạc quan, skeptic_verdict: pass, pipeline_version: V5.0 }
insight: ""
right_source: { name: s, url: u, published: 2026-05-13, raw_title: r }
crawl_funnel: { picked: [], rejected: [], total_candidates: 0 }
gemini:
  title: "ACB tăng vốn 30%"
  body: "Body có **bold** và bullet — em dash."
  word_count: 250
  model: gemini-2.5-pro
  generated_at: 2026-05-13T10:01:23+00:00
---

<!-- left -->

Claude body.

<!-- right -->

Raw.
`;
    const article = parseArticle('id', withGemini);
    expect(article.meta.gemini).toBeDefined();
    expect(article.meta.gemini?.title).toBe('ACB tăng vốn 30%');
    expect(article.meta.gemini?.body).toBe('Body có **bold** và bullet — em dash.');
    expect(article.meta.gemini?.word_count).toBe(250);
    expect(article.meta.gemini?.model).toBe('gemini-2.5-pro');
  });

  it('parses grok block when present in frontmatter', () => {
    const withGrok = `---
title: T
ticker: ACB
sector: Bank
sector_icon: 🏦
crawled_at: 2026-05-14T10:00:00+07:00
funnel_batch_id: ACB-x
left_meta: { author: x, word_count: 1, key_view: lạc quan, skeptic_verdict: pass, pipeline_version: V5.0 }
insight: ""
right_source: { name: s, url: u, published: 2026-05-14, raw_title: r }
crawl_funnel: { picked: [], rejected: [], total_candidates: 0 }
grok:
  title: "Grok ACB hỏi xoáy đáp xoay"
  body: "Body **bold** và bullet."
  word_count: 270
  model: grok-4-fast-non-reasoning
  generated_at: 2026-05-14T10:01:23+00:00
---

<!-- left -->

Claude body.

<!-- right -->

Raw.
`;
    const article = parseArticle('id', withGrok);
    expect(article.meta.grok).toBeDefined();
    expect(article.meta.grok?.title).toBe('Grok ACB hỏi xoáy đáp xoay');
    expect(article.meta.grok?.body).toBe('Body **bold** và bullet.');
    expect(article.meta.grok?.word_count).toBe(270);
    expect(article.meta.grok?.model).toBe('grok-4-fast-non-reasoning');
  });

  it('leaves gemini + grok undefined when absent (legacy article)', () => {
    const article = parseArticle('id', SAMPLE);
    expect(article.meta.gemini).toBeUndefined();
    expect(article.meta.grok).toBeUndefined();
  });
});
