# Live API Spec — Real-time Data

Live data via `lib/finpath_api.py` `FinpathAPI` — base URL `https://api.finpath.vn`.

## When to use Live API

Master gọi Live API khi:
- Cần giá cổ phiếu real-time hoặc gần real-time (T-1, T)
- Cần volume gần đây
- Cần market cap update
- DB BCTC chưa có data Q hiện tại (vd Q2/2026 chưa được import)

KHÔNG gọi Live API cho:
- Data lịch sử (đã có ở DB BCTC Quarter/Annual)
- Topic phân tích (đã có ở KB)

## Endpoints via FinpathAPI

```python
from lib.finpath_api import FinpathAPI
api = FinpathAPI()  # base_url="https://api.finpath.vn", timeout=10, in-memory cache

# Bank ratios: NIM, CASA, COF, NPL, LDR, P/E, P/B, ROE
ratios = api.get_bank_ratios("VCB")
# Returns: {"quarterlyProfits": [...], "yearlyProfits": [...]}

# Shareholders / foreign room
shareholders = api.get_shareholders("VCB")

# Events (M&A, corporate actions)
events = api.get_events("VCB")

# Company profile (market cap, shares outstanding)
profile = api.get_company_profile("VCB")
```

## Helper code pattern

```python
from lib.finpath_api import FinpathAPI

# In master workflow Bước 5:
api = FinpathAPI()
try:
    ratios = api.get_bank_ratios(ticker)
except Exception:
    ratios = None

if not ratios:
    # Bước 6 fallback web_search
    web_results = web_search(f"giá cổ phiếu {ticker} hôm nay")
```

## Constraints

- **Timeout 5s** — Live API chậm hơn → fallback web_search
- **Cache 5 phút** — không hammer API
- **Log trong Ghi chú pipeline** nếu API fail
