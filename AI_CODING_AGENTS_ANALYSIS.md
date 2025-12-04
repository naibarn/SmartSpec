# AI Coding Agents Deep Analysis
## Kilo Code, Claude Code, Roo Code

**Version:** 1.0.0  
**Date:** 2025-01-04  
**Purpose:** วิเคราะห์คุณลักษณะเชิงลึกเพื่อออกแบบ platform-specific instructions ที่ดึงศักยภาพเต็มที่

---

## 📊 Executive Summary

| Feature | Kilo Code | Claude Code | Roo Code |
|---------|-----------|-------------|----------|
| **Auto Subtasks** | ✅ Full (Orchestrator) | ⚠️ Limited (Auto-planning) | ⚠️ Partial (Workflow) |
| **Multi-agent Roles** | ✅ Yes (5 modes) | ❌ No (Single agent) | ❌ No (Single agent) |
| **Sub Agents** | ❌ No | ✅ Yes (User-created) | ❌ No |
| **Debugging** | ⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Very Good |
| **Repo-wide Reasoning** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Best | ⭐⭐⭐ Good |
| **Safety Workflow** | ⭐⭐⭐ Medium | ⭐⭐⭐⭐ High | ⭐⭐⭐⭐⭐ Very High |
| **LLM Switching** | ✅ Automatic per mode | ❌ No | ❌ No |
| **Preview Diffs** | ⚠️ Limited | ⚠️ Limited | ✅ Full |
| **Ideal Use Case** | Large structured tasks | Analysis & refactor | Safe frontend edits |

---

## 🤖 Kilo Code - Deep Analysis

### Core Philosophy
- **Multi-mode architecture** with automatic mode switching
- **Orchestrator-driven** subtask management
- **LLM optimization** per task type
- **Structured execution** for complex projects

### Modes Analysis

#### 1. Architect Mode
**Purpose:** Design decisions, system architecture, planning

**Strengths:**
- ✅ High-level thinking and design patterns
- ✅ System architecture planning
- ✅ Technology stack decisions
- ✅ Database schema design
- ✅ API contract design

**Optimized LLM:** Architecture-specialized model

**Best For:**
- Database schema design (T001: Design database schema)
- System architecture planning (T005: Plan microservices architecture)
- API contract definition (T010: Define API contracts)
- Technology stack selection (T002: Choose tech stack)

**Trigger Patterns:**
- Task title contains: "design", "architecture", "plan", "schema"
- Task description mentions: "system design", "architecture", "patterns"
- Phase name contains: "Planning", "Design", "Architecture"

**Example Tasks:**
```
T001: Design database schema for user management → Architect Mode
T005: Plan microservices architecture → Architect Mode
T010: Define REST API contracts → Architect Mode
```

---

#### 2. Code Mode
**Purpose:** Implementation, file creation/editing, coding

**Strengths:**
- ✅ Code generation
- ✅ File creation and editing
- ✅ Implementation of features
- ✅ Boilerplate generation
- ✅ Code refactoring

**Optimized LLM:** Code generation model

**Best For:**
- Entity/model creation (T020: Create User entity)
- Service implementation (T030: Implement authentication service)
- Controller/endpoint creation (T040: Create user endpoints)
- Utility functions (T050: Create validation helpers)

**Trigger Patterns:**
- Task title contains: "create", "implement", "build", "add"
- Files section has: CREATE or EDIT operations
- Task description mentions: "implement", "code", "function"

**Example Tasks:**
```
T020: Create User entity model → Code Mode
T030: Implement JWT authentication → Code Mode
T040: Build REST API endpoints → Code Mode
```

---

#### 3. Debug Mode
**Purpose:** Error fixing, troubleshooting, issue resolution

**Strengths:**
- ✅ Error analysis
- ✅ Stack trace interpretation
- ✅ Bug fixing
- ✅ Test failure resolution
- ✅ Performance issue diagnosis

**Optimized LLM:** Debugging-specialized model

**Best For:**
- Fixing compilation errors
- Resolving test failures
- Debugging runtime errors
- Performance optimization
- Memory leak fixes

**Trigger Patterns:**
- Task title contains: "fix", "debug", "resolve", "troubleshoot"
- Task description mentions: "error", "bug", "issue", "failing"
- Validation failures detected

