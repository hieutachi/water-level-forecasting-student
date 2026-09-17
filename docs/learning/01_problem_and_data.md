# 01 — Bài toán và dữ liệu

## Bài toán: Multi-step Water Level Forecasting

### Định nghĩa

Cho một thời điểm `t`, dự báo mực nước tại `t+1`, `t+3`, và `t+7` ngày sau:

```
ŴL(t+1) = f₁(X(t))
ŴL(t+3) = f₃(X(t))
ŴL(t+7) = f₇(X(t))
```

Trong đó:
- `X(t)` là vector đặc trưng tại thời điểm `t`
- `f₁, f₃, f₇` là các mô hình riêng cho mỗi horizon

### Tại sao dùng Direct Strategy (không dùng Recursive)?

- **Recursive**: dự báo t+1, rồi dùng kết quả đó để dự báo t+2, v.v. → **tích lũy lỗi**
- **Direct**: mỗi horizon có model riêng → không tích lũy lỗi, mỗi horizon tối ưu riêng

## Dữ liệu: Output MIKE11

### Cấu trúc dữ liệu

| Cột | Đơn vị | Ý nghĩa |
|-----|--------|----------|
| `Date Time` | — | Ngày tháng |
| `Bien tren 1` | m³/s | Lưu lượng nhánh sông Hà Côi |
| `Bien tren 2` | m³/s | Lưu lượng nhánh sông Tài Chi |
| `Bien duoi` | m | Mực nước biên dưới (mực nước biển/triều) |
| `Ket qua HACOI` | m | Mực nước tại khu vực Quảng Hà |

### Quan trọng: Dữ liệu mô phỏng, không phải đo thực

**Đây là điểm quan trọng nhất cần hiểu:**

Tất cả dữ liệu trong nghiên cứu đều là **output của mô hình thủy động lực MIKE11** — một trình mô phỏng giải phương trình thủy động lực. Điều này có nghĩa:

1. **Dữ liệu mô phỏng trơn hơn** dữ liệu đo thực: tuân theo phương trình vật lý xác định, không có nhiễu đo lường, không có missing data
2. **Mô hình ML học được mối quan hệ của trình mô phỏng**, không phải của hệ thống thực địa
3. **R² > 0.998** phản ánh tính "dễ dự báo" của dữ liệu mô phỏng, KHÔNG đảm bảo hiệu suất thực tế tương tự
4. Paper gọi mô hình ML là **"surrogate"** (phần thay thế nhanh) cho mô hình thủy động lực, không phải hệ thống dự báo thực địa

### Vùng nghiên cứu: Quảng Hà, Quảng Ninh

- Cửa sông ven biển, ảnh hưởng bởi cả nước sông và triều
- Nhận nước từ 2 nhánh: Hà Côi (chính) và Tài Chi
- Dữ liệu từ 1990–2021 (32 năm)

## Temporal Split (Chia theo thời gian)

### Tại sao không dùng Random Split?

Dữ liệu thời gian có tính **liên tục** và **tự tương quan**. Nếu chia ngẫu nhiên:
- Dữ liệu ngày 15/1/2015 có thể ở train, nhưng ngày 16/1/2015 ở test
- Mô hình "học thuộc" thông tin của ngày liền kề → **data leakage**
- Kết quả đánh giá sẽ **quá lạc quan** (overestimate)

### Cách chia trong paper

```
Train:  1990–2017 (28 năm, 10,213 mẫu)
Val:    2018–2019 (2 năm, 730 mẫu)
Test:   2020–2021 (2 năm, 722 mẫu)
```

**Lưu ý:** Không dùng thông tin từ tương lai (test set) để tạo feature hoặc chọn feature. Tất cả quá trình feature selection chỉ dùng trên train set.

## Walk-forward Validation

Ngoài temporal split tĩnh, paper còn dùng **walk-forward validation**:
- Mô hình được **retrain mỗi 4 tuần**
- Cửa sổ huấn luyện **mở rộng** qua thời gian (expanding window)
- Phần cuối mỗi cửa sổ (hàng `h`) được bỏ để tránh overlap target
- Kết quả: MAPE từ 3.4% (t+1) đến 7.2% (t+3)

Walk-forward cho thấy hiệu suất **ổn định** dưới điều kiện vận hành thực tế.
