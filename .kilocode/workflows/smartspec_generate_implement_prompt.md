---
description: Generate comprehensive implementation prompt from tasks.md with platform-specific instructions (Kilo Code/Claude Code/Roo Code), safety constraints, supporting files integration, and flexible validation commands.
---

## User Input
```text
$ARGUMENTS
```

**Patterns:**
- `specs/feature/spec-004/tasks.md`
- `specs/feature/spec-004/tasks.md --phase 1`
- `specs/feature/spec-004/tasks.md --phase 1,2,3`
- `specs/feature/spec-004/tasks.md --phase 1-3`
- `specs/feature/spec-004/tasks.md --tasks T001`
- `specs/feature/spec-004/tasks.md --tasks T001,T002,T003`
- `specs/feature/spec-004/tasks.md --tasks T001-T010`
- `specs/feature/spec-004/tasks.md --kilocode`
- `specs/feature/spec-004/tasks.md --kilocode --nosubtasks`
- `specs/feature/spec-004/tasks.md --claude`
- `specs/feature/spec-004/tasks.md --claude --with-subagents`
- `specs/feature/spec-004/tasks.md --roocode`
- `specs/feature/spec-004/tasks.md --phase 1-2 --tasks T001-T010 --kilocode`
- `specs/feature/spec-004/tasks.md --specindex=".smartspec/SPEC_INDEX.json"`

**Default Behavior:**
- Platform: `--claude` (most popular, if not specified)
- Sub-tasks (Kilo Code): enabled (unless `--nosubtasks` is specified)
- Sub-agents (Claude Code): disabled (unless `--with-subagents` is specified)
- Phase: all phases (if not specified)
- Tasks: all tasks (if not specified)
- SPEC_INDEX: auto-detect `.smartspec/SPEC_INDEX.json` if exists

## 0. Load Context

**Read `.smartspec/` files:**
- If user provides `--specindex="path"`: Load from specified path
- Else: Auto-detect `.smartspec/SPEC_INDEX.json` in project root
- If found: Parse and load into SPEC_REGISTRY
- If not found: Continue without dependency resolution (log warning)

**Parse Arguments:**
- Extract tasks.md path
- Parse `--phase` parameter (single, comma-separated, or range)
- Parse `--tasks` parameter (single, comma-separated, or range)
- Parse platform flag: `--kilocode`, `--claude`, `--roocode`
- Parse `--nosubtasks` flag (only valid with `--kilocode`)
- Parse `--with-subagents` flag (only valid with `--claude`)
- Default platform: `--claude` if none specified
- Validate: If `--nosubtasks` without `--kilocode`, show error
- Validate: If `--with-subagents` without `--claude`, show error
- Validate: Only ONE platform flag allowed (--kilocode, --claude, or --roocode)
- Validate: If --with-subagents, verify `.claude/agents/` folder and all required agent files exist
- Validate: Task range must be valid (e.g., T001-T010)
- Validate: Phase range must be valid (e.g., 1-3)
- Validate: `tasks.md` file must exist and not be empty

## 1. Resolve Paths

Extract tasks.md path from arguments
Set TASKS_DIR = directory of tasks.md
Extract SPEC_ID from path or tasks.md metadata

**Determine output filename:**
- Pattern: `implement-prompt-<spec-id>-<timestamp>.md`
- Example: `implement-prompt-spec-004-20250104-143022.md`
- If file exists: Use timestamped version
- Output location: TASKS_DIR/

## 2. Read & Parse tasks.md

**Parse YAML frontmatter (if exists):**
```yaml
---
spec_id: spec-004-financial-system
version: 1.0.0
technology_stack: TypeScript, Node.js, PostgreSQL
validation_commands:
  compile: "tsc --noEmit"
  test: "npm test -- {test_file}"
  lint: "npm run lint"
  integration: "npm run test:integration"
---
```

**If frontmatter missing:**
- Use default TypeScript validation commands
- Log warning: "No validation_commands in frontmatter, using TypeScript defaults"

**Parse structure:**
- Project metadata
- Phase overview table
- All phases with tasks
- Checkpoints
- Supporting files references

**Extract:**
- Total phases/tasks
- High-risk phases
- Dependencies
- Validation requirements
- Technology stack

**Validate format:**
- [ ] Has Project Metadata section
- [ ] Has Phase Overview table
- [ ] Tasks use checkbox format `- [ ]`
- [ ] Tasks have IDs (T001, T002, ...)
- [ ] Tasks have time estimates (Xh)
- [ ] Files specify size category (SMALL/MEDIUM/LARGE)

**If validation fails:**
- Stop and report parsing errors
- Example: "Cannot parse tasks.md: missing Phase Overview table"
- Request user to fix format

## 3. Filter Scope (Based on Parameters)

**Apply phase filter:**
- If `--phase 1`: Include only Phase 1
- If `--phase 1,2,3`: Include Phases 1, 2, 3
- If `--phase 1-3`: Include Phases 1 through 3
- If no `--phase`: Include all phases

**Apply task filter:**
- If `--tasks T001`: Include only T001
- If `--tasks T001,T002,T003`: Include T001, T002, T003
- If `--tasks T001-T010`: Include T001 through T010
- If no `--tasks`: Include all tasks (within selected phases)

**Validate ranges:**
- Check phase numbers exist in tasks.md
- Check task IDs exist in tasks.md
- If invalid: Stop and report error
- Example: "Invalid range: --phase 1-10 (only 5 phases exist)"

**Result:**
- FILTERED_PHASES: List of phases to include
- FILTERED_TASKS: List of tasks to include
- TOTAL_FILTERED_HOURS: Sum of hours for filtered tasks

## 4. Scan Supporting Files

**Detect in TASKS_DIR and subdirectories:**
- openapi.yaml / api-spec.yaml
- data-model.md
- README.md
- research.md
- test-plan.md
- architecture.md
- security-requirements.md
- performance-requirements.md
- Other relevant files

**Read content for context integration**

**If referenced file not found:**
- Log warning: "Referenced openapi.yaml not found in TASKS_DIR"
- Continue with note in prompt about missing file

## 5. Generate Prompt Header

