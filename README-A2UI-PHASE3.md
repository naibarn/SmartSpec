# A2UI Phase 3: Advanced Features - Complete Guide

**SmartSpec A2UI Integration - Phase 3**  
**Version:** 6.3.5  
**Date:** December 22, 2025  
**Status:** ✅ Complete

---

## Overview

Phase 3 adds **advanced features** to SmartSpec's A2UI integration, bringing **multi-platform generation** and **interactive design capabilities** that significantly enhance productivity and user experience.

### New Workflows (2)

1. **`smartspec_generate_multiplatform_ui`** - Generate UI for multiple platforms simultaneously
2. **`smartspec_ui_agent`** - Interactive AI agent for conversational UI design

---

## What's New in Phase 3

### 1. Multi-Platform Generation

**Before Phase 3:**
- Generate UI for one platform at a time
- Manually ensure consistency across platforms
- Separate commands for each platform

**After Phase 3:**
- ✅ Generate for multiple platforms with single command
- ✅ Automatic consistency checking
- ✅ Shared type definitions
- ✅ Cross-platform documentation

**Example:**
```bash
# Generate for Web and Flutter simultaneously
/smartspec_generate_multiplatform_ui \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --platforms web,flutter \
  --web-renderer lit \
  --output-dir src/ui/contact \
  --apply
```

**Result:**
```
src/ui/contact/
├── web/           # Lit implementation
├── flutter/       # Flutter implementation
├── shared/        # Shared types
└── docs/          # Cross-platform docs
```

---

### 2. Interactive UI Design Agent

**Before Phase 3:**
- Write requirements manually
- Generate UI spec
- Review and iterate manually

**After Phase 3:**
- ✅ Conversational UI design
- ✅ Real-time suggestions
- ✅ Iterative refinement
- ✅ Design pattern recognition
- ✅ Session management

**Example:**
```bash
/smartspec_ui_agent --mode interactive
```

**Conversation:**
```
Agent: What would you like to build?
User: A contact form
Agent: What fields do you need?
User: Name, email, and message
Agent: Should any fields be optional?
User: All required
Agent: Here's a preview...
```

---

## Workflow 1: smartspec_generate_multiplatform_ui

### Purpose

Generate platform-specific UI implementation code for **multiple target platforms** (Web, Flutter, etc.) from a **single A2UI specification**.

### Key Features

1. **Multi-Platform Support**
   - Web: Lit, React, Angular
   - Mobile: Flutter
   - Future: Native iOS/Android

2. **Consistency Checking**
   - Component parity verification
   - Data model consistency
   - Action compatibility
   - Accessibility parity

3. **Shared Types**
   - Generated once in `shared/` directory
   - Imported by all platforms
   - Ensures type consistency

4. **Cross-Platform Documentation**
   - Platform comparison table
   - Migration guide
   - Troubleshooting guide

### Usage

#### Basic: Web + Flutter

```bash
/smartspec_generate_multiplatform_ui \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --platforms web,flutter \
  --web-renderer lit \
  --output-dir src/ui/contact \
  --apply
```

#### With Shared Components

```bash
/smartspec_generate_multiplatform_ui \
  --spec specs/feature/spec-004-booking/ui-spec.json \
  --platforms web,flutter \
  --web-renderer lit \
  --output-dir src/ui/booking \
  --shared-components src/ui/shared \
  --apply
```

#### With Storybook

```bash
/smartspec_generate_multiplatform_ui \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --platforms web \
  --web-renderer lit \
  --output-dir src/ui/contact \
  --storybook \
  --apply
```

### Output Structure

