# Hard Criteria — Headline Craft V1.3

> Loaded from `Skill: finpath-newsroom-headline-craft`. ALL criteria MUST pass for title to persist.

## V1.3 PATCH (2026-05-13)

User feedback: "STB xén 85% mà ngành còn lại vẫn tuyển?" — 85% gì? ngành nào? Hook V1.2 word cap ≤12 + rubric `extra_concise +1` ép sacrifice clarity.

3 changes:
1. **Word cap relaxed**: ≤12 → ≤16 (clarity > conciseness)
2. **New criterion `not_orphan_number`**: số/percent phải có subject, "ngành/nhóm" phải có specifier
3. **Rubric replaced**: `extra_concise (≤10) +1` → `self_explanatory (≤14 AND no_orphan) +1` (sweet spot balance)

## Criterion 1 — Ticker present

**Test**: `has_ticker(title)` from `lib.headline_scorer`.

- Detect 139-mã universe ticker OR group ref (Big4, tư nhân, Big5, Big3)
- "STB xén 2.700 người..." → STB
- "Q1 ngành bank phân hóa..." → no ticker yet, but if mentions VPB+TCB+LPB OK
- "Ngân hàng lớn nhất hy sinh..." → no ticker / group ref (fail)

## Criterion 2 — Compact ≤16 từ (V1.3 relaxed)

**Test**: `len(title.split()) <= 16`.

- V1.2 was ≤12 — ép quá ngắn → orphan number / vague reference
- V1.3 allows 16 từ để clarity demand
- "STB sa thải 2.700, VPB tuyển 362. Bank nào đúng?" → 10 từ (pass)
- "Q1 ngành bank phân hóa: STB tống 2.700, VPB+TCB+LPB nhồi thêm 700. Bank nào sai?" → 16 từ (pass, clarity-driven)

## Criterion 3 — Hook strong (nested dict 2 sub-tests)

**Return shape**: `{tension_present: bool, click_test_pass: bool}`. BOTH must be True.

### sub-test: tension_present
- ≥1 dramatic verb (hy sinh / đánh đổi / ăn / khoe / dồn / xén / gom / bơm / tống / nhồi / phân hóa / sa thải)
- OR ≥1 tension word (vì sao / nghịch lý / không phải / bù lại)
- OR paradox pattern (X mà Y / thật ra / kỳ thực)
- OR concrete_question_subject (ai gom / tiền chạy đâu / khôn hay liều / bank nào sai)

### sub-test: click_test_pass
- ≥1 specific number — V1.3 expanded:
  - Financial unit (5.000 tỷ / 67% / 250 đ)
  - Headcount unit (2.700 người / 14.080 nhân viên)
  - Bare ≥4-digit number (2.700 / 11.026)
- OR open question (ends with `?`)
- OR dramatic verb

## Criterion 4 — Bình dân nguy hiểm (nested dict 2 sub-tests)

**Return shape**: `{plain_language: bool, sharp_edge: bool}`. BOTH must be True.

### sub-test: plain_language
- NO English jargon (NIM / CASA / NPL / momentum / ...)
- NO PR clickbait (cú nổ / bí mật / sốc / hot / thông tin nóng)

### sub-test: sharp_edge
- ≥1 dramatic verb / specific number / tension word / paradox pattern

## Criterion 5 — No em dash (V1.1 PATCH preserved)

**Test**: `"—" not in title` (U+2014 only).

## Criterion 6 — Not bao_chi (V1.2 PATCH preserved)

Reject báo chí formulaic phrases: "đánh đổi gì / để đổi lấy / hy sinh để / đặt mục tiêu / lao dốc / bứt phá / Q1/2026 X lãi Y".

## Criterion 7 — Not label_leak (V1.2 PATCH preserved)

Reject rubric label as title ("Question" / "Declarative tension" / "Quote" / "Contrast verb" / "Lối X:").

## Criterion 8 — NOT orphan number (V1.3 NEW) ⭐

**Test**: `not has_orphan_number(title)`.