```markdown
# Implementation Prompt: [Project Name]

**Generated:** YYYY-MM-DD HH:mm:ss
**Author:** SmartSpec Architect v5.0
**Source Tasks:** [Path to tasks.md]
**Source SPEC:** [SPEC-ID] v[X.Y.Z]
**SPEC_INDEX:** [Path used or "Not found"]
**Platform:** [Kilo Code / Claude Code / Roo Code]

---

## Project Overview

**Status:** IMPLEMENTATION
**Total Phases:** X (Filtered: Y phases)
**Total Tasks:** XX (Filtered: YY tasks)
**Estimated Effort:** XX hours (Filtered: YY hours)
**Technology Stack:** [From tasks.md frontmatter or metadata]

**Scope:**
- **Phases:** [List of included phases, e.g., "1, 2, 3" or "All"]
- **Tasks:** [List of included tasks, e.g., "T001-T010" or "All"]
- **Reason:** [User-specified filter or "Full implementation"]

**Supporting Documentation:**
- 📄 SPEC: [Link to spec.md]
- 📋 Tasks: [Link to tasks.md]
- 🔌 API Spec: [Link to openapi.yaml if exists, else "Not found"]
- 📊 Data Model: [Link to data-model.md if exists, else "Not found"]
- 📖 README: [Link to README.md if exists, else "Not found"]
- 🔬 Research: [Link to research.md if exists]
- 🏗️ Architecture: [Link to architecture.md if exists]

**Related Specs:** (Resolved from SPEC_INDEX)
[For each referenced spec:]
- **[spec-id]** (`[path]`, repo: [repo]) - [Title]

[If SPEC_INDEX not found:]
- ⚠️ SPEC_INDEX not found, dependency resolution skipped

---
```

## 6. Platform-Specific Instructions

**Based on detected platform flag:**

### For --kilocode

```markdown
## 🤖 KILO CODE PLATFORM INSTRUCTIONS

**Sub-Task Mode:** {IF --nosubtasks: "Disabled"} {ELSE: "Enabled (Default)"}

### Multi-Mode Architecture

Kilo Code uses **5 specialized modes** with automatic mode switching and LLM optimization.

#### Modes Overview

**1. Architect Mode** - Design & Planning
- **Purpose:** System design, architecture decisions, schema design
- **Auto-selected for:** Tasks with keywords "design", "architecture", "schema", "plan"
- **Optimized LLM:** Architecture reasoning model
- **Best for:**
  - Database schema design (T001: Design database schema)
  - System architecture planning (T005: Plan microservices architecture)
  - API contract definition (T010: Define REST API contracts)
  - Technology stack selection

**2. Code Mode** - Implementation
- **Purpose:** Code generation, file creation/editing, feature implementation
- **Auto-selected for:** Tasks with keywords "create", "implement", "build", "add"
- **Optimized LLM:** Code generation model
- **Best for:**
  - Entity/model creation (T020: Create User entity)
  - Service implementation (T030: Implement auth service)
  - Controller/endpoint creation (T040: Create user endpoints)
  - Utility functions

**3. Debug Mode** - Error Fixing
- **Purpose:** Error analysis, bug fixing, troubleshooting
- **Auto-selected for:** Tasks with keywords "fix", "debug", "resolve", "troubleshoot"
- **Optimized LLM:** Debugging model
- **Best for:**
  - Compilation errors (T025: Fix TypeScript errors)
  - Test failures (T035: Resolve failing tests)
  - Runtime errors (T045: Debug memory leak)
  - Performance issues

**4. Ask Mode** - Clarification
- **Purpose:** Requirement clarification, decision support, Q&A
- **Auto-selected for:** Ambiguous requirements, multiple valid approaches
- **Optimized LLM:** Q&A and reasoning model
- **Best for:**
  - Ambiguous requirements (T015: Clarify auth flow)
  - Multiple options (T025: Choose REST vs GraphQL)
  - Business logic clarification
  - Missing information

**5. Orchestrator Mode** - Task Coordination
- **Purpose:** Subtask breakdown, task coordination, workflow management
- **Auto-activated for:** Tasks >8 hours (automatic)
- **Optimized LLM:** Coordination model
- **Best for:**
  - Large tasks (T050: Implement complete auth system - 12h)
  - Multi-component tasks
  - Complex workflows
  - Integration tasks

### Auto Subtasks Feature (Enhanced with Smart Time Estimation)

{IF --nosubtasks: "**Sub-Tasks are DISABLED for this run.** Execute tasks sequentially as listed without decomposition."}

{ELSE: "**Sub-Tasks are ENABLED (Default).** Use Orchestrator Mode to break down complex tasks."}

**Automatic Breakdown (When Enabled):**
- **Trigger:** Tasks >8h automatically activate Orchestrator Mode
- **Format:** T001.1, T001.2, T001.3, ...
- **Size:** Each subtask 1.5-5h (based on complexity)
- **Time Distribution:** Proportional to component complexity (not equal)
- **Mode Assignment:** Each subtask gets appropriate mode
- **Dependencies:** Tracked automatically

**Smart Time Estimation Algorithm:**

**Step 1: Analyze task complexity**
```
complexity_score = calculate_task_complexity(task)

Factors:
- file_count: number of files to create/edit
- avg_file_size: average lines per file
- risk_level: HIGH=3, MEDIUM=2, LOW=1
- dependency_count: number of dependencies

Formula:
complexity = (file_count * 0.3) + (avg_file_size/100 * 0.2) + 
             (risk_level * 0.3) + (dependency_count * 0.2)

Normalize to 1-10 scale
```

**Step 2: Analyze component complexity**
```
Component type multipliers:
- Model: 1.0 (simple data structures)
- Service: 1.5 (business logic)
- Controller: 1.3 (API handling)
- Middleware: 1.2 (cross-cutting concerns)
- Tests: 0.8 (straightforward testing)
- Integration: 2.0 (external dependencies)

component_complexity = base_score * type_multiplier
```

**Step 3: Distribute time proportionally**
```
total_complexity = sum(all component_complexity)

FOR each component:
  ratio = component_complexity / total_complexity
  component_hours = task.hours * ratio
  
  # Ensure bounds
  component_hours = max(1.5, min(5, component_hours))

# Scale to match total
scale_factor = task.hours / sum(component_hours)
FOR each component:
  component_hours *= scale_factor
```

**Example Breakdown (with Smart Time Estimation):**
```
Original Task:
T050: Implement complete authentication system (12h)

Complexity Analysis:
- User model: complexity 2/10 (simple) → 1.5h
- AuthService: complexity 6/10 (complex logic) → 4h
- AuthController: complexity 4/10 (medium) → 3h
- Auth middleware: complexity 3/10 (medium-low) → 2h
- Tests: complexity 2/10 (simple) → 1.5h

