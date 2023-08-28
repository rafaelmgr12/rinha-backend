import asyncpg
import uuid
from src.domain.entity.Person import Person
from datetime import datetime
from fastapi import HTTPException

class PersonRepository:

    def __init__(self, db_connection):
        self.db = db_connection
        self.insert_person_stmt = None


    async def prepare_statements(self):
        self.insert_person_stmt = await self.db.conn.prepare(
            "INSERT INTO pessoas (id, apelido, nome, nascimento, stack) VALUES ($1, $2, $3, $4, $5)"
        )

    async def get_person_by_apelido(self, apelido: str):
        result = await self.db.conn.fetchrow("SELECT id, apelido, nome, nascimento, stack FROM pessoas WHERE apelido = $1", apelido)
        if result:
            return Person(result['apelido'], result['nome'], result['nascimento'], result['stack'])
        return None

    async def add_person(self, person: Person):
        try:
            if not self.insert_person_stmt:
                await self.prepare_statements()
            nascimento_date = datetime.strptime(person.nascimento, '%Y-%m-%d').date()

            await self.insert_person_stmt.fetch(str(person.id), person.apelido, person.nome, nascimento_date, person.stack)
        except asyncpg.UniqueViolationError:
            raise HTTPException(status_code=400, detail="Person already exists")
        return None

    async def get_person_by_id(self, person_id: uuid.UUID):
        result = await self.db.conn.fetchrow("SELECT id, apelido, nome, nascimento, stack FROM pessoas WHERE id = $1", person_id)
        if result:
            return Person(result['apelido'], result['nome'], result['nascimento'], result['stack'])
        return None

    async def search_person_by_term(self, term: str):
        results = await self.db.conn.fetch("SELECT id, apelido, nome, nascimento, stack FROM pessoas WHERE apelido ILIKE $1 OR nome ILIKE $2 OR $3 = ANY(stack)", f"%{term}%", f"%{term}%", term)
        return [Person(result['apelido'], result['nome'], result['nascimento'], result['stack']) for result in results]

    async def count_persons(self):
        return await self.db.conn.fetchval("SELECT COUNT(*) FROM pessoas")
