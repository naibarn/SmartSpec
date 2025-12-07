---
description: Generate user-friendly prompts from tasks.md for Cursor/Antigravity vibe coding. Converts technical tasks into simple, step-by-step instructions with context preservation, subtask breakdown, and platform-specific optimizations.
---

## User Input
```text
$ARGUMENTS
```

**Patterns:**
- `specs/feature/spec-004/tasks.md --task T001`
- `specs/feature/spec-004/tasks.md --task T001,T002,T003`
- `specs/feature/spec-004/tasks.md --task T001-T010`
- `specs/feature/spec-004/tasks.md --task T050 --breakdown`
- `specs/feature/spec-004/tasks.md --subtask T050.1,T050.2,T050.3`
- `specs/feature/spec-004/tasks.md --task T011-T020 --skip-completed`
- `specs/feature/spec-004/tasks.md --task T001 --antigravity`
- `specs/feature/spec-004/tasks.md --all`

**Default Behavior:**
- Platform: `--cursor` (if not specified)
- Task: Must specify (required)
- Output: Single file `cursor-prompt-<tasks>.md`
- Breakdown: Manual (use --breakdown for auto)
- Skip completed: false (use --skip-completed to enable)

## 0. Parse Arguments

**Extract parameters:**
```
Input: specs/feature/spec-004/tasks.md --task T001,T002,T003 --cursor

Parse:
- tasks_file: "specs/feature/spec-004/tasks.md"
- task_selection: "T001,T002,T003"
- platform: "cursor"
- breakdown: false
- skip_completed: false
- subtask_selection: null
- all_tasks: false
```

**Validation:**
- [ ] tasks.md path exists
- [ ] At least one of: --task, --subtask, or --all specified
- [ ] Platform is valid (cursor or antigravity)
- [ ] Task IDs are valid format (T001, T002, etc.)

**If validation fails:**
- Show error message
- Show usage examples
- Stop execution

## 1. Read tasks.md

**Parse YAML frontmatter:**
```yaml
---
spec_id: spec-004-financial-system
version: 1.0.0
technology_stack: TypeScript, Node.js, PostgreSQL
validation_commands:
  compile: "tsc --noEmit"
  test: "npm test -- {test_file}"
  lint: "npm run lint"
---
```

**Parse structure:**
- Project metadata
- Phase overview table
- All phases with tasks
- Task details (ID, title, description, time, files, dependencies, etc.)

**Extract per task:**
```
Task {
  id: "T001"
  title: "Create User entity"
  description: "..."
  time_hours: 2
  phase: 1
  phase_name: "Database Layer"
  files: [
    {path: "src/models/User.ts", operation: "CREATE", size: "SMALL"}
  ]
  dependencies: []
  acceptance_criteria: [...]
  risks: "LOW"
  completed: false  // from checkbox [ ] or [x]
}
```

**Build task registry:**
```
TaskRegistry = {
  "T001": Task {...},
  "T002": Task {...},
  ...
}
```

## 2. Select Tasks

### Pattern 1: Single Task

```
--task T001
→ selected_tasks = ["T001"]
```

### Pattern 2: Multiple Tasks (Comma-Separated)

```
--task T001,T002,T003
→ Parse comma-separated list
→ selected_tasks = ["T001", "T002", "T003"]
```

### Pattern 3: Task Range

```
--task T001-T010
→ Parse range (start: T001, end: T010)
→ Extract all tasks between T001 and T010
→ selected_tasks = ["T001", "T002", ..., "T010"]
```

### Pattern 4: Subtasks

```
--subtask T050.1,T050.2,T050.3
→ Parse subtask IDs
→ selected_tasks = ["T050.1", "T050.2", "T050.3"]
```

### Pattern 5: All Tasks

```
--all
→ selected_tasks = [all task IDs from tasks.md]
→ Generate one prompt per task
```

**Filter if --skip-completed:**
```
FOR each task IN selected_tasks:
  IF task.completed == true:
    Remove from selected_tasks
```

