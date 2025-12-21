---
workflow_id: smartspec_ui_agent
version: "6.0.0"
status: active
category: ui
platform_support:
  - cli
  - kilo
requires_apply: false
---

# smartspec_ui_agent

**Interactive AI agent for conversational UI design and iterative refinement.**

## Purpose

This workflow provides an interactive, conversational interface for designing UI with A2UI. The agent guides users through UI design, provides suggestions, generates previews, and iteratively refines the design based on feedback. It's ideal for rapid prototyping, design exploration, and collaborative UI development.

## Governance contract

This workflow MUST follow:
- `knowledge_base_smartspec_handbook.md` (v6)
- A2UI Specification v0.8
- `.spec/smartspec.config.yaml`
- `.spec/ui-catalog.json`
- Design best practices

## Prerequisites

**Required:**
- A2UI must be enabled in `.spec/smartspec.config.yaml`
- UI component catalog

**Optional:**
- Existing UI specifications (for refinement)
- Design system tokens
- Brand guidelines

## Invocation

### CLI

```bash
/smartspec_ui_agent \
  --mode interactive \
  --context specs/feature/spec-002-contact
```

### Kilo Code

```bash
/smartspec_ui_agent.md \
  --mode interactive \
  --context specs/feature/spec-002-contact \
  --platform kilo
```

## Flags

### Universal Flags

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--platform` | string | No | Platform: cli, kilo (default: cli) |
| `--verbose` | boolean | No | Verbose output |
| `--report-dir` | path | No | Custom report directory |

### Workflow-Specific Flags

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--mode` | string | No | Mode: interactive, guided, quick (default: interactive) |
| `--context` | path | No | Context directory (spec, existing UI, etc.) |
| `--spec` | path | No | Existing UI spec to refine |
| `--requirements` | string | No | Initial requirements (quick mode) |
| `--target-platforms` | string | No | Target platforms: web, flutter, mobile (default: web) |
| `--design-system` | path | No | Path to design system tokens |
| `--save-session` | boolean | No | Save session for later (default: true) |
| `--session-id` | string | No | Resume previous session |

### Flag Usage Notes

**Modes:**
- `interactive`: Full conversational interface with suggestions
- `guided`: Step-by-step wizard with prompts
- `quick`: Fast generation from requirements

**Context:**
- Provides agent with project context
- Reads existing specs, requirements
- Understands project structure

**Session Management:**
- Sessions auto-saved to `.spec/ui-agent-sessions/`
- Resume with `--session-id`
- Sessions expire after 7 days

## Behavior

### Interactive Mode (default)

1. **Initialize Agent**
   - Load A2UI configuration
   - Load component catalog
   - Load context (if provided)
   - Initialize conversation

2. **Welcome & Context Gathering**
   - Greet user
   - Explain capabilities
   - Ask about project context
   - Understand requirements

3. **Conversational Design Loop**
   - **User input** → Agent processes
   - **Agent suggests** → User responds
   - **Agent generates preview** → User reviews
   - **User provides feedback** → Agent refines
   - Repeat until satisfied

4. **Design Suggestions**
   - Suggest components from catalog
   - Recommend layouts
   - Propose interactions
   - Suggest accessibility improvements

5. **Real-Time Preview Generation**
   - Generate UI spec on-the-fly
   - Show text-based preview
   - Provide visualization links
   - Update preview as design evolves

6. **Iterative Refinement**
   - Accept feedback ("make it bigger", "add validation", etc.)
   - Refine design
   - Regenerate preview
   - Confirm changes

7. **Finalization**
   - Review final design
   - Generate UI spec file
   - Suggest next steps
   - Save session

### Guided Mode

1. **Step-by-Step Wizard**
   - **Step 1:** What are you building?
   - **Step 2:** What components do you need?
   - **Step 3:** How should data flow?
   - **Step 4:** What actions are needed?
   - **Step 5:** Review and confirm

2. **Generate UI Spec**
   - Create spec from wizard answers
   - Show preview
   - Allow refinement

### Quick Mode

1. **Generate from Requirements**
   - Parse requirements string
   - Generate UI spec immediately
   - Show preview
   - Allow quick refinement

## Agent Capabilities

