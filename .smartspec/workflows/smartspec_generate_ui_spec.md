---
workflow_id: smartspec_generate_ui_spec
version: "6.0.0"
status: active
category: ui
platform_support:
  - cli
  - kilo
requires_apply: true
---

# smartspec_generate_ui_spec

**Generate A2UI-compliant UI specification from natural language requirements.**

## Purpose

This workflow generates a governed, platform-agnostic UI specification in A2UI format from high-level natural language requirements. The generated `ui-spec.json` serves as the single source of truth for implementing UIs across multiple platforms (Web, Flutter, React, etc.).

## Governance contract

This workflow MUST follow:
- `knowledge_base_smartspec_handbook.md` (v6)
- A2UI Specification v0.8
- `.spec/smartspec.config.yaml`
- `.spec/ui-catalog.json` (if exists)

## Prerequisites

**Required:**
- A2UI must be enabled in `.spec/smartspec.config.yaml` (`a2ui.enabled: true`)
- UI component catalog must exist (`.spec/ui-catalog.json`) or preset must be configured

**Optional:**
- Existing functional specification for context
- Design references or mockups
- Accessibility requirements

## Invocation

### CLI

```bash
/smartspec_generate_ui_spec \
  --requirements "Create restaurant booking form with date picker, time selector, guest count, and special requests" \
  --spec specs/feature/spec-001-booking/ui-spec.json
```

### Kilo Code

```bash
/smartspec_generate_ui_spec.md \
  --requirements "Create restaurant booking form with date picker, time selector, guest count, and special requests" \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --platform kilo
```

## Flags

### Universal Flags

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--apply` | boolean | No | Apply changes (default: preview mode) |
| `--platform` | string | No | Platform: cli, kilo (default: cli) |
| `--verbose` | boolean | No | Verbose output |
| `--dry-run` | boolean | No | Simulate without changes |
| `--report-dir` | path | No | Custom report directory |
| `--force` | boolean | No | Force overwrite existing files |

### Workflow-Specific Flags

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--requirements` | string | Yes | Natural language UI requirements |
| `--spec` | path | Yes | Path to save ui-spec.json |
| `--target-platform` | string | No | Target platform: web, flutter, mobile, all (default: web) |
| `--catalog` | path | No | Path to component catalog (default: .spec/ui-catalog.json) |
| `--style` | string | No | Style preset: material, fluent, custom (default: from config) |
| `--accessibility` | string | No | Accessibility level: basic, wcag-aa, wcag-aaa (default: from config) |
| `--interactive` | boolean | No | Interactive mode with refinement |
| `--context-spec` | path | No | Path to functional spec for context |
| `--mockup` | path | No | Path to design mockup/reference image |

### Flag Usage Notes

**Path Safety:**
- All paths must be within allowed write roots (see config)
- Spec path must be under `specs/` directory
- Use relative paths from project root

**Requirements Format:**
- Can be inline string (for simple UIs)
- Can be path to requirements file (for complex UIs)
- Should describe components, interactions, and data flow

**Interactive Mode:**
- Agent generates initial UI spec
- Shows preview and mockup
- Asks for feedback
- Refines spec iteratively
- Saves when user approves (if `--apply`)

## Behavior

### Preview Mode (default)

1. **Validate Prerequisites**
   - Check A2UI is enabled in config
   - Verify catalog exists or preset is configured
   - Validate requirements input

2. **Parse Requirements**
   - Extract UI components needed
   - Identify data model structure
   - Determine interactions and workflows
   - Analyze accessibility needs

3. **Load Component Catalog**
   - Read catalog from configured path
   - Validate catalog format
   - Build component registry

4. **Generate A2UI Specification**
   - Create surfaces (UI screens/dialogs)
   - Define components with properties
   - Set up data model
   - Configure data bindings
   - Define actions and interactions

5. **Validate Specification**
   - Check against A2UI schema v0.8
   - Verify all components exist in catalog
   - Validate JSON Pointer paths
   - Check accessibility compliance

6. **Create Visual Mockup**
   - Generate preview image/HTML
   - Show component layout
   - Display data flow

7. **Generate Report**
   - Save ui-spec.json to report directory (NOT final path)
   - Create mockup.png
   - Generate component-analysis.md
   - Create recommendations.md
   - Write full report.md

8. **Display Preview**
   - Show mockup
   - List components used
   - Show data model structure
   - Display recommendations

9. **Prompt for Apply**
   - Instruct user to review
   - Provide command to run with `--apply`

