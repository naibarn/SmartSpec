# วิเคราะห์ส่วนที่ขาดหายไปใน Generate Spec Workflow

**วันที่:** 2025-12-03  
**Workflow:** `smartspec_generate_spec.md`

---

## 1. Backup File Mechanism

### สถานะปัจจุบัน
- ✅ มีการ mention ใน section 13.5 Write Output
- ✅ มีการ mention ใน Report Output (line 1663)
- ❌ **ขาดรายละเอียดการ implement**

### ความจำเป็น: 🔴 CRITICAL

**เหตุผล:**
- ป้องกันการสูญหายของ SPEC เดิมเมื่อ regenerate
- รองรับการ rollback ถ้า generation ผิดพลาด
- เป็น best practice สำหรับ production tool

### แนวทางแก้ไข: ✅ ต้องเพิ่ม

**เพิ่มใน section 13.5:**
```markdown
### 13.5 Write Output

#### 13.5.1 Backup Existing SPEC (if exists)

If spec.md already exists:

1. **Check if backup needed:**
   ```typescript
   if (fs.existsSync(specPath) && !flags.noBackup) {
     // Proceed with backup
   }
   ```

2. **Generate backup filename:**
   ```
   Format: spec.backup-YYYYMMDD-HHmmss.md
   Example: spec.backup-20251203-143022.md
   ```

3. **Create backup:**
   ```typescript
   const timestamp = new Date().toISOString()
     .replace(/:/g, '')
     .replace(/\./g, '')
     .slice(0, 15); // YYYYMMDD-HHmmss
   
   const backupDir = path.join(specDir, '.smartspec/backups');
   fs.mkdirSync(backupDir, { recursive: true });
   
   const backupPath = path.join(backupDir, `spec.backup-${timestamp}.md`);
   fs.copyFileSync(specPath, backupPath);
   ```

4. **Cleanup old backups (optional):**
   - Keep last 10 backups
   - Delete backups older than 30 days
   ```typescript
   const backups = fs.readdirSync(backupDir)
     .filter(f => f.startsWith('spec.backup-'))
     .sort()
     .reverse();
   
   // Keep only last 10
   backups.slice(10).forEach(f => {
     fs.unlinkSync(path.join(backupDir, f));
   });
   ```

#### 13.5.2 Write New SPEC

Write generated content to spec.md

#### 13.5.3 Generate Report

Write generation report to .smartspec/reports/
```

---

## 2. Performance Requirements Section

### สถานะปัจจุบัน
- ✅ มี section 6 "Performance Requirements Handling"
- ✅ มี performance=basic และ performance=full
- ✅ มี Service-level Performance breakdown (ที่เพิ่มใหม่)

### ความจำเป็น: ✅ มีแล้ว - ไม่ต้องเพิ่ม

**สรุป:** ครบถ้วนแล้ว ครอบคลุม:
- System-wide targets
- Per-service targets
- Database performance
- Queue performance
- Load testing

---

## 3. Rate Limiting Section

### สถานะปัจจุบัน
- ✅ มี mention ใน Enhanced Security (Denial of Service)
- ✅ มี rate limiting ใน security section
- ❌ **ไม่มี dedicated section สำหรับ Rate Limiting**

### ความจำเป็น: 🟡 MEDIUM

**เหตุผล:**
- Rate limiting เป็นส่วนหนึ่งของ Security และ Performance
- ไม่จำเป็นต้องมี dedicated section
- ควรรวมอยู่ใน Security (DoS) และ Performance sections

### แนวทางแก้ไข: ⚠️ ปรับปรุงให้ชัดเจนขึ้น

**เพิ่มใน Security section:**
```markdown
### Rate Limiting Strategy

**Per-User Limits:**
- Standard users: 100 req/min
- Premium users: 500 req/min
- Admin users: 1000 req/min

**Per-IP Limits:**
- Public endpoints: 1000 req/min
- Auth endpoints: 20 req/min (prevent brute force)

**Per-Endpoint Limits:**
- GET /api/balance: 200 req/min
- POST /api/credit/add: 50 req/min
- POST /api/payment: 20 req/min

**Implementation:**
- Use Redis for distributed rate limiting
- Sliding window algorithm
- Return 429 Too Many Requests with Retry-After header

**Burst Handling:**
- Allow burst up to 2x limit for 10 seconds
- Then enforce strict limit
```

