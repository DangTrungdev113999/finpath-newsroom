# Format: flash_qa (80-120 từ) — V1.3 Twitter-style

> Loaded from `Skill: finpath-newsroom-master-defensive`. Apply khi `format_id == "flash_qa"`.

## Khi nào dùng

Ticker_status = Hot (top tăng/giảm/bùng nổ/cạn cung) + data_richness ∈ {low, medium}. Người đọc cần info nhanh khi mã đang nóng.

## Body pattern V1.3 (Twitter style)

```
[Opening ≥15 từ: question chính hoặc fact gây tension, có **bold key**]

[Body paragraph 50-80 từ: answer + 1-2 con số **bold** + analogy/metaphor]

[Closing ≤25 từ: stance + quantified trigger + timeframe]
```

- KHÔNG bullet
- KHÔNG heading "## Cần để ý"
- Max 1 em dash / bài
- **≥3 bold absolute** (V1.3 hard cap — Twitter scan needs key signals visible)

## Word count

- Total: **80-120 từ** HARD CAP (V1.3 shrunk from 100-150)
- Opening: ≥15 từ
- Body paragraph: 50-80 từ
- Closing: ≤25 từ

## Voice (V6 + V7 + V3 enforced)

- **Bold density**: ≥3 bold/bài absolute count
- **NO báo chí verbs** ≥2 (V6.1): cấm "bàn giao/ghi nhận/công bố/dự kiến/phát hành" combo
- **Prefer bình dân verbs** (V6.2): "ăn/khoe/dồn/xén/gom/bơm/ngồi trên"
- **Closing actionable** (V3): stance + số/condition + timeframe — không "cần theo dõi"

## Examples V1.3 — Defensive sector

### ✅ Example 1: VCB +6.8% Hot (110 từ)

> **Vietcombank vọt 6,8%** sáng 12/5 sau khi **ăn lãi quý 1 vượt 11%** so cùng kỳ. Vì sao thị trường phản ứng mạnh đến vậy?
>
> Lãi nhảy nhờ **biên lãi vay nới từ 3,1% lên 3,3%**, huy động giá rẻ kéo nguồn về. Nợ xấu **0,9%**, tỷ suất sinh lời tài sản giữ ổn định 1,8%. **Tín dụng quý 1 tăng 3,5%** cao hơn ngành. Thực ra VCB đang ăn được phần lợi chu kỳ NHNN nới — không phải tăng nóng tín dụng.
>
> NĐT giá trị nên cầm trên 92.000, mục tiêu 100-105 trong 12 tháng.

### ✅ Example 2: TCB -6.5% Cold panic (115 từ)

> **Techcombank tụt sàn 6,5%** sau tin **nợ xấu nhóm 2 nhảy 2,4%**, vì sao thị trường panic dù lãi quý vẫn tăng?
>
> Panic chủ yếu lo lan sang nhóm 3-4. Nhưng thật ra **nợ xấu nhóm 2 từ 1,8% → 2,4%** chủ yếu là BĐS tái cơ cấu, không phải tín dụng tiêu dùng mới. **Buffer dự phòng +28% Q1**. TCB đang xén lãi ngắn hạn để gia cố vùng đệm trước rủi ro chu kỳ.
>
> NĐT giá trị tin chiến lược phòng thủ nên cầm 18 tháng; short-term FOMO nên tránh dưới 32.

### ❌ Example xấu V1.3 reject

> Vietcombank ghi nhận lợi nhuận quý 1/2026 vượt 11% so cùng kỳ, đồng thời công bố tăng trưởng tín dụng 3,5%. Ngân hàng đặt mục tiêu hoàn thành kế hoạch 8% năm 2026 và dự kiến đạt tăng trưởng nợ vay tốt. Nhà đầu tư cần theo dõi diễn biến quý 2 làm chỉ báo sớm cho quyết định đầu tư.

→ Fail: 4 báo chí verbs (ghi nhận, công bố, đặt mục tiêu, dự kiến đạt) + closing vague "cần theo dõi làm chỉ báo" + 0 bold.

### ❌ V1.5-lite bad examples — DO NOT invent verb-noun combos

| Pattern | Bad example | Fix |
|---|---|---|
| Verb tự chế | "FPT chấm đích Huế" | "FPT chọn Huế / FPT nhắm tới Huế" |
| Verb cưỡng ép | "vọt lãi" (title) | "lãi vọt / lãi tăng vọt" |
| Verb sai ngữ cảnh | "VCBS chấm 111.421 đồng" | "VCBS định giá 111.421 đồng" |
| Hán-Việt formal | "8 di sản UNESCO độc bản" | "8 di sản UNESCO duy nhất" |
| Hán-Việt formal | "chưa hội đủ điều kiện" | "chưa đủ điều kiện" |
| Abbreviation chưa expand | "BCA nhận 50% vốn" | "Bộ Công An (BCA) nhận 50% vốn" |
| Fabricated price | "FPT dưới 145 nghìn/cp" (FPT thực tế 70 nghìn) | Fetch Finpath current → target ±50% |

Self-test 5 giây: reader bình dân chưa từng nghe combo đó → rewrite.

## Verdict line (V3)

Closing MUST có 5 elements:
1. Stance ("nên cầm/giảm/cắt/thoát") HOẶC "phù hợp NĐT X / không phù hợp NĐT Y"
2. Quantified trigger (giá / percent / điều kiện)
3. Timeframe (12 tháng / Q3/2026 / ngắn-dài hạn)
4. Holder context
5. NO `CLOSING_VAGUE_BAN` ("cần theo dõi" / "làm chỉ báo" / "đánh giá thêm")
