# lib/stages/run_git_publish.py
"""Auto git publish with self-heal for common errors.

Phase H1 — race fix: pipeline must auto push commits before Telegram so
that link to GitHub Pages is guaranteed deployed.

Self-heal cases (in order of detection):
- Behind remote → git pull --rebase → retry push
- Pre-commit hook failed (lint) → auto run npm lint --fix → restage → retry
- Network/timeout → exponential backoff retry
- Auth fail / conflict in non-output files → fail with clear stage label
"""
from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
MAX_PUSH_ATTEMPTS = 3
WEB_DIR = REPO_ROOT / "web"


class GitPublishError(Exception):
    """Raised on unrecoverable git publish failures."""


def _run(cmd: str, cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess:
    """Run shell command, return CompletedProcess (does not raise on non-zero)."""
    return subprocess.run(
        cmd, shell=True, cwd=str(cwd), capture_output=True, text=True
    )


def _is_behind_remote(stderr: str) -> bool:
    return "behind" in stderr.lower() and "origin" in stderr.lower()


def _is_lint_hook_fail(stderr: str) -> bool:
    s = stderr.lower()
    return "pre-commit" in s or ("hook failed" in s and ("lint" in s or "format" in s))


def _is_network_error(stderr: str) -> bool:
    s = stderr.lower()
    return any(k in s for k in ["timed out", "timeout", "connection refused", "could not resolve", "unable to access"])


def _is_auth_error(stderr: str) -> bool:
    s = stderr.lower()
    return "permission denied" in s or "authentication failed" in s or "could not read username" in s


def _is_conflict_error(stderr: str) -> bool:
    return "CONFLICT" in stderr or "merge conflict" in stderr.lower()


def auto_git_publish(batch_id: str, article_count: int) -> dict[str, Any]:
    """Add output files, commit, push with self-heal.

    Returns:
      Success: {"ok": True, "commit_sha": str, "duration_ms": int, "self_heal_actions": [str]}
      Failure: {"ok": False, "error": str, "stage": str, "stderr": str}
    """
    start = time.time()
    self_heal_actions: list[str] = []

    # 1. git add
    add = _run("git add output/compare-feed/")
    if add.returncode != 0:
        return {
            "ok": False,
            "error": "git add failed",
            "stage": "git_add",
            "stderr": add.stderr[:500],
        }

    # 2. git commit
    commit_msg = f"feat(content): auto-publish batch {batch_id} ({article_count} articles)"
    commit = _run(f"git commit -m {_sh_quote(commit_msg)}")
    if commit.returncode != 0:
        # nothing to commit is OK — check if working tree clean
        if "nothing to commit" in commit.stdout.lower():
            sha = _run("git rev-parse HEAD").stdout.strip()
            return {
                "ok": True,
                "commit_sha": sha,
                "duration_ms": int((time.time() - start) * 1000),
                "self_heal_actions": ["nothing_to_commit"],
            }
        return {
            "ok": False,
            "error": "git commit failed",
            "stage": "git_commit",
            "stderr": commit.stderr[:500],
        }

    # 3. git push with self-heal up to MAX_PUSH_ATTEMPTS
    for attempt in range(1, MAX_PUSH_ATTEMPTS + 1):
        push = _run("git push")
        if push.returncode == 0:
            sha = _run("git rev-parse HEAD").stdout.strip()
            return {
                "ok": True,
                "commit_sha": sha,
                "duration_ms": int((time.time() - start) * 1000),
                "self_heal_actions": self_heal_actions,
            }

        stderr = push.stderr

        # Auth/conflict are unrecoverable
        if _is_auth_error(stderr):
            return {
                "ok": False,
                "error": "auth failure on git push",
                "stage": "git_auth",
                "stderr": stderr[:500],
            }
        if _is_conflict_error(stderr):
            _run("git rebase --abort")  # cleanup any partial rebase state
            return {
                "ok": False,
                "error": "merge conflict in non-output files",
                "stage": "git_conflict",
                "stderr": stderr[:500],
            }

        # Self-heal: behind remote → pull rebase
        if _is_behind_remote(stderr):
            self_heal_actions.append("git pull --rebase")
            rebase = _run("git pull --rebase")
            if rebase.returncode != 0:
                return {
                    "ok": False,
                    "error": "git pull --rebase failed",
                    "stage": "git_rebase",
                    "stderr": rebase.stderr[:500],
                }
            continue  # retry push

        # Self-heal: lint hook fail → auto fix
        if _is_lint_hook_fail(stderr):
            self_heal_actions.append("npm lint --fix")
            if WEB_DIR.exists():
                _run("npm run lint -- --fix", cwd=WEB_DIR)
            _run("git add -u")
            recommit = _run(f"git commit -m {_sh_quote(commit_msg)} --allow-empty")
            self_heal_actions.append("recommit_after_lint")
            if recommit.returncode != 0 and "nothing to commit" not in recommit.stdout.lower():
                return {
                    "ok": False,
                    "error": "recommit after lint fix failed",
                    "stage": "git_recommit",
                    "stderr": recommit.stderr[:500],
                }
            continue  # retry push

        # Self-heal: network → exponential backoff retry
        if _is_network_error(stderr):
            backoff = 2 ** attempt
            self_heal_actions.append(f"network_retry_backoff_{backoff}s")
            time.sleep(backoff)
            continue  # retry push

        # Unknown error — fail
        return {
            "ok": False,
            "error": "unknown git push failure",
            "stage": "git_unknown",
            "stderr": stderr[:500],
        }

    # All attempts exhausted
    return {
        "ok": False,
        "error": f"max retries exceeded ({MAX_PUSH_ATTEMPTS})",
        "stage": "git_max_retries",
        "stderr": "",
    }


def _sh_quote(s: str) -> str:
    """POSIX shell single-quote escape."""
    return "'" + s.replace("'", "'\\''") + "'"
