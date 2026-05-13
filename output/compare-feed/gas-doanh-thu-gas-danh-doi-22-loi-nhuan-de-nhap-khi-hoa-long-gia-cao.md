---
title: Vì sao PV GAS tăng doanh thu nhưng lãi lại giảm 22% năm 2026?
ticker: GAS
sector: Phòng thủ
sector_icon: 📰
crawled_at: '2026-05-13T04:13:10.545428+00:00'
funnel_batch_id: GAS-20260513-0413
left_meta:
  author: Chuyên gia
  word_count: 269
  key_view: paradox:GAS doanh thu len 5% nhung lai tut 22% — chuyen dich co cau sang
    LNG nhap bien mong
  skeptic_verdict: null
  pipeline_version: V5.1.3
insight: Kế hoạch GAS 2026 doanh thu nhỉnh 142.000 tỷ nhưng lãi tụt 22% xuống 9.019
  tỷ là tín hiệu sớm cơ cấu nguồn cung chuyển từ khí nội địa biên cao sang LNG nhập
  biên mỏng, sốc giá Hormuz là chất xúc tác đẩy nhanh — không phải bão hoà thị trường.
right_source:
  name: Tin nhanh chứng khoán
  url: https://www.tinnhanhchungkhoan.vn/pv-gas-giu-vung-nguon-cung-lng-lpg-cho-thi-truong-nang-luong-viet-nam-giua-gian-doan-tai-eo-bien-hormuz-post390145.html
  published: '2026-05-12'
  raw_title: PV GAS giữ vững nguồn cung LNG - LPG cho thị trường năng lượng Việt Nam
    giữa gián đoạn tại eo biển Hormuz
why_chosen_narrative: ''
angle_label: Doanh thu tăng, lợi nhuận lùi — đánh đổi gì khi nhập khẩu khí to dần
angle_narrative: ''
deep_question_options:
- question: Vì sao Tổng công ty Khí Việt Nam đặt kế hoạch lợi nhuận 2026 lùi 22% trong
    khi doanh thu vẫn tăng?
  category: paradox
  stance_directive:
    direction: bearish
    confidence: medium
  key_metric_count: 4
  format_id: standard_qa
  format_reason: Category=paradox → candidates=[standard_qa]. Single candidate, no
    tie-break. key_metric_count=4>1 → no downgrade. Picked=standard_qa.
  tone_bias: neutral
  length_target: 250
- question: Vì sao Tổng công ty Khí Việt Nam nâng kho Thị Vải 68% và ký 25 năm với
    PV Power chính trong giai đoạn eo Hormuz căng thẳng nhất?
  category: why_now
  stance_directive:
    direction: bullish
    confidence: medium
  key_metric_count: 4
  format_id: standard_qa
  format_reason: Category=why_now → candidates=[standard_qa]. Single candidate, no
    tie-break. key_metric_count=4>1 → no downgrade. Picked=standard_qa.
  tone_bias: neutral
  length_target: 250
- question: Vì sao thị trường vẫn đẩy cổ phiếu GAS tăng 4,71% lên 80.100 đồng dù kế
    hoạch lợi nhuận 2026 lùi 22%?
  category: hidden_mechanism
  stance_directive:
    direction: divergent
    confidence: low
  key_metric_count: 2
  format_id: standard_qa
  format_reason: 'Category=hidden_mechanism → candidates=[standard_qa, standard_narrative].
    Tie-break: narrative_setup missing → timeline_markers=0 < 3 → pick standard_qa.
    key_metric_count=2>1 → no downgrade. Picked=standard_qa.'
  tone_bias: neutral
  length_target: 250
chosen_question_idx: 0
chosen_pick_reason: 'Option 0 (paradox + bearish/medium + standard_qa) khớp data cứng
  nhất: hai con số đối lập (doanh thu +5% vs lãi -22%) là nghịch lý chỉ có thể giải
  thích qua mechanism cơ cấu nguồn cung — đúng dạng paradox cho standard_qa. Option
  1 (why_now) cùng đề tài nhưng angle hạ tầng dàn trải qua 3 dự án + 25 năm + 2029-2030,
  không gọn cho 240 từ. Option 2 (hidden_mechanism divergent low-confidence) đoán
  hành vi thị trường — yếu cơ sở số liệu, dễ trượt thành speculation.'
skip_reasons:
  '1': 'Option why_now bullish: 3 hành động hạ tầng (kho Thị Vải, hợp đồng PV Power
    25 năm, kho Vũng Áng 26.700 tỷ) trải timeline 2026-2030 — quá dài cho standard_qa
    240 từ, dệt 3 mạch song song không tốt.'
  '2': 'Option hidden_mechanism divergent low-confidence: phân tích vì sao thị trường
    đẩy giá +4,71% dù KH lùi 22% — yêu cầu đào tâm lý NĐT, ít data cứng, easy hedging
    trap.'
