---
name: finpath-newsroom-headline-craft
description: Headline Craft skill V1.1 — 5 hard criteria + 4 lối + 8-point rubric reference for title generation. Use when newsroom-headline-craft agent runs Step 4.5 of pipeline. Covers ticker detection (139 universe + group refs), 4 lối giật tít, dramatic verb pool, specific number regex, paradox pattern, open question, PR clickbait blacklist, English jargon ban, em dash ban (V1.1 PATCH).
---

# Headline Craft Skill V1.1

Compact reference for Headline Craft agent. Loaded via `Skill: finpath-newsroom-headline-craft`.

## 4 lối giật tít (V1.1)

| Lối | Definition | Khi nào |
|---|---|---|
| Question | Title kết bằng `?` | Body có nghịch lý |
| Declarative tension | 2 sự kiện đối lập (NO em dash) | Body 2 fact ngược |
| Quote | Quote CEO/CFO + context | Brief có quote |
| Contrast verb | 2 chủ thể, verb đối lập | Body so sánh 2 nhóm |

## 5 hard criteria (V1.1)

```python
# All MUST be true → title accepted
ticker_present                 # 139-ticker universe or group ref
word_count_le_12               # ≤12 từ
hook_strong:                   # 2 sub-tests dict
  tension_present              # dramatic verb / tension word / paradox
  click_test_pass              # number / question / dramatic verb
binh_dan_nguy_hiem:            # 2 sub-tests dict
  plain_language               # no English + no PR clickbait
  sharp_edge                   # has tension/specific/dramatic
no_em_dash                     # '—' U+2014 BANNED (V1.1 PATCH)
```

Hyphen `-` + en dash `–` acceptable.

## 8-point rubric

Apply only to candidates passing 5 hard criteria.

| Element | Points |
|---|---|
| Dramatic verb | +2 |
| Specific number with units | +2 |
| Open question (ends `?`) | +1 |
| Tension word | +1 |
| Paradox pattern (X mà Y) | +1 |
| Extra concise (≤10 words) | +1 |

Max 8. Pick highest. Tie-break: shortest.

## Dramatic verb pool

```
hy sinh · đánh đổi · đặt cược · bỏ phiếu · lội ngược · lao dốc ·
rút khỏi · vượt mặt · tung đòn · đặt cọc · chấp nhận thua ·
tự chậm lại · đập cửa · thoát hiểm · chấp nhận hi sinh · đánh cược ·
đổ vỡ · vực dậy · tiếp đà · phá kỷ lục · soán ngôi · lấn sang · rơi vào
```

## Tension word pool (lives trong lib/headline_scorer V5.1.3)

```
hy sinh · đánh đổi · nghịch lý · vì sao · đổi lấy · không phải ·
bù lại · thay vì · chấp nhận
```

(Note: "hy sinh" + "đánh đổi" overlap dramatic_verbs — both count cho scoring.)

## PR clickbait blacklist

```
cú nổ · bí mật · sốc · hot · thông tin nóng · không thể tin nổi ·
cú twist · kỳ tích · hé lộ · kỷ tích
```

## Specific number regex

```python
r"\d+([.,]\d+)?\s*(tỷ|triệu|nghìn|%|đ|/năm|/tháng|/quý|đ/tháng|bps|điểm)"
```

## Em dash detector (V1.1)

```python
def has_em_dash(title: str) -> bool:
    return "—" in title  # U+2014 only — hyphen + en dash OK
```

## Output schema (strict V1.1)

```json
{
  "model": "claude-sonnet-4-6",
  "duration_ms": int,
  "tokens": int | null,
  "final_title": "string — passes check_hard_criteria 5 keys",
  "final_loi": "Question | Declarative tension | Quote | Contrast verb",
  "picked_score": int,
  "candidates": [
    {"title": "...", "loi": "...", "score": 7, "criteria": {...}}
  ],
  "hard_criteria_pass": {
    "ticker_present": true,
    "word_count_le_12": true,
    "hook_strong": {"tension_present": true, "click_test_pass": true},
    "binh_dan_nguy_hiem": {"plain_language": true, "sharp_edge": true},
    "no_em_dash": true
  }
}
```

Validation enforced at persist: `lib.pipeline_db.validate_pipeline_step('step_4_5_headline_craft', payload, pipeline_version)`. Title fails 5 criteria → ValueError.

## Anti-hallucination

- 3 candidate per lối khác angle, không cùng style
- NEVER invent PR clickbait
- Reuse dramatic verb pool (don't sáng tạo verb weak)
- If body says "VCB rút 12.000 tỷ" — title quote "VCB rút 12.000 tỷ vì sao?"
- Em dash `—` BANNED — use hyphen `-` if separator needed (but prefer Vietnamese conjunctions)
