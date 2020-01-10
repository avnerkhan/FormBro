import sqlite3
from sqlite3 import Error, Binary
from uuid import uuid4


class DatabaseAPI:
    __db_dir__ = "../db/"

    def __init__(self, table_name: str, db_name: str):
        self.table_name = table_name
        self.db_name = db_name
        self.__db_path__ = self.__db_dir__ + self.db_name
        self.connection = None
        self.cursor = None
        self.connect_db()
        self.create_table()

    def insert_into_table(self, name: str, picture: Binary) -> None:
        """ Generate a random id, and set our intial class to 0. We can reset later """

        self.cursor.execute(self.insert_into_table_query(), [
                            str(uuid4()), name, 0, picture])
        self.connection.commit()

    def insert_into_table_query(self) -> str:
        return """INSERT INTO """ + self.table_name + """ (id,name, class, picture) VALUES (?, ?, ?, ?);"""

    def create_table_query(self) -> str:
        return """CREATE TABLE IF NOT EXISTS """ + self.table_name + """ (
                                    id string PRIMARY KEY ,
                                    name text NOT NULL,
                                    class integer,
                                    picture blob
                                );"""

    def create_table(self) -> None:
        self.cursor.execute(self.create_table_query())
        self.connection.commit()

    def close_connection(self) -> None:
        if self.connection:
            self.connection.close()

    def connect_db(self) -> None:
        try:
            self.connection = sqlite3.connect(self.__db_path__)
            self.cursor = self.connection.cursor()
        except Error as e:
            print(e)
