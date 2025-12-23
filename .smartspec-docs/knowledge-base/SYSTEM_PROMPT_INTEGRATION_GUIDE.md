# System Prompt Integration Guide

## 1. Overview

To ensure that AI agents have the most accurate and up-to-date information about SmartSpec workflows, critical knowledge base files have been placed in the `.smartspec/` directory where system prompts can access them.

## 2. The Critical Knowledge Base Files

The following files in `.smartspec/` are essential for preventing user confusion:

### Primary File for System Prompts

**File:** `.smartspec/knowledge_base_a2ui_workflows.md`

This is the **most critical file** for resolving the confusion about UI JSON formats. It contains:

1. **ui-json-formats-comparison:** Clear comparison between RJSF and A2UI formats
2. **workflow-selection-guide:** Decision tree for choosing the right workflow

**Why this file is critical:**
- Directly addresses the core problem: users don't know there are two UI JSON formats
- Provides clear warnings about renderer compatibility
- Includes decision trees and comparison tables
- Prevents the exact confusion shown in the user's screenshots

### Supporting Files

**File:** `.smartspec/ui-json-formats-comparison.md`
- Standalone comparison guide
- Can be referenced separately if needed

**File:** `.smartspec/workflow-selection-guide.md`
- Standalone decision tree
- Can be referenced separately if needed

## 3. Integration Strategy

### For System Prompts

Load the consolidated file into your AI agent's system prompt:

```python
# Python example
with open('.smartspec/knowledge_base_a2ui_workflows.md', 'r') as f:
    a2ui_knowledge = f.read()

system_prompt = f"""
You are a helpful AI assistant for the SmartSpec framework.

<A2UIKnowledgeBase>
{a2ui_knowledge}
</A2UIKnowledgeBase>

CRITICAL INSTRUCTIONS:
1. When users ask about UI JSON or form generation, ALWAYS check this knowledge base first
2. Make it clear that there are TWO distinct UI JSON formats: RJSF and A2UI
3. Guide users to the correct workflow based on their renderer
4. Warn about compatibility issues if they choose the wrong format

Please answer the user's questions based on the provided knowledge base.
"""
```

### Key Points to Emphasize in System Prompts

1. **Two Formats Exist:** Always clarify that `/smartspec_generate_rjsf_schema` and `/smartspec_generate_ui_spec` produce different outputs
2. **Renderer Matters:** The choice depends on whether the user has an RJSF renderer or an A2UI renderer
3. **Not Interchangeable:** RJSF schemas won't work with A2UI renderers and vice versa
4. **Decision Tree:** Guide users through the decision tree in the knowledge base

## 4. File Locations

### Core Framework Files (Downloaded to User's Machine)
```
.smartspec/
├── knowledge_base_a2ui_workflows.md        ← PRIMARY FILE FOR SYSTEM PROMPTS
├── ui-json-formats-comparison.md           ← Individual component
├── workflow-selection-guide.md             ← Individual component
├── Knowledge-Base.md                       ← General SmartSpec KB
├── knowledge_base_smartspec_handbook.md    ← Handbook
└── knowledge_base_smartspec_install_and_usage.md  ← Install guide
```

### Documentation Files (For Human Reading)
```
.smartspec-docs/
└── knowledge-base/
    ├── ui-json-formats-comparison.md
    ├── workflow-selection-guide.md
    ├── rjsf-schema-generation-concepts.md
    ├── spec-ui-001-integration-guide.md
    ├── theming-system-concepts.md
    ├── component-registry-concepts.md
    └── ... (other detailed articles)
```

## 5. Maintenance

### When to Update

Update `.smartspec/knowledge_base_a2ui_workflows.md` whenever:
1. New UI-related workflows are added
2. Format specifications change
3. Renderer compatibility issues are discovered
4. User confusion patterns emerge

### How to Update

```bash
#!/bin/bash
# Regenerate the consolidated knowledge base

cd .smartspec

cat \
  ui-json-formats-comparison.md \
  workflow-selection-guide.md \
  > knowledge_base_a2ui_workflows.md

echo "A2UI knowledge base updated!"
```

## 6. Why This Structure?

### `.smartspec/` vs `.smartspec-docs/`

-   **`.smartspec/`** contains files that are:
    -   Downloaded to the user's machine during installation
    -   Accessed by AI agents via system prompts
    -   Critical for runtime decision-making
    -   Concise and focused

-   **`.smartspec-docs/`** contains files that are:
    -   For human reading and reference
    -   More detailed and comprehensive
    -   Not loaded into system prompts (too large)
    -   Accessed via documentation websites or direct reading

By keeping the critical knowledge in `.smartspec/`, we ensure that AI agents always have access to the most important information without overwhelming the system prompt with unnecessary details.

## 7. Expected Outcome

With this integration, AI agents will:

1. ✅ Immediately recognize when a user is asking about UI generation
2. ✅ Clarify that two distinct formats exist
3. ✅ Ask about the user's renderer before recommending a workflow
4. ✅ Provide clear warnings about compatibility
5. ✅ Guide users through the decision tree
6. ✅ Prevent the confusion shown in the original user screenshots

This structure ensures that the knowledge base is both accessible to AI agents and maintainable by developers.
