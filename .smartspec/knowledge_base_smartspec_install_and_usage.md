# Knowledge Base — SmartSpec Install & Usage Guide (Updated v5.7.2)

This is the **updated version** of `knowledge_base_smartspec_install_and_usage.md`, modified to:
- Reflect the new Kilo best practice: `--kilocode --require-orchestrator`
- Update installation and workflow-usage guidance
- Preserve backward compatibility

All updates are **additive**, and do not break existing workflows.

---

# 1. Installation Overview

SmartSpec supports:
- Kilo Code
- Claude Code
- Google Antigravity
- CLI environments

Install the SmartSpec extension/plugin according to your IDE.

---

# 2. Running SmartSpec Workflows

Workflows follow the chain:

```
/smartspec_generate_spec
/smartspec_generate_plan
/smartspec_generate_tasks
/smartspec_implement_tasks
```

General rules:
- Always run workflows inside the correct spec folder
- Never modify SPEC_INDEX or registries manually via implement workflows
- Use `--validate-only` to inspect results before writing

---

# 3. Flags & Modes Summary

### Env flags
```
--kilocode
--require-orchestrator
```

### Safety
```
--safety-mode=strict | dev
--strict
```

### Validation
```
--validate-only
--dry-run
```

### Multi-repo
```
--workspace-roots
--repos-config
--registry-dir
--registry-roots
```

---

# 4. Using SmartSpec in Kilo Code

## 4.1 Kilo Integration

SmartSpec supports a special meta-flag:

```
--kilocode
```

This enables:
- Orchestrator-per-task execution
- Kilo-aware code-editing behavior
- Improved file-change consistency

### (Updated) — Strong Recommendation
Whenever you run an implementation workflow under Kilo, SmartSpec strongly recommends:

```
--kilocode --require-orchestrator
```

### Why?
Because Orchestrator Mode significantly improves:
- context consistency
- accuracy of multi-file edits
- stability of long editing sequences
- reduction of ambiguous or conflicting patches

Without Orchestrator Mode, Kilo may:
- lose editing context
- produce incomplete or conflicting changes
- misinterpret task boundaries

Thus:

> **If you use `--kilocode`, you should also use `--require-orchestrator` to ensure Kilo is operating at full capability.**

This is a recommendation, not a breaking requirement.

---

# 5. Workflow Usage Details

## 5.1 /smartspec_generate_spec
Standard rules unchanged.

## 5.2 /smartspec_generate_plan
No changes.

## 5.3 /smartspec_generate_tasks
No changes.

## 5.4 /smartspec_implement_tasks (Updated)

This workflow performs real implementation and must obey safety rules.

### Recommended run pattern inside Kilo:
```
/smartspec_implement_tasks <tasks.md> \
    --kilocode --require-orchestrator --safety-mode=strict
```

### Behavior summary:
- `--kilocode` enables Kilo integration
- `--require-orchestrator` ensures Orchestrator must be active before starting
- `--safety-mode=strict` ensures the workflow stops early on governance issues

### What happens if Orchestrator is not active?
- With `--require-orchestrator`:
  - strict mode → fail immediately with a clear error
  - dev mode → warn loudly; may fallback or stop

---

# 6. Troubleshooting (Updated)

### Problem: Orchestrator is not active
Message:
> "Orchestrator Mode required (`--require-orchestrator`) but not active. Please enable Orchestrator Mode in Kilo and re-run."

Fix:
- Open Kilo UI
- Enable Orchestrator Mode
- Run again with:
```
--kilocode --require-orchestrator
```

### Problem: Kilo edit failed (Edit Unsuccessful)
- Narrow task scope
- Reduce file-range
- Retry task individually

SmartSpec will provide suggestions automatically.

---

# 7. Best Practices (Updated)

### ⭐ When implementing under Kilo:
```
--kilocode --require-orchestrator --safety-mode=strict
```

### ⭐ Use validate-only first on large repos:
```
--validate-only
```

### ⭐ Keep tasks small, precise, and unambiguous

### ⭐ Maintain SPEC_INDEX and registry accuracy

---

# 8. Security & Data Rules

Unchanged from original:
- No secrets or PII in prompts or code
- Treat model inputs/outputs as untrusted
- Use masking/sanitization rules for sensitive data

---

# 9. Appendix

This updated knowledge base remains backward-compatible.
`--require-orchestrator` is fully additive.

# END