```
<output-dir>/
├── web/
│   ├── components/
│   │   ├── ContactForm.ts
│   │   ├── NameField.ts
│   │   └── ...
│   ├── tests/
│   │   └── *.test.ts
│   ├── types/
│   │   └── ContactFormTypes.ts
│   └── README.md
├── flutter/
│   ├── lib/
│   │   ├── widgets/
│   │   │   ├── contact_form.dart
│   │   │   └── ...
│   │   └── models/
│   │       └── contact_form_model.dart
│   ├── test/
│   │   └── *_test.dart
│   └── README.md
├── shared/
│   ├── types/
│   │   ├── ContactFormTypes.ts
│   │   └── CommonTypes.ts
│   └── constants/
│       └── ValidationRules.ts
└── docs/
    ├── README.md
    ├── platform-comparison.md
    └── troubleshooting.md
```

### Consistency Checks

The workflow performs **automatic consistency verification**:

1. **Component Parity (100%)** - All components exist in all platforms
2. **Data Model (100%)** - Same properties, types, validation rules
3. **Actions (100%)** - Same actions with compatible parameters
4. **Accessibility** - WCAG-AA (web) + Material Semantics (flutter)

**Example Report:**
```
✅ Consistency Check: PASS

Component Parity: 100%
- ✅ ContactForm
- ✅ NameField
- ✅ EmailField
- ✅ MessageField
- ✅ SubmitButton

Data Model: 100%
- ✅ Same properties
- ✅ Same types
- ✅ Same validation rules

Actions: 100%
- ✅ submit
- ✅ validate
- ✅ reset
```

---

## Workflow 2: smartspec_ui_agent

### Purpose

Provide an **interactive, conversational interface** for designing UI with A2UI. The agent guides users through UI design, provides suggestions, generates previews, and iteratively refines the design.

### Key Features

1. **Conversational Understanding**
   - Natural language requirements
   - Design feedback ("make it bigger", etc.)
   - Component requests
   - Layout preferences

2. **Design Suggestions**
   - Appropriate components from catalog
   - Layout patterns (forms, cards, lists)
   - Interaction patterns
   - Accessibility improvements

3. **Real-Time Preview**
   - Text-based component tree
   - JSON UI spec
   - Visualization links

4. **Iterative Refinement**
   - Accept feedback
   - Refine design
   - Regenerate preview
   - Confirm changes

5. **Session Management**
   - Auto-save every 5 minutes
   - Resume previous sessions
   - Sessions expire after 7 days

### Modes

#### 1. Interactive Mode (default)

Full conversational interface with suggestions.

```bash
/smartspec_ui_agent --mode interactive
```

**Example Conversation:**
```
Agent: What would you like to build?
User: A contact form

Agent: What fields do you need?
User: Name, email, phone, and message

Agent: Should any fields be optional?
User: Phone is optional

Agent: What should happen when the user submits?
User: Send to /api/contact endpoint

Agent: Here's a preview:

ContactForm
├── NameField (required)
├── EmailField (required)
├── PhoneField (optional)
├── MessageField (required)
└── SubmitButton

Would you like to:
1. Generate the UI spec
2. Refine the design
3. Add more features

User: Add validation to email and phone

Agent: ✅ Added validation. Updated preview:

ContactForm
├── NameField (required)
├── EmailField (required)
│   └── validation: email format ✓
├── PhoneField (optional)
│   └── validation: phone format ✓
├── MessageField (required)
└── SubmitButton

User: Generate the spec

Agent: ✅ UI spec generated: specs/feature/spec-002-contact/ui-spec.json

Next steps:
1. Implement UI
2. Verify implementation
```

#### 2. Guided Mode

Step-by-step wizard with prompts.

```bash
/smartspec_ui_agent --mode guided
```

**Wizard:**
```
Step 1/5: What are you building?
> Contact form

Step 2/5: What components do you need?
> Name field, email field, message field, submit button

Step 3/5: How should data flow?
> Submit to API endpoint

Step 4/5: What actions are needed?
> Submit, validate, reset

Step 5/5: Review and confirm
> [Shows preview]
```

#### 3. Quick Mode

Fast generation from requirements.

```bash
/smartspec_ui_agent \
  --mode quick \
  --requirements "User profile page with avatar, name, email, bio, and edit button"
```

