---
 title: SmartSpec Installation Manual (EN)
 version: 5.6
 audience: Dev / DevOps / Platform team
 scope: Project-local installation of SmartSpec core (.smartspec, .smartspec-docs)
---

# 1. Overview

This manual explains how to install **SmartSpec** in a *project-local* way
using the provided installer scripts:

- `install.sh`  (Linux / macOS, bash)
- `install.ps1` (Windows, PowerShell)

After installation, your project will contain:

- **`.smartspec/`**
  - `system_prompt_smartspec.md`  → global SmartSpec system prompt
  - `knowledge_base_smartspec.md` → global SmartSpec knowledge base (governance v5.6+)
  - `workflows/` → all `/smartspec_*` workflow specs (including `/smartspec_project_copilot`)
- **`.smartspec-docs/`**
  - `workflows/` → manuals and docs for each workflow (TH/EN, examples, changelogs)
- Tool-specific command folders (created/updated if present):
  - `.kilocode/workflows`
  - `.roo/commands`
  - `.claude/commands`
  - `.agent/workflows`
  - `.gemini/commands`

> Important: **The filenames for the system prompt and knowledge base are
> stable** (`system_prompt_smartspec.md`, `knowledge_base_smartspec.md`).
> This allows you to update their contents in the future without editing
> workflows or installer scripts.

---

# 2. What the installer does

When you run the installer, it will:

1. Download the **SmartSpec distribution repo** (URL + branch configurable)
2. Copy the following directories into the current project root:
   - `.smartspec/`
   - `.smartspec-docs/` (if present in the repo)
3. Verify that the core files exist:
   - `.smartspec/system_prompt_smartspec.md`
   - `.smartspec/knowledge_base_smartspec.md`
4. Copy `./.smartspec/workflows` into all relevant tool-specific folders in
   your project:
   - `.kilocode/workflows`
   - `.roo/commands`
   - `.claude/commands`
   - `.agent/workflows`
   - `.gemini/commands`

The installer **does not** touch `.spec/` (index, registry, reports). Those
remain owned by the project and the workflows.

---

# 3. Prerequisites

## 3.1 Linux / macOS (`install.sh`)

You need at least one of the following setups:

- `git` (recommended), **or**
- `curl` or `wget` + `unzip`

The script should be executed from a shell that supports `bash`/`sh`, e.g.:

- Bash on Linux
- Bash/Zsh on macOS

## 3.2 Windows (`install.ps1`)

- PowerShell (with access to):
  - `git` (if available) **or** `Invoke-WebRequest` + `Expand-Archive`
- Sufficient permissions to read/write files in the current project

> Note: On all platforms you must have write permissions to the project
> directory where you run the installer.

---

# 4. Configuring the distribution repo

By default, the scripts respect the following environment variables:

- Linux/macOS (`install.sh`):
  - `SMARTSPEC_REPO_URL`     (default: `https://github.com/your-org/SmartSpec.git`)
  - `SMARTSPEC_REPO_BRANCH`  (default: `main`)

- Windows (`install.ps1`):
  - `$env:SMARTSPEC_REPO_URL`
  - `$env:SMARTSPEC_REPO_BRANCH`

Platform/architecture teams should define:

- which repo URL to use (e.g., internal Git server),
- which branch/tag is the **distribution branch** for each environment.

Example (Linux/macOS):

```bash
export SMARTSPEC_REPO_URL="https://git.company.local/platform/SmartSpec.git"
export SMARTSPEC_REPO_BRANCH="release-5.6"
./install.sh
```

Example (Windows, PowerShell):

```powershell
$env:SMARTSPEC_REPO_URL    = 'https://git.company.local/platform/SmartSpec.git'
$env:SMARTSPEC_REPO_BRANCH = 'release-5.6'
./install.ps1
```

---

# 5. Installation steps on Linux / macOS

1. Open a terminal and `cd` into your project root.
2. Place `install.sh` in the project root.
3. (Optional) Configure `SMARTSPEC_REPO_URL` / `SMARTSPEC_REPO_BRANCH`.
4. Make the script executable:

   ```bash
   chmod +x install.sh
   ```

5. Run the script:

   ```bash
   ./install.sh
   ```

6. On success, you should see output similar to:

   ```
   ✅ SmartSpec installation/update complete.
      - Core:   .smartspec
      - Docs:   .smartspec-docs (if present in repo)
      - Tools:  .kilocode/workflows, .roo/commands, ...
   ```