**Validation:**
- [ ] All selected task IDs exist in TaskRegistry
- [ ] Tasks are in sequential order
- [ ] No duplicate task IDs

## 3. Breakdown Large Tasks (if --breakdown)

**For each selected task:**
```
IF task.time_hours > 8 AND --breakdown flag:
  → Apply breakdown algorithm
  → Generate subtasks
  → Replace task with subtasks in selected_tasks
```

### Breakdown Algorithm (Enhanced with Smart Time Estimation)

**Step 1: Analyze task complexity**
```
complexity_score = calculate_task_complexity(task)

Factors:
- file_count: len(task.files)
- avg_file_size: average of file.size_lines (if available)
- risk_level: HIGH=3, MEDIUM=2, LOW=1
- dependency_count: len(task.dependencies)

Formula:
complexity = (file_count * 0.3) + (avg_file_size/100 * 0.2) + 
             (risk_level * 0.3) + (dependency_count * 0.2)

Normalize to 1-10 scale:
- 1-3: Simple task
- 4-7: Medium complexity
- 8-10: High complexity
```

**Step 2: Analyze component complexity**
```
FOR each component IN components:
  component_complexity = calculate_component_complexity(component)
  
  Type multipliers:
  - Model: 1.0 (simple data structures)
  - Service: 1.5 (business logic)
  - Controller: 1.3 (API handling)
  - Middleware: 1.2 (cross-cutting concerns)
  - Tests: 0.8 (straightforward testing)
  - Integration: 2.0 (external dependencies)
  
  Base factors:
  - file_count: number of files in component
  - external_deps: external libraries/APIs used
  - file_relationships: imports between files
  
  component_complexity = (base_score) * type_multiplier
  
Example:
- User model (1 file, no deps): 2 * 1.0 = 2
- AuthService (1 file, uses bcrypt): 4 * 1.5 = 6
- AuthController (2 files, uses service): 3 * 1.3 = 4
- Auth middleware (1 file, uses JWT): 3 * 1.2 = 4
- Tests (1 file, uses jest): 2 * 0.8 = 2

Total complexity: 2 + 6 + 4 + 4 + 2 = 18
```

**Step 3: Distribute time proportionally**
```
total_complexity = sum(component_complexity for all components)

FOR each component:
  ratio = component_complexity / total_complexity
  component_hours = task.time_hours * ratio
  
  # Ensure bounds (subtasks should be 1.5h - 5h)
  component_hours = max(1.5, min(5, component_hours))

# Adjust to match total hours
subtask_hours_sum = sum(component_hours)
IF subtask_hours_sum != task.time_hours:
  scale_factor = task.time_hours / subtask_hours_sum
  FOR each component:
    component_hours *= scale_factor

Example (12h task):
- Model: 12h * (2/18) = 1.3h → 1.5h (min bound)
- Service: 12h * (6/18) = 4h → 4h
- Controller: 12h * (4/18) = 2.7h → 2.7h
- Middleware: 12h * (4/18) = 2.7h → 2.7h
- Tests: 12h * (2/18) = 1.3h → 1.5h (min bound)

Sum: 12.4h (need to scale)
Scale: 12/12.4 = 0.968

Final:
- Model: 1.5h * 0.968 = 1.5h
- Service: 4h * 0.968 = 3.9h → 4h
- Controller: 2.7h * 0.968 = 2.6h → 3h
- Middleware: 2.7h * 0.968 = 2.6h → 2h
- Tests: 1.5h * 0.968 = 1.5h → 1h

Total: 11.5h ≈ 12h ✅

Note: Time is distributed based on complexity, not equally!
```

**Step 4: Analyze task components**
```
Analyze task.description and task.files:
- Identify logical components (Model, Service, Controller, etc.)
- Group related files by component
- Identify dependencies between components
- Assign complexity scores (from Step 2)
- Assign time estimates (from Step 3)
```

