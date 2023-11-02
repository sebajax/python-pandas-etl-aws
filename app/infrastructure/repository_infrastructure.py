from dataclasses import dataclass

from pymongo import MongoClient
from pymongo.collection import Collection

from infrastructure.config import get_settings


@dataclass
class RepositoryInfrastructure:
    """
    class to represent repository connection to the database
    """
    client: MongoClient

    def __get_collection(self, collection: str) -> Collection:
        # select a database
        db = self.client[get_settings().MONGO_DB]
        # export ok_data collection
        return db[collection]

    def ok_data_collection(self) -> Collection:
        return self.__get_collection("ok_data_collection")

    def error_data_collection(self) -> Collection:
        return self.__get_collection("error_data")
