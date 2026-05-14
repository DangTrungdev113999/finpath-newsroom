"""Step 4.5 Image Generation (V5.1.8 — 2026-05-14, opt-in via --image flag).

Runs AFTER Master + Gemini + Grok have written their bodies. Reads
generated_news.title + body + sector → builds drama-tone prompt from
prompts/image_prompt_template.md + data/sector_thumb_motif.yaml → calls
Imagen 4 → converts PNG bytes to WebP (1024×576) → saves to
output/thumbs/<public_slug>.webp → persists thumb_url + cost_usd.

Pipeline-safety: NEVER raises. Result statuses:
  - success          : webp written + DB row updated
  - skipped_failure  : Imagen API failed (error string captured)
  - skipped_disabled : --image flag not set OR no Imagen API key

CLI:
    uv run python -m lib.stages.run_image_gen --article-id <uuid> --image
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import yaml  # noqa: E402

from lib.llm import imagen_client  # noqa: E402
from lib.pipeline_db import PipelineDB  # noqa: E402

DEFAULT_SECRETS_PATH = REPO_ROOT / "data" / "secrets.yaml"
DEFAULT_DB_PATH = REPO_ROOT / "data" / "pipeline.db"
DEFAULT_PROMPT_PATH = REPO_ROOT / "prompts" / "image_prompt_template.md"
DEFAULT_MOTIF_PATH = REPO_ROOT / "data" / "sector_thumb_motif.yaml"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output" / "thumbs"
DEFAULT_BASE_URL = "https://dangtrungdev113999.github.io/finpath-newsroom"
THUMB_WIDTH, THUMB_HEIGHT = 1024, 576


def _load_motifs(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def _load_article(db: PipelineDB, article_id: str) -> dict[str, Any] | None:
    cur = db.conn.execute(
        """
        SELECT article_id, title, body, sector, public_slug, ticker
        FROM generated_news
        WHERE article_id = ?
        """,
        (article_id,),
    )
    row = cur.fetchone()
    return dict(row) if row else None


def _resolve_sector_key(sector: str) -> str:
    """Map article.sector (VN labels) → motif YAML key."""
    if not isinstance(sector, str):
        return "default"
    s = sector.strip().lower()
    mapping = {
        "bank": "bank",
        "ngân hàng": "bank",
        "ck": "ck",
        "chứng khoán": "ck",
        "bđs": "bds",
        "bds": "bds",
        "bất động sản": "bds",
        "oilgas": "oilgas",
        "dầu khí": "oilgas",
        "logistics": "logistics",
        "fb": "fb",
        "tiêu dùng thực phẩm": "fb",
        "apparel": "apparel",
        "dệt may": "apparel",
        "retail": "retail",
        "bán lẻ": "retail",
        "seafood": "seafood",
        "thuỷ sản": "seafood",
        "thủy sản": "seafood",
        "defensive": "defensive",
        "phòng thủ": "defensive",
    }
    return mapping.get(s, "default")


def _extract_thumb_concept(title: str, body: str) -> str:
    """Derive a 1-line visual concept from title + body opening sentence.

    Used as substitution for {{thumb_concept}} in image_prompt_template.md.
    Falls back to the title alone when body parsing fails.
    """
    title = (title or "").strip().strip(".?!")
    if not title:
        return "Vietnamese stock market drama scene"
    # Pull first body sentence (≤140 chars) as scene anchor.
    body = (body or "").strip()
    opening = ""
    if body:
        for sep in (". ", "! ", "? "):
            idx = body.find(sep)
            if 0 < idx <= 200:
                opening = body[: idx + 1].strip()
                break
        if not opening:
            opening = body[:200].strip()
    if opening and len(opening) > 240:
        opening = opening[:240]
    if opening:
        return f"{title}. Context: {opening}"
    return title


def _build_prompt(
    template_path: Path,
    motif: str,
    thumb_concept: str,
    ticker: str,
) -> str:
    """Substitute {{sector_motif}} / {{thumb_concept}} / {{ticker}} placeholders.

    `ticker` is rendered into the image as the single textual element per
    V5.1.8.1 prompt template — Imagen 4 typically holds 3-4 letter all-caps
    legibly even though general text rendering is hit-or-miss.
    """
    template = template_path.read_text(encoding="utf-8")
    return (
        template
        .replace("{{sector_motif}}", motif)
        .replace("{{thumb_concept}}", thumb_concept)
        .replace("{{ticker}}", (ticker or "").strip().upper())
    )


def _png_to_webp(png_bytes: bytes, *, width: int, height: int, quality: int = 80) -> bytes:
    """Convert Imagen PNG output to WebP at target dimensions.

    Pillow is a dev dependency (already used elsewhere indirectly via genai).
    Resizes to exact 16:9 crop in case Imagen returned slight aspect drift.
    """
    from PIL import Image  # type: ignore[import-not-found]

    img = Image.open(io.BytesIO(png_bytes))
    if img.mode != "RGB":
        img = img.convert("RGB")
    # Center-crop to target aspect, then resize to (width, height)
    target_ratio = width / height
    cur_w, cur_h = img.size
    cur_ratio = cur_w / cur_h if cur_h > 0 else target_ratio
    if cur_ratio > target_ratio:
        new_w = int(cur_h * target_ratio)
        x0 = (cur_w - new_w) // 2
        img = img.crop((x0, 0, x0 + new_w, cur_h))
    elif cur_ratio < target_ratio:
        new_h = int(cur_w / target_ratio)
        y0 = (cur_h - new_h) // 2
        img = img.crop((0, y0, cur_w, y0 + new_h))
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="WEBP", quality=quality, method=6)
    return buf.getvalue()


def run_image_gen(
    article_id: str,
    *,
    db: PipelineDB,
    enable: bool = False,
    secrets_path: Path = DEFAULT_SECRETS_PATH,
    prompt_path: Path = DEFAULT_PROMPT_PATH,
    motif_path: Path = DEFAULT_MOTIF_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    base_url: str = DEFAULT_BASE_URL,
    model: str | None = None,
    client_factory: Callable[[str], Any] | None = None,
) -> dict[str, Any]:
    """Generate Imagen thumb for article. NEVER raises — returns result dict.

    `enable` MUST be True (i.e., user passed --image). When False, returns
    early with status=skipped_disabled + no API call. Caller (pipeline
    orchestrator Step 4.5) sets this from the --image flag.
    """
    if model is None:
        model = imagen_client.DEFAULT_MODEL

    article = _load_article(db, article_id)
    if article is None:
        return {
            "ok": False,
            "thumb_url": None,
            "model": model,
            "cost_usd": None,
            "duration_ms": 0,
            "error": "article_not_found",
        }

    if not enable:
        db.update_thumb_output(
            article_id=article_id,
            status="skipped_disabled",
            model=model,
            error="image_flag_not_set",
        )
        return {
            "ok": False,
            "thumb_url": None,
            "model": model,
            "cost_usd": None,
            "duration_ms": 0,
            "error": "image_flag_not_set",
        }

    motifs = _load_motifs(motif_path)
    sector_key = _resolve_sector_key(article.get("sector") or "")
    motif = motifs.get(sector_key) or motifs.get("default") or ""
    thumb_concept = _extract_thumb_concept(article.get("title") or "", article.get("body") or "")
    ticker = article.get("ticker") or ""
    prompt = _build_prompt(prompt_path, motif, thumb_concept, ticker)

    api_key = imagen_client.load_api_key(secrets_path)
    result = imagen_client.generate_thumb(
        prompt=prompt,
        api_key=api_key,
        model=model,
        _client_factory=client_factory,
    )

    if not result["ok"]:
        status = "skipped_disabled" if result["error"] == "missing_api_key" else "skipped_failure"
        db.update_thumb_output(
            article_id=article_id,
            status=status,
            model=result["model"],
            thumb_prompt=prompt,
            error=result["error"],
        )
        return {**result, "thumb_url": None}

    # Persist webp file
    output_dir.mkdir(parents=True, exist_ok=True)
    public_slug = article.get("public_slug") or article_id
    webp_path = output_dir / f"{public_slug}.webp"
    try:
        webp_bytes = _png_to_webp(result["image_bytes"], width=THUMB_WIDTH, height=THUMB_HEIGHT)
        webp_path.write_bytes(webp_bytes)
    except Exception as exc:  # noqa: BLE001 — Pillow / IO errors handled the same
        db.update_thumb_output(
            article_id=article_id,
            status="skipped_failure",
            model=result["model"],
            thumb_prompt=prompt,
            error=f"webp_convert_failed: {exc}",
        )
        return {**result, "ok": False, "thumb_url": None, "error": f"webp_convert_failed: {exc}"}

    thumb_url = f"{base_url.rstrip('/')}/thumbs/{public_slug}.webp"
    db.update_thumb_output(
        article_id=article_id,
        status="success",
        thumb_url=thumb_url,
        thumb_prompt=prompt,
        model=result["model"],
        generated_at=datetime.now(timezone.utc).isoformat(),
        cost_usd=result["cost_usd"],
    )
    return {**result, "thumb_url": thumb_url}


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Step 4.5 Image Gen (Imagen 4 thumb)")
    parser.add_argument("--article-id", required=True)
    parser.add_argument("--image", action="store_true", help="Opt-in: actually call Imagen (cost $0.04/img)")
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--secrets-path", default=str(DEFAULT_SECRETS_PATH))
    parser.add_argument("--prompt-path", default=str(DEFAULT_PROMPT_PATH))
    parser.add_argument("--motif-path", default=str(DEFAULT_MOTIF_PATH))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--model", default=None)
    args = parser.parse_args(argv)

    db = PipelineDB(args.db_path)
    try:
        result = run_image_gen(
            article_id=args.article_id,
            db=db,
            enable=args.image,
            secrets_path=Path(args.secrets_path),
            prompt_path=Path(args.prompt_path),
            motif_path=Path(args.motif_path),
            output_dir=Path(args.output_dir),
            base_url=args.base_url,
            model=args.model,
        )
    finally:
        db.close()

    summary = {
        "ok": result["ok"],
        "article_id": args.article_id,
        "model": result["model"],
        "thumb_url": result.get("thumb_url"),
        "cost_usd": result.get("cost_usd"),
        "duration_ms": result.get("duration_ms"),
        "error": result.get("error"),
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0  # NEVER halt pipeline


if __name__ == "__main__":
    sys.exit(_main())
