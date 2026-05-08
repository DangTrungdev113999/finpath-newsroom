# Expert Questions — 4 Câu hỏi tổng biên tập 15 năm

Mỗi candidate trong batch, Story Editor hỏi 4 câu trước khi quyết. Đây là examples thinking process.

## Câu 1: Insight potential

❓ Có angle "WOW" không, hay chỉ news routine?

✅ **High potential**:
- "TCB tăng vốn 60% — biggest VN bank capital raise" → angle: pattern strategic shift
- "VCB target 2026 chỉ +5% — chậm nhất Big 4" → angle: nghịch lý "biggest = slowest"
- "NHNN Thông tư 02/2026 ảnh hưởng credit room" → angle: decode policy impact

❌ **Low potential (routine)**:
- "TCB họp ĐHĐCĐ 2026" → routine, không angle
- "VCB công bố BCTC Q1" → routine, không angle ngoài số (số đã có ở DB)
- "MBB ra mắt sản phẩm tiết kiệm mới" → marketing news, không insight

## Câu 2: Data foundation

❓ DB Notion + KB + web search có data anchor để Master viết sâu không?

✅ **Strong foundation**:
- Topic về BCTC TCB Q1/2026 + DB BCTC Bank Quarter có row TCB Q1/2026 → anchor đầy đủ
- Topic về Basel III VN + KB có topic `Basel-III-CAR-VN` → anchor lịch sử

❌ **Weak foundation**:
- Topic về deal M&A confidential — DB chưa có data, web search chỉ có rumor
- Topic về quy định "sắp ra" — không có official document yet
- Topic về ngân hàng nhỏ ngoài universe (vd Eximbank) — DB không cover

## Câu 3: Timeliness

❓ Sự kiện vừa xảy ra hay đã cũ? Cũ thì có angle mới?

✅ **Timely**:
- ĐHĐCĐ TCB ngày hôm qua (Published_time 1 ngày trước)
- BCTC Q1 vừa ra
- NHNN ban hành thông tư mới tuần này

❌ **Stale (reject `not_timely`)**:
- Sự kiện 2 tháng trước, không có update mới
- Topic đã có 5 bài gần đây trong DB Generated News (variety guard catches)
- News từ 2024 không có new angle

## Câu 4: Hypothesis 1 câu

❓ Phát biểu insight 1 câu specific?

✅ **Specific 1 câu** (drives `insight_hypothesis`):
- "VCB chọn thận trọng 2026 với mục tiêu +5% — chậm nhất 4 ngân hàng quốc doanh — phù hợp NĐT giá trị giữ trên 12 tháng"
- "TCB tăng vốn 60% chuẩn bị cho M&A — chuyển hướng chiến lược đến nay rõ ràng"

❌ **Generic / không 1 câu**:
- "Phân tích kết quả Q1 TCB" (generic, không insight)
- "Bài học từ ĐHĐCĐ" (vague)
- 2-3 câu compound — phải nén thành 1 câu

## Câu 5: Angle label — bài này theo HƯỚNG nào? (V3.6)

❓ Đặt tên hướng tiếp cận của bài. Story Editor đóng vai "đầu bếp đặt menu" — chốt position của bài.

`angle_label` là **TÊN GỌI bài** (free text tiếng Việt thuần). Dùng cho:
- Variety guard (tránh 3 bài liên tiếp cùng angle)
- Compare Feed cột phải hiển thị cho sếp biết "bài này theo hướng nào"
- Phân biệt với 2-3 alternative angle khác mà Story Editor cân nhắc

### ✅ Angle label tốt (PREFERRED)

| Bài | angle_label | Vì sao tốt |
|---|---|---|
| TCB ĐHĐCĐ | "Đánh đổi chủ động — chuyển hướng chiến lược" | Decode 3 quyết định thành 1 câu chuyện thống nhất |
| VCB target +5% | "Nghịch lý 'biggest = slowest'" | Highlight mâu thuẫn quy mô vs tốc độ |
| MBB Oceanbank | "Phép tính âm thành dương" | Hint về cơ chế ẩn — kỹ thuật accounting |
| VPB +35% | "Tham vọng đo bằng quá khứ" | Đặt câu hỏi về tính khả thi của lời hứa |

