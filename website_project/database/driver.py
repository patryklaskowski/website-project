from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from typing import Dict
import os


class MongoDatabase:
    def __init__(self) -> None:
        self.assert_requirements()

        self.db_name = os.environ["MONGODB_DB_NAME"]

        self.client = MongoClient(
            self.create_uri(
                os.environ['MONGODB_USERNAME'],
                os.environ['MONGODB_PASSWORD']
            ),
            server_api=ServerApi('1'))
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

    def read_all(self, collection_name: str) -> Dict:
        return {}

    @staticmethod
    def assert_requirements() -> None:
        _required_envs = ("MONGODB_DB_NAME", "MONGODB_USERNAME", "MONGODB_PASSWORD")
        assert all(env_var in os.environ for env_var in _required_envs), \
            f"All required env variables have to be defined: {_required_envs}"
