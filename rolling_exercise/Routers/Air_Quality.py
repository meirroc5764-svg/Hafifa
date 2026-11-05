from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from datetime import date

from Services.air_quality_services import (
    get_air_quality,
    get_air_quality_by_city,
    get_city_aqi_history,
    get_city_aqi_average,
    get_best_cities
)

from myData.data_connect import get_db
from logger import logger


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
    # check if date time is valid before search
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be later than end_date"
        )

    try:
        return await get_air_quality(connection, start_date, end_date)

    except Exception:
        logger.exception("Failed to get air quality data")

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


@air_quality_router.get("/city")
async def get_air_quality_by_city_router(
    city: str,
    connection: AsyncConnection = Depends(get_db)
):
    try:
        return await get_air_quality_by_city(connection, city)

    except Exception:
        logger.exception(f"Failed to get air quality for city: {city}")

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


@air_quality_router.get("/city/history")
async def get_city_aqi_history_router(
    city: str,
    connection: AsyncConnection = Depends(get_db)
):
    try:
        return await get_city_aqi_history(connection, city)

    except Exception:
        logger.exception(f"Failed to get AQI history for city: {city}")

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


@air_quality_router.get("/city/average")
async def get_city_aqi_average_router(
    city: str,
    connection: AsyncConnection = Depends(get_db)
):
    try:
        return await get_city_aqi_average(connection, city)

    except Exception:
        logger.exception(f"Failed to calculate average AQI for city: {city}")

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


@air_quality_router.get("/best-cities")
async def get_best_cities_router(
    connection: AsyncConnection = Depends(get_db)
):
    try:
        return await get_best_cities(connection)

    except Exception:
        logger.exception("Failed to get best cities")

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )