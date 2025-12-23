# Troubleshooting Guide: Common Evidence Hook Issues

This guide helps you diagnose and solve common problems related to evidence hooks, particularly after running the `/smartspec_verify_tasks_progress_strict` workflow.

## Scenario: High Percentage of "Not Verified" or "Missing Hooks"

You run a verification report and get a summary like this:

```
- Verified done: 47 (26%)
- Not verified: 48 (26%) → Marked as [x] but evidence could not be verified
- Missing evidence hooks: 65 (36%) → Marked as [x] but no evidence provided
- Needs manual check: 22 (12%)
```

This is a classic sign that your `tasks.md` file contains legacy, descriptive, or incomplete evidence. The verification workflow cannot parse these entries, leading to a low "Verified" score.

### Step 1: Identify the Root Cause

Look for these common anti-patterns in your `tasks.md` file.

**Anti-Pattern 1: Descriptive, Natural Language Evidence**

This is the most common issue in older projects. The evidence is a sentence meant for a human.

```markdown
| **Evidence:** The user authentication service should be implemented in its own file. |
```

**Anti-Pattern 2: TODO Placeholders**

This happens when a developer knows evidence is needed but doesn't fill it in.

```markdown
| **Evidence:** evidence: TODO: file_exists path=??? |
```

**Anti-Pattern 3: Incomplete or Incorrect Paths**

Paths in evidence hooks must be relative to the repository root.

```markdown
# Incorrect - Missing full path
| **Evidence:** evidence: file_exists path=auth.service.ts |

# Correct
| **Evidence:** evidence: file_exists path=packages/auth-lib/src/services/auth.service.ts |
```

### Step 2: The Wrong Solution (Manual Fixing)

Your first instinct might be to go through the `tasks.md` file and manually fix every single line. You would read the task, figure out the correct hook, and type it in.

**Why this is a bad idea:**
-   **Extremely Time-Consuming:** Can take hours or days for large projects.
-   **Highly Error-Prone:** It's easy to introduce typos or use the wrong hook type.
-   **Not Scalable:** It's not a repeatable or efficient process.

### Step 3: The Right Solution (Automated Migration)

The correct, most efficient, and safest way to solve this problem is to use the `/smartspec_migrate_evidence_hooks` workflow. This tool was built precisely for this scenario.

#### Recommended Remediation Flow

**1. Run in Preview Mode (Safety First)**

Always start with a dry run. This will show you what the AI proposes to change without touching your files.

```bash
/smartspec_migrate_evidence_hooks \
  --tasks-file "specs/core/spec-core-001-authentication/tasks.md"
```

**2. Review the Diff**

The workflow will output a `diff` showing the proposed changes. You will see lines like this:

```diff
- | **Evidence:** The user model should have a password field.
+ | **Evidence:** evidence: db_schema table=users column=password_hash
```

Review these changes to ensure the AI's interpretation is correct. In most cases, it will be highly accurate.

**3. Apply the Changes**

Once you are confident in the preview, run the command again with the `--apply` flag.

```bash
/smartspec_migrate_evidence_hooks \
  --tasks-file "specs/core/spec-core-001-authentication/tasks.md" \
  --apply
```

Your `tasks.md` file will be updated in place, converting all legacy evidence to standardized, machine-readable hooks.

**4. Re-run Verification**

Finally, run the verification workflow again.

```bash
/smartspec_verify_tasks_progress_strict --spec specs/core/spec-core-001-authentication/spec.md
```

You should now see a significantly higher "Verified done" percentage, as the workflow can now parse and check the evidence hooks correctly.

## Conclusion

When faced with a poor verification score due to evidence format issues, resist the urge to fix it manually. The `/smartspec_migrate_evidence_hooks` workflow is the strategic, efficient, and reliable solution designed to modernize your project and unlock the full power of automated governance.
