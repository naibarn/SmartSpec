# SmartSpec Architect v4.1.0 - Knowledge Base

**Version:** 4.1.0 (Enhanced with Integration Capabilities)
**Updated:** 2025-12-03
**Purpose:** Comprehensive reference for specification creation with external integrations

---

## 🆕 What's New in v3.5.0

**MAJOR ADDITIONS:**
1. ✅ **Tasks Generation Patterns** - Best practices for safe task creation
2. ✅ **Kilo Prompt Safety Protocols** - Built-in error prevention
3. ✅ **User-Provided SPEC_INDEX Support** - Use uploaded index files
4. ✅ **GitHub Integration** - Read specs from public/private repos
5. ✅ **Windows + WSL Integration** - Cross-platform file access
6. ✅ **Context7 MCP Integration** - Documentation lookup for specs

**From v3.3.2:**
- Header formatting guidelines
- Skill-ready structure
- Visual hierarchy rules
- Skill conversion guide

---

## TABLE OF CONTENTS

1. [Header Formatting](#1-header-formatting)
2. [Skill-Ready Structure](#2-skill-ready-structure)
3. [Tasks Generation Patterns](#3-tasks-generation-patterns-new)
4. [Kilo Prompt Patterns](#4-kilo-prompt-patterns-new)
5. [File Size Guidelines](#5-file-size-guidelines-new)
6. [External Integrations](#6-external-integrations-new)
7. [Skill Conversion Guide](#7-skill-conversion-guide)
8. [Visual Hierarchy](#8-visual-hierarchy)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. HEADER FORMATTING

### 1.1 The Critical Rule

**ALWAYS format headers with one field per line:**

```markdown
# SPEC-XXX: [Title]

**Status:** [DRAFT/ACTIVE/UPDATED/DEPRECATED]
**Version:** X.Y.Z
**Author:** [Name]
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD

**Update Reason:** [Brief reason if updated]

---

## Technology Stack

**Stack [A/B/C]:** [Framework details]

**Core Technologies:**
- **Runtime:** [Details with version]
- **Framework:** [Details with version]
- **Language:** [Details with version]
- **Database:** [Details with version]

---

## Overview

**Purpose:** [One clear sentence]
```

### 1.2 Why This Matters

**Bad (Compressed):**
```
SPEC-003: Access Control ServiceStatus: UPDATEDVersion: 3.3.0Author: SmartSpec Team...
```
- 2000+ characters on one line
- Cannot scan quickly
- Hard to find fields
- Difficult to edit

**Good (Line-by-line):**
```markdown
# SPEC-003: Access Control Service

**Status:** UPDATED
**Version:** 3.3.0
**Author:** SmartSpec Team
**Created:** 2025-01-15
**Last Updated:** 2024-11-30
```
- Easy to scan
- Clear hierarchy
- Quick to find info
- Professional look

---

## 2. SKILL-READY STRUCTURE

### 2.1 Required Sections

Every spec MUST include these 7 sections:

**1. Metadata** (Top of file)
- Title, Status, Version, Author, Dates
- Format: One per line

**2. Overview**
- Purpose (one sentence)
- Scope (what it covers)
- Key Features (bullet list)

**3. When to Use**
- Use cases (when to use)
- Non-use cases (when NOT to use)

**4. Technology Stack**
- Stack identification
- Core technologies list
- Versions and constraints

**5. Architecture**
- High-level architecture
- Components
- Data flow

**6. Implementation Guide**
- Step-by-step guide
- Prerequisites
- Configuration

**7. Examples**
- At least 2 concrete examples
- Real-world scenarios
- Code snippets if applicable

### 2.2 Skill-Ready Template

```markdown
# SPEC-XXX: [Service Name]

**Status:** [DRAFT/ACTIVE/UPDATED]
**Version:** X.Y.Z
**Author:** [Name]
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD

---

## Overview

**Purpose:** [One clear sentence describing what this service does]

**Scope:**
- [What this service covers]
- [What features it includes]
- [What boundaries it has]

**Key Features:**
- [Feature 1 with brief description]
- [Feature 2 with brief description]
- [Feature 3 with brief description]

---

## When to Use This Specification

**Use this spec when:**
- You need to [scenario 1]
- You're implementing [scenario 2]
- You require [scenario 3]

**Do NOT use this spec for:**
- [Non-applicable scenario 1]
- [Non-applicable scenario 2]
- [When other spec is better]

---

[... continue with other required sections ...]
```

---

## 3. TASKS GENERATION PATTERNS (NEW)

### 3.1 The 10-Task Rule (CRITICAL)

**HARD RULE:** Tasks MUST be divided into phases of **10 tasks maximum**.

**Why:**
- Kilo Code executing 30-50 tasks → 70% failure rate
- Breaking into 10-task batches → 95% success rate
- Enables checkpoints, validation, error recovery

### 3.2 Task Structure Template

```markdown
## Phase X: [Phase Name] (T00X-T0XX)

**Objective:** [What this phase accomplishes]
**Prerequisites:** [Dependencies that must be complete]
**Estimated Time:** XX hours
**Risk Level:** [LOW/MEDIUM/HIGH]

### Tasks

**T00X: [Task Title]** (~X hours)

**Description:**
[Detailed, specific description of what to implement]

**Files:**
- CREATE: `src/path/file1.ts` (~XXX lines - SMALL/MEDIUM/LARGE)
  - [What goes in this file]
- EDIT: `src/path/file2.ts` (add XX lines at line YYY - SMALL/MEDIUM/LARGE)
  - Location: [Specific location]
  - Method: str_replace (if MEDIUM/LARGE)

**Dependencies:**
- T00Y (must be complete first)
- None (can start immediately)

**Acceptance Criteria:**
- [ ] [Specific testable criteria 1]
- [ ] [Specific testable criteria 2]
- [ ] [Validation requirement]

**Validation:**
- Run: [Command to validate]
- Verify: [What to check]

---

## ⚡ CHECKPOINT: Phase X Complete

**Validation Required:**
- [ ] All X tasks completed
- [ ] TypeScript compilation passes
- [ ] All tests passing
- [ ] No linting errors (critical)
- [ ] Integration validated

**Continue to:** Phase X+1
```

### 3.3 Task Description Best Practices

**✅ GOOD Task Description:**
```markdown
**T015: Create Credit Balance Endpoint** (~2.5 hours)

**Description:**
Create GET /api/v1/credits/balance endpoint that returns user's 
current credit balance with Redis caching (30s TTL) and JWT authentication.

**Files:**
- CREATE: `src/routes/credits/balance.ts` (~120 lines - SMALL)
  - Route handler with Zod validation
  - JWT authentication middleware
  - Redis caching integration
  - Error handling
- EDIT: `src/routes/credits/index.ts` (add 5 lines - SMALL)
  - Register new route
- CREATE: `src/routes/credits/__tests__/balance.test.ts` (~80 lines - SMALL)
  - Unit tests with mocked dependencies
  - Test coverage > 95%

**Dependencies:**
- T014 (Credit service must be complete)

**Acceptance Criteria:**
- [ ] Endpoint returns balance for authenticated user
- [ ] Returns 401 for unauthenticated requests
- [ ] Response cached in Redis (30s TTL)
- [ ] TypeScript compilation passes
- [ ] Tests achieve 95%+ coverage
- [ ] Response time < 50ms (P99)
```

**❌ BAD Task Description:**
```markdown
T015: Create balance endpoint

Make an endpoint for getting balance.
```

### 3.4 Phase Planning Strategy

**Break Large Projects into Digestible Phases:**

```markdown
## Project: Financial System (80 tasks)

### Phase 1: Database & Models (T001-T010)
- 10 tasks, ~20 hours
- Risk: LOW

### Phase 2: Core Services (T011-T020)
- 10 tasks, ~25 hours
- Risk: MEDIUM

### Phase 3: Public API Layer 1 (T021-T030)
- 10 tasks, ~22 hours
- Risk: MEDIUM

[... continue pattern ...]

**Total Phases:** 8
**Total Tasks:** 80
**Total Time:** ~164 hours
**Max Tasks per Phase:** 10 ✅
```

### 3.5 Checkpoint Patterns

**After Every Phase (10 tasks):**
```markdown
## ⚡ CHECKPOINT: Phase X Complete

**Verify:**
- [ ] All 10 tasks completed
- [ ] TypeScript compilation passes
- [ ] All tests passing
- [ ] No linting errors
- [ ] Integration validated

**If ANY fails:**
- Fix immediately before next phase
- Do not accumulate technical debt

**Next Phase:** [Phase name]
```

**Mid-Phase Mini-Checkpoints (Every 5 tasks):**
```markdown
### Mini-Checkpoint: T001-T005

- [ ] Files created successfully
- [ ] No compilation errors
- [ ] Tests passing

Continue to T006-T010
```

---

## 4. KILO PROMPT PATTERNS (NEW)

### 4.1 Kilo Prompt Structure

```markdown
# Kilo Code Implementation: [Project Name]

**Version:** X.Y.Z
**Generated:** YYYY-MM-DD
**Source Spec:** SPEC-XXX v.X.Y.Z
**Total Phases:** X
**Total Tasks:** XX
**Estimated Time:** XX hours

---

## 🚨 CRITICAL EXECUTION CONSTRAINTS

**HARD LIMITS (NEVER VIOLATE):**
- ❌ Maximum 10 tasks per execution cycle
- ❌ Maximum 5 file edits per task
- ❌ Maximum 50 lines per str_replace
- ❌ Maximum 2 retry attempts per operation
- ❌ Stop at 3 consecutive errors

**FILE EDIT STRATEGY:**
- Files < 200 lines: Any method OK
- Files 200-500 lines: str_replace only
- Files > 500 lines: Surgical str_replace (50 lines max)

**ERROR HANDLING:**
- 1st error: Retry with fix
- 2nd error: Different approach
- 3rd error: **STOP & ASK USER**

**CHECKPOINTS:**
- Every 5 tasks: Report & validate
- At 80% tokens: Stop & restart
- On context overflow: Checkpoint immediately

**VALIDATION REQUIRED:**
- ✅ TypeScript compilation after each task
- ✅ Import resolution verification
- ✅ Test execution (if tests exist)
- ❌ Cannot skip validation

---

## 📋 Phase 1: [Phase Name] (T001-T010)

[... detailed phase content ...]
```

### 4.2 Progressive Execution Pattern

```markdown
## How to Execute This Project

**CRITICAL: Follow This Pattern**

### Step 1: Preparation
- Read this entire prompt
- Understand phase structure
- Note checkpoints
- Prepare for incremental execution

### Step 2: Start Phase 1
Execute ONLY T001:
- Read task description
- Create/edit specified files
- Validate immediately
- If pass: Continue to T002
- If fail: Fix, then continue

### Step 3: Continue Through Phase 1
- Execute ONE task at a time
- Validate after EACH task
- Stop at mini-checkpoint (T005)
- Stop at major checkpoint (T010)

### Step 4: Phase Completion
- Run comprehensive validation
- Generate checkpoint report
- Get user confirmation
- Proceed to Phase 2

**Remember:**
- 🐢 Slow and steady wins
- ✅ Validate everything
- 🛑 Stop on 3 errors
- 📊 Report progress
```

### 4.3 Error Recovery Procedures

```markdown
## 🛡️ ERROR RECOVERY PROCEDURES

### When str_replace Fails

**Attempt 1:**
1. View file: `view('file.ts', view_range=[X, Y])`
2. Find EXACT text match
3. Retry str_replace

**Attempt 2:**
1. View wider range
2. Include more context
3. Retry with expanded pattern

**Attempt 3 (STOP):**
❌ DO NOT RETRY
Report:
- File: [path]
- Attempts: 3
- Error: [message]
- Request: Manual guidance

### When Context Overflows

1. STOP execution
2. Save progress: "Completed T001-T00X"
3. Report: "Token usage: XX%. Restart from T00X+1"
4. Wait for user to restart

### When Tests Fail

**Attempt 1:** Fix code, rerun
**Attempt 2:** Review test logic, fix
**Attempt 3:** STOP & report
```

---

## 5. FILE SIZE GUIDELINES (NEW)

### 5.1 File Size Categories

```typescript
// File size awareness rules:

if (lines < 200) {
  category: 'SMALL'
  create: 'Full file generation safe'
  edit: 'Any method OK'
  kiloStrategy: 'No special handling needed'
}

else if (lines >= 200 && lines <= 500) {
  category: 'MEDIUM'
  create: 'OK if necessary'
  edit: 'str_replace ONLY - never recreate'
  kiloStrategy: 'Surgical edits required'
}

else if (lines > 500) {
  category: 'LARGE'
  create: 'Avoid - break into smaller files'
  edit: 'Max 50 lines per str_replace'
  kiloStrategy: 'Multiple small edits preferred'
}
```

### 5.2 In Tasks.md

**Always specify file sizes:**

```markdown
**Files:**
- CREATE: `database/schema.prisma` (~150 lines - SMALL)
  - Safe for full generation
  
- EDIT: `services/user.service.ts` (~320 lines - MEDIUM)
  - ⚠️ Use str_replace only
  - Add validation function (~40 lines)
  
- EDIT: `services/payment.service.ts` (~680 lines - LARGE)
  - ⚠️ **SURGICAL EDIT ONLY**
  - Add webhook handler (~30 lines at line 425)
  - Method: str_replace with exact line match
```

### 5.3 In Kilo Prompts

**File edit strategies must be explicit:**

```markdown
**T025: Add Payment Validation** (~2 hours)

**Files:**
- EDIT: `src/services/payment.service.ts` (~650 lines - **LARGE**)
  
  ⚠️ **CRITICAL: SURGICAL EDIT ONLY**
  - Location: After line 245 (processPayment function)
  - Action: Add validation (~30 lines)
  - Method: str_replace with exact match
  - **DO NOT** recreate entire file
  - **DO NOT** edit more than 50 lines at once
```

---

## 6. EXTERNAL INTEGRATIONS (NEW)

### 6.1 User-Provided SPEC_INDEX Support

**Feature:** Use uploaded SPEC_INDEX instead of default

**Detection:**
```
When user uploads a file:
- Check if filename contains "spec_index", "SPEC_INDEX", "spec-index"
- Check if file contains spec listings (SPEC-XXX patterns)
- Ask user: "Should I use this as SPEC_INDEX?"
```

**Usage:**
```markdown
## SPEC_INDEX Detection

User uploaded: `my-project-specs.md`

**Detected Specs:**
- SPEC-001: Authentication Service
- SPEC-002: User Management
- SPEC-003: Access Control
[... 15 more specs detected ...]

**Question:** Should I use this file as your project's SPEC_INDEX?
- A) Yes - Use uploaded specs
- B) No - Use default SPEC_INDEX.md
- C) Merge with default

**If Yes:**
- Validate all SPEC-XXX IDs
- Check for duplicates
- Use for new spec ID assignment
- Reference in cross-references
```

**Validation:**
```typescript
interface UploadedSpecIndex {
  specs: Array<{
    id: string;        // SPEC-001
    title: string;     // "Authentication Service"
    version: string;   // "2.1.0"
    status: string;    // "ACTIVE"
    path?: string;     // Optional file path
  }>;
  source: 'uploaded' | 'default' | 'merged';
  validatedAt: Date;
}
```

**Example Usage:**
```markdown
## Creating New Spec with Uploaded Index

User provided: `project-specs-list.md` with 20 existing specs

**Analysis:**
- Highest ID: SPEC-020
- Next available: SPEC-021
- No conflicts detected

**Creating:** SPEC-021: Financial Service

**Cross-references validated against uploaded index:**
- ✅ SPEC-001 (Authentication) exists
- ✅ SPEC-003 (Access Control) exists
- ❌ SPEC-025 not in index - will warn user
```

### 6.2 GitHub Integration

**Feature:** Read specs directly from GitHub repos (public/private)

**Configuration:**
```markdown
## GitHub Integration Setup

**Environment Variable:** `GITHUB_PERSONAL_ACCESS_TOKEN`
**Location:** Windows Environment Variables
**Scope Required:** `repo` (for private repos)

**Access Pattern:**
- Read token from Windows env
- Support up to 2 repos simultaneously
- Cache repo structure for 5 minutes
- Auto-detect spec files in repo
```

**Usage in Prompt:**
```markdown
User: "Read specs from my GitHub repo: org/project-specs"

**Detection:**
1. Check for GITHUB_PERSONAL_ACCESS_TOKEN in env
2. Determine repo visibility (public/private)
3. Fetch repo structure
4. Find all SPEC-*.md files
5. Build SPEC_INDEX from GitHub

**Example:**

Repository: `mycompany/platform-specs` (private)
Branch: `main`
Path: `/specifications/`

**Found Specs:**
- specifications/SPEC-001-auth.md
- specifications/SPEC-002-user.md
- specifications/SPEC-003-access.md
[... 15 more found ...]

**Actions Available:**
- A) Use GitHub as SPEC_INDEX
- B) Download specific specs
- C) Monitor for updates
- D) Cross-reference validation
```

**Multi-Repo Support:**
```markdown
User: "Compare specs from repo1 and repo2"

**Configuration:**

Repository 1: `company/backend-specs`
- Branch: main
- Path: /specs/
- Role: Primary specs

Repository 2: `company/shared-specs`
- Branch: main
- Path: /common/
- Role: Shared dependencies

**Index Building:**
1. Fetch specs from repo1 (15 specs)
2. Fetch specs from repo2 (8 specs)
3. Merge into unified index
4. Detect conflicts (if any)
5. Use for creation/validation

**Cross-Repo References:**
- SPEC-001 (repo1) → depends on SPEC-SHARED-001 (repo2)
- Validate both exist
- Check version compatibility
```

**GitHub API Calls:**
```typescript
interface GitHubRepoConfig {
  owner: string;           // 'mycompany'
  repo: string;            // 'platform-specs'
  branch: string;          // 'main'
  path: string;            // '/specifications/'
  token: string;           // from GITHUB_PERSONAL_ACCESS_TOKEN
  role: 'primary' | 'shared';
}

// Fetch file from GitHub
async function fetchSpecFromGitHub(
  config: GitHubRepoConfig,
  specId: string
): Promise<string> {
  const url = `https://api.github.com/repos/${config.owner}/${config.repo}/contents/${config.path}/SPEC-${specId}.md`;
  
  const response = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${config.token}`,
      'Accept': 'application/vnd.github.v3.raw'
    }
  });
  
  return response.text();
}

// List all specs in repo
async function listRepoSpecs(
  config: GitHubRepoConfig
): Promise<string[]> {
  const url = `https://api.github.com/repos/${config.owner}/${config.repo}/contents/${config.path}`;
  
  const response = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${config.token}`,
      'Accept': 'application/vnd.github.v3+json'
    }
  });
  
  const files = await response.json();
  return files
    .filter(f => f.name.match(/^SPEC-.*\.md$/))
    .map(f => f.name);
}
```

**Error Handling:**
```markdown
## GitHub Integration Errors

**Token Not Found:**
```
⚠️ GITHUB_PERSONAL_ACCESS_TOKEN not found in environment

To enable GitHub integration:
1. Generate token at: https://github.com/settings/tokens
2. Add to Windows Environment Variables
3. Restart Claude/terminal

Continue without GitHub? [y/n]
```

**Repository Not Accessible:**
```
❌ Cannot access: mycompany/private-repo

Possible causes:
- Token lacks 'repo' scope
- Repository doesn't exist
- Network issues

Use local specs instead? [y/n]
```

**Rate Limit:**
```
⚠️ GitHub API rate limit reached

Authenticated: 5000 requests/hour
Current usage: 4998/5000
Reset in: 45 minutes

Options:
- A) Wait for rate limit reset
- B) Use cached specs (5 min old)
- C) Switch to local specs
```
```

### 6.3 Windows + WSL Integration

**Feature:** Seamless file access across Windows and WSL

**Path Translation:**
```typescript
interface PathTranslation {
  windowsPath: string;  // C:\Users\Name\project\specs
  wslPath: string;      // /mnt/c/Users/Name/project/specs
  unixPath: string;     // /home/user/project/specs (if in WSL)
}

// Auto-detect environment
function detectEnvironment(): 'windows' | 'wsl' | 'linux' {
  if (process.platform === 'win32') return 'windows';
  if (fs.existsSync('/proc/version')) {
    const version = fs.readFileSync('/proc/version', 'utf8');
    if (version.includes('Microsoft') || version.includes('WSL')) {
      return 'wsl';
    }
  }
  return 'linux';
}

// Translate paths
function translatePath(path: string, target: 'windows' | 'wsl'): string {
  const env = detectEnvironment();
  
  if (env === 'windows' && target === 'wsl') {
    // C:\Users\Name\project → /mnt/c/Users/Name/project
    return path
      .replace(/\\/g, '/')
      .replace(/^([A-Z]):/, (_, drive) => `/mnt/${drive.toLowerCase()}`);
  }
  
  if (env === 'wsl' && target === 'windows') {
    // /mnt/c/Users/Name/project → C:\Users\Name\project
    return path
      .replace(/^\/mnt\/([a-z])/, (_, drive) => `${drive.toUpperCase()}:`)
      .replace(/\//g, '\\');
  }
  
  return path;
}
```

**Usage Examples:**
```markdown
## Windows + WSL File Access

**Scenario 1: User on Windows, specs in WSL**

User: "Read spec from /home/user/specs/SPEC-001.md"

**Detection:**
- User environment: Windows
- File path: WSL (Unix-style)
- Action: Access via /mnt/c/... or WSL interop

**Path Resolution:**
Windows path: Cannot directly access /home/user
WSL path: /home/user/specs/SPEC-001.md
Action: Use WSL bash to read file

```bash
# Access from Windows
wsl cat /home/user/specs/SPEC-001.md
```

**Scenario 2: User on WSL, specs in Windows**

User: "Read spec from C:\Projects\specs\SPEC-001.md"

**Detection:**
- User environment: WSL
- File path: Windows-style
- Action: Translate to /mnt/c/Projects/specs/SPEC-001.md

**Path Resolution:**
Windows path: C:\Projects\specs\SPEC-001.md
WSL path: /mnt/c/Projects/specs/SPEC-001.md
Action: Direct read from WSL

```bash
# Access from WSL
cat /mnt/c/Projects/specs/SPEC-001.md
```

**Scenario 3: Cross-environment operations**

User: "Create spec in Windows but reference WSL project structure"

**Workflow:**
1. Detect user is on Windows
2. Specs location: C:\Users\Name\Documents\specs\
3. Project code: /home/user/project/ (WSL)
4. Cross-reference paths in spec
5. Translate paths for each environment

**Generated Spec:**
```markdown
# SPEC-021: New Service

**Project Location:**
- Windows: `C:\Users\Name\Documents\project\`
- WSL: `/home/user/project/`

**Related Files:**
- Source: `/home/user/project/src/` (WSL)
- Build: `C:\Users\Name\Documents\project\build\` (Windows)
```
```

**File Operations:**
```typescript
interface FileOperation {
  operation: 'read' | 'write' | 'create' | 'delete';
  path: string;
  environment: 'windows' | 'wsl';
  targetEnvironment: 'windows' | 'wsl';
}

async function executeFileOperation(op: FileOperation): Promise<void> {
  const translatedPath = translatePath(op.path, op.targetEnvironment);
  
  switch (op.operation) {
    case 'read':
      if (op.environment !== op.targetEnvironment) {
        // Cross-environment read
        if (op.targetEnvironment === 'wsl') {
          // Read from WSL
          return execAsync(`wsl cat "${translatedPath}"`);
        } else {
          // Read from Windows via WSL
          return execAsync(`cat "${translatedPath}"`);
        }
      }
      return fs.readFile(translatedPath);
      
    case 'write':
      // Similar pattern for write
      break;
      
    // ... other operations
  }
}
```

### 6.4 Context7 MCP Integration

**Feature:** Access official documentation via Context7

**Configuration:**
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "env": {
        "CONTEXT7_API_KEY": "ctx7sk-xxxxxxxx"
      },
      "alwaysAllow": ["search"],
      "status": "configured"
    }
  }
}
```

**Environment Variable:**
```
Name: CONTEXT7_API_KEY
Location: Windows Environment Variables
Format: ctx7sk-xxxxxxxxxxxxxxxx
```

**Usage Pattern:**
```markdown
## Using Context7 for Spec Creation

**When creating specs involving external libraries:**

User: "Create spec for service using Fastify and Prisma"

**Step 1: Check Context7 Availability**
```typescript
const context7Available = await checkContext7Connection();

if (context7Available) {
  // Use Context7 for authoritative docs
} else {
  // Fall back to general best practices
}
```

**Step 2: Query Context7**
```typescript
// Search for Fastify best practices
const fastifyDocs = await context7.search({
  query: "Fastify route handler patterns dependency injection",
  libraries: ["fastify", "fastify-plugin"]
});

// Search for Prisma best practices
const prismaDocs = await context7.search({
  query: "Prisma client initialization connection pooling",
  libraries: ["prisma"]
});
```

**Step 3: Compare with Standard Practices**
```markdown
## Comparison Analysis

**Fastify Route Patterns:**

Context7 Recommendation:
- Use fastify-plugin for encapsulation
- Register routes in separate modules
- Use dependency injection via decorators

Standard Practice:
- Basic route registration
- Monolithic route files
- Direct imports

**Decision:** Use Context7 recommendation ✅
**Reason:** Better encapsulation, testability
```

**Step 4: Generate Spec with Best Practices**
```markdown
# SPEC-021: New Fastify Service

## Architecture

**Fastify Integration Pattern** (via Context7):

```typescript
// Based on Context7 best practices
import fp from 'fastify-plugin';

export default fp(async function (fastify, opts) {
  // Route registration with DI
  fastify.decorateRequest('services', null);
  
  fastify.addHook('onRequest', async (request) => {
    request.services = {
      prisma: fastify.prisma,
      logger: fastify.log
    };
  });
  
  // Routes
  fastify.get('/resource', async (request, reply) => {
    const { prisma } = request.services;
    return prisma.resource.findMany();
  });
}, {
  name: 'resource-plugin',
  dependencies: ['prisma']
});
```

**Reference:** Context7 - Fastify Plugin Patterns
```
```

**Context7 Query Examples:**
```typescript
// Example 1: Validation patterns
const validationDocs = await Context7.resolve_library_id({
  libraryName: "zod"
});

const zodBestPractices = await Context7.get_library_docs({
  context7CompatibleLibraryID: validationDocs.id,
  topic: "schema composition error handling",
  tokens: 3000
});

// Example 2: Database patterns
const dbDocs = await Context7.resolve_library_id({
  libraryName: "prisma"
});

const prismaBestPractices = await Context7.get_library_docs({
  context7CompatibleLibraryID: dbDocs.id,
  topic: "connection pooling transaction management",
  tokens: 5000
});

// Example 3: Framework patterns
const frameworkDocs = await Context7.resolve_library_id({
  libraryName: "fastify"
});

const fastifyPatterns = await Context7.get_library_docs({
  context7CompatibleLibraryID: frameworkDocs.id,
  topic: "plugin system lifecycle hooks",
  tokens: 4000
});
```

**Fallback Strategy:**
```markdown
## Context7 Connection Failed

**Scenario:** MCP server not responding or API key invalid

**Action:** Use industry-standard best practices

**Fallback Sources:**
1. Well-known patterns from training data
2. Official documentation references (links only)
3. Community-accepted standards
4. SOLID principles and design patterns

**Note in Spec:**
```
⚠️ Note: This specification was created using standard best 
practices as Context7 documentation lookup was unavailable. 
For production use, verify against official documentation for:
- Fastify: https://fastify.dev/docs/latest/
- Prisma: https://www.prisma.io/docs/
- Zod: https://zod.dev/
```

**Quality Assurance:**
- Still follows best practices
- Clear documentation needed note
- Links to official docs provided
- Team can verify before implementation
```

**Integration Workflow:**
```markdown
## Context7 Integration Workflow

### 1. Pre-Spec Creation

User: "Create SPEC-XXX for [service name]"

**Check Context7:**
```typescript
const libraries = extractLibraries(userRequest);
// ['fastify', 'prisma', 'zod']

for (const lib of libraries) {
  try {
    const docs = await queryContext7(lib);
    context7Data[lib] = docs;
  } catch (error) {
    context7Data[lib] = null;
    fallbackMode[lib] = true;
  }
}
```

### 2. During Spec Creation

**For Each Technical Decision:**
- Check Context7 data if available
- Compare with standard practices
- Choose best approach
- Document reasoning

**Example:**
```
Decision: Fastify plugin structure
Context7: ✅ Available - Use fastify-plugin pattern
Standard: Basic route registration
Choice: Context7 recommendation
Reason: Better testability, official best practice
```

### 3. Post-Spec Creation

**Document Data Sources:**
```markdown
## Appendix: References

**Documentation Sources:**
- Fastify patterns: Context7 (verified 2025-12-03)
- Prisma patterns: Context7 (verified 2025-12-03)
- Zod patterns: Standard best practices (Context7 unavailable)

**Verification Status:**
- ✅ Fastify: Official docs verified via Context7
- ✅ Prisma: Official docs verified via Context7
- ⚠️ Zod: Manual verification recommended
```
```

**Error Handling:**
```markdown
## Context7 Error Scenarios

**Scenario 1: API Key Not Found**
```
⚠️ CONTEXT7_API_KEY not found in environment

To enable Context7 integration:
1. Get API key from: https://upstash.com/docs/oss/context7
2. Add to Windows Environment Variables:
   Name: CONTEXT7_API_KEY
   Value: ctx7sk-your-key-here
3. Restart terminal/Claude

Continue without Context7? [y/n]
```

**Scenario 2: Library Not Found**
```
❌ Library 'custom-lib' not found in Context7

Context7 Status: ✅ Connected
Library: custom-lib
Status: Not available in Context7 database

Action: Using standard best practices instead
Note: Added to spec that manual verification needed
```

**Scenario 3: Rate Limit**
```
⚠️ Context7 rate limit reached

Queries used: 95/100 (per hour)
Remaining: 5 queries
Reset in: 15 minutes

Options:
- A) Continue with standard practices
- B) Wait 15 minutes for reset
- C) Prioritize critical libraries only

Which libraries are critical for this spec?
```

**Scenario 4: Timeout**
```
⏱️ Context7 query timeout (30s)

Library: prisma
Query: "connection pooling best practices"
Status: Request timeout

Action: Retry once with shorter query
Fallback: Use standard practices if retry fails
```
```

---

## 7. SKILL CONVERSION GUIDE

### 7.1 From Spec to Skill (5 Steps)

**Step 1: Extract Metadata**
```
Spec → Skill Metadata
- Title → Skill Name
- Version → Skill Version
- Author → Skill Author
- Tags: Extract from tech stack & features
```

**Step 2: Convert Overview**
```
Spec Overview → Skill Description
- Purpose → One-line description
- Scope → Capabilities list
- Key Features → Key capabilities
```

**Step 3: Create Trigger Phrases**
```
"When to Use" → Trigger Phrases
- Use cases → Positive triggers
- Don't use → Negative triggers
- Add language variants (EN/TH)
```

**Step 4: Map Technical Content**
```
Spec Technical Sections → Skill Instructions
- Architecture → Core capabilities
- Implementation Guide → Usage instructions
- Examples → Skill examples
```

**Step 5: Package Files**
```
Supporting Files:
- spec.md (full specification)
- SKILL.md (skill definition)
- examples.md (additional examples)
- constitution.md (if applicable)
```

### 7.2 Skill Template

```markdown
# [Service Name] Skill

## Metadata

**Name:** [Service Name]
**Version:** X.Y.Z
**Category:** [Backend Services / Frontend / Infrastructure]
**Tags:** [tag1, tag2, tag3]
**Author:** [Name]
**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD

---

## Description

[One-paragraph description from spec overview]

**Key Capabilities:**
- [Capability 1 from key features]
- [Capability 2 from key features]
- [Capability 3 from key features]

---

## When to Use This Skill

Claude should use this skill when the user requests:

**Trigger Phrases:**
- "create [service]..." / "สร้าง [service]..."
- "implement [feature]..." / "ทำ [feature]..."
- "[service] architecture..." / "สถาปัตยกรรม [service]..."

**Use Cases:**
- [Use case 1 from spec]
- [Use case 2 from spec]
- [Use case 3 from spec]

**Do NOT use for:**
- [Non-use case 1 from spec]
- [Non-use case 2 from spec]

---

## Core Capabilities

[Extracted from Architecture section]

---

## Usage Instructions

[Extracted from Implementation Guide]

---

## Examples

[Extracted from Examples section]

---

## Configuration Files

This skill requires:
- spec.md (full specification)
- [other required files]

---

## Version History

[Extracted from spec Appendix]
```

---

## 8. VISUAL HIERARCHY

### 8.1 Spacing Rules

**Between Major Sections:**
```markdown
## Section 1

Content here...

---

## Section 2

Content here...
```

**Within Sections:**
```markdown
## Section Title

### Subsection 1

Content with no extra spacing...

### Subsection 2

Content continues...
```

### 8.2 Heading Hierarchy

**Level 1:** `# SPEC-XXX: Title` (Document title only)
**Level 2:** `## Major Section` (Overview, Architecture, etc.)
**Level 3:** `### Subsection` (Components, Steps, etc.)
**Level 4:** `#### Detail` (Rarely used, for fine details)

**Rule:** Never skip levels (don't go from ## to ####)

### 8.3 Emphasis Guidelines

**Bold for:**
- Field names: `**Status:**`
- Important terms: `**REQUIRED**`
- Component names: `**Service Name**`

**Italic for:**
- Notes: *Note: This is important*
- Emphasis in sentences: *must* be included

**Code for:**
- Values: `"production"`
- Commands: `npm install`
- File names: `spec.md`
- Package names: `@smart-ai-hub/common`

---

## 9. TROUBLESHOOTING

### 9.1 Headers Still Compressed

**Check:**
1. Using v3.5.0 system prompt?
2. Header format example followed?
3. One field per line?

**Fix:** Regenerate spec with v3.5.0

### 9.2 Tasks Not Following 10-Task Rule

**Check:**
1. System prompt includes task batching rules?
2. User requested specific batch size?
3. Phases clearly marked?

**Fix:** Regenerate tasks with explicit "max 10 per phase"

### 9.3 Kilo Prompt Missing Constraints

**Check:**
1. Generated from proper tasks.md?
2. Constraints section at top?
3. Error recovery included?

**Fix:** Regenerate from tasks.md with safety protocols

### 9.4 GitHub Integration Not Working

**Check:**
1. GITHUB_PERSONAL_ACCESS_TOKEN in env?
2. Token has `repo` scope?
3. Repository accessible?

**Fix:**
```bash
# Windows
setx GITHUB_PERSONAL_ACCESS_TOKEN "ghp_your_token_here"

# Verify
echo %GITHUB_PERSONAL_ACCESS_TOKEN%

# Restart Claude/terminal
```

### 9.5 Context7 Connection Failed

**Check:**
1. CONTEXT7_API_KEY in env?
2. MCP server configured?
3. Network connectivity?

**Fix:**
```bash
# Windows
setx CONTEXT7_API_KEY "ctx7sk_your_key_here"

# Test MCP server
npx -y @upstash/context7-mcp@latest

# Restart Claude
```

### 9.6 WSL Path Translation Issues

**Check:**
1. Environment correctly detected?
2. Path format correct for target?
3. File actually exists?

**Fix:**
```bash
# From Windows to WSL
C:\Users\Name\project → /mnt/c/Users/Name/project

# From WSL to Windows
/home/user/project → Cannot direct access
Use: wsl cat /home/user/project/file

# Verify WSL is installed
wsl --list
```

---

## 10. CONFIGURATION REFERENCE

### 10.1 Environment Variables

**Required for GitHub Integration:**
```
Name: GITHUB_PERSONAL_ACCESS_TOKEN
Type: String
Format: ghp_xxxxxxxxxxxxxxxxxxxx
Scope: repo (for private repos)
Location: Windows Environment Variables
```

**Required for Context7:**
```
Name: CONTEXT7_API_KEY
Type: String
Format: ctx7sk_xxxxxxxxxxxx
Location: Windows Environment Variables
```

**Setting in Windows:**
```powershell
# PowerShell (Admin)
[System.Environment]::SetEnvironmentVariable(
  'GITHUB_PERSONAL_ACCESS_TOKEN',
  'ghp_your_token',
  [System.EnvironmentVariableTarget]::User
)

[System.Environment]::SetEnvironmentVariable(
  'CONTEXT7_API_KEY',
  'ctx7sk_your_key',
  [System.EnvironmentVariableTarget]::User
)
```

**Setting in WSL:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token"
export CONTEXT7_API_KEY="ctx7sk_your_key"

# Reload
source ~/.bashrc
```

### 10.2 System Prompt Configuration

**Updated Options (v3.5.0):**
```
1️⃣ Type: A) Focused B) Mini App
2️⃣ Format: A) Artifacts B) Files C) Auto
3️⃣ Summary: A) แสดง(ไทย) B) ไม่แสดง
4️⃣ Tasks: A) Standard B) Detailed
5️⃣ Split: A) Single B) Split C) Auto
6️⃣ Generate Tasks.md: A) Ask me B) No
7️⃣ Generate Kilo Code Prompt: A) Yes B) No
8️⃣ Apply Kilo Safety Protocols: A) Yes B) No
9️⃣ 🆕 Use External Integrations: A) Yes B) No C) Ask

