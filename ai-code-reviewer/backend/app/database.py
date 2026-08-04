from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


class Database:
    client: AsyncIOMotorClient | None = None
    db = None


db_manager = Database()


async def connect_to_mongo():
    db_manager.client = AsyncIOMotorClient(settings.mongodb_uri)
    db_manager.db = db_manager.client[settings.mongodb_db_name]
    await _ensure_indexes()


async def close_mongo_connection():
    if db_manager.client:
        db_manager.client.close()


async def _ensure_indexes():
    db = db_manager.db
    await db.repositories.create_index("full_name", unique=True)
    await db.pull_requests.create_index([("repo_id", 1), ("pr_number", 1)], unique=True)
    await db.reviews.create_index("pr_id")
    await db.reviews.create_index("created_at")
    await db.findings.create_index("review_id")
    await db.findings.create_index("severity")
    await db.rules.create_index([("org_id", 1), ("name", 1)], unique=True)


def get_db():
    return db_manager.db
