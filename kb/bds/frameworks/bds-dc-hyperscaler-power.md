---
category: frameworks
title: "BDS-DC-Hyperscaler-Power"
last_updated: 2026-05-11
notion_page_id: "35d273c7-a9a1-8165-adb0-f87372d60534"
source_url: "https://notion.so/35d273c7a9a18165adb0f87372d60534"
applies_to: ["data_center"]
---

# Trung tâm dữ liệu và ràng buộc hạ tầng điện tại Việt Nam

File này giải thích bất động sản trung tâm dữ liệu Việt Nam — phân khúc mới nổi từ 2024 với nhu cầu từ khách hàng đám mây lớn và ràng buộc hạ tầng điện. Master đọc trước khi viết bài về Kinh Bắc (KBC) — có SGI-HCM Campus trung tâm dữ liệu AI 2 tỷ đô la Mỹ, FPT, Becamex, hoặc Viettel Global Investment (VGI). Chưa có thuần phân khúc trung tâm dữ liệu niêm yết Việt Nam — phải đọc báo cáo phân khúc.

## Khái niệm & cơ chế

Trung tâm dữ liệu là cơ sở vật lý lưu trữ và xử lý dữ liệu. Đo bằng ba đơn vị:

- **Megawatt (MW)** — công suất điện công nghệ thông tin (máy chủ)
- **Vị trí rack server** — số rack server có thể chứa
- **Diện tích sàn (mét vuông)** — diện tích vật lý

Tại Việt Nam, ngành trung tâm dữ liệu mang đặc điểm: quy mô nhỏ so với Singapore và Indonesia (trung tâm khu vực); tăng trưởng nhanh từ 2023-2024 do bùng nổ trí tuệ nhân tạo; yêu cầu điện lớn → tập trung tại vùng có điện ổn.

Ba loại doanh nghiệp trung tâm dữ liệu:

**Khách hàng đám mây lớn (Google, Amazon Web Services, Microsoft Azure, Meta)** — có trung tâm dữ liệu riêng. Quy mô: hàng trăm megawatt mỗi cơ sở. Việt Nam: chưa có khách hàng đám mây lớn tự xây hoàn toàn (do quy định dữ liệu chủ quyền Việt Nam). Thay vào đó: khách hàng đám mây lớn thuê đồng định vị.

**Đồng định vị (trung tâm dữ liệu phục vụ cho thuê chỗ cho nhiều công ty)** — Viettel IDC, FPT Telecom DC, CMC Telecom DC, VNPT IDC. Quy mô: 10-50 megawatt mỗi cơ sở. Khách: khách hàng đám mây lớn, thương mại điện tử, công nghệ tài chính, cơ quan nhà nước.

**Trung tâm dữ liệu doanh nghiệp (một công ty tự có riêng)** — quy mô nhỏ, chỉ phục vụ riêng. Vietcombank, BIDV, Vingroup có trung tâm dữ liệu riêng.

Cơ chế bùng nổ trí tuệ nhân tạo → nhu cầu trung tâm dữ liệu:

Trước 2023, trung tâm dữ liệu chủ yếu cho điện toán đám mây (Amazon Web Services, Azure), thương mại điện tử (Shopee, Lazada, Tiki), trò chơi (VNG, VTV), công nghệ tài chính.

Từ 2023, trí tuệ nhân tạo tác động mạnh: huấn luyện mô hình GPU cần điện gấp 10-100 lần mỗi rack; máy chủ GPU NVIDIA và AMD cần làm mát bằng chất lỏng; khách hàng đám mây lớn mở rộng nhanh chóng.

Tác động Việt Nam: Kinh Bắc công bố SGI-HCM Campus trung tâm dữ liệu AI 2 tỷ đô la Mỹ tại khu công nghiệp Tân Phú Trung; Viglacera (VGC), Viettel Industrial, FPT Telecom đầu tư mở rộng; NVIDIA mở trung tâm nghiên cứu phát triển tại Hà Nội và Thành phố Hồ Chí Minh → cần trung tâm dữ liệu hỗ trợ.

## Threshold benchmark dài hạn

Yêu cầu điện trung tâm dữ liệu:

- 1 rack chuẩn: 10-20 kilowatt
- 1 rack huấn luyện trí tuệ nhân tạo: 50-100 kilowatt
- 1 cơ sở 30 megawatt: khoảng 1.500-3.000 rack

Hạ tầng điện Việt Nam:

- Tổng công suất phát điện Việt Nam năm 2024: khoảng 80 gigawatt
- Dự báo 2030: 130-150 gigawatt
- Tăng trưởng trung tâm dữ liệu 2024-2030: 0,5-1 gigawatt (nhỏ nhưng giá trị cao)

Vùng có điện ổn nhất cho trung tâm dữ liệu:

- Thành phố Hồ Chí Minh và Bình Dương (gần nguồn phát điện)
- Hà Nội và Bắc Ninh
- Một số khu công nghiệp ven Thành phố Hồ Chí Minh có điện dự phòng

Yêu cầu mới — bền vững:

- Năng lượng tái tạo (cam kết phát thải ròng bằng không của khách hàng đám mây lớn) → Kinh Bắc cộng Sembcorp cộng Becamex liên doanh năng lượng tái tạo
- Nguồn nước làm mát bằng chất lỏng

Định giá thuê trung tâm dữ liệu Việt Nam (đồng định vị):

