from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client["task_manager"]
collection_name = db["tasks"]
print("URI:", uri)
