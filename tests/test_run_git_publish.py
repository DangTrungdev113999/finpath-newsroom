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
