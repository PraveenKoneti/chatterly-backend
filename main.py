from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scheduler.cleanup import start_scheduler

from routes.user import router as user_Router
from routes.chat import router as chat_Router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_Router)
app.include_router(chat_Router)

@app.on_event("startup")
def startup_event():
    start_scheduler()

# Optional root route for Render health check
@app.get("/")
def read_root():
    return {"message": "Chatterly backend is running!"}