**Example Tasks:**
```
T025: Fix TypeScript compilation errors → Debug Mode
T035: Resolve failing unit tests → Debug Mode
T045: Debug memory leak in service → Debug Mode
```

---

#### 4. Ask Mode
**Purpose:** Clarification, user input, decision making

**Strengths:**
- ✅ Requirement clarification
- ✅ Decision support
- ✅ Option presentation
- ✅ User guidance
- ✅ Ambiguity resolution

**Optimized LLM:** Q&A and reasoning model

**Best For:**
- Ambiguous requirements
- Multiple implementation options
- Business logic clarification
- User preference decisions
- Missing information

**Trigger Patterns:**
- Task description has: "clarify", "decide", "choose"
- Ambiguous requirements detected
- Multiple valid approaches exist
- Missing critical information

**Example Tasks:**
```
T015: Clarify authentication flow requirements → Ask Mode
T025: Choose between REST vs GraphQL → Ask Mode
T035: Decide on caching strategy → Ask Mode
```

---

#### 5. Orchestrator Mode
**Purpose:** Coordinating multiple tasks, workflow management, subtask breakdown

**Strengths:**
- ✅ **Auto Subtasks** - Automatic breakdown of large tasks
- ✅ Task coordination
- ✅ Dependency management
- ✅ Parallel execution planning
- ✅ Workflow optimization

**Optimized LLM:** Coordination and planning model

**Best For:**
- Tasks >8 hours (auto-breaks into subtasks)
- Multi-component tasks
- Complex workflows
- Cross-cutting concerns
- Integration tasks

**Trigger Patterns:**
- Task hours >8h (automatic activation)
- Task involves multiple components
- Task description mentions: "integrate", "coordinate", "orchestrate"
- Phase name contains: "Integration", "Coordination"

**Subtask Breakdown:**
```
T050: Implement complete authentication system (12h)
  → Orchestrator Mode activates automatically
  
  Subtasks created:
  T050.1: Design auth database schema (2h) → Architect Mode
  T050.2: Create User entity model (2h) → Code Mode
  T050.3: Implement JWT service (3h) → Code Mode
  T050.4: Create auth endpoints (3h) → Code Mode
  T050.5: Add auth tests (2h) → Code Mode
  T050.6: Integrate with existing system (2h) → Orchestrator Mode
```

**Auto Subtask Rules:**
- Tasks >8h: MUST break into subtasks
- Subtasks: 2-4h each (optimal)
- Format: T001.1, T001.2, T001.3, etc.
- Each subtask assigned appropriate mode
- Dependencies tracked automatically

---

### Mode Switching Logic

**Automatic Mode Selection:**
```typescript
function selectMode(task: Task): Mode {
  // Orchestrator for large tasks (auto subtasks)
  if (task.hours > 8) {
    return Mode.ORCHESTRATOR;
  }
  
  // Architect for design tasks
  if (task.title.match(/design|architecture|plan|schema/i)) {
    return Mode.ARCHITECT;
  }
  
  // Debug for fix tasks
  if (task.title.match(/fix|debug|resolve|troubleshoot/i)) {
    return Mode.DEBUG;
  }
  
  // Ask for ambiguous tasks
  if (task.hasAmbiguity || task.needsDecision) {
    return Mode.ASK;
  }
  
  // Code for implementation tasks (default)
  return Mode.CODE;
}
```

**Mode Transition:**
- Seamless switching between modes
- No manual intervention needed
- Context preserved across modes
- LLM switched automatically

---

### LLM Optimization

**Per-Mode LLM Selection:**

| Mode | LLM Type | Optimization |
|------|----------|--------------|
| Architect | GPT-4 / Claude Opus | Architecture reasoning |
| Code | Codex / Code Llama | Code generation |
| Debug | Specialized debug model | Error analysis |
| Ask | GPT-4 / Claude | Reasoning & Q&A |
| Orchestrator | Planning-optimized | Task coordination |

**Benefits:**
- ✅ Optimal performance per task type
- ✅ Cost optimization (cheaper models for simple tasks)
- ✅ Speed optimization (faster models when possible)
- ✅ Quality optimization (best model for each concern)

---

### Auto Subtasks Feature

**Activation:**
- Automatic when task >8h
- Manual trigger: User can request breakdown
- Orchestrator mode handles breakdown

