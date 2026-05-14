"""Tests for lib/llm/grok_master.py — Grok Master with manual tool-call loop."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from lib.llm import grok_master, research_tools


def _build_tools(db=None):
    return research_tools.build_research_tools(
        db=db or MagicMock(),
        secrets_path=Path("/nonexistent"),
    )


def _make_resp(content: str | None, tool_calls: list | None = None,
               prompt_tokens: int = 0, completion_tokens: int = 0):
    """Build a fake openai response object."""
    resp = MagicMock()
    msg = MagicMock()
    msg.content = content
    msg.tool_calls = tool_calls
    choice = MagicMock()
    choice.message = msg
    resp.choices = [choice]
    if prompt_tokens or completion_tokens:
        resp.usage.prompt_tokens = prompt_tokens
        resp.usage.completion_tokens = completion_tokens
    else:
        resp.usage = None
    return resp


def _mock_factory(response_sequence: list, raise_at_turn: int | None = None):
    """Each item in response_sequence is the resp returned by one turn.

    raise_at_turn: if set, raises RuntimeError at that turn index instead of returning.
    """
    captured: dict = {"calls": []}

    def factory(api_key: str, base_url: str):
        captured["api_key"] = api_key
        captured["base_url"] = base_url
        client = MagicMock()

        def create(*, model, messages, tools, response_format, timeout):
            captured["calls"].append({"model": model, "messages": list(messages), "turn": len(captured["calls"])})
            turn = len(captured["calls"]) - 1
            if raise_at_turn is not None and turn == raise_at_turn:
                raise RuntimeError("simulated grok 503")
            return response_sequence[turn]

        client.chat.completions.create.side_effect = create
        return client

    return factory, captured


def test_single_turn_no_tools_returns_payload():
    """Model returns final answer directly without calling tools."""
    final = {
        "title": "VHM chọn lọc 2026",
        "body": "Body content here",
        "word_count": 248,
        "chosen_question_idx": 0,
        "data_trail": [{"source": "Raw news", "fetched": "..."}],
    }
    factory, captured = _mock_factory([_make_resp(json.dumps(final), prompt_tokens=8000, completion_tokens=1200)])
    result = grok_master.generate_article(
        prompt="x", tools=_build_tools(), api_key="k", _client_factory=factory,
    )
    assert result["ok"] is True
    assert result["payload"]["title"] == "VHM chọn lọc 2026"
    assert result["usage"]["prompt_tokens"] == 8000
    assert len(captured["calls"]) == 1


def test_multi_turn_with_tool_calls_aggregates_usage():
    """Turn 0: model requests finpath_overview. Turn 1: model returns final JSON."""
    tool_call = MagicMock()
    tool_call.id = "call_1"
    tool_call.function.name = "finpath_overview"
    tool_call.function.arguments = "{}"

    final = {
        "title": "VCB lãi Q1 vượt 5000 tỷ",
        "body": "Body",
        "word_count": 200,
        "chosen_question_idx": 0,
        "data_trail": [{"source": "Finpath_API/overview", "fetched": "..."}],
    }
    factory, captured = _mock_factory([
        _make_resp(None, tool_calls=[tool_call], prompt_tokens=5000, completion_tokens=100),
        _make_resp(json.dumps(final), prompt_tokens=6500, completion_tokens=800),
    ])
    result = grok_master.generate_article(
        prompt="x", tools=_build_tools(), api_key="k", _client_factory=factory,
    )
    assert result["ok"] is True
    # Tokens aggregated across 2 turns: 5000+6500 in, 100+800 out
    assert result["usage"]["prompt_tokens"] == 11_500
    assert result["usage"]["completion_tokens"] == 900
    assert len(captured["calls"]) == 2
    # Turn 1 messages should include 'tool' role with the dispatch result
    turn1_msgs = captured["calls"][1]["messages"]
    assert any(m.get("role") == "tool" for m in turn1_msgs)


def test_max_turns_exhausted_returns_error():
    """Model keeps calling tools forever — caller sees max_turns_reached error."""
    tool_call = MagicMock()
    tool_call.id = "call_1"
    tool_call.function.name = "finpath_overview"
    tool_call.function.arguments = "{}"
    looping = _make_resp(None, tool_calls=[tool_call], prompt_tokens=1000, completion_tokens=50)
    # Always returns tool_call → loop hits max_turns
    factory, _ = _mock_factory([looping] * 10)
    result = grok_master.generate_article(
        prompt="x", tools=_build_tools(), api_key="k", _client_factory=factory, max_turns=3,
    )
    assert result["ok"] is False
    assert "max_turns_reached" in result["error"]


def test_sdk_exception_in_turn_0_returns_error():
    factory, _ = _mock_factory([], raise_at_turn=0)
    result = grok_master.generate_article(
        prompt="x", tools=_build_tools(), api_key="k", _client_factory=factory,
    )
    assert result["ok"] is False
    assert "simulated grok 503" in result["error"]


def test_missing_api_key_returns_error():
    factory, _ = _mock_factory([])
    result = grok_master.generate_article(
        prompt="x", tools=_build_tools(), api_key=None, _client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "missing_api_key"
