"""
Routing logic cho Finpath Newsroom Editor (M2).

4 chức năng:
1. filter_universe — giữ ticker thuộc universe (M2: full 16 mã)
2. identify_primary_ticker — rule 4 bước
3. worth_writing — simple heuristic check
4. get_sector — lookup ticker → sector (Bank/CK/BĐS)
"""

from .ticker_detection import detect_tickers_with_position, count_ticker_mentions


# Universe constants
BANK_UNIVERSE = [
    # HOSE (16)
    "VCB", "CTG", "BID", "TCB", "MBB", "ACB", "VPB", "HDB",
    "STB", "SHB", "EIB", "TPB", "MSB", "LPB", "OCB", "VIB",
    # HNX (4)
    "NAB", "BAB", "NVB", "SGB",
    # UPCOM (7)
    "VAB", "BVB", "ABB", "KLB", "VBB", "PGB", "HDF",
]  # 27 mã
CK_UNIVERSE = [
    # HOSE (5)
    "SSI", "VND", "HCM", "VCI", "VIX",
    # HNX (15)
    "SHS", "MBS", "BVS", "BSI", "AGR", "CTS", "APG", "EVS",
    "IVS", "PSI", "TVS", "WSS", "ORS", "VFS", "TCI",
    # UPCOM (10)
    "DSC", "FTS", "CSI", "SBS", "PHS", "ART", "APS", "BMS", "AAS", "VTS",
]  # 30 mã
BDS_UNIVERSE = ["VHM", "NVL", "KDH", "DXG"]  # 4 mã (unchanged)
FULL_UNIVERSE = BANK_UNIVERSE + CK_UNIVERSE + BDS_UNIVERSE  # 61 mã
ALL_TICKERS = FULL_UNIVERSE  # alias

# Reverse lookup ticker → sector
TICKER_TO_SECTOR = {}
for t in BANK_UNIVERSE:
    TICKER_TO_SECTOR[t] = "Bank"
for t in CK_UNIVERSE:
    TICKER_TO_SECTOR[t] = "CK"
for t in BDS_UNIVERSE:
    TICKER_TO_SECTOR[t] = "BĐS"


def get_sector(ticker: str) -> str | None:
    """Return sector của ticker (Bank/CK/BĐS), hoặc None nếu không trong universe."""
    return TICKER_TO_SECTOR.get(ticker.upper())


def filter_universe(tickers: list[str], universe: list[str] = None) -> list[str]:
    """
    Giữ tickers nằm trong universe.
    
    Args:
        tickers: list ticker phát hiện được
        universe: list universe (default: M1 Bank only)
    
    Returns:
        Filtered list
    """
    if universe is None:
        universe = FULL_UNIVERSE  # M2 default — full 16 mã
    
    return [t for t in tickers if t in universe]


def identify_primary_ticker(
    valid_tickers: list[str],
    title: str,
    content: str
) -> str | None:
    """
    Identify primary ticker theo rule 4 bước:
    1. Ticker xuất hiện trong title → primary
    2. Earliest mention trong body → primary
    3. Highest frequency → primary
    4. Alphabetical → primary
    
    Args:
        valid_tickers: list ticker đã filter universe
        title: tiêu đề tin
        content: nội dung tin
    
    Returns:
        1 ticker primary, hoặc None nếu valid_tickers empty
    """
    if not valid_tickers:
        return None
    
    if len(valid_tickers) == 1:
        return valid_tickers[0]
    
    # Rule 1: trong title
    tickers_in_title = [t for t in valid_tickers if t in title]
    if len(tickers_in_title) == 1:
        return tickers_in_title[0]
    if len(tickers_in_title) > 1:
        # multiple tickers in title → continue with these
        valid_tickers = tickers_in_title
    
    # Rule 2: earliest mention trong body
    positions = detect_tickers_with_position(content)
    valid_positions = [(t, pos) for t, pos in positions if t in valid_tickers]
    
    if valid_positions:
        earliest_ticker, earliest_pos = valid_positions[0]
        # Check unique earliest
        same_pos = [t for t, p in valid_positions if p == earliest_pos]
        if len(same_pos) == 1:
            return earliest_ticker
    
    # Rule 3: highest frequency
    freq = {t: count_ticker_mentions(title + " " + content, t) for t in valid_tickers}
    max_freq = max(freq.values())
    most_freq = [t for t, f in freq.items() if f == max_freq]
    
    if len(most_freq) == 1:
        return most_freq[0]
    
    # Rule 4: alphabetical
    return sorted(most_freq)[0]


# Heuristic keywords cho worth_writing check
SPAM_KEYWORDS = [
    "khuyến mãi", "giảm giá", "ưu đãi", "đăng ký ngay",
    "nhập mã", "nhận quà", "trúng thưởng",
]

LOW_CONTENT_THRESHOLD = 100  # chars


def worth_writing(row_data: dict, primary_ticker: str) -> tuple[bool, str]:
    """
    M1 simple heuristic check tin worth viết.
    
    Args:
        row_data: row từ DB Crawl Log với Tiêu đề + Nội dung thô
        primary_ticker: primary ticker đã identify
    
    Returns:
        (is_worth, reason): is_worth=True nếu pass, reason string giải thích
    """
    title = row_data.get("Tiêu đề", "")
    content = row_data.get("Nội dung thô", "")
    
    # Check 1: nội dung đủ dài
    if len(content) < LOW_CONTENT_THRESHOLD:
        return False, f"Nội dung quá ngắn ({len(content)} chars < {LOW_CONTENT_THRESHOLD})"
    
    # Check 2: title chứa ticker hoặc tên công ty (heuristic)
    if primary_ticker not in title:
        # Check tên công ty trong title (lowercase compare)
        from .ticker_detection import COMPANY_NAME_TO_TICKER
        title_lower = title.lower()
        company_in_title = any(
            name in title_lower 
            for name, t in COMPANY_NAME_TO_TICKER.items() 
            if t == primary_ticker
        )
        if not company_in_title:
            return False, f"Title không nhắc {primary_ticker} hoặc tên công ty"
    
    # Check 3: không phải spam/quảng cáo
    text_lower = (title + " " + content).lower()
    spam_hits = [kw for kw in SPAM_KEYWORDS if kw in text_lower]
    if len(spam_hits) >= 2:
        return False, f"Có vẻ spam/quảng cáo: {spam_hits}"
    
    return True, "OK"


# Test
if __name__ == "__main__":
    tickers = ["VCB", "TCB", "ACB"]
    title = "VCB công bố KQKD quý 3"
    content = "Vietcombank vừa công bố lợi nhuận. TCB cũng có thông báo. VCB tăng trưởng tốt. VCB và VCB."
    
    print("Universe filter:", filter_universe(tickers, BANK_UNIVERSE))
    print("Primary:", identify_primary_ticker(tickers, title, content))
    
    row = {"Tiêu đề": title, "Nội dung thô": content}
    print("Worth writing:", worth_writing(row, "VCB"))
    
    spam_row = {"Tiêu đề": "VCB khuyến mãi", "Nội dung thô": "Khuyến mãi đăng ký ngay nhận quà " * 5}
    print("Spam check:", worth_writing(spam_row, "VCB"))
