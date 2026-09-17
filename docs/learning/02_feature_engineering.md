# 02 — FEATURE ENGINEERING
## 41 Đặc trưng, 5 Nhóm, Ablation Study

---

## 1. Tổng quan: Feature Engineering là đóng góp chính

```
╔══════════════════════════════════════════════════════════════════════╗
║  KẾT QUẢ QUAN TRỌNG NHẤT CỦA PAPER:                               ║
║                                                                      ║
║  Feature Engineering quan trọng hơn Model Complexity                 ║
║                                                                      ║
║  Linear Regression (model đơn giản nhất) đạt MAE THẤP NHẤT         ║
║  ở t+1 và t+3 — khi có feature engineering tốt!                     ║
║                                                                      ║
║  => Đầu tư vào thiết kế đặc trưng hiệu quả hơn                     ║
║     tìm kiếm model phức tạp (cho short horizon)                     ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 2. Năm nhóm Feature (Table III trong paper)

### Nhóm 1: LAG FEATURES (13 đặc trưng)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Feature              │ Lag    │ Ý nghĩa thủy học                       │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ water_level_lag_1    │ 1 ngày │ TÍNH TRÌ (persistence): WL hôm nay    │
│                      │        │ ≈ WL hôm qua (autocorrelation cao)    │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ water_level_lag_2    │ 2 ngày │ Mở rộng persistence window             │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ water_level_lag_3    │ 3 ngày │ Bắt đầu capture tidal oscillation     │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ water_level_lag_5    │ 5 ngày │ Nửa chu kỳ tuần (~7/2)                │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ water_level_lag_7    │ 7 ngày │ CHU KỲ TUẦN (weekly cycle)            │
│                      │        │ Autocorrelation tại lag 7 = -0.86     │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ water_level_lag_10   │ 10 ngày│ Transition giữa tuần và nửa tháng    │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ water_level_lag_14   │ 14 ngày│ ★ CHU KỲ TRIỀU NỬA THÁNG             │
│                      │        │ (~14.76 ngày spring-neap cycle)        │
│                      │        │ ★ Feature QUAN TRỌNG NHẤT ở t+1       │
│                      │        │ Autocorrelation lag 14 ≈ +0.91        │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ water_level_lag_21   │ 21 ngày│ Chu kỳ 3 tuần                        │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ water_level_lag_28   │ 28 ngày│ Chu kỳ 1 tháng (≈ 2 × spring-neap)   │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ water_level_lag_30   │ 30 ngày│ Chu kỳ tháng dương lịch              │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ water_level_lag_35   │ 35 ngày│ 5 tuần                               │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ water_level_lag_42   │ 42 ngày│ 6 tuần                               │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ water_level_lag_60   │ 60 ngày│ 2 tháng (seasonal memory)             │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ river_flow_A_lag_1   │ 1 ngày │ Lưu lượng Hà Côi hôm qua             │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ river_flow_B_lag_1   │ 1 ngày │ Lưu lượng Tài Chi hôm qua            │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ sea_level_lag_1      │ 1 ngày │ Mực nước biển hôm qua                 │
├──────────────────────┼────────┼─────────────────────────────────────────┤
│ sea_level_lag_3      │ 3 ngày │ Mực nước biển 3 ngày trước            │
└──────────────────────┴────────┴─────────────────────────────────────────┘
```

**Công thức toán:**
```
lag_h(Xₜ) = X(t - h)
```

**Tại sao lag_14 quan trọng nhất ở t+1?**

