# CK KB Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build local knowledge base (6 markdown framework files) + manual quantitative data (4 YAML files) cho ngành chứng khoán VN, song song với KB Bank đã có. Update Master CK skill để query KB + YAML trước khi web_search.

**Architecture:** Hand-craft 6 markdown từ Notion child pages (read 1 lần, output Notion-free) + 4 YAML mock stub cho 5 mã universe (SSI/VND/HCM/VCI/SHS). Reuse `lib/kb_loader.py` (đã generic — accept arbitrary root path). Update `.claude/skills/finpath-newsroom-master-ck/SKILL.md` wire KB + YAML.

**Tech Stack:** Python 3 / `lib/kb_loader.py` / PyYAML / Markdown. Reference Bank pattern: `kb/bank/frameworks/` + `data/manual/{targets,credit_room,nhnn_circulars}.yaml` + `.claude/skills/finpath-newsroom-master-bank/SKILL.md`.

**Spec:** `docs/superpowers/specs/2026-05-11-ck-kb-bootstrap-design.md`

---

## File Structure

**Will create (10 file mới):**

```
kb/ck/frameworks/
├── ck-margin-cycle.md                  # Task 1
├── ck-brokerage-marketshare.md         # Task 2
├── ck-ib-revenue-volatility.md         # Task 3
├── ck-proprietary-trading.md           # Task 4
├── ck-liquidity-sensitivity.md         # Task 5
└── ck-industry-master-reference.md     # Task 6 (last — cross-link 5 deep dives)

data/manual/
├── ck_targets.yaml                     # Task 7
├── ck_market_share.yaml                # Task 8
├── ck_margin_outstanding.yaml          # Task 9
└── ssc_circulars.yaml                  # Task 10
```

**Will modify (1 file):**

```
.claude/skills/finpath-newsroom-master-ck/SKILL.md   # Task 11
```

**Will NOT touch:**
- `lib/kb_loader.py` — already generic (accepts root path)
- `lib/kb_ingest.py` / `lib/notion_fetch.py` — Bank-specific, leave alone
- `.claude/agents/` — no agent file for CK yet (Phase sau)
- `kb/bank/` — Bank KB unchanged

---

## Notion source pages (read-only research material)

Fetch via Notion MCP `mcp__notion__API-get-block-children` (recursive nếu `has_children: true`):

| Notion Child Page Title | Notion block_id | Output Markdown |
|---|---|---|
| `CK-Industry-Master-Reference` | `35a273c7-a9a1-816f-8fab-c24290aecd71` | `ck-industry-master-reference.md` |
| `CK-Margin-cycle` | `35a273c7-a9a1-815d-a457-c663117d9cfb` | `ck-margin-cycle.md` |
| `CK-Brokerage-marketshare` | `35a273c7-a9a1-81e0-97c5-dabfae3298d7` | `ck-brokerage-marketshare.md` |
| `CK-IB-revenue-volatility` | `35a273c7-a9a1-81fc-a650-e6d6d1ef5d44` | `ck-ib-revenue-volatility.md` |
| `CK-Proprietary-trading` | `35a273c7-a9a1-81d9-9348-f0a3bc7d40ef` | `ck-proprietary-trading.md` |
| `CK-Liquidity-sensitivity` | `35a273c7-a9a1-8110-8661-dfc576c7baf7` | `ck-liquidity-sensitivity.md` |

Output frontmatter Notion-free (no `notion_page_id`, no `source_url` Notion).

---

## Common content pattern (apply to Tasks 1-5 deep dives)

Mỗi deep dive markdown follow 4-section pattern (per spec § 5):

```markdown
---
category: frameworks
title: "CK-<Name>"
last_updated: 2026-05-11
---

[1 đoạn intro 30-50 từ — what is this framework + why it matters cho Master CK skill]

## Concept

[Định nghĩa + cơ chế. Tiếng Việt thuần. Map jargon Anh → Việt (margin → cho vay ký quỹ, broker → công ty CK, IB → ngân hàng đầu tư, AUM → tài sản quản lý, prop trading → tự doanh).]

## Anchor data (Q1/2026 reference, 5 mã universe)

[Benchmark numbers cụ thể cho SSI/VND/HCM/VCI/SHS — Master CK quote khi viết bài.
Format: bảng hoặc bullet "Ticker — metric — value".]

## Pitfalls khi đọc

[3-5 bẫy phổ biến khi đọc số/định nghĩa, mỗi bẫy 1-2 câu.
Vd: "Nhầm doanh thu môi giới gross với phí thuần (đã trừ chi phí trả cho bên thứ ba)".]

## Source log

[2-5 nguồn web (URL + ngày verified) — KHÔNG ghi Notion.
Format: `- [Title](url) — verified 2026-05-11`]
```

Mục tiêu kích thước: **7-11 KB mỗi file** (parity với Bank deep dives).

---

## Task 1: Margin cycle deep dive

**Files:**
- Create: `kb/ck/frameworks/ck-margin-cycle.md`

**Notion source:** block_id `35a273c7-a9a1-815d-a457-c663117d9cfb`

