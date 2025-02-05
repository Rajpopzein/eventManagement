import pytest
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_create_event(client):
    # Valid event data
    event_data = {
        "name": "Tech Conference",
        "description": "Annual tech event",
        "start_time": datetime.utcnow().isoformat(),
        "end_time": (datetime.utcnow() + timedelta(hours=2)).isoformat(),
        "location": "New York",
        "max_attendees": 100
    }
    response = await client.post("/events/", json=event_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == event_data["name"]
    assert data["status"] == "scheduled"

@pytest.mark.asyncio
async def test_list_events(client):
    response = await client.get("/events/")
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)

    # Check if events are correctly marked as completed if their end_time has passed
    for event in events:
        if event["end_time"] < datetime.utcnow().isoformat():
            assert event["status"] == "completed"

@pytest.mark.asyncio
async def test_create_event_with_invalid_data(client):
    # Invalid event data with missing end_time
    event_data = {
        "name": "Invalid Event",
        "description": "Missing end time",
        "start_time": datetime.utcnow().isoformat(),
        "location": "New York",
        "max_attendees": 50
    }
    response = await client.post("/events/", json=event_data)
    assert response.status_code == 422  # Unprocessable Entity

@pytest.mark.asyncio
async def test_event_status_update(client):
    # Create an event and simulate the time passing
    event_data = {
        "name": "Expired Event",
        "description": "This event will expire soon",
        "start_time": datetime.utcnow().isoformat(),
        "end_time": (datetime.utcnow() - timedelta(hours=1)).isoformat(),  # Event already expired
        "location": "New York",
        "max_attendees": 100
    }
    response = await client.post("/events/", json=event_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"  # Automatically marked as completed after expiration
