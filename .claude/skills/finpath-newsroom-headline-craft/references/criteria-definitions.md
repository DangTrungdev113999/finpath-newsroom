# 7 Hard Criteria — Headline Craft V1.8 (objective rejects, NOT craft rubric)

> 7 objective rejects via `lib.headline_scorer.check_hard_criteria()`. ALL must pass — agent re-craft nếu fail. KHÔNG dùng để craft, dùng để filter sau.

## V1.6+ shift (2026-05-13 evening)

V1.5-lite có 8 hard + 6-point rubric — rubric pulled agent into Pattern A pile-on (force concrete_number + paradox marker). V1.6 dropped `not_orphan_number` to soft hint. V1.8 simplifies further: 7 hard = SAFETY NET only. Craft = agent judgment + 7 expert benchmark in `professional-patterns.md`.

## 7 hard criteria

1. **ticker_present** — Finpath 139+ universe OR full brand name (Petrolimex / PV GAS / Vietcombank)
2. **word_count_le_16** — `len(title.split()) <= 16`
3. **no_em_dash** — `—` (U+2014) BANNED. Hyphen `-` + en dash `–` OK.
4. **not_label_leak** — reject "Question:" / "Lối X:" / "Declarative tension" / "Quote" / "Contrast verb" bare prefix
5. **no_han_viet_formal** — title không chứa `lib/voice_rules.py::HAN_VIET_FORMAL_BAN` (độc bản / hội đủ / tái định giá / cấu trúc / phương án xử lý / etc.)
6. **abbreviation_expanded** — 3-4 letter uppercase MUST be: expansion in parentheses on first use OR in `NATURALIZED_FINANCE_TERMS` allowlist (ESOP/NIM/CASA/ROE/ETF/IPO/...) OR Finpath ticker
7. **plain_language** — no English jargon (except NATURALIZED) + no PR clickbait (cú nổ / bí mật / sốc / hot / thông tin nóng)

## Info-only fields (soft hints, NOT in `passed`)

- `not_orphan_number` — số/% phải có subject within 4 tokens (V1.3 detector, V1.6 demoted to soft)
- `has_concrete_number` — has specific number + subject (info)
- `vague_action_verbs` — list of vague verbs detected (ăn/che/nguy/mắc/đẻ/đốt without concrete object)

Agent đọc soft hints → tự cân nhắc rewrite. KHÔNG halt pipeline.

## Reference

- 7 criteria implementation: `lib/headline_scorer.py::check_hard_criteria()`
- Vague verb detector: `lib/headline_scorer.py::detect_vague_action_verb()`
- 7 expert benchmark + craft principles: `professional-patterns.md`
- Em dash detection: `no-em-dash-policy.md`
