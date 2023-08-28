import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

class PostgresDatabase:
    def __init__(self):
        self.config = {
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
            "database": os.getenv("POSTGRES_DB"),  # Note: asyncpg uses "database" instead of "dbname"
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "timeout": 5  # asyncpg uses "timeout" instead of "connect_timeout"
        }
        self.conn = None

    async def connect(self):
        try:
            self.conn = await asyncpg.connect(**self.config)
            print("Connected to the PostgreSQL database successfully!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    async def close(self):
        if self.conn:
            await self.conn.close()
            print("Database connection closed.")

async def get_db():
    db = PostgresDatabase()
    await db.connect()
    try:
        yield db
    finally:
        await db.close()
