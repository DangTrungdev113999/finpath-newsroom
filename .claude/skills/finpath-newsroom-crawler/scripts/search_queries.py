"""
Search query builder cho Finpath Newsroom Crawler.

Build các query khác nhau để search nhiều góc tin về 1 ticker:
- Ticker + tên công ty
- Ticker + KQKD
- Ticker + cổ phiếu tin tức
- Ticker + sector keyword
"""

from .source_whitelist import get_company_name, SECTOR_KEYWORDS


def build_queries(ticker: str, sector: str) -> list[str]:
    """
    Build 4 query variants cho ticker.
    
    Args:
        ticker: vd "VCB"
        sector: vd "Bank"
    
    Returns:
        List of query strings (4 queries)
    """
    ticker = ticker.upper()
    company_name = get_company_name(ticker)
    sector_keyword = SECTOR_KEYWORDS.get(sector, "")
    
    queries = [
        f"{ticker} {company_name}",
        f"{ticker} kết quả kinh doanh",
        f"{ticker} cổ phiếu tin tức",
    ]
    
    if sector_keyword:
        queries.append(f"{ticker} {sector_keyword}")
    
    return queries


def build_query_with_site(query: str, domain: str) -> str:
    """Append site: filter to query for nguồn-specific search."""
    return f"{query} site:{domain}"


# Test
if __name__ == "__main__":
    qs = build_queries("VCB", "Bank")
    print("Queries for VCB Bank:")
    for q in qs:
        print(f"  - {q}")
    
    print("\nWith site filter (cafef.vn):")
    for q in qs:
        print(f"  - {build_query_with_site(q, 'cafef.vn')}")
