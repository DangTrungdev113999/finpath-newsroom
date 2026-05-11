import { useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Fuse, { type FuseResult, type FuseResultMatch } from 'fuse.js';
import { Search, X } from 'lucide-react';
import type { KbDoc } from '../../lib/kbTypes';
import { titleForSlug } from '../../lib/kbTree';
import { cn } from '../../shared/lib/cn';

interface Props { docs: KbDoc[]; }

interface IndexedDoc extends KbDoc {
  title: string;
  headingText: string;
}

const SNIPPET_RADIUS = 60;
const MAX_RESULTS = 5;

export function KbSearch({ docs }: Props) {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const indexed = useMemo<IndexedDoc[]>(
    () =>
      docs.map((d) => ({
        ...d,
        title: titleForSlug(d.slug, d.body, d.meta.title),
        headingText: d.headings.map((h) => h.text).join(' \n '),
      })),
    [docs],
  );

  const fuse = useMemo(
    () =>
      new Fuse(indexed, {
        keys: [
          { name: 'title', weight: 3 },
          { name: 'headingText', weight: 2 },
          { name: 'body', weight: 1 },
        ],
        includeMatches: true,
        ignoreLocation: true,
        threshold: 0.4,
        minMatchCharLength: 2,
      }),
    [indexed],
  );

  const results = useMemo(() => {
    const q = query.trim();
    if (q.length < 2) return [];
    return fuse.search(q, { limit: MAX_RESULTS });
  }, [fuse, query]);

  const onPick = (slug: string, anchor?: string) => {
    const url = anchor ? `/tai-lieu/${slug}#${anchor}` : `/tai-lieu/${slug}`;
    navigate(url);
    setQuery('');
  };

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape' && document.activeElement === inputRef.current) {
        setQuery('');
        inputRef.current?.blur();
      }
    }
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, []);

  const isOpen = query.trim().length >= 2;

  return (
    <div className="relative px-3 pb-2">
      <div className="relative">
        <Search
          className="pointer-events-none absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-fg-3"
          strokeWidth={2}
          aria-hidden
        />
        <input
          ref={inputRef}
          type="search"
          placeholder="tìm KB..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="h-9 w-full rounded-md border border-fg-4/40 bg-bg-1 pl-9 pr-8 font-sans text-[13px] text-fg-0 placeholder:text-fg-3 focus:border-brand/60 focus:outline-none focus:ring-2 focus:ring-brand/30"
        />
        {query && (
          <button
            type="button"
            onClick={() => setQuery('')}
            className="absolute right-2 top-1/2 flex h-5 w-5 -translate-y-1/2 items-center justify-center rounded text-fg-3 hover:bg-bg-2 hover:text-fg-0"
            aria-label="Xoá tìm kiếm"
          >
            <X className="h-3 w-3" strokeWidth={2.2} aria-hidden />
          </button>
        )}
      </div>
      {isOpen && (
        <div className="mt-1.5 overflow-hidden rounded-md border border-fg-4/40 bg-bg-1 shadow-lg">
          {results.length === 0 ? (
            <p className="px-3 py-3 font-sans text-[12px] text-fg-3">
              Không có KB nào khớp "<span className="text-fg-1">{query}</span>".
            </p>
          ) : (
            <ul role="listbox" className="flex flex-col">
              {results.map((r) => (
                <ResultRow key={r.item.slug} result={r} onPick={onPick} />
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

function ResultRow({
  result,
  onPick,
}: {
  result: FuseResult<IndexedDoc>;
  onPick: (slug: string, anchor?: string) => void;
}) {
  const { item, matches } = result;
  const { snippet, headingSlug } = useMemo(
    () => buildSnippet(item, matches ?? []),
    [item, matches],
  );

  return (
    <li>
      <button
        type="button"
        onClick={() => onPick(item.slug, headingSlug)}
        className="flex w-full flex-col gap-1 px-3 py-2.5 text-left transition-colors duration-fast hover:bg-bg-2"
      >
        <span className="font-sans text-[12.5px] font-semibold text-fg-0">
          {item.title}
        </span>
        {/* snippet HTML is safe: all doc/query content is escapeHtml'd; only <mark> tag is injected */}
        <span
          className="font-sans text-[11.5px] leading-snug text-fg-2"
          dangerouslySetInnerHTML={{ __html: snippet }}
        />
      </button>
    </li>
  );
}

function buildSnippet(
  doc: IndexedDoc,
  matches: readonly FuseResultMatch[],
): { snippet: string; headingSlug?: string } {
  const headingMatch = matches.find((m) => m.key === 'headingText');
  const bodyMatch = matches.find((m) => m.key === 'body');
  const titleMatch = matches.find((m) => m.key === 'title');

  if (bodyMatch?.indices?.length) {
    const [start, end] = bodyMatch.indices[0];
    return { snippet: sliceSnippet(doc.body, start, end) };
  }

  if (headingMatch?.indices?.length) {
    const [start, end] = headingMatch.indices[0];
    const text = doc.headingText;
    const snippet = sliceSnippet(text, start, end);
    let cumulative = 0;
    for (const h of doc.headings) {
      const next = cumulative + h.text.length + 3;
      if (start >= cumulative && start < next) {
        return { snippet, headingSlug: h.slug };
      }
      cumulative = next;
    }
    return { snippet };
  }

  if (titleMatch) {
    return { snippet: escapeHtml(doc.title) };
  }

  return { snippet: escapeHtml(doc.body.slice(0, 120)) + '...' };
}

function sliceSnippet(text: string, start: number, end: number): string {
  const left = Math.max(0, start - SNIPPET_RADIUS);
  const right = Math.min(text.length, end + 1 + SNIPPET_RADIUS);
  const prefix = left > 0 ? '...' : '';
  const suffix = right < text.length ? '...' : '';
  const before = escapeHtml(text.slice(left, start));
  const match = escapeHtml(text.slice(start, end + 1));
  const after = escapeHtml(text.slice(end + 1, right));
  return `${prefix}${before}<mark class="bg-brand/30 text-fg-0 rounded px-0.5">${match}</mark>${after}${suffix}`;
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
