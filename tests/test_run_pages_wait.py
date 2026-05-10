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
