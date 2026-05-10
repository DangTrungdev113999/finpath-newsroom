"""Subprocess helper for concurrent SQLite write test.

Invoked by test_pipeline_db.py via subprocess.Popen × 3.
Each invocation inserts one crawl_log row with unique row_id.
"""
import sys
import uuid
from pathlib import Path

# Allow import lib.pipeline_db when running as subprocess
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.pipeline_db import PipelineDB


def main(db_path: str, batch_id: str, source_url: str) -> int:
    db = PipelineDB(db_path)
    row_id = str(uuid.uuid4())
    db.insert_crawl_row({
        "row_id": row_id,
        "funnel_batch_id": batch_id,
        "ticker": "TEST",
        "source_name": "concurrent_test",
        "source_url": source_url,
        "title": f"Concurrent write {row_id[:8]}",
        "raw_content": "test content",
        "crawled_at": "2026-05-10T00:00:00Z",
    })
    db.close()
    print(row_id)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
