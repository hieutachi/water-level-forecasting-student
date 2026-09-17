---
marp: true
theme: default
paginate: true
title: Multi-step Water Level Forecasting - Quang Ha
---

# Multi-step Water Level Forecasting
## Using Feature-Engineering-Driven ML as Surrogate of Hydrodynamic Simulation

**Quảng Hà Estuary, Quảng Ninh, Vietnam**

Hieu Ta, Thao Nguyen Thi
Faculty of Information Technology, Thuyloi University
VNICT 2026

<!-- Speaker notes: Xin chào, tôi sẽ trình bày nghiên cứu về dự báo mực nước đa bước tại vùng cửa sông Quảng Hà, sử dụng học máy với đặc trưng được thiết kế từ kiến thức thủy văn. -->

---

## Background & Problem

- Estuarine water levels = **river discharge** + **tidal dynamics**
- Quang Ha, Quang Ninh: coastal estuary with compound flood risk
- Need: **multi-step forecasting** (t+1, t+3, t+7 days) for early warning
- Challenge: nonlinear river–sea interaction, long-term dependencies

<!-- Speaker notes: Vùng cửa sông bị ảnh hưởng bởi cả dòng chảy thượng nguồn và triều. Khi cả hai cùng cao, nguy cơ ngập lụt tăng. Chúng ta cần dự báo trước 1, 3, 7 ngày để cảnh báo sớm. Bài toán phức tạp vì mối quan hệ phi tuyến tính giữa sông và biển. -->

---

## Data: Surrogate of MIKE11 Simulation

- **NOT field observations** — all series from MIKE11 hydrodynamic simulator
- 32 years (1990–2021), daily resolution
- Variables: river flow A, river flow B, sea level, water level at Ha Coi
- **Implication:** R² > 0.998 reflects simulation smoothness, not field accuracy

> The ML model is a **fast surrogate** of the hydrodynamic simulator, not a validated field forecasting tool.

<!-- Speaker notes: Dữ liệu trong nghiên cứu là output của mô hình thủy động lực MIKE11, không phải đo trực tiếp tại trạm. Điều này rất quan trọng: R² rất cao vì dữ liệu mô phỏng trơn, mượt hơn dữ liệu đo thực. Mô hình ML đóng vai trò "surrogate" - phần thay thế nhanh cho trình mô phỏng. -->

---

## Pipeline Overview

```
Raw MIKE11 data (1990–2021)
    → Feature Engineering (41 → 26–27 features)
    → Temporal Split (Train/Val/Test)
    → Train models (LR, RF, XGBoost, Stacking, AdaptiveStack)
    → Evaluate (MAE, RMSE, R², walk-forward, risk-zone)
    → Interpret (feature importance, SHAP)
```

![Pipeline](pipeline_diagram.png)

<!-- Speaker notes: Pipeline gồm 4 bước: tiền xử lý, tạo đặc trưng, huấn luyện mô hình và đánh giá. Điểm khác biệt chính là feature engineering - tạo 5 nhóm đặc trưng có ý nghĩa thủy văn. -->

---

## Feature Engineering (5 Groups)

| Group | # | Examples | Hydrological Meaning |
|-------|---|----------|---------------------|
| **Lag** | 13 | water_level_lag_1, lag_7, lag_14 | Persistence, tidal memory |
| **Rolling** | 10 | rolling_mean_7, std_7 | Short-term trend |
| **Seasonal** | 8 | month_sin, tidal_cycle_sin | Tidal & seasonal cycles |
| **Interaction** | 4 | sea_river_diff, flood_pressure | River–sea coupling |
| **Risk** | 6 | distance_to_threshold, acceleration | Warning proximity |

> **Key finding:** Feature engineering linearizes the short-horizon problem!

<!-- Speaker notes: 5 nhóm feature, mỗi nhóm có ý nghĩa thủy văn rõ ràng. Lag features ghi nhớ chu kỳ triều (~14.76 ngày). Rolling features bắt xu hướng ngắn hạn. Seasonal features mã hóa mùa và chu kỳ. Interaction features mô tả tương tác sông-biển. Risk features đo khoảng cách đến ngưỡng cảnh báo. Điểm quan trọng nhất: feature engineering làm cho bài toán ngắn hạn gần như tuyến tính. -->

---

## Main Result: Linear Wins at Short Horizon

| Horizon | Linear Regression | XGBoost | Stacking |
|---------|------------------|---------|----------|
| **t+1** | **0.0077 m** | 0.0108 m | 0.0105 m |
| **t+3** | **0.0086 m** | 0.0157 m | 0.0169 m |
| t+7 | 0.0216 m | 0.0155 m | 0.0161 m |

**Takeaway:** Invest in feature engineering, not model complexity, for short lead times.

<!-- Speaker notes: Kết quả quan trọng nhất: Linear Regression đạt MAE thấp nhất ở t+1 và t+3, thấp hơn cả XGBoost và Stacking. Điều này cho thấy feature engineering đã "linearize" được bài toán. Ở short horizon, đầu tư vào thiết kế đặc trưng hiệu quả hơn tìm model phức tạp. -->

---

## AdaptiveStack at t+7

Ensemble diversity matters **only at the longest horizon**:

