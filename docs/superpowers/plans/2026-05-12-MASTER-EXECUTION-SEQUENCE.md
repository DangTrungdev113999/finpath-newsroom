# Master Execution Sequence V5.1.4

> **For executor**: Single source of truth cho execution order across 5 plans (B / C / A / F / G / H + patches). Read TRƯỚC khi launch subagent-driven-development.

**Created**: 2026-05-12 PM (post-advisor review)

**Purpose**: Resolve advisor gap 5 (execution order undocumented) + gap 6 (file merge conflicts in shared files).

---

## 📊 Plan inventory

| Plan | Tasks | Phase count | Notes |
|---|---|---|---|
| Plan B (Format Diversity V5.1.2) | 23+ + Phase 6 (Tasks 23-30) | 6 phases | V5.1.2 PATCH NOTICE at top — split skill + voice + stance |
| Plan C (Headline Craft V1.1) | 13 (Tasks 1-9 + Phase 2 Tasks 10-13) | 2 phases | V1.1 PATCH NOTICE — UPDATE SQL + 4 lối flexible |
| Plan A (Hot Ticker V1.1) | Existing 6 tasks + V1.2 PATCH in Plan F Task 16 | — | V1.2 PATCH = intersect 61→139 only (no foreign) |
| Plan F (Universe Expansion V5.1.3) | 17 + Task 5.5 (alias mapping patch) = 18 | 4 phases | NEW — universe 61→139 + 7 master mới |
| Plan G (Foreign Flow V1.1) | 8 | 3 phases | V1.1 simplification — on-demand tool |
| Plan H (Pipeline Run History V1.0.1) | 9 | 4 phases | NEW — /pipeline-runs page |

**Total tasks**: ~67 atomic tasks across 5 plans + patches.

---

## 🔗 Hidden cross-plan dependencies

### Hard dependencies (must serialize)

| Predecessor | Successor | Reason |
|---|---|---|
| **Plan B V5.1.2 Phase 6 (Tasks 23-30)** | **Plan F Tasks 6-12** | Plan F masters `cp` từ Bank split structure (format-bodies/, voice, stance) |
| **Plan F Task 1** (`_apply_migrations` method) | **Plan G Task 1, Plan H Task 1** | Migration SQL files load qua `_apply_migrations` |
| **Plan F Tasks 6-12** (7 new master folders exist) | **Plan G Task 5** (cp foreign-flow-when-to-call.md vào 10 master) | Folder phải tồn tại trước khi cp |
| **Plan C Task 5** (Step 4.5 Headline dispatch wire orchestrator) | **V5.1.3 ship** | Master no-title → pipeline crash render nếu Headline chưa wire |
| **Plan F Task 5.5** (extend COMPANY_NAME_TO_TICKER) | **Plan F Phase 2 ticker dispatch** | New tickers cần alias để Editor V1 detect |

### Soft dependencies (parallel OK but order preferred)

| Task | Conflicts with | Resolution |
|---|---|---|
| Plan F Task 1 (modify pipeline_db.py schema) | Plan G Task 2 (extend finpath_api in pipeline_db connection) | Serialize F1 → G2 |
| Plan F Task 5 (modify pipeline_db.py validation) | Plan H Task 1 (modify pipeline_db.py schema migration) | Serialize F5 → H1 |
| Plan F Task 15 (CLAUDE.md universe) | Plan G Task 7 (CLAUDE.md foreign API) | Serialize F15 → G7 |
| Plan G Task 7 (CLAUDE.md) | Plan H Task 9 (CLAUDE.md pipeline runs) | Serialize G7 → H9 |
| Plan F types.ts (FormatId) | Plan H Task 4 types.ts (PipelineSession) | Serialize FormatId → PipelineSession |

---

## 📋 Recommended execution sequence

### Stage 1: Foundation (Plan B Phase 6 + Plan F Phase 1)

**Goal**: Split Bank skill structure + universe expansion foundation.

```
Plan B Task 23 (Split orchestrator skill)
Plan B Task 24 (Split master-bank skill — CREATES format-bodies/ for cp later)
Plan B Task 25 (Split master-ck skill)
Plan B Task 26 (Split master-bds skill)
Plan B Task 27 (Master prompts dỡ title rule)
Plan B Task 28 (Story Editor brief stance_directive)
Plan B Task 29 (Master apply stance_directive)
Plan B Task 30 (Voice Rule 2 LLM no-hedging)
   ↓
Plan F Task 1 (SQLite migration finpath_sectors_cache + _apply_migrations)
Plan F Task 2 (lib/finpath_sectors.py)
Plan F Task 3 (lib/sector_router.py + sector_routing.yaml)
Plan F Task 4 (refresh_sector_cache CLI + initial populate)
Plan F Task 5 (Editor V1 update)
Plan F Task 5.5 (PATCH: extend COMPANY_NAME_TO_TICKER 78 entries)
```