- [ ] **Step 1: Tạo thư mục `kb/ck/frameworks/`**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && mkdir -p kb/ck/frameworks
```

Expected: directory tạo, không lỗi.

- [ ] **Step 2: Fetch Notion CK-Margin-cycle child page (recursive)**

Tool: `mcp__notion__API-get-block-children` với `block_id="35a273c7-a9a1-815d-a457-c663117d9cfb"`. Nếu block con có `has_children: true`, fetch tiếp recursive đến hết.

Lưu nội dung extracted vào memory để hand-craft markdown step tiếp.

- [ ] **Step 3: Web research enhancement (data Q1/2026 + jargon mapping)**

Web search bổ sung nếu Notion thiếu:
- Trần dư nợ ký quỹ SSC (TT 121/2020 — 200% (2.0×) vốn chủ sở hữu)
- Q1/2026 dư nợ ký quỹ 5 mã CK universe (SSI/VND/HCM/VCI/SHS)
- Cycle 2018 NHNN siết ký quỹ (impact lên broker doanh thu)
- Lãi suất margin VN 2026 (broker quote 12-14%/năm điển hình)
- Mapping jargon: margin lending → cho vay ký quỹ, margin call → giải chấp, leverage → đòn bẩy, headroom → dư địa

Lưu URLs verified vào memory cho Source log section.

- [ ] **Step 4: Write `kb/ck/frameworks/ck-margin-cycle.md`**

Use Write tool. Content theo 4-section pattern (Concept / Anchor data / Pitfalls / Source log) per spec § 5. Frontmatter:

```yaml
---
category: frameworks
title: "CK-Margin-cycle"
last_updated: 2026-05-11
---
```

Body sections:
- **Concept**: định nghĩa cho vay ký quỹ + cơ chế trần 200% (2.0×) SSC + cycle theo lãi suất (LS giảm → margin demand tăng → doanh thu margin tăng; LS tăng → ngược lại).
- **Anchor data Q1/2026**: bảng dư nợ ký quỹ + tỷ lệ / vốn chủ + headroom 5 mã universe.
- **Pitfalls**: 3-5 bẫy (vd: nhầm dư nợ ký quỹ với cho vay tổng; nhầm doanh thu margin gross/net; nhầm trần 200% (2.0×) với 2.0× cũ; bỏ sót buffer cảnh báo 1.5×).
- **Source log**: URLs verified.

Target size 7-11 KB.

- [ ] **Step 5: Smoke check file loadable**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.kb_loader import KBLoader
loader = KBLoader('kb/ck/')
results = loader.search(['ký quỹ'])
print('FILES:', len(loader._all_files()))
print('MATCHES:', [r['title'] for r in results])
"
```

Expected: `FILES: 1`, `MATCHES: ['CK-Margin-cycle']`.

- [ ] **Step 6: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add kb/ck/frameworks/ck-margin-cycle.md && git commit -m "kb(ck): add margin cycle framework deep dive

Cho vay ký quỹ — trần 200% (2.0×) SSC, cycle theo lãi suất, anchor data
5 mã universe Q1/2026. Hand-craft từ Notion baseline + web research
2018 NHNN siết ký quỹ + 2020 COVID rally context.

Spec: docs/superpowers/specs/2026-05-11-ck-kb-bootstrap-design.md"
```

---

## Task 2: Brokerage market share deep dive

**Files:**
- Create: `kb/ck/frameworks/ck-brokerage-marketshare.md`

**Notion source:** block_id `35a273c7-a9a1-81e0-97c5-dabfae3298d7`

- [ ] **Step 1: Fetch Notion CK-Brokerage-marketshare child page (recursive)**

Tool: `mcp__notion__API-get-block-children` với `block_id="35a273c7-a9a1-81e0-97c5-dabfae3298d7"`. Recursive nếu có `has_children: true`.

- [ ] **Step 2: Web research enhancement**

- HOSE công bố Top 10 CTCK thị phần môi giới Q1/2026 (số % cụ thể)
- HNX Top 10 thị phần môi giới Q1/2026
- VPS soán ngôi SSI từ Q1/2024 (case study)
- Fee compression: phí môi giới VN giảm từ 0.15% (2018) → 0.10% (2024) → 0.07% retail online (2026)
- TCBS / DNSE zero-fee disruption 2024-2025

- [ ] **Step 3: Write `kb/ck/frameworks/ck-brokerage-marketshare.md`**

Use Write tool. Frontmatter:

```yaml
---
category: frameworks
title: "CK-Brokerage-marketshare"
last_updated: 2026-05-11
---
```

Sections:
- **Concept**: thị phần môi giới = (giá trị giao dịch khớp lệnh khách qua mã CTCK / tổng giá trị thị trường). Leading indicator phí năm sau.
- **Anchor data**: bảng Top 10 HOSE Q1/2026 (5 mã universe + VPS, TCBS, DNSE, MBS, MAS) + HNX Top 5.
- **Pitfalls**: nhầm thị phần khớp lệnh với thị phần thỏa thuận; nhầm thị phần HOSE với toàn thị trường; bẫy "thị phần lên ≠ doanh thu lên" khi fee compression mạnh.
- **Source log**: URLs HOSE/HNX công bố thị phần + bài báo VPS soán ngôi.

Target size 7-11 KB.

- [ ] **Step 4: Smoke check**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.kb_loader import KBLoader
loader = KBLoader('kb/ck/')
results = loader.search(['thị phần'])
print('MATCHES:', [r['title'] for r in results])
"
```

Expected: matches include `CK-Brokerage-marketshare`.

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add kb/ck/frameworks/ck-brokerage-marketshare.md && git commit -m "kb(ck): add brokerage market share framework

Thị phần HOSE/HNX leading indicator phí — anchor Top 10 Q1/2026,
case study VPS soán ngôi SSI 2024, fee compression 0.15% → 0.07%.

