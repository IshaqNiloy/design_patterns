import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()


class ConnectionPool:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConnectionPool, cls).__new__(cls)
            cls._instance.initialize_connection_pool()
            return cls._instance

        return cls._instance

    def initialize_connection_pool(self):
        db_params = {
            'database': os.getenv('DATABASE_NAME'),
            'user': os.getenv('DATABASE_USER'),
            'password': os.getenv('DATABASE_PASSWORD'),
            'host': os.getenv('DATABASE_HOST'),
            'port': os.getenv('DATABASE_PORT')
        }

        self.connection_pool = psycopg2.pool.SimpleConnectionPool(1, 5, **db_params)

    def get_connection(self):
        return self.connection_pool.getconn()

    def release_connection(self, connection):
        self.connection_pool.putconn(connection)


if __name__ == '__main__':
    pool = ConnectionPool()
    conn1 = pool.get_connection()

    if conn1:
        print('Connection 1 acquired')
        cursor1 = conn1.cursor()
        cursor1.execute("SELECT * FROM movie_movie")
        result = cursor1.fetchall()
        print(result)
        cursor1.close()
        pool.release_connection(conn1)

    conn2 = pool.get_connection()

    if conn2:
        print('Connection 2 acquired')
        cursor2 = conn2.cursor()
        cursor2.execute("SELECT * FROM user_review_userreview")
        result = cursor2.fetchall()
        print(result)
        cursor2.close()
        pool.release_connection(conn2)


