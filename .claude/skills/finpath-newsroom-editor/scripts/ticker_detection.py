"""
Ticker detection cho Finpath Newsroom Editor.

Phase A: Regex 3 chữ uppercase (cheap, fast)
Phase B: LLM fallback nếu regex miss obvious cases (vd "Vietcombank" without "VCB")
"""

import re
from typing import Optional

# Regex pattern: 3 chữ cái uppercase đứng riêng (không phải part của 1 từ dài hơn)
TICKER_PATTERN = re.compile(r'\b([A-Z]{3})\b')


def detect_tickers(text: str) -> list[str]:
    """
    Detect ticker từ text bằng regex.
    
    Returns:
        List ticker (đã dedupe, giữ thứ tự xuất hiện)
    """
    if not text:
        return []
    
    matches = TICKER_PATTERN.findall(text)
    
    # Dedupe giữ thứ tự
    seen = set()
    result = []
    for t in matches:
        if t not in seen:
            seen.add(t)
            result.append(t)
    
    return result


def detect_tickers_with_position(text: str) -> list[tuple[str, int]]:
    """
    Detect tickers + position (for primary ticker rule).
    
    Returns:
        List of (ticker, first_position_in_text)
    """
    if not text:
        return []
    
    tickers_seen = {}
    for match in TICKER_PATTERN.finditer(text):
        ticker = match.group(1)
        if ticker not in tickers_seen:
            tickers_seen[ticker] = match.start()
    
    return sorted(tickers_seen.items(), key=lambda x: x[1])


def count_ticker_mentions(text: str, ticker: str) -> int:
    """Đếm số lần ticker xuất hiện trong text."""
    if not text or not ticker:
        return 0
    
    pattern = re.compile(rf'\b{re.escape(ticker)}\b')
    return len(pattern.findall(text))


# Common name → ticker mapping (cho LLM fallback context)
COMPANY_NAME_TO_TICKER = {
    # Bank
    "techcombank": "TCB",
    "vietcombank": "VCB",
    "mbbank": "MBB",
    "mb bank": "MBB",
    "acb": "ACB",
    "bidv": "BID",
    "vietinbank": "CTG",
    "vpbank": "VPB",
    # CK
    "vndirect": "VND",
    "hsc": "HCM",
    "bản việt": "VCI",
    # BĐS
    "vinhomes": "VHM",
    "novaland": "NVL",
    "khang điền": "KDH",
    "đất xanh": "DXG",
}


def detect_via_company_name(text: str) -> list[str]:
    """
    Fallback: detect ticker qua tên công ty (lowercase match).
    Cheap heuristic trước khi gọi LLM.
    """
    if not text:
        return []
    
    text_lower = text.lower()
    found = []
    seen = set()
    
    for name, ticker in COMPANY_NAME_TO_TICKER.items():
        if name in text_lower and ticker not in seen:
            seen.add(ticker)
            found.append(ticker)
    
    return found


def detect_combined(text: str) -> list[str]:
    """
    Combined detection: regex + company name fallback.
    Dedupe + giữ priority regex first.
    """
    by_regex = detect_tickers(text)
    by_name = detect_via_company_name(text)
    
    seen = set(by_regex)
    result = list(by_regex)
    
    for t in by_name:
        if t not in seen:
            seen.add(t)
            result.append(t)
    
    return result


# Test
if __name__ == "__main__":
    sample = """
    Vietcombank (VCB) vừa công bố kết quả kinh doanh quý 3, 
    trong khi đó Techcombank cũng có thông báo. TCB và VCB là 2 ngân hàng lớn.
    """
    
    print("Regex only:", detect_tickers(sample))
    print("With position:", detect_tickers_with_position(sample))
    print("Mentions VCB:", count_ticker_mentions(sample, "VCB"))
    print("Company names:", detect_via_company_name(sample))
    print("Combined:", detect_combined(sample))
