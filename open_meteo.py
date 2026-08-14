import httpx
from typing import Dict, Any, List, Optional
from app.config import OPEN_METEO_GEOCODING_URL, OPEN_METEO_FORECAST_URL, OPEN_METEO_HISTORICAL_URL

async def search_city(name: str, count: int = 5) -> List[Dict[str, Any]]:
    params = {
        "name": name,
        "count": count,
        "language": "en",
        "format": "json"
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.get(OPEN_METEO_GEOCODING_URL, params=params)
        res.raise_for_status()
        data = res.json()
        results = data.get("results", [])
        formatted = []
        for r in results:
            formatted.append({
                "id": r.get("id"),
                "name": r.get("name"),
                "latitude": r.get("latitude"),
                "longitude": r.get("longitude"),
                "country": r.get("country", ""),
                "country_code": r.get("country_code", ""),
                "admin1": r.get("admin1", ""), # region/state
                "timezone": r.get("timezone", "UTC")
            })
        return formatted

async def get_current_and_forecast(latitude: float, longitude: float) -> Dict[str, Any]:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature",
            "is_day", "precipitation", "rain", "showers", "snowfall",
            "weather_code", "cloud_cover", "pressure_msl", "surface_pressure",
            "wind_speed_10m", "wind_direction_10m", "uv_index"
        ],
        "hourly": [
            "temperature_2m", "relative_humidity_2m", "dew_point_2m",
            "apparent_temperature", "precipitation_probability", "precipitation",
            "rain", "weather_code", "pressure_msl", "surface_pressure",
            "cloud_cover", "visibility", "wind_speed_10m", "uv_index"
        ],
        "daily": [
            "weather_code", "temperature_2m_max", "temperature_2m_min",
            "apparent_temperature_max", "apparent_temperature_min",
            "sunrise", "sunset", "uv_index_max", "precipitation_sum",
            "rain_sum", "showers_sum", "snowfall_sum", "precipitation_hours",
            "precipitation_probability_max", "wind_speed_10m_max",
            "wind_gusts_10m_max", "wind_direction_10m_dominant"
        ],
        "timezone": "auto"
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.get(OPEN_METEO_FORECAST_URL, params=params)
        res.raise_for_status()
        return res.json()

async def get_historical_weather(latitude: float, longitude: float, start_date: str, end_date: str) -> Dict[str, Any]:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
            "precipitation_sum", "rain_sum", "wind_speed_10m_max",
            "relative_humidity_2m_mean"
        ],
        "timezone": "auto"
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.get(OPEN_METEO_HISTORICAL_URL, params=params)
        res.raise_for_status()
        return res.json()
