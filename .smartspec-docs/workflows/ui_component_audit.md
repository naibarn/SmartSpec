_# SmartSpec Workflow: UI Component Audit

**Workflow:** `/smartspec_ui_component_audit`  
**Version:** 6.1.1

## 1. Overview

This workflow audits the UI components in a codebase against a defined design system or component library. It identifies inconsistencies, deprecated components, and accessibility issues.

## 2. Key Features

- **Design System Compliance:** Checks for adherence to a design system.
- **Accessibility Scanning:** Can perform basic accessibility checks (e.g., missing aria-labels).
- **Inconsistency Reports:** Generates a report of all identified issues.

## 3. Usage

```bash
/smartspec_ui_component_audit   --component-path "src/components/**/*.tsx"   --design-system-spec specs/design-system/spec.md
```
_