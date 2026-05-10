# Phase H — Comment Feedback + Deploy Race Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** (1) Fix Telegram link → 404 race by auto git push + poll Pages deploy before Telegram. (2) Add inline comment feedback per article → Cloudflare Worker → private Telegram group.

**Architecture:** H1 modifies pipeline orchestration (per-article render moves earlier; batch-level git_publish + pages_wait + telegram cycle at end). H2 adds frontend CommentSection with feature flag fallback (hides UI when Worker URL missing); Worker is separate Cloudflare deployment.

**Tech Stack:** Python 3 (pipeline stages, pytest), TypeScript + React + Vite + Tailwind (frontend, vitest), Cloudflare Worker (TypeScript runtime, wrangler CLI).

**Hard gate:** T14 stops subagent — Worker deploy requires user's Cloudflare account.

---

## Phase H1 — Race fix (autonomous, no human gates)

### Task 1: Tests for `run_git_publish` (TDD red phase)

**Files:**
- Create: `tests/test_run_git_publish.py`

- [ ] **Step 1: Write failing tests covering self-heal cases**

```python
# tests/test_run_git_publish.py
"""Tests for lib/stages/run_git_publish.py — auto git publish with self-heal."""
import subprocess
from unittest.mock import patch, MagicMock
import pytest

from lib.stages.run_git_publish import auto_git_publish, GitPublishError


def _mk_completed(returncode=0, stdout="", stderr=""):
    cp = MagicMock()
    cp.returncode = returncode
    cp.stdout = stdout
    cp.stderr = stderr
    return cp


@patch("lib.stages.run_git_publish.subprocess.run")
def test_happy_path_succeeds_first_try(mock_run):
    # add OK, commit OK, push OK, rev-parse OK
    mock_run.side_effect = [
        _mk_completed(),  # git add
        _mk_completed(),  # git commit
        _mk_completed(),  # git push
        _mk_completed(stdout="abc123def\n"),  # rev-parse HEAD
    ]
    result = auto_git_publish(batch_id="VCB-20260511-0830", article_count=2)
    assert result["ok"] is True
    assert result["commit_sha"] == "abc123def"
    assert result["self_heal_actions"] == []


@patch("lib.stages.run_git_publish.subprocess.run")
def test_self_heal_behind_remote_then_succeeds(mock_run):
    push_behind = _mk_completed(returncode=1, stderr="hint: Your branch is behind 'origin/main'")
    mock_run.side_effect = [
        _mk_completed(),  # add
        _mk_completed(),  # commit
        push_behind,      # push fails
        _mk_completed(),  # pull --rebase
        _mk_completed(),  # push retry
        _mk_completed(stdout="def456\n"),  # rev-parse
    ]
    result = auto_git_publish(batch_id="VCB-x", article_count=1)
    assert result["ok"] is True
    assert "git pull --rebase" in result["self_heal_actions"]


@patch("lib.stages.run_git_publish.subprocess.run")
def test_self_heal_lint_fail_then_succeeds(mock_run):
    push_lint = _mk_completed(returncode=1, stderr="pre-commit hook failed: lint error")
    mock_run.side_effect = [
        _mk_completed(),  # add
        _mk_completed(),  # commit
        push_lint,        # push fails on hook
        _mk_completed(),  # npm lint --fix
        _mk_completed(),  # git add -u
        _mk_completed(),  # git commit --amend or recommit
        _mk_completed(),  # push retry
        _mk_completed(stdout="ghi789\n"),
    ]
    result = auto_git_publish(batch_id="VCB-x", article_count=1)
    assert result["ok"] is True
    assert any("lint" in a for a in result["self_heal_actions"])


@patch("lib.stages.run_git_publish.subprocess.run")
def test_network_retry_with_backoff(mock_run):
    push_net = _mk_completed(returncode=1, stderr="fatal: unable to access ... Connection timed out")
    mock_run.side_effect = [
        _mk_completed(),
        _mk_completed(),
        push_net,         # attempt 1 fail
        push_net,         # attempt 2 fail
        _mk_completed(),  # attempt 3 success
        _mk_completed(stdout="net123\n"),
    ]
    with patch("lib.stages.run_git_publish.time.sleep") as mock_sleep:
        result = auto_git_publish(batch_id="x", article_count=1)
    assert result["ok"] is True
    assert mock_sleep.called


@patch("lib.stages.run_git_publish.subprocess.run")
def test_unrecoverable_auth_fail(mock_run):
    push_auth = _mk_completed(returncode=1, stderr="Permission denied (publickey)")
    mock_run.side_effect = [
        _mk_completed(),
        _mk_completed(),
        push_auth,
    ]
    result = auto_git_publish(batch_id="x", article_count=1)
    assert result["ok"] is False
    assert result["stage"] == "git_auth"


@patch("lib.stages.run_git_publish.subprocess.run")
def test_unrecoverable_conflict_in_non_output_files(mock_run):
    push_conflict = _mk_completed(returncode=1, stderr="CONFLICT (content): Merge conflict in lib/foo.py")
    mock_run.side_effect = [
        _mk_completed(),
        _mk_completed(),
        push_conflict,
        _mk_completed(),  # rebase abort
    ]
    result = auto_git_publish(batch_id="x", article_count=1)
    assert result["ok"] is False
    assert result["stage"] == "git_conflict"


@patch("lib.stages.run_git_publish.subprocess.run")
def test_max_retries_exceeded(mock_run):
    push_net = _mk_completed(returncode=1, stderr="Connection timed out")
    # 3 attempts all fail
    mock_run.side_effect = [
        _mk_completed(),  # add
        _mk_completed(),  # commit
        push_net, push_net, push_net,  # 3 push attempts
    ]
    with patch("lib.stages.run_git_publish.time.sleep"):
        result = auto_git_publish(batch_id="x", article_count=1)
    assert result["ok"] is False
    assert "max retries" in result["error"].lower()
```

- [ ] **Step 2: Run tests to verify they fail (module not yet exists)**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_run_git_publish.py -v`
Expected: FAIL with `ModuleNotFoundError: lib.stages.run_git_publish`

---

### Task 2: Implement `run_git_publish.py` (TDD green phase)

**Files:**
- Create: `lib/stages/run_git_publish.py`

- [ ] **Step 1: Implement module passing all tests**

```python
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
```

- [ ] **Step 2: Run tests to verify they pass**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_run_git_publish.py -v`
Expected: PASS all 7 tests

- [ ] **Step 3: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent"
git add lib/stages/run_git_publish.py tests/test_run_git_publish.py
git commit -m "feat(pipeline): auto git publish with self-heal (Phase H1 T1-T2)

Self-heals: behind remote (pull --rebase), lint hook fail (npm fix +
restage), network/timeout (exponential backoff). Unrecoverable: auth,
non-output conflicts. 7 tests pass.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Tests for `run_pages_wait` (TDD red phase)

