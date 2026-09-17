# 03 — MÔ HÌNH VÀ ĐÁNH GIÁ
## 10+ Mô hình, Metrics, Walk-forward, Risk-zone, Noise Experiment

---

## 1. Tất cả mô hình được đánh giá

### Baselines (Naive & Linear)

```
┌──────────────────────────────────────────────────────────────────────┐
│ Mô hình          │ Gia đình    │ Công thức / Mô tả                  │
├──────────────────┼─────────────┼─────────────────────────────────────┤
│ Naive-lag1       │ Naive       │ ŴL(t+h) = WL(t)                   │
│                  │             │ Dự báo = giá trị HÔM QUA           │
├──────────────────┼─────────────┼─────────────────────────────────────┤
│ Naive-lag7       │ Naive       │ ŴL(t+h) = WL(t-7+h)              │
│                  │             │ Dự báo = giá trị 7 ngày trước      │
│                  │             │ (bắt chu kỳ tuần)                   │
├──────────────────┼─────────────┼─────────────────────────────────────┤
│ Naive-lag14      │ Naive       │ ŴL(t+h) = WL(t-14+h)             │
│                  │             │ Dự báo = giá trị 14 ngày trước     │
│                  │             │ (bắt chu kỳ triều nửa tháng)        │
│                  │             │ ★ Tốt nhất trong baselines ở t+1   │
├──────────────────┼─────────────┼─────────────────────────────────────┤
│ Linear Regr.     │ Linear      │ ŷ = Xβ + ε                        │
│                  │ baseline    │ β* = (X^T X)^{-1} X^T y            │
│                  │             │ (OLS — Ordinary Least Squares)      │
│                  │             │ ★ MAE THẤP NHẤT ở t+1, t+3!       │
├──────────────────┼─────────────┼─────────────────────────────────────┤
│ Ridge            │ Linear      │ β* = argmin(||y - Xβ||² + α||β||²)│
│                  │ baseline    │ Regularized LR (L2 penalty)        │
│                  │             │ α = 1.0 (paper)                     │
└──────────────────┴─────────────┴─────────────────────────────────────┘
```

### Mô hình chính (Existing ML)

```
┌──────────────────────────────────────────────────────────────────────┐
│ Mô hình          │ Gia đình    │ Nguyên lý hoạt động                │
├──────────────────┼─────────────┼─────────────────────────────────────┤
│ Random Forest    │ Bagging     │ ★ Tạo B cây quyết định (B=500)    │
│ (RF)             │             │ ★ Mỗi cây train trên bootstrap     │
│                  │             │   sample (lấy ngẫu nhiên có hoàn   │
│                  │             │   lại từ train set)                │
│                  │             │ ★ Dự báo = TRUNG BÌNH B cây       │
│                  │             │ ★ Giảm VARIANCE (overfitting)      │
│                  │             │                                     │
│                  │             │ Importance = Mean Decrease Impurity │
│                  │             │ MDI = Σ(trees) Δimpurity(feature)  │
│                  │             │   / n_trees                        │
├──────────────────┼─────────────┼─────────────────────────────────────┤
│ XGBoost          │ Gradient    │ ★ Học TUẦN TỰ: cây sau sửa lỗi   │
│                  │ Boosting    │   của cây trước                    │
│                  │             │ ★ ŷ_m = ŷ_{m-1} + η × h_m(x)     │
│                  │             │   η = learning rate (0.05)         │
│                  │             │ ★ h_m fit vào GRADIENT of loss     │
│                  │             │ ★ Giảm BIAS (underfitting)         │
│                  │             │                                     │
│                  │             │ Importance = Total Gain             │
│                  │             │ Gain = Σ(boosting rounds) gain(f)  │
├──────────────────┼─────────────┼─────────────────────────────────────┤
│ Stacking         │ Meta-       │ ★ Kết hợp RF + XGBoost            │
│                  │ Learning    │ ★ Meta-learner: Ridge Regression   │
│                  │             │ ★ Train trên out-of-fold preds     │
│                  │             │   với TEMPORAL GAP (tránh leakage) │
│                  │             │ ★ MAE tốt nhất ở t+1 (0.0105)     │
└──────────────────┴─────────────┴─────────────────────────────────────┘
```

### Mô hình nâng cao + AdaptiveStack