Spec: docs/superpowers/specs/2026-05-11-ck-kb-bootstrap-design.md"
```

---

## Task 3: IB revenue volatility deep dive

**Files:**
- Create: `kb/ck/frameworks/ck-ib-revenue-volatility.md`

**Notion source:** block_id `35a273c7-a9a1-81fc-a650-e6d6d1ef5d44`

- [ ] **Step 1: Fetch Notion CK-IB-revenue-volatility child page (recursive)**

- [ ] **Step 2: Web research enhancement**

- 3 mảng IB: bảo lãnh phát hành (cổ phiếu IPO + tăng vốn) + tư vấn M&A/cổ phần hóa + môi giới trái phiếu (TPDN)
- Khủng hoảng TPDN 2022 (Vạn Thịnh Phát + Tân Hoàng Minh) — broker tổn thất
- TT 65/2022 + Nghị định 65/2022/NĐ-CP — siết phát hành TPDN, tác động lên doanh thu IB
- Doanh thu IB chiếm % cấu trúc doanh thu 5 mã universe (typical 5-15%)
- Cycle 2020-2021 TPDN bùng nổ (1 triệu tỷ phát hành) → 2022 sụp → 2023-2024 phục hồi chậm

- [ ] **Step 3: Write `kb/ck/frameworks/ck-ib-revenue-volatility.md`**

Frontmatter:

```yaml
---
category: frameworks
title: "CK-IB-revenue-volatility"
last_updated: 2026-05-11
---
```

Sections:
- **Concept**: doanh thu ngân hàng đầu tư (IB) = bảo lãnh phát hành + tư vấn + môi giới TPDN. Volatility cao do depend cycle phát hành + M&A — tốt năm bull, sụp năm bear.
- **Anchor data**: cấu trúc doanh thu IB 5 mã Q1/2026 + so sánh 2021 peak vs 2023 trough.
- **Pitfalls**: nhầm doanh thu IB với phí môi giới; gộp self-deal vào IB; bỏ sót rủi ro guarantee TPDN khi broker đứng tên bảo lãnh.
- **Source log**: URLs.

Target size 7-11 KB.

- [ ] **Step 4: Smoke check**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.kb_loader import KBLoader
loader = KBLoader('kb/ck/')
results = loader.search(['ngân hàng đầu tư'])
print('MATCHES:', [r['title'] for r in results])
"
```

Expected: matches include `CK-IB-revenue-volatility`.

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add kb/ck/frameworks/ck-ib-revenue-volatility.md && git commit -m "kb(ck): add IB revenue volatility framework

Bảo lãnh + tư vấn + môi giới TPDN — cycle 2020-2026 (peak/trough),
khủng hoảng Vạn Thịnh Phát 2022, TT 65/2022 siết phát hành.

Spec: docs/superpowers/specs/2026-05-11-ck-kb-bootstrap-design.md"
```

---

## Task 4: Proprietary trading deep dive

**Files:**
- Create: `kb/ck/frameworks/ck-proprietary-trading.md`

**Notion source:** block_id `35a273c7-a9a1-81d9-9348-f0a3bc7d40ef`

- [ ] **Step 1: Fetch Notion CK-Proprietary-trading child page (recursive)**

- [ ] **Step 2: Web research enhancement**

- Cấu trúc danh mục tự doanh: cổ phiếu niêm yết (FVTPL/AFS) + trái phiếu chính phủ + TPDN + chứng chỉ quỹ + phái sinh
- Mark-to-market mỗi quý — earnings volatility cao
- Quy định IFRS 9 / VAS riêng cho FVTPL vs AFS
- 5 mã universe Q1/2026 cấu trúc tự doanh (% danh mục)
- Case 2022: SSI/VND tổn thất tự doanh do TPDN + cổ phiếu giảm
- Tier 1 capital + risk weight cho tự doanh

- [ ] **Step 3: Write `kb/ck/frameworks/ck-proprietary-trading.md`**

Frontmatter:

```yaml
---
category: frameworks
title: "CK-Proprietary-trading"
last_updated: 2026-05-11
---
```

Sections:
- **Concept**: tự doanh = CTCK dùng vốn riêng đầu tư cổ phiếu/trái phiếu, mark-to-market gây earnings volatility cao.
- **Anchor data**: cấu trúc danh mục tự doanh 5 mã Q1/2026 + case 2022 tổn thất.
- **Pitfalls**: nhầm tự doanh với môi giới ủy thác; bỏ sót mark-to-market impact; nhầm AFS với FVTPL (recognition khác nhau); chia tự doanh "kinh doanh" vs "đầu tư".
- **Source log**: URLs.

Target size 7-11 KB.

- [ ] **Step 4: Smoke check**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.kb_loader import KBLoader
loader = KBLoader('kb/ck/')
results = loader.search(['tự doanh'])
print('MATCHES:', [r['title'] for r in results])
"
```

Expected: matches include `CK-Proprietary-trading`.

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add kb/ck/frameworks/ck-proprietary-trading.md && git commit -m "kb(ck): add proprietary trading framework

Tự doanh CTCK — mark-to-market FVTPL/AFS, cấu trúc danh mục 5 mã
Q1/2026, case 2022 tổn thất TPDN + cổ phiếu giảm.

Spec: docs/superpowers/specs/2026-05-11-ck-kb-bootstrap-design.md"
```

---

## Task 5: Liquidity sensitivity deep dive

**Files:**
- Create: `kb/ck/frameworks/ck-liquidity-sensitivity.md`

**Notion source:** block_id `35a273c7-a9a1-8110-8661-dfc576c7baf7`

- [ ] **Step 1: Fetch Notion CK-Liquidity-sensitivity child page (recursive)**

- [ ] **Step 2: Web research enhancement**

- VN-Index thanh khoản trung bình ngày 2020-2026 (peak Q4/2021 ~36,000 tỷ → trough 2023 ~10,000 tỷ → 2026 mức bình thường ~20,000 tỷ)
- Earnings beta = doanh thu CTCK ↔ thanh khoản (cả 4 mảng đều positive correlation)
- Sensitivity per mảng: môi giới (linear), margin (lagged), IB (cycle-driven), tự doanh (P&L volatile)
- Decision rule: thanh khoản giảm 30% → doanh thu môi giới giảm tương đương; margin tổng dư nợ giảm chậm hơn (sticky)

- [ ] **Step 3: Write `kb/ck/frameworks/ck-liquidity-sensitivity.md`**

Frontmatter:

```yaml
---
category: frameworks
title: "CK-Liquidity-sensitivity"
last_updated: 2026-05-11
---
```

Sections:
- **Concept**: earnings CTCK gắn chặt thanh khoản thị trường — cross-cutting theme ảnh hưởng cả 4 mảng (môi giới, margin, IB, tự doanh).
- **Anchor data**: bảng thanh khoản trung bình ngày HOSE 2020-2026 + sensitivity per mảng (slope correlation).
- **Pitfalls**: nhầm thanh khoản khớp lệnh với thỏa thuận; gộp phái sinh vào spot; bỏ sót lag effect (margin chậm 1-2 quý); bỏ sót base effect khi thanh khoản recovery.
- **Source log**: URLs HOSE thanh khoản hàng tháng + báo cáo SSI Research.

Target size 7-11 KB.

- [ ] **Step 4: Smoke check**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.kb_loader import KBLoader
loader = KBLoader('kb/ck/')
results = loader.search(['thanh khoản'])
print('MATCHES:', [r['title'] for r in results])
"
```

