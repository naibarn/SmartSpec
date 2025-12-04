# `/smartspec_generate_tasks.md`

**Breaks down a SPEC document into a detailed, developer-ready `tasks.md` checklist, automatically creating supporting documents.**

---

## 1. Summary

This command is the engine of execution. It transforms a high-level `spec.md` into a granular, developer-ready checklist of tasks (`tasks.md`). It doesn't just list tasks; it intelligently scans for supporting files (like OpenAPI specs, data models), and if they're missing, it generates them.

- **What it solves:** It bridges the gap between specification and coding, creating a clear, actionable to-do list. It eliminates manual setup by auto-generating essential developer documents.
- **When to use it:** After the `spec.md` is ready and you want to generate a concrete, step-by-step implementation checklist for developers or AI agents.

---

## 2. Usage

```bash
/smartspec_generate_tasks.md <spec_path> [options...]
```

---

## 3. Parameters & Options

### **Primary Argument**

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `spec_path` | `string` | ✅ Yes | The full path to the source `spec.md` file. | `specs/features/new-login/spec.md` |

### **Options**

| Option | Value | Default | Description |
| :--- | :--- | :--- | :--- |
| `--specindex` | `<path>` | `.smartspec/SPEC_INDEX.json` | Points to a custom `SPEC_INDEX.json` file for resolving dependencies. | `--specindex=config/spec_index_v2.json` |
| `--nogenerate` | (flag) | (unset) | Performs a "dry run". Analyzes the SPEC and shows what *would* be generated without writing any files. |

---

## 4. Key Features & Logic

This workflow is more than a simple task generator. It includes several intelligent features:

1.  **Supporting File Detection:** It scans the SPEC's directory for existing documents like `openapi.yaml`, `data-model.md`, `test-plan.md`, etc. If found, it uses them as context for generating more accurate tasks.
2.  **Automatic Document Generation:** If the SPEC implies a need for a document that doesn't exist (e.g., the SPEC defines API endpoints but no `openapi.yaml` is found), the AI will **automatically generate it** based on the SPEC's content. This includes:
    - `openapi.yaml` from API specifications.
    - `data-model.md` from schema definitions.
    - A project-specific `README.md` for complex SPECs.
3.  **Dependency Resolution:** Using the `--specindex`, it can understand relationships between different SPECs, which helps in generating tasks related to integration.
4.  **Task Granularity:** It breaks down work into small, verifiable tasks, each with a unique ID (e.g., `T001`), making them perfect for tracking and for use in AI development environments like Cursor or Kilo Code.

---

## 5. Detailed Examples

### **Example 1: Basic Task Generation**

**Goal:** Create a standard `tasks.md` from a simple SPEC.

```bash
/smartspec_generate_tasks.md specs/services/user-profile/spec.md
```

**Result:**
- A new file, `specs/services/user-profile/tasks.md`, is created.
- It contains a checklist of tasks broken down by epics (e.g., "Database Setup", "API Endpoint").

### **Example 2: Auto-Generating Supporting Documents**

**Goal:** Generate tasks for a new API service where no supporting documents exist yet.

**Prerequisite:** `specs/services/new-api/spec.md` exists and contains sections for `## API Specification` and `## Data Models`.

```bash
/smartspec_generate_tasks.md specs/services/new-api/spec.md
```

**Result:** This is where the magic happens. In addition to `tasks.md`, the command also creates:
- `specs/services/new-api/openapi.yaml`: An OpenAPI 3.0 specification generated from the `## API Specification` section of the SPEC.
- `specs/services/new-api/data-model.md`: A document detailing the database schema, generated from the `## Data Models` section.

The `tasks.md` will then include tasks like "*Implement the API according to `openapi.yaml`*" and "*Create database migrations based on `data-model.md`*."

### **Example 3: Dry Run to Preview Tasks and Generated Files**

**Goal:** See what tasks and files would be generated for a complex SPEC without actually creating them.

```bash
/smartspec_generate_tasks.md specs/critical/payment-gateway/spec.md --nogenerate
```

**Result:** The AI outputs a report to the console, detailing:
- The full `tasks.md` that would be created.
- A list of supporting files it would auto-generate (e.g., `openapi.yaml`, `test-plan.md`).
- An estimated task count and complexity assessment.
This allows for a final review before any files are written to disk.

---

## 6. How to Verify the Result

1.  **Check for `tasks.md`:** Ensure the `tasks.md` file has been created.
2.  **Check for Supporting Files:** Look for any auto-generated files like `openapi.yaml` or `data-model.md` in the same directory.
3.  **Review Task Quality:** Are the tasks granular and specific? Do they logically follow from the SPEC and any supporting documents?

---

## 7. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **File not created** | The `spec.md` path is wrong, or you used `--nogenerate`. | Double-check the path. If using `--nogenerate`, this is expected. |
| **Tasks are too high-level** | The `spec.md` lacks detail. | The quality of the tasks is directly proportional to the quality of the SPEC. Add more specific details to the `Data Model`, `API Specification`, and `Business Rules` sections of your `spec.md` and re-run. |
| **Supporting files not generated** | The SPEC might not contain enough information to trigger the auto-generation logic. | Ensure your SPEC has clear, well-structured sections for APIs, data models, etc. For example, a section titled `## API Specification` with defined endpoints is needed to trigger `openapi.yaml` generation. |

---

## 8. For the LLM

- **Primary Goal:** To convert a `spec.md` into a checklist of small, actionable tasks in `tasks.md`, and to auto-generate missing supporting documents.
- **Key Entities:** `spec_path`, `--specindex`, `--nogenerate`.
- **Workflow Position:** This is the **third step** in the core workflow, after `generate_plan`.
- **Input Artifacts:** `spec.md`, and any existing supporting files in the same directory.
- **Output Artifacts:** `tasks.md`, and any newly generated supporting files (`openapi.yaml`, `data-model.md`, etc.).
