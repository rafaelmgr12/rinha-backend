from pydantic import BaseModel, constr
from typing import List, Optional
from pydantic import BaseModel


class PessoaDto(BaseModel):
    apelido: constr(max_length=32)
    nome: constr(max_length=100)
    nascimento: str
    stack: Optional[List[constr(max_length=32)]]