Expected: matches include `CK-Liquidity-sensitivity`.

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add kb/ck/frameworks/ck-liquidity-sensitivity.md && git commit -m "kb(ck): add liquidity sensitivity framework

Earnings beta theo thanh khoản — cross-cutting theme 4 mảng,
HOSE thanh khoản 2020-2026, sensitivity per revenue stream.

Spec: docs/superpowers/specs/2026-05-11-ck-kb-bootstrap-design.md"
```

---

## Task 6: Master reference (cross-link 5 deep dives)

**Files:**
- Create: `kb/ck/frameworks/ck-industry-master-reference.md`

**Notion source:** block_id `35a273c7-a9a1-816f-8fab-c24290aecd71`

- [ ] **Step 1: Fetch Notion CK-Industry-Master-Reference child page (recursive)**

- [ ] **Step 2: Web research enhancement**

- 5 mã universe positioning (SSI = leader truyền thống, VND = aggressive growth, HCM = quality + foreign-friendly, VCI = high-margin niche, SHS = consumer-retail tilt)
- Case study lịch sử CK VN: 2018 NHNN siết ký quỹ + 2020 COVID rally + 2022 TPDN crisis + 2023-2024 phục hồi + 2025-2026 fee compression
- P/B vs P/E thận trọng cho CK (earnings volatility cao → P/E ít tin cậy hơn ngân hàng)
- ROE benchmark 5 mã Q1/2026

- [ ] **Step 3: Write `kb/ck/frameworks/ck-industry-master-reference.md`**

Frontmatter:

```yaml
---
category: frameworks
title: "CK-Industry-Master-Reference"
last_updated: 2026-05-11
---
```

Body — 6 lớp mental model (target ≤ 12 KB tổng):

```markdown
[1 đoạn intro 50 từ — what is this master reference + how Master CK skill use it]

# LỚP 1: HIỂU NGÀNH

## 1.1 Mô hình kinh doanh — 4 mảng doanh thu

- Môi giới khách (commission)
- Cho vay ký quỹ (interest)
- Ngân hàng đầu tư (bảo lãnh + tư vấn + TPDN)
- Tự doanh (mark-to-market)

## 1.2 UBCKNN kiểm soát

- Trần dư nợ ký quỹ 200% (2.0×) vốn chủ sở hữu (TT 121/2020)
- Công bố thông tin (TT 96/2020)
- Tỷ lệ an toàn vốn khả dụng

## 1.3 Đặc thù VN

- 30+ CTCK niêm yết, top 5 chiếm >40% thị phần
- VPS leader thị phần Q1/2026 (~17%)
- Fee compression mạnh từ 2024 do TCBS/DNSE zero-fee
- Margin lending là 30-50% doanh thu cho top broker

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics quan trọng

### Tier 1 — phản ứng ngay
- Thị phần môi giới (HOSE + HNX)
- Dư nợ cho vay ký quỹ + headroom vs trần 200%

### Tier 2 — phản ứng chậm
- ROE
- Biên lợi nhuận môi giới (gross/net)
- Cơ cấu doanh thu (môi giới/margin/IB/tự doanh)

### Tier 3 — dài hạn
- Tỷ lệ an toàn vốn khả dụng
- Tài sản quản lý (AUM)

## 2.2 Bẫy BCTC CTCK

- Doanh thu môi giới gross vs net (trừ chi phí trả bên thứ ba)
- Tự doanh "kinh doanh" vs "đầu tư" (recognition khác)
- Mark-to-market FVTPL impact lợi nhuận từng quý
- TPDN exposure ẩn trong "Tài sản tài chính sẵn sàng để bán"

# LỚP 3: HIỂU CHU KỲ

CK gắn CHẶT với:
1. Chu kỳ lãi suất NHNN
2. Thanh khoản thị trường (cross-cutting theme — xem [CK-Liquidity-sensitivity](./ck-liquidity-sensitivity.md))

## 3.1 Lãi suất giảm = MUA CK
- Cho vay ký quỹ chi phí giảm → biên lãi tăng
- Khách vay ký quỹ tăng → doanh thu margin tăng (xem [CK-Margin-cycle](./ck-margin-cycle.md))
- Thanh khoản thị trường tăng → môi giới tăng (xem [CK-Brokerage-marketshare](./ck-brokerage-marketshare.md))
- Phát hành cổ phiếu/trái phiếu thuận lợi → IB tăng (xem [CK-IB-revenue-volatility](./ck-ib-revenue-volatility.md))
- Cổ phiếu/trái phiếu trong tự doanh tăng giá → P&L tích cực (xem [CK-Proprietary-trading](./ck-proprietary-trading.md))

## 3.2 Lãi suất tăng = BÁN CK
- Ngược lại 5 chiều trên

# LỚP 4: PER-TICKER POSITIONING

## SSI — Leader truyền thống
[1-2 đoạn: positioning + edge + risk Q1/2026]

## VND — Aggressive growth
[1-2 đoạn]

## HCM — Quality + foreign-friendly
[1-2 đoạn]

## VCI — High-margin niche IB
[1-2 đoạn]

## SHS — Consumer-retail tilt
[1-2 đoạn]

# LỚP 5: ĐỊNH GIÁ

- P/B benchmark Q1/2026 (5 mã universe)
- P/E thận trọng (earnings volatility cao do tự doanh + IB cycle-driven)
- Decision rule: dùng P/B 3-year average + ROE forward thay P/E spot

# LỚP 6: CASE STUDY LỊCH SỬ

## 6.1 2018 NHNN siết ký quỹ
[2-3 câu impact lên broker doanh thu margin]

## 6.2 2020 COVID rally
[VN-Index 660 → 1500, broker ăn fee + margin both]

