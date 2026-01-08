# EventRELY - Event Reminder System

A backend for event reminders application built with FastAPI and Supabase connection.

[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue.svg)](https://www.postgresql.org/docs/17/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🏗️ Architecture

- **Domain-Driven Design (DDD)**: Business logic isolated from infrastructure
- **CQRS**: Clear separation between Commands (write) and Queries (read)
- **Clean Architecture**: 4-layer structure with dependency inversion
- **Aggregate Pattern**: Event as the Aggregate Root
- **Repository Pattern**: Abstract data access

## 🚀 Links

- **Swagger UI**: [https://eventrely-api-platform.azurewebsites.net/docs](https://eventrely-api-platform.azurewebsites.net/docs)
- **ReDocly UI**: [https://eventrely-api-platform.azurewebsites.net/redoc](https://eventrely-api-platform.azurewebsites.net/redoc)
- **Status Page**: [https://stats.uptimerobot.com/MBVmW8Pm1L](https://stats.uptimerobot.com/MBVmW8Pm1L)

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
