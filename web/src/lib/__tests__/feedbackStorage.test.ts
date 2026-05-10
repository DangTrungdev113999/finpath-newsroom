// web/src/lib/__tests__/feedbackStorage.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  getStorage,
  saveName,
  appendComment,
  getCommentsForArticle,
  resetStorage,
  isStorageDisabled,
} from '../feedbackStorage';

describe('feedbackStorage', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('initializes with null name and generated client_id', () => {
    const s = getStorage();
    expect(s.name).toBeNull();
    expect(s.client_id).toMatch(/^[0-9a-f-]{36}$/);
    expect(s.comments).toEqual({});
  });

  it('persists name across reads', () => {
    saveName('Trung');
    expect(getStorage().name).toBe('Trung');
  });

  it('appends comment to article-specific list', () => {
    appendComment('vcb-123', { comment: 'hay', timestamp: '2026-05-11T08:00:00Z' });
    appendComment('vcb-123', { comment: 'lủng', timestamp: '2026-05-11T09:00:00Z' });
    appendComment('tcb-456', { comment: 'ok', timestamp: '2026-05-11T10:00:00Z' });
    const vcb = getCommentsForArticle('vcb-123');
    expect(vcb).toHaveLength(2);
    expect(vcb[0].comment).toBe('hay');
    const tcb = getCommentsForArticle('tcb-456');
    expect(tcb).toHaveLength(1);
  });

  it('returns empty array for unknown article', () => {
    expect(getCommentsForArticle('unknown')).toEqual([]);
  });

  it('reuses existing client_id across calls', () => {
    const a = getStorage().client_id;
    const b = getStorage().client_id;
    expect(a).toBe(b);
  });

  it('resetStorage clears everything', () => {
    saveName('x');
    appendComment('a', { comment: 'c', timestamp: 't' });
    resetStorage();
    const s = getStorage();
    expect(s.name).toBeNull();
    expect(s.comments).toEqual({});
  });

  it('detects disabled localStorage', () => {
    const original = Storage.prototype.setItem;
    Storage.prototype.setItem = vi.fn(() => {
      throw new Error('disabled');
    });
    expect(isStorageDisabled()).toBe(true);
    Storage.prototype.setItem = original;
  });
});
