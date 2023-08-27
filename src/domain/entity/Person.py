import uuid

from typing import Optional,List


class Person:

    __id_: uuid
    __apelido: str
    __nome: str
    __nascimento: str
    __stack:  Optional[List[str]]

    def __init__(self, id_: uuid, apelido: str, nome: str, nascimento: str, stack: Optional[List[str]]):
        self.__id_ = id_
        self.__apelido = apelido
        self.__nome = nome
        self.__nascimento = nascimento
        self.__stack = stack