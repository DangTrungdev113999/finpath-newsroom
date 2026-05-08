---
description: Viết bài tin chuyên sâu về 1 mã cổ phiếu Việt Nam (Bank universe MVP)
argument-hint: <TICKER>
allowed-tools: Bash, Task, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

Trigger pipeline 6-step Newsroom V3.6 cho ticker **$ARGUMENTS**.

Universe MVP Bank: **TCB · VCB · MBB · ACB · BID · CTG · VPB**.

Nếu $ARGUMENTS không thuộc universe → reply "Ticker $ARGUMENTS không thuộc MVP Bank universe. CK + BĐS sẽ thêm sau." và dừng pipeline.

Nếu $ARGUMENTS hợp lệ → dispatch agent `newsroom-pipeline` với input ticker = $ARGUMENTS, để chạy 6-step:

1. **Crawler** — Python script `lib/stages/run_crawler.py` (mechanical, đã port)
2. **Editor V1** — subagent `newsroom-editor` (Phase 4 implements; Phase 3 stub)
3. **Story Editor** — subagent `newsroom-story-editor` (Phase 4 implements; Phase 3 stub)
4. **Master Bank** — subagent `newsroom-master-bank` (Phase 4 implements; Phase 3 stub)
5. **Skeptic** — subagent `newsroom-skeptic` (Phase 4 implements; Phase 3 stub)
6. **Render** — Python script `lib/render_compare_feed.py` → `output/compare-feed/<batch>.md` + cập nhật `manifest.json`

**Phase 3 mechanical**: Step 1 + 6 chạy thật, Step 2-5 stub (tạo placeholder generated_news row). Output là 1 file markdown render được trên web React viewer (`cd web && npm run dev` → localhost:5173).

**Phase 4 LLM agents** sẽ thay stub bằng dispatch thật + bài 200-400 từ pass 5 quality gates V3.6.
