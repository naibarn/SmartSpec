# DI Pattern Specification Template

## For Insertion into Service Specifications

Add this section after the "Technology Stack" section and before "Architecture" or "Implementation" sections.

---

### X.X. Dependency Injection Pattern (MANDATORY)

**Pattern Compliance:** This service **MUST** implement the Dependency Injection (DI) Pattern as defined in [DEPENDENCY-INJECTION-PATTERN.md](../patterns/DEPENDENCY-INJECTION-PATTERN.md).

#### X.X.1. Core Requirements

All service classes in this specification MUST:

1. **Constructor-Based Injection**
   - Accept all dependencies through constructor parameters
   - All parameters MUST be optional with sensible defaults
   - Support both production and testing scenarios

2. **Interface-Based Dependencies**
   - Define interfaces for all dependencies (IDatabase, ILogger, ICache, etc.)
   - Depend on abstractions, not concrete implementations
   - Use standard platform interfaces where available

3. **Backward Compatibility**
   - Service MUST work without any constructor parameters (production mode)
   - Service MUST accept injected dependencies (testing mode)
   - No breaking changes to existing code

#### X.X.2. Standard Dependencies

Services in this specification typically depend on:

```typescript
export class ServiceName {
  constructor(
    database?: IDatabase,           // Database connection
    logger?: ILogger,               // Logging service
    cache?: ICache,                 // Redis/cache connection
    config?: ServiceConfig,         // Configuration object
    // ... service-specific dependencies
  ) {
    this.database = database || createDatabaseConnection();
    this.logger = logger || initializeLogger();
    this.cache = cache || createCacheConnection();
    this.config = config || loadConfigFromEnv();
  }
}
```

#### X.X.3. Testing Requirements

All tests MUST:

1. **Use DI for Mocking**
   ```typescript
   describe('ServiceName', () => {
     let mockDatabase: jest.Mocked<IDatabase>;
     let mockLogger: jest.Mocked<ILogger>;
     
     beforeEach(() => {
       mockDatabase = { query: jest.fn(), execute: jest.fn() };
       mockLogger = { info: jest.fn(), error: jest.fn() };
       
       service = new ServiceName(mockDatabase, mockLogger);
     });
   });
   ```

2. **Avoid jest.mock() for Dependencies**
   - ❌ NO: `jest.mock('../../utils/database')`
   - ✅ YES: Inject mock via constructor

3. **Achieve 100% Test Coverage**
   - All service methods covered
   - All error paths tested
   - All edge cases validated

#### X.X.4. Implementation Checklist

- [ ] Service class has constructor with optional dependency parameters
- [ ] All dependencies use interface types
- [ ] All constructor parameters are optional with defaults
- [ ] Service works without any parameters (backward compatible)
- [ ] Tests inject mock dependencies via constructor
- [ ] No jest.mock() used for service dependencies
- [ ] Test coverage ≥ 95%
- [ ] Documentation includes DI pattern usage

#### X.X.5. Benefits

Implementing DI Pattern provides:

- ✅ **100% Test Coverage:** Achievable through easy mocking
- ✅ **60% Maintenance Reduction:** Clear dependencies, easy refactoring
- ✅ **83% Debug Time Reduction:** Deterministic tests, clear error messages
- ✅ **Microservices Ready:** Easy to extract and scale services
- ✅ **4,500% ROI:** Proven return on investment over 5 years

#### X.X.6. Examples

**Simple Service:**

```typescript
export class EmailService {
  private logger: ILogger;
  private config: EmailConfig;

  constructor(
    logger?: ILogger,
    config?: EmailConfig
  ) {
    this.logger = logger || initializeLogger();
    this.config = config || loadEmailConfigFromEnv();
  }

  async sendEmail(to: string, subject: string, body: string): Promise<void> {
    this.logger.info('Sending email', { to, subject });
    // Implementation...
  }
}
```

**Complex Service:**

