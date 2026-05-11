# BĐS KB Build — Design Spec v1.0

**Date:** 2026-05-11
**Author:** Claude (drafted via brainstorming with user @dangtrungicloud)
**Status:** Draft — awaiting user review

## 1. Mục tiêu

Build **static knowledge base** cho ngành Bất động sản (BĐS) toàn diện, cho phép Master agent phân tích bất kỳ mã cổ phiếu BĐS Việt nào (không chỉ MVP universe). 18 file markdown tại `kb/bds/frameworks/` chứa **framework + mechanism + threshold dài hạn + case study lịch sử + pitfalls + regulatory** — kiến thức tĩnh không đổi theo quý.

**Universe coverage:**
- **MVP residential (priority):** VHM, NVL, KDH, DXG, NLG
- **KCN khu công nghiệp:** KBC, BCM, IDC, SZC, SIP, SNZ
- **Retail bán lẻ:** VRE, AEON Mall (chủ đầu tư)
- **Office văn phòng:** các REIT văn phòng + landlord lớn
- **Resort nghỉ dưỡng:** SDI, NTL, NVL (phân khúc condotel), Sun Group portfolio
- **Data Center:** VNG Data, CMC Telecom, FPT DC

**Nguyên tắc cốt lõi:** KB chỉ chứa **kiến thức tĩnh dài hạn**. Data động (anchor data Q1/2026, backlog quý hiện hành, doanh số bán trước tháng này) → Master tự fetch realtime qua **Finpath API** (BCTC/events/news) hoặc **web_search** (BĐS-specific như tiến độ pháp lý dự án, FDI tháng, occupancy quý). Lý do:

- Sau 3 tháng số dynamic stale → KB hóa thông tin sai
- Master skill đã có web_search + Finpath API → realtime accurate hơn
- KB không phình theo quarter (không cần update mỗi 3 tháng)
- KB framework dùng chung cho mọi ticker BĐS (Master tự match ticker với loại BĐS qua routing table)

## 2. Scope

### In scope

- **18 file markdown** tại `kb/bds/frameworks/` — pure static (framework + mechanism + threshold range + pitfalls + case study lịch sử + regulatory)
- **1 file master reference** = `bds-industry-master-reference.md` chứa 6-layer mental model + routing table (ticker → loại BĐS → framework file apply)
- Source: 20 Notion pages của KB BĐS (sếp đã pre-write), 1-to-1 mapping (không consolidate)
- Update `lib/kb_loader.py` nếu cần để đọc `kb/bds/` cùng pattern với `kb/bank/` + `kb/ck/`

### Out of scope (defer)

