-- Migration: finpath_foreign_cache table for V5.1.3 foreign flow API
-- Hybrid TTL per endpoint:
--   /v2/rooms: 900s (15 min)
--   /roomstatistics/{code}: 3600s (1 h)
--   /roombars/{code}: 21600s (6 h)

CREATE TABLE IF NOT EXISTS finpath_foreign_cache (
    cache_key TEXT PRIMARY KEY,
    endpoint TEXT NOT NULL,
    payload JSON NOT NULL,
    fetched_at TIMESTAMP NOT NULL,
    ttl_seconds INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_foreign_cache_fetched
    ON finpath_foreign_cache(fetched_at);
