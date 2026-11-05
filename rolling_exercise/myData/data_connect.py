"""
Database configuration and table definitions.

Creates an asynchronous SQLAlchemy engine, defines database tables,
and provides functions for database initialization and connections.
"""

from sqlalchemy import MetaData, Table, Column, Integer, String, Float, Date
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from logger import logger
import os


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

metadata = MetaData()

air_quality = Table(
    "air_quality",
    metadata,

    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("date", Date, nullable=False),
    Column("city", String(100), nullable=False),
    Column("PM2.5", Float),
    Column("NO2", Float),
    Column("CO2", Float),
    Column("AQI", Integer)
)

alert = Table(
    "alerts",
    metadata,

    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("date", Date, nullable=False),
    Column("city", String(100), nullable=False),
    Column("AQI", Integer)
)


async def create_tables():
    """
    Create database tables if they do not already exist.

    Uses the SQLAlchemy metadata to create all defined tables.
    Logs the operation and raises an exception if creation fails.
    """
    try:
        logger.info("Starting database table creation")

        async with engine.begin() as connection:
            await connection.run_sync(metadata.create_all)

        logger.info("Database tables created successfully")

    except Exception:
        logger.exception("Failed to create database tables")
        raise


async def get_db():
    """
    Provide an asynchronous database connection.

    Yields:
        AsyncConnection: An active SQLAlchemy database connection.

    The connection is automatically closed after the caller finishes.
    """
    async with engine.connect() as connection:
        yield connection


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())
    logger.info("Database initialization completed")
