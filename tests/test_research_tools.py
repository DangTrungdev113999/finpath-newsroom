"""Tests for lib/llm/research_tools.py."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from lib.llm import research_tools


# === Fixtures ===============================================================


@pytest.fixture
def mock_db():
    db = MagicMock()
    db.recent_generated_news.return_value = [
        {
            "title": "VCB lãi Q1 vượt 5000 tỷ",
            "variety_guard_angle": "paradox-credit-growth",
            "insight_final": "TPB ăn theo Big4",
            "published_at": "2026-05-12T10:00:00Z",
        }
    ]
    return db


@pytest.fixture
def secrets_no_tavily(tmp_path: Path) -> Path:
    p = tmp_path / "secrets.yaml"
    p.write_text("telegram:\n  bot_token: 'x'\n", encoding="utf-8")
    return p


@pytest.fixture
def secrets_with_tavily(tmp_path: Path) -> Path:
    p = tmp_path / "secrets.yaml"
    p.write_text("tavily:\n  api_key: 'tvly-real-key'\n", encoding="utf-8")
    return p


# === finpath_* tools ========================================================


def test_finpath_overview_success(mock_db):
    """When FinpathAPI returns dict, tool wraps with source + ok=True."""
    tools = research_tools.build_research_tools(db=mock_db, secrets_path=Path("/nonexistent"))
    with patch("lib.llm.research_tools.FinpathAPI") as FakeApi:
        FakeApi.return_value.get_overview.return_value = {"stocks": [{"c": "VCB"}]}
        tools2 = research_tools.build_research_tools(db=mock_db, secrets_path=Path("/nonexistent"))
        result = tools2.dispatch["finpath_overview"]()
    assert result["ok"] is True
    assert result["source"] == "Finpath_API/overview"
    assert result["data"]["stocks"][0]["c"] == "VCB"


def test_finpath_income_statement_error_handled(mock_db):
    """Network error in API surfaces as ok=False without raising."""
    with patch("lib.llm.research_tools.FinpathAPI") as FakeApi:
        FakeApi.return_value.get_income_statement.side_effect = RuntimeError("upstream 503")
        tools = research_tools.build_research_tools(db=mock_db, secrets_path=Path("/nonexistent"))
        result = tools.dispatch["finpath_income_statement"](ticker="VCB")
    assert result["ok"] is False
    assert "upstream 503" in result["error"]
    assert "VCB" in result["source"]


def test_finpath_bank_ratios_passes_ticker(mock_db):
    with patch("lib.llm.research_tools.FinpathAPI") as FakeApi:
        FakeApi.return_value.get_bank_ratios.return_value = {"NIM": [2.67]}
        tools = research_tools.build_research_tools(db=mock_db, secrets_path=Path("/nonexistent"))
        result = tools.dispatch["finpath_bank_ratios"](ticker="SHB")
    FakeApi.return_value.get_bank_ratios.assert_called_once_with("SHB")
    assert result["ok"] is True
    assert result["data"]["NIM"] == [2.67]


# === kb_search ==============================================================


def test_kb_search_returns_top_3_with_snippet(mock_db, tmp_path: Path):
    kb_root = tmp_path / "kb"
    kb_root.mkdir()
    (kb_root / "bank-test.md").write_text(
        "---\ntitle: Bank test topic\ncategory: bank\n---\nNIM giảm Q1 2026 do COF tăng.\n",
        encoding="utf-8",
    )
    tools = research_tools.build_research_tools(
        db=mock_db, kb_root=kb_root, secrets_path=Path("/nonexistent")
    )
    result = tools.dispatch["kb_search"](query="NIM Q1")
    assert result["ok"] is True
    assert len(result["data"]) >= 1
    assert result["data"][0]["title"] == "Bank test topic"
    assert "NIM" in result["data"][0]["snippet"]


def test_kb_search_empty_query_returns_empty(mock_db, tmp_path: Path):
    tools = research_tools.build_research_tools(
        db=mock_db, kb_root=tmp_path / "empty", secrets_path=Path("/nonexistent")
    )
    result = tools.dispatch["kb_search"](query="")
    assert result["ok"] is True
    assert result["data"] == []


# === read_recent_articles ===================================================


def test_read_recent_articles_passes_through_db(mock_db):
    tools = research_tools.build_research_tools(db=mock_db, secrets_path=Path("/nonexistent"))
    result = tools.dispatch["read_recent_articles"](ticker="VCB", limit=3)
    assert result["ok"] is True
    assert result["data"][0]["title"] == "VCB lãi Q1 vượt 5000 tỷ"
    mock_db.recent_generated_news.assert_called_once_with("VCB", limit=3)


def test_read_recent_articles_clamps_limit(mock_db):
    tools = research_tools.build_research_tools(db=mock_db, secrets_path=Path("/nonexistent"))
    tools.dispatch["read_recent_articles"](ticker="VCB", limit=99)
    mock_db.recent_generated_news.assert_called_with("VCB", limit=5)


# === web_search =============================================================


def test_web_search_disabled_when_no_key(mock_db, secrets_no_tavily: Path):
    """Without Tavily key, web_search gracefully degrades."""
    tools = research_tools.build_research_tools(db=mock_db, secrets_path=secrets_no_tavily)
    result = tools.dispatch["web_search"](query="VCB Q1 2026")
    assert result["ok"] is False
    assert result["error"] == "tavily_disabled"


def test_web_search_calls_tavily_when_key_present(mock_db, secrets_with_tavily: Path):
    fake_resp = MagicMock()
    fake_resp.read.return_value = json.dumps(
        {"results": [{"title": "VCB lãi Q1", "url": "https://cafef.vn/x", "content": "VCB ăn lãi 12k tỷ"}]}
    ).encode("utf-8")
    fake_resp.__enter__ = lambda self: self
    fake_resp.__exit__ = lambda *args: None

    with patch("lib.llm.research_tools.urllib.request.urlopen", return_value=fake_resp) as mock_open:
        tools = research_tools.build_research_tools(db=mock_db, secrets_path=secrets_with_tavily)
        result = tools.dispatch["web_search"](query="VCB Q1 2026", max_results=3)
    assert result["ok"] is True
    assert result["data"][0]["title"] == "VCB lãi Q1"
    assert result["data"][0]["url"] == "https://cafef.vn/x"
    assert "WebSearch:" in result["source"]
    # urlopen called once with our payload
    mock_open.assert_called_once()


# === ResearchTools shape ====================================================


def test_research_tools_exposes_callables_and_schema_in_sync(mock_db):
    tools = research_tools.build_research_tools(db=mock_db, secrets_path=Path("/nonexistent"))
    # 8 tools total
    assert len(tools.callables) == 8
    assert len(tools.openai_schema) == 8
    assert len(tools.dispatch) == 8
    # Names in schema match callables
    schema_names = {entry["function"]["name"] for entry in tools.openai_schema}
    callable_names = {fn.__name__ for fn in tools.callables}
    assert schema_names == callable_names
    # dispatch keys match
    assert set(tools.dispatch.keys()) == callable_names
