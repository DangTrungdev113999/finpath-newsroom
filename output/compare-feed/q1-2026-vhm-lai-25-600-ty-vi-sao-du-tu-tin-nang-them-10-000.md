---
title: Q1/2026 VHM lãi 25.600 tỷ — vì sao đủ tự tin nâng thêm 10.000 tỷ giữa chừng?
ticker: VHM
sector: BĐS
sector_icon: 🏠
crawled_at: '2026-05-11T09:55:10.246259+00:00'
funnel_batch_id: VHM-20260511-0955
left_meta:
  author: Chuyên gia bất động sản
  word_count: 329
  key_view: lạc quan
  skeptic_verdict: pass_with_caveats
  pipeline_version: V4
insight: VHM nâng mục tiêu lợi nhuận thêm 10.000 tỷ vì Q1/2026 đã đạt 25.625 tỷ (43%
  kế hoạch cũ) + doanh số chờ ghi nhận 201.600 tỷ có tỷ lệ chuyển đổi trên 90% — quyết
  định dựa trên số liệu thực, không phải kỳ vọng thị trường
right_source:
  name: VnEconomy
  url: https://znews.vn/vi-sao-vinhomes-bat-ngo-nang-muc-tieu-lai-len-60000-ty-nam-2026-post1645189.html
  published: '2026-04-21'
  raw_title: Vì sao Vinhomes bất ngờ nâng mục tiêu lãi lên 60.000 tỷ năm 2026?
why_chosen_narrative: Tin ĐHĐCĐ 21/4, có quote trực tiếp từ Giám đốc Tài chính Lê
  Tiến Công giải thích vì sao nâng mục tiêu từ 50.000 lên 60.000 tỷ giữa chừng. Đây
  là case hiếm — công ty BĐS thường hạ target, không nâng. CFO nêu rõ Q1 milestones
  là trigger quyết định.
angle_label: Nâng mục tiêu giữa năm — tự tin hay liều?
angle_narrative: 'Bài đi theo hướng timing: Thị trường BĐS vẫn được coi là khó khăn,
  nhưng VHM dám nâng target +20% sau Q1. Đào sâu milestones cụ thể nào khiến CFO đủ
  tự tin, và liệu đó có phải confidence thật hay chỉ là kỳ vọng.'
deep_question_options:
- question: Q1/2026 có gì đặc biệt khiến VHM dám nâng mục tiêu từ 50.000 lên 60.000
    tỷ — tăng 20% giữa chừng?
  category: why_now
  pick_hint: Có quote CFO nêu milestones, dễ verify với BCTC Q1
- question: Công thức nào từ Q1 milestones ra con số 60.000 tỷ cả năm — VHM tính toán
    như thế nào?
  category: hidden_mechanism
  pick_hint: Cần backlog + seasonality pattern để verify, phức tạp hơn
- question: Thị trường BĐS vẫn được coi là khó khăn, sao VHM dám nâng target trong
    khi NVL/KDH giữ nguyên hoặc hạ?
  category: paradox
  pick_hint: So sánh ngành hay nhưng cần data đối thủ
chosen_question_idx: 0
chosen_pick_reason: Câu hỏi why_now có quote CFO trực tiếp từ Znews, dễ verify với
  BCTC Q1 (25.625 tỷ = 43% target cũ), backlog 201.600 tỷ rõ ràng — data đầy đủ cho
  5 substantive bullets
skip_reasons:
  '1': hidden_mechanism cần phân tích sâu công thức seasonality + conversion rate,
    phức tạp hơn và không có quote trực tiếp từ CFO
  '2': paradox cần data NVL/KDH để so sánh, ngoài scope search hiện tại, rủi ro thiếu
    data đối thủ
