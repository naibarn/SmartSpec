---
description: Generate a SmartSpec v4.0 compliant tasks.md from a SPEC file with auto-detection of supporting files, auto-generation of supplementary documents, and full integration with the SmartSpec ecosystem. Supports custom SPEC_INDEX and dry-run mode.
handoffs:
  - label: Validate Tasks
    agent: smartspec.analyze
    prompt: Validate the generated tasks.md for correctness, dependencies, and safety compliance.
    send: true
  - label: Prepare Kilo Prompt
    agent: smartspec.kilo
    prompt: Generate the Kilo Code implementation prompt for this tasks.md
    send: true
---

## User Input

```text
$ARGUMENTS
```

You MUST consider the user input before proceeding.

**Expected patterns:**
- SPEC path: `specs/feature/spec-004-financial-system/spec.md`
- With custom index: `specs/feature/spec-004/spec.md --specindex="path/to/index.json"`
- Dry run: `specs/feature/spec-004/spec.md --nogenerate`
- Combined: `specs/feature/spec-004/spec.md --specindex="path" --nogenerate`

If no explicit SPEC path is given, assume the currently open file is the SPEC.

---

## 0. Load SmartSpec Context (MANDATORY)

Before deriving any tasks, you MUST read and follow all of these files from the repository root:

1. `.smartspec/system_prompt.md`  
   - Defines core SmartSpec Architect behaviour, safety rules, and execution strategy.
2. `.smartspec/Knowledge-Base.md`  
   - Defines required SPEC sections, task generation patterns, Kilo Code safety rules, phase/checkpoint standards, and file-size strategies.
3. `.smartspec/constitution.md`  
   - Defines additional constraints, quality requirements, and non-negotiable guardrails.
4. `.smartspec/kilocode-context.md`  
   - Defines how tasks.md will be used inside Kilo Code and what constraints apply at execution time.
5. SPEC_INDEX file (path determined in step 0.2)
   - Provides the **global list of SPEC IDs and metadata** and MUST be used when resolving dependencies and spec references.

### 0.1 Safety: do NOT unzip or modify .smartspec.zip

- Do **NOT** run any shell commands such as:
  - `unzip .smartspec.zip`
  - `tar`, `7z`, or any other archive extraction.
- Assume that `.smartspec/` and all knowledge base files already exist on disk.
- If any required `.smartspec/*.md` files are missing:
  - STOP immediately.
  - Ask the user to install or unzip `.smartspec/` manually.
  - Do **NOT** attempt to create, download, or unzip these files yourself.

### 0.2 Determine SPEC_INDEX Path

Parse `$ARGUMENTS` to find `--specindex` parameter:

**Step 1: Extract --specindex value**
- Pattern: `--specindex="path/to/file"` or `--specindex=path/to/file`
- If found:
  - `SPEC_INDEX_PATH` = extracted path
  - Remove `--specindex="..."` from `$ARGUMENTS` for further processing
- If not found:
  - Check `.smartspec/Knowledge-Base.md` or `.smartspec/system_prompt.md` for default SPEC_INDEX path
  - If specified in knowledge base, use that path
  - Otherwise, use default: `SPEC_INDEX_PATH = ".smartspec/SPEC_INDEX.json"`

**Step 2: Check and optionally create SPEC_INDEX (Enhanced with Auto-Creation)**

Check if `SPEC_INDEX_PATH` exists:
```bash
test -f ${SPEC_INDEX_PATH} && echo "EXISTS" || echo "NOT_EXISTS"
```

If NOT_EXISTS:
```
1. ⚠️ WARNING: "SPEC_INDEX.json not found at: {SPEC_INDEX_PATH}"
2. ❓ Ask user: "Create new SPEC_INDEX.json? [Y/n]"

3. If user confirms (Y):
   a. Create .smartspec/ directory (if not exists):
      mkdir -p .smartspec
   
   b. Create SPEC_INDEX.json with initial structure:
      {
        "version": "5.0",
        "created": "<current_timestamp>",
        "last_updated": "<current_timestamp>",
        "specs": [],
        "metadata": {
          "total_specs": 0,
          "by_status": {
            "draft": 0,
            "active": 0,
            "deprecated": 0,
            "placeholder": 0
          },
          "by_repo": {},
          "validation": {
            "last_validated": "<current_timestamp>",
            "status": "valid",
            "errors": [],
            "warnings": [],
            "health_score": 100
          }
        }
      }
   
   c. Add current spec to INDEX:
      - Extract spec ID, title, path from SPEC file
      - Add as first entry
      - Update metadata
   
   d. Save SPEC_INDEX.json
   
   e. Log: "✅ Created SPEC_INDEX.json with current spec"
   
   f. Continue with tasks generation

4. If user declines (n):
   a. ⚠️ WARNING: "Continuing without SPEC_INDEX"
   b. ⚠️ "Dependency resolution will be skipped"
   c. Set SPEC_INDEX_AVAILABLE = false
   d. Continue with tasks generation (without dependency info)
```

