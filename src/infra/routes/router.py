import uuid
from fastapi import APIRouter, Depends, Response
from src.domain.dto.PersonDto import PessoaDto
from src.infra.db.Connect import get_db,PostgresDatabase

from src.infra.handler.PersonHandler import PessoaHandler
from src.infra.repository.PersonRepository import PersonRepository
from fastapi import HTTPException


router = APIRouter()

def get_repository(db: PostgresDatabase = Depends(get_db)):
    return PersonRepository(db)


def get_handler(repo: PersonRepository = Depends(get_repository)):
    return PessoaHandler(repo)


@router.post("/pessoas", status_code=201 )
async def create_pessoa(response:Response ,pessoa_dto: PessoaDto, handler: PessoaHandler = Depends(get_handler)):
    return await handler.create(pessoa_dto, response)

@router.get("/pessoas/{person_id}")
async def get_pessoa(person_id: str, handler: PessoaHandler = Depends(get_handler)):
    return await handler.retrieve(uuid.UUID(person_id))

@router.get("/pessoas")
async def search_pessoa(term: str=None, handler: PessoaHandler = Depends(get_handler)):
    if term is None:
        raise HTTPException(status_code=400, detail="bad request")
    return await handler.search(term)

@router.get("/contagem-pessoas")
async def count_pessoas(handler: PessoaHandler = Depends(get_handler)):
    return await handler.count()
