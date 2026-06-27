from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import init_db
from routers import slots, sessions, analytics
from stream import router as stream_router
import os

app = FastAPI(title="Smart Parking Monitor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("../evidence", exist_ok=True)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"status": "Smart Parking Monitor API is running"}

app.include_router(slots.router, prefix="/api/slots", tags=["Parking Slots"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(stream_router, prefix="/api/video", tags=["Video Stream"])