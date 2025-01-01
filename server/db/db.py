from fastapi import HTTPException
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB Connection String
MONGO_URI = "mongodb+srv://gauravmasand99:xNcZdKhJ9GgG2424@gauravmasand99.2qqkl.mongodb.net/?retryWrites=true&w=majority&appName=GauravMasand99"

class DB:
    """
    A class to manage MongoDB connection and operations.
    """

    @staticmethod
    def connect_db():
        """
        Establish a connection to the MongoDB database and return the database object.
        """
        client = MongoClient(MONGO_URI)
        db = client['ImageToMol']  # Replace with your desired database name
        print("MongoDB connected successfully.")
        return db

    @staticmethod
    def make_records_of_request(data: dict):
        """
        Insert data into a specified MongoDB collection.

        Args:
            collection_name (str): The name of the collection.
            data (dict): The data to insert into the collection.

        Returns:
            str: The ID of the inserted document.
        """
        collection_name = "ImageToMolConversations"
        db = DB.connect_db()
        collection = db[collection_name]
        result = collection.insert_one(data)
        return str(result.inserted_id)
    
    @staticmethod
    def fetch_document_by_id(document_id: str):
        """
        Fetch a document from the MongoDB collection by its ID.

        Args:
            document_id (str): The ID of the document to fetch.

        Returns:
            dict: The document data.
        """

        collection_name = "ImageToMolConversations"
        db = DB.connect_db()
        collection = db[collection_name]
        document = collection.find_one({"_id": ObjectId(document_id)})
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        document["_id"] = str(document["_id"])  # Convert ObjectId to string
        return document