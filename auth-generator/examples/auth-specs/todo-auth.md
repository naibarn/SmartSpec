# Authentication Specification: Todo App

## User Model

### Fields
- id: string (UUID, primary key)
- email: string (required, unique, max 255)
- password: string (required, hashed)
- name: string (required, max 200)
- role: enum (user, admin)
- emailVerified: boolean (default: false)
- createdAt: datetime (auto)
- updatedAt: datetime (auto)

### Indexes
- email (unique)
- role

## Authentication Methods

- Email/Password

## Token Configuration

- Access Token: 15 minutes
- Refresh Token: 7 days
- Algorithm: RS256

## Protected Endpoints

### Todo Endpoints
- GET /api/todos (auth required, role: user)
- POST /api/todos (auth required, role: user)
- GET /api/todos/:id (auth required, role: user)
- PUT /api/todos/:id (auth required, role: user, owner only)
- DELETE /api/todos/:id (auth required, role: admin)

## Public Endpoints

### Authentication
- POST /auth/register - Register new user
- POST /auth/login - Login user
- POST /auth/refresh - Refresh access token
- POST /auth/logout - Logout user (invalidate tokens)
- POST /auth/forgot-password - Request password reset
- POST /auth/reset-password - Reset password with token

### User Profile
- GET /auth/me (auth required) - Get current user profile
- PUT /auth/me (auth required) - Update current user profile
- PUT /auth/me/password (auth required) - Change password

## Features

- Email verification: yes
- Password reset: yes
- Rate limiting: 5 requests/minute for auth endpoints
- Session management: JWT only (no sessions)
- Token blacklist: yes (Redis)

## Security Settings

### Password Requirements
- Minimum length: 8 characters
- Must contain: uppercase, lowercase, number, special character

### Rate Limits
- Auth endpoints: 5 requests/minute
- API endpoints (authenticated): 100 requests/minute
- Public endpoints: 20 requests/minute

### Account Security
- Max login attempts: 5 per 15 minutes
- Account lockout duration: 30 minutes
- Password reset token expiry: 1 hour
- Email verification token expiry: 24 hours

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token",
  "code": "AUTH_INVALID_TOKEN"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Insufficient permissions",
  "code": "AUTH_INSUFFICIENT_PERMISSIONS"
}
```

### 429 Too Many Requests
```json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded. Try again in 60 seconds.",
  "code": "RATE_LIMIT_EXCEEDED",
  "retryAfter": 60
}
```

## Business Rules

1. **Registration**
   - Email must be unique
   - Password must meet strength requirements
   - Default role is 'user'
   - Email verification email sent automatically

2. **Login**
   - Email and password required
   - Account must be active (not locked)
   - Failed attempts tracked
   - Successful login resets failed attempts counter

3. **Token Refresh**
   - Refresh token must be valid and not expired
   - New access token and refresh token issued
   - Old refresh token invalidated

4. **Password Reset**
   - Reset token sent to email
   - Token valid for 1 hour
   - Old password not required if using reset token
   - All sessions invalidated after password reset

5. **Authorization**
   - User can only access their own todos
   - Admin can access all todos
   - Admin can delete any todo
   - User can only delete their own todos
