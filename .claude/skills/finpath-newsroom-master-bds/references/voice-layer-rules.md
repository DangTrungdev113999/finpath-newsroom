# Voice Layer 7 Rules — Master BĐS V1.3

> Loaded from `Skill: finpath-newsroom-master-bds`. Apply CROSS-CUTTING toàn bộ 4 format (flash_qa / standard_qa / standard_listicle / standard_narrative).

V1.3 (2026-05-13) — Body voice "bình dân xuồng xã nguy hiểm" parallel V1.2 title rules. User feedback: body audit 5 bài bold density TB 1.83% (cần ≥4%), 3/5 closing vague "theo dõi X làm chỉ báo", top 3 báo chí verbs "bàn giao/ghi nhận/công bố/dự kiến/phát hành" → kill stance + actionability.

Voice rules orthogonal với 11 quality gates V5.1.2 + V1.3 — both layers áp dụng đồng thời.

---

## V1 — Stance required

Bài MUST có quan điểm rõ. Nhận `stance_directive` từ brief (schema + apply rules: see `stance-directive-handler.md`).

Stance = direction (bullish/bearish/divergent) + confidence (high/medium/low) + key_evidence.

Bài không có stance → fail V1. Bài "đưa thông tin trung lập" không acceptable — đó là feed wire, không phải tin chuyên gia.

---

## V2 — No-hedging (LLM-as-judge V5.1.2 PATCH)

### Định nghĩa "ba phải" (hedging)

Câu khẳng định trung tính không cam kết hướng nào, có thể đúng dù sự thật ngược lại.

### Test 1 — Đảo sự thật

Đảo ngược sự thật, câu vẫn đúng? → fail.
- Xấu: "Cổ phiếu có thể tăng tùy thuộc thị trường" (tăng/giảm đều đúng → BA PHẢI)
- Tốt: "Cổ phiếu sẽ tăng vì quý 1 lãi vượt 30%" (có direction + lý do)

### Test 2 — Direction check

Có cam kết direction không? → không = fail.

LLM-as-judge runs both tests inline. Falls back keyword check when no API key.

---

## V3 — Verdict line bắt buộc (V1.3 TIGHTEN)

Closing MUST có verdict cụ thể cho NĐT. 5 elements bắt buộc (V1.3 — bumped from 3):

1. **Stance verb** — "nên cầm/giảm/giữ/bán/tích lũy/thoát" HOẶC "phù hợp/không phù hợp NĐT" HOẶC "phòng thủ"
2. **Quantified trigger** — number with unit (giá/percent/tỷ) HOẶC điều kiện định lượng ("nếu NIM > 3,5%", "khi CASA tụt dưới 22%")
3. **Timeframe** — "12 tháng", "24-36 tháng", "Q3/2026", "ngắn hạn / dài hạn"
4. **Holder context** — "NĐT đang cầm", "người giữ", "khớp NĐT" + động từ action
5. **NO vague phrase** — auto-reject nếu chứa từ trong `CLOSING_VAGUE_BAN`:
   - "cần theo dõi" · "đáng theo dõi" · "cần thận trọng" · "tham khảo trước khi"
   - "làm chỉ báo" · "là chỉ báo sớm" · "đánh giá thêm" · "chờ thêm dữ liệu"

Implementation: `lib.quality_gates.check_verdict_line` composes `check_actionable_closing` (V1.3). Cũ 3-element rule + V1.3 actionability layer.

### ✅ Tốt (V1.3 actionable closings)

1. "NĐT đang cầm nên giữ ACB 12-18 tháng nếu NIM duy trì trên 3,5% Q3/2026; giảm 30% vị thế nếu CASA tụt dưới 22%."
2. "Mã phù hợp NĐT giá trị giữ vùng 75-80 nghìn/cp, cắt 30% nếu rơi dưới 70."
3. "NĐT short-term FOMO không phù hợp — TCB cần 18 tháng nữa để re-rate khi P/B vượt 1,7."
4. "Người giữ VCB nên tích lũy dưới 90.000 đồng, mục tiêu 110-115 trong 24 tháng nếu RWA tiếp tục cải thiện."
5. "Đang cầm nên thoát 50% khi VHM vượt 85.000 đồng Q2 — buffer phòng thủ phần còn lại."

