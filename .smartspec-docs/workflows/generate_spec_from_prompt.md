# /smartspec_generate_spec_from_prompt Manual (v6.0, English)

## Overview

The `/smartspec_generate_spec_from_prompt` workflow (Version 6.0.1) is a core SmartSpec utility designed to generate **one or more starter specification documents** from a natural-language requirement prompt.

**Purpose:** To accelerate the specification process by applying reuse-first intelligence. The workflow automatically checks against existing specifications (`.spec/SPEC_INDEX.json`) to detect overlaps, preferring **reuse and referencing** over creating duplicates. It ensures generated specs meet high quality standards (UX/UI-ready, states, a11y, responsive design) and rigorously captures external references and sources in an auditable manner.

**Category:** `spec-gen`
**Status:** Production Ready

---

## Usage

### CLI

The command-line interface (CLI) is the primary method for invoking the workflow.

```bash
/smartspec_generate_spec_from_prompt \
  "<your requirement prompt>" \
  [--spec-category <category>] \
  [--max-specs <n>] \
  [--refs <dir>] \
  [--update-index] \
  [--dry-run] \
  [--json] \
  [--apply]
```

### Kilo Code

For execution within the SmartSpec Kilo Code environment or scripting:

```bash
/smartspec_generate_spec_from_prompt.md \
  "<your requirement prompt>" \
  [--spec-category <category>] \
  [--max-specs <n>] \
  [--refs <dir>] \
  [--update-index] \
  [--dry-run] \
  [--json] \
  [--apply]
```

---

## Use Cases

### Use Case 1: Generating a New Feature Spec (Preview Mode)

**Scenario:** A product manager needs a detailed specification for a new "Dark Mode Toggle" feature, but wants to review the proposal and reuse analysis before committing the files. They provide a reference directory containing design mockups.

**CLI Command:**

```bash
/smartspec_generate_spec_from_prompt \
  "Implement a user-configurable Dark Mode toggle with system preference detection and persistence across sessions." \
  --spec-category "settings" \
  --refs "./design_assets/dark_mode_v1" \
  --dry-run
```

**Expected Result:**
1. **Output:** A deterministic preview bundle is written to `.spec/reports/spec-from-prompt/<run-id>/`.
2. **Reuse Analysis:** The `report.md` shows the similarity check against existing specs. If no strong match is found, it proposes a new spec ID (e.g., `dark-mode-toggle`).
3. **Artifacts:** A draft `spec.md` (including states, a11y, and microcopy guidance) and `references/REFERENCE_INDEX.yaml` (citing assets from `./design_assets/dark_mode_v1`) are created in the preview directory.
4. **Governed Writes:** No files are written to the `specs/` directory or `.spec/SPEC_INDEX.json` because `--dry-run` was used.

### Use Case 2: Extending an Existing Spec (Reuse Proposal)

**Scenario:** A developer attempts to generate a spec for "User Profile Avatar Upload," unaware that a strong match exists for "User Profile Management." The workflow should detect the overlap and recommend extension.

**Kilo Code Command:**

```bash
/smartspec_generate_spec_from_prompt.md \
  "Allow users to upload and crop a custom avatar image for their profile, storing it in S3." \
  --spec-category "user-mgmt"
```

**Expected Result:**
1. **Reuse Analysis:** The workflow identifies a strong match (e.g., `user-profile-v1`) in the index.
2. **Output:** The workflow **MUST NOT** create a new spec folder.
3. **Report:** The `report.md` (written to reports/ directory) contains a **Reuse Proposal**, stating:
    *   **Decision:** Reuse `user-profile-v1`.
    *   **Delta:** The current spec lacks avatar upload/cropping requirements.
    *   **Next Step Recommendation:** `/smartspec_generate_spec --spec-ids=user-profile-v1 --extension-prompt="Add avatar upload and cropping..." --apply`

### Use Case 3: Applying and Indexing a New Spec

**Scenario:** A new, complex feature ("Real-time Notification Center") requires a dedicated spec, and the user is ready to commit the final specification files and update the central index.

**CLI Command:**

```bash
/smartspec_generate_spec_from_prompt \
  "Design a real-time notification center with unread counts, filtering by type, and a 'mark all read' action, using the internal WebSocket API." \
  --spec-category "platform" \
  --apply \
  --update-index
```

**Expected Result:**
1. **Governed Writes:** A new spec folder is created: `specs/platform/real-time-notifications/`.
2. **Artifacts:** `spec.md`, `references/REFERENCE_INDEX.yaml`, and `references/decisions.md` are written to the new spec folder.
3. **Indexing:** If `.spec/SPEC_INDEX.json` is allowlisted, it is updated with the metadata for the new `real-time-notifications` spec ID.
4. **Report:** A final `report.md` confirms the successful application and paths of the governed artifacts.

---

## Parameters

| Type | Parameter/Flag | Description | Default | Required |
| :--- | :--- | :--- | :--- | :--- |
| Positional | `<your requirement prompt>` | The natural-language requirement text used to generate the spec. | N/A | Yes |
| Flag | `--spec-category <category>` | The category under which the spec folder will be created (e.g., `settings`, `platform`). | `miniapp` (or project default) | No |
| Flag | `--max-specs <n>` | Maximum number of specs to generate from the prompt. | `1` (Max `5`) | No |
| Flag | `--refs <dir>` | Read-only directory containing reference materials (screenshots, docs, notes) for research. | N/A | No |
| Flag | `--update-index` | If used with `--apply`, updates the `.spec/SPEC_INDEX.json` with the new spec entry. | N/A | No |
| Flag | `--dry-run` | Executes the workflow but only writes safe previews to the reports directory. Ignores `--apply`. | N/A | No |
| Flag | `--json` | Outputs the final report summary in JSON format (`summary.json`) in addition to Markdown. | N/A | No |
| Flag | `--apply` | Enables governed write operations (creating spec folders and updating the index). | N/A | No |
| Universal | `--config <path>` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | No |
| Universal | `--lang <th|en>` | Language for generated output. | N/A | No |
| Universal | `--platform <cli|kilo|ci|other>` | Execution platform metadata. | N/A | No |
| Universal | `--out <path>` | Base path for safe reports/previews (never for governed spec placement). | N/A | No |
| Universal | `--quiet` | Suppress standard output logs. | N/A | No |

---

## Output

The workflow produces two types of output, depending on the use of the `--apply` and `--dry-run` flags.

### 1. Safe Preview Bundle (Always generated, or when `--dry-run`)

This bundle is written to a unique run folder under the reports path:

*   `.spec/reports/spec-from-prompt/<run-id>/report.md`: Detailed execution summary, reuse analysis, and next steps.
*   `.spec/reports/spec-from-prompt/<run-id>/summary.json` (if `--json`): Structured metadata about the run and proposed specs.
*   `.spec/reports/spec-from-prompt/<run-id>/preview/<spec-id>/spec.md`: The generated specification draft.
*   `.spec/reports/spec-from-prompt/<run-id>/preview/<spec-id>/references/REFERENCE_INDEX.yaml`: Draft reference index.

### 2. Governed Output (Only with `--apply` and not `--dry-run`)

These artifacts are written to the governed source tree:

*   `specs/<category>/<spec-id>/spec.md`: Final, committed specification document.
*   `specs/<category>/<spec-id>/references/REFERENCE_INDEX.yaml`: Structured index of external and internal references.
*   `specs/<category>/<spec-id>/references/decisions.md`: Log of key design and reuse decisions.
*   `.spec/SPEC_INDEX.json` (If `--update-index` is used and allowed