```
  Periodogram phân tích chu kỳ trong dữ liệu:
  
  Power
    │    *
    │   * *
    │  *   *
    │ *     *
    │*       *           *     *
    │         *         * *   *
    │          *       *   * *
    │           *     *     *
    │            *   *
    │             * *
    │              *
    └──────────────────────────────────────── Period (days)
    0    5    10   14.76  20    25    30
    
                   ↑
            Đỉnh chính: 14.76 ngày (train)
                        14.73 ngày (test)
            ≈ chu kỳ spring-neap (14.8 ngày)
  
  Autocorrelation structure:
  ┌───────┬────────────────┬───────────────────────────────┐
  │  Lag  │ Autocorrelation│ Ý nghĩa                       │
  ├───────┼────────────────┼───────────────────────────────┤
  │  1    │  +0.91         │ Rất cao (persistence)          │
  │  3    │  +0.33         │ Trung bình (đang giảm)         │
  │  7    │  -0.86         │ Âm mạnh (nửa chu kỳ triều!)   │
  │  14   │  +0.91         │ Lại dương (1 chu kỳ đầy đủ!)  │
  │  4    │  ≈ 0           │ Zero crossing (nửa nửa chu kỳ)│
  └───────┴────────────────┴───────────────────────────────┘
  
  So sánh với sin thuần: sin(t) tại lag 7 → -0.99
  Thực tế: -0.86 (gần nhưng không hoàn hảo do noise)
```

### Nhóm 2: ROLLING FEATURES (10 đặc trưng)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Feature               │ Window │ Stat  │ Ý nghĩa thủy học              │
├───────────────────────┼────────┼───────┼─────────────────────────────────┤
│ rolling_mean_3        │ 3 ngày │ mean  │ Xu hướng ngắn hạn (3 ngày)     │
│ rolling_mean_7        │ 7 ngày │ mean  │ Xu hướng trung bình tuần       │
│ rolling_mean_14       │ 14 ngày│ mean  │ Xu hướng nửa tháng             │
│ rolling_mean_30       │ 30 ngày│ mean  │ Xu hướng tháng                 │
│ rolling_std_3         │ 3 ngày │ std   │ Biến động 3 ngày               │
│ rolling_std_7         │ 7 ngày │ std   │ ★ Biến động tuần (volatility)  │
│ rolling_std_14        │ 14 ngày│ std   │ Biến động nửa tháng            │
│ rolling_std_30        │ 30 ngày│ std   │ Biến động tháng                │
│ rolling_min_7         │ 7 ngày │ min   │ Mực nước thấp nhất 7 ngày      │
│ rolling_max_7         │ 7 ngày │ max   │ Mực nước cao nhất 7 ngày       │
│ sea_rolling_mean_7    │ 7 ngày │ mean  │ Mực nước biển TB tuần          │
│ sea_rolling_std_7     │ 7 ngày │ std   │ Biến động biển tuần            │
│ cumulative_flow_7d    │ 7 ngày │ sum   │ ★ Tổng lưu lượng 7 ngày (lũ)  │
└───────────────────────┴────────┴───────┴─────────────────────────────────┘
```

**Công thức toán:**
```
rolling_mean_w(Xₜ) = (1/w) × Σ_{i=0}^{w-1} X(t-i)
rolling_std_w(Xₜ)  = sqrt((1/w) × Σ_{i=0}^{w-1} (X(t-i) - μ_w)²)
cumulative_flow_7d  = Σ_{i=0}^{6} [river_flow_A(t-i) + river_flow_B(t-i)]
```

### Nhóm 3: SEASONAL FEATURES (8 đặc trưng)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Feature             │ Công thức                    │ Ý nghĩa           │
├─────────────────────┼──────────────────────────────┼───────────────────┤
│ month_sin           │ sin(2π × month/12)           │ Mã hóa mùa liên  │
│ month_cos           │ cos(2π × month/12)           │ tục (sin/cos)    │
│ day_of_year_sin     │ sin(2π × day/365.25)         │ Mã hóa ngày trong│
│ day_of_year_cos     │ cos(2π × day/365.25)         │ năm              │
│ tidal_cycle_sin     │ sin(2π × t/T)                │ Mã hóa chu kỳ    │
│                     │ T = 14.76 ngày               │ triều spring-neap │
│ tidal_cycle_cos     │ cos(2π × t/T)                │                   │
│ is_monsoon          │ 1 nếu month ∈ [6,10]         │ Mùa mưa hay khô? │
└─────────────────────┴──────────────────────────────┴───────────────────┘

  Tại sao dùng sin/cos thay vì categorical?
  
  month = 6 (tháng 6) → 0.866
  month = 7 (tháng 7) → 1.000
  month = 8 (tháng 8) → 0.866
  
  → LIÊN TỤC: tháng 6 gần tháng 7 hơn tháng 12
  → categorical sẽ tạo ra discontinuity không mong muốn
  
  Tương tự cho tidal_cycle: T = 14.76 ngày
  → Đoạn sin/cos quay 2π mỗi 14.76 ngày
  → Giúp mô hình "biết" đang ở pha nào của chu kỳ triều
```

