from fastapi import APIRouter, HTTPException, Query
from app.services.open_meteo import get_current_and_forecast
from app.services.ml_service import predictor_service

router = APIRouter()

@router.get("/predict")
async def predict_weather_endpoint(lat: float = Query(...), lon: float = Query(...)):
    try:
        data = await get_current_and_forecast(lat, lon)
        current = data.get("current", {})
        daily = data.get("daily", {})
        
        prediction = predictor_service.predict_weather(
            current_weather=current,
            daily_forecast=daily,
            latitude=lat
        )
        return {
            "latitude": lat,
            "longitude": lon,
            "prediction": prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction service error: {str(e)}")
