_# SmartSpec Workflow: Hotfix Assistant

**Workflow:** `/smartspec_hotfix_assistant`  
**Version:** 6.1.1

## 1. Overview

The Hotfix Assistant is a specialized workflow designed to manage the entire lifecycle of a hotfix, from identifying the issue to generating a patch and planning the release. It enforces a strict, audited process for emergency changes.

## 2. Key Features

- **End-to-End Management:** Guides the user through identifying the root cause, creating a minimal fix, and generating a deployment plan.
- **Evidence-Based:** Requires a link to a production issue (e.g., a ticket) and a verification report.
- **Cherry-Picking:** Identifies the exact commit to be hotfixed.

## 3. Usage

```bash
/smartspec_hotfix_assistant   --issue-url <url-to-ticket>   --target-commit <commit-hash>   --apply
```
_