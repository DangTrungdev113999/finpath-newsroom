export interface KbMeta {
  category?: string;
  title?: string;
  last_updated?: string;
  applies_to?: string[];
  notion_page_id?: string;
  source_url?: string;
  [extra: string]: unknown;
}

export interface KbHeading {
  level: 2 | 3;
  text: string;
  slug: string;
}

export const SECTORS = [
  'bank', 'ck', 'bds',
  'automotive', 'aviation', 'chemicals', 'construction', 'food',
  'industrial-park', 'insurance', 'oil-gas', 'pharma', 'public-investment',
  'retail', 'seafood', 'stock-master', 'sugar', 'technology', 'textile',
  'tourism', 'transport', 'utilities', 'viettel', 'vingroup',
] as const;

export type Sector = (typeof SECTORS)[number];

export const SECTOR_LABELS: Record<Sector, string> = {
  bank: 'Ngân hàng',
  ck: 'Chứng khoán',
  bds: 'Bất động sản',
  automotive: 'Ô tô',
  aviation: 'Hàng không',
  chemicals: 'Hóa chất',
  construction: 'Xây dựng',
  food: 'Thực phẩm',
  'industrial-park': 'Khu công nghiệp',
  insurance: 'Bảo hiểm',
  'oil-gas': 'Dầu khí',
  pharma: 'Dược phẩm',
  'public-investment': 'Đầu tư công',
  retail: 'Bán lẻ',
  seafood: 'Thủy sản',
  'stock-master': 'Tra cứu mã',
  sugar: 'Mía đường',
  technology: 'Công nghệ',
  textile: 'Dệt may',
  tourism: 'Du lịch',
  transport: 'Vận tải',
  utilities: 'Điện/Tiện ích',
  viettel: 'Nhóm Viettel',
  vingroup: 'Nhóm Vingroup',
};

export function isSector(v: string | null): v is Sector {
  return SECTORS.includes(v as Sector);
}

export interface KbDoc {
  slug: string;
  sector: Sector;
  meta: KbMeta;
  body: string;
  headings: KbHeading[];
}

export interface KbGroupConfig {
  id: string;
  icon: string;
  label: string;
  match: (slug: string) => boolean;
}
