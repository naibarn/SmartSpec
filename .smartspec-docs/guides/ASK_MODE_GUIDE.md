# Kilo Code Ask Mode Guide

## Overview

**Ask Mode** is a built-in mode in Kilo Code designed for **analysis, understanding, and exploration** before making decisions. It's used when you need to "analyze", "understand", "explore options", or "clarify" before deciding what to do.

Ask Mode doesn't write code or fix bugs. Instead, it focuses on **thinking, analyzing, and providing insights** to help you make informed decisions.

---

## When to Use Ask Mode

### ✅ Use Ask Mode when:

| Situation | Why Ask Mode? |
|-----------|---------------|
| **Understanding Code** | Need to analyze existing code before modifying |
| **Exploring Options** | Need to know what approaches are available |
| **Clarifying Requirements** | Requirements are unclear or ambiguous |
| **Impact Analysis** | Need to understand consequences of changes |
| **Best Practices** | Need to know the best way to implement something |
| **Decision Making** | Need help deciding between multiple approaches |

---

## Ask Mode vs Other Modes

| Mode | Purpose | Output |
|------|---------|--------|
| **Ask Mode** | Analyze and understand | Insights, options, recommendations |
| **Architect Mode** | Design and plan | Architecture, technical specs, plans |
| **Code Mode** | Implement | Actual code |
| **Debug Mode** | Fix problems | Bug fixes, error resolution |
| **Orchestrator Mode** | Manage workflow | Sub-tasks, task breakdown |

**Key Difference:**

```
Ask Mode = วิเคราะห์ (analyze before deciding)
Architect Mode = วางแผน (design and plan)
Code/Debug Mode = ลงมือทำ (actually do it)
```

---

## Ask Mode Use Cases

### ✅ 1) Understanding Existing Code

**Scenario:**
- Need to understand how current authentication works before modifying
- Need to know how payment system is structured
- Need to understand data flow in the application

**Example Prompt:**
```
Ask Mode.
Based on the current project structure, how does the authentication system work?
What are the key components and their responsibilities?
```

**Ask Mode will:**
- Analyze existing code
- Explain architecture and patterns
- Identify key components
- Describe data flow
- Point out important files and functions

---

### ✅ 2) Exploring Implementation Options

**Scenario:**
- Multiple ways to implement a feature
- Need to know pros/cons of each approach
- Want to choose the best approach for the project

**Example Prompt:**
```
Ask Mode.
Based on the current project structure, what approaches can we use to add role-based authentication?
What are the pros and cons of each approach?
```

**Ask Mode will:**
- List available approaches
- Explain pros and cons
- Consider project context
- Recommend best approach
- Explain trade-offs

---

### ✅ 3) Impact Analysis

**Scenario:**
- Need to know what will be affected by a change
- Want to understand risks before making changes
- Need to identify dependencies

**Example Prompt:**
```
Ask Mode.
If we change the User model to add role-based permissions, what other parts of the system will be affected?
```

**Ask Mode will:**
- Analyze dependencies
- Identify affected files and components
- Explain potential impacts
- Warn about risks
- Suggest mitigation strategies

---

### ✅ 4) Clarifying Vague Requirements

**Scenario:**
- Requirements are unclear or incomplete
- Need to understand what the user really wants
- Need to identify missing information

**Example Prompt:**
```
Ask Mode.
The requirement says "add payment processing". What specific details do we need to clarify before implementation?
```

**Ask Mode will:**
- Identify ambiguities
- List questions that need answers
- Suggest clarifications
- Identify missing requirements
- Propose assumptions to validate

---

### ✅ 5) Best Practices and Recommendations

**Scenario:**
- Want to know the best way to do something
- Need to follow project conventions
- Want to avoid common mistakes

**Example Prompt:**
```
Ask Mode.
What's the best way to handle error logging in this Express.js project?
Should we use middleware, service layer, or both?
```

**Ask Mode will:**
- Analyze project patterns
- Recommend best practices
- Consider project context
- Explain reasoning
- Provide examples

---

### ✅ 6) Decision Support

**Scenario:**
- Need to choose between multiple libraries
- Need to decide on architecture approach
- Want expert opinion before committing

**Example Prompt:**
```
Ask Mode.
Should we use BullMQ or Agenda for background job processing in this project?
Consider our current tech stack and requirements.
```

**Ask Mode will:**
- Compare options
- Consider project context
- Analyze requirements
- Provide recommendation
- Explain reasoning

---

## Typical Workflow with Ask Mode

### Pattern 1: Ask → Architect → Code

