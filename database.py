import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "event_management")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

async def drop_test_db():
    await client.drop_database(DB_NAME)

async def init_db():
    pass
