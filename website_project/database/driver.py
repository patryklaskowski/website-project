from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from typing import Dict, Optional, Iterable
import os
import pandas as pd

load_dotenv()

class MongoDb:
    def __init__(
            self,
            db_name: Optional[str] = None,
            username: Optional[str] = None,
    ) -> None:

        self.db_name = db_name if db_name is not None else os.environ["MONGODB_DB_NAME"]
        self.username = username if username is not None else os.environ["MONGODB_USERNAME"]
        self.uri = self.create_uri(self.username, os.environ["MONGODB_PASSWORD"])

        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client[self.db_name]

    @staticmethod
    def create_uri(username: str, password: str) -> str:
        return (
            "mongodb+srv://"
            f"{username}:{password}@"
            "website-project-mongodb.g8jumkz.mongodb.net/"
            "?retryWrites=true&w=majority"
        )

    def save_record(self, collection_name: str, data: Dict) -> str:
        collection = self.db[collection_name]
        _id = collection.insert_one(data)

        return _id.inserted_id

    def read_all(self, collection_name: str, columns: Optional[Iterable[str]] = None) -> pd.DataFrame:
        columns = set([] if columns is None else columns)
        columns = {col: 1 for col in columns}
        columns["_id"] = 0  # Don't show id

        collection = self.db[collection_name]

        cursor = collection.find({}, projection=columns)

        return pd.DataFrame(list(cursor))
