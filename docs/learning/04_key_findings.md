# 04 — KẾT QUẢ CHÍNH
## Tất cả bảng từ Paper Final, Phân tích chi tiết, Trả lời câu hỏi

---

## 1. TABLE VI — So sánh hiệu suất đầy đủ trên Test Set (2020–2021)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Horizon │ Model            │ Family       │ MAE    │ RMSE   │ R²       │
├─────────┼──────────────────┼──────────────┼────────┼────────┼──────────┤
│ t+1     │ Naive-lag14      │ Naive        │ 0.0814 │ 0.1019 │ 0.9818   │
│ t+1     │ Naive-lag1       │ Naive        │ 0.5370 │ 0.6006 │ 0.3673   │
│ t+1     │ Naive-lag7       │ Naive        │ 1.2847 │ 1.4416 │ −2.6455  │
│ t+1     │ ★ Linear Regr.   │ Linear       │ 0.0077 │ 0.0150 │ 0.9996   │
│ t+1     │ Ridge            │ Linear       │ 0.0086 │ 0.0157 │ 0.9996   │
│ t+1     │ Stacking         │ ML           │ 0.0105 │ 0.0186 │ 0.9994   │
│ t+1     │ XGBoost          │ ML           │ 0.0108 │ 0.0191 │ 0.9994   │
│ t+1     │ RF               │ ML           │ 0.0109 │ 0.0189 │ 0.9994   │
├─────────┼──────────────────┼──────────────┼────────┼────────┼──────────┤
│ t+3     │ Naive-lag14      │ Naive        │ 0.6001 │ 0.6751 │ 0.1986   │
│ t+3     │ Naive-lag7       │ Naive        │ 1.0999 │ 1.2320 │ −1.6693  │
│ t+3     │ ★ Linear Regr.   │ Linear       │ 0.0086 │ 0.0153 │ 0.9996   │
│ t+3     │ Ridge            │ Linear       │ 0.0140 │ 0.0201 │ 0.9993   │
│ t+3     │ XGBoost          │ ML           │ 0.0157 │ 0.0225 │ 0.9991   │
│ t+3     │ Stacking         │ ML           │ 0.0169 │ 0.0234 │ 0.9990   │
│ t+3     │ RF               │ ML           │ 0.0170 │ 0.0247 │ 0.9989   │
├─────────┼──────────────────┼──────────────┼────────┼────────┼──────────┤
│ t+7     │ Naive-lag7       │ Naive        │ 0.2120 │ 0.2374 │ 0.9011   │
│ t+7     │ Naive-lag14      │ Naive        │ 1.2609 │ 1.4148 │ −2.5132  │
│ t+7     │ Naive-lag1       │ Naive        │ 1.2846 │ 1.4413 │ −2.6460  │
│ t+7     │ Linear Regr.     │ Linear       │ 0.0216 │ 0.0286 │ 0.9986   │
│ t+7     │ Ridge            │ Linear       │ 0.0244 │ 0.0316 │ 0.9982   │
│ t+7     │ ★ XGBoost        │ ML           │ 0.0155 │ 0.0248 │ 0.9989   │
│ t+7     │ RF               │ ML           │ 0.0156 │ 0.0258 │ 0.9988   │
│ t+7     │ Stacking         │ ML           │ 0.0161 │ 0.0249 │ 0.9989   │
└─────────┴──────────────────┴──────────────┴────────┴────────┴──────────┘

