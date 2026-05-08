"""
Dedupe utility cho Finpath Newsroom Crawler.

Check URL đã tồn tại trong crawl_log (data/pipeline.db) chưa.
"""
from __future__ import annotations
from lib.pipeline_db import PipelineDB


def filter_existing_urls(candidate_urls: list[str], db: PipelineDB) -> set[str]:
    """
    Query crawl_log để check URLs nào đã tồn tại.

    Args:
        candidate_urls: list URL cần check
        db: PipelineDB instance wrapping data/pipeline.db

    Returns:
        Set URLs đã tồn tại (skip these khi write rows mới)
    """
    if not candidate_urls:
        return set()

    placeholders = ",".join("?" for _ in candidate_urls)
    cur = db.conn.execute(
        f"SELECT source_url FROM crawl_log WHERE source_url IN ({placeholders})",
        candidate_urls,
    )
    return {row["source_url"] for row in cur.fetchall() if row["source_url"]}


def is_new_url(url: str, existing_urls: set[str]) -> bool:
    """Check 1 URL có mới (chưa có trong crawl_log) hay không."""
    return url not in existing_urls
