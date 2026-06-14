# MyGym Retention Analytics & Churn Prediction

## Project Overview
This project builds a Business Intelligence and Machine Learning system for MyGym to analyze member engagement, monitor churn/retention, and predict members at risk of leaving.

## Level 1 - Business Intelligence
Power BI dashboards:
1. Overview
2. Churn & Retention
3. Engagement Analytics
4. Membership Performance
5. Branch Performance

## Level 2 - Machine Learning
Models:
- Logistic Regression
- Decision Tree
- Random Forest

Metrics:
- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

## Level 3 - Retention Analytics & Explainable AI
This repository includes:
- Churn Risk Score for each member
- Risk Level: Low, Medium, High, Critical
- Early-warning member list
- Recommended retention actions
- Feature importance for explainable AI
- Customer segmentation using K-Means

## Files
| File | Description |
|---|---|
| `mygym_level3_retention_ai.py` | Main Level 3 Python script |
| `retention_risk_scores.csv` | Churn risk score and recommendation for each member |
| `early_warning_members.csv` | High-risk and critical-risk members |
| `explainable_ai_feature_importance.csv` | Feature importance for model explainability |
| `customer_segments.csv` | Member-level customer segmentation |
| `customer_segment_summary.csv` | Segment-level summary |
| `requirements.txt` | Python dependencies |

## How to Run
```bash
pip install -r requirements.txt
python mygym_level3_retention_ai.py
```

## Business Recommendations
- High-risk members: early-warning call/SMS, personalized offers, win-back vouchers.
- Low-engagement members: visit reminders, free group lesson invitations.
- Members without PT usage: free trial PT session.
- Loyal members: loyalty program and membership upgrade offers.