**Files:**
- Create: `tests/test_run_pages_wait.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_run_pages_wait.py
"""Tests for lib/stages/run_pages_wait.py — poll GH Actions deploy."""
from unittest.mock import patch, MagicMock
import pytest

from lib.stages.run_pages_wait import wait_pages_deployed


def _mk_run(name="Deploy GitHub Pages", status="completed", conclusion="success", html_url="https://github.com/x/y/runs/1"):
    return {"name": name, "status": status, "conclusion": conclusion, "html_url": html_url}


@patch("lib.stages.run_pages_wait._gh_get")
def test_success_immediately(mock_get):
    mock_get.return_value = {"workflow_runs": [_mk_run()]}
    result = wait_pages_deployed(commit_sha="abc", token="t", owner="o", repo="r", timeout_s=10)
    assert result["ok"] is True
    assert "elapsed_s" in result
    assert "actions/runs" in result["workflow_run_url"] or "github.com" in result["workflow_run_url"]


@patch("lib.stages.run_pages_wait.time.sleep")
@patch("lib.stages.run_pages_wait._gh_get")
def test_polls_until_completed(mock_get, mock_sleep):
    mock_get.side_effect = [
        {"workflow_runs": [_mk_run(status="in_progress", conclusion=None)]},
        {"workflow_runs": [_mk_run(status="in_progress", conclusion=None)]},
        {"workflow_runs": [_mk_run(status="completed", conclusion="success")]},
    ]
    result = wait_pages_deployed(commit_sha="x", token="t", owner="o", repo="r", timeout_s=60)
    assert result["ok"] is True
    assert mock_get.call_count == 3


@patch("lib.stages.run_pages_wait._gh_get")
def test_workflow_failure_returns_fail(mock_get):
    mock_get.return_value = {
        "workflow_runs": [
            _mk_run(status="completed", conclusion="failure", html_url="https://github.com/x/y/runs/2")
        ]
    }
    result = wait_pages_deployed(commit_sha="x", token="t", owner="o", repo="r", timeout_s=10)
    assert result["ok"] is False
    assert "deploy failed" in result["error"]
    assert "y/runs/2" in result["run_url"]


@patch("lib.stages.run_pages_wait.time.sleep")
@patch("lib.stages.run_pages_wait._gh_get")
def test_timeout_returns_fallback_signal(mock_get, mock_sleep):
    # Always in_progress, never completes
    mock_get.return_value = {"workflow_runs": [_mk_run(status="in_progress", conclusion=None)]}
    # Force timeout by mocking time.time
    with patch("lib.stages.run_pages_wait.time.time") as mock_time:
        mock_time.side_effect = [0, 0, 5, 95]  # start=0, then poll iter checks
        result = wait_pages_deployed(commit_sha="x", token="t", owner="o", repo="r", timeout_s=90)
    assert result["ok"] is False
    assert result["error"] == "timeout"
    assert result["fallback"] == "push_telegram_anyway"


@patch("lib.stages.run_pages_wait.time.sleep")
@patch("lib.stages.run_pages_wait._gh_get")
def test_filters_by_workflow_name(mock_get, mock_sleep):
    # Returns runs for OTHER workflows AND our deploy run
    mock_get.return_value = {
        "workflow_runs": [
            _mk_run(name="Other Workflow", status="completed", conclusion="success"),
            _mk_run(name="Deploy GitHub Pages", status="completed", conclusion="success"),
        ]
    }
    result = wait_pages_deployed(commit_sha="x", token="t", owner="o", repo="r", timeout_s=10)
    assert result["ok"] is True


@patch("lib.stages.run_pages_wait.time.sleep")
@patch("lib.stages.run_pages_wait._gh_get")
def test_no_matching_workflow_yet_polls(mock_get, mock_sleep):
    # Empty first, then deploy run appears
    mock_get.side_effect = [
        {"workflow_runs": []},
        {"workflow_runs": [_mk_run(status="completed", conclusion="success")]},
    ]
    result = wait_pages_deployed(commit_sha="x", token="t", owner="o", repo="r", timeout_s=60)
    assert result["ok"] is True
    assert mock_get.call_count == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_run_pages_wait.py -v`
Expected: FAIL — module not yet exists

---

### Task 4: Implement `run_pages_wait.py`

**Files:**
- Create: `lib/stages/run_pages_wait.py`

- [ ] **Step 1: Implement module**

```python
# lib/stages/run_pages_wait.py
"""Poll GitHub Actions API until Pages deploy workflow completes.

Phase H1 — race fix: after pipeline pushes commit, poll until the
"Deploy GitHub Pages" workflow finishes successfully before telling
Telegram (link guaranteed to work).

Workflow name "Deploy GitHub Pages" matches `name:` in
.github/workflows/deploy.yml. If renamed, update WORKFLOW_NAME below.
"""
from __future__ import annotations

import time
import urllib.request
import urllib.error
import json
from typing import Any

WORKFLOW_NAME = "Deploy GitHub Pages"
POLL_INTERVAL_S = 5


def _gh_get(url: str, token: str) -> dict[str, Any]:
    """GET GitHub API, return parsed JSON. Raises on HTTP error."""
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def wait_pages_deployed(
    commit_sha: str,
    token: str,
    owner: str,
    repo: str,
    timeout_s: int = 90,
) -> dict[str, Any]:
    """Poll workflow runs for commit_sha until deploy completes or timeout.

    Returns:
      Success:  {"ok": True, "elapsed_s": int, "workflow_run_url": str}
      Fail:     {"ok": False, "error": str, "elapsed_s": int, "run_url"|"fallback": ...}
    """
    start = time.time()
    url = (
        f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
        f"?head_sha={commit_sha}&event=push&per_page=20"
    )

    while True:
        elapsed = time.time() - start
        if elapsed > timeout_s:
            return {
                "ok": False,
                "error": "timeout",
                "elapsed_s": int(elapsed),
                "fallback": "push_telegram_anyway",
            }

        try:
            data = _gh_get(url, token)
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            # Network blip — sleep and retry, do not fail entire wait
            time.sleep(POLL_INTERVAL_S)
            continue

        runs = data.get("workflow_runs", [])
        deploy_run = next((r for r in runs if r.get("name") == WORKFLOW_NAME), None)

        if deploy_run:
            status = deploy_run.get("status")
            conclusion = deploy_run.get("conclusion")
            run_url = deploy_run.get("html_url", "")

            if status == "completed":
                if conclusion == "success":
                    return {
                        "ok": True,
                        "elapsed_s": int(time.time() - start),
                        "workflow_run_url": run_url,
                    }
                # failure / cancelled / etc
                return {
                    "ok": False,
                    "error": f"deploy failed (conclusion={conclusion})",
                    "elapsed_s": int(time.time() - start),
                    "run_url": run_url,
                }

        # Still running OR no matching workflow yet → poll again
        time.sleep(POLL_INTERVAL_S)
```

- [ ] **Step 2: Run tests to verify pass**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_run_pages_wait.py -v`
Expected: PASS all 6 tests

- [ ] **Step 3: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent"
git add lib/stages/run_pages_wait.py tests/test_run_pages_wait.py
git commit -m "feat(pipeline): wait_pages_deployed polls GH Actions API (Phase H1 T3-T4)

Polls workflow_runs filtered by name='Deploy GitHub Pages' until
completed. Returns ok+elapsed on success, fail+run_url on conclusion!=success,
fail+fallback flag on timeout. 6 tests pass.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Update pipeline agent + secrets schema

**Files:**
- Modify: `.claude/agents/newsroom-pipeline.md` (Step 7 restructure)
- Modify: `data/secrets.yaml.example` (add github.token + feedback_group_chat_id)

- [ ] **Step 1: Read current pipeline agent file to see Step 7 structure**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -n "Step 7\|Step 6\|Step 5\|Step 4" .claude/agents/newsroom-pipeline.md | head -20`

- [ ] **Step 2: Modify pipeline agent — describe new flow**

Add a new section near Step 7 describing the H1 race-fix flow. Specifically:

After the per-article loop (Master → Skeptic → Render markdown), add a BATCH-LEVEL phase:

```markdown
### Step 7 — Batch git publish (NEW Phase H1)

After all articles in the batch have been rendered to `output/compare-feed/`:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json
from lib.stages.run_git_publish import auto_git_publish
result = auto_git_publish(batch_id='<BATCH_ID>', article_count=<N>)
print(json.dumps(result))
"
```

If `result.ok == False` → FAIL pipeline, log error, do NOT push Telegram.
If `result.ok == True` → record `commit_sha`, proceed to Step 8.

