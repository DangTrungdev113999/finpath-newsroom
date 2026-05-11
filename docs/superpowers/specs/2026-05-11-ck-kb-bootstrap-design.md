# CK KB Bootstrap — Design Spec v1.0

**Date:** 2026-05-11
**Author:** Claude (drafted via brainstorming with user @dangtrungicloud)
**Status:** Draft — awaiting user review

## 1. Mục tiêu

Build **static knowledge base** cho ngành chứng khoán (CK). Khi pipeline V4.0 mở rộng từ MVP Bank sang CK (Phase sau), Master CK skill có local KB chứa **framework + mechanism + case study + threshold + pitfalls + regulatory** (kiến thức tĩnh không đổi theo quý) để query.

**Nguyên tắc cốt lõi (v1.2):** KB chỉ chứa kiến thức **tĩnh dài hạn**. Data động (thị phần Q[X]/[Y], dư nợ ký quỹ Q[X], BCTC quarter cụ thể) → Master tự fetch realtime qua **Finpath API** (BCTC + events + news cho mọi ticker) hoặc **web_search** (CK-specific data API không có). Lý do:
- Sau 3 tháng số dynamic stale → KB hoá thông tin sai
- Master skill đã có web_search + Finpath API tool → realtime accurate hơn
- KB không phình theo quarter (không cần update mỗi 3 tháng)
- KB framework dùng chung cho 5 mã universe (Master tự match ticker với framework)

## 2. Scope

### In scope (deliverable trong spec này — v1.2 revised)

- **6 markdown KB** tại `kb/ck/frameworks/` — **pure static** (framework + mechanism + benchmark ranges + thresholds + pitfalls + case study lịch sử)
- **1 YAML static** tại `data/manual/ssc_circulars.yaml` — quy định UBCKNN (static archive)
- Update `.claude/skills/finpath-newsroom-master-ck/SKILL.md` — wire KB + ssc_circulars + **explicit auto-fallback**: Master query KB cho framework guidance → fetch realtime data qua Finpath API (BCTC/events/news) hoặc web_search (CK-specific như thị phần/dư nợ ký quỹ chi tiết)

### Dropped from v1.0 (per pivot v1.2 — pure static KB)

- ~~`data/manual/ck_targets.yaml`~~ — DYNAMIC (kế hoạch ĐHĐCĐ + actual quarter), Master web_search
- ~~`data/manual/ck_market_share.yaml`~~ — DYNAMIC (HOSE/HNX công bố quarter), Master web_search
- ~~`data/manual/ck_margin_outstanding.yaml`~~ — DYNAMIC (BCTC quarter), Master Finpath API + web_search

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

## 4. File layout (v1.2 revised)

```
kb/ck/
└── frameworks/
    ├── ck-industry-master-reference.md      # 6 lớp mental model — anchor cho master skill (STATIC)
    ├── ck-margin-cycle.md                   # cho vay ký quỹ, trần 200% SSC, cycle lãi suất (STATIC)
    ├── ck-brokerage-marketshare.md          # thị phần HOSE/HNX, fee compression (STATIC)
    ├── ck-ib-revenue-volatility.md          # ngân hàng đầu tư (bảo lãnh + tư vấn + TPDN) (STATIC)
    ├── ck-proprietary-trading.md            # tự doanh, mark-to-market (STATIC)
    └── ck-liquidity-sensitivity.md          # earnings beta theo thanh khoản (STATIC)

data/manual/
└── ssc_circulars.yaml                       # quy định UBCKNN (STATIC archive)
```

Tổng: **6 markdown + 1 YAML = 7 file mới** + 1 file edit (`finpath-newsroom-master-ck/SKILL.md`).

## 5. Markdown structure (per file — v1.2 PURE STATIC)

### Frontmatter (Notion-free)

```yaml
---
category: frameworks
title: "CK-<Name>"
last_updated: 2026-05-11
---
```

### Body — pure static sections

