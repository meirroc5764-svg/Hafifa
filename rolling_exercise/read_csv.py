from data_validation import master_validator
from calculate_aqi import calculate_aqi
from myData.Save_to_data import insert_all_data, insert_alert
from fastapi import APIRouter, UploadFile, File, HTTPException
import uvicorn
import pandas as pd
import csv
import io


file_read_router = APIRouter(
    prefix="/read",
    tags=["Read_data_file"]
)

@file_read_router.post("/upload_csv")
async def upload_file(file: UploadFile = File(...)):

    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    df = master_validator(df)

    if df.empty:
        return HTTPException(status_code=500, detail = "invalid data")

    df["AQI"] = df.apply(
        lambda row: calculate_aqi(
            row["PM2.5"],
            row["NO2"],
            row["CO2"]
        ),
        axis=1
    )

    df["AQI"] = pd.to_numeric(df["AQI"], errors="coerce")
    
    # Filter dangerous measurements
    alerts_df = df[df["AQI"] > 300]

    # Filter normal measurements
    normal_df = df[df["AQI"] <= 300]

    insert_all_data(normal_df)

    if not alerts_df.empty:
        insert_alert(alerts_df)

    return "finish"



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)