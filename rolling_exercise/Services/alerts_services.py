"""
Alerts database services.

Provides asynchronous database operations for retrieving
all alerts and filtering alerts by date or city.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection
from myData.data_connect import alert
from datetime import date
from logger import logger


async def get_all_alerts(connection: AsyncConnection):
    """
    Retrieve all alert records from the database.

    Args:
        connection (AsyncConnection): Active database connection.

    Returns:
        list[dict]: All alert records.
    """
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
    """
    Retrieve alerts for a specific date.

    Args:
        connection (AsyncConnection): Active database connection.
        alert_date (date): Date used to filter alert records.

    Returns:
        list[dict]: Alert records matching the specified date.
    """
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
    """
    Retrieve alerts for a specific city.

    Args:
        connection (AsyncConnection): Active database connection.
        city (str): Name of the city used to filter alerts.

    Returns:
        list[dict]: Alert records matching the specified city.
    """
    logger.info(f"Getting alerts for city: {city}")

    query = select(alert).where(
        alert.c.city == city
    )

    result = await connection.execute(query)
    rows = result.mappings().all()

    logger.info(f"Found {len(rows)} alerts for city: {city}")

    return [dict(row) for row in rows]