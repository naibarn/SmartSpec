# Technical Specification: User Authentication API

## Overview

This document provides the technical specification for implementing a JWT-based authentication API. The system will handle user registration, login, token management, and session control.

**Version:** 1.0
**Last Updated:** 2024-12-27
**Status:** Draft

## Architecture

### High-Level Architecture

```
┌──────────┐      ┌──────────┐      ┌──────────┐
│  Client  │─────▶│   API    │─────▶│ Database │
└──────────┘      │ Gateway  │      └──────────┘
                  └────┬─────┘
                       │
                       ▼
                  ┌──────────┐
                  │  Cache   │
                  └──────────┘
```

### Component Diagram

```
┌─────────────────────────────────────┐
│         API Gateway (Port 3000)     │
├─────────────────────────────────────┤
│  ┌──────────────────────────────┐  │
│  │   Authentication Service     │  │
│  ├──────────────────────────────┤  │
│  │  - Registration Handler      │  │
│  │  - Login Handler             │  │
│  │  - Token Manager             │  │
│  │  - Session Manager           │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   Validation Middleware      │  │
│  ├──────────────────────────────┤  │
│  │  - Input Validator           │  │
│  │  - Token Validator           │  │
│  │  - Rate Limiter              │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
         │                   │
         ▼                   ▼
┌─────────────┐     ┌─────────────┐
│ PostgreSQL  │     │    Redis    │
│  (Port 5432)│     │ (Port 6379) │
└─────────────┘     └─────────────┘
```

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Runtime | Node.js | 18.x | Server runtime |
| Framework | Express | 4.18.x | Web framework |
| Database | PostgreSQL | 15.x | Primary data store |
| Cache | Redis | 7.x | Session & cache |
| Auth | jsonwebtoken | 9.x | JWT handling |
| Hashing | bcrypt | 5.x | Password hashing |
| Validation | Joi | 17.x | Input validation |
| ORM | Prisma | 5.x | Database ORM |

## API

### Authentication Endpoints

#### POST /api/auth/register

Register a new user account.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Validation Rules:**
- `email`: Required, valid email format, max 255 chars
- `password`: Required, min 8 chars, max 128 chars, must contain uppercase, lowercase, number, special char
- `name`: Required, min 2 chars, max 100 chars

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Registration successful. Please check your email.",
  "data": {
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Error Responses:**

400 Bad Request:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

409 Conflict:
```json
{
  "success": false,
  "error": {
    "code": "EMAIL_EXISTS",
    "message": "Email already registered"
  }
}
```

---

#### POST /api/auth/login

Authenticate user and issue tokens.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "rememberMe": false
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "550e8400-e29b-41d4-a716-446655440000",
    "expiresIn": 3600,
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "name": "John Doe",
      "role": "user"
    }
  }
}
```

**Error Responses:**

401 Unauthorized:
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}
```

423 Locked:
```json
{
  "success": false,
  "error": {
    "code": "ACCOUNT_LOCKED",
    "message": "Account locked due to too many failed attempts",
    "lockedUntil": "2024-12-27T10:30:00Z"
  }
}
```

---

#### POST /api/auth/refresh

Refresh access token using refresh token.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "refreshToken": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 3600
  }
}
```

---

#### POST /api/auth/logout

Invalidate current session and refresh token.

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "refreshToken": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

#### GET /api/auth/me

Get current user profile.

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "emailVerified": true,
    "createdAt": "2024-12-27T08:00:00Z"
  }
}
```

---

#### PUT /api/auth/password

Change user password.

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "currentPassword": "OldPass123!",
  "newPassword": "NewPass456!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

---

#### DELETE /api/auth/account

