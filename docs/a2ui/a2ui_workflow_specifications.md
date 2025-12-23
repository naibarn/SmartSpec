# A2UI SmartSpec Workflow Specifications

**Date:** December 21, 2025  
**Purpose:** Detailed specifications for SmartSpec workflows integrating A2UI  
**Status:** Design Complete

---

## Overview

This document provides detailed specifications for six new SmartSpec workflows that integrate Google's A2UI protocol for agent-driven UI generation.

**Workflows:**
1. `smartspec_generate_ui_spec` - Generate A2UI specifications from requirements
2. `smartspec_implement_ui_from_spec` - Implement platform-specific UI from A2UI spec
3. `smartspec_manage_ui_catalog` - Manage A2UI component catalogs
4. `smartspec_verify_ui_implementation` - Verify UI implementation against spec
5. `smartspec_generate_multiplatform_ui` - Generate UI for multiple platforms
6. `smartspec_ui_agent` - Interactive UI design agent

---

## Workflow 1: `smartspec_generate_ui_spec`

### Purpose

Generate A2UI-compatible UI specification from natural language requirements.

### Governance Contract

**Must follow:**
- SmartSpec Handbook v6
- A2UI Specification v0.8
- `.spec/smartspec.config.yaml`
- `.spec/ui-catalog.json` (if exists)

### Invocation

**CLI:**
```bash
/smartspec_generate_ui_spec \
  --requirements "Create restaurant booking form" \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --platform web
```

**Kilo Code:**
```bash
/smartspec_generate_ui_spec.md \
  --requirements "Create restaurant booking form" \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --platform web \
  --platform kilo
```

### Flags

#### Universal Flags
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--apply` | boolean | No | Apply changes (default: preview mode) |
| `--platform` | string | No | Platform: cli, kilo (default: cli) |
| `--verbose` | boolean | No | Verbose output |
| `--dry-run` | boolean | No | Simulate without changes |
| `--report-dir` | path | No | Custom report directory |
| `--force` | boolean | No | Force overwrite existing files |

#### Workflow-Specific Flags
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--requirements` | string | Yes | Natural language UI requirements |
| `--spec` | path | Yes | Path to save ui-spec.json |
| `--target-platform` | string | No | Target platform: web, flutter, mobile, all (default: web) |
| `--catalog` | path | No | Path to component catalog (default: .spec/ui-catalog.json) |
| `--style` | string | No | Style preset: material, fluent, custom |
| `--accessibility` | string | No | Accessibility level: basic, wcag-aa, wcag-aaa |
| `--interactive` | boolean | No | Interactive mode with refinement |

### Behavior

**Preview Mode (default):**
1. Parse natural language requirements
2. Analyze UI patterns and components needed
3. Generate A2UI specification (JSON)
4. Create visual mockup/preview
5. Save to report directory (not to spec path)
6. Display preview and recommendations
7. Prompt user to review and run with `--apply`

**Apply Mode (`--apply`):**
1. Perform all preview mode steps
2. Validate A2UI specification
3. Check against component catalog
4. Save ui-spec.json to specified path
5. Update spec index
6. Generate documentation
7. Create usage examples

**Interactive Mode (`--interactive`):**
1. Generate initial UI spec
2. Show preview
3. Ask for feedback
4. Refine spec based on feedback
5. Repeat until user approves
6. Save final spec (if `--apply`)

### Output

**Preview Mode:**
```
.spec/reports/generate-ui-spec/<run-id>/
├── ui-spec-preview.json          # Generated A2UI spec
├── mockup.png                     # Visual mockup
├── component-analysis.md          # Components used
├── recommendations.md             # Suggestions
└── report.md                      # Full report
```

**Apply Mode (additional):**
```
specs/<category>/<spec-id>/
├── ui-spec.json                   # A2UI specification
├── ui-spec-docs.md                # Documentation
└── ui-spec-examples.md            # Usage examples

.spec/
└── SPEC_INDEX.json                # Updated index
```

### Example

**Requirements:**
```
Create a restaurant booking form with:
- Date picker for reservation date
- Time selector with available slots
- Number of guests selector (1-10)
- Special requests text area
- Submit button
- Show confirmation after submission
```