Total: 12h ✅

↓ Orchestrator Mode activates automatically ↓

Subtasks Created:
- [ ] T050.1: Create User model (1.5h) → Code Mode
  Complexity: 2/10 (simple data structure)
  Files: src/models/User.ts
  
- [ ] T050.2: Implement AuthService (4h) → Code Mode
  Complexity: 6/10 (business logic, bcrypt, JWT)
  Files: src/services/AuthService.ts
  Dependencies: T050.1
  
- [ ] T050.3: Create AuthController (3h) → Code Mode
  Complexity: 4/10 (API handling, validation)
  Files: src/controllers/AuthController.ts, src/routes/auth.ts
  Dependencies: T050.2
  
- [ ] T050.4: Add auth middleware (2h) → Code Mode
  Complexity: 3/10 (JWT verification)
  Files: src/middleware/auth.ts
  Dependencies: T050.2
  
- [ ] T050.5: Add auth tests (1.5h) → Code Mode
  Complexity: 2/10 (test coverage)
  Files: tests/auth.test.ts
  Dependencies: T050.2, T050.3, T050.4

Note: Time distributed by complexity (not equal 2-3h each!)
```

**Quality Validation (Phase 5):**

After generating subtasks, run comprehensive validation:

```
validation_result = validate_subtasks(subtasks, original_task)

Checks:
1. Count: 2-8 subtasks (ERROR if < 2, WARNING if > 8)
2. Balance: max/min ratio < 3 (WARNING if ≥ 3)
3. Dependencies: no circular, correct order (ERROR if invalid)
4. Completeness: all files covered (WARNING if missing)
5. Coverage: all components present (WARNING if missing)

IF validation_result.errors:
  SHOW errors and STOP
  
IF validation_result.warnings:
  SHOW warnings and suggestions
  IF auto_fix_available:
    APPLY auto-fixes
    RE-VALIDATE
```

**Validation Examples:**

**Example 1: Valid Breakdown** ✅
```
Subtasks:
- T050.1: User model (1.5h)
- T050.2: AuthService (4h) [depends on T050.1]
- T050.3: AuthController (3h) [depends on T050.2]
- T050.4: Middleware+Tests (3.5h) [depends on T050.2]

Validation:
✅ Count: 4 subtasks (2-8 range)
✅ Balance: max 4h, min 1.5h, ratio 2.67 (< 3)
✅ Dependencies: Valid order, no circular
✅ Completeness: All 5 files covered
✅ Coverage: All components present

Result: ✅ All validations passed!
```

**Example 2: Unbalanced (Auto-fixed)** ⚠️
```
Subtasks (before fix):
- T060.1: Model (1h)
- T060.2: Service (5h)
- T060.3: Controller (3h)
- T060.4: Tests (1h)

Validation:
✅ Count: 4 subtasks
❌ Balance: max 5h, min 1h, ratio 5.0 (> 3) - UNBALANCED
⚠️ Suggestion: Combine T060.1 and T060.4

Auto-fix applied:
- T060.1: Service (5h)
- T060.2: Controller (3h)
- T060.3: Model and Tests (2h) [combined]

Re-validation:
✅ Count: 3 subtasks
✅ Balance: max 5h, min 2h, ratio 2.5 (< 3)

Result: ✅ Fixed and validated!
```

**Example 3: Circular Dependency (Error)** ❌
```
Subtasks:
- T070.1: Component A [depends on T070.3]
- T070.2: Component B [depends on T070.1]
- T070.3: Component C [depends on T070.2]

Validation:
✅ Count: 3 subtasks
✅ Balance: ratio 1.5
❌ Dependencies: Circular dependency detected!
  Cycle: T070.1 → T070.3 → T070.2 → T070.1

Result: ❌ ERROR - Cannot proceed with circular dependencies
Action: Review task dependencies and break the cycle
```

**Benefits:**
- ✅ Prevents context overflow
- ✅ Better progress tracking
- ✅ Easier error recovery
- ✅ Clearer validation points
- ✅ Catches errors early (95%+ detection)
- ✅ Provides actionable suggestions
- ✅ Auto-fixes common issues

### Mode Selection Logic

**Automatic Detection:**
```
IF task.hours > 8:
  → Orchestrator Mode (create subtasks)
ELSE IF task.title matches /design|architecture|schema|plan/i:
  → Architect Mode
ELSE IF task.title matches /fix|debug|resolve|troubleshoot/i:
  → Debug Mode
ELSE IF task.hasAmbiguity OR task.needsDecision:
  → Ask Mode
ELSE:
  → Code Mode (default)
```

**You don't need to specify modes** - they're selected automatically based on:
- Task title keywords
- Task description content
- Task duration (>8h)
- File operations (CREATE/EDIT)
- Error patterns

### LLM Optimization

**Per-Mode LLM Selection:**
- Each mode uses a different LLM optimized for that task type
- Automatic switching between LLMs
- No manual configuration needed
- Cost optimization (cheaper models for simple tasks)
- Speed optimization (faster models when possible)
- Quality optimization (best model for each concern)

### Execution Strategy

**Autonomous Batch Processing:**

1. **Read All Tasks**
   - Parse tasks.md completely
   - Identify task boundaries
   - Note dependencies

2. **Let Orchestrator Work**
   - Tasks >8h: Wait for Orchestrator to create subtasks
   - Don't manually break down large tasks
   - Trust automatic breakdown

3. **Execute Sequentially**
   - Process tasks in order (T001, T002, T003, ...)
   - Respect dependencies
   - Skip if dependency not met

4. **Mode Switching**
   - Automatic mode selection per task
   - Seamless transitions
   - Context preserved across modes

5. **Validate After Each Task**
   - Run validation commands
   - Check compilation
   - Run relevant tests
   - Verify changes

6. **Track Progress**
   - Update checkboxes: `- [ ]` → `- [x]`
   - Log completed tasks
   - Note any failures

### Safety Constraints

**Hard Limits:**
- Maximum 10 tasks per execution cycle
- Maximum 5 file edits per task
- Maximum 50 lines per str_replace
- Stop at 3 consecutive errors

**Validation:**
- Compile after every task
- Test after every task
- Lint after every task
- Retry on failure (max 2 attempts)

### Error Handling

**On Error:**
1. Automatically switch to Debug Mode
2. Analyze error messages
3. Attempt fix (max 2 attempts)
4. If still failing: Stop and report

**On 3 Consecutive Errors:**
- STOP execution immediately
- Create checkpoint
- Report errors with details
- Request manual intervention

### Checkpoints

**Automatic Checkpoints:**
- Every 5 tasks
- At phase boundaries
- On context limit (80% tokens)
- On error threshold

**Checkpoint Contents:**
- Last completed task
- Failed tasks list
- Skipped tasks list
- Validation status
- Files modified
- Next task to execute

### Trust the System

✅ **Let Orchestrator handle large tasks** - Don't manually break down tasks >8h
✅ **Trust automatic mode switching** - Don't specify modes manually
✅ **Trust LLM selection** - System picks optimal LLM per mode
✅ **Focus on clear task descriptions** - Good descriptions enable better mode detection

---
```

