# 00 — TỔNG QUAN BÀI TOÁN VÀ REPO
## Multi-step Water Level Forecasting — Quang Ha Estuarine Area

---

## 1. Vấn đề: Tại sao dự báo mực nước cửa sông khó?

Vùng cửa sông (estuary) là nơi **giao nhau** giữa nước sông từ thượng nguồn và nước triều từ biển:

```
                          THƯỢNG NGUỒN
                              |
                    +---------+---------+
                    |                   |
              Nhánh Hà Côi         Nhánh Tài Chi
              (river_flow_A)       (river_flow_B)
                    |                   |
                    +--------+----------+
                             |
                    +--------v--------+
                    |   QUANG HÀ      |  <-- Mực nước WL(t)
                    |  (cửa sông)     |
                    +--------+--------+
                             |
                    +--------v--------+
                    |  BIỂN / TRIỀU   |  <-- sea_level(t)
                    |  (downstream)    |
                    +-----------------+
```

**Thách thức:**
- Mực nước bị ảnh hưởng bởi **cả hai** nguồn: sông + biển
- Khi lũ thượng nguồn GẶP triều cường → nguy cơ ngập lụt cao
- Mối quan hệ giữa predictor và mực nước trở nên **phi tuyến tính** trong sự kiện compound

---

## 2. Mục tiêu nghiên cứu (Paper VNICT2026)

```
+------------------------------------------------------------------+
| MỤC TIÊU: Dự báo mực nước tại Quang Hà cho 3 horizon           |
|                                                                  |
|   WL(t) ──►  f₁(Xₜ) = WL(t+1)   [1 ngày tới]                  |
|   WL(t) ──►  f₃(Xₜ) = WL(t+3)   [3 ngày tới]                  |
|   WL(t) ──►  f₇(Xₜ) = WL(t+7)   [7 ngày tới]                  |
|                                                                  |
| Strategy: DIRECT (mỗi horizon có model riêng, KHÔNG recursive)   |
+------------------------------------------------------------------+
```

**5 đóng góp chính (Section I):**

```
+---+-------------------------------------------------------------------+
| # | Đóng góp                                                          |
+---+-------------------------------------------------------------------+
| 1 | Pipeline multi-step (t+1, t+3, t+7) cho Quang Hà, data 1990-2021 |
| 2 | Feature engineering: 5 nhóm feature thủy học → linearize bài toán |
| 3 | So sánh RF, XGBoost, Stacking vs baseline tuyến tính & lag        |
| 4 | Feature importance theo horizon: cơ chế thủy học khác nhau         |
| 5 | AdaptiveStack: giảm 19.1% MAE ở t+7 so với XGBoost gốc           |
+---+-------------------------------------------------------------------+
```

---

## 3. Framing quan trọng: "Surrogate" — không phải dự báo thực địa

```
╔══════════════════════════════════════════════════════════════════════╗
║  CẢNH BÁO QUAN TRỌNG NHẤT CỦA PAPER NÀY                          ║
║                                                                      ║
║  TẤT CẢ dữ liệu trong nghiên cứu là OUTPUT CỦA MÔ PHỎNG MIKE11,    ║
║  KHÔNG PHẢI đo trực tiếp tại trạm thủy văn.                        ║
║                                                                      ║
║  => Mô hình ML học mối quan hệ CỦA TRÌNH MÔ PHỎNG                 ║
║  => KHÔNG PHẢI là hệ thống dự báo thực địa đã validated             ║
║  => Paper gọi mô hình là "SURROGATE" (phần thay thế nhanh)          ║
╚══════════════════════════════════════════════════════════════════════╝
```

**Tại sao điều này quan trọng?**

```
  Dữ liệu MIKE11 (mô phỏng)          Dữ liệu đo thực tế (field)
  +---------------------------+        +---------------------------+
  | • Tuân theo phương trình  |        | • Có nhiễu đo lường      |
  |   vật lý xác định         |        | • Có missing data          |
  | • Mượt, ít nhiễu         |        | • Có lỗi sensor            |
  | • Không missing data      |        | • Có biến động ngẫu nhiên |
  | • R² > 0.998              |        | • R² dự kiến thấp hơn    |
  +---------------------------+        +---------------------------+
        ▼                                      ▼
   Mô hình ML học được                Cần validate riêng
   "surrogate" của simulator          trước khi deploy
```