### ❌ Angle label dở (AVOID)

- "TCB Q1/2026 kết quả tốt" — generic, không hint hướng tiếp cận
- "ĐHĐCĐ TCB 2026" — tóm tắt event, không decode
- "TCB strategic shift" — leak enum metadata, không tiếng Việt thuần
- "TCB chia cổ tức 67% tăng vốn 113.738 tỷ rút BĐS dưới 30%" — liệt kê facts, không gọi tên hướng

### Workflow Câu 5

Story Editor V3.6 generate **2-3 angle option** khả thi cho mỗi candidate đáng pick:
1. Pick **1 default** (rank tốt nhất theo data foundation + insight WOW + variety)
2. Flag **2-3 alternatives** với rationale ngắn cho mỗi option
3. Compare Feed cột phải hiển thị tất cả option → sếp review/override

Examples 3 angle option cho TCB ĐHĐCĐ:
- ✅ **Default**: "Đánh đổi chủ động — chuyển hướng chiến lược" (3 quyết định cùng một câu chuyện)
- 🔄 Alt 1: "Hậu Vạn Thịnh Phát — TCB chuẩn bị regulator" (focus vào áp lực bên ngoài)
- 🔄 Alt 2: "5.000 tỷ Lottner 'hy sinh' — bài toán phân khúc khách hàng" (focus vào CEO claim)

## Câu 6: Deep question — câu hỏi đào sâu cụ thể (V3.6 — gate cứng)

❓ Đặt câu hỏi cụ thể Master phải trả lời với 3-7 lý do mechanism.

`deep_question` là **ĐỀ BÀI** Master nhận được. KHÁC `angle_label` — angle là tên hướng, deep_question là câu hỏi cụ thể force Master đào.

### 5 category câu hỏi đào sâu được

Deep question MUST thuộc 1 trong 5 category dưới đây. Fail → reject `low_writeability`.

#### 🔴 Paradox — 2 dữ kiện mâu thuẫn cùng tồn tại
Force Master đào lý do thật giải thích cả 2 mặt mâu thuẫn.
- "Vì sao to nhất lại đi chậm nhất?" (VCB)
- "Vì sao 2 quyết định ngược chiều xảy ra cùng lúc?" (TCB)
- "TCB nợ xấu thấp nhất ngành nhưng giá cổ phiếu thua MBB — vì sao thị trường định giá như vậy?"

**Đặc điểm**: thường có cấu trúc "Vì sao... lại..." — từ "lại" là dấu hiệu paradox.

#### 🟠 Why now — Sự kiện không mới về bản chất, nhưng thời điểm có ý nghĩa
Force Master tham chiếu lịch sử + bối cảnh hiện tại.
- "Vì sao TCB rút BĐS bây giờ, không phải 2023 hay 2024?"
- "Vì sao bank đua tăng vốn cùng đầu 2026?"
- "Vì sao Vinhomes chuyển focus sang BĐS công nghiệp 2026?"

**Đặc điểm**: ép Master so sánh với năm trước → đào áp lực thời điểm (regulator / chu kỳ / lịch sử).

#### 🟡 Hidden mechanism — 1 claim/quyết định lớn nhưng chưa rõ điều kiện
Force Master decode điều kiện + giả định + cơ chế hỗ trợ.
- "VPB hứa lợi nhuận +35% trong khi ngành chỉ +12% — hứa nhiều thì làm được không?"
- "MBB nhận chuyển giao Oceanbank không lỗ — bằng cách gì?"
- "ACB target 2026 +20% sau 3 năm beat — pattern này còn duy trì được bao lâu?"

**Đặc điểm**: câu hỏi về tính khả thi / bí quyết / điều kiện ngầm.

#### 🟢 Comparison deep — 2 chủ thể đối xứng có triết lý khác biệt
Force Master đào triết lý + chu kỳ + hệ quả.
- "MBB chia cổ phiếu vs VCB chia tiền — 2 trường phái có gì khác?"
- "Big 4 vs tư nhân Q1/2026 — ai đặt cược đúng hơn?"
- "TCB và VPB cùng tăng vốn 60-67% — chiến lược giống nhau hay khác?"