**Step 3: Parse SPEC_INDEX and extract metadata**
- Based on file extension:
  - `.json` → JSON format
  - `.sql` → SQL format (may need different parsing)
  - Other → Assume JSON format as default
- Parse the file to extract for ALL specs:
  - SPEC ID
  - Title
  - Path (relative to repo root)
  - Repository (if specified: "private", "public", etc.)
  - Status
  - Dependencies (if specified)
- Store this data in memory as `SPEC_REGISTRY` for later use

These files together are the **single source of truth** for:
- Maximum 10 tasks per phase.
- Phase planning strategy.
- File-size-aware editing rules.
- Checkpoint and validation expectations.
- Error handling and recovery.

If instructions in this workflow conflict with system prompt + knowledge base, the **system prompt + knowledge base take precedence**.

---

## 0.3 Parse --nogenerate Flag (NEW)

Check if `--nogenerate` flag is present in `$ARGUMENTS`:

**Step 1: Check for flag**
- Pattern: `--nogenerate` (exact match)
- If found:
  - Set `DRY_RUN_MODE = true`
  - Remove `--nogenerate` from `$ARGUMENTS`
- If not found:
  - Set `DRY_RUN_MODE = false` (default - will generate files)

**Step 2: Dry run behavior**
If `DRY_RUN_MODE = true`:
- Do NOT create any files
- Do NOT modify any existing files
- DO show complete plan of what would be created:
  - tasks.md structure
  - Supporting files that would be generated
  - Phase breakdown
  - Task count and estimates
- DO provide detailed report for review
- DO ask user for confirmation before actual generation

---

## 1. Resolve SPEC Path

After removing `--specindex` and `--nogenerate` from arguments:

1.1 If remaining `$ARGUMENTS` contains a path ending with `spec.md`:
- `SPEC_PATH` = that path (absolute or resolvable from repo root).

1.2 Else:
- Assume the active editor file is the SPEC to use.
- `SPEC_PATH` = path of active file.

---

## 2. Setup from SPEC

### 2.1 Read and Parse SPEC

- Read `SPEC_PATH` and parse according to `.smartspec/Knowledge-Base.md` structure:
  - **Metadata:** Author, Version, Status, SPEC ID, Created/Updated dates
  - **Overview:** Purpose, Scope, Non-Goals, Key Features
  - **When to Use / When NOT to Use**
  - **Technology Stack**
  - **Architecture**
  - **Implementation Guide**
  - **Testing / Monitoring / Security sections**
  - **Examples**
  - **Related Specs** (will be enhanced with paths + repos)

### 2.2 Identify Key Information

- Identify from the SPEC:
  - Major components / services / modules
  - External integrations and dependencies
  - Critical paths and high-risk areas
  - Data models and schemas
  - API contracts and interfaces
  - Any explicit constraints or sequencing requirements
  - Any **Non-Goals** or out-of-scope areas so you do NOT generate tasks for them

### 2.3 Extract Spec References

- Parse Related Specs section
- Extract all referenced spec IDs
- For each referenced spec:
  - Look up in `SPEC_REGISTRY` (from SPEC_INDEX)
  - Extract: path, repository, title
  - Will be used later for task dependencies

---

## 3. Scan for Supporting Files (NEW - CRITICAL)

### 3.1 Detect Existing Supporting Files

Let `SPEC_DIR` = directory of `SPEC_PATH`.

**Scan for these file patterns in `SPEC_DIR`:**

1. **API Specifications:**
   - `api-spec.yaml` / `api-spec.json`
   - `openapi.yaml` / `openapi.json`
   - `swagger.yaml` / `swagger.json`
   - `contracts/*.yaml` / `contracts/*.json`

2. **Data Models:**
   - `data-model.md` / `data-models.md`
   - `schema.md` / `schemas.md`
   - `models/*.ts` / `models/*.json`
   - `types/*.ts`

3. **Research & Documentation:**
   - `research.md` / `research/*.md`
   - `analysis.md`
   - `requirements.md`
   - `design.md`

4. **Implementation Guides:**
   - `README.md` (implementation-specific)
   - `IMPLEMENTATION.md`
   - `SETUP.md`

5. **Test Specifications:**
   - `test-plan.md`
   - `test-cases.md`
   - `acceptance-criteria.md`

