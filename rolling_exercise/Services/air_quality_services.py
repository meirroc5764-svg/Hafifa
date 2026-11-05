"""
Air quality database services.

Provides asynchronous database operations for retrieving air quality
measurements, city AQI history, average AQI values, and the best cities.
"""

from myData.data_connect import air_quality
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select, func
from datetime import date
from logger import logger


async def get_air_quality(
    connection: AsyncConnection,
    start_date: date,
    end_date: date
):
    """
    Retrieve air quality records within a specified date range.

    Args:
        connection (AsyncConnection): Active database connection.
        start_date (date): Beginning of the date range.
        end_date (date): End of the date range.

    Returns:
        list[dict]: Air quality records within the specified date range.
    """
    logger.info(f"Getting air quality from {start_date} to {end_date}")

    query = select(air_quality).where(
        air_quality.c.date >= start_date,
        air_quality.c.date <= end_date
    )

    result = await connection.execute(query)
    rows = result.mappings().all()

    logger.info(f"Found {len(rows)} air quality records")

    return [dict(row) for row in rows]


async def get_air_quality_by_city(connection: AsyncConnection, city: str):
    """
    Retrieve all air quality records for a specific city.

    Args:
        connection (AsyncConnection): Active database connection.
        city (str): Name of the city.

    Returns:
        list[dict]: Air quality records belonging to the specified city.
    """
    logger.info(f"Getting air quality data for city: {city}")

    query = select(air_quality).where(
        air_quality.c.city == city
    )

    result = await connection.execute(query)
    rows = result.mappings().all()

    logger.info(f"Found {len(rows)} records for city: {city}")

    return [dict(row) for row in rows]


async def get_city_aqi_history(connection: AsyncConnection, city: str):
    """
    Retrieve the historical AQI measurements for a specific city.

    Args:
        connection (AsyncConnection): Active database connection.
        city (str): Name of the city.

    Returns:
        list[dict]: AQI measurements ordered by date.
    """
    logger.info(f"Getting AQI history for city: {city}")

    query = (
        select(
            air_quality.c.date,
            air_quality.c.AQI
        )
        .where(air_quality.c.city == city)
        .order_by(air_quality.c.date)
    )

    result = await connection.execute(query)
    rows = result.mappings().all()

    logger.info(f"Found {len(rows)} AQI history records for {city}")

    return [dict(row) for row in rows]


async def get_city_aqi_average(connection: AsyncConnection, city: str):
    """
    Calculate the average AQI for a specific city.

    Args:
        connection (AsyncConnection): Active database connection.
        city (str): Name of the city.

    Returns:
        dict | None: Dictionary containing the average AQI,
                     or None if no result is available.
    """
    logger.info(f"Calculating average AQI for city: {city}")

    query = select(
        func.avg(air_quality.c.AQI).label("average_aqi")
    ).where(
        air_quality.c.city == city
    )

    result = await connection.execute(query)
    row = result.mappings().first()

    logger.info(f"Average AQI calculated for city: {city}")

    return dict(row) if row is not None else None


async def get_best_cities(connection: AsyncConnection):
    """
    Retrieve the three cities with the lowest average AQI.

    Args:
        connection (AsyncConnection): Active database connection.

    Returns:
        list[dict]: Up to three cities ordered by average AQI
                    in ascending order.
    """
    logger.info("Getting top 3 cities with the lowest average AQI")

    query = (
        select(
            air_quality.c.city,
            func.avg(air_quality.c.AQI).label("average_aqi")
        )
        .group_by(air_quality.c.city)
        .order_by(func.avg(air_quality.c.AQI).asc())
        .limit(3)
    )

    result = await connection.execute(query)
    rows = result.mappings().all()

    logger.info(f"Found {len(rows)} best cities")

    return [dict(row) for row in rows]