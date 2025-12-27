"use strict";
/**
 * Demo Mini SaaS Application
 * Showcasing Auth Generator integration
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const helmet_1 = __importDefault(require("helmet"));
const auth_routes_1 = require("./auth/routes/auth.routes");
const auth_middleware_1 = require("./auth/middleware/auth.middleware");
const todo_routes_1 = require("./routes/todo.routes");
const app = (0, express_1.default)();
const authMiddleware = new auth_middleware_1.AuthMiddleware();
// Security middleware
app.use((0, helmet_1.default)());
app.use((0, cors_1.default)({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
    credentials: true
}));
// Body parsing
app.use(express_1.default.json());
app.use(express_1.default.urlencoded({ extended: true }));
// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});
// Auth routes (public)
app.use('/auth', auth_routes_1.authRouter);
// Protected API routes
app.use('/api/todos', authMiddleware.authenticate(), todo_routes_1.todoRouter);
// Admin routes
app.get('/api/admin/stats', authMiddleware.authenticate(), authMiddleware.requireRole('admin'), (req, res) => {
    res.json({
        message: 'Admin stats',
        user: req.user
    });
});
// Error handling
app.use((error, req, res, next) => {
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
//# sourceMappingURL=index.js.map