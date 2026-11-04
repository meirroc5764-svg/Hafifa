from fastapi import APIRouter, HTTPException, Depends
from datetime import date


from Serivces.air_quality_services import *
from myData.data_connect import get_db




air_quality_router = APIRouter(
    prefix="/air-quality",
    tags=["Air Quality"]
)

@air_quality_router.get("/", summary="Get Air Quality Data")
async def get_air_quality_router(
    start_date: date,
    end_date: date,
    connection: AsyncConnection = Depends(get_db)

):
    # check if date time is valid before serch
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be later than end_date"
        )

    try:
       await get_air_quality(connection, start_date, end_date)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(error)}"
        )

@air_quality_router.get("/city")
async def get_air_quality_by_city_router(city: str, connection: AsyncConnection = Depends(get_db)):

    try:
        await get_air_quality_by_city(connection, city)
    
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(error)}"
        )

@air_quality_router.get("/city/history")
async def get_city_aqi_history_router(city: str, connection: AsyncConnection = Depends(get_db)):

    try:
        await get_city_aqi_history(connection, city)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(error)}"
        )

@air_quality_router.get("/city/average")
async def get_city_aqi_average_router(city: str, connection: AsyncConnection = Depends(get_db)):

    try:
        await get_city_aqi_average(connection, city)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(error)}"
        )

@air_quality_router.get("/best-cities")
async def get_best_cities_router(connection: AsyncConnection = Depends(get_db)):

    try:
        await get_best_cities(connection)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(error)}"
        )