---
title: BIDV lãi Q1 tăng 15,6% — nhưng nợ xấu tăng 21,9% nói lên điều gì?
ticker: BID
sector: Bank
sector_icon: 🏦
crawled_at: '2026-05-10T07:05:33.740788+00:00'
funnel_batch_id: BID-20260510-0705
left_meta:
  author: Chuyên gia ngân hàng
  word_count: 378
  key_view: thận trọng
  skeptic_verdict: pass_with_caveats
  pipeline_version: V4.0
insight: 'BIDV Q1 2026: lợi nhuận tăng nhờ mở rộng tín dụng, nhưng nợ xấu tăng nhanh
  hơn lợi nhuận (21,9% vs 15,6%), dự phòng chỉ che 87% — tăng trưởng thật sự hay tích
  lũy rủi ro là câu hỏi trung tâm.'
right_source:
  name: Báo Tin tức
  url: https://vietnambiz.vn/ngan-hang-co-quy-mo-lon-nhat-he-thong-bao-lai-quy-i-hon-8500-ty-no-xau-tang-hon-7600-ty-2026429174923937.htm
  published: '2026-04-30'
  raw_title: Ngân hàng có quy mô lớn nhất hệ thống báo lãi quý I hơn 8.500 tỷ, nợ
    xấu tăng hơn 7.600 tỷ
why_chosen_narrative: 'Paradox rõ ràng: lợi nhuận tăng trưởng tốt trong khi nợ xấu
  tăng nhanh hơn — tạo câu hỏi về chất lượng tăng trưởng. Số liệu cụ thể (42.654 tỷ
  nợ xấu, tỷ lệ 1.76%) cho phép phân tích sâu.'
angle_label: paradox
angle_narrative: BIDV báo lãi Q1 tăng 15.6% nhưng nợ xấu tăng 21.9% cùng kỳ — hai
  tín hiệu đối nghịch phát ra cùng lúc từ ngân hàng lớn nhất hệ thống
deep_question_options:
- idx: 0
  category: paradox
  question: BIDV lãi Q1 tăng 15.6% nhưng nợ xấu tăng 21.9% — tăng trưởng thật sự hay
    tích lũy rủi ro?
  writeability: high
- idx: 1
  category: hidden_mechanism
  question: Vì sao dự phòng chỉ che phủ 87% nợ xấu trong khi BIDV vẫn báo lãi cao
    — cơ chế nào đứng sau?
  writeability: medium
chosen_question_idx: 0
chosen_pick_reason: ''
skip_reasons: {}
crawl_funnel:
  picked:
  - source: VnEconomy
    url: https://vneconomy.vn/dai-dien-big-4-ngan-hang-kien-nghi-duoc-ban-no-xau-thap-hon-gia-tri-so-sach.htm
    published: '2026-03-27'
    reason: 'Comparison deep: BIDV kiến nghị chính sách bán nợ xấu đúng lúc mình có
      nợ xấu lớn nhất — phân tích động cơ và phân phối lợi ích'
  - source: Thời báo Tài chính
    url: https://thoibaotaichinhvietnam.vn/bidv-quyet-liet-tang-von-dieu-le-nham-moc-100000-ty-dong-phan-dau-tang-tong-tai-san-5-10-195999.html
    published: '2026-04-20'
    reason: 'Hidden mechanism: tăng vốn đồng thời nợ xấu leo thang — chiến lược phòng
      thủ tài chính chủ động'
  - source: Báo Tin tức
    url: https://vietnambiz.vn/ngan-hang-co-quy-mo-lon-nhat-he-thong-bao-lai-quy-i-hon-8500-ty-no-xau-tang-hon-7600-ty-2026429174923937.htm
    published: '2026-04-30'
    reason: 'Paradox: lợi nhuận tăng 15.6% vs nợ xấu tăng 21.9% — chất lượng tăng
      trưởng Q1 đặt câu hỏi'
  rejected:
  - source: Thời báo Tài chính
    url: https://vneconomy.vn/thu-tuong-yeu-cau-thi-diem-go-bo-room-tin-dung-tu-nam-2026.htm
    published: '2025-08-07'
    reject_agent: editor_v1
    reject_label: Gác cổng bỏ
    reason: Thủ tướng yêu cầu thí điểm bỏ room tín dụng 2026 — bài 8/2025, quá cũ
      (>30 ngày từ hôm nay 5/2026), macro policy, không BID-specific. Reject.
  - source: Nhịp sống Kinh tế
    url: https://vneconomy.vn/ngan-hang-nha-nuoc-co-the-giam-chi-tieu-tin-dung-neu-rui-ro-gia-tang.htm
    published: '2026-04-14'
    reject_agent: editor_v1
    reject_label: Gác cổng bỏ
    reason: NHNN có thể giảm chỉ tiêu tín dụng — macro policy article, không đặc thù
      BID, không đủ primary anchor. Reject.
  - source: Tuổi Trẻ
    url: https://tuoitre.vn/bidv-lai-lon-nhung-no-xau-khoang-27-600-ti-dong-cu-the-ket-qua-kinh-doanh-ra-sao-20260107140015676.htm
    published: '2026-01-07'
    reject_agent: story_editor
    reject_label: Tổng biên tập bỏ
    reason: Bài 2025 full-year — quá cũ so với Q1 2026 fresh data, góc nhìn historical
      không đủ writeability riêng.
  total_candidates: 10