**Stage 1 commits**: ~8 atomic. Sequential execution required (each depends on prior).

### Stage 2: New master agents (Plan F Phase 2, parallel-safe)

**Goal**: Scaffold 7 new master agents từ Bank split template.

```
Plan F Task 6 (master-oilgas)     ─┐
Plan F Task 7 (master-logistics)  │
Plan F Task 8 (master-fb)         │  PARALLEL — 7 subagents
Plan F Task 9 (master-apparel)    │  same time
Plan F Task 10 (master-retail)    │
Plan F Task 11 (master-seafood)   │
Plan F Task 12 (master-defensive) ─┘
```

**Each Task 6-12 includes Step 6.5 (PATCH critical gap 1) cp format-bodies from Bank** — must verify Bank's format-bodies/ exists (Plan B Task 24 prerequisite).

### Stage 3: Headline integration (Plan C)

**Goal**: Headline Craft agent + Step 4.5 orchestrator wiring.

```
Plan C Task 1 (headline_scorer.py + check_hard_criteria)
Plan C Task 2 (Headline agent prompt)
Plan C Task 3 (Headline output schema)
Plan C Task 4 (Headline skill)
Plan C Task 5 (ORCHESTRATOR Step 4.5 dispatch — CRITICAL for V5.1.3 ship)
Plan C Task 6 (pipeline_db step_4_5 schema)
Plan C Task 7 (UPDATE generated_news.title SQL)
Plan C Task 8 (Skeptic SKIP — paused 2026-05-12)
Plan C Task 9 (Tests integration)
   ↓
Plan C Phase 2 Tasks 10-13 (skill split: SKILL + 4 references)
```

**Critical**: Plan C Task 5 MUST complete before pipeline run that uses Plan F masters (no-title), otherwise render crashes.

### Stage 4: Foreign Flow + Plan A patch (Plan G + Plan F Task 16)

**Goal**: Foreign flow API methods + Hot Ticker universe patch.

```
Plan G Task 1 (SQLite finpath_foreign_cache migration)
Plan G Task 2 (lib/finpath_api.py extend 3 methods)
Plan G Task 3 (live API smoke)
   ↓
Plan G Task 4 (Story Editor foreign-flow-when-to-call.md)
Plan G Task 5 (10 Master skills foreign-flow-when-to-call.md — DUPLICATE pattern)
Plan G Task 6 (10 Master SKILL.md register reference)
   ↓
Plan F Task 16 (Spec A V1.2 PATCH NOTICE — universe intersect 61→139)
```

### Stage 5: Pipeline Run History (Plan H)

**Goal**: /pipeline-runs page.

```
Plan H Task 1 (SQLite session_grouping migration)
Plan H Task 2 (orchestrator session_id + run_crawler.py CLI args PATCH gap 2)
Plan H Task 3 (build_pipeline_runs_manifest)
   ↓
Plan H Task 4 (types + loader)
Plan H Task 5 (PipelineSession + PipelineBatch components)
Plan H Task 6 (PipelineRunsPage + route + filter)
   ↓
Plan H Task 7 (Remove RightColumn section 5)
Plan H Task 8 (batch_id hyperlink + Header nav)
   ↓
Plan H Task 9 (E2E smoke)
```

### Stage 6: CLAUDE.md aggregate + final smoke

**Goal**: Update CLAUDE.md once (avoid 3 conflicting modifications).

```
SINGLE TASK: aggregate CLAUDE.md updates from
- Plan F Task 15 (universe 61→139, sector list, master agents)
- Plan G Task 7 (foreign flow API note)
- Plan H Task 9 (pipeline runs page note)

Apply all 3 sections in single commit, single subagent.
   ↓
Plan F Task 17 (Smoke tests universe expansion)
Final E2E: /tin VHM + /tin BSR (oilgas) + /tin-hot 2
```

---

## ⚠ Merge conflict resolution (gap 6)

### File: `lib/pipeline_db.py`

Multiple plans modify. Serialize trong sequence:

