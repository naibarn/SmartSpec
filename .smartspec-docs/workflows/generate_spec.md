# `/smartspec_generate_spec.md`

**Generates a new, comprehensive SPEC document from a high-level idea, with fine-grained control over its structure and content.**

---

## 1. Summary

This is the starting point for any new project or feature in SmartSpec. It transforms a vague, high-level idea into a structured, detailed, and machine-readable blueprint (`spec.md`). This document becomes the single source of truth for the entire development lifecycle.

- **What it solves:** It prevents ambiguity, ensures all critical aspects (security, performance, data models) are considered upfront, and provides the necessary context for AI agents.
- **When to use it:** At the very beginning of a new project, or when starting a significant new feature.

---

## 2. Usage

```bash
/smartspec_generate_spec.md <description_or_path> [options...]
```

---

## 3. Parameters & Options

This command offers a rich set of parameters and options to tailor the generated SPEC to your exact needs.

### **Primary Argument**

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `description_or_path` | `string` | ✅ Yes | A natural language description of the feature, OR the path to an existing `spec.md` file to edit. | `"Create a new payment gateway using Stripe"` or `specs/feature/spec-004/spec.md` |

### **Profile & Mode Options**

These options control the overall structure and verbosity of the SPEC.

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--profile` | `basic`, `backend-service`, `financial`, `full` | `full` | Selects a template with a predefined set of sections. `financial` is the most comprehensive. |
| `--mode` | `standard`, `compact` | `standard` | `compact` generates a condensed 5-section SPEC for simple projects. |

### **Content Control Options**

These flags allow you to fine-tune the content of specific sections.

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--security` | `none`, `basic`, `stride-basic`, `stride-full` | `auto` | Controls the level of detail in the Security section. `stride-full` is the most detailed. |
| `--di` | `full`, `minimal`, `none` | `auto` | Controls the Dependency Injection pattern documentation. `--no-di` is a shorthand for `none`. |
| `--performance` | `full`, `basic`, `none` | `auto` | Controls the detail of performance requirements. `basic` includes key metrics like P99, TPS, uptime. |
| `--domain` | `healthcare`, `iot`, `logistics`, `ai`, `fintech`, `saas`, `internal` | (none) | Provides a hint to the AI about the project's domain to generate more relevant content. |

## Parse Command-Line Flags

### 0.1 Profile Selection

```
--profile=<type>

Options:
  basic           - Minimal SPEC (Overview, Architecture, API/Data)
  backend-service - Standard backend (DI, testing, monitoring)
  financial       - Full security + performance (STRIDE, SLA, metrics)
  full            - All sections (default - v4.0 compatibility)
```

### 0.2 Mode Selection

```
--mode=<type>

Options:
  standard - Full SPEC with all details (default)
  compact  - Condensed 5-section SPEC for simple projects
```

### 0.3 Security Level

```
--security=<level>

Options:
  none         - No security section
  basic        - Basic security considerations
  stride-basic - STRIDE table (5-10 lines, key threats only)
  stride-full  - Complete STRIDE model (100+ lines, detailed)
  auto         - Auto-detect based on profile (default)
```

### 0.4 DI Pattern Control

```
--di=<level>

Options:
  full    - Complete DI pattern documentation (default for backend)
  minimal - Brief DI pattern mention
  none    - No DI pattern section
  auto    - Auto-detect based on project type (default)

Shorthand:
  --no-di  - Same as --di=none
```

### 0.5 Performance Requirements Control

```
--performance=<level>

Options:
  full    - Complete performance requirements
  basic   - Key metrics only (P99, TPS, uptime)
  none    - No performance section
  auto    - Auto-detect based on profile/domain (default)
```

### 0.6 Force Update Critical Sections

```
--force-update=<sections>

Options:
  all                          - Allow update all critical sections
  stride,config,di            - Allow specific sections
  none                        - Preserve all critical sections (default)
```

### 0.7 Content Preservation Strategy (NEW v5.1)

```
--preserve-strategy=<strategy>

Options:
  conservative - Preserve all existing detailed content, only add missing sections (default)
  balanced     - Merge existing with new, prefer existing for critical sections
  aggressive   - Regenerate all, only preserve critical sections marked with meta tags
  
--preserve-sections=<sections>

Specify sections to always preserve (comma-separated):
  --preserve-sections=stride,performance,di,api-spec,data-model
```

### 0.8 Output Organization

```
--no-backup        - Don't create backup files
--no-report        - Don't generate reports
--no-diff          - Don't generate diff report (NEW v5.1)
--output-dir=<dir> - Custom output directory (default: .smartspec/)
```

### 0.9 Validation

```
--validate-consistency  - Check consistency between sections
--validate-quality      - Check content quality (NEW v5.1)
--no-validation        - Skip validation checks
```

### 0.10 Domain Hints

```
--domain=<type>

Options:
  healthcare - Real-time + privacy critical
  iot        - High throughput, telemetry
  logistics  - High SLA requirements
  ai         - Latency sensitive
  fintech    - Security + performance critical
  saas       - Scalability focused
  internal   - Lower requirements
```

<br>

### **File & Operation Options**

