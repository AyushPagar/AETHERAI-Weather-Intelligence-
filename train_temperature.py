import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

FEATURE_COLS = [
    "latitude", "temp_max_today", "temp_min_today", "temp_mean_today",
    "temp_lag1", "temp_lag2", "humidity_mean", "pressure_mean",
    "pressure_change", "wind_max", "cloud_cover_mean", "precipitation_today",
    "day_of_year_sin", "day_of_year_cos"
]

def train_temperature_model(data_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(data_path)
    
    X = df[FEATURE_COLS]
    y = df["target_temp_max_next"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    metrics = {
        "model_name": "RandomForestRegressor (Temperature)",
        "mae": round(float(mae), 4),
        "rmse": round(float(rmse), 4),
        "r2": round(float(r2), 4),
        "feature_importance": dict(zip(FEATURE_COLS, [round(float(fi), 4) for fi in model.feature_importances_]))
    }

    joblib.dump(model, os.path.join(output_dir, "temp_model.joblib"))
    joblib.dump(scaler, os.path.join(output_dir, "temp_scaler.joblib"))
    with open(os.path.join(output_dir, "temp_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    print("=== Temperature Model Trained Successfully ===")
    print(f"MAE: {mae:.4f} °C, RMSE: {rmse:.4f} °C, R²: {r2:.4f}")
    return metrics

if __name__ == "__main__":
    base_dir = "C:/Users/Sham/.gemini/antigravity/scratch/aetherweather-ai/backend"
    train_temperature_model(
        data_path=os.path.join(base_dir, "data/historical_weather_dataset.csv"),
        output_dir=os.path.join(base_dir, "ml/models")
    )
