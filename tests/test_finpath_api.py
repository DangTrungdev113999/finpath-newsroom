"""Tests for lib.finpath_api — Bank endpoints wrapper."""
import pytest
import responses

from lib.finpath_api import FinpathAPI


@pytest.fixture
def api():
    return FinpathAPI(base_url="https://api.finpath.vn")


@responses.activate
def test_get_bank_ratios_returns_data(api):
    """get_bank_ratios returns the .data dict from response."""
    responses.add(
        responses.GET,
        "https://api.finpath.vn/api/stocks/bankfinancialratios/VCB",
        json={"data": {"yearlyProfits": [{"code": "VCB", "nim": 2.6}], "quarterlyProfits": []}},
        status=200,
    )
    result = api.get_bank_ratios("VCB")
    assert "yearlyProfits" in result
    assert result["yearlyProfits"][0]["code"] == "VCB"


@responses.activate
def test_get_bank_ratios_batch_csv(api):
    """get_bank_ratios_batch joins tickers with comma."""
    responses.add(
        responses.GET,
        "https://api.finpath.vn/api/stocks/bankfinancialratios-eboard",
        json={"data": [{"code": "TCB"}, {"code": "VCB"}]},
        status=200,
    )
    result = api.get_bank_ratios_batch(["TCB", "VCB"])
    assert len(result) == 2
    url = responses.calls[0].request.url
    # Allow url-encoded or raw comma
    assert "TCB%2CVCB" in url or "TCB,VCB" in url


@responses.activate
def test_caches_repeat_calls(api):
    """Same ticker query twice → 1 HTTP call (in-memory cache)."""
    responses.add(
        responses.GET,
        "https://api.finpath.vn/api/stocks/bankfinancialratios/VCB",
        json={"data": {"yearlyProfits": [], "quarterlyProfits": []}},
        status=200,
    )
    api.get_bank_ratios("VCB")
    api.get_bank_ratios("VCB")
    assert len(responses.calls) == 1


@responses.activate
def test_404_raises(api):
    responses.add(
        responses.GET,
        "https://api.finpath.vn/api/stocks/bankfinancialratios/XXX",
        json={"error": "not found"},
        status=404,
    )
    with pytest.raises(Exception):
        api.get_bank_ratios("XXX")


@responses.activate
def test_get_shareholders(api):
    responses.add(
        responses.GET,
        "https://api.finpath.vn/api/stocks/shareholderstructure/VCB",
        json={"data": {"yearlyProfits": [{"foreign_pct": 22}]}},
        status=200,
    )
    result = api.get_shareholders("VCB")
    assert "yearlyProfits" in result


@responses.activate
def test_get_events(api):
    responses.add(
        responses.GET,
        "https://api.finpath.vn/api/events/VCB",
        json={"data": [{"event": "dividend"}]},
        status=200,
    )
    result = api.get_events("VCB")
    assert isinstance(result, list)
    assert result[0]["event"] == "dividend"