```
┌──────────────────────────────────────────────────────────────────────┐
│ Mô hình             │ Gia đình   │ Đặc điểm riêng                  │
├─────────────────────┼────────────┼───────────────────────────────────┤
│ ExtraTrees          │ Bagging    │ RF + thêm ngẫu nhiên: split      │
│                     │            │ threshold ngẫu nhiên (không tìm  │
│                     │            │ optimal split) → giảm variance   │
│                     │            │ ★ #2 ở t+3, t+7                 │
├─────────────────────┼────────────┼───────────────────────────────────┤
│ LightGBM            │ Gradient   │ Histogram-based splitting:       │
│                     │ Boosting   │ chia giá trị feature thành bins  │
│                     │            │ → nhanh hơn XGBoost cho data lớn│
│                     │            │ Leaf-wise growth (không level-   │
│                     │            │ wise) → sâu hơn ở nhánh tốt    │
├─────────────────────┼────────────┼───────────────────────────────────┤
│ HistGradientBoost   │ Gradient   │ scikit-learn's histogram-based   │
│                     │ Boosting   │ gradient boosting + early stopping│
│                     │            │ Loss = MAE                        │
├─────────────────────┼────────────┼───────────────────────────────────┤
│ MLP                 │ Neural     │ Feedforward NN:                  │
│                     │ Network    │ Input → 128 (ReLU) → 64 (ReLU)  │
│                     │            │ → Output                          │
│                     │            │ Optimizer: Adam                   │
│                     │            │ Preprocessing: StandardScaler     │
│                     │            │ ★ Luôn tệ nhất trong tất cả     │
├─────────────────────┼────────────┼───────────────────────────────────┤
│ AdaptiveStack       │ Proposed   │ ★ KẾT HỢP 4 model nâng cao:     │
│ (LGBM+ET+HGB+MLP)  │            │ LightGBM + ExtraTrees +          │
│                     │            │ HistGB + MLP                      │
│                     │            │ Meta-learner: Ridge Regression    │
│                     │            │ ★ MAE THẤP NHẤT ở t+7 (0.0125)  │
│                     │            │ ★ Giảm 19.1% MAE vs XGBoost     │
└─────────────────────┴────────────┴───────────────────────────────────┘
```

---

## 2. Metrics đánh giá — Công thức đầy đủ

```
┌──────────────────────────────────────────────────────────────────────┐
│ METRIC │ CÔNG THỨC                │ ĐƠN VỊ │ Ý NGHĨA              │
├────────┼──────────────────────────┼────────┼───────────────────────┤
│ MAE    │ MAE = (1/n)Σ|yᵢ - ŷᵢ|  │ mét (m)│ Sai số TB, robust    │
│        │                          │        │ với outlier           │
│        │ MAE(t+1) = 0.0077 m     │        │ ★ metric chính       │
├────────┼──────────────────────────┼────────┼───────────────────────┤
│ RMSE   │ RMSE = √(MSE)           │ mét (m)│ Phạt lỗi LỚN nặng   │
│        │ MSE = (1/n)Σ(yᵢ-ŷᵢ)²   │        │ Luôn ≥ MAE           │
│        │ RMSE(t+1) = 0.0150 m    │        │                       │
├────────┼──────────────────────────┼────────┼───────────────────────┤
│ MAPE   │ MAPE = (100/n)          │ %      │ Sai số TƯƠNG ĐỐI    │
│        │   × Σ|yᵢ-ŷᵢ|/|yᵢ|     │        │ Không ổn khi yᵢ≈0   │
│        │ MAPE(t+1) = 3.4%        │        │ Walk-forward metric  │
├────────┼──────────────────────────┼────────┼───────────────────────┤
│ R²     │ R² = 1 - SS_res/SS_tot  │ [−∞, 1]│ Tỷ lệ phương sai    │
│        │ SS_res = Σ(yᵢ - ŷᵢ)²   │        │ được giải thích      │
│        │ SS_tot = Σ(yᵢ - ȳ)²    │        │                       │
│        │ R²(t+1) = 0.9996        │        │ Rất cao do MIKE11    │
└────────┴──────────────────────────┴────────┴───────────────────────┘

  Lưu ý quan trọng về R²:
  ┌─────────────────────────────────────────────────────────────────┐
  │ R² = 0.9996 NGHE rất ấn tượng, NHƯNG:                         │
  │                                                                 │
  │ 1. Dữ liệu MIKE11 tuân theo phương trình vật lý → mượt       │
  │    → R² cao là TÍNH CHẤT CỦA DỮ LIỆU, không phải model giỏi  │
  │                                                                 │
  │ 2. Dữ liệu đo thực tế sẽ cho R² THẤP HƠN                     │
  │    (noise, missing data, unmodeled processes)                   │
  │                                                                 │
  │ 3. Paper báo cáo R² dải: 0.9984 – 0.9996 (learned models)    │
  │                                                                 │
  │ 4. MAPE walk-forward (3.4% – 7.2%) là ước tính THỰC TẾ HƠN   │
  └─────────────────────────────────────────────────────────────────┘
```

