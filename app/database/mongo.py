from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DETAILS, DATABASE_NAME

try:
    client = AsyncIOMotorClient(MONGO_DETAILS)
    database = client[DATABASE_NAME]
    item_collection = database.get_collection("micro")
    portal_collection = database.get_collection("portals")
except Exception as e:
    raise ConnectionError(f"Could not connect to MongoDB: {str(e)}")
