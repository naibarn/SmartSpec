---
description: Generate a SmartSpec v5.0 compliant tasks.md from a SPEC file with auto-detection of supporting files (including Prisma schema), auto-generation of supplementary documents, Prisma ↔ OpenAPI consistency validation, and full integration with the SmartSpec ecosystem. Supports custom SPEC_INDEX and dry-run mode.
handoffs:
  - label: Validate Tasks
    agent: smartspec.analyze
    prompt: Validate the generated tasks.md for correctness, dependencies, and safety compliance.
    send: true
  - label: Prepare Kilo Prompt
    agent: smartspec.kilo
    prompt: Generate the Kilo Code implementation prompt for this tasks.md
    send: true
version: 5.0.1
changelog: |
  v5.0.1 (2024-12-06) - Hotfix: SPEC_INDEX Path Detection
  - 🐛 Fixed: SPEC_INDEX detection now checks project root first
  - ✅ Added: Multi-path auto-detection (5 locations)
  - ✅ Fixed: Smart directory creation (only if needed)
  - ✅ Added: User choice for SPEC_INDEX location
  - ✅ Improved: Better logging and error messages
  - Priority order: root → .smartspec/ → specs/ → alternatives
  - No breaking changes - fully backward compatible
  
  v5.0 (2024-12-06) - Prisma Schema Consistency
  - ✅ Added Prisma schema auto-detection (highest priority)
  - ✅ Added Prisma parser (Section 3.1.5) to extract models and fields
  - ✅ Enhanced openapi.yaml generation to use Prisma field names
  - ✅ Added Prisma → OpenAPI type mapping
  - ✅ Added schema consistency validation (Section 8.2.5)
  - ✅ Added schema validation task template (Section 7.2.6)
  - ✅ Added field name registry for canonical references
  - ✅ Prevented field name transformations (creditAmount → credits)
  - ✅ Added x-prisma-model metadata to OpenAPI schemas
  - ✅ Added automated validation scripts
  
  v4.0 (Previous)
  - Auto-detection of supporting files
  - Auto-generation of missing documentation
  - SPEC_INDEX integration
  - Dry-run mode support
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
- If not found, proceed to auto-detection (Step 1.1)

**Step 1.1: Auto-detect SPEC_INDEX.json (if --specindex not provided)**

Try to find SPEC_INDEX.json in these locations (in order):

```bash
# Priority order for SPEC_INDEX detection:
POSSIBLE_PATHS=(
  "SPEC_INDEX.json"                    # 1. Project root (HIGHEST PRIORITY)
  ".smartspec/SPEC_INDEX.json"         # 2. .smartspec directory
  "specs/SPEC_INDEX.json"              # 3. specs directory
  ".smartspec/spec-index.json"         # 4. Alternative name
  "spec-index.json"                    # 5. Alternative name in root
)

SPEC_INDEX_PATH=""
for path in "${POSSIBLE_PATHS[@]}"; do
  if [ -f "$path" ]; then
    SPEC_INDEX_PATH="$path"
    echo "✅ Found SPEC_INDEX at: $path"
    break
  fi
done
```

**If found:**
- Use detected path
- Log: `"📄 Using SPEC_INDEX: ${SPEC_INDEX_PATH}"`
- Continue to Step 3

**If not found:**
- Check `.smartspec/Knowledge-Base.md` or `.smartspec/system_prompt.md` for default path
- If specified in knowledge base, use that path
- Otherwise, use default: `SPEC_INDEX_PATH = "SPEC_INDEX.json"` (project root)
- Continue to Step 2

**Step 2: Handle missing SPEC_INDEX (Enhanced with Smart Creation)**

If `SPEC_INDEX_PATH` doesn't exist:

```
1. ⚠️ WARNING: "SPEC_INDEX.json not found"
   
2. 📍 Searched in:
   - SPEC_INDEX.json (project root)
   - .smartspec/SPEC_INDEX.json
   - specs/SPEC_INDEX.json
   - Other alternative paths
   
3. ❓ Ask user: "Where should I create SPEC_INDEX.json?"
   Options:
   [1] SPEC_INDEX.json (project root) - RECOMMENDED
   [2] .smartspec/SPEC_INDEX.json
   [3] Custom path
   [n] Skip (continue without SPEC_INDEX)

4. Based on user choice:

   Option 1 or 2:
   a. Set SPEC_INDEX_PATH to chosen location
   
   b. Create parent directory ONLY if needed:
      # Check if directory exists
      PARENT_DIR=$(dirname ${SPEC_INDEX_PATH})
      if [ "$PARENT_DIR" != "." ] && [ ! -d "$PARENT_DIR" ]; then
        echo "📁 Creating directory: $PARENT_DIR"
        mkdir -p "$PARENT_DIR"
      else
        echo "✅ Directory already exists: $PARENT_DIR (no need to create)"
      fi
   
   c. Create SPEC_INDEX.json with initial structure:
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
   
   d. Add current spec to INDEX:
      - Extract spec ID, title, path from SPEC file
      - Add as first entry
      - Update metadata
   
   e. Save SPEC_INDEX.json
   
   f. Log: "✅ Created SPEC_INDEX at: ${SPEC_INDEX_PATH}"
   
   g. Continue with tasks generation
   
   Option 3 (Custom path):
   a. Prompt: "Enter custom path (e.g., custom/spec-index.json):"
   b. Validate path is not empty
   c. Set SPEC_INDEX_PATH = custom path
   d. Follow steps b-g from Option 1
   
   Option n (Skip):
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

1. **Prisma Schema (CRITICAL - HIGHEST PRIORITY):**
   - `schema.prisma`
   - `prisma/schema.prisma`
   - `prisma/*.prisma`
   - `database/schema.prisma`
   - `models/schema.prisma`
   
   **Priority Note:**
   - Prisma schema is the SOURCE OF TRUTH for data models
   - If found, it takes precedence over data-model.md
   - All API specs must use field names from Prisma

2. **API Specifications:**
   - `api-spec.yaml` / `api-spec.json`
   - `openapi.yaml` / `openapi.json`
   - `swagger.yaml` / `swagger.json`
   - `contracts/*.yaml` / `contracts/*.json`

3. **Data Models:**
   - `data-model.md` / `data-models.md`
   - `schema.md` / `schemas.md`
   - `models/*.ts` / `models/*.json`
   - `types/*.ts`
   
   **Note:** If Prisma schema exists, data-model.md is secondary

4. **Research & Documentation:**
   - `research.md` / `research/*.md`
   - `analysis.md`
   - `requirements.md`
   - `design.md`

5. **Implementation Guides:**
   - `README.md` (implementation-specific)
   - `IMPLEMENTATION.md`
   - `SETUP.md`

6. **Test Specifications:**
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
  prisma_schema: null,      // NEW: Highest priority
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

## 3.1.5 Parse Prisma Schema (NEW - CRITICAL)

**This section is MANDATORY if Prisma schema is detected.**

**If Prisma schema detected in Step 1:**

### Step 1: Read Prisma Schema

```bash
# Find and read Prisma schema
PRISMA_PATH=$(find . -name "schema.prisma" -type f | head -1)
cat "$PRISMA_PATH"
```

### Step 2: Parse Models and Fields

Extract all models with their fields, types, and modifiers:

```javascript
// Example structure to build in memory
PRISMA_MODELS = {
  "User": {
    fields: [
      { 
        name: "id", 
        type: "String", 
        modifiers: ["@id", "@default(cuid())"],
        isOptional: false,
        isArray: false
      },
      { 
        name: "email", 
        type: "String", 
        modifiers: ["@unique"],
        isOptional: false,
        isArray: false
      },
      { 
        name: "creditBalance", 
        type: "Float", 
        modifiers: ["@default(0)"],
        isOptional: false,
        isArray: false
      }
    ],
    relations: [
      { field: "transactions", model: "Transaction", type: "one-to-many" }
    ]
  },
  "Transaction": {
    fields: [
      { name: "id", type: "String", modifiers: ["@id", "@default(cuid())"] },
      { name: "userId", type: "String", modifiers: [] },
      { name: "amount", type: "Float", modifiers: [] },
      { name: "type", type: "String", modifiers: [] },
      { name: "status", type: "String", modifiers: [] },
      { name: "idempotencyKey", type: "String", modifiers: ["@unique"] },
      { name: "metadata", type: "Json", modifiers: [], isOptional: true }
    ],
    relations: [
      { field: "user", model: "User", type: "many-to-one" }
    ]
  },
  "PromoCode": {
    fields: [
      { name: "id", type: "String", modifiers: ["@id", "@default(cuid())"] },
      { name: "code", type: "String", modifiers: ["@unique"] },
      { name: "creditAmount", type: "Float", modifiers: [] },
      { name: "usageLimit", type: "Int", modifiers: [] },
      { name: "usedCount", type: "Int", modifiers: ["@default(0)"] }
    ],
    relations: []
  }
}
```

### Step 3: Create Field Name Registry

Build canonical field name mapping:

```javascript
FIELD_NAME_REGISTRY = {
  "User": {
    canonical_fields: ["id", "email", "creditBalance", "createdAt"],
    type_mapping: {
      "id": { prisma: "String", openapi: "string", format: "uuid" },
      "email": { prisma: "String", openapi: "string", format: "email" },
      "creditBalance": { prisma: "Float", openapi: "number", format: "float" }
    }
  },
  "PromoCode": {
    canonical_fields: ["id", "code", "creditAmount", "usageLimit", "usedCount"],
    type_mapping: {
      "creditAmount": { prisma: "Float", openapi: "number", format: "float" },
      "usageLimit": { prisma: "Int", openapi: "integer", format: "int32" },
      "usedCount": { prisma: "Int", openapi: "integer", format: "int32" }
    }
  }
}
```

### Step 4: Prisma Type → OpenAPI Type Mapping

**Standard Type Mappings:**

| Prisma Type | OpenAPI Type | Format | Notes |
|-------------|--------------|--------|-------|
| String      | string       | -      | Default string |
| Int         | integer      | int32  | 32-bit integer |
| BigInt      | integer      | int64  | 64-bit integer |
| Float       | number       | float  | Single precision |
| Decimal     | number       | double | Double precision |
| Boolean     | boolean      | -      | True/false |
| DateTime    | string       | date-time | ISO 8601 |
| Json        | object       | -      | JSON object |
| Bytes       | string       | binary | Binary data |

### Step 5: Validate Against SPEC

Check for inconsistencies:

```bash
# Check if SPEC mentions different field names
if SPEC contains "credits" but Prisma has "creditAmount":
  ⚠️ WARNING: "SPEC uses 'credits' but Prisma schema uses 'creditAmount'"
  ⚠️ "Generated tasks will use Prisma field name: 'creditAmount'"
  ⚠️ "Consider updating SPEC for consistency"
```

### Step 6: Store Prisma Context

```javascript
PRISMA_CONTEXT = {
  schema_path: "[path to schema.prisma]",
  models: PRISMA_MODELS,
  field_registry: FIELD_NAME_REGISTRY,
  is_source_of_truth: true,
  use_for_api_generation: true
}
```

**Critical Rules:**
- ✅ Prisma field names are CANONICAL - must be used exactly in API specs
- ✅ No field name transformations allowed (creditAmount → credits) ❌
- ✅ All generated schemas must reference Prisma as source
- ✅ Any conflicts → Prisma wins

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
**Author:** SmartSpec Architect v5.0

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
**Author:** SmartSpec Architect v5.0

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

### 3.3.3 Generate openapi.yaml (ENHANCED WITH PRISMA SYNC)

**CRITICAL RULE: Field Name Consistency**

**🚨 MANDATORY: Source Priority for Field Names**
1. **If Prisma schema exists** → Use Prisma field names (SOURCE OF TRUTH)
2. **If data-model.md exists** → Use data-model field names
3. **If only SPEC exists** → Derive from SPEC descriptions

**Prisma Type → OpenAPI Type Mapping:**
```yaml
# Use mappings from Section 3.1.5
String → { type: "string" }
Int → { type: "integer", format: "int32" }
BigInt → { type: "integer", format: "int64" }
Float → { type: "number", format: "float" }
Decimal → { type: "number", format: "double" }
Boolean → { type: "boolean" }
DateTime → { type: "string", format: "date-time" }
Json → { type: "object" }
Bytes → { type: "string", format: "binary" }
```

**If SPEC defines REST API:**

```yaml
# Auto-generated OpenAPI Specification
# Source: [SPEC-ID]
# Prisma Schema: [path to schema.prisma] (if exists)
# Generated: YYYY-MM-DD
# Author: SmartSpec Architect v5.0

openapi: 3.0.0
info:
  title: [API Title from SPEC]
  version: [Version from SPEC]
  description: |
    [Description from SPEC]
    
    ⚠️ IMPORTANT: Field Name Consistency
    This API uses field names directly from the Prisma schema.
    Database fields = API request/response fields (no transformation).
    
    Source: [path to schema.prisma]

servers:
  - url: http://localhost:3000
    description: Development server
  - url: https://staging.example.com
    description: Staging server
  - url: https://api.example.com
    description: Production server

paths:
  # Generate paths based on SPEC API descriptions
  
  /api/v1/promo-codes:
    post:
      summary: Create promo code
      description: Create a new promotional code for credit distribution
      tags:
        - Promo Codes
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PromoCodeCreate'
      responses:
        '201':
          description: Promo code created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PromoCode'
        '400':
          description: Invalid request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '409':
          description: Promo code already exists
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
    
    get:
      summary: List promo codes
      description: Retrieve list of all promo codes
      tags:
        - Promo Codes
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
      responses:
        '200':
          description: List of promo codes
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/PromoCode'
                  total:
                    type: integer
                  limit:
                    type: integer
                  offset:
                    type: integer
  
  /api/v1/promo-codes/{code}/redeem:
    post:
      summary: Redeem promo code
      description: Apply promo code to user account
      tags:
        - Promo Codes
      parameters:
        - name: code
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - userId
              properties:
                userId:
                  type: string
      responses:
        '200':
          description: Promo code redeemed successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                  creditAmount:
                    type: number
                  newBalance:
                    type: number
        '404':
          description: Promo code not found
        '410':
          description: Promo code expired or usage limit reached

components:
  schemas:
    # 🚨 CRITICAL: Use exact field names from Prisma schema
    # NO transformations allowed (e.g., creditAmount → credits)
    
    PromoCode:
      type: object
      required:
        - code
        - creditAmount      # ✅ From Prisma (NOT "credits")
        - usageLimit        # ✅ From Prisma (NOT "maxUses")
      properties:
        id:
          type: string
          format: uuid
          description: Unique identifier (from Prisma @id @default(cuid()))
          readOnly: true
        code:
          type: string
          description: Unique promo code
          example: "SAVE20"
        creditAmount:       # ✅ EXACT match from Prisma
          type: number
          format: float
          minimum: 0
          description: Credit amount to grant (from Prisma Float)
          example: 100.50
        usageLimit:         # ✅ EXACT match from Prisma
          type: integer
          format: int32
          minimum: 1
          description: Maximum number of redemptions (from Prisma Int)
          example: 100
        usedCount:
          type: integer
          format: int32
          minimum: 0
          default: 0
          description: Current redemption count (from Prisma Int @default(0))
          readOnly: true
        expiresAt:
          type: string
          format: date-time
          nullable: true
          description: Expiration timestamp (from Prisma DateTime?)
          example: "2024-12-31T23:59:59Z"
        createdAt:
          type: string
          format: date-time
          description: Creation timestamp
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          description: Last update timestamp
          readOnly: true
      
      # Metadata for traceability
      x-prisma-model: PromoCode
      x-prisma-source: prisma/schema.prisma
      x-field-mapping: canonical (no transformation)
    
    PromoCodeCreate:
      type: object
      required:
        - code
        - creditAmount
        - usageLimit
      properties:
        code:
          type: string
          minLength: 3
          maxLength: 50
        creditAmount:       # ✅ Same as Prisma
          type: number
          format: float
          minimum: 0
        usageLimit:         # ✅ Same as Prisma
          type: integer
          format: int32
          minimum: 1
        expiresAt:
          type: string
          format: date-time
          nullable: true
      x-prisma-model: PromoCode
      x-operation: create
    
    User:
      type: object
      required:
        - email
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        email:
          type: string
          format: email
        creditBalance:      # ✅ From Prisma (NOT "balance" or "credits")
          type: number
          format: float
          default: 0
          readOnly: true
        createdAt:
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true
      x-prisma-model: User
      x-prisma-source: prisma/schema.prisma
    
    Transaction:
      type: object
      required:
        - userId
        - amount
        - type
        - status
        - idempotencyKey
      properties:
        id:
          type: string
          readOnly: true
        userId:
          type: string
        amount:
          type: number
          format: float
        type:
          type: string
          enum: [credit, debit]
        status:
          type: string
          enum: [pending, completed, failed, cancelled]
        idempotencyKey:     # ✅ From Prisma (NOT "idempotency_key")
          type: string
        metadata:
          type: object
          nullable: true
        createdAt:
          type: string
          format: date-time
          readOnly: true
      x-prisma-model: Transaction
      x-prisma-source: prisma/schema.prisma
    
    Error:
      type: object
      required:
        - error
        - message
      properties:
        error:
          type: string
          description: Error code
        message:
          type: string
          description: Human-readable error message
        details:
          type: object
          description: Additional error details
          nullable: true
  
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token from authentication endpoint

security:
  - bearerAuth: []

# VALIDATION NOTES:
# 1. All field names match Prisma schema exactly
# 2. All types mapped according to Prisma → OpenAPI rules
# 3. No camelCase ↔ snake_case transformations
# 4. Review and validate during implementation
# 5. Use validation script: npm run validate:schemas
```

**Post-Generation Validation:**
```bash
# Check field name consistency
echo "Validating field names against Prisma schema..."

# Extract field names from Prisma
grep -A 20 "model PromoCode" prisma/schema.prisma | \
  grep "^\s\+\w\+" | \
  awk '{print $1}' | sort > /tmp/prisma-fields.txt

# Extract field names from OpenAPI
grep -A 30 "PromoCode:" openapi.yaml | \
  grep "^\s\+[a-z]" | \
  awk '{print $1}' | sed 's/://g' | sort > /tmp/openapi-fields.txt

# Compare
diff /tmp/prisma-fields.txt /tmp/openapi-fields.txt && \
  echo "✅ Field names match exactly" || \
  echo "❌ CRITICAL: Field name mismatch detected - FIX IMMEDIATELY"
```

**Critical Reminders:**
- ✅ **Always use Prisma field names** - they are canonical
- ✅ **No transformations** - creditAmount stays creditAmount
- ✅ **Add x-prisma-model metadata** - for traceability
- ✅ **Validate after generation** - use diff checks above
- ✅ **Document source** - reference schema.prisma in spec

### 3.3.4 Generate test-plan.md

**If SPEC has comprehensive testing requirements:**

```markdown
# Test Plan - [Project Name]

**Generated:** YYYY-MM-DD
**Source:** [SPEC-ID]
**Author:** SmartSpec Architect v5.0

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
**Author:** SmartSpec Architect v5.0
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

### 7.2.6 Schema Synchronization Tasks (NEW - CRITICAL)

**For projects with Prisma + API (openapi.yaml):**

**MANDATORY: Add schema validation task to ensure Prisma ↔ OpenAPI consistency**

**Task Template:**

```markdown
- [ ] **T0XX: Validate Schema Consistency** (2h)

  **Description:**
  Ensure Prisma schema and OpenAPI spec use identical field names.
  Prevent runtime errors from field name mismatches between database and API.
  This validation must pass before any API implementation begins.
  
  **Subtasks:**
  - [ ] T0XX.1: Create schema validation script (1.5h)
    - Description: Build TypeScript/Node.js script to parse and compare schemas
    - Files: `scripts/validate-schemas.ts`
  - [ ] T0XX.2: Integrate into CI/CD pipeline (0.5h)
    - Description: Add validation step to GitHub Actions / CI workflow
    - Files: `.github/workflows/ci.yml` or equivalent
  
  **Files:**
  
  **CREATE: `scripts/validate-schemas.ts`** (~300 lines - MEDIUM)
  - Parse Prisma schema file (prisma/schema.prisma)
  - Extract all models with fields, types, modifiers
  - Parse OpenAPI spec (openapi.yaml or openapi.json)
  - Extract all component schemas with properties
  - Compare field names for exact matches
  - Compare type mappings (Prisma type → OpenAPI type)
  - Generate detailed error report for mismatches
  - Exit with error code if inconsistencies found
  - Strategy: Iterative build (parser → comparator → reporter)
  
  **EDIT: `package.json`** (add 1-2 lines - SMALL)
  - Location: "scripts" section
  - Changes: Add "validate:schemas": "ts-node scripts/validate-schemas.ts"
  - Strategy: Simple addition
  
  **EDIT: `.github/workflows/ci.yml`** (add 3-5 lines - SMALL)
  - Location: After test step
  - Changes: Add schema validation job
  ```yaml
  - name: Validate Schema Consistency
    run: npm run validate:schemas
  ```
  - Strategy: Insert new step
  
  **CREATE: `scripts/README.md`** (~50 lines - SMALL)
  - Document validation script usage
  - Explain Prisma → OpenAPI type mappings
  - Provide troubleshooting guide
  - Strategy: Full creation
  
  **Dependencies:**
  - Prisma schema must exist
  - OpenAPI spec must be generated
  - ts-node and yaml packages installed
  
  **Acceptance Criteria:**
  - [ ] Script successfully parses Prisma schema
  - [ ] Script successfully parses OpenAPI spec (YAML/JSON)
  - [ ] All model names match between Prisma and OpenAPI
  - [ ] All field names match exactly (no transformations)
  - [ ] All type mappings validated correctly
  - [ ] Clear error messages for any mismatches
  - [ ] Script exits with code 0 if consistent, 1 if errors
  - [ ] Script integrated in CI/CD pipeline
  - [ ] CI fails if schemas inconsistent
  - [ ] Documentation complete
  
  **Validation:**
  ```bash
  # Install dependencies
  npm install --save-dev ts-node yaml @types/node
  
  # Run validation
  npm run validate:schemas
  
  # Expected output if consistent:
  # 🔍 Validating schema consistency...
  # 📋 Checking User...
  # 📋 Checking PromoCode...
  # 📋 Checking Transaction...
  # ✅ All schemas are consistent!
  
  # Test CI integration
  git add .
  git commit -m "test: add schema validation"
  git push  # CI should run validation
  ```
  
  **Expected Outcome:**
  - Automated validation prevents field name mismatches
  - CI catches schema inconsistencies before deployment
  - Developers get clear feedback on schema changes
  - Database and API always use same field names

---
```

**Placement Guidelines:**
- Place this task in **Phase 2** (Database & Models) or **Phase 3** (after both Prisma and OpenAPI are created)
- Must complete BEFORE any API controller/service implementation begins
- Should be one of first tasks after schema/API spec creation

**Example Placement in tasks.md:**
```markdown
## Phase 2: Database Schema & Core Models (T011-T020)

- [ ] T015: Create Prisma Schema (4h)
  [... task details ...]

- [ ] T016: Generate OpenAPI Spec (3h)
  [... task details ...]

- [ ] T017: Validate Schema Consistency (2h)  ← ADD HERE
  [... use template above ...]

- [ ] T018: Create Database Migrations (2h)
  [... task details ...]
```

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

### 8.2.5 Schema Consistency Check (NEW - CRITICAL)

**🚨 MANDATORY if Prisma schema exists:**

This validation ensures that database schema (Prisma) and API schema (OpenAPI) use identical field names to prevent runtime errors.

**Pre-Generation Validation:**

Before finalizing tasks.md, verify:

```bash
# Step 1: Verify Prisma schema exists
if [ -f "prisma/schema.prisma" ]; then
  echo "✅ Prisma schema found"
else
  echo "⏭️ No Prisma schema - skipping validation"
  exit 0
fi

# Step 2: Verify OpenAPI spec exists or will be generated
if [ -f "openapi.yaml" ] || [ -f "openapi.json" ] || grep -q "openapi.yaml" tasks.md; then
  echo "✅ OpenAPI spec exists or will be generated"
else
  echo "⚠️ WARNING: No OpenAPI spec - consider adding if API exists"
fi

# Step 3: Extract models from Prisma
echo "📊 Prisma Models:"
grep "^model " prisma/schema.prisma | awk '{print "  -", $2}'

# Step 4: Quick field name check (for generated openapi.yaml)
if [ -f "openapi.yaml" ]; then
  echo "📊 OpenAPI Schemas:"
  grep "^\s\+[A-Z].*:" openapi.yaml | sed 's/://g' | awk '{print "  -", $1}'
  
  # Check for common mismatches
  echo ""
  echo "🔍 Checking for common field name issues..."
  
  # Example: creditAmount vs credits
  if grep -q "creditAmount" prisma/schema.prisma && grep -q '"credits"' openapi.yaml; then
    echo "❌ CRITICAL: Found 'creditAmount' in Prisma but 'credits' in OpenAPI"
    echo "   FIX: Use 'creditAmount' in OpenAPI (exact match from Prisma)"
    exit 1
  fi
  
  # Example: usageLimit vs maxUses
  if grep -q "usageLimit" prisma/schema.prisma && grep -q '"maxUses"' openapi.yaml; then
    echo "❌ CRITICAL: Found 'usageLimit' in Prisma but 'maxUses' in OpenAPI"
    echo "   FIX: Use 'usageLimit' in OpenAPI (exact match from Prisma)"
    exit 1
  fi
  
  # Example: idempotencyKey vs idempotency_key
  if grep -q "idempotencyKey" prisma/schema.prisma && grep -q '"idempotency_key"' openapi.yaml; then
    echo "❌ CRITICAL: Found 'idempotencyKey' in Prisma but 'idempotency_key' in OpenAPI"
    echo "   FIX: Use 'idempotencyKey' in OpenAPI (exact match from Prisma)"
    exit 1
  fi
  
  echo "✅ No obvious field name mismatches found"
fi
```

**Comprehensive Validation Checklist:**

When both Prisma schema and OpenAPI spec exist:

- [ ] ✅ All models in Prisma have corresponding schemas in OpenAPI
- [ ] ✅ All field names in OpenAPI match Prisma exactly (case-sensitive)
- [ ] ✅ All Prisma types correctly mapped to OpenAPI types:
  - String → string
  - Int → integer (format: int32)
  - Float → number (format: float)
  - Decimal → number (format: double)
  - Boolean → boolean
  - DateTime → string (format: date-time)
  - Json → object
- [ ] ✅ Required fields match (Prisma fields without ? → OpenAPI required array)
- [ ] ✅ Optional fields match (Prisma fields with ? → OpenAPI nullable or not in required)
- [ ] ✅ Default values documented in OpenAPI descriptions
- [ ] ✅ No field transformations (camelCase → snake_case) ❌
- [ ] ✅ x-prisma-model metadata added to all schemas
- [ ] ✅ x-prisma-source documented in OpenAPI

**Validation Script Check:**

Verify that tasks.md includes schema validation task:

```bash
# Check if validation task exists in tasks.md
if grep -q "Validate Schema Consistency" tasks.md; then
  echo "✅ Schema validation task found in tasks.md"
  
  # Verify it's placed appropriately (after schema creation, before API implementation)
  if grep -B 5 "Validate Schema Consistency" tasks.md | grep -q "Phase [2-3]"; then
    echo "✅ Validation task in correct phase (2 or 3)"
  else
    echo "⚠️ WARNING: Validation task may be in wrong phase"
    echo "   Recommend: Place in Phase 2 or 3, after schema creation"
  fi
else
  echo "❌ CRITICAL: Schema validation task missing from tasks.md"
  echo "   FIX: Add validation task from Section 7.2.6 template"
  echo "   Placement: Phase 2 or 3, after Prisma + OpenAPI creation"
  exit 1
fi
```

**Field Name Validation Table:**

Document all model fields to ensure consistency:

```markdown
## Schema Field Mapping (Auto-Generated)

### PromoCode Model

| Prisma Field    | Type    | OpenAPI Property | Type            | Status |
|-----------------|---------|------------------|-----------------|--------|
| id              | String  | id               | string (uuid)   | ✅     |
| code            | String  | code             | string          | ✅     |
| creditAmount    | Float   | creditAmount     | number (float)  | ✅     |
| usageLimit      | Int     | usageLimit       | integer (int32) | ✅     |
| usedCount       | Int     | usedCount        | integer (int32) | ✅     |
| expiresAt       | DateTime? | expiresAt      | string (date-time) | ✅  |

### User Model

| Prisma Field    | Type    | OpenAPI Property | Type            | Status |
|-----------------|---------|------------------|-----------------|--------|
| id              | String  | id               | string (uuid)   | ✅     |
| email           | String  | email            | string (email)  | ✅     |
| creditBalance   | Float   | creditBalance    | number (float)  | ✅     |
| createdAt       | DateTime | createdAt       | string (date-time) | ✅  |

### Transaction Model

| Prisma Field    | Type    | OpenAPI Property | Type            | Status |
|-----------------|---------|------------------|-----------------|--------|
| id              | String  | id               | string          | ✅     |
| userId          | String  | userId           | string          | ✅     |
| amount          | Float   | amount           | number (float)  | ✅     |
| type            | String  | type             | string (enum)   | ✅     |
| status          | String  | status           | string (enum)   | ✅     |
| idempotencyKey  | String  | idempotencyKey   | string          | ✅     |
| metadata        | Json?   | metadata         | object          | ✅     |

**Legend:**
- ✅ = Field names match exactly
- ❌ = Mismatch detected (MUST FIX)
- ⚠️ = Partial match (review needed)
```

**Automated Validation Commands:**

Add these to tasks.md validation sections:

```bash
# Full schema consistency check
npm run validate:schemas

# Quick field name check (manual)
for model in User PromoCode Transaction; do
  echo "Checking $model..."
  
  # Prisma fields
  awk "/^model $model/,/^}/" prisma/schema.prisma | \
    grep "^\s\+[a-z]" | \
    awk '{print $1}' | sort > /tmp/prisma-$model.txt
  
  # OpenAPI properties
  awk "/$model:/,/x-prisma/" openapi.yaml | \
    grep "^\s\+[a-z]" | \
    awk '{print $1}' | sed 's/://g' | sort > /tmp/openapi-$model.txt
  
  # Compare
  if diff /tmp/prisma-$model.txt /tmp/openapi-$model.txt > /dev/null; then
    echo "  ✅ $model: All fields match"
  else
    echo "  ❌ $model: Field mismatch detected"
    echo "     Differences:"
    diff /tmp/prisma-$model.txt /tmp/openapi-$model.txt
    exit 1
  fi
done

echo ""
echo "✅ All schemas consistent!"
```

**Post-Validation Actions:**

If validation fails:

1. ⚠️ **STOP** - Do not proceed with generation
2. 📋 **Report** inconsistencies to user with clear examples
3. 🔧 **Suggest** corrections:
   ```
   Found: "credits" in OpenAPI
   Should be: "creditAmount" (from Prisma)
   
   Found: "maxUses" in OpenAPI
   Should be: "usageLimit" (from Prisma)
   ```
4. 🔄 **Regenerate** OpenAPI spec with corrected field names
5. ✅ **Re-validate** until all checks pass

**Critical Rules:**
- ✅ Prisma schema is SOURCE OF TRUTH for field names
- ✅ Zero tolerance for field name mismatches
- ✅ Validation MUST pass before tasks.md finalization
- ✅ Include validation in CI/CD pipeline
- ✅ Document all mappings in tasks.md

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

---

# UI Centralization Addendum (Penpot-first)

เอกสารนี้เป็นส่วนเสริมของ **SmartSpec Centralization Contract**  
เพื่อรองรับ **SPEC ประเภท UI** ที่มีข้อกำหนดพิเศษ:

- **UI design source of truth เป็น JSON** (เพื่อใช้กับ Penpot)
- ทีม UI ต้องสามารถแก้ UI ได้ตรงจากไฟล์นี้
- งานของทีม dev ต้องผูกกับ component/logic โดยไม่ทำให้ไฟล์ UI JSON ปน logic

ใช้ addendum นี้วางต่อท้าย contract ในทุก workflow ที่แตะ UI:
- generate-spec
- generate-plan
- generate-tasks
- implement-tasks
- verify-tasks-progress
- generate-tests
- refactor-code
- reverse-to-spec
- reindex-specs
- validate-index
- sync-spec-tasks
- fix-errors
- generate-implement-prompt / generate-cursor-prompt (ในส่วน canonical constraints)

---

## 1) UI File Model

สำหรับ UI spec ให้ถือว่าในโฟลเดอร์ spec มีไฟล์หลัก 2 ชั้น:

1) `spec.md`  
   - narrative, scope, non-goals, UX rules, accessibility, performance targets  
   - อ้างอิงไฟล์ UI JSON เป็น design artifact

2) `ui.json` (หรือชื่อที่ทีมกำหนดใน config)  
   - **Penpot-editable**  
   - เก็บ layout, components mapping, design tokens references  
   - **ห้าม** ใส่ business logic หรือ API behaviour ในไฟล์นี้

> ถ้าทีมต้องการชื่อไฟล์เฉพาะ ให้กำหนดใน config:
```json
{
  "ui_spec": {
    "ui_json_name": "ui.json",
    "component_registry": "ui-component-registry.json"
  }
}
```

---

## 2) Registry เพิ่มเติมสำหรับ UI (แนะนำ)

เพิ่มไฟล์ registry ใหม่แบบ optional:

- `.spec/registry/ui-component-registry.json`

โครงสร้างขั้นต่ำแนะนำ:
```json
{
  "version": "1.0.0",
  "last_updated": "ISO-8601",
  "components": [
    {
      "canonical_name": "UserAvatar",
      "penpot_component_id": "penpot:component:xxx",
      "code_component_path": "src/components/user/UserAvatar.tsx",
      "owned_by_spec": "spec-XXX",
      "aliases": []
    }
  ]
}
```

**กติกา:**
- ชื่อ component ใน tasks/implementation ต้องอ้าง `canonical_name` เป็นค่า default
- ถ้าพบชื่อใหม่:
  - generate-spec / generate-tasks สามารถเพิ่ม entry ใหม่ได้
  - implement / verify ต้องอ่านอย่างเดียว

---

## 3) UI Naming & Separation Rules (MUST)

### 3.1 Separation of Concerns

- `ui.json` = design + structure + bindings
- business logic / data fetching / permissions  
  ต้องอยู่ใน:
  - code components
  - service layer
  - hooks/store
  - หรือ spec.md ในส่วน logic description

### 3.2 Canonical-first

เมื่อ workflow ต้องเสนอชื่อ component:
1) เช็ค `ui-component-registry.json` (ถ้ามี)
2) เช็ค glossary (คำเรียกหน้าจอ/ฟีเจอร์)
3) ถ้ายังไม่มี:
   - เสนอชื่อใหม่แบบ `Proposed`
   - สร้าง task ให้ลงทะเบียน

---

## 4) Workflow-specific Enforcement

### 4.1 generate-spec (UI category)

ต้อง:
- ตรวจ/สร้าง `ui.json` template ขั้นต่ำ (ถ้ายังไม่มี)
- เพิ่ม `ui.json` ลงใน SPEC_INDEX `files` (ถ้าสคีมารองรับ)
- ระบุใน spec.md ว่า:
  - design source-of-truth = ui.json
  - logic อยู่ที่ code layer

### 4.2 generate-tasks

สำหรับ UI spec:
- สร้าง 3 กลุ่มงานแยกกันชัดเจน:

1) **Design tasks (UI team)**
   - ปรับ layout/flow ใน `ui.json` ผ่าน Penpot

2) **Component binding tasks**
   - map Penpot component → code component
   - อัปเดต `ui-component-registry.json` (ถ้าจำเป็น)

3) **Logic tasks (Dev team)**
   - สร้าง/แก้ hooks/services/state
   - ห้ามใส่ logic ใหม่ใน `ui.json`

### 4.3 implement-tasks / refactor-code

- Treat `ui.json` เป็น **design-owned**
- แก้ไขได้เฉพาะเมื่อ tasks ระบุชัดเจน
- ถ้าพบว่า logic ถูกฝังใน ui.json:
  - สร้าง refactor task เพื่อย้าย logic ออก

### 4.4 generate-tests

- อ้าง component canonical names
- สนับสนุนแนวทาง:
  - component tests
  - accessibility checks
  - visual regression (ถ้าทีมใช้)

---

## 5) Index & Validation Rules

### 5.1 SPEC_INDEX

สำหรับ UI spec:
- แนะนำให้มี field เสริมใน entry (ถ้าทีมอนุญาตแบบ additive):
```json
{
  "ui_artifacts": {
    "ui_json_path": "specs/ui/spec-123/ui.json",
    "penpot_project": "optional-string"
  }
}
```

ถ้าไม่เพิ่ม schema:
- ให้ใช้ `files` list แทน

### 5.2 validate-index / global-registry-audit

ต้องตรวจอย่างน้อย:
- UI spec ที่ category=ui ต้องมี `ui.json`
- ชื่อ component ที่ spec/tasks อ้าง ต้องสอดคล้องกับ registry

---

## 6) ผลลัพธ์ที่ต้องการ

- ทีม UI แก้ UI ได้โดยไม่ชนกับ dev logic
- ลดการแตกชื่อ component ซ้ำซ้อน
- UI specs กลายเป็นส่วนหนึ่งของ centralization ไม่ใช่โลกคู่ขนาน
