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
