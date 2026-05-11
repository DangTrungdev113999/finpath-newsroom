import { useSearchParams } from 'react-router-dom';
import { cn } from '../../shared/lib/cn';

type Sector = 'bds' | 'bank' | 'ck';

const TABS: { id: Sector; label: string; enabled: boolean }[] = [
  { id: 'bds', label: 'Bất động sản', enabled: true },
  { id: 'bank', label: 'Ngân hàng', enabled: false },
  { id: 'ck', label: 'Chứng khoán', enabled: false },
];

export function KbTabs({ active }: { active: Sector }) {
  const [params, setParams] = useSearchParams();

  const onSelect = (sector: Sector) => {
    const next = new URLSearchParams(params);
    if (sector === 'bds') next.delete('sector');
    else next.set('sector', sector);
    setParams(next, { replace: true });
  };

  return (
    <div
      role="tablist"
      aria-label="Sector"
      className="flex items-center gap-1 border-b border-fg-4/40 px-2"
    >
      {TABS.map((t) => {
        const isActive = t.id === active;
        return (
          <button
            key={t.id}
            type="button"
            role="tab"
            aria-selected={isActive}
            disabled={!t.enabled}
            title={t.enabled ? undefined : 'Sắp có — đang refactor pipeline'}
            onClick={() => t.enabled && onSelect(t.id)}
            className={cn(
              'relative h-9 px-3 font-sans text-[12.5px] font-medium transition-colors duration-fast',
              t.enabled
                ? isActive
                  ? 'text-fg-0'
                  : 'text-fg-2 hover:text-fg-0'
                : 'cursor-not-allowed text-fg-3 opacity-60',
            )}
          >
            {t.label}
            {!t.enabled && (
              <span className="ml-1 align-middle font-mono text-[9px] uppercase tracking-wider text-fg-3">
                sắp có
              </span>
            )}
            {isActive && (
              <span
                aria-hidden
                className="absolute inset-x-2 -bottom-px h-[2px] rounded-full bg-brand"
              />
            )}
          </button>
        );
      })}
    </div>
  );
}
