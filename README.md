# Event Management REST API
This project is a Django-based REST API that manages events like conferences and meetups. It allows users to create, view, update, and delete events and supports user registrations for those events.

## Features
Features
- User Registration & Authentication: Users can register and authenticate using JSON Web Tokens (JWT).
- CRUD Operations for Events: Create, Read, Update, and Delete events.
- Event Registration: Users can register for events.
- Email Notifications: Users receive email notifications upon registering for an event.
- Search & Filtering: Events can be filtered and searched by title, date, and location (optional).

## API Endpoints
- Swagger
    -  /api/schema/swagger-ui/ — swagger for API

- Users
    - POST /api/register/ — Register a new user.
    - POST /api/login/ — Authenticate a user and return a token.


- Events
    - GET /api/events/ — List all events.
    - POST /api/events/ — Create a new event (authentication required).
    - GET /api/events/{id}/ — Retrieve details of a specific event.
    - PUT /api/events/{id}/ — Update an event (authentication required).
    - DELETE /api/events/{id}/ — Delete an event (authentication required).


- Event Registration
    - POST /api/register_event/ — Register for an event (authentication required).


- Event Search and Filtering (Bonus)
    - GET /api/events/?search={query} — Search events by title, date, or location.

Installation
Clone the repository:

```bash
git clone https://github.com/yourusername/event-management.git
cd event-management
Install dependencies: This project uses Poetry. Install the dependencies by running:
```

```bash
poetry install
Environment variables: Create a .env file in the project root and configure the following variables:

POSTGRES_DB=your_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```

This project supports Docker. To run the application using Docker:

Build the Docker image:

```bash
docker compose -up build
```


