# MCP `news_stock_harvester` — Evaluation cho thay thế Crawler Step 1

**Date:** 2026-05-12
**Tool:** `mcp__finpath-context__news_stock_harvester`
**Endpoint:** `https://api.finpath.vn/ai_service/api/v1/mcp`
**Mục đích:** Đánh giá xem có đủ thông tin để thay Crawler 20-source hiện tại không.

---

## Schema declared

```json
{
  "type": "object",
  "properties": {
    "symbol": {
      "type": "string",
      "description": "Optional stock ticker symbol (e.g., VCB, HPG, FPT)"
    }
  }
}
```

Chỉ 1 param duy nhất: `symbol` (Optional).

---

## Probe results — 10 test cases

Test với: `TCB`, `VCB`, `MBB`, `ACB`, `SSI`, `""` (empty), `INVALID_TICKER`, `TCB+limit=50`, `TCB+from/to`, `TCB+days=7`.

### KEY FINDING — Server IGNORE TOÀN BỘ params

| Test | Records | Time range | Response chars |
|---|---|---|---|
| TCB | 12 | 12/05 02:17 → 12/05 08:29 | 58,752 |
| VCB | 12 | 12/05 02:17 → 12/05 08:29 | 58,752 |
| MBB | 12 | 12/05 02:17 → 12/05 08:29 | 58,752 |
| ACB | 12 | 12/05 02:17 → 12/05 08:29 | 58,752 |
| SSI | 12 | 12/05 02:17 → 12/05 08:29 | 58,752 |
| `""` (empty) | 12 | identical | 58,752 |
| INVALID_TICKER | 12 | identical | 58,752 |
| TCB + limit=50 | 12 | identical | 58,752 |
| TCB + from/to | 12 | identical | 58,752 |
| TCB + days=7 | 12 | identical | 58,752 |

→ **Tất cả 10 responses BYTE-IDENTICAL.** Server hardcode trả về 12 records latest globally, không lọc theo ticker, không filter timerange, không respect limit.

→ **Ticker mention count trong body: 0** cho mọi mã test (TCB/VCB/MBB/ACB/SSI). Confirm response là **global news feed**, không filtered per ticker.

---

## Format trả về (raw structure)

### Header
```
## Tin chứng khoán (12 bản ghi gần đây)
```

### Per record
```
### [DD/MM HH:MM] <Title>

<Body — full text scraped, có "Đọc tiếp" + "Về trang Chủ đề" suffix, có thể có metadata footer như "Trở thành người đầu tiên tặng sao..." spam>

---
```

### Sample 12 records (body trimmed first 200 chars)

| # | Timestamp | Title | Body chars |
|---|---|---|---|
| 1 | 12/05 08:29 | Cơ hội 'làm mới' chính sách ngành ô tô | 7,117 |
| 2 | 12/05 07:58 | Bất ngờ phát hiện nợ thuế hàng trăm triệu đồng sau khi cài eTax Mobile | 8,718 |
| 3 | 12/05 07:32 | Tập đoàn của các tỉ phú Việt Nam kiếm bao nhiêu tiền mỗi ngày | 3,268 |
| 4 | 12/05 07:30 | Chứng khoán 12-5: Vì sao nhiều doanh nghiệp lãi lớn nhưng cổ phiếu chưa hút dòng | 3,573 |
| 5 | 12/05 06:26 | Những căn nhà xa hoa vắng bóng người ở New York và tranh cãi đánh thuế nhà thứ hai | 6,019 |
| 6 | 12/05 02:17 | Bí thư Trần Lưu Quang: TP.HCM sắp khởi động loạt dự án tổng vốn hơn 10 tỷ USD | 5,628 |
| 7 | 12/05 02:17 | Giá vàng SJC, vàng nhẫn hôm nay (ngày 12/5) | 3,161 |
| 8 | 12/05 02:17 | Tư nhân tham gia kiến tạo hạ tầng | 9,243 |
| 9 | 12/05 02:17 | Tối 11-5, giá vàng miếng SJC, vàng nhẫn rớt mạnh theo thế giới | 1,904 |
| 10 | 12/05 02:17 | Tất cả chủ xe vượt đèn đỏ, chạy quá tốc độ trong danh sách | 2,601 |
| 11 | 12/05 02:17 | Prudential Việt Nam chi trả gần 16.500 tỷ đồng quyền lợi bảo hiểm | 4,168 |
| 12 | 12/05 02:17 | Hà Nội có thêm 2 Phó chủ tịch UBND thành phố | 2,148 |