---

## 3. Walk-forward Validation — Chi tiết kỹ thuật

```
  ┌──────────────────────────────────────────────────────────────────┐
  │         WALK-FORWARD VALIDATION SCHEME                          │
  │         (Expanding Window, retrain 4 tuần/lần)                  │
  │                                                                  │
  │  Thoi gian: ─────────────────────────────────────────────────── │
  │  1990       2015      2018     2019     2020     2021           │
  │  │          │         │        │        │        │              │
  │  ├──────────┤         │        │        │        │              │
  │  │ Window 1 │→eval    │        │        │        │              │
  │  ├──────────┤         │        │        │        │              │
  │  │          │         │        │        │        │              │
  │  ├──────────────┤     │        │        │        │              │
  │  │ Window 2     │→eval│        │        │        │              │
  │  ├──────────────┤     │        │        │        │              │
  │  ...              ...           ...                             │
  │  ├─────────────────────────────────────────┤                    │
  │  │ Window 13 (final)                       │→eval              │
  │  ├─────────────────────────────────────────┤                    │
  │                                                                  │
  │  Quy tắc:                                                        │
  │  - Window MỞ RỘNG (expanding, không sliding)                     │
  │  - Retrain mỗi 4 TUẦN (28 ngày)                                 │
  │  - Phần cuối (hàng h) bị BỎ để tránh target overlap             │
  │  - Chỉ đánh giá Stacking model                                  │
  │  - 366 evaluation days (năm 2020)                                │
  └──────────────────────────────────────────────────────────────────┘
```

**Kết quả Walk-forward vs Static Split:**

```
┌─────────┬──────────────────┬─────────────────┬──────────────────────────┐
│ Horizon │ MAPE Walk-fwd (%)│ MAE Static (m)  │ Ghi chú                  │
├─────────┼──────────────────┼─────────────────┼──────────────────────────┤
│ t+1     │ 3.4%             │ 0.0105          │ Tăng nhẹ → có thể cần   │
│         │                  │                 │ update thường xuyên hơn  │
├─────────┼──────────────────┼─────────────────┼──────────────────────────┤
│ t+3     │ 7.2%             │ 0.0157          │ ≈ khớp static split     │
├─────────┼──────────────────┼─────────────────┼──────────────────────────┤
│ t+7     │ —                │ 0.0155          │ Chưa báo cáo chi tiết    │
│         │                  │                 │ trong walk-forward        │
└─────────┴──────────────────┴─────────────────┴──────────────────────────┘

Walk-forward cho thấy hiệu suất ỔN ĐỊNH dưới điều kiện vận hành.
Đây là ước tính THỰC TẾ HƠN so với static split.
```

---

## 4. Risk-zone Evaluation — Chi tiết (Section IV-C, Table VIII)

### Định nghĩa vùng nguy hiểm

```
  Mực nước (m)
  
  1.5 ┤ ~~~~~~~~~~~~~~~~~~~~~~~~ Exceedance (WL ≥ 1.24m)
      │                           ▲ P99 = 1.24 m (99th percentile)
  1.2 ┤═══════════════════════════╪═══════════════════════════
      │ ~~~~~~~~~~~~~~~~~~~~~~~~ Warning (1.06 ≤ WL < 1.24)
  1.0 ┤                           ▲ P95 = 1.06 m (95th percentile)
      │═══════════════════════════╪═══════════════════════════
      │ ~~~~~~~~~~~~~~~~~~~~~~~~ Normal (WL < 1.06)
  0.8 ┤
      │
  0.5 ┤
      └──────────────────────────────────────────────────────── WL
        0    50   100  150  200  250  300  350  400 (ngày)
  
  Nguồn ngưỡng: P95 và P99 của chuỗi TRAIN 28 năm (1990–2017)
  → KHÔNG được tuning trên test set!
```