| Mô hình | MAE t+7 | Cải thiện |
|---------|---------|-----------|
| XGBoost | 0.0155 m | baseline |
| **AdaptiveStack** | **0.0125 m** | **-19.1%** |
| RMSE | 0.0248→0.0219 m | -11.7% |
| R² | 0.9989→0.9992 | +0.0003 |

AdaptiveStack = LightGBM + ExtraTrees + HistGB + MLP → Ridge meta-learner

<!-- Speaker notes: Ở t+7, mô hình ensemble đa dạng giúp ích. AdaptiveStack kết hợp 4 mô hình khác nhau qua Ridge meta-learner, giảm 19% MAE so với XGBoost. Điều này phù hợp: ở horizon dài, mối quan hệ phi tuyến tính mạnh hơn, cần nhiều mô hình khác nhau để bắt được. -->

---

## Walk-forward Validation & MAPE

- Expanding window, retrain every 4 weeks
- Drop trailing `h` rows to avoid target leakage

| Horizon | MAPE | MAE (static) |
|---------|------|-------------|
| t+1 | 3.4% | 0.0105 m |
| t+3 | 7.2% | 0.0157 m |
| t+7 | — | 0.0155 m |

**Walk-forward MAPE** is a more realistic performance estimate than static split.

<!-- Speaker notes: Walk-forward validation mô phỏng điều kiện vận hành thực tế: mô hình được retrain mỗi 4 tuần, cửa sổ huấn luyện mở rộng. MAPE từ 3.4% đến 7.2%. Đây là ước tính thực tế hơn so với đánh giá tĩnh. -->

---

## Risk-zone Evaluation

Thresholds: **P95 = 1.06 m** (Warning), **P99 = 1.24 m** (Exceedance)

| Horizon | Accuracy | Prec (dangerous) | Recall (dangerous) | F1 |
|---------|----------|-----------------|-------------------|-----|
| t+1 | 99.45% | 1.000 | 0.974 | 0.987 |
| t+3 | 99.58% | 0.974 | 0.974 | 0.974 |
| t+7 | 99.45% | 0.974 | 0.974 | 0.974 |

**Caution:** 684 Normal / 29 Warning / **9 Exceedance** days in test set

- Exceedance recall 6/9 → Wilson 95% CI [0.35, 0.88] → **too wide**
- All Exceedance errors are **downgrades to Warning**, never to Normal

<!-- Speaker notes: Risk-zone evaluation phân loại mực nước thành 3 vùng. Accuracy rất cao nhưng cần thận trọng: chỉ có 9 ngày Exceedance trong test set. Wilson CI [0.35, 0.88] quá rộng, không thể phân biệt với mô hình ngẫu nhiên. Điểm tích cực: không có ngày Exceedance nào bị phân loại nhầm thành Normal, và tất cả lỗi đều là downgrade xuống Warning. -->

---

## Feature Importance by Horizon

| Horizon | Top Feature | Importance | Meaning |
|---------|-------------|-----------|---------|
| t+1 | water_level_lag_14 | 0.496 | Semi-monthly tidal cycle |
| t+3 | is_rising | 0.921 | Rising/falling tidal state |
| t+7 | acceleration | 0.421 | Rate of change trend |

- At t+1: **tidal memory** (lag 14 ≈ spring-neap cycle)
- At t+3: **rising/falling state** more informative than a single past level
- At t+7: **acceleration + weekly cycle** (lag 7)

<!-- Speaker notes: Feature importance cho thấy cơ chế khác nhau theo horizon. Ở t+1, lag 14 ngày (chu kỳ triều nửa tháng) quan trọng nhất. Ở t+3, trạng thái đang tăng/giảm quan trọng hơn. Ở t+7, gia tốc thay đổi và chu kỳ tuần (lag 7) là chính. Đây là phân tích giải thích, không phải nhân quả. -->

---

## Limitations & Validation Roadmap

1. **All data are MIKE11 simulation** — surrogate, not field-validated
2. **No rainfall/meteorological variables** included
3. **Single station** — generalizability unverified
4. **R² inflated** by simulation smoothness
5. **Only 9 Exceedance days** — not enough for strong claims

**Validation roadmap:**
1. Obtain observed water levels from MIKE11 calibration record
2. Quantify MIKE11-vs-observation error
3. Extend to multiple stations and storm-tide events

<!-- Speaker notes: Giới hạn lớn nhất là dữ liệu mô phỏng, không phải đo thực. Chúng tôi đề xuất roadmap 3 bước để validate trong tương lai. Noise experiment phần nào đo lường khoảng cách giữa mô phỏng và thực tế: khi thêm noise 1cm, MAE tăng 40%. -->

---

## Key Takeaways for Students

1. **Feature engineering > model complexity** for short horizons
2. **Temporal split** is essential for time series — no random split!
3. **Surrogate framing** is honest about what the model can do
4. **R² > 0.998 needs context** — simulation data is smooth
5. **Class imbalance** matters in risk-zone evaluation
6. **Read the reviewer response** — learn scientific writing!

> "The revision improved the paper more than we expected — not by changing results, but by stating their scope more precisely."

<!-- Speaker notes: Bài học cho sinh viên: Feature engineering quan trọng hơn model phức tạp. Phải chia dữ liệu theo thời gian. Phải trung thực về giới hạn. R² cao cần bối cảnh. Mất cân bằng lớp rất quan trọng. Và hãy đọc thư trả lời reviewer - rất hữu ích cho việc viết báo khoa học. Cảm ơn các bạn! -->
