from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class ProcessingRequestSchema(BaseModel):
    """
    Pydantic schema for the API processing request.
    """
    start_time: datetime = Field(..., example=datetime.utcnow())
    image_paths: List[str] = Field(..., example=["users_images_uploaded/image1.png", "users_images_uploaded/image2.png"])
    results: List[str] = Field(..., example=["SMILES1", "SMILES2"])
    request_completion_time: datetime = Field(..., example=datetime.utcnow())
    