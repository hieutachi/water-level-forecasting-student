# 05 — HƯỚNG DẪN ĐỌC PAPER VÀ THƯ TRẢ LỜI
## So sánh 2 phiên bản, Bài học Scientific Writing, Script trình bày

---

## 1. Cách đọc paper khoa học — Thứ tự hiệu quả

```
  THỨ TỰ ĐỌC (khuyến nghị cho sinh viên):
  
  ┌──────────────────────────────────────────────────────────────────┐
  │ Bước 1: ABSTRACT                                               │
  │ → Tóm tắt TOÀN BỘ bài báo trong 1 đoạn                       │
  │ → Đọc trong 2 phút, nắm: bài toán, phương pháp, kết quả chính │
  ├──────────────────────────────────────────────────────────────────┤
  │ Bước 2: INTRODUCTION (Section I)                               │
  │ → Khoảng trống nghiên cứu (research gaps)                     │
  │ → 5 contributions                                             │
  │ → Hiểu WHY (tại sao làm nghiên cứu này)                       │
  ├──────────────────────────────────────────────────────────────────┤
  │ Bước 3: RESULTS (Section IV)                                   │
  │ → BẢNG kết quả (Table VI, VIII, IX, XII)                     │
  │ → FIGURES (feature importance, MAE comparison)                │
  │ → Hiểu WHAT (kết quả chính là gì)                            │
  ├──────────────────────────────────────────────────────────────────┤
  │ Bước 4: LIMITATIONS (Section V)                                │
  │ → ★ PHẦN QUAN TRỌNG NHẤT để học                              │
  │ → Tác giả tự nhận thiếu sót gì?                               │
  │ → Validation roadmap                                           │
  ├──────────────────────────────────────────────────────────────────┤
  │ Bước 5: CONCLUSION (Section VI)                                │
  │ → Tổng kết đóng góp                                           │
  │ → Future work                                                  │
  ├──────────────────────────────────────────────────────────────────┤
  │ Bước 6: METHODS (Section III)                                  │
  │ → Chi tiết kỹ thuật (đọc KHI CẦN)                             │
  │ → Feature engineering, model setup, evaluation protocol        │
  ├──────────────────────────────────────────────────────────────────┤
  │ Bước 7: RELATED WORK (Section II)                              │
  │ → Bối cảnh học thuật                                           │
  │ → Paper nào liên quan, khác gì?                               │
  └──────────────────────────────────────────────────────────────────┘
```

---

## 2. So sánh 2 phiên bản Paper

Paper có 2 phiên bản trong repo:
- **Paper gốc** (`paper_quang_ha_water_level_forecasting.md`): viết lần đầu, đầy đủ
- **Paper VNICT2026** (`VNICT2026_paper_6546.txt`): bản nộp hội nghị, 6 trang