crawl_funnel:
  picked:
  - source: VnEconomy
    url: https://znews.vn/vi-sao-vinhomes-bat-ngo-nang-muc-tieu-lai-len-60000-ty-nam-2026-post1645189.html
    published: '2026-04-21'
    reason: 'OK — data confirm insight, accepted_hypothesis: true'
  - source: Tuổi Trẻ
    url: https://tuoitre.vn/vi-sao-vinhomes-chi-tra-co-tuc-khung-trong-khi-co-nhieu-du-an-can-nguon-von-lon-20260421110151578.htm
    published: '2026-04-21'
    reason: 'OK — data confirm insight, accepted_hypothesis: true'
  - source: Báo Pháp luật
    url: https://baophapluat.vn/vinhomes-vhm-bao-lai-sau-thue-quy-i-2026-vuot-25-600-ty-dong-tiep-tuc-trien-khai-du-an-moi.html
    published: '2026-04-30'
    reason: 'Master BĐS V4.0: picked question 0 (hidden_mechanism), 5/5 gates passed,
      article persisted'
  rejected:
  - source: VnEconomy
    url: https://vnbusiness.vn/vinhomes-dat-muc-tieu-loi-nhuan-sau-thue-60000-ty-dong-nam-2026.html
    published: '2026-04-21'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: 'dup_event: Cùng topic mục tiêu 60.000 tỷ với 1f5302be nhưng thiếu quote
      CFO giải thích'
  - source: VnEconomy
    url: https://mekongasean.vn/quy-12026-vinhomes-bao-lai-gap-10-lan-cung-ky-54629.html
    published: '2026-04-30'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: 'dup_event: Cùng topic Q1 results với 550339f3 nhưng thiếu breakdown chi
      tiết'
  - source: CafeF
    url: https://cafef.vn/hang-nghin-can-ho-vinhomes-co-gia-chi-tu-650-trieu-sap-mo-ban-188260508070838405.chn
    published: '2026-05-08'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: 'low_writeability: Product news nhà ở xã hội 650 triệu — không generate
      được deep question thuộc 5 category, chỉ verify factual'
  - source: Báo Đầu tư
    url: https://dantri.com.vn/bat-dong-san/lai-suat-tran-6nam-gian-xay-18-thang-tai-vinhomes-hai-van-bay-hut-nha-dau-tu-20260507113732005.htm
    published: '2026-05-07'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: 'low_insight_potential: Marketing policy Hải Vân Bay — tin sản phẩm không
      có insight depth, không đào sâu được cơ chế'
  - source: Báo Đầu tư
    url: https://danviet.vn/dhdcd-2026-vinhomes-chia-co-tuc-sau-3-nam-im-ang-doanh-nghiep-noi-chi-dung-hon-10-loi-nhuan-tich-luy-d1420317.html
    published: '2026-04-21'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: 'dup_event: Cùng topic cổ tức với 973b6172 nhưng angle yếu hơn — 973b6172
      có quote leadership giải thích cơ chế phân bổ vốn'
  - source: CafeF
    url: https://cafef.vn/dhcd-vinhomes-dat-muc-tieu-loi-nhuan-cao-nhat-lich-su-60000-ty-dongke-hoach-dua-loat-chinh-sach-bung-no-ta-thi-truong-188260421095246897.chn
    published: '2026-04-21'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: 'dup_event: Tổng hợp 2 tin (mục tiêu + cổ tức), overlap với cả 973b6172
      và 1f5302be, không có angle riêng'
  - source: Vietstock
    url: https://vietstock.vn/2026/04/kinh-doanh-bung-no-vinhomes-ghi-nhan-loi-nhuan-quy-1-tang-866-737-1434795.htm
    published: '2026-04-30'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: 'dup_event: Cùng topic Q1 +866% với 550339f3, source Vietstock không có
      data bổ sung'
  total_candidates: 10
master_data_trail:
- source: https://znews.vn/vi-sao-vinhomes-bat-ngo-nang-muc-tieu-lai-len-60000-ty-nam-2026-post1645189.html
  fetched: 'Quote CFO Lê Tiến Công: Q1 triển khai nhiều bước chuẩn bị quan trọng,
    30-40% doanh thu từ doanh số chốt cuối 2025'
  purpose: Lấy quote trực tiếp từ CFO giải thích lý do nâng mục tiêu
  supports_argument: Bullet 3 (luận điểm 30-40% kế hoạch năm từ doanh số đã chốt)
