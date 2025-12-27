# API Generator Requirements
## SmartSpec API Generator - Complete Specification

**Version:** 1.0  
**Date:** 2024-12-27  
**Status:** Week 0 - Planning

---

## 1. Overview

### 1.1 Purpose

Generate production-ready REST API code from specifications using a **Hybrid approach** (Template-based 80% + AI-assisted 20%).

### 1.2 Goals

1. **Speed:** Generate API in minutes, not hours
2. **Quality:** Production-ready code with tests
3. **Consistency:** Follow best practices automatically
4. **Flexibility:** Handle both simple and complex cases
5. **Maintainability:** Clean, documented code

### 1.3 Scope

**In Scope:**
- ✅ REST API generation (CRUD + custom endpoints)
- ✅ Request/response validation
- ✅ Error handling
- ✅ Authentication integration
- ✅ Database integration
- ✅ API documentation (OpenAPI/Swagger)
- ✅ Unit tests
- ✅ Integration tests

**Out of Scope:**
- ❌ GraphQL (future)
- ❌ WebSocket (future)
- ❌ gRPC (future)
- ❌ Frontend code
- ❌ Database migrations (separate workflow)

---

## 2. Input Specification

### 2.1 Input Format

**Primary Input:** Markdown specification file

**Example:**
```markdown
# API Specification: Todo App

## Entities

### Todo
- id: string (UUID, auto-generated)
- title: string (required, max 200 chars)
- description: string (optional, max 1000 chars)
- completed: boolean (default: false)
- userId: string (UUID, foreign key to User)
- createdAt: datetime (auto-generated)
- updatedAt: datetime (auto-updated)

### User
- id: string (UUID, auto-generated)
- email: string (required, unique, email format)
- name: string (required, max 100 chars)
- createdAt: datetime (auto-generated)

## Endpoints

### GET /api/todos
- Description: List all todos for current user
- Auth: Required
- Query params:
  - completed: boolean (optional, filter)
  - limit: integer (optional, default 20, max 100)
  - offset: integer (optional, default 0)
- Response: 200 OK
  ```json
  {
    "data": [Todo],
    "total": integer,
    "limit": integer,
    "offset": integer
  }
  ```

### POST /api/todos
- Description: Create a new todo
- Auth: Required
- Body:
  ```json
  {
    "title": string,
    "description": string (optional)
  }
  ```
- Response: 201 Created
  ```json
  {
    "data": Todo
  }
  ```
- Errors:
  - 400: Invalid input
  - 401: Unauthorized

### GET /api/todos/:id
- Description: Get a single todo
- Auth: Required
- Response: 200 OK
  ```json
  {
    "data": Todo
  }
  ```
- Errors:
  - 404: Todo not found
  - 401: Unauthorized
  - 403: Forbidden (not owner)

### PUT /api/todos/:id
- Description: Update a todo
- Auth: Required
- Body: Partial Todo
- Response: 200 OK
- Errors: 400, 401, 403, 404

### DELETE /api/todos/:id
- Description: Delete a todo
- Auth: Required
- Response: 204 No Content
- Errors: 401, 403, 404

## Business Rules

1. Users can only access their own todos
2. Title is required and cannot be empty
3. Completed todos cannot be deleted (must be archived)
4. Maximum 100 todos per user
```

### 2.2 Required Fields

**Entity Definition:**
- Entity name
- Fields (name, type, constraints)
- Relationships (if any)

**Endpoint Definition:**
- HTTP method
- Path
- Description
- Authentication requirement
- Request body schema (if applicable)
- Response schema
- Error responses

**Business Rules:**
- Validation rules
- Authorization rules
- Business logic constraints

---

## 3. Output Specification

### 3.1 Output Structure

