# CK KB Bootstrap — Design Spec v1.0

**Date:** 2026-05-11
**Author:** Claude (drafted via brainstorming with user @dangtrungicloud)
**Status:** Draft — awaiting user review

## 1. Mục tiêu

Build knowledge base cho ngành chứng khoán (CK) song song với KB Bank đã có. Khi pipeline V4.0 mở rộng từ MVP Bank sang CK (Phase sau), Master CK skill có local KB + YAML để query trước khi web_search — giảm latency, giảm fabrication risk, và đảm bảo Master CK reach mức độ "chuyên gia 10+ năm" như Master Bank hiện tại.

## 2. Scope

### In scope (deliverable trong spec này)

- 6 markdown KB tại `kb/ck/frameworks/`
- 4 YAML manual data tại `data/manual/`
- Update `.claude/skills/finpath-newsroom-master-ck/SKILL.md` — wire KB + YAML + sửa wording "Finpath API" → "web_search"

### Out of scope (defer / không động)

- **`.claude/agents/newsroom-master-ck.md`** — chưa tồn tại, sẽ tạo khi pipeline V4.0 expand từ Bank sang CK (Phase riêng).
- **Wire CK route vào `newsroom-pipeline.md`** — Phase riêng (Bank-only MVP đang chạy).
- **Bump CK SKILL.md lên V4.0 parity** (deep_question_options array, 5 quality gates V4.0, body pattern V4.0). Hiện tại SKILL.md là V2.4/V3.6 mixed; KB này build now để Phase sau dùng. Việc bump version là Phase riêng.
- **`lib/kb_ingest.py` + `lib/notion_fetch.py`** — Bank-specific bootstrap đã xong. Leave alone (working code, không xóa, không refactor cho CK).
- **Tests automated** — chỉ smoke check manual (xem § 9).
- **Notion publish output** — đã defer per CLAUDE.md, không động.

## 3. Content sourcing strategy

**One-shot read Notion → output Notion-free.** Cụ thể:

- Đọc 6 Notion child pages (`CK-Industry-Master-Reference` + 5 frameworks) **1 lần** trong implementation session làm research baseline.
- **Enhance** với web research (case study lịch sử CK VN: 2018 NHNN siết ký quỹ, 2020 COVID rally, 2022 khủng hoảng TPDN, 2023-2024 phục hồi, 2025-2026 fee compression) + jargon mapping Việt-Anh.
- Output markdown **KHÔNG có `notion_page_id` / `source_url` Notion** trong frontmatter — chỉ `category` + `title` + `last_updated`.
- **KHÔNG runtime call Notion** từ Master CK skill / agent.

Nếu Notion có chỗ thiếu / sơ sài → fill bằng web research, ghi rõ source URL trong section "Source log" của markdown body.

## 4. File layout

```
kb/ck/
└── frameworks/
    ├── ck-industry-master-reference.md      # 6 lớp mental model — anchor cho master skill
    ├── ck-margin-cycle.md                   # cho vay ký quỹ, trần 200% SSC, cycle lãi suất
    ├── ck-brokerage-marketshare.md          # thị phần HOSE/HNX, fee compression
    ├── ck-ib-revenue-volatility.md          # ngân hàng đầu tư (bảo lãnh + tư vấn + TPDN)
    ├── ck-proprietary-trading.md            # tự doanh, mark-to-market
    └── ck-liquidity-sensitivity.md          # earnings beta theo thanh khoản

data/manual/
├── ck_targets.yaml                          # ĐHĐCĐ kế hoạch vs actual Q1 (5 mã)
├── ck_market_share.yaml                     # thị phần môi giới HOSE/HNX per quarter
├── ck_margin_outstanding.yaml               # dư nợ ký quỹ + headroom 200% SSC
└── ssc_circulars.yaml                       # quy định UBCKNN
```

Tổng: **6 markdown + 4 YAML = 10 file mới** + 1 file edit (`finpath-newsroom-master-ck/SKILL.md`).

## 5. Markdown structure (per file)

### Frontmatter (Notion-free)

```yaml
---
category: frameworks
title: "CK-<Name>"
last_updated: 2026-05-11
---
```

### Body — 4-section pattern (theo Notion convention user set)

1. **Concept** — định nghĩa + cơ chế. Tiếng Việt thuần (mapping margin → cho vay ký quỹ, broker → công ty CK, IB → ngân hàng đầu tư, AUM → tài sản quản lý, prop trading → tự doanh).
2. **Anchor data** — benchmark Q1/2026 cho 5 mã universe (SSI/VND/HCM/VCI/SHS), numbers cụ thể có thể quote khi viết bài.
3. **Pitfalls khi đọc** — bẫy phổ biến (vd: nhầm doanh thu môi giới với phí thuần; nhầm margin gross vs net; nhầm tự doanh tài sản với tự doanh tự kinh doanh).
4. **Source log** — nguồn (web URLs + ngày verified). KHÔNG ghi Notion link.