### Bảng so sánh chi tiết

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Khía cạnh          │ Paper gốc (submitted)     │ Paper revised (VNICT2026) │
├─────────────────────┼───────────────────────────┼───────────────────────────┤
│ TIÊU ĐỀ            │ "Multi-step WL Forecasting│ "Feature-Engineering-     │
│                     │ Using Ensemble ML and     │  Driven ML as Surrogate   │
│                     │ Interpretable Feature     │  of Hydrodynamic Sim."    │
│                     │ Analysis"                 │                           │
│                     │ → Dẫn đầu bằng "Ensemble"│ → Dẫn đầu bằng "Feature  │
│                     │                           │   Engineering" + "Surrogate│
├─────────────────────┼───────────────────────────┼───────────────────────────┤
│ FRAMING             │ ML là "forecasting model" │ ML là "surrogate" của     │
│                     │                           │ MIKE11 simulator          │
│                     │ → Có thể hiểu nhầm là    │ → Trung thực về scope     │
│                     │   dự báo thực địa         │                           │
├─────────────────────┼───────────────────────────┼───────────────────────────┤
│ R² REPORTING        │ R² > 0.998 (đơn lẻ)     │ R² dải: 0.9984–0.9996   │
│                     │                           │ + caveat về simulation     │
├─────────────────────┼───────────────────────────┼───────────────────────────┤
│ NOISE EXPERIMENT    │ ★ KHÔNG CÓ               │ ★ Section IV-G, Table IV │
│                     │                           │   (mới thêm!)             │
│                     │                           │   2 scenarios, 3 seeds    │
├─────────────────────┼───────────────────────────┼───────────────────────────┤
│ RISK-ZONE TABLE     │ Chỉ accuracy              │ + Wilson CI, precision,   │
│                     │                           │ recall, F1, per-zone MAE, │
│                     │                           │ sample counts              │
├─────────────────────┼───────────────────────────┼───────────────────────────┤
│ NAIVE BASELINES     │ ★ BUG: data leakage      │ ĐÃ SỬA: leak-free        │
│                     │ (shift target column)     │ (lookup by date)           │
│                     │ MAE sai lệch              │ MAE: 0.212–1.292 m       │
├─────────────────────┼───────────────────────────┼───────────────────────────┤
│ STATISTICAL TEST    │ "RF vs XGB significant    │ "RF vs XGB NOT significant│
│                     │  at t+1" (p < 0.05)      │  at t+1" (p = 0.31)      │
├─────────────────────┼───────────────────────────┼───────────────────────────┤
│ 19.4% vs 19.1%     │ 19.4% (4 lần)            │ 19.1% (đã sửa từ file)   │
├─────────────────────┼───────────────────────────┼───────────────────────────┤
│ MODEL TABLES        │ 2 bảng riêng              │ Gộp thành 1 Table I      │
│                     │                           │ → tiết kiệm chỗ cho      │
│                     │                           │   noise experiment        │
├─────────────────────┼───────────────────────────┼───────────────────────────┤
│ FEATURE ABLATION    │ Có figure                 │ Bỏ figure, báo cáo số    │
│ FIGURE              │                           │ trong text                │
├─────────────────────┼───────────────────────────┼───────────────────────────┤
│ REFERENCES          │ [6] sai paper             │ ĐÃ SỬA: đúng paper       │
│                     │ [8] sai tên tác giả      │ ĐÃ SỬA: đúng tên (Xiong) │
├─────────────────────┼───────────────────────────┼───────────────────────────┤
│ FORMAT              │ > 6 trang                 │ = 6 trang (đúng IEEE)    │
│                     │                           │ Không đổi font/margin     │
└─────────────────────┴───────────────────────────┴───────────────────────────┘
```

---

## 3. Đọc thư trả lời Reviewer — Học cách phản biện

Thư trả lời (`THU_TRA_LOI_REVIEWER.md`) là tài liệu **CỰC KỲ GIÁ TRỊ** cho sinh viên. Đây là ví dụ thực tế về:

### Quy trình peer review khoa học

```
  ┌──────────────────────────────────────────────────────────────────┐
  │          QUY TRÌNH PHẢN BIỆN KHOA HỌC                          │
  │                                                                  │
  │  Bước 1: Nộp paper                                              │
  │     │                                                            │
  │  Bước 2: Reviewer đọc → nhận xét (2 reviewers, weak accept)    │
  │     │                                                            │
  │  Bước 3: Tác giả ĐỌC KỸ → ĐỒNG Ý với reviewer                 │
  │     │    KHÔNG bào chữa!                                         │
  │     │                                                            │
  │  Bước 4: CẢI THIỆN paper (không chỉ sửa lời)                   │
  │     │    → Thêm experiment mới (noise experiment)                │
  │     │    → Rebuild risk-zone evaluation                          │
  │     │    → Sửa bug baseline                                      │
  │     │    → Đổi tiêu đề                                           │
  │     │                                                            │
  │  Bước 5: Trả lời chi tiết MỖI comment                          │
  │     │    → Đồng ý ở đâu                                          │
  │     │    → Sửa thế nào                                            │
  │     │    → Thêm gì                                                │
  │     │                                                            │
  │  Bước 6: Đối chiếu TẤT CẢ số liệu (126 claims!)               │
  │     │    → 106 khớp ngay                                          │
  │     │    → 20 lỗi đã sửa                                         │
  │     │    → 2 tồn nhỏ                                             │
  │     │                                                            │
  │  Bước 7: Nộp bản sửa                                            │
  └──────────────────────────────────────────────────────────────────┘
