---
category: frameworks
title: "Food-NVL-Cycle"
last_updated: 2026-05-12
---

Deep dive: Chu kỳ giá nguyên vật liệu (NVL) và impact lên biên gộp ngành F&B VN.

## Changelog

| Ngày | Thay đổi |
|---|---|
| 2026-05-12 | v1.0 — Bootstrap. |

---

# 1. Nguyên tắc cốt lõi

```
NVL = 40-70% giá vốn F&B.
Biên gộp = f(Giá bán - Giá NVL).
Giá NVL tăng → Biên gộp giảm (lag 1-2 quý vì inventory).
Giá NVL giảm → Biên gộp tăng (lag 1-2 quý).
```

---

# 2. NVL theo phân khúc

## 2.1 Sữa (VNM)

**NVL chính:** Bột sữa (skimmed milk powder, whole milk powder)

| Nguồn | Tỷ trọng giá vốn | Theo dõi |
|---|---|---|
| Bột sữa NZ/Úc | ~40% | GDT (Global Dairy Trade) auctions — 2 tuần/lần |
| Sữa tươi nội địa | ~20% | Giá thu mua nông dân VN |
| Đường, bao bì | ~15% | Giá đường nội + giá giấy/nhựa |

**Pattern:**
- GDT tăng → VNM biên gộp giảm sau 1-2 quý (inventory buffer)
- GDT giảm → VNM biên gộp tăng sau 1-2 quý
- VNM có quyền điều chỉnh giá bán để pass-through, nhưng limited vì cạnh tranh

**Historical range GDT:**
- Đáy: 2.500-3.000 USD/tấn (Q2/2020, COVID)
- Đỉnh: 4.500-5.000 USD/tấn (Q1/2022)
- Trung bình: 3.200-3.800 USD/tấn

## 2.2 Bia (SAB, BHN)

**NVL chính:** Mạch nha (malt), hoa bia (hops)

| Nguồn | Tỷ trọng giá vốn | Theo dõi |
|---|---|---|
| Mạch nha Úc/EU | ~25% | Giá malt global + tỷ giá USD |
| Hoa bia Đức/Mỹ | ~10% | Giá hops global |
| Bao bì (chai, lon) | ~20% | Giá nhôm, thuỷ tinh |
| Thuế tiêu thụ đặc biệt | ~35% giá bán | Cố định theo % |

**Pattern:**
- Mạch nha tăng + USD tăng → SAB biên giảm
- Mạch nha ổn định, thu nhập tăng → SAB tăng ASP → biên cải thiện
- Thuế tiêu thụ đặc biệt = chi phí cố định, không thay đổi theo NVL

## 2.3 FMCG (MCH)

**NVL chính:** Bột mì (mì), ớt/muối/đường (gia vị), thịt (thịt chế biến)

| Nguồn | Tỷ trọng giá vốn | Theo dõi |
|---|---|---|
| Bột mì nhập | ~30% (mì) | Giá lúa mì CBOT + tỷ giá |
| Nông sản nội địa | ~20% | Giá ớt, muối, đường VN |
| Bao bì | ~15% | Giá nhựa, giấy |

**Pattern:**
- MCH có pricing power mạnh nhất F&B → pass-through NVL tốt
- Biên 40-50% = buffer lớn, ít bị ảnh hưởng NVL ngắn hạn
- Brand mạnh (Chinsu, Omachi) → giảm nhạy cảm giá

## 2.4 Đường (SBT, QNS mảng đường)

**NVL chính:** Mía nội địa, đường thô nhập

| Nguồn | Tỷ trọng giá vốn | Theo dõi |
|---|---|---|
| Mía nội địa | ~50% | Giá thu mua mía VN (vụ T10-T4) |
| Đường thô nhập | ~30% | Giá ICE #11 + tỷ giá + thuế CBPG |

**Pattern:**
- Giá ICE #11 tăng → giá bán tăng → DT tăng, biên có thể tăng hoặc giảm tuỳ tốc độ pass-through
- Giá ICE #11 giảm → ngược lại
- CBPG (chống bán phá giá) từ 2021 = premium bảo hộ cho đường nội

**Historical range ICE #11:**
- Đáy: 10-12 cent/lb (2020)
- Đỉnh: 25-28 cent/lb (2023)
- Trung bình: 15-20 cent/lb

---

# 3. Lag effect và cách đọc

| Khi NVL thay đổi | Impact BCTC | Thời điểm phản ánh |
|---|---|---|
| Q1 NVL tăng | Biên Q2-Q3 giảm | Inventory buffer 1-2 quý |
| Q3 NVL giảm | Biên Q4-Q1 năm sau tăng | Inventory buffer 1-2 quý |

**Bẫy:**
- VNM biên Q1 tốt trong khi GDT Q4 năm trước cao → inventory cũ giá thấp đang được sử dụng, Q2-Q3 sẽ bị
- SBT lãi kỷ lục Q4 → giá đường đỉnh, không bền

---

# 4. Checklist NVL cho Master

1. **Xu hướng NVL 2 quý gần nhất?** GDT (sữa), malt (bia), ICE #11 (đường), CBOT wheat (mì)
2. **Biên gộp QoQ thay đổi bao nhiêu?** >2 điểm % = significant
3. **DN có pass-through không?** Check giá bán trung bình (ASP) tăng hay giảm
4. **Inventory days thay đổi?** Inventory tăng + NVL giảm = smart, inventory tăng + NVL tăng = risk
5. **Tỷ giá USD ảnh hưởng?** VNM/SAB nhập NVL = USD tăng bất lợi

---

# 5. Web search keywords

- GDT dairy prices NZ
- Malt barley price Australia
- ICE sugar #11 price
- CBOT wheat price
- Vietnam milk powder import price
