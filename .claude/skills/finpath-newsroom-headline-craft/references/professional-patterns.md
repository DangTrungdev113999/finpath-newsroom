# Headline Quality Reference — Expert Investor Voice

> KHÔNG phải template. KHÔNG phải checklist. Là **7 ví dụ chuẩn** của chuyên gia in-house đọc bài và giật tít — đọc để cảm nhận quality bar, sau đó CRAFT theo bài cụ thể.

## 3 nguyên tắc craft (principles, không phải rules)

1. **Đọc body như analyst** — không grep số/verb. Đọc xong tự hỏi: "NĐT cầm mã này đang cược điều gì? Lo gì? Nên nhìn gì?" Title trả lời câu đó.

2. **Zoom-out > zoom-in** — Đừng chộp local detail mạnh nhất. Tìm strategic stake / asset to / decision lớn nhất bài bàn về.

3. **Reader bình dân test** — Title đứng độc lập, NĐT thường (không phải Petroleum analyst) đọc 5s có hiểu cược/rủi ro không? Nếu cần biết "Lô B là gì" / "FOX là gì" / proprietary ref → REPHRASE hoặc gloss inline.

Mọi quyết định craft (metaphor / question / declarative / brand name / number-or-not) đều TỪ bài, không từ template.

## 7 expert benchmark (quality bar to feel)

7 ví dụ này là chuẩn — đọc để cảm thấy "title hay là gì". KHÔNG copy template, không apply pattern. Khi craft cho bài mới, tự ra title cùng tầm.

| # | Article (1-sentence body summary) | Expert title |
|---|---|---|
| 1 | PVS Q1 lãi gộp gấp 3,3 lần nhưng 282 tỷ trích lập bảo hành dồn vào chi phí; tiền mặt 16.000 tỷ chủ yếu là vốn lưu động cho dự án khí Lô B – Ô Môn | **PVS đang giữ 16.000 tỷ để làm gì? Bên trong canh bạc Lô B – Ô Môn** |
| 2 | PVS tiền mặt = 82% vốn hoá, lõi kinh doanh chỉ 17,7% vốn hoá — thị trường mispricing? | **PVS: giữ núi tiền mặt nhưng thị trường vẫn không tin** |
| 2b | (same article — option B) | **PVS đang rẻ khó tin hay thị trường đang nhìn thấy rủi ro?** |
| 3 | PV GAS doanh thu 142k tỷ nhưng lãi rút 22% do nhập LNG giá cao; cổ tức ổn định 30%+ | **Nhà đầu tư nên nhìn gì ở PV GAS ngoài cổ tức** |
| 4 | FPT Telecom (FOX) lãi Q1 tăng hai chữ số NHƯNG free float 4,3% (Bộ Công an 50% + FPT mẹ 45,7%) → risk mất tư cách công ty đại chúng | **FPT Telecom: lợi nhuận tăng hai chữ số nhưng nguy cơ mất chuẩn công ty đại chúng** |
| 5 | FPT đầu tư 89 triệu USD vào Huế (không TP.HCM/Hà Nội) — build kho dữ liệu di sản số cấp tỉnh, playbook tỉnh thứ 4 | **FPT đang biến Huế thành "mỏ dữ liệu" AI đầu tiên của Việt Nam** |
| 6 | Petrolimex Q1 bán thêm 10% xăng dầu nhưng lãi giảm; chiếm 50% thị phần nội địa | **Vì sao Petrolimex không thể kiếm thêm tiền dù chiếm 50% thị phần?** |
| 7 | Petrolimex hợp tác Selex (startup xe máy điện) thay vì tự xây hệ sinh thái như VinFast; tiếp tục lỗ xăng dầu | **Vì sao Petrolimex chọn hợp tác với Selex thay vì tự xây hệ sinh thái như VinFast?** |

## Observation về 7 expert examples (cảm nhận, không phải rule)

- Đôi khi có số (16.000 tỷ / 50% / 82%), đôi khi 0 số — tùy bài cần gì
- Đôi khi có metaphor (núi tiền / mỏ dữ liệu / canh bạc), đôi khi prose thuần — tùy có scaleable asset
- Đôi khi ticker (PVS), đôi khi full brand (Petrolimex / PV GAS / Vietcombank) — tùy brand mạnh hay không
- Đôi khi question, đôi khi declarative — tùy có tension visible hay paradox
- Câu nào cũng đủ subject + impact, không cụt
- Reader bình dân test pass: KHÔNG có ref opaque (trừ trường hợp #1 "Lô B – Ô Môn" — chấp nhận vì bài về dự án đó là thesis chính)

## Safety net (objective rejects, NOT craft constraints)

`lib.headline_scorer.check_hard_criteria` enforces 7 objective rejects:
- ticker_present (Finpath universe OR full brand)
- word_count_le_16
- no_em_dash (U+2014 banned)
- not_label_leak (no "Question:" / "Lối X:" prefixes)
- no_han_viet_formal (độc bản / hội đủ / tái định giá / etc.)
- abbreviation_expanded (BCA / GRDP need expansion or be in NATURALIZED list)
- plain_language (no English jargon, no PR clickbait — cú nổ / bí mật / sốc / hot)

7 hard = OBJECTIVE pass/fail. KHÔNG dùng để craft. Agent craft trước, scorer reject sau nếu fail.

Soft hints (`not_orphan_number` + `vague_action_verbs` + `has_concrete_number`) = info log only. Agent đọc → tự cân nhắc, không gate.
