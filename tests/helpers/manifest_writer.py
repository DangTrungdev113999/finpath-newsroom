"""Subprocess helper for concurrent manifest write test (Phase G T6)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.render_compare_feed import update_manifest


def main(manifest_path: str, article_id: str, crawled_at: str) -> int:
    summary = {
        "id": article_id,
        "ticker": "TEST",
        "sector": "Bank",
        "title": f"Test article {article_id}",
        "crawled_at": crawled_at,
        "key_view": "trung lập",
        "word_count": 300,
    }
    update_manifest(Path(manifest_path), summary)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
