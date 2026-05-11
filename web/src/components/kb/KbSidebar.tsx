import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { X } from 'lucide-react';
import type { KbDoc } from '../../lib/kbTypes';
import { cn } from '../../shared/lib/cn';
import { groupForSlug } from '../../lib/kbTree';
import { KbSearch } from './KbSearch';
import { KbTabs } from './KbTabs';
import { KbTree } from './KbTree';

type Sector = 'bds' | 'bank' | 'ck';

interface Props {
  sector: Sector;
  docs: KbDoc[];
  isDrawerOpen: boolean;
  onClose: () => void;
}

export function KbSidebar({ sector, docs, isDrawerOpen, onClose }: Props) {
  const { slug: activeSlug } = useParams<{ slug?: string }>();

  // ESC closes drawer
  useEffect(() => {
    if (!isDrawerOpen) return;
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose();
    }
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [isDrawerOpen, onClose]);

  // Search state shared between desktop + mobile renders
  const [query, setQuery] = useState('');

  // Expand state shared between desktop + mobile renders
  const storageKey = `kb.expanded.${sector}`;
  const [expanded, setExpanded] = useState<Set<string>>(() => {
    try {
      const raw = localStorage.getItem(storageKey);
      if (raw) return new Set(JSON.parse(raw) as string[]);
    } catch { /* ignore */ }
    return new Set();
  });

  useEffect(() => {
    try {
      localStorage.setItem(storageKey, JSON.stringify([...expanded]));
    } catch { /* ignore */ }
  }, [expanded, storageKey]);

  // Auto-expand active slug's owner group
  useEffect(() => {
    if (!activeSlug) return;
    const owner = groupForSlug(activeSlug);
    setExpanded((prev) => (prev.has(owner.id) ? prev : new Set([...prev, owner.id])));
  }, [activeSlug]);

  const body = (
    <div className="flex h-full flex-col">
      <KbTabs active={sector} />
      <div className="flex-1 overflow-y-auto pb-4">
        <KbSearch docs={docs} query={query} onQueryChange={setQuery} />
        {docs.length === 0 ? (
          <p className="px-3 pt-4 font-sans text-[12px] text-fg-3">
            Sector này chưa có KB. Sắp có.
          </p>
        ) : (
          <KbTree docs={docs} expanded={expanded} onExpandedChange={setExpanded} />
        )}
      </div>
    </div>
  );

  return (
    <>
      <aside className="hidden w-[280px] shrink-0 border-r border-fg-4/40 bg-bg-1 lg:block">
        {body}
      </aside>

      <div
        className={cn(
          'fixed inset-0 z-40 lg:hidden',
          isDrawerOpen ? 'pointer-events-auto' : 'pointer-events-none',
        )}
        aria-hidden={!isDrawerOpen}
      >
        <button
          type="button"
          aria-label="Đóng phụ lục"
          onClick={onClose}
          className={cn(
            'absolute inset-0 bg-bg-0/60 backdrop-blur-sm transition-opacity duration-fast',
            isDrawerOpen ? 'opacity-100' : 'opacity-0',
          )}
        />
        <aside
          className={cn(
            'absolute left-0 top-0 h-full w-[280px] border-r border-fg-4/40 bg-bg-1 shadow-xl transition-transform duration-med ease-out-quart',
            isDrawerOpen ? 'translate-x-0' : '-translate-x-full',
          )}
        >
          <div className="flex items-center justify-end px-2 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="rounded-md p-1.5 text-fg-2 hover:bg-bg-2 hover:text-fg-0"
              aria-label="Đóng"
            >
              <X className="h-4 w-4" strokeWidth={2.2} aria-hidden />
            </button>
          </div>
          {body}
        </aside>
      </div>
    </>
  );
}