**Step 5: Generate subtasks**
```
Example (with Smart Time Estimation):
T050: Implement authentication system (12h)

Complexity analysis:
- Model: 2/18 complexity → 1.5h (simple)
- Service: 6/18 complexity → 4h (complex, business logic)
- Controller: 4/18 complexity → 3h (medium)
- Middleware+Tests: 4/18 complexity → 3.5h → 3h (combined)

Subtasks:
T050.1: Create User model and database schema (1.5h)
  Files: src/models/User.ts, prisma/schema.prisma
  Dependencies: None
  Complexity: 2/10 (simple data structures)

T050.2: Implement AuthService with login/register (4h)
  Files: src/services/AuthService.ts
  Dependencies: T050.1
  Complexity: 6/10 (business logic, bcrypt, JWT)

T050.3: Create AuthController and API endpoints (3h)
  Files: src/controllers/AuthController.ts, src/routes/auth.ts
  Dependencies: T050.2
  Complexity: 4/10 (API handling, validation)

T050.4: Add auth middleware and tests (3.5h)
  Files: src/middleware/auth.ts, tests/auth.test.ts
  Dependencies: T050.2
  Complexity: 4/10 (JWT verification, test coverage)

Total: 12h ✅
Note: Time distributed by complexity (not equal 3h each!)
```

**Step 6: Update selected_tasks**
```
Replace T050 with [T050.1, T050.2, T050.3, T050.4]
```

### Quality Validation (Phase 5)

**Step 7: Validate subtask quality**

Before finalizing subtasks, run comprehensive validation:

**Validation 1: Count Check**
```
IF subtask_count < 2:
  ERROR: "Too few subtasks (minimum 2 required)"
  STOP

IF subtask_count > 8:
  WARNING: "Too many subtasks ({count}), consider grouping related components"
  # Continue but warn user
```

**Validation 2: Time Balance Check**
```
max_hours = max(subtask.hours for all subtasks)
min_hours = min(subtask.hours for all subtasks)
ratio = max_hours / min_hours

IF ratio > 3:
  WARNING: "Unbalanced subtasks (ratio: {ratio:.1f})"
  
  # Find candidates to combine
  small_subtasks = [s for s in subtasks if s.hours < 2]
  
  IF len(small_subtasks) >= 2:
    SUGGEST: "Consider combining {small_subtasks[0].id} ({small_subtasks[0].hours}h) 
              and {small_subtasks[1].id} ({small_subtasks[1].hours}h)"
    
    # Auto-fix option
    IF auto_fix_enabled:
      combined_subtask = merge(small_subtasks[0], small_subtasks[1])
      combined_subtask.hours = small_subtasks[0].hours + small_subtasks[1].hours
      combined_subtask.files = small_subtasks[0].files + small_subtasks[1].files
      
      Remove small_subtasks[0] and small_subtasks[1]
      Add combined_subtask
      
      RE-VALIDATE

Example:
Before: T050.1 (1.5h), T050.2 (4h), T050.3 (3h), T050.4 (1.5h)
Ratio: 4/1.5 = 2.67 (< 3) ✅ Good balance

Bad example: T060.1 (1h), T060.2 (5h), T060.3 (3h)
Ratio: 5/1 = 5 (> 3) ⚠️ Unbalanced
Suggestion: Combine T060.1 with another small task
```

