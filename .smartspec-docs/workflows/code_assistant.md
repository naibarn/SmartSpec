_# SmartSpec Workflow: Code Assistant

**Workflow:** `/smartspec_code_assistant`  
**Version:** 6.1.1

## 1. Overview

The Code Assistant is a general-purpose, interactive workflow for getting help with coding tasks within the context of a specific `spec.md`. It acts as a flexible, spec-aware assistant that can answer questions, generate code snippets, and provide guidance on implementation, all while respecting the project's governance rules.

This is a **reports-only** workflow. It provides information and suggestions but does not write or modify any code on its own.

## 2. Key Features

- **Spec-Aware Context:** Understands the context of the provided `spec.md` to give relevant answers.
- **Interactive Q&A:** Allows you to ask freeform questions about implementation, libraries, or best practices.
- **Code Generation:** Can generate boilerplate code, functions, or snippets that align with the spec.
- **Safe and Read-Only:** Does not modify any files, making it a safe tool for exploration and assistance.

## 3. How It Works

1.  **Loads Context:** Reads the specified `spec.md` and any other context files provided (like `tasks.md`).
2.  **Receives Prompt:** Takes a user's natural language question or request as input.
3.  **Generates Response:** Uses its understanding of the context to generate a helpful response, which could be an explanation, a code snippet, or a suggested command.
4.  **Outputs Report:** Delivers the response in a standard report format.

## 4. Usage

### Ask a Question

```bash
/smartspec_code_assistant \
  specs/my-feature/spec.md \
  --prompt "What is the best library for handling JWT authentication in Node.js?"
```

### Generate a Code Snippet

```bash
/smartspec_code_assistant \
  specs/my-feature/spec.md \
  --prompt "Generate a TypeScript function to validate an email address based on the User model in the spec."
```

## 5. Input and Flags

- **`spec_md` (Required):** Path to the `spec.md` file to provide context.
- **`--prompt <string>` (Required):** The question or request for the assistant.
- **`--tasks <path>` (Optional):** Path to a `tasks.md` file for additional context.

## 6. Output: Assistant's Response

The output is a report containing the assistant's answer to your prompt.

### Example Report Snippet

```markdown
### Prompt

> Generate a TypeScript function to validate an email address based on the User model in the spec.

### Response

Based on the `User` model in `specs/my-feature/spec.md`, which defines the email format, here is a TypeScript function using the `zod` library for validation:

```typescript
import { z } from 'zod';

const UserEmailSchema = z.string().email({ message: "Invalid email address" });

export function validateEmail(email: string): boolean {
  try {
    UserEmailSchema.parse(email);
    return true;
  } catch (error) {
    return false;
  }
}
```

This function aligns with the constraints specified in your spec.
```

## 7. Use Cases

- **Quick Implementation Help:** Get unstuck by asking for help with a specific coding problem.
- **Boilerplate Generation:** Generate repetitive code quickly, such as model definitions or API client functions.
- **Explore Best Practices:** Ask for advice on the best way to implement a feature according to modern standards.
_
