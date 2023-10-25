import pymongo

from config import get_settings

# connect to MongoDB server
client = pymongo.MongoClient(get_settings().assemble_db_connection())

# select a database
db = client[get_settings().MONGO_DB]

# export ok_data collection
ok_data_collection = db["ok_data_collection"]
# export error_data collection
error_data_collection = db["error_data"]