**Validation 3: Dependency Check**
```
# Check all dependencies exist and are in correct order
FOR each subtask IN subtasks:
  FOR each dependency IN subtask.dependencies:
    IF dependency NOT IN previous_subtasks:
      ERROR: "{subtask.id} depends on {dependency} which comes after it or doesn't exist"
      STOP

# Check for circular dependencies
dependency_graph = build_graph(subtasks)
IF has_cycle(dependency_graph):
  ERROR: "Circular dependency detected"
  cycles = find_cycles(dependency_graph)
  SHOW: "Cycle: {' → '.join(cycles)} → {cycles[0]}"
  STOP

Example:
Valid:
- T050.1 (no deps)
- T050.2 (depends on T050.1) ✅
- T050.3 (depends on T050.2) ✅

Invalid:
- T050.1 (depends on T050.3) ❌
- T050.2 (depends on T050.1) ✅
- T050.3 (depends on T050.2) ✅
Error: T050.1 depends on T050.3 which comes after it

Circular:
- T050.1 (depends on T050.3)
- T050.2 (depends on T050.1)
- T050.3 (depends on T050.2)
Error: Cycle: T050.1 → T050.3 → T050.2 → T050.1
```

**Validation 4: Completeness Check**
```
original_files = set(original_task.files)
subtask_files = set(file for subtask in subtasks for file in subtask.files)

missing = original_files - subtask_files
extra = subtask_files - original_files

IF missing:
  WARNING: "Missing files in subtasks: {missing}"
  SUGGEST: "Add missing files to appropriate subtasks"

IF extra:
  WARNING: "Extra files in subtasks (not in original): {extra}"
  SUGGEST: "Remove extra files or add to original task"

Example:
Original files: [User.ts, AuthService.ts, AuthController.ts, auth.ts, auth.test.ts]
Subtask files: [User.ts, AuthService.ts, AuthController.ts, auth.ts, auth.test.ts]
Result: ✅ All files covered

Bad example:
Original files: [User.ts, AuthService.ts, AuthController.ts]
Subtask files: [User.ts, AuthService.ts]
Missing: [AuthController.ts]
Warning: AuthController.ts not assigned to any subtask
```

**Validation 5: Component Coverage Check**
```
required_components = detect_required_components(original_task)
subtask_components = [subtask.component for subtask in subtasks]

FOR component IN required_components:
  IF component NOT IN subtask_components:
    WARNING: "Missing component: {component}"
    SUGGEST: "Add subtask for {component} or merge with existing subtask"

Example:
Required: [Model, Service, Controller, Tests]
Subtasks: [Model, Service, Controller, Tests]
Result: ✅ All components covered

Bad example:
Required: [Model, Service, Controller, Middleware, Tests]
Subtasks: [Model, Service, Controller]
Missing: [Middleware, Tests]
Warning: Middleware and Tests components not covered
```

**Validation 6: Provide Suggestions**
```
suggestions = []

# Suggestion 1: Combine small subtasks
IF ratio > 3 AND len(small_subtasks) >= 2:
  suggestions.append({
    type: "COMBINE",
    message: "Combine small subtasks to balance workload",
    subtasks: small_subtasks,
    action: "Merge {small_subtasks[0].id} and {small_subtasks[1].id}"
  })

# Suggestion 2: Split large subtasks
large_subtasks = [s for s in subtasks if s.hours > 5]
IF large_subtasks:
  suggestions.append({
    type: "SPLIT",
    message: "Consider splitting large subtasks (>5h)",
    subtasks: large_subtasks,
    action: "Split {large_subtasks[0].id} into smaller tasks"
  })

# Suggestion 3: Reorder for dependencies
IF dependency_order_errors:
  suggestions.append({
    type: "REORDER",
    message: "Reorder subtasks to satisfy dependencies",
    action: "Move dependent subtasks after their dependencies"
  })

# Suggestion 4: Add missing components
IF missing_components:
  suggestions.append({
    type: "ADD_COMPONENT",
    message: "Add missing components",
    components: missing_components,
    action: "Create subtasks for {', '.join(missing_components)}"
  })

RETURN validation_result = {
  valid: all_checks_passed,
  errors: errors,
  warnings: warnings,
  suggestions: suggestions
}

IF errors:
  SHOW errors
  STOP (do not generate prompts)

IF warnings:
  SHOW warnings and suggestions
  IF auto_fix_available:
    APPLY auto-fixes
    RE-VALIDATE
  ELSE:
    CONTINUE (generate prompts with warnings)
```

