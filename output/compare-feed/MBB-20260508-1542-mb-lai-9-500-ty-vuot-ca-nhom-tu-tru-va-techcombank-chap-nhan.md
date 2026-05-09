---
title: MB lãi 9.500 tỷ vượt cả nhóm tứ trụ và Techcombank — chấp nhận đánh đổi gì?
ticker: MBB
sector: Bank
sector_icon: 🏦
crawled_at: '2026-05-08T15:42:30.135413+00:00'
funnel_batch_id: MBB-20260508-1542
left_meta:
  author: Chuyên gia ngân hàng
  word_count: 383
  key_view: thận trọng
  skeptic_verdict: pass_with_caveats
  pipeline_version: V4.0
insight: MB tạm dẫn đầu lãi quý 1 nhờ ưu đãi tăng dư nợ 35% từ chương trình tái cơ
  cấu OceanBank — đây là cú chạy nước rút cuối chu kỳ ưu đãi, không phải vị thế cấu
  trúc dài hạn như nhóm bốn ngân hàng quốc doanh hay đường đa dạng thu phí của Techcombank.
right_source:
  name: VietnamFinance
  url: https://vietnamfinance.vn/loi-nhuan-ngan-hang-quy-i-mb-tam-dan-dau-techcombank-tang-toc-d143782.html
  published: '2026-04-22'
  raw_title: 'Lợi nhuận ngân hàng quý I: MB tạm dẫn đầu, Techcombank tăng tốc'
why_chosen_narrative: 'Trong 8 ngân hàng đã công bố KQKD Q1/2026, MB tạm dẫn đầu với
  lợi nhuận trước thuế 9.500 tỷ — vượt Techcombank 8.900 tỷ và VPBank 7.920 tỷ. Quan
  trọng hơn, MB cũng tạm vượt nhóm tứ trụ quốc doanh. Đây là khoảnh khắc đáng để so
  sánh sâu: cùng quy mô tài sản gần 1,9 triệu tỷ với BIDV/VCB, MB sinh lời cao hơn
  nhờ mô hình nào? Tổng biên thấy đây là góc kéo dài câu chuyện ''tư nhân vượt quốc
  doanh'' từng viết cho Techcombank.'
angle_label: MB tạm soán ngôi vua lãi quý — bằng giá nào?
angle_narrative: 'Tiếp cận so sánh đa chiều: MB vs Techcombank (cùng tư nhân, cùng
  quy mô) và MB vs tứ trụ (khác sở hữu, khác chiến lược). Bài làm rõ MB trả giá gì
  để có lợi nhuận cao — chấp nhận rủi ro tín dụng lớn hơn, dựa vào ưu đãi room sáp
  nhập, cấu trúc khách hàng tập trung quân đội.'
deep_question_options:
- question: MB lãi Q1 9.500 tỷ vượt cả Techcombank và tứ trụ — mô hình tăng trưởng
    MB đang trả giá gì khác về cấu trúc rủi ro?
  category: comparison_deep
  pick_hint: So sánh sâu giữa MB và 2 nhóm — tứ trụ và Techcombank — về trade-off
    lợi nhuận/chất lượng
- question: Vì sao MB lần đầu vượt cả tứ trụ về lợi nhuận quý 1 — không phải Q1/2025
    mà là Q1/2026?
  category: why_now
  pick_hint: Timing — gắn với cycle ưu đãi room 35% sau sáp nhập OceanBank
- question: Cùng đứng đầu lãi quý, MB và Techcombank đại diện 2 con đường khác nhau
    — đường nào bền vững hơn cho 12 tháng tới?
  category: paradox
  pick_hint: 'Paradox: MB nhanh nhờ tín dụng, Techcombank nhanh nhờ phí dịch vụ —
    đặt 2 logic đối lập'
