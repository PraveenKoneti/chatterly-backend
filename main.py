from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scheduler.cleanup import start_scheduler

from routes.user import router as user_Router
from routes.chat import router as chat_Router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],                # Allow all HTTP methods
    allow_headers=["*"],                # Allow all headers
)

app.include_router(user_Router)
app.include_router(chat_Router)

@app.on_event("startup")
def startup_event():
    start_scheduler()