---

# 6. Installation steps on Windows (PowerShell)

1. Open PowerShell and `cd` into your project root.
2. Place `install.ps1` in the project root.
3. (Optional) configure `$env:SMARTSPEC_REPO_URL` / `$env:SMARTSPEC_REPO_BRANCH`.
4. If your execution policy is restrictive, temporarily relax it for this
   session:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

5. Run the script:

   ```powershell
   ./install.ps1
   ```

6. On success, you will see summary output similar to the Linux/macOS script.

---

# 7. Directory layout after installation

After a successful installation, your project should contain structures like:

```text
.
├─ .smartspec/
│  ├─ system_prompt_smartspec.md
│  ├─ knowledge_base_smartspec.md
│  └─ workflows/
│     ├─ smartspec_generate_spec.md
│     ├─ smartspec_generate_plan.md
│     ├─ smartspec_project_copilot.md
│     └─ ...
├─ .smartspec-docs/
│  └─ workflows/
│     ├─ smartspec_generate_spec/
│     │  ├─ manual_th.md
│     │  ├─ manual_en.md
│     │  └─ examples.md
│     ├─ smartspec_project_copilot/
│     │  ├─ manual_th.md
│     │  ├─ manual_en.md
│     │  └─ ...
│     └─ ...
├─ .kilocode/workflows/
├─ .roo/commands/
├─ .claude/commands/
├─ .agent/workflows/
└─ .gemini/commands/
```

> Note: `.spec/` (index, registries, reports) is owned by the project and
> is not created/modified by the installer.

---

# 8. Updating SmartSpec versions

To update SmartSpec (e.g., new workflows, updated KB/system prompt):

1. Platform team updates the distribution repo content:
   - `.smartspec/*`
   - `.smartspec-docs/*`
2. In each project, rerun `install.sh` or `install.ps1`.
3. The installer will:
   - backup existing directories when present, e.g.:
     - `.smartspec/` → `.smartspec.backup.<timestamp>`
     - `.smartspec-docs/` → `.smartspec-docs.backup.<timestamp>`
   - copy the latest version from the distribution repo into the project.

> Recommendation: Avoid editing `.smartspec/workflows` directly in projects.
> If customization is needed, consider overlay patterns or project-specific
> workflow files, to avoid conflicts when the installer updates core files.

---

# 9. Using SmartSpec with `/smartspec_project_copilot`

After installation, you can use `/smartspec_project_copilot` as a
project-level "secretary/copilot" via Kilo/Roo/Claude/Antigravity/Gemini.

Conceptual flow:

- Run the copilot workflow pointing to your project root.
- The copilot reads:
  - `.spec/` (index, registries, reports)
  - `.smartspec/system_prompt_smartspec.md`
  - `.smartspec/knowledge_base_smartspec.md`
  - `.smartspec-docs/workflows/**`
- You can then ask natural-language questions like:
  - "Is this project ready for production?"
  - "Which workflow should I run next to check security/performance/UI?"

> For more details, see the dedicated manual for
> `/smartspec_project_copilot` under
> `.smartspec-docs/workflows/smartspec_project_copilot/`.

---

# 10. Security notes and guardrails

- Always point `SMARTSPEC_REPO_URL` to a **trusted** distribution repo.
- Avoid editing `system_prompt_smartspec.md` or `knowledge_base_smartspec.md`
  within individual projects unless you fully understand the implications
  (they control global SmartSpec behavior).
- When key policies change (e.g., tool-version registry, security rules,
  design-system governance), platform teams should update those in the
  distribution repo and have projects rerun the installer.

---

# 11. Basic troubleshooting

- **Error: git/curl/wget/unzip not found**
  - Install the missing tools or choose a supported combination.
- **`.smartspec/` not created after running the installer**
  - Ensure the distribution repo actually contains `.smartspec/`.
- **`system_prompt_smartspec.md` or `knowledge_base_smartspec.md` missing**
  - Check the distribution repo layout; rerun the installer after fixing.
- **Workflows cannot find docs in `.smartspec-docs/`**
  - Ensure `.smartspec-docs/` exists in the distribution repo and was
    copied; verify `--docs-root` configuration in relevant workflows.

For more complex issues, capture the full installer output and contact the
platform/architecture team to verify the distribution repo and environment
setup.

