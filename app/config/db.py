from motor.motor_asyncio import AsyncIOMotorClient
from app.config.env import MONGODB_URI, DB_NAME
client = AsyncIOMotorClient(MONGODB_URI)

db = client[DB_NAME]

user_collection = db['users']
