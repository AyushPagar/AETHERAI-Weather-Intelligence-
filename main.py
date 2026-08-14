import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure app package is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.routes import geocode, weather, forecast, historical, predict, analytics, compare, alerts

app = FastAPI(
    title="AetherWeather AI API",
    description="Machine Learning Weather Intelligence & Forecast Engine",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routes
app.include_router(geocode.router, prefix="/api", tags=["Geocoding"])
app.include_router(weather.router, prefix="/api", tags=["Weather"])
app.include_router(forecast.router, prefix="/api", tags=["Forecast"])
app.include_router(historical.router, prefix="/api", tags=["Historical"])
app.include_router(predict.router, prefix="/api", tags=["Machine Learning"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])
app.include_router(compare.router, prefix="/api", tags=["City Comparison"])
app.include_router(alerts.router, prefix="/api", tags=["Severe Weather Alerts"])

@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "AetherWeather AI Engine",
        "version": "1.0.0",
        "ml_status": "loaded"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