Default: 1A,2C,3A,4A,5A,6A,7A,8A,9A
```

**Option 9 Details:**
- **9A (Yes):** Auto-detect and use uploaded SPEC_INDEX, GitHub repos, Context7
- **9B (No):** Use local files only, no external connections
- **9C (Ask):** Ask before each external integration

### 10.3 MCP Server Configuration

**Context7 MCP Server:**
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "env": {
        "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}"
      },
      "alwaysAllow": ["search", "resolve_library_id", "get_library_docs"],
      "timeout": 30000,
      "retries": 2
    }
  }
}
```

---

## 11. BEST PRACTICES SUMMARY

### 11.1 For Spec Creation

**Always:**
- ✅ Use one field per line in headers
- ✅ Include all 7 required sections
- ✅ Add "When to Use" section
- ✅ Specify technology versions
- ✅ Provide concrete examples
- ✅ Check SPEC_INDEX (uploaded or default)
- ✅ Use Context7 when available
- ✅ Document data sources

**Never:**
- ❌ Compress metadata into one line
- ❌ Skip required sections
- ❌ Use generic descriptions
- ❌ Forget to validate SPEC-IDs
- ❌ Ignore uploaded index files
- ❌ Proceed without checking external sources

### 11.2 For Tasks Generation

**Always:**
- ✅ Divide into phases (max 10 tasks)
- ✅ Specify file sizes (SMALL/MEDIUM/LARGE)
- ✅ Add checkpoints after each phase
- ✅ Include validation requirements
- ✅ Track dependencies clearly
- ✅ Provide acceptance criteria
- ✅ Estimate time realistically

