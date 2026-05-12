---
description: Viết bài tin chuyên sâu cho NHIỀU mã cổ phiếu cùng lúc (parallel pipelines, đa sector Bank/CK/BĐS)
argument-hint: <TICKER1,TICKER2,TICKER3,...>
allowed-tools: Bash, Task, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, mcp__tavily__tavily_search
---

Trigger N pipeline 6-step Newsroom V4.0 PARALLEL cho list tickers comma-separated **$ARGUMENTS**.

FULL_UNIVERSE 61 mã (3 sector):
- **Bank** (27): HOSE 16 + HNX 4 + UPCOM 7 (see routing.BANK_UNIVERSE)
- **CK** (30): HOSE 5 + HNX 15 + UPCOM 10 (see routing.CK_UNIVERSE)
- **BĐS** (4): VHM · NVL · KDH · DXG (KBC defer)

## Parse $ARGUMENTS

1. **Empty $ARGUMENTS** → reply usage:
   ```
   Usage: /tin-batch <TICKER1,TICKER2,...>
   Example: /tin-batch VCB,SSI,VHM    (mixed sectors)
   Example: /tin-batch ACB,TPB,VPB    (Bank only)
   Single ticker: /tin-batch VCB     (fall back to /tin behavior)
   ```
   Stop.

2. **Single ticker no comma** (vd `/tin-batch VCB`) → fall back to `/tin VCB` behavior:
   - Single Task dispatch `newsroom-pipeline` với ticker=VCB
   - Same output format as /tin

3. **Comma-separated** (vd `/tin-batch VCB,SSI,VHM`) → split → list of N tickers.

## Validate tickers

For mỗi ticker trong list:
- Strip whitespace + uppercase
- Alias mapping comprehensive — see `.claude/skills/finpath-newsroom-editor/scripts/ticker_detection.py::COMPANY_NAME_TO_TICKER` (~80 alias entries covering 61 tickers).
  - Bank examples: Vietcombank→VCB, Sacombank→STB, Eximbank→EIB, HDBank→HDB, Nam Á Bank→NAB, ...
  - CK examples: VNDirect→VND, HSC→HCM, FPTS→FTS, Petrosetco→PSI, BIDV Securities→BSI, ...
  - BĐS examples: Vinhomes→VHM, Novaland→NVL, Khang Điền→KDH, Đất Xanh→DXG
- Check membership trong FULL_UNIVERSE (61 mã, see routing.py) — use `from scripts.routing import FULL_UNIVERSE` để verify
- Invalid → log warn `⚠️ Skip ticker [X] — không thuộc 61 mã FULL_UNIVERSE` + remove khỏi list (KHÔNG crash whole batch)

Nếu sau validation 0 ticker hợp lệ → reply "Không có ticker hợp lệ trong 61 mã FULL_UNIVERSE" + stop.

## Step 0 (V5.1.4 / Subsystem H) — Generate parent SESSION_ID once

Trước khi spawn N parallel pipelines, generate ONE `SESSION_ID` cho cả batch để `/pipeline-runs` viewer group N tickers thành 1 session × N batches:

```bash
SESSION_ID=$(uuidgen)
TRIGGER_TYPE="tin-batch"
TRIGGER_ARGS="$ARGUMENTS"   # original comma list, vd "VCB,SSI,VHM"
echo "Batch session: $SESSION_ID ($TRIGGER_TYPE $TRIGGER_ARGS)"
```

**CRITICAL** — sinh `SESSION_ID` ĐÚNG 1 LẦN cho cả batch. KHÔNG sinh 1 SESSION_ID per ticker (sẽ tạo N session thay vì N batches trong 1 session).

## Spawn parallel pipelines

Single message với N Task tool calls — Claude Code runs parallel. Pass shared session metadata vào prompt cho mỗi child `newsroom-pipeline`:

```
Task tool call 1: subagent_type=newsroom-pipeline,
  prompt="ticker=VCB session_id=$SESSION_ID trigger_type=tin-batch trigger_args=$TRIGGER_ARGS ..."
Task tool call 2: subagent_type=newsroom-pipeline,
  prompt="ticker=SSI session_id=$SESSION_ID trigger_type=tin-batch trigger_args=$TRIGGER_ARGS ..."
Task tool call 3: subagent_type=newsroom-pipeline,
  prompt="ticker=VHM session_id=$SESSION_ID trigger_type=tin-batch trigger_args=$TRIGGER_ARGS ..."
```

Mỗi pipeline có own `funnel_batch_id` (timestamp + ticker) → no row collision. Child `newsroom-pipeline` Step 0 phát hiện `session_id` đã inherit từ parent prompt → KHÔNG sinh thêm UUID (xem `.claude/agents/newsroom-pipeline.md` Step 0).

Pipeline orchestrator tự route master theo sector (Editor V1 set sector field từ routing.get_sector(ticker)):
- VCB → sector=Bank → Master Bank
- SSI → sector=CK → Master CK
- VHM → sector=BĐS → Master BĐS

Prereqs (Phase G):
- **WAL mode** (T1) handles SQLite write serialization automatically
- **Atomic manifest write** (T6) handles output/compare-feed/manifest.json race
- Existing `crawl_log.source_url` UNIQUE constraint catches dup URLs across batches

## Aggregate output

Sau khi all N pipelines return, format final reply:

```
✅ Pipeline /tin-batch <TICKER1,TICKER2,...> hoàn tất

[per ticker block — group by sector]

📊 Bank:
  VCB:
    - Funnel batch: VCB-YYYYMMDD-HHMM
    - Crawled: N rows
    - Articles: M published
    - Files: output/compare-feed/VCB-...

📊 CK:
  SSI:
    - Funnel batch: SSI-YYYYMMDD-HHMM
    ...

📊 BĐS:
  VHM:
    - Funnel batch: VHM-YYYYMMDD-HHMM
    ...

Total: <N tickers across X sectors> × <avg articles per ticker> = <total> articles
Total Telegram: <K> pushed
Total wall-clock: <T>s (parallel speedup vs <T_seq>s sequential = X.Yx)
```

## Edge cases

- **1 pipeline crashes** → other pipelines continue (Task isolation). Log error + skip in aggregate report.
- **Skipped invalid tickers** → list at top of reply ("⚠️ Bỏ qua: [X, Y]").
- **0 valid tickers** → reply stop message (see Validate section above).
- **All pipelines reject (0 articles each)** → aggregate "Batch không đủ chất lượng cho tất cả tickers — xem reject reasons per ticker."
- **Mixed sectors** (vd VCB+SSI+VHM) — Pipeline orchestrator handles routing tự động per ticker. Output group by sector trong reply.
