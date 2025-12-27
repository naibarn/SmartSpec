# Auth Generator Requirements
## Comprehensive Authentication System Generator

**Version:** 1.0  
**Date:** 2024-12-27  
**Status:** Planning

---

## Overview

Auth Generator เป็น workflow ที่ generate authentication system สำหรับ API ที่สร้างจาก API Generator โดยอัตโนมัติ รองรับ JWT authentication, role-based access control (RBAC), และ security best practices

---

## Goals

### Primary Goals

1. **Generate Complete Auth System**
   - User registration & login
   - JWT token generation & validation
   - Password hashing (bcrypt)
   - Refresh token mechanism
   - Email verification (optional)
   - Password reset (optional)

2. **Generate Auth Middleware**
   - JWT verification middleware
   - Role-based authorization
   - Permission guards
   - Rate limiting per user

3. **Integrate with Existing API**
   - Add auth to existing endpoints
   - Protect routes automatically
   - Add user context to requests

4. **Security Best Practices**
   - Secure password storage
   - Token expiration
   - CSRF protection
   - SQL injection prevention
   - XSS prevention

---

## Input Specification

### Auth Spec Format (Markdown)

```markdown
# Authentication Specification

## User Model
- id: string (UUID, primary key)
- email: string (required, unique)
- password: string (required, hashed)
- name: string (required)
- role: enum (user, admin, moderator)
- emailVerified: boolean (default: false)
- createdAt: datetime (auto)
- updatedAt: datetime (auto)

## Authentication Methods
- Email/Password
- OAuth (Google, GitHub) [optional]

## Token Configuration
- Access Token: 15 minutes
- Refresh Token: 7 days
- Algorithm: RS256

## Protected Endpoints
- GET /api/todos (auth required, role: user)
- POST /api/todos (auth required, role: user)
- DELETE /api/todos/:id (auth required, role: admin)

## Public Endpoints
- POST /auth/register
- POST /auth/login
- POST /auth/refresh
- POST /auth/forgot-password
- POST /auth/reset-password

## Features
- Email verification: yes
- Password reset: yes
- Rate limiting: 5 requests/minute for auth endpoints
- Session management: JWT only (no sessions)
```

---

## Output Specification

### Generated Files

```
output/
├── src/
│   ├── auth/
│   │   ├── auth.controller.ts       # Auth endpoints (register, login, refresh)
│   │   ├── auth.service.ts          # Auth business logic
│   │   ├── auth.middleware.ts       # JWT verification middleware
│   │   ├── auth.guards.ts           # Role/permission guards
│   │   ├── jwt.service.ts           # JWT generation/validation
│   │   ├── password.service.ts      # Password hashing/verification
│   │   └── auth.types.ts            # Auth-related types
│   ├── users/
│   │   ├── user.controller.ts       # User CRUD (protected)
│   │   ├── user.service.ts          # User business logic
│   │   ├── user.model.ts            # User database model
│   │   └── user.validator.ts        # User validation schemas
│   ├── middleware/
│   │   ├── authenticate.ts          # Auth middleware
│   │   ├── authorize.ts             # Authorization middleware
│   │   └── rate-limit.ts            # Rate limiting middleware
│   └── config/
│       ├── jwt.config.ts            # JWT configuration
│       └── security.config.ts       # Security settings
├── tests/
│   ├── auth.test.ts                 # Auth endpoint tests
│   ├── middleware.test.ts           # Middleware tests
│   └── integration/
│       └── auth-flow.test.ts        # Full auth flow tests
└── docs/
    └── AUTH.md                      # Auth documentation
```

---

## Features

### 1. User Registration

