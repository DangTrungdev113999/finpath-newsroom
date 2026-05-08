"""
Source whitelist + universe constants for Finpath Newsroom Crawler V2.4.

20 nguồn báo chí Việt Nam (cập nhật 07/05/2026 — bỏ SSI/VND sell-side,
thêm 14 nguồn tài chính/báo phổ biến mọi người hay đọc).
"""

# 20 nguồn whitelist V2.4
SOURCES_WHITELIST = {
    # Tier 1 — Tài chính chuyên (8 nguồn)
    "CafeF": "cafef.vn",
    "VietnamBiz": "vietnambiz.vn",
    "Vietstock": "vietstock.vn",
    "Tinnhanh CK": "tinnhanhchungkhoan.vn",
    "FireAnt": "fireant.vn",
    "VnEconomy": "vneconomy.vn",
    "Báo Đầu tư": "baodautu.vn",
    "Nhịp sống KD": "nhipsongkinhdoanh.vn",

    # Tier 2 — Báo tổng hợp KD (5 nguồn)
    "VnExpress KD": "vnexpress.net",
    "Tuổi Trẻ KD": "tuoitre.vn",
    "Thanh Niên KD": "thanhnien.vn",
    "Dân Trí KD": "dantri.com.vn",
    "ZNews KD": "znews.vn",

    # Tier 3 — Báo doanh nghiệp/specialized (3 nguồn)
    "Báo Pháp luật": "baophapluat.vn",
    "The LEADER": "theleader.vn",
    "Doanh nhân SG": "doanhnhansaigon.vn",

    # Tier 4 — Nhà nước + sector specialized (4 nguồn)
    "NHNN": "sbv.gov.vn",
    "UBCKNN": "ssc.gov.vn",
    "Bộ Xây dựng": "xaydung.gov.vn",
    "CafeLand": "cafeland.vn",
}

# Total: 20 nguồn × 3 tin mới nhất/nguồn = 60 candidates max per ticker call

# DEPRECATED V2.4 (07/05/2026) — bỏ vì user feedback "lấy nguồn mọi người hay đọc, không sell-side":
# - SSI (ssi.com.vn) — sell-side research, low frequency news
# - VND (vndirect.com.vn) — sell-side research, low frequency news
# Note: SSI/VND vẫn có trong DB Crawl Log Nguồn options (legacy data),
# nhưng crawler V2.4 KHÔNG dùng nữa.

# M1 scope: Bank only
BANK_UNIVERSE = ["TCB", "VCB", "MBB", "ACB", "BID", "CTG", "VPB"]

# Full universe (M2+)
FULL_UNIVERSE = {
    "CK": ["SSI", "VND", "HCM", "VCI", "SHS"],
    "BĐS": ["VHM", "NVL", "KDH", "DXG"],
    "Bank": BANK_UNIVERSE,
}

# Mapping ticker → tên công ty (cho search query)
TICKER_NAMES = {
    # Bank
    "TCB": "Techcombank",
    "VCB": "Vietcombank",
    "MBB": "MBBank",
    "ACB": "ACB",
    "BID": "BIDV",
    "CTG": "VietinBank",
    "VPB": "VPBank",
    # CK
    "SSI": "Chứng khoán SSI",
    "VND": "VNDirect",
    "HCM": "HSC",
    "VCI": "Chứng khoán Bản Việt",
    "SHS": "Chứng khoán Sài Gòn Hà Nội",
    # BĐS
    "VHM": "Vinhomes",
    "NVL": "Novaland",
    "KDH": "Khang Điền",
    "DXG": "Đất Xanh",
}


def get_sector_for_ticker(ticker: str) -> str:
    """Return sector name for a given ticker. Raises ValueError if not in universe."""
    for sector, tickers in FULL_UNIVERSE.items():
        if ticker in tickers:
            return sector
    raise ValueError(f"Ticker {ticker} not in universe")