**Generated A2UI Spec (simplified):**
```json
{
  "version": "0.8",
  "surfaces": [
    {
      "id": "booking-form",
      "components": [
        {
          "id": "date-picker",
          "type": "date-picker",
          "label": "Reservation Date",
          "valuePath": "/booking/date",
          "required": true
        },
        {
          "id": "time-selector",
          "type": "select",
          "label": "Time",
          "valuePath": "/booking/time",
          "optionsPath": "/availableSlots",
          "required": true
        },
        {
          "id": "guests-selector",
          "type": "number-input",
          "label": "Number of Guests",
          "valuePath": "/booking/guests",
          "min": 1,
          "max": 10,
          "required": true
        },
        {
          "id": "special-requests",
          "type": "text-area",
          "label": "Special Requests",
          "valuePath": "/booking/specialRequests",
          "rows": 4
        },
        {
          "id": "submit-button",
          "type": "button",
          "label": "Book Table",
          "action": "submit-booking"
        }
      ]
    },
    {
      "id": "confirmation-dialog",
      "type": "dialog",
      "visible": false,
      "components": [
        {
          "id": "confirmation-message",
          "type": "text",
          "valuePath": "/booking/confirmationMessage"
        }
      ]
    }
  ],
  "dataModel": {
    "booking": {
      "date": null,
      "time": null,
      "guests": 2,
      "specialRequests": ""
    },
    "availableSlots": ["17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00"]
  }
}
```

---

## Workflow 2: `smartspec_implement_ui_from_spec`

### Purpose

Generate platform-specific UI implementation from A2UI specification.

### Governance Contract

**Must follow:**
- SmartSpec Handbook v6
- A2UI Specification v0.8
- Platform-specific guidelines
- `.spec/smartspec.config.yaml`

### Invocation

**CLI:**
```bash
/smartspec_implement_ui_from_spec \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --platform web \
  --renderer lit \
  --output-dir src/ui/booking
```

**Kilo Code:**
```bash
/smartspec_implement_ui_from_spec.md \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --platform web \
  --renderer lit \
  --output-dir src/ui/booking \
  --platform kilo
```

### Flags

#### Universal Flags
(Same as Workflow 1)

#### Workflow-Specific Flags
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--spec` | path | Yes | Path to ui-spec.json |
| `--target-platform` | string | Yes | Platform: web, flutter, react, angular |
| `--renderer` | string | No | Renderer: lit, angular, react (for web) |
| `--output-dir` | path | Yes | Output directory for implementation |
| `--style-framework` | string | No | CSS framework: tailwind, bootstrap, material |
| `--typescript` | boolean | No | Generate TypeScript (default: true) |
| `--tests` | boolean | No | Generate unit tests (default: true) |
| `--storybook` | boolean | No | Generate Storybook stories |

### Behavior

**Preview Mode:**
1. Read A2UI specification
2. Validate specification
3. Generate platform-specific code
4. Create component files
5. Generate styling files
6. Create integration guide
7. Save to report directory
8. Display preview and file list

**Apply Mode:**
1. Perform all preview steps
2. Write files to output directory
3. Update project configuration
4. Install dependencies (if needed)
5. Generate documentation
6. Create usage examples

### Output

**Preview Mode:**
```
.spec/reports/implement-ui/<run-id>/
├── components/                    # Generated components
├── styles/                        # Generated styles
├── integration-guide.md           # How to integrate
├── file-list.md                   # Files to be created
└── report.md                      # Full report
```

**Apply Mode (additional):**
```
src/ui/booking/
├── components/
│   ├── booking-form.ts            # Main form component
│   ├── date-picker.ts             # Date picker component
│   ├── time-selector.ts           # Time selector component
│   └── ...
├── styles/
│   ├── booking-form.css
│   └── ...
├── tests/
│   ├── booking-form.test.ts
│   └── ...
├── index.ts                       # Exports
└── README.md                      # Documentation
```

### Example

**Input:** `ui-spec.json` (from Workflow 1)

**Generated Code (Lit Web Component):**
```typescript
import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';

@customElement('booking-form')
export class BookingForm extends LitElement {
  @property({ type: Object }) booking = {
    date: null,
    time: null,
    guests: 2,
    specialRequests: ''
  };

  @property({ type: Array }) availableSlots = [
    '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00'
  ];

  static styles = css`
    :host {
      display: block;
      padding: 1rem;
    }
    .form-field {
      margin-bottom: 1rem;
    }
    label {
      display: block;
      margin-bottom: 0.5rem;
      font-weight: bold;
    }
  `;

  render() {
    return html`
      <form @submit=${this.handleSubmit}>
        <div class="form-field">
          <label for="date">Reservation Date</label>
          <input
            type="date"
            id="date"
            .value=${this.booking.date}
            @change=${this.handleDateChange}
            required
          />
        </div>

        <div class="form-field">
          <label for="time">Time</label>
          <select
            id="time"
            .value=${this.booking.time}
            @change=${this.handleTimeChange}
            required
          >
            ${this.availableSlots.map(slot => html`
              <option value=${slot}>${slot}</option>
            `)}
          </select>
        </div>

        <div class="form-field">
          <label for="guests">Number of Guests</label>
          <input
            type="number"
            id="guests"
            .value=${this.booking.guests}
            @change=${this.handleGuestsChange}
            min="1"
            max="10"
            required
          />
        </div>

        <div class="form-field">
          <label for="special-requests">Special Requests</label>
          <textarea
            id="special-requests"
            .value=${this.booking.specialRequests}
            @input=${this.handleSpecialRequestsChange}
            rows="4"
          ></textarea>
        </div>

        <button type="submit">Book Table</button>
      </form>
    `;
  }