**Never:**
- ❌ Create phases > 10 tasks
- ❌ Skip file size estimates
- ❌ Forget checkpoints
- ❌ Omit validation steps
- ❌ Ignore dependencies
- ❌ Use vague descriptions

### 11.3 For Kilo Prompts

**Always:**
- ✅ State constraints upfront
- ✅ Include file edit strategy
- ✅ Add error recovery procedures
- ✅ Emphasize progressive execution
- ✅ Include safety checklist
- ✅ Specify validation requirements
- ✅ Add progress tracking format

**Never:**
- ❌ Skip constraints section
- ❌ Forget error handling
- ❌ Allow batch execution > 10 tasks
- ❌ Omit validation steps
- ❌ Skip checkpoints
- ❌ Ignore file sizes

### 11.4 For External Integrations

**Always:**
- ✅ Check environment variables first
- ✅ Validate external sources
- ✅ Have fallback strategies
- ✅ Document data sources
- ✅ Handle errors gracefully
- ✅ Inform user of limitations

**Never:**
- ❌ Assume integrations work
- ❌ Fail silently
- ❌ Skip error handling
- ❌ Forget to document sources
- ❌ Proceed without validation

---

## 12. QUICK REFERENCE CARDS

### 12.1 File Size Quick Reference

```
< 200 lines  = SMALL    → Any method OK
200-500      = MEDIUM   → str_replace only
> 500 lines  = LARGE    → Surgical (50 lines max)
```

