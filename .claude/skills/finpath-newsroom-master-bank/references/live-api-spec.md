# Live API Spec — Real-time Data

Catalog page: `358273c7-a9a1-810f-a38e-d3c5b8dd5ed2`

## When to use Live API

Master gọi Live API khi:
- Cần giá cổ phiếu real-time hoặc gần real-time (T-1, T)
- Cần volume gần đây
- Cần market cap update
- DB BCTC chưa có data Q hiện tại (vd Q2/2026 chưa được import)

KHÔNG gọi Live API cho:
- Data lịch sử (đã có ở DB BCTC Quarter/Annual)
- Topic phân tích (đã có ở KB)

## Endpoints (placeholder — anh fill thực tế)

```python
# Stock price + volume
GET /api/v1/quote?ticker=VCB
# Response: { "price": 88500, "volume": 2.3e6, "change_pct": 1.2, "as_of": "2026-05-07T10:30:00Z" }

# Market cap
GET /api/v1/marketcap?ticker=VCB
# Response: { "market_cap_ty_dong": 425000, "shares_outstanding": 4.8e9 }

# Foreign room
GET /api/v1/foreignroom?ticker=VCB
# Response: { "foreign_owned_pct": 22.5, "foreign_room_pct": 7.5, "foreign_buy_5d": 1.2e6 }
```

⚠️ **Replace placeholders với actual endpoints** từ Live API catalog page khi user setup.

## Helper code pattern

```python
import requests

def fetch_live_quote(ticker: str) -> dict:
    """Fetch real-time quote. Cache 5 min."""
    try:
        r = requests.get(f"{LIVE_API_BASE}/quote", params={"ticker": ticker}, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        # Fallback web_search
        return None

# In master workflow Bước 5:
quote = fetch_live_quote(ticker)
if not quote:
    # Bước 6 fallback web_search
    web_results = web_search(f"giá cổ phiếu {ticker} hôm nay")
```

## Constraints

- **Timeout 5s** — Live API chậm hơn → fallback web_search
- **Cache 5 phút** — không hammer API
- **Log trong Ghi chú pipeline** nếu API fail
