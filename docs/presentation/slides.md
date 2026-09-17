---
marp: true
theme: default
paginate: true
title: Multi-step Water Level Forecasting - Quang Ha
---

# Feature-Engineering-Driven ML as Surrogate of Hydrodynamic Simulation for Multi-Step Water Level Forecasting

**Quảng Hà Estuary, Quảng Ninh, Vietnam**

Hieu Ta*, Thao Nguyen Thi
Faculty of Information Technology, Thuyloi University
VNICT 2026 — Paper ID 6546

<!-- Speaker notes: Xin chào, tôi sẽ trình bày nghiên cứu về dự báo mực nước đa bước tại vùng cửa sông Quảng Hà. Đây là nghiên cứu sử dụng học máy với đặc trưng được thiết kế từ kiến thức thủy văn. Quan trọng: tất cả dữ liệu là output mô phỏng MIKE11, mô hình ML là surrogate. -->

---

## Background & Problem

- Estuarine water levels = **river discharge** + **tidal dynamics**
- Quang Ha, Quang Ninh: coastal estuary, 2 river branches (Hà Côi + Tài Chi)
- Need: **multi-step forecasting** (t+1, t+3, t+7 days) for early warning
- Challenge: nonlinear compound river–sea interaction

```
  Thượng nguồn                    Hạ nguồn
  Hà Côi + Tài Chi ──► QUANG HÀ ◄── Biển Đông (triều)
                     │  mực nước  │
                     │  WL(t)     │
                     └────────────┘
```

<!-- Speaker notes: Vùng cửa sông Quảng Hà nhận nước từ 2 nhánh sông và bị ảnh hưởng bởi triều. Khi cả hai cùng cao → nguy cơ ngập lụt. Chúng ta cần dự báo trước 1, 3, 7 ngày. Bài toán phức tạp vì mối quan hệ phi tuyến tính giữa sông và biển trong compound events. -->

---

## Data: Surrogate of MIKE11 Simulation

```
╔════════════════════════════════════════════════════════════╗
║  KHÔNG PHẢI field observations!                            ║
║  TẤT CẢ data = output của MIKE11 simulator                ║
║  → ML model = "surrogate" (phần thay thế nhanh)           ║
║  → KHÔNG phải hệ thống dự báo thực địa đã validated      ║
╚════════════════════════════════════════════════════════════╝
```

| Biến | Đơn vị | Vai trò |
|------|--------|---------|
| river_flow_A | m³/s | Lưu lượng Hà Côi (biên trên 1) |
| river_flow_B | m³/s | Lưu lượng Tài Chi (biên trên 2) |
| sea_level | m | Mực nước biển/triều (biên dưới) |
| **water_level** | **m** | **Mục tiêu dự báo (Kết quả)** |

- 32 năm (1990–2021), daily resolution, 11,688 ngày
- Temporal split: Train 1990–2017 / Val 2018–2019 / Test 2020–2021

<!-- Speaker notes: Dữ liệu là output MIKE11, không phải đo thực. R² > 0.998 phản ánh tính mượt của simulation, không phải model quá giỏi. Khi thêm noise 1cm, MAE tăng 40%. Dữ liệu 32 năm, chia temporal: train 28 năm, val 2 năm, test 2 năm. -->

---

## Pipeline Overview

```
  Raw MIKE11 data (4 biến, 1990-2021)
       │
       ▼
  Feature Engineering (41 features → 26-27 per horizon)
  ┌─────────────────────────────────────────────┐
  │ Lag (13) + Rolling (10) + Seasonal (8)       │
  │ + Interaction (4) + Risk (6)                 │
  └─────────────────────────────────────────────┘
       │
       ▼
  Temporal Train/Val/Test Split
       │
       ▼
  Train Models + Evaluate
  ┌─────────────────────────────────────────────┐
  │ LR, Ridge, RF, XGBoost, Stacking            │
  │ ExtraTrees, LightGBM, HistGB, MLP           │
  │ AdaptiveStack (proposed)                     │
  └─────────────────────────────────────────────┘
       │
       ▼
  Walk-forward + Risk-zone + Feature Importance
```

