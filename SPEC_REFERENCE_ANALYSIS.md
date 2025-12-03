# การวิเคราะห์รูปแบบการอ้างอิง Spec Dependencies

## รูปแบบปัจจุบัน (ไม่สมบูรณ์)

```markdown
### 19.1. Core Dependencies
- **spec-core-001-authentication** - User authentication for financial operations
- **spec-core-002-authorization** - RBAC for admin financial operations
- **spec-core-003-audit-logging** - Audit trail for all financial transactions
- **spec-core-004-rate-limiting** - Rate limiting for payment endpoints

### 19.2. Feature Specs
- **spec-002-user-management** - User profile and account management
- **spec-012-subscription-plans** - Subscription plan definitions
- **spec-013-promptpay-credit-topup** - PromptPay payment integration
```

**ปัญหา:**
- ไม่มี path ของไฟล์ spec
- ไม่มีข้อมูล repo (public/private)
- ไม่สามารถนำไปใช้งานได้โดยตรง

## รูปแบบที่ถูกต้อง (ตาม COMPLETE_EXAMPLE.md)

```markdown
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

**ข้อดี:**
- มี path ของไฟล์ spec ที่ชัดเจน
- มีข้อมูล repo (public/private)
- สามารถนำไปใช้งานได้โดยตรง
- อ่านค่าจาก SPEC_INDEX.json

## โครงสร้างข้อมูลใน SPEC_INDEX.json

```json
{
  "id": "spec-core-001-authentication",
  "title": "Authentication System",
  "repo": "private",
  "category": "core",
  "status": "active",
  "priority": "high",
  "path": "specs/core/spec-core-001-authentication",
  "dependencies": [...]
}
```

**ข้อมูลที่ต้องดึงมาใช้:**
1. `id` - Spec ID
2. `title` - ชื่อ Spec
3. `path` - Path ของ Spec (ต้องเพิ่ม `/spec.md` ท้าย)
4. `repo` - Repository type (public/private)

## รูปแบบ Output ที่ต้องการ

### Template สำหรับแต่ละ dependency:

```
- **{spec_id}** - {description} - Spec Path: "{path}/spec.md" Repo: {repo}
```

### ตัวอย่าง:

```
- **spec-core-001-authentication** - User authentication for financial operations - Spec Path: "specs/core/spec-core-001-authentication/spec.md" Repo: private
```

## ขั้นตอนการแก้ไข Workflow

### 1. เพิ่มการอ่าน SPEC_INDEX.json

Workflow ต้องสามารถ:
- อ่านไฟล์ `.smartspec/SPEC_INDEX.json`
- ค้นหา spec ที่ต้องการจาก dependencies list
- ดึงข้อมูล path และ repo

### 2. สร้าง Function สำหรับ Resolve Dependencies

```
Function: resolveSpecDependencies(specIds: string[])
Input: ["spec-core-001-authentication", "spec-core-002-authorization"]
Output: [
  {
    id: "spec-core-001-authentication",
    title: "Authentication System",
    path: "specs/core/spec-core-001-authentication/spec.md",
    repo: "private"
  },
  ...
]
```

### 3. Format Output

แปลงข้อมูลที่ได้เป็นรูปแบบ markdown:

```markdown
### 19.1. Core Dependencies
- **spec-core-001-authentication** - Authentication System - Spec Path: "specs/core/spec-core-001-authentication/spec.md" Repo: private
```

## การจัดกลุ่ม Dependencies

### แบ่งตาม Category:

1. **Core Dependencies** (category: "core")
   - spec-core-001-authentication
   - spec-core-002-authorization
   - spec-core-003-audit-logging
   - spec-core-004-rate-limiting

2. **Feature Specs** (category: "feature")
   - spec-002-user-management
   - spec-012-subscription-plans
   - spec-013-promptpay-credit-topup

3. **Infrastructure Specs** (category: "infrastructure")
   - spec-000-infrastructure

## Error Handling

### กรณีที่ spec ไม่พบใน SPEC_INDEX.json:

```markdown
- **spec-unknown-001** - [NOT FOUND IN SPEC_INDEX] - Spec Path: "N/A" Repo: unknown
```

### กรณีที่ SPEC_INDEX.json ไม่มี:

```markdown
⚠️ Warning: SPEC_INDEX.json not found. Dependencies listed without path/repo information.

### 19.1. Dependencies
- **spec-core-001-authentication** - User authentication for financial operations
```

## สรุปการแก้ไข

### ไฟล์ที่ต้องแก้ไข:

1. `.kilocode/workflows/smartspec_generate_spec.md`
   - เพิ่มขั้นตอนการอ่าน SPEC_INDEX.json
   - เพิ่ม function สำหรับ resolve dependencies
   - แก้ไข template สำหรับ Related Specs section

### จุดที่ต้องแก้ไขใน Workflow:

**Section ที่ต้องเพิ่ม:**
- การโหลด SPEC_INDEX.json (ใน section "Load SmartSpec Context")
- การ resolve dependencies (ก่อน section "Generate SPEC")
- Template สำหรับ Related Specs section (ใน section "Generate SPEC")

**Format ที่ต้องใช้:**
```
- **{id}** - {description} - Spec Path: "{path}/spec.md" Repo: {repo}
```
