# Add Sector Checklist

Checklist đầy đủ khi thêm ngành mới vào Finpath Newsroom pipeline.

## Pre-requisites

- [ ] Xác định tên sector (kebab-case: `insurance`, Title Case: `Insurance`)
- [ ] Danh sách ticker universe (tối thiểu 5, tối đa 30)
- [ ] Phân loại theo sàn (HOSE/HNX/UPCOM)
- [ ] Company aliases cho mỗi ticker
- [ ] Jargon mapping English → Vietnamese cho sector

## Step 1: Tạo KB Framework

```bash
mkdir -p kb/<sector>/frameworks/
```

- [ ] Tạo `kb/<sector>/frameworks/<sector>-industry-master-reference.md`
- [ ] Điền 6 lớp mental model (xem `kb-framework-template.md`)
- [ ] Web search để fill data thực tế cho sector

## Step 2: Update routing.py

File: `.claude/skills/finpath-newsroom-editor/scripts/routing.py`

- [ ] Add `<SECTOR>_UNIVERSE` constant với danh sách ticker
- [ ] Add comment phân theo sàn (HOSE/HNX/UPCOM)
- [ ] Append `<SECTOR>_UNIVERSE` vào `FULL_UNIVERSE`
- [ ] Add loop mapping `TICKER_TO_SECTOR[t] = "<Sector>"`
- [ ] Update docstring comment nếu cần (số mã total)

## Step 3: Update ticker_detection.py

File: `.claude/skills/finpath-newsroom-editor/scripts/ticker_detection.py`

- [ ] Add section comment `# <Sector> (N mã)`
- [ ] Add company aliases vào `COMPANY_NAME_TO_TICKER`
- [ ] Add tickers vào `SHORT_FORM_TO_TICKER`

## Step 4: Tạo Master Agent Skill

```bash
mkdir -p .claude/skills/finpath-newsroom-master-<sector>/references/
```

- [ ] Tạo `SKILL.md` từ template (`master-skill-template.md`)
- [ ] Customize frontmatter (name, description với ticker list)
- [ ] Customize Universe table
- [ ] Add Jargon mapping table (English → Vietnamese)
- [ ] Add Sector-specific pitfalls (5-10 items)
- [ ] Add Data fetching protocol (web search keywords cho sector)
- [ ] Optional: tạo reference files nếu cần

## Step 5: Update /tin Command

File: `.claude/commands/tin.md`

- [ ] Update `description` với số mã mới
- [ ] Update `FULL_UNIVERSE` count
- [ ] Add sector vào list với ticker count
- [ ] Add routing rule: `sector=<Sector> → newsroom-master-<sector>`
- [ ] Update "N sector" count

## Step 6: Update CLAUDE.md

File: `CLAUDE.md`

- [ ] Update Identity section: "X mã: ... + N <Sector>"
- [ ] Update Universe section header: "N sector (X mã)"
- [ ] Add sector block với ticker list
- [ ] Update Architecture map: add `kb/<sector>/`
- [ ] Update Total count comment

## Step 7: Verify

```bash
cd .claude/skills/finpath-newsroom-editor/scripts/
python -c "
exec(open('routing.py').read().replace('from .ticker_detection', '# from .'))
print(f'Total: {len(FULL_UNIVERSE)} mã')
for t in <SECTOR>_UNIVERSE:
    print(f'{t} → {get_sector(t)}')"
```

- [ ] get_sector() trả về đúng sector name
- [ ] FULL_UNIVERSE count đúng
- [ ] Tất cả ticker trong universe

## Post-completion

- [ ] Test `/tin <TICKER>` với 1 mã mới
- [ ] Verify pipeline route đúng master
- [ ] Optional: commit changes với message rõ ràng

## Common Issues

| Issue | Solution |
|-------|----------|
| Import error khi test | Chạy trong folder scripts/, dùng exec() trick |
| Ticker không detect | Check COMPANY_NAME_TO_TICKER lowercase |
| Wrong sector | Check TICKER_TO_SECTOR mapping order |
| KB not found | Verify folder path kb/<sector>/frameworks/ |
