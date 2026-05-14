# Spawn step agent (V5.1.5)

Reference cho `Bash: uv run python lib/stages/spawn_step_agent.py` — transport thay `Task` tool cho Steps 2-5 + 3.5 + 4.5 + 9.

## Tại sao

Claude Code platform filter `Task` tool ra khỏi subagent runtime context (GH issue #4182, confirmed Anthropic docs). `newsroom-pipeline` chạy như subagent của parent slash command (`/tin` / `/tin-batch` / `/tin-hot`), nên KHÔNG có `Task`. Inline self-execute cấm bởi schema validation `lib/pipeline_db.py::validate_pipeline_step` (NVL 2026-05-11 postmortem) + voice quality drift.

Root fix V5.1.5: dispatch qua `claude -p --agent <name>` — fresh top-level process có full tool access (kể cả `Task` nếu agent body cần). Agent body load tự động từ `.claude/agents/<name>.md`.

## Helper signature

```bash
uv run python lib/stages/spawn_step_agent.py \
  <agent_name> <prompt_file_or_text> \
  [--model sonnet|opus|haiku] \
  [--max-budget-usd 2.0] \
  [--timeout-s 600] \
  [--allowed-tools "Bash,Read,WebSearch"]
```

Returns JSON on stdout:

```json
{
  "ok": true,
  "result": "<final agent reply text>",
  "session_id": "<uuid>",
  "duration_ms": 29944,
  "num_turns": 3,
  "stop_reason": "end_turn",
  "tokens": {
    "input": 6,
    "output": 2084,
    "cache_creation": 15155,
    "cache_read": 90921
  },
  "cost_usd": 0.11538,
  "model_usage": {"claude-sonnet-4-6": {...}}
}
```

`ok:false` → `{ok, error, duration_ms, stderr_tail?, stdout_head?}`. Pipeline MUST STOP + report error — KHÔNG inline fallback.

## Pattern per step

| Step | Agent | Model preset | max-budget | timeout |
|---|---|---|---|---|
| 2 Editor V1 | `newsroom-editor` | sonnet | 0.5 | 180s |
| 3 Story Editor | `newsroom-story-editor` | opus | 3.0 | 600s |
| 3.5 Format Director | `newsroom-format-director` | sonnet | 0.8 | 180s |
| 4 Master sector | `newsroom-master-<route>` | opus | 4.0 | 900s |
| 5 Skeptic (⏸ paused) | `newsroom-skeptic` | opus | 2.0 | 600s |
| 9 Telegram | `newsroom-telegram-publisher` | haiku | 0.3 | 120s |

Adjust per agent skill spec — defaults shown match V5.1.5 baseline.

## Bash escaping rule

⚠️ KHÔNG inline large prompt (`claude -p "..."`) khi prompt chứa Vietnamese diacritics + embedded JSON + quotes. Write to `/tmp/prompt-<step>-<id>.md` heredoc:

```bash
cat > /tmp/prompt-editor-<row_id>.md <<'EOF'
Process row_id <row_id>. Follow newsroom-editor skill V5.1.3 ...
EOF
```

Helper auto-detects: nếu arg `<prompt>` là file path tồn tại, đọc file content; ngược lại treat raw string.

## Parsing in orchestrator

```bash
spawn_out=$(uv run python lib/stages/spawn_step_agent.py newsroom-editor /tmp/prompt-editor-$ROW_ID.md \
  --model sonnet --max-budget-usd 0.5 --timeout-s 180)

ok=$(echo "$spawn_out" | python3 -c "import json,sys; print(json.load(sys.stdin)['ok'])")
if [ "$ok" != "True" ]; then
  echo "Step 2 spawn FAILED for $ROW_ID: $spawn_out" >&2
  exit 1
fi

# Extract for pipeline_log persistence
duration_ms=$(echo "$spawn_out" | python3 -c "import json,sys; print(json.load(sys.stdin)['duration_ms'])")
tokens_input=$(echo "$spawn_out" | python3 -c "import json,sys; print(json.load(sys.stdin)['tokens']['input'])")
cost_usd=$(echo "$spawn_out" | python3 -c "import json,sys; print(json.load(sys.stdin)['cost_usd'])")
```

## Cost economics

Per spawn ~$0.05-0.15 (sonnet, depending on cache hit ratio). Opus runs 3-5x more. Full ticker pipeline V5.1.5 cost rough breakdown:
- Step 2 × 10 rows: ~$0.5-1.0 (sonnet, mechanical)
- Step 3 × 1 batch: ~$1.0-2.0 (opus, judgment)
- Step 3.5 × 1 batch: ~$0.1-0.3 (sonnet)
- Step 4 × N briefs: ~$2-5 per brief (opus, writing)
- Step 4.5 × N articles: ~$0.5-1.0 per article
- Step 9 × N articles: ~$0.05 per article (haiku)

Typical 2-3 brief ticker: $5-15 per pipeline run. Compare to inline Task (free) — but inline is broken under nesting, so cost is acceptable trade.

## Verification — spawn loads agent body

```bash
claude -p "Reply: (1) Agent name? (2) First 3 tools? (3) Skill version?" \
  --agent newsroom-editor --output-format json --model sonnet \
  --no-session-persistence --permission-mode bypassPermissions
```

Expected: agent identifies as Editor V1, lists Bash/Read tools, references V5.1.3. If reply is generic "I'm Claude with default tools" → `--agent` flag broken, transport unusable.

## Failure modes

| Failure | Cause | Recovery |
|---|---|---|
| `ok:false` `error="timeout"` | Agent stuck (network / long thinking) | Retry once with larger `--timeout-s`; if still timeout, STOP pipeline |
| `ok:false` `error="exit_code=2"` | `claude` CLI not found / invalid flag | Check `which claude` + CLI version |
| `ok:false` `error="json_parse"` | Malformed JSON from claude | Inspect `stdout_head` — likely transient API error; retry once |
| `ok:true` but `result` empty | Agent gave up / refused | Inspect agent body, prompt clarity. Bug in spec — fix at agent level |
| Schema validation fail downstream | Agent returned wrong JSON shape | Bug in agent body — fix skill, NOT orchestrator workaround |

NEVER fallback to inline self-execute on spawn failure — that's the original bug we just fixed.
