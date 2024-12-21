from pymongo import MongoClient

# MongoDB Connection String
MONGO_URI = "mongodb+srv://gauravmasand99:xNcZdKhJ9GgG2424@gauravmasand99.2qqkl.mongodb.net/?retryWrites=true&w=majority&appName=GauravMasand99"

def get_database():
    """
    Establish a connection to the MongoDB database and return the database object.
    """
    client = MongoClient(MONGO_URI)
    db = client['gaurav_database']  # Replace with your desired database name
    return db