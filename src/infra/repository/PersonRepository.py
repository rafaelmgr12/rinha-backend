import uuid
import psycopg2

from src.domain.entity.Person import Person

class PersonRepository:

    def __init__(self, db_connection):
        self.db = db_connection    
        self.db.cursor.execute("PREPARE person_insert AS INSERT INTO pessoas (id, apelido, nome, nascimento, stack) VALUES ($1, $2, $3, $4, $5)")


    def get_person_by_apelido(self, apelido: str):
        self.db.cursor.execute("SELECT id, apelido, nome, nascimento, stack FROM pessoas WHERE apelido = %s", (apelido,))
        result = self.db.cursor.fetchone()
        if result:
            return Person(result[1], result[2], result[3], result[4])
        return None

    def add_person(self, person: Person):
        try:
            self.db.cursor.execute("EXECUTE person_insert (%s, %s, %s, %s, %s)", (str(person.id), person.apelido, person.nome, person.nascimento, person.stack))
            self.db.conn.commit()
        except psycopg2.errors.UniqueViolation:
            self.db.conn.rollback()
            
        return None

    def get_person_by_id(self, person_id: uuid.UUID):
        self.db.cursor.execute("SELECT id, apelido, nome, nascimento, stack FROM pessoas WHERE id = %s", (person_id,))
        result = self.db.cursor.fetchone()
        if result:
            return Person(result[1], result[2], result[3], result[4])
        return None

    def search_person_by_term(self, term: str):
        named_cursor = self.db.conn.cursor('named_cursor')
        named_cursor.execute(
            "SELECT id, apelido, nome, nascimento, stack FROM pessoas WHERE apelido ILIKE %s OR nome ILIKE %s OR %s = ANY(stack)",
            (f"%{term}%", f"%{term}%", term)
        )
        results = named_cursor.fetchall()
        persons = [Person(result[1], result[2], result[3], result[4]) for result in results]
        return persons



    def count_persons(self):
        self.db.cursor.execute("SELECT COUNT(*) FROM pessoas")
        return self.db.cursor.fetchone()[0]
