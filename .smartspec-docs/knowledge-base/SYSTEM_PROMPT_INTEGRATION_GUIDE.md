# System Prompt Integration Guide

## 1. Overview

To ensure that AI agents have the most accurate and up-to-date information, it is essential to integrate key knowledge base articles directly into their system prompts. This guide outlines which files to use and how to structure them for optimal performance.

## 2. The Consolidated Knowledge Base File

A new, consolidated file has been created specifically for this purpose:

**File:** `.smartspec-docs/knowledge-base/SYSTEM_PROMPT_KNOWLEDGE_BASE.md`

This file is a concatenation of the most critical knowledge base articles, ordered by importance, to provide a comprehensive but concise context for the AI.

### Source Files Included

The consolidated file is created by combining the following articles in this specific order:

1.  **ui-json-formats-comparison.md:** The most critical document for resolving user confusion. It directly addresses the core problem of the two UI JSON formats.
2.  **workflow-selection-guide.md:** Provides a clear decision-making framework, which is essential for guiding users to the correct workflow.
3.  **rjsf-schema-generation-concepts.md:** Details the specifics of the RJSF workflow, including its scope and limitations.
4.  **spec-ui-001-integration-guide.md:** Explains how the A2UI workflows fit together, providing a high-level architectural view.
5.  **theming-system-concepts.md:** Covers the foundational concepts of the theming system.
6.  **component-registry-concepts.md:** Explains the automation behind component mapping.

### Files Excluded and Rationale

-   **ai-feedback-loop-concepts.md** and **golden-tests-concepts.md:** These are important but less frequently confused topics. They can be retrieved by the AI via standard retrieval-augmented generation (RAG) when needed, rather than occupying valuable context space in every prompt.
-   **multi-level-theming-concepts.md:** The core concepts are already covered in the updated `theming-system-concepts.md`. This more detailed article can be retrieved via RAG.

## 3. Integration Strategy

To integrate this knowledge into your AI agents, follow this strategy:

1.  **Load the Content:** In your agent initialization process, load the full content of `SYSTEM_PROMPT_KNOWLEDGE_BASE.md`.

2.  **Inject into System Prompt:** Structure your system prompt to include this content under a clear heading. For example:

    ```
    You are a helpful AI assistant for the SmartSpec framework.

    <KnowledgeBase>
    {content of SYSTEM_PROMPT_KNOWLEDGE_BASE.md}
    </KnowledgeBase>

    Please answer the user's questions based on the provided knowledge base and your general expertise.
    ```

3.  **Prioritize the Knowledge Base:** Instruct the model to prioritize the information within the `<KnowledgeBase>` tags, as it is the most current and authoritative source.

## 4. Maintenance and Updates

This consolidated file should be treated as a build artifact. It should be regenerated whenever any of its source files are updated. This can be automated with a simple script in your CI/CD pipeline:

```bash
#!/bin/bash

KB_DIR=".smartspec-docs/knowledge-base"
OUTPUT_FILE="$KB_DIR/SYSTEM_PROMPT_KNOWLEDGE_BASE.md"

cat \
  "$KB_DIR/ui-json-formats-comparison.md" \
  "$KB_DIR/workflow-selection-guide.md" \
  "$KB_DIR/rjsf-schema-generation-concepts.md" \
  "$KB_DIR/spec-ui-001-integration-guide.md" \
  "$KB_DIR/theming-system-concepts.md" \
  "$KB_DIR/component-registry-concepts.md" \
  > "$OUTPUT_FILE"

echo "System prompt knowledge base updated."
```

By following this guide, you can ensure that your AI agents are equipped with the necessary knowledge to provide clear, accurate, and helpful answers, preventing the kind of user confusion that was previously identified.
