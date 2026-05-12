-- Migration: Add finpath_sectors_cache table for V5.1.3 universe expansion
-- TTL 365 days for sector mapping (user feedback: data này 1 năm mới thay đổi 1 lần)

CREATE TABLE IF NOT EXISTS finpath_sectors_cache (
    ticker TEXT PRIMARY KEY,
    sector_code TEXT NOT NULL,
    sector_name TEXT NOT NULL,
    sector_parent TEXT,
    exchange TEXT,
    fetched_at TIMESTAMP NOT NULL,
    pe REAL,
    pb REAL,
    eps REAL,
    roa REAL,
    roe REAL,
    mc REAL
);

CREATE INDEX IF NOT EXISTS idx_finpath_cache_sector
    ON finpath_sectors_cache(sector_code);