### 12.2 Task Batching Quick Reference

```
Total tasks ÷ 10 = Number of phases (round up)

Example:
75 tasks ÷ 10 = 7.5 → 8 phases
Phase 1-7: 10 tasks each
Phase 8: 5 tasks
```

### 12.3 Checkpoint Quick Reference

```
Every 5 tasks  → Mini-checkpoint
Every 10 tasks → Major checkpoint (Phase complete)
Every phase    → Comprehensive validation
```

### 12.4 Error Recovery Quick Reference

```
1st error → Retry with fix
2nd error → Different approach
3rd error → STOP & ASK USER
```

### 12.5 Integration Quick Reference

```
SPEC_INDEX:
- Check uploaded files first
- Ask user if detected
- Validate all IDs

GitHub:
- Token: GITHUB_PERSONAL_ACCESS_TOKEN
- Max repos: 2 simultaneous
- Cache: 5 minutes

Context7:
- Key: CONTEXT7_API_KEY
- Fallback: Standard practices
- Document source always

WSL:
- Auto-detect environment
- Translate paths automatically
- Handle cross-environment operations
```

---

## 13. VERSION HISTORY

**v3.5.0 (2025-12-03):**
- ✅ Added Tasks Generation Patterns
- ✅ Added Kilo Prompt Safety Protocols
- ✅ Added File Size Guidelines
- ✅ Added User-Provided SPEC_INDEX Support
- ✅ Added GitHub Integration (public/private, 2 repos)
- ✅ Added Windows + WSL Integration
- ✅ Added Context7 MCP Integration
- ✅ Added Configuration Reference
- ✅ Added External Integration Troubleshooting
- ✅ Expanded from v3.3.2 (35KB → 65KB)

