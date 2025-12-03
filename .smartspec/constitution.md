# Smart AI Hub Constitution

## Core Principles

### I. Test-Driven Development (NON-NEGOTIABLE)
TDD is mandatory for all feature development: Tests must be written first, reviewed and approved by the user, and must fail initially (red state) before any implementation begins. Red-Green-Refactor cycle is strictly enforced. User approval is required before proceeding from test writing to implementation. Unit test coverage must exceed 80%.

### II. Context7 Compliance
All implementations must follow Context7 standards as primary technical guidance. This includes security requirements (JWT RS256 authentication, rate limiting, Zod validation), API design requirements (RESTful design, standardized error format), data layer requirements (Prisma ORM, Redis caching), and technology stack requirements (Node.js 22.x, Fastify 5.x, TypeScript strict mode).

### III. Library-First Approach
Every feature starts as a standalone library that is self-contained, independently testable, and documented. Libraries must have clear purpose and follow established patterns. No organizational-only libraries without clear functional purpose.

### IV. Integration Testing
Focus areas requiring integration tests include: new library contract tests, contract changes, inter-service communication, and shared schemas. All API endpoints must have integration test coverage.

### V. Observability
Structured logging with correlation IDs is required for all operations. Text I/O ensures debuggability. Metrics collection and monitoring must be implemented for all critical paths.

### VI. Security by Default
Default deny policy with explicit allow only is mandatory. All admin actions require audit logging. Input validation and sanitization is required for all endpoints. SQL injection prevention via parameterized queries is mandatory.

## Additional Constraints

### Technology Stack Requirements
- Node.js 22.x with ES modules and strict mode
- Fastify 5.x for backend services
- TypeScript strict mode with no `any` type
- PostgreSQL 16+ with Prisma ORM
- Redis 7+ for caching and BullMQ 5.x for queues
- Zod for validation, Winston for logging, Prometheus for metrics

### Performance Standards
- API response time p95 < 500ms (authorization: <100ms)
- Database queries <50ms average execution time
- Cache hit rate >80% during steady state
- Support for 10,000+ concurrent users

### Security Requirements
- JWT RS256 authentication for all API endpoints
- Rate limiting per user and per IP
- CSRF protection for state-changing endpoints
- Data encryption (TLS 1.3 in transit, AES-256 at rest)
- Audit logging with correlation IDs

## Development Workflow

### Quality Gates
- All constitution principles must be verified
- Performance targets must be met in production-like environment
- Security review must pass with no critical findings
- Unit test coverage must exceed 80%
- Integration tests for all API contracts

### Review Process
- Code review must verify compliance with constitution
- Security review must validate all security requirements
- Performance review must validate SLO compliance
- Architecture review must validate Context7 compliance

## Governance

This constitution supersedes all other practices. Amendments require documentation, approval, and migration plan. All PRs/reviews must verify compliance. Complexity must be justified. Use Context7 guidance for runtime development.

**Version**: 1.0.0 | **Ratified**: 2024-11-14 | **Last Amended**: 2024-11-14