**Output:**
```
✅ UI spec generated in 5 seconds

Preview:
UserProfile
├── Avatar
├── NameDisplay
├── EmailDisplay
├── BioDisplay
└── EditButton

Next: Implement UI
```

### Agent Commands

During conversation, user can type:

- `/preview` - Show current preview
- `/save` - Save current design
- `/reset` - Start over
- `/undo` - Undo last change
- `/help` - Show available commands
- `/exit` - Exit agent (saves session)

### Design Patterns

Agent recognizes common patterns:

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
       3. Confirmation (review and submit)"
```

### Session Management

**Auto-save:**
- Sessions auto-save every 5 minutes
- Manually save with `/save` command

**Resume:**
```bash
/smartspec_ui_agent --session-id abc123
```

**Agent:**
```
Agent: Welcome back! Last time we were designing a contact form.
       You wanted to add phone validation. Ready to continue?
```

---

## Common Scenarios

### Scenario 1: Rapid Multi-Platform Prototyping

**Goal:** Create a contact form for both Web and Flutter quickly.

**Steps:**

1. **Design with agent:**
   ```bash
   /smartspec_ui_agent --mode interactive
   ```
   
   ```
   Agent: What would you like to build?
   User: Contact form with name, email, message
   Agent: [Guides through design]
   Agent: ✅ UI spec generated
   ```

2. **Generate for multiple platforms:**
   ```bash
   /smartspec_generate_multiplatform_ui \
     --spec specs/feature/spec-002-contact/ui-spec.json \
     --platforms web,flutter \
     --web-renderer lit \
     --output-dir src/ui/contact \
     --apply
   ```

3. **Verify both platforms:**
   ```bash
   # Web
   /smartspec_verify_ui_implementation \
     --spec specs/feature/spec-002-contact/ui-spec.json \
     --implementation src/ui/contact/web \
     --target-platform web

   # Flutter
   /smartspec_verify_ui_implementation \
     --spec specs/feature/spec-002-contact/ui-spec.json \
     --implementation src/ui/contact/flutter/lib \
     --target-platform flutter
   ```

**Time:** 10-15 minutes (vs hours manually)

---

### Scenario 2: Iterative Design Refinement

**Goal:** Refine existing UI based on feedback.

**Steps:**

1. **Load existing UI:**
   ```bash
   /smartspec_ui_agent \
     --mode interactive \
     --spec specs/feature/spec-002-contact/ui-spec.json
   ```

2. **Refine:**
   ```
   Agent: What would you like to change?
   User: Add a phone field
   Agent: Should it be required?
   User: Optional
   Agent: ✅ Done. Updated preview...
   ```

3. **Regenerate implementation:**
   ```bash
   /smartspec_generate_multiplatform_ui \
     --spec specs/feature/spec-002-contact/ui-spec.json \
     --platforms web,flutter \
     --web-renderer lit \
     --output-dir src/ui/contact \
     --apply
   ```

---

### Scenario 3: Design Exploration

**Goal:** Explore different UI designs quickly.

**Steps:**

1. **Start agent:**
   ```bash
   /smartspec_ui_agent --mode interactive
   ```

2. **Explore options:**
   ```
   Agent: What would you like to build?
   User: Dashboard with metrics
   
   Agent: I suggest:
   1. Card-based layout
   2. Grid layout
   3. List layout
   
   Which do you prefer?
   
   User: Card-based
   Agent: [Generates card-based design]
   
   User: Show me grid layout instead
   Agent: [Regenerates with grid layout]
   ```

3. **Save favorite:**
   ```
   User: /save
   Agent: ✅ Design saved to session abc123
   ```

---

### Scenario 4: Multi-Platform with Shared Components

**Goal:** Generate UI for multiple platforms using shared component library.

**Steps:**

1. **Generate with shared components:**
   ```bash
   /smartspec_generate_multiplatform_ui \
     --spec specs/feature/spec-004-booking/ui-spec.json \
     --platforms web,flutter \
     --web-renderer lit \
     --output-dir src/ui/booking \
     --shared-components src/ui/shared \
     --apply
   ```

**Result:**
- Imports shared components instead of regenerating
- Reduces code duplication
- Maintains consistency across features

---

## Complete Workflow Comparison

### Phase 1 (Foundation)

**Workflows:** 1
- `smartspec_generate_ui_spec`

**Capabilities:**
- Generate UI spec from requirements

### Phase 2 (Core)

**Workflows:** 3
- `smartspec_implement_ui_from_spec`
- `smartspec_verify_ui_implementation`
- `smartspec_manage_ui_catalog`

**Capabilities:**
- Generate platform code (single platform)
- Verify implementation
- Manage component catalog

### Phase 3 (Advanced) ← **NEW!**

**Workflows:** 2
- `smartspec_generate_multiplatform_ui` ← **NEW!**
- `smartspec_ui_agent` ← **NEW!**

**Capabilities:**
- Generate for multiple platforms simultaneously ← **NEW!**
- Interactive conversational design ← **NEW!**
- Automatic consistency checking ← **NEW!**
- Shared type generation ← **NEW!**
- Design pattern recognition ← **NEW!**
- Session management ← **NEW!**

---

## Best Practices

### Multi-Platform Generation

**Do:**
- ✅ Use when building for multiple platforms
- ✅ Enable consistency checking
- ✅ Generate shared types
- ✅ Verify each platform separately

**Don't:**
- ❌ Skip consistency checks without reason
- ❌ Modify generated code directly (regenerate instead)
- ❌ Use for platforms with significantly different UX

### Interactive Agent

**Do:**
- ✅ Be specific in requests
- ✅ Provide context
- ✅ Iterate gradually
- ✅ Save sessions frequently

**Don't:**
- ❌ Try to specify everything at once
- ❌ Skip preview reviews
- ❌ Ignore agent suggestions
- ❌ Forget to save sessions

---

## Troubleshooting

### Multi-Platform Generation

**Issue:** "Consistency check failed"

**Solution:** Review consistency report:
```
.spec/reports/generate-multiplatform-ui/.../consistency-report.md
```

Fix issues or skip check:
```bash
--consistency-check false
```

---

**Issue:** "Platform not supported"

**Solution:** Check platform name:
```bash
# Correct
--platforms web,flutter