<!-- Speaker notes: Pipeline 4 bước: tiền xử lý, feature engineering 5 nhóm, huấn luyện 10+ models, đánh giá toàn diện. Điểm khác biệt chính: feature engineering là đóng góp chính, không phải model phức tạp. -->

---

## Feature Engineering — 5 Groups (41 features)

| Group | # | Ví dụ | Ý nghĩa thủy học |
|-------|---|-------|-------------------|
| **Lag** | 13 | water_level_lag_14, lag_7 | Chu kỳ triều ~14.76 ngày |
| **Rolling** | 10 | rolling_mean_7, std_7 | Xu hướng và biến động ngắn hạn |
| **Seasonal** | 8 | month_sin, tidal_cycle_sin | Chu kỳ mùa và triều |
| **Interaction** | 4 | sea_river_diff, flood_pressure | Tương tác sông–biển |
| **Risk** | 6 | distance_to_threshold, acceleration | Cảnh báo, gia tốc thay đổi |

**Feature selection:** 41 → 26–27 per horizon (Spearman ρ filtering)

> **Finding:** Feature engineering **linearizes** the short-horizon problem!

<!-- Speaker notes: 5 nhóm feature, mỗi nhóm có ý nghĩa thủy văn. Lag_14 bắt chu kỳ triều half-month. is_rising bắt trạng thái tăng/giảm. acceleration bắt gia tốc thay đổi. Feature selection bằng Spearman correlation: loại bỏ feature đa cộng tuyến (|ρ|>0.95) và yếu (|ρ_target|<0.05). -->

---

## Result 1: Linear Regression Wins at t+1, t+3

| Horizon | **Linear Regr.** | XGBoost | Stacking | Insight |
|---------|-----------------|---------|----------|---------|
| **t+1** | **0.0077 m** | 0.0108 | 0.0105 | ★ LR #1 |
| **t+3** | **0.0086 m** | 0.0157 | 0.0169 | ★ LR #1 |
| t+7 | 0.0216 | **0.0155** | 0.0161 | XGB #1 |

```
  MAE t+1 (m):  LR ████████░░░░░░░░░░ 0.0077
                 XGB ████████████░░░░░░ 0.0108
                 Stk ███████████░░░░░░░ 0.0105
```

**Takeaway:** Invest in feature engineering, not model complexity!

**Why?** lag_14 autocorrelation = 0.91 → relationship nearly linear at t+1.

<!-- Speaker notes: Kết quả quan trọng nhất: Linear Regression — model đơn giản nhất — đạt MAE thấp nhất ở t+1 và t+3. Vì feature engineering tạo ra feature mạnh (lag_14 tương quan 0.91) nên mối quan hệ gần tuyến tính. Ensemble thêm variance mà không giảm bias đủ. Bài học: đầu tư feature engineering tốt hơn tìm model phức tạp. -->

---

## Result 2: AdaptiveStack at t+7 (−19.1% MAE)

Ensemble diversity matters **only at the longest horizon**:

| Metric | XGBoost | **AdaptiveStack** | Δ |
|--------|---------|------------------|---|
| MAE | 0.0155 m | **0.0125 m** | **−19.1%** |
| RMSE | 0.0248 m | 0.0219 m | −11.7% |
| R² | 0.9989 | 0.9992 | +0.0003 |

```
  AdaptiveStack = LightGBM + ExtraTrees + HistGB + MLP
                       ↓
               Ridge Meta-Learner
                       ↓
                ŷ_adaptive(x)
```

At t+7: nonlinear dynamics ↑ → model diversity helps.