### Bảng kết quả chi tiết (Table VIII — Stacking model)

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Horizon │ Acc.(3z)│ Prec_D  │ Rec_D   │ F1_D   │ n_Nor │ MAE_N │ n_Wrn │ MAE_W │ n_Exc │ MAE_E        │
├─────────┼─────────┼─────────┼─────────┼────────┼───────┼───────┼───────┼───────┼───────┼──────────────┤
│ t+1     │ 0.9945  │ 1.0000  │ 0.9737  │ 0.9867 │ 684   │ 0.010 │ 29    │ 0.014 │ 9     │ 0.021        │
│ t+3     │ 0.9958  │ 0.9737  │ 0.9737  │ 0.9737 │ 684   │ 0.017 │ 29    │ 0.017 │ 9     │ 0.008        │
│ t+7     │ 0.9945  │ 0.9737  │ 0.9737  │ 0.9737 │ 684   │ 0.016 │ 29    │ 0.016 │ 9     │ 0.016        │
└─────────┴─────────┴─────────┴─────────┴────────┴───────┴───────┴───────┴───────┴───────┴──────────────┘

Phân bố mẫu trong test set (722 ngày):
┌────────────────┬───────────┬──────────┐
│ Zone           │ Số ngày   │ Tỷ lệ    │
├────────────────┼───────────┼──────────┤
│ Normal         │ 684       │ 94.7%    │ ← Chiếm GẦN NHƯ TOÀN BỘ
│ Warning        │ 29        │ 4.0%     │
│ Exceedance     │ 9         │ 1.2%     │ ← RẤT ÍT (9 ngày)
├────────────────┼───────────┼──────────┤
│ TỔNG           │ 722       │ 100%     │
└────────────────┴───────────┴──────────┘
```

### Vấn đề IMBALANCE — Wilson CI

```
╔══════════════════════════════════════════════════════════════════════╗
║  EXCEEDANCE RECALL: 6/9 (t+1), 8/9 (t+3), 7/9 (t+7)             ║
║                                                                      ║
║  Wilson 95% CI cho 6/9 = [0.354, 0.879]                            ║
║                                                                      ║
║  ┌─────────────────────────────────────────────────────────────┐    ║
║  │                    0.0   0.2   0.4   0.6   0.8   1.0        │    ║
║  │  Exceedance recall: ├─────────[=====■=====]──────────┤      │    ║
║  │                     0.354     0.667     0.879               │    ║
║  │                                                             │    ║
║  │  CI quá RỘNG → không thể phân biệt với RANDOM (0.5)!       │    ║
║  │  → KHÔNG đủ bằng chứng để claim "high accuracy"            │    ║
║  └─────────────────────────────────────────────────────────────┘    ║
║                                                                      ║
║  Nguyên nhân: chỉ 9 ngày Exceedance trong 722 ngày test            ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Đọc kết quả HAI CÁCH (Section IV-C trong thư trả lời)

```
  CÁCH ĐỌC THUẬN LỢI:                    CÁCH ĐỌC KHÔNG THUẬN LỢI:
  ┌───────────────────────────────┐      ┌───────────────────────────────┐
  │ • Exceedance recall 6/9-8/9  │      │ • Wilson CI [0.35, 0.88]     │
  │ • 37/38 ngày nguy hiểm đúng  │      │ → quá rộng, ≈ coin flip     │
  │ • Precision = 1.0 (t+1)      │      │ • 9 ngày Exceedance KHÔNG ĐỦ│
  │ → không có cảnh báo giả      │      │ • Bias ÂM ở Exceedance:     │
  │ • Không có ngày Exceedance    │      │   RF: -0.005 m              │
  │   bị phân loại thành Normal  │      │   XGBoost: -0.019 m         │
  │ → tất cả lỗi đều downgrade   │      │   Stacking: -0.026 m        │
  │   xuống Warning (direction    │      │ → under-predict = hướng      │
  │   an toàn cho cảnh báo)      │      │   KHÔNG AN TOÀN cho flood    │
  └───────────────────────────────┘      └───────────────────────────────┘
```

---

## 5. Noise Experiment — Section IV-G (Table IV trong revised paper)

### Thiết kế thí nghiệm