```

### Phân tích từng Comment

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Comment 1: Walk-forward validation hợp lý                                  │
│ Reviewer: "Temporal split và walk-forward reasonably designed"             │
│ Tác giả: "Cảm ơn, NHƯNG phải nói rõ: chỉ 1 năm (2020), chỉ Stacking,    │
│           retrain 4 tuần, trailing h rows bị bỏ"                          │
│ → Bài học: Khi reviewer khen → vẫn phải nêu rõ scope/limitations          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Comment 2: Tất cả dữ liệu là MIKE11 → surrogate                          │
│ Reviewer: "ML model mainly approximates simulator, not field forecasting" │
│ Tác giả: "ĐỒNG Ý HOÀN TOÀN" → thay đổi framing TOÀN BỘ paper            │
│ → Abstract, Intro, Discussion, Limitations đều có surrogate framing       │
│ → Bài học: KHÔNG bào chữa khi reviewer đúng. Cải thiện paper thực sự.    │
├─────────────────────────────────────────────────────────────────────────────┤
│ Comment 3: R² > 0.998 cần giải thích                                      │
│ Reviewer: "Centimeter-level MAE need cautious interpretation"             │
│ Tác giả: "ĐỒNG Ý" → thêm Section IV-G (noise experiment)                 │
│ → Thêm Gaussian noise σ = 1, 2, 5 cm                                     │
│ → 2 scenarios: S1 (clean→noisy), S2 (noisy→noisy)                        │
│ → Kết luận: "MAE centimet-level là tính chất của dữ liệu sạch"          │
│ → Bài học: Thêm experiment định lượng thay vì chỉ qualitative caveat      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Comment 4: Imbalance (684/29/9)                                            │
│ Reviewer: "High accuracy rests on imbalanced test set"                    │
│ Tác giả: Rebuild Table II → thêm Wilson CI, precision/recall/F1          │
│ → Tách 2 cách đọc: thuận lợi và không thuận lợi                         │
│ → Báo bias âm ở Exceedance (under-predict → KHÔNG an toàn)              │
│ → Bài học: Imbalance phải được nêu rõ, không giấu                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Comment 5: Feature engineering là đóng góp chính, không phải ensemble     │
│ Reviewer: "Linear Regression best at t+1, t+3 → framing should change"   │
│ Tác giả: ĐỔI TIÊU ĐỀ paper! "Ensemble ML" → "Feature-Engineering-Driven"│
│ → Thêm Contribution 5 vào Introduction                                    │
│ → Báo Wilcoxon: RF vs XGB KHÔNG significant ở t+1 (p=0.31)             │
│ → Bài học: Tiêu đề phải phản ánh đúng đóng góp                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Comment 6: Cần validate với dữ liệu thực                                  │
│ Reviewer: "Validation against real stations needed"                       │
│ Tác giả: "KHÔNG THỂ thêm trong revision" → thêm roadmap 3 bước          │
│ → 1. Lấy dữ liệu đo từ MIKE11 calibration record                       │
│ → 2. Định lượng MIKE11-vs-observation error                              │
│ → 3. Mở rộng nhiều trạm + compound events                               │
│ → Bài học: Trung thực khi chưa làm được, nhưng đề xuất roadmap cụ thể   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Comment 7: Các sửa lỗi tự phát hiện (10 lỗi!)                            │
│ → Bug nghiêm trọng nhất: Naive baseline data leakage                     │
│ → 19.4% → 19.1% (4 lần trong paper)                                    │
│ → SHAP contradiction (text ≠ figure)                                     │
│ → Threshold: P95/P99 trên 28 năm (không phải 31 năm)                     │
│ → Bài học: Đối chiếu CHÍNH XÁC mọi số trước khi nộp                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Bài học về Scientific Writing

```
┌──────────────────────────────────────────────────────────────────────┐
│ BÀI HỌC #1: FRAMING QUAN TRỌNG HƠN BẠN NGHĨ                       │
│                                                                      │
│ Tiêu đề cũ: "Ensemble ML" → bị reviewer phản bác                    │
│ → vì LR tốt hơn ở t+1, t+3 → ensemble KHÔNG phải đóng góp chính   │
│                                                                      │
│ Tiêu đề mới: "Feature-Engineering-Driven ML as Surrogate"            │
│ → phản ánh ĐÚNG: FE là chính, surrogate framing là trung thực       │
│                                                                      │
│ → Khi viết paper: tiêu đề phải match với KẾT QUẢ                    │
├──────────────────────────────────────────────────────────────────────┤
│ BÀI HỌC #2: THỪA NHẬN GIỚI HẠN MẠNH HƠN BÀO CHỮA                 │
│                                                                      │
│ Paper gốc: "R² > 0.998" (ấn tượng nhưng thiếu bối cảnh)            │
│ Paper sửa: "R² cao do simulation smoothness, cần field validation"  │
│                                                                      │
│ → Thừa nhận giới hạn → reviewer tin tưởng hơn                       │
│ → Thêm experiment định lượng (noise) thay vì chỉ caveat chữ        │
├──────────────────────────────────────────────────────────────────────┤
│ BÀI HỌC #3: DATA LEAKAGE RẤT DỄ XẢY RA                             │
│                                                                      │
│ Naive baseline trong bản gốc: target.shift(lag)                     │
│ → Khi h > lag → dùng giá trị TƯƠNG LAI!                           │
│ → Bug này tồn tại qua nhiều lần review                             │
│                                                                      │
│ → Luôn kiểm tra: mỗi prediction chỉ dùng thông tin QUÁ KHỨ         │
├──────────────────────────────────────────────────────────────────────┤
│ BÀI HỌC #4: SỐ LIỆU PHẢI CHÍNH XÁC                                 │
│                                                                      │
│ 19.4% xuất hiện 4 lần → đúng là 19.1%                              │
│ "Significant at t+1" → p = 0.31 → KHÔNG significant                │
│ Threshold "31-year" → đúng là "28-year"                             │
│                                                                      │
│ → Đối chiếu MỌI con số từ file kết quả gốc                        │
│ → Không copy-paste số từ draft cũ                                   │
├──────────────────────────────────────────────────────────────────────┤
│ BÀI HỌC #5: IMBALANCE PHẢI ĐƯỢC NÔI RÕ                             │
│                                                                      │
│ Accuracy 99.5% NGHE ấn tượng nhưng:                                 │
│ → 9/722 ngày Exceedance → Wilson CI [0.35, 0.88]                   │
│ → KHÔNG đủ bằng chứng                                               │
│                                                                      │
│ → Luôn báo sample counts + confidence interval cho minority class   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 5. Checklist đọc paper cho sinh viên

