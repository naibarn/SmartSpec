# SmartSpec Platform Support Guide

## Overview

SmartSpec V5.2 supports **5 major AI coding platforms** with automatic installation and synchronization. This guide explains how workflows are installed and managed across different platforms.

---

## Supported Platforms

### 1. Kilo Code

**Type:** Autonomous AI agent-driven development  
**Workflow Directory:** `.kilocode/workflows/`  
**File Format:** Markdown (`.md`)  
**Command Prefix:** `/`  
**Example:** `/smartspec_generate_spec`

**Installation:**
- Workflows are copied directly from `.smartspec/workflows/`
- No conversion needed (Markdown format)

---

### 2. Roo Code

**Type:** Safety-first, workflow-driven development  
**Workflow Directory:** `.roo/commands/`  
**File Format:** Markdown (`.md`)  
**Command Prefix:** `/`  
**Example:** `/smartspec_generate_spec`

**Installation:**
- Workflows are copied directly from `.smartspec/workflows/`
- No conversion needed (Markdown format)

---

### 3. Claude Code

**Type:** Deep analysis with sub-agents  
**Workflow Directory:** `.claude/commands/`  
**File Format:** Markdown (`.md`)  
**Command Prefix:** `/`  
**Example:** `/smartspec_generate_spec`

**Installation:**
- Workflows are copied directly from `.smartspec/workflows/`
- No conversion needed (Markdown format)

---

### 4. Google Antigravity (NEW in v5.2)

**Type:** Agentic IDE with autonomous agents  
**Workflow Directory:** `.agent/workflows/` (workspace)  
**Global Directory:** `~/.gemini/antigravity/global_workflows/` (optional)  
**File Format:** Markdown (`.md`)  
**Command Prefix:** `/`  
**Example:** `/smartspec_generate_spec`

**Installation:**
- Workflows are copied directly from `.smartspec/workflows/`
- No conversion needed (Markdown format)
- Supports both workspace and global workflows

**Key Features:**
- Workspace workflows: Project-specific
- Global workflows: Available across all projects
- Rules system: Separate from workflows (system instructions)

---

### 5. Gemini CLI (NEW in v5.2)

**Type:** Terminal-based AI coding assistant  
**Workflow Directory:** `.gemini/commands/` (project)  
**Global Directory:** `~/.gemini/commands/` (optional)  
**File Format:** TOML (`.toml`)  
**Command Prefix:** `/`  
**Example:** `/smartspec_generate_spec`

**Installation:**
- Workflows are **automatically converted** from Markdown to TOML
- Conversion happens during installation and sync
- Supports both project and global commands

**Key Features:**
- Project commands: Project-specific
- Global commands: Available across all projects
- Namespacing: Subdirectories create namespaced commands (e.g., `git/commit.toml` → `/git:commit`)

**TOML Format Example:**
```toml
description = "Generate a comprehensive specification from an idea or requirement"

prompt = """
You are an expert software architect and technical writer...
{{args}}
"""
```

---

## Installation Process

### Single-Command Installation

**Unix / macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.ps1 | iex
```

### Installation Steps

1. **Platform Detection**: The installer automatically detects which platforms are present in your project
2. **Platform Selection**: You choose which platforms to install SmartSpec workflows for
3. **Workflow Installation**:
   - **Markdown platforms** (Kilo, Roo, Claude, Antigravity): Direct copy
   - **TOML platforms** (Gemini CLI): Automatic conversion
4. **Sync Script Creation**: A sync script is created for future updates

### Installation Menu

```
Which platforms do you want to install/update?
  1) Kilo Code
  2) Roo Code
  3) Claude Code
  4) Google Antigravity
  5) Gemini CLI
  6) All of the above
Enter choice [1-6] (default: 1):
```

---

## Workflow Management

### Master Source

All workflows are stored in `.smartspec/workflows/` as the **master source**. This is the single source of truth for all platforms.

**Important:** Always edit workflows in `.smartspec/workflows/`, never in platform-specific directories.

### Syncing Changes

After editing workflows in `.smartspec/workflows/`, sync changes to all platforms:

```bash
.smartspec/sync.sh
```

The sync script will:
- Copy Markdown workflows to Markdown platforms (Kilo, Roo, Claude, Antigravity)
- Convert and copy workflows to TOML platforms (Gemini CLI)

### Platform-Specific Directories

| Platform | Directory | Format | Sync Method |
|----------|-----------|--------|-------------|
| Kilo Code | `.kilocode/workflows/` | Markdown | Direct copy |
| Roo Code | `.roo/commands/` | Markdown | Direct copy |
| Claude Code | `.claude/commands/` | Markdown | Direct copy |
| Antigravity | `.agent/workflows/` | Markdown | Direct copy |
| Gemini CLI | `.gemini/commands/` | TOML | Convert + copy |

---

## Format Conversion (Gemini CLI)

### Automatic Conversion

Gemini CLI requires TOML format, so SmartSpec automatically converts Markdown workflows to TOML during:
- Initial installation
- Sync operations

### Conversion Process

1. **Extract Description**: First line of Markdown file (after `# `)
2. **Extract Prompt**: Rest of the file content
3. **Escape Special Characters**: Backslashes and quotes
4. **Create TOML File**: With `description` and `prompt` fields

