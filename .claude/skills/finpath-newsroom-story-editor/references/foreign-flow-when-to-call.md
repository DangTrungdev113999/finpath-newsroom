# Foreign Flow — Khi nào Story Editor call API?

> Loaded from `Skill: finpath-newsroom-story-editor`. Free-form judgment — KHÔNG prescriptive "must call". Guide WHEN call adds stance signal value.

## Available API methods

- `api.get_foreign_rooms()` — snapshot all ~1902 records foreign flow (use to lookup ticker)
- `api.get_foreign_roomstatistics(ticker, period)` — per-ticker drilldown, period ∈ {1D, 1W, 1M, 3M, 6M, 1Y}
- `api.get_foreign_roombars(ticker)` — time series daily bars

## Call API khi:

### Trigger 1: Ticker đang Hot + stance unclear

Khi crawl_log row có ticker đang trong top tăng/giảm mạnh, NHƯNG insight chưa định hình stance rõ:

```python
rooms = api.get_foreign_rooms()
my_ticker = next((r for r in rooms if r["c"] == ticker), None)
if my_ticker:
    dnva = my_ticker.get("dnva", 0)
    # dnva > 0 = NN mua ròng VND. < 0 = NN bán ròng.
```

- NN dnva > 50 tỷ + price up → strong institutional confirm → positive stance high confidence
- NN dnva < -50 tỷ + price up → "ai đẩy giá khi NN rút?" → caution flag, stance medium confidence

### Trigger 2: Brief candidate có angle về money flow

Khi `angle_narrative` draft mentions "ai đặt cược", "thị trường đang nghi ngờ", "institutional sentiment":
- MUST call foreign API để có concrete data backing
- Add `key_evidence` entry: "NN [mua/bán] ròng [X] tỷ phiên [date]"

### Trigger 3: Multi-period trend confirmation

Khi stance dựa trend (vd "downtrend cần xác nhận"):
- Call `get_foreign_roomstatistics(ticker, "1W")` — 5 phiên gần
- Or `get_foreign_roomstatistics(ticker, "1M")` cho monthly trend

## KHÔNG call khi:

- Stance đã clear từ 7-layer khác (BCTC + sector cycle + chiến lược rõ) — don't waste API call
- Brief về fundamental sự kiện (Q1 report, BCTC, ĐHĐCĐ) — NN flow off-topic
- Ticker không Hot + không price action — NN flow signal weak
- Bài format `flash_qa` 100-150 từ — quá ngắn cite extra signal

## Cite format trong stance_directive

Khi call → add to `key_evidence` array:
- "NN bán ròng 85,78 tỷ phiên 12/5" (cụ thể số tỷ + period)
- "Top 30 NN bán ròng thị trường" (rank context, nếu drilldown rank lookup)
- Period clear: "phiên 12/5" (1D), "5 phiên" (1W), "tháng 5" (1M)

## Decision matrix 4-quadrant (price + foreign confirmed)

|  | Price up | Price down |
|---|---|---|
| **NN strong buy (>50 tỷ)** | STRONG BULLISH — institutional confirm | "Ai đang đặt cược ngược?" — positive medium |
| **NN strong sell (<-50 tỷ)** | "Ai đẩy giá khi NN rút?" — caution flag | STRONG BEARISH — institutional confirm sell |
| **NN normal** | Price signal only | Price signal only |
| **NN no data** | Skip foreign signal | Skip foreign signal |

## Examples

### Case 1: VHM tăng 6,8% + NN bán ròng 85,78 tỷ

```yaml
stance_directive:
  direction: neutral
  confidence: medium
  reason: |
    VHM tăng kịch trần 6,8% phiên 12/5 nhưng khối ngoại bán ròng top
    thị trường (85,78 tỷ). Tín hiệu CONTRADICT — institutional thoát
    trong khi retail đẩy giá. Cần check WHO đang mua + tin gì làm
    catalyst trước khi confirm direction.
  key_evidence:
    - "NN bán ròng 85,78 tỷ phiên 12/5"
    - "Price +6.8% intraday (kịch trần)"
```

### Case 2: FPT tăng 4% + NN mua ròng top

```yaml
stance_directive:
  direction: positive
  confidence: high
  reason: |
    FPT tăng giá cùng NN mua ròng top 30 (+120 tỷ phiên 12/5).
    Institutional confirm uptrend, không phải pump retail.
    7-layer nội lực: Q1 LNST tăng + sector tech đỉnh cycle.
  key_evidence:
    - "NN mua ròng 120 tỷ phiên 12/5"
    - "FPT Software Q1 +28% YoY"
    - "Tech sector tailwind cycle"
```

## Anti-pattern

- ❌ Call API mỗi brief khi không cần — waste tokens + time
- ❌ Cite "NN bán" without specific số → vague, fail Voice Rule 2 no-hedging
- ❌ Force fit foreign signal khi angle là fundamental → off-topic