**Quan sát:**
- Topic mix: ô tô / thuế / tỉ phú / chứng khoán tổng quan / BĐS Mỹ / hạ tầng TP.HCM / vàng (×2) / giao thông / bảo hiểm / nhân sự HN
- **0 record nào về Bank cụ thể** (TCB/VCB/MBB/ACB/BID/CTG/VPB)
- **0 record nào về CK ticker cụ thể** (SSI/VND/HCM/VCI/SHS)
- Chỉ 1 record (#4) liên quan chứng khoán tổng quan ("VN-Index 11-5 giảm 20 điểm")
- **Time range 6h12min** (02:17 → 08:29) — feed update rất tươi nhưng SHALLOW span
- Body size dao động 1.9KB - 9.2KB, trung bình ~4.8KB per record

---

## Fields available vs Crawler schema cần

| Field crawler hiện cần | Trong response harvester? | Ghi chú |
|---|---|---|
| `source_name` | ❌ KHÔNG có field tách | Có thể parse từ body footer ("Tuổi Trẻ Online", "Tiền Phong", ...) — heuristic không chắc chắn |
| `source_url` (canonical link) | ❌ KHÔNG có | KHÔNG có field URL. Body có "Đọc tiếp" anchor nhưng không kèm href |
| `title` | ✅ trong header `### [...]` | OK parse |
| `body` / `snippet` | ✅ full text | Body lớn (avg 4.8KB), có metadata footer spam cần clean |
| `published_time` | ⚠️ partial — `[DD/MM HH:MM]` thiếu năm + timezone | Phải assume current year + UTC+7 → có thể sai khi crawl cuối năm |
| `ticker` | ❌ feed global, không tag ticker | Phải grep trong body — không strict |
| `crawled_at` | ✅ derive từ API call time | OK |
| `funnel_batch_id` | ❌ feed không có batch concept | Wrap script tự generate |
| `editor_v1_decision` (downstream) | ❌ feed không pre-classified | Editor V1 phải chạy trên parsed rows |

---

## Gap matrix vs Crawler hiện tại

| Aspect | Crawler 20-source | MCP harvester | Verdict |
|---|---|---|---|
| **Source diversity** | 20 nguồn báo VN (cafef, vietstock, tuoitre, ...) | 1 feed aggregated (mix nhiều báo nhưng không transparent) | Harvester thiếu transparency |
| **Symbol filter** | Strict per ticker keyword | KHÔNG (ignored) | **Harvester KHÔNG dùng được standalone cho per-ticker pipeline** |
| **Records per call** | 3 articles × 20 sources = 60 candidates | 12 fixed | Harvester thiếu depth |
| **Timerange** | Configurable (3 mới nhất) | Fixed last ~6h | Harvester KHÔNG dùng được cho historical sweep |
| **source_url** | Canonical URL từ scraping | KHÔNG | Render "Đọc bài gốc" sẽ broken |
| **published_time** | ISO timestamp full | DD/MM HH:MM partial | Cần parse + assume year/timezone |
| **Latency** | ~40s (20 sources × 2s) | ~1s | Harvester thắng |
| **Cost** | Free (own crawler) | Có cost API key | Crawler thắng |

---

## Verdict

❌ **KHÔNG ĐỦ thay thế Crawler hiện tại.** Lý do critical:

1. **Symbol filter không work** — server ignore param hoàn toàn. Mọi `/tin TCB` `/tin VCB` `/tin SSI` sẽ nhận cùng 1 feed không liên quan ticker.
2. **Feed global, không tag ticker** — 12 records hôm 12/05 trả về 0 record nào về Bank/CK universe (61 mã).
3. **Thiếu source_url** — render right column "Đọc bài gốc" link sẽ break.
4. **Time range cố định ~6h** — không đủ cho mã có ít tin (nhiều ngày mới có 1 bài).

## Cần gì để harvester đủ thay crawler?

Phải request Finpath team upgrade server-side:

1. **Strict symbol filter** — `symbol=TCB` chỉ trả về records có ticker TCB mention trong title/body
2. **`source_url` field** — return canonical link cho mỗi record (current chỉ có "Đọc tiếp" text)
3. **`source_name` field** — explicit source name (cafef.vn, tuoitre.vn) thay vì ẩn trong body
4. **Configurable `limit` param** — default 12 quá ít, cần ≥50 cho deep search
5. **Configurable `from`/`to` timerange** — default last 6h quá hẹp, cần 24h-7day window
6. **Full ISO `published_at`** — thay `[DD/MM HH:MM]` partial
7. **Ticker tag** — return `tickers: ["TCB", "VCB"]` array detected mentions per record (giúp Editor V1 skip universe validation)

→ **Đề xuất feedback gửi Finpath team**: nếu họ implement 7 items trên thì harvester có thể replace crawler. Hiện tại fit cho **augment** (thêm vào layer fallback Master/Skeptic) thay vì **replace**.

---

## Files to evaluate

- `tmp/mcp-eval/harvester-raw.json` — full raw JSON envelope (770 KB, 10 test cases)
- `tmp/mcp-eval/EVAL.md` — file này

Recommend đọc raw response (1 sample đủ vì 10 identical) để confirm format observation.