```
  ┌──────────────────────────────────────────────────────────────────┐
  │  NOISE EXPERIMENT: Đo khoảng cách MIKE11 → Field Observations  │
  │                                                                  │
  │  Mục đích: Khi thêm noise vào input, MAE thay đổi thế nào?    │
  │  → Cho thấy kết quả R² cao "survive" bao nhiêu % dưới noise   │
  │                                                                  │
  │  Thiết kế:                                                       │
  │  - Thêm Gaussian noise N(0, σ²) vào input water_level & sea    │
  │  - Target VẪN LÀ clean simulation (không thêm noise)           │
  │  - Features được TÍNH LẠI sau khi thêm noise                   │
  │  - σ ∈ {0, 0.01, 0.02, 0.05} mét                               │
  │  - 3 noise seeds per configuration (trung bình)                 │
  │                                                                  │
  │  2 scenarios:                                                    │
  │  S1: Train CLEAN → Test NOISY (distribution mismatch)           │
  │  S2: Train NOISY → Test NOISY (same distribution)              │
  └──────────────────────────────────────────────────────────────────┘
```

### Kết quả chi tiết (Table IV — Scenario S1)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Horizon │ σ(m)  │ Stacking  │ LR        │ XGBoost   │ Ridge             │
├─────────┼───────┼───────────┼───────────┼───────────┼───────────────────┤
│ t+1     │ 0.00  │ 0.0105    │ 0.0078    │ 0.0108    │ 0.0086            │
│ t+1     │ 0.01  │ 0.0147    │ —         │ —         │ —                 │
│ t+1     │ 0.02  │ —         │ 0.051     │ 0.039     │ —                 │
│ t+1     │ 0.05  │ —         │ —         │ —         │ —                 │
├─────────┼───────┼───────────┼───────────┼───────────┼───────────────────┤
│ t+3     │ 0.00  │ —         │ 0.0086    │ 0.0157    │ 0.0140            │
│ t+3     │ 0.01  │ —         │ 0.0693    │ —         │ —                 │
│ t+3     │ 0.05  │ —         │ 0.3291    │ 0.0818    │ —                 │
├─────────┼───────┼───────────┼───────────┼───────────┼───────────────────┤
│ t+7     │ 0.02  │ —         │ —         │ —         │ Ridge robust nhất │
└─────────┴───────┴───────────┴───────────┴───────────┴───────────────────┘

  MAE (m)
  0.35 ┤
       │                                                    LR t+3
  0.30 ┤                                                    ▲
       │                                                   ╱
  0.25 ┤                                                  ╱
       │                                                 ╱
  0.20 ┤                                                ╱
       │                                              ╱
  0.15 ┤                                            ╱
       │                                          ╱
  0.10 ┤                              XGB t+3 ───╱───
       │                        ╱──────────────
  0.05 ┤              LR t+1 ──╱───────────────
       │        ╱─────────────
  0.02 ┤  XGB t+1 ─────────────────────── (gần như phẳng)
       │──────
  0.00 ┼──────┬──────┬──────┬──────┬──────
       0.00  0.01  0.02  0.03  0.04  0.05  σ (m)
  
  ► LR t+3 COLLAPSE khi noise tăng (0.009→0.069→0.329)
  ► XGBoost DEGRADE từ từ → ROBUST hơn linear
  ► Ở t+1 với σ=0.02: XGBoost (0.039) < LR (0.051)
     → Ranking THAY ĐỔI: ensemble vượt linear
```

### Scenario S2 (train noisy → test noisy)

```
┌────────────────────────────────────────────────────────────────────┐
│ Scenario S2: Train & Test cùng noise level                        │
│                                                                    │
│ t+3, σ=0.02:                                                      │
│   LR:     0.030 m (S2) vs 0.136 m (S1)                          │
│   XGBoost: 0.028 m (S2) ≈ 0.028 m (S1)                          │
│                                                                    │
│ → S1 collapse là do DISTRIBUTION MISMATCH,                        │
│   không phải do LR bản thân yếu                                   │
│ → Khi train & test cùng noise, LR KHỎE hơn nhiều                 │
└────────────────────────────────────────────────────────────────────┘
```

### Kết luận từ Noise Experiment

```
╔══════════════════════════════════════════════════════════════════════╗
║  KẾT LUẬN:                                                         ║
║                                                                      ║
║  1. MAE centimet-level và ưu thế LR là TÍNH CHẤT CỦA DỮ LIỆU SẠCH ║
║                                                                      ║
║  2. Khi có noise ≥ 2cm:                                             ║
║     → Tree ensembles VƯỢT linear models ở t+1                      ║
║     → XGBoost VƯỢT LR ở t+3                                       ║
║     → Ridge trở nên robust nhất ở t+7                               ║
║                                                                      ║
║  3. Regularization VÀ model diversity TRỞ NÊN QUAN TRỌNG           ║
║     khi có measurement error                                         ║
║                                                                      ║
║  4. Khoảng 1–5 cm là GIẢ ĐỊNH về gauge error                      ║
║     (chưa có số liệu cụ thể từ trạm)                               ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 6. Giải thích thuật toán — Random Forest và XGBoost