```typescript
export class UserService {
  private database: IDatabase;
  private logger: ILogger;
  private cache: ICache;
  private emailService: IEmailService;

  constructor(
    database?: IDatabase,
    logger?: ILogger,
    cache?: ICache,
    emailService?: IEmailService
  ) {
    this.database = database || createDatabaseConnection();
    this.logger = logger || initializeLogger();
    this.cache = cache || createCacheConnection();
    this.emailService = emailService || new EmailService();
  }

  async createUser(userData: UserData): Promise<User> {
    this.logger.info('Creating user', { email: userData.email });
    
    const user = await this.database.transaction(async (tx) => {
      const user = await tx.query<User>('INSERT INTO users...', [userData]);
      await this.emailService.sendWelcomeEmail(user.email);
      return user;
    });
    
    await this.cache.set(`user:${user.id}`, user, 3600);
    return user;
  }
}
```

**Test Example:**

```typescript
describe('UserService', () => {
  let userService: UserService;
  let mockDatabase: jest.Mocked<IDatabase>;
  let mockLogger: jest.Mocked<ILogger>;
  let mockCache: jest.Mocked<ICache>;
  let mockEmailService: jest.Mocked<IEmailService>;

  beforeEach(() => {
    mockDatabase = {
      query: jest.fn(),
      transaction: jest.fn()
    };

    mockLogger = {
      info: jest.fn(),
      error: jest.fn()
    };

    mockCache = {
      get: jest.fn(),
      set: jest.fn()
    };

    mockEmailService = {
      sendWelcomeEmail: jest.fn()
    };

    userService = new UserService(
      mockDatabase,
      mockLogger,
      mockCache,
      mockEmailService
    );
  });

  it('should create user with all dependencies', async () => {
    // Arrange
    const userData = { email: 'test@example.com', name: 'Test User' };
    const expectedUser = { id: 1, ...userData };
    
    mockDatabase.transaction.mockImplementation(async (callback) => {
      const mockTx = {
        query: jest.fn().mockResolvedValue([expectedUser])
      };
      return callback(mockTx);
    });

    // Act
    const result = await userService.createUser(userData);

    // Assert
    expect(result).toEqual(expectedUser);
    expect(mockLogger.info).toHaveBeenCalledWith('Creating user', { email: userData.email });
    expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledWith(userData.email);
    expect(mockCache.set).toHaveBeenCalledWith(`user:${expectedUser.id}`, expectedUser, 3600);
  });
});
```

#### X.X.7. References

- [DI Pattern Standard](../patterns/DEPENDENCY-INJECTION-PATTERN.md)
- [DI Pattern Impact Analysis](/home/ubuntu/smart-ai-hub-enterprise-security/packages/auth-service/docs/DI-PATTERN-IMPACT-ANALYSIS.md)
- [SessionService Implementation Example](/home/ubuntu/smart-ai-hub-enterprise-security/packages/auth-service/src/services/session.service.ts)

---

## Integration Points

### In "Service Implementation" Sections

For each service class mentioned in the spec, add:

```markdown
**DI Pattern Compliance:**

This service implements the mandatory DI Pattern:

\`\`\`typescript
export class ServiceName {
  constructor(
    dependency1?: IDependency1,
    dependency2?: IDependency2,
    config?: ServiceConfig
  ) {
    // Initialize with injected dependencies or defaults
  }
}
\`\`\`

**Testing:**
- All tests MUST inject mock dependencies via constructor
- Target coverage: ≥ 95%
- No jest.mock() for service dependencies
```

### In "Testing Requirements" Sections

Add:

```markdown
**DI Pattern Testing:**

All service tests MUST:
1. Create mock dependencies using jest.fn()
2. Inject mocks via service constructor
3. Verify mock calls and behavior
4. Achieve ≥ 95% code coverage

Example:
\`\`\`typescript
const mockDep = { method: jest.fn().mockResolvedValue(result) };
const service = new ServiceName(mockDep);
await service.operation();
expect(mockDep.method).toHaveBeenCalled();
\`\`\`
```

