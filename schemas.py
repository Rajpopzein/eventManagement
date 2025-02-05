from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class EventStatus(str, Enum):
    scheduled = "scheduled"
    ongoing = "ongoing"
    completed = "completed"
    canceled = "canceled"

class EventCreate(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int

class EventResponse(EventCreate):
    event_id: str
    status: EventStatus

class AttendeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    event_id: str

class AttendeeResponse(AttendeeCreate):
    attendee_id: str
    check_in_status: bool