```
┌──────────────────────────────────────────────────────────────────────┐
│ Paper gốc:                                                         │
│ □ Đọc abstract + introduction                                      │
│ □ Đọc Section IV (Results) — hiểu TẤT CẢ bảng                     │
│ □ Đọc Section V (Limitations)                                      │
│ □ Đọc Section VI (Conclusion)                                      │
│                                                                      │
│ Paper VNICT2026 (6 trang):                                         │
│ □ So sánh tiêu đề                                                  │
│ □ Tìm surrogate framing                                            │
│ □ Tìm noise experiment (Section IV-G)                              │
│ □ Tìm Wilson CI trong risk-zone table                              │
│                                                                      │
│ Thư trả lời Reviewer:                                              │
│ □ Đọc TOÀN BỘ (7 comments)                                        │
│ □ Ghi lại: 3 điều reviewer đúng mà tác giả đồng ý                │
│ □ Ghi lại: bug baseline data leakage (Comment 7)                   │
│ □ Ghi lại: 19.4% → 19.1% (sai số số liệu)                       │
│                                                                      │
│ Viết 1 trang tóm tắt:                                              │
│ □ Bài học về scientific writing                                     │
│ □ Cách trả lời reviewer                                            │
│ □ Tại sao framing quan trọng                                       │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 6. Script nói khi có người hỏi sâu

```
┌──────────────────────────────────────────────────────────────────────┐
│ Q: "Paper này có novelty gì?"                                       │
│ A: "Feature engineering là novelty chính. 5 nhóm feature thủy học   │
│    làm cho short-horizon gần như tuyến tính. AdaptiveStack cải thiện│
│    19.1% MAE ở t+7. Nhưng quan trọng nhất: paper thừa nhận        │
│    surrogate framing và thêm noise experiment."                      │
├──────────────────────────────────────────────────────────────────────┤
│ Q: "Tại sao đổi tiêu đề?"                                         │
│ A: "Tiêu đề cũ dẫn đầu bằng 'Ensemble ML' nhưng kết quả cho thấy  │
│    Linear Regression tốt hơn ensemble ở t+1, t+3. Feature eng.     │
│    mới là đóng góp chính. Reviewer cũng chỉ ra điều này."          │
├──────────────────────────────────────────────────────────────────────┤
│ Q: "Sao không dùng SHAP?"                                          │
│ A: "Paper dùng tree-based importance (MDI, total gain) vì nhanh     │
│    và globally consistent. SHAP instance-level là future work.      │
│    Note: paper gốc có inconsistency giữa text và SHAP figure →     │
│    đã sửa trong bản revised."                                       │
├──────────────────────────────────────────────────────────────────────┤
│ Q: "Data từ simulator có tin được không?"                           │
│ A: "Đây là surrogate model — học mối quan hệ CỦA simulator.       │
│    Chưa validated với data thực. Noise experiment đo lường          │
│    bao nhiêu % accuracy survive contact với measurement error.     │
│    Roadmap 3 bước cho field validation."                            │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Tài liệu tham khảo trong Paper

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ #   │ Tác giả chính │ Năm  │ Nội dung chính                               │
├─────┼────────────────┼──────┼───────────────────────────────────────────────┤
│ [1] │ Mosavi         │ 2018 │ Review: ML flood prediction (ANN, SVM, RF)  │
│ [2] │ Mahmud         │ 2018 │ ANN weekly water level (Malaysia)            │
│ [3] │ Breiman        │ 2001 │ ★ Random Forests (gốc)                      │
│ [4] │ Chen & Guestrin│ 2016 │ ★ XGBoost (gốc)                             │
│ [5] │ Lundberg & Lee │ 2017 │ ★ SHAP (gốc)                                │
│ [6] │ Le et al.      │ 2021 │ Multi-step WL at tidal sluice gates (VN)    │
│ [7] │ Li et al.      │ 2023 │ XGBoost + SHAP reservoir releases           │
│ [8] │ Xiong et al.   │ 2026 │ Storm surge Pearl River Estuary             │
│ [9] │ Ke et al.      │ 2017 │ ★ LightGBM (gốc)                           │
│ [10]│ Geurts et al.  │ 2006 │ ★ Extremely Randomized Trees (gốc)          │
│ [11]│ Pedregosa et al│ 2011 │ ★ scikit-learn (gốc)                        │
└─────┴────────────────┴──────┴───────────────────────────────────────────────┘
```
