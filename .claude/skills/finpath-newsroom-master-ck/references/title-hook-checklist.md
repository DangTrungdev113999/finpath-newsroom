# Title Hook Checklist V4.0 (CK)

Master MUST đọc checklist này TRƯỚC khi finalize title bài viết CK. Hook quality = first impression — title kém → user skip dù body có insight.

## 5-second test

Đọc title 5 giây. User có thấy ngay:
- Angle nào (nghịch lý / vì sao / thay đổi mô hình / cạnh tranh thị phần)?
- Đối tượng cụ thể (ticker)?
- Tension hoặc số "đắt giá"?

Nếu user phải đọc 2 lần mới hiểu → hook fail.

## Preference order (1 = best, 4 = avoid)

1. **Quote trực tiếp** — `"Chấp nhận giảm biên để giữ thị phần" — Chủ tịch VCI nói gì về 2026?`
   - Lấy quote thực từ Chủ tịch / Tổng giám đốc / báo cáo thường niên. Tăng credibility + emotion.

2. **Câu hỏi tò mò** — `Vì sao SSI tăng vốn 4.155 tỷ đúng lúc thị trường co?`
   - 1 câu hỏi sharp, KHÔNG parallelism awkward. Câu hỏi nên về MECHANISM hoặc REASON, không về fact.

3. **Nghịch lý declarative** — `VCI mất thị phần môi giới — bù lại bằng ngân hàng đầu tư 84% biên lãi?`
   - State 2 facts đối nghịch → em-dash → sharpen với question hoặc ý chính. Đọc 1 lần hiểu.

4. **Tóm tắt sự kiện** (LAST RESORT) — `SSI Q1/2026 lãi 1.200 tỷ vượt VND`
   - Chỉ dùng khi sự kiện quá lớn không cần hook. Risk: bài liệt kê → user complain.

## Anti-patterns — TRÁNH

### A1. Parallelism awkward "Vì sao X vẫn Y?"
- ❌ "Vì sao SSI vừa tăng vốn 4.155 tỷ vẫn giảm dư nợ ký quỹ?"
- Lý do fail: 2 sự kiện trong 1 câu hỏi → reader phải parse "vừa X vẫn Y" mất 2-3 giây. Hook 5s test fail.
- ✅ Sửa: "SSI tăng vốn 4.155 tỷ giữa lúc dư nợ ký quỹ co — vì sao gọi vốn trước, cho vay sau?"
  - Nghịch lý declarative + sharpen với câu hỏi MECHANISM.

### A2. PR-friendly verbose
- ❌ "SSI đẩy mạnh chiến lược tăng trưởng đa dịch vụ trong bối cảnh thị trường biến động"
- Lý do fail: PR boilerplate, không có angle, không có số.
- ✅ Sửa: "SSI dồn 4.155 tỷ vốn mới vào cho vay ký quỹ — bù lại bằng ngân hàng đầu tư?"

### A3. 2 sự kiện không phải nghịch lý
- ❌ "SSI doanh thu tăng và lợi nhuận tăng Q1/2026"
- Lý do fail: 2 sự kiện cùng chiều, không tension.
- ✅ Sửa: "SSI doanh thu tăng Q1 nhưng biên lợi nhuận môi giới co — bào mòn phí thật?"

### A4. Clickbait fake
- ❌ "Sốc: VCI vừa làm điều không tưởng"
- Lý do fail: empty hype, không có insight, không có số.

### A5. Question về fact
- ❌ "SSI lãi bao nhiêu Q1/2026?"
- Lý do fail: hook về fact thì body phải answer fact → bài liệt kê.
- ✅ Question phải về MECHANISM, REASON, INTERPRETATION:
  - "Vì sao SSI vẫn dẫn đầu thị phần dù bào mòn phí 4 năm liên tiếp?" (MECHANISM)
  - "SSI chấp nhận đánh đổi gì để giữ ngôi đầu thị phần?" (TRADE-OFF reasoning)

### A6. Marketing language / outlook generic
- ❌ "Triển vọng ngành chứng khoán 2026 — cơ hội và thách thức"
- Lý do fail: generic outlook, không ticker cụ thể, không tension.
- ✅ Sửa: "VCI hưởng lợi sớm nhất từ FTSE — vì sao không phải SSI hay HCM?"

## Tension words bắt buộc (Rule 2)

Title MUST chứa `?` HOẶC `—` + ≥1 trong các từ sau:
- `hy sinh`
- `đánh đổi`
- `nghịch lý`
- `vì sao`
- `đổi lấy`
- `không phải`
- `bù lại`
- `thay vì`
- `chấp nhận`

Không có tension word → fail mechanical gate `title_as_hook`.

## Self-check trước finalize

1. Đọc title 5 giây — hiểu angle?
2. Title chứa `?` HOẶC `—` HOẶC tension word? (Mechanical gate đã check)
3. KHÔNG anti-pattern A1-A6?
4. Title preference rank ≤ 3 (tránh A4 — tóm tắt sự kiện)?
5. 0% từ tiếng Anh trong title (kể cả viết tắt margin/IB/AUM)?

Nếu fail bất kỳ → rewrite title trước khi persist.

## Examples — concrete bad → good (CK sector)

| Bad | Good rewrite |
|---|---|
| SSI Q1/2026 lãi 1.200 tỷ tăng 18% | SSI tăng vốn 4.155 tỷ — vì sao đúng lúc thị trường co? |
| Triển vọng ngành chứng khoán 2026 | VCI hưởng lợi sớm nhất từ FTSE — vì sao không phải SSI hay HCM? |
| Vì sao VCI vừa giảm phí vẫn giữ biên lãi 84%? | VCI chấp nhận biên lãi môi giới giảm để giữ thị phần — đáng không? |
| VND báo cáo doanh thu Q1 môi giới giảm 12% | VND mất thị phần môi giới Q1 — bù lại bằng đâu? |
| HCM tăng dư nợ ký quỹ 35% YoY | HCM đẩy dư nợ ký quỹ chạm 180% vốn chủ — sắp phải tăng vốn? |
| SHS phát hành 5.000 tỷ trái phiếu doanh nghiệp | SHS gọi vốn 5.000 tỷ thay vì phát hành cổ phiếu — đánh đổi gì? |

## Sector-specific anchor angles (gợi ý hook cho CK)

CK có 4 chu kỳ cạnh tranh thường xuất hiện trong hook:

1. **Thị phần môi giới HOSE/HNX**: ai mất, ai được, ai chấp nhận đánh đổi để giữ
2. **Trần 200% vốn chủ** cho dư nợ ký quỹ: ai gần trần phải tăng vốn
3. **Bào mòn phí**: ai chống được, ai chấp nhận giảm để giữ khách
4. **Ngân hàng đầu tư + TPDN**: ai phục hồi sau 2022, ai vẫn cẩn trọng

Mỗi angle anchor có tension built-in — dễ build hook hơn so với "doanh thu tăng" generic.
