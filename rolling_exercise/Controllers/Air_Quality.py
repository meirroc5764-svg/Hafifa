from fastapi import APIRouter, HTTPException
from myData.data_connect import air_quality, engine
from sqlalchemy import select

from datetime import date


air_quality_router = APIRouter(
    prefix="/air quality",
    tags=["Air Quality"]
)

@air_quality_router.get("/", summary="Get Air Quality Data")
async def get_air_quality(
    start_date: date,
    end_date: date
):
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be later than end_date"
        )

    query = select(air_quality).where(
        air_quality.c.date >= start_date,
        air_quality.c.date <= end_date
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


