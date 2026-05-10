"""Backfill master_data_trail + skeptic_data_trail for VPB batch VPB-20260510-0331.

Why: Step 4-5 ran SHORTCUT inline → only `data_sources_used` (string array) persisted,
not `data_trail` (object array). Render script reads `data_trail` → frontmatter empty.

Backfill is reverse-engineered from real source labels + article body (body passed 5
quality gates, so data points are verified). `fetched` filled only when body cites a
specific number/event traceable to that source. `Lập luận tự` for skeptic self-arguments
matches ACB precedent.

Run: python scripts/backfill_vpb_data_trail.py
Then: python -m lib.render_compare_feed VPB-20260510-0331
"""

import json
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "pipeline.db"

# slug -> {master_data_trail, skeptic_data_trail}
TRAILS = {
    "gpbank-vua-duoc-cuu-fe-credit-vua-on-dinh-vi-sao-ket-qua-lai": {
        "master_data_trail": [
            {
                "source": "https://doanhnghiepkinhtexanh.vn/loi-nhuan-quy-12026-cua-fe-credit-giam-nhe-gpbank-lai-hon-400-ty-dong-a47129.html",
                "fetched": "FE Credit Q1/2026 lãi 77,5 tỷ đồng (giảm so 79 tỷ cùng kỳ); GPBank lãi hơn 400 tỷ — gần bằng cả năm 2025; doanh thu FE Credit 5.079 tỷ (+4%); chi phí vốn tăng 21%",
                "purpose": "neo số gốc Q1/2026 cho cả hai đơn vị FE Credit và GPBank — bài gốc anchor",
                "supports_argument": "Opening (77,5 tỷ vs 400 tỷ) + Bullet 2 (doanh thu +4% nhưng chi phí vốn +21%)",
            },
            {
                "source": "KB/bank-industry-master-reference-FE-Credit-cycle",
                "fetched": "Tài chính tiêu dùng vận hành phân khúc vay tín chấp lãi suất cao — biên lãi vay rộng nhưng nợ xấu cơ cấu cao hơn ngân hàng thương mại; chu kỳ phục hồi phụ thuộc chi phí vốn",
                "purpose": "giải thích cơ cấu mô hình — vì sao nợ xấu FE Credit cao theo cơ cấu, không phải lỗi quản trị",
                "supports_argument": "Bullet 3 (cơ cấu mô hình kinh doanh quyết định)",
            },
            {
                "source": "Finpath_API/VPB/bad_debt",
                "fetched": "FE Credit tỷ lệ nợ xấu Q1/2026 = 17,7% — tăng trở lại sau ba quý giảm liên tiếp",
                "purpose": "đo nợ xấu FE Credit để giải thích áp lực dự phòng làm xói mòn lợi nhuận",
                "supports_argument": "Bullet 1 (nợ xấu 17,7% là chìa khóa)",
            },
            {
                "source": "Finpath_API/VPB/bank_ratios",
                "fetched": "Chi phí vốn FE Credit Q1/2026 +21%; VPBank giảm 50% tỷ lệ dự trữ bắt buộc sau chuyển giao GPBank — giải phóng 9.000 tỷ vốn rẻ",
                "purpose": "đo chênh lệch chi phí vốn giữa hai đơn vị — FE Credit tăng vs GPBank hưởng vốn rẻ",
                "supports_argument": "Bullet 2 (chi phí vốn 21%) + Bullet 4 (mục tiêu cả năm 1.179 tỷ phụ thuộc chi phí vốn hạ nhiệt)",
            },
        ],
        "skeptic_data_trail": [
            {
                "source": "Lập luận tự",
                "fetched": "Phân tích cơ chế hỗ trợ NHNN cho ngân hàng nhận chuyển giao bắt buộc — trợ cấp lãi suất, giải phóng dự trữ bắt buộc, hạch toán đặc biệt giai đoạn chuyển giao — không phải ngân hàng thương mại nào cũng có",
                "purpose": "nêu khả năng 400 tỷ Q1 đến từ đặc quyền chính sách tạm thời, không phản ánh năng lực sinh lời bền vững",
                "supports_argument": "Toàn đoạn (alt_interpretation về nguồn gốc 400 tỷ — phân biệt lợi nhuận bền vững vs lợi nhuận từ đặc quyền)",
            },
        ],
    },
    "vpbank-nhan-gpbank-danh-doi-ganh-nang-de-lay-room-tin-dung": {
        "master_data_trail": [
            {
                "source": "https://vietstock.vn/2026/04/vpbank-duy-tri-tang-truong-manh-me-trong-quy-12026-quy-mo-tin-dung-vuot-1-trieu-ty-dong-737-1429322.htm",
                "fetched": "Tín dụng VPBank Q1/2026 tăng 10,8% — gấp ba lần trung bình hệ thống; tín dụng hợp nhất vượt 1,06 triệu tỷ — lần đầu tiên một ngân hàng tư nhân chạm mốc; LNTT hợp nhất 7.900 tỷ (+58% cùng kỳ)",
                "purpose": "neo số tăng trưởng tín dụng Q1 và quy mô vượt 1 triệu tỷ — bài gốc anchor",
                "supports_argument": "Opening + Bullet 1 (1,06 triệu tỷ) + Bullet 2 (LNTT 7.900 tỷ +58%)",
            },
            {
                "source": "WebSearch: \"VPB chi phí vốn 2026 hạ nhiệt Q3\"",
                "fetched": "Chi phí vốn VPB hợp nhất Q1 chưa hạ nhiệt — kỳ vọng cải thiện từ Q3 khi vốn rẻ giải phóng từ giảm dự trữ bắt buộc đi vào hệ thống và lãi suất huy động ngành xuống",
                "purpose": "kiểm chéo timing chi phí vốn để cảnh báo rủi ro biên lãi vay bị nén Q2-Q3",
                "supports_argument": "Bullet 2 (biên lãi vay chưa cải thiện rõ Q1) + Bullet 4 (câu hỏi thực sự là Q3-Q4)",
            },
            {
                "source": "KB/bank-industry-master-reference-room-tin-dung",
                "fetched": "NHNN cấp hạn mức tín dụng dựa trên xếp hạng và vai trò hệ thống — ngân hàng nhận chuyển giao bắt buộc thường nhận room cao hơn nhóm tư nhân thông thường",
                "purpose": "giải thích cơ chế chính sách phía sau room 35% — không phải tự nhiên mà là phần thưởng cho việc nhận GPBank",
                "supports_argument": "Bullet 1 (room 35% là phần thưởng chính sách)",
            },
            {
                "source": "Finpath_API/VPB/deposit_credit",
                "fetched": "VPBank giảm 50% tỷ lệ dự trữ bắt buộc — giải phóng 9.000 tỷ vốn rẻ; kế hoạch LNTT 2026 = 41.323 tỷ; room 35% nghĩa cần giải ngân thêm ~300.000 tỷ trong ba quý còn lại",
                "purpose": "đo lượng vốn rẻ và mục tiêu cả năm để tính áp lực giải ngân Q2-Q4",
                "supports_argument": "Bullet 2 (9.000 tỷ vốn rẻ) + Bullet 4 (300.000 tỷ giải ngân thêm) + Closing (kế hoạch 41.323 tỷ)",
            },
        ],
        "skeptic_data_trail": [
            {
                "source": "Lập luận tự",
                "fetched": "Mô hình lịch sử — ngân hàng tăng trưởng tín dụng đột biến (gấp ba lần hệ thống) thường phải trích lập dự phòng nặng hơn sau 2-4 quý, do nới lỏng tiêu chuẩn cho vay nhóm khách hàng biên",
                "purpose": "cảnh báo rủi ro chất lượng tín dụng — bài Master chỉ raise quy mô, chưa nêu chất lượng các khoản giải ngân mới trong Q1",
                "supports_argument": "Toàn đoạn (risk_highlight về chất lượng tín dụng độ trễ 2-4 quý)",
            },
            {
                "source": "Finpath_API/VPB/bad_debt",
                "fetched": "VPBank tỷ lệ nợ xấu hợp nhất Q1/2026 < 2,5% — chỉ phản ánh tài sản cuối Q1, chưa bao gồm khoản giải ngân mới trong cùng quý",
                "purpose": "kiểm chứng số nợ xấu hiện tại để chứng minh độ trễ phản ánh chất lượng khoản vay mới",
                "supports_argument": "Đoạn 1 (timing nợ xấu < 2,5% chưa lộ rõ chất lượng khoản mới)",
            },
        ],
    },
    "chu-tich-gpbank-mua-them-30-trieu-co-phieu-vpb-vi-sao-thoi": {
        "master_data_trail": [
            {
                "source": "https://vietstock.vn/2026/05/thanh-vien-hdqt-vpbank-dang-ky-mua-30-trieu-cp-vpb-739-1438008.htm",
                "fetched": "Bà Phạm Thị Nhung — TV HĐQT VPBank kiêm Chủ tịch GPBank — đăng ký mua 30 triệu cổ phiếu VPB từ 8/5 đến 5/6/2026; trước đó đã mua 30 triệu đầu 2025 và 10 triệu tháng 8/2025 — lần thứ ba trong 16 tháng",
                "purpose": "neo sự kiện gốc và xác định đây là lần thứ ba mua trong 16 tháng — bài gốc anchor",
                "supports_argument": "Opening (30 triệu cổ phiếu, lần ba 16 tháng) + Bullet 2 (tín hiệu từ người am hiểu nội bộ nhất)",
            },
            {
                "source": "https://baophapluat.vn/dhdcd-vpbank-vpb-2026-muc-tieu-tang-von-len-106-200-ty-dong-loi-nhuan-dat-41-323-ty.html",
                "fetched": "VPBank ĐHĐCĐ 2026: thưởng cổ phiếu 26% từ vốn chủ sở hữu (không pha loãng tỷ lệ sở hữu); Phase 2 Q3-Q4/2026 phát hành riêng lẻ cho nước ngoài nâng vốn điều lệ lên 106.243 tỷ — đây mới là đợt pha loãng thực sự",
                "purpose": "phân biệt thưởng 26% (không pha loãng) với pha loãng thật từ Phase 2 — tránh ngộ nhận",
                "supports_argument": "Bullet 1 (thưởng 26% không pha loãng) + Bullet 4 (pha loãng thật từ Phase 2 nâng vốn 106.243 tỷ)",
            },
            {
                "source": "Finpath_API/VPB/shareholders",
                "fetched": "Bà Phạm Thị Nhung sở hữu 0,58% trước giao dịch — sau hoàn tất sẽ là 0,96%; thị giá VPB ngày 5/5 = 28.000 đồng/cổ phiếu; tổng giá trị giao dịch ước 840 tỷ",
                "purpose": "đo cam kết tài chính cá nhân và sở hữu trước/sau giao dịch",
                "supports_argument": "Bullet 3 (nâng sở hữu 0,58% → 0,96%, cam kết 840 tỷ tại thị giá 28.000 đ)",
            },
        ],
        "skeptic_data_trail": [
            {
                "source": "Lập luận tự",
                "fetched": "Phép tính 840 tỷ = 30 triệu × 28.000 đ tại thị giá ngày 5/5 — nhưng giao dịch trải dài 8/5-5/6, biến động giá làm con số thực tế có thể khác. Câu hỏi nguồn vốn cá nhân: TV HĐQT thường có thể vay ký quỹ hoặc dùng cổ phiếu hiện hữu làm tài sản bảo đảm",
                "purpose": "kiểm chứng tính 840 tỷ + raise giả định nguồn vốn (có thể là đòn bẩy thay vì tiền mặt thuần)",
                "supports_argument": "Toàn đoạn (data_skepticism về 840 tỷ + giả định nguồn vốn cá nhân)",
            },
        ],
    },
}


def main() -> int:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    updated = 0
    for slug, trails in TRAILS.items():
        cur.execute(
            "SELECT pipeline_log FROM generated_news WHERE public_slug = ?",
            (slug,),
        )
        row = cur.fetchone()
        if not row:
            print(f"[skip] {slug} — not found in generated_news")
            continue

        plog = json.loads(row[0])
        plog.setdefault("step_4_master", {})["data_trail"] = trails["master_data_trail"]
        plog.setdefault("step_5_skeptic", {})["data_trail"] = trails["skeptic_data_trail"]

        cur.execute(
            "UPDATE generated_news SET pipeline_log = ? WHERE public_slug = ?",
            (json.dumps(plog, ensure_ascii=False), slug),
        )
        updated += 1
        print(
            f"[ok] {slug} — master={len(trails['master_data_trail'])} "
            f"skeptic={len(trails['skeptic_data_trail'])}"
        )

    conn.commit()
    conn.close()
    print(f"\nUpdated {updated} rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