**Validation Summary Output:**
```
Example output:

✅ Validation Results for T050 Breakdown:

✅ Count: 4 subtasks (2-8 range)
✅ Balance: max 4h, min 1.5h, ratio 2.67 (< 3)
✅ Dependencies: Valid order, no circular dependencies
✅ Completeness: All 5 files covered
✅ Coverage: All components present (Model, Service, Controller, Tests)

✅ All validations passed! Proceeding with prompt generation.

---

Bad example output:

⚠️ Validation Results for T060 Breakdown:

✅ Count: 3 subtasks (2-8 range)
❌ Balance: max 5h, min 1h, ratio 5.0 (> 3) - UNBALANCED
✅ Dependencies: Valid order
⚠️ Completeness: Missing 1 file (middleware.ts)
⚠️ Coverage: Missing component (Middleware)

⚠️ Warnings found. Suggestions:
1. Combine T060.1 (1h) and T060.3 (2h) to balance workload
2. Add middleware.ts to appropriate subtask
3. Create subtask for Middleware component

Apply auto-fixes? [Y/n]
```

## 4. Build Context for Each Task

**For each task in selected_tasks:**

### Context Type 1: Previous Tasks

```
previous_tasks = []
FOR each task IN TaskRegistry:
  IF task.id < current_task.id:
    IF task.completed OR task IN selected_tasks:
      Add to previous_tasks
```

### Context Type 2: Dependencies

```
dependencies = current_task.dependencies
FOR each dep IN dependencies:
  Resolve dep from TaskRegistry
  Check if completed
```

### Context Type 3: Files Created

```
files_created_before = []
FOR each prev_task IN previous_tasks:
  FOR each file IN prev_task.files:
    IF file.operation == "CREATE":
      Add to files_created_before
```

### Context Type 4: Phase Info

```
phase_info = {
  phase_number: current_task.phase
  phase_name: current_task.phase_name
  phase_tasks: [all tasks in same phase]
  phase_progress: "X of Y tasks"
}
```

**Build complete context:**
```
Context {
  previous_tasks: [...]
  dependencies: [...]
  files_created_before: [...]
  phase_info: {...}
  tech_stack: [from frontmatter]
  validation_commands: [from frontmatter]
}
```

## 5. Generate Prompt

### Output Filename

**Single Task:**
```
cursor-prompt-T001.md
```

**Multiple Tasks:**
```
cursor-prompt-T001-T003.md
```

**Task Range:**
```
cursor-prompt-T001-T010.md
```

**Subtasks:**
```
cursor-prompt-T050.1-T050.3.md
```

**All Tasks (one file per task):**
```
cursor-prompt-T001.md
cursor-prompt-T002.md
...
```

### Prompt Template Selection

**If single task:**
→ Use Single Task Template

**If multiple tasks:**
→ Use Multiple Tasks Template

**If --all:**
→ Use Single Task Template for each task

---

## 6. Single Task Template

```markdown
# Task {task.id}: {task.title}

## 🎯 What You'll Build

{Simple, non-technical description of what this task accomplishes}

{Explain the purpose and value of this task}

## 📋 Context

**Phase:** Phase {phase_number} - {phase_name}
**Position:** {position in phase} of {total tasks in phase}
**Dependencies:** {list dependencies or "None"}

{IF previous_tasks exist:}
**What you've built so far:**

{FOR each prev_task IN previous_tasks:}
In {prev_task.id}, you created:
- {prev_task.title}
- {list key files created}
- {brief description of what was accomplished}

{IF dependencies exist:}
**This task depends on:**
{FOR each dep IN dependencies:}
- ✅ {dep.id}: {dep.title} {IF dep.completed: "(completed)" ELSE: "(must complete first)"}

{IF files_created_before exist:}
**Files you'll use:**
{FOR each file IN files_created_before:}
- `{file.path}` (from {file.task_id})

{IF dependent_tasks exist:}
**What comes after:**
{FOR each dep_task IN dependent_tasks:}
- {dep_task.id} will use the code you create here

## 🔧 Implementation Steps

{Generate step-by-step instructions based on task.description and task.files}

### Step 1: {First major step}

{Detailed instructions for this step}

{IF creating file:}
Create a new file: `{file.path}`

{IF editing file:}
Edit existing file: `{file.path}`

### Step 2: {Second major step}

{Detailed instructions}

{Continue for all major steps...}

### Step {N}: {Final step}

{Final instructions}

{IF validation needed:}
Validate your implementation (see Validation section below)

## 💻 Code Structure

{IF task involves code:}
Here's the basic structure your code should follow:

```{language}
// {file.path}

