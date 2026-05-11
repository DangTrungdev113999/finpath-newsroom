/**
 * Single source of truth for the 16-ticker MVP universe.
 *
 * Acts as the static "API" for the filter UI. When a real backend ticker
 * endpoint comes online, swap the constants for an async fetch — the
 * `TickerInfo` shape and the `SECTORS` enum stay the same.
 */

export type Sector = 'bank' | 'ck' | 'bds';

export interface TickerInfo {
  code: string;
  name: string;
  sector: Sector;
  /** Extra search hints — diacritic-stripped names, alt spellings, popular nicknames. */
  aliases?: string[];
}

export interface SectorOption {
  id: Sector;
  label: string;
  short: string;
}

export const SECTORS: readonly SectorOption[] = [
  { id: 'bank', label: 'Ngân hàng', short: 'NH' },
  { id: 'ck', label: 'Chứng khoán', short: 'CK' },
  { id: 'bds', label: 'Bất động sản', short: 'BĐS' },
] as const;

export const TICKER_UNIVERSE: TickerInfo[] = [
  // ─── Bank (7) ───────────────────────────────────────────────────────
  {
    code: 'TCB',
    name: 'Techcombank',
    sector: 'bank',
    aliases: ['Kỹ Thương', 'Ky Thuong', 'NH Kỹ Thương'],
  },
  {
    code: 'VCB',
    name: 'Vietcombank',
    sector: 'bank',
    aliases: ['Ngoại Thương', 'Ngoai Thuong', 'NH Ngoại Thương'],
  },
  {
    code: 'MBB',
    name: 'MB Bank',
    sector: 'bank',
    aliases: ['Quân Đội', 'Quan Doi', 'MBBank', 'NH Quân Đội'],
  },
  {
    code: 'ACB',
    name: 'ACB',
    sector: 'bank',
    aliases: ['Á Châu', 'A Chau', 'NH Á Châu'],
  },
  {
    code: 'BID',
    name: 'BIDV',
    sector: 'bank',
    aliases: ['Đầu tư và Phát triển', 'Dau tu Phat trien', 'NH BIDV'],
  },
  {
    code: 'CTG',
    name: 'VietinBank',
    sector: 'bank',
    aliases: ['Công Thương', 'Cong Thuong', 'Vietin', 'NH Công Thương'],
  },
  {
    code: 'VPB',
    name: 'VPBank',
    sector: 'bank',
    aliases: ['Việt Nam Thịnh Vượng', 'Viet Nam Thinh Vuong', 'VPB Bank'],
  },

  // ─── Chứng khoán (5) ───────────────────────────────────────────────
  {
    code: 'SSI',
    name: 'CK SSI',
    sector: 'ck',
    aliases: ['SSI Securities', 'Sài Gòn Hà Nội Inc'],
  },
  {
    code: 'VND',
    name: 'VNDirect',
    sector: 'ck',
    aliases: ['VN Direct', 'VND Securities'],
  },
  {
    code: 'HCM',
    name: 'HSC',
    sector: 'ck',
    aliases: ['Chứng khoán TP HCM', 'HCMC Securities', 'Ho Chi Minh Securities'],
  },
  {
    code: 'VCI',
    name: 'Vietcap',
    sector: 'ck',
    aliases: ['Bản Việt', 'Ban Viet', 'CK Bản Việt'],
  },
  {
    code: 'SHS',
    name: 'SHS',
    sector: 'ck',
    aliases: ['Sài Gòn Hà Nội', 'Sai Gon Ha Noi', 'SHS Securities'],
  },

  // ─── Bất động sản (4) ──────────────────────────────────────────────
  {
    code: 'VHM',
    name: 'Vinhomes',
    sector: 'bds',
    aliases: ['Vin Homes', 'Vinhomes JSC'],
  },
  {
    code: 'NVL',
    name: 'Novaland',
    sector: 'bds',
    aliases: ['Nova Land', 'NVL Group'],
  },
  {
    code: 'KDH',
    name: 'Khang Điền',
    sector: 'bds',
    aliases: ['Khang Dien', 'Nhà Khang Điền'],
  },
  {
    code: 'DXG',
    name: 'Đất Xanh Group',
    sector: 'bds',
    aliases: ['Dat Xanh', 'Đất Xanh', 'DXG Real Estate'],
  },
];

export function getTickerInfo(code: string): TickerInfo | undefined {
  return TICKER_UNIVERSE.find((t) => t.code === code);
}

export function getSectorOption(id: Sector): SectorOption | undefined {
  return SECTORS.find((s) => s.id === id);
}
