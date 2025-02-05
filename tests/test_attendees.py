import pytest

@pytest.mark.asyncio
async def test_register_attendee(client):
    # Create an event with limited capacity
    event_response = await client.post("/events/", json={
        "name": "Music Fest",
        "description": "Live Music Event",
        "start_time": "2025-06-10T18:00:00",
        "end_time": "2025-06-10T22:00:00",
        "location": "Los Angeles",
        "max_attendees": 2
    })
    event = event_response.json()

    # Register the first attendee
    attendee_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone_number": "1234567890",
        "event_id": event["event_id"]
    }
    response = await client.post("/attendees/", json=attendee_data)
    assert response.status_code == 200
    assert response.json()["email"] == "john@example.com"

    # Register the second attendee
    attendee_data = {
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice@example.com",
        "phone_number": "0987654321",
        "event_id": event["event_id"]
    }
    response = await client.post("/attendees/", json=attendee_data)
    assert response.status_code == 200

    # Try to register a third attendee and expect a failure (event full)
    attendee_data = {
        "first_name": "Bob",
        "last_name": "Brown",
        "email": "bob@example.com",
        "phone_number": "1122334455",
        "event_id": event["event_id"]
    }
    response = await client.post("/attendees/", json=attendee_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Event is full"

@pytest.mark.asyncio
async def test_checkin_attendee(client):
    event_response = await client.post("/events/", json={
        "name": "Tech Meetup",
        "description": "Networking event",
        "start_time": "2025-06-15T18:00:00",
        "end_time": "2025-06-15T22:00:00",
        "location": "San Francisco",
        "max_attendees": 50
    })
    event = event_response.json()

    # Register an attendee
    attendee_response = await client.post("/attendees/", json={
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "phone_number": "9876543210",
        "event_id": event["event_id"]
    })
    attendee = attendee_response.json()

    # Check-in the attendee
    checkin_response = await client.put(f"/attendees/{attendee['attendee_id']}/checkin")
    assert checkin_response.status_code == 200
    assert checkin_response.json() == {"message": "Check-in successful"}

    # Try to check-in again and expect an error (already checked-in)
    checkin_response = await client.put(f"/attendees/{attendee['attendee_id']}/checkin")
    assert checkin_response.status_code == 400
    assert checkin_response.json()["detail"] == "Attendee already checked in"

@pytest.mark.asyncio
async def test_register_attendee_with_invalid_data(client):
    event_response = await client.post("/events/", json={
        "name": "Invalid Event",
        "description": "Event with invalid attendee data",
        "start_time": "2025-06-10T18:00:00",
        "end_time": "2025-06-10T22:00:00",
        "location": "Los Angeles",
        "max_attendees": 2
    })
    event = event_response.json()

    # Missing email
    attendee_data = {
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "1234567890",
        "event_id": event["event_id"]
    }
    response = await client.post("/attendees/", json=attendee_data)
    assert response.status_code == 422  # Unprocessable Entity

    # Missing phone number
    attendee_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "event_id": event["event_id"]
    }
    response = await client.post("/attendees/", json=attendee_data)
    assert response.status_code == 422  # Unprocessable Entity