```
output/
├── src/
│   ├── controllers/
│   │   ├── todo.controller.ts
│   │   └── user.controller.ts
│   ├── services/
│   │   ├── todo.service.ts
│   │   └── user.service.ts
│   ├── models/
│   │   ├── todo.model.ts
│   │   └── user.model.ts
│   ├── validators/
│   │   ├── todo.validator.ts
│   │   └── user.validator.ts
│   ├── routes/
│   │   ├── todo.routes.ts
│   │   └── user.routes.ts
│   ├── middleware/
│   │   ├── auth.middleware.ts
│   │   ├── error.middleware.ts
│   │   └── validation.middleware.ts
│   └── app.ts
├── tests/
│   ├── unit/
│   │   ├── todo.service.test.ts
│   │   └── user.service.test.ts
│   └── integration/
│       ├── todo.api.test.ts
│       └── user.api.test.ts
├── docs/
│   ├── openapi.yaml
│   └── API.md
├── package.json
├── tsconfig.json
└── README.md
```

### 3.2 Code Quality Requirements

**Must Have:**
- ✅ TypeScript (strict mode)
- ✅ ESLint configured
- ✅ Prettier configured
- ✅ Type safety (no `any`)
- ✅ Error handling (try-catch)
- ✅ Input validation (all endpoints)
- ✅ Logging (structured)
- ✅ Comments (JSDoc)

