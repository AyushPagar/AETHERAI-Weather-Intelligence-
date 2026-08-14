from fastapi import APIRouter, HTTPException, Query
import datetime
import numpy as np
from app.services.open_meteo import get_historical_weather

router = APIRouter()

@router.get("/analytics")
async def get_weather_analytics(
    lat: float = Query(...),
    lon: float = Query(...),
    days: int = Query(30, ge=7, le=365)
):
    try:
        end_date = datetime.date.today() - datetime.timedelta(days=1)
        start_date = end_date - datetime.timedelta(days=days)
        
        data = await get_historical_weather(
            lat, lon,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d")
        )
        
        daily = data.get("daily", {})
        times = daily.get("time", [])
        t_max = [t for t in daily.get("temperature_2m_max", []) if t is not None]
        t_min = [t for t in daily.get("temperature_2m_min", []) if t is not None]
        t_mean = [t for t in daily.get("temperature_2m_mean", []) if t is not None]
        precip = [p for p in daily.get("precipitation_sum", []) if p is not None]
        wind = [w for w in daily.get("wind_speed_10m_max", []) if w is not None]
        humidity = [h for h in daily.get("relative_humidity_2m_mean", []) if h is not None]

        summary = {
            "avg_temp": round(float(np.mean(t_mean)), 1) if t_mean else 0.0,
            "max_temp": round(float(np.max(t_max)), 1) if t_max else 0.0,
            "min_temp": round(float(np.min(t_min)), 1) if t_min else 0.0,
            "total_rainfall": round(float(np.sum(precip)), 1) if precip else 0.0,
            "avg_humidity": round(float(np.mean(humidity)), 1) if humidity else 0.0,
            "max_wind": round(float(np.max(wind)), 1) if wind else 0.0,
            "sample_days": len(times)
        }

        # Daily chart entries
        chart_data = []
        raw_times = daily.get("time", [])
        for i in range(len(raw_times)):
            chart_data.append({
                "date": raw_times[i],
                "temp_max": daily.get("temperature_2m_max", [])[i],
                "temp_min": daily.get("temperature_2m_min", [])[i],
                "temp_mean": daily.get("temperature_2m_mean", [])[i],
                "rainfall": daily.get("precipitation_sum", [])[i],
                "wind_speed": daily.get("wind_speed_10m_max", [])[i],
                "humidity": daily.get("relative_humidity_2m_mean", [])[i]
            })

        return {
            "latitude": lat,
            "longitude": lon,
            "timeframe_days": days,
            "summary": summary,
            "chart_data": chart_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics service error: {str(e)}")