**Breakdown Strategy:**
```
Original Task: T050 (12h)
  ↓
Orchestrator Analysis:
  - Identify components
  - Estimate subtask sizes
  - Assign modes
  - Create dependencies
  ↓
Subtasks Generated:
  T050.1 (2h) - Architect Mode
  T050.2 (2h) - Code Mode
  T050.3 (3h) - Code Mode
  T050.4 (3h) - Code Mode
  T050.5 (2h) - Code Mode
  ↓
Sequential Execution:
  Each subtask executed in appropriate mode
  Progress tracked per subtask
  Validation after each subtask
```

**Subtask Format:**
- Parent: T050
- Subtasks: T050.1, T050.2, T050.3, ...
- Checkbox: `- [ ] T050.1: Design auth schema (2h)`
- Independent validation per subtask

**Benefits:**
- ✅ Prevents context overflow
- ✅ Better progress tracking
- ✅ Easier error recovery
- ✅ Clearer validation points
- ✅ Parallel execution potential

---

### Strengths Summary

1. **Multi-mode Intelligence**
   - Right tool for right job
   - Automatic mode selection
   - LLM optimization

2. **Auto Subtasks**
   - Prevents context overflow
   - Better task management
   - Clearer progress

3. **Structured Execution**
   - Predictable workflow
   - Clear validation points
   - Easy debugging

4. **Scalability**
   - Handles large projects
   - Complex task coordination
   - Multi-component systems

---

### Weaknesses

1. **Learning Curve**
   - Need to understand modes
   - Mode selection logic

2. **Overhead**
   - Mode switching overhead
   - More complex architecture

3. **Limited Safety Preview**
   - No comprehensive diff preview
   - Less visibility before execution

---

### Ideal Use Cases

✅ **Perfect For:**
- Large structured projects (>100 tasks)
- Complex multi-component systems
- Tasks requiring different expertise (design, code, debug)
- Projects with clear phases and dependencies
- Enterprise-grade applications

❌ **Not Ideal For:**
- Simple single-file edits
- Quick prototypes
- Projects requiring extensive preview before execution

---

## 🧠 Claude Code - Deep Analysis

### Core Philosophy
- **Single-agent architecture** with deep reasoning
- **User-created sub agents** for specialization
- **Interactive execution** with human oversight
- **Best-in-class analysis** and understanding

### Architecture

**Single Agent + Sub Agents:**
```
Main Claude Agent
  ├─ Sub Agent: Database Expert (user-created)
  ├─ Sub Agent: API Developer (user-created)
  ├─ Sub Agent: Test Engineer (user-created)
  └─ Sub Agent: Integration Coordinator (user-created)
```

**Key Difference from Kilo Code:**
- Kilo Code: Built-in modes (automatic)
- Claude Code: User creates sub agents (manual)

---

### Modes / Behaviors

#### 1. Code Generation Mode
**Purpose:** Standard code implementation

**Strengths:**
- ✅ High-quality code generation
- ✅ Context-aware implementation
- ✅ Best-in-class code understanding
- ✅ Natural language to code

**Best For:**
- Feature implementation
- Code creation
- Refactoring
- Code completion

---

#### 2. Auto-Refactor Mode
**Purpose:** Automatic code improvement

**Strengths:**
- ✅ Code quality improvement
- ✅ Pattern detection
- ✅ Best practices application
- ✅ Technical debt reduction

**Best For:**
- Code cleanup
- Pattern refactoring
- Performance optimization
- Modernization

---

#### 3. Auto-Debug Mode
**Purpose:** Automatic error detection and fixing

**Strengths:**
- ✅ Excellent error analysis
- ✅ Root cause identification
- ✅ Fix suggestions
- ✅ Test failure resolution

**Best For:**
- Bug fixing
- Test debugging
- Error resolution
- Performance issues

---

#### 4. Deep Project Analysis
**Purpose:** Comprehensive codebase understanding

**Strengths:**
- ✅ **Best-in-class** repo-wide reasoning
- ✅ Architecture understanding
- ✅ Dependency analysis
- ✅ Impact assessment
- ✅ Code relationship mapping

**Best For:**
- Large codebase analysis
- Refactoring planning
- Architecture review
- Technical debt assessment
- Migration planning

**Example:**
```
"Analyze this entire codebase and identify:
1. All authentication-related code
2. Security vulnerabilities
3. Performance bottlenecks
4. Refactoring opportunities
5. Test coverage gaps"

→ Claude provides comprehensive analysis across entire repo
```