- ❌ Master BĐS skill (đã có `.claude/skills/finpath-newsroom-master-bds/` từ V3.6 cho residential — sẽ update SKILL.md riêng sau khi KB xong)
- ❌ Per-ticker data file (anchor data Q1/2026, backlog snapshot) — Master web_search realtime
- ❌ data/manual/*.yaml (targets / credit room / regulatory) cho BĐS — defer cho phase sau nếu thấy cần curated DB
- ❌ Notion publish automation — KB markdown đứng riêng, Notion là source of truth (đã có sẵn)

## 3. Architecture

```
kb/bds/
└── frameworks/                                 ← flat structure (theo CK pattern)
    │
    │  --- Hub (1 file) ---
    ├── bds-industry-master-reference.md        ← 6-layer mental model + routing table
    │
    │  --- Framework chung (5 file, cross-category) ---
    ├── bds-revenue-recognition-vas.md          ← VAS 14/15 — pre-sales ≠ doanh thu
    ├── bds-debt-leverage.md                    ← D/E theo cycle + trái phiếu BĐS
    ├── bds-macro-cycle-credit.md               ← NHNN credit cycle + lãi suất
    ├── bds-legal-framework.md                  ← Luật Đất đai 2024 + 4 luật BĐS
    ├── bds-hybrid-business-models.md           ← Developer + landlord + môi giới hybrid
    │
    │  --- Residential (3 file) ---
    ├── bds-res-presales-backlog.md             ← Backlog leading indicator 12-24 tháng
    ├── bds-res-land-bank-nav.md                ← Quỹ đất + P/NAV trap
    ├── bds-res-project-lifecycle.md            ← 5 phase: Acquisition → Legal → Build → Sale → Handover
    │
    │  --- KCN (3 file) ---
    ├── bds-kcn-fdi-demand-mechanism.md         ← FDI demand drive thuê đất KCN
    ├── bds-kcn-inventory-pricing.md            ← Tồn kho đất + giá thuê
    ├── bds-kcn-lease-structure.md              ← HĐ thuê 30-50 năm, one-shot vs spread
    │
    │  --- Retail (3 file) ---
    ├── bds-retail-footfall-mechanism.md        ← Lượt khách → doanh thu thuê
    ├── bds-retail-tenant-mix-quality.md        ← Chất lượng tenant mix
    ├── bds-retail-anchor-vs-sme-tenants.md     ← Anchor tenant vs SME thuê nhỏ
    │
    │  --- Office (2 file) ---
    ├── bds-office-class-tiering.md             ← Grade A/B/C + định giá thuê
    ├── bds-office-hybrid-work-impact.md        ← Work-from-home impact post-COVID
    │
    │  --- Resort (3 file) ---
    ├── bds-resort-condotel-legal-pitfalls.md   ← Pháp lý condotel — sổ hồng vs SH du lịch
    ├── bds-resort-tourism-cycle.md             ← Chu kỳ du lịch + occupancy rate
    ├── bds-resort-hybrid-model.md              ← Hybrid: cho thuê + bán cho NĐT cá nhân
    │
    │  --- Data Center (1 file) ---
    └── bds-dc-hyperscaler-power.md             ← Hyperscaler clients + nguồn điện
```

**Tổng: 18 file** (1 hub + 5 framework chung + 3 residential + 3 KCN + 3 retail + 2 office + 3 resort + 1 DC).

## 4. Per-file template

Mỗi file follow template chuẩn:

```markdown
---
category: frameworks
title: "BDS-{Topic-name}"
last_updated: 2026-05-11
notion_page_id: "<uuid từ Notion>"
source_url: "https://notion.so/<id>"
applies_to: ["residential", "kcn", "retail"]   # loại BĐS áp dụng — guide Master routing
---

# {Tiêu đề tiếng Việt thuần}

{Intro 2-3 câu — mục đích file, khi nào Master đọc}

## Khái niệm & cơ chế

{Định nghĩa Vietnamese pure + cơ chế hoạt động}

## Threshold benchmark dài hạn

{Số sanity-check khi web_search. KHÔNG per-quarter snapshot. Range rộng OK.}

vd: D/E peak cycle 1.5-2.0x = normal; >2.5x = warning zone

## Pitfalls (đọc số dễ sai) — bắt buộc ≥ 2 pitfall

{Bẫy phổ biến khi đọc BCTC/báo cáo BĐS, minh họa với case lịch sử}

## Case study lịch sử

**Format mỗi case study:**

> **{Năm} — {Loại BĐS} — Minh họa {mechanism}**:
> {Mô tả ngắn 2-3 câu}
>
> **Không analogize sang**: {loại BĐS khác mechanism — kèm link file framework đúng}

## Regulatory (nếu có)

{Luật + Thông tư + Nghị định, historical (đã ban hành)}

vd: Luật Kinh doanh BĐS 2023 Điều 26 — điều kiện bàn giao

## Source log

- {URL gốc Notion / báo / luật}
- Stamp: `build YYYY-MM-DD. Review every N years tuỳ tốc độ đổi`
```

**Notes về template:**

1. **`applies_to` field mới** — KHÔNG có ở CK pattern. Guide Master routing. Vd `bds-res-presales-backlog.md` có `applies_to: ["residential"]` → Master phân tích KBC sẽ skip file này. **Enum values cho phép:** `residential`, `kcn`, `retail`, `office`, `resort`, `data_center`, `all` (cho Framework chung 5 file).
2. **`notion_page_id` + `source_url`** — kế thừa CK/Bank pattern, cho phép re-sync khi Notion update.
3. **Section "Pitfalls" bắt buộc ≥ 2** — BĐS đặc biệt dễ đọc sai (booking ≠ ghi nhận, landbank ≠ sẵn sàng bán).
4. **Case study guardrail 3-label** + dòng `Không analogize sang` để Master không over-generalize.
5. **KHÔNG section "Anchor data hiện hành"** — static-only. Bất cứ dòng nào có nguy cơ stale sau 3 tháng → reject.

## 5. Content principles (5 hard rules)

Mỗi file viết phải pass 5 nguyên tắc, vi phạm bất kỳ rule nào → rewrite, không persist.

### 5.1 Static knowledge only

| ✅ Cho phép | ❌ Cấm |
|---|---|
| "D/E BĐS dân cư cycle peak 1.5-2.0x normal, >2.5x warning" (threshold dài hạn) | "VHM D/E hiện tại 0.8x" (rolling snapshot) |
| "Luật Kinh doanh BĐS 2023 Điều 26 quy định 5 điều kiện bàn giao" (lịch sử) | "Q1/2026 NVL backlog 8.000 tỷ" (anchor data) |
| "TT 16/2021 sửa đổi 2024 — riêng lẻ trái phiếu BĐS cần xếp hạng tín nhiệm" | "Tháng 4/2026 NHNN cấp room 16% ngành" (current month) |

**Test:** Sau 6 tháng dòng này còn đúng không? Có khả năng stale → strip, Master web_search realtime.

### 5.2 Vietnamese pure (0% từ Anh)

Mapping cứng cho BĐS (mở rộng từ Bank/CK):

| Tiếng Anh | Tiếng Việt thay thế |
|---|---|
| Pre-sales | doanh số bán trước |
| Backlog | doanh số chờ ghi nhận |
| Landbank | quỹ đất |
| NAV | giá trị tài sản ròng |
| P/NAV | hệ số giá trên giá trị tài sản ròng |
| Cap rate | tỷ suất sinh lời cho thuê |
| GFA | tổng diện tích sàn |
| NLA | diện tích cho thuê thuần |
| Occupancy rate | tỷ lệ lấp đầy |
| Footfall | lượt khách |
| Anchor tenant | khách thuê chủ chốt |
| FDI | vốn đầu tư trực tiếp nước ngoài |
| Hyperscaler | khách hàng đám mây lớn |
| Condotel | căn hộ khách sạn |
| Lease | hợp đồng thuê |
| POS recognition | ghi nhận khi bàn giao |
| POC recognition | ghi nhận theo tiến độ |
| Lump-sum | ghi nhận một lần |
| Recurring revenue | doanh thu định kỳ |

**Exception:** Tên riêng (Vincom Retail, Vinhomes, Ocean City, Aqua City, Sun Group...) + mã CK (VHM, NVL, KDH, DXG, KBC, VRE...).

### 5.3 Case study guardrail 3-label

Mỗi case study cuối file PHẢI có 3 label + dòng "Không analogize sang":

```
> **2024 — Residential developer (POS recognition) — Lag P&L lump-sum**:
> VHM bàn giao Ocean City Q3/2024 → doanh thu quarter 30k+ tỷ.
> Quarter trước & sau dưới 10k tỷ vì không có dự án bàn giao cùng quy mô.
>
> **Không analogize sang**: KCN (one-shot lease — xem `bds-kcn-lease-structure.md`);
> Retail (recurring monthly — xem `bds-retail-footfall-mechanism.md`).
```

### 5.4 Source log + stamp bắt buộc

Mỗi file cuối có:

```markdown
## Source log

- {URL gốc Notion}
- {URL báo / luật / nguồn dữ liệu}
- Stamp: build 2026-05-11. Review every 3 years (VAS / luật ít đổi).
```

Master có thể click verify; audit nguồn dễ.

### 5.5 Pitfall section ≥ 2 pitfall mỗi file

BĐS đặc biệt dễ đọc sai. Mỗi file phải có ≥ 2 bẫy phổ biến minh họa bằng case lịch sử ngắn.

## 6. Implementation approach

### Stage 1: Notion fetch (subagent)

Spawn 1 general-purpose subagent với prompt chi tiết:

- 20 Notion page IDs đầy đủ
- Notion MCP credentials đã setup
- Output: raw content text mỗi page (extract `plain_text` từ blocks, ignore JSON noise)

### Stage 2: Draft 18 file (subagent)

Cùng subagent tiếp tục viết 18 file draft v1 theo template Section 4 + 5 principles Section 5.

Output: 18 file tại `kb/bds/frameworks/*.md`.

### Stage 3: Review từng file (main session)

Em review từng file (parallel batch 4-5 file/lần):

1. Check 5 principles violation:
   - English jargon → fix theo mapping table 5.2
   - Anchor data Q1/Q2/Q3 2026 → strip
   - Case study thiếu 3-label → add
   - Source log thiếu → add
   - Pitfall < 2 → add
2. Verify `applies_to` field đúng
3. Test kb_loader: `loader.search([keyword])` return hợp lý

### Stage 4: Update `lib/kb_loader.py` nếu cần

Verify loader scan `kb/bds/` cùng pattern `kb/bank/` + `kb/ck/`. Có thể không cần thay đổi nếu loader đã glob `kb/*/frameworks/*.md`.

### Stage 5: Commit + update CLAUDE.md

- Commit atomic: `feat(kb): BĐS knowledge base — 18 files`
- Update CLAUDE.md Architecture map section thêm `kb/bds/` reference (nếu chưa có)

## 7. Risks & mitigation

| Risk | Mitigation |
|---|---|
| Subagent leak English jargon (POS recognition, anchor tenant...) trong draft v1 | Em review từng file, fix theo mapping 5.2 |
| Subagent inject Q1/2026 anchor data từ Notion source | Mapping table 5.1 + grep `Q[1-4]/202[5-9]` post-build → strip rolling current refs |
| Case study analogize sai (residential pattern apply nhầm KCN) | Format 3-label + dòng "Không analogize sang" bắt buộc, em verify mỗi case |
| 18 file × ~150 lines = 2700 lines KB → loader slow? | Existing kb_loader.py đã handle Bank (4 file) + CK (6 file). 18 file vẫn nhanh (regex search). |
| Notion content có "[SUY LUẬN]" / "[CHƯA VERIFY]" tag (em thấy trong sample VAS page) | Strip 2 tag này khi viết draft — không quote vào KB output (annotation Notion internal). |

## 8. Success criteria

- [ ] 18 file markdown tồn tại tại `kb/bds/frameworks/`
- [ ] Mỗi file pass 5 principles (5.1-5.5 Section 5)
- [ ] `lib/kb_loader.py` đọc được `kb/bds/` (test với `loader.search(['backlog', 'doanh số bán trước'])`)
- [ ] Hub file `bds-industry-master-reference.md` có routing table mapping 30+ ticker BĐS Việt → loại BĐS → framework file apply
- [ ] Commit atomic + push remote

## 9. Open questions

(Không có — design đã chốt qua brainstorming.)

## 10. Changelog

| Date | Version | Change |
|---|---|---|
| 2026-05-11 | v1.0 | Initial draft sau brainstorming với user |
