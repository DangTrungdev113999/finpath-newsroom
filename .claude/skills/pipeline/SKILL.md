---
name: pipeline
description: Quản lý Finpath Newsroom pipeline. Hiện hỗ trợ add-sector — thêm ngành mới vào universe với đầy đủ KB, routing, master agent. Trigger khi user muốn mở rộng pipeline sang sector mới (telecom, insurance, pharma...) hoặc hỏi về cấu trúc pipeline.
---

# Pipeline Management — Finpath Newsroom

Skill quản lý và mở rộng Finpath Newsroom pipeline.

## Commands hiện có

| Command | Mô tả |
|---------|-------|
| `/pipeline add-sector <NAME>` | Thêm ngành mới vào universe |
| `/pipeline status` | Xem trạng thái pipeline hiện tại |

## /pipeline add-sector <SECTOR_NAME>

Thêm ngành mới vào Finpath Newsroom pipeline với đầy đủ components.

### Input cần thu thập

Nếu user chưa cung cấp đủ, hỏi từng bước:

1. **Tên sector** (kebab-case cho folder, Title Case cho display)
   - Ví dụ: `telecom` / `Telecom`, `insurance` / `Insurance`

2. **Danh sách ticker universe** (10-30 mã, phân theo sàn)
   ```
   HOSE: VTT, VTEL, ...
   HNX: ABC, DEF, ...
   UPCOM: GHI, JKL, ...
   ```

3. **Company name aliases** cho mỗi ticker (để detect trong tin tức)
   ```
   VTT: "viettel", "tập đoàn viettel"
   VTEL: "viettel telecom", "viễn thông viettel"
   ```

4. **Jargon mapping** (English → Vietnamese cho sector)
   ```
   ARPU → doanh thu bình quân/thuê bao
   churn rate → tỷ lệ rời mạng
   ```

### Workflow 7 bước

Đọc `references/add-sector-checklist.md` để thực hiện đầy đủ:

#### Bước 1: Tạo KB framework
```bash
mkdir -p kb/<sector>/frameworks/
```
Tạo file `<sector>-industry-master-reference.md` theo template `references/kb-framework-template.md`.

#### Bước 2: Update routing.py
File: `.claude/skills/finpath-newsroom-editor/scripts/routing.py`

```python
# Thêm universe constant
<SECTOR>_UNIVERSE = [
    # HOSE
    "TICKER1", "TICKER2", ...
    # HNX
    "TICKER3", ...
    # UPCOM
    "TICKER4", ...
]  # N mã

# Append to FULL_UNIVERSE
FULL_UNIVERSE = BANK_UNIVERSE + CK_UNIVERSE + BDS_UNIVERSE + OIL_GAS_UNIVERSE + <SECTOR>_UNIVERSE

# Add to TICKER_TO_SECTOR
for t in <SECTOR>_UNIVERSE:
    TICKER_TO_SECTOR[t] = "<Sector-Name>"
```

#### Bước 3: Update ticker_detection.py
File: `.claude/skills/finpath-newsroom-editor/scripts/ticker_detection.py`

```python
# Add to COMPANY_NAME_TO_TICKER
"company name lowercase": "TICKER",
"tên công ty": "TICKER",

# Add to SHORT_FORM_TO_TICKER
"TICKER": "TICKER",
```

#### Bước 4: Tạo master agent skill
```bash
mkdir -p .claude/skills/finpath-newsroom-master-<sector>/references/
```
Copy từ `references/master-skill-template.md`, customize:
- Universe list
- Jargon mapping table
- Sector-specific pitfalls
- Data fetching protocol (API endpoints, web search keywords)

#### Bước 5: Update /tin command
File: `.claude/commands/tin.md`
- Update FULL_UNIVERSE count (vd: 71 → 81)
- Add sector vào list
- Add routing rule cho master mới

#### Bước 6: Update CLAUDE.md
- Update universe count trong Identity section
- Add sector vào Universe section với ticker list
- Add kb folder vào Architecture map

#### Bước 7: Verify
```python
# Test routing
from routing import get_sector, FULL_UNIVERSE
print(f"Total: {len(FULL_UNIVERSE)} mã")
print(f"TICKER1 → {get_sector('TICKER1')}")
```

### Output

Sau khi hoàn thành, pipeline sẽ:
- Nhận diện ticker mới thuộc sector đúng
- Route sang master agent đúng
- Có KB framework để Master reference
- `/tin <TICKER>` hoạt động với mã mới

## /pipeline status

Xem trạng thái pipeline hiện tại:

```
Finpath Newsroom Pipeline V4.0
==============================
Universe: 71 mã (4 sector)
├── Bank:    27 mã (routing.BANK_UNIVERSE)
├── CK:      30 mã (routing.CK_UNIVERSE)
├── BĐS:      4 mã (routing.BDS_UNIVERSE)
└── Oil-Gas: 10 mã (routing.OIL_GAS_UNIVERSE)

KB folders: kb/bank/, kb/ck/, kb/bds/, kb/oil-gas/
Master agents: 4 (bank, ck, bds, oil-gas)
Quality gates: 5 (V4.0)
```

## References

- `references/add-sector-checklist.md` — Checklist đầy đủ với checkboxes
- `references/master-skill-template.md` — Template SKILL.md cho master mới
- `references/kb-framework-template.md` — Template KB 6 lớp mental model

## Future commands (placeholder)

- `/pipeline add-ticker <SECTOR> <TICKER>` — Thêm 1 ticker vào sector có sẵn
- `/pipeline remove-ticker <TICKER>` — Xóa ticker khỏi universe
- `/pipeline validate` — Kiểm tra consistency giữa routing/KB/skills
