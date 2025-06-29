from fastapi.concurrency import run_in_threadpool
from models.chat import Chat
from database.db_connection import db
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Optional
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


# ⚠️ Secure your key using environment variables in production!
# Make sure API key is set
api_key = os.getenv("groq_apikey")
if not api_key:
    raise ValueError("Missing 'groq_api' environment variable")

client = Groq(api_key=api_key)

chat_collection = db["chats"]

# ------------------- Answer Generation -------------------

def generate_answer(question: str) -> str:
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": question}],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    answer = ""
    for chunk in completion:
        answer += chunk.choices[0].delta.content or ""
    return answer

# ------------------- Save Chat -------------------

async def save_chat(chat: Chat):
    chat_dict = chat.dict()
    try:
        chat_dict["user_id"] = ObjectId(chat.user_id)
    except Exception:
        raise ValueError("Invalid user_id format")

    chat_dict["timestamp"] = datetime.utcnow()

    # Generate LLM response in background thread
    answer = await run_in_threadpool(generate_answer, chat.message)
    chat_dict["response"] = answer

    result = chat_collection.insert_one(chat_dict)

    # Serialize inserted chat
    saved_doc = chat_collection.find_one({"_id": result.inserted_id})
    saved_doc["id"] = str(saved_doc["_id"])
    saved_doc["user_id"] = str(saved_doc["user_id"])
    del saved_doc["_id"]

    return {"message": "Chat saved successfully", "chat": saved_doc, "success":True}

# ------------------- Get Chats by User & Date -------------------

def get_chats_by_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise ValueError("Invalid user_id")

    user_obj_id = ObjectId(user_id)
    query = {"user_id": user_obj_id}

    
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    query["timestamp"] = {"$gte": today, "$lt": tomorrow}

    chats_cursor = chat_collection.find(query)
    chats = []
    for chat in chats_cursor:
        chat["id"] = str(chat["_id"])
        del chat["_id"]
        chat["user_id"] = str(chat["user_id"])
        chats.append(chat)

    return chats