---

#### 5. Agentic Computer Use Mode
**Purpose:** Autonomous system interaction

**Strengths:**
- ✅ Terminal command execution
- ✅ File system operations
- ✅ Tool invocation
- ✅ Multi-step workflows

**Best For:**
- Setup automation
- Build processes
- Testing workflows
- Deployment tasks

---

#### 6. Ask / Reasoning Mode
**Purpose:** Deep reasoning and explanation

**Strengths:**
- ✅ Excellent reasoning
- ✅ Clear explanations
- ✅ Decision support
- ✅ Trade-off analysis

**Best For:**
- Architecture decisions
- Technology choices
- Approach selection
- Problem solving

---

### Sub Agents System

**Concept:**
User creates specialized sub agents for different concerns

**Creation:**
```typescript
// User creates DB Agent
"Create a sub agent specialized in database operations.
Focus: PostgreSQL, migrations, entity models, queries.
Responsibilities: All database-related tasks (T001-T010)"

// User creates API Agent
"Create a sub agent specialized in API development.
Focus: Express.js, endpoints, validation, error handling.
Responsibilities: All API tasks (T011-T025)"

// User creates Test Agent
"Create a sub agent specialized in testing.
Focus: Jest, unit tests, integration tests, mocking.
Responsibilities: All testing tasks (T026-T035)"
```

**Benefits:**
- ✅ Specialized expertise per domain
- ✅ Context isolation
- ✅ Parallel work (conceptually)
- ✅ Clear responsibility boundaries

**Workflow:**
```
Main Agent:
  "I need to implement authentication system"
  ↓
  Delegates to DB Agent: "Create auth schema"
  ↓
  Delegates to API Agent: "Create auth endpoints"
  ↓
  Delegates to Test Agent: "Create auth tests"
  ↓
  Coordinates integration
```

---

### Auto-Planning Feature

**Limited Auto Subtasks:**
- Can break down tasks into steps
- Not as automatic as Kilo Code Orchestrator
- Requires more user guidance

**Example:**
```
User: "Implement authentication system"

Claude: "I'll break this down into steps:
1. Design database schema
2. Create User entity
3. Implement JWT service
4. Create auth endpoints
5. Add tests

Shall I proceed with step 1?"

→ User confirms each step
→ More interactive, less automatic
```

---

### Strengths Summary

1. **Best Repo-wide Understanding**
   - Unmatched codebase analysis
   - Deep context awareness
   - Relationship mapping

2. **Sub Agents Flexibility**
   - User-defined specialization
   - Clear responsibility boundaries
   - Context isolation

3. **Interactive Control**
   - Human oversight
   - Step-by-step confirmation
   - Flexible execution

4. **Analysis Excellence**
   - Best for refactoring
   - Architecture review
   - Technical debt assessment

---

### Weaknesses

1. **Manual Sub Agent Creation**
   - User must create agents
   - No automatic specialization
   - More setup overhead

2. **Limited Auto Subtasks**
   - Not as automatic as Kilo Code
   - Requires more user interaction
   - Less structured breakdown

3. **Interactive Overhead**
   - More user involvement needed
   - Slower for large batch tasks
   - Less autonomous

---

### Ideal Use Cases

✅ **Perfect For:**
- Analysis-heavy projects
- Large codebase refactoring
- Architecture review and planning
- Projects requiring deep understanding
- Interactive development with oversight
- Complex decision-making scenarios

❌ **Not Ideal For:**
- Fully autonomous batch execution
- Projects requiring minimal user interaction
- Simple structured tasks

---

## 🦘 Roo Code - Deep Analysis

### Core Philosophy
- **Workflow-driven** execution
- **Safety-first** approach with preview diffs
- **Frontend-optimized** for Node.js/React
- **Structured phases** for predictable execution

### Workflow Modes

#### 1. Plan Mode
**Purpose:** Task planning and breakdown

**Strengths:**
- ✅ Clear task structure
- ✅ Dependency identification
- ✅ Effort estimation
- ✅ Risk assessment

**Best For:**
- Project planning
- Task breakdown
- Dependency mapping
- Timeline estimation

---

#### 2. Implement Mode
**Purpose:** Code implementation

**Strengths:**
- ✅ Safe code changes
- ✅ Preview before apply
- ✅ Incremental edits
- ✅ Rollback support

