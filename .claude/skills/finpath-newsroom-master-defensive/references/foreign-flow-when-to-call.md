# Foreign Flow — Khi nào Master call API?

> Loaded from `Skill: finpath-newsroom-master-{sector}`. Same pattern as get_income_statement / get_bank_ratios — call when body needs the data.

## Available API methods

- `api.get_foreign_rooms()` — all foreign flow snapshot
- `api.get_foreign_roomstatistics(ticker, period)` — drilldown over period (1D/1W/1M/3M/6M/1Y)
- `api.get_foreign_roombars(ticker)` — time series daily

## Call API khi viết bài:

### Trigger 1: Brief angle mention NN flow

Khi `brief.angle_narrative` hoặc `brief.deep_question` mention NN flow:
- MUST cite số liệu cụ thể trong body
- Call `api.get_foreign_rooms()` → lookup ticker → cite dnva

### Trigger 2: Body cần institutional context

Vd "ai đẩy giá hôm nay?" hoặc "tin tốt nhưng không có ai mua":
- Call để answer question concretely với data
- Add to data_trail entry với source "Finpath_API/foreign-rooms"

### Trigger 3: Multi-period trend narrative

"NN bán ròng 5 phiên liên tiếp":
- Call `api.get_foreign_roomstatistics(ticker, period="1W")`
- Cite specific số cho từng phiên hoặc total

### Trigger 4: Time series chart-like long-form

"30 ngày qua institutional sentiment":
- Call `api.get_foreign_roombars(ticker)`
- Cite trend pattern (consecutive selling, V-recovery, etc.)

## KHÔNG call khi:

- Bài về fundamental (lãi/lỗ/ROE/ratio analysis) — NN flow off-topic
- Format `flash_qa` 100-150 từ — không đủ space cite extra signal
- Brief KHÔNG mention NN + angle khác (Q1 report, ĐHĐCĐ event) — don't force fit
- Stance đã có 3+ key_evidence solid — không cần thêm NN

## Cite format

- Bold số tỷ: `**NN bán ròng 85,78 tỷ**`
- Format VN: `85780000000` → `"85,78 tỷ"` (dấu phẩy thập phân, đơn vị "tỷ")
- Period clear: "phiên 12/5" / "tuần qua" / "5 phiên liên tiếp" / "30 ngày qua"

## Data trail entry MUST

```yaml
data_trail:
  - source: "Finpath_API/foreign-rooms"      # hoặc "Finpath_API/roomstatistics" / "Finpath_API/roombars"
    fetched: "dnva = -85780000000 (today net VND)"
    purpose: "cite NN sell pressure"
    supports_argument: "Opening question paragraph"
```

## Example body cite

### Listicle bullet

> - **NN bán ròng 85,78 tỷ phiên 12/5**: institutional rút trong khi giá tăng kịch trần. Câu hỏi đặt ra: ai đang đẩy giá (retail FOMO? prop trading?), và đợt tăng này có bền không?

### Opening paragraph (Q&A format)

> Cổ phiếu VHM tăng kịch trần 6,8% phiên 12/5, nhưng **khối ngoại bán ròng 85,78 tỷ** — top 1 thị trường. Câu hỏi: tại sao institutional thoát khi giá đỉnh ATH?

### Multi-period narrative

> Trong 5 phiên gần nhất, **khối ngoại bán ròng tổng 340 tỷ** với BSR — chuỗi rút vốn dài nhất 6 tháng qua. Pattern này thường báo hiệu sector cycle inflection.

## Anti-patterns

- ❌ Cite NN khi không relevant tới insight ("force fit" data trail entry)
- ❌ "NN đang có vẻ bán" (vague — phải số cụ thể với period)
- ❌ "85.78 billion VND" (Anh — phải VN "85,78 tỷ")
- ❌ Cite mỗi paragraph — overkill, 1-2 cite/article đủ