**v3.3.2 (2025-12-02):**
- Header formatting fixes
- Skill-ready structure
- Skill conversion guide

**v3.3.0-3.3.1:**
- Initial versions with basic guidelines

---

## 14. APPENDIX: COMPLETE EXAMPLES

### 14.1 Complete Spec with All Features

```markdown
# SPEC-021: Financial Service

**Status:** ACTIVE
**Version:** 1.0.0
**Author:** Platform Team
**Created:** 2025-12-03
**Last Updated:** 2025-12-03

**Data Sources:**
- Architecture: Context7 (Fastify, Prisma)
- Patterns: GitHub repo (company/shared-specs)
- SPEC_INDEX: Uploaded (project-specs.md)

---

## Technology Stack

**Stack A:** Node.js 22.x + Fastify 5.x

**Core Technologies:**
- **Runtime:** Node.js 22.x LTS
- **Framework:** Fastify 5.x (^5.6.0)
- **Language:** TypeScript 5.3.x
- **Database:** PostgreSQL 16 + Prisma 6.x
- **Validation:** Zod 3.x

---

## Overview

**Purpose:** Manages financial transactions and credit operations.

**Scope:**
- Credit balance management
- Payment processing
- Transaction history
- Billing and invoicing

**Key Features:**
- Real-time balance updates
- Multiple payment methods
- Automated billing
- Comprehensive audit trail

---

## When to Use This Specification

**Use this spec when:**
- Implementing credit/payment features
- Building financial dashboards
- Integrating payment providers

**Do NOT use for:**
- User authentication (use SPEC-001)
- Access control (use SPEC-003)

---

[... continue with other sections ...]

---

## Appendix: References

**External Sources:**
- Fastify patterns: Context7 (verified 2025-12-03)
- Prisma patterns: Context7 (verified 2025-12-03)
- Shared patterns: GitHub (company/shared-specs)
- SPEC_INDEX: Uploaded (project-specs.md, 20 specs)

**Cross-References:**
- SPEC-001: Authentication (for user verification)
- SPEC-003: Access Control (for permissions)
- SPEC-SHARED-001: Payment Gateway (from shared repo)
```