**Best For:**
- Feature implementation
- Code changes
- Refactoring
- Bug fixes

---

#### 3. Review Mode
**Purpose:** Code review and validation

**Strengths:**
- ✅ **Full diff preview** (best-in-class)
- ✅ Change visualization
- ✅ Impact assessment
- ✅ Safety validation

**Best For:**
- Code review
- Change verification
- Safety checks
- Quality assurance

**Preview Diffs:**
```diff
File: src/auth/user.ts

- export class User {
+ export class User implements IUser {
    private id: string;
+   private email: string;
    
-   constructor(id: string) {
+   constructor(id: string, email: string) {
      this.id = id;
+     this.email = email;
    }
  }

[Preview] Apply these changes? (y/n)
```

---

#### 4. Execute Mode
**Purpose:** Running tests and validation

**Strengths:**
- ✅ Test execution
- ✅ Validation checks
- ✅ Build verification
- ✅ Integration testing

**Best For:**
- Test running
- Build verification
- Validation
- CI/CD integration

---

#### 5. Explain Mode
**Purpose:** Code explanation and documentation

**Strengths:**
- ✅ Clear explanations
- ✅ Code documentation
- ✅ Learning support
- ✅ Onboarding help

**Best For:**
- Code understanding
- Documentation
- Knowledge transfer
- Onboarding

---

### Workflow-Based Subtasks

**Partial Auto Subtasks:**
- Workflow-driven breakdown
- Phase-based execution
- Not as automatic as Kilo Code Orchestrator

**Example:**
```
Task: Implement authentication

Roo Code Workflow:
1. Plan Mode: Break down into phases
   - Phase 1: Database setup
   - Phase 2: Service implementation
   - Phase 3: API endpoints
   - Phase 4: Testing

2. Implement Mode: Execute each phase
   - Preview changes before apply
   - User confirms each phase

3. Review Mode: Review all changes
   - Show comprehensive diffs
   - Verify safety

4. Execute Mode: Run tests
   - Validate implementation
   - Check integration
```

---

### Safety Features

**Best-in-Class Safety:**

1. **Preview Diffs**
   - ✅ Full diff visualization before apply
   - ✅ Line-by-line changes shown
   - ✅ Impact assessment
   - ✅ Rollback support

2. **Incremental Changes**
   - ✅ Small, safe edits
   - ✅ Step-by-step application
   - ✅ Easy rollback

3. **Validation Gates**
   - ✅ Checks before apply
   - ✅ Test verification
   - ✅ Build validation

**Safety Workflow:**
```
1. Plan changes
   ↓
2. Generate diffs
   ↓
3. Preview diffs (user review)
   ↓
4. User approval
   ↓
5. Apply changes
   ↓
6. Validate (tests, build)
   ↓
7. Confirm success or rollback
```

---

### Strengths Summary

1. **Safety First**
   - Best preview diffs
   - Incremental changes
   - Easy rollback

2. **Frontend Optimized**
   - Excellent for React/Node
   - Modern frontend tooling
   - Component-based development

3. **Structured Workflow**
   - Clear phases
   - Predictable execution
   - Easy to understand

4. **User Control**
   - High visibility
   - Manual approval gates
   - Flexible execution

---

### Weaknesses

1. **Limited Automation**
   - More manual steps
   - Less autonomous
   - Slower for large tasks

2. **Workflow Overhead**
   - Must follow phases
   - Less flexible
   - More structured

3. **Partial Subtasks**
   - Not as automatic as Kilo Code
   - Workflow-based, not Orchestrator-based

---

### Ideal Use Cases

✅ **Perfect For:**
- Frontend development (React, Vue, Angular)
- Node.js projects
- Projects requiring high safety
- Teams needing change visibility
- Incremental refactoring
- Learning and onboarding

❌ **Not Ideal For:**
- Fully autonomous execution
- Backend-heavy projects
- Large batch operations
- Projects requiring minimal user interaction

---

## 🎯 Comparison Matrix

### Auto Subtasks Comparison