1. **Khái niệm & cơ chế (Concept)** — định nghĩa + cơ chế. Tiếng Việt thuần (mapping cho vay ký quỹ, công ty CK, ngân hàng đầu tư, tài sản quản lý, tự doanh).
2. **Quy định pháp lý + threshold cứng** — SSC/UBCKNN circulars + hard caps + warning thresholds (vd: trần 200%, cảnh báo 150%). STATIC.
3. **Benchmark dài hạn (ranges)** — KHÔNG per-ticker per-quarter. Chỉ ranges historical (vd: "thị phần Top 10 HOSE: top 3 = 11-17%, mid 4-7 = 5-10%, bottom 8-10 = 3-5%"). Master CK dùng để sanity-check số fetch về.
4. **Case study lịch sử + chu kỳ** — sự kiện đã xảy ra (vd 2018 NHNN siết ký quỹ, 2020-2021 COVID rally, 2022 khủng hoảng TPDN). STATIC.
5. **Bẫy khi đọc số/định nghĩa** — pitfalls phổ biến (vd: nhầm vốn điều lệ với VCSH, nhầm doanh thu môi giới gross/net). STATIC.
6. **5 câu hỏi cho Master agent** — guidance khi Master viết tin về topic này. STATIC.
7. **Realtime data fetch guidance** — hướng dẫn Master cụ thể: data nào dùng Finpath API (`get_income_statement`, `get_balance_sheet`, `get_cashflow`, `get_events`, `get_news`), data nào web_search (vd: thị phần HOSE quarter X, dư nợ ký quỹ chi tiết). KHÔNG hard-code numbers.
8. **Cross-link** — relative path đến framework CK khác.
9. **Source log** — web URLs background research + dates. KHÔNG Notion link.
10. **Phần suy luận (cần verify)** — H2 riêng, inference của agent cần verify thêm.

**KHÔNG có section "Anchor data Q[X]/[Y]" với per-ticker numbers**. Đã DROP per pivot v1.2.

### Master reference file đặc biệt (`ck-industry-master-reference.md`)

Cấu trúc 6 lớp giống `bank-industry-master-reference.md`:

- **Lớp 1: Hiểu ngành** — 4 mảng doanh thu (môi giới + margin + IB + tự doanh) + UBCKNN kiểm soát (TT 121/2020 trần dư nợ ký quỹ 200%, công bố thông tin TT 96/2020).
- **Lớp 2: Đọc số** — metrics tier 1/2/3 (thị phần + dư nợ ký quỹ tier 1; ROE + biên lợi nhuận tier 2; CAR/RWA tier 3) + bẫy BCTC.
- **Lớp 3: Hiểu chu kỳ** — CK gắn với chu kỳ lãi suất + thanh khoản. Cross-link sang 5 deep dives bằng relative path: `[CK-Margin-cycle](./ck-margin-cycle.md)`, etc.
- **Lớp 4: Per-ticker structural positioning** — 5 mã universe (SSI/VND/HCM/VCI/SHS), mỗi mã 1-2 paragraph compact mô tả **positioning STRUCTURAL** (vd: "VPS = leader khách lẻ trực tuyến mô hình miễn phí giao dịch + margin"; "HCM = mạnh khối ngoại + IB tổ chức"). KHÔNG quarterly numbers. **Inline trong file master, KHÔNG tách file thứ 7.** File master target ≤ 12 KB.
- **Lớp 5: Định giá** — P/B vs P/E thận trọng cho CK (earnings volatility cao → P/E ít tin cậy hơn ngân hàng).
- **Lớp 6: Case study lịch sử** — 2018 NHNN siết ký quỹ / 2020 COVID rally / 2022 khủng hoảng TPDN / 2023-2024 phục hồi / 2025-2026 fee compression.

## 6. YAML structure (v1.2 — chỉ 1 file static)

Per pivot v1.2: chỉ giữ **1 YAML static** = `ssc_circulars.yaml`. 3 YAML dynamic (`ck_targets`, `ck_market_share`, `ck_margin_outstanding`) DROPPED — Master fetch realtime.

### `ssc_circulars.yaml` — quy định UBCKNN/SSC (STATIC archive)

Format theo Bank `nhnn_circulars.yaml`:

```yaml
- title: "Thông tư 121/2020/TT-BTC"
  effective_date: 2021-01-01
  affected_topics: ["Tỷ lệ an toàn vốn khả dụng", "Margin lending"]
  summary: "Quy định trần dư nợ ký quỹ 200% vốn chủ (Điều 28). Cảnh báo nội bộ broker khi vượt 150%."
  url: "https://thuvienphapluat.vn/van-ban/Doanh-nghiep/Thong-tu-121-2020-TT-BTC..."

- title: "Thông tư 96/2020/TT-BTC"
  effective_date: 2021-01-01
  affected_topics: ["Công bố thông tin"]
  summary: "Quy định công bố thông tin định kỳ + bất thường cho CTCK + công ty đại chúng."
  url: "..."

- title: "Thông tư 134/2020/TT-BTC"
  effective_date: 2021-01-01
  affected_topics: ["Hoạt động CTCK"]
  summary: "Quy định hoạt động kinh doanh chứng khoán của CTCK + tỷ lệ giới hạn."
  url: "..."

- title: "Nghị định 65/2022/NĐ-CP"
  effective_date: 2022-09-16
  affected_topics: ["Phát hành TPDN", "IB revenue"]
  summary: "Sửa đổi NĐ 153/2020 về phát hành TPDN — tăng yêu cầu xếp hạng tín nhiệm. Tác động giảm doanh thu IB CTCK."
  url: "..."

- title: "Quyết định 87/QĐ-UBCK 2017"
  effective_date: 2017-01-01
  affected_topics: ["Margin lending", "Risk management"]
  summary: "Quy định về tỷ lệ vay/cho vay ký quỹ + quy trình giám sát."
  url: "..."
```

