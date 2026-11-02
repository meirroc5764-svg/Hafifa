from data_validation import master_validator
from fastapi import APIRouter, UploadFile, File
import uvicorn
import pandas as pd
import csv
import io


router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    clean_data = master_validator(df)

    



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)