## 6.3 2022 khủng hoảng TPDN
[Vạn Thịnh Phát + Tân Hoàng Minh, broker tổn thất tự doanh + IB sụp]

## 6.4 2023-2024 phục hồi
[Recovery từ low base, fee compression bắt đầu]

## 6.5 2025-2026 fee compression
[Zero-fee disruption, top broker mất thị phần, margin = profit driver]
```

Cross-link 5 deep dives bằng relative path. Per-ticker compact 1-2 paragraph/mã (KHÔNG tách file thứ 7 per spec § 5).

- [ ] **Step 4: Smoke check toàn bộ 6 file**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.kb_loader import KBLoader
loader = KBLoader('kb/ck/')
print('FILES:', len(loader._all_files()))
for kw in ['ký quỹ', 'thị phần', 'ngân hàng đầu tư', 'tự doanh', 'thanh khoản', '6 lớp']:
    matches = [r['title'] for r in loader.search([kw])]
    print(f'  search [{kw}]: {matches}')
"
```

Expected: `FILES: 6`, mỗi keyword search có ít nhất 1 match.

- [ ] **Step 5: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add kb/ck/frameworks/ck-industry-master-reference.md && git commit -m "kb(ck): add industry master reference (6 lớp mental model)

Anchor cho Master CK skill — 6 lớp Hiểu ngành/Đọc số/Hiểu chu kỳ/
Per-ticker/Định giá/Case study lịch sử. Cross-link 5 framework
deep dives. Per-ticker positioning 5 mã universe inline (compact).

Spec: docs/superpowers/specs/2026-05-11-ck-kb-bootstrap-design.md"
```

---

## Task 7: ck_targets.yaml

**Files:**
- Create: `data/manual/ck_targets.yaml`

- [ ] **Step 1: Web research kế hoạch ĐHĐCĐ 2026 + Q1 actuals**

Search nghị quyết ĐHĐCĐ 2026 cho 5 mã: SSI, VND, HCM, VCI, SHS. Lấy:
- `target_lntt_ty` (lợi nhuận trước thuế cả năm tỷ đồng)
- `target_revenue_ty` (doanh thu cả năm tỷ đồng)
- `actual_lntt_q1_ty` (Q1/2026 BCTC)
- `actual_revenue_q1_ty` (Q1/2026 BCTC)
- `source` + `source_url`

Nếu data thiếu / chưa public → dùng mock với `last_verified: "unknown"`, `verified_by: "bootstrap"`.

- [ ] **Step 2: Write `data/manual/ck_targets.yaml`**

Use Write tool. Format theo Bank `targets.yaml` pattern:

```yaml
# CK Targets vs Actual — kế hoạch ĐHĐCĐ vs thực tế per quý
# Source: nghị quyết ĐHĐCĐ năm + quarterly BCTC
# MOCK stubs cho bootstrap — replace với data thật khi web search confirm
#
# Freshness fields:
#   last_verified: ISO date when row was last confirmed
#   verified_by:   short string (operator/run id)
#   source_url:    canonical URL của nghị quyết / BCTC

- ticker: SSI
  year: 2026
  target_lntt_ty: 4000
  target_revenue_ty: 9500
  actual_lntt_q1_ty: 850
  actual_revenue_q1_ty: 2100
  source: "Nghị quyết ĐHĐCĐ 20/4/2026"
  source_url: "https://example.com/ssi-dhdcd-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"

- ticker: VND
  year: 2026
  target_lntt_ty: 2800
  target_revenue_ty: 6800
  actual_lntt_q1_ty: 580
  actual_revenue_q1_ty: 1450
  source: "Nghị quyết ĐHĐCĐ 25/4/2026"
  source_url: "https://example.com/vnd-dhdcd-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"

- ticker: HCM
  year: 2026
  target_lntt_ty: 1800
  target_revenue_ty: 4500
  actual_lntt_q1_ty: 420
  actual_revenue_q1_ty: 1080
  source: "Nghị quyết ĐHĐCĐ 22/4/2026"
  source_url: "https://example.com/hcm-dhdcd-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"

- ticker: VCI
  year: 2026
  target_lntt_ty: 1500
  target_revenue_ty: 3800
  actual_lntt_q1_ty: 380
  actual_revenue_q1_ty: 920
  source: "Nghị quyết ĐHĐCĐ 24/4/2026"
  source_url: "https://example.com/vci-dhdcd-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"

- ticker: SHS
  year: 2026
  target_lntt_ty: 1200
  target_revenue_ty: 3200
  actual_lntt_q1_ty: 280
  actual_revenue_q1_ty: 780
  source: "Nghị quyết ĐHĐCĐ 23/4/2026"
  source_url: "https://example.com/shs-dhdcd-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"
```

Replace mock numbers với data thật khi web research confirm. Mock OK nếu không tìm được — `last_verified: "unknown"` sẽ trigger Master CK gọi web_search refresh khi viết bài.

- [ ] **Step 3: Smoke check**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import yaml
with open('data/manual/ck_targets.yaml') as f:
    data = yaml.safe_load(f)
print(f'Rows: {len(data)}')
print(f'Tickers: {[r[\"ticker\"] for r in data]}')
"
```

Expected: `Rows: 5`, `Tickers: ['SSI', 'VND', 'HCM', 'VCI', 'SHS']`.

- [ ] **Step 4: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add data/manual/ck_targets.yaml && git commit -m "data(ck): add targets vs actual yaml (5 mã universe)

Kế hoạch ĐHĐCĐ 2026 vs Q1 actuals — SSI/VND/HCM/VCI/SHS.
Mock stub với last_verified=unknown. Master CK sẽ web_search
refresh khi viết bài đầu tiên.