These options control how the command operates and handles files.

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--force-update` | `all`, `stride,config,di` | `none` | A comma-separated list of critical sections to allow overwriting when editing an existing SPEC. Use with caution. |
| `--output-dir` | `<directory_path>` | `.smartspec/` | Specifies a custom directory for the output files. |
| `--no-backup` | (flag) | (unset) | If set, disables the creation of backup files (`.bak`) when editing. |
| `--no-report` | (flag) | (unset) | If set, suppresses the generation of a summary report. |
| `--no-validation` | (flag) | (unset) | If set, skips all validation checks for consistency and completeness. |

---

## 4. Detailed Examples

### **Example 1: Creating a Simple SPEC for a Prototype**

**Goal:** Create a minimal SPEC for a quick prototype.

```bash
/smartspec_generate_spec.md "Create a simple user login page" --profile=basic --mode=compact
```

**Result:** A short, 5-section `spec.md` is created, perfect for getting started quickly.

### **Example 2: Creating a Comprehensive SPEC for a Fintech Feature**

**Goal:** Create a detailed, secure, and performant SPEC for a new financial feature.

```bash
/smartspec_generate_spec.md "Build a credit purchase system with PCI DSS compliance" --profile=financial --security=stride-full --performance=full --domain=fintech
```

**Result:** A highly detailed `spec.md` with comprehensive security (STRIDE), performance, and audit sections, tailored for the fintech domain.

### **Example 3: Creating a New SPEC from a Detailed User Request**

**Goal:** Generate a comprehensive SPEC for a new, complex feature by providing a detailed, multi-line description directly in the command.

**User's Idea (The `description_or_path` argument):**

> "I need to build a real-time collaborative whiteboard feature.
> Key requirements:
> - Users can create, join, and share whiteboards via a unique URL.
> - It must support basic drawing tools: pen, eraser, shapes (circle, square), and text boxes.
> - All actions must be synced in real-time (<200ms latency) across all participants using WebSockets.
> - The backend should be built on Node.js and the frontend in React.
> - User authentication is handled by a separate, existing service, so we just need to validate a JWT token.
> - All whiteboard data must be saved to a PostgreSQL database."

**Command:**

```bash
/smartspec_generate_spec.md "I need to build a real-time collaborative whiteboard feature. Key requirements: - Users can create, join, and share whiteboards via a unique URL. - It must support basic drawing tools: pen, eraser, shapes (circle, square), and text boxes. - All actions must be synced in real-time (<200ms latency) across all participants using WebSockets. - The backend should be built on Node.js and the frontend in React. - User authentication is handled by a separate, existing service, so we just need to validate a JWT token. - All whiteboard data must be saved to a PostgreSQL database." --profile=full --security=stride-basic --domain=saas
```

**Result:**

This command generates a highly detailed `spec.md` file. The AI uses the rich description to populate multiple sections:

*   **`## 2. Functional Requirements`**: The drawing tools, sharing mechanism, and real-time sync are listed as key features.
*   **`## 4. Technical Specifications`**: The tech stack (Node.js, React, WebSockets, PostgreSQL) is documented.
*   **`## 5. Data Models`**: A preliminary data model for `Whiteboard` and `DrawingAction` is created.
*   **`## 6. Security`**: The JWT validation requirement is noted under an `Authentication` subsection.
*   **`## 8. Performance`**: The `<200ms` latency requirement is added as a key performance indicator (KPI).

### **Example 4: Editing an Existing SPEC to Update Security**

**Goal:** Update the security section of an existing SPEC without touching other critical parts.

```bash
/smartspec_generate_spec.md specs/services/user-profile/spec.md --force-update=stride --security=stride-full
```

**Result:** The `spec.md` file is updated in place. Only the security section is regenerated with a full STRIDE analysis. A backup (`spec.md.bak`) is created automatically.

---

## 5. How to Verify the Result

1.  **Check the file:** Ensure the `spec.md` file has been created in the correct directory.
2.  **Review the content:** Open the file and check that the sections match the profile and options you selected (e.g., if you used `--security=stride-full`, look for a detailed STRIDE table).
3.  **Check for completeness:** Read through the generated content. While much of it will be boilerplate, ensure it has correctly incorporated your high-level description and domain hints.

---

## 6. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **File not created** | Incorrect path or permissions issue. | Verify the path is correct and that you have write permissions in the target directory. |
| **Critical sections not updated** | The `--force-update` flag was not used. | When editing, you must explicitly allow updates to protected sections like `security`, `di`, and `config` using `--force-update=<section_name>`. |
| **Content is irrelevant** | The initial description was too vague or the wrong domain was used. | Re-run the command with a more detailed description and a specific `--domain` hint. |

---

## 7. For the LLM

- **Primary Goal:** To convert a user's natural language description and command-line options into a structured `spec.md` file.
- **Key Entities:** `description_or_path`, `--profile`, `--mode`, `--security`, `--di`, `--performance`, `--domain`, `--force-update`.
- **Workflow Position:** This is always the **first step** in the SmartSpec workflow.
- **Output Artifact:** A single Markdown file (`spec.md`) which serves as the input for `/smartspec_generate_plan.md` and `/smartspec_generate_tasks.md`.
