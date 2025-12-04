# SmartSpec Troubleshooting Guide

This guide helps you diagnose and solve common errors when using SmartSpec workflows.

---

## 1. `generate_implement_prompt` Errors

This is the most complex workflow, so most errors occur here.

### Error: `Multiple platform flags detected`

- **Cause:** You used more than one of `--kilocode`, `--claude`, or `--roocode` at the same time.
- **Solution:** Use only ONE platform flag.
- **Example:**
  ```bash
  # ❌ WRONG
  /smartspec_generate_implement_prompt.md tasks.md --kilocode --claude

  # ✅ CORRECT
  /smartspec_generate_implement_prompt.md tasks.md --kilocode
  ```

---

### Error: `tasks.md not found`

- **Cause:** The path to your `tasks.md` file is incorrect.
- **Solution:**
  1. Check the file path is correct.
  2. Use a relative or absolute path.
  3. Make sure you are in the correct directory.
- **Example:**
  ```bash
  # ✅ CORRECT
  /smartspec_generate_implement_prompt.md specs/my-feature/tasks.md
  ```

---

### Error: `tasks.md is empty`

- **Cause:** The `tasks.md` file exists but has no content.
- **Solution:** Generate tasks first using `/smartspec_generate_tasks.md`.
- **Example:**
  ```bash
  # 1. Generate tasks
  /smartspec_generate_tasks.md specs/my-feature/plan.md

  # 2. Generate prompt
  /smartspec_generate_implement_prompt.md specs/my-feature/tasks.md --kilocode
  ```

---

### Error: `--nosubtasks can only be used with --kilocode`

- **Cause:** You used `--nosubtasks` with `--claude` or `--roocode`.
- **Solution:** `--nosubtasks` is a Kilo Code-only feature. Remove it or use `--kilocode`.
- **Example:**
  ```bash
  # ❌ WRONG
  /smartspec_generate_implement_prompt.md tasks.md --claude --nosubtasks

  # ✅ CORRECT (Kilo Code)
  /smartspec_generate_implement_prompt.md tasks.md --kilocode --nosubtasks

  # ✅ CORRECT (Claude Code)
  /smartspec_generate_implement_prompt.md tasks.md --claude
  ```

---

### Error: `--with-subagents can only be used with --claude`

- **Cause:** You used `--with-subagents` with `--kilocode` or `--roocode`.
- **Solution:** `--with-subagents` is a Claude Code-only feature. Remove it or use `--claude`.
- **Example:**
  ```bash
  # ❌ WRONG
  /smartspec_generate_implement_prompt.md tasks.md --kilocode --with-subagents

  # ✅ CORRECT (Claude Code)
  /smartspec_generate_implement_prompt.md tasks.md --claude --with-subagents

  # ✅ CORRECT (Kilo Code)
  /smartspec_generate_implement_prompt.md tasks.md --kilocode
  ```

---

### Error: `.claude/agents/ directory not found`

- **Cause:** You used `--with-subagents` but the standard agent files are missing.
- **Solution:** Copy the standard agents into your project.
- **Command:**
  ```bash
  cp -r .smartspec-docs/templates/claude-agents .claude/agents
  ```

---

### Error: `Invalid task range` or `Invalid phase range`

- **Cause:** The range format is incorrect (e.g., `T010-T001`, `3-1`).
- **Solution:** Use ascending order for ranges.
- **Example:**
  ```bash
  # ❌ WRONG
  --tasks T010-T001

  # ✅ CORRECT
  --tasks T001-T010
  ```

---

### Warning: `SPEC_INDEX.json is invalid`

- **Cause:** The `.smartspec/SPEC_INDEX.json` file has a JSON syntax error.
- **Solution:**
  1. The workflow will continue without dependency resolution.
  2. To fix, validate your `SPEC_INDEX.json` file using a JSON linter.
  3. Common errors: missing commas, extra commas, incorrect brackets.

---

### Warning: `Max dependency depth reached`

- **Cause:** Your project has a very deep dependency chain (more than 10 levels), or a circular dependency was not detected.
- **Solution:**
  1. The workflow will continue but may have incomplete context.
  2. Review your `SPEC_INDEX.json` and simplify dependencies.
  3. Check for circular dependencies (e.g., A → B → A).

---

### Error: `Circular dependency detected`

- **Cause:** Two or more specs depend on each other in a loop.
- **Solution:**
  1. The workflow will stop to prevent an infinite loop.
  2. Review the dependency chain shown in the error message.
  3. Refactor your specs to remove the circular dependency.

---

## 2. General Best Practices

- **Start simple:** Run workflows without parameters first.
- **Use `--dry-run`:** Add a `--dry-run` flag (coming soon) to preview without creating files.
- **Check the logs:** SmartSpec provides detailed logs to help you understand what it's doing.
- **Keep documents clean:** Ensure your `tasks.md` and `plan.md` files have correct formatting.

---

If you encounter an error not listed here, please report it as an issue on the GitHub repository.