master_data_trail: []
skeptic_data_trail:
- source: Kiến thức ngành ngân hàng Việt Nam — mùa vụ nợ xấu Q1
  fetched: '2026-05-10'
  purpose: 'Ngữ cảnh mùa vụ: nợ xấu Q1 thường cao nhất năm do doanh nghiệp tất toán
    cuối năm'
  supports_argument: 'Alt interpretation: spike Q1 có thể là mùa vụ, không phải tích
    lũy hệ thống'
- source: KB/Big4-vs-Tunhan — so sánh tỷ lệ dự phòng hệ thống
  fetched: '2026-05-10'
  purpose: Tỷ lệ dự phòng 60-75% ở ngân hàng tư nhân vs 87% BIDV
  supports_argument: Framing thiếu ngữ cảnh so sánh — 87% vẫn tốt hơn nhiều ngân hàng
    khác
raw_article_url: https://vietnambiz.vn/ngan-hang-co-quy-mo-lon-nhat-he-thong-bao-lai-quy-i-hon-8500-ty-no-xau-tang-hon-7600-ty-2026429174923937.htm
---

<!-- left -->

BIDV mở đầu 2026 với kết quả tài chính hai mặt: lợi nhuận trước thuế quý I đạt 8.572 tỷ đồng, tăng 15,6% so cùng kỳ, nhưng cùng lúc đó nợ xấu tăng 21,9% lên 42.654 tỷ đồng, đẩy tỷ lệ nợ xấu từ 1,47% lên 1,76%. Đây là nghịch lý mà nhà đầu tư cần giải mã trước khi đọc con số lợi nhuận.

- **Thu nhập lãi thuần 15.734 tỷ đồng tăng 12,8%** là động lực chính giúp lợi nhuận tăng trưởng, nhưng mức tăng này phần lớn đến từ việc mở rộng dư nợ tín dụng 2,4% trong quý — tức là tăng trưởng quy mô, không phải cải thiện biên lãi vay.

- **Nợ xấu tuyệt đối tăng thêm hơn 7.600 tỷ đồng chỉ trong 3 tháng**: từ khoảng 35.000 tỷ cuối 2025 lên 42.654 tỷ cuối quý I/2026 — tốc độ hình thành nợ xấu vượt xa tốc độ xử lý, tích lũy áp lực cho các quý tiếp theo.

- **Dự phòng rủi ro tín dụng 37.061 tỷ đồng chỉ bao phủ 87% nợ xấu**: so với nhiều quý trước khi tỷ lệ này thường trên 100%, đây là tín hiệu rõ ràng rằng BIDV đang chấp nhận mức đệm thấp hơn để bảo vệ lợi nhuận ngắn hạn, đánh đổi sức chịu đựng dài hạn.

- **Tiền gửi khách hàng giảm 3,7% trong quý** xuống 2,14 triệu tỷ đồng trong bối cảnh cạnh tranh huy động vốn gay gắt — BIDV thừa nhận huy động vốn quý I rất căng thẳng, buộc phải tăng lãi suất tiết kiệm kỳ hạn 24-36 tháng lên 6,5%/năm, tăng thêm 1,2 điểm phần trăm, đẩy chi phí vốn lên cao hơn.

- **Hoạt động kinh doanh khác tăng vọt 70%** đóng góp 2.067 tỷ đồng vào thu nhập — mức tăng đột biến này cần theo dõi tính bền vững, vì không phản ánh mảng ngân hàng cốt lõi.

Ngân hàng lớn nhất hệ thống đang ở thời điểm thử thách: lợi nhuận ngắn hạn trông tốt, nhưng nợ xấu tích lũy đặt câu hỏi về chất lượng tăng trưởng — phù hợp với nhà đầu tư giá trị chấp nhận rủi ro trung hạn và theo dõi sát tỷ lệ nợ xấu quý II/2026.

## Góc nhìn ngược

Bài phân tích dựng nghịch lý thuyết phục nhưng có một hướng đọc khác chưa được kiểm tra: nợ xấu tăng mạnh trong quý I thường có yếu tố mùa vụ. Doanh nghiệp Việt Nam thường dồn nợ đến hạn vào đầu năm sau khi tất toán dòng tiền cuối năm — điều này khiến quý I thường là điểm nợ xấu cao nhất trong năm, không phản ánh xu hướng tích lũy dài hạn.

Điểm thứ hai: tỷ lệ dự phòng 87% của BIDV vẫn cao hơn nhiều ngân hàng tư nhân trong hệ thống đang duy trì mức 60-75%. Framing '87% thay vì trên 100%' là đúng về chiều hướng nhưng thiếu ngữ cảnh so sánh — BIDV vẫn đang che phủ nợ xấu tốt hơn phần lớn đồng nghiệp.

Câu hỏi cần trả lời trong quý II: nếu nợ xấu đảo chiều giảm (như thường xảy ra sau quý I), nghịch lý sẽ tan biến và bài viết mất điểm tựa. Nhà đầu tư nên đặt mốc kiểm tra tỷ lệ nợ xấu vào 30/6/2026 trước khi kết luận về 'tích lũy rủi ro'.

<!-- right -->


