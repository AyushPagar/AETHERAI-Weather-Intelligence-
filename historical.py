from fastapi import APIRouter, HTTPException, Query
import datetime
from app.services.open_meteo import get_historical_weather

router = APIRouter()

@router.get("/historical")
async def get_historical_data(
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
        t_max = daily.get("temperature_2m_max", [])
        t_min = daily.get("temperature_2m_min", [])
        t_mean = daily.get("temperature_2m_mean", [])
        precip = daily.get("precipitation_sum", [])
        wind = daily.get("wind_speed_10m_max", [])
        humidity = daily.get("relative_humidity_2m_mean", [])

        records = []
        for i in range(len(times)):
            records.append({
                "date": times[i],
                "temp_max": t_max[i] if i < len(t_max) else 0,
                "temp_min": t_min[i] if i < len(t_min) else 0,
                "temp_mean": t_mean[i] if i < len(t_mean) else 0,
                "precipitation": precip[i] if i < len(precip) else 0,
                "wind_speed": wind[i] if i < len(wind) else 0,
                "humidity": humidity[i] if i < len(humidity) else 0
            })

        return {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "records": records
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Historical weather error: {str(e)}")
