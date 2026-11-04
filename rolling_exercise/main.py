from fastapi import FastAPI
from contextlib import asynccontextmanager
from Routers.read_csv import file_read_router
from Routers.Alerts import alerts_router
from Routers.Air_Quality import air_quality_router
from myData.data_connect import create_tables
import uvicorn





@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI()


'''all routers'''
app.include_router(file_read_router)
app.include_router(air_quality_router)
app.include_router(alerts_router)



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)