---

## 4. Role Terminology Section

### สถานะปัจจุบัน
- ❌ **ไม่มี dedicated section**
- มี mention ใน Security (RBAC)

### ความจำเป็น: 🟡 MEDIUM

**เหตุผล:**
- สำคัญสำหรับระบบที่มี complex authorization
- ช่วยให้ทีมเข้าใจ roles และ permissions
- ควรมีสำหรับ financial systems

### แนวทางแก้ไข: ✅ ต้องเพิ่ม (สำหรับ financial profile)

**เพิ่มใน financial profile:**
```markdown
## Role Terminology & Permissions

### User Roles

#### 1. End User (ROLE_USER)
**Description:** Standard customer using the system

**Permissions:**
- View own balance
- Add credit (via payment)
- View own transaction history
- View own invoices
- Update own profile

**Restrictions:**
- Cannot view other users' data
- Cannot perform admin operations
- Cannot access system reports

---

#### 2. Premium User (ROLE_PREMIUM)
**Description:** Paid subscription customer

**Inherits:** ROLE_USER

**Additional Permissions:**
- Higher rate limits (500 req/min vs 100 req/min)
- Access to advanced features
- Priority support
- Export transaction history (CSV, PDF)

---

#### 3. Support Agent (ROLE_SUPPORT)
**Description:** Customer support team member

**Permissions:**
- View user profiles (read-only)
- View user transaction history (read-only)
- View user balance (read-only)
- Create support tickets
- Add notes to user accounts

**Restrictions:**
- Cannot modify user balance
- Cannot process refunds
- Cannot delete data
- All actions logged for audit

---

#### 4. Finance Manager (ROLE_FINANCE)
**Description:** Finance team member

**Permissions:**
- View all financial reports
- Process refunds (with approval)
- Generate invoices
- View all transactions
- Export financial data
- Reconcile accounts

**Restrictions:**
- Cannot modify system configuration
- Cannot manage users
- Cannot access technical logs

---

#### 5. Admin (ROLE_ADMIN)
**Description:** System administrator

**Permissions:**
- All ROLE_FINANCE permissions
- Manage users (create, update, disable)
- Modify user balances (with audit)
- Configure system settings
- View system logs
- Manage roles and permissions

**Restrictions:**
- Cannot delete audit logs
- Cannot bypass security controls
- All actions logged and alerted

---

#### 6. Super Admin (ROLE_SUPER_ADMIN)
**Description:** Technical team lead

**Permissions:**
- All ROLE_ADMIN permissions
- Access database directly (emergency only)
- Modify audit logs (emergency recovery only)
- Deploy system updates
- Access production servers

**Restrictions:**
- All actions require MFA
- All actions alerted to security team
- Emergency access logged and reviewed

---

### Permission Matrix

| Action | User | Premium | Support | Finance | Admin | Super Admin |
|--------|------|---------|---------|---------|-------|-------------|
| View own balance | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Add credit | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| View other user balance | ❌ | ❌ | ✅ (read) | ✅ | ✅ | ✅ |
| Modify user balance | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Process refund | ❌ | ❌ | ❌ | ✅ (approval) | ✅ | ✅ |
| View financial reports | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Manage users | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| System configuration | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Database access | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

### Role Assignment Rules

1. **Default Role:** New users get ROLE_USER
2. **Role Elevation:** Requires approval from ROLE_ADMIN or higher
3. **Role Downgrade:** Can be done by ROLE_ADMIN or higher
4. **Multiple Roles:** Users can have multiple roles (additive permissions)
5. **Temporary Roles:** Support temporary role elevation (e.g., 24 hours)

---

### Implementation

**Database Schema:**
```sql
CREATE TABLE roles (
  id UUID PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  description TEXT,
  permissions JSONB NOT NULL
);

