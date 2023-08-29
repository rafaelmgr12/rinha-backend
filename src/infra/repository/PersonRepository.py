import asyncpg
import uuid
from src.domain.entity.Person import Person
from datetime import datetime
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
            nascimento_date = datetime.strptime(person.nascimento, '%Y-%m-%d').date()
            try:
                await conn.execute(
                    "INSERT INTO pessoas (id, apelido, nome, nascimento, stack) VALUES ($1, $2, $3, $4, $5)",
                    str(person.id), person.apelido, person.nome, nascimento_date, person.stack
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
        async with self.db_pool.pool.acquire() as conn:
            results = await conn.fetch("SELECT id, apelido, nome, nascimento, stack FROM pessoas WHERE apelido ILIKE $1 OR nome ILIKE $2 OR $3 = ANY(stack)", f"%{term}%", f"%{term}%", term)
            return [Person(result['apelido'], result['nome'], result['nascimento'], result['stack']) for result in results]

    async def count_persons(self):
        async with self.db_pool.pool.acquire() as conn:
            return await conn.fetchval("SELECT COUNT(*) FROM pessoas")