### Master reference file đặc biệt (`ck-industry-master-reference.md`)

Cấu trúc 6 lớp giống `bank-industry-master-reference.md`:

- **Lớp 1: Hiểu ngành** — 4 mảng doanh thu (môi giới + margin + IB + tự doanh) + UBCKNN kiểm soát (TT 121/2020 trần dư nợ ký quỹ 200%, công bố thông tin TT 96/2020).
- **Lớp 2: Đọc số** — metrics tier 1/2/3 (thị phần + dư nợ ký quỹ tier 1; ROE + biên lợi nhuận tier 2; CAR/RWA tier 3) + bẫy BCTC.
- **Lớp 3: Hiểu chu kỳ** — CK gắn với chu kỳ lãi suất + thanh khoản. Cross-link sang 5 deep dives bằng relative path: `[CK-Margin-cycle](./ck-margin-cycle.md)`, etc.
- **Lớp 4: Per-ticker** — 5 mã universe (SSI/VND/HCM/VCI/SHS), mỗi mã 1-2 paragraph compact (positioning + edge + risk). **Inline trong file master, KHÔNG tách file thứ 7.** File master target ≤ 12 KB.
- **Lớp 5: Định giá** — P/B vs P/E thận trọng cho CK (earnings volatility cao → P/E ít tin cậy hơn ngân hàng).
- **Lớp 6: Case study lịch sử** — 2018 NHNN siết ký quỹ / 2020 COVID rally / 2022 khủng hoảng TPDN / 2023-2024 phục hồi / 2025-2026 fee compression.

## 6. YAML structure (mock stub)

Mỗi YAML mock 5 row (1/ticker), thêm metadata `last_verified` + `verified_by` + `source_url` để consistent với Bank pattern (Master CK gọi `kb_loader.freshness_warning()` để biết khi nào cần web_search refresh).

### `ck_targets.yaml` — kế hoạch ĐHĐCĐ vs thực tế

```yaml
- ticker: SSI
  year: 2026
  target_lntt_ty: 4000               # mục tiêu LNTT cả năm (tỷ đồng)
  target_revenue_ty: 9500
  actual_lntt_q1_ty: 850
  actual_revenue_q1_ty: 2100
  source: "Nghị quyết ĐHĐCĐ 20/4/2026"
  source_url: "https://example.com/ssi-dhdcd-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"
```

### `ck_market_share.yaml` — thị phần môi giới HOSE/HNX

```yaml
- ticker: SSI
  exchange: HOSE
  quarter: 2026Q1
  market_share_pct: 9.5
  rank: 2
  prev_quarter_pct: 10.2             # so quý trước, để tính delta
  source: "HOSE công bố thị phần Q1/2026"
  source_url: "https://example.com/hose-marketshare-q1-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"
```

### `ck_margin_outstanding.yaml` — dư nợ ký quỹ + headroom 200%

**Lưu ý:** SSC trần thực tế là **200% (2.0×) vốn chủ sở hữu** per Điều 28 TT 121/2020/TT-BTC + Quyết định 87/QĐ-UBCK 2017. (Spec v1.0 draft ghi nhầm 1.7× — fix v1.1.)

```yaml
- ticker: SSI
  quarter: 2026Q1
  margin_outstanding_ty: 36928       # dư nợ ký quỹ cuối quý (tỷ đồng) — số thật từ BCTC
  equity_ty: 38531                   # vốn chủ — số thật từ BCTC
  ratio: 0.96                        # = 36928/38531
  cap_ratio: 2.00                    # SSC trần 200%
  headroom_to_cap_ty: 40134          # = (2.0 × 38531) - 36928
  source: "BCTC Q1/2026 SSI"
  source_url: "https://example.com/ssi-bctc-q1-2026"
  last_verified: "2026-05-11"
  verified_by: "bootstrap web research"
```

### `ssc_circulars.yaml` — quy định UBCKNN

```yaml
- title: "Thông tư 121/2020/TT-BTC"
  effective_date: 2021-01-01
  affected_topics: ["Tỷ lệ an toàn vốn khả dụng", "Margin lending"]
  summary: "Quy định trần dư nợ ký quỹ 200% vốn chủ (Điều 28). Cảnh báo nội bộ broker khi vượt 150%."
  url: "https://example.com/ssc-tt121-2020"

- title: "Thông tư 96/2020/TT-BTC"
  effective_date: 2021-01-01
  affected_topics: ["Công bố thông tin"]
  summary: "Quy định công bố thông tin định kỳ + bất thường cho CTCK + công ty đại chúng."
  url: "https://example.com/ssc-tt96-2020"
```

(Spec chỉ show 1-2 row mẫu mỗi YAML — implementation sẽ fill 5 row/ticker cho 3 YAML đầu, 3-5 thông tư cho `ssc_circulars`.)

## 7. SKILL.md updates (`.claude/skills/finpath-newsroom-master-ck/SKILL.md`)

3 thay đổi cụ thể:

