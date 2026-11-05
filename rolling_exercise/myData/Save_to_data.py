"""
Database insertion services.

Provides asynchronous functions for inserting air quality
measurements and alert records into PostgreSQL.
"""

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncConnection
from myData.data_connect import air_quality, alert
from logger import logger


async def insert_all_data(connection: AsyncConnection, df):
    """
    Insert air quality records into the database.

    Args:
        connection (AsyncConnection): Active SQLAlchemy database connection.
        df (pd.DataFrame): DataFrame containing air quality measurements.

    Raises:
        Exception: If the database insertion fails.
    """
    records = df.to_dict(orient="records")

    try:
        logger.info(f"Starting insertion of {len(records)} air quality records")

        await connection.execute(
            insert(air_quality),
            records
        )

        logger.info(f"Successfully inserted {len(records)} air quality records")

    except Exception:
        logger.exception("Failed to insert air quality records")
        raise


async def insert_alert(connection: AsyncConnection, df):
    """
    Insert alert records into the database.

    Args:
        connection (AsyncConnection): Active SQLAlchemy database connection.
        df (pd.DataFrame): DataFrame containing alert information.

    Raises:
        Exception: If the database insertion fails.
    """
    records = df.to_dict(orient="records")

    try:
        logger.info(f"Starting insertion of {len(records)} alert records")

        await connection.execute(
            insert(alert),
            records
        )

        logger.info(f"Successfully inserted {len(records)} alert records")

    except Exception:
        logger.exception("Failed to insert alert records")
        raise