### 14.2 Complete Tasks.md with All Features

```markdown
# SPEC-021 Implementation Tasks

**Spec:** SPEC-021: Financial Service v1.0.0
**Total Tasks:** 40
**Total Phases:** 4
**Estimated Time:** 82 hours
**Data Sources:** Context7, GitHub (company/shared-specs)

---

## Phase 1: Database & Models (T001-T010)

**Objective:** Set up database schema and models
**Prerequisites:** None
**Estimated Time:** 20 hours
**Risk Level:** LOW
**Context7 Patterns:** Prisma best practices verified

### Tasks

**T001: Setup Prisma Configuration** (~1.5 hours)

**Description:**
Initialize Prisma ORM with PostgreSQL based on Context7 
best practices for connection pooling and error handling.

**Files:**
- CREATE: `prisma/schema.prisma` (~50 lines - SMALL)
  - Database configuration
  - Connection pool settings (Context7 recommended)
  - Basic model definitions

**Dependencies:** None

**Acceptance Criteria:**
- [ ] Prisma configured per Context7 guidelines
- [ ] Connection pooling: min=2, max=10
- [ ] Database connection successful
- [ ] `prisma generate` runs without errors

**Validation:**
- Run: `npx prisma validate`
- Run: `npx prisma generate`
- Verify: Connection pool settings

**Context7 Reference:** Prisma connection pooling best practices

---

[... T002-T010 continue ...]

---

## ⚡ CHECKPOINT: Phase 1 Complete

**Validation Required:**
- [ ] All 10 tasks completed
- [ ] TypeScript compilation passes
- [ ] Prisma schema valid
- [ ] All tests passing
- [ ] Context7 patterns followed

**Context7 Verification:**
- [ ] Prisma patterns match recommendations
- [ ] Connection pooling configured correctly

**Continue to:** Phase 2 (Core Services)

---

[... Phases 2-4 continue ...]
```

