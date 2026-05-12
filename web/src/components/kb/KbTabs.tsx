import { useSearchParams } from 'react-router-dom';
import { ChevronDown } from 'lucide-react';
import { SECTORS, SECTOR_LABELS, type Sector } from '../../lib/kbTypes';
import { docsForSector } from '../../lib/kbLoader';

// Group sectors by category for better UX
const SECTOR_CATEGORIES = [
  { label: 'Tài chính', sectors: ['bank', 'ck', 'insurance'] as Sector[] },
  { label: 'Bất động sản', sectors: ['bds', 'industrial-park', 'construction', 'public-investment'] as Sector[] },
  { label: 'Tiêu dùng', sectors: ['retail', 'food', 'pharma', 'automotive'] as Sector[] },
  { label: 'Xuất khẩu', sectors: ['seafood', 'textile'] as Sector[] },
  { label: 'Năng lượng & Vật liệu', sectors: ['oil-gas', 'utilities', 'chemicals', 'sugar'] as Sector[] },
  { label: 'Vận tải & Du lịch', sectors: ['aviation', 'transport', 'tourism'] as Sector[] },
  { label: 'Công nghệ & Tập đoàn', sectors: ['technology', 'viettel', 'vingroup'] as Sector[] },
  { label: 'Tra cứu', sectors: ['stock-master'] as Sector[] },
];

export function KbTabs({ active }: { active: Sector }) {
  const [params, setParams] = useSearchParams();

  const onSelect = (sector: Sector) => {
    const next = new URLSearchParams(params);
    if (sector === 'bds') next.delete('sector');
    else next.set('sector', sector);
    setParams(next, { replace: true });
  };

  const activeLabel = SECTOR_LABELS[active];
  const activeDocs = docsForSector(active);

  return (
    <div className="border-b border-fg-4/40 p-2">
      <div className="relative">
        <select
          value={active}
          onChange={(e) => onSelect(e.target.value as Sector)}
          className="w-full appearance-none rounded-md border border-fg-4/50 bg-bg-2 py-2 pl-3 pr-8 font-sans text-[13px] font-medium text-fg-0 focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand"
        >
          {SECTOR_CATEGORIES.map((cat) => (
            <optgroup key={cat.label} label={cat.label}>
              {cat.sectors.map((s) => {
                const docs = docsForSector(s);
                const count = docs.length;
                return (
                  <option key={s} value={s}>
                    {SECTOR_LABELS[s]} {count > 0 ? `(${count})` : '(sắp có)'}
                  </option>
                );
              })}
            </optgroup>
          ))}
        </select>
        <ChevronDown
          className="pointer-events-none absolute right-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-fg-2"
          strokeWidth={2}
        />
      </div>
      <p className="mt-1.5 px-1 font-sans text-[11px] text-fg-3">
        {activeDocs.length} tài liệu
      </p>
    </div>
  );
}