```
1. Ask Mode: Analyze current system and explore options
2. Architect Mode: Design architecture based on insights
3. Code Mode: Implement based on architecture
```

**Example:**
```
Task: Add shopping cart feature

Step 1 (Ask Mode):
→ "Ask Mode. How is the current e-commerce system structured? What patterns are used?"
→ Analyzes existing code, identifies patterns

Step 2 (Architect Mode):
→ "Use Architect Mode to design shopping cart following existing patterns"
→ Designs architecture consistent with current system

Step 3 (Code Mode):
→ Implements shopping cart based on architecture
```

---

### Pattern 2: Ask → Code (Simple Tasks)

```
1. Ask Mode: Clarify requirements and approach
2. Code Mode: Implement directly
```

**Example:**
```
Task: Add validation to user registration

Step 1 (Ask Mode):
→ "Ask Mode. What validation rules should we apply to user registration?"
→ Lists standard validation rules, suggests best practices

Step 2 (Code Mode):
→ Implements validation based on recommendations
```

---

### Pattern 3: Ask → Debug (Problem Analysis)

```
1. Ask Mode: Analyze problem and potential causes
2. Debug Mode: Fix based on analysis
```

**Example:**
```
Problem: API endpoint returns 500 error

Step 1 (Ask Mode):
→ "Ask Mode. What could cause this endpoint to return 500 error?"
→ Lists potential causes, suggests debugging steps

Step 2 (Debug Mode):
→ "Use Debug Mode to analyze and fix the issue"
→ Fixes the actual problem
```

---

## When NOT to Use Ask Mode

### 🛑 Don't use Ask Mode when:

| Situation | Why Not | Use Instead |
|-----------|---------|-------------|
| **Need to write code** | Ask Mode doesn't write code | **Code Mode** |
| **Need to fix bugs** | Ask Mode doesn't fix bugs | **Debug Mode** |
| **Need architecture design** | Ask Mode analyzes, doesn't design | **Architect Mode** |
| **Requirements are clear** | No need to analyze | **Code Mode** directly |
| **Simple, straightforward task** | Overkill | **Code Mode** directly |

---

## How SmartSpec Uses Ask Mode

### 1. Before Complex Implementation

**When:**
- Task is complex and unclear
- Multiple approaches possible
- Need to understand existing code first

**SmartSpec workflow:**
```
1. Ask Mode: Analyze and explore options
2. Architect Mode: Design based on analysis
3. Code Mode: Implement based on design
4. Debug Mode: Fix any issues
5. Test Mode: Validate
```

---

### 2. With `--kilocode` Flag

**When using Orchestrator Mode:**

Orchestrator may use **Ask Mode first** to analyze before deciding:

```
Orchestrator analyzes task complexity
→ If unclear or complex: Use Ask Mode first
→ Then decide: Architect → Code or Code directly
```

**Example:**
```
Task: T015: Integrate third-party payment API (3h)

Orchestrator decides: Need analysis first

Sub-tasks:
1. Ask Mode: Analyze payment API options and current payment flow
2. Architect Mode: Design payment integration architecture
3. Code Mode: Implement API client
4. Code Mode: Implement webhook handler
5. Code Mode: Add error handling
6. Debug Mode: Fix any issues
7. Test Mode: Validate integration
```

---

### 3. During Error Analysis

**When validation or tests fail:**

```
Validation fails
→ Ask Mode: Analyze why validation failed
→ Debug Mode: Fix based on analysis
```

---

## Example Scenarios

### Scenario 1: Adding Authentication

```markdown
**Task:** T020: Add JWT authentication to API (2h)

**Step 1: Ask Mode (Analysis)**
→ Command: "Ask Mode. How is authentication currently handled in this project? What patterns are used?"

→ Ask Mode output:
  - Current auth: Basic session-based
  - Pattern: Middleware-based
  - Files: src/middleware/auth.ts
  - Database: User model in src/models/user.ts
  - Recommendation: Add JWT middleware following existing pattern

**Step 2: Architect Mode (Design)**
→ Command: "Use Architect Mode to design JWT authentication following existing middleware pattern"

→ Architect Mode output:
  - JWT middleware structure
  - Token generation service
  - Token validation logic
  - Refresh token handling

**Step 3: Code Mode (Implementation)**
→ Implements JWT authentication based on architecture

**Result:** ✅ JWT authentication that fits existing patterns
```

---

### Scenario 2: Choosing Database Library