### Apply Mode (`--apply`)

1. **Perform all preview mode steps**

2. **Save to Final Location**
   - Write ui-spec.json to specified path
   - Create parent directories if needed
   - Validate write permissions

3. **Update Spec Index**
   - Add entry to `.spec/SPEC_INDEX.json`
   - Link to functional spec (if provided)
   - Add metadata

4. **Generate Documentation**
   - Create ui-spec-docs.md
   - Document components used
   - Explain data model
   - Provide usage examples

5. **Create Usage Examples**
   - Generate ui-spec-examples.md
   - Show how to implement
   - Provide next steps

6. **Report Success**
   - Display file paths
   - Show next workflow suggestions
   - Provide implementation command

### Interactive Mode (`--interactive`)

1. **Generate Initial Spec**
   - Create first version from requirements

2. **Show Preview**
   - Display mockup
   - List components

3. **Collect Feedback**
   - Ask specific questions
   - "Does this layout match your vision?"
   - "Are all required fields included?"
   - "Should we add any validation?"

4. **Refine Specification**
   - Update based on feedback
   - Regenerate mockup
   - Show changes

5. **Repeat Until Approved**
   - Continue refinement cycle
   - Track iterations

6. **Save Final Spec**
   - If user approves and `--apply` is set
   - Otherwise save to report directory

## Output

### Preview Mode

```
.spec/reports/generate-ui-spec/<run-id>/
├── ui-spec-preview.json          # Generated A2UI specification
├── mockup.png                     # Visual mockup
├── mockup.html                    # Interactive preview (optional)
├── component-analysis.md          # Components used and analysis
├── data-model.md                  # Data model structure
├── recommendations.md             # Suggestions for improvement
└── report.md                      # Full report with next steps
```

### Apply Mode (additional)

```
specs/<category>/<spec-id>/
├── ui-spec.json                   # A2UI specification (final)
├── ui-spec-docs.md                # Documentation
└── ui-spec-examples.md            # Usage examples

.spec/
└── SPEC_INDEX.json                # Updated with new UI spec entry
```

### Interactive Mode (additional)

```
.spec/reports/generate-ui-spec/<run-id>/
└── iterations/                    # UI spec iterations
    ├── iteration-1.json
    ├── iteration-2.json
    ├── iteration-3.json
    └── ...
```

## Example Usage

### Example 1: Simple Form

**Requirements:**
```
Create a contact form with:
- Name field (required)
- Email field (required, validated)
- Message textarea (required)
- Submit button
```

**Command:**
```bash
/smartspec_generate_ui_spec \
  --requirements "Create a contact form with name, email, message, and submit button" \
  --spec specs/feature/spec-002-contact/ui-spec.json
```

**Generated Spec (simplified):**
```json
{
  "version": "0.8",
  "surfaces": [
    {
      "id": "contact-form",
      "components": [
        {
          "id": "name-field",
          "type": "text-field",
          "label": "Name",
          "valuePath": "/contact/name",
          "required": true
        },
        {
          "id": "email-field",
          "type": "text-field",
          "label": "Email",
          "type": "email",
          "valuePath": "/contact/email",
          "required": true
        },
        {
          "id": "message-field",
          "type": "text-area",
          "label": "Message",
          "valuePath": "/contact/message",
          "rows": 6,
          "required": true
        },
        {
          "id": "submit-button",
          "type": "button",
          "label": "Send Message",
          "action": "submit-contact",
          "variant": "primary"
        }
      ]
    }
  ],
  "dataModel": {
    "contact": {
      "name": "",
      "email": "",
      "message": ""
    }
  }
}
```

### Example 2: Complex Dashboard

**Requirements File:** `requirements/dashboard-ui.md`

**Command:**
```bash
/smartspec_generate_ui_spec \
  --requirements requirements/dashboard-ui.md \
  --spec specs/feature/spec-003-dashboard/ui-spec.json \
  --target-platform web \
  --accessibility wcag-aa \
  --interactive
```

**Interactive Session:**
```
Agent: I've generated an initial dashboard with 3 cards: metrics, chart, and recent activity. 
       Would you like to see the preview?

User: Yes

Agent: [Shows mockup]
       The dashboard includes:
       - Metrics card with 4 KPIs
       - Line chart for trends
       - Table for recent activity
       
       Does this match your vision?

User: Add a filter dropdown at the top

Agent: I'll add a date range filter. Should it be:
       1. Predefined ranges (Last 7 days, Last 30 days, etc.)
       2. Custom date picker
       3. Both

User: Both

Agent: [Updates spec and shows new mockup]
       I've added a filter with predefined ranges and custom date picker.
       Anything else to adjust?

User: Looks good, save it

Agent: Saved to specs/feature/spec-003-dashboard/ui-spec.json
```

