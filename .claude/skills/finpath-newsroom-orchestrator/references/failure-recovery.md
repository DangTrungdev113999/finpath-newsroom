# Failure Recovery — Per-step + Batch survival

> Loaded from `Skill: finpath-newsroom-orchestrator` references. Pipeline 6+ steps; each step can soft-fail (continue degraded) or hard-fail (stop pipeline). Rules below.

## Brief-level isolation (Step 4 + Step 5)

Per-brief outer loop. If brief N fails (Master `accepted_hypothesis: false`, Skeptic crash), **continue with brief N+1** — KHÔNG crash whole batch.

```
brief 1 → Master accepted → article persisted → continue
brief 2 → Master rejected (accepted_hypothesis=false) → log, skip → continue
brief 3 → Master accepted → article persisted → continue
```

Final batch can have 0..N accepted articles. 0 articles → final reply explains funnel reject reasons.

## Soft-fail steps (continue degraded)

| Step | Failure mode | Behavior |
|---|---|---|
| Step 1.5 Market Snapshot | Finpath API down / ticker not found | Result = `None`, `soft_failed: true`, pipeline continues. Format Director receives `ticker_market_data=null`. |
| Step 5 Skeptic | Critique crash / fail verdict | Publish article without "Góc nhìn ngược" — log warning. ⏸ Currently paused — N/A until re-enabled. |
| Step 8 Pages wait | Timeout | Proceed Step 9 BUT pass fallback footer warning to Telegram publisher: `⚠️ Đang deploy, link có thể chưa work trong 30s`. |
| Step 9 Telegram | Telegram API error | Article remains published on Pages — log error, do NOT block. |

## Hard-fail steps (STOP pipeline)

| Step | Failure mode | Action |
|---|---|---|
| Step 1 Crawler | 0 candidates after WebSearch | Reply "Không tìm thấy tin về [TICKER] trong 30 ngày." Stop. |
| Step 2 Editor V1 | Subagent crash | STOP — KHÔNG self-execute fallback (HARD RULE). |
| Step 3 Story Editor | 0 briefs OR subagent crash | If 0 briefs → reply "Batch không đủ chất lượng" + funnel summary. If crash → STOP + report. |
| Step 3.5 Format Director | Schema validation fail / subagent crash | STOP — schema validation in `validate_pipeline_step` blocks persist. No inline self-execute fallback. |
| Step 7 Git publish | `result.ok == False` | STOP — do NOT push Telegram (broken commit = broken link). Articles remain on disk + DB (idempotent). Log `result.stage` + `result.stderr`. |
| Step 8 Pages wait | `error.startswith("deploy failed")` | STOP — broken deploy = bad link, do not push Telegram. |

## Step 7 self-heal note

`lib/stages/run_git_publish.py` has self-heal logic for common git issues (rebase on conflict, retry on transient auth). `result.self_heal_actions` lists what was applied. Log it for observability — user can see if pipeline silently recovered.

## Idempotency

Every step persists state to SQLite BEFORE proceeding. Re-running pipeline after partial failure:
- `crawl_log` row already has `editor_v1_decision` → Step 2 skips (or re-evaluates if `--force`)
- `generated_news` row exists → Step 4 skips this brief
- `step_X_*` payload already logged → overwrite on retry (idempotent by step_key)

User can re-run `/tin <TICKER>` after fixing root cause (`git_auth` → re-add token, `git_conflict` → manual resolve) without duplication.

## NO silent skip of Step 7-9

HARD RULE: Step 7-9 MUST attempt every run. If skip has legitimate reason (secrets missing, dev mode), MUST emit explicit `step_<N>_skipped` payload with `reason` narrative + final reply MUST include `⚠️ Skipped Step <N>: <reason>` line — NEVER hidden.

Skip without log → violates "log THẬT" rule (CLAUDE.md).

## Escalation rules

- Subagent (Step 2-5 + 3.5) crash 2x same brief → STOP brief, log error, continue next brief.
- Step 7 fail after self-heal exhausted → STOP pipeline, surface error to user.
- Step 8 timeout >90s → fallback degrade (push Telegram with warning footer), NOT stop.
- Any subagent persists invalid schema (caught by `validate_pipeline_step`) → STOP that brief, log `ValueError`, continue next brief.