### For --claude

```markdown
## 🤖 CLAUDE CODE PLATFORM INSTRUCTIONS

### Sub Agents Architecture

Claude Code uses **user-created sub agents** for specialized expertise and domain separation.

**Note:** Sub-agents are **OPTIONAL**. Only use them when:
- The `--with-subagents` flag is specified
- The project has `.claude/agents/` directory with agent definitions
- You need specialized expertise for complex, multi-domain projects

**If `--with-subagents` is NOT specified:** Skip this section and use standard Claude Code instructions (interactive, single-agent approach).

#### Step 1: Reference Standard Sub-Agent Definitions

**SmartSpec provides standard sub-agent definitions in `.claude/agents/`:**

- **Planner Agent** (`.claude/agents/planner/planner-smart.md`)
  - Reads SmartSpec files and creates execution plans
  - Maps tasks to appropriate agents
  
- **Backend Agent** (`.claude/agents/backend/backend-smart.md`)
  - Implements business logic and services
  - Follows project architecture patterns
  
- **Database Agent** (`.claude/agents/db/db-agent-smart.md`)
  - Handles Prisma schema and migrations
  - Optimizes database performance
  
- **API Agent** (`.claude/agents/api/api-agent-smart.md`)
  - Builds REST/API layer
  - Implements validation and error handling
  
- **Tester Agent** (`.claude/agents/tester/tester-smart.md`)
  - Writes unit, integration, and e2e tests
  - Ensures test coverage
  
- **Security Agent** (`.claude/agents/security/security-finance.md`)
  - Audits for security vulnerabilities
  - Ensures compliance (PCI DSS, GDPR, etc.)

**These agents are already created and ready to use.** You can customize them by editing the `.md` files.

#### Step 2: Agent-Based Execution Workflow (When Using Sub-Agents)

**Recommended Workflow:**

**Step 1: Planning (Planner Agent)**
```text
Use the "planner" agent (`.claude/agents/planner/planner-smart.md`) to:
1. Read the SmartSpec SPEC and Tasks
2. Create a phase-by-phase execution plan
3. Map tasks to appropriate agents (db, backend, api, tester, security)
4. Return a structured checklist
```

**Step 2: Database (DB Agent)**
```text
Use the "db" agent (`.claude/agents/db/db-agent-smart.md`) to:
1. Design and implement Prisma schema
2. Create database migrations
3. Add indexes and constraints
4. Validate schema and migrations
```

**Step 3: Backend (Backend Agent)**
```text
Use the "backend" agent (`.claude/agents/backend/backend-smart.md`) to:
1. Implement business logic and services
2. Create repositories and data access layers
3. Follow project architecture patterns
4. Ensure production-ready code
```

**Step 4: API (API Agent)**
```text
Use the "api" agent (`.claude/agents/api/api-agent-smart.md`) to:
1. Implement HTTP routes and controllers
2. Add request/response validation
3. Implement error handling
4. Connect to backend services
```

**Step 5: Testing (Tester Agent)**
```text
Use the "tester" agent (`.claude/agents/tester/tester-smart.md`) to:
1. Write unit tests for services
2. Write integration tests for APIs
3. Achieve coverage targets
4. Report test results
```

**Step 6: Security Review (Security Agent)**
```text
Use the "security" agent (`.claude/agents/security/security-finance.md`) to:
1. Audit authentication and authorization
2. Check for security vulnerabilities
3. Verify compliance requirements
4. Suggest security improvements
```

**Benefits:**
- ✅ Specialized expertise per domain
- ✅ Clear responsibility boundaries
- ✅ Context isolation
- ✅ Parallel conceptual work

### Deep Analysis Capabilities

**Leverage Best-in-Class Repo-wide Reasoning:**

**Before Starting:**
```
Analyze this entire codebase and identify:
1. All authentication-related code
2. Current security patterns
3. Database access patterns
4. Error handling approaches
5. Testing strategies

Use this analysis to guide implementation and maintain consistency.
```

**Benefits:**
- ✅ Understand existing patterns
- ✅ Maintain consistency
- ✅ Avoid duplication
- ✅ Identify refactoring opportunities

### Interactive Execution

**Execution Style:** INTERACTIVE
- Manual task selection
- User-driven validation
- Flexible checkpoint timing
- More control, requires more oversight

**Mode Control:** MANUAL
- You decide when to switch approaches
- Can pause and resume anytime
- More flexibility in execution order
- User confirms each major decision

### Validation Strategy

**Per-Agent Validation:**
- DB Agent: Schema validation, migration testing
- API Agent: Endpoint testing, contract validation
- Test Agent: Coverage verification, test quality

**Manual Validation:**
1. Run validation commands after each task
2. Check output and decide whether to continue
3. Fix errors before proceeding
4. User confirms validation results

**Validation Commands:**
```bash
# After each task
{validation_commands.compile}
{validation_commands.test}
{validation_commands.lint}
```

### Checkpoint Strategy

**Manual Checkpoints:**
- Create checkpoints at logical points
- Recommended: After each phase
- Can checkpoint anytime for safety
- User decides checkpoint timing

**Checkpoint Contents:**
- Phase completed
- Tasks completed
- Validation status
- Next phase to start

### Interactive Decision Making

**When to Ask User:**
- Ambiguous requirements
- Multiple valid approaches
- Architecture decisions
- Trade-off analysis
- Missing information

**How to Ask:**
```
"I see two approaches for implementing authentication:

Option 1: JWT with refresh tokens
  Pros: Stateless, scalable
  Cons: Token revocation complexity

