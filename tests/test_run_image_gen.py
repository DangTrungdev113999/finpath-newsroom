"""Tests for lib/stages/run_image_gen.py — Step 4.5 orchestration."""

from __future__ import annotations

import io
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PIL import Image

from lib import pipeline_db
from lib.stages import run_image_gen

SCHEMA_SQL = Path(__file__).resolve().parents[1] / "data" / "pipeline.schema.sql"


@pytest.fixture
def db(tmp_path: Path):
    target = tmp_path / "pipeline.db"
    conn = pipeline_db.PipelineDB(str(target))
    conn.init_schema(SCHEMA_SQL)
    yield conn
    conn.close()


@pytest.fixture
def secrets_with_key(tmp_path: Path) -> Path:
    p = tmp_path / "secrets.yaml"
    p.write_text("gemini:\n  api_key: 'real-google-key'\n", encoding="utf-8")
    return p


@pytest.fixture
def secrets_missing_key(tmp_path: Path) -> Path:
    p = tmp_path / "secrets.yaml"
    p.write_text("gemini:\n  api_key: 'REPLACE_WITH_KEY'\n", encoding="utf-8")
    return p


@pytest.fixture
def prompt_template(tmp_path: Path) -> Path:
    p = tmp_path / "image_prompt.md"
    p.write_text(
        "Motif: {{sector_motif}}\nConcept: {{thumb_concept}}\n",
        encoding="utf-8",
    )
    return p


@pytest.fixture
def motif_yaml(tmp_path: Path) -> Path:
    p = tmp_path / "motifs.yaml"
    p.write_text(
        "bank: 'Bank skyline drama'\nbds: 'Crane silhouette'\ndefault: 'Generic cityscape'\n",
        encoding="utf-8",
    )
    return p


def _make_png_bytes(width: int = 1024, height: int = 576) -> bytes:
    img = Image.new("RGB", (width, height), color=(20, 50, 90))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _seed_article(db, *, article_id: str = "art-001", sector: str = "BĐS") -> None:
    db.conn.execute(
        "INSERT INTO crawl_log (row_id, funnel_batch_id, ticker, source_name, "
        "source_url, title, raw_content, crawled_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        ("row-001", "batch-001", "VHM", "cafef", "https://cafef.vn/vhm-q1",
         "VHM news title", "VHM raw content", "2026-05-14"),
    )
    db.conn.execute(
        "INSERT INTO generated_news (article_id, row_id, ticker, sector, title, "
        "body, public_slug, accepted_hypothesis) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (article_id, "row-001", "VHM", sector, "VHM chọn lọc 2026: ai sống ai ngáp?",
         "Chủ tịch VHM hôm 21/4 vạch ranh giới 'phục hồi có chọn lọc'. NĐT đang cầm VHM "
         "đứng trước quyết định cắt-giữ. Bốn mã BĐS niêm yết chia 2 nhóm rõ rệt.",
         "VHM-20260514-1010-vhm-chon-loc-2026", 1),
    )
    db.conn.commit()


def _mock_factory(image_bytes: bytes, raise_exc: Exception | None = None):
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
            response.generated_images = [generated]
            return response

        client.models.generate_images.side_effect = gen_images
        return client

    return factory, captured