- source: https://vietstock.vn/2026/04/kinh-doanh-bung-no-vinhomes-ghi-nhan-loi-nhuan-quy-1-tang-866-737-1434795.htm
  fetched: LNST Q1/2026 = 25.625 tỷ (+866% so với cùng kỳ), doanh thu thuần = 65.114
    tỷ (+315%), doanh số chờ ghi nhận 201.600 tỷ (+68%)
  purpose: Verify số liệu BCTC Q1/2026 từ nguồn chính thống
  supports_argument: Bullet 1 (43% kế hoạch cũ), Bullet 2 (201.600 tỷ backlog), Bullet
    4 (65.114 tỷ doanh thu)
- source: https://cafef.vn/dhcd-vinhomes-dat-muc-tieu-loi-nhuan-cao-nhat-lich-su-60000-ty-dongke-hoach-dua-loat-chinh-sach-bung-no-ta-thi-truong-188260421095246897.chn
  fetched: ĐHĐCĐ 21/4 thông qua kế hoạch 285.000 tỷ doanh thu, 60.000 tỷ LNST (điều
    chỉnh từ 50.000 tỷ ban đầu)
  purpose: Verify sự kiện ĐHĐCĐ và con số mục tiêu chính thức
  supports_argument: Opening paragraph (tension setup sự kiện nâng mục tiêu)
- source: KB/bds/frameworks/bds-res-presales-backlog.md
  fetched: Tỷ lệ chuyển đổi doanh số chờ ghi nhận Vinhomes trên 90% trong 24 tháng
    vs Novaland chỉ 12%
  purpose: Lấy framework so sánh chất lượng backlog VHM vs NVL
  supports_argument: Bullet 5 (luận điểm tỷ lệ chuyển đổi 90% vs 12%)
- source: KB/bds/frameworks/bds-revenue-recognition-vas.md
  fetched: Mẫu hình doanh thu lồi theo quý của doanh nghiệp phát triển dân cư — quý
    bàn giao lớn vs quý không bàn giao
  purpose: Framework hiểu chu kỳ ghi nhận doanh thu BĐS
  supports_argument: Bullet 4 (chu kỳ bàn giao lớn đã bắt đầu)
skeptic_data_trail:
- source: https://vinhomes.vn/en/announcement-of-1q2025-business-results
  fetched: Q1/2025 LNST = 2.652 tỷ đồng, tăng 193% vs Q1/2024
  purpose: Verify nền so sánh Q1/2025 để kiểm tra tính hợp lệ của số 866% trong bài
    Master
  supports_argument: 'Luận điểm chính: 866% là hiệu ứng nền thấp, không phải tăng
    trưởng bền vững'
- source: https://fili.vn/2026/01/vinhomes-lai-rong-ky-luc-hon-41-ngan-ty-dong-trong-nam-2025-737-1397512.htm
  fetched: FY2025 LNST VHM = 41.000 tỷ đồng (kỷ lục)
  purpose: 'Tính so sánh năm với năm: 60.000 tỷ target 2026 vs 41.000 tỷ thực 2025
    = +46%'
  supports_argument: 'Counter-evidence bullet 1: so sánh có ý nghĩa hơn là +46% YoY
    thay vì 866%'
- source: KB/bds/frameworks/bds-res-presales-backlog.md
  fetched: 'Pitfall: bàn giao dồn cuối năm làm nhiễu con số quý, quý 4 nhiễu bởi áp
    lực hoàn thành kế hoạch'
  purpose: Framework hiểu mẫu hình doanh thu lồi theo quý của BĐS dân cư
  supports_argument: 'Bullet 2: Q1/2026 là quý cao điểm bàn giao, không lặp lại được'
- source: Lập luận tự
  fetched: 25.625 tỷ Q1 = 62% của 41.000 tỷ FY2025; còn 34.375 tỷ cho Q2-Q4
  purpose: 'Tính toán kiểm chéo: Q1 chiếm tỷ trọng bất thường cao'
  supports_argument: 'Bullet 3: câu hỏi về phân bổ Q2-Q4'
raw_article_url: https://znews.vn/vi-sao-vinhomes-bat-ngo-nang-muc-tieu-lai-len-60000-ty-nam-2026-post1645189.html
---

<!-- left -->