Option 2: Session-based with Redis
  Pros: Easy revocation, server control
  Cons: Stateful, Redis dependency

Which approach do you prefer?"
```

### Workflow Example

```
1. Read full prompt and analyze codebase
2. Create specialized sub agents (DB, API, Test)
3. Activate DB Agent
4. DB Agent: Execute T001-T015 (database tasks)
5. Validate database phase
6. Checkpoint: Phase 1 complete
7. Activate API Agent
8. API Agent: Execute T016-T030 (API tasks)
9. Validate API phase
10. Checkpoint: Phase 2 complete
11. Activate Test Agent
12. Test Agent: Execute T031-T045 (test tasks)
13. Validate test phase
14. Checkpoint: Phase 3 complete
15. Main Agent: Integration and final validation
16. Report completion
```

### Best Practices

✅ **Create sub agents early** - Setup specialized agents before starting
✅ **Use deep analysis** - Leverage repo-wide reasoning for consistency
✅ **Interactive decisions** - Involve user in key decisions
✅ **Phase-based execution** - Complete one phase before moving to next
✅ **Validate frequently** - Check after each task and phase

---
```

### For --roocode

```markdown
## 🤖 ROO CODE PLATFORM INSTRUCTIONS

### Workflow-Driven Development

Roo Code uses **structured workflow phases** with emphasis on safety and preview.

#### Workflow Phases

**1. Plan Mode** - Task planning and breakdown
**2. Implement Mode** - Code implementation with preview
**3. Review Mode** - Comprehensive diff review
**4. Execute Mode** - Testing and validation
**5. Explain Mode** - Documentation and explanation

### Safety-First Approach

**Key Features:**
- ✅ **Full diff preview** before any changes (best-in-class)
- ✅ **Approval gates** at each phase
- ✅ **Incremental changes** (small, safe edits)
- ✅ **Easy rollback** if issues found
- ✅ **Validation gates** before proceeding

### Workflow Structure

```
For each Phase:
  1. Plan Mode: Break down into steps
  2. Implement Mode: Generate changes
  3. Review Mode: Preview all diffs
  4. User Approval: Review and approve
  5. Apply Changes: Execute approved changes
  6. Execute Mode: Run tests and validate
  7. Confirm or Rollback: Verify success
```

### Phase Execution Template

#### Phase 1: Plan Mode

```markdown
## Phase X: [Phase Name]

### Planning

**Tasks:**
- T001: Design database schema (3h)
- T002: Create entity models (2h)
- T003: Setup Prisma client (1h)

**Steps:**
1. Design schema structure
2. Create Prisma schema file
3. Generate migration files
4. Setup Prisma client

**Files:**
- prisma/schema.prisma (to create)
- docs/database-design.md (to create)

**Dependencies:**
- None (first phase)

**Estimated Duration:** 6 hours
```

#### Phase 2: Implement Mode

```markdown
### Implementation

**Task T001: Design database schema (3h)**

**Files to Create:**
- `prisma/schema.prisma` (~200 lines - MEDIUM)
- `docs/database-design.md` (~100 lines - SMALL)

**Implementation:**
[Generate code here]
```

#### Phase 3: Review Mode

```markdown
### Review

**Preview All Changes:**

```diff
File: prisma/schema.prisma (NEW FILE)

+ generator client {
+   provider = "prisma-client-js"
+ }
+
+ datasource db {
+   provider = "postgresql"
+   url      = env("DATABASE_URL")
+ }
+
+ model User {
+   id        String   @id @default(uuid())
+   email     String   @unique
+   password  String
+   createdAt DateTime @default(now())
+   updatedAt DateTime @updatedAt
+   sessions  Session[]
+ }

File: docs/database-design.md (NEW FILE)

+ # Database Design
+
+ ## User Table
+ - id: UUID primary key
+ - email: Unique email address
+ ...
```

**Review Checklist:**
- [ ] Schema structure correct
- [ ] Relations defined properly
- [ ] Indexes added
- [ ] No syntax errors
- [ ] Documentation complete

**Safety Check:**
- [ ] No breaking changes
- [ ] Backward compatible
- [ ] No security issues
- [ ] Performance acceptable

**[APPROVAL REQUIRED]**
Review complete. Approve changes? (y/n)
```

#### Phase 4: Execute Mode

```markdown
### Execution

**After Approval:**

1. **Apply Changes**
   ```bash
   create prisma/schema.prisma
   create docs/database-design.md
   ```

2. **Validate**
   ```bash
   npx prisma generate
   npx prisma validate
   ```

3. **Test**
   ```bash
   npm test -- schema.test.ts
   ```

**Validation Results:**
```
✅ Prisma client generated successfully
✅ Schema validation passed
✅ Tests passed (3/3)
```

**[CONFIRMATION]**
Changes applied successfully. Proceed to next task? (y/n)
```

#### Phase 5: Rollback (If Needed)

```markdown
### Rollback Procedure

**If Any Validation Fails:**

1. **Identify Failure**
   - Which validation failed
   - Error messages
   - Root cause

2. **Rollback Changes**
   ```bash
   git restore .
   ```

3. **Report Error**
   ```
   ❌ Validation Failed: [validation type]
   
   Error: [error message]
   
   Root Cause: [analysis]
   
   Suggested Fix: [fix description]
   
   Retry: [y/n]
   ```

4. **Fix and Retry**
   - Apply suggested fix
   - Re-run from Implement Mode
   - Preview changes again
```

### Incremental Changes Strategy

**For Large Changes:**

1. **Break into Smaller Steps**
   ```
   Large Task: Implement auth system (12h)
   
   Break into phases:
   - Phase 1: Database (2h)
   - Phase 2: Models (2h)
   - Phase 3: Service (3h)
   - Phase 4: Endpoints (3h)
   - Phase 5: Tests (2h)
   ```

2. **Execute Phase by Phase**
   - Complete Phase 1
   - Validate Phase 1
   - Commit Phase 1
   - Proceed to Phase 2

3. **Validate After Each Phase**
   - Compilation
   - Tests
   - Integration
   - Commit

**Benefits:**
- ✅ Smaller, safer changes
- ✅ Easier to review
- ✅ Easier to rollback
- ✅ Clear progress tracking

### Safety Gates

**Mandatory Gates:**

1. **Before Apply:**
   - Preview all diffs
   - User approval required

2. **After Apply:**
   - Compilation check
   - Test execution
   - Lint check

3. **Before Proceed:**
   - All validations pass
   - User confirmation

**Gate Failure:**
- Automatic rollback
- Error report
- Fix suggestions
- Retry option

### Frontend-Specific Optimizations

**For React/Vue/Angular:**

1. **Component-Based Workflow**
   ```
   Phase 1: Component structure
   Phase 2: Component logic
   Phase 3: Component styles
   Phase 4: Component tests
   ```

2. **Preview in Browser**
   - Start dev server
   - Preview changes live
   - Visual verification

3. **Hot Reload Testing**
   - Make changes
   - Preview immediately
   - Validate visually

**For Node.js:**

1. **Module-Based Workflow**
   ```
   Phase 1: Module structure
   Phase 2: Module logic
   Phase 3: Module tests
   Phase 4: Module integration
   ```

2. **API Testing**
   - Start server
   - Test endpoints
   - Validate responses

### Validation Strategy

**After Each Phase:**
```bash
# Compilation
{validation_commands.compile}

