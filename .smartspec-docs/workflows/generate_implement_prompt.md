# Manual — Generate Implementation Prompt Workflow (Aligned with SmartSpec v5.2)

> This manual updates and replaces the original **generate_implement_prompt.md** instructions so they fully align with the authoritative workflow described in **smartspec_generate_implement_prompt.md**. It provides a complete, English-language reference for generating implementation prompts using centralized SmartSpec context, canonical registries, and optional UI JSON addendum.

---

## 1. Purpose
The `/generate_implement_prompt.md` command creates a **single, comprehensive implementation prompt file** from a project’s `tasks.md`. This prompt is intended for automated AI coding platforms such as:
- Claude Code
- Roo Code
- Kilo Code
- Gemini CLI
- Google Antigravity
- Other agent-based coding tools

This manual reflects the **canonical SmartSpec v5.2 workflow**:
- `.spec/` is the project-owned source of truth
- `.spec/SPEC_INDEX.json` defines canonical spec relationships
- `.spec/registry/` defines shared APIs, models, glossary terms, patterns, etc.
- `ui.json` (when present) is design-owned and must be respected

---

## 2. High-Level Workflow Summary
The workflow executed by this command includes:
1. **Resolving canonical index and registry paths**
2. **Reading the target `spec.md`, `tasks.md`, and UI JSON (if applicable)**
3. **Collecting dependency and cross-SPEC context**
4. **Applying registry rules to prevent name drift**
5. **Applying UI JSON rules when applicable**
6. **Structuring an implementation prompt** using the SmartSpec standard format
7. **Generating platform-specific instructions** (Kilo / Claude / Roo) when flags are provided

---

## 3. Usage
### Command
```bash
/smartspec_generate_implement_prompt.md <path_to_tasks.md> [options]
```

### Options
| Flag | Description | Default |
|------|-------------|---------|
| `--kilocode` | Include Kilo Code–specific workflow guidance | - |
| `--nosubtasks` | Disable automatic sub-task decomposition (Kilo only) | Enabled by default |
| `--claude` | Generate prompt optimized for Claude Code | claude |
| `--with-subagents` | Enable Claude Sub-Agent workflow (requires `.claude/agents/`) | Disabled |
| `--roocode` | Generate a prompt tuned for Roo Code | - |
| `--tasks <range>` | Select tasks (e.g., `T001-T010`) | All tasks |
| `--phase <range>` | Select phases | All phases |
| `--index` | Manually specify SPEC_INDEX | Auto-detect |
| `--registry-dir` | Manually specify registry directory | `.spec/registry` |
| `--spec` | Explicit spec path | Auto-detect |
| `--strict` | Stop execution if canonical conflicts are detected | Disabled |

---

## 4. Canonical SmartSpec Workflow
Below is the unified workflow sourced from SmartSpec v5.2.

### **4.1 Resolve Canonical Index & Registry**
- Detect `.spec/SPEC_INDEX.json` (canonical)
- Fallback to legacy or alternative paths
- Resolve `.spec/registry/` directory
- Validate presence of:
  - API registry
  - Model registry
  - Glossary
  - Critical sections
  - Patterns
  - UI component registry (if applicable)

**Rules:**
- **Do not create new shared names** (API/model/term/pattern) unless explicitly listed under *Pending Registry Additions*.

---

### **4.2 Identify Target Spec & Tasks**
- Use `--spec` or `--tasks` flags when provided
- Otherwise detect automatically based on file structure
- Default expected layout:
  - `spec.md`
  - `tasks.md`
  - `ui.json` (if UI spec)

---

### **4.3 Read Inputs (Read-Only)**
- Read `spec.md`
- Read `tasks.md`
- Detect and read `ui.json` when applicable

**Never write or modify these files.**

---

### **4.4 Compile Cross-SPEC Context**
If SPEC_INDEX exists:
- Load required dependency SPEC IDs
- Extract minimal required knowledge:
  - shared API prefixes
  - shared models
  - domain terminology
  - cross-cutting security or observability requirements