### Step 8 — Wait Pages deploy (NEW Phase H1)

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import json, yaml
from lib.stages.run_pages_wait import wait_pages_deployed
secrets = yaml.safe_load(open('data/secrets.yaml'))
gh = secrets['github']
result = wait_pages_deployed(
    commit_sha='<COMMIT_SHA>',
    token=gh['token'],
    owner=gh['owner'],
    repo=gh['repo'],
    timeout_s=90,
)
print(json.dumps(result))
"
```

Behaviors:
- `result.ok == True` → proceed Step 9 (Telegram push) normally
- `result.ok == False` AND `error == 'timeout'` → proceed Step 9 BUT add fallback note `⚠️ Đang deploy, link có thể chưa work trong 30s` to channel post
- `result.ok == False` AND `error startswith 'deploy failed'` → FAIL pipeline (broken deploy = bad link, do not push Telegram)

### Step 9 — Per-article Telegram push (was Step 7)

For each article (loop), dispatch `newsroom-telegram-publisher` agent as before.
T14b idempotency unchanged. If Step 8 returned timeout fallback, pass extra
`channel_footer_warning="⚠️ Đang deploy, link có thể chưa work trong 30s"`
parameter to the publisher.
```

Apply this conceptually — find the existing Step 7 in the agent file, REPLACE the per-article telegram dispatch with the new ordering: render markdown moves earlier (still per-article), Telegram push moves to AFTER batch git_publish + pages_wait.

- [ ] **Step 3: Update `data/secrets.yaml.example`**

Read current file first, then add new sections. Final content should include (preserving existing telegram block):

```yaml
telegram:
  bot_token: "<BOT_TOKEN>"
  chat_id: "<CHANNEL_ID>"  # main article channel
  linked_group_chat_id: "<LINKED_GROUP_ID>"  # for thread replies
  feedback_group_chat_id: "<NEW — separate group for user feedback>"
  base_url: "https://dangtrungdev113999.github.io/finpath-newsroom"

github:
  # Personal Access Token with `repo` scope (classic) OR
  # Fine-grained PAT with `Actions: Read` permission on this repo.
  # Verify before use:
  #   curl -H "Authorization: Bearer $TOKEN" \
  #     "https://api.github.com/repos/dangtrungdev113999/finpath-newsroom/actions/runs?per_page=1"
  token: "<GH_PAT>"
  owner: "dangtrungdev113999"
  repo: "finpath-newsroom"
```

- [ ] **Step 4: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent"
git add .claude/agents/newsroom-pipeline.md data/secrets.yaml.example
git commit -m "feat(pipeline): Step 7 race-fix flow — git_publish then pages_wait then telegram

Per-article: Master → Skeptic → Render (moved earlier)
Batch tail: git_publish → pages_wait → per-article Telegram push

secrets.yaml.example adds github.{token,owner,repo} + feedback_group_chat_id

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Frontend types + PipelineObservability rows for new steps

**Files:**
- Modify: `web/src/types.ts` (add step_7_git_publish + step_8_pages_wait)
- Modify: `web/src/components/PipelineObservability.tsx` (add row labels)

- [ ] **Step 1: Read current types.ts to find PipelineLog interface**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent/web" && grep -n "PipelineLog\|step_" src/types.ts`

- [ ] **Step 2: Extend PipelineLog interface**

Add to the existing PipelineLog interface in `web/src/types.ts`:

```typescript
// (in PipelineLog interface, alongside existing step_1...step_6)
step_7_git_publish?: {
  ok: boolean;
  commit_sha?: string;
  duration_ms: number;
  self_heal_actions?: string[];
  error?: string;
  stage?: string;
};
step_8_pages_wait?: {
  ok: boolean;
  elapsed_s: number;
  workflow_run_url?: string;
  error?: string;
  run_url?: string;
  fallback?: string;
};
```

- [ ] **Step 3: Add display rows to PipelineObservability**

Edit `web/src/components/PipelineObservability.tsx` STEP_LABELS array — add 2 entries:

```typescript
const STEP_LABELS: Array<{ key: keyof PipelineLog; label: string }> = [
  { key: 'step_1_crawler', label: '1. Crawler' },
  { key: 'step_2_editor', label: '2. Editor V1' },
  { key: 'step_3_story_editor', label: '3. Story Editor' },
  { key: 'step_4_master', label: '4. Master' },
  { key: 'step_5_skeptic', label: '5. Skeptic' },
  { key: 'step_6_render', label: '6. Render' },
  { key: 'step_7_git_publish', label: '7. Git publish' },
  { key: 'step_8_pages_wait', label: '8. Pages deploy' },
];
```

Note: `step_7_git_publish` schema differs from `StepLog` (uses `commit_sha`, `self_heal_actions` instead of `model`, `tokens`). The current row renderer reads `log.model`, `log.duration_ms`, `log.tokens` — for step 7 these are absent. The renderer at line 47-58 already uses `??  '—'` for missing values, so it gracefully shows `—` for `model` and `tokens`. Acceptable.

- [ ] **Step 4: Run TypeScript check**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit`
Expected: 0 errors

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent"
git add web/src/types.ts web/src/components/PipelineObservability.tsx
git commit -m "feat(web): PipelineObservability rows for step 7 (git_publish) + 8 (pages_wait)

PipelineLog interface extends with H1 race-fix step entries.
TypeScript check clean.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: H1 close-out — E2E verify + tag

**Files:** none (verification + tag only)

- [ ] **Step 1: Verify GitHub PAT works (USER MAY HAVE ALREADY ADDED TOKEN)**

If `data/secrets.yaml` does NOT yet have `github.token`, this verification will skip the live API check. Document the curl command for the user to run manually:

```bash
# User runs this manually (subagent cannot guess token):
TOKEN=$(grep -A1 'github:' data/secrets.yaml | grep token | awk -F'"' '{print $2}')
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/dangtrungdev113999/finpath-newsroom/actions/runs?per_page=1"
# Expect 200 + JSON. 401/403 → token wrong scope, regenerate.
```

If token IS configured, run the curl test to confirm 200 OK. Otherwise leave a TODO note in the H1 close-out summary.

- [ ] **Step 2: Run all unit tests**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run pytest tests/test_run_git_publish.py tests/test_run_pages_wait.py -v`
Expected: 13 tests pass

- [ ] **Step 3: TypeScript build**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit && npm run build`
Expected: 0 TS errors, build succeeds

- [ ] **Step 4: Tag H1 close-out**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent"
git tag -a v4.0-phase-h1-deploy-race-fix -m "Phase H1 — pipeline auto git publish + Pages deploy poll + Telegram

- lib/stages/run_git_publish.py: 7 self-heal cases tested
- lib/stages/run_pages_wait.py: 6 poll scenarios tested
- pipeline agent updated with new Step 7-9 flow
- frontend PipelineObservability shows new step rows
- secrets.yaml.example documents github.token + feedback_group_chat_id

Race condition: Telegram link to /article/<slug> now guaranteed deployed
before push (or fallback note added on 90s timeout)."
```

NOTE: do NOT push tag yet — user wakes up first, may want to verify with live `/tin` run before tagging publicly. Tag stays local.

---

## Phase H2a — Comment frontend (autonomous)

### Task 8: localStorage utility + tests (TDD)

**Files:**
- Create: `web/src/lib/feedbackStorage.ts`
- Create: `web/src/lib/__tests__/feedbackStorage.test.ts`

- [ ] **Step 1: Write failing tests**