# Tests
{validation_commands.test}

# Linting
{validation_commands.lint}
```

**Validation Checklist:**
- [ ] Compilation passes
- [ ] All tests passing
- [ ] No lint errors
- [ ] No breaking changes

### Checkpoint Strategy

**Checkpoint Timing:**
- After each phase completion
- After validation passes
- Before major changes
- User-requested checkpoints

**Checkpoint Contents:**
- Phase completed
- Files modified
- Validation status
- Next phase to start

### Best Practices

✅ **Preview first** - Always review diffs before applying
✅ **Incremental changes** - Small, safe edits
✅ **Validate frequently** - After each phase
✅ **Easy rollback** - Commit after each phase
✅ **User approval** - Confirm before major changes

---
```

## 7. Critical Execution Constraints

```markdown
## 🚨 CRITICAL EXECUTION CONSTRAINTS

**THESE RULES ARE NON-NEGOTIABLE**

### Hard Limits (NEVER VIOLATE)
- ❌ Maximum 10 tasks per execution cycle
- ❌ Maximum 5 file edits per task
- ❌ Maximum 50 lines per str_replace operation
- ❌ Maximum 2 retry attempts per failed operation
- ❌ STOP at 3 consecutive errors

### File Size Strategy (MANDATORY)

**SMALL Files (< 200 lines):**
- CREATE: Full file generation is safe
- EDIT: Any method OK (str_replace or full rewrite)
- No special handling needed

**MEDIUM Files (200-500 lines):**
- CREATE: Staged creation preferred
- EDIT: **str_replace ONLY** - NO full file rewrites
- Max 50 lines per str_replace

**LARGE Files (> 500 lines):**
- CREATE: Incremental build required
- EDIT: **Surgical str_replace ONLY**
- Max 50 lines per operation
- Multiple small edits instead of one large edit

### Error Handling Protocol

**Attempt 1:** Identify issue, apply fix, retry
**Attempt 2:** Different approach, verify context, retry
**Attempt 3:** **STOP IMMEDIATELY**
- DO NOT continue
- Report error details
- Request manual guidance

### Context Management

**At 80% token usage:**
- Stop execution
- Create checkpoint
- Report progress: "Completed T001-T0XX"
- Wait for user to restart from next task

**On context overflow:**
- Immediate checkpoint
- Save state
- Report: "Restart from T0XX"

### Validation Requirements (EVERY TASK)

**After EACH task completion:**
```bash
# Use commands from tasks.md frontmatter
{validation_commands.compile}
{validation_commands.test}
{validation_commands.lint}
```

**Default (if no frontmatter):**
```bash
# TypeScript projects
tsc --noEmit

# Tests (if exist)
npm test -- [relevant-test-file]

# Linting (critical only)
npm run lint
```

**For other languages:**
```bash
# Python
python -m py_compile {file}
pytest {test_file}
flake8 {file}

# Go
go build ./...
go test {package}
golangci-lint run

# Rust
cargo check
cargo test {test_name}
cargo clippy
```

**If validation fails:**
- Fix immediately
- Do NOT proceed to next task
- Re-validate before continuing

### Supporting Files Integration

**When tasks reference supporting files:**

**openapi.yaml:**
- Use for endpoint definitions
- Reference for request/response schemas
- Validation rules

**data-model.md:**
- Use for entity relationships
- Database schema reference
- Field definitions

**README.md:**
- Setup instructions
- Environment requirements
- Development workflow

**Example task integration:**
```markdown
Task T015: Create GET /api/v1/balance endpoint

Supporting Files:
- openapi.yaml: Line 45-60 defines endpoint spec
- data-model.md: Credit entity schema for queries

Implementation:
1. Read openapi.yaml endpoint definition
2. Use data-model.md Credit schema
3. Implement according to specs
```

---
```

## 8. Progressive Execution Guide

```markdown
## 📖 How to Execute This Project

**CRITICAL: Follow This Exact Pattern**

### Execution Philosophy
🐢 **Slow and steady wins**
✅ **Validate everything**
🛑 **Stop on errors**
📊 **Report progress**

### Step-by-Step Process

**Step 1: Preparation**
- Read this ENTIRE prompt
- Understand all phases
- Note checkpoints
- Review supporting files
- Prepare incremental execution

**Step 2: Start Phase 1**

Execute **ONLY Task T001:**
1. Read complete task description
2. Review supporting files referenced
3. Create/edit specified files
4. Use appropriate strategy (SMALL/MEDIUM/LARGE)
5. Validate immediately:
   ```bash
   {validation_commands.compile}
   {validation_commands.test}
   ```
6. **If PASS:** Continue to T002
7. **If FAIL:** Fix, re-validate, then continue

**Step 3: Continue Through Phase 1**

For T002-T010:
- ONE task at a time
- Validate after EACH task
- Stop at mini-checkpoint (T005)
- Validate mini-checkpoint
- Continue to T006-T010
- Stop at major checkpoint (T010)

**Step 4: Major Checkpoint (End of Phase)**

Run comprehensive validation:
```bash
# Full compilation
{validation_commands.compile}

# All tests
{validation_commands.test}

# Linting
{validation_commands.lint}

