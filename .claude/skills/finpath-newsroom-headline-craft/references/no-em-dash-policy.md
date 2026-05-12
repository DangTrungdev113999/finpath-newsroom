# No Em Dash Policy — Headline V1.1 PATCH

> Em dash `—` (U+2014) BANNED trong title. AI-tell signal — model nào cũng dùng em dash dễ nhận.

## Why ban

User feedback 2026-05-12: "bỏ cái dấu —, nhìn dấu này là biết AI viết bài rồi".

Em dash là tell-tale của AI text generation:
- ChatGPT default style heavy em dash
- Claude default style heavy em dash
- Human Vietnamese writers thường dùng phẩy `,` hoặc xuống dòng

Loại bỏ em dash → giảm "AI vibe" rõ rệt.

## Detection

```python
def has_em_dash(title: str) -> bool:
    return "—" in title  # U+2014 ONLY
```

Phân biệt 3 character:
- `—` U+2014 EM DASH → BANNED
- `–` U+2013 EN DASH → acceptable
- `-` U+002D HYPHEN-MINUS → acceptable

## Body density

Em dash trong body (NOT title) OK nhưng giới hạn: max 1 em dash per 100 từ body. Quá → AI vibe rõ. Enforce qua `check_em_dash_density()` gate.

## Substitution patterns

Thay vì:
- "TCB lãi 30% — cổ phiếu giảm 6%"

Dùng:
- "TCB lãi 30%, cổ phiếu giảm 6%" (phẩy)
- "TCB lãi 30% nhưng cổ phiếu giảm 6%" (liên từ)
- "TCB lãi 30% trong khi cổ phiếu giảm 6%" (liên từ)
- "TCB lãi 30%. Cổ phiếu giảm 6%." (chấm hết câu — nếu dài)

## V1.0 → V1.1 migration

V1.0 cho phép em dash trong "Declarative tension" lối. V1.1 PATCH BAN entirely. Update Declarative tension examples: dùng phẩy hoặc liên từ.
