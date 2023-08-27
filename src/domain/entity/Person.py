import uuid

from typing import Optional,List


class Person:

    __id_: uuid
    __apelido: str
    __nome: str
    __nascimento: str
    __stack:  Optional[List[str]]

    def __init__(self, apelido: str, nome: str, nascimento: str, stack: Optional[List[str]]):
        self.__id_ = uuid.uuid4()
        self.__apelido = apelido
        self.__nome = nome
        self.__nascimento = nascimento
        self.__stack = stack
   
    @property
    def id(self):
        return self.__id_

    @property
    def apelido(self):
        return self.__apelido

    @property
    def nome(self):
        return self.__nome

    @property
    def nascimento(self):
        return self.__nascimento

    @property
    def stack(self):
        return self.__stack