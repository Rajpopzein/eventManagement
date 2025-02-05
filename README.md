# Event Management API

## Description

This is an Event Management API built with FastAPI. The API allows the creation of events, attendee registration, and attendee check-in. It also supports bulk check-in functionality for multiple attendees.

## Features

- **Create Event**: Allows the creation of events with details like name, description, time, location, and maximum attendees.
- **Register Attendee**: Allows users to register for events, with attendee details including name, email, phone number, and the event they are attending.
- **Check-in Attendee**: Allows attendees to check in to events.
- **Bulk Check-in**: Upload a CSV file to check in multiple attendees at once.
- **Event Status**: Events automatically mark their status as `completed` when the `end_time` has passed.

## Technologies

- **FastAPI**: For building the API.
- **MongoDB**: For data storage.
- **Pytest**: For testing the application.
- **Python**: For backend logic.

## Prerequisites

Ensure you have the following installed:

- Python 3.8+
- MongoDB (local or cloud instance)
- pip

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/event-management-api.git
cd event-management-api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
uvicorn main:app --reload
```

## API Endpoints

### 1. Create Event
- **Endpoint:** `POST /events/`
- **Description:** Create a new event.
- **Request Body:**
```json
{
  "name": "Event Name",
  "description": "Event Description",
  "start_time": "2025-02-10T10:00:00",
  "end_time": "2025-02-10T14:00:00",
  "location": "Event Location",
  "max_attendees": 100
}
```

### 2. Register Attendee
- **Endpoint:** `POST /attendees/`
- **Description:** Register a new attendee for an event.
- **Request Body:**
```json
{
  "name": "John Doe",
  "email": "johndoe@example.com",
  "phone": "1234567890",
  "event_id": "event123"
}
```

### 3. Check-in Attendee
- **Endpoint:** `POST /check-in/`
- **Description:** Check-in an attendee.
- **Request Body:**
```json
{
  "attendee_id": "attendee123"
}
```

### 4. Bulk Check-in
- **Endpoint:** `POST /bulk-check-in/`
- **Description:** Upload a CSV file to check in multiple attendees.
- **Request Body:** CSV file containing attendee IDs.

## Running Tests

Run tests using Pytest:

```bash
pytest
```