**Exclusions:**
- Ignore files with "backup" in name
- Ignore `.backup-*` files
- Ignore `.old` / `.tmp` files
- Ignore `spec.new.md` / `spec.backup-*.md`

**Step 1: List all detected files**
```
SUPPORTING_FILES = {
  api_specs: [],
  data_models: [],
  research: [],
  guides: [],
  tests: []
}
```

**Step 2: Read and parse relevant files**
- Read content of each detected file
- Extract key information for task generation
- Store in memory for reference

---

## 3.2 Determine Missing Supporting Files (NEW - CRITICAL)

Based on SPEC content, determine which supporting files SHOULD exist but don't:

**Rule-based Detection:**

1. **If SPEC mentions API endpoints** → Need `openapi.yaml`
2. **If SPEC mentions database schema** → Need `data-model.md`
3. **If SPEC is complex (>50 tasks estimated)** → Need `README.md`
4. **If SPEC mentions testing requirements** → Need `test-plan.md`
5. **If SPEC references research/analysis** → Need `research.md`

**Store missing files:**
```
MISSING_SUPPORT_FILES = [
  {
    filename: "openapi.yaml",
    reason: "SPEC defines REST API endpoints",
    priority: "HIGH",
    auto_generate: true
  },
  {
    filename: "data-model.md",
    reason: "SPEC mentions database tables",
    priority: "HIGH",
    auto_generate: true
  }
]
```

---

## 3.3 Auto-Generate Missing Supporting Files (NEW - CRITICAL)

For each file in `MISSING_SUPPORT_FILES` with `auto_generate: true`:

### 3.3.1 Generate README.md

**If missing and SPEC is complex:**

```markdown
# [Project Name] - Implementation Guide

**Generated:** YYYY-MM-DD
**Source:** [SPEC-ID]
**Author:** SmartSpec Architect v4.0

## Overview

[Extract from SPEC Overview]

## Project Structure

```
[Expected directory structure based on SPEC]
```

## Prerequisites

[Extract from SPEC Prerequisites/Technology Stack]

## Setup Instructions

1. [Step-by-step setup based on SPEC]

## Implementation Checklist

- [ ] Phase 1: [Phase name]
- [ ] Phase 2: [Phase name]
...

## Testing

[Extract from SPEC Testing section]

## Deployment

[Extract from SPEC if available]

## Related Documentation

- SPEC: [Link to spec.md]
- Tasks: [Link to tasks.md]
- API Spec: [Link if exists]

---

**Note:** This is an auto-generated guide. Update as implementation progresses.
```

### 3.3.2 Generate data-model.md

**If SPEC mentions database/schema:**

```markdown
# Data Model - [Project Name]

**Generated:** YYYY-MM-DD
**Source:** [SPEC-ID]
**Author:** SmartSpec Architect v4.0

## Overview

Data model for [project description from SPEC].

## Entities

### [Entity 1]

**Description:** [From SPEC]

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| [field] | [type] | [yes/no] | [description] |

**Relationships:**
- [Relationship description]

**Indexes:**
- [Index specifications]

### [Entity 2]
[Repeat pattern]

## Database Schema (SQL)

```sql
-- Auto-generated schema based on SPEC
-- Review and adjust as needed

CREATE TABLE [entity] (
  [fields based on analysis]
);
```

## Migrations

[Migration strategy from SPEC]

## Data Integrity Rules

[From SPEC validation/business rules]

---

**Note:** This is an auto-generated model. Validate and refine during implementation.
```

### 3.3.3 Generate openapi.yaml

**If SPEC defines REST API:**

```yaml
# Auto-generated OpenAPI Specification
# Source: [SPEC-ID]
# Generated: YYYY-MM-DD
# Author: SmartSpec Architect v4.0

openapi: 3.0.0
info:
  title: [API Title from SPEC]
  version: [Version from SPEC]
  description: [Description from SPEC]

servers:
  - url: http://localhost:3000
    description: Development server

paths:
  [Generate paths based on SPEC API descriptions]:
    [method]:
      summary: [From SPEC]
      description: [From SPEC]
      parameters:
        - [Extract from SPEC]
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                [From SPEC or data-model]

components:
  schemas:
    [Generate from SPEC and data-model]
  
  securitySchemes:
    [From SPEC Security section]

# Note: Auto-generated. Review and complete during implementation.
```

### 3.3.4 Generate test-plan.md

**If SPEC has comprehensive testing requirements:**