**Đặc điểm**: không "ai thắng" mà "ai theo logic gì" — đào triết lý kinh doanh.

#### 🔵 Early signal — 1 data point bất thường → ý nghĩa + lookforward + risk
Force Master mở rộng từ 1 con số thành câu chuyện cảnh báo / theo dõi.
- "TCB CASA giảm 2,5 điểm phần trăm Q1 — chỉ số nào quyết định 2026 đúng hay sai?"
- "Tín dụng ngành âm tháng 1/2026 — báo hiệu gì cho cả năm?"
- "ACB nợ xấu nhóm 5 tăng đột biến Q1 — đợt sóng mới hay bất thường thống kê?"

**Đặc điểm**: từ 1 anomaly → mở thành câu chuyện theo dõi tương lai.

### ❌ Deep question giả (fail Câu 6 — reject low_writeability)

| Anti-pattern | Vì sao fail |
|---|---|
| **Verify factual** | "5.000 tỷ Lottner nói — số đó từ đâu ra?" — 1 phép tính arithmetic, không có 3-7 mechanism độc lập |
| **Yes/No** | "TCB có chuyển hướng chiến lược không?" — đáp án 1 từ |
| **Single fact** | "Tăng trưởng tín dụng quý 1 bao nhiêu?" — tra DB là xong |
| **Generic too broad** | "Ảnh hưởng thế nào?" / "Có gì đáng chú ý?" — không bound được, Master không biết đào hướng nào |
| **Câu hỏi giả** | "TCB hy sinh 5.000 tỷ để đổi lấy gì?" — có dấu "?" nhưng câu trả lời ngầm = "thanh khoản", không 3-7 lý do để đào |

### Workflow Câu 6

1. Story Editor có angle_label rồi (Câu 5)
2. Reformulate thành deep_question phù hợp 1 trong 5 category
3. Test deep_question: đếm xem có 3-7 mechanism độc lập trả lời được không (mỗi mechanism từ thế giới khác nhau: regulator / market structure / industry cycle / customer side / lịch sử / phép tính)
4. Nếu < 3 mechanism → câu hỏi quá hẹp, refactor hoặc reject
5. Nếu > 7 mechanism → câu hỏi quá rộng, scope down

Examples Câu 5 → Câu 6 mapping:

| angle_label | deep_question_category | deep_question |
|---|---|---|
| Đánh đổi chủ động — chuyển hướng chiến lược | paradox | Vì sao 2 quyết định ngược chiều xảy ra cùng lúc? |
| Nghịch lý "biggest = slowest" | paradox | Vì sao ngân hàng to nhất lại đi chậm nhất? |
| Phép tính âm thành dương | hidden_mechanism | MBB nhận chuyển giao Oceanbank không lỗ — bằng cách gì? |
| Tham vọng đo bằng quá khứ | hidden_mechanism | VPB hứa +35% — hứa nhiều thì làm được không? |
| 2 trường phái lệch quỹ đạo | comparison_deep | Big 4 vs tư nhân Q1/2026 — ai đặt cược đúng hơn? |

## Quyết định pick/reject

```
6/6 strong → PICK (top 1-3)
5/6 strong (Câu 6 fail) → REJECT low_writeability — deep_question không đào được
4/6 strong → REJECT (specify which 2 weak)
≤3/6 strong → REJECT
```

## Why_chosen format

Sau khi pick, write `why_chosen` 3+ câu cho sếp đọc Compare Feed cột phải:

✅ Example:
> Bài này pick vì: (1) Data foundation mạnh — DB BCTC Bank Quarter có TCB Q1/2026 đầy đủ + KB có topic Lottner-era + Big4 pattern. (2) Insight WOW — "TCB tăng vốn 60% biggest" là pattern strategic shift hiếm thấy với bank tư nhân. (3) Timely — ĐHĐCĐ vừa xảy ra ngày 25/4, breaking. Memory check: 3 bài TCB gần nhất khác angle (1 về NPL trái phiếu, 1 về CFS Q4, 1 về Lottner liquidity) → variety OK.

❌ BAD why_chosen:
> Bài về TCB ĐHĐCĐ. (1 câu, không đủ depth)