**Endpoint:** `POST /auth/register`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "emailVerified": false
  },
  "tokens": {
    "accessToken": "jwt-token",
    "refreshToken": "refresh-token",
    "expiresIn": 900
  }
}
```

**Features:**
- Email validation
- Password strength validation
- Duplicate email check
- Automatic password hashing
- Optional email verification

---

### 2. User Login

**Endpoint:** `POST /auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user"
  },
  "tokens": {
    "accessToken": "jwt-token",
    "refreshToken": "refresh-token",
    "expiresIn": 900
  }
}
```

**Features:**
- Email/password verification
- Rate limiting (5 attempts/minute)
- Account lockout after failed attempts
- Login history tracking

---

### 3. Token Refresh

**Endpoint:** `POST /auth/refresh`

**Request:**
```json
{
  "refreshToken": "refresh-token"
}
```

**Response:**
```json
{
  "accessToken": "new-jwt-token",
  "refreshToken": "new-refresh-token",
  "expiresIn": 900
}
```

---

### 4. JWT Middleware

**Usage:**
```typescript
import { authenticate } from './middleware/authenticate';

router.get('/api/todos', authenticate, todoController.getAll);
```

**Features:**
- Extract JWT from Authorization header
- Verify token signature
- Check token expiration
- Attach user to request object
- Handle invalid/expired tokens

---

### 5. Authorization Guards

**Role-based:**
```typescript
import { authorize } from './middleware/authorize';

router.delete('/api/todos/:id', 
  authenticate, 
  authorize(['admin']), 
  todoController.delete
);
```

**Permission-based:**
```typescript
router.put('/api/todos/:id', 
  authenticate, 
  authorize({ permissions: ['todos:update'] }), 
  todoController.update
);
```

---

### 6. Password Reset

**Request Reset:**
```
POST /auth/forgot-password
{
  "email": "user@example.com"
}
```

**Reset Password:**
```
POST /auth/reset-password
{
  "token": "reset-token",
  "newPassword": "NewSecurePass123!"
}
```

---

## Technology Stack

### Core Libraries

- **jsonwebtoken** - JWT generation/validation
- **bcrypt** - Password hashing
- **zod** - Input validation
- **express** - Web framework
- **express-rate-limit** - Rate limiting

### Optional Libraries

- **nodemailer** - Email sending (for verification)
- **passport** - OAuth integration
- **redis** - Token blacklist/session storage

---

## Security Features

### 1. Password Security

- **Hashing:** bcrypt with salt rounds = 10
- **Strength Requirements:**
  - Minimum 8 characters
  - At least 1 uppercase
  - At least 1 lowercase
  - At least 1 number
  - At least 1 special character

### 2. JWT Security

- **Algorithm:** RS256 (asymmetric)
- **Access Token:** 15 minutes expiration
- **Refresh Token:** 7 days expiration
- **Token Rotation:** New refresh token on each refresh
- **Blacklist:** Revoked tokens stored in Redis

### 3. Rate Limiting

- **Auth Endpoints:** 5 requests/minute
- **API Endpoints:** 100 requests/minute (authenticated)
- **Public Endpoints:** 20 requests/minute

### 4. Protection Against

- **SQL Injection:** Parameterized queries
- **XSS:** Input sanitization
- **CSRF:** CSRF tokens (optional)
- **Brute Force:** Rate limiting + account lockout
- **Session Fixation:** Token rotation

---

## Integration with API Generator

### Automatic Integration

Auth Generator จะ:

1. **Scan existing API endpoints**
   ```typescript
   const endpoints = await scanEndpoints('./src');
   // Found: GET /api/todos, POST /api/todos, ...
   ```

2. **Add auth middleware to protected endpoints**
   ```typescript
   // Before
   router.get('/api/todos', todoController.getAll);
   
   // After
   router.get('/api/todos', authenticate, todoController.getAll);
   ```

3. **Add user context to controllers**
   ```typescript
   // Before
   async getAll(req: Request, res: Response) {
     const todos = await this.service.findAll();
   }
   
   // After
   async getAll(req: Request, res: Response) {
     const todos = await this.service.findAll({
       userId: req.user.id  // ← Added automatically
     });
   }
   ```

4. **Update validators to include user context**
   ```typescript
   // Before
   export const TodoCreateSchema = z.object({
     title: z.string(),
   });
   
   // After
   export const TodoCreateSchema = z.object({
     title: z.string(),
     userId: z.string().uuid(),  // ← Added automatically
   });
   ```

---

## Workflow

### Input: Auth Spec

```markdown
# Authentication Specification

