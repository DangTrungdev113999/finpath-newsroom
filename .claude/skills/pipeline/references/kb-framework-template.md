# KB Framework Template

Template cho file `<sector>-industry-master-reference.md` khi thêm ngành mới.

Copy và customize các placeholder.

---

```markdown
---
category: frameworks
title: "<Sector>-Industry-Master-Reference"
last_updated: <YYYY-MM-DD>
---

Master reference cho Master <Sector> — mental model 6 lớp phân tích ngành <tên tiếng Việt>. File này là neo nhận thức: đọc trước khi phân tích bất kỳ mã nào thuộc nhóm **<TICKER_LIST>**.

## Changelog

| Ngày | Thay đổi |
|---|---|
| <YYYY-MM-DD> | v1.0 — Bootstrap KB <sector> với <N> mã universe. |

---

# LỚP 1: HIỂU NGÀNH

## 1.1 Chuỗi giá trị

[Mô tả chuỗi giá trị ngành — các khâu chính, ai làm gì]

```
KHÂU 1               KHÂU 2               KHÂU 3
────────────────────────────────────────────────
Mô tả                Mô tả                Mô tả
    │                    │                    │
    ▼                    ▼                    ▼
TICKER1              TICKER2              TICKER3
```

## 1.2 Phân loại doanh nghiệp

| Mã | Tên | Đặc trưng cấu trúc |
|---|---|---|
| TICKER1 | Tên công ty | Mô tả ngắn đặc điểm |
| TICKER2 | Tên công ty | Mô tả ngắn đặc điểm |
| ... | ... | ... |

## 1.3 Ai quyết định luật chơi

| Yếu tố | Vai trò | Tác động |
|---|---|---|
| Yếu tố 1 | Vai trò gì | Tác động thế nào |
| Yếu tố 2 | ... | ... |

---

# LỚP 2: ĐỌC SỐ

## 2.1 Metrics quan trọng

### Tier 1 — Phản ứng ngay

| Metric | Ý nghĩa | Áp dụng | Benchmark |
|---|---|---|---|
| Metric 1 | Ý nghĩa | Mã nào | Ngưỡng tốt/xấu |
| Metric 2 | ... | ... | ... |

### Tier 2 — Phản ứng chậm

| Metric | Ý nghĩa | Áp dụng |
|---|---|---|
| Metric 1 | ... | ... |

## 2.2 Bẫy BCTC

| Bẫy | Phải làm gì |
|---|---|
| Bẫy 1 | Cách xử lý |
| Bẫy 2 | ... |

---

# LỚP 3: HIỂU CHU KỲ

## 3.1 Nguyên tắc cốt lõi

[Mô tả đặc điểm chu kỳ ngành — có chu kỳ không, bao lâu, driver là gì]

## 3.2 Các giai đoạn chu kỳ

| Giai đoạn | Đặc điểm | Tín hiệu nhận diện | Giá cổ phiếu |
|---|---|---|---|
| Đáy | ... | ... | ... |
| Hồi phục | ... | ... | ... |
| Tăng trưởng | ... | ... | ... |
| Đỉnh | ... | ... | ... |

## 3.3 Tín hiệu sớm

### Đáy hình thành
- Tín hiệu 1
- Tín hiệu 2

### Đỉnh hình thành
- Tín hiệu 1
- Tín hiệu 2

---

# LỚP 4: HIỂU VĨ MÔ

## 4.1 Yếu tố vĩ mô tác động

| Yếu tố | Tác động |
|---|---|
| Yếu tố 1 | Mô tả |
| Yếu tố 2 | ... |

## 4.2 Động lực & Rủi ro

### Động lực cấu trúc (dài hạn)
- Động lực 1
- Động lực 2

### Rủi ro cấu trúc (dài hạn)
- Rủi ro 1
- Rủi ro 2

---

# LỚP 5: ĐỊNH GIÁ

## 5.1 Phương pháp phổ biến

| Phân khúc | Phương pháp | Ghi chú |
|---|---|---|
| Phân khúc A | P/E, EV/EBITDA | ... |
| Phân khúc B | DCF, P/B | ... |

## 5.2 Vùng định giá lịch sử

| Mã | P/E range | P/B range |
|---|---|---|
| TICKER1 | X-Yx | A-Bx |
| TICKER2 | ... | ... |

## 5.3 Bẫy định giá

| Bẫy | Thực tế |
|---|---|
| Bẫy 1 | Giải thích |
| Bẫy 2 | ... |

---

# LỚP 6: TƯ VẤN

## 6.1 Phân biệt loại rủi ro

| Tình huống | Loại | Phản ứng |
|---|---|---|
| Tình huống 1 | Biến động/Chu kỳ/Sự kiện | Hành động |
| ... | ... | ... |

## 6.2 Tư vấn theo profile

### Dài hạn (>1 năm)
- Focus: ...
- Ưu tiên: ...
- Tránh: ...

### Trung hạn (3-12 tháng)
- Focus: ...

### Ngắn hạn (<3 tháng)
- Focus: ...

## 6.3 Ngôn ngữ cho NĐT retail

| Thuật ngữ | Dịch dễ hiểu |
|---|---|
| Term 1 | Giải thích đơn giản |
| Term 2 | ... |

---

# PHỤ LỤC

## A. Hướng dẫn tra dữ liệu

### Finpath API
- Endpoint 1: `GET /api/v1/...`
- Endpoint 2: ...

### Web search keywords
- Keyword 1: "..."
- Keyword 2: "..."

## B. Nguồn tham khảo
- [Link 1](url) — mô tả
- [Link 2](url) — mô tả
```

---

## Fill Guide

1. **Lớp 1**: Research chuỗi giá trị ngành, phân loại công ty
2. **Lớp 2**: Xác định KPIs chính, benchmark ngành
3. **Lớp 3**: Xác định có chu kỳ không, nếu có thì driver là gì
4. **Lớp 4**: Macro factors ảnh hưởng ngành
5. **Lớp 5**: Phương pháp định giá phù hợp, range lịch sử
6. **Lớp 6**: Hướng dẫn cho Master khi tư vấn

**Tip**: Web search để fill data thực tế. Không cần fill 100% ngay — có thể bổ sung sau.
