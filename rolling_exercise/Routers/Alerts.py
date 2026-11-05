"""
Alerts API routes.

Defines FastAPI endpoints for retrieving all alerts,
filtering alerts by date, and filtering alerts by city.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from datetime import date

from myData.data_connect import get_db
from logger import logger

from Services.alerts_services import (
    get_all_alerts,
    get_alerts_by_date,
    get_alerts_by_city
)


alerts_router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@alerts_router.get("/")
async def get_all_alerts_router(
    connection: AsyncConnection = Depends(get_db)
):
    """
    Retrieve all alerts from the database.

    Args:
        connection (AsyncConnection): Database connection provided by FastAPI.

    Returns:
        list: All alert records.

    Raises:
        HTTPException: 500 if a database error occurs.
    """
    try:
        return await get_all_alerts(connection)

    except Exception:
        logger.exception("Failed to get all alerts")

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


@alerts_router.get("/date")
async def get_alerts_by_date_router(
    alert_date: date,
    connection: AsyncConnection = Depends(get_db)
):
    """
    Retrieve alerts for a specific date.

    Args:
        alert_date (date): Date used to filter the alerts.
        connection (AsyncConnection): Database connection provided by FastAPI.

    Returns:
        list: Alert records matching the specified date.

    Raises:
        HTTPException: 500 if a database error occurs.
    """
    try:
        return await get_alerts_by_date(connection, alert_date)

    except Exception:
        logger.exception(f"Failed to get alerts for date: {alert_date}")

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


@alerts_router.get("/city")
async def get_alerts_by_city_router(
    city: str,
    connection: AsyncConnection = Depends(get_db)
):
    """
    Retrieve alerts for a specific city.

    Args:
        city (str): Name of the city used to filter alerts.
        connection (AsyncConnection): Database connection provided by FastAPI.

    Returns:
        list: Alert records matching the specified city.

    Raises:
        HTTPException: 500 if a database error occurs.
    """
    try:
        return await get_alerts_by_city(connection, city)

    except Exception:
        logger.exception(f"Failed to get alerts for city: {city}")

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )