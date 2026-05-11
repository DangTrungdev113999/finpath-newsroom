/**
 * Single source of truth for the ticker universe.
 *
 * Acts as the static "API" for the filter UI. When a real backend ticker
 * endpoint comes online, swap the constants for an async fetch — the
 * `TickerInfo` shape and the `SECTORS` enum stay the same.
 *
 * Note: HDF (Bank cooperative) intentionally deferred — flagged uncertain.
 */

export type Sector = 'bank' | 'ck' | 'bds';
export type Exchange = 'HOSE' | 'HNX' | 'UPCOM';

export interface TickerInfo {
  code: string;
  name: string;
  sector: Sector;
  exchange: Exchange;
  /** Diacritic-stripped names, alt spellings, popular nicknames. */
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
  // ─── Bank · HOSE (16) ────────────────────────────────────────────────
  { code: 'VCB', name: 'Vietcombank', sector: 'bank', exchange: 'HOSE', aliases: ['Ngoại Thương', 'Ngoai Thuong', 'NH Ngoại Thương'] },
  { code: 'CTG', name: 'VietinBank', sector: 'bank', exchange: 'HOSE', aliases: ['Công Thương', 'Cong Thuong', 'Vietin'] },
  { code: 'BID', name: 'BIDV', sector: 'bank', exchange: 'HOSE', aliases: ['Đầu tư và Phát triển', 'Dau tu Phat trien'] },
  { code: 'TCB', name: 'Techcombank', sector: 'bank', exchange: 'HOSE', aliases: ['Kỹ Thương', 'Ky Thuong'] },
  { code: 'MBB', name: 'MB Bank', sector: 'bank', exchange: 'HOSE', aliases: ['Quân Đội', 'Quan Doi', 'MBBank', 'MB'] },
  { code: 'ACB', name: 'ACB', sector: 'bank', exchange: 'HOSE', aliases: ['Á Châu', 'A Chau'] },
  { code: 'VPB', name: 'VPBank', sector: 'bank', exchange: 'HOSE', aliases: ['Việt Nam Thịnh Vượng', 'Viet Nam Thinh Vuong'] },
  { code: 'HDB', name: 'HDBank', sector: 'bank', exchange: 'HOSE', aliases: ['Phát triển TP HCM', 'HD Bank'] },
  { code: 'STB', name: 'Sacombank', sector: 'bank', exchange: 'HOSE', aliases: ['Sài Gòn Thương Tín', 'Sai Gon Thuong Tin', 'Sacom'] },
  { code: 'SHB', name: 'SHB', sector: 'bank', exchange: 'HOSE', aliases: ['Sài Gòn Hà Nội Bank', 'Sai Gon Ha Noi'] },
  { code: 'EIB', name: 'Eximbank', sector: 'bank', exchange: 'HOSE', aliases: ['Xuất nhập khẩu', 'Xuat nhap khau'] },
  { code: 'TPB', name: 'TPBank', sector: 'bank', exchange: 'HOSE', aliases: ['Tiên Phong', 'Tien Phong'] },
  { code: 'MSB', name: 'MSB', sector: 'bank', exchange: 'HOSE', aliases: ['Maritime Bank', 'Hàng Hải', 'Hang Hai'] },
  { code: 'LPB', name: 'LPBank', sector: 'bank', exchange: 'HOSE', aliases: ['Lộc Phát', 'Loc Phat', 'Liên Việt', 'LienVietPostBank'] },
  { code: 'OCB', name: 'OCB', sector: 'bank', exchange: 'HOSE', aliases: ['Phương Đông', 'Phuong Dong'] },
  { code: 'VIB', name: 'VIB', sector: 'bank', exchange: 'HOSE', aliases: ['Quốc tế', 'Quoc te', 'NH Quốc tế'] },