```markdown
# Test Plan - [Project Name]

**Generated:** YYYY-MM-DD
**Source:** [SPEC-ID]
**Author:** SmartSpec Architect v4.0

## Test Strategy

[Extract from SPEC Testing Strategy section]

## Test Levels

### Unit Tests
- Coverage target: [From SPEC or default 80%]
- Key areas: [From SPEC Implementation Guide]

### Integration Tests
- [From SPEC Integration Testing section]

### E2E Tests
- [From SPEC if specified]

## Test Cases

### [Feature 1]

**Test Case ID:** TC001
**Description:** [From SPEC Acceptance Criteria]
**Prerequisites:** [From SPEC]
**Steps:** [From SPEC examples]
**Expected:** [From SPEC]

[Generate for major features from SPEC]

## Performance Testing

[From SPEC Performance Requirements if exists]

## Security Testing

[From SPEC Security section]

---

**Note:** Auto-generated from SPEC. Expand during implementation.
```

---

## 4. Plan Task & Phase Structure

Using the guidelines in `.smartspec/Knowledge-Base.md`:

### 4.1 Estimate Total Tasks

- Analyze SPEC complexity:
  - Small project: 20-40 tasks
  - Medium project: 60-80 tasks
  - Large project: 100-150 tasks
- Consider:
  - Number of components/services
  - External integrations
  - API endpoints
  - Database tables
  - Security requirements
  - Testing requirements

### 4.2 Enforce Phase Rules

- **10-task maximum per phase** rule (MANDATORY)
- **Minimum 5 tasks per phase** (avoid too-small phases)
- Define clear phases with logical grouping

**Standard 10-Phase Structure for Financial/Complex Systems:**

1. **Phase 1: Foundation & Setup** (T001-T010)
   - Project initialization, build config
   - Database setup (PostgreSQL, Redis)
   - Core infrastructure (logging, monitoring)
   - Basic authentication

2. **Phase 2: Database Schema & Core Models** (T011-T020)
   - All database tables (15+ tables)
   - Prisma schema
   - Migrations
   - Seed data

3. **Phase 3: Authentication & Authorization** (T021-T030)
   - JWT implementation
   - RBAC middleware
   - Permission matrix
   - MFA enforcement

4. **Phase 4: Credit Management Core** (T031-T040)
   - Credit balance service
   - Reserve/Commit/Release flows
   - Transaction ledger
   - Idempotency

5. **Phase 5: Payment Integration** (T041-T050)
   - Payment gateway integration
   - Payment intent flow
   - Webhook handlers
   - Refund system

6. **Phase 6: Billing System** (T051-T060)
   - Billing cycle engine
   - Invoice generation
   - Subscription management
   - Payment method management

7. **Phase 7: Cost Management & Analytics** (T061-T070)
   - Cost tracking
   - Analytics pipeline
   - Reporting APIs
   - Forecasting

8. **Phase 8: Security & Compliance** (T071-T080)
   - Audit logging
   - Security monitoring
   - Fraud detection
   - Compliance checks (PCI DSS)

9. **Phase 9: API Layer & Integration** (T081-T090)
   - Public APIs
   - Admin APIs
   - Internal APIs
   - API documentation

10. **Phase 10: Testing & Deployment** (T091-T100)
    - Integration tests
    - E2E tests
    - Performance tests
    - Deployment automation

**For smaller projects (<50 tasks):**
- Combine related phases
- Maintain 5-10 tasks per phase
- Still use clear phase boundaries

**For larger projects (>100 tasks):**
- Split large phases into sub-phases
- Example: Phase 4A, Phase 4B
- Maintain 10-task maximum per sub-phase

### 4.2.1 Complete Coverage Requirements (CRITICAL)

**🚨 MANDATORY: 100% SPEC Coverage**

All tasks.md MUST cover 100% of SPEC requirements. Check coverage for:

**Business Logic (MUST be 100%):**
- [ ] All core flows (e.g., credit reserve/commit/release)
- [ ] All payment flows (purchase, refund, failed payment)
- [ ] All billing operations (invoice, subscription, payment method)
- [ ] All cost management features (tracking, analytics, forecasting)
- [ ] All fraud prevention mechanisms

**API Endpoints (MUST be 100%):**
- [ ] All public user APIs (balance, history, transactions)
- [ ] All admin APIs (adjustments, refunds, overrides)
- [ ] All billing APIs (invoices, subscriptions, payment methods)
- [ ] All payment webhook handlers
- [ ] All internal service APIs

**Security (MUST be 100%):**
- [ ] MFA enforcement
- [ ] RBAC middleware for all endpoints
- [ ] Permission checks
- [ ] Audit trail for financial events
- [ ] Security monitoring automation
- [ ] Compliance checks (PCI DSS, SOC 2, GDPR)

**Database (MUST be 100%):**
- [ ] All tables from data model (15+ tables)
- [ ] All migrations
- [ ] All indexes
- [ ] All partitioning strategies
- [ ] Seed data