1. **Plan F Task 1** — add `_apply_migrations` method + new schema fields
2. **Plan F Task 5** — add `validate_crawl_log_v5_1_3` + `_MASTER_ROUTE_VALID`
3. **Plan G Task 2** — accept `db` parameter trong FinpathAPI (uses but doesn't modify pipeline_db.py)
4. **Plan H Task 1** — migration triggers `_apply_migrations` (no pipeline_db.py modification, just SQL file)
5. **Plan H Task 2** — modify `insert_crawl_row` accept session_id/trigger_type/trigger_args

→ Order: F1 → F5 → H2. Each subagent reads file before edit → no conflict.

### File: `CLAUDE.md`

3 plans add sections. **Resolution**: Stage 6 single aggregate task (above).

### File: `web/src/types.ts`

2 plans add types. Serialize:
1. Plan F (FormatId, MasterRoute enum)
2. Plan H Task 4 (PipelineSession, PipelineBatch types)

→ Order: F first → H Task 4 reads + extends.

### File: `.claude/agents/newsroom-pipeline.md`

Multiple plans modify orchestrator prompt. **Resolution**: Each modification is additive (Step 0 session, Step 1.5 Market Snapshot, Step 3.5 Format Director, Step 4.5 Headline). Apply in order:

1. Plan F Task 5 (Editor V1 V5.1.3 routing)
2. Plan B Phase 6 (Format Director Step 3.5 — already in V5.1.2)
3. Plan C Task 5 (Headline Step 4.5)
4. Plan H Task 2 Step 4 (session_id Step 0)
5. Plan H Step 3.6 (Bash invocation update)

---

## ✅ Verification gates

After each Stage, run verification:

### Gate 1 (after Stage 1)
```bash
uv run pytest tests/test_finpath_sectors.py tests/test_sector_router.py tests/test_pipeline_db_finpath_cache.py tests/test_company_name_mapping_v5_1_3.py -v
```
All foundation tests pass.

### Gate 2 (after Stage 2)
```bash
# 10 master skill folders exist with proper structure
for s in bank ck bds oilgas logistics fb apparel retail seafood defensive; do
  test -d ".claude/skills/finpath-newsroom-master-$s/references/format-bodies/" || echo "MISSING: $s"
done
```
All 10 folders + format-bodies/ exist.

### Gate 3 (after Stage 3)
Smoke test `/tin VHM` end-to-end (manual or scripted):
- Master writes body với title=NULL
- Headline Step 4.5 generates title
- Render produces markdown file with proper slug

### Gate 4 (after Stage 4)
```bash
uv run pytest tests/test_finpath_api_foreign.py tests/integration/test_foreign_flow_smoke.py -v
```

### Gate 5 (after Stage 5)
Smoke test `/pipeline-runs` page:
- Run `/tin VHM` → check pipeline-runs.json updated
- Open `localhost:5173/pipeline-runs` → see session

### Gate 6 (final)
Full E2E:
```bash
/tin BSR              # oilgas master, web search heavy
/tin VCB              # bank master, full KB
/tin-hot 2            # 8 ticker batch, 1 session
```

All produce valid markdown + pipeline-runs.json updated + Headline title in DB.

---

## 🚨 Hard rules during execution

1. **NEVER skip Stage order** — Stage 2 cp from Bank requires Stage 1 split done first.
2. **NEVER parallel within Stage 1 + Stage 6** — sequential dependencies.
3. **PARALLEL Stage 2 + Stage 4 Tasks 4-6 OK** — different files.
4. **NEVER ship V5.1.3 without Plan C Task 5** — Master no-title needs Headline wired.
5. **Run Gate after each Stage** — early failure detection cheaper than late.
6. **Single subagent per shared file modification** — pipeline_db.py + CLAUDE.md + types.ts, not parallel.

---

## 📦 Effort estimate

| Stage | Tasks | Effort (subagent-parallel) |
|---|---|---|
| 1 Foundation | 13 sequential | ~6-7 hours |
| 2 New masters | 7 parallel | ~1-1.5 hours (with 7 subagents simultaneous) |
| 3 Headline | 13 sequential | ~5-6 hours |
| 4 Foreign + Plan A patch | 8 + 1 = 9 | ~3-4 hours |
| 5 Pipeline runs | 9 sequential | ~4-5 hours |
| 6 CLAUDE.md aggregate + final | 2-3 | ~1 hour |
| **Total** | **~52 atomic + parallel** | **~20-25 hours** = **~3-4 ngày wall clock** với subagent-driven parallel |

---

## Recommendation

Launch subagent-driven-development with this sequence as input. Each Stage = batch of tasks for spec-reviewer + code-quality-reviewer cycles. Don't deviate from order — advisor flagged execution order as gap 5 specifically.
