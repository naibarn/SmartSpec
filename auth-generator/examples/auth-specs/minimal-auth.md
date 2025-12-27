# Authentication Specification: Minimal App

## User Model

### Fields
- id: string (UUID, primary key)
- email: string (required, unique)
- password: string (required, hashed)
- createdAt: datetime (auto)
- updatedAt: datetime (auto)

### Indexes
- email (unique)

## Authentication Methods

- Email/Password

## Token Configuration

- Access Token: 15 minutes
- Refresh Token: 7 days
- Algorithm: RS256

## Protected Endpoints

### API Endpoints
- GET /api/data (auth required)
- POST /api/data (auth required)

## Public Endpoints

### Authentication
- POST /auth/register - Register new user
- POST /auth/login - Login user
- POST /auth/refresh - Refresh access token
- POST /auth/logout - Logout user

### User Profile
- GET /auth/me (auth required) - Get current user profile

## Features

- Email verification: no
- Password reset: no
- Rate limiting: no
- Session management: JWT only
- Token blacklist: no

## Security Settings

### Password Requirements
- Minimum length: 8 characters
- Must contain: lowercase

### Account Security
- Max login attempts: 5 per 15 minutes
- Account lockout duration: 15 minutes