**Testing (MUST be 100%):**
- [ ] Unit tests for all services
- [ ] Integration tests for all flows
- [ ] E2E tests for critical paths
- [ ] Permission tests for all endpoints
- [ ] Fraud scenario tests
- [ ] Performance tests

**Coverage Validation:**

Before finalizing tasks.md:
1. Read SPEC completely
2. List ALL requirements
3. Map each requirement to task(s)
4. Verify no gaps
5. Add missing tasks if needed

**If coverage < 90%:** STOP and add missing tasks

### 4.3 Assign Risk Levels

For each phase:
- **LOW:** Standard implementation, no external dependencies
- **MEDIUM:** Some complexity, external APIs involved
- **HIGH:** Complex integration, security-critical, performance-sensitive
- **CRITICAL:** Core infrastructure, high impact of failure

### 4.4 Ensure Alignment with SPEC

- Tasks must cover SPEC Scope
- Tasks must NOT cover SPEC Non-Goals
- Tasks must respect SPEC constraints
- Tasks must follow SPEC architecture

---

## 5. Determine Output Paths

Let `SPEC_DIR` = directory of `SPEC_PATH`.

### 5.1 Primary Output

- `TASKS_PATH = SPEC_DIR/tasks.md`
- Example:
  - SPEC:  `specs/feature/spec-004-financial-system/spec.md`
  - TASKS: `specs/feature/spec-004-financial-system/tasks.md`

### 5.2 Supporting Files Output

For auto-generated supporting files:
- `README.md` → `SPEC_DIR/README.md`
- `data-model.md` → `SPEC_DIR/data-model.md`
- `openapi.yaml` → `SPEC_DIR/openapi.yaml`
- `test-plan.md` → `SPEC_DIR/test-plan.md`

**Overwrite Policy:**
- If file exists: Create `[filename].new.md` instead
- Report to user that existing file was preserved
- User can manually merge if needed

---

## 6. Generate tasks.md Header

### 6.1 Project Metadata

```markdown
# Implementation Tasks - [Project Name]

**Generated:** YYYY-MM-DD HH:mm
**Author:** SmartSpec Architect v4.0
**Source SPEC:** [SPEC-ID] v[Version]
**SPEC Path:** [Relative path to spec.md]
**SPEC_INDEX:** [Path used]

---

## Project Information

**Status:** [From SPEC Status]
**Technology Stack:** [From SPEC]
**Estimated Total Effort:** [XX hours]
**Total Phases:** [X]
**Total Tasks:** [XX]

---

## Supporting Documentation

**Available Files:**
[List detected supporting files with paths]

**Auto-Generated Files:**
[List files generated by this workflow with paths]

**Related Specs:** (Resolved from SPEC_INDEX)
[For each referenced spec:]
- **[spec-id]** (`[path]`, repo: [repo]) - [Title/Description]

---
```

### 6.2 Phase Overview Table

```markdown
## Phase Overview

| Phase | Tasks | Focus | Hours | Risk | Status |
|-------|-------|-------|-------|------|--------|
| Phase 1 | T001-T010 | [Focus area] | XX | [LOW/MED/HIGH] | ⬜ Pending |
| Phase 2 | T011-T020 | [Focus area] | XX | [MED/HIGH] | ⬜ Pending |
...

**Legend:**
- ⬜ Pending
- 🟦 In Progress
- ✅ Complete
- ❌ Blocked

---
```

---

## 7. Generate Tasks for Each Phase

For each phase X:

### 7.1 Phase Heading

```markdown
## 📋 Phase X: [Phase Name] (T00A–T00B)

**Objective:** [Clear phase goal]

**Focus Areas:**
- [Area 1]
- [Area 2]

**Dependencies:**
- [External dependencies or previous phases]

**Risk Level:** [LOW/MEDIUM/HIGH/CRITICAL]
**Estimated Effort:** [XX hours]

---
```

### 7.2 Task Generation

For every task T in this phase:

```markdown
- [ ] **T00X: [Task Title]** (Xh)

  **Description:**
  [Concrete, actionable implementation details - what, why, how]
  
  **Subtasks:**
  - [ ] T00X.1: [Subtask 1 name] (2h)
    - Description: [Specific action]
    - Files: `path/to/file1.ts`
  - [ ] T00X.2: [Subtask 2 name] (3h)
    - Description: [Specific action]
    - Files: `path/to/file2.ts`
  - [ ] T00X.3: [Subtask 3 name] (2h)
    - Description: [Specific action]
    - Files: `path/to/file3.ts`
  
  **Files:**
  
  **CREATE: `[path/to/file.ts]`** (~XXX lines - [SMALL/MEDIUM/LARGE])
  - [What this file contains]
  - [Key responsibilities]
  - Strategy: [Full creation / Iterative build]
  
  **EDIT: `[path/to/existing.ts]`** (add XX lines - [SMALL/MEDIUM/LARGE])
  - Location: [Where to edit]
  - Changes: [What to change]
  - Strategy: [str_replace / surgical edit]
  - Max lines per change: [Based on file size category]
  
  **Supporting Files Referenced:**
  - `[supporting-file.yaml]` - [How it's used in this task]
  
  **Dependencies:**
  - T00Y: [Reason for dependency]
  - Related Spec: **[spec-id]** (`[path]`, repo: [repo])
  
  **Acceptance Criteria:**
  - [ ] [Testable criterion 1]
  - [ ] [Testable criterion 2]
  - [ ] [Testable criterion 3]
  - [ ] Tests pass with >80% coverage
  - [ ] No TypeScript errors
  - [ ] Documentation updated
  
  **Validation:**
  ```bash
  # Commands to verify task completion
  tsc --noEmit
  npm test -- [relevant-test-file]
  npm run lint
  ```
  
  **Expected Outcome:**
  [What should work after this task]

---
```

### 7.2.1 Task Sizing Rules (CRITICAL)

**🚨 MANDATORY: Prevent Context Overflow**

Every task MUST be sized appropriately to prevent LLM context overflow and infinite loops:

**Small Task (2-4h):**
- Single file or function
- Clear, focused objective
- No complex dependencies
- Output: <200 lines of code
- Context: <5K tokens
- Subtasks: 0-2

**Medium Task (4-8h):**
- 2-3 related files
- Some integration work
- Few dependencies
- Output: 200-500 lines
- Context: 5-10K tokens
- Subtasks: 2-4 (REQUIRED)

**Large Task (8-16h):**
- Multiple components
- Complex integration
- Multiple dependencies
- Output: 500-1000 lines
- Context: 10-20K tokens
- Subtasks: 4-6 (MANDATORY)

**❌ TOO LARGE (>16h):**
- **NOT ALLOWED**
- MUST split into 2+ separate tasks
- Each new task follows rules above

**Context Overflow Prevention Checklist:**

Before creating a task, verify:
- [ ] Task requires reading <5 files
- [ ] Task description <500 words
- [ ] Task has <6 subtasks
- [ ] Task output <1000 lines
- [ ] Task can be completed without reading entire codebase

If ANY checkbox fails: **SPLIT THE TASK**

### 7.2.2 Subtask Breakdown Rules

**When to create subtasks:**
1. Task > 8h (MANDATORY)
2. Task involves >3 files (MANDATORY)
3. Task has multiple logical steps (RECOMMENDED)
4. Task requires multiple skills (DB + API + Tests) (RECOMMENDED)

**Subtask format:**
```markdown
- [ ] T00X.1: [Specific, actionable subtask name] (2h)
  - Description: [Clear, focused description]
  - Files: `path/to/specific/file.ts`
  - Output: [What this subtask produces]
```

**Subtask naming:**
- ✅ GOOD: "T401.1: Create reserve() method in CreditService"
- ✅ GOOD: "T401.2: Implement reservation timeout worker"
- ❌ BAD: "T401.1: Implement credit logic"
- ❌ BAD: "T401.2: Add tests"

**Subtask sizing:**
- Each subtask: 1-4h
- If subtask >4h: Split further
- Total subtasks per task: 2-6
- If >6 subtasks needed: Split parent task

### 7.3 Task Details Best Practices

**File Size Awareness:**
- SMALL (< 200 lines): Any method OK, can regenerate
- MEDIUM (200-500 lines): Use `str_replace` only, no full rewrites
- LARGE (> 500 lines): Surgical edits only, ≤ 50 lines per change

**Clear Edit Strategy:**
```markdown
**EDIT: `src/services/large-file.ts`** (1200 lines - LARGE)
- Operation: Add new method `calculateDiscount()`
- Location: After line 450 (in PricingService class)
- Method: str_replace
- Max change: 35 lines
- Strategy: Surgical insertion, preserve existing code
```

**Supporting File Integration:**
```markdown
**Supporting Files Referenced:**
- `openapi.yaml` - Use endpoint `/api/v1/credits/balance` spec for validation schema
- `data-model.md` - Reference Credit entity schema for database queries
```

---

## 7.4 Checkpoints

### 7.4.1 Mini-Checkpoint (Every 5 tasks)

```markdown
### 🔍 Mini-Checkpoint: T00X-T00Y

**Quick Validation:**
- [ ] All 5 tasks completed
- [ ] Files created/edited as expected
- [ ] TypeScript compilation passes
- [ ] No critical lint errors
- [ ] Basic functionality verified

**If any fails:** Fix before proceeding to next 5 tasks.

---
```

