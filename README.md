# EventRELY - Event Reminder System

A backend for event reminders built with FastAPI, following Domain-Driven Design (DDD) and CQRS principles.

## 🏗️ Architecture

- **Domain-Driven Design (DDD)**: Business logic isolated from infrastructure
- **CQRS**: Clear separation between Commands (write) and Queries (read)
- **Clean Architecture**: 4-layer structure with dependency inversion
- **Aggregate Pattern**: Event as the Aggregate Root
- **Repository Pattern**: Abstract data access

## 🚀 Quick Start

### Prerequisites

- Python 3.13
- PostgreSQL 17

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd eventrely
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Start PostgreSQL**
   ```bash
   # Using Docker
   docker run --name eventrely-db \
     -e POSTGRES_USER=user \
     -e POSTGRES_PASSWORD=password \
     -e POSTGRES_DB=reminder_db \
     -p 5432:5432 \
     -d postgres:16
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Commands (Write Operations)

- `POST /api/v1/events` - Create new event
- `PUT /api/v1/events/{id}` - Update event
- `DELETE /api/v1/events/{id}` - Delete event
- `POST /api/v1/events/{id}/complete` - Mark as completed
- `POST /api/v1/events/{id}/cancel` - Cancel event

### Queries (Read Operations)

- `GET /api/v1/events/{id}` - Get event by ID
- `GET /api/v1/events/user/{user_id}` - Get all user events
- `GET /api/v1/events/user/{user_id}/date/{date}` - Get events by date
- `GET /api/v1/events/user/{user_id}/upcoming` - Get upcoming events

## 📝 Example Requests

### Create Event

```bash
curl -X POST http://localhost:8000/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "title": "Pagar alquiler",
    "event_date": "2025-12-22T10:00:00",
    "description": "Recordatorio mensual"
  }'
```

### Get Upcoming Events

```bash
curl http://localhost:8000/api/v1/events/user/user_123/upcoming?limit=10
```

## 🏛️ Domain Model

### Event Aggregate

The `Event` class is the Aggregate Root that:
- Protects business invariants
- Contains domain logic
- Acts as the ORM model (inherits from SQLAlchemy Base)

**Business Rules**:
- Events cannot be scheduled in the past
- Only pending events can be completed
- Completed events cannot be cancelled

### Value Objects

- **EventId**: Represents event identifier with validation
- **EventDate**: Represents event date with business methods
- **ReminderStatus**: Enum for event statuses

### Commands

Immutable data structures representing write intentions:
- `CreateEventCommand`
- `UpdateEventCommand`
- `DeleteEventCommand`

### Queries

Immutable data structures representing read requests:
- `GetEventByIdQuery`
- `GetEventsByDateQuery`
- `GetUpcomingEventsQuery`


## 🔒 Security Notes

**Current State**: No authentication implemented (MVP)

**For Production**, required to be added:
- JWT authentication
- User authorization
- Rate limiting
- Input validation
- HTTPS only

## 📈 Future Enhancements

### Ready to Add:
- [ ] Alembic migrations for production
- [ ] JWT authentication
- [ ] Push notifications
- [ ] Recurring events
- [ ] Event categories/tags
- [ ] Search functionality
- [ ] Event sharing
- [ ] Integration tests
- [ ] Docker Compose setup

## 🛠️ Technology Stack

- **FastAPI**: Modern async web framework
- **SQLAlchemy 2.0**: Async ORM
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

## 📚 Architecture Patterns

### DDD (Domain-Driven Design)
- Bounded contexts
- Aggregates and entities
- Value objects
- Domain events

### CQRS (Command Query Responsibility Segregation)
- Separate write (commands) and read (queries) models
- CommandServiceImpl handles writes
- QueryServiceImpl handles reads

### Repository Pattern
- Abstract data access
- Interface in domain layer
- Implementation in infrastructure layer

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests
4. Submit a pull request

## 📄 License

MIT License

## 👥 Author

- Oscar Gabriel Aranda Vallejos

---