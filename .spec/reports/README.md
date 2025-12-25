# SmartSpec Reports Directory

This directory contains generated reports from SmartSpec workflows.

## Purpose

- **Read-Write Area:** LLM can read and write reports here
- **Project-Specific:** Reports are specific to this project
- **Temporary:** Reports can be regenerated at any time

## Structure

Reports are organized by workflow and run ID:

```
.spec/reports/
├── implement-tasks/
│   └── <spec-id>/
│       ├── report.md
│       ├── summary.json
│       └── change_plan.md
├── verify-tasks-progress/
│   └── <spec-id>/
│       ├── report.md
│       └── summary.json
├── generate-spec/
│   └── <run-id>/
│       ├── spec.md
│       └── summary.json
└── ...
```

## Design Principle

### `.smartspec/` - Read-Only (Knowledge Base)
- Workflows, scripts, knowledge base
- LLM **reads only**, does not modify
- Prevents LLM from altering workflow logic

### `.spec/` - Read-Write (Project Data)
- Reports, specs, registry
- LLM **reads and writes**
- Project-specific data

## Cleanup

Reports can be safely deleted to free up space:

```bash
# Delete all reports
rm -rf .spec/reports/*

# Delete specific workflow reports
rm -rf .spec/reports/implement-tasks/*

# Delete old reports (older than 7 days)
find .spec/reports/ -type f -mtime +7 -delete
```

## Gitignore

Reports should be added to `.gitignore` to avoid committing temporary files:

```gitignore
# SmartSpec Reports
.spec/reports/
```

## Related

- **Workflows:** `.smartspec/workflows/`
- **Scripts:** `.smartspec/scripts/`
- **Registry:** `.spec/registry/`
- **Config:** `.spec/smartspec.config.yaml`
