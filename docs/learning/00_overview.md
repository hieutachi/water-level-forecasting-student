# 00 — Tổng quan bài toán và repo

## Bài toán: Dự báo mực nước vùng cửa sông Quảng Hà

Vùng cửa sông (estuary) là nơi nước sông từ thượng nguồn gặp nước triều từ biển. Mực nước tại đây bị ảnh hưởng bởi **cả hai yếu tố**:
- **Dòng chảy thượng nguồn**: lưu lượng từ các nhánh sông (Hà Côi, Tài Chi)
- **Dynamics triều**: mực nước biển/điều kiện thủy triều thay đổi theo chu kỳ

Khi cả hai yếu tố cùng cao (lũ kết hợp triều cường), nguy cơ ngập lụt tăng đáng kể. Việc **dự báo mực nước trước 1, 3, 7 ngày** rất quan trọng cho cảnh báo sớm.

## Dữ liệu: Output mô phỏng MIKE11

Dữ liệu trong nghiên cứu này được tạo ra từ **mô hình thủy động lực MIKE11**, không phải đo trực tiếp tại trạm. Điều này có nghĩa:
- Dữ liệu **mượt hơn** so với thực tế (ít nhiễu đo lường)
- Mô hình ML học được mối quan hệ input-output của **trình mô phỏng**, không phải của hệ thống thực địa
- Kết quả R² rất cao (>0.998) cần được hiểu trong bối cảnh này

## Pipeline học máy

```
Dữ liệu thô (MIKE11 output)
    ↓
Feature Engineering (5 nhóm feature)
    ↓
Temporal Train/Val/Test Split
    ↓
Huấn luyện mô hình (LR, RF, XGBoost, Stacking...)
    ↓
Đánh giá (MAE, RMSE, R², walk-forward, risk-zone)
    ↓
Giải thích (feature importance, SHAP)
```

## Mục tiêu học tập

Sau khi hoàn thành repo này, sinh viên sẽ hiểu được:
1. Cách xây dựng pipeline dự báo multi-step từ dữ liệu thủy văn
2. Tầm quan trọng của **feature engineering** (đôi khi quan trọng hơn model phức tạp)
3. Cách đánh giá mô hình đúng cách: temporal split, walk-forward, risk-zone
4. Cách đọc và viết paper khoa học

## Tài liệu tham khảo chính

Trong repo này, bạn sẽ tìm thấy:

| File | Mô tả |
|------|-------|
| `papers/paper_quang_ha_water_level_forecasting.pdf` | Paper đầy đủ (bản Markdown/LaTeX) |
| `papers/VNICT2026_paper_6546.pdf` | Paper đã nộp hội nghị VNICT2026 |
| `papers/THU_TRA_LOI_REVIEWER.md` | Thư trả lời phản biện — rất hữu ích cho sinh viên |

## Đọc tiếp

- [01 — Bài toán và dữ liệu](01_problem_and_data.md)
- [02 — Feature Engineering](02_feature_engineering.md)
- [03 — Mô hình và đánh giá](03_models_and_evaluation.md)
- [04 — Kết quả chính](04_key_findings.md)
- [05 — Hướng dẫn đọc paper](05_how_to_read_papers.md)
