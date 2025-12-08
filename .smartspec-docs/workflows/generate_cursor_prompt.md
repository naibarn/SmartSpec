# Manual — Generate Cursor Prompt Workflow (English Version)

> This manual has been rewritten entirely in English and aligned with the workflow described in **smartspec_generate_cursor_prompt.md**, including canonical context resolution, registry alignment, cross‑SPEC context loading, UI JSON rules, and optimized Cursor‑ready prompt generation.

---

## 1. Overview
The **/generate_cursor_prompt.md** command produces a series of clean, human‑readable prompts suitable for manual, step‑by‑step execution in environments like **Cursor IDE** or **Google Antigravity**.  
This updated version now fully follows SmartSpec’s centralized workflow:

- Detect canonical **SPEC_INDEX**
- Load shared registries (API, models, glossary, UI components, etc.)
- Read `spec.md`, `tasks.md`, and `ui.json` (if present)
- Validate naming consistency across SPECs
- Generate conflict‑free prompts tailored for Cursor

---

## 2. Purpose of the Command
- Convert selected tasks into **individually executable prompts**
- Preserve canonical shared naming (APIs, models, domain terms)
- Ensure implementation is consistent with project‑wide context
- Support UI JSON specifications when applicable

---

## 3. Target Platforms & Execution Model
| Platform | How to Use | Workflow |
|---|---|---|
| **Cursor** | Copy and paste one prompt at a time | Manual / Interactive |
| **Antigravity** | Same copy‑paste flow | Manual / Interactive |

---

## 4. Usage
```bash
/generate_cursor_prompt.md <tasks_path> --tasks <task_id_or_range> [options...]
```

### Arguments
| Name | Type | Required | Description | Example |
|---|---|---|---|---|
| `tasks_path` | string | ✔ | Path to `tasks.md` | `specs/features/login/tasks.md` |

### Options
| Option | Value | Default | Description |
|---|---|---|---|
| `--tasks` | task ID(s) | ✔ | Select one or more tasks | `T001,T003` |
| `--cursor` | flag | Yes | Optimize prompt structure for Cursor |
| `--antigravity` | flag | - | Optimize prompts for Antigravity |
| `--breakdown` | flag | - | Auto‑split large tasks |

---

## 5. Integrated SmartSpec Workflow
The complete workflow from **smartspec_generate_cursor_prompt.md** is now applied to this command.

### **Step 0: Load Canonical Context**
- Resolve canonical **SPEC_INDEX**
- Load registries:
  - API registry
  - model registry
  - glossary
  - critical sections
  - patterns
  - UI component registry (if available)
- **No new shared names may be invented** unless declared in "Open Questions / Registry Additions".

### **Step 1: Identify Target Spec & Tasks**
- Read `spec.md`
- Read `tasks.md`
- Read `ui.json` if it exists

### **Step 2: Compile Cross‑SPEC Context**
- Extract dependency SPECs using SPEC_INDEX
- Summaries are concise and limited to context needed by tasks

### **Step 3: Consistency Validation**
- Validate naming against registries
- Validate task order against cross‑SPEC dependencies

### **Step 4: Build the Final Cursor Prompt File**
The generated prompt file must contain:
1. **Project Context**
2. **Target Spec Information** (ID, title, objective)
3. **Dependencies**
4. **Canonical Names (Do Not Rename)**
5. **Ordered Tasks**
6. **Testing Requirements**
7. **UI JSON Rules** (if applicable)
8. **Open Questions / Registry Additions**
9. **Definition of Done**

---

## 6. Output Format
The command generates a **single file** containing multiple prompts, clearly separated, e.g.:

```markdown
--- PROMPT FOR TASK T001 ---
...content...
---
--- PROMPT FOR TASK T002 ---
...content...
---
```

You then copy each section into Cursor **one prompt at a time**.

---

## 7. Examples
### Example 1: Generate prompts for task range
```bash
/generate_cursor_prompt.md specs/user/tasks.md --tasks T001-T003
```
Output: `cursor-prompt-T001-T003.md`

### Example 2: Use Antigravity mode
```bash
/generate_cursor_prompt.md specs/auth/tasks.md --tasks T010,T012 --antigravity
```
Output: prompts optimized for Antigravity

---

## 8. Troubleshooting
| Problem | Cause | Fix |
|---|---|---|
| Task not found | Wrong ID | Check tasks.md |
| Prompts too simple | tasks.md lacks detail | Add clearer steps |
| AI becomes confused | Multiple prompts pasted at once | Paste one at a time |

---

## 9. Final Notes
This manual unifies the original simple workflow with SmartSpec’s full canonical workflow:
- Registry‑aligned naming rules
- Cross‑SPEC context resolution
- UI JSON support
- Cursor‑optimized formatting

The result is a high‑quality, conflict‑free implementation prompt that guides Cursor toward consistent, correct output across large multi‑SPEC systems.

