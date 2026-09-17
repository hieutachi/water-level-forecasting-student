# 02 — Feature Engineering

## Tổng quan

Feature engineering là **đóng góp chính** của nghiên cứu này. Từ 4 biến gốc, paper tạo ra **41 đặc trưng** được nhóm thành 5 nhóm có ý nghĩa thủy văn.

**Kết quả quan trọng:** Feature engineering làm cho bài toán ở short horizon (t+1, t+3) trở nên **gần như tuyến tính** — Linear Regression đạt MAE tốt nhất ở các horizon này!

## 5 nhóm Feature

### Nhóm 1: Lag Features (13 đặc trưng)

**Ví dụ:** `water_level_lag_1`, `water_level_lag_7`, `water_level_lag_14`, `river_flow_A_lag_1`, `sea_level_lag_3`

**Ý nghĩa thủy văn:**
- `water_level_lag_1`: tính trì (persistence) của mực nước
- `water_level_lag_14`: chu kỳ triều nửa tháng (~14.76 ngày, gần với chu kỳ spring-neap)
- `river_flow_lag`: thời gian di chuyển dòng chảy từ thượng nguồn
- `sea_level_lag`: ảnh hưởng triều chậm

**Tại sao lag_14 quan trọng nhất ở t+1?**
- Chu kỳ triều chính là ~14.76 ngày (spring-neap cycle)
- Mực nước hôm nay tương tự mực nước 14 ngày trước
- Periodogram cho thấy đỉnh ở 14.76 ngày (train) và 14.73 ngày (test)

### Nhóm 2: Rolling Features (10 đặc trưng)

**Ví dụ:** `rolling_mean_3`, `rolling_mean_7`, `rolling_std_7`, `sea_rolling_mean_7`, `cumulative_flow_7d`

**Ý nghĩa thủy văn:**
- `rolling_mean_7`: xu hướng mực nước trung bình 7 ngày
- `rolling_std_7`: biến động (không ổn định) gần đây
- `cumulative_flow_7d`: tổng lưu lượng 7 ngày (phản ánh lũ lũy)

### Nhóm 3: Seasonal Features (8 đặc trưng)

**Ví dụ:** `month_sin`, `month_cos`, `day_of_year_sin`, `tidal_cycle_sin`, `tidal_cycle_cos`

**Ý nghĩa thủy văn:**
- `month_sin/cos`: mã hóa mùa (mùa lũ vs mùa khô) liên tục
- `tidal_cycle_sin/cos`: mã hóa chu kỳ triều (14.76 ngày)
- Sử dụng sin/cos thay vì categorical để giữ tính liên tục

### Nhóm 4: Interaction Features (4 đặc trưng)

**Ví dụ:** `total_flow`, `flow_A_ratio`, `sea_river_diff`, `flood_pressure`

**Ý nghĩa thủy văn:**
- `total_flow`: tổng lưu lượng 2 nhánh sông
- `sea_river_diff`: hiệu mực nước biển - mực nước sông (áp lực triều)
- `flood_pressure`: kết hợp standardized của dòng chảy và mực nước biển → đo "áp lực lũ"

### Nhóm 5: Risk-oriented Features (6 đặc trưng)

**Ví dụ:** `distance_to_threshold`, `delta_1`, `acceleration`, `is_rising`, `danger_flag`

**Ý nghĩa thủy văn:**
- `distance_to_threshold`: khoảng cách đến ngưỡng cảnh báo P95
- `delta_1`: thay đổi mực nước 1 ngày (đang tăng hay giảm)
- `acceleration`: gia tốc thay đổi (phát hiện xu hướng tích cực)
- `is_rising`: mực nước đang tăng (1) hay giảm (0)

## Kết quả Feature Engineering

### Feature-group ablation (thêm từng nhóm vào mô hình)

| Nhóm thêm vào | MAE t+1 (RF) | MAE t+7 (RF) |
|---------------|-------------|-------------|
| Chỉ lag | 0.0300 m | 0.0340 m |
| + Rolling | 0.0250 m | 0.0280 m |
| + Seasonal | 0.0200 m | 0.0226 m |
| + Interaction | 0.0162 m | 0.0207 m |
| + Risk (full) | 0.0131 m | 0.0207 m |

**Nhận xét:** 
- Tại t+1, nhóm interaction và risk giúp giảm MAE nhiều nhất
- Tại t+7, nhóm seasonal giúp giảm MAE nhiều nhất (phản ánh chu kỳ)

### Feature selection

Sau khi tạo 41 feature, sử dụng Spearman correlation để lọc:
- Loại bỏ cặp feature có |ρ| > 0.95 (đa cộng tuyến)
- Loại bỏ feature có |ρ với target| < 0.05 (không liên quan)
- Kết quả: còn **26–27 feature** mỗi horizon

## Bài học chính

1. **Feature engineering quan trọng hơn model phức tạp** — Linear Regression với feature tốt > ensemble với feature đơn giản
2. **Hiểu domain để thiết kế feature** — knowledge về chu kỳ triều, thời gian di chuyển dòng chảy rất quan trọng
3. **Feature engineering "linearize" bài toán** — mối quan hệ trở nên tuyến tính ở short horizon
