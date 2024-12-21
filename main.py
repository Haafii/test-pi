from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Dict

# Initialize FastAPI app
app = FastAPI()

# MongoDB connection setup
MONGO_URL = "mongodb+srv://hafi:Hafi1234@cluster0.wgiuymy.mongodb.net/testpi?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URL)
db = client["testpi"]  # Database name
collection = db["testpidata"]  # Collection name

# Pydantic model for incoming data
class Item(BaseModel):
    name: str
    description: str

# Helper function to convert MongoDB ObjectId to string
def serialize_item(item: Dict) -> Dict:
    item["_id"] = str(item["_id"])
    return item

# POST endpoint to add data to MongoDB
@app.post("/items/")
async def add_item(item: Item):
    try:
        # Insert item into the database
        result = collection.insert_one(item.dict())
        return {"message": "Item added successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding item: {str(e)}")

# GET endpoint to retrieve all items from MongoDB
@app.get("/items/", response_model=List[Dict])
async def get_items():
    try:
        # Fetch all items from the database
        items = list(collection.find())
        return [serialize_item(item) for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {str(e)}")

# Run the app using uvicorn (development server)
# uvicorn filename:app --reload
