import asyncpg
import uuid
from src.domain.entity.Person import Person
from fastapi import HTTPException

class PersonRepository:

    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def get_person_by_apelido(self, apelido: str):
        async with self.db_pool.pool.acquire() as conn:
            result = await conn.fetchrow("SELECT id, apelido, nome, nascimento, stack FROM pessoas WHERE apelido = $1", apelido)
            if result:
                return Person(result['apelido'], result['nome'], result['nascimento'], result['stack'])
        return None

    async def add_person(self, person: Person):
        async with self.db_pool.pool.acquire() as conn:
            try:
                await conn.execute(
                    "INSERT INTO pessoas (id, apelido, nome, nascimento, stack) VALUES ($1, $2, $3, $4, $5)",
                    str(person.id), person.apelido, person.nome, person.nascimento, person.stack
                )
            except asyncpg.UniqueViolationError:
                raise HTTPException(status_code=400, detail="Person already exists")

    async def get_person_by_id(self, person_id: uuid.UUID):
        async with self.db_pool.pool.acquire() as conn:
            result = await conn.fetchrow("SELECT id, apelido, nome, nascimento, stack FROM pessoas WHERE id = $1", person_id)
            if result:
                return Person(result['apelido'], result['nome'], result['nascimento'], result['stack'])
        return None

    async def search_person_by_term(self, term: str):
        search_term = f"%{term}%"
        async with self.db_pool.pool.acquire() as conn:
            results = await conn.fetch("SELECT id, apelido, nome, nascimento, stack FROM pessoas WHERE apelido ILIKE $1 OR nome ILIKE $1 OR $2 = ANY(stack)", search_term, term)
            return [Person(result['apelido'], result['nome'], result['nascimento'], result['stack']) for result in results]

    async def count_persons(self):
        async with self.db_pool.pool.acquire() as conn:
            return await conn.fetchval("SELECT COUNT(*) FROM pessoas")
