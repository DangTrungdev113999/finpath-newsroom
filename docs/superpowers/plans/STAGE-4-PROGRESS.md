# Stage 4 Progress — Plan G Foreign Flow API + Plan F Task 16

> **Last updated**: 2026-05-12 evening (Stage 4 COMPLETE).
> **Master sequence**: `docs/superpowers/plans/2026-05-12-MASTER-EXECUTION-SEQUENCE.md`

## Status: ✅ COMPLETE — 8/9 task done (G-7 BLOCKED → Stage 6)

**Gate 4 verification PASSED**: 402 passed + 7 deselected default suite. Live `-m integration`: 7/7 pass (4 G-3 + 3 G-8 against `api.finpath.vn`).

9 commits added Stage 4 (commits `7774855` → `fc45eb6`).

## Task summary — Plan G V1.1 PATCH

V1.1 dropped: `lib/foreign_flow.py` top compute • `/tin-hot` auto-enrich • Editor V1 foreign stamp • Master Step 4.5 foreign check • pipeline_log nested foreign field.

V1.1 keeps: 3 API methods + SQLite cache + judgment guides + smoke tests.

### Phase 1 — API client extension (G-1 to G-3)

| Task | Subject | Commit |
|---|---|---|
| ✅ G-1 | SQLite finpath_foreign_cache migration | `7774855` |
| ✅ G-2 | lib/finpath_api.py 3 methods + cache helpers | `12238b1` |
| ✅ G-3 | Live API smoke (4 integration tests) | `2fd790e` + `c41e922` |

G-3 follow-up commit `c41e922` registers `integration` marker in pyproject.toml with `addopts = "-m 'not integration'"` so default suite skips live API tests.

### Phase 2 — Judgment guides (G-4 to G-6)

| Task | Subject | Commit |
|---|---|---|
| ✅ G-4 | Story Editor foreign-flow-when-to-call reference + SKILL.md register | `c793190` |
| ✅ G-5 | 10 Master skills foreign-flow reference (template + 9 copies) | `a700579` |
| ✅ G-6 | 10 Master SKILL.md register foreign-flow reference | `3d65fdc` |

### Phase 3 — Verification + Plan F Task 16 (G-7 to G-8)

| Task | Subject | Commit |
|---|---|---|
| ⏸ G-7 | CLAUDE.md aggregate (BLOCKED → Stage 6) | — |
| ✅ G-8 | Master integration smoke test | `fc45eb6` |
| ✅ Plan F Task 16 | Spec A V1.2 PATCH NOTICE universe intersect 61→139 | `e276c7c` |

## Test count

- Default suite: **402 passed, 7 deselected** (skip integration)
- Live integration suite (opt-in `-m integration`): **7 passed** (4 foreign flow smoke + 3 master uses smoke)
- New tests added during Stage 4: **8** unit + **7** integration

## Architecture state after Stage 4

### lib/finpath_api.py FinpathAPI class — Group F: Foreign flow

```python
# Constructor V5.1.3
FinpathAPI(base_url="https://api.finpath.vn", timeout=10, db=None)

# 3 new methods
api.get_foreign_rooms() -> list[dict]                        # all snapshot, TTL 900s
api.get_foreign_roomstatistics(ticker, period="1D") -> dict  # per-ticker, TTL 3600s, period ∈ {1D,1W,1M,3M,6M,1Y}
api.get_foreign_roombars(ticker) -> list[dict]               # time series, TTL 21600s

# Cache helpers (private)
_sqlite_cached_get / _sqlite_cache_lookup / _sqlite_cache_set / _fetch_api / _unwrap
```

### SQLite schema

```sql
CREATE TABLE finpath_foreign_cache (
    cache_key TEXT PRIMARY KEY,    -- "rooms" | "roomstat:VHM:1W" | "roombars:VHM"
    endpoint TEXT NOT NULL,        -- "/v2/rooms" | "/roomstatistics" | "/roombars"
    payload JSON NOT NULL,
    fetched_at TIMESTAMP NOT NULL,
    ttl_seconds INTEGER NOT NULL   -- 900 | 3600 | 21600
);
CREATE INDEX idx_foreign_cache_fetched ON finpath_foreign_cache(fetched_at);
```

### Behavior

- Cache miss → API → persist → return
- Cache hit (age < ttl) → return cached, no API
- Cache stale + API ok → refresh + return new
- Cache stale + API down → return stale + log warning
- No cache + API down → `RuntimeError`

### Agents updated

- `.claude/skills/finpath-newsroom-story-editor/references/foreign-flow-when-to-call.md` — judgment 3 triggers + 4-quadrant matrix
- `.claude/skills/finpath-newsroom-master-{bank,ck,bds,oilgas,logistics,fb,apparel,retail,seafood,defensive}/references/foreign-flow-when-to-call.md` — 10 mechanical duplicates (per CLAUDE.md no-shared rule)
- 11 SKILL.md (1 story editor + 10 master) register reference load

### Plan A V1.2 PATCH NOTICE

`docs/superpowers/plans/2026-05-12-hot-ticker-trigger.md` head — `/tin-hot N` intersect set switches from hardcoded `FULL_UNIVERSE` (61) to `FinpathSectors.get_all_cached_tickers()` (~139). NO foreign auto-enrichment (Spec G V1.1 PATCH reverted).

## Gate 4 verification

```bash
uv run pytest tests/test_finpath_foreign_cache_schema.py \
              tests/test_finpath_api_foreign.py -v
# 11 passed (3 schema + 8 api unit)

uv run pytest tests/integration/test_foreign_flow_smoke.py \
              tests/integration/test_master_uses_foreign_flow.py -v -m integration
# 7 passed (live API)

uv run pytest -q
# 402 passed, 7 deselected (default suite — integration skipped)
```

## Next: Stage 5 — Plan H Pipeline Run History

Per MASTER-EXECUTION-SEQUENCE.md + advisor flag from Stage 3 review:

> User requirement (compact-args): "phần này cho mỗi bài viết không cần nữa, nhưng không bỏ, tôi cần vẫn cần đọc để biết pipeline đó chạy thì bao nhiêu tin được tìm thấy, reject tin nào lý do reject. giờ bố trí cái crawl funnel đó ở đâu thì hợp lý dể xem được lịch sử những lần chạy"

Stage 5 must include:
- Crawl funnel section REMOVED from per-article view (ArticleLoader)
- Crawl funnel data MOVED to per-pipeline-run view (history page)
- New nav item "Lịch sử pipeline" linking to history page
- Per-run: fetched / selected / rejected + reasons

Verify `docs/superpowers/specs/2026-05-12-pipeline-run-history-design.md` V1.0.1 captures these before plan execution.

## Known deferred items

- G-7 CLAUDE.md update — Stage 6 aggregate (data sourcing rule note + foreign flow data source)
- Spec G §10/§11 sections dropped (V1.1 PATCH) — not implemented intentionally

## Cumulative ahead of origin

Stage 1: 63 commits. Stage 2: 8. Stage 3: 8. Stage 4: 9. **Total ahead: ~88 commits**.

User instruction: "đúng ui đừng push lên main vội" — kept local.