### 7.4.2 Major Checkpoint (End of phase)

```markdown
## ⚡ CHECKPOINT: Phase X Complete

**Comprehensive Validation:**

**Code Quality:**
- [ ] TypeScript compilation passes (`tsc --noEmit`)
- [ ] All tests passing (`npm test`)
- [ ] No critical lint errors (`npm run lint`)
- [ ] Code coverage ≥ [target]%

**Functionality:**
- [ ] All phase tasks completed
- [ ] Acceptance criteria met for all tasks
- [ ] Integration points verified
- [ ] API endpoints responding correctly

**Documentation:**
- [ ] Code comments present
- [ ] README updated if needed
- [ ] Supporting docs updated

**Performance:**
- [ ] No obvious performance issues
- [ ] Response times within targets

**Security:**
- [ ] No security vulnerabilities introduced
- [ ] Authentication/authorization working

**Integration:**
- [ ] Works with existing system
- [ ] No breaking changes to other modules

**⚠️ CRITICAL:**
- If ANY validation fails: **STOP**
- Fix all issues before Phase X+1
- Do not accumulate technical debt

**Next Steps:**
Continue to Phase X+1: [Phase name]

---
```

---

## 8. Finalise tasks.md

### 8.1 Assemble Complete Document

Structure:
1. Header with metadata
2. Supporting documentation references
3. Related specs with paths
4. Phase overview table
5. Phase 1 with tasks and checkpoints
6. Phase 2 with tasks and checkpoints
7. ...continue for all phases
8. Final notes and appendix

### 8.2 Consistency Checks

- ✅ All phases follow 10-task rule
- ✅ File-size strategies respected
- ✅ All tasks have acceptance criteria
- ✅ All tasks have validation steps
- ✅ All checkpoints present
- ✅ All spec references resolved with paths
- ✅ Supporting files referenced where needed

---

## 9. Handle Dry Run Mode (NEW)

If `DRY_RUN_MODE = true`:

### 9.1 Generate Comprehensive Plan

Instead of creating files, output detailed plan:

```markdown
# 📋 Task Generation Plan (DRY RUN)

**Would Generate:**

## Primary Output
✅ `[TASKS_PATH]`
- XX phases
- XX total tasks
- XX hours estimated effort

## Supporting Files

**Existing Files Detected:**
- `[file1]` - [description]
- `[file2]` - [description]

**Would Auto-Generate:**
- ✨ `README.md` - Implementation guide (~XXX lines)
  - Reason: [why needed]
  - Content: [summary]
  
- ✨ `data-model.md` - Data model specification (~XXX lines)
  - Reason: [why needed]
  - Entities: [list]
  
- ✨ `openapi.yaml` - API specification (~XXX lines)
  - Reason: [why needed]
  - Endpoints: [count]

**Would NOT Generate (already exists):**
- ⏭️ `existing-file.md` - Would create .new version

## Phase Structure

### Phase 1: [Name] (T001-T010)
- Focus: [areas]
- Risk: [level]
- Hours: XX
- Key tasks:
  - T001: [title]
  - T002: [title]
  ...

[Continue for all phases]

## Tasks Summary

**Total Tasks:** XX
**By Category:**
- CREATE operations: XX files
- EDIT operations: XX files
- TEST files: XX

**File Size Distribution:**
- SMALL (< 200 lines): XX files
- MEDIUM (200-500 lines): XX files
- LARGE (> 500 lines): XX files

## Related Specs (Resolved)

[List with paths and repos]

## Validation

**Would Include:**
- XX mini-checkpoints
- XX major phase checkpoints
- XX validation commands

---

## 📝 Review and Confirm

**To proceed with actual generation:**
Remove --nogenerate flag and run again:
```bash
[original command without --nogenerate]
```

**To modify plan:**
Update spec.md and re-run with --nogenerate

---
```

### 9.2 Report Dry Run Results

Output in Thai:
```
🔍 โหมด Dry Run - ไม่มีการสร้างไฟล์

📊 สิ่งที่จะถูกสร้าง:
- tasks.md: XX phases, XX tasks
- Supporting files: XX ไฟล์

📄 รายละเอียดครบถ้วนอยู่ข้างบน

✅ หากต้องการสร้างจริง:
ลบ --nogenerate flag และรันใหม่
```

**STOP HERE** - Do not proceed to step 10

---

## 10. Write Files (If NOT Dry Run)

If `DRY_RUN_MODE = false`:

### 10.1 Write tasks.md

- Write complete tasks.md to `TASKS_PATH`
- If file exists: Report that regenerating

