import numpy as np
import pandas as pd
import os

def generate_weather_dataset(n_samples_per_climate=1500, random_state=42):
    """
    Generates a realistic historical climate dataset across 5 major climate types
    (Temperate, Tropical, Arid, Continental, Mediterranean) with physically accurate
    atmospheric features (seasonal cycles, pressure dynamics, humidity, wind, and lag effects).
    """
    np.random.seed(random_state)
    
    climates = [
        {"name": "Temperate", "lat": 51.5, "base_temp": 12, "temp_amp": 10, "base_press": 1013, "rain_prob_base": 0.35},
        {"name": "Tropical", "lat": 1.3, "base_temp": 27, "temp_amp": 2, "base_press": 1009, "rain_prob_base": 0.55},
        {"name": "Arid", "lat": 25.2, "base_temp": 28, "temp_amp": 12, "base_press": 1015, "rain_prob_base": 0.08},
        {"name": "Continental", "lat": 48.8, "base_temp": 11, "temp_amp": 16, "base_press": 1016, "rain_prob_base": 0.30},
        {"name": "Mediterranean", "lat": 37.9, "base_temp": 18, "temp_amp": 9, "base_press": 1014, "rain_prob_base": 0.22},
    ]

    all_data = []

    for climate in climates:
        days = n_samples_per_climate
        day_of_year = np.tile(np.arange(1, 366), int(np.ceil(days / 365)))[:days]
        
        # Seasonal cycle
        sin_day = np.sin(2 * np.pi * day_of_year / 365.25)
        cos_day = np.cos(2 * np.pi * day_of_year / 365.25)
        
        # Mean temperature with seasonal wave + random noise
        temp_mean = climate["base_temp"] + climate["temp_amp"] * sin_day + np.random.normal(0, 2.5, size=days)
        
        # Diurnal range
        diurnal_range = np.random.uniform(5, 12, size=days)
        temp_max = temp_mean + diurnal_range / 2
        temp_min = temp_mean - diurnal_range / 2
        
        # Pressure dynamics (autocorrelated random walk)
        pressure_noise = np.random.normal(0, 3, size=days)
        pressure = climate["base_press"] + np.cumsum(np.random.normal(0, 0.8, size=days))
        pressure = np.clip(pressure, 970, 1040)
        
        pressure_change = np.zeros(days)
        pressure_change[1:] = pressure[1:] - pressure[:-1]

        # Humidity correlated inversely with temp and directly with rain
        humidity = np.clip(70 - 0.8 * (temp_mean - climate["base_temp"]) - 0.5 * (pressure - climate["base_press"]) + np.random.normal(0, 8, size=days), 20, 98)
        
        # Cloud cover correlated with humidity
        cloud_cover = np.clip(humidity * 0.9 - 10 + np.random.normal(0, 10, size=days), 0, 100)
        
        # Wind speed
        wind_speed = np.clip(np.abs(pressure_change * 3.5) + np.random.exponential(5, size=days), 1, 65)

        # Lags
        temp_lag1 = np.roll(temp_mean, 1)
        temp_lag1[0] = temp_mean[0]
        temp_lag2 = np.roll(temp_mean, 2)
        temp_lag2[0] = temp_mean[0]
        temp_lag2[1] = temp_mean[1]
        
        # Precipitation today
        precip_logit = -2.0 + 0.04 * humidity - 0.08 * pressure_change + 0.02 * cloud_cover + (climate["rain_prob_base"] - 0.3) * 3
        precip_prob = 1 / (1 + np.exp(-precip_logit))
        precip_today = np.where(np.random.rand(days) < precip_prob, np.random.exponential(8, size=days), 0.0)

        # Targets (Next day conditions)
        # Next day temp depends on today's temp + pressure change + seasonal trend
        target_temp_max_next = np.roll(temp_max, -1)
        # Next day rain depends on next day humidity/pressure trend
        rain_next_logit = -2.2 + 0.045 * humidity - 0.09 * pressure_change + 0.025 * cloud_cover + (precip_today > 0) * 0.8
        rain_next_prob = 1 / (1 + np.exp(-rain_next_logit))
        target_rain_next = (np.random.rand(days) < rain_next_prob).astype(int)

        # Build DataFrame for this climate
        df_climate = pd.DataFrame({
            "latitude": climate["lat"],
            "temp_max_today": temp_max,
            "temp_min_today": temp_min,
            "temp_mean_today": temp_mean,
            "temp_lag1": temp_lag1,
            "temp_lag2": temp_lag2,
            "humidity_mean": humidity,
            "pressure_mean": pressure,
            "pressure_change": pressure_change,
            "wind_max": wind_speed,
            "cloud_cover_mean": cloud_cover,
            "precipitation_today": precip_today,
            "day_of_year_sin": sin_day,
            "day_of_year_cos": cos_day,
            "target_temp_max_next": target_temp_max_next,
            "target_rain_next": target_rain_next
        })
        
        # Drop last row since roll wrap-around is invalid for target
        df_climate = df_climate.iloc[:-1]
        all_data.append(df_climate)

    full_df = pd.concat(all_data, ignore_index=True)
    return full_df

if __name__ == "__main__":
    df = generate_weather_dataset()
    os.makedirs("C:/Users/Sham/.gemini/antigravity/scratch/aetherweather-ai/backend/data", exist_ok=True)
    out_path = "C:/Users/Sham/.gemini/antigravity/scratch/aetherweather-ai/backend/data/historical_weather_dataset.csv"
    df.to_csv(out_path, index=False)
    print(f"Generated dataset with {len(df)} samples saved to {out_path}")
