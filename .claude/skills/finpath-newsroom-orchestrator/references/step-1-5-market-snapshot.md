# Step 1.5 — Market Snapshot (Python self-execute)

> Loaded from `Skill: finpath-newsroom-orchestrator` references. Mechanical Python soft-fetch — orchestrator may run inline (same pattern as Step 1 Crawler and Step 6 Render).

## Purpose

Fetch ticker quote (price + percent change) via Finpath API. Result passed downstream to Format Director (Step 3.5) via `brief.ticker_market_data`. Drives `tone_bias` selection.

## Soft fetch semantic

Failure → `None`, do NOT block pipeline. Format Director must handle `ticker_market_data=null` gracefully.

## Invocation

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.stages.run_market_snapshot import fetch_market_snapshot
snap = fetch_market_snapshot('<TICKER>')
print(json.dumps(snap.to_dict() if snap else None, ensure_ascii=False))
" > /tmp/market_snapshot.json
```

Read `/tmp/market_snapshot.json`:
- Success → `{"price": 89500.0, "pct_change": -1.23, "as_of": "2026-05-12T09:30:00Z", ...}`
- Soft fail → `null`

## Observability emit (defer persist to after Step 4)

```python
import time
from datetime import datetime, timezone

started_at_market = datetime.now(timezone.utc).isoformat()
t0_market = time.time()

# ... run fetch_market_snapshot ...
snapshot_dict_or_none = json.loads(open('/tmp/market_snapshot.json').read())

payload_market = {
    "model": "python",
    "started_at": started_at_market,
    "duration_ms": int((time.time() - t0_market) * 1000),
    "tokens": None,
    "result": snapshot_dict_or_none,
    "soft_failed": (snapshot_dict_or_none is None),
}
# Defer log_pipeline_step(article_id, "step_1_5_market_snapshot", payload_market)
# to AFTER Step 4 — same batch-level duplication pattern as Step 1 / 6.
```

## Downstream contract

Pass to Format Director Task input:

```json
{
  "brief": { ... },
  "ticker_market_data": {"price": 89500.0, "pct_change": -1.23, "as_of": "..."}
  // OR: "ticker_market_data": null
}
```

Format Director uses `pct_change` sign for tone bias:
- `> +2%` → bullish tone, format candidates lean optimistic
- `< -2%` → bearish/defensive tone, format candidates lean cautious
- between → neutral
- `null` → fallback neutral (no bias applied)

## Failure modes

- Ticker not in Finpath universe → `None` (no crash)
- API timeout → `None` (10s default)
- Auth fail → `None` + stderr warning (does NOT block)

Pipeline continues regardless. Format Director receives null safely.

## Why Python-inline (acceptable shortcut)

Mechanical fetch, no LLM reasoning. Same architectural intent as Step 1 (Crawler runs WebSearch + WebFetch + Python script) and Step 6 (render_compare_feed.py). No subagent needed because there is no judgment to delegate.

## Position in pipeline

```
Step 1 Crawler → Step 1.5 Market Snapshot → Step 2 Editor V1 → Step 3 Story Editor → Step 3.5 Format Director → ...
```

Step 1.5 outputs into Step 3.5 input (via brief enrichment), not Step 2. Sequencing: run after Step 1 (need ticker), before Step 3.5 (need market_data for tone_bias).
