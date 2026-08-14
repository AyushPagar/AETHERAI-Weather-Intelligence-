from fastapi import APIRouter, HTTPException, Query
from app.services.open_meteo import get_current_and_forecast
from app.services.alert_service import evaluate_weather_alerts

router = APIRouter()

@router.get("/alerts")
async def get_weather_alerts_endpoint(lat: float = Query(...), lon: float = Query(...)):
    try:
        data = await get_current_and_forecast(lat, lon)
        current = data.get("current", {})
        daily = data.get("daily", {})
        alerts = evaluate_weather_alerts(current, daily)
        return {
            "latitude": lat,
            "longitude": lon,
            "alerts": alerts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Alert service error: {str(e)}")
