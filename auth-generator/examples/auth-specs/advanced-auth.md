# Authentication Specification: Advanced Enterprise App

## User Model

### Fields
- id: string (UUID, primary key)
- email: string (required, unique, max 255)
- password: string (required, hashed)
- firstName: string (required, max 100)
- lastName: string (required, max 100)
- role: enum (user, manager, admin, superadmin)
- emailVerified: boolean (default: false)
- phoneNumber: string (optional, max 20)
- department: string (optional, max 100)
- isActive: boolean (default: true)
- lastLoginAt: datetime (optional)
- createdAt: datetime (auto)
- updatedAt: datetime (auto)

### Indexes
- email (unique)
- role
- department
- isActive

## Authentication Methods

- Email/Password

## Token Configuration

- Access Token: 30 minutes
- Refresh Token: 30 days
- Algorithm: RS256

## Protected Endpoints

### User Management
- GET /api/users (auth required, role: admin)
- POST /api/users (auth required, role: admin)
- GET /api/users/:id (auth required, role: manager)
- PUT /api/users/:id (auth required, role: admin, owner only)
- DELETE /api/users/:id (auth required, role: superadmin)

### Reports
- GET /api/reports (auth required, role: manager)
- POST /api/reports (auth required, role: manager)

## Public Endpoints

### Authentication
- POST /auth/register - Register new user
- POST /auth/login - Login user
- POST /auth/refresh - Refresh access token
- POST /auth/logout - Logout user
- POST /auth/forgot-password - Request password reset
- POST /auth/reset-password - Reset password with token
- GET /auth/verify-email/:token - Verify email address

### User Profile
- GET /auth/me (auth required) - Get current user profile
- PUT /auth/me (auth required) - Update current user profile
- PUT /auth/me/password (auth required) - Change password

## Features

- Email verification: yes
- Password reset: yes
- Rate limiting: 10 requests/minute for auth endpoints
- Session management: JWT only
- Token blacklist: yes (Redis)

## Security Settings

### Password Requirements
- Minimum length: 12 characters
- Must contain: uppercase, lowercase, number, special character

### Rate Limits
- Auth endpoints: 10 requests/minute
- API endpoints (authenticated): 200 requests/minute
- Public endpoints: 50 requests/minute

### Account Security
- Max login attempts: 3 per 10 minutes
- Account lockout duration: 60 minutes
- Password reset token expiry: 30 minutes
- Email verification token expiry: 48 hours
- Require email verification for login: yes
- Require password change every: 90 days

## Business Rules

1. **Registration**
   - Email must be unique
   - Password must meet strength requirements
   - Default role is 'user'
   - Email verification email sent automatically
   - Account inactive until email verified

2. **Login**
   - Email and password required
   - Account must be active (not locked)
   - Email must be verified
   - Failed attempts tracked
   - Successful login resets failed attempts counter
   - Update lastLoginAt timestamp

3. **Token Refresh**
   - Refresh token must be valid and not expired
   - New access token and refresh token issued
   - Old refresh token invalidated
   - Check if account is still active

4. **Password Reset**
   - Reset token sent to email
   - Token valid for 30 minutes
   - Old password not required if using reset token
   - All sessions invalidated after password reset

5. **Authorization**
   - User can only access their own profile
   - Manager can view users in their department
   - Admin can manage all users except superadmin
   - Superadmin has full access
   - Owner-only resources require ownership check