### Random Forest (Bagging)

```
  Training Data D
  ┌──────────────────────────────────────────┐
  │ (x₁,y₁), (x₂,y₂), ..., (xₙ,yₙ)       │
  └──────────────┬───────────────────────────┘
                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼
  Bootstrap   Bootstrap   Bootstrap    ... (B lần, B=500)
  Sample 1    Sample 2    Sample 3
      │          │          │
      ▼          ▼          ▼
  Tree 1      Tree 2      Tree 3       (mỗi cây: random subset features)
      │          │          │
      ▼          ▼          ▼
  ŷ₁(x)      ŷ₂(x)      ŷ₃(x)
      │          │          │
      └──────────┼──────────┘
                 ▼
         ŷ = (1/B) Σ ŷᵢ(x)          TRUNG BÌNH
         
  Tham số quan trọng:
  - n_estimators = 500 (số cây)
  - max_depth = 20 (độ sâu tối đa)
  - min_samples_split = 5
```

### XGBoost (Gradient Boosting)

```
  Iteration 1: h₁ fit vào y (target gốc)
              residual₁ = y - h₁(x)
  
  Iteration 2: h₂ fit vào residual₁
              residual₂ = residual₁ - η×h₂(x)
  
  ...
  
  Iteration M: hₘ fit vào residual_{M-1}
  
  Final: ŷ(x) = h₁(x) + η×h₂(x) + ... + η×hₘ(x)
  
       ┌──────────────────────────────────────────────┐
       │ ŷ = Σ_{m=1}^{M} η × hₘ(x)                  │
       │                                              │
       │ η = learning rate (0.05 trong paper)         │
       │ M = n_estimators (500 trong paper)           │
       │ hₘ = regression tree tại iteration m         │
       └──────────────────────────────────────────────┘
  
  Gradient Boosting = fit vào GRADIENT của loss function
  → Giảm BIAS (sai số mô hình)
  → So với RF giảm VARIANCE (sai số do randomness)
```

---

## 7. AdaptiveStack — Mô hình đề xuất

```
  ┌──────────────────────────────────────────────────────────────────┐
  │               ADAPTIVESTACK ARCHITECTURE                        │
  │                                                                  │
  │   Train Set          Val Set            Test Set                │
  │   ┌────────┐        ┌────────┐         ┌────────┐              │
  │   │X_train │        │ X_val  │         │ X_test │              │
  │   └───┬────┘        └───┬────┘         └───┬────┘              │
  │       │                 │                   │                    │
  │       ▼                 ▼                   ▼                    │
  │   ┌───────────────────────────────────────────────────┐         │
  │   │           4 BASE LEARNERS                         │         │
  │   │                                                   │         │
  │   │  ┌──────────┐ ┌──────────┐ ┌────────┐ ┌───────┐ │         │
  │   │  │ LightGBM │ │ExtraTrees│ │HistGB  │ │  MLP  │ │         │
  │   │  └────┬─────┘ └────┬─────┘ └───┬────┘ └───┬───┘ │         │
  │   │       │             │            │          │     │         │
  │   └───────┼─────────────┼────────────┼──────────┼─────┘         │
  │           │             │            │          │                │
  │           ▼             ▼            ▼          ▼                │
  │       p₁(x)val      p₂(x)val    p₃(x)val   p₄(x)val         │
  │           │             │            │          │                │
  │           └─────────────┼────────────┼──────────┘                │
  │                         ▼                                        │
  │              ┌─────────────────────┐                            │
  │              │ META-FEATURES       │                            │
  │              │ [p₁, p₂, p₃, p₄]  │ ← 4 predictions            │
  │              └──────────┬──────────┘                            │
  │                         │                                        │
  │                         ▼                                        │
  │              ┌─────────────────────┐                            │
  │              │ RIDGE META-LEARNER  │                            │
  │              │ ŷ = Σ wᵢpᵢ + b    │                            │
  │              └──────────┬──────────┘                            │
  │                         │                                        │
  │                         ▼                                        │
  │              ŷ_adaptive(x_test)                                 │
  │                                                                  │
  │  Kết quả t+7: MAE = 0.0125 m                                   │
  │  Cải thiện: 19.1% so với XGBoost (0.0155 m)                   │
  └──────────────────────────────────────────────────────────────────┘
```
