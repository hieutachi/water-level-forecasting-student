# 01 — BÀI TOÁN VÀ DỮ LIỆU
## Chi tiết Problem Formulation, Dataset, Temporal Split

---

## 1. Problem Formulation (Section III-B)

### Bài toán: Direct Multi-step Regression

Tại mỗi thời điểm `t`, mô hình nhận vector đặc trưng X(t) và dự báo mực nước tại 3 thời điểm tương lai:

```
ŴL(t+1) = f₁(Xₜ; θ₁)
ŴL(t+3) = f₃(Xₜ; θ₃)
ŴL(t+7) = f₇(Xₜ; θ₇)
```

Trong đó:
- `WL` = water level tại Quang Hà (m)
- `Xₜ` = vector đặc trưng tại thời điểm t (26–27 features)
- `fₕ` = mô hình dự báo trực tiếp cho horizon h
- `θₕ` = tham số học được của fₕ

### Tại sao DIRECT strategy?

```
  RECURSIVE (TỪNG BƯỚC):                   DIRECT (TRỰC TIẾP):
  +---+     +---+     +---+                 +---+     +---+     +---+
  | t |--►--|t+1|--►--|t+2|                 | t |--►--|t+1|     |t+3|     |t+7|
  +---+     +---+     +---+                 +---+     +---+     +---+     +---+
    |         |         |                      │        │         │         │
    ▼         ▼         ▼                      ▼        ▼         ▼         ▼
  f(Xₜ)    f(Xₜ₊₁)  f(Xₜ₊₂)              f₁(Xₜ)  f₃(Xₜ)   f₇(Xₜ)
             ▲                                              ▲         ▲
             │                                              │         │
         LỖI TÍCH LŨY!                               KHÔNG tích lũy lỗi!
         (error từ t+1                                 (mỗi model
          propagate → t+2, t+3)                         học riêng)
```

**Paper sử dụng DIRECT strategy** vì:
1. Tránh tích lũy lỗi (error accumulation) qua các bước
2. Mỗi horizon có thể có subset features riêng (26–27 features khác nhau)
3. Mỗi horizon có thể dùng model configuration riêng

---

## 2. Dataset chi tiết (Section III-A, III-B)

### Nguồn dữ liệu: MIKE11 Hydrodynamic Simulation

```
╔══════════════════════════════════════════════════════════════════════════╗
║                     MIKE11 HYDRODYNAMIC MODEL                          ║
║                                                                        ║
║  MÔ HÌNH THỦY ĐỘNG LỰC: Giải phương trình Saint-Venant 1D             ║
║                                                                        ║
║  ∂A/∂t + ∂Q/∂x = q        (continuity - bảo toàn khối lượng)          ║
║                                                                        ║
║  ∂Q/∂t + ∂(Q²/A)/∂x + gA ∂h/∂x = -gA·Sf   (momentum)                ║
║                                                                        ║
║  Trong đó:                                                             ║
║    A = tiết diện ngang (m²)                                           ║
║    Q = lưu lượng (m³/s)                                               ║
║    h = mực nước (m)                                                   ║
║    g = gia tốc trọng lực (9.81 m/s²)                                  ║
║    Sf = slope ma sát                                                  ║
║    q = dòng vào/ra bên (lateral inflow)                               ║
║                                                                        ║
║  INPUT:  - Boundary conditions (upstream Q, downstream WL)             ║
║          - Cross-section geometry                                      ║
║          - Manning roughness coefficients                              ║
║                                                                        ║
║  OUTPUT: Daily water level at Ha Coi section (1990–2021)               ║
║          → Đây chính là dữ liệu dùng trong bài báo!                  ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Cấu trúc dữ liệu

```
┌───────────────┬───────────────┬──────────────┬──────────────┬──────────────┐
│ Date Time     │ Biên trên 1   │ Biên trên 2  │ Biên dưới    │ Kết quả      │
│ (DD/MM/YYYY)  │ river_flow_A  │ river_flow_B │ sea_level    │ water_level  │
│               │ (m³/s)        │ (m³/s)       │ (m)          │ (m)          │
├───────────────┼───────────────┼──────────────┼──────────────┼──────────────┤
│ 01/01/1990    │ 1.070         │ 7.517        │ -0.217       │ -3.480       │
│ 01/02/1990    │ 1.070         │ 0.000        │ 0.231        │ 0.220        │
│ 01/03/1990    │ 0.970         │ 0.000        │ 0.600        │ 0.570        │
│ ...           │ ...           │ ...          │ ...          │ ...          │
│ 31/12/2021    │ ...           │ ...          │ ...          │ ...          │
└───────────────┴───────────────┴──────────────┴──────────────┴──────────────┘

  Tổng số mẫu: 11,688 ngày (32 năm × 365.25 ngày/năm)
  Tần suất:    Daily (hourly aggregated → daily mean)
  Missing:     Không có (simulation output hoàn chỉnh)
