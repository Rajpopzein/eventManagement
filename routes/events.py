from fastapi import APIRouter, HTTPException, BackgroundTasks
from database import db
from schemas import EventCreate, EventResponse, EventStatus
from bson import ObjectId
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/events", tags=["Events"])

def mark_event_as_completed(event_id: str):
    """Function to update event status to completed"""
    current_time = datetime.utcnow()
    event = db.events.find_one({"event_id": event_id})
    if event and event.get("end_time") and event["end_time"] < current_time:
        db.events.update_one(
            {"event_id": event_id},
            {"$set": {"status": EventStatus.completed}}
        )

@router.post("/", response_model=EventResponse)
async def create_event(event: EventCreate):
    new_event = event.dict()
    new_event["status"] = EventStatus.scheduled
    new_event["event_id"] = str(ObjectId())

    await db.events.insert_one(new_event)
    return {"message": "Event created successfully", "event": new_event}

@router.get("/", response_model=list[EventResponse])
async def list_events(status: Optional[EventStatus] = None, background_tasks: BackgroundTasks = None):
    query = {} if status is None else {"status": status}
    events = await db.events.find(query).to_list(100)

    current_time = datetime.utcnow()
    updated_count = 0
    for event in events:
        if event.get("end_time") and event["end_time"] < current_time and event["status"] != EventStatus.completed:
            # Run the background task to mark the event as completed
            if background_tasks:
                background_tasks.add_task(mark_event_as_completed, event["event_id"])
            updated_count += 1

    return {
        "message": f"{updated_count} events marked as completed.",
        "events": events
    }