  // ─── Bank · HNX (4) ─────────────────────────────────────────────────
  { code: 'NAB', name: 'Nam Á Bank', sector: 'bank', exchange: 'HNX', aliases: ['Nam A', 'Nam Á'] },
  { code: 'BAB', name: 'Bắc Á Bank', sector: 'bank', exchange: 'HNX', aliases: ['Bac A', 'BacABank'] },
  { code: 'NVB', name: 'NCB', sector: 'bank', exchange: 'HNX', aliases: ['Quốc Dân', 'Quoc Dan', 'National Citizen'] },
  { code: 'SGB', name: 'Saigonbank', sector: 'bank', exchange: 'HNX', aliases: ['Sài Gòn Công Thương', 'Sai Gon Cong Thuong'] },

  // ─── Bank · UPCOM (6) ───────────────────────────────────────────────
  { code: 'VAB', name: 'VietABank', sector: 'bank', exchange: 'UPCOM', aliases: ['Việt Á', 'Viet A'] },
  { code: 'BVB', name: 'Viet Capital Bank', sector: 'bank', exchange: 'UPCOM', aliases: ['Bản Việt Bank', 'Ban Viet Bank'] },
  { code: 'ABB', name: 'ABBank', sector: 'bank', exchange: 'UPCOM', aliases: ['An Bình', 'An Binh'] },
  { code: 'KLB', name: 'Kienlongbank', sector: 'bank', exchange: 'UPCOM', aliases: ['Kiên Long', 'Kien Long'] },
  { code: 'VBB', name: 'VietBank', sector: 'bank', exchange: 'UPCOM', aliases: ['Việt Nam Thương Tín', 'Viet Nam Thuong Tin'] },
  { code: 'PGB', name: 'PGBank', sector: 'bank', exchange: 'UPCOM', aliases: ['Xăng dầu Petrolimex', 'Xang dau'] },

  // ─── CK · HOSE (5) ──────────────────────────────────────────────────
  { code: 'SSI', name: 'SSI', sector: 'ck', exchange: 'HOSE', aliases: ['CK SSI', 'Sài Gòn', 'SSI Securities'] },
  { code: 'VND', name: 'VNDirect', sector: 'ck', exchange: 'HOSE', aliases: ['VN Direct', 'VND Securities'] },
  { code: 'HCM', name: 'HSC', sector: 'ck', exchange: 'HOSE', aliases: ['Chứng khoán TP HCM', 'HCMC Securities'] },
  { code: 'VCI', name: 'Vietcap', sector: 'ck', exchange: 'HOSE', aliases: ['Bản Việt', 'Ban Viet', 'CK Bản Việt'] },
  { code: 'VIX', name: 'VIX', sector: 'ck', exchange: 'HOSE', aliases: ['VnInvest', 'Vietnam Investment'] },

  // ─── CK · HNX (15) ──────────────────────────────────────────────────
  { code: 'SHS', name: 'SHS', sector: 'ck', exchange: 'HNX', aliases: ['Sài Gòn Hà Nội CK', 'Sai Gon Ha Noi'] },
  { code: 'MBS', name: 'MBS', sector: 'ck', exchange: 'HNX', aliases: ['MB Securities', 'MB CK'] },
  { code: 'BVS', name: 'BVSC', sector: 'ck', exchange: 'HNX', aliases: ['Bảo Việt CK', 'Bao Viet'] },
  { code: 'BSI', name: 'BSC', sector: 'ck', exchange: 'HNX', aliases: ['BIDV Securities', 'BIDV CK'] },
  { code: 'AGR', name: 'Agriseco', sector: 'ck', exchange: 'HNX', aliases: ['Agribank CK', 'Agribank Securities'] },
  { code: 'CTS', name: 'CTS', sector: 'ck', exchange: 'HNX', aliases: ['VietinBank Securities', 'Vietin CK'] },
  { code: 'APG', name: 'APG', sector: 'ck', exchange: 'HNX', aliases: ['APG Securities'] },
  { code: 'EVS', name: 'Everest', sector: 'ck', exchange: 'HNX', aliases: ['Everest Securities', 'Everest CK'] },
  { code: 'IVS', name: 'IVS', sector: 'ck', exchange: 'HNX', aliases: ['Đầu tư Việt Nam', 'Dau tu Viet Nam'] },
  { code: 'PSI', name: 'PSI', sector: 'ck', exchange: 'HNX', aliases: ['Dầu khí', 'Dau khi', 'Petrosetco'] },
  { code: 'TVS', name: 'Thiên Việt', sector: 'ck', exchange: 'HNX', aliases: ['Thien Viet', 'TVS Securities'] },
  { code: 'WSS', name: 'Phố Wall', sector: 'ck', exchange: 'HNX', aliases: ['Pho Wall', 'Wall Street'] },
  { code: 'ORS', name: 'TPS', sector: 'ck', exchange: 'HNX', aliases: ['Tiên Phong CK', 'Tien Phong Securities'] },
  { code: 'VFS', name: 'Nhất Việt', sector: 'ck', exchange: 'HNX', aliases: ['Nhat Viet CK', 'NVS'] },
  { code: 'TCI', name: 'Thành Công', sector: 'ck', exchange: 'HNX', aliases: ['Thanh Cong', 'TCI Securities'] },