Spec: docs/superpowers/specs/2026-05-11-ck-kb-bootstrap-design.md"
```

---

## Task 8: ck_market_share.yaml

**Files:**
- Create: `data/manual/ck_market_share.yaml`

- [ ] **Step 1: Web research thị phần HOSE/HNX Q1/2026**

Search "HOSE thị phần môi giới Q1 2026" + "HNX thị phần CTCK Q1 2026". Lấy thị phần %, rank, prev quarter % cho 5 mã.

- [ ] **Step 2: Write `data/manual/ck_market_share.yaml`**

```yaml
# CK Market Share — thị phần môi giới HOSE/HNX per quarter per ticker
# Source: HOSE/HNX công bố Top 10 thị phần môi giới hàng quý
# Leading indicator phí năm sau

- ticker: SSI
  exchange: HOSE
  quarter: 2026Q1
  market_share_pct: 9.5
  rank: 2
  prev_quarter_pct: 10.2
  source: "HOSE công bố thị phần Q1/2026"
  source_url: "https://example.com/hose-marketshare-q1-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"

- ticker: VND
  exchange: HOSE
  quarter: 2026Q1
  market_share_pct: 7.2
  rank: 4
  prev_quarter_pct: 7.8
  source: "HOSE công bố thị phần Q1/2026"
  source_url: "https://example.com/hose-marketshare-q1-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"

- ticker: HCM
  exchange: HOSE
  quarter: 2026Q1
  market_share_pct: 5.8
  rank: 5
  prev_quarter_pct: 6.0
  source: "HOSE công bố thị phần Q1/2026"
  source_url: "https://example.com/hose-marketshare-q1-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"

- ticker: VCI
  exchange: HOSE
  quarter: 2026Q1
  market_share_pct: 4.5
  rank: 7
  prev_quarter_pct: 4.7
  source: "HOSE công bố thị phần Q1/2026"
  source_url: "https://example.com/hose-marketshare-q1-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"

- ticker: SHS
  exchange: HOSE
  quarter: 2026Q1
  market_share_pct: 2.8
  rank: 11
  prev_quarter_pct: 3.0
  source: "HOSE công bố thị phần Q1/2026"
  source_url: "https://example.com/hose-marketshare-q1-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"
```

Replace mock với data web search nếu confirm. Mock OK với `last_verified: unknown`.

- [ ] **Step 3: Smoke check**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import yaml
with open('data/manual/ck_market_share.yaml') as f:
    data = yaml.safe_load(f)
print(f'Rows: {len(data)}')
print(f'Tickers: {[r[\"ticker\"] for r in data]}')
"
```

Expected: `Rows: 5`, tickers all 5.

- [ ] **Step 4: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add data/manual/ck_market_share.yaml && git commit -m "data(ck): add market share yaml (HOSE Q1/2026 5 mã)

Thị phần môi giới HOSE Q1/2026 + delta vs Q4/2025 — leading
indicator phí. Mock với last_verified=unknown, refresh khi cần.

Spec: docs/superpowers/specs/2026-05-11-ck-kb-bootstrap-design.md"
```

---

## Task 9: ck_margin_outstanding.yaml

**Files:**
- Create: `data/manual/ck_margin_outstanding.yaml`

- [ ] **Step 1: Web research dư nợ ký quỹ Q1/2026 + vốn chủ 5 mã**

Lấy từ BCTC Q1/2026 5 mã CK: dư nợ cho vay ký quỹ cuối quý + vốn chủ sở hữu. Tính `ratio = margin / equity` và `headroom_to_cap_ty = (2.0 × equity) - margin`.

- [ ] **Step 2: Write `data/manual/ck_margin_outstanding.yaml`**

```yaml
# CK Margin Outstanding — dư nợ cho vay ký quỹ + headroom vs trần 200% (2.0×) SSC
# Source: BCTC Q1/2026 5 mã CK universe
# SSC trần: dư nợ ký quỹ ≤ 200% (2.0×) vốn chủ sở hữu sở hữu (TT 121/2020)
# Cảnh báo nội bộ broker khi vượt 150%

- ticker: SSI
  quarter: 2026Q1
  margin_outstanding_ty: 18000
  equity_ty: 12000
  ratio: 1.50
  cap_ratio: 2.00
  headroom_to_cap_ty: 6000
  source: "BCTC Q1/2026 SSI"
  source_url: "https://example.com/ssi-bctc-q1-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"

- ticker: VND
  quarter: 2026Q1
  margin_outstanding_ty: 14000
  equity_ty: 10500
  ratio: 1.33
  cap_ratio: 2.00
  headroom_to_cap_ty: 7000
  source: "BCTC Q1/2026 VND"
  source_url: "https://example.com/vnd-bctc-q1-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"

- ticker: HCM
  quarter: 2026Q1
  margin_outstanding_ty: 9500
  equity_ty: 7800
  ratio: 1.22
  cap_ratio: 2.00
  headroom_to_cap_ty: 6100
  source: "BCTC Q1/2026 HCM"
  source_url: "https://example.com/hcm-bctc-q1-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"

- ticker: VCI
  quarter: 2026Q1
  margin_outstanding_ty: 8200
  equity_ty: 6500
  ratio: 1.26
  cap_ratio: 2.00
  headroom_to_cap_ty: 4800
  source: "BCTC Q1/2026 VCI"
  source_url: "https://example.com/vci-bctc-q1-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"

- ticker: SHS
  quarter: 2026Q1
  margin_outstanding_ty: 4800
  equity_ty: 4200
  ratio: 1.14
  cap_ratio: 2.00
  headroom_to_cap_ty: 3600
  source: "BCTC Q1/2026 SHS"
  source_url: "https://example.com/shs-bctc-q1-2026"
  last_verified: "unknown"
  verified_by: "bootstrap"
```

Replace mock với BCTC thật khi web search confirm.

- [ ] **Step 3: Smoke check**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import yaml
with open('data/manual/ck_margin_outstanding.yaml') as f:
    data = yaml.safe_load(f)
print(f'Rows: {len(data)}')
for r in data:
    expected_headroom = round(r['cap_ratio'] * r['equity_ty'] - r['margin_outstanding_ty'])
    actual = r['headroom_to_cap_ty']
    diff = abs(expected_headroom - actual)
    flag = 'OK' if diff < 50 else 'MISMATCH'
    print(f'  {r[\"ticker\"]}: ratio={r[\"ratio\"]}, headroom={actual} (calc={expected_headroom}) {flag}')
"
```