### 10.2 Write Supporting Files

For each auto-generated supporting file:
- Check if file exists
- If exists: Write to `[filename].new.[ext]`
- If not exists: Write to `[filename].[ext]`
- Log each file created

### 10.3 Validation

After writing all files:
- Verify all files created successfully
- Verify file sizes reasonable
- Verify no corruption

---

## 11. Report Back

In the workflow output (chat), summarize in Thai:

```
✅ สร้าง tasks.md เรียบร้อยแล้ว

📁 ไฟล์หลัก:
- Path: [TASKS_PATH]
- จำนวน phases: XX
- จำนวน tasks: XX
- ประมาณการเวลา: XX hours

📊 โครงสร้าง:
- Phase ที่มีความเสี่ยงสูงสุด: Phase X ([reason])
- Supporting files ที่ตรวจพบ: XX ไฟล์
- Supporting files ที่สร้างใหม่: XX ไฟล์

📄 Supporting Files ที่สร้าง:
[If any generated:]
- ✨ README.md - คู่มือการ implement
- ✨ data-model.md - โครงสร้างข้อมูล
- ✨ openapi.yaml - API specification
- ✨ test-plan.md - แผนการทดสอบ

📎 Supporting Files ที่ตรวจพบ:
[If any detected:]
- 📄 [filename] - [brief description]

🔗 Related Specs (ที่ resolve แล้ว):
- **[spec-id]** ([path], repo: [repo])

📋 ใช้ SPEC_INDEX จาก: [SPEC_INDEX_PATH]

🔄 ขั้นตอนต่อไป:
1. Review tasks.md ให้แน่ใจว่าครบถ้วน
2. Review supporting files ที่สร้างขึ้นมา
3. Run workflow smartspec.generate_kilo_prompt เพื่อสร้าง implementation prompt
4. Optional: Update SPEC_INDEX ถ้าจำเป็น

💡 เคล็ดลับ:
- Supporting files ที่มี .new.md extension แสดงว่ามีไฟล์เดิมอยู่แล้ว
- ควร review และ merge เนื้อหาถ้าจำเป็น
- สามารถ edit tasks.md เพิ่มเติมได้ตามความเหมาะสม
```

---

## Appendix A: File Size Category Reference

```typescript
// Quick reference for task authors

interface FileSizeStrategy {
  SMALL: {
    maxLines: 200,
    createMethod: "full generation safe",
    editMethod: "any method OK",
    strategy: "no special handling"
  },
  
  MEDIUM: {
    maxLines: 500,
    createMethod: "staged creation",
    editMethod: "str_replace only",
    strategy: "no full rewrites"
  },
  
  LARGE: {
    maxLines: Infinity,
    createMethod: "incremental build",
    editMethod: "surgical str_replace",
    strategy: "max 50 lines per change"
  }
}
```

---

## Appendix B: Task Template

```markdown
### Task T0XX: [Clear, Action-Oriented Title] (~X.X hours)

**Description:**
[Detailed explanation of what needs to be done and why]

**Files:**

**CREATE: `path/to/new-file.ts`** (~XXX lines - SMALL)
- [Purpose and responsibilities]
- [Key functions/classes]
- Strategy: [Creation approach]

**EDIT: `path/to/existing.ts`** (add/modify XX lines - MEDIUM)
- Location: [Where in file]
- Changes: [What to change]
- Strategy: str_replace (no full rewrite)

**Supporting Files Referenced:**
- `supporting-file.yaml` - [How used]

**Dependencies:**
- T0YY: [Reason]
- Related Spec: **spec-xxx** (`path`, repo: private)

**Acceptance Criteria:**
- [ ] [Testable criterion]
- [ ] [Testable criterion]

**Validation:**
```bash
[Commands to verify]
```

**Expected Outcome:**
[What works after completion]

---
```

---

## Appendix C: Supporting Files Detection Rules

**Auto-detect patterns:**
- `api-spec.yaml`, `openapi.yaml`, `swagger.yaml`
- `data-model.md`, `schema.md`
- `research.md`, `analysis.md`
- `README.md` (implementation guide)
- `test-plan.md`, `test-cases.md`

**Exclude patterns:**
- `*.backup`, `*.backup-*`, `.backup-*`
- `*.old`, `*.tmp`, `*.temp`
- `spec.new.md`, `spec.backup-*.md`
- `*Zone.Identifier*`

**Auto-generate when:**
- API endpoints in SPEC → `openapi.yaml`
- Database schema in SPEC → `data-model.md`
- Complex project (>50 tasks) → `README.md`
- Testing requirements → `test-plan.md`

---

Context for task generation:
$ARGUMENTS
