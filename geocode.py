from fastapi import APIRouter, HTTPException, Query
from app.services.open_meteo import search_city

router = APIRouter()

@router.get("/geocode")
async def geocode_city(q: str = Query(..., min_length=2, description="City name to search")):
    try:
        results = await search_city(q)
        return {"query": q, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Geocoding service error: {str(e)}")
