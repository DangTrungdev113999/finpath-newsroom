---
description: Viết bài tin chuyên sâu cho NHIỀU mã cổ phiếu Bank cùng lúc (parallel pipelines)
argument-hint: <TICKER1,TICKER2,TICKER3,...>
allowed-tools: Bash, Task, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

Trigger N pipeline 6-step Newsroom V4.0 PARALLEL cho list tickers comma-separated **$ARGUMENTS**.

Universe MVP Bank: **TCB · VCB · MBB · ACB · BID · CTG · VPB**.

## Parse $ARGUMENTS

1. **Empty $ARGUMENTS** → reply usage:
   ```
   Usage: /tin-batch <TICKER1,TICKER2,...>
   Example: /tin-batch ACB,TPB,VPB
   Single ticker: /tin-batch VCB (fall back to /tin behavior)
   ```
   Stop.

2. **Single ticker no comma** (vd `/tin-batch VCB`) → fall back to `/tin VCB` behavior:
   - Single Task dispatch `newsroom-pipeline` với ticker=VCB
   - Same output format as /tin

3. **Comma-separated** (vd `/tin-batch ACB,TPB,VPB`) → split → list of N tickers.

## Validate tickers

For mỗi ticker trong list:
- Strip whitespace + uppercase
- Map alias: Vietcombank→VCB, Techcombank→TCB, BIDV→BID, VietinBank→CTG, MB Bank→MBB, ACB→ACB, VPBank→VPB
- Check membership trong UNIVERSE = `{TCB, VCB, MBB, ACB, BID, CTG, VPB}`
- Invalid → log warn `⚠️ Skip ticker [X] — không thuộc MVP Bank universe` + remove khỏi list (KHÔNG crash whole batch)

Nếu sau validation 0 ticker hợp lệ → reply "Không có ticker hợp lệ trong universe MVP Bank" + stop.

## Spawn parallel pipelines

Single message với N Task tool calls — Claude Code runs parallel:

```
Task tool call 1: subagent_type=newsroom-pipeline, prompt="ticker=ACB ..."
Task tool call 2: subagent_type=newsroom-pipeline, prompt="ticker=TPB ..."
Task tool call 3: subagent_type=newsroom-pipeline, prompt="ticker=VPB ..."
```

Mỗi pipeline có own `funnel_batch_id` (timestamp + ticker) → no row collision.

Prereqs (Phase G):
- **WAL mode** (T1) handles SQLite write serialization automatically
- **Atomic manifest write** (T6) handles output/compare-feed/manifest.json race
- Existing `crawl_log.source_url` UNIQUE constraint catches dup URLs across batches

## Aggregate output

Sau khi all N pipelines return, format final reply:

```
✅ Pipeline /tin-batch <TICKER1,TICKER2,...> hoàn tất

[per ticker block]
📊 ACB:
  - Funnel batch: ACB-YYYYMMDD-HHMM
  - Crawled: N rows
  - Articles: M published
  - Files: output/compare-feed/ACB-...
  - Telegram: K pushed (X failed)

📊 TPB:
  ...

📊 VPB:
  ...

Total: <N tickers> × <avg articles per ticker> = <total> articles
Total Telegram: <K> pushed
Total wall-clock: <T>s (parallel speedup vs <T_seq>s sequential = X.Yx)
```

## Edge cases

- **1 pipeline crashes** → other pipelines continue (Task isolation). Log error + skip in aggregate report.
- **Skipped invalid tickers** → list at top of reply ("⚠️ Bỏ qua: [X, Y]").
- **0 valid tickers** → reply stop message (see Validate section above).
- **All pipelines reject (0 articles each)** → aggregate "Batch không đủ chất lượng cho tất cả tickers — xem reject reasons per ticker."