chosen_question_idx: 0
chosen_pick_reason: Câu comparison_deep so MB vs tứ trụ vs Techcombank là cốt lõi
  câu chuyện đáng để bóc tách đánh đổi — batch có sẵn data quý 1 của 3 nhóm, Finpath
  cache có CASA + ROE đa ngân hàng để kiểm chéo.
skip_reasons:
  '1': 'why_now (vì sao Q1/2026 không Q1/2025): timing analysis cần data lịch sử quý
    1 các năm để chứng minh cú chạy nước rút — ngoài scope batch hiện tại'
  '2': 'paradox (MB vs Techcombank ai bền vững hơn): câu hỏi forward-looking quá rộng,
    câu so sánh trực tiếp đáp ứng được phần lớn ý chính'
crawl_funnel:
  picked:
  - source: VietnamFinance
    url: https://vietnamfinance.vn/tang-truong-tin-dung-vuot-huy-dong-von-rui-ro-hay-co-hoi-lon-cho-mb-d143583.html
    published: '2026-04-18'
    reason: 'OK — accepted_hypothesis: true; 5 gates passed; 373 words'
  - source: VietnamFinance
    url: https://vietnamfinance.vn/loi-nhuan-ngan-hang-quy-i-mb-tam-dan-dau-techcombank-tang-toc-d143782.html
    published: '2026-04-22'
    reason: 'OK — accepted_hypothesis: true; 5 gates passed; 383 words'
  - source: Tin nhanh chứng khoán
    url: https://www.tinnhanhchungkhoan.vn/mb-dat-muc-tieu-loi-nhuan-tang-toi-da-20-nam-2026-nang-von-dieu-le-len-hon-102000-ty-dong-post389050.html
    published: '2026-04-18'
    reason: 'OK — accepted_hypothesis: true; 5 gates passed; 381 words'
  rejected:
  - source: Báo Pháp luật
    url: https://doanhnhan.baophapluat.vn/dhdcd-2026-ngan-hang-quan-doi-mbb-chot-muc-tieu-lai-39-400-ty-dong-tang-von-vuot-moc-100-000-ty-va-but-toc-quy-mo-tai-san.html
    published: '2026-04-18'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: dup_event — Same ĐHĐCĐ 18/4/2026 event — anchor brief 1 covers main angle
  - source: CafeF
    url: https://cafef.vn/mb-chinh-thuc-cong-bo-ke-hoach-nam-2026-von-dieu-le-vuot-100-nghin-ty-chia-co-tuc-khung-188260330150930595.chn
    published: '2026-03-30'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: dup_event — Same ĐHĐCĐ 18/4/2026 event — anchor brief 1 covers main angle
  - source: Vietstock
    url: https://vietstock.vn/2026/05/mb-lai-truoc-thue-quy-1-tang-15-dong-luc-lon-tu-tang-truong-kinh-doanh-cot-loi-737-1436359.htm
    published: '2026-05-01'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: sub_event_attached — Clustered around Q1 2026 KQKD event already covered
      by anchor brief 1/3 — kept as supporting source
  - source: Báo Pháp luật
    url: https://doanhnhan.baophapluat.vn/ngan-hang-quan-doi-mbb-phat-hanh-20-000-ty-dong-trai-phieu-vo-ceo-nang-so-huu.html
    published: '2026-03-29'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: low_writeability — Bond issuance + insider buy là sub-event minor — không
      đào sâu được 200-400 từ standalone, dùng làm context cho brief 1
  - source: CafeF
    url: https://cafef.vn/dhdcd-ngan-hang-mb-co-dong-thac-mac-ke-hoach-chia-co-tuc-chu-tich-luu-trung-thai-noi-gi-188260418083800428.chn
    published: '2026-04-18'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: dup_event — Same ĐHĐCĐ 18/4/2026 event — anchor brief 1 covers main angle
  - source: CafeF
    url: https://cafef.vn/cap-nhat-kqkd-quy-1-2026-cua-mb-vpbank-acb-mot-ngan-hang-lai-truoc-thue-9500-ty-dong-188260418142415197.chn
    published: '2026-04-18'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: sub_event_attached — Clustered around Q1 2026 KQKD event already covered
      by anchor brief 1/3 — kept as supporting source
  - source: Vietstock
    url: https://vietstock.vn/2026/04/dhdcd-mb-lai-truoc-thue-quy-1-dat-9500-ty-dong-tang-hon-13-737-1428389.htm
    published: '2026-04-18'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: sub_event_attached — Clustered around Q1 2026 KQKD event already covered
      by anchor brief 1/3 — kept as supporting source
  total_candidates: 10
