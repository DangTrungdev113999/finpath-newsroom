"""
Dedupe utility cho Finpath Newsroom Crawler.

Check URL đã tồn tại trong DB Newsroom Crawl Log chưa.
"""

DB_CRAWL_LOG_DS_ID = "8aad4abe-496f-480f-ad13-8996d22fe447"


def filter_existing_urls(candidate_urls: list[str], query_data_source_fn) -> set[str]:
    """
    Query DB Crawl Log để check URLs nào đã tồn tại.
    
    Args:
        candidate_urls: list URL cần check
        query_data_source_fn: callable wrapping Notion MCP query_data_sources
    
    Returns:
        Set URLs đã tồn tại (skip these khi write rows mới)
    """
    if not candidate_urls:
        return set()
    
    # Query DB filter by Link gốc trong list candidate
    # Notion API support filter "in" với list values
    existing = query_data_source_fn(
        data_source_id=DB_CRAWL_LOG_DS_ID,
        filter={
            "Link gốc": {"in": candidate_urls}
        },
        return_only=["Link gốc"]
    )
    
    return {row["Link gốc"] for row in existing if row.get("Link gốc")}


def is_new_url(url: str, existing_urls: set[str]) -> bool:
    """Check 1 URL có mới (chưa có trong DB) hay không."""
    return url not in existing_urls