★ = Mô hình tốt nhất theo MAE tại mỗi horizon
```

### Trả lời: "Tại sao Linear Regression thắng ở t+1, t+3?"

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  CÂU HỎI: Model phức tạp hơn (RF, XGBoost) có nên tốt hơn LR?     │
│  TRẢ LỜI: KHÔNG NHẤT THIẾT — vì feature engineering đã            │
│            "linearize" bài toán ở short horizon!                     │
│                                                                      │
│  Giải thích:                                                         │
│                                                                      │
│  1. Feature engineering tạo ra các feature MẠNH:                     │
│     - water_level_lag_14: tương quan 0.91 với target t+1            │
│     - distance_to_threshold, flood_pressure: bắt trực tiếp          │
│     → Mối quan hệ gần như TUYẾN TÍNH                                │
│                                                                      │
│  2. Linear Regression: ŷ = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ        │
│     → Tìm hệ số β tối ưu bằng OLS                                  │
│     → Khi mối quan hệ tuyến tính, OLS là BLUE                      │
│       (Best Linear Unbiased Estimator — định lý Gauss-Markov)       │
│                                                                      │
│  3. Ensemble (RF, XGBoost) tạo thêm BIẾN ĐỘNG                      │
│     → Giúp ở t+7 khi có nonlinear dynamics                         │
│     → Nhưng thêm nhiễu ở t+1, t+3 khi tuyến tính là đủ            │
│                                                                      │
│  4. Bài học: Feature engineering > Model complexity                  │
│     (cho short horizon, khi features đủ tốt)                        │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. TABLE XII — Advanced Model Comparison (tất cả 8 models)

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ t+1                                                                                │
│ Horizon │ Model            │ Family    │ MAE     │ RMSE    │ MAPE(%) │ R²         │
├─────────┼──────────────────┼───────────┼─────────┼─────────┼─────────┼────────────┤
│ t+1     │ ★ Stacking       │ Original  │ 0.0105  │ 0.0186  │ 3.575   │ 0.9994     │
│ t+1     │ XGBoost          │ Original  │ 0.0108  │ 0.0191  │ 3.569   │ 0.9994     │
│ t+1     │ RF               │ Original  │ 0.0109  │ 0.0189  │ 3.987   │ 0.9994     │
│ t+1     │ ExtraTrees       │ Advanced  │ 0.0113  │ 0.0239  │ 3.705   │ 0.9990     │
│ t+1     │ AdaptiveStack    │ Proposed  │ 0.0116  │ 0.0243  │ 3.659   │ 0.9990     │
│ t+1     │ LightGBM         │ Advanced  │ 0.0125  │ 0.0204  │ 4.911   │ 0.9993     │
│ t+1     │ HistGB           │ Advanced  │ 0.0140  │ 0.0223  │ 5.793   │ 0.9991     │
│ t+1     │ MLP              │ Advanced  │ 0.0207  │ 0.0281  │ 8.069   │ 0.9986     │
├─────────┼──────────────────┼───────────┼─────────┼─────────┼─────────┼────────────┤
│ t+3     │ ★ XGBoost        │ Original  │ 0.0157  │ 0.0225  │ 6.914   │ 0.9991     │
│ t+3     │ ExtraTrees       │ Advanced  │ 0.0157  │ 0.0238  │ 6.803   │ 0.9990     │
│ t+3     │ AdaptiveStack    │ Proposed  │ 0.0158  │ 0.0231  │ 6.625   │ 0.9991     │
│ t+3     │ Stacking         │ Original  │ 0.0169  │ 0.0234  │ 6.769   │ 0.9990     │
│ t+3     │ RF               │ Original  │ 0.0170  │ 0.0247  │ 6.827   │ 0.9989     │
│ t+3     │ LightGBM         │ Advanced  │ 0.0179  │ 0.0241  │ 7.791   │ 0.9990     │
│ t+3     │ HistGB           │ Advanced  │ 0.0185  │ 0.0247  │ 8.174   │ 0.9989     │
│ t+3     │ MLP              │ Advanced  │ 0.0248  │ 0.0349  │ 10.292  │ 0.9979     │
├─────────┼──────────────────┼───────────┼─────────┼─────────┼─────────┼────────────┤
│ t+7     │ ★ AdaptiveStack  │ Proposed  │ 0.0125  │ 0.0219  │ 5.311   │ 0.9992     │
│ t+7     │ ExtraTrees       │ Advanced  │ 0.0131  │ 0.0239  │ 5.751   │ 0.9990     │
│ t+7     │ XGBoost          │ Original  │ 0.0155  │ 0.0248  │ 6.442   │ 0.9989     │
│ t+7     │ RF               │ Original  │ 0.0156  │ 0.0258  │ 6.359   │ 0.9988     │
│ t+7     │ LightGBM         │ Advanced  │ 0.0161  │ 0.0245  │ 6.941   │ 0.9989     │
│ t+7     │ Stacking         │ Original  │ 0.0161  │ 0.0249  │ 6.087   │ 0.9989     │
│ t+7     │ HistGB           │ Advanced  │ 0.0171  │ 0.0262  │ 7.541   │ 0.9988     │
│ t+7     │ MLP              │ Advanced  │ 0.0255  │ 0.0334  │ 11.273  │ 0.9980     │
└─────────┴──────────────────┴───────────┴─────────┴─────────┴─────────┴────────────┘
```

