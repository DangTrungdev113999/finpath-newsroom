---
description: Viết bài tin chuyên sâu về 1 mã cổ phiếu Việt Nam (71 mã: Bank/CK/BĐS/Oil-Gas)
argument-hint: <TICKER>
allowed-tools: Bash, Task, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, mcp__tavily__tavily_search
---

Trigger pipeline 6-step Newsroom V4.0 cho ticker **$ARGUMENTS**.

FULL_UNIVERSE 71 mã (4 sector):
- **Bank** (27): HOSE 16 + HNX 4 + UPCOM 7 (see routing.BANK_UNIVERSE)
- **CK** (30): HOSE 5 + HNX 15 + UPCOM 10 (see routing.CK_UNIVERSE)
- **BĐS** (4): VHM · NVL · KDH · DXG (KBC defer)
- **Oil-Gas** (10): GAS · PVD · PVS · PVT · BSR · PLX · OIL · DPM · DCM · PVC

Alias mapping comprehensive — see `.claude/skills/finpath-newsroom-editor/scripts/ticker_detection.py::COMPANY_NAME_TO_TICKER` (~100 alias entries covering 71 tickers).

Examples:
- Bank: Vietcombank→VCB, Sacombank→STB, Eximbank→EIB, HDBank→HDB, LPBank→LPB, Maritime Bank→MSB, Nam Á Bank→NAB, ...
- CK: VNDirect→VND, HSC→HCM, Vietcap→VCI, FPTS→FTS, Petrosetco→PSI, BIDV Securities→BSI, Agriseco→AGR, ...
- BĐS: Vinhomes→VHM, Novaland→NVL, Khang Điền→KDH, Đất Xanh→DXG
- Oil-Gas: PV Gas→GAS, PV Drilling→PVD, PTSC→PVS, Petrolimex→PLX, Bình Sơn→BSR, Đạm Phú Mỹ→DPM, Đạm Cà Mau→DCM, ...

Nếu $ARGUMENTS không thuộc 71 mã → reply "Ticker $ARGUMENTS không thuộc 71 mã universe Finpath Newsroom (Bank/CK/BĐS/Oil-Gas)." và dừng pipeline.

Nếu $ARGUMENTS hợp lệ → dispatch agent `newsroom-pipeline` với input ticker = $ARGUMENTS, để chạy 6-step:

1. **Crawler** — Python script `lib/stages/run_crawler.py` (mechanical)
2. **Editor V1** — subagent `newsroom-editor` (detect ticker + lookup sector via routing.get_sector → set sector field Bank/CK/BĐS/Oil-Gas)
3. **Story Editor** — subagent `newsroom-story-editor` (cross-sector, output briefs V4.0 với deep_question_options array)
4. **Master sector** — subagent route theo sector field từ Editor:
   - sector=Bank → `newsroom-master-bank`
   - sector=CK → `newsroom-master-ck`
   - sector=BĐS → `newsroom-master-bds`
   - sector=Oil-Gas → `newsroom-master-oil-gas`
5. **Skeptic** — subagent `newsroom-skeptic` (cross-sector, ONE skeptic cho cả 4 master)
6. **Render** — Python script `lib/render_compare_feed.py` → `output/compare-feed/<batch>.md` + cập nhật `manifest.json`

Pipeline tự route master theo sector → output bài 200-400 từ pass 5 quality gates V4.0 (no_english_jargon | word_count | body_pattern | title_as_hook | no_metadata_leak).
