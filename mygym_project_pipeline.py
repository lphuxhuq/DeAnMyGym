import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


def load_and_prepare(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["join_date"] = pd.to_datetime(df["join_date"])
    df["last_visit_date"] = pd.to_datetime(df["last_visit_date"])
    df.insert(0, "member_id", [f"MB{str(i+1).zfill(5)}" for i in range(len(df))])
    df["discount_type"] = df["discount_type"].fillna("No Discount")

    reference_date = df["last_visit_date"].max() + pd.Timedelta(days=1)
    df["reference_date"] = reference_date.date().isoformat()
    df["membership_tenure_days"] = (reference_date - df["join_date"]).dt.days
    df["days_since_last_visit"] = (reference_date - df["last_visit_date"]).dt.days

    # Business rule: no visit in more than 30 days => churn
    df["churn"] = (df["days_since_last_visit"] > 30).astype(int)
    df["churn_label"] = np.where(df["churn"] == 1, "Churn", "Retained")

    scaler = MinMaxScaler()
    scaled = pd.DataFrame(
        scaler.fit_transform(df[["visit_per_week", "duration_in_gym_minutes", "personal_training_hours"]]),
        columns=["visit_per_week", "duration_in_gym_minutes", "personal_training_hours"]
    )

    df["engagement_score"] = (
        0.45 * scaled["visit_per_week"] +
        0.25 * scaled["duration_in_gym_minutes"] +
        0.15 * df["attend_group_lesson"].astype(int) +
        0.10 * df["personal_training"].astype(int) +
        0.05 * df["uses_sauna"].astype(int)
    ) * 100

    return df


def train_models(df: pd.DataFrame) -> pd.DataFrame:
    feature_cols = [
        "age", "membership_type", "visit_per_week", "attend_group_lesson",
        "duration_in_gym_minutes", "has_drink_subscription", "personal_training",
        "uses_sauna", "self_identified_gender", "subscription_price",
        "subscription_model", "discount_type", "discount_rate", "final_price",
        "access_hours", "home_gym_location", "personal_training_hours",
        "multi_location_access", "membership_tenure_days"
    ]

    X = df[feature_cols].copy()
    y = df["churn"]

    categorical_cols = X.select_dtypes(include=["object", "bool"]).columns.tolist()
    numeric_cols = [c for c in X.columns if c not in categorical_cols]

    preprocess = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
        ]
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(n_estimators=300, max_depth=8, random_state=42, class_weight="balanced")
    }

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    rows = []

    for name, model in models.items():
        pipe = Pipeline([
            ("preprocess", preprocess),
            ("model", model)
        ])

        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        y_prob = pipe.predict_proba(X_test)[:, 1]

        rows.append({
            "model": name,
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred),
            "roc_auc": roc_auc_score(y_test, y_prob)
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = load_and_prepare("Fitness_Membership_Analytics.csv")
    df.to_csv("mygym_cleaned_features.csv", index=False, encoding="utf-8-sig")
    metrics = train_models(df)
    print(metrics)
    metrics.to_csv("model_metrics.csv", index=False, encoding="utf-8-sig")