### Manual Conversion

You can also manually convert workflows using the converter script:

```bash
.smartspec/scripts/convert-md-to-toml.sh <source_dir> <target_dir>
```

Example:
```bash
.smartspec/scripts/convert-md-to-toml.sh .smartspec/workflows .gemini/commands
```

---

## Global vs Workspace Workflows

### Workspace Workflows (Project-Specific)

Available only in the current project.

| Platform | Directory |
|----------|-----------|
| Kilo Code | `.kilocode/workflows/` |
| Roo Code | `.roo/commands/` |
| Claude Code | `.claude/commands/` |
| Antigravity | `.agent/workflows/` |
| Gemini CLI | `.gemini/commands/` |

### Global Workflows (User-Wide)

Available across all projects for the current user.

| Platform | Directory | Support |
|----------|-----------|---------|
| Kilo Code | N/A | ❌ |
| Roo Code | N/A | ❌ |
| Claude Code | N/A | ❌ |
| Antigravity | `~/.gemini/antigravity/global_workflows/` | ✅ |
| Gemini CLI | `~/.gemini/commands/` | ✅ |

**Note:** Currently, SmartSpec installer focuses on workspace workflows. Global workflow installation may be added in future versions.

---

## Troubleshooting

### Workflows Not Showing Up

1. **Check platform directory exists:**
   ```bash
   ls -la .kilocode/workflows/  # For Kilo Code
   ls -la .agent/workflows/     # For Antigravity
   ls -la .gemini/commands/     # For Gemini CLI
   ```

2. **Check workflow files exist:**
   ```bash
   ls -la .smartspec/workflows/smartspec_*.md
   ```

3. **Re-run sync script:**
   ```bash
   .smartspec/sync.sh
   ```

### Gemini CLI Commands Not Working

1. **Check TOML syntax:**
   ```bash
   cat .gemini/commands/smartspec_generate_spec.toml
   ```

2. **Verify file extension is `.toml`:**
   ```bash
   ls .gemini/commands/*.toml
   ```

3. **Re-convert workflows:**
   ```bash
   rm -rf .gemini/commands/*.toml
   .smartspec/sync.sh
   ```

### Platform Not Detected

1. **Check platform directory exists:**
   ```bash
   ls -la | grep -E "\.(kilocode|roo|claude|agent|gemini)"
   ```

2. **Create platform directory manually:**
   ```bash
   mkdir -p .agent/workflows  # For Antigravity
   mkdir -p .gemini/commands  # For Gemini CLI
   ```

3. **Re-run installer:**
   ```bash
   curl -fsSL https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.sh | bash
   ```

---

## Platform Comparison

| Feature | Kilo Code | Roo Code | Claude | Antigravity | Gemini CLI |
|---------|-----------|----------|--------|-------------|------------|
| **Workspace Workflows** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Global Workflows** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **File Format** | Markdown | Markdown | Markdown | Markdown | TOML |
| **Command Prefix** | `/` | `/` | `/` | `/` | `/` |
| **Auto-Detection** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Auto-Conversion** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Namespacing** | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## Best Practices

### 1. Always Edit Master Source
Edit workflows in `.smartspec/workflows/`, never in platform-specific directories.

### 2. Sync After Changes
Run `.smartspec/sync.sh` after editing workflows to update all platforms.

### 3. Use Version Control
Commit `.smartspec/workflows/` to version control, but consider ignoring platform-specific directories.

**Example `.gitignore`:**
```gitignore
# Platform-specific workflows (auto-generated)
.kilocode/workflows/smartspec_*.md
.roo/commands/smartspec_*.md
.claude/commands/smartspec_*.md
.agent/workflows/smartspec_*.md
.gemini/commands/smartspec_*.toml

# Keep master source
!.smartspec/workflows/
```

### 4. Test on Multiple Platforms
If you use multiple platforms, test workflows on each to ensure compatibility.

### 5. Keep Workflows Simple
Avoid platform-specific features in workflows to maintain compatibility across all platforms.

---

## Future Enhancements

### Planned Features

1. **Global Workflow Installation**: Option to install workflows globally for Antigravity and Gemini CLI
2. **Custom Namespacing**: Support for organizing workflows in subdirectories
3. **Workflow Templates**: Pre-built workflow templates for common tasks
4. **Platform-Specific Optimizations**: Enhanced features for each platform
5. **Workflow Validation**: Automatic validation of workflow syntax

---

## Support

For issues, questions, or feature requests:
- **GitHub Issues**: https://github.com/naibarn/SmartSpec/issues
- **Documentation**: https://github.com/naibarn/SmartSpec

---

## Version History

- **v5.2.0**: Added Google Antigravity and Gemini CLI support
- **v5.1.0**: Enhanced Kilo Code integration and documentation
- **v5.0.0**: Initial multi-platform support (Kilo, Roo, Claude)