  handleDateChange(e: Event) {
    this.booking = { ...this.booking, date: (e.target as HTMLInputElement).value };
  }

  handleTimeChange(e: Event) {
    this.booking = { ...this.booking, time: (e.target as HTMLSelectElement).value };
  }

  handleGuestsChange(e: Event) {
    this.booking = { ...this.booking, guests: parseInt((e.target as HTMLInputElement).value) };
  }

  handleSpecialRequestsChange(e: Event) {
    this.booking = { ...this.booking, specialRequests: (e.target as HTMLTextAreaElement).value };
  }

  handleSubmit(e: Event) {
    e.preventDefault();
    this.dispatchEvent(new CustomEvent('submit-booking', {
      detail: this.booking,
      bubbles: true,
      composed: true
    }));
  }
}
```

---

## Workflow 3: `smartspec_manage_ui_catalog`

### Purpose

Create and manage A2UI component catalogs for governance and reuse.

### Invocation

**CLI:**
```bash
/smartspec_manage_ui_catalog \
  --action create \
  --catalog .spec/ui-catalog.json
```

**Kilo Code:**
```bash
/smartspec_manage_ui_catalog.md \
  --action create \
  --catalog .spec/ui-catalog.json \
  --platform kilo
```

### Flags

#### Workflow-Specific Flags
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--action` | string | Yes | Action: create, update, add-component, remove-component, list |
| `--catalog` | path | Yes | Path to catalog file |
| `--component` | string | No | Component name (for add/remove) |
| `--component-def` | path | No | Component definition file (for add) |
| `--preset` | string | No | Preset catalog: material, fluent, custom |

### Behavior

**Actions:**

1. **create:** Create new catalog
2. **update:** Update existing catalog
3. **add-component:** Add component to catalog
4. **remove-component:** Remove component from catalog
5. **list:** List all components in catalog

### Output

```
.spec/
├── ui-catalog.json                # Component catalog
├── ui-catalog-docs.md             # Documentation
└── ui-catalog-registry.json       # Metadata
```

---

## Workflow 4: `smartspec_verify_ui_implementation`

### Purpose

Verify UI implementation matches A2UI specification.

### Invocation

**CLI:**
```bash
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --implementation src/ui/booking \
  --platform web
```

### Flags

#### Workflow-Specific Flags
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--spec` | path | Yes | Path to ui-spec.json |
| `--implementation` | path | Yes | Path to implementation directory |
| `--target-platform` | string | Yes | Platform: web, flutter, react |
| `--strict` | boolean | No | Strict verification mode |
| `--accessibility-check` | boolean | No | Check accessibility compliance |

### Output

```
.spec/reports/verify-ui/<run-id>/
├── verification-report.md         # Verification results
├── compliance-score.json          # Compliance metrics
├── issues.md                      # Found issues
└── recommendations.md             # Fix recommendations
```

---

## Workflow 5: `smartspec_generate_multiplatform_ui`

### Purpose

Generate UI for multiple platforms from single A2UI specification.

### Invocation

**CLI:**
```bash
/smartspec_generate_multiplatform_ui \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --platforms web,flutter \
  --output-base src/ui
```

### Flags

#### Workflow-Specific Flags
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--spec` | path | Yes | Path to ui-spec.json |
| `--platforms` | string | Yes | Comma-separated platforms: web,flutter,react |
| `--output-base` | path | Yes | Base directory for outputs |
| `--renderers` | string | No | Comma-separated renderers per platform |
| `--consistency-check` | boolean | No | Check cross-platform consistency |

### Output

```
src/ui/
├── web/
│   └── booking/
├── flutter/
│   └── booking/
└── react/
    └── booking/

.spec/reports/generate-multiplatform-ui/<run-id>/
├── consistency-report.md          # Cross-platform consistency
├── platform-web.md                # Web-specific report
├── platform-flutter.md            # Flutter-specific report
└── integration-guide.md           # Integration guide
```

---

## Workflow 6: `smartspec_ui_agent`

### Purpose

Interactive UI design agent using A2UI for real-time collaboration.

### Invocation

**CLI:**
```bash
/smartspec_ui_agent \
  --mode interactive
```

