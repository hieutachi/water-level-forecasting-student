# Multi-step Water Level Forecasting — Từ DATN đến Paper Quốc tế

Repo học tập về hành trình **3 bước** từ Đồ án Tốt nghiệp đến Paper VNICT2026: dự báo mực nước đa bước tại cửa sông Quảng Hà bằng học máy.

## Hành trình 3 bước

| Level | Nội dung | Trạng thái |
|-------|----------|------------|
| **Level 1: DATN** | Sinh viên Nguyễn Thị Thảo xây dựng pipeline đầy đủ: data → 41 features → RF/XGB/Stacking → AdaptiveStack → demo website | ✅ Hoàn thành |
| **Level 2: Paper Gốc** | Giảng viên phát triển DATN thành paper 6 trang, thêm walk-forward, SHAP, nộp VNICT2026 | ✅ Đã nộp |
| **Level 3: Paper Sửa** | Sau 7 comments reviewer: đổi tiêu đề, surrogate framing, noise experiment, rebuild risk-zone, sửa 10 lỗi | ✅ Đã sửa |

📖 **Xem chi tiết tại trang HTML:** [GitHub Pages](https://hieutachi.github.io/water-level-forecasting-student/)

## Mô tả

Repository phục vụ sinh viên muốn hiểu:
- Cách xây dựng pipeline dự báo mực nước từ dữ liệu thủy văn
- Tầm quan trọng của **feature engineering** (LR thắng ensemble ở t+1, t+3)
- Cách đánh giá mô hình đúng cách: temporal split, walk-forward, risk-zone
- Cách phản biện và cải thiện paper khoa học (đọc thư trả lời reviewer)

**Lưu ý:** Dữ liệu là **output mô phỏng MIKE11** (không phải đo thực). Mô hình ML là "surrogate" — phần thay thế nhanh cho trình mô phỏng, KHÔNG phải hệ thống dự báo thực địa đã validated.

## Yêu cầu hệ thống

- Python 3.10+
- pip hoặc conda
- Git

## Cài đặt

### Cách 1: Dùng venv (khuyến nghị)

```bash
# Clone repo
git clone <repo-url>
cd water-level-forecasting-student

# Tao moi truong ao
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Kích hoạt (Linux/Mac)
source venv/bin/activate

# Cai dat thu vien
pip install -r requirements.txt
```

### Cách 2: Dùng conda

```bash
conda env create -f environment.yml
conda activate water-level-forecasting
```

## Tạo dữ liệu mẫu (nếu chưa có)

Nếu bạn chưa có dữ liệu thật, chạy script sau để tạo dữ liệu giả lập có cấu trúc giống MIKE11:

```bash
python scripts/generate_data.py
```

Dữ liệu sẽ được lưu vào `data/raw/Dulieughep.csv`.

## Chạy mẫu

### Cách 1: Chạy notebook (khuyến nghị)

Mở notebook theo thứ tự:

1. **`notebooks/01_exploratory_data_analysis.ipynb`** — Phân tích khám phá dữ liệu
2. **`notebooks/02_feature_engineering_demo.ipynb`** — Minh họa feature engineering
3. **`notebooks/03_model_comparison.ipynb`** — So sánh mô hình (pipeline chính)
4. **`notebooks/04_risk_zone_and_shap.ipynb`** — Risk-zone evaluation

```bash
cd notebooks
jupyter notebook
```

### Cách 2: Chạy test

```bash
python -m pytest tests/ -v
```

## Tài liệu học

Sinh viên bắt đầu từ **`docs/learning/00_overview.md`**, sau đó đọc lần lượt:

| File | Nội dung |
|------|----------|
| `docs/learning/00_overview.md` | Tổng quan bài toán và repo |
| `docs/learning/01_problem_and_data.md` | Bài toán multi-step và dữ liệu MIKE11 |
| `docs/learning/02_feature_engineering.md` | 5 nhóm feature và ý nghĩa thủy văn |
| `docs/learning/03_models_and_evaluation.md` | Các mô hình và cách đánh giá |
| `docs/learning/04_key_findings.md` | Kết quả chính từ paper |
| `docs/learning/05_how_to_read_papers.md` | Hướng dẫn đọc paper và thư trả lời |
| `docs/checklist.md` | Checklist công việc cho sinh viên |

## Chuẩn bị trình bày

1. Đọc `docs/presentation/presentation_guide.md` — hướng dẫn chi tiết
2. Xem `docs/presentation/slides.md` — slide mẫu (mở bằng Marp hoặc VS Code)
3. Tập nói theo speaker notes (thời gian: 10–12 phút)
4. Chuẩn bị trả lời câu hỏi thường gặp

## Papers tham khảo

| File | Mô tả |
|------|-------|
| `papers/paper_quang_ha_water_level_forecasting.pdf` | Paper đầy đủ |
| `papers/VNICT2026_paper_6546.pdf` | Paper đã nộp hội nghị (6 trang) |
| `papers/THU_TRA_LOI_REVIEWER.md` | Thư trả lời phản biện — rất hữu ích! |

Xem thêm hướng dẫn đọc tại `docs/learning/05_how_to_read_papers.md`.

## Cấu trúc thư mục

```
water-level-forecasting-student/
├── configs/
│   └── config.yaml              # Cau hinh pipeline
├── data/
│   ├── raw/                     # Du lieu goc (CSV)
│   └── processed/               # Du lieu da xu ly
├── docs/
│   ├── learning/                # Tai lieu hoc (6 file markdown)
│   ├── presentation/            # Slide va huong dan trinh bay
│   └── checklist.md             # Checklist cong viec
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_feature_engineering_demo.ipynb
│   ├── 03_model_comparison.ipynb
│   └── 04_risk_zone_and_shap.ipynb
├── papers/                      # Paper va thu tra loi reviewer
├── scripts/
│   └── generate_data.py         # Tao du lieu gia lap
├── src/
│   ├── data/                    # Doc va chuan bi du lieu
│   ├── features/                # Feature engineering
│   ├── models/                  # Huan luyen mo hinh
│   ├── evaluation/              # Danh gia (metrics, risk-zone)
│   └── utils/                   # Tien ich (config, plotting)
├── tests/
│   ├── test_features.py
│   ├── test_models.py
│   └── test_evaluation.py
├── .gitignore
├── environment.yml
├── LICENSE
├── README.md
└── requirements.txt
```

## Ghi chú về dữ liệu

- Nếu repo không kèm dữ liệu thật, chạy `python scripts/generate_data.py` để tạo dữ liệu giả lập
- Dữ liệu giả lập có cấu trúc giống MIKE11 nhưng giá trị không phải số liệu thật
- Để có dữ liệu thật, liên hệ giảng viên

## License

MIT License — xem file `LICENSE` để biết thêm chi tiết.