### 1. Conversational Understanding

**Agent understands:**
- Natural language requirements
- Design feedback ("make it bigger", "use blue", etc.)
- Component requests ("add a button", "need a form")
- Layout preferences ("side-by-side", "stacked")
- Interaction patterns ("on submit", "when clicked")

**Examples:**
```
User: "I need a contact form"
Agent: "I'll create a contact form. What fields do you need?"

User: "Name, email, and message"
Agent: "Got it. Should the name field be required?"

User: "Yes, all fields are required"
Agent: "Perfect. What should happen when the user submits?"

User: "Send to API and show success message"
Agent: "Understood. Here's a preview..."
```

### 2. Design Suggestions

**Agent suggests:**
- Appropriate components from catalog
- Layout patterns (forms, cards, lists)
- Interaction patterns (validation, loading states)
- Accessibility improvements (ARIA labels, keyboard nav)
- Error handling (validation messages, error states)

**Example:**
```
Agent: "I notice you have a form with many fields. 
       Would you like to:
       1. Group fields into sections
       2. Add a progress indicator
       3. Enable autosave"
```

### 3. Component Recommendations

**Agent recommends based on:**
- Use case (form → text-field, select, etc.)
- Data type (date → date-picker, number → number-input)
- Security level (only safe/trusted components)
- Platform compatibility

**Example:**
```
User: "I need a date input"
Agent: "I recommend using 'date-picker' component.
       It's trusted, accessible, and works on all platforms.
       Would you like to use it?"
```

### 4. Validation & Best Practices

**Agent validates:**
- Component catalog adherence
- Accessibility compliance
- Data model consistency
- Action definitions

**Agent enforces:**
- Required ARIA labels
- Keyboard navigation
- Error handling
- Loading states

### 5. Preview Generation

**Agent generates:**
- Text-based component tree
- JSON UI spec
- Visualization links (optional)
- Code snippets (optional)

**Example Preview:**
```
ContactForm
├── NameField (required)
│   └── label: "Name"
├── EmailField (required)
│   └── label: "Email"
│   └── validation: email format
├── MessageField (required)
│   └── label: "Message"
│   └── multiline: true
└── SubmitButton
    └── label: "Send"
    └── action: submit
```

### 6. Iterative Refinement

**Agent accepts feedback:**
- "Make the button bigger" → Update button size
- "Add validation to email" → Add email validation
- "Change label to 'Full Name'" → Update label
- "Move button to the right" → Update layout

**Agent confirms changes:**
```
Agent: "I've updated the button size to 'large'.
       Here's the updated preview..."
```

## Conversation Flow

### Example Session

```
Agent: Welcome to SmartSpec UI Agent! I'll help you design your UI.
       What would you like to build today?

User: A contact form for our website

Agent: Great! Let's design a contact form. What fields do you need?

User: Name, email, phone, and message

Agent: Perfect. Should any of these fields be optional?

User: Phone is optional, the rest are required

Agent: Got it. What should happen when the user submits the form?

User: Send to /api/contact endpoint

Agent: Understood. Should we show a loading state while submitting?

User: Yes, and show success message after

Agent: Excellent. Here's a preview of your contact form:

ContactForm
├── NameField (required)
├── EmailField (required)
├── PhoneField (optional)
├── MessageField (required)
└── SubmitButton
    └── Shows loading spinner while submitting
    └── Shows success message on completion

Would you like to:
1. Generate the UI spec
2. Refine the design
3. Add more features

User: Add validation to email and phone

Agent: I'll add email format validation and phone number validation.
       Updated preview:

ContactForm
├── NameField (required)
├── EmailField (required)
│   └── validation: email format ✓
├── PhoneField (optional)
│   └── validation: phone format ✓
├── MessageField (required)
└── SubmitButton

Looks good?

User: Yes, generate the spec

Agent: ✅ UI spec generated: specs/feature/spec-002-contact/ui-spec.json

Next steps:
1. Implement UI:
   /smartspec_implement_ui_from_spec \
     --spec specs/feature/spec-002-contact/ui-spec.json \
     --target-platform web \
     --apply

2. Verify implementation:
   /smartspec_verify_ui_implementation \
     --spec specs/feature/spec-002-contact/ui-spec.json \
     --implementation src/ui/contact \
     --target-platform web

Would you like to design another UI or refine this one?
```

