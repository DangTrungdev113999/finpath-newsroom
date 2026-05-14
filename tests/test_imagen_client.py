"""Tests for lib/llm/imagen_client.py — Imagen 4 thumb generation."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from lib.llm import imagen_client


def _mock_factory(image_bytes: bytes | None = b"\x89PNG\r\n\x1a\nFAKE", raise_exc: Exception | None = None):
    captured: dict = {}

    def factory(api_key: str):
        captured["api_key"] = api_key
        client = MagicMock()

        def gen_images(*, model, prompt, config):
            captured.setdefault("calls", []).append(
                {"model": model, "prompt": prompt, "config": config}
            )
            if raise_exc is not None:
                raise raise_exc
            generated = MagicMock()
            generated.image.image_bytes = image_bytes
            response = MagicMock()
            response.generated_images = [generated] if image_bytes is not None else []
            return response

        client.models.generate_images.side_effect = gen_images
        return client

    return factory, captured


def test_load_api_key_reads_gemini_section(tmp_path: Path) -> None:
    p = tmp_path / "secrets.yaml"
    p.write_text("gemini:\n  api_key: 'real-google-key'\n", encoding="utf-8")
    assert imagen_client.load_api_key(p) == "real-google-key"


def test_load_api_key_returns_none_when_placeholder(tmp_path: Path) -> None:
    p = tmp_path / "secrets.yaml"
    p.write_text("gemini:\n  api_key: 'REPLACE_WITH_KEY'\n", encoding="utf-8")
    assert imagen_client.load_api_key(p) is None


def test_load_api_key_returns_none_when_missing_file(tmp_path: Path) -> None:
    assert imagen_client.load_api_key(tmp_path / "nope.yaml") is None


def test_generate_thumb_success() -> None:
    factory, captured = _mock_factory(image_bytes=b"\x89PNGFAKEbytes")
    result = imagen_client.generate_thumb(
        "VHM drama scene paradox", api_key="key", _client_factory=factory
    )
    assert result["ok"] is True
    assert result["image_bytes"] == b"\x89PNGFAKEbytes"
    assert result["cost_usd"] == 0.04  # Imagen 4 flat
    assert result["error"] is None
    assert captured["api_key"] == "key"
    assert captured["calls"][0]["model"] == "imagen-4.0-generate-001"


def test_generate_thumb_missing_api_key() -> None:
    factory, _ = _mock_factory()
    result = imagen_client.generate_thumb("x", api_key=None, _client_factory=factory)
    assert result["ok"] is False
    assert result["error"] == "missing_api_key"
    assert result["image_bytes"] is None


def test_generate_thumb_sdk_exception_returns_error() -> None:
    factory, _ = _mock_factory(raise_exc=RuntimeError("imagen quota exceeded"))
    result = imagen_client.generate_thumb("x", api_key="k", _client_factory=factory)
    assert result["ok"] is False
    assert "quota exceeded" in result["error"]
    assert result["image_bytes"] is None


def test_generate_thumb_empty_response_returns_error() -> None:
    factory, _ = _mock_factory(image_bytes=None)
    result = imagen_client.generate_thumb("x", api_key="k", _client_factory=factory)
    assert result["ok"] is False
    assert "missing generated_images" in result["error"]


def test_generate_thumb_custom_model_id() -> None:
    factory, captured = _mock_factory()
    imagen_client.generate_thumb(
        "x", api_key="k", model="imagen-3.0-generate-002", _client_factory=factory
    )
    assert captured["calls"][0]["model"] == "imagen-3.0-generate-002"
