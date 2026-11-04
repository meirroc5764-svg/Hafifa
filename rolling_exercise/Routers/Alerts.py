from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from datetime import date

from myData.data_connect import get_db
from logger import logger

from Serivces.alerts_services import (
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
    try:
        return await get_alerts_by_city(connection, city)

    except Exception:
        logger.exception(f"Failed to get alerts for city: {city}")

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )