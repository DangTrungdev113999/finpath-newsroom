"""Crawler stage — Step 1 of pipeline.

This script writes candidates (already fetched by Claude via WebSearch + WebFetch)
to SQLite crawl_log with a funnel_batch_id. It does NOT make HTTP calls itself.
"""
from __future__ import annotations
import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Ensure project root is on sys.path when run as a script
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# Full 61-mã universe (Bank 27 + CK 30 + BĐS 4).
# Source of truth: .claude/skills/finpath-newsroom-editor/scripts/routing.py::FULL_UNIVERSE
# Inlined here to avoid import-time circular dep; keep in sync with routing.py.
BANK_UNIVERSE = [
    "VCB", "CTG", "BID", "TCB", "MBB", "ACB", "VPB", "HDB",
    "STB", "SHB", "EIB", "TPB", "MSB", "LPB", "OCB", "VIB",
    "NAB", "BAB", "NVB", "SGB",
    "VAB", "BVB", "ABB", "KLB", "VBB", "PGB", "HDF",
]
CK_UNIVERSE = [
    "SSI", "VND", "HCM", "VCI", "VIX",
    "SHS", "MBS", "BVS", "BSI", "AGR", "CTS", "APG", "EVS",
    "IVS", "PSI", "TVS", "WSS", "ORS", "VFS", "TCI",
    "DSC", "FTS", "CSI", "SBS", "PHS", "ART", "APS", "BMS", "AAS", "VTS",
]
BDS_UNIVERSE = ["VHM", "NVL", "KDH", "DXG"]
FULL_UNIVERSE = BANK_UNIVERSE + CK_UNIVERSE + BDS_UNIVERSE

SOURCES_WHITELIST = {
    "CafeF": "cafef.vn",
    "VnEconomy": "vneconomy.vn",
    "Vietstock": "vietstock.vn",
    "Báo Pháp luật": "doanhnhan.baophapluat.vn",
    "Tin nhanh chứng khoán": "tinnhanhchungkhoan.vn",
    "VnExpress": "vnexpress.net",
    "Báo Đầu tư": "baodautu.vn",
    "Diễn đàn Doanh nghiệp": "diendandoanhnghiep.vn",
    "Nhịp sống Kinh tế": "nhipsongkinhdoanh.vn",
    "Thời báo Tài chính": "thoibaotaichinhvietnam.vn",
    "Người Lao động": "nld.com.vn",
    "Thanh Niên": "thanhnien.vn",
    "Tuổi Trẻ": "tuoitre.vn",
    "Lao Động": "laodong.vn",
    "Saigon Times": "saigontimes.vn",
    "VietnamNet": "vietnamnet.vn",
    "Báo Tin tức": "baotintuc.vn",
    "VietnamFinance": "vietnamfinance.vn",
    "Bizlive": "bizlive.vn",
    "Reatimes": "reatimes.vn",
}


def build_queries(ticker: str, sector: str = "Bank") -> list[str]:
    company_name = {
        "TCB": "Techcombank", "VCB": "Vietcombank", "MBB": "MB Bank",
        "ACB": "ACB", "BID": "BIDV", "CTG": "VietinBank", "VPB": "VPBank",
    }.get(ticker, ticker)
    return [
        f"{ticker} {company_name}",
        f"{ticker} kết quả kinh doanh",
        f"{ticker} cổ phiếu tin tức",
        f"{ticker} ngân hàng",
    ]


def make_funnel_batch_id(ticker: str) -> str:
    return f"{ticker}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')}"


def write_candidate_to_db(db, candidate: dict, funnel_batch_id: str) -> str | None:
    row_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()
    try:
        db.insert_crawl_row({
            "row_id": row_id,
            "funnel_batch_id": funnel_batch_id,
            "ticker": candidate["ticker"],
            "source_name": candidate["source_name"],
            "source_url": candidate["url"],
            "title": candidate.get("title", "(no title)"),
            "raw_content": (candidate.get("content") or "")[:2000],
            "published_time": candidate.get("published_time"),
            "crawled_at": now_iso,
        })
        return row_id
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Crawler stage — write candidates to SQLite")
    parser.add_argument("ticker", help="Bank ticker (e.g. VCB)")
    parser.add_argument("--candidates-json", type=Path, required=True,
                        help="Path to JSON file with array of candidate dicts")
    parser.add_argument("--db", type=Path, default=Path("data/pipeline.db"))
    parser.add_argument("--schema", type=Path, default=Path("data/pipeline.schema.sql"))
    args = parser.parse_args()

    ticker = args.ticker.upper()
    if ticker not in FULL_UNIVERSE:
        print(json.dumps({"error": f"{ticker} not in 61-mã FULL_UNIVERSE (Bank/CK/BĐS)", "universe_count": len(FULL_UNIVERSE)}))
        return 1

    from lib.pipeline_db import PipelineDB

    args.db.parent.mkdir(parents=True, exist_ok=True)
    needs_schema = (not args.db.exists()) or args.db.stat().st_size == 0
    db = PipelineDB(args.db)
    if needs_schema:
        db.init_schema(args.schema)

    candidates = json.loads(args.candidates_json.read_text(encoding="utf-8"))
    if not isinstance(candidates, list):
        print(json.dumps({"error": "candidates JSON must be a list"}))
        return 1

    funnel_batch_id = make_funnel_batch_id(ticker)
    rows_written = []
    rows_skipped = 0
    errors = []

    for c in candidates:
        c.setdefault("ticker", ticker)
        if "url" not in c or "source_name" not in c:
            errors.append({"candidate": c, "error": "missing url or source_name"})
            continue
        rid = write_candidate_to_db(db, c, funnel_batch_id)
        if rid:
            rows_written.append({"row_id": rid, "url": c["url"], "source_name": c["source_name"]})
        else:
            rows_skipped += 1

    db.close()
    print(json.dumps({
        "ticker": ticker,
        "funnel_batch_id": funnel_batch_id,
        "rows_written": rows_written,
        "rows_skipped_dedupe": rows_skipped,
        "errors": errors,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