{Generate code skeleton/structure based on task.description}

{Show:}
- Class/function signatures
- Key properties/methods
- Important logic (as comments)
- Imports needed
```

{Explain the structure}

## 📁 Files

**Create:**
{FOR each file IN task.files WHERE operation == "CREATE":}
- `{file.path}` (~{file.size_lines} lines, {file.size_category})

**Edit:**
{FOR each file IN task.files WHERE operation == "EDIT":}
- `{file.path}` (add {file.changes_description})

**Use:**
{FOR each file IN files_created_before THAT this task uses:}
- `{file.path}` (from {file.task_id})

## ✅ Validation

After implementing, run these commands to validate:

```bash
# Check TypeScript compilation
{validation_commands.compile}

# Run tests
{validation_commands.test}

# Check linting
{validation_commands.lint}
```

**Expected Results:**
- ✅ No compilation errors
- ✅ All tests passing
- ✅ No lint errors

{IF task.acceptance_criteria exist:}
**Acceptance Criteria:**
{FOR each criterion IN task.acceptance_criteria:}
- [ ] {criterion}

## ⏱️ Estimated Time

**{task.time_hours} hours**

{IF task.time_hours >= 3:}
This includes:
- Planning and setup ({10% of time})
- Implementation ({60% of time})
- Testing and validation ({20% of time})
- Documentation ({10% of time})

## ➡️ Next Steps

After completing this task:

1. **Validate your implementation** using the commands above
2. **Mark task as complete** in tasks.md: `- [x] {task.id}`
3. **Commit your changes** to version control

{IF next_task exists:}
4. **Move to {next_task.id}**: {next_task.title}
   {IF next_task depends on current task:}
   - {next_task.id} will use the code you created here
   - Make sure everything is working before proceeding

{IF task.risks != "LOW":}
## ⚠️ Important Notes

**Risk Level:** {task.risks}

{IF task.risks == "HIGH":}
This task has high impact on the system. Be extra careful:
- Test thoroughly before proceeding
- Consider creating a backup/branch
- Review changes carefully

{IF task.risks == "MEDIUM":}
This task has moderate complexity:
- Follow the steps carefully
- Validate after each major step
- Ask for help if needed

## 💡 Tips

{Generate platform-specific tips based on platform flag}

{IF platform == "cursor":}
**Cursor Tips:**
- Use `Cmd+K` (Mac) or `Ctrl+K` (Windows) to ask Cursor for help
- Use `Cmd+L` to select code and ask questions
- Use Tab to accept inline suggestions
- Use `Cmd+Shift+P` for command palette

**Cursor Workflow:**
1. Create the file(s) listed above
2. Start typing the class/function name
3. Let Cursor suggest the structure
4. Accept suggestions with Tab
5. Ask Cursor for help: "Add {specific feature}"
6. Review and refine suggestions

{IF platform == "antigravity":}
**Antigravity Tips:**
- Use AI pair programming mode
- Ask for code review after implementation
- Request refactoring suggestions
- Generate tests automatically

**Antigravity Workflow:**
1. Start pair programming session
2. Describe what you want to build
3. Review AI suggestions
4. Accept or modify
5. Ask for code review
6. Request test generation

{IF task has common pitfalls:}
## 🚨 Common Pitfalls

{List common mistakes to avoid}

## 🔗 Dependencies

**This task depends on:**
{IF dependencies exist:}
{FOR each dep IN dependencies:}
- {dep.id}: {dep.title}
{ELSE:}
- None (this is a starting point)

**Tasks that depend on this:**
{IF dependent_tasks exist:}
{FOR each dep_task IN dependent_tasks:}
- {dep_task.id}: {dep_task.title}
{ELSE:}
- None (this is an endpoint)

---

**Platform:** {platform_name}
**Generated:** {current_date}
**Source:** {tasks_file_path}
**Spec:** {spec_id} v{version}
```