| Feature | Kilo Code | Claude Code | Roo Code |
|---------|-----------|-------------|----------|
| **Automatic Breakdown** | ✅ Full (>8h tasks) | ⚠️ Limited (manual) | ⚠️ Workflow-based |
| **Subtask Format** | T001.1, T001.2 | Steps 1, 2, 3 | Phase 1, 2, 3 |
| **Mode Assignment** | ✅ Automatic | ❌ No | ❌ No |
| **Orchestration** | ✅ Orchestrator Mode | ❌ Manual | ⚠️ Workflow |
| **User Intervention** | ❌ Minimal | ✅ High | ✅ High |

---

### Multi-Agent / Sub Agents Comparison

| Feature | Kilo Code | Claude Code | Roo Code |
|---------|-----------|-------------|----------|
| **Built-in Modes** | ✅ 5 modes | ❌ No | ❌ No |
| **User-Created Agents** | ❌ No | ✅ Yes | ❌ No |
| **Automatic Switching** | ✅ Yes | ❌ No | ❌ No |
| **LLM per Mode** | ✅ Yes | ❌ No | ❌ No |
| **Specialization** | ✅ Built-in | ✅ User-defined | ❌ No |

---

### Safety & Preview Comparison

| Feature | Kilo Code | Claude Code | Roo Code |
|---------|-----------|-------------|----------|
| **Preview Diffs** | ⚠️ Limited | ⚠️ Limited | ✅ **Full** |
| **Approval Gates** | ❌ Minimal | ⚠️ Some | ✅ **Many** |
| **Rollback** | ⚠️ Manual | ⚠️ Manual | ✅ **Easy** |
| **Safety Score** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

### Analysis & Understanding Comparison

| Feature | Kilo Code | Claude Code | Roo Code |
|---------|-----------|-------------|----------|
| **Repo-wide Reasoning** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ **Best** | ⭐⭐⭐ Good |
| **Deep Analysis** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ **Best** | ⭐⭐⭐ Good |
| **Context Awareness** | ⭐⭐⭐⭐ Very Good | ⭐⭐⭐⭐⭐ **Best** | ⭐⭐⭐⭐ Very Good |
| **Refactoring** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ **Best** | ⭐⭐⭐⭐ Very Good |

---

### Automation Level Comparison

| Aspect | Kilo Code | Claude Code | Roo Code |
|--------|-----------|-------------|----------|
| **Automation Level** | ⭐⭐⭐⭐⭐ Highest | ⭐⭐⭐ Medium | ⭐⭐ Low |
| **User Interaction** | ⭐ Minimal | ⭐⭐⭐ Medium | ⭐⭐⭐⭐ High |
| **Batch Processing** | ✅ Excellent | ⚠️ Limited | ❌ Not ideal |
| **Autonomous** | ✅ Yes | ⚠️ Partial | ❌ No |

---

## 🎨 Optimal Use Case Matrix

### Task Type Recommendations

| Task Type | Best Tool | Reason |
|-----------|-----------|--------|
| **Large Project (>100 tasks)** | Kilo Code | Auto subtasks, Orchestrator |
| **Deep Analysis** | Claude Code | Best repo-wide reasoning |
| **Safe Refactoring** | Roo Code | Preview diffs, safety |
| **Complex Architecture** | Kilo Code | Architect Mode |
| **Frontend Development** | Roo Code | Frontend-optimized |
| **Batch Implementation** | Kilo Code | Autonomous execution |
| **Interactive Development** | Claude Code | Sub agents, flexibility |
| **Learning/Onboarding** | Roo Code | Explain Mode, safety |

---

### Project Size Recommendations

| Project Size | Best Tool | Alternative |
|--------------|-----------|-------------|
| **Small (<20 tasks)** | Roo Code | Claude Code |
| **Medium (20-100 tasks)** | Claude Code | Kilo Code |
| **Large (>100 tasks)** | Kilo Code | Claude Code |
| **Enterprise (>500 tasks)** | Kilo Code | - |

---

### Team Experience Recommendations

| Team Level | Best Tool | Reason |
|------------|-----------|--------|
| **Junior** | Roo Code | Safety, learning |
| **Mid-level** | Claude Code | Flexibility, guidance |
| **Senior** | Kilo Code | Autonomy, efficiency |
| **Mixed** | Claude Code | Balance of control & power |

---

## 🚀 Optimization Strategies

### For Kilo Code

**Maximize Efficiency:**
1. ✅ Let Orchestrator handle >8h tasks
2. ✅ Trust automatic mode switching
3. ✅ Use structured task format
4. ✅ Define clear task boundaries
5. ✅ Leverage LLM optimization

