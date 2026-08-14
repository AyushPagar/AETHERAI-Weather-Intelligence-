from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.open_meteo import get_current_and_forecast, search_city

router = APIRouter()

@router.get("/compare")
async def compare_cities(cities: str = Query(..., description="Comma-separated city names e.g. London,Tokyo,New York")):
    city_list = [c.strip() for c in cities.split(",") if c.strip()][:4] # max 4 cities
    if not city_list:
        raise HTTPException(status_code=400, detail="Please provide at least one city name.")

    comparison_results = []
    for cname in city_list:
        try:
            geo_res = await search_city(cname, count=1)
            if not geo_res:
                continue
            loc = geo_res[0]
            lat, lon = loc["latitude"], loc["longitude"]
            
            wdata = await get_current_and_forecast(lat, lon)
            curr = wdata.get("current", {})
            daily = wdata.get("daily", {})
            
            comparison_results.append({
                "city": loc["name"],
                "country": loc["country"],
                "region": loc["admin1"],
                "latitude": lat,
                "longitude": lon,
                "temp": curr.get("temperature_2m"),
                "feels_like": curr.get("apparent_temperature"),
                "humidity": curr.get("relative_humidity_2m"),
                "wind_speed": curr.get("wind_speed_10m"),
                "pressure": curr.get("pressure_msl") or curr.get("surface_pressure"),
                "weather_code": curr.get("weather_code"),
                "uv_index": curr.get("uv_index"),
                "cloud_cover": curr.get("cloud_cover"),
                "rain_prob": daily.get("precipitation_probability_max", [0])[0],
                "temp_max": daily.get("temperature_2m_max", [0])[0],
                "temp_min": daily.get("temperature_2m_min", [0])[0]
            })
        except Exception as err:
            continue

    return {"comparison": comparison_results}
