from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pymongo import MongoClient
import logging

# MongoDB connection (adjust URI and DB/Collection)
client = MongoClient("mongodb://localhost:27017")
db = client["your_db_name"]
chat_collection = db["chats"]




def delete_chats():
    try:
        result = chat_collection.delete_many({})
        print(f"✅ Deleted {result.deleted_count} chat records at 1:00 AM.")
    except Exception as e:
        logging.error(f"❌ Failed to delete chats: {e}")




def start_scheduler():
    scheduler = BackgroundScheduler()
    # CronTrigger: run every day at 1:00 AM
    scheduler.add_job(delete_chats, CronTrigger(hour=1, minute=0))
    scheduler.start()
