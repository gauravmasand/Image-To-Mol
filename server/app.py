from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import os, time
from datetime import datetime
import aiofiles
from db.db import DB
from run_decimer_save_results import run_decimer  # Importing the function

app = FastAPI(title="Image Processing API", debug=True)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to the database
db = DB.connect_db()

# Constants
UPLOAD_DIR = "users_images_uploaded"
RESULTS_DIR = "DECIMER_results"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
RESULTS_FILE = os.path.join(RESULTS_DIR, "results.txt")

# Create necessary directories
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


class ImageResponse(BaseModel):
    message: str
    file_name: str
    status: str
    similes: str
    result_path: Optional[str] = None,
    resultsURL: Optional[str] = None
    

@app.get("/")
async def inital_route():
    return {"Status": "Server is running successfully"}


@app.post("/api/v1/process-image/", response_model=ImageResponse)
async def process_image(file: UploadFile = File(...)) -> ImageResponse:
    """
    Process an uploaded image using DECIMER.
    """
    # Start time of calculation
    startTime = datetime.utcnow()

    # Validate file size
    file_size = 0
    chunk_size = 1024 * 1024  # 1MB chunks

    while True:
        chunk = await file.read(chunk_size)
        file_size += len(chunk)
        if not chunk:
            break
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File size too large. Maximum size allowed is {MAX_FILE_SIZE} bytes"
            )

    # Reset file position
    await file.seek(0)

    # Generate a unique filename with milliseconds
    timestamp = int(time.time() * 1000)  # Current time in milliseconds
    file_name_with_timestamp = f"{timestamp}_{file.filename}"

    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file_name_with_timestamp)
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # Process image using the imported `run_decimer` function
    results = run_decimer(UPLOAD_DIR, RESULTS_FILE)
    result_entry = next((res for res in results if res[0] == file_name_with_timestamp), None)
    if not result_entry:
        raise HTTPException(
            status_code=500,
            detail="Processing failed: No result found for the uploaded image"
        )
    
    endTime = datetime.utcnow()

    data = {
        "start_time": startTime,
        "image_paths": ["users_images_uploaded/image1.png"],
        "results": ["SMILES1"],
        "request_completion_time": endTime,
    }
    
    document_id = DB.make_records_of_request(data)

    # Return response
    return ImageResponse(
        message="Image processed successfully",
        file_name=file_name_with_timestamp,
        status="success",
        result_path=RESULTS_FILE,
        similes=result_entry[1],  # Corrected to use the matched result entry
        resultsURL=document_id
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8089,
        reload=True,
        log_level="debug"  # Set log level to debug for detailed logs
    )