### Visualize: MAE theo Model và Horizon

```
  MAE (m)
  0.025 ┤
        │                                                              MLP
  0.020 ┤  MLP                                                        ▲
        │  ▲                                                    ┌──────┤
  0.018 ┤  │ HistGB                                             │      │
        │  │ ▲  LightGBM                               HistGB  │      │
  0.016 ┤  │ │  ▲  AS                           ┌─────▲────────┤      │
        │  │ │  │  ▲  ET        ┌────┐    ┌─────┤     │  LGBM  │      │
  0.014 ┤  │ │  │  │  ▲  Stack  │    │    │     ├─────┼────────┤      │
        │  │ │  │  │  │  ▲  XGB │    │    │ ET  │     │  XGB   │      │
  0.012 ┤  │ │  │  │  │  │  ▲   │    │    │ ▲   │     │  ▲     │  ★AS │
        │  │ │  │  │  │  │  │   │    │    │ │   │     │  │     │  ▲   │
  0.010 ┤  │ │  │  │  │  │  │   │★S  │    │ │   │     │  │     │  │   │
        │  │ │  │  │  │  │  │   │▲   │    │ │   │     │  │     │  │   │
  0.008 ┤  │ │  │  │  │  │  │   │XGB │    │ │   │     │  │     │  │   │
        │  ▼ ▼  ▼  ▼  ▼  ▼  ▼   ▼▼   ▼    ▼ ▼   ▼     ▼  ▼     ▼  ▼   ▼
        └────────────────────────────────────────────────────────────────
                t+1                     t+3                    t+7
  
  ★ S = Stacking (t+1), ★ XGB = XGBoost (t+3), ★ AS = AdaptiveStack (t+7)
```

### Trả lời: "MLP luôn tệ nhất — tại sao?"

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  MLP (Multilayer Perceptron) luôn có MAE cao nhất:                   │
│  t+1: 0.0207 m (gấp 2× Stacking!)                                  │
│  t+3: 0.0248 m (gấp 1.6× XGBoost)                                  │
│  t+7: 0.0255 m (gấp 2× AdaptiveStack)                              │
│                                                                      │
│  Lý do:                                                             │
│  1. Dữ liệu tabular (bảng) → tree-based methods tốt hơn neural nets│
│  2. Feature engineering tạo feature thủ công → tree khai thác tốt   │
│  3. MLP cần nhiều data hơn để học nonlinear patterns                │
│  4. MLP nhạy cảm với scale (cần StandardScaler)                    │
│  5. Shallow NN (128-64 neurons) không đủ capacity                  │
│     → nhưng thêm layers sẽ overfit với data MIKE11                  │
│                                                                      │
│  Bài học: KHÔNG phải model phức tạp hơn = tốt hơn                   │
│  → Phù hợp với đặc điểm dữ liệu và feature set                    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. AdaptiveStack — Chi tiết cải thiện ở t+7

