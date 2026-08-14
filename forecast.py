from fastapi import APIRouter, HTTPException, Query
from app.services.open_meteo import get_current_and_forecast

router = APIRouter()

@router.get("/forecast")
async def get_forecast_data(lat: float = Query(...), lon: float = Query(...)):
    try:
        data = await get_current_and_forecast(lat, lon)
        hourly = data.get("hourly", {})
        daily = data.get("daily", {})
        
        # Process hourly into structured array (first 24 hours)
        hourly_list = []
        times = hourly.get("time", [])
        temps = hourly.get("temperature_2m", [])
        humidity = hourly.get("relative_humidity_2m", [])
        precip_prob = hourly.get("precipitation_probability", [])
        precip = hourly.get("precipitation", [])
        weather_codes = hourly.get("weather_code", [])
        wind_speeds = hourly.get("wind_speed_10m", [])
        uv_indices = hourly.get("uv_index", [])

        limit = min(24, len(times))
        for i in range(limit):
            hourly_list.append({
                "time": times[i],
                "temp": temps[i] if i < len(temps) else 0,
                "humidity": humidity[i] if i < len(humidity) else 0,
                "rain_prob": precip_prob[i] if i < len(precip_prob) else 0,
                "precipitation": precip[i] if i < len(precip) else 0,
                "weather_code": weather_codes[i] if i < len(weather_codes) else 0,
                "wind_speed": wind_speeds[i] if i < len(wind_speeds) else 0,
                "uv_index": uv_indices[i] if i < len(uv_indices) else 0
            })

        # Process daily into structured array (7 days)
        daily_list = []
        d_times = daily.get("time", [])
        d_codes = daily.get("weather_code", [])
        d_tmax = daily.get("temperature_2m_max", [])
        d_tmin = daily.get("temperature_2m_min", [])
        d_precip = daily.get("precipitation_sum", [])
        d_rain_prob = daily.get("precipitation_probability_max", [])
        d_wind = daily.get("wind_speed_10m_max", [])
        d_uv = daily.get("uv_index_max", [])

        d_limit = min(7, len(d_times))
        for i in range(d_limit):
            daily_list.append({
                "date": d_times[i],
                "weather_code": d_codes[i] if i < len(d_codes) else 0,
                "temp_max": d_tmax[i] if i < len(d_tmax) else 0,
                "temp_min": d_tmin[i] if i < len(d_tmin) else 0,
                "precipitation": d_precip[i] if i < len(d_precip) else 0,
                "rain_prob": d_rain_prob[i] if i < len(d_rain_prob) else 0,
                "wind_max": d_wind[i] if i < len(d_wind) else 0,
                "uv_max": d_uv[i] if i < len(d_uv) else 0
            })

        return {
            "latitude": lat,
            "longitude": lon,
            "hourly": hourly_list,
            "daily": daily_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast service error: {str(e)}")
