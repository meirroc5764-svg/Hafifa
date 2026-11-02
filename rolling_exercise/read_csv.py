from fastapi import APIRouter, UploadFile, File
import uvicorn
import csv
import io


router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    content = await file.read()
    csv_file = io.StringIO(content.decode("utf-8"))
    reader = csv.DictReader(csv_file)

    rows = list(reader)

    return rows

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)