**Kết quả trong paper (R² > 0.998) phản ánh tính "dễ dự báo" của dữ liệu mô phỏng, KHÔNG đảm bảo hiệu suất thực tế tương tự.**

→ Xem thêm: Thư trả lời Reviewer Comment 2, Comment 3.

---

## 4. Pipeline tổng quan

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PIPELINE DỰ BÁO MỰC NƯỚC                        │
│                                                                     │
│  ┌───────────┐    ┌──────────────────┐    ┌──────────────────┐     │
│  │  GIAI ĐOẠN │    │   GIAI ĐOẠN      │    │   GIAI ĐOẠN      │     │
│  │     1      │───►│       2           │───►│       3           │    │
│  │ Tiền xử lý│    │ Feature Eng.      │    │ Train & Evaluate  │    │
│  └───────────┘    └──────────────────┘    └──────────────────┘     │
│       │                   │                        │                │
│       ▼                   ▼                        ▼                │
│  ┌───────────┐    ┌──────────────────┐    ┌──────────────────┐     │
│  │ Raw MIKE11│    │ 41 features:     │    │ Models:          │     │
│  │ 1990-2021 │    │  • Lag (13)      │    │  • LR, Ridge     │     │
│  │ Daily     │    │  • Rolling (10)  │    │  • RF, XGBoost   │     │
│  │ 4 biến    │    │  • Seasonal (8)  │    │  • Stacking       │     │
│  │           │    │  • Interact (4)  │    │  • AdaptiveStack  │     │
│  │           │    │  • Risk (6)      │    │                   │     │
│  └───────────┘    └──────────────────┘    └──────────────────┘     │
│                           │                        │                │
│                           ▼                        ▼                │
│                    ┌──────────────┐        ┌──────────────────┐     │
│                    │ Selection:   │        │ Evaluation:       │     │
│                    │ 41 → 26-27   │        │ • MAE/RMSE/R²     │     │
│                    │ (Spearman ρ) │        │ • Walk-forward     │     │
│                    └──────────────┘        │ • Risk-zone        │     │
│                                            │ • Wilcoxon test    │     │
│                                            │ • Feature ablation │     │
│                                            └──────────────────┘     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5. Vùng nghiên cứu: Quảng Hà, Quảng Ninh

```
    VIETNAM
    ┌──────────────────────────────────────────────┐
    │                                              │
    │         ● Hanoi (Thủ đô)                     │
    │          \                                   │
    │           \  ~150 km                         │
    │            \                                 │
    │             ● Quảng Ninh Province            │
    │               │                              │
    │               ▼                              │
    │    ┌─────────────────────────┐              │
    │    │     VÙNG CỬA SÔNG       │              │
    │    │      QUẢNG HÀ           │              │
    │    │                         │              │
    │    │   ┌─────┐   ┌─────┐    │              │
    │    │   │Hà Côi│   │Tài Chi│   │              │
    │    │   │ 2380 │   │ 780  │   │  (lưu lượng  │
    │    │   │km²   │   │ km²  │   │   lưu vực)   │
    │    │   └──┬───┘   └──┬───┘   │              │
    │    │      └────┬─────┘       │              │
    │    │           ▼             │              │
    │    │     ● Ha Coi gauge      │              │
    │    │     (đo mực nước)       │              │
    │    │           │             │              │
    │    └───────────┼─────────────┘              │
    │                ▼                             │
    │         Biển Đông (Tidal boundary)           │
    └──────────────────────────────────────────────┘
```

**Đặc điểm:**
- Vùng cửa sông ven biển, Quảng Ninh, Việt Nam
- Nhận nước từ 2 nhánh sông: **Hà Côi** (chính) và **Tài Chi**
- Ảnh hưởng triều từ Biển Đông
- Dữ liệu: 32 năm (1990–2021), daily resolution

---

## 6. Dữ liệu: 4 biến gốc

