# AETHERAI-Weather-Intelligence-
AetherWeather AI is a full-stack, intelligent weather analytics and prediction platform. It pairs real-time meteorological data with custom Machine Learning models to deliver next-day atmospheric forecasts, climate trends, risk alerts, and multi-city comparisons.

┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)                  │
│   • Glassmorphic UI & Dynamic Ambient Glow (Weather-reactive)│
│   • Interactive Recharts, Framer Motion, Lucide Icons       │
└──────────────────────────────┬──────────────────────────────┘
                               │ REST APIs / JSON
┌──────────────────────────────▼──────────────────────────────┐
│                    Backend (FastAPI / Python)               │
│   • Async routing, aggregation, and caching                 │
│   • Real-time rule-based Risk & Hazard Engine               │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
┌──────────────▼─────────────┐   ┌─────────────▼──────────────┐
│  Machine Learning (Scikit) │   │     Open-Meteo REST APIs   │
│  • RandomForestRegressor   │   │  • Geocoding API           │
│  • RandomForestClassifier  │   │  • Forecast & Hourly API   │
│  • Metrics & Confidence    │   │  • Historical Archive API  │
└────────────────────────────┘   └────────────────────────────┘

Key Capabilities & Features
AI Atmospheric Predictions:

Machine Learning: Utilizes Scikit-Learn (RandomForestRegressor and RandomForestClassifier trained via 

train_all.py
) to forecast next-day maximum temperatures and precipitation probabilities.
Explainable AI: Displays model metrics (MAE, RMSE, $R^2$, Accuracy, Precision, Recall, F1 Score) and confidence scoring.
Current Weather & Extended Forecasts:

Live temperature, feels-like temperature, and WMO weather condition icons.
Metrics cards for humidity, wind speed, pressure, cloud cover, UV index, and visibility.
24-hour horizontal hourly forecast and 7-day extended outlook.
Climate Analytics & Trends:

Historical temperature trends, rainfall volume, humidity, and peak wind speeds rendered with interactive Recharts (over 7, 14, 30, or 90 days).
Multi-City Comparison:

Side-by-side comparison matrix for up to 4 cities simultaneously with comparative temperature and moisture charts.
Automated Risk & Hazard Alerts:

Real-time rule evaluation for extreme heat, heavy rain, gale-force winds, thunderstorms, and high UV radiation.
Dynamic Atmospheric UI:

Weather-reactive background glow (transitions across Sunny, Rain, Cloudy, Storm, and Night modes), dark/light mode toggle, and responsive glassmorphism.
💻 Tech Stack
Frontend: 

React.js
, Vite, Tailwind CSS, Recharts, Framer Motion, Lucide Icons, Axios
Backend: 

FastAPI
, Uvicorn, Python async HTTP client (httpx)
Machine Learning: Scikit-Learn, Pandas, NumPy, Joblib
Data Source: Open-Meteo APIs (Geocoding, Forecast, Archive)
