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

### Breakdown Algorithm

**Step 1: Calculate subtask count**
```
target_hours = 3  // optimal subtask size
subtask_count = ceil(task.time_hours / target_hours)
hours_per_subtask = task.time_hours / subtask_count
```

**Step 2: Analyze task components**
```
Analyze task.description and task.files:
- Identify logical components
- Group related files
- Identify dependencies between components
```

**Step 3: Generate subtasks**
```
Example:
T050: Implement authentication system (12h)
→ 4 subtasks (3h each)

T050.1: Create User model and database schema (3h)
  Files: src/models/User.ts, prisma/schema.prisma
  Dependencies: None

T050.2: Implement AuthService with login/register (3h)
  Files: src/services/AuthService.ts
  Dependencies: T050.1

T050.3: Create AuthController and API endpoints (3h)
  Files: src/controllers/AuthController.ts, src/routes/auth.ts
  Dependencies: T050.2

T050.4: Add auth middleware and tests (3h)
  Files: src/middleware/auth.ts, tests/auth.test.ts
  Dependencies: T050.3
```

**Step 4: Update selected_tasks**
```
Replace T050 with [T050.1, T050.2, T050.3, T050.4]
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
