# MyGym Retention Analytics

## Tổng quan dự án

Dự án này xây dựng hệ thống Business Intelligence kết hợp Machine Learning cho MyGym nhằm phân tích hành vi hội viên, theo dõi hiệu quả kinh doanh, dự đoán nguy cơ rời bỏ và hỗ trợ đưa ra các quyết định giữ chân khách hàng.

Hệ thống bao gồm dashboard Power BI, mô hình dữ liệu Star Schema, mô hình Machine Learning dự đoán churn, phân tích nguy cơ rời bỏ, Explainable AI và phân khúc khách hàng.

## Bài toán kinh doanh

MyGym muốn cải thiện khả năng giữ chân hội viên bằng cách phân tích hành vi sử dụng dịch vụ và xác định những hội viên có nguy cơ ngừng sử dụng phòng gym.

Dự án tập trung vào các mục tiêu chính:

* Phân tích hành vi và mức độ gắn kết của hội viên.
* Theo dõi tỷ lệ rời bỏ và tỷ lệ giữ chân hội viên.
* Đánh giá hiệu quả các gói hội viên.
* Đánh giá hiệu quả hoạt động theo chi nhánh.
* Dự đoán nguy cơ rời bỏ bằng Machine Learning.
* Xác định nhóm hội viên có rủi ro cao để đưa ra hành động giữ chân phù hợp.
* Phân khúc khách hàng để hỗ trợ chiến lược chăm sóc và marketing.

## Dữ liệu sử dụng

Dự án sử dụng tập dữ liệu:

* `Fitness_Membership_Analytics.csv`

Bộ dữ liệu bao gồm các thông tin về hội viên phòng gym như loại gói hội viên, mô hình đăng ký, tần suất đi tập, thời lượng tập, tham gia lớp nhóm, sử dụng huấn luyện viên cá nhân, sử dụng sauna, đăng ký nước uống, giảm giá, chi nhánh, ngày tham gia, ngày sử dụng gần nhất và thông tin giá tiền.

## Phân chia nội dung theo mức

## Mức 1 - Business Intelligence

Mức 1 tập trung vào tiền xử lý dữ liệu, thiết kế mô hình dữ liệu Star Schema, xây dựng KPI và trực quan hóa dữ liệu bằng Power BI.

### Công việc chính

* Làm sạch và tiền xử lý dữ liệu.
* Xử lý dữ liệu thiếu.
* Chuẩn hóa dữ liệu.
* Feature Engineering.
* Exploratory Data Analysis.
* Thiết kế Star Schema.
* Xây dựng các chỉ số KPI.
* Thiết kế dashboard trên Power BI.

### Các trang Power BI thuộc Mức 1

* Overview
* Churn & Retention
* Engagement Analytics
* Membership Performance
* Branch Performance

### Các KPI chính

* Tổng số hội viên
* Số hội viên rời bỏ
* Số hội viên được giữ chân
* Tỷ lệ Churn
* Tỷ lệ Retention
* Tần suất đi tập trung bình
* Thời lượng tập trung bình
* Thời gian gắn bó trung bình
* Điểm gắn kết hội viên
* Tổng doanh thu
* ARPU

### Mô hình Star Schema

Dữ liệu được thiết kế theo mô hình Star Schema để tối ưu cho quá trình phân tích và trực quan hóa.

Bảng Fact:

* `fact_membership_activity.csv`

Các bảng Dimension:

* `dim_member.csv`
* `dim_membership.csv`
* `dim_discount.csv`
* `dim_location.csv`
* `dim_date.csv`

Bảng Fact lưu trữ các chỉ số hoạt động của hội viên như tần suất đi tập, thời lượng tập, doanh thu, điểm gắn kết, thời gian gắn bó và trạng thái churn. Các bảng Dimension hỗ trợ phân tích theo hội viên, loại gói tập, chính sách giảm giá, chi nhánh và thời gian.

## Mức 2 - Machine Learning

Mức 2 tập trung vào xây dựng mô hình Machine Learning để dự đoán khả năng hội viên rời bỏ.

Pipeline Machine Learning được triển khai trong file:

* `mygym_project_pipeline.py`

Kết quả đánh giá mô hình được lưu trong file:

* `model_metrics.csv`

Kết quả được trực quan hóa trong trang Power BI:

* Machine Learning Results

### Biến mục tiêu

Biến mục tiêu của bài toán là:

* `churn`

Trong dự án này, hội viên được xem là churn nếu không quay lại phòng gym trong hơn 30 ngày, dựa trên quy tắc nghiệp vụ được xây dựng từ dữ liệu.

### Các mô hình sử dụng

Dự án triển khai các mô hình Machine Learning sau:

* Logistic Regression
* Decision Tree
* Random Forest

### Các chỉ số đánh giá mô hình

Các mô hình được đánh giá bằng các chỉ số:

* Accuracy
* Precision
* Recall
* F1-score
* ROC-AUC

### Quy trình Machine Learning

Quy trình thực hiện gồm:

1. Đọc dữ liệu gốc.
2. Làm sạch và tiền xử lý dữ liệu.
3. Tạo biến mục tiêu churn.
4. Chọn các đặc trưng đầu vào.
5. Mã hóa dữ liệu phân loại.
6. Chuẩn hóa dữ liệu số.
7. Chia dữ liệu thành tập train và test.
8. Huấn luyện các mô hình Machine Learning.
9. Đánh giá hiệu quả mô hình.
10. Xuất kết quả ra file `model_metrics.csv`.
11. Trực quan hóa kết quả trong Power BI.

## Mức 3 - Retention Analytics và Explainable AI