# Incorrect
--platforms ios,android  # Use "flutter" instead
```

---

### Interactive Agent

**Issue:** "Agent doesn't understand my request"

**Solution:** Be more specific:
```
Instead of: "Add input"
Try: "Add a text input field for user's name"
```

---

**Issue:** "Session not found"

**Solution:** Check session ID:
```bash
ls .spec/ui-agent-sessions/
```

Or start new session.

---

## Next Steps

### After Phase 3

**Optional Phase 4: Integration**

Integrate A2UI workflows with existing SmartSpec workflows:
- UI specs in SPEC_INDEX
- UI tasks in tasks.md
- UI verification in verify_tasks_progress_strict
- UI documentation in docs_generator

**Estimated Effort:** 1-2 weeks

---

## Summary

**Phase 3 delivers:**

✅ **Multi-platform generation** - Single command, multiple platforms  
✅ **Interactive design** - Conversational UI creation  
✅ **Consistency checking** - Automatic verification  
✅ **Shared types** - Type safety across platforms  
✅ **Design patterns** - Pattern recognition and suggestions  
✅ **Session management** - Save and resume design sessions  

**Impact:**

- **10x faster** multi-platform development
- **100% consistency** across platforms
- **Intuitive** UI design experience
- **Reduced errors** with automatic checking

---

**Phase 3 Status:** ✅ **COMPLETE**  
**SmartSpec Version:** v6.3.5  
**Total Workflows:** 46  
**A2UI Workflows:** 6  
**Date:** December 22, 2025

🎉 **SmartSpec now has complete A2UI support with advanced features!** 🎉
