import { useMemo } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ChevronDown } from 'lucide-react';
import type { KbDoc } from '../../lib/kbTypes';
import { BDS_GROUPS, groupForSlug, titleForSlug } from '../../lib/kbTree';
import { cn } from '../../shared/lib/cn';

interface Props {
  docs: KbDoc[];
  expanded: Set<string>;
  onExpandedChange: (next: Set<string>) => void;
}

interface GroupedDocs {
  groupId: string;
  icon: string;
  label: string;
  docs: KbDoc[];
}

export function KbTree({ docs, expanded, onExpandedChange }: Props) {
  const { slug: activeSlug } = useParams<{ slug?: string }>();

  const grouped = useMemo<GroupedDocs[]>(() => {
    const result: GroupedDocs[] = BDS_GROUPS.map((g) => ({
      groupId: g.id,
      icon: g.icon,
      label: g.label,
      docs: [] as KbDoc[],
    }));
    for (const doc of docs) {
      const group = groupForSlug(doc.slug);
      const bucket = result.find((g) => g.groupId === group.id);
      if (bucket) bucket.docs.push(doc);
    }
    return result.filter((g) => g.docs.length > 0);
  }, [docs]);

  const toggle = (id: string) => {
    const next = new Set(expanded);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    onExpandedChange(next);
  };

  return (
    <nav aria-label="Phụ lục KB" className="flex flex-col gap-1">
      <p className="px-3 pb-1 pt-2 font-sans text-[10.5px] uppercase tracking-[0.14em] text-fg-3">
        Phụ lục
      </p>
      {grouped.map((group) => {
        const isOpen = expanded.has(group.groupId);
        const isMasterOnly = group.groupId === 'master' && group.docs.length === 1;
        return (
          <div key={group.groupId}>
            {!isMasterOnly && (
              <button
                type="button"
                onClick={() => toggle(group.groupId)}
                className={cn(
                  'group flex w-full items-center gap-2 rounded-md px-3 py-1.5 text-left transition-colors duration-fast',
                  'hover:bg-bg-2',
                )}
                aria-expanded={isOpen}
              >
                <span aria-hidden className="w-5 text-base leading-none">{group.icon}</span>
                <span className="flex-1 font-sans text-[13px] font-semibold text-fg-1">
                  {group.label}
                </span>
                <span className="font-mono text-[10px] tabular-nums text-fg-3">
                  {group.docs.length}
                </span>
                <ChevronDown
                  className={cn(
                    'h-3.5 w-3.5 text-fg-3 transition-transform duration-fast',
                    !isOpen && '-rotate-90',
                  )}
                  strokeWidth={2.2}
                  aria-hidden
                />
              </button>
            )}
            {(isMasterOnly || isOpen) && (
              <ul className={cn('flex flex-col gap-0.5', !isMasterOnly && 'pl-3')}>
                {group.docs.map((doc) => {
                  const title = titleForSlug(doc.slug, doc.body, doc.meta.title);
                  const isActive = doc.slug === activeSlug;
                  return (
                    <li key={doc.slug}>
                      <Link
                        to={`/tai-lieu/${doc.slug}`}
                        className={cn(
                          'flex items-center gap-2 rounded-md px-3 py-1.5 font-sans text-[12.5px] transition-colors duration-fast',
                          isMasterOnly && 'gap-2.5',
                          isActive
                            ? 'bg-brand/10 text-fg-0 border-l-2 border-brand pl-[10px]'
                            : 'text-fg-2 hover:bg-bg-2 hover:text-fg-0',
                        )}
                      >
                        {isMasterOnly && (
                          <span aria-hidden className="text-base leading-none">{group.icon}</span>
                        )}
                        <span className="truncate">{title}</span>
                      </Link>
                    </li>
                  );
                })}
              </ul>
            )}
          </div>
        );
      })}
    </nav>
  );
}
