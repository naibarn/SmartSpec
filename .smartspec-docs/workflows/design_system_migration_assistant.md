_# SmartSpec Workflow: Design System Migration Assistant

**Workflow:** `/smartspec_design_system_migration_assistant`  
**Version:** 6.1.1

## 1. Overview

The Design System Migration Assistant helps automate the process of migrating a codebase from an old design system (or no design system) to a new one. It can identify old components and suggest or even automatically apply replacements.

## 2. Key Features

- **Automated Component Mapping:** Maps old components to their new equivalents.
- **Code Transformation:** Can apply basic code modifications to replace components.
- **Migration Planning:** Generates a report that can be used to plan a larger migration effort.

## 3. Usage

```bash
/smartspec_design_system_migration_assistant   --source-path "src/views/**/*.vue"   --migration-map path/to/migration-map.json   --apply
```
_