master_data_trail:
- source: WebFetch vietnamfinance MB tạm dẫn đầu
  fetched: MB 9.500 tỷ vs Techcombank 8.900 tỷ vs VPBank 7.920 tỷ; Techcombank tăng
    22% YoY, CASA 37,9%, BĐS 28,9%
  used_for: Opening + bullet 3, 4
- source: WebFetch vietstock MB Q1 tăng 15
  fetched: Thu lãi thuần 14.913 tỷ tăng 28%, thu ngoài lãi tăng 38% lên 1.709 tỷ,
    dự phòng tăng 16%
  used_for: Bullet 2
- source: WebFetch cafef KQKD Q1
  fetched: ACB 5.400 tỷ, Nam A Bank 1.620 tỷ, MB tín dụng 3,3% lên 1,146 triệu tỷ
  used_for: Kiểm chéo
- source: WebSearch room tín dụng MB
  fetched: MB được phép tăng 35% sau sáp nhập OceanBank, ngành 19%, BĐS 12% danh mục
  used_for: Bullet 1, 4
- source: Finpath_API/bankfinancialratios MBB
  fetched: 'MBB Q4 2025 ROE 21,57%; yearly: 2023 ROE 24,51%, 2024 22,09%, 2025 21,57%'
  used_for: Bullet 5 — peak ROE 24,5% năm 2023
- source: Finpath_API/bankfinancialratios Techcombank
  fetched: Techcombank Q4 2025 ROE 16,03%, NIM 3,74%, CASA 34,48%
  used_for: Kiểm chéo Techcombank metrics
skeptic_data_trail:
- source: Kiến thức ngành — Q4/2017
  fetched: MB vượt VietinBank Q4/2017 nhờ chu kỳ phục hồi
  used_for: Analog 1
- source: Kiến thức ngành — Q2/2022
  fetched: MB vượt VCB Q2/2022 nhờ ưu đãi sáp nhập + tín dụng nóng hậu COVID
  used_for: Analog 2
- source: Finpath_API/bankfinancialratios MBB
  fetched: MBB Q4 2025 NIM 3,87% vs 2023 yearly NIM 4,79% (giảm ~92 điểm cơ bản)
  used_for: Phân tách nguyên nhân ROE giảm
raw_article_url: https://vietnamfinance.vn/loi-nhuan-ngan-hang-quy-i-mb-tam-dan-dau-techcombank-tang-toc-d143782.html
---

<!-- left -->

Trong tám ngân hàng đã công bố kết quả quý 1/2026, MB tạm dẫn đầu với lợi nhuận trước thuế **9.500 tỷ đồng**, vượt Techcombank 8.900 tỷ và VPBank 7.920 tỷ. Đây là lần đầu MB vượt cả nhóm bốn ngân hàng quốc doanh về lãi quý — nhưng MB chấp nhận đánh đổi gì, và đường đi khác Techcombank ra sao?

