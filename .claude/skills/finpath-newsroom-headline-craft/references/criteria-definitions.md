# 5 Hard Criteria — Headline Craft V1.1

> Loaded from `Skill: finpath-newsroom-headline-craft`. ALL 5 MUST pass for title to persist.

## Criterion 1 — Ticker present

**Test**: `has_ticker(title)` from `lib.headline_scorer`.

- Detect 139-mã universe ticker OR group ref (Big4, tư nhân, Big5, Big3)
- Regex `\b[A-Z]{3,4}\b` matches uppercase 3-4 letter sequences
- "TCB hy sinh 5.000 tỷ..." → TCB
- "Big4 tăng tốc 4,3%..." → Big4 group ref
- "Ngân hàng lớn nhất hy sinh..." → no ticker / group ref (fail)

## Criterion 2 — Compact ≤12 từ

**Test**: `len(title.split()) <= 12`.

- Vietnamese word split by whitespace
- "TCB hy sinh 5.000 tỷ/năm để đổi lấy gì?" → 9 từ (pass)
- "TCB hy sinh năm tỷ đồng trong năm 2026 để đổi lấy gì cho tương lai dài hạn" → 16 từ (fail)

## Criterion 3 — Hook strong (nested dict 2 sub-tests)

**Return shape**: `{tension_present: bool, click_test_pass: bool}`. BOTH must be True.

### sub-test: tension_present
- ≥1 dramatic verb (hy sinh / đánh đổi / lao dốc / ...)
- OR ≥1 tension word (vì sao / đánh đổi / nghịch lý / ...)
- OR paradox pattern (X mà Y / thật ra / kỳ thực)

### sub-test: click_test_pass
- ≥1 specific number with units (5.000 tỷ / 67% / /năm)
- OR open question (ends with `?`)
- OR dramatic verb (overlap with tension)

"click test" = đọc 5 giây, reader có muốn biết "vì sao" không? Concrete signals = number / question / dramatic.

## Criterion 4 — Bình dân nguy hiểm (nested dict 2 sub-tests)

**Return shape**: `{plain_language: bool, sharp_edge: bool}`. BOTH must be True.

### sub-test: plain_language
- NO English jargon (NIM / CASA / NPL / NIM expansion / momentum / ...)
- NO PR clickbait (cú nổ / bí mật / sốc / hot / thông tin nóng)

### sub-test: sharp_edge
- ≥1 dramatic verb / specific number / tension word / paradox pattern
- (Avoid bland: "TCB tăng trưởng tốt năm 2026" — pass plain_language but fails sharp_edge)

## Criterion 5 — No em dash (V1.1 PATCH)

**Test**: `"—" not in title` (U+2014 only).

- "TCB hy sinh 5.000 tỷ — đổi lấy gì?" — em dash present (fail)
- "TCB hy sinh 5.000 tỷ, đổi lấy gì?" — comma OK
- "TCB hy sinh 5.000 tỷ - đổi lấy gì?" — hyphen U+002D OK
- "TCB hy sinh 5.000 tỷ – đổi lấy gì?" — en dash U+2013 OK

## Combined: `passed` flag

```python
passed = (
    ticker_present
    and word_count_le_12
    and hook_strong["tension_present"] and hook_strong["click_test_pass"]
    and binh_dan_nguy_hiem["plain_language"] and binh_dan_nguy_hiem["sharp_edge"]
    and no_em_dash
)
```

Validation enforced at persist: `lib.pipeline_db.validate_pipeline_step('step_4_5_headline_craft', ...)`. Fail → ValueError + halt pipeline.

## Reference pools

### Dramatic verb pool

```
hy sinh · đánh đổi · đặt cược · bỏ phiếu · lội ngược · lao dốc ·
rút khỏi · vượt mặt · tung đòn · đặt cọc · chấp nhận thua ·
tự chậm lại · đập cửa · thoát hiểm · chấp nhận hi sinh · đánh cược ·
đổ vỡ · vực dậy · tiếp đà · phá kỷ lục · soán ngôi · lấn sang · rơi vào
```

### Tension word pool (lib/headline_scorer V5.1.3)

```
hy sinh · đánh đổi · nghịch lý · vì sao · đổi lấy · không phải ·
bù lại · thay vì · chấp nhận
```

(Note: "hy sinh" + "đánh đổi" overlap dramatic_verbs — both count cho scoring.)

### PR clickbait blacklist

```
cú nổ · bí mật · sốc · hot · thông tin nóng · không thể tin nổi ·
cú twist · kỳ tích · hé lộ · kỷ tích
```

### Specific number regex

```python
r"\d+([.,]\d+)?\s*(tỷ|triệu|nghìn|%|đ|/năm|/tháng|/quý|đ/tháng|bps|điểm)"
```
