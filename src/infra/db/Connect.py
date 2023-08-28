from contextlib import asynccontextmanager
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

class PostgresDatabase:
    def __init__(self):
        self.config = {
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
            "database": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "min_size": 5,  # Minimum number of connections in the pool
            "max_size": 20,  # Maximum number of connections in the pool
            "timeout": 10  # Connection timeout
        }
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(**self.config)
        print("Connection pool created successfully!")

    async def close(self):
        await self.pool.close()
        print("Connection pool closed.")

    async def get_conn(self):
        return await self.pool.acquire()

    async def release_conn(self, conn):
        await self.pool.release(conn)
    
    async def __aenter__(self):
        self.conn = await self.pool.acquire()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.pool.release(self.conn)
    
    async def fetchval(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)
    async def fetchrow(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)
    async def fetch(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

async def get_db():
    db = PostgresDatabase()
    await db.connect()
    try:
        yield db
    finally:
        await db.close()