```typescript
// web/src/lib/__tests__/feedbackStorage.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  getStorage,
  saveName,
  appendComment,
  getCommentsForArticle,
  resetStorage,
  isStorageDisabled,
} from '../feedbackStorage';

describe('feedbackStorage', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('initializes with null name and generated client_id', () => {
    const s = getStorage();
    expect(s.name).toBeNull();
    expect(s.client_id).toMatch(/^[0-9a-f-]{36}$/);
    expect(s.comments).toEqual({});
  });

  it('persists name across reads', () => {
    saveName('Trung');
    expect(getStorage().name).toBe('Trung');
  });

  it('appends comment to article-specific list', () => {
    appendComment('vcb-123', { comment: 'hay', timestamp: '2026-05-11T08:00:00Z' });
    appendComment('vcb-123', { comment: 'lủng', timestamp: '2026-05-11T09:00:00Z' });
    appendComment('tcb-456', { comment: 'ok', timestamp: '2026-05-11T10:00:00Z' });
    const vcb = getCommentsForArticle('vcb-123');
    expect(vcb).toHaveLength(2);
    expect(vcb[0].comment).toBe('hay');
    const tcb = getCommentsForArticle('tcb-456');
    expect(tcb).toHaveLength(1);
  });

  it('returns empty array for unknown article', () => {
    expect(getCommentsForArticle('unknown')).toEqual([]);
  });

  it('reuses existing client_id across calls', () => {
    const a = getStorage().client_id;
    const b = getStorage().client_id;
    expect(a).toBe(b);
  });

  it('resetStorage clears everything', () => {
    saveName('x');
    appendComment('a', { comment: 'c', timestamp: 't' });
    resetStorage();
    const s = getStorage();
    expect(s.name).toBeNull();
    expect(s.comments).toEqual({});
  });

  it('detects disabled localStorage', () => {
    const original = Storage.prototype.setItem;
    Storage.prototype.setItem = vi.fn(() => {
      throw new Error('disabled');
    });
    expect(isStorageDisabled()).toBe(true);
    Storage.prototype.setItem = original;
  });
});
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx vitest run src/lib/__tests__/feedbackStorage.test.ts`
Expected: FAIL — module missing

---

### Task 9: Implement `feedbackStorage.ts`

**Files:**
- Create: `web/src/lib/feedbackStorage.ts`

- [ ] **Step 1: Implement module**

```typescript
// web/src/lib/feedbackStorage.ts
/**
 * localStorage-backed feedback state.
 *
 * Schema (under key `finpath-newsroom-feedback`):
 *   { name: string|null, client_id: uuid, comments: { [article_id]: Entry[] } }
 *
 * Falls back to in-memory if localStorage throws (private mode, quota).
 */

const STORAGE_KEY = 'finpath-newsroom-feedback';

export interface CommentEntry {
  comment: string;
  timestamp: string; // ISO 8601
  telegram_message_id?: number;
}

export interface FeedbackStorage {
  name: string | null;
  client_id: string;
  comments: Record<string, CommentEntry[]>;
}

// In-memory fallback when localStorage unavailable
let memoryFallback: FeedbackStorage | null = null;
let storageBroken = false;

function uuidv4(): string {
  // crypto.randomUUID is available in modern browsers + Vite dev; fall back to manual
  if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
    return crypto.randomUUID();
  }
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16);
  });
}

function defaultStorage(): FeedbackStorage {
  return { name: null, client_id: uuidv4(), comments: {} };
}

function tryRead(): FeedbackStorage {
  if (storageBroken) return memoryFallback ?? (memoryFallback = defaultStorage());
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      const fresh = defaultStorage();
      tryWrite(fresh);
      return fresh;
    }
    const parsed = JSON.parse(raw) as FeedbackStorage;
    // Defensive: ensure shape (legacy or corrupted entries)
    if (!parsed.client_id) parsed.client_id = uuidv4();
    if (!parsed.comments) parsed.comments = {};
    if (parsed.name === undefined) parsed.name = null;
    return parsed;
  } catch {
    storageBroken = true;
    memoryFallback = defaultStorage();
    return memoryFallback;
  }
}

function tryWrite(s: FeedbackStorage): void {
  if (storageBroken) {
    memoryFallback = s;
    return;
  }
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
  } catch {
    storageBroken = true;
    memoryFallback = s;
  }
}

export function getStorage(): FeedbackStorage {
  return tryRead();
}

export function saveName(name: string): void {
  const s = tryRead();
  s.name = name;
  tryWrite(s);
}

export function appendComment(article_id: string, entry: CommentEntry): void {
  const s = tryRead();
  if (!s.comments[article_id]) s.comments[article_id] = [];
  s.comments[article_id].push(entry);
  tryWrite(s);
}

export function getCommentsForArticle(article_id: string): CommentEntry[] {
  return tryRead().comments[article_id] ?? [];
}

export function resetStorage(): void {
  storageBroken = false;
  memoryFallback = null;
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    /* ignore */
  }
}

export function isStorageDisabled(): boolean {
  if (storageBroken) return true;
  try {
    const test = '__finpath_test__';
    localStorage.setItem(test, '1');
    localStorage.removeItem(test);
    return false;
  } catch {
    storageBroken = true;
    return true;
  }
}
```

- [ ] **Step 2: Run tests**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx vitest run src/lib/__tests__/feedbackStorage.test.ts`
Expected: PASS all 7 tests

- [ ] **Step 3: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent"
git add web/src/lib/feedbackStorage.ts web/src/lib/__tests__/feedbackStorage.test.ts
git commit -m "feat(web): feedbackStorage util — localStorage with in-memory fallback

Schema: {name, client_id (uuid), comments: per-article-id[]}
Graceful degrade when localStorage throws (private mode/quota).
7 tests pass.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 10: feedbackClient — Worker POST wrapper

**Files:**
- Create: `web/src/lib/feedbackClient.ts`

- [ ] **Step 1: Implement client (no tests — thin wrapper, will exercise via component)**

```typescript
// web/src/lib/feedbackClient.ts
/**
 * POST feedback to Cloudflare Worker proxy.
 * Worker URL injected at build time via VITE_FEEDBACK_WORKER_URL.
 * If env var missing → isFeedbackEnabled() returns false; UI hides.
 */

const WORKER_URL = import.meta.env.VITE_FEEDBACK_WORKER_URL as string | undefined;

export const isFeedbackEnabled = (): boolean => Boolean(WORKER_URL && WORKER_URL.startsWith('http'));

export interface FeedbackPayload {
  name: string;
  article_id: string;
  article_title: string;
  ticker: string;
  comment: string;
  timestamp: string;
  client_id: string;
}

export interface FeedbackOk {
  ok: true;
  telegram_message_id: number;
}

export interface FeedbackErr {
  ok: false;
  error: 'validation' | 'rate_limited' | 'telegram_fail' | 'network' | 'disabled';
  message?: string;
  field?: string;
  retry_after?: number;
}

export type FeedbackResult = FeedbackOk | FeedbackErr;

