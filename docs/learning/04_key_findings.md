# 04 — Kết quả chính

## Kết quả 1: Feature Engineering > Model Complexity

**Tại t+1 và t+3, Linear Regression đạt MAE thấp nhất:**

| Horizon | Linear Regression | XGBoost | Stacking |
|---------|------------------|---------|----------|
| t+1 | **0.0077 m** | 0.0108 m | 0.0105 m |
| t+3 | **0.0086 m** | 0.0157 m | 0.0169 m |

**Ý nghĩa:** Đặc trưng được thiết kế tốt làm cho bài toán ở short horizon gần như tuyến tính. Đầu tư vào feature engineering tốt hơn là tìm model phức tạp.

## Kết quả 2: Ensemble chỉ có lợi ở t+7

**Tại t+7, AdaptiveStack giảm ~19% MAE so với XGBoost:**

| Mô hình | MAE t+7 | RMSE t+7 | R² |
|---------|---------|----------|-----|
| XGBoost | 0.0155 m | 0.0248 m | 0.9989 |
| **AdaptiveStack** | **0.0125 m** | **0.0219 m** | **0.9992** |
| Cải thiện | -19.1% | -11.7% | +0.0003 |

**Ý nghĩa:** Khi horizon dài hơn, mối quan hệ phi tuyến tính tăng → ensemble đa dạng (LightGBM + ExtraTrees + HistGB + MLP) giúp ích.

## Kết quả 3: R² rất cao do dữ liệu mô phỏng

**R² > 0.998 cho tất cả mô hình học.** Lý do:
- Dữ liệu MIKE11 tuân theo phương trình vật lý xác định
- Mượt hơn dữ liệu đo thực (không nhiễu, không missing)
- MAPE walk-forward (3.4%–7.2%) là ước tính thực tế hơn

## Kết quả 4: Noise experiment thay đổi ranking

Khi thêm Gaussian noise vào input (σ = 0.01, 0.02, 0.05 m):

| σ (m) | LR MAE t+1 | XGBoost MAE t+1 | Mô hình tốt nhất |
|-------|------------|-----------------|-------------------|
| 0.00 | 0.0078 | 0.0108 | Linear Regression |
| 0.01 | 0.0147 | 0.0130 | Gần nhau |
| 0.02 | 0.051 | 0.039 | **XGBoost** |

**Ý nghĩa:** Khi có nhiễu đo lường, mô hình ensemble trở nên robust hơn linear.

## Kết quả 5: Risk-zone accuracy cao nhưng cần thận trọng

**Phân bố test set:** 684 Normal / 29 Warning / 9 Exceedance

| Metric | Giá trị | Lưu ý |
|--------|---------|-------|
| Accuracy 3-zone | 99.45–99.58% | Rất cao nhưng dominated bởi Normal |
| Precision dangerous | 0.974–1.000 | Ít cảnh báo giả |
| Exceedance recall | 6/9 – 8/9 | Wilson CI [0.35, 0.88] → quá rộng |
| Bias Exceedance | -0.005 đến -0.026 m | Under-predict → hướng KHÔNG an toàn |

**Cảnh báo:** 9 ngày Exceedance không đủ để đưa ra kết luận mạnh.

## Kết quả 6: Feature importance theo horizon

| Horizon | Feature quan trọng nhất | Ý nghĩa |
|---------|------------------------|----------|
| t+1 | `water_level_lag_14` | Chu kỳ triều nửa tháng |
| t+3 | `is_rising` | Trạng thái đang tăng/giảm |
| t+7 | `acceleration` | Gia tốc thay đổi mực nước |

## Liên hệ với paper

- **Table I** (paper VNICT2026): So sánh hiệu suất tất cả mô hình
- **Table II**: Risk-zone evaluation với Wilson CI
- **Figure SHAP**: Feature importance theo horizon
- **Table IV** (revised): Noise experiment
- **Section IV-D**: Feature ablation study