From registries:
- Extract only the relevant slices needed to perform the tasks

---

### **4.5 Consistency Gate (Pre-Prompt Checks)**
Before generating the final prompt:
- Validate task ordering against SPEC_INDEX dependencies
- Validate naming against registry entries
- Check for namespace duplication or conflicts
- If `--strict` is enabled: stop and list all conflicts

---

### **4.6 UI JSON Addendum (Conditional)**
Applied when:
- SPEC category = `ui`, or
- `ui.json` exists, or
- the spec explicitly uses a Penpot / UI JSON workflow

**UI JSON Rules:**
1. `ui.json` is **design-owned** (no business logic allowed)
2. Separate instructions into:
   - UI component mapping
   - UI rendering & state orchestration
   - Non-UI business logic
3. If UI component registry exists, component names must match
4. If project has no UI JSON:
   - fallback to textual UI instructions from `spec.md`

---

## 5. Output: Implementation Prompt Structure
All generated implementation prompts follow a consistent structure:

1. **Role & Objective**
2. **Canonical Context**
3. **Non-Negotiable Constraints**
4. **Spec Summary**
5. **Dependencies**
6. **Canonical Names (Do Not Rename)**
7. **Implementation Tasks (Ordered)**
8. **Testing Expectations**
9. **UI JSON Rules (If Applicable)**
10. **Pending Registry Additions**
11. **Definition of Done**

This structure ensures that all coding agents execute consistently and without drifting from project-wide conventions.

---

## 6. Platform-Specific Extensions
### **6.1 Kilo Code Mode**
When `--kilocode` is provided:
- Enable Orchestrator Mode (default)
- Auto-subtask decomposition unless `--nosubtasks` is used
- Provide Kilo-specific execution steps

### **6.2 Claude Code Mode**
When `--claude` is provided:
- Add Claude-specific prompt guidance
- If `--with-subagents` is set:
  - Add instructions for planner/db/backend/api/tester/security sub-agents

### **6.3 Roo Code Mode**
When `--roocode` is provided:
- Add Roo-style instructions for code generation and validation

---

## 7. Example Implementation Prompt Template
A concise, canonical example:

```text
You are implementing SmartSpec: <SPEC_ID> - <TITLE>.

Canonical context:
- SPEC_INDEX: <INDEX_PATH or NONE>
- Registry dir: <REGISTRY_DIR or NONE>

Hard rules:
- Use canonical names from registries when available.
- Do not introduce new shared API/model/term names without listing them under "Pending Registry Additions".
- Respect dependency order from SPEC_INDEX.
- Do not alter public contracts without a phased migration plan.

Spec objectives:
- <short bullet list>

Dependencies:
- <dep-1> (why it matters)
- <dep-2>

Canonical names:
- APIs: <list>
- Models: <list>
- Terms: <list>
- Patterns: <list>

Implementation tasks (from tasks.md):
1) <task 1>
2) <task 2>
...

Testing:
- Unit, Integration, Contract, Security, Performance

UI JSON (if applicable):
- Treat ui.json as design-owned
- Map UI nodes to registry-named components
- Keep business logic outside UI JSON

Pending Registry Additions:
- <item 1>

Definition of Done:
- All tasks completed
- No registry drift introduced
- All tests pass
- UI JSON rules satisfied (if applicable)
```

---

## 8. Summary
This updated manual fully aligns with the canonical SmartSpec v5.2 workflow and provides:
- Registry-aware implementation
- Cross-SPEC dependency enforcement
- UI JSON workflow support
- Platform-specific extensions

It ensures that all generated implementation prompts are consistent, conflict-resistant, and ready for automated AI coding execution.

If you want, I can also generate:
- A shorter TL;DR version
- A version tailored for junior devs
- A version tailored for PMs or architects
- A comparison between Cursor vs Implement prompt workflows