Expected: `Rows: 5`, tất cả `OK` (headroom đúng công thức ±50 tỷ rounding).

- [ ] **Step 4: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add data/manual/ck_margin_outstanding.yaml && git commit -m "data(ck): add margin outstanding yaml + headroom vs SSC 200%

Dư nợ ký quỹ Q1/2026 + vốn chủ + ratio vs trần SSC. Mock 5 mã,
last_verified=unknown để Master CK web search BCTC thật khi cần.

Spec: docs/superpowers/specs/2026-05-11-ck-kb-bootstrap-design.md"
```

---

## Task 10: ssc_circulars.yaml

**Files:**
- Create: `data/manual/ssc_circulars.yaml`

- [ ] **Step 1: Web research SSC circulars affecting CTCK 2020-2026**

Key thông tư:
- TT 121/2020/TT-BTC — tỷ lệ an toàn vốn khả dụng + trần dư nợ ký quỹ 200% (Điều 28)
- TT 96/2020/TT-BTC — công bố thông tin
- TT 134/2020/TT-BTC — quy định CTCK
- TT 65/2022/TT-BTC — siết phát hành TPDN (impact IB)
- Recent updates 2024-2026

- [ ] **Step 2: Write `data/manual/ssc_circulars.yaml`**

Format theo Bank `nhnn_circulars.yaml`:

```yaml
# SSC Circulars affecting CK sector
# Source: UBCKNN + Bộ Tài chính

- title: "Thông tư 121/2020/TT-BTC"
  effective_date: 2021-01-01
  affected_topics: ["Tỷ lệ an toàn vốn khả dụng", "Margin lending"]
  summary: "Quy định CTCK rủi ro vốn khả dụng + trần dư nợ ký quỹ 200% (2.0×) vốn chủ sở hữu. Cảnh báo nội bộ broker khi vượt 150%."
  url: "https://example.com/ssc-tt121-2020"

- title: "Thông tư 96/2020/TT-BTC"
  effective_date: 2021-01-01
  affected_topics: ["Công bố thông tin"]
  summary: "Công bố thông tin định kỳ + bất thường cho CTCK + công ty đại chúng."
  url: "https://example.com/ssc-tt96-2020"

- title: "Thông tư 134/2020/TT-BTC"
  effective_date: 2021-01-01
  affected_topics: ["Hoạt động CTCK"]
  summary: "Quy định hoạt động kinh doanh chứng khoán của CTCK + tỷ lệ giới hạn."
  url: "https://example.com/ssc-tt134-2020"

- title: "Thông tư 65/2022/TT-BTC"
  effective_date: 2022-09-25
  affected_topics: ["Phát hành TPDN", "IB revenue"]
  summary: "Siết tiêu chí phát hành trái phiếu doanh nghiệp riêng lẻ — tác động giảm doanh thu IB của CTCK."
  url: "https://example.com/ssc-tt65-2022"

- title: "Nghị định 65/2022/NĐ-CP"
  effective_date: 2022-09-16
  affected_topics: ["Phát hành TPDN", "IB revenue"]
  summary: "Sửa đổi Nghị định 153/2020 về phát hành TPDN — tăng yêu cầu xếp hạng tín nhiệm."
  url: "https://example.com/ssc-nd65-2022"
```

Replace mock URLs với thật khi research confirm.

- [ ] **Step 3: Smoke check**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
import yaml
with open('data/manual/ssc_circulars.yaml') as f:
    data = yaml.safe_load(f)
print(f'Rows: {len(data)}')
for r in data:
    print(f'  {r[\"title\"]} — {r[\"effective_date\"]}')
"
```

Expected: `Rows: 5`, mỗi row print title + effective_date.

- [ ] **Step 4: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add data/manual/ssc_circulars.yaml && git commit -m "data(ck): add SSC circulars yaml (5 thông tư key)

UBCKNN/Bộ Tài chính circulars affecting CTCK — TT 121/2020 trần
ký quỹ, TT 96/2020 công bố thông tin, TT 65/2022 siết TPDN.

Spec: docs/superpowers/specs/2026-05-11-ck-kb-bootstrap-design.md"
```

---

## Task 11: SKILL.md update — wire KB + YAML + wording fix

**Files:**
- Modify: `.claude/skills/finpath-newsroom-master-ck/SKILL.md`

- [ ] **Step 1: Read current SKILL.md để identify exact lines cần sửa**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -n "Phase 1\|Finpath API\|Live API\|web_search\|primary source" .claude/skills/finpath-newsroom-master-ck/SKILL.md
```

Expected: list các line có wording cần thay (ít nhất 3 chỗ: SKILL.md line 18-20 "Phase 1 chưa có DB Notion riêng" + line 129 "DB IDs CK sector" + workflow step 3 "Query Live API").

- [ ] **Step 2: Edit (a) — wording fix "Finpath API/Live API → web_search"**

Use Edit tool. Tìm và thay 3 đoạn:

**Edit 1** — line 18-20 (workflow step 4):
- old: `**Web search** — Phase 1 chưa có DB CK Notion, dùng web_search + web_fetch làm primary source`
- new: `**Web search** — bổ sung khi local KB + YAML thiếu data. Finpath API chưa có CK data — KHÔNG query.`

**Edit 2** — line 129 (DB IDs CK sector):
- old: `⚠️ **Phase 1**: CK chưa có DB Notion riêng. Master CK V2.4 dùng web_search + Live API làm primary source. Phase 2 sẽ build DB CK (BCTC CK Quarter, Margin Outstanding, Foreign Activity).`
- new: `Master CK query local KB (`kb/ck/`) + YAML (`data/manual/ck_*.yaml` + `ssc_circulars.yaml`) trước. Web_search bổ sung khi thiếu. Finpath API chưa có CK data — KHÔNG query.`