### 14.3 Complete Kilo Prompt with All Features

```markdown
# Kilo Code Implementation: SPEC-021 Financial Service

**Version:** 1.0.0
**Generated:** 2025-12-03
**Source Spec:** SPEC-021 v1.0.0
**Total Phases:** 4
**Total Tasks:** 40
**Estimated Time:** 82 hours

**Data Sources:**
- Fastify patterns: Context7
- Prisma patterns: Context7
- Shared patterns: GitHub (company/shared-specs)

---

## 🚨 CRITICAL EXECUTION CONSTRAINTS

**HARD LIMITS (NEVER VIOLATE):**
- ❌ Maximum 10 tasks per execution cycle
- ❌ Maximum 5 file edits per task
- ❌ Maximum 50 lines per str_replace
- ❌ Maximum 2 retry attempts per operation
- ❌ Stop at 3 consecutive errors

**FILE EDIT STRATEGY:**
- Files < 200 lines: Any method OK
- Files 200-500 lines: str_replace only
- Files > 500 lines: Surgical str_replace (50 lines max)

**CONTEXT7 PATTERNS:**
- Follow Context7 recommendations when specified
- If Context7 pattern unclear, ask before implementing
- Document which patterns come from Context7

[... continue with detailed phases ...]
```

---

**END OF KNOWLEDGE BASE v3.5.0**

