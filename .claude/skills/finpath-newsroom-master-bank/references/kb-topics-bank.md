# KB ngành Ngân hàng — Topic Catalog

KB ID: `358273c7-a9a1-8164-8981-f2ac7807a13b` (Bank-only, KHÔNG share cross-sector)

## Topic categories

### 1. Frameworks (analytical models)
- `Bank-Liquidity-3-layer-Framework` — Jens Lottner's 3-layer liquidity model (TCB innovation, ngân hàng VN đầu tiên áp dụng)
- `Big4-vs-Tu-nhan-target-pattern` — pattern under-promise của Big 4 (VCB/BID/CTG/Vietinbank), conservative target để dễ vượt
- `Basel-III-CAR-VN` — Basel III implementation timeline VN, CAR yêu cầu
- `NPL-coverage-ratio-benchmark` — benchmark NPL/coverage 2018-2026 ngành

### 2. Industry trends
- `CASA-evolution` — CASA trend ngành 2020-2026, các bank dẫn đầu
- `Credit-growth-policy-NHNN` — chính sách credit room hàng năm
- `Foreign-ownership-cap-VN` — quy định trần sở hữu ngoại 30% bank

### 3. Historical analogs
- `VCBNeo-VNCB-cycle` — pattern xử lý ngân hàng 0 đồng (VNCB→GP Bank→OceanBank cycle)
- `2008-Bank-bailout-VN` — bailout cycle 2008-2012
- `2018-NPL-spike-VN` — spike NPL 2018 sau Thông tư 02/2017
- `2022-Bond-crisis` — khủng hoảng trái phiếu doanh nghiệp 2022 (Vạn Thịnh Phát, Tân Hoàng Minh)

### 4. Reports & statements
- `NHNN-circulars-2024-2026` — danh sách thông tư NHNN gần đây
- `BCTC-disclosure-rules` — quy định công bố BCTC ngân hàng
- `Stress-test-2025-NHNN` — kết quả stress test NHNN năm 2025

### 5. Bank-specific (per ticker)
- `VCB-strategic-shifts` — các quyết định chiến lược VCB qua năm
- `TCB-Lottner-era` — Jens Lottner CEO era của TCB (2020-now)
- `MBB-tech-bank-positioning` — positioning fintech của MBB
- `ACB-conservative-strategy` — chiến lược conservative của ACB
- `BID-VCB-state-mandate` — vai trò state mandate của BID + VCB
- `CTG-foreign-strategic` — strategic foreign partner của CTG
- `VPB-FE-Credit-cycle` — cycle FE Credit (VPB) 2018-2024

## Query pattern

Story Editor lightweight access — chỉ check topic exists:
```python
result = query_data_sources(
    data_source_id="358273c7-a9a1-8164-8981-f2ac7807a13b",
    sql="SELECT \"Title\" FROM data_source WHERE \"Title\" LIKE '%Lottner%' LIMIT 1"
)
exists = len(result) > 0
```

Master full content:
```python
# Fetch full page
page = fetch(page_url=kb_topic_url)
# Use page.content for analysis
```