### ❌ Xấu (V1.3 reject)

1. "NĐT cần theo dõi tốc độ hấp thụ Hải Vân Bay Q2/2026 làm chỉ báo sớm cho năm 2027-2028."
   → fail Layer 5 ("cần theo dõi" + "làm chỉ báo")
2. "Tùy quan điểm NĐT đánh giá thêm trong các quý tới."
   → fail Layer 1 (no stance) + Layer 5 ("đánh giá thêm")
3. "Cần thêm thông tin để đánh giá — nhà đầu tư thận trọng quan sát."
   → fail Layer 5 + Layer 2 (no quantified trigger)
4. "Mã đáng chú ý cho NĐT dài hạn."
   → fail Layer 2 (no number/condition)

---

## V4 — Title delegate (V5.1.2)

Master KHÔNG generate title. Headline agent (Step 4.5 in pipeline) writes title via 7 hard criteria + 4 lối V1.2.

Master ensures body có 1 angle dominant để Headline agent extract title hook. Đừng spread 3 angle khác nhau trong body.

Em dash trong title BANNED (AI-tell signal). Hyphen `-` + en dash `–` OK trong body.

---

## V5 — Contrarian-when-warranted

Master được phép viết góc nghịch CHỈ KHI data clear support. KHÔNG override `stance_directive` từ brief.

- Story Editor brief `direction: bullish`. Master tìm data confirming bullish + 1 caveat. → Write bullish body, caveat vào closing.
- Master tìm data flat-out contradict bullish stance. → KHÔNG override → `master_decision: reject_data_conflict` + push back lên Story Editor.

Contrarian-when-warranted ≠ override. Master không tự ý lật stance.

---

## V6 — Bình dân xuồng xã nguy hiểm (V1.3 NEW)

### Định nghĩa

Voice "bình dân xuồng xã + nguy hiểm" = ngôn ngữ đời thường người Việt + sharp/edge cảm xúc + ưu tiên ví von > số khô khan. Parallel V1.2 title rules.

User feedback 2026-05-13: 5/5 bài audit dùng báo chí formal verbs ("bàn giao", "ghi nhận", "công bố", "dự kiến đạt", "phát hành") — kill stance + sound như thông cáo báo chí, không phải tin chuyên gia.

### V6.1 — Ban báo chí body verbs (≥2 occurrence = fail)

Reject body chứa ≥2 occurrence của từ trong `BAO_CHI_BODY_VERBS`:

```
bàn giao | ghi nhận | công bố | dự kiến đạt | phát hành thành công
đang tiến hành | tiếp tục triển khai | đặt mục tiêu | hoàn thành kế hoạch
phấn đấu | thông qua nghị quyết | đã được phê duyệt | đã được thông qua
ban hành | triển khai đồng bộ | tích cực triển khai
```

1 occurrence OK (factual reporting), ≥2 = thông cáo style.

Implementation: `lib.quality_gates.check_bao_chi_body`.

### V6.2 — Prefer bình dân verbs

Khi Master cần verb action, ưu tiên `PREFERRED_BODY_VERBS`:

| Báo chí (BAN) | Bình dân (PREFER) | Ví dụ V1.3 |
|---|---|---|
| ghi nhận lợi nhuận | ăn lãi / khoe lãi | "VHM ăn 25.625 tỷ Q1" |
| phát hành trái phiếu | bơm vốn / gọi vốn | "VHM bơm 11.000 tỷ trái phiếu" |
| bàn giao căn hộ | giao / trả khách | "VHM trả 4.000 căn Royal Island" |
| công bố kế hoạch | khoe đích / đặt cọc | "VHM khoe đích 60.000 tỷ năm 2026" |
| đặt mục tiêu | nhắm / chấm đích | "VHM nhắm 60K tỷ năm 2026" |
| đang tiến hành | đang đẩy / đang gom | "TCB đang gom danh mục mới" |
| phấn đấu | cố / lùa | "VHM cố tăng tốc Q2 sau khi tụt Q1" |

### V6.3 — Ưu tiên ví von > số khô khan

Khi viết về 1 con số to, thay vì dồn 3 fact liên tiếp, dùng analogy/metaphor (V1.3 METAPHOR_MARKERS):

