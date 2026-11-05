from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection
from myData.data_connect import alert
from datetime import date
from logger import logger


async def get_all_alerts(connection: AsyncConnection):

    logger.info("Getting all alerts")

    query = select(alert)

    result = await connection.execute(query)
    rows = result.mappings().all()

    logger.info(f"Found {len(rows)} alerts")

    return [dict(row) for row in rows]


async def get_alerts_by_date(
    connection: AsyncConnection,
    alert_date: date
):

    logger.info(f"Getting alerts for date: {alert_date}")

    query = select(alert).where(
        alert.c.date == alert_date
    )

    result = await connection.execute(query)
    rows = result.mappings().all()

    logger.info(f"Found {len(rows)} alerts for date: {alert_date}")

    return [dict(row) for row in rows]


async def get_alerts_by_city(
    connection: AsyncConnection,
    city: str
):

    logger.info(f"Getting alerts for city: {city}")

    query = select(alert).where(
        alert.c.city == city
    )

    result = await connection.execute(query)
    rows = result.mappings().all()

    logger.info(f"Found {len(rows)} alerts for city: {city}")

    return [dict(row) for row in rows]