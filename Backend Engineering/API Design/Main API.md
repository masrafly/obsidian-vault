# Backend API Design
**Version:** v1.0
**Last Updated:** 2024-10-20

## OpenAPI Specification

### Authentication
```
POST /api/auth/login
POST /api/auth/refresh
```

### User Endpoints
```
GET /api/users
POST /api/users
GET /api/users/{id}
PUT /api/users/{id}
DELETE /api/users/{id}
```

## Schema Definitions
- [[Schemas/User|User Schema]]
- [[Schemas/Project|Project Schema]]

## Error Handling
All endpoints return consistent error format:
```json
{
  "error": "string",
  "code": "number",
  "details": "object"
}
```