Reader test 5 giây: title đứng độc lập, mọi number/percent phải có subject explicit.

### Sub-rule a: Số/percent có subject trong 4 token kế tiếp

NOUN_HINTS subset: người / nhân / viên / tỷ / triệu / nghìn / đồng / lợi / nhuận / doanh / thu / vốn / cổ / phiếu / tiền / nợ / lãi / năm / tháng / quý / kỳ / cùng / trên / dưới / vượt / thấp / cao.

```
❌ "STB xén 85% mà ngành còn lại vẫn tuyển?" — 85% no noun within 4 tokens
✅ "STB xén 85% nhân sự ngành bank Q1?" — 85% nhân sự (noun ngay sau)
✅ "DXG bán hàng vọt 46%, lãi mẹ tụt 22%. Tiền chạy đâu?" — 46% (hàng OK before) / 22% (mẹ OK)
```

### Sub-rule b: "ngành/nhóm/khu vực" có specifier trong window 3 tokens trước+sau

REFERENCE_SPECIFIERS: bank / ngân hàng / tư nhân / Big4 / BĐS / CK / chứng khoán / dầu khí / logistics / FB / retail / bán lẻ / seafood / thuỷ sản / apparel / dệt may / defensive / phòng thủ / tài chính / công nghệ / điện.

```
❌ "VHM cứu ngành sau khủng hoảng?" — "ngành" no specifier
✅ "STB ôm 85% nhân sự cắt giảm ngành bank Q1, lạ?" — "ngành bank" specifier
✅ "Big4 nhồi tư nhân chạy. Nhóm BĐS đứng nhìn." — "nhóm BĐS" specifier
```

## Combined: `passed` flag V1.3

```python
passed = (
    ticker_present
    and word_count_le_16              # V1.3 relaxed
    and hook_strong["tension_present"] and hook_strong["click_test_pass"]
    and binh_dan_nguy_hiem["plain_language"] and binh_dan_nguy_hiem["sharp_edge"]
    and no_em_dash
    and not_bao_chi
    and not_label_leak
    and not_orphan_number             # V1.3 NEW ⭐
)
```

Validation enforced at persist: `lib.pipeline_db.validate_pipeline_step('step_4_5_headline_craft', ...)`. Fail → ValueError + halt pipeline.

## Reference pools

### Dramatic verb pool (V1.3 expanded with bình dân + restructuring)

```
hy sinh · đánh đổi · đặt cược · lội ngược · rút khỏi · vượt mặt ·
ăn (lãi/ưu đãi/lời) · khoe · dồn · xén · gom · bơm · đẻ · ngồi trên ·
vọt · tụt · rớt · nhảy · gọi vốn · chia kỷ lục · đổi tên · đổi hướng ·
bán hàng · bán ESOP · thật ra · thực ra ·
tống · nhồi · sa thải · lùa · rước · phân hóa · ngược chiều · cắt sâu (V1.3)
```

### Concrete question subjects (V1.3 expanded)

```
ai gom · ai trả · ai bán · ai chạy · ai thoát ·
tiền đâu · tiền chạy · sợ gì · lo gì · khôn hay liều · đúng hay sai ·
bao giờ · khi nào · trước ngày · lạ? · thật? ·
nào sai · nào đúng · ai thắng · ai thua · bên nào · kẻ nào · phe nào · nhóm nào (V1.3)
```

### Specific number patterns V1.3

```python
# Financial unit
r"\d+([.,]\d+)?\s*(tỷ|triệu|nghìn|%|đ|/năm|/tháng|/quý|bps|điểm)"
# Headcount unit
r"\d+([.,]\d+)?\s*(người|nhân viên|nhân sự|lao động|cổ phiếu|cp)"
# Bare ≥4-digit (2.700 / 11.026)
r"\b\d{1,3}[.,]\d{3,}\b"
```

### PR clickbait blacklist

```
cú nổ · bí mật · sốc · hot · thông tin nóng · không thể tin nổi ·
cú twist · kỳ tích · hé lộ · kỷ tích
```
