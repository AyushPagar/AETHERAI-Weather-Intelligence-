import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

FEATURE_COLS = [
    "latitude", "temp_max_today", "temp_min_today", "temp_mean_today",
    "temp_lag1", "temp_lag2", "humidity_mean", "pressure_mean",
    "pressure_change", "wind_max", "cloud_cover_mean", "precipitation_today",
    "day_of_year_sin", "day_of_year_cos"
]

def train_rain_model(data_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(data_path)
    
    X = df[FEATURE_COLS]
    y = df["target_rain_next"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_prob)

    metrics = {
        "model_name": "RandomForestClassifier (Rain Probability)",
        "accuracy": round(float(accuracy), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1": round(float(f1), 4),
        "roc_auc": round(float(roc_auc), 4),
        "feature_importance": dict(zip(FEATURE_COLS, [round(float(fi), 4) for fi in model.feature_importances_]))
    }

    joblib.dump(model, os.path.join(output_dir, "rain_model.joblib"))
    joblib.dump(scaler, os.path.join(output_dir, "rain_scaler.joblib"))
    with open(os.path.join(output_dir, "rain_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    print("=== Rain Model Trained Successfully ===")
    print(f"Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}, ROC-AUC: {roc_auc:.4f}")
    return metrics

if __name__ == "__main__":
    base_dir = "C:/Users/Sham/.gemini/antigravity/scratch/aetherweather-ai/backend"
    train_rain_model(
        data_path=os.path.join(base_dir, "data/historical_weather_dataset.csv"),
        output_dir=os.path.join(base_dir, "ml/models")
    )
