from motor.motor_asyncio import AsyncIOMotorClient

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    async def close(self):
        self.client.close()

# Dependency
def get_database() -> MongoDB:
    return MongoDB(uri="mongodb://localhost:27017", db_name="test_db")