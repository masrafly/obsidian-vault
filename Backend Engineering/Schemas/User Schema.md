# User Schema
**Description:** User entity in the system

## Properties
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | UUID v4 |
| email | string | Yes | Valid email address |
| name | string | Yes | Full name |
| role | enum | Yes | admin, developer, reviewer |
| created_at | datetime | Yes | ISO 8601 format |
| updated_at | datetime | No | ISO 8601 format |

## JSON Example
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "developer"
}
```

## Related
- [[Main API|API Endpoints]]
- [[../Project Documentation/Sprint 3 Goals|Sprint Goals]]