Mức 3 tập trung vào phân tích giữ chân khách hàng nâng cao, tính điểm rủi ro churn, phát hiện hội viên cần cảnh báo sớm, giải thích mô hình bằng Feature Importance và phân khúc khách hàng.

Pipeline Mức 3 được triển khai trong file:

* `mygym_level3_retention_ai.py`

### Các trang Power BI thuộc Mức 3

* Retention Risk Analysis
* Customer Segmentation

### Kết quả chính

* Churn Risk Score
* Early-warning Members
* Recommended Retention Actions
* Feature Importance
* Customer Segmentation

### Các file kết quả

* `retention_risk_scores.csv`
* `early_warning_members.csv`
* `explainable_ai_feature_importance.csv`
* `customer_segments.csv`
* `customer_segment_summary.csv`

### Phân tích nguy cơ rời bỏ

Phần Retention Risk Analysis giúp xác định những hội viên có nguy cơ rời bỏ cao. Hệ thống tính điểm rủi ro churn cho từng hội viên và phân loại hội viên theo các nhóm rủi ro.

Danh sách hội viên cảnh báo sớm được sử dụng để hỗ trợ MyGym đưa ra các hành động giữ chân khách hàng kịp thời.

### Explainable AI

Dự án sử dụng Feature Importance để giải thích các yếu tố ảnh hưởng mạnh đến dự đoán churn.

Một số yếu tố có thể ảnh hưởng đến churn gồm:

* Số ngày kể từ lần sử dụng gần nhất
* Tần suất đi tập
* Thời lượng tập
* Thời gian gắn bó
* Điểm gắn kết
* Sử dụng huấn luyện viên cá nhân
* Loại giảm giá
* Loại gói hội viên

### Phân khúc khách hàng

Phân khúc khách hàng được sử dụng để chia hội viên thành các nhóm khác nhau dựa trên hành vi, mức độ gắn kết, doanh thu và nguy cơ rời bỏ.

Kết quả phân khúc giúp MyGym xây dựng chiến lược chăm sóc, marketing và giữ chân khách hàng phù hợp với từng nhóm hội viên.

## Các file chính trong dự án

| File                                    | Mô tả                                                                               |
| --------------------------------------- | ----------------------------------------------------------------------------------- |
| `FullProjectDe10.pbix`                  | File dashboard Power BI trình bày kết quả Mức 1, Mức 2 và Mức 3                     |
| `Fitness_Membership_Analytics.csv`      | Dữ liệu gốc của hội viên MyGym                                                      |
| `mygym_project_pipeline.py`             | Code Mức 2 dùng để huấn luyện mô hình dự đoán churn                                 |
| `model_metrics.csv`                     | Kết quả đánh giá các mô hình Machine Learning                                       |
| `mygym_level3_retention_ai.py`          | Code Mức 3 dùng để tạo churn risk score, feature importance và phân khúc khách hàng |
| `retention_risk_scores.csv`             | Điểm rủi ro churn của từng hội viên                                                 |
| `early_warning_members.csv`             | Danh sách hội viên có nguy cơ cao và hành động giữ chân đề xuất                     |
| `explainable_ai_feature_importance.csv` | Kết quả Feature Importance để giải thích mô hình                                    |
| `customer_segments.csv`                 | Kết quả phân khúc của từng hội viên                                                 |
| `customer_segment_summary.csv`          | Bảng tổng hợp các phân khúc khách hàng                                              |
| `fact_membership_activity.csv`          | Bảng Fact trong mô hình Star Schema                                                 |
| `dim_member.csv`                        | Bảng Dimension về hội viên                                                          |
| `dim_membership.csv`                    | Bảng Dimension về gói hội viên                                                      |
| `dim_discount.csv`                      | Bảng Dimension về giảm giá                                                          |
| `dim_location.csv`                      | Bảng Dimension về chi nhánh                                                         |
| `dim_date.csv`                          | Bảng Dimension về thời gian                                                         |
| `requirements.txt`                      | Danh sách thư viện Python cần cài đặt                                               |

## Các trang trong Power BI

File Power BI gồm các trang:

1. Overview
2. Churn & Retention
3. Engagement Analytics
4. Membership Performance
5. Branch Performance
6. Machine Learning Results
7. Retention Risk Analysis
8. Customer Segmentation

## Cách chạy code Python

### 1. Cài đặt thư viện cần thiết

```bash
pip install -r requirements.txt
```

### 2. Chạy pipeline Machine Learning Mức 2

```bash
python mygym_project_pipeline.py
```

Sau khi chạy, chương trình tạo ra file:

* `model_metrics.csv`

### 3. Chạy pipeline Retention Analytics Mức 3

```bash
python mygym_level3_retention_ai.py
```

Sau khi chạy, chương trình tạo ra các file:

* `retention_risk_scores.csv`
* `early_warning_members.csv`
* `explainable_ai_feature_importance.csv`
* `customer_segments.csv`
* `customer_segment_summary.csv`

## Cách xem dashboard

Mở file sau bằng Power BI Desktop:

* `FullProjectDe10.pbix`

Dashboard Power BI trình bày toàn bộ kết quả của dự án từ Mức 1 đến Mức 3.

## Kết luận

Dự án cung cấp một giải pháp phân tích dữ liệu hoàn chỉnh cho MyGym, kết hợp Business Intelligence, Machine Learning, Retention Analytics, Explainable AI và Customer Segmentation. Hệ thống giúp doanh nghiệp theo dõi hiệu quả hoạt động, dự đoán nguy cơ rời bỏ hội viên và đề xuất các chiến lược giữ chân khách hàng phù hợp.