### Nhóm 4: INTERACTION FEATURES (4 đặc trưng)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Feature            │ Công thức                   │ Ý nghĩa thủy học    │
├────────────────────┼─────────────────────────────┼─────────────────────┤
│ total_flow         │ flow_A + flow_B             │ Tổng lưu lượng      │
│                    │                             │ thượng nguồn         │
├────────────────────┼─────────────────────────────┼─────────────────────┤
│ flow_A_ratio       │ flow_A / (total_flow + ε)   │ Tỷ lệ Hà Côi trong │
│                    │                             │ tổng lưu lượng       │
├────────────────────┼─────────────────────────────┼─────────────────────┤
│ sea_river_diff     │ sea_level - water_level     │ ★ ÁP LỰC TRIỀU:    │
│                    │                             │ biển cao hơn sông   │
│                    │                             │ → nước bị "đẩy lên" │
├────────────────────┼─────────────────────────────┼─────────────────────┤
│ flood_pressure     │ (flow_z) + (sea_z)          │ ★ ÁP LỰC LŨ:       │
│                    │ flow_z = (flow - μ)/σ        │ kết hợp standardized│
│                    │ sea_z = (sea - μ)/σ          │ cả dòng chảy + triều│
└────────────────────┴─────────────────────────────┴─────────────────────┘
```

**Giải thích `sea_river_diff` (áp lực triều):**
```
  Khi sea_level >> water_level:
  +--------+         +--------+
  | Biển   | ▲ cao   | Sông   | ▼ thấp
  | (high) |         | (low)  |
  +--------+         +--------+
       │                    │
       └──── sea_river_diff > 0 ────► Nước bị "đẩy" từ biển vào sông
                                      → mực nước sông TĂNG
  
  Khi sea_level << water_level:
  sea_river_diff < 0 → nước "thoát" ra biển → mực nước sông GIẢM
```

### Nhóm 5: RISK-ORIENTED FEATURES (6 đặc trưng)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Feature               │ Công thức              │ Ý nghĩa thủy học      │
├───────────────────────┼────────────────────────┼────────────────────────┤
│ distance_to_threshold │ P95 - water_level      │ Khoảng cách đến ngưỡng│
│                       │ P95 = 1.06 m           │ cảnh báo Warning       │
│                       │                        │ (+ = an toàn, - = nguy)│
├───────────────────────┼────────────────────────┼────────────────────────┤
│ delta_1               │ WL(t) - WL(t-1)        │ THAY ĐỔI 1 NGÀY:     │
│                       │                        │ (+) = đang TĂNG       │
│                       │                        │ (-) = đang GIẢM       │
├───────────────────────┼────────────────────────┼────────────────────────┤
│ acceleration          │ delta_1(t) - delta_1(t-1)│ GIA TỐC thay đổi:   │
│                       │                        │ (+) = đang TĂNG tốc   │
│                       │                        │ (-) = đang GIẢM tốc   │
│                       │                        │ ★ Feature #1 ở t+7   │
├───────────────────────┼────────────────────────┼────────────────────────┤
│ is_rising             │ 1 nếu delta_1 > 0      │ Mực nước ĐANG TĂNG?  │
│                       │ 0 nếu delta_1 ≤ 0      │ ★ Feature #1 ở t+3   │
├───────────────────────┼────────────────────────┼────────────────────────┤
│ danger_flag           │ 1 nếu WL > 0.9 × P95   │ Gần ngưỡng nguy hiểm?│
│                       │ 0 nếu ngược lại        │ (cờ cảnh báo sớm)    │
├───────────────────────┼────────────────────────┼────────────────────────┤
│ sea_delta_1           │ sea(t) - sea(t-1)       │ Thay đổi mực nước    │
│                       │                        │ biển 1 ngày (triều    │
│                       │                        │ đang lên hay xuống?)  │
└───────────────────────┴────────────────────────┴────────────────────────┘
```

---

## 3. Feature Ablation Study (Section IV-D, Figure 3)

Thử nghiệm thêm từng nhóm feature vào mô hình, đo MAE:

```
  MAE (m)
  0.035 ┤
        │  ████████
  0.030 ┤  ████████
        │  ████████
  0.025 ┤  ████████  ▓▓▓▓▓▓▓▓
        │  ████████  ▓▓▓▓▓▓▓▓
  0.020 ┤  ████████  ▓▓▓▓▓▓▓▓  ░░░░░░░░
        │  ████████  ▓▓▓▓▓▓▓▓  ░░░░░░░░
  0.015 ┤  ████████  ▓▓▓▓▓▓▓▓  ░░░░░░░░  ▒▒▒▒▒▒▒▒  ████
        │  ████████  ▓▓▓▓▓▓▓▓  ░░░░░░░░  ▒▒▒▒▒▒▒▒  ████
  0.010 ┤  ████████  ▓▓▓▓▓▓▓▓  ░░░░░░░░  ▒▒▒▒▒▒▒▒  ████
        │  ████████  ▓▓▓▓▓▓▓▓  ░░░░░░░░  ▒▒▒▒▒▒▒▒  ████
  0.005 ┤  ████████  ▓▓▓▓▓▓▓▓  ░░░░░░░░  ▒▒▒▒▒▒▒▒  ████
        └──────────────────────────────────────────────────
           Lag only   +Rolling   +Seasonal  +Interact  Full
                       only       only       only       set
  
  ████ MAE t+1 (Ridge)    ████ MAE t+7 (Ridge)
```

**Bảng chi tiết:**

```
┌──────────────────────┬───────────────┬───────────────┬───────────────┐
│ Nhóm feature thêm    │ MAE t+1 (m)   │ MAE t+3 (m)   │ MAE t+7 (m)   │
│                      │ (Ridge)       │ (Ridge)       │ (Ridge)       │
├──────────────────────┼───────────────┼───────────────┼───────────────┤
│ Chỉ Lag (baseline)   │ 0.0248        │ —             │ 0.0345        │
│ + Rolling            │ 0.0220        │ —             │ 0.0300        │
│ + Seasonal           │ 0.0200        │ —             │ ★ 0.0163      │
│ + Interaction        │ 0.0162        │ —             │ 0.0160        │
│ + Risk (FULL SET)    │ ★ 0.0131      │ 0.0140        │ 0.0207        │
└──────────────────────┴───────────────┴───────────────┴───────────────┘

Nhận xét quan trọng:
- Ở t+1: interaction + risk features giúp giảm MAE nhiều nhất
- Ở t+7: ★ seasonal features giúp giảm MAE nhiều nhất (0.0345→0.0163)
          → Phản ánh tầm quan trọng của chu kỳ mùa ở horizon dài
- Ở t+3: Ridge đạt optimal với FULL SET (0.0140 m)
          → Xác nhận: feature engineering "linearize" bài toán t+3
```

---

## 4. Feature Importance theo Horizon (Table IX)

```
  t+1 (Random Forest — Mean Decrease in Impurity):
  ┌────────────────────────────┬──────────┐
  │ Feature                    │ Importance│
  ├────────────────────────────┼──────────┤
  │ water_level_lag_14         │ ████████████████████ 0.496 │ ←★ #1
  │ distance_to_threshold      │ █████████ 0.205           │
  │ flood_pressure             │ ████ 0.095                │
  │ sea_delta_1                │ ███ 0.063                 │
  │ water_level_lag_7          │ ██ 0.054                  │
  └────────────────────────────┴──────────┘
  Cơ chế: CHU KỲ TRIỀU NỬA THÁNG (14.76 ngày)
  
  t+3 (XGBoost — Total Gain):
  ┌────────────────────────────┬──────────┐
  │ Feature                    │ Importance│
  ├────────────────────────────┼──────────┤
  │ is_rising                  │ ████████████████████████████████████████ 0.921│ ←★ #1
  │ sea_delta_1                │ ██ 0.040                  │
  │ rolling_min_7              │ █ 0.012                   │
  │ rolling_std_7              │ █ 0.010                   │
  │ day_of_year_sin            │ ▌ 0.004                   │
  └────────────────────────────┴──────────┘
  Cơ chế: TRẠNG THÁI TĂNG/GIẢM (rising/falling dynamics)
  
  t+7 (XGBoost — Total Gain):
  ┌────────────────────────────┬──────────┐
  │ Feature                    │ Importance│
  ├────────────────────────────┼──────────┤
  │ acceleration               │ ████████████████████ 0.421 │ ←★ #1
  │ water_level_lag_7          │ ████████████ 0.253        │
  │ rolling_std_7              │ ████ 0.075                │
  │ sea_river_diff             │ ████ 0.073                │
  │ rolling_min_7              │ ██ 0.032                  │
  └────────────────────────────┴──────────┘
  Cơ chế: GIA TỐC + CHU KỲ TUẦN (acceleration + weekly cycles)
```

**Tổng hợp cơ chế theo horizon:**

```
┌─────────┬──────────────────────────────────────────────────────────────┐
│ Horizon │ Cơ chế thủy học chi phối                                    │
├─────────┼──────────────────────────────────────────────────────────────┤
│ t+1     │ TÍNH TRÌ + CHU KỲ TRIỀU:                                   │
│ (1 ngày)│ Mực nước hôm nay rất giống 14 ngày trước (spring-neap)     │
│         │ Feature chính: water_level_lag_14 (0.496)                   │
│         │ Autocorrelation lag 14 ≈ +0.91                              │
├─────────┼──────────────────────────────────────────────────────────────┤
│ t+3     │ TRẠNG THÁI TĂNG/GIẢM:                                      │
│ (3 ngày)│ Biết mực nước ĐANG TĂNG hay GIẢM quan trọng hơn            │
│         │ việc biết giá trị cụ thể 3 ngày trước                      │
│         │ Feature chính: is_rising (0.921) — chiếm 92% importance!   │
│         │ Autocorrelation lag 3 = +0.33 (đã yếu)                     │
├─────────┼──────────────────────────────────────────────────────────────┤
│ t+7     │ GIA TỐC + CHU KỲ TUẦN:                                     │
│ (7 ngày)│ Xu hướng TĂNG/GIẢM TỐC ĐỘ thay đổi quan trọng              │
│         │ Feature chính: acceleration (0.421) + lag_7 (0.253)         │
│         │ Autocorrelation lag 7 = -0.86 (nửa chu kỳ triều)           │
└─────────┴──────────────────────────────────────────────────────────────┘
```

---

## 5. Wilcoxon Signed-Rank Tests

So sánh statistical significance giữa các cặp mô hình:

```
┌──────────────┬─────────────┬─────────────┬─────────────────────────────┐
│ So sánh      │ Horizon     │ p-value     │ Significant?                │
├──────────────┼─────────────┼─────────────┼─────────────────────────────┤
│ RF vs XGB    │ t+1         │ 0.31        │ ❌ KHÔNG (không phân biệt) │
│ RF vs XGB    │ t+3         │ < 0.05      │ ✅ CÓ                      │
│ RF vs XGB    │ t+7         │ > 0.05      │ ❌ KHÔNG                   │
│ XGB vs Stack │ t+3         │ < 0.001     │ ✅ CÓ (rất significant)    │
│ XGB vs Stack │ t+7         │ 0.022       │ ✅ CÓ                      │
│ RF vs Stack  │ t+7         │ 0.004       │ ✅ CÓ                      │
└──────────────┴─────────────┴─────────────┴─────────────────────────────┘

Sai sót trong bản gốc: claim "significant at t+1" nhưng p=0.31 → ĐÃ SỬA
→ Không có sự khác biệt có ý nghĩa thống kê giữa RF và XGBoost ở t+1
→ Ba ensemble khác nhau < 0.0005 m MAE ở t+1 → gần như tương đương
```
