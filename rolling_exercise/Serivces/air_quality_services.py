from myData.data_connect import air_quality, engine
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select, func

from datetime import date

async def get_air_quality(
    connection: AsyncConnection,
    start_date: date,
    end_date: date,

):

    query = select(air_quality).where(
        air_quality.c.date >= start_date,
        air_quality.c.date <= end_date
    )

    result = await connection.execute(query)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_air_quality_by_city(connection: AsyncConnection, city: str):
    
    query = select(air_quality).where(
            air_quality.c.city == city
        )

    result = connection.execute(query)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_city_aqi_history(connection: AsyncConnection, city: str):

    query = (
        select(
            air_quality.c.date,
            air_quality.c.AQI
        )
        .where(air_quality.c.city == city)
        .order_by(air_quality.c.date)
    )

    result = connection.execute(query)
    rows = result.mappings().all()

    return [dict(row) for row in rows]

async def get_city_aqi_average(connection: AsyncConnection, city: str):

    query = select(
        func.avg(air_quality.c.AQI).label("average_aqi")
    ).where(
        air_quality.c.city == city
    )
     
    result = connection.execute(query)
    row = result.mappings().first()

    return dict(row)

async def get_best_cities(connection: AsyncConnection):

    query = (
        select(
            air_quality.c.city,
            func.avg(air_quality.c.AQI).label("average_aqi")
        )
        .group_by(air_quality.c.city)
        .order_by(func.avg(air_quality.c.AQI).asc())
        .limit(3)
    )

    result = connection.execute(query)
    rows = result.mappings().all()

    return [dict(row) for row in rows]