## User Model
- email, password, name, role

## Protected Endpoints
- GET /api/todos (auth required)
- POST /api/todos (auth required)
```

### Command

```bash
node dist/cli.js generate-auth auth-spec.md -o src/
```

### Process

1. **Parse auth spec**
   ```typescript
   const authSpec = await authParser.parse('auth-spec.md');
   ```

2. **Generate auth files**
   ```typescript
   await authGenerator.generate(authSpec, {
     outputDir: 'src/',
     features: ['registration', 'login', 'refresh', 'reset']
   });
   ```

3. **Integrate with existing API**
   ```typescript
   await authIntegrator.integrate({
     apiDir: 'src/',
     protectedEndpoints: authSpec.protectedEndpoints
   });
   ```

4. **Generate tests**
   ```typescript
   await testGenerator.generateAuthTests(authSpec);
   ```

### Output

```
✓ Generated auth.controller.ts (250 lines)
✓ Generated auth.service.ts (180 lines)
✓ Generated auth.middleware.ts (120 lines)
✓ Generated jwt.service.ts (150 lines)
✓ Generated password.service.ts (80 lines)
✓ Updated todo.controller.ts (added user context)
✓ Updated todo.routes.ts (added auth middleware)
✓ Generated auth.test.ts (300 lines)
✓ Generated AUTH.md documentation

Total: 8 files generated, 2 files updated
Time: < 2 seconds
```

---

## Success Criteria

### Functional Requirements

- [ ] User can register with email/password
- [ ] User can login and receive JWT tokens
- [ ] User can refresh access token
- [ ] User can reset password
- [ ] Protected endpoints require valid JWT
- [ ] Role-based authorization works
- [ ] Rate limiting prevents abuse

### Non-Functional Requirements

- [ ] Generation time < 2 seconds
- [ ] Generated code passes all tests
- [ ] Generated code follows best practices
- [ ] Documentation is comprehensive
- [ ] Integration with existing API is seamless

### Security Requirements

- [ ] Passwords are hashed with bcrypt
- [ ] JWT tokens are signed with RS256
- [ ] Tokens expire appropriately
- [ ] Rate limiting is enforced
- [ ] Input validation prevents injection attacks

---

## Testing Strategy

### Unit Tests

- Auth service methods
- JWT generation/validation
- Password hashing/verification
- Middleware functions

### Integration Tests

- Full registration flow
- Full login flow
- Token refresh flow
- Password reset flow
- Protected endpoint access

### Security Tests

- Brute force protection
- Token expiration
- Invalid token handling
- SQL injection attempts
- XSS attempts

---

## Timeline

### Week 3

**Day 1: Planning & Setup**
- Requirements finalization
- Project structure
- Dependencies installation

**Day 2-3: Core Implementation**
- Auth service
- JWT service
- Password service
- Auth controller
- Middleware

**Day 4-5: Integration & Testing**
- API integration
- Unit tests
- Integration tests
- Documentation

---

## Dependencies

### Required

- API Generator (completed ✅)
- Node.js >= 18
- TypeScript >= 5.0
- Express >= 4.18

### Optional

- Database Setup (for user storage)
- Email service (for verification)
- Redis (for token blacklist)

---

## Future Enhancements

### Phase 2 (Optional)

- OAuth integration (Google, GitHub)
- Two-factor authentication (2FA)
- Biometric authentication
- Social login
- SSO (Single Sign-On)

### Phase 3 (Optional)

- Multi-tenancy support
- API key authentication
- Webhook authentication
- GraphQL authentication

---

## References

- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [bcrypt Documentation](https://github.com/kelektiv/node.bcrypt.js)

---

**Prepared by:** Dev Team  
**Date:** 2024-12-27  
**Status:** Ready for Implementation