<!-- Speaker notes: Ở t+7, AdaptiveStack giảm 19.1% MAE so với XGBoost. Kết hợp 4 model khác nhau: LightGBM (histogram), ExtraTrees (randomized), HistGB (early stopping), MLP (neural). Ridge meta-learner học cách blend tối ưu. Tại sao ensemble chỉ có lợi ở t+7? Vì ở t+1, t+3 mối quan hệ gần tuyến tính → ensemble thêm noise. Ở t+7 nonlinear dynamics mạnh → ensemble đa dạng giúp ích. -->

---

## Result 3: R² > 0.998 — Context Required

```
  R² = 1 - SS_res / SS_tot

  Dữ liệu MIKE11:                    Dữ liệu đo thực:
  ┌─────────────────────┐             ┌─────────────────────┐
  │ Tuân theo PT vật lý │             │ Có nhiễu đo lường   │
  │ Mượt, ít noise      │             │ Missing data          │
  │ R² > 0.998          │             │ R² dự kiến THẤP HƠN │
  └─────────────────────┘             └─────────────────────┘
```

| Noise σ | MAE Stacking t+1 | Thay đổi |
|---------|------------------|----------|
| 0 cm | 0.0105 m | baseline |
| 1 cm | 0.0147 m | +40% |
| 2 cm | 0.0212 m | +102% |

**Conclusion:** High R² = property of smooth simulation data, NOT model quality.

<!-- Speaker notes: R² rất cao cần bối cảnh. Dữ liệu MIKE11 tuân theo phương trình Saint-Venant → mượt hơn dữ liệu đo thực. Noise experiment cho thấy: chỉ thêm 1cm noise vào input → MAE tăng 40%. 2cm noise → MAE tăng gấp đôi. Và ranking thay đổi: XGBoost vượt Linear Regression từ 2cm noise. Walk-forward MAPE 3.4%–7.2% phản ánh thực tế hơn. -->

---

## Walk-forward Validation

```
  Expanding window, retrain mỗi 4 tuần:
  [1990──────────2019.12] → eval 2020.01-02
  [1990──────────2020.02] → eval 2020.03-04
  ...
  [1990──────────2020.12] → eval 2021.01-02
```

| Horizon | MAPE (walk-fwd) | MAE (static) | Note |
|---------|-----------------|-------------|------|
| t+1 | 3.4% | 0.0105 m | ↑ slightly |
| t+3 | 7.2% | 0.0157 m | ≈ static |
| t+7 | — | 0.0155 m | Not reported |

Walk-forward MAPE is the **more realistic** performance estimate.

<!-- Speaker notes: Walk-forward validation mô phỏng điều kiện vận hành thực tế. Expanding window, retrain mỗi 4 tuần. MAPE 3.4%–7.2%. Lưu ý: t+1 error tăng nhẹ dưới walk-forward → có thể cần update thường xuyên hơn cho short horizon. -->

---

## Risk-zone Evaluation — Caution Required

Thresholds: **P95 = 1.06 m** (Warning), **P99 = 1.24 m** (Exceedance)

| Horizon | Accuracy | Prec_D | Recall_D | F1_D |
|---------|----------|--------|----------|------|
| t+1 | 99.45% | 1.000 | 0.974 | 0.987 |
| t+3 | 99.58% | 0.974 | 0.974 | 0.974 |
| t+7 | 99.45% | 0.974 | 0.974 | 0.974 |

**Test set:** 684 Normal / 29 Warning / **9 Exceedance**

```
  Exceedance recall 6/9 → Wilson 95% CI = [0.35, 0.88]
  CI quá RỘNG → KHÔNG thể phân biệt với coin flip (0.5)!
```

- ✅ Không có ngày Exceedance nào bị phân loại thành Normal
- ⚠️ Bias âm (under-predict) → hướng KHÔNG an toàn cho flood warning