def test_skipped_disabled_when_flag_off(db, secrets_with_key, prompt_template, motif_yaml, tmp_path) -> None:
    _seed_article(db)
    factory, _ = _mock_factory(_make_png_bytes())
    result = run_image_gen.run_image_gen(
        article_id="art-001",
        db=db,
        enable=False,
        secrets_path=secrets_with_key,
        prompt_path=prompt_template,
        motif_path=motif_yaml,
        output_dir=tmp_path / "thumbs",
        client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "image_flag_not_set"

    row = db.conn.execute(
        "SELECT thumb_status, thumb_error FROM generated_news WHERE article_id = ?",
        ("art-001",),
    ).fetchone()
    assert row["thumb_status"] == "skipped_disabled"
    assert row["thumb_error"] == "image_flag_not_set"


def test_success_writes_webp_and_db(db, secrets_with_key, prompt_template, motif_yaml, tmp_path) -> None:
    _seed_article(db, sector="BĐS")
    factory, captured = _mock_factory(_make_png_bytes())
    output_dir = tmp_path / "thumbs"
    result = run_image_gen.run_image_gen(
        article_id="art-001",
        db=db,
        enable=True,
        secrets_path=secrets_with_key,
        prompt_path=prompt_template,
        motif_path=motif_yaml,
        output_dir=output_dir,
        base_url="https://example.com",
        client_factory=factory,
    )
    assert result["ok"] is True
    assert result["thumb_url"] == "https://example.com/thumbs/VHM-20260514-1010-vhm-chon-loc-2026.webp"
    assert result["cost_usd"] == 0.04
    # File written
    webp_path = output_dir / "VHM-20260514-1010-vhm-chon-loc-2026.webp"
    assert webp_path.exists()
    assert webp_path.stat().st_size > 1000  # reasonable WebP size

    # DB row updated
    row = db.conn.execute(
        "SELECT thumb_status, thumb_url, image_cost_usd FROM generated_news WHERE article_id = ?",
        ("art-001",),
    ).fetchone()
    assert row["thumb_status"] == "success"
    assert row["image_cost_usd"] == 0.04
    # Prompt picked the BĐS motif
    sent_prompt = captured["calls"][0]["prompt"]
    assert "Crane silhouette" in sent_prompt
    assert "VHM chọn lọc 2026" in sent_prompt


def test_missing_api_key_status_skipped_disabled(db, secrets_missing_key, prompt_template, motif_yaml, tmp_path) -> None:
    _seed_article(db)
    factory, _ = _mock_factory(_make_png_bytes())
    result = run_image_gen.run_image_gen(
        article_id="art-001",
        db=db,
        enable=True,
        secrets_path=secrets_missing_key,
        prompt_path=prompt_template,
        motif_path=motif_yaml,
        output_dir=tmp_path / "thumbs",
        client_factory=factory,
    )
    assert result["ok"] is False
    row = db.conn.execute(
        "SELECT thumb_status, thumb_error FROM generated_news WHERE article_id = ?",
        ("art-001",),
    ).fetchone()
    assert row["thumb_status"] == "skipped_disabled"
    assert row["thumb_error"] == "missing_api_key"


def test_imagen_failure_status_skipped_failure(db, secrets_with_key, prompt_template, motif_yaml, tmp_path) -> None:
    _seed_article(db)
    factory, _ = _mock_factory(_make_png_bytes(), raise_exc=RuntimeError("imagen quota exceeded"))
    result = run_image_gen.run_image_gen(
        article_id="art-001",
        db=db,
        enable=True,
        secrets_path=secrets_with_key,
        prompt_path=prompt_template,
        motif_path=motif_yaml,
        output_dir=tmp_path / "thumbs",
        client_factory=factory,
    )
    assert result["ok"] is False
    row = db.conn.execute(
        "SELECT thumb_status, thumb_error FROM generated_news WHERE article_id = ?",
        ("art-001",),
    ).fetchone()
    assert row["thumb_status"] == "skipped_failure"
    assert "quota exceeded" in row["thumb_error"]


def test_article_not_found_no_db_write(db, secrets_with_key, prompt_template, motif_yaml, tmp_path) -> None:
    factory, _ = _mock_factory(_make_png_bytes())
    result = run_image_gen.run_image_gen(
        article_id="does-not-exist",
        db=db,
        enable=True,
        secrets_path=secrets_with_key,
        prompt_path=prompt_template,
        motif_path=motif_yaml,
        output_dir=tmp_path / "thumbs",
        client_factory=factory,
    )
    assert result["ok"] is False
    assert result["error"] == "article_not_found"
