from fastapi import FastAPI
from database import init_db
from routes.events import router as event_router
from routes.attendees import router as attendee_router

app = FastAPI(title="Event Management API")

@app.on_event("startup")
async def startup_db():
    await init_db()

app.include_router(event_router)
app.include_router(attendee_router)
