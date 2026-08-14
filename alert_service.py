from typing import Dict, Any, List

def evaluate_weather_alerts(current_weather: Dict[str, Any], daily_forecast: Dict[str, Any]) -> List[Dict[str, Any]]:
    alerts = []
    
    temp = current_weather.get("temperature_2m", 0.0)
    wind_speed = current_weather.get("wind_speed_10m", 0.0)
    precip = current_weather.get("precipitation", 0.0)
    uv = current_weather.get("uv_index", 0.0)
    weather_code = current_weather.get("weather_code", 0)

    # 1. Extreme Heat Alert
    if temp >= 38.0:
        alerts.append({
            "id": "extreme-heat-danger",
            "type": "danger",
            "title": "Extreme Heat Advisory",
            "description": f"Dangerous temperatures reaching {temp}°C. Hydrate and avoid direct sun exposure during afternoon hours.",
            "category": "Temperature",
            "severity": "CRITICAL"
        })
    elif temp >= 32.0:
        alerts.append({
            "id": "high-heat-warning",
            "type": "warning",
            "title": "High Temperature Warning",
            "description": f"Elevated temperature recorded at {temp}°C. Prolonged outdoor activity may cause heat fatigue.",
            "category": "Temperature",
            "severity": "MODERATE"
        })

    # 2. Heavy Rain Alert
    rain_sum = daily_forecast.get("rain_sum", [0])[0] if daily_forecast.get("rain_sum") else 0
    if precip >= 15.0 or rain_sum >= 25.0:
        alerts.append({
            "id": "heavy-rain-warning",
            "type": "danger",
            "title": "Heavy Precipitation Warning",
            "description": f"Significant rainfall expected ({rain_sum if rain_sum else precip} mm). Potential for localized urban flooding and slippery road surfaces.",
            "category": "Precipitation",
            "severity": "HIGH"
        })
    elif precip >= 5.0 or rain_sum >= 10.0:
        alerts.append({
            "id": "moderate-rain-info",
            "type": "info",
            "title": "Rain Advisory",
            "description": f"Steady rainfall detected ({rain_sum if rain_sum else precip} mm). Carry umbrellas and exercise caution while driving.",
            "category": "Precipitation",
            "severity": "LOW"
        })

    # 3. High Wind Advisory
    if wind_speed >= 50.0:
        alerts.append({
            "id": "high-wind-gale",
            "type": "danger",
            "title": "High Wind Warning",
            "description": f"Gale-force wind gusts up to {wind_speed} km/h recorded. Secure loose outdoor objects and remain vigilant near trees.",
            "category": "Wind",
            "severity": "HIGH"
        })
    elif wind_speed >= 30.0:
        alerts.append({
            "id": "wind-breeze-info",
            "type": "warning",
            "title": "Breezy Conditions",
            "description": f"Fresh to strong wind speeds averaging {wind_speed} km/h.",
            "category": "Wind",
            "severity": "MODERATE"
        })

    # 4. Thunderstorm / Extreme Weather Code Alert (95-99 = Thunderstorm)
    if weather_code in [95, 96, 99]:
        alerts.append({
            "id": "thunderstorm-danger",
            "type": "danger",
            "title": "Severe Thunderstorm Hazard",
            "description": "Active severe thunderstorm cell with lightning activity detected in the region.",
            "category": "Storm",
            "severity": "CRITICAL"
        })

    # 5. UV Alert
    if uv >= 8.0:
        alerts.append({
            "id": "uv-extreme-warning",
            "type": "warning",
            "title": "Very High UV Radiation",
            "description": f"UV Index registered at {uv}. Wear broad-spectrum SPF 30+ sunscreen and protective eyewear.",
            "category": "UV Index",
            "severity": "MODERATE"
        })

    # Default Low-Risk status if no severe conditions triggered
    if not alerts:
        alerts.append({
            "id": "normal-conditions",
            "type": "success",
            "title": "Optimal Weather Conditions",
            "description": "No active severe weather warnings detected for this location.",
            "category": "General",
            "severity": "NORMAL"
        })

    return alerts
