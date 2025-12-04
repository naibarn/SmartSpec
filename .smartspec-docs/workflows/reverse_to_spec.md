# `/smartspec_reverse_to_spec.md`

**Reverse-engineers an existing codebase into a SmartSpec `spec.md` document.**

---

## 1. Summary

This powerful command allows you to bring existing projects into the SmartSpec ecosystem. It analyzes your source code, database schema, and existing documentation to generate a `spec.md` file automatically.

- **What it solves:** It saves a massive amount of time by eliminating the need to manually document legacy projects. It allows you to apply SmartSpec's structured workflows to code you've already written.
- **When to use it:** When you want to onboard an existing project to SmartSpec, or when you need to generate up-to-date documentation for a legacy system.

---

## 2. Usage

```bash
/smartspec_reverse_to_spec.md <src_path> [--prisma <prisma_path>] [--docs <docs_path>] [--output <output_path>]
```

### Parameters

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `src_path` | `string` | ✅ Yes | The path to the source code directory of the project. | `~/projects/my-legacy-app/src` |

### Options

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--prisma <prisma_path>` | `string` | ❌ No | Path to the `schema.prisma` file for accurate data modeling. | `~/projects/my-legacy-app/prisma/schema.prisma` |
| `--docs <docs_path>` | `string` | ❌ No | Path to a directory containing existing Markdown documentation (`.md` files). | `~/projects/my-legacy-app/docs` |
| `--output <output_path>` | `string` | ❌ No | The full path where the new `spec.md` file will be created. Defaults to `./spec.md`. | `specs/reversed/my-legacy-app/spec.md` |

---

## 3. Input

- Source code files (TypeScript/JavaScript supported in MVP).
- Optionally, a `schema.prisma` file.
- Optionally, a folder of existing Markdown documentation.

---

## 4. Output

A new `spec.md` file that represents the analyzed codebase.

**Important:** The generated SPEC is a **best-effort draft**. It will be highly accurate for things it can statically analyze (like data models from Prisma and API routes from Express) but will require human review for inferred business logic.

---

## 5. Detailed Examples

### Example 1: Reversing a full-stack NestJS project with Prisma

1.  **Run the command:**
    ```bash
    /smartspec_reverse_to_spec.md ~/projects/my-app/src --prisma ~/projects/my-app/prisma/schema.prisma --docs ~/projects/my-app/docs --output specs/my-app/spec.md
    ```

**Result:** A new `spec.md` is created, combining insights from the source code, the precise data model from Prisma, and high-level concepts from the existing documentation.

---

## 6. How to Verify the Result

1.  **Review the SPEC:** This is a critical step. Carefully read the generated `spec.md`.
2.  **Check for `[NEEDS REVIEW]` tags:** The tool will insert these tags in sections where it had to make an assumption or could not fully understand the logic. Pay close attention to these.
3.  **Compare with source code:** Spot-check a few key areas. Does the generated API spec match your routes? Does the data model match your schema?

---

## 7. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **SPEC is inaccurate or incomplete** | The codebase uses unsupported frameworks, or the logic is too complex to be inferred. | 1. Provide more context via the `--docs` parameter. 2. Manually edit the generated `spec.md` to correct the inaccuracies. The goal is to get a good starting point, not a perfect final document. |
| **Data model is wrong** | You did not provide a `--prisma` path for a project that uses Prisma. | Re-run the command and include the path to your `schema.prisma` file. |

---

## 8. For the LLM

- **Primary Goal:** To analyze an existing codebase and generate a `spec.md` document.
- **Key Entities:** `src_path`, `prisma_path`, `docs_path`, `output_path`.
- **Workflow Position:** This is a special entry point into the SmartSpec ecosystem. Its output (`spec.md`) can then be used by the standard workflows (`generate_plan`, `generate_tasks`).
- **Input Artifacts:** Source code files, schema files, documentation files.
- **Output Artifact:** A `spec.md` file.
