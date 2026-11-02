from fastapi import FastAPI, UploadFile, File
import uvicorn
import csv
import io


app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    csv_file = io.StringIO(content.decode("utf-8"))
    reader = csv.DictReader(csv_file)

    for row in reader:
        print(row)

    return {"message": "CSV processed"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)