  // ─── CK · UPCOM (10) ────────────────────────────────────────────────
  { code: 'DSC', name: 'DSC', sector: 'ck', exchange: 'UPCOM', aliases: ['Đông Sài Gòn', 'Dong Sai Gon'] },
  { code: 'FTS', name: 'FPTS', sector: 'ck', exchange: 'UPCOM', aliases: ['FPT Securities', 'FPT CK'] },
  { code: 'CSI', name: 'CSI', sector: 'ck', exchange: 'UPCOM', aliases: ['Kiến Thiết', 'Kien Thiet'] },
  { code: 'SBS', name: 'SBSC', sector: 'ck', exchange: 'UPCOM', aliases: ['Sacombank Securities', 'Sacombank CK'] },
  { code: 'PHS', name: 'Phú Hưng', sector: 'ck', exchange: 'UPCOM', aliases: ['Phu Hung', 'PHS Securities'] },
  { code: 'ART', name: 'BOS', sector: 'ck', exchange: 'UPCOM', aliases: ['BOS Securities', 'ART CK'] },
  { code: 'APS', name: 'APEC', sector: 'ck', exchange: 'UPCOM', aliases: ['APEC Securities', 'Châu Á Thái Bình Dương'] },
  { code: 'BMS', name: 'Bảo Minh CK', sector: 'ck', exchange: 'UPCOM', aliases: ['Bao Minh', 'BMS Securities'] },
  { code: 'AAS', name: 'Smart Invest', sector: 'ck', exchange: 'UPCOM', aliases: ['SmartInvest', 'AAS Securities'] },
  { code: 'VTS', name: 'Việt Tín', sector: 'ck', exchange: 'UPCOM', aliases: ['Viet Tin', 'VTS Securities'] },

