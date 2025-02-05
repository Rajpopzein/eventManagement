from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
import csv
from database import db
from schemas import AttendeeCreate, AttendeeResponse
from bson import ObjectId

router = APIRouter(prefix="/attendees", tags=["Attendees"])

@router.post("/", response_model=AttendeeResponse)
async def register_attendee(attendee: AttendeeCreate):
    event = await db.events.find_one({"event_id": attendee.event_id})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    attendee_count = await db.attendees.count_documents({"event_id": attendee.event_id})
    if attendee_count >= event["max_attendees"]:
        raise HTTPException(status_code=400, detail="Event is full")

    new_attendee = attendee.dict()
    new_attendee["attendee_id"] = str(ObjectId())
    new_attendee["check_in_status"] = False

    await db.attendees.insert_one(new_attendee)
    return new_attendee

@router.put("/{attendee_id}/checkin")
async def checkin_attendee(attendee_id: str):
    updated_attendee = await db.attendees.find_one_and_update(
        {"attendee_id": attendee_id},
        {"$set": {"check_in_status": True}},
        return_document=True
    )

    if not updated_attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")

    return {"message": "Check-in successful"}

@router.post("/bulk-checkin")
async def bulk_checkin(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

    content = await file.read()
    decoded_content = content.decode('utf-8').splitlines()
    csv_reader = csv.DictReader(decoded_content)

    updated_count = 0
    not_found_ids = []

    for row in csv_reader:
        attendee_id = row.get("attendee_id")
        if attendee_id:
            result = await db.attendees.update_one(
                {"attendee_id": attendee_id},
                {"$set": {"check_in_status": True}}
            )
            if result.modified_count:
                updated_count += 1
            else:
                not_found_ids.append(attendee_id)

    return {
        "message": f"Bulk check-in completed. {updated_count} attendees checked in.",
        "not_found_ids": not_found_ids
    }