import pandas as pd
import sqlite3


class Db:
    def __init__(self, db_path: str):

        self.db_path = db_path

    def read_table(self, name: str) -> pd.DataFrame:
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class SqliteDb(Db):
    def __init__(self, db_path: str = ":memory:") -> None:
        super().__init__(db_path)
        self.con = sqlite3.connect(self.db_path)

    def __enter__(self):
        print("DB connection open...")
        self._cursor = self.con.cursor()

        return self._cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self._cursor.close()
        print("DB connection closed")



swimming = {
    "name": "swimming",
    "date": "date",
    "distance": "float",
    "time_total": "int",
    "description": "str",
    "create_query": (
        "CREATE TABLE IF NOT EXISTS swimming ("
        "id INTEGER PRIMARY KEY,"
        "date TEXT NOT NULL,"
        "distance FLOAT NOT NULL,"
        "time_total INT NOT NULL,"
        "description TEXT"
        ")"
    ),
    "select_all": "SELECT * FROM swimming;"
}


if __name__ == "__main__":
    db = SqliteDb()
    with db as conn:
        conn.execute(swimming["create_query"])

        for row in conn.execute(swimming["select_all"]).fetchall():
            print(row)
