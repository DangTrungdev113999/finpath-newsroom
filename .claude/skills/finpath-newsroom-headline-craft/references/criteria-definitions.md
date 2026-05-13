# Hard Criteria — Headline Craft V1.5-lite

> Loaded from `Skill: finpath-newsroom-headline-craft`. 8 hard criteria ALL must pass.

## V1.5-lite PATCH note (2026-05-13 PM)

User feedback: V1.2-V1.4 word-list scorer bonuses (DRAMATIC_VERBS +2,
CONCRETE_QUESTION_SUBJECTS +1, self_explanatory +1) caused Pattern A
pile-on — AI invented verbs from lists ("chấm đích / vọt lãi / xén lợi").

V1.5-lite drops word bonuses + word-list checks. Adds Hán-Việt + abbreviation
mechanical bans. Simplified 6-point rubric.

## 8 hard criteria V1.5-lite

### Criterion 1 — Ticker present
`has_ticker(title)` — match Finpath 139+ universe OR group ref (Big4/tư nhân).

### Criterion 2 — Compact ≤16 từ
V1.3 relaxed from 12 → 16 (clarity > conciseness).

### Criterion 3 — No em dash (V1.1)
`"—" not in title` (U+2014 only). Hyphen + en dash OK.

### Criterion 4 — Not label leak (V1.2)
Reject "Question" / "Declarative tension" / "Quote" / "Contrast verb" as bare title or `Lối X:` prefix.

### Criterion 5 — Not orphan number (V1.3)
Number/percent MUST have subject within 4 tokens. "ngành/nhóm" MUST have specifier (bank/CK/BĐS/etc.).

### Criterion 6 — No Hán-Việt formal (V1.5 NEW)
Title không chứa term từ `HAN_VIET_FORMAL_BAN` (độc bản / hội đủ / tái định giá / cấu trúc / phương án xử lý / etc.).

### Criterion 7 — Abbreviation expanded (V1.5 NEW)
3-4 letter uppercase first occurrence MUST be:
- Followed by `(<expansion>)`, OR
- In NATURALIZED_FINANCE_TERMS allowlist (ESOP/NIM/ROE/etc.), OR
- Is a Finpath ticker

### Criterion 8 — Plain language
No English jargon (except NATURALIZED) + no PR clickbait (cú nổ / bí mật / sốc / hot / thông tin nóng).

## Combined: `passed` flag

```python
passed = (
    ticker_present
    and word_count_le_16
    and no_em_dash
    and not_label_leak
    and not_orphan_number
    and no_han_viet_formal     # V1.5 NEW
    and abbreviation_expanded   # V1.5 NEW
    and plain_language
)
```

`has_concrete_number` is returned as info field (not part of passed flag).

## Reference

- Hán-Việt mapping: `lib/voice_rules.py::HAN_VIET_FORMAL_BAN`
- Abbreviation: `lib/quality_gates.py::check_abbreviation_expanded`
- NATURALIZED: `lib/voice_rules.py::NATURALIZED_FINANCE_TERMS`