crawl_funnel:
  picked:
  - source: Tin nhanh chứng khoán
    url: https://www.tinnhanhchungkhoan.vn/pv-gas-giu-vung-nguon-cung-lng-lpg-cho-thi-truong-nang-luong-viet-nam-giua-gian-doan-tai-eo-bien-hormuz-post390145.html
    published: '2026-05-12'
    reason: Option 0 paradox bearish standard_qa 239 words, all 11 V5.1.2+V1.3 gates
      pass
  rejected:
  - source: Vietstock
    url: https://vietstock.vn/2026/05/vnm-mwg-pow-co-trien-vong-gi-145-1440670.htm
    published: '2026-05-11'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: sub_event_attached — primary ticker là VNM, GAS chỉ xuất hiện như nguồn
      cung khí hoá lỏng phụ trợ POW. Bài này phù hợp batch VNM/POW chứ không phải
      angle GAS standalone. Điểm dữ liệu giá 80.100 đồng +4,71% đã trích sang brief
      a9a6422e cho option hidden_mechanism.
  - source: VietnamFinance
    url: https://vietnamfinance.vn/pv-gas-giu-vung-nguon-cung-lng-lpg-cho-thi-truong-nang-luong-viet-nam-d144629.html
    published: '2026-05-11'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: dup_event — cùng câu chuyện PV GAS giữ nguồn cung LNG-LPG nhưng phiên
      bản này thiếu kế hoạch lợi nhuận 2026 và chi tiết gián đoạn Hormuz. Bài a9a6422e
      đầy đủ hơn.
  total_candidates: 3
master_data_trail:
- source: WebSearch/vietnambiz.vn-pv-gas-loi-nhuan-giam-20-2026
  url: https://vietnambiz.vn/pv-gas-du-bao-loi-nhuan-giam-hon-20-nam-2026-202632510378278.htm
  fetched: '2026-05-13'
  purpose: 'Verify KH 2026: doanh thu 142.000 tỷ (+4%), lãi sau thuế 9.019 tỷ (-22%)'
  supports_argument: Opening fact + Bullet 3
- source: WebSearch/tinnhanhchungkhoan.vn-pv-gas-2026-loi-nhuan-co-tuc-20
  url: https://www.tinnhanhchungkhoan.vn/pv-gas-gas-dat-muc-tieu-lai-sau-thue-nam-2026-hon-8800-ty-dong-va-co-tuc-ty-le-20-post387358.html
  fetched: '2026-05-13'
  purpose: Cổ tức 2026 giữ 20%, doanh thu 2025 đạt 136.843 tỷ — lãi 11.572 tỷ
  supports_argument: Bullet 4 (cổ tức) + benchmark 2025
- source: WebSearch/tuoitre.vn-hai-ong-lon-dau-khi-cai-so-lui-loi-nhuan-2026
  url: https://tuoitre.vn/hai-ong-lon-dau-khi-cai-so-lui-loi-nhuan-nam-2026-vi-sao-khong-gay-bat-ngo-20260326201348027.htm
  fetched: '2026-05-13'
  purpose: Áp lực chi phí nhập khẩu LNG là lý do chính cho KH lãi lùi
  supports_argument: Bullet 2 (Hormuz disruption) + Bullet 3 (cơ cấu đảo trục)
- source: Crawl/tinnhanhchungkhoan.vn-pv-gas-Hormuz-LNG-LPG
  url: https://www.tinnhanhchungkhoan.vn/pv-gas-giu-vung-nguon-cung-lng-lpg-cho-thi-truong-nang-luong-viet-nam-giua-gian-doan-tai-eo-bien-hormuz-post390145.html
  fetched: '2026-05-13'
  purpose: 'PV GAS chủ động nhập 120.000 tấn LNG/LPG, vận hành Nhơn Trạch 3-4, KH
    2026: doanh thu 142K tỷ lãi 9.019 tỷ'
  supports_argument: Opening + Bullet 2
skeptic_data_trail: []
raw_article_url: https://www.tinnhanhchungkhoan.vn/pv-gas-giu-vung-nguon-cung-lng-lpg-cho-thi-truong-nang-luong-viet-nam-giua-gian-doan-tai-eo-bien-hormuz-post390145.html
format_director: null
---

<!-- left -->

PV GAS nhắm doanh thu **142.000 tỷ** năm 2026, tăng nhẹ so với **135.000 tỷ** thực hiện 2025, nhưng kế hoạch lợi nhuận sau thuế giảm **22%** xuống **9.019 tỷ** từ mức **11.572 tỷ** đã đạt. Nghịch lý: doanh thu vẫn lên mà lợi nhuận rút mạnh vì cơ cấu nguồn cung thay đổi.

- **Khí thiên nhiên hoá lỏng (LNG) nhập khẩu ép biên gộp**: PV GAS chuyển dần từ khí nội địa biên gộp cao sang LNG nhập, phần chênh lệch giá vận chuyển và nguồn gốc ăn vào lợi nhuận thay vì chảy về cổ đông.
- **Giá LNG tăng gấp ba trong Q1/2026**: gián đoạn eo Hormuz tháng 2-3/2026 đẩy giá khí nhập lên gấp ba, cước vận tải tăng 10-15 lần; doanh nghiệp tự xác nhận đây là lý do chính khiến kế hoạch lợi nhuận lùi.
- **Khối lượng phân phối giữ được, biên gộp không giữ được**: doanh thu tăng **5%** nhờ sản lượng lớn hơn, nhưng tỷ trọng LNG trong cơ cấu nguồn cung kéo biên gộp xuống; đây là thay đổi cơ cấu dài hạn, không phải bão hoà nhất thời.
- **Cổ tức giữ nguyên 20% dù lợi nhuận lùi**: ban lãnh đạo chưa cắt cổ tức, tin chi phí LNG sẽ ổn lại từ Q3/2026 khi giá khí hạ nhiệt; chưa phải khủng hoảng nhưng áp lực rõ ràng hơn từng quý.

NĐT đang cầm nên giảm tỷ trọng **30%** ở vùng **78-82 nghìn/cp** trong 6-12 tháng nếu biên gộp Q2/2026 không hồi trên 10%; người muốn cầm cổ tức phòng thủ nên đợi vùng dưới 75 nghìn.

<!-- right -->


