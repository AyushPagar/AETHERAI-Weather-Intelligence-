from fastapi import APIRouter, HTTPException, Query
from app.services.open_meteo import get_current_and_forecast

router = APIRouter()

@router.get("/weather")
async def get_current_weather(lat: float = Query(...), lon: float = Query(...)):
    try:
        data = await get_current_and_forecast(lat, lon)
        current = data.get("current", {})
        daily = data.get("daily", {})
        return {
            "latitude": lat,
            "longitude": lon,
            "timezone": data.get("timezone"),
            "current": current,
            "today_summary": {
                "temp_max": daily.get("temperature_2m_max", [None])[0],
                "temp_min": daily.get("temperature_2m_min", [None])[0],
                "sunrise": daily.get("sunrise", [None])[0],
                "sunset": daily.get("sunset", [None])[0],
                "uv_max": daily.get("uv_index_max", [None])[0]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather service error: {str(e)}")
