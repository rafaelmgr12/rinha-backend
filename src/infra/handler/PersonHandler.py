from datetime import datetime
from pydantic import ValidationError
from fastapi import HTTPException
from src.domain.entity.Person import Person
from src.infra.repository.PersonRepository import PersonRepository

class PessoaHandler:

    def __init__(self, person_repo: PersonRepository):
        self.person_repo = person_repo

    async def create(self, pessoa_dto):
        try:
            person = Person(pessoa_dto.apelido, pessoa_dto.nome, pessoa_dto.nascimento, pessoa_dto.stack)
            if not PessoaHandler.__is_valid_date(person.nascimento):
                raise HTTPException(status_code=400, detail="Invalid date format")
            apelido = await self.person_repo.get_person_by_apelido(person.apelido)
            if apelido:
                raise HTTPException(status_code=400, detail="Apelido already exists")
            await self.person_repo.add_person(person)
            return {"id": person.id}
        except ValidationError:
            raise HTTPException(status_code=400, detail="Data validation error")

    async def retrieve(self, person_id):
        person = await self.person_repo.get_person_by_id(person_id)
        if person:
            return {
                "id": person.id,
                "apelido": person.apelido,
                "nome": person.nome,
                "nascimento": person.nascimento,
                "stack": person.stack
            }
        raise HTTPException(status_code=404, detail="Person not found")

    async def search(self, term):
        persons = await self.person_repo.search_person_by_term(term)
        return [{"id": person.id, "apelido": person.apelido, "nome": person.nome, "nascimento": person.nascimento, "stack": person.stack} for person in persons]

    async def count(self):
        return {"count": await self.person_repo.count_persons()}
    
    @staticmethod
    def __is_valid_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