```
┌──────────────────────────────────────────────────────────────────────┐
│ Metric         │ XGBoost    │ AdaptiveStack │ Cải thiện             │
├────────────────┼────────────┼───────────────┼───────────────────────┤
│ MAE (m)        │ 0.0155     │ 0.0125        │ ★ −19.1%             │
│ RMSE (m)       │ 0.0248     │ 0.0219        │ −11.7%               │
│ MAPE (%)       │ 6.442      │ 5.311         │ −17.6%               │
│ R²             │ 0.9989     │ 0.9992        │ +0.0003              │
└────────────────┴────────────┴───────────────┴───────────────────────┘

  Cải thiện MAE 19.1% NGHE NHỎ nhưng trong bối cảnh:
  - XGBoost đã rất giỏi (MAE = 0.0155 m = 1.55 cm!)
  - Từ 1.55 cm → 1.25 cm = tiết kiệm 3mm
  - Cho cảnh báo lũ 7 ngày → 3mm có thể là RẤT NHIỀU
  
  Tại sao ensemble có lợi ở t+7 (nhưng không ở t+1)?
  ┌──────────────────────────────────────────────────────────────┐
  │ t+1: Mối quan hệ gần tuyến tính → LR đủ                    │
  │      Ensemble thêm variance mà không giảm bias đủ           │
  │                                                              │
  │ t+7: Mối quan hệ PHI TUYẾN MẠNH hơn                       │
  │      → River-sea interaction phức tạp                        │
  │      → Không model đơn lẻ capture hết                      │
  │      → Ensemble đa dạng (LGBM+ET+HGB+MLP) bổ trợ          │
  │      → Ridge meta-learner học cách blend tối ưu             │
  └──────────────────────────────────────────────────────────────┘
```

---

## 4. Limitations và Validation Roadmap (Section V)

