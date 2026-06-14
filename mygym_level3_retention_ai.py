import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans

# Run: python mygym_level3_retention_ai.py

df = pd.read_csv("Fitness_Membership_Analytics.csv")
df["join_date"] = pd.to_datetime(df["join_date"])
df["last_visit_date"] = pd.to_datetime(df["last_visit_date"])
df.insert(0, "member_id", [f"MB{str(i+1).zfill(5)}" for i in range(len(df))])
df["discount_type"] = df["discount_type"].fillna("No Discount")

reference_date = df["last_visit_date"].max() + pd.Timedelta(days=1)
df["membership_tenure_days"] = (reference_date - df["join_date"]).dt.days
df["days_since_last_visit"] = (reference_date - df["last_visit_date"]).dt.days
df["churn"] = (df["days_since_last_visit"] > 30).astype(int)
df["churn_label"] = np.where(df["churn"] == 1, "Churn", "Retained")

df["engagement_score"] = (
    (df["visit_per_week"] / df["visit_per_week"].max()) * 45
    + (df["duration_in_gym_minutes"] / df["duration_in_gym_minutes"].max()) * 25
    + df["attend_group_lesson"].astype(int) * 15
    + df["personal_training"].astype(int) * 10
    + df["uses_sauna"].astype(int) * 5
)

feature_cols = [
    "age", "membership_type", "visit_per_week", "attend_group_lesson",
    "duration_in_gym_minutes", "has_drink_subscription", "personal_training",
    "uses_sauna", "self_identified_gender", "subscription_price",
    "subscription_model", "discount_type", "discount_rate", "final_price",
    "access_hours", "home_gym_location", "personal_training_hours",
    "multi_location_access", "membership_tenure_days"
]

X = df[feature_cols].copy()
y = df["churn"].astype(int)
categorical_cols = X.select_dtypes(include=["object", "bool"]).columns.tolist()
numeric_cols = [c for c in X.columns if c not in categorical_cols]

preprocess = ColumnTransformer([
    ("num", StandardScaler(), numeric_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
])

model = Pipeline([
    ("preprocess", preprocess),
    ("model", RandomForestClassifier(n_estimators=250, max_depth=8, random_state=42, class_weight="balanced"))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
model.fit(X_train, y_train)

df["churn_risk_score"] = model.predict_proba(X)[:, 1] * 100
df["risk_level_ml"] = pd.cut(df["churn_risk_score"], bins=[-1, 30, 60, 80, 100],
                             labels=["Low Risk", "Medium Risk", "High Risk", "Critical Risk"])

def recommend_action(row):
    actions = []
    if str(row["risk_level_ml"]) in ["High Risk", "Critical Risk"]:
        actions.append("Early-warning call/SMS")
    if row["visit_per_week"] < 2:
        actions.append("Personalized visit reminder")
    if not bool(row["attend_group_lesson"]):
        actions.append("Invite to free group lesson")
    if not bool(row["personal_training"]):
        actions.append("Offer trial PT session")
    if row["days_since_last_visit"] > 30:
        actions.append("Win-back voucher")
    if row["engagement_score"] < 40:
        actions.append("Loyalty points boost")
    return "; ".join(actions[:3]) if actions else "Maintain standard membership care"

df["recommended_retention_action"] = df.apply(recommend_action, axis=1)

risk_cols = [
    "member_id", "churn", "churn_label", "churn_risk_score", "risk_level_ml",
    "recommended_retention_action", "membership_type", "subscription_model",
    "discount_type", "visit_per_week", "duration_in_gym_minutes",
    "membership_tenure_days", "days_since_last_visit", "engagement_score",
    "home_gym_location"
]
df[risk_cols].sort_values("churn_risk_score", ascending=False).to_csv("retention_risk_scores.csv", index=False, encoding="utf-8-sig")
df[df["risk_level_ml"].isin(["High Risk", "Critical Risk"])][risk_cols].to_csv("early_warning_members.csv", index=False, encoding="utf-8-sig")

ohe = model.named_steps["preprocess"].named_transformers_["cat"]
encoded_cat_names = list(ohe.get_feature_names_out(categorical_cols))
feature_names = numeric_cols + encoded_cat_names
feature_importance = pd.DataFrame({
    "feature": feature_names,
    "importance": model.named_steps["model"].feature_importances_
}).sort_values("importance", ascending=False)
feature_importance.to_csv("explainable_ai_feature_importance.csv", index=False, encoding="utf-8-sig")

seg_cols = ["visit_per_week", "duration_in_gym_minutes", "final_price", "membership_tenure_days", "engagement_score", "churn_risk_score"]
seg_scaled = StandardScaler().fit_transform(df[seg_cols].fillna(df[seg_cols].median(numeric_only=True)))
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df["customer_segment"] = kmeans.fit_predict(seg_scaled)

segment_summary = df.groupby("customer_segment").agg(
    members=("member_id", "count"),
    avg_churn_risk=("churn_risk_score", "mean"),
    avg_engagement=("engagement_score", "mean"),
    avg_visit_per_week=("visit_per_week", "mean"),
    avg_revenue=("final_price", "mean")
).reset_index()

df[["member_id", "customer_segment", "churn_risk_score", "engagement_score", "visit_per_week", "final_price", "membership_type", "home_gym_location"]].to_csv("customer_segments.csv", index=False, encoding="utf-8-sig")
segment_summary.to_csv("customer_segment_summary.csv", index=False, encoding="utf-8-sig")

print("Level 3 Retention Analytics files created.")
