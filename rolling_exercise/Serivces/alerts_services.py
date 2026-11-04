from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection
from myData.data_connect import alert
from datetime import date


async def get_all_alerts(connection: AsyncConnection):

    query = select(alert)

    result = await connection.execute(query)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_alerts_by_date(
    connection: AsyncConnection,
    alert_date: date
):

    query = select(alert).where(
        alert.c.date == alert_date
    )

    result = await connection.execute(query)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_alerts_by_city(
    connection: AsyncConnection,
    city: str
):

    query = select(alert).where(
        alert.c.city == city
    )

    result = await connection.execute(query)
    rows = result.mappings().all()

    return [dict(row) for row in rows]