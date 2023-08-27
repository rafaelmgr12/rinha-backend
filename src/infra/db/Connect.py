import psycopg2

class PostgresDatabase:
    def __init__(self, config):
        self.config = config
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