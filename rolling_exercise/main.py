from fastapi import FastAPI
from read_csv import file_read_router
from myData.data_connect import create_tables
import uvicorn



app = FastAPI()

app.include_router(file_read_router)

if __name__ == "__main__":
    create_tables()
    uvicorn.run("main:app", reload=True)