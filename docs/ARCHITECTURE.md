# Architecture

## Overview

SmartSpec Pro Web Dashboard is a modern React application built with TypeScript, Vite, and Tailwind CSS.

## Tech Stack

### Frontend
- React 18.3.1
- TypeScript 5.6.2
- Vite 7.3.0
- Tailwind CSS 3.4.17

### UI Components
- shadcn/ui
- Radix UI
- Framer Motion

### State Management
- React Context API
- TanStack Query

### Routing
- React Router 7.1.1

## Architecture Layers

### 1. Presentation Layer
- Pages and components
- UI components from shadcn/ui
- Styling with Tailwind CSS

### 2. Business Logic Layer
- React contexts
- Custom hooks
- Form validation with Zod

### 3. Data Layer
- API service (Axios)
- TanStack Query for data fetching
- Local state management

### 4. Infrastructure Layer
- Vite build tool
- Environment configuration
- Deployment setup

## Key Patterns

### Component Structure
\`\`\`
Component/
├── Component.tsx
├── Component.test.tsx
└── index.ts
\`\`\`

### API Service Pattern
\`\`\`typescript
// Centralized API service
import api from '@/services/api';

// Usage in components
const { data } = useQuery({
  queryKey: ['credits'],
  queryFn: api.credits.getBalance
});
\`\`\`

### Protected Routes
\`\`\`typescript
<Route element={<ProtectedRoute />}>
  <Route path="dashboard/*" element={<DashboardLayout />} />
</Route>
\`\`\`

## Security

- JWT authentication
- OAuth 2.0 integration
- Input validation with Zod
- XSS protection (React built-in)
- HTTPS in production

## Performance

- Code splitting
- Lazy loading
- Image optimization
- Bundle size optimization
- Caching strategies

---

For more details, see [README.md](../README.md).
