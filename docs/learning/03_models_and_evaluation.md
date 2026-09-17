# 03 — Mô hình và đánh giá

## Các mô hình được đánh giá

### Baselines (đường cơ sở)

| Mô hình | Mô tả | Mục đích |
|---------|-------|----------|
| Naive-lag1 | Dự báo = giá trị hôm qua | Baseline đơn giản nhất |
| Naive-lag7 | Dự báo = giá trị 7 ngày trước | Baseline chu kỳ tuần |
| Naive-lag14 | Dự báo = giá trị 14 ngày trước | Baseline chu kỳ triều |
| Linear Regression | Hồi quy tuyến tính đơn giản | Kiểm tra tính tuyến tính |
| Ridge | Linear Regression + regularization | So sánh với LR |

### Mô hình chính (Existing ML)

| Mô hình | Gia đình | Đặc điểm |
|---------|----------|-----------|
| **Random Forest (RF)** | Bagging | Trung bình nhiều cây quyết định, giảm variance |
| **XGBoost** | Gradient boosting | Học tuần tự, sửa lỗi các cây trước |
| **Stacking** | Meta-learning | Kết hợp RF + XGBoost qua Ridge meta-learner |

### Mô hình nâng cao (Advanced)

| Mô hình | Đặc điểm |
|---------|-----------|
| **ExtraTrees** | Random Forest + thêm ngẫu nhiên trong split |
| **LightGBM** | Gradient boosting tối ưu tốc độ (histogram-based) |
| **HistGradientBoosting** | scikit-learn's histogram-based boosting |
| **MLP** | Neural network 2 lớp ẩn (128-64 neurons) |
| **AdaptiveStack** | Kết hợp 4 mô hình nâng cao qua Ridge meta-learner |

## Metrics đánh giá

### MAE (Mean Absolute Error)
```
MAE = mean(|y_true - y_pred|)
```
- Đơn vị: mét (m)
- Ý nghĩa: sai số trung bình, dễ hiểu
- Ưu điểm: robust với outlier

### RMSE (Root Mean Squared Error)
```
RMSE = sqrt(mean((y_true - y_pred)²))
```
- Đơn vị: mét (m)
- Ý nghĩa: phạt nặng các lỗi lớn
- Luôn >= MAE

### MAPE (Mean Absolute Percentage Error)
```
MAPE = mean(|y_true - y_pred| / |y_true|) × 100%
```
- Đơn vị: phần trăm (%)
- Ý nghĩa: sai số tương đối
- Lưu ý: không ổn định khi y_true gần 0

### R² (Coefficient of Determination)
```
R² = 1 - SS_res / SS_tot
```
- Phạm vi: (-∞, 1], giá trị 1 là hoàn hảo
- Ý nghĩa: tỷ lệ phương sai được giải thích
- **Cảnh báo:** R² > 0.998 trong paper là do dữ liệu mô phỏng trơn, không phải do mô hình quá giỏi

## Walk-forward Validation

### Tại sao cần walk-forward?

Temporal split tĩnh chỉ đánh giá trên 1 khoảng thời gian cố định. Walk-forward mô phỏng điều kiện **vận hành thực tế**:

```
Cửa sổ 1: Train [1990–2019.12] → Test [2020.01 – 2020.02]
Cửa sổ 2: Train [1990–2020.02] → Test [2020.03 – 2020.04]
...
```

- Mô hình được retrain mỗi 4 tuần
- Cửa sổ huấn luyện mở rộng qua thời gian (expanding window)
- Phần cuối mỗi cửa sổ (hàng `h`) bị bỏ để tránh data leakage

### Kết quả walk-forward

| Horizon | MAPE (walk-forward) | MAE (static split) |
|---------|---------------------|---------------------|
| t+1 | 3.4% | 0.0105 m |
| t+3 | 7.2% | 0.0157 m |
| t+7 | — | 0.0155 m |

## Risk-zone Evaluation

### Định nghĩa vùng nguy hiểm

Dựa trên phân vị của tập train 28 năm:
- **Normal:** WL < 1.06 m (dưới P95)
- **Warning:** 1.06 m ≤ WL < 1.24 m (P95–P99)
- **Exceedance:** WL ≥ 1.24 m (trên P99)

### Vấn đề mất cân bằng (Imbalance)

Test set phân bố:
- **Normal:** 684 ngày (94.7%)
- **Warning:** 29 ngày (4.0%)
- **Exceedance:** 9 ngày (1.2%)

**Đây là vấn đề lớn:** Accuracy 99.5% có vẻ ấn tượng, nhưng:
- Chỉ có 9 ngày Exceedance → Wilson 95% CI = [0.35, 0.88] → KHÔNG thể phân biệt với ngẫu nhiên
- Precision "dangerous" = 1.0 tại t+1 → không có cảnh báo giả, NHƯNG...
- Hệ thống có xu hướng **under-predict** mức nước cao (bias âm) → hướng KHÔNG AN TOÀN cho cảnh báo lũ

### Đọc kết quả hai cách

**Cách đọc thuận lợi:**
- Exceedance recall 6/9 (t+1), 8/9 (t+3), 7/9 (t+7)
- Không có ngày Exceedance nào bị phân loại nhầm thành Normal
- Precision cao → ít cảnh báo giả

**Cách đọc không thuận lợi:**
- Wilson CI [0.35, 0.88] → quá rộng
- Bias âm ở ngày nguy hiểm (under-predict) → hướng không an toàn
- Cần dữ liệu thực và nhiều extreme events hơn để kết luận mạnh