```
┌──────────────────────────────────────────────────────────────────────┐
│ STT │ Limitation                        │ Nghiêm trọng?             │
├─────┼───────────────────────────────────┼───────────────────────────┤
│  1  │ Không có dữ liệu mưa, gió,       │ Trung bình                │
│     │ áp suất khí quyển                │ → bỏ lỡ meteorological    │
│     │                                   │   driven extremes         │
├─────┼───────────────────────────────────┼───────────────────────────┤
│  2  │ Chỉ 1 trạm/station               │ Trung bình                │
│     │                                   │ → chưa biết generalize    │
├─────┼───────────────────────────────────┼───────────────────────────┤
│  3  │ Dataset kết thúc 2021            │ Thấp                      │
│     │                                   │ → không evaluate post-2021│
├─────┼───────────────────────────────────┼───────────────────────────┤
│  4  │ ★ Dữ liệu MIKE11 (surrogate)     │ ★★ CAO NHẤT              │
│     │ Không phải đo thực               │ → chưa validated field    │
│     │ R² cao do simulation smoothness   │                           │
├─────┼───────────────────────────────────┼───────────────────────────┤
│  5  │ AdaptiveStack thêm complexity     │ Trung bình                │
│     │ Improvement mainly ở t+7          │                           │
├─────┼───────────────────────────────────┼───────────────────────────┤
│  6  │ Feature importance (tree-based)   │ Thấp                      │
│     │ chưa phải SHAP instance-level     │ → future work             │
└─────┴───────────────────────────────────┴───────────────────────────┘

VALIDATION ROADMAP (3 bước):
┌──────────────────────────────────────────────────────────────────────┐
│ Bước 1: Lấy dữ liệu đo thực tại Ha Coi gauge                     │
│         (từ MIKE11 calibration record)                               │
│                                                                      │
│ Bước 2: Định lượng sai số MIKE11 vs observation                    │
│         → Tách lỗi mô phỏng và lỗi mô hình                        │
│                                                                      │
│ Bước 3: Mở rộng ra nhiều trạm + compound storm-tide events         │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 5. Liên kết với thư trả lời Reviewer — Các sửa đổi quan trọng

```
┌──────────────────────────────────────────────────────────────────────┐
│ Sửa đổi                           │ Trước (submitted) → Sau (revised│
├───────────────────────────────────┼──────────────────────────────────┤
│ Tiêu đề                           │ "Ensemble ML" →                 │
│                                   │ "Feature-Engineering-Driven ML   │
│                                   │  as Surrogate"                  │
├───────────────────────────────────┼──────────────────────────────────┤
│ Surrogate framing                 │ Chỉ trong Limitations →         │
│                                   │ Abstract + Intro + Discussion   │
├───────────────────────────────────┼──────────────────────────────────┤
│ R² reporting                      │ Đơn lẻ → Dải 0.9984–0.9996    │
├───────────────────────────────────┼──────────────────────────────────┤
│ Noise experiment                  │ KHÔNG CÓ → Section IV-G,        │
│                                   │ Table IV (mới!)                 │
├───────────────────────────────────┼──────────────────────────────────┤
│ Risk-zone evaluation              │ Chỉ accuracy → + Wilson CI,     │
│                                   │ precision/recall/F1, per-zone   │
│                                   │ MAE, sample counts              │
├───────────────────────────────────┼──────────────────────────────────┤
│ Naive baseline                    │ CÓ BUG data leakage → ĐÃ SỬA  │
├───────────────────────────────────┼──────────────────────────────────┤
│ Statistical significance claim    │ "Significant at t+1" →          │
│                                   │ "NOT significant (p=0.31)"      │
├───────────────────────────────────┼──────────────────────────────────┤
│ 19.4% → 19.1%                    │ Sai số (4 lần) → ĐÃ SỬA       │
├───────────────────────────────────┼──────────────────────────────────┤
│ SHAP contradiction                │ Text nói "not SHAP" nhưng       │
│                                   │ figure là SHAP → ĐÃ SỬA        │
└───────────────────────────────────┴──────────────────────────────────┘
```

---

## 6. Trả lời các câu hỏi thường gặp

### Q1: "Sao R² cao vậy? Mô hình có thật sự giỏi không?"

**A:** R² > 0.998 phản ánh tính chất của DỮ LIỆU MÔ PHỎNG MIKE11, không phải model quá giỏi:
- MIKE11 tuân theo phương trình Saint-Venant → dynamics mượt
- Không có nhiễu đo lường, không missing data
- Khi thêm Gaussian noise σ = 1cm → MAE tăng 40%
- Walk-forward MAPE (3.4%–7.2%) là ước tính thực tế hơn

### Q2: "Model áp dụng trực tiếp ngoài thực tế được không?"

**A:** Chưa. Paper rõ ràng nói: "further validation with field observations is warranted." Cần:
1. Lấy dữ liệu đo thực từ Ha Coi gauge
2. Tách lỗi mô phỏng vs lỗi mô hình
3. Validate trên nhiều trạm và nhiều sự kiện extreme

### Q3: "Tại sao Linear Regression tốt hơn ensemble?"

**A:** Feature engineering đã "linearize" bài toán:
- `water_level_lag_14` tương quan 0.91 với target t+1
- OLS (Linear Regression) là BLUE khi mối quan hệ tuyến tính
- Ensemble thêm variance mà không giảm bias đủ → tệ hơn
- Chỉ ở t+7 khi nonlinear dynamics mạnh → ensemble mới có lợi

### Q4: "9 ngày Exceedance có đủ không?"

**A:** Không đủ cho kết luận mạnh:
- Wilson 95% CI = [0.354, 0.879] → quá rộng
- Không thể phân biệt với coin flip (random = 0.5)
- Tuy nhiên: KHÔNG có ngày Exceedance nào bị phân loại thành Normal
- Tất cả lỗi downgrade xuống Warning (direction an toàn)
- Cần thêm dữ liệu extreme events

### Q5: "Noise experiment cho thấy gì?"

**A:** Đo khoảng cách simulator → field:
- σ = 1cm → MAE Stacking tăng 40% (t+1)
- σ = 2cm → ranking thay đổi: XGBoost > LR (t+1)
- σ = 5cm → LR t+3 collapse (0.33 m!) vs XGBoost (0.08 m)
- Kết luận: regularization và model diversity quan trọng khi có noise