**Total Size:** ~65 KB (expanded from 35 KB)
**Sections:** 14 major sections
**New Features:** 4 major integrations
**Compatibility:** Backward compatible with v3.3.2
**Status:** Production Ready

---

## 10. CONDITIONAL SECTIONS (NEW v4.0)

### 10.1 Performance Requirements Section

**When to Include:**

Performance Requirements section is **MANDATORY** for:

✅ **Financial/Payment Systems:**
- Credit systems, billing, ledger, payment processing
- Any system handling money transactions
- Systems with financial data integrity requirements

✅ **High-Load Systems:**
- Platform core / central backend services
- APIs handling flash sales, events, high traffic
- Systems with queue/worker as core architecture

✅ **Critical Path Services:**
- Authentication, authorization, rate limiting
- Audit logging, central ledger
- Any service that affects all other services

**Detection Criteria:**

Include Performance Requirements if SPEC mentions:
- Keywords: "credit", "payment", "billing", "ledger", "financial", "money", "transaction"
- Architecture: "saga", "queue", "worker", "orchestrator", "high throughput"
- Scale: "TPS", "concurrent", "load", "peak traffic"
- Critical: "SLA", "uptime", "availability", "real-time"

**Do NOT Include for:**

❌ Internal tools with low traffic (< 20 TPS)
❌ Admin systems with few users
❌ Non-critical batch jobs
❌ Libraries / utility packages
❌ UI/UX design specs
❌ Data contracts / schema specs

**Performance Requirements Template:**

```markdown
## Performance Requirements

### Latency Targets
- **P50**: < 150 ms
- **P90**: < 250 ms  
- **P95**: < 300 ms
- **P99**: < 600 ms

### Throughput Capacity
**Normal Load:**
- 50-200 TPS sustained

**Peak Load:**
- [Define peak scenarios]
- [Expected TPS during peak]

### Availability & SLA
- **Uptime**: 99.9% monthly
- **RTO**: ≤ 5 minutes
- **RPO**: 0 (no data loss acceptable)

### Database Performance
- Write latency: < 10 ms
- Read latency: < 5 ms
- Transaction isolation: SERIALIZABLE or optimistic locking

### Queue & Worker (if applicable)
- Queue delay P99: < 500 ms
- Max retries: 3
- DLQ threshold: < 1%

### Metrics & Alerting
**Required Metrics:**
- `api_latency_p50`, `api_latency_p95`, `api_latency_p99`
- `throughput_tps`
- `error_rate`
- `queue_delay_p99` (if applicable)

**Critical Alerts:**
- P99 latency > threshold for 5 minutes
- Error rate > 1%
- Queue delay > 1 second
```

---

### 10.2 Dependency Injection Pattern Section

**When to Include:**

DI Pattern section is **MANDATORY** for:

✅ **All Backend Services:**
- Any service with business logic
- API services
- Background workers
- Microservices

✅ **Services with Dependencies:**
- Database connections
- External API clients
- Caching services
- Logging services

**Detection Criteria:**

Include DI Pattern if SPEC is:
- Backend service (Node.js/Python/Java backend)
- Has database operations
- Has external integrations
- Needs testing with mocks

**Do NOT Include for:**

❌ Frontend-only applications
❌ Static websites
❌ Pure data schemas
❌ UI/UX designs
❌ Infrastructure specs (unless they define services)

**DI Pattern Template (Concise Version for SPEC):**

```markdown
## Dependency Injection Pattern (MANDATORY)

**Pattern Compliance:** This service **MUST** implement the Dependency Injection (DI) Pattern.

### Requirements

1. **Constructor-Based Injection**
   - All dependencies via constructor parameters
   - All parameters optional with sensible defaults
   - Support production and testing modes

2. **Interface-Based Dependencies**
   ```typescript
   export class ServiceName {
     constructor(
       database?: IDatabase,
       logger?: ILogger,
       cache?: ICache,
       config?: ServiceConfig
     ) {
       this.database = database || createDatabaseConnection();
       this.logger = logger || initializeLogger();
       this.cache = cache || createCacheConnection();
       this.config = config || loadConfigFromEnv();
     }
   }
   ```

3. **Testing Requirements**
   - Inject mock dependencies via constructor
   - No `jest.mock()` for service dependencies
   - Target coverage: ≥ 95%

### Benefits
- ✅ 100% test coverage achievable
- ✅ 60% maintenance reduction
- ✅ 83% debug time reduction  
- ✅ Microservices ready

### Example Test
```typescript
describe('ServiceName', () => {
  let service: ServiceName;
  let mockDatabase: jest.Mocked<IDatabase>;
  
  beforeEach(() => {
    mockDatabase = { query: jest.fn(), execute: jest.fn() };
    service = new ServiceName(mockDatabase);
  });
  
  it('should use injected dependencies', async () => {
    await service.operation();
    expect(mockDatabase.query).toHaveBeenCalled();
  });
});
```

**Reference:** See [DEPENDENCY-INJECTION-PATTERN.md] for full standard.
```

---

### 10.3 Auto-Detection Rules for Workflows

**For generate_spec workflow:**

When creating/updating SPEC:

1. **Analyze SPEC content** for keywords and patterns
2. **Determine if Performance Requirements needed:**
   ```
   IF (
     mentions: credit|payment|billing|ledger|financial|money|transaction
     OR mentions: saga|queue|orchestrator|worker
     OR mentions: TPS|throughput|load|peak|concurrent
     OR mentions: SLA|uptime|critical|real-time
   ) THEN include Performance Requirements
   ```

3. **Determine if DI Pattern needed:**
   ```
   IF (
     is backend service (Node.js/Python/Java/Go)
     AND has database operations
     OR has external integrations
     OR is microservice
   ) THEN include DI Pattern section
   ```

4. **Insert sections in appropriate locations:**
   - Performance Requirements: After "Implementation Guide", before "Examples"
   - DI Pattern: After "Technology Stack", before "Architecture"

---

### 10.4 Examples

**Example 1: Financial System SPEC**
```
Keywords detected: "credit", "payment", "ledger"
Architecture: Saga orchestration, queue workers
→ Include: Performance Requirements ✅
→ Include: DI Pattern ✅
```

**Example 2: Internal Admin Tool**
```
Purpose: Admin dashboard for 5 users
Load: < 10 TPS
→ Include: Performance Requirements ❌
→ Include: DI Pattern ✅ (still a backend service)
```

**Example 3: UI Component Library**
```
Type: Frontend React components
No backend logic
→ Include: Performance Requirements ❌
→ Include: DI Pattern ❌
```

---

### 10.5 Content Customization

**Performance Requirements customization:**
- Adjust latency targets based on system criticality
- Define peak scenarios based on business requirements
- Set appropriate SLA based on service tier
- Include queue metrics only if queues are used

**DI Pattern customization:**
- List actual dependencies for the service
- Use appropriate language syntax (TypeScript/Python/Java)
- Include service-specific examples
- Reference actual interface names from project

---