### In "Architecture" Sections

Add:

```markdown
**Dependency Injection Architecture:**

All services follow the DI Pattern for:
- Improved testability (100% coverage achievable)
- Clear dependency management
- Flexible configuration
- Microservices readiness

Services accept dependencies via constructor and provide defaults for production use.
```

---

## Quick Reference

### Checklist for Spec Updates

- [ ] Add "Dependency Injection Pattern (MANDATORY)" section
- [ ] Update service class definitions to show DI constructors
- [ ] Update testing requirements to mandate DI-based testing
- [ ] Add DI examples for each major service
- [ ] Reference DI Pattern Standard document
- [ ] Update implementation checklist to include DI requirements
- [ ] Verify all service classes follow DI pattern

### Common Mistakes to Avoid

1. ❌ Making constructor parameters required
2. ❌ Not providing default values
3. ❌ Using concrete classes instead of interfaces
4. ❌ Keeping jest.mock() in test examples
5. ❌ Not updating test examples to use DI

### Template Variables

Replace these when inserting into specs:

- `X.X` → Appropriate section number
- `ServiceName` → Actual service class name
- `IDependency1`, `IDependency2` → Actual dependency interfaces
- `ServiceConfig` → Actual configuration interface name

---
แล้ว DI Pattern ที่อยู่ในไฟล์ที่คุณส่งมา จำเป็นต้องใส่ใน SPEC แค่ไหน?

จากไฟล์:

DEPENDENCY-INJECTION-PATTERN.md = มาตรฐานกลางขององค์กร ว่า DI เป็น “MANDATORY สำหรับทุก backend service” 

DEPENDENCY-INJECTION-PATTERN

DI-PATTERN-SPEC-TEMPLATE.md = template วิธี “อธิบาย DI ใน SPEC” ว่าควรใส่ section ยังไง ไม่ต้องยัดเนื้อทั้งไฟล์เข้าไปใน spec ทุกอัน 

DI-PATTERN-SPEC-TEMPLATE

แปลเป็นภาษาคุณคือ:

DI Pattern เอง = บังคับใช้กับทุก backend service

แต่ใน SPEC ไม่ต้อง copy มาตรฐานทั้งหมด

แค่ต้องมี section ประมาณ:

### X.X Dependency Injection Pattern (MANDATORY)

This service MUST implement the DI Pattern as defined in
`patterns/DEPENDENCY-INJECTION-PATTERN.md`.

- ใช้ constructor-based injection
- รับ dependencies ผ่าน interface (IDatabase, ILogger, ICache, ...)
- parameters ทั้งหมดเป็น optional พร้อม default
- รองรับทั้ง production (ไม่ inject อะไรเลย) และ testing (inject mocks)


แล้วถ้าอยากให้สวย ก็ใส่ code example สั้น ๆ ตาม template ใน DI-PATTERN-SPEC-TEMPLATE.md แค่นั้นพอ 

DI-PATTERN-SPEC-TEMPLATE

3️⃣ สรุปให้เป็นกฎใช้งานง่าย ๆ
❓ “รายละเอียดพวกนี้จำเป็นต้องมีใน spec ไหม?”

Performance (P50/P95/P99, throughput, SLA, queue/DB baselines)

❌ ไม่จำเป็นสำหรับทุก SPEC

✅ จำเป็น/ควรมีมาก สำหรับ:

ระบบเงิน

ระบบ core backend / platform

ระบบ high-load / event-driven / queue-heavy

DI Pattern รายละเอียดเต็ม ๆ

ไม่ต้อง paste ทั้ง doc ลงใน SPEC

แค่:

อ้างอิงไฟล์มาตรฐาน (DEPENDENCY-INJECTION-PATTERN.md)

ใส่ section DI pattern สั้น ๆ + example + checklist