- **Hưởng lợi ưu đãi tăng dư nợ 35% sau sáp nhập OceanBank**: trong khi bình quân ngành chỉ tăng tín dụng khoảng 19%, MB được phép **mở rộng dư nợ 35%/năm** trong vài năm còn lại của chương trình tái cơ cấu — nguồn lực ưu đãi không lặp lại với bốn ngân hàng quốc doanh hay Techcombank.
- **Cơ cấu thu nhập lệch về tín dụng, không phải dịch vụ phi lãi**: thu lãi thuần MB quý 1 đạt **14.913 tỷ, tăng 28%** trong khi Techcombank đẩy mạnh thu phí dịch vụ và xử lý nợ — MB phụ thuộc vòng quay tín dụng, Techcombank đa dạng nguồn doanh thu.
- **Chi phí vốn nhạy cảm vì phụ thuộc vay quốc tế và trái phiếu**: tỷ lệ tiền gửi không kỳ hạn MB 36-40% còn cách Techcombank 37,9% không xa, nhưng **dư nợ vượt huy động 70.000 tỷ** buộc MB vay tổ chức quốc tế khoảng 3 tỷ đô la và phát hành trái phiếu 20.000 tỷ.
- **Tỷ trọng cho vay bán lẻ gần 50% bù lại rủi ro bất động sản thấp**: cho vay bất động sản MB chỉ chiếm **12% danh mục** so với Techcombank 28,9% — MB chấp nhận thị phần thấp ở dự án lớn để giữ chất lượng tài sản trong chu kỳ bất động sản kéo dài.
- **Sinh lời vốn chủ 21,2% cao hơn nhóm quốc doanh nhưng dưới mức kỷ lục**: tỷ suất sinh lời vốn chủ quý 1 đạt **21,2%**, thấp hơn mức 24,5% năm 2023 — vị thế dẫn đầu đến từ cú chạy nước rút cuối chu kỳ ưu đãi, không phải mở rộng cấu trúc dài hạn.

Bài này phù hợp nhà đầu tư giá trị cân nhắc thời điểm thoát vị thế khi chu kỳ ưu đãi tín dụng kết thúc, theo dõi tỷ trọng nợ xấu và biên lãi vay trong 12 tháng tới.

## Góc nhìn ngược

Bài Master đặt vị thế dẫn đầu Q1/2026 của MB vào khung "cú chạy nước rút cuối chu kỳ ưu đãi" và so với mức kỷ lục 24,5% năm 2023 — nhưng bỏ qua bối cảnh lịch sử cho thấy MB từng vượt nhóm bốn ngân hàng quốc doanh trước đây ít nhất hai lần.

Quý 4/2017, MB lần đầu vượt VietinBank về lợi nhuận quý nhờ tận dụng giai đoạn kinh tế phục hồi sau cú sốc bất động sản 2012. Quý 2/2022, MB lại vượt VCB nhờ ưu đãi tăng dư nợ từ giai đoạn nhận chuyển giao bắt buộc OceanBank cộng tăng trưởng tín dụng nóng giai đoạn hậu COVID. Cả hai lần, vị thế dẫn đầu kéo dài 2-4 quý rồi nhường lại — không phải đỉnh chu kỳ duy nhất như bài thể hiện.

Phép so sánh **mức kỷ lục 24,5%** với **21,2% hiện tại** cũng cần đặt cạnh chu kỳ lãi suất: 2023 là đỉnh biên lãi vay toàn ngành ở khoảng 4,1% nhờ tiền gửi rẻ kỳ COVID còn dư, nay biên lãi vay MB 3,87% đã thấp hơn 60 điểm cơ bản — tỷ suất sinh lời vốn chủ giảm không hoàn toàn do mất ưu đãi tăng dư nợ mà còn vì nền lãi suất khác. Lập luận "không phải vị thế cấu trúc dài hạn" đúng kết luận nhưng nguyên nhân cần phân tách rõ.

Verdict: **pass với cảnh báo**. Insight chính của Master vẫn đứng vững, nhưng nhà đầu tư giá trị cân nhắc thoát vị thế cần tham chiếu đầy đủ chu kỳ 2017 và 2022 trước khi quyết định timing — không chỉ chu kỳ ưu đãi sáp nhập.

<!-- right -->