### Example 3: With Context Spec

**Command:**
```bash
/smartspec_generate_ui_spec \
  --requirements "Create booking form UI" \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --context-spec specs/feature/spec-001-booking/spec.md \
  --apply
```

**Benefit:** Agent reads functional spec for:
- Business rules
- Data validation requirements
- Workflow steps
- Integration points

## Evidence sources

When answering questions, the agent MUST read:

1) **Knowledge base** (MUST read before answering)
   - `knowledge_base_smartspec_handbook.md`
   - `knowledge_base_smartspec_install_and_usage.md`
   - `.smartspec/WORKFLOW_PARAMETERS_REFERENCE.md`
   - `.smartspec/WORKFLOW_SCENARIOS_GUIDE.md`

2) **A2UI Resources**
   - A2UI Specification v0.8
   - `.spec/ui-catalog.json` or `.spec/ui-catalog.template.json`
   - `docs/a2ui/A2UI_SmartSpec_Integration_Report.md`
   - `a2ui_workflow_specifications.md`

3) **Configuration**
   - `.spec/smartspec.config.yaml` (a2ui section)

4) **Context (if provided)**
   - Functional specification (--context-spec)
   - Design mockups (--mockup)
   - Requirements file

5) **Indexes**
   - `.spec/SPEC_INDEX.json`
   - `.spec/WORKFLOWS_INDEX.yaml`

## Best Practices

### Requirements Writing

**Good:**
```
Create a product search interface with:
- Search input with autocomplete
- Filter sidebar (category, price range, rating)
- Grid of product cards (image, name, price, rating)
- Pagination at bottom
- Sort dropdown (relevance, price, rating)
```

**Bad:**
```
Make a search page
```

### Component Selection

- **Use catalog components only** - Don't invent new component types
- **Prefer simple components** - Compose complex UIs from simple building blocks
- **Follow Material Design patterns** - Use established UI patterns

### Data Model Design

- **Flat structure preferred** - Avoid deep nesting
- **Use JSON Pointer paths** - Follow RFC 6901
- **Separate UI state from data** - Keep concerns separate

### Accessibility

- **Always include labels** - Every input needs a label
- **Mark required fields** - Use `required: true`
- **Provide error messages** - Plan for validation feedback
- **Support keyboard navigation** - Consider tab order

## Troubleshooting

### Error: "A2UI not enabled"

**Solution:** Enable A2UI in config:
```yaml
a2ui:
  enabled: true
```

### Error: "Catalog not found"

**Solution:** Create catalog or use preset:
```bash
cp .spec/ui-catalog.template.json .spec/ui-catalog.json
```

### Error: "Component not in catalog"

**Solution:** 
1. Use a different component from catalog
2. Add component to catalog using `smartspec_manage_ui_catalog`

### Error: "Invalid JSON Pointer path"

**Solution:** Check data binding paths:
- Must start with `/`
- Use `/` to separate levels
- Example: `/user/profile/name`

## Related Workflows

**Next steps after generating UI spec:**

1. **Implement UI:**
   ```bash
   /smartspec_implement_ui_from_spec \
     --spec specs/feature/spec-001-booking/ui-spec.json \
     --target-platform web \
     --output-dir src/ui/booking \
     --apply
   ```

2. **Generate tasks:**
   ```bash
   /smartspec_generate_tasks \
     specs/feature/spec-001-booking/spec.md \
     --apply
   ```

3. **Verify implementation:**
   ```bash
   /smartspec_verify_ui_implementation \
     --spec specs/feature/spec-001-booking/ui-spec.json \
     --implementation src/ui/booking \
     --target-platform web
   ```

## Security Considerations

- **Catalog-based security** - Only approved components can be used
- **No code execution** - Spec is declarative data only
- **Path validation** - All paths validated against allowlist
- **Secret redaction** - Secrets redacted from specs

## Version History

- **6.0.0** (2025-12-22): Initial release with A2UI v0.8 support

---

**Status:** Active  
**Requires Apply:** Yes (for final spec save)  
**Platform Support:** CLI, Kilo  
**Category:** UI Generation
