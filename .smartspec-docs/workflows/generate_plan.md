# `/smartspec_generate_plan.md`

**Generates a high-level, phased project plan from a SPEC document, complete with realistic timelines, milestones, and risk assessment.**

---

## 1. Summary

This command transforms a detailed `spec.md` into a strategic, actionable implementation plan (`plan.md`). It serves as the bridge between specification and execution, breaking down a complex project into logical phases, estimating timelines, and defining clear milestones with exit criteria.

- **What it solves:** It provides a strategic roadmap, aligns team expectations, and surfaces potential risks and resource needs before development begins. It automates the tedious process of project planning based on engineering best practices.
- **When to use it:** After the `spec.md` is finalized and you need a high-level strategic plan before breaking it down into granular tasks.

---

## 2. Usage

```bash
/smartspec_generate_plan.md <spec_path> [options...]
```

---

## 3. Parameters & Options

### **Primary Argument**

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `spec_path` | `string` | ✅ Yes | The full path to the source `spec.md` file that will be used to generate the plan. | `specs/features/new-login/spec.md` |

### **Options**

These optional flags provide more control over the generation process.

| Option | Value | Default | Description |
| :--- | :--- | :--- | :--- |
| `--output` | `<filename>` | `plan.md` | Specifies a custom name for the output plan file. | `--output=roadmap.md` |
| `--specindex` | `<path>` | `.smartspec/SPEC_INDEX.json` | Points to a custom `SPEC_INDEX.json` file for resolving dependencies. | `--specindex=config/spec_index_v2.json` |
| `--nogenerate` | (flag) | (unset) | Performs a "dry run". The AI will analyze the SPEC and output its analysis to the console without writing any files. Useful for validation. |

---

## 4. Under the Hood: How the Plan is Generated

The AI follows a sophisticated process to create a realistic and comprehensive plan:

1.  **SPEC Analysis:** It parses all sections of the `spec.md`, extracting key entities like complexity, domain (e.g., `fintech`, `healthcare`), compliance needs (PCI DSS, HIPAA), and technical requirements.
2.  **Timeline Calculation:** A formula is used to estimate the timeline:
    - **Base Timeline:** Determined by project complexity (Low: 8 weeks, Critical: 20+ weeks).
    - **Multipliers:** Adjusted by domain (e.g., `fintech` adds 1.3x) and the number of microservices.
    - **Risk Buffer:** A buffer (20-35%) is added based on risk and complexity.
3.  **Phase Distribution:** The total timeline is distributed across standard software development phases (Foundation, Core Development, Testing, Deployment).
4.  **Milestone Generation:** For each phase, it generates detailed milestones with:
    - **Deliverables:** Concrete outputs for the phase.
    - **Acceptance Criteria:** A checklist to verify completion.
    - **Quality Gates:** Measurable standards (e.g., code coverage > 85%, zero critical bugs).
    - **Performance Validation:** Specific targets (e.g., P99 latency < 200ms).

This automated process ensures consistency and incorporates best practices into every plan.

---

## 5. Detailed Examples

### **Example 1: Basic Plan Generation**

**Goal:** Create a standard `plan.md` for a new backend service.

```bash
/smartspec_generate_plan.md specs/services/user-profile/spec.md
```

**Result:** A new file is created at `specs/services/user-profile/plan.md` outlining the phases, timeline, and milestones for building the service.

### **Example 2: Generating a Plan with a Custom Output Name**

**Goal:** Generate a plan but name it `roadmap.md` instead of the default.

```bash
/smartspec_generate_plan.md specs/services/user-profile/spec.md --output=roadmap.md
```

**Result:** The plan is generated and saved as `specs/services/user-profile/roadmap.md`.

### **Example 3: Performing a "Dry Run" for Analysis**

**Goal:** Analyze the SPEC and see the proposed plan in the console without creating a file.

```bash
/smartspec_generate_plan.md specs/critical/payment-gateway/spec.md --nogenerate
```

**Result:** The AI outputs a detailed analysis, including the calculated timeline, risk assessment, and proposed phases, directly to the console. No `plan.md` file is written, allowing you to review the plan before committing to it.

### **Example 4: Generating a Plan for a Complex Financial SPEC**

**Goal:** Generate a plan for a high-complexity fintech feature that requires PCI DSS compliance.

**Prerequisite:** The file `specs/critical/payment-gateway/spec.md` exists and contains a `domain: fintech` hint and requirements for handling credit card data.

```bash
/smartspec_generate_plan.md specs/critical/payment-gateway/spec.md
```

**Result:** A highly detailed `plan.md` is generated with the following special characteristics:
- **Increased Timeline:** The timeline is automatically extended due to the `fintech` domain factor and a larger risk buffer.
- **Compliance Phase:** A dedicated phase for "Security & PCI DSS Compliance" is added.
- **Detailed Milestones:** Milestones include specific deliverables and quality gates for PCI DSS, such as implementing data encryption, secure key management, and passing security scans.

---

## 6. How to Verify the Result

1.  **Check the File:** Ensure the `plan.md` (or your custom output file) has been created in the correct directory.
2.  **Review the Content:** Read the plan. Does it logically break down the project? Do the phases and timelines seem reasonable given the SPEC's complexity?
3.  **Check for Specifics:** If you provided a complex SPEC (e.g., fintech), verify that the plan includes relevant compliance tasks and security-focused milestones.

---

## 7. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **File not created** | The source `spec.md` path is incorrect, or you used `--nogenerate`. | Verify the path to the `spec.md` file is correct. If you used `--nogenerate`, this is the expected behavior. |
| **Plan seems too simple/short** | The source `spec.md` may lack detail, complexity, or domain hints. | Enhance the `spec.md` with more specific technical requirements, data models, and domain context, then re-run the command. |
| **Plan is not created in the right place** | The output path is always relative to the directory of the input `spec_path`. | This is by design. The `plan.md` is always co-located with its corresponding `spec.md`. |

---

## 8. For the LLM

- **Primary Goal:** To convert a detailed `spec.md` into a high-level, phased `plan.md`.
- **Key Entities:** `spec_path`, `--output`, `--specindex`, `--nogenerate`.
- **Workflow Position:** This is the **second step** in the SmartSpec workflow, after `generate_spec`.
- **Input Artifact:** `spec.md`.
- **Output Artifact:** `plan.md` (or custom name from `--output`).