```
┌──────────────────────────────────────────────────────────────────────┐
│ Biến                │ Đơn vị │ Vai trò                              │
├─────────────────────┼────────┼──────────────────────────────────────┤
│ river_flow_A        │ m³/s   │ Lưu lượng nhánh Hà Côi (biên trên 1)│
│ river_flow_B        │ m³/s   │ Lưu lượng nhánh Tài Chi (biên trên 2│
│ sea_level           │ m      │ Mực nước biển/triều (biên dưới)     │
│ water_level         │ m      │ Mực nước tại Quang Hà (KẾT QUẢ)    │
└─────────────────────┴────────┴──────────────────────────────────────┘
  Nguồn: MIKE11 hydrodynamic simulation (calibrated cho Quang Hà)
  Chu kỳ: 1990-01-01 → 2021-12-31 (11,688 ngày)
  Bản ghi: hourly → aggregated to daily (mean)
```

---

## 7. Kết quả chính (tóm tắt nhanh)

```
┌──────────────────────────────────────────────────────────────────────┐
│ Horizon │ Mô hình tốt nhất │ MAE (m) │ RMSE (m) │ R²      │ Ghi chú│
├─────────┼───────────────────┼─────────┼──────────┼─────────┼────────┤
│ t+1     │ Linear Regression │ 0.0077  │ 0.0150   │ 0.9996  │★ LR #1 │
│ t+3     │ Linear Regression │ 0.0086  │ 0.0153   │ 0.9996  │★ LR #1 │
│ t+7     │ AdaptiveStack     │ 0.0125  │ 0.0219   │ 0.9992  │★ 19.1% │
└─────────┴───────────────────┴─────────┴──────────┴─────────┴────────┘

★ Feature engineering > Model complexity (ở short horizon)
★ Ensemble chỉ có lợi ở t+7 (AdaptiveStack giảm 19.1% MAE vs XGBoost)
★ R² > 0.998 là do dữ liệu MIKE11 trơn (KHÔNG phải model quá giỏi)
```

---

## 8. Tài liệu tham khảo trong repo

| File | Mô tả | Mục đích học tập |
|------|-------|------------------|
| `papers/THU_TRA_LOI_REVIEWER.md` | Thư trả lời phản biện (7 comments) | Học scientific writing & cách trả lời reviewer |
| `papers/README.md` | Hướng dẫn tìm paper gốc | Đọc paper đầy đủ |
| `docs/learning/00-05` | Tài liệu học chi tiết | Hiểu bài toán từ A-Z |
| `docs/presentation/slides.md` | Slide mẫu 12 slide | Chuẩn bị trình bày |
| `docs/checklist.md` | Checklist công việc | Theo dõi tiến độ |

---

## 9. Liên kết với thư trả lời Reviewer

Thư trả lời (`THU_TRA_LOI_REVIEWER.md`) **thay đổi hoàn toàn framing** của paper:

| Comment | Reviewer nói gì | Tác giả phản hồi ra sao |
|---------|-----------------|--------------------------|
| Comment 1 | Walk-forward hợp lý | Đồng ý, nhưng nói rõ: chỉ 1 năm, chỉ Stacking |
| Comment 2 | Dữ liệu MIKE11 → surrogate | **Thay đổi framing toàn paper** — surrogate từ abstract |
| Comment 3 | R² > 0.998 cần giải thích | Thêm noise experiment (Section IV-G, Table IV) |
| Comment 4 | Imbalance (684/29/9) | Rebuild Table II: thêm Wilson CI, per-zone MAE |
| Comment 5 | LR tốt hơn → feature eng. là chính | Đổi tiêu đề paper, framing lại contribution |
| Comment 6 | Cần validate với data thực | Thêm roadmap 3 bước (Section V) |
| Comment 7 | Sửa lỗi tự phát hiện | 10 corrections (bug naive baseline, 19.4→19.1%, v.v.) |

---

## Tiếp theo

- [01 — Bài toán và dữ liệu](01_problem_and_data.md) — Chi tiết formulation, temporal split, MIKE11
- [02 — Feature Engineering](02_feature_engineering.md) — 41 features, 5 nhóm, ablation
- [03 — Mô hình và đánh giá](03_models_and_evaluation.md) — 10+ models, metrics, walk-forward
- [04 — Kết quả chính](04_key_findings.md) — Bảng đầy đủ, noise experiment, SHAP
- [05 — Hướng dẫn đọc paper](05_how_to_read_papers.md) — So sánh 2 phiên bản, bài học
