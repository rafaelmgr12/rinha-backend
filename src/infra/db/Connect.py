import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()

class PostgresDatabase:
    def __init__(self):
        self.config = {
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
            "dbname": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD")
        }
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.config)
            self.cursor = self.conn.cursor()
            print("Conectado ao banco de dados PostgreSQL com sucesso!")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Conexão ao banco de dados fechada.")