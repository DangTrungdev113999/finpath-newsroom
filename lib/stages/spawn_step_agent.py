"""Spawn a Claude agent as a fresh top-level `claude -p` process.

Workaround for Claude Code subagent Task-tool nesting limit: subagents cannot
dispatch further subagents via the `Task` tool (platform filters it out at
runtime — confirmed via Anthropic docs + GH issue #4182).

Each invocation spawns a fresh top-level Claude process via `claude -p
--agent <name>`, which sees the full agent definition under
`.claude/agents/<name>.md` and has the Task tool available if the agent body
needs it.

Usage from pipeline orchestrator:
    uv run python lib/stages/spawn_step_agent.py <agent_name> <prompt_file> \\
        --model sonnet --max-budget-usd 2.0 --timeout-s 600

Returns JSON on stdout with: ok, result, duration_ms, tokens{...}, cost_usd,
session_id, num_turns, error (if any).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


def spawn(
    agent_name: str,
    prompt: str,
    allowed_tools: list[str] | None = None,
    model: str = "sonnet",
    max_budget_usd: float = 2.0,
    timeout_s: int = 600,
    extra_allow_dirs: list[str] | None = None,
) -> dict:
    cmd = [
        "claude",
        "-p",
        "--agent", agent_name,
        "--output-format", "json",
        "--no-session-persistence",
        "--permission-mode", "bypassPermissions",
        "--model", model,
        "--max-budget-usd", str(max_budget_usd),
    ]
    if allowed_tools:
        cmd.extend(["--allowed-tools", ",".join(allowed_tools)])
    if extra_allow_dirs:
        cmd.extend(["--add-dir", *extra_allow_dirs])
    cmd.append(prompt)

    t0 = time.time()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "error": f"timeout after {timeout_s}s",
            "duration_ms": timeout_s * 1000,
        }

    duration_ms = int((time.time() - t0) * 1000)

    if proc.returncode != 0:
        return {
            "ok": False,
            "error": f"exit_code={proc.returncode}",
            "stderr_tail": proc.stderr[-1000:] if proc.stderr else "",
            "stdout_head": proc.stdout[:500] if proc.stdout else "",
            "duration_ms": duration_ms,
        }

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "error": f"json_parse: {exc}",
            "stdout_head": proc.stdout[:500],
            "duration_ms": duration_ms,
        }

    if data.get("is_error"):
        return {
            "ok": False,
            "error": data.get("api_error_status") or "is_error_flag",
            "result": data.get("result"),
            "duration_ms": data.get("duration_ms", duration_ms),
        }

    usage = data.get("usage", {}) or {}
    return {
        "ok": True,
        "result": data.get("result", ""),
        "session_id": data.get("session_id"),
        "duration_ms": data.get("duration_ms", duration_ms),
        "num_turns": data.get("num_turns", 0),
        "stop_reason": data.get("stop_reason"),
        "tokens": {
            "input": usage.get("input_tokens", 0),
            "output": usage.get("output_tokens", 0),
            "cache_creation": usage.get("cache_creation_input_tokens", 0),
            "cache_read": usage.get("cache_read_input_tokens", 0),
        },
        "cost_usd": data.get("total_cost_usd", 0.0),
        "model_usage": data.get("modelUsage", {}),
    }


def _read_prompt(prompt_or_file: str) -> str:
    """If arg is a readable file path, return its content; else treat as raw prompt."""
    p = Path(prompt_or_file)
    if p.is_file():
        return p.read_text(encoding="utf-8")
    return prompt_or_file


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("agent_name", help="Subagent name (e.g. newsroom-editor)")
    ap.add_argument(
        "prompt",
        help="Prompt text OR path to file containing prompt (preferred for large prompts)",
    )
    ap.add_argument(
        "--allowed-tools",
        help="Comma-separated tool whitelist (overrides agent's default tools)",
    )
    ap.add_argument("--model", default="sonnet", help="Model alias (sonnet|opus|haiku)")
    ap.add_argument("--max-budget-usd", type=float, default=2.0)
    ap.add_argument("--timeout-s", type=int, default=600)
    ap.add_argument(
        "--add-dir",
        action="append",
        help="Extra directories to allow tool access (repeatable)",
    )
    args = ap.parse_args()

    prompt = _read_prompt(args.prompt)
    tools = args.allowed_tools.split(",") if args.allowed_tools else None

    out = spawn(
        agent_name=args.agent_name,
        prompt=prompt,
        allowed_tools=tools,
        model=args.model,
        max_budget_usd=args.max_budget_usd,
        timeout_s=args.timeout_s,
        extra_allow_dirs=args.add_dir,
    )
    print(json.dumps(out, ensure_ascii=False))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
