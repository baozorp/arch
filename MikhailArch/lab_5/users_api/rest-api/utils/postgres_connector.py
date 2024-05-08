import psycopg2
import time


class PostgresConnector:

    def __init__(self, db_name: str = 'postgres') -> None:
        self.db_name = db_name
        self.user = 'baozorp'
        self.password = 'baozorp'
        self.host = 'postgres'
        self.port = '5432'
        while True:
            try:
                self.conn = psycopg2.connect(dbname=self.db_name, user=self.user,
                                             password=self.password, host=self.host, port=self.port)
                break
            except:
                print("Can't connect to postgres")
                time.sleep(5)

    def get_cursor(self) -> psycopg2.extensions.cursor:

        self.cur = self.conn.cursor()
        return self.cur

    def close_connection(self):
        self.cur.close()
        if self.conn:
            self.conn.close()
