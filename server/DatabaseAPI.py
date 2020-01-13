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

    def insert_into_table(self, user_email: str, name: str, class_type: int, picture: any) -> None:
        """ Generate a random id, the rest is simply using paramters """
        try:
            self.cursor.execute(self.insert_into_table_query(), [
                                str(uuid4()), user_email, name, class_type, Binary(picture)])
            self.connection.commit()
        except:
            print("Error in inserting into table.")

    def insert_into_table_query(self) -> str:
        return """INSERT INTO """ + self.table_name + """ (id, userEmail, name, class, picture) VALUES (?, ?, ?, ?);"""

    def create_table_query(self) -> str:
        return """CREATE TABLE IF NOT EXISTS """ + self.table_name + """ (
                                    id string PRIMARY KEY ,
                                    userEmail string NOT NULL
                                    name text NOT NULL,
                                    class integer NOT NULL,
                                    picture blob NOT NULL
                                );"""

    def create_table(self) -> None:
        try:
            self.cursor.execute(self.create_table_query())
            self.connection.commit()
        except:
            print("Error in creating table.")

    def close_connection(self) -> None:
        if self.connection:
            try:
                self.connection.close()
            except:
                print("Error in closing connection")

    def connect_db(self) -> None:
        try:
            self.connection = sqlite3.connect(self.__db_path__)
            self.cursor = self.connection.cursor()
        except Error as e:
            print(e)
