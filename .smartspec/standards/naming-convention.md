# SmartSpec Naming Convention Standard

**Version:** 1.0.0  
**Date:** 2025-12-27  
**Status:** Official Standard  
**Applies to:** All SmartSpec projects

---

## 📖 Table of Contents

1. [Introduction](#introduction)
2. [File Naming Rules](#file-naming-rules)
3. [Directory Structure](#directory-structure)
4. [Package Placement](#package-placement)
5. [Test Files](#test-files)
6. [Validation Rules](#validation-rules)
7. [Examples](#examples)
8. [Anti-Patterns](#anti-patterns)
9. [Exceptions](#exceptions)
10. [Enforcement](#enforcement)

---

## Introduction

### Purpose

This standard defines **mandatory** naming conventions for all files in SmartSpec projects to ensure:

- **Consistency** across all packages and services
- **Predictability** in file locations and naming
- **Maintainability** through clear, unambiguous names
- **Automation** through standardized patterns

### Scope

This standard applies to:

- ✅ All TypeScript files (`.ts`, `.tsx`)
- ✅ All JavaScript files (`.js`, `.jsx`)
- ✅ All test files
- ✅ All configuration files
- ✅ All documentation files

### Principles

1. **Explicit over Implicit** - Names should be clear and unambiguous
2. **Consistency over Convenience** - Follow rules even if longer
3. **Purpose over Brevity** - Clarity is more important than short names
4. **Convention over Configuration** - Standard patterns, minimal exceptions

---

## File Naming Rules

### 1. Case Convention

**Rule:** Use `kebab-case` for all file names

**Format:** `word1-word2-word3.suffix.ext`

**Examples:**
```
✅ CORRECT:
- user-service.ts
- sms-provider.ts
- jwt-util.ts
- password-hash.ts
- api-key-model.ts
- auth-middleware.ts

❌ INCORRECT:
- userService.ts        (camelCase)
- SMSProvider.ts        (PascalCase)
- jwt_util.ts           (snake_case)
- User_Service.ts       (mixed case)
- user.service.ts       (dot separator - reserved for suffixes)
```

**Rationale:**
- **Case-insensitive safe** - Works on all file systems
- **URL-friendly** - Can be used in URLs without encoding
- **Readable** - Easy to read and type
- **Standard** - Common in web development

---

### 2. File Suffixes

**Rule:** Use specific suffixes to indicate file purpose

#### Core Suffixes

| Suffix | Purpose | Example |
|:-------|:--------|:--------|
| `.service.ts` | Business logic services | `user-service.ts` |
| `.provider.ts` | External integrations | `sms-provider.ts` |
| `.client.ts` | API clients | `oauth-client.ts` |
| `.controller.ts` | HTTP controllers | `auth-controller.ts` |
| `.middleware.ts` | Express middleware | `auth-middleware.ts` |
| `.util.ts` | Utility functions | `jwt-util.ts` |
| `.helper.ts` | Helper functions | `date-helper.ts` |
| `.model.ts` | Data models | `user-model.ts` |
| `.schema.ts` | Validation schemas | `user-schema.ts` |
| `.config.ts` | Configuration | `database-config.ts` |
| `.constant.ts` | Constants | `error-constant.ts` |
| `.type.ts` | TypeScript types | `user-type.ts` |
| `.interface.ts` | TypeScript interfaces | `api-interface.ts` |
| `.enum.ts` | TypeScript enums | `role-enum.ts` |
| `.guard.ts` | Route guards | `auth-guard.ts` |
| `.decorator.ts` | Decorators | `cache-decorator.ts` |
| `.factory.ts` | Factory functions | `user-factory.ts` |
| `.repository.ts` | Data repositories | `user-repository.ts` |
| `.dto.ts` | Data transfer objects | `create-user-dto.ts` |

#### Suffix Selection Guide

**Use `.service.ts` when:**
- Implementing business logic
- Orchestrating multiple operations
- Managing application state

**Example:**
```typescript
// user-service.ts
export class UserService {
  async createUser(data: CreateUserDto): Promise<User> {
    // Business logic
  }
}
```

**Use `.provider.ts` when:**
- Integrating with external services
- Wrapping third-party APIs
- Managing external connections

**Example:**
```typescript
// sms-provider.ts
export class SmsProvider {
  async sendSms(phone: string, message: string): Promise<void> {
    // External API call
  }
}
```

**Use `.client.ts` when:**
- Creating API clients
- HTTP request wrappers
- SDK implementations

**Example:**
```typescript
// oauth-client.ts
export class OAuthClient {
  async getAccessToken(code: string): Promise<string> {
    // OAuth flow
  }
}
```

**Use `.util.ts` when:**
- Pure utility functions
- No side effects
- Reusable across modules

**Example:**
```typescript
// jwt-util.ts
export function generateToken(payload: any): string {
  // JWT generation
}
```

**Use `.helper.ts` when:**
- Helper functions with side effects
- Context-specific utilities
- Not pure functions

**Example:**
```typescript
// date-helper.ts
export function formatDate(date: Date): string {
  // Date formatting with locale
}
```

---

### 3. Multi-Word Names

**Rule:** Separate words with hyphens, use descriptive names

**Examples:**
```
✅ CORRECT:
- user-authentication-service.ts
- sms-verification-provider.ts
- jwt-token-util.ts
- password-hash-helper.ts
- api-key-validation-middleware.ts

❌ INCORRECT:
- userauth.ts              (too abbreviated)
- sms.ts                   (too generic)
- jwt.ts                   (no suffix)
- pwd.ts                   (unclear abbreviation)
```

**Rationale:**
- **Clarity** - Full words are clearer than abbreviations
- **Searchability** - Easy to find with full-text search
- **Maintainability** - New developers understand purpose

---

### 4. Abbreviations

**Rule:** Avoid abbreviations except for well-known acronyms

**Allowed Abbreviations:**
```
✅ ALLOWED:
- API, HTTP, HTTPS, URL, URI
- JWT, OAuth, SAML
- SMS, MMS, Email
- JSON, XML, YAML
- SQL, NoSQL
- ID (identifier)
- DTO (data transfer object)
- UUID, GUID

❌ NOT ALLOWED:
- usr (user)
- pwd (password)
- auth (authentication) - use full word
- svc (service) - use full word
- cfg (config) - use full word
```

**Examples:**
```
✅ CORRECT:
- jwt-util.ts
- oauth-client.ts
- sms-provider.ts
- api-key-model.ts
- user-dto.ts

❌ INCORRECT:
- usr-svc.ts
- pwd-util.ts
- auth-svc.ts
- cfg-helper.ts
```

---

## Directory Structure

### 1. Standard Package Structure

**Rule:** Follow standard directory structure for all packages

```
packages/
  {package-name}/
    src/
      controllers/      # HTTP controllers
      services/         # Business logic services
      providers/        # External integrations
      clients/          # API clients
      middleware/       # Express middleware
      guards/           # Route guards
      decorators/       # Decorators
      models/           # Data models
      schemas/          # Validation schemas
      repositories/     # Data repositories
      dto/              # Data transfer objects
      utils/            # Utility functions
      helpers/          # Helper functions
      config/           # Configuration
      constants/        # Constants
      types/            # TypeScript types
      interfaces/       # TypeScript interfaces
      enums/            # TypeScript enums
      factories/        # Factory functions
    tests/
      unit/             # Unit tests
      integration/      # Integration tests
      e2e/              # End-to-end tests
      fixtures/         # Test fixtures
      mocks/            # Test mocks
```

### 2. Directory Placement Rules

**Rule:** Place files in appropriate directories based on purpose

| File Type | Directory | Example |
|:----------|:----------|:--------|
| Business logic | `services/` | `user-service.ts` |
| External integration | `providers/` | `sms-provider.ts` |
| API client | `clients/` | `oauth-client.ts` |
| HTTP controller | `controllers/` | `auth-controller.ts` |
| Middleware | `middleware/` | `auth-middleware.ts` |
| Data model | `models/` | `user-model.ts` |
| Validation schema | `schemas/` | `user-schema.ts` |
| Utility function | `utils/` | `jwt-util.ts` |
| Helper function | `helpers/` | `date-helper.ts` |
| Configuration | `config/` | `database-config.ts` |
| Constants | `constants/` | `error-constant.ts` |
| TypeScript types | `types/` | `user-type.ts` |

**Examples:**
```
✅ CORRECT:
packages/auth-lib/src/services/user-service.ts
packages/auth-lib/src/providers/sms-provider.ts
packages/auth-lib/src/utils/jwt-util.ts
packages/auth-lib/src/models/user-model.ts

❌ INCORRECT:
packages/auth-lib/src/user-service.ts           (missing directory)
packages/auth-lib/src/integrations/sms-provider.ts  (use providers/)
packages/auth-lib/src/lib/jwt-util.ts           (use utils/)
```

---

## Package Placement

### 1. Package Types

**Rule:** Place files in appropriate package types

| Package Type | Purpose | Examples |
|:-------------|:--------|:---------|
| `*-lib` | Shared code, utilities, models | `auth-lib`, `core-lib` |
| `*-service` | Business logic, APIs, controllers | `auth-service`, `user-service` |
| `*-client` | Client libraries, SDKs | `auth-client`, `api-client` |
| `*-common` | Common utilities, shared types | `common`, `shared` |

### 2. Placement Rules

**Rule:** Place files based on reusability and purpose

**Shared Code → `*-lib` packages:**
```
✅ CORRECT:
packages/auth-lib/src/providers/sms-provider.ts
packages/auth-lib/src/utils/jwt-util.ts
packages/auth-lib/src/models/user-model.ts

Rationale: Reusable across multiple services
```

**Business Logic → `*-service` packages:**
```
✅ CORRECT:
packages/auth-service/src/services/auth-service.ts
packages/auth-service/src/controllers/auth-controller.ts
packages/auth-service/src/middleware/auth-middleware.ts

Rationale: Service-specific business logic
```

**Client Libraries → `*-client` packages:**
```
✅ CORRECT:
packages/auth-client/src/client.ts
packages/auth-client/src/types/auth-type.ts

Rationale: Client-side usage
```

### 3. Cross-Package References

**Rule:** Follow dependency hierarchy

```
Allowed:
- service → lib ✅
- service → common ✅
- client → lib ✅
- client → common ✅

Not Allowed:
- lib → service ❌
- lib → client ❌
- service → client ❌ (usually)
```

---

## Test Files

### 1. Test File Naming

**Rule:** Mirror source file with `.test.ts` or `.spec.ts` suffix

**Format:** `{source-name}.{test-type}.test.ts`

**Examples:**
```
Source: user-service.ts
Tests:
  - user-service.test.ts                    (unit test)
  - user-service.integration.test.ts        (integration test)
  - user-service.e2e.test.ts                (e2e test)
  - user-service.edge-cases.test.ts         (edge cases)
  - user-service.performance.test.ts        (performance test)
```

### 2. Test Directory Structure

**Rule:** Mirror source directory structure in tests/

```
Source:
packages/auth-lib/src/services/user-service.ts

Tests:
packages/auth-lib/tests/unit/services/user-service.test.ts
packages/auth-lib/tests/integration/services/user-service.integration.test.ts
```

### 3. Test Types

| Test Type | Suffix | Purpose |
|:----------|:-------|:--------|
| Unit | `.test.ts` | Test individual functions/classes |
| Integration | `.integration.test.ts` | Test module interactions |
| E2E | `.e2e.test.ts` | Test complete flows |
| Edge Cases | `.edge-cases.test.ts` | Test edge cases |
| Performance | `.performance.test.ts` | Performance benchmarks |

---

## Validation Rules

### 1. Strict Mode

**Rule:** Exact match required in strict mode

```
Expected: packages/auth-lib/src/providers/sms-provider.ts
Found:    packages/auth-lib/src/providers/sms-provider.ts
Result:   ✅ PASS

Expected: packages/auth-lib/src/providers/sms-provider.ts
Found:    packages/auth-lib/src/services/sms-service.ts
Result:   ❌ FAIL (naming issue)
```

### 2. Naming Convention Checks

**Validation Checklist:**

1. ✅ **Case Convention** - kebab-case
2. ✅ **Suffix** - Correct suffix for file type
3. ✅ **Directory** - Correct directory for file type
4. ✅ **Package** - Correct package for file purpose
5. ✅ **No Abbreviations** - Full words (except allowed acronyms)
6. ✅ **Descriptive** - Clear, unambiguous name

**Example Validation:**
```
File: packages/auth-lib/src/providers/sms-provider.ts

Checks:
1. ✅ kebab-case: "sms-provider"
2. ✅ Suffix: ".provider.ts" (external integration)
3. ✅ Directory: "providers/" (correct for integrations)
4. ✅ Package: "auth-lib" (shared code)
5. ✅ No abbreviations: "sms" is allowed acronym
6. ✅ Descriptive: Clear purpose

Result: ✅ PASS
```

### 3. Fuzzy Matching (Fallback)

**Rule:** Only use fuzzy matching after strict check fails

**Threshold:** ≥80% similarity

**Process:**
1. Try exact match
2. If fails, check naming convention compliance
3. If compliant but not found, try fuzzy match (≥80%)
4. If multiple matches, require manual review

---

## Examples

### Complete Examples

#### Example 1: SMS Provider

**Purpose:** External SMS service integration

**Correct:**
```
File: packages/auth-lib/src/providers/sms-provider.ts
Test: packages/auth-lib/tests/unit/providers/sms-provider.test.ts

Rationale:
- kebab-case: "sms-provider"
- Suffix: ".provider.ts" (external integration)
- Directory: "providers/" (external services)
- Package: "auth-lib" (shared integration)
```

**Incorrect:**
```
❌ packages/auth-lib/src/integrations/sms.provider.ts
   (wrong directory, wrong naming)

❌ packages/auth-service/src/services/sms-service.ts
   (wrong package, wrong suffix)

❌ packages/auth-lib/src/smsProvider.ts
   (no directory, wrong case, no suffix)
```

#### Example 2: User Service

**Purpose:** User management business logic

**Correct:**
```
File: packages/auth-service/src/services/user-service.ts
Test: packages/auth-service/tests/unit/services/user-service.test.ts

Rationale:
- kebab-case: "user-service"
- Suffix: ".service.ts" (business logic)
- Directory: "services/" (business logic)
- Package: "auth-service" (service-specific)
```

**Incorrect:**
```
❌ packages/auth-lib/src/services/user-service.ts
   (wrong package - should be in service, not lib)

❌ packages/auth-service/src/userService.ts
   (no directory, wrong case)

❌ packages/auth-service/src/services/user.ts
   (no suffix)
```

#### Example 3: JWT Utility

**Purpose:** JWT token generation and validation

**Correct:**
```
File: packages/auth-lib/src/utils/jwt-util.ts
Test: packages/auth-lib/tests/unit/utils/jwt-util.test.ts

Rationale:
- kebab-case: "jwt-util"
- Suffix: ".util.ts" (utility function)
- Directory: "utils/" (utilities)
- Package: "auth-lib" (shared utility)
```

**Incorrect:**
```
❌ packages/auth-lib/src/jwt.ts
   (no directory, no suffix)

❌ packages/auth-lib/src/utils/jwtUtil.ts
   (wrong case)

❌ packages/auth-lib/src/helpers/jwt-helper.ts
   (wrong directory - utils not helpers for pure functions)
```

---

## Anti-Patterns

### Common Mistakes

#### 1. Wrong Case

```
❌ WRONG:
- userService.ts        (camelCase)
- UserService.ts        (PascalCase)
- user_service.ts       (snake_case)

✅ CORRECT:
- user-service.ts       (kebab-case)
```

#### 2. Missing Suffix

```
❌ WRONG:
- user.ts               (no suffix - ambiguous)
- sms.ts                (no suffix - unclear purpose)
- jwt.ts                (no suffix - could be anything)

✅ CORRECT:
- user-service.ts       (clear purpose)
- sms-provider.ts       (clear purpose)
- jwt-util.ts           (clear purpose)
```

#### 3. Wrong Directory

```
❌ WRONG:
- packages/auth-lib/src/integrations/sms-provider.ts
  (use providers/ not integrations/)

- packages/auth-lib/src/lib/jwt-util.ts
  (use utils/ not lib/)

✅ CORRECT:
- packages/auth-lib/src/providers/sms-provider.ts
- packages/auth-lib/src/utils/jwt-util.ts
```

#### 4. Wrong Package

```
❌ WRONG:
- packages/auth-service/src/providers/sms-provider.ts
  (shared integration should be in lib)

- packages/auth-lib/src/services/auth-service.ts
  (service-specific logic should be in service)

✅ CORRECT:
- packages/auth-lib/src/providers/sms-provider.ts
- packages/auth-service/src/services/auth-service.ts
```

#### 5. Over-Abbreviation

```
❌ WRONG:
- usr-svc.ts            (unclear abbreviations)
- pwd-util.ts           (unclear abbreviations)
- auth-cfg.ts           (use full words)

✅ CORRECT:
- user-service.ts       (clear and explicit)
- password-util.ts      (clear and explicit)
- auth-config.ts        (clear and explicit)
```

---

## Exceptions

### Allowed Exceptions

#### 1. Framework Files

**Exception:** Framework-specific files may use framework conventions

**Examples:**
```
✅ ALLOWED:
- index.ts              (entry point)
- main.ts               (application entry)
- app.ts                (application setup)
- server.ts             (server setup)
```

#### 2. Configuration Files

**Exception:** Configuration files may use standard names

**Examples:**
```
✅ ALLOWED:
- package.json
- tsconfig.json
- .eslintrc.js
- jest.config.js
```

#### 3. Documentation Files

**Exception:** Documentation files may use standard names

**Examples:**
```
✅ ALLOWED:
- README.md
- CHANGELOG.md
- LICENSE.md
- CONTRIBUTING.md
```

### Requesting Exceptions

**Process:**
1. Document reason for exception
2. Get approval from tech lead
3. Add to exceptions list
4. Document in code comments

---

## Enforcement

### 1. Validation Levels

| Level | Description | Action |
|:------|:------------|:-------|
| **ERROR** | Naming convention violation | Block commit/PR |
| **WARNING** | Potential issue | Allow but report |
| **INFO** | Suggestion | No action |

### 2. Enforcement Tools

**Pre-commit Hook:**
```bash
# Validate naming convention before commit
npm run validate:naming
```

**CI/CD Pipeline:**
```bash
# Validate naming convention in CI
npm run validate:naming --strict
```

**IDE Integration:**
```bash
# ESLint plugin for naming convention
eslint-plugin-smartspec-naming
```

### 3. Migration Period

**Grace Period:** 30 days from standard publication

**During Grace Period:**
- **New files:** Must follow standard (ERROR)
- **Existing files:** Warning only
- **Modified files:** Should follow standard (WARNING)

**After Grace Period:**
- **All files:** Must follow standard (ERROR)

---

## Summary

### Quick Reference

**File Naming:**
- ✅ Use kebab-case
- ✅ Use specific suffixes
- ✅ Use descriptive names
- ✅ Avoid abbreviations (except acronyms)

**Directory Structure:**
- ✅ Follow standard structure
- ✅ Place files in appropriate directories
- ✅ Mirror structure in tests

**Package Placement:**
- ✅ Shared code in `*-lib`
- ✅ Business logic in `*-service`
- ✅ Client code in `*-client`

**Validation:**
- ✅ Exact match first
- ✅ Check naming convention
- ✅ Fuzzy match last resort

### Benefits

1. **Consistency** - Same patterns everywhere
2. **Predictability** - Easy to find files
3. **Maintainability** - Clear purpose from name
4. **Automation** - Standardized patterns enable tooling

---

## Version History

**Version 1.0.0** (2025-12-27)
- ✅ Initial standard
- ✅ File naming rules
- ✅ Directory structure
- ✅ Package placement
- ✅ Validation rules
- ✅ Examples and anti-patterns

---

**Status:** ✅ **OFFICIAL STANDARD**  
**Effective Date:** 2025-12-27  
**Review Date:** 2026-01-27 (monthly review)