### (a) Wording fix — "Finpath API" → "web_search"

Hiện tại line 18-20 và line 129:
> "Phase 1 chưa có DB Notion riêng. Master CK V2.4 dùng web_search + Live API làm primary source"

Thay thành:
> "Master CK query local KB (`kb/ck/`) + YAML (`data/manual/ck_*.yaml`) + `ssc_circulars.yaml` trước. Web_search bổ sung khi local thiếu data. Finpath API chưa có CK data — KHÔNG query."

### (b) Add workflow steps query KB + YAML

Thêm 2 step mới vào workflow (sau Step "Pull memory", trước "web_search"), copy pattern từ Master Bank SKILL.md line 4-5 + agent file line 87-88, sửa path:

```python
# Step query KB CK
from lib.kb_loader import KBLoader
loader = KBLoader('kb/ck/')
results = loader.search([<keywords from deep_question>])
# top match: loader.load_topic('<best_path>')
```

```python
# Step query manual YAML
import yaml
with open('data/manual/ck_targets.yaml') as f:        targets = yaml.safe_load(f)
with open('data/manual/ck_market_share.yaml') as f:   shares = yaml.safe_load(f)
with open('data/manual/ck_margin_outstanding.yaml') as f: margin = yaml.safe_load(f)
with open('data/manual/ssc_circulars.yaml') as f:     circulars = yaml.safe_load(f)
# filter by ticker / year / quarter / topic
```

### (c) Update References section

Thêm reference vào KB CK markdown files trong section `## References` ở cuối SKILL.md (giữ 5 reference cũ).

## 8. Implementation order

Atomic commits, độc lập, có thể review riêng:

1. **Commit 1 — KB markdown** (`kb/ck/frameworks/` + 6 file)
2. **Commit 2 — YAML manual** (`data/manual/ck_*.yaml` + `ssc_circulars.yaml`)
3. **Commit 3 — SKILL.md update** (wire KB + YAML + wording fix)

Mỗi commit message follow project convention (concise Vietnamese, why-focused).

## 9. Validation (manual smoke check)

### KB loader smoke
```bash
uv run python -c "
from lib.kb_loader import KBLoader
loader = KBLoader('kb/ck/')
print('FILES:', len(loader._all_files()))
print('SEARCH ký quỹ:', [r['title'] for r in loader.search(['ký quỹ'])])
print('SEARCH ngân hàng đầu tư:', [r['title'] for r in loader.search(['ngân hàng đầu tư'])])
print('SEARCH tự doanh:', [r['title'] for r in loader.search(['tự doanh'])])
"
```

**Expected:**
- `FILES: 6`
- search "ký quỹ" → match `CK-Margin-cycle` + `CK-Industry-Master-Reference`
- search "ngân hàng đầu tư" → match `CK-IB-revenue-volatility`
- search "tự doanh" → match `CK-Proprietary-trading`

### YAML smoke
```bash
uv run python -c "
import yaml
for fname in ['ck_targets', 'ck_market_share', 'ck_margin_outstanding', 'ssc_circulars']:
    with open(f'data/manual/{fname}.yaml') as f:
        data = yaml.safe_load(f)
    print(f'{fname}: {len(data)} rows')
"
```

**Expected:** 4 file load OK, 5 rows mỗi file (3 file đầu), 3-5 rows `ssc_circulars`.

### SKILL.md smoke (visual)
- Open `.claude/skills/finpath-newsroom-master-ck/SKILL.md`
- Verify wording "Finpath API" đã thay → "web_search"
- Verify 2 code block KB + YAML đã add vào workflow
- Verify References section có 6 KB markdown links

## 10. Open questions / followup

- **CK SKILL.md V4.0 bump** — sẽ làm khi pipeline V4.0 expand. Track: cần update brief schema (`deep_question_options` array thay vì `deep_question` đơn) + 5 quality gates V4.0 + body pattern V4.0.
- **YAML data accuracy** — bootstrap dùng mock stub (last_verified: unknown). Khi user trigger first CK article, Master CK sẽ thấy freshness warning → web_search refresh và update YAML thật.
- **HCM/VCI/VND/SHS positioning trong Lớp 4 master reference** — bootstrap dùng public knowledge. Phase sau có thể enhance bằng broker reports nếu cần.
- **Nếu Notion 6 trang con quá sơ sài** → ghi vào commit message + spec changelog, fill bằng web research.

## Changelog

- **v1.1 (2026-05-11):** Fix SSC trần 1.7× → **200% (2.0×)** per Điều 28 TT 121/2020 + Quyết định 87/QĐ-UBCK 2017 (web research từ ssc.gov.vn + thuvienphapluat.vn). Discovered during Task 1 (margin cycle) implementation.
- **v1.0 (2026-05-11):** Initial spec, drafted via brainstorming với user. Approved structure: 6 markdown + 4 YAML + SKILL.md update. Content sourcing = read Notion 1x (output Notion-free).