**Architecture:**
- ✅ Layered architecture (Controller → Service → Model)
- ✅ Dependency injection
- ✅ Single responsibility principle
- ✅ DRY (Don't Repeat Yourself)

---

## 4. Hybrid Approach

### 4.1 Template-Based (80%)

**What Templates Handle:**
- ✅ Standard CRUD operations
- ✅ Basic validation
- ✅ Error handling patterns
- ✅ Authentication middleware
- ✅ Database queries (simple)
- ✅ Response formatting
- ✅ Test boilerplate

**Template Engine:** Handlebars

**Example Template:**
```handlebars
// {{entity.name}}.controller.ts
import { Request, Response, NextFunction } from 'express';
import { {{entity.name}}Service } from '../services/{{entity.name}}.service';

export class {{entity.name}}Controller {
  constructor(private service: {{entity.name}}Service) {}

  async getAll(req: Request, res: Response, next: NextFunction) {
    try {
      const { limit = 20, offset = 0 } = req.query;
      const result = await this.service.findAll({
        limit: Number(limit),
        offset: Number(offset),
        userId: req.user.id
      });
      res.json(result);
    } catch (error) {
      next(error);
    }
  }

  // ... more methods
}
```

### 4.2 AI-Assisted (20%)

**What AI Handles:**
- ✅ Complex business logic
- ✅ Custom validations
- ✅ Complex queries (joins, aggregations)
- ✅ Edge cases
- ✅ Performance optimizations
- ✅ Security considerations

**AI Provider:** GPT-4 (primary), Claude (fallback)

**Example AI Prompt:**
```
Generate a service method that:
1. Validates that a user cannot delete a completed todo
2. Checks if user has reached the limit of 100 todos
3. Implements soft delete (archive) instead of hard delete
4. Logs the deletion with user context

Context:
- Entity: Todo
- Business rule: Completed todos must be archived, not deleted
- Limit: 100 todos per user
- User: req.user.id

Return TypeScript code only.
```

### 4.3 Decision Logic

```typescript
function shouldUseAI(endpoint: Endpoint): boolean {
  // Use AI if:
  return (
    endpoint.hasComplexBusinessLogic() ||
    endpoint.hasComplexValidation() ||
    endpoint.hasComplexQuery() ||
    endpoint.hasCustomErrorHandling() ||
    endpoint.hasPerformanceRequirements()
  );
}
```

---

## 5. Technology Stack

### 5.1 Backend Framework

**Primary:** Node.js + Express + TypeScript

**Why?**
- ✅ Most popular
- ✅ Large ecosystem
- ✅ Easy to learn
- ✅ Good performance

**Alternative (Future):**
- FastAPI (Python)
- NestJS (TypeScript)
- Go (Gin/Fiber)

### 5.2 Database

**Primary:** PostgreSQL

**ORM:** Prisma

**Why Prisma?**
- ✅ Type-safe
- ✅ Auto-completion
- ✅ Migrations
- ✅ Great DX

### 5.3 Validation

**Library:** Zod

**Why Zod?**
- ✅ TypeScript-first
- ✅ Type inference
- ✅ Composable
- ✅ Great error messages

### 5.4 Testing

**Unit Tests:** Jest  
**Integration Tests:** Supertest  
**Coverage:** > 80%

### 5.5 Documentation

**API Docs:** OpenAPI 3.0 (Swagger)  
**Code Docs:** JSDoc + TypeDoc

---

## 6. Generator Architecture

### 6.1 Components

```
API Generator
├── Parser
│   └── Parse markdown spec → AST
├── Analyzer
│   └── Analyze complexity → Template vs AI
├── Template Engine
│   ├── Load templates
│   └── Render with data
├── AI Assistant
│   ├── Generate complex code
│   └── Optimize & validate
├── Validator
│   ├── Syntax check
│   ├── Type check
│   └── Lint
└── Output Writer
    └── Write files to disk
```

### 6.2 Workflow

```
1. Parse Input
   ↓
2. Analyze Complexity
   ↓
3. Generate Code
   ├─→ Template Engine (80%)
   └─→ AI Assistant (20%)
   ↓
4. Merge & Validate
   ↓
5. Run Tests
   ↓
6. Write Output
```

### 6.3 Implementation

```typescript
// api-generator.ts
export class APIGenerator {
  constructor(
    private parser: SpecParser,
    private analyzer: ComplexityAnalyzer,
    private templateEngine: TemplateEngine,
    private aiAssistant: AIAssistant,
    private validator: CodeValidator
  ) {}

  async generate(specFile: string): Promise<GeneratedAPI> {
    // 1. Parse
    const spec = await this.parser.parse(specFile);
    
    // 2. Analyze
    const analysis = await this.analyzer.analyze(spec);
    
    // 3. Generate
    const templateCode = await this.templateEngine.generate(
      spec,
      analysis.templateParts
    );
    
    const aiCode = await this.aiAssistant.generate(
      spec,
      analysis.aiParts
    );
    
    // 4. Merge
    const mergedCode = this.merge(templateCode, aiCode);
    
    // 5. Validate
    const validated = await this.validator.validate(mergedCode);
    
    // 6. Return
    return validated;
  }
}
```

---

## 7. Validation & Quality Gates

### 7.1 Pre-Generation Validation

**Input Validation:**
- ✅ Spec file exists
- ✅ Spec file is valid markdown
- ✅ Required sections present
- ✅ Entity definitions valid
- ✅ Endpoint definitions valid

### 7.2 Post-Generation Validation

**Code Quality:**
- ✅ TypeScript compiles (no errors)
- ✅ ESLint passes (no errors)
- ✅ Prettier formatted
- ✅ No security vulnerabilities (npm audit)

**Functional:**
- ✅ All tests pass
- ✅ Coverage > 80%
- ✅ API documentation generated

### 7.3 Validator Integration

**Use Existing Validator:**
```bash
python3 .smartspec/scripts/validate_generate_spec.py output/
```

**Custom API Validator:**
```bash
python3 .smartspec/scripts/validate_api_generator.py output/
```

---

## 8. Success Criteria

### 8.1 Week 2 (Demo)

**Must Have:**
- ✅ Generate basic CRUD API
- ✅ Single entity support
- ✅ Template-based generation working
- ✅ TypeScript output
- ✅ Basic tests

**Demo Scenario:**
```bash
# Input: Simple todo spec
# Output: Working CRUD API
# Time: < 2 minutes
```

### 8.2 Week 4 (Production)

**Must Have:**
- ✅ Multiple entities support
- ✅ Relationships support
- ✅ Complex business logic (AI-assisted)
- ✅ Full test coverage
- ✅ API documentation
- ✅ Error handling
- ✅ Validation
- ✅ Authentication integration

**Production Criteria:**
- ✅ Generates API in < 5 minutes
- ✅ Code quality score > 90%
- ✅ Test coverage > 80%
- ✅ Zero critical bugs
- ✅ Documentation complete

---

## 9. Non-Functional Requirements

### 9.1 Performance

- **Generation Time:** < 5 minutes for typical API (10 endpoints)
- **Memory Usage:** < 500 MB
- **Concurrent Generations:** Support 3+ parallel

### 9.2 Reliability

- **Success Rate:** > 95%
- **Error Recovery:** Automatic retry (3x)
- **Rollback:** Support rollback on failure

### 9.3 Usability

- **Learning Curve:** < 30 minutes to first API
- **Documentation:** Complete with examples
- **Error Messages:** Clear and actionable

### 9.4 Maintainability

- **Code Coverage:** > 80%
- **Documentation:** JSDoc for all public APIs
- **Versioning:** Semantic versioning
- **Backwards Compatibility:** Maintain for 2 major versions

---

## 10. Risks & Mitigation

### 10.1 Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| AI generates incorrect code | Medium | High | Validation layer + tests |
| Templates too rigid | Low | Medium | AI fallback for complex cases |
| Performance issues | Low | Medium | Caching + optimization |
| Spec parsing errors | Medium | Medium | Robust parser + validation |

### 10.2 Mitigation Strategies

**AI Quality:**
- ✅ Validation layer (syntax, types, lint)
- ✅ Automated tests
- ✅ Human review (optional)

**Template Flexibility:**
- ✅ AI fallback for complex cases
- ✅ Template customization support
- ✅ Plugin system (future)

**Performance:**
- ✅ Template caching
- ✅ Parallel generation
- ✅ Incremental generation

---

## 11. Future Enhancements

### Phase 2 (After Week 4)

- [ ] GraphQL support
- [ ] WebSocket support
- [ ] Multiple frameworks (FastAPI, NestJS)
- [ ] Custom templates
- [ ] Plugin system

### Phase 3 (Long-term)

- [ ] Visual API designer
- [ ] Real-time collaboration
- [ ] API versioning
- [ ] API analytics
- [ ] Performance monitoring

---

## 12. Acceptance Criteria

### Week 2 Demo

**Scenario:** Generate Todo CRUD API

**Input:**
```markdown
# Todo API
## Entity: Todo
- id, title, completed
## Endpoints:
- GET /todos
- POST /todos
- GET /todos/:id
- PUT /todos/:id
- DELETE /todos/:id
```

**Expected Output:**
- ✅ 5 endpoints working
- ✅ TypeScript code
- ✅ Basic tests passing
- ✅ < 2 minutes generation time

**Demo Success:** ✅ All stakeholders approve

---

### Week 4 Production

**Scenario:** Generate Complex SaaS API

**Input:**
```markdown
# SaaS API (10 entities, 30 endpoints)
- Users, Organizations, Projects, Tasks, Comments
- Authentication, Authorization
- Complex business rules
- Relationships, Joins
```

**Expected Output:**
- ✅ All endpoints working
- ✅ Business logic correct
- ✅ Tests passing (>80% coverage)
- ✅ API docs generated
- ✅ < 5 minutes generation time

**Production Success:** ✅ Ready for real projects

---

## 13. Dependencies

### 13.1 External

- Node.js >= 18
- TypeScript >= 5.0
- PostgreSQL >= 14
- OpenAI API key (for AI)

### 13.2 Internal

- SmartSpec validators
- SmartSpec templates
- Base validator (base_validator.py)

---

## 14. Timeline

### Week 0 (Current)
- [x] Requirements finalization
- [ ] Project structure setup
- [ ] Template design
- [ ] AI integration design

### Week 1-2
- [ ] Parser implementation
- [ ] Template engine
- [ ] Basic CRUD generation
- [ ] Demo preparation

### Week 3-4
- [ ] AI integration
- [ ] Complex logic support
- [ ] Testing & validation
- [ ] Documentation
- [ ] Production readiness

---

## Appendix A: Example Templates

See: `.smartspec/templates/api/`

## Appendix B: Example Specs

See: `examples/api-specs/`

## Appendix C: Testing Strategy

See: `tests/api-generator/`

---

**Status:** ✅ Requirements Finalized  
**Next:** Project Structure Setup  
**Owner:** Dev Team  
**Reviewers:** Tech Lead, Product Owner
