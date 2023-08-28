import uuid
from fastapi import APIRouter, Depends
from src.domain.dto.PersonDto import PessoaDto

from src.infra.handler.PersonHandler import PessoaHandler
from src.infra.repository.PersonRepository import PersonRepository


router = APIRouter()

def get_handler(person_repo=Depends(PersonRepository)):
    return PessoaHandler(person_repo)

@router.post("/pessoas")
async def create_pessoa(pessoa_dto: PessoaDto, handler: PessoaHandler = Depends(get_handler)):
    return handler.create(pessoa_dto)

@router.get("/pessoas/{person_id}")
async def get_pessoa(person_id: uuid.UUID, handler: PessoaHandler = Depends(get_handler)):
    return handler.retrieve(person_id)

@router.get("/pessoas/")
async def search_pessoa(term: str, handler: PessoaHandler = Depends(get_handler)):
    return handler.search(term)

@router.get("/contagem-pessoas/")
async def count_pessoas(handler: PessoaHandler = Depends(get_handler)):
    return handler.count()