### Flags

#### Workflow-Specific Flags
| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--mode` | string | Yes | Mode: interactive, generate, refine |
| `--spec` | path | No | Path to ui-spec.json (for refine mode) |
| `--context` | string | No | User context for dynamic generation |
| `--transport` | string | No | Transport: a2a, websocket, sse (default: websocket) |

### Behavior

**Interactive Mode:**
1. Start interactive session
2. User describes UI requirements
3. Agent generates A2UI messages in real-time
4. Client renders UI progressively
5. User provides feedback
6. Agent refines UI
7. Repeat until satisfied
8. Save final ui-spec.json

**Generate Mode:**
1. Generate UI from requirements
2. Stream A2UI messages
3. Client renders
4. Save ui-spec.json

**Refine Mode:**
1. Load existing ui-spec.json
2. User describes changes
3. Agent updates UI incrementally
4. Save updated ui-spec.json

### Output

```
.spec/reports/ui-agent/<session-id>/
├── session-transcript.md          # Conversation transcript
├── ui-spec-final.json             # Final UI specification
├── iterations/                    # UI iterations
│   ├── iteration-1.json
│   ├── iteration-2.json
│   └── ...
└── report.md                      # Session report
```

---

## Integration with Existing SmartSpec Workflows

### Workflow Integration Points

**1. `smartspec_generate_spec` → `smartspec_generate_ui_spec`**
- Generate functional spec first
- Then generate UI spec from functional requirements
- Link UI spec to functional spec

**2. `smartspec_generate_tasks` → `smartspec_implement_ui_from_spec`**
- Generate tasks including UI implementation
- Use A2UI spec as input for UI tasks
- Automated UI implementation from tasks

**3. `smartspec_implement_tasks` → `smartspec_verify_ui_implementation`**
- Implement UI tasks
- Verify implementation against A2UI spec
- Automated verification as part of implementation

**4. `smartspec_verify_tasks` → `smartspec_verify_ui_implementation`**
- Verify all tasks including UI
- UI verification as part of overall verification
- Comprehensive quality assurance

### Example End-to-End Flow

```
1. Requirements (Natural Language)
   ↓
2. /smartspec_generate_spec
   → specs/feature/spec-001/spec.md
   ↓
3. /smartspec_generate_ui_spec
   → specs/feature/spec-001/ui-spec.json
   ↓
4. /smartspec_generate_tasks
   → specs/feature/spec-001/tasks.md (includes UI tasks)
   ↓
5. /smartspec_implement_tasks
   → src/ (implementation)
   ↓
6. /smartspec_implement_ui_from_spec
   → src/ui/ (UI implementation)
   ↓
7. /smartspec_verify_ui_implementation
   → verification report
   ↓
8. /smartspec_verify_tasks
   → overall verification report
```

---

## Configuration

### `.spec/smartspec.config.yaml` Updates

```yaml
# A2UI Configuration
a2ui:
  enabled: true
  version: "0.8"
  
  # Renderers
  renderers:
    web: "lit"          # lit, angular, react
    mobile: "flutter"   # flutter
    
  # Catalog
  catalog:
    path: ".spec/ui-catalog.json"
    preset: "material"  # material, fluent, custom
    
  # Transport
  transport: "websocket"  # a2a, websocket, sse
  
  # Generation
  generation:
    style: "material"
    accessibility: "wcag-aa"
    typescript: true
    tests: true
    storybook: false
    
  # Verification
  verification:
    strict: false
    accessibility_check: true
    cross_platform_consistency: true
```

---

## Dependencies

### Package Dependencies

**Node.js:**
```json
{
  "dependencies": {
    "@a2ui/core": "^0.8.0",
    "@a2ui/lit-renderer": "^0.8.0",
    "@a2ui/flutter-renderer": "^0.8.0",
    "lit": "^3.0.0"
  },
  "devDependencies": {
    "@a2ui/testing": "^0.8.0"
  }
}
```

**Python (for SmartSpec workflows):**
```
a2ui-python==0.8.0
```

---

## Summary

These six workflows provide comprehensive A2UI integration with SmartSpec, enabling:

1. ✅ **AI-powered UI specification generation**
2. ✅ **Automated platform-specific implementation**
3. ✅ **Governed component catalog management**
4. ✅ **Automated UI verification**
5. ✅ **Cross-platform UI generation**
6. ✅ **Interactive UI design agent**

All workflows follow SmartSpec's **preview-first pattern** and integrate seamlessly with existing SmartSpec workflows for end-to-end development automation.

---

**Status:** Design Complete  
**Next Step:** Implementation  
**Estimated Effort:** 8-10 weeks for full implementation
