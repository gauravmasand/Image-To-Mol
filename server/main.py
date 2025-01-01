from db.db import DB
from datetime import datetime

# Connect to the database
db = DB.connect_db()

# Insert data into a collection
data = {
    "start_time": datetime.utcnow(),
    "image_paths": ["users_images_uploaded/image1.png"],
    "results": ["SMILES1"],
    "request_completion_time": datetime.utcnow(),
}
document_id = DB.make_records_of_request(data)
print(f"Inserted document ID: {document_id}")