```
như | kiểu | giống | ví như | nói nôm na | nói cách khác
thật ra | thực ra | kỳ thực
gấp X lần | bằng | tương đương | ngang ngửa | ngang với
tựa hồ | chẳng khác | khác nào
```

### ✅ Tốt (V6 examples)

1. **"VHM Q1 ăn 25.625 tỷ, gấp 3 lần Vietcombank cùng kỳ."** — bình dân verb "ăn" + analogy "gấp 3 lần"
2. **"TCB cố lùa thêm 8% CASA Q2, nhưng tiền tiết kiệm cứ chạy sang quỹ MMF."** — verb "cố lùa" + tension
3. **"VPB khoe lãi 30% YoY mà cổ phiếu vẫn tụt 5% — thị trường đang nhìn cái gì?"** — verb "khoe" + paradox
4. **"BSR ngồi trên 8.265 tỷ Q1 nhưng sếp chỉ hứa 2.162 tỷ cả năm. Bảo thủ hay sợ gì?"** — "ngồi trên" + concrete question

### ❌ Xấu (V6 reject)

1. "VHM ghi nhận lợi nhuận sau thuế 25.625 tỷ đồng quý 1/2026, đặt mục tiêu 60.000 tỷ năm 2026, đồng thời công bố kế hoạch phát hành trái phiếu 11.000 tỷ."
   → 4 báo chí verbs (ghi nhận + đặt mục tiêu + công bố + phát hành) → fail bao_chi_body
2. "Theo công bố, ngân hàng dự kiến đạt 8% tăng trưởng tín dụng năm 2026 và sẽ tiếp tục triển khai chiến lược phòng thủ."
   → 3 báo chí verbs (công bố + dự kiến đạt + tiếp tục triển khai)

---

## V7 — Bold density per format (V1.3 NEW)

User feedback: body audit TB bold density 1.83% — user bỏ qua vì không tô đậm ý chính. Tham khảo X/Twitter Wu Blockchain style.

### Target per format

| Format | Mode | Target | Equivalent |
|---|---|---|---|
| flash_qa | absolute | ≥3 bold/bài | ~3% tại 100 từ |
| standard_qa | ratio | ≥4% | 1 bold per 25 từ |
| standard_listicle | ratio | ≥5% (densest) | 1 bold per 20 từ |
| standard_narrative | ratio | ≥3% (prose flow) | 1 bold per 33 từ |

Implementation: `lib.quality_gates.check_bold_density` reads `bold_density_min` từ `data/format_registry.yaml` (single source of truth).

### Bold target priority

1. **Số key** — `**5.000 tỷ**`, `**67%**`, `**3,5%/năm**`
2. **Tên ticker/tổ chức nổi bật** — `**Vietcombank**`, `**Big4**`, `**NHNN**`
3. **Verb hành động sắc** — `**ăn lãi**`, `**khoe**`, `**dồn tiền**`, `**xén cổ tức**`
4. **Phán quyết closing** — `**phù hợp NĐT giá trị**`, `**không phù hợp short-term**`

### Anti-pattern V7

- Bold cả câu dài (>10 từ) → mất signal value
- Bold từ chung chung ("**lợi nhuận**", "**doanh thu**") không kèm số
- Bold lập đi lập lại 1 từ — 3 lần "**VCB**" trong 1 bullet không add scan value

---

## Em dash density (V5.1.2 PATCH preserved)

- **flash_qa**: max 1 em dash / bài
- **standard_qa / listicle / narrative**: max 1 em dash / 100 từ
- Em dash trong title BANNED (AI-tell signal — feedback_no_em_dash_title.md)

Implementation: `lib.quality_gates.check_em_dash_density`.

---

## Cross-reference

- V1 stance → `stance-directive-handler.md`
- V3 actionable closing → `lib.quality_gates.check_actionable_closing` + `lib.voice_rules.STANCE_VERBS` + `CLOSING_VAGUE_BAN`
- V6 body voice → `lib.voice_rules.BAO_CHI_BODY_VERBS` + `PREFERRED_BODY_VERBS` + `METAPHOR_MARKERS`
- V7 bold density → `data/format_registry.yaml.formats.*.bold_density_min`
- 4 format pattern → `format-bodies/{flash-qa,standard-qa,standard-listicle,standard-narrative}.md`