**Edit 3** — workflow step 3 "Query Live API":
- old: `3. **Query Live API** — real-time price/volume/margin data`
- new: `3. **Query local KB CK** — `KBLoader('kb/ck/').search([keywords])` + `loader.load_topic(path)` cho top match`

- [ ] **Step 3: Edit (b) — add workflow step query YAML**

Add new step sau "Query local KB CK" (insert before "Web search"):

**Edit:** Thêm Step 4 mới (renumber Web search → Step 5, Verify → Step 6, ...):

```markdown
4. **Query manual YAML** — `ck_targets.yaml` + `ck_market_share.yaml` + `ck_margin_outstanding.yaml` + `ssc_circulars.yaml`. Filter by ticker / quarter / topic. Check `freshness_warning()` — nếu stale → web_search refresh.
```

- [ ] **Step 4: Edit (c) — add KB + YAML code blocks ở Compare Feed spec section**

Sau workflow steps, add code block reference (giống Master Bank SKILL.md line 247-252 pattern):

**Edit:** Tìm section `## Compare Feed prepend` hoặc end of workflow, thêm:

```markdown
## Local data sources

| Resource | Pattern |
|---|---|
| KB ngành CK | `KBLoader('kb/ck/').search([keywords])` + `loader.load_topic(path)` |
| YAML manual | `yaml.safe_load(open('data/manual/ck_<X>.yaml'))` |
| SSC circulars | `yaml.safe_load(open('data/manual/ssc_circulars.yaml'))` |

`from lib.kb_loader import KBLoader` → `loader = KBLoader('kb/ck/')`
`from lib.kb_loader import freshness_warning` → check YAML row staleness.
```

- [ ] **Step 5: Edit (d) — update References section ở cuối SKILL.md**

Tìm `## References` section cuối file, thêm KB CK markdown links sau 5 reference cũ:

```markdown
- `kb/ck/frameworks/ck-industry-master-reference.md` — 6 lớp mental model anchor
- `kb/ck/frameworks/ck-margin-cycle.md` — cho vay ký quỹ + trần 200% (2.0×)
- `kb/ck/frameworks/ck-brokerage-marketshare.md` — thị phần HOSE/HNX
- `kb/ck/frameworks/ck-ib-revenue-volatility.md` — ngân hàng đầu tư
- `kb/ck/frameworks/ck-proprietary-trading.md` — tự doanh
- `kb/ck/frameworks/ck-liquidity-sensitivity.md` — earnings beta thanh khoản
```

- [ ] **Step 6: Smoke check SKILL.md valid**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -c "Finpath API\|Live API" .claude/skills/finpath-newsroom-master-ck/SKILL.md
```

Expected: `0` hoặc chỉ còn ở context "Finpath API chưa có CK data — KHÔNG query" (1 mention OK vì là negative reference).

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && grep -c "kb/ck/\|ck_targets\|ck_market_share\|ck_margin_outstanding\|ssc_circulars" .claude/skills/finpath-newsroom-master-ck/SKILL.md
```

Expected: ≥ 6 (KB references + 4 YAML mentions).

- [ ] **Step 7: Final smoke check end-to-end**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && uv run python -c "
from lib.kb_loader import KBLoader
import yaml

loader = KBLoader('kb/ck/')
print(f'KB CK files: {len(loader._all_files())}')
print(f'KB CK topics:', [f['title'] for f in [{'title': p.stem} for p in loader._all_files()]])

for fname in ['ck_targets', 'ck_market_share', 'ck_margin_outstanding', 'ssc_circulars']:
    with open(f'data/manual/{fname}.yaml') as f:
        data = yaml.safe_load(f)
    print(f'YAML {fname}: {len(data)} rows')
"
```

Expected:
- KB CK files: 6
- KB CK topics: ['ck-industry-master-reference', 'ck-margin-cycle', 'ck-brokerage-marketshare', 'ck-ib-revenue-volatility', 'ck-proprietary-trading', 'ck-liquidity-sensitivity']
- YAML rows: 5/5/5/5

- [ ] **Step 8: Commit**

```bash
cd "/Users/trungdt/Desktop/Stream Intelligent" && git add .claude/skills/finpath-newsroom-master-ck/SKILL.md && git commit -m "skill(ck): wire KB + YAML, replace 'Finpath API' wording

Master CK skill now queries local KB (kb/ck/) + YAML
(data/manual/ck_*.yaml) trước khi web_search. Wording fix:
Finpath API chưa có CK data → web_search bổ sung.

KB SKILL.md V2.4/V3.6 version chưa bump V4.0 — out of scope spec
này, sẽ do Phase pipeline expand sau.

Spec: docs/superpowers/specs/2026-05-11-ck-kb-bootstrap-design.md"
```

---

## Self-review checklist (run sau khi xong cả 11 task)

- [ ] **Spec coverage:** All 10 sections of spec mapped to tasks (§ 4 file layout = Tasks 1-10, § 5 markdown structure = Task 1-6 content pattern, § 6 YAML structure = Tasks 7-10, § 7 SKILL.md updates = Task 11, § 9 validation = Task 11 step 7).

- [ ] **No placeholder leak:** Search plan cho "TODO", "TBD", "fill in later" → 0 hit (mock URLs are intentional with `last_verified: unknown`, không phải placeholder logic).

- [ ] **Type/path consistency:** All file paths match spec § 4 layout. KBLoader pattern = `KBLoader('kb/ck/')` consistent across tasks. YAML field names match across `ck_*.yaml` files (ticker / quarter / source / source_url / last_verified / verified_by).

- [ ] **Final smoke check passes:** Task 11 Step 7 confirms 6 KB files + 4 YAML files load OK.

---

## Open questions / followup (post-plan)

- **Replace mock URLs trong YAML với thật** — khi user trigger first CK article, Master CK web_search refresh, append thật URL vào YAML, set `last_verified` thật.
- **Bump SKILL.md V4.0 parity** — separate phase khi pipeline expand từ Bank → CK.
- **Tạo `.claude/agents/newsroom-master-ck.md`** — separate phase cùng V4.0 bump.