<!-- Speaker notes: Risk-zone evaluation phân loại Normal/Warning/Exceedance. Accuracy 99.5% nhưng cần thận trọng: 9 ngày Exceedance → Wilson CI [0.35, 0.88] quá rộng. Điểm tích cực: không ngày Exceedance nào bị phân loại thành Normal (tất cả downgrade xuống Warning). Nhưng bias âm (under-predict) ở Exceedance → hướng không an toàn. Paper đề xuất cost-weighted loss hoặc bias correction. -->

---

## Feature Importance by Horizon

| Horizon | #1 Feature | Importance | Cơ chế |
|---------|-----------|-----------|--------|
| t+1 | water_level_lag_14 | 0.496 | Chu kỳ triều ~14.76 ngày |
| t+3 | is_rising | 0.921 | Trạng thái tăng/giảm |
| t+7 | acceleration | 0.421 | Gia tốc thay đổi |

```
  Autocorrelation structure (giải thích cơ chế):
  Lag 1:  +0.91 (persistence cao)
  Lag 3:  +0.33 (đang giảm)
  Lag 7:  -0.86 (nửa chu kỳ triều!)
  Lag 14: +0.91 (1 chu kỳ đầy đủ!)
```

**Note:** Tree-based importance ≠ causal evidence. Interpretation only.

<!-- Speaker notes: Feature importance thay đổi theo horizon phản ánh cơ chế thủy học khác nhau. Ở t+1, lag_14 (chu kỳ triều half-month, autocorrelation +0.91) chi phối. Ở t+3, is_rising chiếm 92% importance → biết mực nước đang tăng/giảm quan trọng hơn biết giá trị cụ thể. Ở t+7, acceleration (gia tốc) + lag_7 (chu kỳ tuần) chi phối. Đây là phân tích giải thích, không phải nhân quả. -->

---

## Limitations & Validation Roadmap

1. **All data are MIKE11 simulation** — surrogate, not field-validated
2. **No rainfall/meteorological** variables
3. **Single station** — generalizability unverified
4. **R² inflated** by simulation smoothness
5. **Only 9 Exceedance days** — not enough for strong claims

```
  Validation Roadmap (3 bước):
  ┌───────────────────────────────────────────────┐
  │ 1. Lấy data đo thực từ MIKE11 calibration    │
  │ 2. Tách lỗi mô phỏng vs lỗi mô hình          │
  │ 3. Mở rộng nhiều trạm + storm-tide events    │
  └───────────────────────────────────────────────┘
```

<!-- Speaker notes: Giới hạn lớn nhất: dữ liệu mô phỏng. Noise experiment phần nào đo lường khoảng cách MIKE11→field. Roadmap 3 bước để validate trong tương lai. Hiện tại: accuracy figures mô tả "how well the model reproduces the simulator", KHÔNG phải "how well it forecasts real water levels". -->

---

## Key Takeaways for Students

```
  ┌────────────────────────────────────────────────────────────┐
  │ 1. Feature Engineering > Model Complexity (short horizon)  │
  │ 2. Temporal Split — NEVER random split for time series     │
  │ 3. Surrogate Framing — honest about model's scope          │
  │ 4. R² > 0.998 = property of data, NOT model quality       │
  │ 5. Class imbalance — always report Wilson CI + counts      │
  │ 6. Read the reviewer response — learn scientific writing!  │
  └────────────────────────────────────────────────────────────┘
```

> "The revision improved the paper more than we expected — not by changing results, but by stating their scope more precisely."

**References:** Mosavi 2018, Breiman 2001, Chen & Guestrin 2016, Lundberg & Lee 2017, Le et al. 2021

<!-- Speaker notes: Bài học chính cho sinh viên: Feature engineering quan trọng hơn model phức tạp. Phải chia temporal, không random split. Phải trung thực về scope. R² cao cần bối cảnh. Imbalance phải được nêu rõ. Và đọc thư trả lời reviewer — học cách phản biện và cải thiện paper. Cảm ơn các bạn! -->
