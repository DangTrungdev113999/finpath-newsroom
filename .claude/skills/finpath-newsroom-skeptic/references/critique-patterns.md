# Critique Patterns — 6 Angles V2.4

Examples per critique angle. Skeptic pick 1 angle dựa trên Pass 1 (fresh impression) + Pass 2 (compare editorial intent).

## 1. data_skepticism

Khi dùng: Master claim số cụ thể nhưng context unclear hoặc số có thể bị manipulated.

Pattern:
> Số X% Master đưa ra là [quarterly|annualized|YoY|YTD]? Nếu khác → ý nghĩa khác hẳn.
> Hoặc: số X có thể là [end-of-period|average|peak]? Khác nhau ý nghĩa.

Example:
> Master nói "VCB NIM 3.2%" — nhưng đây là NIM annualized hay quý? Nếu là số quý (annual = 3.2% × 4 = 12.8% — không hợp lý), thì NIM thực tế chỉ 0.8% mỗi quý — thấp hơn peer ngành (1.0% trung bình). Cần Master clarify metric.

## 2. historical_analog

Khi dùng: Master không tham chiếu lịch sử + có analog quan trọng.

Pattern:
> Tình huống tương tự [năm X]: [event]. Khi đó kết cục [Z]. Đáng để nhớ trước khi kết luận.

Example (Bank):
> Master kết luận TCB tăng vốn 60% là positive. Nhưng nhớ 2018: ACB tăng vốn ~50% trong 12 tháng → 6 tháng sau pha loãng EPS, giá rớt 30% trước khi recover. Lịch sử cho thấy capital raise kèm risk pha loãng nếu deploy không hiệu quả ngay.

Example (BĐS):
> Master kết luận VHM Q1 doanh thu +30% là momentum mạnh. Nhưng 2022 cũng tăng tương tự rồi sụp pre-sales. Cần verify pre-sales Q1 thực tế trước khi confirm momentum.

## 3. alt_interpretation

Khi dùng: Master đọc data 1 cách, có cách đọc ngược hợp lý không kém.

Pattern:
> Master đọc data X là dấu hiệu A. Nhưng nhìn từ peer Y cùng kỳ → có thể là dấu hiệu B (ngược lại).

Example:
> Master đọc "VCB target 2026 +5% = defensive". Cách đọc khác: VCB 2025 đã LNTT +18%, nếu target +5% còn nghĩa là expect Q2-Q4 chậm hẳn — không phải defensive mà là "Big 4 đang concern outlook H2 2026". Đây là warning chứ không chỉ là conservatism.

## 4. risk_highlight

Khi dùng: Master không raise risk Master nên raise.

Pattern:
> Master không nhắc đến [risk Z]. Lịch sử [năm X] cho thấy đây là risk lớn cần để ý.

Example:
> Master không nhắc đến concentration risk: TCB cho vay BĐS chiếm 40%+ portfolio. Nếu chu kỳ BĐS xuống (2022 lặp lại?), TCB exposure cao hơn VCB. NĐT cần weight risk này vào đánh giá momentum hiện tại.

## 5. insight_wrong ⭐ V2.4

Khi dùng: Insight Master finalize CONFLICT với data thực tế — vấn đề ở Story Editor judgment hoặc Master Bước 7.5.

Pattern:
> Insight nói "[X]" nhưng data thực tế cho thấy "[Y]" — insight pick sai.

Example:
> Master finalize insight "VCB defensive — chậm nhất Big 4". Nhưng query DB Q1/2026 cho thấy VCB tín dụng +4.1% > VPB +3.8% > BID +3.5%. VCB không phải chậm nhất. Insight chosen wrong từ đầu (Story Editor lỗi) hoặc Master Bước 7.5 không catch (Master lỗi). Cần re-frame angle khác — vd "VCB target 5% nhưng actual có thể vượt 2-3x".

## 6. execution_unfaithful ⭐ V2.4

Khi dùng: Insight đúng nhưng bài viết execute lệch — vấn đề ở Master writing.

Pattern:
> Insight nói "[X về ticker A]" nhưng bài talks [Y% nội dung] về [topic khác]. Reader đọc xong rút ra impression sai.

Example:
> Insight "VCB defensive 2026". Nhưng bài viết 60% talks về VPB +35% target — readers đọc xong impression chính là VPB momentum, không phải VCB defensive. Body off-topic so với insight chosen. Cần restructure để body match insight.

## Variety guard pattern

Memory query last 3 critique cùng ticker:
```python
recent = query_data_sources(
    data_source_id="74a01cc3-c3c4-4dbe-a43f-c7572fa68d20",
    sql="""
        SELECT "Critique angle" FROM data_source 
        WHERE "Ticker" = 'VCB' AND "Skeptic_review_full" IS NOT NULL
        ORDER BY "date:Published at:start" DESC LIMIT 3
    """
)

# Nếu 3 cùng angle (vd 3 lần data_skepticism) → MUST pick khác cho lần này
forbidden_angles = [r["Critique angle"] for r in recent if recent.count(r) >= 3]
```