**Task Structure:**
```markdown
## Phase 1: Database Design (T001-T010)

### T001: Design user authentication schema (3h)
- [ ] T001: Design user authentication schema (3h)
**Mode:** Architect (auto-selected)
**Description:** Design PostgreSQL schema for user auth...

### T015: Implement complete auth system (12h)
- [ ] T015: Implement complete auth system (12h)
**Mode:** Orchestrator (auto-activated, will create subtasks)
**Description:** Full authentication implementation...
```

---

### For Claude Code

**Maximize Analysis Power:**
1. ✅ Create specialized sub agents early
2. ✅ Use for deep codebase analysis
3. ✅ Leverage repo-wide reasoning
4. ✅ Interactive decision-making
5. ✅ Refactoring planning

**Sub Agent Setup:**
```markdown
## Setup Sub Agents

### 1. Database Agent
"Create a sub agent specialized in database operations.
Focus: PostgreSQL, migrations, Prisma ORM, queries.
Expertise: Schema design, optimization, indexing.
Responsibilities: T001-T015 (all database tasks)"

### 2. API Agent
"Create a sub agent specialized in API development.
Focus: Express.js, REST APIs, validation, error handling.
Expertise: Endpoint design, middleware, security.
Responsibilities: T016-T030 (all API tasks)"

### 3. Test Agent
"Create a sub agent specialized in testing.
Focus: Jest, unit tests, integration tests, E2E.
Expertise: Test design, mocking, coverage.
Responsibilities: T031-T045 (all testing tasks)"

## Execution Strategy

1. DB Agent handles all database tasks (T001-T015)
2. API Agent handles all API tasks (T016-T030)
3. Test Agent handles all testing tasks (T031-T045)
4. Main agent coordinates integration
```

---

### For Roo Code

**Maximize Safety:**
1. ✅ Use workflow phases
2. ✅ Review all diffs before apply
3. ✅ Incremental changes
4. ✅ Validate after each phase
5. ✅ Leverage preview features

**Workflow Structure:**
```markdown
## Phase 1: Database Setup

### Plan Mode
- Design schema
- Identify dependencies
- Estimate effort

### Implement Mode
- Create migration files
- Preview diffs
- Apply changes incrementally

### Review Mode
- Review all changes
- Verify safety
- Check impact

### Execute Mode
- Run migrations
- Run tests
- Validate

## Phase 2: Service Implementation
(Repeat workflow)
```

---

## 📊 Decision Tree

```
Start: Need to implement tasks
  ↓
Q1: Project size?
  ├─ Small (<20 tasks) → Roo Code (safety, learning)
  ├─ Medium (20-100) → Claude Code (analysis, flexibility)
  └─ Large (>100) → Kilo Code (automation, orchestration)
  
Q2: Need deep analysis?
  ├─ Yes → Claude Code (best repo-wide reasoning)
  └─ No → Continue
  
Q3: Need high safety/preview?
  ├─ Yes → Roo Code (best preview diffs)
  └─ No → Continue
  
Q4: Need full automation?
  ├─ Yes → Kilo Code (Orchestrator, auto subtasks)
  └─ No → Claude Code (interactive, sub agents)
  
Q5: Frontend-heavy?
  ├─ Yes → Roo Code (frontend-optimized)
  └─ No → Kilo Code or Claude Code
```

---

## ✅ Recommendations Summary

### Use Kilo Code When:
- ✅ Large projects (>100 tasks)
- ✅ Need full automation
- ✅ Tasks >8h (auto subtasks)
- ✅ Structured execution required
- ✅ Multi-mode intelligence needed
- ✅ Batch processing
- ✅ Enterprise-grade projects

### Use Claude Code When:
- ✅ Need deep codebase analysis
- ✅ Refactoring large projects
- ✅ Architecture review
- ✅ Interactive development
- ✅ Complex decision-making
- ✅ Need specialized sub agents
- ✅ Medium-sized projects (20-100 tasks)

### Use Roo Code When:
- ✅ Frontend development (React, Vue, Angular)
- ✅ Need high safety (preview diffs)
- ✅ Learning/onboarding
- ✅ Incremental refactoring
- ✅ Small projects (<20 tasks)
- ✅ Need change visibility
- ✅ Team requires approval gates

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-01-04  
**Next Review:** When new features/modes are added
