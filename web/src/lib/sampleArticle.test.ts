import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { resolve } from 'path';
import { parseArticle } from './parseArticle';

describe('sample VCB article', () => {
  it('parses without error and contains expected sections', () => {
    const raw = readFileSync(
      resolve(__dirname, '../../../output/compare-feed/VCB-20260508-1530.md'),
      'utf8',
    );
    const a = parseArticle('VCB-20260508-1530', raw);
    expect(a.meta.ticker).toBe('VCB');
    expect(a.leftMarkdown.length).toBeGreaterThan(200);
    expect(a.rightMarkdown.length).toBeGreaterThan(50);
  });
});