```markdown
**Task:** T025: Add database caching layer (3h)

**Step 1: Ask Mode (Exploration)**
→ Command: "Ask Mode. What caching solutions work well with PostgreSQL and TypeScript? Consider our current tech stack."

→ Ask Mode output:
  - Option 1: Redis with ioredis
    - Pros: Fast, widely used, good TypeScript support
    - Cons: Additional service to manage
  
  - Option 2: In-memory cache with node-cache
    - Pros: Simple, no additional services
    - Cons: Lost on restart, not distributed
  
  - Option 3: PostgreSQL materialized views
    - Pros: Native to PostgreSQL, no new dependencies
    - Cons: Less flexible, requires database migrations
  
  - Recommendation: Redis with ioredis (best for scalability)

**Step 2: Architect Mode (Design)**
→ Designs Redis caching layer

**Step 3: Code Mode (Implementation)**
→ Implements Redis caching

**Result:** ✅ Informed decision with clear reasoning
```

---

### Scenario 3: Impact Analysis

```markdown
**Task:** T030: Refactor User model to support multiple roles (4h)

**Step 1: Ask Mode (Impact Analysis)**
→ Command: "Ask Mode. If we change the User model from single role to multiple roles, what parts of the system will be affected?"

→ Ask Mode output:
  - Affected components:
    1. Authentication middleware (checks user.role)
    2. Authorization guards (checks permissions)
    3. User registration (assigns default role)
    4. Admin panel (displays user roles)
    5. Database migrations (schema change)
  
  - Migration strategy:
    1. Add new roles table
    2. Create user_roles junction table
    3. Migrate existing role data
    4. Update all role checks
    5. Add backward compatibility layer
  
  - Risks:
    - Breaking changes in auth middleware
    - Need to update all role checks
    - Database migration required

**Step 2: Architect Mode (Design)**
→ Designs multi-role system with migration strategy

**Step 3: Code Mode (Implementation)**
→ Implements changes carefully

**Result:** ✅ Smooth refactoring with no surprises
```

---

## Best Practices

### ✅ Do:

- Use Ask Mode **before** making decisions on complex tasks
- Use Ask Mode to **understand existing code** before modifying
- Use Ask Mode to **explore options** when multiple approaches exist
- Use Ask Mode for **impact analysis** before large changes
- Combine Ask Mode with **Architect Mode** for best results

### ❌ Don't:

- Use Ask Mode for **simple, clear tasks** (overkill)
- Use Ask Mode when you **already know what to do**
- Expect Ask Mode to **write code** (use Code Mode)
- Expect Ask Mode to **fix bugs** (use Debug Mode)
- Skip Ask Mode for **complex, unclear tasks** (will cause problems)

---

## Combining with Other Modes

### Ask + Architect + Code

**Best for:** Complex features with multiple options

```
Ask Mode → Architect Mode → Code Mode → Debug Mode → Test Mode
```

**Example:** New authentication system

---

### Ask + Code

**Best for:** Simple features needing clarification

```
Ask Mode → Code Mode → Test Mode
```

**Example:** Add validation rules

---

### Ask + Debug

**Best for:** Complex bugs needing analysis

```
Ask Mode → Debug Mode
```

**Example:** Performance issue analysis

---

## Troubleshooting

### Ask Mode provides too much information

**Solution:**
- Be more specific in your question
- Focus on one aspect at a time
- Ask for summary or key points only

### Ask Mode doesn't understand the question

**Solution:**
- Provide more context
- Reference specific files or components
- Break down into smaller questions

### Ask Mode recommendations don't fit the project

**Solution:**
- Provide more project context
- Mention existing patterns and conventions
- Ask to consider current tech stack

---

## Summary

**Ask Mode is your analyst and advisor:**

- ✅ Use for analysis, understanding, and exploration
- ✅ Use BEFORE making decisions on complex tasks
- ✅ Part of Ask → Architect → Code → Debug workflow
- ✅ Focuses on insights and recommendations, not implementation
- ✅ Helps make informed decisions

**Remember:** 

```
Ask Mode = Analyze and understand
Architect Mode = Design and plan
Code Mode = Implement
Debug Mode = Fix problems
```

**Typical workflow:**

```
Ask (understand) → Architect (design) → Code (implement) → Debug (fix) → Test (validate)
```

---

## Related Guides

- **[Architect Mode Guide](ARCHITECT_MODE_GUIDE.md)** - How to use Architect Mode for system design
- **[Debug Mode Guide](DEBUG_MODE_GUIDE.md)** - How to use Debug Mode for problem-solving
- **[Kilo Code Sub-Task Mode Guide](KILOCODE_MODE_GUIDE.md)** - How to use Orchestrator Mode
- **[Kilo Code Complete Guide](KILO_CODE_COMPLETE_GUIDE.md)** - Complete guide for all Kilo Code modes