Delete user account.

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "password": "SecurePass123!",
  "confirmation": "DELETE"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Account deleted successfully"
}
```

## Data Models

### User Model

```typescript
interface User {
  id: string;                    // UUID
  email: string;                 // Unique, indexed
  passwordHash: string;          // bcrypt hash
  name: string;
  role: 'admin' | 'user' | 'guest';
  emailVerified: boolean;
  failedLoginAttempts: number;
  lockedUntil: Date | null;
  createdAt: Date;
  updatedAt: Date;
}
```

**Database Schema:**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'user',
  email_verified BOOLEAN DEFAULT FALSE,
  failed_login_attempts INTEGER DEFAULT 0,
  locked_until TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_locked_until ON users(locked_until) WHERE locked_until IS NOT NULL;
```

---

### RefreshToken Model

```typescript
interface RefreshToken {
  id: string;                    // UUID
  userId: string;                // Foreign key to User
  token: string;                 // Unique token
  expiresAt: Date;
  createdAt: Date;
}
```

**Database Schema:**
```sql
CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(500) UNIQUE NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_refresh_tokens_token ON refresh_tokens(token);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);
```

---

### Session Model (Redis)

```typescript
interface Session {
  userId: string;
  email: string;
  role: string;
  loginAt: number;               // Unix timestamp
  expiresAt: number;             // Unix timestamp
}
```

**Redis Key Pattern:**
```
session:{userId}:{sessionId}
```

**TTL:** 1 hour (access token expiration)

## Implementation

### Project Structure

```
src/
├── config/
│   ├── database.ts
│   ├── redis.ts
│   └── jwt.ts
├── controllers/
│   └── auth.controller.ts
├── middleware/
│   ├── auth.middleware.ts
│   ├── validation.middleware.ts
│   └── rateLimit.middleware.ts
├── services/
│   ├── auth.service.ts
│   ├── token.service.ts
│   └── email.service.ts
├── models/
│   ├── user.model.ts
│   └── refreshToken.model.ts
├── validators/
│   └── auth.validator.ts
├── utils/
│   ├── password.util.ts
│   └── error.util.ts
├── types/
│   └── auth.types.ts
└── app.ts
```

### Authentication Flow

```
1. User submits credentials
   ↓
2. Validate input (Joi)
   ↓
3. Check rate limit (Redis)
   ↓
4. Query user from database
   ↓
5. Verify password (bcrypt)
   ↓
6. Generate JWT access token
   ↓
7. Generate refresh token (UUID)
   ↓
8. Store refresh token in database
   ↓
9. Create session in Redis
   ↓
10. Return tokens to client
```

### Token Generation

```typescript
// Access Token (JWT)
const accessToken = jwt.sign(
  {
    userId: user.id,
    email: user.email,
    role: user.role
  },
  process.env.JWT_SECRET,
  {
    expiresIn: '1h',
    issuer: 'auth-api',
    audience: 'api-gateway'
  }
);

// Refresh Token (UUID)
const refreshToken = uuidv4();
```

### Password Hashing

```typescript
import bcrypt from 'bcrypt';

// Hash password
const saltRounds = 12;
const passwordHash = await bcrypt.hash(password, saltRounds);

// Verify password
const isValid = await bcrypt.compare(password, passwordHash);
```

### Rate Limiting

```typescript
// Login endpoint: 5 requests per 15 minutes
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: 'Too many login attempts, please try again later'
});

// Registration endpoint: 3 requests per hour
const registerLimiter = rateLimit({
  windowMs: 60 * 60 * 1000,
  max: 3,
  message: 'Too many registration attempts, please try again later'
});
```

## Testing

### Unit Tests

- Password hashing and verification
- JWT token generation and validation
- Input validation schemas
- Utility functions

### Integration Tests

- User registration flow
- User login flow
- Token refresh flow
- Password change flow
- Account deletion flow

### Security Tests

- SQL injection attempts
- XSS attempts
- CSRF attacks
- Brute force attacks
- Token manipulation

### Performance Tests

- Concurrent login requests (1000 users)
- Token generation performance
- Database query performance
- Cache hit/miss ratios

### Test Coverage Target

- Unit tests: > 90%
- Integration tests: > 80%
- Overall coverage: > 85%
