# main.py or database.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")  # Corrected key
MONGO_DB = os.getenv("MONGO_DB")

client = MongoClient(MONGODB_URL)
db = client[MONGO_DB]