CREATE TABLE user_roles (
  user_id UUID NOT NULL,
  role_id UUID NOT NULL,
  granted_by UUID NOT NULL,
  granted_at TIMESTAMP NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMP,
  PRIMARY KEY (user_id, role_id)
);
```

**Permission Check:**
```typescript
function hasPermission(user: User, permission: string): boolean {
  return user.roles.some(role => 
    role.permissions.includes(permission)
  );
}

// Usage
if (!hasPermission(user, 'credit:modify')) {
  throw new ForbiddenError('Insufficient permissions');
}
```
```

---

## 5. Deployment Architecture Section

### สถานะปัจจุบัน
- ❌ **ไม่มี dedicated section**
- มี mention ใน Architecture section (general)

### ความจำเป็น: 🟢 OPTIONAL

**เหตุผล:**
- Deployment architecture เป็นส่วนของ implementation detail
- SPEC ควรเน้น business logic และ technical specification
- Deployment details ควรอยู่ใน Plan หรือ Infrastructure docs

### แนวทางแก้ไข: ⚠️ เพิ่มเป็น optional section

**เพิ่มเป็น optional section (ไม่ auto-generate):**
```markdown
## Deployment Architecture (Optional)

> **Note:** This section is optional and typically added manually for complex systems.

### Production Environment

**Infrastructure:**
- Cloud Provider: AWS / GCP / Azure
- Region: [Primary region]
- Availability Zones: 3 AZs for high availability

**Components:**
```
┌─────────────────────────────────────────────────┐
│                  Load Balancer                  │
│              (AWS ALB / GCP LB)                 │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
   ┌────▼────┐         ┌────▼────┐
   │  App 1  │   ...   │  App N  │
   │ (ECS)   │         │ (ECS)   │
   └────┬────┘         └────┬────┘
        │                   │
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │                   │
   ┌────▼────┐         ┌────▼────┐
   │   DB    │◄────────┤  Cache  │
   │ (RDS)   │         │ (Redis) │
   └─────────┘         └─────────┘
```

**Scaling:**
- Auto-scaling: 2-20 instances
- Scale up: CPU > 70% for 5 minutes
- Scale down: CPU < 30% for 10 minutes

**Deployment Strategy:**
- Blue-Green deployment
- Zero-downtime deployment
- Automated rollback on failure
```

---

## 6. API Section

### สถานะปัจจุบัน
- ✅ มี mention ใน Architecture section
- ✅ มี API endpoints ใน Examples section
- ❌ **ไม่มี comprehensive API specification**

### ความจำเป็น: 🟡 MEDIUM

**เหตุผล:**
- API specification สำคัญสำหรับ backend services
- ช่วยให้ frontend/client developers เข้าใจ API
- ควรมีสำหรับ backend-service และ financial profiles

### แนวทางแก้ไข: ✅ ต้องเพิ่ม (สำหรับ backend profiles)

**เพิ่มใน backend-service และ financial profiles:**
```markdown
## API Specification

### Base URL
```
Production: https://api.example.com/v1
Staging: https://api-staging.example.com/v1
Development: http://localhost:3000/v1
```

### Authentication
All endpoints require JWT authentication unless marked as public.

**Header:**
```
Authorization: Bearer <jwt_token>
```

### Common Response Format

**Success Response:**
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "timestamp": "2025-12-03T14:30:00Z",
    "requestId": "req_abc123"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_CREDIT",
    "message": "Insufficient credit balance",
    "details": {
      "required": 100.00,
      "available": 50.00
    }
  },
  "meta": {
    "timestamp": "2025-12-03T14:30:00Z",
    "requestId": "req_abc123"
  }
}
```

---

### Credit Management Endpoints

#### Get Balance
```http
GET /credit/balance
```

**Response:**
```json
{
  "success": true,
  "data": {
    "userId": "user_123",
    "balance": 1000.00,
    "reservedBalance": 50.00,
    "availableBalance": 950.00,
    "currency": "THB",
    "lastUpdated": "2025-12-03T14:30:00Z"
  }
}
```

---

#### Add Credit
```http
POST /credit/add
```

