# Brief Schema Full — V2.2 (1.2)

Full JSON schema với examples cho mỗi field.

## Schema

```json
{
  "row_id": "string — Notion page ID của row Crawl Log",
  "ticker": "string — 1 of 16 universe",
  "sector": "Bank | CK | BĐS",
  
  "angle": "string — hướng đi specific, KHÔNG generic. TIẾNG VIỆT THUẦN, KHÔNG đính enum tag (vd ❌ 'Trade-off chủ động (strategic-shift)' → ✅ 'Đánh đổi chủ động — chuyển hướng chiến lược')",
  "angle_rationale": "string 1-2 câu — vì sao chọn hướng này",
  "source_rationale": "string 1-2 câu — vì sao chọn nguồn này",
  
  "insight_hypothesis": "string 1 CÂU — phát biểu insight specific, không hedge. TIẾNG VIỆT THUẦN, không jargon Anh không giải thích",
  "why_chosen": "string 3+ câu — Story Editor judgment cho sếp đọc",
  "insight_type": "string ENUM — phân loại cổ phiếu | decode | risk | pattern | catalyst | strategic-shift | industry-impact | position. METADATA ONLY — KHÔNG xuất hiện trong angle text hoặc content user-facing",
  
  "data_spec": {
    "fetch_dbs": ["array — DB names cần Master query"],
    "kb_topics": ["array — KB topic IDs cần Master fetch"],
    "fetch_keys": ["array — specific data points format <ticker>|<period>|<field>"]
  },
  
  "memory_check": {
    "passed": "boolean",
    "recent_angles": ["array — angle của 3 bài gần nhất"],
    "recent_insight_types": ["array — insight_type của 3 bài gần nhất"]
  },
  
  "primary_url": "string — URL bài gốc primary (cho Skeptic Pass 4.5 conditional fetch)"
}
```

## Example 1 — Bank brief (TCB)

```json
{
  "row_id": "abc-123-...",
  "ticker": "TCB",
  "sector": "Bank",
  
  "angle": "Pattern strategic shift — capital raise + 3-layer liquidity convergence",
  "angle_rationale": "TCB Q1 vừa tăng vốn 60% lên 113.738 tỷ + tiếp tục Lottner 3-layer liquidity model. 2 strategic moves cùng năm = pattern lớn worth deep dive.",
  "source_rationale": "CafeF cover ĐHĐCĐ chi tiết nhất với quotes Hồ Hùng Anh + Jens Lottner + số liệu cụ thể. Báo Pháp luật có LIVE coverage thay thế.",
  
  "insight_hypothesis": "TCB tăng vốn 60% chuẩn bị cho M&A + duy trì 3-layer liquidity với chi phí 5K tỷ/năm — pattern strategic shift sang ngân hàng tư nhân vốn lớn nhất, phù hợp NĐT giá trị giữ trên 18 tháng",
  
  "why_chosen": "Bài pick vì 3 lý do: (1) Data foundation mạnh — DB BCTC Bank Quarter có TCB Q1/2026 đầy đủ với LNTT 8.900 tỷ + dư nợ 796.864 tỷ + NPL 1.15% + CASA 37.9%, KB có topic Bank-Liquidity-3-layer-Framework + Big4-vs-Tu-nhan-target-pattern. (2) Insight WOW level cao — TCB từ vốn 70K tỷ → 113K tỷ trong 1 năm là biggest VN bank capital raise, pattern strategic shift kết hợp với Lottner liquidity innovation tạo angle độc đáo. (3) Timely — ĐHĐCĐ vừa xảy ra 25/4, news breaking. Memory: 3 bài TCB gần khác angle (NPL trái phiếu, CFS Q4, Lottner liquidity standalone) → variety OK + lần này là pattern hợp nhất cả strategic + financial.",
  
  "insight_type": "strategic-shift",
  
  "data_spec": {
    "fetch_dbs": ["BCTC_Quarter", "BCTC_Annual", "Targets", "M&A"],
    "kb_topics": ["TCB-Lottner-era", "Bank-Liquidity-3-layer-Framework", "Big4-vs-Tu-nhan-target-pattern"],
    "fetch_keys": [
      "TCB|2026-Q1|LNTT", "TCB|2026-Q1|du_no", "TCB|2026-Q1|NPL_pct", "TCB|2026-Q1|CASA_pct",
      "TCB|2025|Von_dieu_le", "TCB|2026|target_LNTT_plan_A", "TCB|2026|target_LNTT_plan_B"
    ]
  },
  
  "memory_check": {
    "passed": true,
    "recent_angles": ["NPL trái phiếu cycle", "CFS Q4/2025 read", "Lottner liquidity standalone"],
    "recent_insight_types": ["risk", "decode", "pattern"]
  },
  
  "primary_url": "https://cafef.vn/tcb-dhdcdq-2026-..."
}
```

## Example 2 — Reject (low data foundation)

Brief NOT created. Logged in `rejected[]`:

```json
{
  "row_id": "xyz-456-...",
  "reject_reason": "low_data_foundation",
  "reject_note": "Tin về deal Sân bay Gia Bình 196K tỷ TCB tài trợ — DB chưa có deal data, web search chỉ 2 nguồn cùng nội dung không đủ anchor. Master không thể viết sâu mà chỉ paraphrase news."
}
```
