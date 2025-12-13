---
description: Detect whether the current workflow is running on Kilo Code and report the active mode
version: 1.0
last_updated: 2025-12-08
---

# /smartspec_check_kilo_mode

Detect whether the current SmartSpec workflow is running on Kilo Code and report the active mode.

This workflow parses the `environment_details` block and prompt context to determine:
- If the session is running on Kilo Code
- The current active mode (Ask, Architect, Code, Debug, Orchestrator)
- Whether Kilo Code-specific flags (e.g., `--kilocode`, `--architect`) are in use
- If Orchestrator mode is managing subtasks

---

## What It Does

1) Parses the `environment_details` section for mode indicators
2) Checks prompt context for Kilo Code-specific flags
3) Detects Orchestrator activity when subtasks are present
4) Outputs a concise status report

---

## When to Use

- During any SmartSpec workflow to verify the execution environment
- Before switching modes manually to confirm current state
- When troubleshooting unexpected behavior
- To validate that `--kilocode` or `--architect` flags are active

---

## Inputs

- None (reads from current context)

---

## Outputs

- Console output with:
  - Kilo Code status (Yes/No)
  - Current mode
  - Active flags
  - Orchestrator status
  - Model information

---

## Flags

- `--json` Output results in JSON format for scripting
- `--quiet` Suppress explanatory text, show only key-value pairs

---

## Detection Logic

### 1) Environment Details Parsing

The workflow inspects these fields in `environment_details`:

```yaml
Current Mode:
  slug: <mode_slug>          # ask, architect, code, debug, orchestrator
  name: <mode_name>          # Ask, Architect, Code, Debug, Orchestrator
  model: <model_name>        # x-ai/grok-4.1-fast, etc.
```

### 2) Prompt Context Detection

Scans the current prompt for:
- `--kilocode` flag presence
- `--architect` flag presence
- Orchestrator keywords: "sub-task", "break into subtasks", "Orchestrator Mode"
- Mode prefixes: "Ask Mode.", "Use Architect Mode", "Use Debug Mode"

### 3) Detection Rules

| Indicator | Detection Method | Meaning |
|------------|------------------|---------|
| **Kilo Code Active** | `model` contains "kilo" OR prompt contains Kilo Code tools | Running on Kilo Code platform |
| **Current Mode** | `slug` from environment_details | Active execution mode |
| **Orchestrator Active** | Prompt contains orchestrator keywords AND subtasks are present | Orchestrator is managing workflow |
| **Flags Active** | Prompt contains `--kilocode`, `--architect` | Special execution modes enabled |

---

## Output Formats

### Standard Output

```
🤖 Kilo Code Status: Yes
📋 Current Mode: architect
🚀 Flags: --architect
🎯 Orchestrator: No
🧠 Model: x-ai/grok-4.1-fast
```

### JSON Output (`--json`)

```json
{
  "kilo_code_active": true,
  "current_mode": {
    "slug": "architect",
    "name": "Architect",
    "model": "x-ai/grok-4.1-fast"
  },
  "flags": {
    "kilocode": false,
    "architect": true
  },
  "orchestrator_active": false,
  "timestamp": "2025-12-08T15:42:00.000Z"
}
```

### Quiet Output (`--quiet`)

```
kilo_code=true
mode=architect
flags=architect
orchestrator=false
model=x-ai/grok-4.1-fast
```

---

## Implementation Steps

1) Parse `environment_details` for mode and model
2) Scan prompt context for Kilo Code indicators
3) Check for flag patterns in the prompt
4) Detect Orchestrator activity via keyword matching
5) Format output based on requested flags
6) Print results to console

---

## Examples

### Basic Check

```bash
/smartspec_check_kilo_mode
```

Output:
```
🤖 Kilo Code Status: Yes
📋 Current Mode: code
🚀 Flags: --kilocode
🎯 Orchestrator: Yes
🧠 Model: x-ai/grok-4.1-fast
```

### JSON for Scripting

```bash
/smartspec_check_kilo_mode --json
```

Output:
```json
{
  "kilo_code_active": true,
  "current_mode": {
    "slug": "code",
    "name": "Code",
    "model": "x-ai/grok-4.1-fast"
  },
  "flags": {
    "kilocode": true,
    "architect": false
  },
  "orchestrator_active": true,
  "timestamp": "2025-12-08T15:42:00.000Z"
}
```

### Quiet Mode for CI

```bash
/smartspec_check_kilo_mode --quiet
```

Output:
```
kilo_code=true
mode=code
flags=kilocode
orchestrator=true
model=x-ai/grok-4.1-fast
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Shows "No" for Kilo Code | Running on non-Kilo platform | Use on Kilo Code platform |
| Incorrect mode detected | environment_details not updated | Wait for next assistant response |
| Flags not detected | Flags in workflow but not in prompt | Check workflow command line |

---

## Notes

- This workflow is read-only and makes no changes to files
- Detection relies on current context; it reflects the state at time of execution
- JSON output includes ISO timestamp for logging
- Quiet mode is useful for CI/CD pipelines and scripts

---

## Version History

- **v1.0** (2025-12-08): Initial release with basic detection and JSON output