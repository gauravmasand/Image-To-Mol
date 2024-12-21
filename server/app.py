from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import os
import aiofiles
from run_decimer_save_results import run_decimer  # Importing the function

app = FastAPI(title="Image Processing API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
UPLOAD_DIR = "test_images"
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
    result_path: Optional[str] = None


@app.get("/")
async def inital_route():
    return {"Status": "Server is running successfully"}


@app.post("/api/v1/process-image/", response_model=ImageResponse)
async def process_image(file: UploadFile = File(...)) -> ImageResponse:
    """
    Process an uploaded image using DECIMER.
    """
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

    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    # Process image using the imported `run_decimer` function
    results = run_decimer(UPLOAD_DIR, RESULTS_FILE)
    result_entry = next((res for res in results if res[0] == file.filename), None)
    if not result_entry:
        raise HTTPException(
            status_code=500,
            detail="Processing failed: No result found for the uploaded image"
        )

    # Return response
    return ImageResponse(
        message="Image processed successfully",
        file_name=file.filename,
        status="success",
        result_path=RESULTS_FILE
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8089, reload=True)