export async function submitFeedback(payload: FeedbackPayload): Promise<FeedbackResult> {
  if (!isFeedbackEnabled()) {
    return { ok: false, error: 'disabled', message: 'Feature flag off (no Worker URL)' };
  }
  try {
    const resp = await fetch(`${WORKER_URL}/api/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const json = (await resp.json()) as FeedbackResult;
    return json;
  } catch (e) {
    return {
      ok: false,
      error: 'network',
      message: e instanceof Error ? e.message : 'unknown network error',
    };
  }
}
```

- [ ] **Step 2: TypeScript check**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit`
Expected: 0 errors

- [ ] **Step 3: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent"
git add web/src/lib/feedbackClient.ts
git commit -m "feat(web): feedbackClient — Worker POST + isFeedbackEnabled flag

Reads VITE_FEEDBACK_WORKER_URL at build. Missing → disabled status.
Returns typed FeedbackResult union for caller pattern-match.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 11: CommentSection component + tests

**Files:**
- Create: `web/src/components/CommentSection.tsx`
- Create: `web/src/components/__tests__/CommentSection.test.tsx`

- [ ] **Step 1: Write tests covering states**

```tsx
// web/src/components/__tests__/CommentSection.test.tsx
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { CommentSection } from '../CommentSection';
import * as client from '../../lib/feedbackClient';
import { resetStorage, saveName } from '../../lib/feedbackStorage';

beforeEach(() => {
  resetStorage();
  vi.spyOn(client, 'isFeedbackEnabled').mockReturnValue(true);
});

describe('CommentSection', () => {
  it('renders nothing when isFeedbackEnabled() is false', () => {
    vi.spyOn(client, 'isFeedbackEnabled').mockReturnValue(false);
    const { container } = render(
      <CommentSection articleId="x" articleTitle="t" ticker="VCB" />,
    );
    expect(container.firstChild).toBeNull();
  });

  it('renders collapsed CTA initially', () => {
    render(<CommentSection articleId="x" articleTitle="t" ticker="VCB" />);
    expect(screen.getByText(/Góp ý cho bài này/)).toBeInTheDocument();
  });

  it('expands to show form on click', () => {
    render(<CommentSection articleId="x" articleTitle="t" ticker="VCB" />);
    fireEvent.click(screen.getByText(/Góp ý cho bài này/));
    expect(screen.getByPlaceholderText(/Nhập góp ý/)).toBeInTheDocument();
  });

  it('shows name field on first use, hides after saved', () => {
    const { rerender } = render(
      <CommentSection articleId="x" articleTitle="t" ticker="VCB" />,
    );
    fireEvent.click(screen.getByText(/Góp ý cho bài này/));
    expect(screen.getByPlaceholderText(/Tên/)).toBeInTheDocument();

    saveName('Trung');
    rerender(<CommentSection articleId="x" articleTitle="t" ticker="VCB" />);
    fireEvent.click(screen.getByText(/Góp ý cho bài này/));
    expect(screen.queryByPlaceholderText(/Tên/)).toBeNull();
  });

  it('disables submit when comment too short', () => {
    saveName('Trung');
    render(<CommentSection articleId="x" articleTitle="t" ticker="VCB" />);
    fireEvent.click(screen.getByText(/Góp ý cho bài này/));
    const ta = screen.getByPlaceholderText(/Nhập góp ý/);
    fireEvent.change(ta, { target: { value: 'hi' } });
    expect(screen.getByRole('button', { name: /Gửi/ })).toBeDisabled();
  });

  it('submits payload then clears textarea on success', async () => {
    saveName('Trung');
    const submitSpy = vi
      .spyOn(client, 'submitFeedback')
      .mockResolvedValue({ ok: true, telegram_message_id: 999 });
    render(<CommentSection articleId="vcb-1" articleTitle="VCB" ticker="VCB" />);
    fireEvent.click(screen.getByText(/Góp ý cho bài này/));
    const ta = screen.getByPlaceholderText(/Nhập góp ý/) as HTMLTextAreaElement;
    fireEvent.change(ta, { target: { value: 'câu opening hơi lủng' } });
    fireEvent.click(screen.getByRole('button', { name: /Gửi/ }));

    await waitFor(() => expect(submitSpy).toHaveBeenCalled());
    const payload = submitSpy.mock.calls[0][0];
    expect(payload.name).toBe('Trung');
    expect(payload.comment).toBe('câu opening hơi lủng');
    expect(payload.article_id).toBe('vcb-1');
    expect(payload.ticker).toBe('VCB');

    await waitFor(() => expect(ta.value).toBe(''));
  });

  it('keeps textarea on rate-limit error', async () => {
    saveName('Trung');
    vi.spyOn(client, 'submitFeedback').mockResolvedValue({
      ok: false,
      error: 'rate_limited',
      retry_after: 240,
    });
    render(<CommentSection articleId="x" articleTitle="t" ticker="VCB" />);
    fireEvent.click(screen.getByText(/Góp ý cho bài này/));
    const ta = screen.getByPlaceholderText(/Nhập góp ý/) as HTMLTextAreaElement;
    fireEvent.change(ta, { target: { value: 'thử submit khi rate limit' } });
    fireEvent.click(screen.getByRole('button', { name: /Gửi/ }));

    await waitFor(() => expect(screen.getByText(/đợi vài phút/i)).toBeInTheDocument());
    expect(ta.value).toBe('thử submit khi rate limit');
  });

  it('shows local history badge when comments exist', () => {
    saveName('Trung');
    // simulate prior comment
    const { appendComment } = require('../../lib/feedbackStorage');
    appendComment('vcb-1', { comment: 'cũ', timestamp: '2026-05-11T00:00:00Z' });
    render(<CommentSection articleId="vcb-1" articleTitle="t" ticker="VCB" />);
    expect(screen.getByText(/1/)).toBeInTheDocument(); // badge count
  });
});
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx vitest run src/components/__tests__/CommentSection.test.tsx`
Expected: FAIL — component missing

---

### Task 12: Implement `CommentSection.tsx`

**Files:**
- Create: `web/src/components/CommentSection.tsx`

- [ ] **Step 1: Implement component**

```tsx
// web/src/components/CommentSection.tsx
import { useState, useMemo } from 'react';
import {
  appendComment,
  getCommentsForArticle,
  getStorage,
  isStorageDisabled,
  saveName,
} from '../lib/feedbackStorage';
import { isFeedbackEnabled, submitFeedback } from '../lib/feedbackClient';

interface Props {
  articleId: string;
  articleTitle: string;
  ticker: string;
}

type FormState = 'idle' | 'submitting' | 'success' | 'error';

const MIN_COMMENT = 5;
const MAX_COMMENT = 1000;
const MIN_NAME = 1;
const MAX_NAME = 50;

export function CommentSection({ articleId, articleTitle, ticker }: Props) {
  // Feature flag — entire section absent in environments without Worker URL
  if (!isFeedbackEnabled()) return null;

  const [expanded, setExpanded] = useState(false);
  const [state, setState] = useState<FormState>('idle');
  const [errMsg, setErrMsg] = useState<string | null>(null);
  const [comment, setComment] = useState('');
  const [nameInput, setNameInput] = useState('');

  // Refresh on each render so badge count + history always live.
  // Cheap (sync read) — fine for low-volume feedback UI.
  const storage = getStorage();
  const savedName = storage.name;
  const history = getCommentsForArticle(articleId);
  const showNameField = !savedName;
  const storageDisabled = useMemo(() => isStorageDisabled(), []);

  const trimmedComment = comment.trim();
  const trimmedName = nameInput.trim();
  const effectiveName = savedName ?? trimmedName;
  const canSubmit =
    trimmedComment.length >= MIN_COMMENT &&
    trimmedComment.length <= MAX_COMMENT &&
    effectiveName.length >= MIN_NAME &&
    effectiveName.length <= MAX_NAME &&
    state !== 'submitting';

  async function onSubmit() {
    if (!canSubmit) return;
    setState('submitting');
    setErrMsg(null);

    // Capture name on first submit
    if (showNameField) saveName(trimmedName);

    const payload = {
      name: effectiveName,
      article_id: articleId,
      article_title: articleTitle,
      ticker,
      comment: trimmedComment,
      timestamp: new Date().toISOString(),
      client_id: storage.client_id,
    };

    const result = await submitFeedback(payload);
    if (result.ok) {
      appendComment(articleId, {
        comment: trimmedComment,
        timestamp: payload.timestamp,
        telegram_message_id: result.telegram_message_id,
      });
      setComment('');
      setState('success');
      setTimeout(() => setState('idle'), 2500);
      return;
    }

    // Error path — KEEP textarea
    let msg = result.message ?? 'Lỗi không xác định';
    if (result.error === 'rate_limited') {
      msg = `Bạn đang góp ý quá nhanh, đợi vài phút (${result.retry_after ?? 240}s)`;
    } else if (result.error === 'validation') {
      msg = `Lỗi nhập liệu (${result.field}): ${result.message ?? 'không hợp lệ'}`;
    } else if (result.error === 'telegram_fail') {
      msg = `Không gửi được tới Telegram: ${result.message ?? ''}`;
    } else if (result.error === 'network') {
      msg = 'Mất kết nối, thử lại nhé';
    } else if (result.error === 'disabled') {
      msg = 'Tính năng góp ý đang tắt (build thiếu Worker URL)';
    }
    setErrMsg(msg);
    setState('error');
  }

  return (
    <section className="mt-8 border-t border-fg-4/40 pt-6">
      <button
        type="button"
        onClick={() => setExpanded((v) => !v)}
        className="flex w-full items-center justify-between rounded-md bg-bg-2 px-4 py-3 text-sm font-semibold text-fg-1 transition-colors hover:bg-bg-3/60"
        aria-expanded={expanded}
      >
        <span>
          💬 Góp ý cho bài này
          {history.length > 0 && (
            <span className="ml-2 rounded-pill bg-bg-3 px-2 py-0.5 text-xs font-normal text-fg-2">
              Đã gửi: {history.length}
            </span>
          )}
        </span>
        <span className="text-fg-3">{expanded ? '▴' : '▾'}</span>
      </button>

      {expanded && (
        <div className="mt-3 rounded-md border border-fg-4/40 bg-bg-1 p-4">
          {storageDisabled && (
            <div className="mb-3 rounded-md bg-warn/10 px-3 py-2 text-xs text-warn">
              ⚠️ Lưu trữ local bị tắt — lịch sử góp ý sẽ mất khi reload.
            </div>
          )}

          {showNameField && (
            <div className="mb-3">
              <label className="mb-1 block text-xs font-semibold text-fg-2">Tên</label>
              <input
                type="text"
                placeholder="Tên (sẽ lưu cho lần sau)"
                value={nameInput}
                onChange={(e) => setNameInput(e.target.value)}
                maxLength={MAX_NAME}
                className="w-full rounded-md border border-fg-4 bg-bg-1 px-3 py-2 text-sm text-fg-0 focus:border-brand focus:outline-none"
              />
            </div>
          )}

          <textarea
            placeholder="Nhập góp ý (5-1000 ký tự)…"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            maxLength={MAX_COMMENT}
            rows={3}
            className="w-full resize-y rounded-md border border-fg-4 bg-bg-1 px-3 py-2 text-sm text-fg-0 focus:border-brand focus:outline-none"
          />
          <div className="mt-1 text-right text-xs text-fg-3">
            {trimmedComment.length}/{MAX_COMMENT} ký tự
          </div>

          <div className="mt-3 flex items-center gap-3">
            <button
              type="button"
              onClick={onSubmit}
              disabled={!canSubmit}
              className="rounded-md bg-brand px-4 py-2 text-sm font-medium text-brand-fg transition-colors hover:bg-brand-hot disabled:cursor-not-allowed disabled:opacity-50"
            >
              {state === 'submitting' ? 'Đang gửi…' : 'Gửi'}
            </button>
            {state === 'success' && (
              <span className="text-sm text-done">✅ Đã gửi</span>
            )}
            {state === 'error' && errMsg && (
              <span className="text-sm text-rec">❌ {errMsg}</span>
            )}
          </div>

          {history.length > 0 && (
            <div className="mt-5 border-t border-fg-4/40 pt-4">
              <h4 className="mb-2 text-xs font-semibold uppercase tracking-wide text-fg-3">
                Lịch sử góp ý của bạn ({history.length})
              </h4>
              <ul className="space-y-2 pl-0 text-sm">
                {history.map((h, i) => (
                  <li key={i} className="border-l-2 border-fg-4/60 pl-3">
                    <div className="text-fg-1">{h.comment}</div>
                    <div className="text-xs text-fg-3">
                      {new Date(h.timestamp).toLocaleString('vi-VN')}
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
```

- [ ] **Step 2: Run tests**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx vitest run src/components/__tests__/CommentSection.test.tsx`
Expected: PASS all 8 tests

- [ ] **Step 3: TypeScript check**

Run: `cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit`
Expected: 0 errors

- [ ] **Step 4: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent"
git add web/src/lib/feedbackClient.ts web/src/components/CommentSection.tsx web/src/components/__tests__/CommentSection.test.tsx
git commit -m "feat(web): CommentSection — collapsed CTA + form + history (Phase H2a)

Render-nothing when isFeedbackEnabled() = false (no Worker URL).
Shows name field first time, caches in localStorage.
8 tests pass — states (collapsed/expanded/submitting/success/error)
and validation paths covered.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 13: Wire CommentSection into CompareFeedLayout + workflow env injection

**Files:**
- Modify: `web/src/components/CompareFeedLayout.tsx`
- Modify: `.github/workflows/deploy.yml`

- [ ] **Step 1: Read current CompareFeedLayout**

Run: `cat "/Users/trungdt/Desktop/Stream Intelligent/web/src/components/CompareFeedLayout.tsx"`

- [ ] **Step 2: Add CommentSection at bottom of article**

Edit `web/src/components/CompareFeedLayout.tsx`:
- Import: `import { CommentSection } from './CommentSection';`
- Render after the grid (or single-column container in focus mode), respecting `showRight` constraint:

```tsx
{showRight ? (
  <div className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-6">
    <LeftColumn meta={meta.left_meta} body={leftMarkdown} />
    <RightColumn meta={meta} />
  </div>
) : (
  <div className="max-w-3xl mx-auto">
    <LeftColumn meta={meta.left_meta} body={leftMarkdown} />
  </div>
)}

{/* Phase H2 — comment feedback */}
<div className={showRight ? '' : 'max-w-3xl mx-auto'}>
  <CommentSection
    articleId={meta.public_slug ?? meta.title}
    articleTitle={meta.title}
    ticker={meta.ticker ?? ''}
  />
</div>
```

NOTE: `meta.public_slug` and `meta.ticker` field names — verify they exist in `web/src/types.ts ArticleMeta`. If not, fall back to existing identifiers (`meta.title` for both is acceptable degradation).

- [ ] **Step 3: Update `.github/workflows/deploy.yml` env injection**

Edit `.github/workflows/deploy.yml`, find the "Build Vite production" step, add `VITE_FEEDBACK_WORKER_URL` to env:

```yaml
- name: Build Vite production
  working-directory: web
  env:
    VITE_DEPLOY: '1'
    VITE_FEEDBACK_WORKER_URL: ${{ secrets.VITE_FEEDBACK_WORKER_URL }}
  run: npm run build
```

If `VITE_FEEDBACK_WORKER_URL` secret is unset in repo settings, GitHub passes empty string → `isFeedbackEnabled()` returns false → comment section hidden in production. NO BROKEN STATE.

- [ ] **Step 4: TypeScript check + production build (NO env var → comment section absent)**

Run:
```bash
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npx tsc --noEmit
cd "/Users/trungdt/Desktop/Stream Intelligent/web" && npm run build
```
Expected: 0 errors, build succeeds. CommentSection imported but won't render.

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent"
git add web/src/components/CompareFeedLayout.tsx .github/workflows/deploy.yml
git commit -m "feat(web): wire CommentSection into article layout + workflow env injection

CommentSection renders bottom of each article, respects showRight focus mode.
.github/workflows/deploy.yml passes VITE_FEEDBACK_WORKER_URL secret to Vite
build. Missing secret → empty string → feature flag hides UI gracefully.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Phase H2b — Worker code (autonomous code, manual deploy)

### Task 14: Cloudflare Worker — feedback proxy

**Files:**
- Create: `worker/feedback.ts`
- Create: `worker/wrangler.toml`
- Create: `worker/README.md`
- Create: `worker/package.json` (so wrangler can find TypeScript)
- Create: `worker/tsconfig.json`

- [ ] **Step 1: Create `worker/feedback.ts`**

```typescript
// worker/feedback.ts
/**
 * Cloudflare Worker — comment feedback proxy.
 *
 * Endpoint: POST /api/feedback
 * Validates payload, rate-limits per client_id (KV), forwards to Telegram
 * group as a flat text message.
 *
 * Secrets (set via `wrangler secret put`):
 *   TELEGRAM_BOT_TOKEN
 *   TELEGRAM_FEEDBACK_GROUP_ID
 *
 * KV binding (in wrangler.toml):
 *   FEEDBACK_RL — rate-limit buckets (key: rl:<client_id>:<hour>)
 */

interface Env {
  TELEGRAM_BOT_TOKEN: string;
  TELEGRAM_FEEDBACK_GROUP_ID: string;
  FEEDBACK_RL: KVNamespace;
}

const ALLOWED_ORIGINS = [
  'https://dangtrungdev113999.github.io',
  'http://localhost:5174',
  'http://localhost:5175',
];

const MAX_REQS_PER_HOUR = 10;
const SECONDS_PER_HOUR = 3600;

const TICKER_RE = /^[A-Z]{3,4}$/;
const SLUG_RE = /^[a-z0-9-]+$/;
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

interface FeedbackPayload {
  name: string;
  article_id: string;
  article_title: string;
  ticker: string;
  comment: string;
  timestamp: string;
  client_id: string;
}

function corsHeaders(origin: string | null): Record<string, string> {
  const allowed = origin && ALLOWED_ORIGINS.includes(origin) ? origin : '';
  return {
    'Access-Control-Allow-Origin': allowed,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Vary': 'Origin',
  };
}

function jsonResponse(body: unknown, status: number, origin: string | null): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) },
  });
}

function htmlEscape(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function validate(p: Partial<FeedbackPayload>): { ok: true; v: FeedbackPayload } | { ok: false; field: string; message: string } {
  if (!p.name || typeof p.name !== 'string') return { ok: false, field: 'name', message: 'thiếu' };
  const name = p.name.trim().replace(/[\x00-\x1f]/g, '');
  if (name.length < 1 || name.length > 50) return { ok: false, field: 'name', message: '1-50 ký tự' };

  if (!p.comment || typeof p.comment !== 'string') return { ok: false, field: 'comment', message: 'thiếu' };
  const comment = p.comment.trim();
  if (comment.length < 5 || comment.length > 1000) return { ok: false, field: 'comment', message: '5-1000 ký tự' };

  if (!p.ticker || !TICKER_RE.test(p.ticker)) return { ok: false, field: 'ticker', message: 'invalid ticker' };
  if (!p.article_id || !SLUG_RE.test(p.article_id) || p.article_id.length > 200) {
    return { ok: false, field: 'article_id', message: 'invalid slug' };
  }
  if (!p.article_title || typeof p.article_title !== 'string' || p.article_title.length > 500) {
    return { ok: false, field: 'article_title', message: 'invalid title' };
  }
  if (!p.client_id || !UUID_RE.test(p.client_id)) return { ok: false, field: 'client_id', message: 'invalid uuid' };

  if (!p.timestamp || typeof p.timestamp !== 'string') return { ok: false, field: 'timestamp', message: 'thiếu' };
  const ts = Date.parse(p.timestamp);
  if (isNaN(ts)) return { ok: false, field: 'timestamp', message: 'invalid ISO' };
  const nowMs = Date.now();
  if (ts > nowMs + 5 * 60 * 1000) return { ok: false, field: 'timestamp', message: 'in future' };
  if (ts < nowMs - 24 * 60 * 60 * 1000) return { ok: false, field: 'timestamp', message: 'too old' };

  return {
    ok: true,
    v: {
      name,
      article_id: p.article_id,
      article_title: p.article_title,
      ticker: p.ticker,
      comment,
      timestamp: p.timestamp,
      client_id: p.client_id,
    },
  };
}

async function rateLimitCheck(kv: KVNamespace, client_id: string): Promise<{ ok: true } | { ok: false; retry_after: number }> {
  const nowSec = Math.floor(Date.now() / 1000);
  const hourBucket = Math.floor(nowSec / SECONDS_PER_HOUR);
  const key = `rl:${client_id}:${hourBucket}`;
  const current = parseInt((await kv.get(key)) ?? '0', 10);
  if (current >= MAX_REQS_PER_HOUR) {
    const retry_after = SECONDS_PER_HOUR - (nowSec % SECONDS_PER_HOUR);
    return { ok: false, retry_after };
  }
  await kv.put(key, String(current + 1), { expirationTtl: SECONDS_PER_HOUR });
  return { ok: true };
}

function buildTelegramMessage(p: FeedbackPayload, baseUrl: string): string {
  const url = `${baseUrl}/article/${p.article_id}`;
  const tsLocal = new Date(p.timestamp).toLocaleString('vi-VN', {
    timeZone: 'Asia/Ho_Chi_Minh',
    hour12: false,
  });
  return [
    `💬 <b>Góp ý cho bài [${htmlEscape(p.ticker)}]</b>`,
    `<b>${htmlEscape(p.article_title)}</b>`,
    ``,
    `<b>${htmlEscape(p.name)}</b>: ${htmlEscape(p.comment)}`,
    ``,
    `🔗 ${url}`,
    `🕐 ${tsLocal}`,
  ].join('\n');
}

async function postTelegram(env: Env, text: string): Promise<{ ok: true; message_id: number } | { ok: false; message: string }> {
  const url = `https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`;
  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: env.TELEGRAM_FEEDBACK_GROUP_ID,
      text,
      parse_mode: 'HTML',
      disable_web_page_preview: false,
    }),
  });
  const data = (await resp.json()) as { ok: boolean; result?: { message_id: number }; description?: string };
  if (data.ok && data.result) {
    return { ok: true, message_id: data.result.message_id };
  }
  return { ok: false, message: data.description ?? 'unknown telegram error' };
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const origin = req.headers.get('Origin');
    const url = new URL(req.url);

    if (req.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }

    if (url.pathname !== '/api/feedback' || req.method !== 'POST') {
      return jsonResponse({ ok: false, error: 'not_found' }, 404, origin);
    }

    if (!origin || !ALLOWED_ORIGINS.includes(origin)) {
      return jsonResponse({ ok: false, error: 'origin_not_allowed' }, 403, origin);
    }

    let payload: Partial<FeedbackPayload>;
    try {
      payload = (await req.json()) as Partial<FeedbackPayload>;
    } catch {
      return jsonResponse({ ok: false, error: 'validation', message: 'invalid json' }, 400, origin);
    }

    const v = validate(payload);
    if (!v.ok) {
      return jsonResponse({ ok: false, error: 'validation', field: v.field, message: v.message }, 400, origin);
    }

    const rl = await rateLimitCheck(env.FEEDBACK_RL, v.v.client_id);
    if (!rl.ok) {
      return jsonResponse({ ok: false, error: 'rate_limited', retry_after: rl.retry_after }, 429, origin);
    }

    const baseUrl = origin.replace(/\/$/, '') + (origin.endsWith('github.io') ? '/finpath-newsroom' : '');
    const text = buildTelegramMessage(v.v, baseUrl);

    const tg = await postTelegram(env, text);
    if (!tg.ok) {
      return jsonResponse({ ok: false, error: 'telegram_fail', message: tg.message }, 502, origin);
    }

    return jsonResponse({ ok: true, telegram_message_id: tg.message_id }, 200, origin);
  },
};
```

- [ ] **Step 2: Create `worker/wrangler.toml`**

```toml
name = "feedback-finpath"
main = "feedback.ts"
compatibility_date = "2025-01-01"

# KV namespace for rate-limit buckets — `id` populated after `wrangler kv:namespace create FEEDBACK_RL`
[[kv_namespaces]]
binding = "FEEDBACK_RL"
id = "REPLACE_WITH_KV_ID_FROM_WRANGLER_OUTPUT"

# Secrets (set via `wrangler secret put`):
#   TELEGRAM_BOT_TOKEN
#   TELEGRAM_FEEDBACK_GROUP_ID
```

- [ ] **Step 3: Create `worker/package.json`**

```json
{
  "name": "feedback-worker",
  "private": true,
  "version": "1.0.0",
  "devDependencies": {
    "@cloudflare/workers-types": "^4.20250101.0",
    "wrangler": "^3.0.0"
  }
}
```

- [ ] **Step 4: Create `worker/tsconfig.json`**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "Bundler",
    "lib": ["ES2022"],
    "types": ["@cloudflare/workers-types"],
    "strict": true,
    "noEmit": true,
    "isolatedModules": true,
    "skipLibCheck": true
  },
  "include": ["feedback.ts"]
}
```

- [ ] **Step 5: Create `worker/README.md`**

```markdown
# Feedback Worker — Cloudflare deploy guide

Comment feedback proxy: receives POST from `/feed` page, validates, rate-limits, forwards to Telegram.

## One-time setup (USER must do, subagent cannot)

1. Install wrangler if not present:
   ```bash
   npm i -g wrangler
   ```

2. Login to Cloudflare:
   ```bash
   wrangler login
   ```

3. Create KV namespace for rate-limiting:
   ```bash
   cd worker
   wrangler kv:namespace create FEEDBACK_RL
   # Copy the printed `id` into wrangler.toml replacing REPLACE_WITH_KV_ID_FROM_WRANGLER_OUTPUT
   ```

4. Set secrets:
   ```bash
   wrangler secret put TELEGRAM_BOT_TOKEN
   # Paste bot token from data/secrets.yaml `telegram.bot_token`

   wrangler secret put TELEGRAM_FEEDBACK_GROUP_ID
   # Paste the FEEDBACK group chat id (NOT the article channel chat id)
   # Format: -100xxxxxxxxxx (with -100 prefix for supergroup)
   ```

5. Deploy:
   ```bash
   wrangler deploy
   # Output prints Worker URL: https://feedback-finpath.<account>.workers.dev
   ```

6. Add Worker URL to GitHub Actions secrets:
   - GitHub repo → Settings → Secrets and variables → Actions
   - Add new secret: `VITE_FEEDBACK_WORKER_URL` = `https://feedback-finpath.<account>.workers.dev`

7. Trigger Pages rebuild so new env var is baked in:
   ```bash
   git commit --allow-empty -m "trigger pages rebuild for VITE_FEEDBACK_WORKER_URL"
   git push
   ```

8. Verify: open production `/feed`, check that "💬 Góp ý cho bài này" CTA appears under each article.

## Local dev

```bash
cd worker
wrangler dev
# Hits http://localhost:8787/api/feedback
```

In `web/.env.local`:
```
VITE_FEEDBACK_WORKER_URL=http://localhost:8787
```

Then `cd web && npm run dev` → comment section uses local Worker.

## CORS

Worker allows: `https://dangtrungdev113999.github.io`, `http://localhost:5174`, `http://localhost:5175`. Other origins → 403.

## Rate limit

Per `client_id` (uuid in browser localStorage): max 10 requests/hour.
Stored in KV bucket key `rl:<client_id>:<hour_bucket>` with 1h TTL.
```

- [ ] **Step 6: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent"
git add worker/
git commit -m "feat(worker): Cloudflare Worker feedback proxy code (Phase H2b)

- worker/feedback.ts: validation + rate-limit (KV) + Telegram relay
- worker/wrangler.toml: KV binding placeholder
- worker/README.md: USER setup guide (wrangler login + secrets + deploy)
- HTML escape includes quotes; CORS allowlist localhost dev origins

User must run setup steps in worker/README.md to activate.
GitHub secret VITE_FEEDBACK_WORKER_URL needed for production frontend.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 15: 🛑 STOP — USER ACTION REQUIRED

**This is not a code task.** When subagent reaches this point, halt execution and produce a summary report:

```
═══════════════════════════════════════════════════════════════
✅ Phase H — autonomous portion COMPLETE

Done autonomously:
  H1 (race fix):
    ✓ T1-T2: lib/stages/run_git_publish.py + 7 tests pass
    ✓ T3-T4: lib/stages/run_pages_wait.py + 6 tests pass
    ✓ T5: pipeline agent updated (Step 7-9 flow)
    ✓ T6: PipelineLog types + observability rows
    ✓ T7: H1 close-out, tag v4.0-phase-h1-deploy-race-fix (LOCAL ONLY, not pushed)

  H2a (frontend code):
    ✓ T8-T9: feedbackStorage.ts + 7 tests
    ✓ T10: feedbackClient.ts (feature flag wrapper)
    ✓ T11-T12: CommentSection.tsx + 8 tests
    ✓ T13: wired into CompareFeedLayout + .github/workflows/deploy.yml env injection

  H2b (Worker code):
    ✓ T14: worker/{feedback.ts, wrangler.toml, README.md, package.json, tsconfig.json}

═══════════════════════════════════════════════════════════════
🛑 USER ACTION REQUIRED to activate H2 (Worker deploy + secrets):

1. Create private Telegram group for feedback
2. Add bot @<your_bot> as admin (so it can post)
3. Get group chat_id (use bot getUpdates)
4. Add to data/secrets.yaml:
     telegram.feedback_group_chat_id: "<id>"
   And github section:
     github.token: "<PAT>"
     github.owner: "dangtrungdev113999"
     github.repo: "finpath-newsroom"

5. Verify GitHub PAT scope:
     curl -H "Authorization: Bearer <TOKEN>" \
       "https://api.github.com/repos/dangtrungdev113999/finpath-newsroom/actions/runs?per_page=1"
   Expect 200 + JSON workflow_runs

6. Deploy Cloudflare Worker (full guide in worker/README.md):
     cd worker
     wrangler login
     wrangler kv:namespace create FEEDBACK_RL
     # Copy id → wrangler.toml
     wrangler secret put TELEGRAM_BOT_TOKEN
     wrangler secret put TELEGRAM_FEEDBACK_GROUP_ID
     wrangler deploy
     # Note Worker URL output

7. Add GitHub Actions secret:
   Settings → Secrets and variables → Actions → New
     Name:  VITE_FEEDBACK_WORKER_URL
     Value: https://feedback-finpath.<account>.workers.dev

8. Trigger Pages rebuild:
     git commit --allow-empty -m "trigger pages rebuild for feedback worker URL"
     git push

9. Test E2E:
   - Open production /feed
   - Click "💬 Góp ý cho bài này" on any article
   - Submit a test comment
   - Verify message arrives in Telegram feedback group

10. Tag H2 close-out (after E2E green):
      git tag -a v4.0-phase-h2-comment-feedback -m "Phase H2 — comment feedback live"
      git push --tags

═══════════════════════════════════════════════════════════════
Optional H1 verification (live `/tin VCB` test) — run when ready:
  /tin VCB
  → check pipeline_log for step_7_git_publish + step_8_pages_wait
  → click Telegram link → verify no 404
═══════════════════════════════════════════════════════════════
```

---

## Out-of-scope follow-ups (tracked for later)

- Comment moderation/admin UI
- Two-way reply from admin → user (e.g., bot replies in feedback group, user sees in web)
- Cross-device sync of comment history (would need server-side store)
- Custom Cloudflare Worker domain (vs default `workers.dev`)
- Migration to Telegram forum topics if comment volume warrants