Ngày 21/4, Vinhomes bất ngờ điều chỉnh mục tiêu lợi nhuận sau thuế năm 2026 từ 50.000 tỷ lên 60.000 tỷ đồng — tăng 20% ngay trước thềm đại hội cổ đông. Trong bối cảnh thị trường bất động sản còn nhiều e ngại, quyết định này đặt câu hỏi: đây là tự tin hay liều lĩnh?

- **Quý 1/2026 đã chốt 43% kế hoạch cũ**: lợi nhuận sau thuế đạt 25.625 tỷ đồng, tăng 866% so với cùng kỳ năm trước, tương đương 51% kế hoạch mới 60.000 tỷ — nền móng số liệu vững chắc để ban lãnh đạo mạnh dạn điều chỉnh.

- **Doanh số chờ ghi nhận 201.600 tỷ cuối quý 1** đảm bảo doanh thu các quý tiếp theo, tăng 68% so với cùng kỳ — đây là nguồn doanh thu đã ký hợp đồng, chỉ chờ bàn giao để ghi nhận, không phải kỳ vọng thị trường.

- **30-40% kế hoạch năm đến từ doanh số đã chốt cuối 2025**: các dự án Đan Phượng, Dương Kinh, Ocean Park 2, Ocean Park 3, Vũ Yên đã có giao dịch hoàn tất — giám đốc tài chính Lê Tiến Công xác nhận đây là nền tảng để điều chỉnh mục tiêu.

- **Doanh thu quý 1 đạt 65.114 tỷ, tăng 315%** so với cùng kỳ, cho thấy chu kỳ bàn giao lớn đã bắt đầu — khác biệt cơ bản so với giai đoạn 2023-2024 khi Vinhomes chủ yếu tích luỹ doanh số chờ ghi nhận mà chưa ghi nhận doanh thu.

- **Tỷ lệ chuyển đổi doanh số chờ ghi nhận của Vinhomes trên 90%** trong 24 tháng nhờ pháp lý hoàn thiện trước khi bán — khác xa trường hợp Novaland chỉ đạt khoảng 12% do vướng quy hoạch chi tiết.

Cổ phiếu VHM phù hợp nhà đầu tư tin vào chu kỳ ghi nhận doanh thu lớn 2026-2027, chấp nhận định giá không rẻ so với giá trị tài sản ròng.

## Góc nhìn ngược

Bài Master chốt luận điểm rằng con số 866% tăng trưởng lợi nhuận là nền móng để ban lãnh đạo mạnh dạn nâng mục tiêu. Tuy nhiên, con số này cần bối cảnh quan trọng: quý 1/2025, Vinhomes chỉ ghi nhận 2.652 tỷ đồng lợi nhuận sau thuế — một quý cầm cự giữa chu kỳ với lượng bàn giao tối thiểu. Nhảy từ 2.652 tỷ lên 25.625 tỷ chủ yếu là hiệu ứng nền thấp, không phải tốc độ tăng trưởng bền vững.

- **So sánh có ý nghĩa hơn**: cả năm 2025 Vinhomes lãi kỷ lục 41.000 tỷ, mục tiêu 2026 là 60.000 tỷ — tương đương +46% so với năm trước, con số đáng nể nhưng khác xa 866% trong bài.

- **Bẫy quý bàn giao dồn**: quý 1/2026 ghi nhận 25.625 tỷ = 62% toàn bộ năm 2025. Đây là quý cao điểm bàn giao các dự án Đan Phượng, Ocean Park — không phải nhịp tăng trưởng lặp lại được mỗi quý.

- **Câu hỏi còn lại**: ba quý sau cần đạt thêm 34.375 tỷ nữa để chạm 60.000 tỷ. Liệu backlog 201.600 tỷ có đủ bàn giao đều trong Q2-Q4 hay lại dồn cuối năm như thông lệ ngành?

Verdict: **đạt có cảnh báo**. Bài không sai số liệu nhưng số 866% dễ gây hiểu lầm về tốc độ tăng trưởng thực của Vinhomes. Nhà đầu tư cần nhìn so sánh năm với năm (+46%) thay vì quý trough với quý peak.

<!-- right -->


