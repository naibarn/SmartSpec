# API Integration Guide

This guide explains how to integrate the web dashboard with the SmartSpec Pro backend API.

## Base Configuration

The API base URL is configured in `.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
```

## API Service

The main API service is located in `src/services/api.ts`. It uses Axios for HTTP requests and includes:

- Automatic token injection
- Request/response interceptors
- Error handling
- Timeout configuration

### Usage Example

```typescript
import api from '@/services/api';

// Login
const response = await api.auth.login({
  email: 'user@example.com',
  password: 'password123'
});

// Get user profile
const user = await api.auth.getProfile();

// Get credits balance
const credits = await api.credits.getBalance();
```

## Authentication APIs

### Login
```typescript
POST /api/auth/login
Body: { email: string, password: string }
Response: { access_token: string, user: User }
```

### Register
```typescript
POST /api/auth/register
Body: { email: string, password: string, name: string }
Response: { access_token: string, user: User }
```

### OAuth
```typescript
GET /api/oauth/{provider}/authorize
Response: { authorization_url: string }

GET /api/oauth/{provider}/callback?code=xxx
Response: { access_token: string, user: User }
```

## Credits APIs

### Get Balance
```typescript
GET /api/credits/balance
Response: { balance: number, total_purchased: number, total_used: number }
```

### Get Transactions
```typescript
GET /api/credits/transactions?limit=50&offset=0
Response: { transactions: Transaction[], total: number }
```

## Payment APIs

### Create Payment Intent
```typescript
POST /api/payments/create-intent
Body: { amount: number, currency: string }
Response: { client_secret: string, payment_intent_id: string }
```

## Error Handling

All API errors follow this format:

```typescript
{
  error: string,
  message: string,
  status_code: number
}
```

### Common Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Authentication Flow

1. User logs in via email/password or OAuth
2. Backend returns JWT access token
3. Frontend stores token in memory (AuthContext)
4. Token is automatically included in all API requests
5. If token expires, user is redirected to login

---

For more details, see the [Backend API Documentation](../../python-backend/README.md).