**Request:**
```json
{
  "amount": 100.00,
  "paymentMethod": "promptpay",
  "idempotencyKey": "idem_abc123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "transactionId": "txn_abc123",
    "userId": "user_123",
    "amount": 100.00,
    "newBalance": 1100.00,
    "status": "completed",
    "createdAt": "2025-12-03T14:30:00Z"
  }
}
```

---

#### Deduct Credit
```http
POST /credit/deduct
```

**Request:**
```json
{
  "amount": 50.00,
  "reason": "Service usage",
  "metadata": {
    "serviceId": "svc_123",
    "usageType": "api_call"
  },
  "idempotencyKey": "idem_xyz789"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "transactionId": "txn_xyz789",
    "userId": "user_123",
    "amount": 50.00,
    "newBalance": 1050.00,
    "status": "completed",
    "createdAt": "2025-12-03T14:30:00Z"
  }
}
```

---

### Transaction History Endpoints

#### Get Transaction History
```http
GET /transactions?page=1&limit=20&type=credit
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20, max: 100)
- `type` (optional): Filter by type (credit, debit, refund)
- `startDate` (optional): Start date (ISO 8601)
- `endDate` (optional): End date (ISO 8601)

**Response:**
```json
{
  "success": true,
  "data": {
    "transactions": [
      {
        "id": "txn_abc123",
        "type": "credit",
        "amount": 100.00,
        "balance": 1100.00,
        "description": "Credit added via PromptPay",
        "createdAt": "2025-12-03T14:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "totalPages": 8
    }
  }
}
```

---

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Invalid request parameters |
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `INSUFFICIENT_CREDIT` | 400 | Not enough credit balance |
| `DUPLICATE_TRANSACTION` | 409 | Duplicate idempotency key |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Internal server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

---

### Rate Limits

See [Rate Limiting Strategy](#rate-limiting-strategy) section.

---

### Idempotency

All mutation endpoints (POST, PUT, DELETE) support idempotency via `idempotencyKey`.

**Rules:**
- Key format: Any string up to 255 characters
- Key expiration: 24 hours
- Duplicate requests return cached response
- Different payload with same key returns 409 Conflict
```

---

## สรุปความจำเป็น

| Section | ความจำเป็น | สถานะ | แนวทางแก้ไข |
|---------|-----------|-------|-------------|
| 1. Backup File Mechanism | 🔴 CRITICAL | ❌ ขาด | ✅ ต้องเพิ่ม implementation |
| 2. Performance Requirements | ✅ มีแล้ว | ✅ ครบ | ไม่ต้องแก้ไข |
| 3. Rate Limiting | 🟡 MEDIUM | ⚠️ มีบางส่วน | ✅ ปรับปรุงให้ชัดเจน |
| 4. Role Terminology | 🟡 MEDIUM | ❌ ขาด | ✅ เพิ่มสำหรับ financial |
| 5. Deployment Architecture | 🟢 OPTIONAL | ❌ ขาด | ⚠️ เพิ่มเป็น optional |
| 6. API Specification | 🟡 MEDIUM | ⚠️ มีบางส่วน | ✅ เพิ่มสำหรับ backend |

---

## ลำดับความสำคัญในการแก้ไข

### Priority 1: CRITICAL (ต้องแก้ไขทันที)
1. ✅ Backup File Mechanism

### Priority 2: MEDIUM (ควรแก้ไข)
2. ✅ Rate Limiting (ปรับปรุง)
3. ✅ Role Terminology (เพิ่มสำหรับ financial)
4. ✅ API Specification (เพิ่มสำหรับ backend)

### Priority 3: OPTIONAL (แก้ไขถ้ามีเวลา)
5. ⚠️ Deployment Architecture (optional section)

---

## แนวทางการ implement

1. **เพิ่ม Backup mechanism** ใน section 13.5
2. **เพิ่ม Rate Limiting details** ใน Security section
3. **เพิ่ม Role Terminology section** สำหรับ financial profile
4. **เพิ่ม API Specification section** สำหรับ backend-service และ financial profiles
5. **เพิ่ม Deployment Architecture** เป็น optional section

---

**Next Step:** ดำเนินการแก้ไขตามลำดับความสำคัญ