# Integration check (if defined)
{validation_commands.integration}
```

**If ALL pass:**
- Generate checkpoint report
- Get user confirmation (if interactive)
- Proceed to Phase 2

**If ANY fail:**
- **STOP**
- Fix all issues
- Re-validate
- Do not continue until 100% pass

**Step 5: Repeat for Remaining Phases**

Continue pattern for Phase 2, 3, 4...
- One task at a time
- Validate everything
- Stop at checkpoints
- Fix before continuing

### Token/Context Management

**Monitor usage continuously:**

**At 80% tokens:**
- Stop current task
- Complete validation
- Report: "Phase X, completed T001-T0YY"
- Instructions: "Restart from T0YY+1"

**On overflow:**
- Immediate stop
- Checkpoint state
- Report current position

### Supporting Files Workflow

**Before starting each task:**
1. Check if task references supporting files
2. Read referenced sections
3. Use information in implementation
4. Verify alignment with supporting docs

**Example:**
```
Task T020: Implement user authentication

References:
- openapi.yaml: /auth/login endpoint (line 120)
- data-model.md: User entity (section 3)

Steps:
1. Read openapi.yaml lines 120-140
2. Read data-model.md section 3
3. Implement per specifications
4. Validate against schemas
```

---
```

## 9. Error Recovery Procedures

```markdown
## 🛡️ ERROR RECOVERY PROCEDURES

### str_replace Failures

**Attempt 1: Context Review**
```typescript
// If str_replace fails:
1. view('file.ts', view_range=[start-10, end+10])
2. Find EXACT text match (including whitespace)
3. Retry str_replace with precise match
```

**Attempt 2: Expand Context**
```typescript
// If still fails:
1. view('file.ts', view_range=[start-50, end+50])
2. Include more surrounding context
3. Adjust match pattern
4. Retry with expanded pattern
```

**Attempt 3: STOP**
```
❌ DO NOT RETRY AGAIN

Report:
- File: [path]
- Operation: str_replace
- Attempts: 3
- Last error: [message]
- Context: [show relevant lines]

Request: Manual guidance needed
```

### Compilation Errors

**Error Detected:**
```bash
$ {validation_commands.compile}
error TS2304: Cannot find name 'User'
```

**Response:**
1. **DO NOT** continue to next task
2. Identify root cause
3. Fix error (import, type definition, etc.)
4. Re-compile
5. Verify fix successful
6. **THEN** continue

**If cannot fix after 2 attempts:**
- STOP
- Report error details
- Request guidance

### Test Failures

**Attempt 1: Fix Implementation**
```typescript
// Test fails:
1. Read test code
2. Understand expectation
3. Fix implementation
4. Re-run test
```

**Attempt 2: Verify Test Logic**
```typescript
// If still fails:
1. Review test logic
2. Check if test or code is wrong
3. Fix appropriate side
4. Re-run
```

**Attempt 3: STOP**
```
Report:
- Test: [name]
- Failure: [message]
- Attempts: 3
- Request: Manual review
```

### Context Overflow

**When approaching limit:**
```markdown
🛑 TOKEN USAGE: 85%

STOPPING EXECUTION

Progress Report:
- Completed: Phase 1 (T001-T010) ✅
- Completed: Phase 2 (T011-T018) ✅
- Current: Phase 2, Task T019 (in progress)

Validation:
- Compilation: ✅ PASS
- Tests: ✅ PASS (95% coverage)
- Linting: ✅ PASS

Next Steps:
1. Resume from Task T019
2. Provide prompt: "Continue Phase 2 from T019"
3. I will pick up exactly where I left off

Files Modified This Session:
- [list of files with changes]

State saved. Ready for continuation.
```

### Integration Issues

**If integration with existing code breaks:**
1. Identify breaking change
2. Review affected components
3. Fix backward compatibility
4. Re-validate integration
5. Update tests if needed

**If cannot resolve:**
- STOP
- Report:
  - What broke
  - Which components affected
  - Attempted fixes
- Request architecture review

### Missing Dependencies

**If task depends on incomplete task:**
1. Check dependency status
2. If dependency not complete: **SKIP task**
3. Log: "Skipped T0XX: depends on incomplete T0YY"
4. Continue to next task
5. Return to skipped tasks later

**If spec dependency not implemented:**
1. Check SPEC_INDEX for dependency info
2. If dependency spec not implemented: **SKIP task**
3. Log: "Skipped T0XX: depends on unimplemented spec-YYY"
4. Continue to next task
5. Note in final report

---
```

## 10. Phase & Task Details

For each phase in FILTERED_PHASES:

```markdown
## 📋 Phase [X]: [Phase Name] (T00A–T00B)

**Objective:** [Phase goal from tasks.md]

**Focus Areas:**
- [Area 1]
- [Area 2]

**Risk Level:** [LOW/MEDIUM/HIGH/CRITICAL]
**Estimated Effort:** [XX hours]

**Supporting Files for This Phase:**
- [List relevant supporting files]

---

### Task T00X: [Task Title] (~X.X hours)

**Description:**
[From tasks.md - concrete implementation details]

**Files:**

**CREATE: `[path/to/file.ts]`** (~XXX lines - SMALL)
- Purpose: [What this file does]
- Key functions: [List]
- Strategy: Full creation safe
- Supporting file reference: [If any]

**EDIT: `[path/to/existing.ts]`** (add XX lines - MEDIUM)
- Location: [Where to edit]
- Change: [What to change]
- Strategy: **str_replace ONLY** (MEDIUM file - no full rewrite)
- Max lines per change: 50
- Supporting file reference: [If any]

**Dependencies:**
- T00Y: [Reason]
- Related Spec: **[spec-id]** (`[path]`, repo: [repo])

**Validation:**
```bash
{validation_commands.compile}
{validation_commands.test}
```

**Expected Outcome:**
[What should work after this task]

**Supporting Files Integration:**
- `openapi.yaml` (lines XX-YY): Endpoint definition for this feature
- `data-model.md` (section Z): Entity schema to use

---

[Continue for all tasks in phase...]

### 🔍 Mini-Checkpoint: T00X-T00Y

**Validation:**
- [ ] Files created as expected
- [ ] No compilation errors
- [ ] Tests passing
- [ ] No critical lint issues

**If any fails:** Fix before continuing

---

[At end of phase:]

## ⚡ CHECKPOINT: Phase [X] Complete

**Comprehensive Validation:**

**Code Quality:**
- [ ] Compilation passes
- [ ] All tests passing
- [ ] No critical lint errors
- [ ] Code coverage ≥ [target]%

**Functionality:**
- [ ] All [X] tasks completed
- [ ] Acceptance criteria met
- [ ] Integration verified
- [ ] Supporting files alignment confirmed

**Documentation:**
- [ ] Code comments present
- [ ] README updated (if needed)

**Performance:**
- [ ] No obvious bottlenecks
- [ ] Response times acceptable

**Security:**
- [ ] No vulnerabilities introduced
- [ ] Auth/authz working

**Integration:**
- [ ] Works with existing system
- [ ] No breaking changes

**⚠️ CRITICAL:**
- If ANY validation fails: **STOP**
- Fix ALL issues before Phase [X+1]
- Do not accumulate technical debt

**Next Steps:**
Continue to Phase [X+1]: [Phase name]

---
```

