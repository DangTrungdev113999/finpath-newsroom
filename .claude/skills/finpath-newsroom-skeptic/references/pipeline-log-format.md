# Pipeline Log Format — Skeptic Step 5 + 6

Skeptic append Step 5 và Step 6 vào pipeline log toggle (Master đã tạo Step 1-4).

## Format Step 5

```markdown
### Step 5 — Skeptic V2.4 (mục đích: phản biện độc lập với context Master + brief)
- pull memory: <N> critiques recent về <TICKER>
- pass 1 fresh impression: <1 sentence first reaction từ body only>
- pass 2 compare insight: <1 sentence — match hay diverge>
- critique_angle picked: <1 of 6>
- variety_guard: <pass / triggered (lý do)>
- data fetched: <DBs/KB/API/web sources used>
- raw_fetched: <true|false> (Pass 4.5 conditional)
- key data anchor: <1-2 số cụ thể từ data fetch để support critique>
```

## Format Step 6

```markdown
### Step 6 — Persist phản biện
- update DB Generated News row <row_id>
- properties set:
  - Phản biện: <critique 100-300 từ>
  - Skeptic_review_full: <full critique>
  - Skeptic_verdict: <pass | pass_with_caveats | fail>
  - Critique angle: <1 of 6>
  - Variety_guard_angle: <angle>
- append "## Góc nhìn ngược" section vào page body
- agreement_level: <đồng tình phần lớn | đồng tình một phần | không đồng tình>
```

## Insertion logic

Master đã tạo `<details>📋 Pipeline log</details>` toggle với Step 1-4. Skeptic:

1. Fetch page content (Notion API)
2. Tìm `</details>` đóng pipeline log toggle
3. Insert Step 5 + Step 6 NGAY TRƯỚC dòng `</details>`
4. Update page content

Code pattern:
```python
page_content = fetch_page_content(row_id)
new_steps = """
### Step 5 — Skeptic V2.4 ...
### Step 6 — Persist phản biện ...
"""
updated_content = page_content.replace(
    "</details>",
    f"{new_steps}\n</details>",
    1  # only first occurrence
)
update_page_content(row_id, updated_content)
```
