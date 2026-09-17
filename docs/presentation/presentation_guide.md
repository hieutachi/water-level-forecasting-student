# Hướng dẫn trình bày trước hội nghị (10–12 phút)

## Phân bổ thời gian

| Phần | Thời gian | Nội dung |
|------|----------|----------|
| Mở đầu | 1 phút | Tiêu đề, tác giả, affiliation |
| Background & Problem | 1.5 phút | Vùng cửa sông, bài toán multi-step |
| Data & Framing | 1 phút | Dữ liệu MIKE11, surrogate framing |
| Pipeline | 1 phút | Tổng quan 4 bước |
| Feature Engineering | 2 phút | 5 nhóm feature, tại sao quan trọng |
| Main Results | 2 phút | Linear Regression thắng ở t+1/t+3 |
| AdaptiveStack t+7 | 1 phút | Ensemble có lợi ở horizon dài |
| Risk-zone & Limitations | 1.5 phút | Accuracy, imbalance, Wilson CI |
| Conclusion | 1 phút | Bài học chính |

## Các điểm nhấn cần nói rõ

### 1. Surrogate Framing (Rất quan trọng!)
> "Tất cả dữ liệu là output mô phỏng MIKE11. Mô hình ML là surrogate — phần thay thế nhanh cho trình mô phỏng, KHÔNG phải hệ thống dự báo thực địa đã validated."

### 2. Feature Engineering > Model Complexity
> "Linear Regression đạt MAE thấp nhất ở t+1 và t+3. Đầu tư vào feature engineering tốt hơn tìm model phức tạp."

### 3. R² cao cần bối cảnh
> "R² > 0.998 phản ánh tính 'dễ dự báo' của dữ liệu mô phỏng. MAPE walk-forward (3.4%–7.2%) phản ánh thực tế hơn."

### 4. Imbalance trong Risk-zone
> "Chỉ có 9 ngày Exceedance trong 722 ngày test. Wilson CI [0.35, 0.88] quá rộng để đưa ra kết luận mạnh."

## Cách trả lời câu hỏi thường gặp

### "Sao R² cao vậy?"
> "Vì dữ liệu là output mô phỏng MIKE11 — tuân theo phương trình vật lý xác định, mượt hơn dữ liệu đo thực. Khi thêm noise 1cm vào input, MAE tăng 40%. R² cao là tính chất của dữ liệu, không phải của mô hình."

### "Model này áp dụng trực tiếp ngoài thực tế được không?"
> "Chưa. Cần validate với dữ liệu đo thực tại trạm. Paper hiện tại cho thấy pipeline reproduces behavior của simulator accurately. Roadmap 3 bước: (1) lấy dữ liệu đo từ MIKE11 calibration record, (2) tách lỗi mô phỏng và lỗi mô hình, (3) mở rộng nhiều trạm."

### "Tại sao Linear Regression tốt hơn ensemble?"
> "Feature engineering đã 'linearize' bài toán ở short horizon. Mối quan hệ giữa feature và target gần như tuyến tính ở t+1 và t+3. Ensemble chỉ có lợi ở t+7 khi mối quan hệ phi tuyến tính mạnh hơn."

### "9 ngày Exceedance có đủ không?"
> "Không đủ cho kết luận mạnh. Wilson 95% CI cho Exceedance recall là [0.35, 0.88] — quá rộng. Tuy nhiên, điểm tích cực: không có ngày Exceedance nào bị phân loại nhầm thành Normal (tất cả downgrade xuống Warning). Cần thêm dữ liệu extreme events."

### "Noise experiment cho thấy gì?"
> "Khi thêm Gaussian noise σ = 1cm vào input, MAE Stacking tăng 40% (t+1). Ở t+3 với noise 2cm, ranking mô hình đổi: XGBoost vượt qua Linear Regression. Điều này cho thấy độ chính xác centimet-level và lợi thế linear model là tính chất của dữ liệu sạch."

## Liên hệ với paper và thư trả lời

Khi có người hỏi sâu:
- "Chi tiết hơn mời đọc Section IV-G trong paper về noise experiment"
- "Phân tích feature ablation chi tiết ở Section IV-D"
- "Thư trả lời reviewer giải thích chi tiết các sửa đổi"
- "Phân tích SHAP instance-level là future work"

## Mẹo trình bày

1. **Bắt đầu bằng bức tranh lớn** — bài toán, tại sao quan trọng
2. **Nói surrogate framing NGAY từ đầu** — tránh hiểu lầm
3. **Dùng bảng so sánh** để minh họa Linear > Ensemble ở t+1/t+3
4. **Nhấn mạnh bài học** — feature engineering, temporal split, honest framing
5. **Kết thúc bằng takeaway** cho sinh viên
6. **Nói chậm ở phần Limitations** — đây là phần quan trọng nhất
