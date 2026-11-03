from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from datetime import date

from myData.data_connect import alert, engine

alerts_router = APIRouter(
    prefix="/alerst",
    tags=["Alerts"]
)

@alerts_router.get("/")
async def get_all_alerts():

    query = select(alert)

    try:
        with engine.connect() as connection:
            result = connection.execute(query)
            rows = result.mappings().all()

            return [dict(row) for row in rows]

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(error)}"
        )

@alerts_router.get("/date")
async def get_alerts_by_date(alert_date: date):

    query = select(alert).where(
        alert.c.date == alert_date
    )

    try:
        with engine.connect() as connection:
            result = connection.execute(query)
            rows = result.mappings().all()

            return [dict(row) for row in rows]

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(error)}"
        )

@alerts_router.get("/city")
async def get_alerts_by_city(city: str):

    query = select(alert).where(
        alert.c.city == city
    )

    try:
        with engine.connect() as connection:
            result = connection.execute(query)
            rows = result.mappings().all()

            return [dict(row) for row in rows]

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(error)}"
        )