```

### Ý nghĩa thủy văn của 4 biến

```
┌───────────────────────────────────────────────────────────────────────┐
│ Biến            │Nguồn        │ Ý nghĩa thủy học                    │
├─────────────────┼─────────────┼──────────────────────────────────────┤
│ river_flow_A    │ Nhánh Hà Côi│ Lưu lượng thượng nguồn CHÍNH.       │
│ (Biên trên 1)   │ (2380 km²)  │ Chiếm phần lớn dòng chảy. Tăng     │
│                 │             │ vào mùa mưa (tháng 6–10).           │
├─────────────────┼─────────────┼──────────────────────────────────────┤
│ river_flow_B    │ Nhánh Tài Chi│ Lưu lượng thượng nguồn PHỤ.       │
│ (Biên trên 2)   │ (780 km²)   │ Nhỏ hơn Hà Côi. Đóng góp ~25%.    │
├─────────────────┼─────────────┼──────────────────────────────────────┤
│ sea_level       │ Biển Đông   │ Mực nước biển/triều (downstream     │
│ (Biên dưới)     │ (tidal      │ boundary). Chu kỳ triều ~14.76     │
│                 │ boundary)   │ ngày (spring-neap cycle).           │
├─────────────────┼─────────────┼──────────────────────────────────────┤
│ water_level     │ Gauge Ha Coi│ Mực nước tại Quang Hà — BIẾN MỤC   │
│ (Kết quả)       │ (4985.68)   │ TIÊU (target). Bị ảnh hưởng bởi    │
│                 │             │ TẤT CẢ 3 biến trên.                 │
└─────────────────┴─────────────┴──────────────────────────────────────┘
```

---

## 3. Temporal Train/Val/Test Split (Section III-A)

### Tại sao KHÔNG dùng Random Split?

```
  ❌ RANDOM SPLIT (SAI cho time series):
  
  Dữ liệu:  t=1  t=2  t=3  t=4  t=5  t=6  t=7  t=8
             [  TRAIN  ] [TEST] [  TRAIN  ] [TEST]
                  ▲                ▲
                  │                │
            Dữ liệu ngày t+1 ở TEST
            nhưng t ở TRAIN
            → MODEL "THẤY" thông tin tương lai!
            → DATA LEAKAGE!
  
  
  ✅ TEMPURAL SPLIT (ĐÚNG cho time series):
  
  Dữ liệu:  t=1  t=2  t=3  t=4  t=5  t=6  t=7  t=8
             [====== TRAIN ======] [ VAL ] [ TEST ]
             1990─────────2017    2018-19  2020-21
             
             → KHÔNG có overlap
             → KHÔNG leak thông tin tương lai
```

### Phân chia cụ thể trong paper

```
┌──────────────────────────────────────────────────────────────────────┐
│ Tập      │ Thời gian      │ Số mẫu   │ Tỷ lệ  │ Vai trò           │
├──────────┼────────────────┼──────────┼────────┼───────────────────┤
│ Train    │ 1990–2017      │ 10,213   │ 87.5%  │ Huấn luyện model  │
│          │ (28 năm)       │          │        │ Feature selection  │
│          │                │          │        │ Tính P95/P99       │
├──────────┼────────────────┼──────────┼────────┼───────────────────┤
│ Val      │ 2018–2019      │ 730      │ 6.2%   │ Optuna hyper-     │
│          │ (2 năm)        │          │        │ parameter tuning   │
│          │                │          │        │ Meta-learner train │
├──────────┼────────────────┼──────────┼────────┼───────────────────┤
│ Test     │ 2020–2021      │ 722      │ 6.2%   │ Đánh giá cuối cùng│
│          │ (2 năm)        │          │        │ KHÔNG touch cho    │
│          │                │          │        │ đến khi xong       │
├──────────┼────────────────┼──────────┼────────┼───────────────────┤
│ TỔNG     │ 1990–2021      │ 11,665   │ 100%   │                   │
│          │ (32 năm)       │ (after   │        │                   │
│          │                │ drop NaN)│        │                   │
└──────────┴────────────────┴──────────┴────────┴───────────────────┘
```

### Walk-forward Validation (Section III-D, IV-B)

```
  Expanding window, retrain mỗi 4 tuần:
  
  Window 1:  [1990──────────────────2019.12] |eval: 2020.01-02|
  Window 2:  [1990──────────────────2020.02] |eval: 2020.03-04|
  Window 3:  [1990──────────────────2020.04] |eval: 2020.05-06|
  ...        ...                              ...
  Window 13: [1990──────────────────2020.12] |eval: 2021.01-02|
  
  Lưu ý:
  - Cửa sổ MỞ RỘNG qua thời gian (expanding, KHÔNG sliding)
  - Phần cuối mỗi cửa sổ (hàng h) bị BỎ để tránh target leakage
  - Chỉ đánh giá trên Stacking model
  - Cho 366 evaluation days per horizon (1 năm 2020)
  
  Kết quả:
  ┌─────────┬────────────┬──────────────────────┐
  │ Horizon │ MAPE (%)   │ Ghi chú              │
  ├─────────┼────────────┼──────────────────────┤
  │ t+1     │ 3.4%       │ Tăng nhẹ so static   │
  │ t+3     │ 7.2%       │ ≈ static split       │
  │ t+7     │ —          │ Chưa báo cáo chi tiết│
  └─────────┴────────────┴──────────────────────┘
```

---

## 4. Vấn đề Data Leakage trong Naive Baselines

**Bug nghiêm trọng** được phát hiện trong thư trả lời Reviewer (Comment 7):

```
  ❌ BẢN GỐC (CÓ BUG):
  
  naive_forecast = target_column.shift(lag)
  
  Vấn đề: Khi h > lag, shift(-h) DÙNG GIÁ TRỊ TƯƠNG LAI
  → Data leakage!
  
  
  ✅ BẢN SỬA (ĐÚNG):
  
  naive_forecast = water_level_by_date[date - lag]
  
  Tra cứu theo NGÀY, không phải theo index
  → Leak-free, MAE ≈ hằng số across horizons (như kỳ vọng)
```

**Kết quả sau khi sửa:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Baseline    │ MAE t+1  │ MAE t+3  │ MAE t+7  │ Ghi chú        │
├─────────────┼──────────┼──────────┼──────────┼────────────────┤
│ Naive-lag14 │ 0.0814   │ 0.6001   │ 1.2609   │ Tốt nhất t+1   │
│ Naive-lag7  │ 1.2847   │ 1.0999   │ 0.2120   │ Tốt nhất t+7   │
│ Naive-lag1  │ 0.5370   │ —        │ 1.2846   │ Rất tệ         │
└─────────────┴──────────┴──────────┴──────────┴────────────────┘

Nhận xét: Naive-lag14 tốt nhất ở t+1 → phản ánh chu kỳ triều ~14 ngày
          Naive-lag7 tốt nhất ở t+7 → phản ánh chu kỳ tuần
```

---

## 5. Giải thích R² rất cao

```
╔══════════════════════════════════════════════════════════════════════════╗
║  TẠI SAO R² > 0.998?                                                  ║
║                                                                        ║
║  R² = 1 - (SS_res / SS_tot)                                          ║
║                                                                        ║
║  SS_tot = Σ(yᵢ - ȳ)²    Tổng phương sai của target                  ║
║  SS_res = Σ(yᵢ - ŷᵢ)²   Tổng phương sai dư                         ║
║                                                                        ║
║  Khi dữ liệu MIKE11 tuân theo phương trình vật lý XÁC ĐỊNH:         ║
║  → Phương trình mượt (smooth dynamics)                                ║
║  → Ít biến động ngẫu nhiên                                           ║
║  → SS_res rất nhỏ so với SS_tot                                      ║
║  → R² ≈ 1                                                            ║
║                                                                        ║
║  Dữ liệu đo thực tế:                                                  ║
║  → Có nhiễu đo lường, missing data, unmodeled processes             ║
║  → SS_res lớn hơn                                                    ║
║  → R² dự kiến THẤP HƠN NHIỀU                                         ║
║                                                                        ║
║  Paper báo cáo R² dải: 0.9984 – 0.9996 (cho learned models)         ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Spearman Correlation Filtering (Section III-C)

Quá trình chọn feature (chỉ dùng trên train set!):

```
  Bước 1: Tính Spearman ρ giữa MỌI ĐẶC TRƯNG và TARGET
           (chỉ trên train set)
  
  Bước 2: Loại bỏ feature có |ρ_target| < 0.05
           (feature không liên quan đến target)
  
  Bước 3: Với mỗi cặp feature có |ρ_AB| > 0.95:
           Giữ lại feature có |ρ_target| CAO HƠN
           Loại bỏ feature kia
           (giảm đa cộng tuyến)
  
  Kết quả: 41 features → 26–27 features per horizon
  
  ┌─────────┬──────────────────────────────────────┐
  │ Horizon │ Số features sau selection             │
  ├─────────┼──────────────────────────────────────┤
  │ t+1     │ 27 features                          │
  │ t+3     │ 26 features                          │
  │ t+7     │ 27 features                          │
  └─────────┴──────────────────────────────────────┘
```

**LƯU Ý QUAN TRỌNG:** Feature selection CHỈ dùng trên train set. KHÔNG dùng thông tin từ val/test để chọn feature → tránh data leakage.
