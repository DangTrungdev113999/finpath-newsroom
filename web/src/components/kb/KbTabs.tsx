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
      className="flex items-stretch border-b border-fg-4/40"
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
              'relative flex-1 whitespace-nowrap px-2 py-2.5 font-sans text-[11.5px] font-medium tracking-[0.005em] transition-colors duration-fast',
              t.enabled
                ? isActive
                  ? 'text-brand'
                  : 'text-fg-2 hover:text-fg-0'
                : 'cursor-not-allowed text-fg-3 opacity-45',
            )}
          >
            {t.label}
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
