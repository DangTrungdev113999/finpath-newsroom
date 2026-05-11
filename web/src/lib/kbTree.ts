import type { KbGroupConfig } from './kbTypes';

// BĐS group config. Match order = display order in sidebar. First match wins.
// Last entry "other" is a catch-all so new KB files never disappear from the tree.
export const BDS_GROUPS: KbGroupConfig[] = [
  { id: 'master',  icon: '🏛', label: 'Tham chiếu ngành',
    match: (slug) => slug === 'bds-industry-master-reference' },
  { id: 'general', icon: '📊', label: 'Khái niệm chung',
    match: (slug) => /^bds-(macro|legal|debt|revenue|hybrid)-/.test(slug) },
  { id: 'res',     icon: '🏘', label: 'Phát triển dân cư',
    match: (slug) => /^bds-res-/.test(slug) },
  { id: 'kcn',     icon: '🏭', label: 'Khu công nghiệp',
    match: (slug) => /^bds-kcn-/.test(slug) },
  { id: 'retail',  icon: '🛍', label: 'Bán lẻ trung tâm',
    match: (slug) => /^bds-retail-/.test(slug) },
  { id: 'office',  icon: '🏢', label: 'Văn phòng cho thuê',
    match: (slug) => /^bds-office-/.test(slug) },
  { id: 'resort',  icon: '🏖', label: 'Nghỉ dưỡng',
    match: (slug) => /^bds-resort-/.test(slug) },
  { id: 'dc',      icon: '🖥', label: 'Trung tâm dữ liệu',
    match: (slug) => /^bds-dc-/.test(slug) },
  { id: 'other',   icon: '📎', label: 'Khác',
    match: () => true },
];

export const BDS_TITLES: Record<string, string> = {
  'bds-industry-master-reference': 'Tham chiếu ngành',
  'bds-macro-cycle-credit': 'Chu kỳ vĩ mô & tín dụng',
  'bds-legal-framework': 'Khung pháp lý',
  'bds-debt-leverage': 'Đòn bẩy nợ',
  'bds-revenue-recognition-vas': 'Ghi nhận doanh thu (VAS)',
  'bds-hybrid-business-models': 'Mô hình kinh doanh lai',
  'bds-res-land-bank-nav': 'Quỹ đất & NAV',
  'bds-res-project-lifecycle': 'Vòng đời dự án',
  'bds-res-presales-backlog': 'Bán trước & backlog',
  'bds-kcn-fdi-demand-mechanism': 'Cơ chế cầu FDI',
  'bds-kcn-lease-structure': 'Cấu trúc thuê đất',
  'bds-kcn-inventory-pricing': 'Tồn kho & giá thuê',
  'bds-retail-footfall-mechanism': 'Lưu lượng khách',
  'bds-retail-anchor-vs-sme-tenants': 'Anchor & khách thuê SME',
  'bds-retail-tenant-mix-quality': 'Chất lượng tenant mix',
  'bds-office-class-tiering': 'Phân hạng văn phòng',
  'bds-office-hybrid-work-impact': 'Tác động làm việc kết hợp',
  'bds-resort-tourism-cycle': 'Chu kỳ du lịch',
  'bds-resort-condotel-legal-pitfalls': 'Cạm bẫy pháp lý condotel',
  'bds-resort-hybrid-model': 'Mô hình lai nghỉ dưỡng',
  'bds-dc-hyperscaler-power': 'Điện cho hyperscaler',
};

export function groupForSlug(slug: string): KbGroupConfig {
  for (const group of BDS_GROUPS) {
    if (group.match(slug)) return group;
  }
  return BDS_GROUPS[BDS_GROUPS.length - 1];
}

// Resolve display title for a KB slug.
// Order: BDS_TITLES map → first H1 in body → frontmatter title → slug.
export function titleForSlug(
  slug: string,
  body: string,
  frontmatterTitle: string | undefined,
): string {
  if (BDS_TITLES[slug]) return BDS_TITLES[slug];
  const h1Match = body.match(/^#\s+(.+)$/m);
  if (h1Match) return h1Match[1].trim();
  if (frontmatterTitle) return frontmatterTitle;
  return slug;
}
