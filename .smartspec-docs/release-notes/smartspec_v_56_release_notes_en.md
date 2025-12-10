# SmartSpec v5.6 — Release Notes (EN)

SmartSpec **v5.6** is a major governance, safety, and usability upgrade across the SmartSpec ecosystem. This release strengthens workflow correctness, multi-platform behavior, dependency/security guardrails, and introduces an entirely new assistant experience to support every user.

---

## 🚀 New Feature: SmartSpec Copilot — Your Dedicated SmartSpec Help Assistant

SmartSpec 5.6 introduces **SmartSpec Copilot**, an always-on interactive assistant built using OpenAI CustomGPT:

👉 https://chatgpt.com/g/g-6936ffad015c81918e006a9ee2077074-smartspec-copilot

### What SmartSpec Copilot provides
You can now ask *any* SmartSpec-related question in natural language:
- Installation issues
- Understanding SmartSpec concepts & workflows
- How to run SPEC → PLAN → TASKS → IMPLEMENT
- How to use any workflow correctly in Kilo, Claude, Antigravity, or CLI
- Troubleshooting errors, missing files, index problems
- Understanding vibe coding, design philosophy, or workflow order

Copilot responds in English or any language you prefer, including Thai.  
It is now the **official support channel** for learning and using SmartSpec.

---

## 🌟 Highlights of SmartSpec v5.6

### 1. Unified Installation & Usage Flow
- Standardized installation scripts for macOS, Linux, and Windows.
- Clear directory layout after installation (`.smartspec/`, `.smartspec-docs/`, platform workflow folders).
- Consistent rules for command naming (`/smartspec_*` vs `.md --kilocode`).

### 2. Strengthened Workflow Governance
- Zero-removal backward compatibility policy.
- Mandatory **Legacy Flags Inventory** in all workflow upgrades.
- Strict role-based write guards (`NO-WRITE`, `READ-ONLY`, `ALLOW-WRITE`).
- Clarified mode defaults for Kilo Code, Claude Code, Antigravity.
- No internal workflow-calling; workflows use inline detection logic.

### 3. Multi-Repo & Multi-Registry Safety
- Unified flags: `--workspace-roots`, `--repos-config`.
- Clear registry precedence (`--registry-dir` primary, `--registry-roots` supplemental).
- Cross-repo duplication detection and enforced reuse.

### 4. SPEC → PLAN → TASKS → IMPLEMENT Improvements
- Mature index detection order for locating `SPEC_INDEX.json`.
- Task generation prioritizes concrete artefacts (schemas, OpenAPI, models).
- Implementation runs include validation, checkpointing, and per-run summaries.
- Verification workflows strengthened with strict **NO-WRITE** guarantees.

### 5. Advanced UI Governance
- Full JSON-first UI specification support (`ui.json`).
- Inline UI rules with modern UX guidance.
- Design system alignment (tokens, component registry, app-level components).
- Security-conscious UI validation (no secrets in UI JSON, safe patterns).

### 6. Critical Web Security & Dependency Guardrails
- Mandatory detection of React / Next.js / RSC usage.
- High-risk classification for `react-server-dom-*` dependencies.
- CVE-based upgrade requirements (including **CVE-2025-55182** baselines).
- Node/npm dependency governance (lockfiles, audits, CI gating).

### 7. New Tool Version Registry
A new canonical file:
```
.spec/registry/tool-version-registry.json
```
This governs:
- Minimum allowed versions
- Patch baselines
- Preventing framework downgrades
- Coordinated upgrades across multiple repositories

### 8. Improved Manuals & Documentation
- All manuals must start with the governance table header.
- Dual-language EN/TH manuals.
- Consistent workflow examples for Kilo and non-Kilo environments.
- Expanded examples for multi-repo, UI, and security scenarios.

### 9. Expanded Workflow Catalog
SmartSpec v5.6 includes a redesigned and expanded workflow catalog covering:
- Governance & portfolio
- Spec & plan generation
- Implementation
- Testing & quality
- UI & design system governance
- Security & NFR workflows
- Indexing, syncing, and environment verification

---

## 🧭 Migration Guidelines
If upgrading from SmartSpec 5.5.x or earlier:
1. Re-run the installer to sync `.smartspec/` and workflow updates.
2. Ensure `.spec/registry/` exists; adopt `tool-version-registry.json`.
3. Review UI specifications for JSON-first or inline compliance.
4. Use **SmartSpec Copilot** for onboarding and troubleshooting.

---

## 🎉 Summary
SmartSpec v5.6 delivers:
- **Stronger governance**
- **Centralized security & dependency control**
- **Better workflow consistency across platforms**
- **Modern UI governance and design-system alignment**
- **A new conversational assistant (SmartSpec Copilot) to support all users**

This release elevates SmartSpec into a safer, more reliable, and far more approachable AI-assisted development framework.

---

End of file.

