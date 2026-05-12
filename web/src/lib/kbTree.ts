import type { KbGroupConfig, Sector } from './kbTypes';

// BĐS group config
export const BDS_GROUPS: KbGroupConfig[] = [
  { id: 'master', icon: '🏛', label: 'Tham chiếu ngành',
    match: (slug) => slug === 'bds-industry-master-reference' },
  { id: 'general', icon: '📊', label: 'Khái niệm chung',
    match: (slug) => /^bds-(macro|legal|debt|revenue|hybrid)-/.test(slug) },
  { id: 'res', icon: '🏘', label: 'Phát triển dân cư',
    match: (slug) => /^bds-res-/.test(slug) },
  { id: 'kcn', icon: '🏭', label: 'Khu công nghiệp',
    match: (slug) => /^bds-kcn-/.test(slug) },
  { id: 'retail', icon: '🛍', label: 'Bán lẻ trung tâm',
    match: (slug) => /^bds-retail-/.test(slug) },
  { id: 'office', icon: '🏢', label: 'Văn phòng cho thuê',
    match: (slug) => /^bds-office-/.test(slug) },
  { id: 'resort', icon: '🏖', label: 'Nghỉ dưỡng',
    match: (slug) => /^bds-resort-/.test(slug) },
  { id: 'dc', icon: '🖥', label: 'Trung tâm dữ liệu',
    match: (slug) => /^bds-dc-/.test(slug) },
  { id: 'other', icon: '📎', label: 'Khác',
    match: () => true },
];

// Default groups for sectors that don't have custom config
function defaultGroups(prefix: string): KbGroupConfig[] {
  return [
    { id: 'master', icon: '🏛', label: 'Tham chiếu ngành',
      match: (slug) => slug.includes('master-reference') || slug.includes('industry-master') },
    { id: 'frameworks', icon: '📊', label: 'Frameworks',
      match: (slug) => slug.startsWith(prefix) },
    { id: 'other', icon: '📎', label: 'Khác',
      match: () => true },
  ];
}

// Sector-specific group configs
const SECTOR_GROUPS: Partial<Record<Sector, KbGroupConfig[]>> = {
  bds: BDS_GROUPS,
  bank: [
    { id: 'master', icon: '🏛', label: 'Tham chiếu ngành',
      match: (slug) => slug === 'bank-industry-master-reference' },
    { id: 'deep-dive', icon: '📊', label: 'Deep dive',
      match: (slug) => /^bank-(nim|npl|target)-/.test(slug) },
    { id: 'other', icon: '📎', label: 'Khác',
      match: () => true },
  ],
  ck: [
    { id: 'master', icon: '🏛', label: 'Tham chiếu ngành',
      match: (slug) => slug === 'ck-industry-master-reference' },
    { id: 'deep-dive', icon: '📊', label: 'Deep dive',
      match: (slug) => /^ck-(margin|brokerage|liquidity|proprietary|ib)-/.test(slug) },
    { id: 'other', icon: '📎', label: 'Khác',
      match: () => true },
  ],
  aviation: [
    { id: 'master', icon: '🏛', label: 'Tham chiếu ngành',
      match: (slug) => slug.includes('master-reference') },
    { id: 'deep-dive', icon: '📊', label: 'Deep dive',
      match: (slug) => /aviation-(operating|fuel)-/.test(slug) },
    { id: 'other', icon: '📎', label: 'Khác',
      match: () => true },
  ],
  food: [
    { id: 'master', icon: '🏛', label: 'Tham chiếu ngành',
      match: (slug) => slug.includes('master-reference') },
    { id: 'deep-dive', icon: '📊', label: 'Deep dive',
      match: (slug) => /food-(nvl|seasonality)-/.test(slug) },
    { id: 'other', icon: '📎', label: 'Khác',
      match: () => true },
  ],
  retail: [
    { id: 'master', icon: '🏛', label: 'Tham chiếu ngành',
      match: (slug) => slug.includes('master-reference') },
    { id: 'deep-dive', icon: '📊', label: 'Deep dive',
      match: (slug) => /retail-(sssg|inventory)-/.test(slug) },
    { id: 'other', icon: '📎', label: 'Khác',
      match: () => true },
  ],
  seafood: [
    { id: 'master', icon: '🏛', label: 'Tham chiếu ngành',
      match: (slug) => slug.includes('master-reference') },
    { id: 'deep-dive', icon: '📊', label: 'Deep dive',
      match: (slug) => /seafood-(vhc|export)-/.test(slug) },
    { id: 'other', icon: '📎', label: 'Khác',
      match: () => true },
  ],
  textile: [
    { id: 'master', icon: '🏛', label: 'Tham chiếu ngành',
      match: (slug) => slug.includes('master-reference') },
    { id: 'deep-dive', icon: '📊', label: 'Deep dive',
      match: (slug) => /textile-(cmt|fta)-/.test(slug) },
    { id: 'other', icon: '📎', label: 'Khác',
      match: () => true },
  ],
};

export function groupsForSector(sector: Sector): KbGroupConfig[] {
  return SECTOR_GROUPS[sector] ?? defaultGroups(sector);
}

export function groupForSlug(slug: string, sector: Sector = 'bds'): KbGroupConfig {
  const groups = groupsForSector(sector);
  for (const group of groups) {
    if (group.match(slug)) return group;
  }
  return groups[groups.length - 1];
}

// Resolve display title for a KB slug.
export function titleForSlug(
  slug: string,
  body: string,
  frontmatterTitle: string | undefined,
): string {
  const h1Match = body.match(/^#\s+(.+)$/m);
  if (h1Match) return h1Match[1].trim();
  if (frontmatterTitle) return frontmatterTitle;
  return slug;
}