  // ─── BĐS · HOSE (23) ────────────────────────────────────────────────
  // BĐS dân cư + retail RE (KCN deferred per CLAUDE.md — KBC etc.)
  { code: 'VHM', name: 'Vinhomes', sector: 'bds', exchange: 'HOSE', aliases: ['Vin Homes'] },
  { code: 'NVL', name: 'Novaland', sector: 'bds', exchange: 'HOSE', aliases: ['Nova Land', 'NVL Group'] },
  { code: 'KDH', name: 'Khang Điền', sector: 'bds', exchange: 'HOSE', aliases: ['Khang Dien'] },
  { code: 'DXG', name: 'Đất Xanh Group', sector: 'bds', exchange: 'HOSE', aliases: ['Dat Xanh', 'DXG Real Estate'] },
  { code: 'VRE', name: 'Vincom Retail', sector: 'bds', exchange: 'HOSE', aliases: ['Vincom', 'Vin Retail'] },
  { code: 'PDR', name: 'Phát Đạt', sector: 'bds', exchange: 'HOSE', aliases: ['Phat Dat', 'PDR Real Estate'] },
  { code: 'DIG', name: 'DIC Group', sector: 'bds', exchange: 'HOSE', aliases: ['DIC Corp', 'Phát triển Xây dựng'] },
  { code: 'NLG', name: 'Nam Long', sector: 'bds', exchange: 'HOSE', aliases: ['Nam Long Investment', 'NLG Group'] },
  { code: 'HDG', name: 'Hà Đô', sector: 'bds', exchange: 'HOSE', aliases: ['Ha Do', 'Hà Đô Group'] },
  { code: 'HDC', name: 'Hodeco', sector: 'bds', exchange: 'HOSE', aliases: ['Phát triển Nhà BR-VT', 'Bà Rịa Vũng Tàu'] },
  { code: 'CRE', name: 'CenLand', sector: 'bds', exchange: 'HOSE', aliases: ['Cen Land', 'Cen Group'] },
  { code: 'AGG', name: 'An Gia', sector: 'bds', exchange: 'HOSE', aliases: ['An Gia Investment', 'AGG Real Estate'] },
  { code: 'HQC', name: 'Hoàng Quân', sector: 'bds', exchange: 'HOSE', aliases: ['Hoang Quan', 'Địa ốc Hoàng Quân'] },
  { code: 'SCR', name: 'TTC Land', sector: 'bds', exchange: 'HOSE', aliases: ['Sài Gòn Thương Tín RE', 'TTC'] },
  { code: 'QCG', name: 'Quốc Cường Gia Lai', sector: 'bds', exchange: 'HOSE', aliases: ['Quoc Cuong Gia Lai', 'QCG'] },
  { code: 'LDG', name: 'LDG Group', sector: 'bds', exchange: 'HOSE', aliases: ['LDG Investment'] },
  { code: 'SJS', name: 'Sudico', sector: 'bds', exchange: 'HOSE', aliases: ['Sông Đà Urban', 'Song Da'] },
  { code: 'ITC', name: 'Intresco', sector: 'bds', exchange: 'HOSE', aliases: ['ITC Real Estate', 'Đầu tư XD Kinh doanh'] },
  { code: 'KHG', name: 'Khải Hoàn Land', sector: 'bds', exchange: 'HOSE', aliases: ['Khai Hoan Land', 'KHG Real Estate'] },
  { code: 'VPI', name: 'Văn Phú Invest', sector: 'bds', exchange: 'HOSE', aliases: ['Van Phu Invest', 'VPI Group'] },
  { code: 'TCH', name: 'Hoàng Huy', sector: 'bds', exchange: 'HOSE', aliases: ['Hoang Huy', 'TCH Group'] },
  { code: 'DXS', name: 'Đất Xanh Services', sector: 'bds', exchange: 'HOSE', aliases: ['Dat Xanh Services', 'DXS'] },
  { code: 'NTL', name: 'Lideco', sector: 'bds', exchange: 'HOSE', aliases: ['Phát triển Đô thị Từ Liêm', 'Tu Liem Urban'] },

  // ─── BĐS · HNX (5) ──────────────────────────────────────────────────
  { code: 'CEO', name: 'CEO Group', sector: 'bds', exchange: 'HNX', aliases: ['CEO Real Estate'] },
  { code: 'HUT', name: 'Tasco', sector: 'bds', exchange: 'HNX', aliases: ['HUT Real Estate'] },
  { code: 'VC3', name: 'Vinaconex 3', sector: 'bds', exchange: 'HNX', aliases: ['Vinaconex VC3', 'VC3 Real Estate'] },
  { code: 'TIG', name: 'TIG Group', sector: 'bds', exchange: 'HNX', aliases: ['TIG Real Estate'] },
  { code: 'API', name: 'APEC Investment', sector: 'bds', exchange: 'HNX', aliases: ['APEC Group BĐS'] },
];

export function getTickerInfo(code: string): TickerInfo | undefined {
  return TICKER_UNIVERSE.find((t) => t.code === code);
}

export function getSectorOption(id: Sector): SectorOption | undefined {
  return SECTORS.find((s) => s.id === id);
}
