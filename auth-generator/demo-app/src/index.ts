/**
 * Demo Mini SaaS Application
 * Showcasing Auth Generator integration
 */

import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { authRouter } from './auth/routes/auth.routes';
import { AuthMiddleware } from './auth/middleware/auth.middleware';
import { todoRouter } from './routes/todo.routes';

const app = express();
const authMiddleware = new AuthMiddleware();

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
  credentials: true
}));

// Body parsing
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Auth routes (public)
app.use('/auth', authRouter);

// Protected API routes
app.use('/api/todos',
  authMiddleware.authenticate(),
  todoRouter
);

// Admin routes
app.get('/api/admin/stats',
  authMiddleware.authenticate(),
  authMiddleware.requireRole('admin'),
  (req, res) => {
    res.json({
      message: 'Admin stats',
      user: req.user
    });
  }
);

// Error handling
app.use((error: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Error:', error);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? error.message : undefined
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Not found' });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════╗
║   Demo Mini SaaS Application           ║
║   Auth Generator Integration           ║
╚════════════════════════════════════════╝

✓ Server running on port ${PORT}
✓ Environment: ${process.env.NODE_ENV || 'development'}
✓ Auth endpoints: http://localhost:${PORT}/auth
✓ API endpoints: http://localhost:${PORT}/api

Available endpoints:
  POST   /auth/register
  POST   /auth/login
  POST   /auth/refresh
  GET    /auth/me
  GET    /api/todos
  POST   /api/todos
  GET    /api/admin/stats (admin only)
`);
});
