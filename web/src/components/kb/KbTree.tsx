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

const ROW_BASE =
  'group/row flex w-full items-center gap-2.5 rounded-md px-2 transition-colors duration-fast';
const ROW_HEIGHT = 'py-1.5 leading-tight';

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
    <nav aria-label="Phụ lục KB" className="flex flex-col gap-px px-1.5 pb-3">
      <p className="px-2 pb-1.5 pt-2 font-sans text-[10px] font-semibold uppercase tracking-[0.18em] text-fg-3">
        Phụ lục
      </p>
      {grouped.map((group, idx) => {
        const isOpen = expanded.has(group.groupId);
        const isMasterOnly =
          group.groupId === 'master' && group.docs.length === 1;
        const dividerCls =
          idx > 0 ? 'mt-1.5 pt-1.5 border-t border-fg-4/25' : '';

        if (isMasterOnly) {
          const doc = group.docs[0];
          const title = titleForSlug(doc.slug, doc.body, doc.meta.title);
          const isActive = doc.slug === activeSlug;
          return (
            <Link
              key={group.groupId}
              to={`/tai-lieu/${doc.slug}`}
              aria-current={isActive ? 'page' : undefined}
              className={cn(
                ROW_BASE,
                ROW_HEIGHT,
                'font-sans text-[12.5px]',
                isActive
                  ? 'bg-brand/10 font-semibold text-brand'
                  : 'font-medium text-fg-1 hover:bg-bg-2 hover:text-fg-0',
              )}
            >
              <span aria-hidden className="w-5 shrink-0 text-center text-base leading-none">
                {group.icon}
              </span>
              <span className="truncate">{title}</span>
            </Link>
          );
        }

        return (
          <div key={group.groupId} className={dividerCls}>
            <button
              type="button"
              onClick={() => toggle(group.groupId)}
              aria-expanded={isOpen}
              className={cn(
                ROW_BASE,
                ROW_HEIGHT,
                'text-left hover:bg-bg-2',
              )}
            >
              <span aria-hidden className="w-5 shrink-0 text-center text-base leading-none">
                {group.icon}
              </span>
              <span className="flex-1 truncate font-sans text-[12.5px] font-semibold text-fg-1">
                {group.label}
              </span>
              <span className="font-mono text-[10px] tabular-nums text-fg-3">
                {group.docs.length}
              </span>
              <ChevronDown
                aria-hidden
                strokeWidth={2.2}
                className={cn(
                  'h-3 w-3 shrink-0 text-fg-3 transition-transform duration-fast',
                  !isOpen && '-rotate-90',
                )}
              />
            </button>
            {isOpen && (
              <ul className="flex list-none flex-col gap-px pb-0.5">
                {group.docs.map((doc) => {
                  const title = titleForSlug(doc.slug, doc.body, doc.meta.title);
                  const isActive = doc.slug === activeSlug;
                  return (
                    <li key={doc.slug}>
                      <Link
                        to={`/tai-lieu/${doc.slug}`}
                        aria-current={isActive ? 'page' : undefined}
                        className={cn(
                          ROW_BASE,
                          'py-1 leading-tight font-sans text-[12px]',
                          isActive
                            ? 'bg-brand/10 font-medium text-brand'
                            : 'text-fg-2 hover:bg-bg-2 hover:text-fg-0',
                        )}
                      >
                        <span aria-hidden className="w-5 shrink-0" />
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
