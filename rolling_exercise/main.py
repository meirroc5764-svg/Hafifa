"""
Application entry point.

Initializes the FastAPI application, manages the application lifecycle,
creates database tables on startup, and registers API routers.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from Routers.read_csv import file_read_router
from Routers.Alerts import alerts_router
from Routers.Air_Quality import air_quality_router
from myData.data_connect import create_tables
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage the FastAPI application lifecycle.

    Creates database tables when the application starts.
    """
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


# Register all application routers
app.include_router(file_read_router)
app.include_router(air_quality_router)
app.include_router(alerts_router)


if __name__ == "__main__":
    """
    Start the application using Uvicorn.

    Enables automatic server reload when code changes.
    """
    uvicorn.run("main:app", reload=True)