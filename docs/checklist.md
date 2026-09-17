# Checklist cho sinh viên — Mini-project dự báo mực nước

## Bước 1: Đọc hiểu bài toán (1–2 giờ)

- [ ] Đọc `docs/learning/00_overview.md` — tổng quan
- [ ] Đọc `docs/learning/01_problem_and_data.md` — bài toán và dữ liệu
- [ ] Xem cấu trúc dữ liệu mẫu trong `data/raw/`
- [ ] Hiểu tại sao dùng temporal split, không dùng random split

## Bước 2: Chạy EDA (1–2 giờ)

- [ ] Mở notebook `notebooks/01_exploratory_data_analysis.ipynb`
- [ ] Chạy tất cả cells, hiểu phân bố dữ liệu
- [ ] Nhận xét: mực nước có chu kỳ không? Lưu lượng thay đổi thế nào theo mùa?

## Bước 3: Feature Engineering (2–3 giờ)

- [ ] Đọc `docs/learning/02_feature_engineering.md`
- [ ] Chạy notebook `notebooks/02_feature_engineering_demo.ipynb`
- [ ] **Thử sửa/nhóm lại feature** (ví dụ: thêm feature mới, bỏ feature yếu)
- [ ] Ghi nhận: feature nào quan trọng nhất? Tại sao?

## Bước 4: Huấn luyện và so sánh mô hình (2–3 giờ)

- [ ] Đọc `docs/learning/03_models_and_evaluation.md`
- [ ] Chạy notebook `notebooks/03_model_comparison.ipynb`
- [ ] **Huấn luyện ít nhất 2 mô hình** (Linear Regression, XGBoost)
- [ ] So sánh MAE, R² cho t+1, t+3, t+7
- [ ] Trả lời: Mô hình nào tốt nhất? Tại sao?

## Bước 5: Risk-zone evaluation (1–2 giờ)

- [ ] Chạy notebook `notebooks/04_risk_zone_and_shap.ipynb`
- [ ] **Viết 1 trang nhận xét** về:
  - Phân bố 3 vùng (Normal/Warning/Exceedance)
  - Tại sao accuracy cao nhưng cần thận trọng?
  - Vấn đề imbalance và Wilson CI

## Bước 6: Đọc paper và thư trả lời (2–3 giờ)

- [ ] Đọc abstract + introduction cả 2 paper
- [ ] Đọc Section IV (Results) — hiểu từng bảng
- [ ] Đọc Section V (Limitations) — **phần quan trọng nhất!**
- [ ] Đọc `THU_TRA_LOI_REVIEWER.md` — học cách phản biện
- [ ] **Viết 1 trang tóm tắt** bài học về scientific writing
- [ ] Trả lời: Tiêu đề paper thay đổi như thế nào? Tại sao?

## Bước 7: Chuẩn bị trình bày (1–2 giờ)

- [ ] Đọc `docs/presentation/presentation_guide.md`
- [ ] Xem `docs/presentation/slides.md` (mở bằng Marp hoặc VS Code)
- [ ] **Tạo slide 5–7 slide ngắn** cho báo cáo lớp, dựa trên template
- [ ] **Tập nói** theo speaker notes (thời gian: 5–7 phút)
- [ ] Chuẩn bị trả lời 2 câu hỏi thường gặp

## Bonus (nếu có thời gian)

- [ ] Thử thêm noise vào dữ liệu (tham khảo noise experiment trong paper)
- [ ] Phân tích feature importance cho mô hình của bạn
- [ ] So sánh walk-forward vs static split
- [ ] Thử feature mới mà bạn nghĩ ra

## Nộp bài

- [ ] Notebook đã chạy hết, không lỗi
- [ ] File nhận xét risk-zone (1 trang)
- [ ] File tóm tắt bài học scientific writing (1 trang)
- [ ] Slide trình bày (5–7 slide)
