from data_validation import master_validator
from calculate_aqi import calculate_aqi
from myData.Save_to_data import insert_all_data, insert_alert
from myData.data_connect import get_db

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncConnection

from logger import logger

import pandas as pd
import io


file_read_router = APIRouter(
    prefix="/read",
    tags=["Read_data_file"]
)


@file_read_router.post("/upload_csv")
async def upload_file(
    file: UploadFile = File(...),
    connection: AsyncConnection = Depends(get_db)
):
    try:
        logger.info(f"Starting CSV upload: {file.filename}")

        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))

        df = master_validator(df)

        if df.empty:
            logger.warning("CSV validation failed: no valid data")
            raise HTTPException(
                status_code=400,
                detail="Invalid data"
            )

        df["AQI"] = df.apply(
            lambda row: calculate_aqi(
                row["PM2.5"],
                row["NO2"],
                row["CO2"]
            ),
            axis=1
        )

        df["AQI"] = pd.to_numeric(
            df["AQI"],
            errors="coerce"
        ).fillna(500)

        # Filter dangerous measurements
        alerts_df = df[df["AQI"] > 300]

        # Save all records and alerts in one transaction
        async with connection.begin():

            await insert_all_data(connection, df)

            if not alerts_df.empty:
                await insert_alert(connection, alerts_df)

        logger.info(
            f"CSV upload completed: {len(df)} records, "
            f"{len(alerts_df)} alerts"
        )

        return {
            "message": "CSV uploaded successfully",
            "total_records": len(df),
            "alerts": len(alerts_df)
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Failed to upload CSV")

        raise HTTPException(
            status_code=500,
            detail="Failed to process CSV file"
        )