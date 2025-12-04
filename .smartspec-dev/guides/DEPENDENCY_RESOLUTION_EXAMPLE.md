# ตัวอย่างการใช้งาน Dependency Resolution

## Input: User Specification

เมื่อผู้ใช้ระบุ dependencies ในการสร้าง SPEC:

```
Create SPEC for payment system with dependencies:
- spec-core-001-authentication
- spec-core-002-authorization
- spec-core-003-audit-logging
- spec-core-004-rate-limiting
- spec-002-user-management
- spec-012-subscription-plans
- spec-013-promptpay-credit-topup
```

## Step 1: Load SPEC_INDEX.json

```json
{
  "specs": [
    {
      "id": "spec-core-001-authentication",
      "title": "Authentication System",
      "repo": "private",
      "category": "core",
      "path": "specs/core/spec-core-001-authentication"
    },
    {
      "id": "spec-core-002-authorization",
      "title": "Authorization & RBAC",
      "repo": "private",
      "category": "core",
      "path": "specs/core/spec-core-002-authorization"
    },
    {
      "id": "spec-002-user-management",
      "title": "User Management",
      "repo": "public",
      "category": "feature",
      "path": "specs/feature/spec-002-user-management"
    }
  ]
}
```

## Step 2: Resolve Each Dependency

### Dependency: spec-core-001-authentication

**Lookup result:**
```json
{
  "id": "spec-core-001-authentication",
  "title": "Authentication System",
  "repo": "private",
  "category": "core",
  "path": "specs/core/spec-core-001-authentication"
}
```

**Formatted output:**
```
- **spec-core-001-authentication** - Authentication System - Spec Path: "specs/core/spec-core-001-authentication/spec.md" Repo: private
```

### Dependency: spec-002-user-management

**Lookup result:**
```json
{
  "id": "spec-002-user-management",
  "title": "User Management",
  "repo": "public",
  "category": "feature",
  "path": "specs/feature/spec-002-user-management"
}
```

**Formatted output:**
```
- **spec-002-user-management** - User Management - Spec Path: "specs/feature/spec-002-user-management/spec.md" Repo: public
```

## Step 3: Group by Category

### Core Dependencies (category: "core")
- spec-core-001-authentication
- spec-core-002-authorization
- spec-core-003-audit-logging
- spec-core-004-rate-limiting

### Feature Specs (category: "feature")
- spec-002-user-management
- spec-012-subscription-plans
- spec-013-promptpay-credit-topup

## Step 4: Generate Final Output

```markdown
## 19. Related Specs

### 19.1. Core Dependencies
- **spec-core-001-authentication** - User authentication for financial operations - Spec Path: "specs/core/spec-core-001-authentication/spec.md" Repo: private
- **spec-core-002-authorization** - RBAC for admin financial operations - Spec Path: "specs/core/spec-core-002-authorization/spec.md" Repo: private
- **spec-core-003-audit-logging** - Audit trail for all financial transactions - Spec Path: "specs/core/spec-core-003-audit-logging/spec.md" Repo: private
- **spec-core-004-rate-limiting** - Rate limiting for payment endpoints - Spec Path: "specs/core/spec-core-004-rate-limiting/spec.md" Repo: private

### 19.2. Feature Specs
- **spec-002-user-management** - User profile and account management - Spec Path: "specs/feature/spec-002-user-management/spec.md" Repo: public
- **spec-012-subscription-plans** - Subscription plan definitions - Spec Path: "specs/feature/spec-012-subscription-plans/spec.md" Repo: public
- **spec-013-promptpay-credit-topup** - PromptPay payment integration - Spec Path: "specs/feature/spec-013-promptpay-credit-topup/spec.md" Repo: public
```

## Error Cases

### Case 1: Spec Not Found

**Input:** spec-unknown-999

**Lookup result:** Not found in SPEC_INDEX.json

**Output:**
```
- **spec-unknown-999** - [NOT FOUND IN SPEC_INDEX] - Spec Path: "N/A" Repo: unknown
```

### Case 2: SPEC_INDEX.json Missing

**Warning message:**
```
⚠️ Warning: SPEC_INDEX.json not found at .smartspec/SPEC_INDEX.json
Dependencies will be listed without path/repo information.
```

**Output:**
```markdown
## 19. Related Specs

⚠️ Warning: SPEC_INDEX.json not found. Dependencies listed without path/repo information.

- **spec-core-001-authentication** - User authentication for financial operations
- **spec-core-002-authorization** - RBAC for admin financial operations
```

## Alternative: User-Provided Index File

ผู้ใช้สามารถระบุไฟล์ index เอง:

```bash
/smartspec_generate_spec.md --spec-index=custom-index.json
```

จากนั้น workflow จะอ่านจากไฟล์ที่ระบุแทน `.smartspec/SPEC_INDEX.json`

## Integration with Other Workflows

### Generate Plan Workflow

เมื่อ `smartspec_generate_plan.md` อ่าน SPEC ที่มี dependencies แบบสมบูรณ์:

```markdown
**Related Specs:** (Resolved from SPEC_INDEX)
- **spec-core-001-authentication** (`specs/core/spec-core-001-authentication/spec.md`, repo: private) - Authentication System
- **spec-feature-002-user-management** (`specs/feature/spec-feature-002-user-management/spec.md`, repo: private) - User Management
```

### Generate Tasks Workflow

Tasks สามารถอ้างอิงถึง spec dependencies ได้โดยตรง:

```markdown
**Dependencies:**
- Read spec-core-001-authentication at `specs/core/spec-core-001-authentication/spec.md`
- Implement authentication integration as specified
```

## Benefits

1. **ความสมบูรณ์:** มีข้อมูล path และ repo ครบถ้วน
2. **ความสะดวก:** สามารถนำไปใช้งานได้ทันที
3. **ความถูกต้อง:** อ่านจาก SPEC_INDEX.json ที่เป็นแหล่งข้อมูลกลาง
4. **ความยืดหยุ่น:** รองรับทั้งกรณีมีและไม่มี SPEC_INDEX.json
5. **การจัดกลุ่ม:** แบ่งตาม category ทำให้อ่านง่าย
