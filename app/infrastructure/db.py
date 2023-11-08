# module import
import pymongo

# config import
from infrastructure.config import get_settings


def connect():
    """
    dependency inject database session to repositories
    :return: database session
    :rtype: Generator
    """
    # create a new client and connect to the server
    return pymongo.MongoClient(get_settings().assemble_db_connection())