## Output

### Session Files

```
.spec/ui-agent-sessions/<session-id>/
├── session.json                   # Session metadata
├── conversation.txt               # Full conversation log
├── design-iterations/             # Design iterations
│   ├── iteration-1.json
│   ├── iteration-2.json
│   └── iteration-3.json
└── final-spec.json                # Final UI spec
```

### Generated UI Spec

```
specs/feature/<feature-name>/
└── ui-spec.json                   # Generated UI specification
```

### Session Report

```
.spec/reports/ui-agent/<session-id>/
├── report.md                      # Session summary
├── design-evolution.md            # How design evolved
├── suggestions-made.md            # Suggestions agent made
└── final-spec.json                # Final UI spec
```

## Example Usage

### Example 1: Interactive Design

**Start interactive session:**

```bash
/smartspec_ui_agent \
  --mode interactive \
  --context specs/feature/spec-002-contact
```

**Conversation:**
```
Agent: What would you like to build?
User: A login form
Agent: What fields do you need?
User: Username and password
Agent: Should we add "Remember me" checkbox?
User: Yes
Agent: Here's a preview...
```

### Example 2: Guided Wizard

**Start guided wizard:**

```bash
/smartspec_ui_agent \
  --mode guided \
  --context specs/feature/spec-003-dashboard
```

**Wizard:**
```
Step 1/5: What are you building?
> Dashboard with metrics

Step 2/5: What components do you need?
> Cards, charts, tables

Step 3/5: How should data flow?
> Fetch from API on load

Step 4/5: What actions are needed?
> Refresh, filter, export

Step 5/5: Review and confirm
> [Shows preview]
```

### Example 3: Quick Generation

**Quick generation from requirements:**

```bash
/smartspec_ui_agent \
  --mode quick \
  --requirements "User profile page with avatar, name, email, bio, and edit button" \
  --context specs/feature/spec-010-profile
```

**Output:**
```
✅ UI spec generated in 5 seconds
📄 specs/feature/spec-010-profile/ui-spec.json

Preview:
UserProfile
├── Avatar
├── NameDisplay
├── EmailDisplay
├── BioDisplay
└── EditButton

Next: Implement UI
```

### Example 4: Refine Existing UI

**Refine existing UI spec:**

```bash
/smartspec_ui_agent \
  --mode interactive \
  --spec specs/feature/spec-002-contact/ui-spec.json
```

**Conversation:**
```
Agent: I've loaded your contact form. What would you like to change?
User: Add a phone field
Agent: I'll add a phone field. Should it be required?
User: Optional
Agent: Done. Here's the updated preview...
```

### Example 5: Multi-Platform Design

**Design for multiple platforms:**

```bash
/smartspec_ui_agent \
  --mode interactive \
  --target-platforms web,flutter \
  --context specs/feature/spec-004-booking
```

**Agent considers:**
- Platform-specific components
- Cross-platform compatibility
- Platform conventions

### Example 6: Resume Session

**Resume previous session:**

```bash
/smartspec_ui_agent \
  --session-id abc123
```

**Agent:**
```
Agent: Welcome back! Last time we were designing a contact form.
       You wanted to add phone validation. Ready to continue?
```

## Agent Commands

### During Conversation

**User can type:**
- `/preview` - Show current preview
- `/save` - Save current design
- `/reset` - Start over
- `/undo` - Undo last change
- `/help` - Show available commands
- `/exit` - Exit agent (saves session)

**Example:**
```
User: /preview

Agent: Current design:

ContactForm
├── NameField (required)
├── EmailField (required)
└── SubmitButton

User: /save

Agent: ✅ Design saved to session abc123
```

## Design Patterns

### Agent Recognizes Patterns

**Common patterns:**
- **Forms** - Collection of input fields with submit
- **Lists** - Repeating items with optional actions
- **Cards** - Grouped information with optional actions
- **Dashboards** - Multiple cards/widgets
- **Wizards** - Multi-step flows
- **Modals** - Overlay dialogs