- Rack chuẩn (5-10 kilowatt): 5-10 triệu đồng mỗi tháng
- Rack mật độ cao (15-25 kilowatt): 15-30 triệu đồng mỗi tháng
- Rack trí tuệ nhân tạo (50-100 kilowatt): 80-150 triệu đồng mỗi tháng + chi phí điện tách riêng

Doanh thu trung tâm dữ liệu trên mỗi megawatt (gồm cả điện + làm mát + diện tích + dịch vụ): 8-15 triệu đô la Mỹ trên megawatt mỗi năm — lớn hơn khu công nghiệp nhiều.

Biên lợi nhuận: cao hơn khu công nghiệp khoảng 30-50% biên gộp.

Trên thế giới, trung tâm dữ liệu được định giá hệ số giá trị doanh nghiệp trên lợi nhuận trước lãi vay thuế và khấu hao 18-25 lần (so với văn phòng 12-15 lần, khu công nghiệp 8-12 lần). Lý do: doanh thu cực ổn định, hợp đồng dài 5-10 năm, hợp đồng thường "trả dù không sử dụng" (khách phải trả dù không dùng), chi phí đầu tư cao nhưng rào cản gia nhập rất bền, bùng nổ trí tuệ nhân tạo tăng nhu cầu dài hạn. Tại Việt Nam, trung tâm dữ liệu chưa có thuần phân khúc niêm yết, khó ước tính định giá.

## Pitfalls (đọc số dễ sai)

- **Bẫy 1**: "Bùng nổ trí tuệ nhân tạo" giá cổ phiếu khu công nghiệp và trung tâm dữ liệu là giao dịch theo đà tăng. Nhà đầu tư Việt Nam dễ bị câu chuyện hấp dẫn. Cần tách rõ thực tế và câu chuyện kể.
- **Bẫy 2**: Kinh Bắc SGI-HCM Campus 2 tỷ đô la Mỹ — con số tổng vốn. Chưa có thời gian hoàn thành cấp tốc. Doanh thu Kinh Bắc lớn từ trung tâm dữ liệu sẽ là 2027-2028 sớm nhất.
- **Bẫy 3**: "Trung tâm dữ liệu = biên lợi nhuận cao" KHÔNG đúng tại Việt Nam. Chi phí điện cao cộng làm mát đắt cộng cạnh tranh giữa Viettel, VNPT, FPT → biên lợi nhuận thấp hơn thị trường phát triển.
- **Bẫy 4**: Quy định dữ liệu chủ quyền Việt Nam — từ 2019, một số loại dữ liệu phải lưu tại Việt Nam. Tăng nhu cầu trung tâm dữ liệu NHƯNG cũng giới hạn khách hàng đám mây lớn tự xây.
- **Bẫy 5**: Quan hệ đối tác NVIDIA công bố KHÔNG đồng nghĩa doanh thu năm sau. Các quan hệ đối tác Nhà máy AI thường mất 18-36 tháng từ công bố đến vận hành.
- **Bẫy 6**: Cam kết bền vững của khách hàng đám mây lớn — Microsoft, Google, Amazon Web Services cam kết 100% năng lượng tái tạo đến năm 2030. Trung tâm dữ liệu Việt Nam phải sở hữu nguồn năng lượng tái tạo → Becamex và Kinh Bắc mạnh hơn vì có liên doanh năng lượng tái tạo.

## Case study lịch sử

> **2026 — Trung tâm dữ liệu — Kinh Bắc công bố SGI-HCM Campus 2 tỷ đô la Mỹ**:
> Kinh Bắc công bố hợp tác với SGI (đối tác chưa công khai chi tiết) xây dựng SGI-HCM Campus trung tâm dữ liệu trí tuệ nhân tạo 2 tỷ đô la Mỹ tại khu công nghiệp Tân Phú Trung Thành phố Hồ Chí Minh. Nguồn điện từ điện gió Gia Lai (1,1 tỷ kilowatt giờ mỗi năm). Triển khai 2025-2026. Doanh thu lớn từ dự án này sẽ là 2027-2028 sớm nhất vì xây dựng trung tâm dữ liệu công suất cao mất 18-36 tháng. Bài học: nhà đầu tư không nên giả định doanh thu đến ngay sau khi công bố hợp đồng — cần thời gian xây dựng và khởi động.
>
> **Không analogize sang**: khu công nghiệp truyền thống (xem `bds-kcn-fdi-demand-mechanism.md`) — doanh thu ghi nhận một lần khi ký hợp đồng thuê đất, không cần thời gian xây dựng 18-36 tháng như trung tâm dữ liệu.

## Regulatory

- Luật An ninh mạng — quy định dữ liệu chủ quyền Việt Nam, một số loại dữ liệu phải lưu tại Việt Nam
- Luật Bảo vệ Dữ liệu cá nhân — quy định bảo vệ dữ liệu công dân

## Source log

- https://notion.so/35d273c7a9a18165adb0f87372d60534
- cafeland.vn 10/2/2026 — Kinh Bắc SGI-HCM Campus trung tâm dữ liệu AI 2 tỷ đô la Mỹ tại Tân Phú Trung
- Báo cáo tài chính FPT Corporation — phân khúc trung tâm dữ liệu FPT Telecom
- Báo cáo tài chính Becamex — liên doanh Sembcorp năng lượng tái tạo
- Stamp: build 2026-05-11. Review every 1 year (công nghệ và quy định trung tâm dữ liệu thay đổi nhanh).
