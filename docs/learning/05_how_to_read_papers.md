# 05 — Hướng dẫn đọc paper và thư trả lời

## Cách đọc paper khoa học

### Thứ tự đọc hiệu quả

1. **Abstract** → Tóm tắt toàn bộ bài báo trong 1 đoạn
2. **Introduction** → Bài toán, khoảng trống nghiên cứu, đóng góp
3. **Results** (Section IV) → Kết quả chính, bảng, figure
4. **Limitations** (Section V) → Tác giả tự nhận thiếu sót gì
5. **Conclusion** → Tổng kết đóng góp
6. **Methods** (Section III) → Chi tiết kỹ thuật (đọc khi cần)
7. **Related Work** → Bối cảnh học thuật

### Đọc 2 paper và so sánh

Paper trong repo có 2 phiên bản:
1. **Paper gốc** (`paper_quang_ha_water_level_forecasting.pdf`): bản đầy đủ, viết lần đầu
2. **Paper VNICT2026** (`VNICT2026_paper_6546.pdf`): bản đã nộp hội nghị (6 trang)

**So sánh để học:**

| Khía cạnh | Paper gốc | Paper VNICT2026 (revised) |
|-----------|----------|--------------------------|
| Tiêu đề | Dẫn đầu bằng "Ensemble ML" | Dẫn đầu bằng "Feature Engineering" |
| Framing | ML là mô hình dự báo | ML là surrogate của MIKE11 |
| R² | Báo cáo đơn lẻ | Báo cáo dải (0.9984–0.9996) |
| Risk-zone | Accuracy cao | Thêm Wilson CI + cảnh báo imbalance |
| Naive baseline | Có bug data leakage | Đã sửa |

## Đọc thư trả lời Reviewer

Thư trả lời (`THU_TRA_LOI_REVIEWER.md`) là tài liệu **rất giá trị** cho sinh viên, vì nó cho thấy:

### Quy trình phản biện khoa học

1. **Reviewer nêu vấn đề** → tất cả dữ liệu là MIKE11, R² quá cao, imbalance
2. **Tác giả đồng ý** và cải thiện paper (không bào chữa!)
3. **Thêm experiment mới** (noise experiment) để trả lời trực tiếp
4. **Sửa số liệu** cẩn thận (đối chiếu 126 claims)

### Các bài học rút ra

**Bài học 1: Framing quan trọng**
- Tiêu đề cũ: "Ensemble ML" → bị reviewer phản bác (vì LR tốt hơn ở t+1, t+3)
- Tiêu đề mới: "Feature Engineering" → phản ánh đúng đóng góp

**Bài học 2: Thừa nhận giới hạn**
- Paper gốc: "R² > 0.998" (ấn tượng nhưng thiếu bối cảnh)
- Paper sửa: "R² rất cao do dữ liệu mô phỏng trơn" (trung thực)

**Bài học 3: Data leakage rất dễ xảy ra**
- Naive baseline trong bản gốc có bug: dùng giá trị tương lai
- Phải cẩn thận khi xây dựng baseline

**Bài học 4: Thống kê cần chính xác**
- Ban đầu claim "significance at t+1" nhưng Wilcoxon test không hỗ trợ
- Phải sửa lại: RF và XGBoost KHÔNG phân biệt được ở t+1 (p = 0.31)

**Bài học 5: Imbalance cần được nêu rõ**
- 9/722 ngày Exceedance → Wilson CI [0.35, 0.88]
- Không thể claim "high accuracy" dựa trên 9 mẫu

### Các câu hỏi thường gặp khi bảo vệ

**Q: "Sao R² cao vậy?"**
A: "Vì dữ liệu là output mô phỏng MIKE11, trơn hơn dữ liệu đo thực. MAPE walk-forward (3.4%–7.2%) phản ánh thực tế hơn."

**Q: "Model áp dụng trực tiếp ngoài thực tế được không?"**
A: "Chưa thể. Cần validate với dữ liệu đo thực tại trạm. Paper hiện tại là surrogate của simulator."

**Q: "Tại sao Linear Regression tốt hơn ensemble?"**
A: "Feature engineering làm cho mối quan hệ gần như tuyến tính ở short horizon. Ensemble chỉ có lợi ở t+7."

**Q: "9 ngày Exceedance có đủ không?"**
A: "Không đủ. Wilson CI [0.35, 0.88] quá rộng. Cần thêm dữ liệu extreme events."

## Checklist cho sinh viên

- [ ] Đọc abstract + introduction cả 2 paper
- [ ] So sánh tiêu đề 2 phiên bản
- [ ] Đọc Section IV (Results) và hiểu từng bảng
- [ ] Đọc Section V (Limitations) — phần quan trọng nhất!
- [ ] Đọc thư trả lời reviewer — học cách phản biện
- [ ] Viết 1 trang tóm tắt bài học về scientific writing
