from db.db_connect import get_database
from db.schema import ProcessingRequestSchema

# Get the database instance
db = get_database()

def add_processing_request(data: dict):
    """
    Add a processing request document to the 'processing_requests' collection.
    Args:
        data (dict): Processing request data to be inserted.
    Returns:
        str: The ID of the inserted document.
    """
    # Validate the data using Pydantic
    validated_data = ProcessingRequestSchema(**data)
    # Insert into the database
    collection = db['processing_requests']  # Collection name
    result = collection.insert_one(validated_data.dict())
    return str(result.inserted_id)

def get_all_requests():
    """
    Retrieve all processing requests from the 'processing_requests' collection.
    Returns:
        list: A list of processing request documents.
    """
    collection = db['processing_requests']
    return list(collection.find({}, {"_id": 0}))  # Exclude MongoDB's internal `_id` field
