// web/src/lib/feedbackStorage.ts
/**
 * localStorage-backed feedback state.
 *
 * Schema (under key `finpath-newsroom-feedback`):
 *   { name: string|null, client_id: uuid, comments: { [article_id]: Entry[] } }
 *
 * Falls back to in-memory if localStorage throws (private mode, quota).
 */

const STORAGE_KEY = 'finpath-newsroom-feedback';

export interface CommentEntry {
  comment: string;
  timestamp: string; // ISO 8601
  telegram_message_id?: number;
}

export interface FeedbackStorage {
  name: string | null;
  client_id: string;
  comments: Record<string, CommentEntry[]>;
}

// In-memory fallback when localStorage unavailable
let memoryFallback: FeedbackStorage | null = null;
let storageBroken = false;

function uuidv4(): string {
  // crypto.randomUUID is available in modern browsers + Vite dev; fall back to manual
  if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
    return crypto.randomUUID();
  }
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16);
  });
}

function defaultStorage(): FeedbackStorage {
  return { name: null, client_id: uuidv4(), comments: {} };
}

function tryRead(): FeedbackStorage {
  if (storageBroken) return memoryFallback ?? (memoryFallback = defaultStorage());
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      const fresh = defaultStorage();
      tryWrite(fresh);
      return fresh;
    }
    const parsed = JSON.parse(raw) as FeedbackStorage;
    // Defensive: ensure shape (legacy or corrupted entries)
    if (!parsed.client_id) parsed.client_id = uuidv4();
    if (!parsed.comments) parsed.comments = {};
    if (parsed.name === undefined) parsed.name = null;
    return parsed;
  } catch {
    storageBroken = true;
    memoryFallback = defaultStorage();
    return memoryFallback;
  }
}

function tryWrite(s: FeedbackStorage): void {
  if (storageBroken) {
    memoryFallback = s;
    return;
  }
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
  } catch {
    storageBroken = true;
    memoryFallback = s;
  }
}

export function getStorage(): FeedbackStorage {
  return tryRead();
}

export function saveName(name: string): void {
  const s = tryRead();
  s.name = name;
  tryWrite(s);
}

export function appendComment(article_id: string, entry: CommentEntry): void {
  const s = tryRead();
  if (!s.comments[article_id]) s.comments[article_id] = [];
  s.comments[article_id].push(entry);
  tryWrite(s);
}

export function getCommentsForArticle(article_id: string): CommentEntry[] {
  return tryRead().comments[article_id] ?? [];
}

export function resetStorage(): void {
  storageBroken = false;
  memoryFallback = null;
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    /* ignore */
  }
}

export function isStorageDisabled(): boolean {
  if (storageBroken) return true;
  try {
    const test = '__finpath_test__';
    localStorage.setItem(test, '1');
    localStorage.removeItem(test);
    return false;
  } catch {
    storageBroken = true;
    return true;
  }
}
