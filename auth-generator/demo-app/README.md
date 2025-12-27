# Demo Mini SaaS Application

Demo application showcasing **Auth Generator** integration with a simple Todo API.

## Features

✅ **Generated Authentication System**
- User registration with email/password
- Login with JWT tokens
- Token refresh
- Role-based access control (user, admin)
- Protected API routes

✅ **Todo API**
- Create, read, update, delete todos
- User-specific todo lists
- Protected by authentication middleware

✅ **Security**
- Helmet.js for security headers
- CORS configuration
- JWT token authentication
- Password hashing with bcrypt

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Run Development Server

```bash
npm run dev
```

Server will start on http://localhost:3000

## API Endpoints

### Authentication

**Register**
```bash
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Login**
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Get Current User**
```bash
GET /auth/me
Authorization: Bearer <access_token>
```

**Refresh Token**
```bash
POST /auth/refresh
Content-Type: application/json

{
  "refreshToken": "<refresh_token>"
}
```

### Todos (Protected)

**Get All Todos**
```bash
GET /api/todos
Authorization: Bearer <access_token>
```

**Create Todo**
```bash
POST /api/todos
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Buy groceries"
}
```

**Update Todo**
```bash
PUT /api/todos/:id
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Buy groceries and cook dinner",
  "completed": true
}
```

**Delete Todo**
```bash
DELETE /api/todos/:id
Authorization: Bearer <access_token>
```

### Admin (Admin Role Only)

**Get Stats**
```bash
GET /api/admin/stats
Authorization: Bearer <access_token>
```

## Testing with cURL

### 1. Register a User

```bash
curl -X POST http://localhost:3000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Response:
```json
{
  "accessToken": "eyJhbGc...",
  "refreshToken": "eyJhbGc...",
  "expiresIn": 900
}
```

### 2. Login

```bash
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 3. Get Current User

```bash
curl -X GET http://localhost:3000/auth/me \
  -H "Authorization: Bearer <your_access_token>"
```

### 4. Create a Todo

```bash
curl -X POST http://localhost:3000/api/todos \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Auth Generator"
  }'
```

### 5. Get All Todos

```bash
curl -X GET http://localhost:3000/api/todos \
  -H "Authorization: Bearer <your_access_token>"
```

## Project Structure

```
demo-app/
├── src/
│   ├── auth/              # Generated auth code
│   │   ├── controllers/
│   │   ├── middleware/
│   │   ├── routes/
│   │   ├── services/
│   │   └── types/
│   ├── routes/            # Application routes
│   │   └── todo.routes.ts
│   └── index.ts           # Main application
├── .env                   # Environment variables
├── package.json
├── tsconfig.json
└── README.md
```

## Generated Auth Code

The authentication system in `src/auth/` was generated using:

```bash
npx ts-node -e "
import { AuthGenerator } from '../src/generator/auth-generator';
(async () => {
  const generator = new AuthGenerator();
  await generator.generateFromFile('../examples/auth-specs/todo-auth.md', {
    outputDir: './src/auth'
  });
})();
"
```

## Development

### Build for Production

```bash
npm run build
npm start
```

### Environment Variables

- `NODE_ENV` - Environment (development/production)
- `PORT` - Server port (default: 3000)
- `JWT_SECRET` - Secret key for JWT signing
- `JWT_ACCESS_EXPIRY` - Access token expiry (default: 15m)
- `JWT_REFRESH_EXPIRY` - Refresh token expiry (default: 7d)
- `ALLOWED_ORIGINS` - CORS allowed origins

## Performance

Generated auth code performance:
- **Registration:** ~50-100ms (with bcrypt)
- **Login:** ~50-100ms (with bcrypt)
- **Token Verification:** ~1-5ms
- **Protected Route:** ~2-10ms overhead

## Security Features

✅ Password hashing with bcrypt (10 rounds)  
✅ JWT tokens with RS256 algorithm  
✅ Token expiration (15min access, 7d refresh)  
✅ Role-based access control  
✅ Helmet.js security headers  
✅ CORS configuration  
✅ Input validation with Zod  

## Next Steps

1. **Add Database:** Integrate with PostgreSQL/MongoDB
2. **Add Email:** Implement email verification
3. **Add Tests:** Write integration tests
4. **Add Logging:** Implement structured logging
5. **Add Monitoring:** Add metrics and health checks

## License

ISC

## Learn More

- [Auth Generator Documentation](../docs/API_DOCUMENTATION.md)
- [Template Usage Guide](../docs/TEMPLATE_GUIDE.md)
- [Integration Guide](../docs/INTEGRATION_GUIDE.md)
