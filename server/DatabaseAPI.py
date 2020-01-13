import sqlite3
from sqlite3 import Error
from uuid import uuid4


class DatabaseAPI:
    __db_dir__ = "db/"

    def __init__(self, table_name: str, db_name: str):
        self.table_name = table_name
        self.db_name = db_name
        self.db_path = self.__db_dir__ + self.db_name + ".db"
        self.create_table()

    def insert_into_table(self, user_email: str, name: str, class_type: int) -> None:
        """ Generate a random id, the rest is simply using paramters """
        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.cursor()
                cur.execute(self.insert_into_table_query(), [
                                    str(uuid4()), user_email, name, class_type])
                con.commit()
        except Error as e:
            print(e)
            print("Error in inserting into table.")
    
    def get_all_from_table_query(self) -> str:
        return """SELECT * FROM """ + self.table_name

    def insert_into_table_query(self) -> str:
        return """INSERT INTO """ + self.table_name + """ (id, userEmail, name, class) VALUES (?, ?, ?, ?);"""

    def create_table_query(self) -> str:
        return """CREATE TABLE IF NOT EXISTS """ + self.table_name + """ (
                                    id text PRIMARY KEY ,
                                    userEmail text NOT NULL,
                                    name text NOT NULL,
                                    class integer NOT NULL
                                );"""

    def get_all_from_table(self):
        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.cursor()
                cur.execute(self.get_all_from_table_query())
                return cur.fetchall()
        except Error as e:
            print(e)
            print("Could not retrieve from Database")
    
    def create_table(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.cursor()
                cur.execute(self.create_table_query())
                con.commit()
        except Error as e:
            print(e)
            print("Error in creating table.")
