# SmartSpec Workflow: Security Threat Modeler

**Workflow:** `/smartspec_security_threat_modeler`  
**Version:** 6.1.0

## 1. Overview

The Security Threat Modeler is an automated workflow that generates a preliminary threat model by analyzing your project's `spec.md` and `plan.md`. It helps identify and document potential security risks early in the development lifecycle, using standard methodologies like STRIDE.

This process creates a `threats.md` artifact, providing a structured overview of potential vulnerabilities before any code is written.

## 2. Key Features

- **Automated Analysis:** Parses specification documents to identify assets, trust boundaries, and potential threats.
- **STRIDE Framework:** Applies the STRIDE methodology (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) to categorize threats.
- **Governed Writes:** Safely creates or updates the `threats.md` file only when the `--apply` flag is used.
- **Non-Destructive:** Merges new findings into an existing `threats.md` without overwriting manual entries.
- **Secure by Design:** Operates without network access and redacts sensitive information from all outputs.

## 3. How It Works

The workflow performs the following steps:

1.  **Parses Inputs:** Reads the `spec.md` and `plan.md` to understand the system's components, data flows, and user roles.
2.  **Identifies Assets:** Defines what needs protection, such as user data, authentication services, and APIs.
3.  **Applies STRIDE Analysis:**
    -   **Spoofing:** Checks for weak authentication.
    -   **Tampering:** Looks for data flows lacking integrity checks (e.g., no HTTPS).
    -   **Repudiation:** Identifies actions that lack a clear audit trail.
    -   **Information Disclosure:** Pinpoints sensitive data and checks for encryption.
    -   **Denial of Service:** Checks for rate limiting and resource management.
    -   **Elevation of Privilege:** Analyzes user roles for potential escalation paths.
4.  **Generates `threats.md`:** Creates a structured Markdown file detailing each identified threat, its category, assets at risk, and suggested mitigations.

## 4. Usage

### Command Line

To generate a preview of the threat model:

```bash
/smartspec_security_threat_modeler specs/my-feature/spec.md
```

To create or update the `threats.md` file:

```bash
/smartspec_security_threat_modeler specs/my-feature/spec.md --apply
```

### Kilo Code

```bash
/smartspec_security_threat_modeler.md specs/my-feature/spec.md --apply
```

## 5. Input and Flags

- **`spec_md` (Required):** Path to the `spec.md` file.
- **`--apply` (Optional):** Applies the changes and writes to `threats.md`.
- **`--framework <STRIDE|DREAD>` (Optional):** Specifies the threat modeling framework. Defaults to `STRIDE`.
- **`--json` (Optional):** Outputs the report in JSON format.

## 6. Output Artifact: `threats.md`

The primary output is a `threats.md` file with the following structure:

```markdown
# Threat Model for <Spec Title>

**Spec ID:** my-feature
**Framework:** STRIDE

## Summary

| Threat Category        | Threats Identified |
| ---------------------- | ------------------ |
| Spoofing               | 2                  |
| Information Disclosure | 4                  |

---

## Identified Threats

### T-001: [Spoofing] User Impersonation

- **Description**: An attacker could potentially impersonate another user due to weak session management.
- **Asset at Risk**: User Account, User Data
- **Affected Component**: Authentication Service
- **Suggested Mitigation**: Implement secure session management with short-lived tokens.

### T-002: [Information Disclosure] Sensitive Data in Logs

- **Description**: The specification does not explicitly forbid logging of sensitive user data.
- **Asset at Risk**: User PII
- **Affected Component**: Logging Subsystem
- **Suggested Mitigation**: Implement redaction of sensitive fields in all logs.
```

## 7. Use Cases

- **Proactive Security:** Identify and mitigate security risks before development begins.
- **Security Reviews:** Provide a baseline document for manual security reviews.
- **Compliance:** Generate auditable evidence of security considerations.
