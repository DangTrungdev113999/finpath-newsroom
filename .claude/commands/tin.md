---
description: Viết bài tin chuyên sâu về 1 mã cổ phiếu Việt Nam (16 mã: Bank/CK/BĐS)
argument-hint: <TICKER>
allowed-tools: Bash, Task, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

Trigger pipeline 6-step Newsroom V4.0 cho ticker **$ARGUMENTS**.

FULL_UNIVERSE 16 mã (3 sector):
- **Bank** (7): TCB · VCB · MBB · ACB · BID · CTG · VPB
- **CK** (5): SSI · VND · HCM · VCI · SHS
- **BĐS** (4): VHM · NVL · KDH · DXG (KBC defer — KCN pattern khác)

Map alias full names:
- Bank: Vietcombank→VCB, Techcombank→TCB, BIDV→BID, VietinBank→CTG, MB Bank→MBB, ACB→ACB, VPBank→VPB
- CK: SSI→SSI, VNDirect→VND, HSC→HCM, Vietcap→VCI, Sài Gòn-Hà Nội→SHS
- BĐS: Vinhomes→VHM, Novaland→NVL, Khang Điền→KDH, Đất Xanh→DXG

Nếu $ARGUMENTS không thuộc 16 mã → reply "Ticker $ARGUMENTS không thuộc 16 mã universe Finpath Newsroom (Bank/CK/BĐS)." và dừng pipeline.

Nếu $ARGUMENTS hợp lệ → dispatch agent `newsroom-pipeline` với input ticker = $ARGUMENTS, để chạy 6-step:

1. **Crawler** — Python script `lib/stages/run_crawler.py` (mechanical)
2. **Editor V1** — subagent `newsroom-editor` (detect ticker + lookup sector via routing.get_sector → set sector field Bank/CK/BĐS)
3. **Story Editor** — subagent `newsroom-story-editor` (cross-sector, output briefs V4.0 với deep_question_options array)
4. **Master sector** — subagent route theo sector field từ Editor:
   - sector=Bank → `newsroom-master-bank`
   - sector=CK → `newsroom-master-ck`
   - sector=BĐS → `newsroom-master-bds`
5. **Skeptic** — subagent `newsroom-skeptic` (cross-sector, ONE skeptic cho cả 3 master)
6. **Render** — Python script `lib/render_compare_feed.py` → `output/compare-feed/<batch>.md` + cập nhật `manifest.json`

Pipeline tự route master theo sector → output bài 200-400 từ pass 5 quality gates V4.0 (no_english_jargon | word_count | body_pattern | title_as_hook | no_metadata_leak).