**Example:**
```
User: "I need a multi-step registration form"

Agent: "I recognize this as a wizard pattern. 
       How many steps do you need?"

User: "Three: personal info, account details, confirmation"

Agent: "Perfect. I'll create a wizard with:
       1. Personal Info (name, email, phone)
       2. Account Details (username, password)
       3. Confirmation (review and submit)
       
       Shall I proceed?"
```

## Evidence sources

When answering questions, the agent MUST read:

1) **Knowledge base**
   - `knowledge_base_smartspec_handbook.md`
   - `knowledge_base_smartspec_install_and_usage.md`
   - `.smartspec/WORKFLOW_PARAMETERS_REFERENCE.md`

2) **A2UI Resources**
   - A2UI Specification v0.8
   - `.spec/ui-catalog.json`
   - `docs/a2ui/A2UI_SmartSpec_Integration_Report.md`

3) **Configuration**
   - `.spec/smartspec.config.yaml` (a2ui section)

4) **Context**
   - Files in `--context` directory
   - Existing UI specs
   - Project requirements

5) **Design Resources**
   - Design system tokens (if provided)
   - Brand guidelines (if provided)

## Best Practices

### When to Use UI Agent

**Use for:**
- Rapid prototyping
- Design exploration
- Learning A2UI
- Collaborative design sessions
- Iterative refinement

**Don't use for:**
- Batch generation (use smartspec_generate_ui_spec)
- Automated workflows (use other workflows)
- Production deployments (verify first)

### Effective Conversations

**Be specific:**
- ✅ "Add a required email field with validation"
- ❌ "Add email"

**Provide context:**
- ✅ "This is a checkout form, so emphasize the submit button"
- ❌ "Make button bigger"

**Iterate gradually:**
- ✅ Design → Review → Refine → Review → Finalize
- ❌ Try to specify everything at once

### Session Management

**Save sessions:**
- Sessions auto-save every 5 minutes
- Manually save with `/save` command
- Sessions expire after 7 days

**Resume sessions:**
- Use `--session-id` to resume
- Agent remembers context and progress

## Troubleshooting

### Issue: "Agent doesn't understand my request"

**Solution:** Be more specific:
```
Instead of: "Add input"
Try: "Add a text input field for user's name"
```

### Issue: "Agent suggests unavailable component"

**Solution:** Check catalog:
```bash
/smartspec_manage_ui_catalog --action list
```

Add component if needed:
```bash
/smartspec_manage_ui_catalog \
  --action add \
  --component-type <type> \
  --component-def <file> \
  --apply
```

### Issue: "Session not found"

**Solution:** Check session ID:
```bash
ls .spec/ui-agent-sessions/
```

Or start new session (agent will ask if you want to resume).

### Issue: "Preview not showing"

**Solution:** Type `/preview` command:
```
User: /preview
Agent: [Shows current design preview]
```

## Related Workflows

**After designing with agent:**

1. **Implement UI:**
   ```bash
   /smartspec_implement_ui_from_spec \
     --spec specs/feature/<feature>/ui-spec.json \
     --target-platform web \
     --apply
   ```

2. **Verify implementation:**
   ```bash
   /smartspec_verify_ui_implementation \
     --spec specs/feature/<feature>/ui-spec.json \
     --implementation src/ui/<feature> \
     --target-platform web
   ```

**Alternative workflows:**

3. **Quick generation (non-interactive):**
   ```bash
   /smartspec_generate_ui_spec \
     --requirements "..." \
     --spec specs/feature/<feature>/ui-spec.json \
     --apply
   ```

4. **Multi-platform generation:**
   ```bash
   /smartspec_generate_multiplatform_ui \
     --spec specs/feature/<feature>/ui-spec.json \
     --platforms web,flutter \
     --apply
   ```

## Security Considerations

- **Catalog validation** - Only approved components suggested
- **Session isolation** - Sessions are user-specific
- **No code execution** - Agent only generates specs
- **Input sanitization** - User input validated

## Version History

- **6.0.0** (2025-12-22): Initial release with A2UI v0.8 support

---

**Status:** Active  
**Requires Apply:** No (interactive, generates specs on request)  
**Platform Support:** CLI, Kilo  
**Category:** UI Design (Interactive)