---

## 7. Multiple Tasks Template

```markdown
# Tasks {first_task.id}-{last_task.id}: {phase_name or combined_title}

## 🎯 Overview

{High-level description of what these tasks accomplish together}

**Phase:** Phase {phase_number} - {phase_name}
**Total Time:** {sum of all task hours} hours
**Tasks:** {count} tasks

{IF dependencies exist:}
**Prerequisites:**
{List tasks that must be completed before starting}

---

{FOR each task IN selected_tasks:}

## Task {task.id}: {task.title}

### 🎯 What You'll Build

{Simple description}

### 📋 Context

{IF previous tasks in selection:}
**Builds on:**
{List previous tasks in this selection}

{IF dependencies outside selection:}
**Depends on:**
{List external dependencies}

{IF files from previous tasks:}
**Files from previous tasks:**
{List files created in previous tasks}

### 🔧 Implementation Steps

{Step-by-step instructions}

#### Step 1: {First step}
{Instructions}

#### Step 2: {Second step}
{Instructions}

{Continue...}

### 💻 Code Structure

```{language}
{Code skeleton}
```

### 📁 Files

**Create:**
{List files to create}

**Edit:**
{List files to edit}

**Use:**
{List files from previous tasks}

### ⏱️ Time: {task.time_hours} hours

---

{END FOR each task}

## ✅ Validation (All Tasks)

After completing all tasks, run:

```bash
{validation_commands.compile}
{validation_commands.test}
{validation_commands.lint}
```

**Expected Results:**
- ✅ All tasks completed
- ✅ No compilation errors
- ✅ All tests passing
- ✅ No lint errors

## 📊 Progress Tracking

{FOR each task IN selected_tasks:}
- [ ] {task.id}: {task.title} ({task.time_hours}h)

**Total:** {total_hours} hours

## ➡️ Next Steps

After completing all {count} tasks:

1. Validate all implementations
2. Mark all tasks as complete in tasks.md
3. Commit changes to version control

{IF next_phase exists:}
4. Move to Phase {next_phase.number}: {next_phase.name}

{IF next_tasks exist:}
4. Continue with next tasks: {next_tasks_list}

## 💡 Tips

{Platform-specific tips}

{Workflow suggestions}

---

**Platform:** {platform_name}
**Generated:** {current_date}
**Source:** {tasks_file_path}
**Spec:** {spec_id} v{version}
```

---

## 8. Generate Output

**Write prompt file:**
```
output_path = TASKS_DIR / output_filename
Write prompt content to output_path
```

**If --all (multiple files):**
```
FOR each task IN selected_tasks:
  output_filename = f"cursor-prompt-{task.id}.md"
  Generate single task prompt
  Write to output_path
```

## 9. Report Success

