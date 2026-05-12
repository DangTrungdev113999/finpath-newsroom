"""CLI to manually refresh Finpath sectors cache.

Usage:
    uv run python lib/refresh_sector_cache.py             # refresh if stale
    uv run python lib/refresh_sector_cache.py --force      # clear + refresh
"""
import argparse
import sys
from lib.pipeline_db import PipelineDB
from lib.finpath_sectors import FinpathSectors


def main(db_path: str = "data/pipeline.db", force: bool = False) -> int:
    db = PipelineDB(db_path)
    fs = FinpathSectors(db)

    if force:
        db.conn.execute("DELETE FROM finpath_sectors_cache")
        db.conn.commit()
        print("Cleared cache.")

    try:
        count = fs.refresh_cache()
        print(f"Cached {count} tickers from Finpath API.")
        return 0
    except Exception as e:
        print(f"Refresh failed: {e}", file=sys.stderr)
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-path", default="data/pipeline.db")
    parser.add_argument("--force", action="store_true", help="Clear cache before refresh")
    args = parser.parse_args()
    sys.exit(main(db_path=args.db_path, force=args.force))
