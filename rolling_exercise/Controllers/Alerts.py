from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from datetime import date

from myData.data_connect import get_db

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

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(error)}"
        )


@alerts_router.get("/date")
async def get_alerts_by_date_router(
    alert_date: date,
    connection: AsyncConnection = Depends(get_db)
):

    try:
        return await get_alerts_by_date(connection, alert_date)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(error)}"
        )


@alerts_router.get("/city")
async def get_alerts_by_city_router(
    city: str,
    connection: AsyncConnection = Depends(get_db)
):

    try:
        return await get_alerts_by_city(connection, city)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(error)}"
        )