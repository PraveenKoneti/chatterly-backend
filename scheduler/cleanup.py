from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pymongo import MongoClient
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
MONGODB_URL = os.getenv("MONGODB_URL")  # e.g. "mongodb://localhost:27017"
MONGO_DB = os.getenv("MONGO_DB")        # e.g. "chatterly_db"

# Validate env vars
if not MONGODB_URL or not MONGO_DB:
    raise EnvironmentError("Missing MONGODB_URL or MONGO_DB in .env file")

# Connect to MongoDB
client = MongoClient(MONGODB_URL)
db = client[MONGO_DB]
chat_collection = db["chats"]

def delete_chats():
    try:
        result = chat_collection.delete_many({})
        print(f"✅ Deleted {result.deleted_count} chat records at 1:00 AM.")
    except Exception as e:
        logging.error(f"❌ Failed to delete chats: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Run every day at 1:00 AM
    scheduler.add_job(delete_chats, CronTrigger(hour=1, minute=0))
    scheduler.start()
    print("🚀 Scheduler started.")