Implementation: 5-7 thông tư key, 1 row mỗi thông tư.

## 7. SKILL.md updates (`.claude/skills/finpath-newsroom-master-ck/SKILL.md`)

4 thay đổi cụ thể (v1.2 revised):

### (a) Wording — clarify data source priority

Hiện tại line 18-20 và line 129 ghi "Phase 1 chưa có DB Notion riêng. Master CK V2.4 dùng web_search + Live API làm primary source".

Thay thành:
> "Master CK query data theo thứ tự: (1) local KB `kb/ck/frameworks/` cho framework + mechanism + threshold + case study + pitfalls (kiến thức tĩnh); (2) `data/manual/ssc_circulars.yaml` cho regulatory archive; (3) **Finpath API** cho BCTC/events/news (`get_income_statement`, `get_balance_sheet`, `get_cashflow`, `get_events`, `get_news` — work cho CK ticker); (4) **web_search** cho data CK-specific Finpath API không có (thị phần HOSE/HNX quarter cụ thể, dư nợ ký quỹ chi tiết, cấu trúc tự doanh)."

### (b) Add workflow step query KB

Thêm step mới vào workflow (sau Step "Pull memory", trước Finpath API):

```python
# Step query KB CK (static framework guidance)
from lib.kb_loader import KBLoader
loader = KBLoader('kb/ck/')
results = loader.search([<keywords from deep_question>])
# top match: loader.load_topic('<best_path>')
# KB cho framework + mechanism + threshold + case study — KHÔNG có per-ticker per-quarter numbers
```

### (c) Add workflow step query SSC circulars

Thêm step query 1 YAML static:

```python
# Step query regulatory archive
import yaml
with open('data/manual/ssc_circulars.yaml') as f: circulars = yaml.safe_load(f)
# filter by affected_topics (vd: "Margin lending", "Phát hành TPDN")
```

### (d) Add explicit auto-fallback guidance — Master MUST chain data sources

Thêm section mới `## Data fetching protocol — auto-fallback`:

```markdown
Khi viết bài, Master CK phải chain data sources theo thứ tự, KHÔNG skip:

1. **Local KB** (`kb/ck/frameworks/*.md`) — luôn query đầu để có framework + threshold + pitfall guidance.
2. **SSC circulars** (`data/manual/ssc_circulars.yaml`) — query khi đề cập regulatory.
3. **Finpath API** — fetch realtime BCTC + events:
   - `get_income_statement(ticker)` — P&L quarter/year
   - `get_balance_sheet(ticker)` — bảng cân đối (lấy VCSH, dư nợ ký quỹ nếu có dòng riêng)
   - `get_cashflow(ticker)` — luồng tiền
   - `get_events(ticker)` — DHCD + sự kiện
   - `get_news(ticker)` — tin liên quan
   - **KHÔNG dùng** `get_bank_ratios(ticker)` (Bank-only).
4. **Web_search** — fallback khi 1-3 thiếu, ESPECIALLY:
   - Thị phần môi giới HOSE/HNX quarter cụ thể (HOSE/HNX công bố, KHÔNG có trong API)
   - Dư nợ ký quỹ chi tiết per CTCK quarter (BCTC bổ sung, KHÔNG luôn có trong balance sheet)
   - Cấu trúc danh mục tự doanh per CTCK
   - Doanh thu per mảng (môi giới / margin / IB / tự doanh) breakdown
   - Lãi suất margin quote real-time
   - Thị phần fee compression dynamics

KHÔNG bịa số khi data động không có. Nếu sau cả 4 step vẫn không có data → reject với `master_decision: reject_no_data`.
```

### (e) Update References section

Thêm 6 KB CK markdown links + 1 YAML link trong section `## References` ở cuối SKILL.md (giữ 5 reference cũ về format/insight/jargon).

## 8. Implementation order (v1.2 revised)

Atomic commits, độc lập, có thể review riêng:

1. **Commits 1-2 — Tasks 1+2 ALREADY DONE** (`ck-margin-cycle.md` + `ck-brokerage-marketshare.md`). Có dynamic anchor section — **cần refactor xóa Q1/2026 per-ticker** + thay benchmark dài hạn ranges.
2. **Commit 3 — Refactor Tasks 1+2** xóa dynamic, thay static benchmark ranges.
3. **Commits 4-7 — KB Tasks 3-6** (`ck-ib-revenue-volatility.md`, `ck-proprietary-trading.md`, `ck-liquidity-sensitivity.md`, `ck-industry-master-reference.md`) với pure-static pattern v1.2.
4. **Commit 8 — Task 10** (`data/manual/ssc_circulars.yaml`).
5. **Commit 9 — Task 11** (SKILL.md wire KB + circulars + auto-fallback guidance).

Mỗi commit message follow project convention (concise Vietnamese, why-focused).

## 9. Validation (manual smoke check — v1.2)

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

### Pure-static check (v1.2)

Verify KB markdown KHÔNG còn per-ticker per-quarter snapshot:

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -rn "Q1/2026\|Q2/2026\|Q3/2026" kb/ck/ | grep -v "case study\|2018\|2020\|2021\|2022\|2023\|2024\|2025"
```

**Expected:** ≤5 hits (Q1/2026 chỉ trong sourced URLs ngày verified). KHÔNG trong narrative tables.

### YAML smoke (chỉ ssc_circulars)
```bash
uv run python -c "
import yaml
with open('data/manual/ssc_circulars.yaml') as f:
    data = yaml.safe_load(f)
print(f'ssc_circulars: {len(data)} rows')
for r in data:
    print(f'  {r[\"title\"]} — {r[\"effective_date\"]}')
"
```

**Expected:** 5-7 rows (TT 121/2020, TT 96/2020, TT 134/2020, TT 65/2022, NĐ 65/2022, QĐ 87/2017, ...).

### SKILL.md smoke (visual)
- Verify section `## Data fetching protocol — auto-fallback` exists
- Verify mention 4 sources (KB → ssc_circulars → Finpath API → web_search)
- Verify References section có 6 KB markdown links + 1 YAML

## 10. Open questions / followup

- **CK SKILL.md V4.0 bump** — sẽ làm khi pipeline V4.0 expand. Track: cần update brief schema (`deep_question_options` array thay vì `deep_question` đơn) + 5 quality gates V4.0 + body pattern V4.0.
- **YAML data accuracy** — bootstrap dùng mock stub (last_verified: unknown). Khi user trigger first CK article, Master CK sẽ thấy freshness warning → web_search refresh và update YAML thật.
- **HCM/VCI/VND/SHS positioning trong Lớp 4 master reference** — bootstrap dùng public knowledge. Phase sau có thể enhance bằng broker reports nếu cần.
- **Nếu Notion 6 trang con quá sơ sài** → ghi vào commit message + spec changelog, fill bằng web research.

## Changelog

- **v1.2 (2026-05-11):** **PIVOT pure-static KB.** User feedback giữa Task 2 + 3: KB phải chứa kiến thức TĨNH (framework/mechanism/case study/threshold/pitfalls/regulatory) — KHÔNG per-ticker per-quarter snapshot. Lý do: data động stale 3 tháng, Master đã có web_search + Finpath API tool, KB phình vô ích.
  - DROP 3 dynamic YAML (`ck_targets`, `ck_market_share`, `ck_margin_outstanding`).
  - REFACTOR Task 1+2 markdown: xóa "Dữ liệu neo Q1/2026" section, thay benchmark dài hạn ranges + threshold static.
  - Lớp 4 master reference per-ticker: chỉ structural positioning (NOT quarterly state).
  - SKILL.md add `## Data fetching protocol — auto-fallback` (KB → ssc_circulars → Finpath API → web_search).
- **v1.1 (2026-05-11):** Fix SSC trần 1.7× → **200% (2.0×)** per Điều 28 TT 121/2020 + Quyết định 87/QĐ-UBCK 2017 (web research từ ssc.gov.vn + thuvienphapluat.vn). Discovered during Task 1 (margin cycle) implementation.
- **v1.0 (2026-05-11):** Initial spec, drafted via brainstorming với user. Approved structure: 6 markdown + 4 YAML + SKILL.md update. Content sourcing = read Notion 1x (output Notion-free).