## 11. Safety Checklist

```markdown
## 🔒 SAFETY CHECKLIST

**Before Starting Implementation:**

**I understand and accept:**
- [ ] Maximum 10 tasks per execution cycle
- [ ] File size strategies (SMALL/MEDIUM/LARGE)
- [ ] str_replace-only for MEDIUM/LARGE files
- [ ] Maximum 50 lines per str_replace
- [ ] Stop at 3 consecutive errors
- [ ] Validation after EVERY task
- [ ] Checkpoints are mandatory
- [ ] Progress reporting required
- [ ] Supporting files must be referenced
- [ ] Spec alignment must be verified

**I will:**
- [ ] Execute ONE task at a time
- [ ] Validate after EACH task
- [ ] Stop on validation failure
- [ ] Report progress at checkpoints
- [ ] Use supporting files appropriately
- [ ] Follow error recovery procedures
- [ ] Respect token/context limits
- [ ] Not skip any safety steps

**I will NOT:**
- [ ] Skip tasks or rush ahead
- [ ] Ignore validation failures
- [ ] Rewrite MEDIUM/LARGE files entirely
- [ ] Exceed str_replace line limits
- [ ] Continue after 3 errors
- [ ] Modify supporting files unless instructed

---

✅ All checks confirmed
🚀 Ready to begin implementation

---
```

## 12. Write Prompt File

Determine output path:
- Pattern: `implement-prompt-<spec-id>-<timestamp>.md`
- Location: TASKS_DIR/
- If exists: Add timestamp suffix

Write complete prompt to file with all sections:
1. Header with project overview
2. Platform-specific instructions
3. Critical execution constraints
4. Progressive execution guide
5. Error recovery procedures
6. Phase & task details (filtered)
7. Safety checklist

## 13. Report (Thai)

```
✅ สร้าง Implementation Prompt เรียบร้อยแล้ว

📁 ไฟล์: [Path to implement-prompt-<spec-id>-<timestamp>.md]
🎯 Platform: [Kilo Code / Claude Code / Roo Code]

📊 Structure:
- Phases: X (Filtered: Y phases - [list])
- Tasks: XX (Filtered: YY tasks - [range])
- Hours: ZZ estimated (Filtered: WW hours)

🔧 Technology Stack: [From tasks.md]

🔒 Safety Features:
- File size strategies: ✅
- Error recovery: ✅
- Checkpoints: X points
- Validation: After every task

📄 Supporting Files Integrated:
- openapi.yaml: [✅ Found / ⚠️ Not found]
- data-model.md: [✅ Found / ⚠️ Not found]
- README.md: [✅ Found / ⚠️ Not found]
- [Other files if any]

🔗 Spec References Resolved: X specs
[If SPEC_INDEX not found: ⚠️ SPEC_INDEX not found, dependency resolution skipped]

✅ Validation Commands:
- Compile: {validation_commands.compile}
- Test: {validation_commands.test}
- Lint: {validation_commands.lint}
[If from frontmatter: ✅ From tasks.md frontmatter]
[If default: ⚠️ Using TypeScript defaults (no frontmatter found)]

💡 วิธีใช้:

**สำหรับ Kilo Code:**
```bash
kilo code implement implement-prompt-<spec-id>-<timestamp>.md
```
- Auto subtasks: ✅ Enabled
- Mode switching: ✅ Automatic
- LLM selection: ✅ Automatic

**สำหรับ Claude Code:**
1. เปิด Claude Code
2. Load prompt file
3. (Optional) Create sub agents for specialized tasks
4. Execute ทีละ task
5. Follow checkpoint pattern
- Sub agents: ✅ Available
- Execution: Interactive
- Mode control: Manual

**สำหรับ Roo Code:**
1. เปิด Roo Code
2. Load prompt file
3. Execute ทีละ task
4. Follow checkpoint pattern

⚠️ Important:
- Execute ONE task at a time
- Validate after EACH task
- Stop at checkpoints
- Use supporting files
- Follow platform-specific instructions

🔄 ต่อไป:
1. Review prompt
2. Prepare environment
3. Start Phase 1, Task T001
4. Execute incrementally

---

**Note:** This prompt generator creates implementation instructions only.
For auto-implementation, use: /smartspec_implement_tasks.md
```

---

Context: $ARGUMENTS


---

## X. Error Handling & Messages

This section defines the clear, user-friendly error messages for validation failures.

### Error: Multiple Platform Flags
- **Trigger:** More than one of `--kilocode`, `--claude`, `--roocode` is used.
- **Message:** `Error: Multiple platform flags detected. Use only ONE platform flag.`
- **Solution:** `Example: --kilocode OR --claude`

### Error: Invalid Flag Combination
- **Trigger:** `--nosubtasks` without `--kilocode`, or `--with-subagents` without `--claude`.
- **Message:** `Error: --nosubtasks can only be used with --kilocode.`
- **Solution:** `Remove --nosubtasks or add --kilocode.`

### Error: Missing Sub-Agent Files
- **Trigger:** `--with-subagents` is used, but `.claude/agents/` or required files are missing.
- **Message:** `Error: --with-subagents requires the .claude/agents/ directory with all standard agent files.`
- **Solution:** `Run 'cp -r .smartspec-docs/templates/claude-agents .claude/agents' to create them.`

### Error: Invalid Task/Phase Range
- **Trigger:** Range is invalid (e.g., `T010-T001`, `3-1`).
- **Message:** `Error: Invalid range. Start must be less than or equal to end.`
- **Solution:** `Use ascending order: --tasks T001-T010`

### Error: File Not Found or Empty
- **Trigger:** `tasks.md` does not exist or is empty.
- **Message:** `Error: tasks.md not found or is empty.`
- **Solution:** `Ensure the path is correct and the file contains tasks. You can generate tasks with /smartspec_generate_tasks.md.`