```markdown
✅ Prompt generated successfully!

📁 File: {output_filename}
📊 Tasks: {count} ({task_ids_list})
⏱️ Time: {total_hours} hours
🎯 Platform: {platform_name}

{IF breakdown occurred:}
🔄 Breakdown applied:
{FOR each original_task that was broken down:}
- {original_task.id} ({original_task.hours}h) → {subtask_count} subtasks
  {List subtasks}

{IF tasks were skipped:}
⏭️ Skipped (completed):
{List skipped tasks}

📋 Tasks included:
{FOR each task IN selected_tasks:}
- {task.id}: {task.title} ({task.time_hours}h)

{IF dependencies not met:}
⚠️ Dependencies:
{FOR each task WITH unmet dependencies:}
- {task.id} depends on {dependency_ids} (not yet completed)
  → Complete dependencies first

💡 Next steps:

{IF platform == "cursor":}
**For Cursor:**
1. Open {output_filename}
2. Copy the prompt content
3. Open Cursor
4. Paste the prompt in Cursor chat
5. Start implementing!

{IF platform == "antigravity":}
**For Antigravity:**
1. Open {output_filename}
2. Copy the prompt content
3. Open Antigravity
4. Start pair programming session
5. Paste the prompt
6. Begin implementation!

{IF multiple files generated:}
**Multiple prompts generated:**
{FOR each file IN output_files:}
- {file.name} ({file.task_id}, {file.hours}h)

Start with the first file and work sequentially.

📚 Documentation:
- Analysis: CURSOR_ANTIGRAVITY_ANALYSIS.md
- Architecture: CURSOR_PROMPT_ARCHITECTURE.md

🔗 Related workflows:
- Generate implement prompt: /smartspec_generate_implement_prompt
- Implement tasks: /smartspec_implement_tasks
```

---

## Error Handling

### Error: No tasks specified

```
❌ Error: No tasks specified

You must specify which tasks to generate prompts for.

Usage:
  --task T001              (single task)
  --task T001,T002,T003    (multiple tasks)
  --task T001-T010         (task range)
  --subtask T050.1,T050.2  (subtasks)
  --all                    (all tasks)

Example:
  /smartspec_generate_cursor_prompt tasks.md --task T001
```

### Error: Task not found

```
❌ Error: Task not found

Task ID "T999" does not exist in tasks.md

Available tasks:
- T001: Create User entity
- T002: Create AuthService
- T003: Setup database
...

Please check the task ID and try again.
```

### Error: Unmet dependencies

```
⚠️ Warning: Unmet dependencies

Task T003 depends on:
- T001: Create User entity (not completed)
- T002: Create AuthService (not completed)

Recommendation:
1. Complete T001 and T002 first, OR
2. Generate prompt for T001-T003 together, OR
3. Use --skip-completed to filter

Continue anyway? (y/n)
```

### Error: Invalid task range

```
❌ Error: Invalid task range

Range "T010-T001" is invalid (end before start)

Valid format:
  --task T001-T010  (start must be before end)

Please correct the range and try again.
```

---

## Platform-Specific Optimizations

### Cursor Optimizations

**Prompt Features:**
- Inline code suggestions
- Tab completion hints
- Command palette shortcuts
- Multi-file editing tips

**Workflow Guidance:**
- Use Cmd+K for questions
- Use Tab for suggestions
- Use Cmd+L for code selection

### Antigravity Optimizations

**Prompt Features:**
- Pair programming mode
- Code review requests
- Refactoring suggestions
- Test generation

**Workflow Guidance:**
- Start pair programming
- Request code reviews
- Ask for refactoring
- Generate tests automatically

---

## Notes

**Design Principles:**
1. **Simplicity** - Use non-technical language
2. **Clarity** - Step-by-step instructions
3. **Context** - Preserve dependencies and history
4. **Examples** - Include code structure
5. **Validation** - Clear verification steps

**Target Audience:**
- Developers using Cursor/Antigravity
- Prefer vibe coding over autonomous agents
- Want clear, simple instructions
- Need context preservation

**Integration:**
- Works with existing tasks.md format
- Compatible with Kilo Code workflow
- Supports hybrid workflows
- Enables platform switching

**Future Enhancements:**
- Interactive mode (ask user for tasks)
- Progress tracking (mark completed)
- Batch generation (all tasks at once)
- Custom templates (user-defined)
- AI-powered breakdown (smarter subtask generation)

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
