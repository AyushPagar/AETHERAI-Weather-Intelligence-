-import os
import sys

# Ensure backend root is on Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(backend_dir)

from data.generate_training_data import generate_weather_dataset
from ml.train_temperature import train_temperature_model
from ml.train_rain import train_rain_model

def run_full_pipeline():
    print("Step 1: Generating synthetic historical weather dataset...")
    data_dir = os.path.join(backend_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, "historical_weather_dataset.csv")
    
    df = generate_weather_dataset()
    df.to_csv(csv_path, index=False)
    print(f"Dataset generated with {len(df)} records at {csv_path}")

    models_dir = os.path.join(backend_dir, "ml", "models")
    print("\nStep 2: Training Next-Day Temperature ML Model...")
    temp_metrics = train_temperature_model(csv_path, models_dir)

    print("\nStep 3: Training Next-Day Rain Probability ML Model...")
    rain_metrics = train_rain_model(csv_path, models_dir)

    print("\n✅ ML Training Pipeline Complete! Models and Metrics saved successfully.")

if __name__ == "__main__":
    run_full_pipeline()
