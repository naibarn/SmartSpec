# API Specification: Todo App

**Version:** 1.0  
**Description:** Simple todo management API

---

## Entities

### Todo

**Fields:**
- `id`: string (UUID, auto-generated, primary key)
- `title`: string (required, max 200 chars, not empty)
- `description`: string (optional, max 1000 chars)
- `completed`: boolean (default: false)
- `userId`: string (UUID, foreign key to User, required)
- `createdAt`: datetime (auto-generated)
- `updatedAt`: datetime (auto-updated)

**Indexes:**
- `userId` (for faster user queries)
- `completed` (for filtering)

**Relationships:**
- belongs to User (many-to-one)

---

### User

**Fields:**
- `id`: string (UUID, auto-generated, primary key)
- `email`: string (required, unique, email format)
- `name`: string (required, max 100 chars)
- `createdAt`: datetime (auto-generated)

**Indexes:**
- `email` (unique)

**Relationships:**
- has many Todos (one-to-many)

---

## Endpoints

### GET /api/todos

**Description:** List all todos for the current authenticated user

**Authentication:** Required (JWT)

**Authorization:** User can only see their own todos

**Query Parameters:**
- `completed`: boolean (optional) - Filter by completion status
- `limit`: integer (optional, default: 20, max: 100) - Number of results
- `offset`: integer (optional, default: 0) - Pagination offset
- `sort`: string (optional, default: "createdAt", values: "createdAt", "title") - Sort field
- `order`: string (optional, default: "desc", values: "asc", "desc") - Sort order

**Response:** 200 OK
```json
{
  "data": [
    {
      "id": "uuid",
      "title": "string",
      "description": "string",
      "completed": false,
      "userId": "uuid",
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z"
    }
  ],
  "meta": {
    "total": 100,
    "limit": 20,
    "offset": 0
  }
}
```

**Errors:**
- `401 Unauthorized`: Missing or invalid authentication token

---

### POST /api/todos

**Description:** Create a new todo for the current user

**Authentication:** Required (JWT)

**Request Body:**
```json
{
  "title": "string (required, max 200 chars)",
  "description": "string (optional, max 1000 chars)"
}
```

**Validation:**
- Title is required and cannot be empty
- Title max length: 200 characters
- Description max length: 1000 characters

**Response:** 201 Created
```json
{
  "data": {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "completed": false,
    "userId": "uuid",
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z"
  }
}
```

**Errors:**
- `400 Bad Request`: Invalid input (validation errors)
- `401 Unauthorized`: Missing or invalid authentication token

---

### GET /api/todos/:id

**Description:** Get a single todo by ID

**Authentication:** Required (JWT)

**Authorization:** User can only access their own todos

**Path Parameters:**
- `id`: string (UUID) - Todo ID

**Response:** 200 OK
```json
{
  "data": {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "completed": false,
    "userId": "uuid",
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z"
  }
}
```

**Errors:**
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User does not own this todo
- `404 Not Found`: Todo not found

---

### PUT /api/todos/:id

**Description:** Update an existing todo

**Authentication:** Required (JWT)

**Authorization:** User can only update their own todos

**Path Parameters:**
- `id`: string (UUID) - Todo ID

**Request Body:** (all fields optional)
```json
{
  "title": "string (optional, max 200 chars)",
  "description": "string (optional, max 1000 chars)",
  "completed": "boolean (optional)"
}
```

**Validation:**
- If title provided: cannot be empty, max 200 characters
- If description provided: max 1000 characters

**Response:** 200 OK
```json
{
  "data": {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "completed": false,
    "userId": "uuid",
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z"
  }
}
```

**Errors:**
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User does not own this todo
- `404 Not Found`: Todo not found

---

### DELETE /api/todos/:id

**Description:** Delete a todo

**Authentication:** Required (JWT)

**Authorization:** User can only delete their own todos

**Path Parameters:**
- `id`: string (UUID) - Todo ID

**Response:** 204 No Content

**Errors:**
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User does not own this todo
- `404 Not Found`: Todo not found

---

## Business Rules

### Validation Rules

1. **Title Validation:**
   - Required for creation
   - Cannot be empty string
   - Maximum 200 characters
   - Trimmed automatically

2. **Description Validation:**
   - Optional
   - Maximum 1000 characters
   - Trimmed automatically

3. **Completed Validation:**
   - Must be boolean
   - Defaults to false on creation

### Authorization Rules

1. **User Isolation:**
   - Users can only access their own todos
   - All queries automatically filtered by userId
   - Attempting to access other user's todos returns 403

2. **Authentication:**
   - All endpoints require valid JWT token
   - Token must contain valid userId
   - Expired tokens return 401

### Data Integrity

1. **User Reference:**
   - userId must reference an existing user
   - Cascade delete: when user deleted, all todos deleted

2. **Timestamps:**
   - createdAt set automatically on creation
   - updatedAt updated automatically on modification
   - Cannot be manually set

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Field-specific error (for validation errors)"
    }
  }
}
```

### Error Codes

- `VALIDATION_ERROR`: Input validation failed
- `UNAUTHORIZED`: Authentication required or invalid
- `FORBIDDEN`: User not authorized to access resource
- `NOT_FOUND`: Resource not found
- `INTERNAL_ERROR`: Server error

---

## Rate Limiting

- **Rate:** 100 requests per minute per user
- **Response:** 429 Too Many Requests
- **Headers:**
  - `X-RateLimit-Limit`: 100
  - `X-RateLimit-Remaining`: <remaining>
  - `X-RateLimit-Reset`: <timestamp>

---

## Notes for Generator

### Template-Based (Simple)

These can be generated with templates:
- ✅ Basic CRUD operations (GET, POST, PUT, DELETE)
- ✅ Standard validation (required, max length, type)
- ✅ Standard error responses
- ✅ Pagination logic
- ✅ Filtering by completed status
- ✅ Sorting logic

### AI-Assisted (Complex)

These need AI assistance:
- ⚠️ None (this is a simple spec, all template-based)

### Complexity Score

**Overall:** Low (Template-based 100%, AI-assisted 0%)

This spec is intentionally simple for Week 2 demo.
