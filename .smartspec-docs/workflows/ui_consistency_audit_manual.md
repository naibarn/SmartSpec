---
manual_name: /smartspec_ui_consistency_audit Manual (EN)
manual_version: 5.6
compatible_workflow: /smartspec_ui_consistency_audit
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (design system, frontend, UX, QA, release, platform)
---

# /smartspec_ui_consistency_audit Manual (v5.6, English)

## 1. Overview

This manual explains how to use the workflow:

> `/smartspec_ui_consistency_audit v5.6.2+`

The workflow is a **governance layer for UI design & UX consistency**.
It focuses on:

- checking that implemented UI **uses the design system / design tokens
  / component library consistently**
- evaluating **pattern consistency** across screens/flows, including:
  - colors / typography / spacing / radius / shadows
  - consistent use and reuse of components and patterns
  - state handling (hover, focus, disabled, loading)
  - theming (light/dark mode, multi-brand)
  - naming conventions (components, tokens, variants)
- comparing implementation against **design system registry, brand
  guidelines, UI specs / UI JSON**
- producing a **UI consistency audit report** per UI unit
  (route/screen/flow) with `risk_level` and `blocking_for_release`
  signals
- from v5.6.2 onwards, treating **AI-generated `ui.json`** as a
  first-class input:
  - origin (AI vs human vs mixed)
  - review status
  - design system version and style preset
  - overall `ui.json` structural quality

> **Governance-only:**
> - This workflow is **verification/governance + NO-WRITE**.
> - It does not modify UI code, CSS, themes, or configs.
> - It does not create patches/PRs or apply refactors.
> - It does not run tests or launch browsers/devices.
> - It only reads artifacts and produces an audit report.
>
> **Scope vs `/smartspec_ui_validation`:**
> - `/smartspec_ui_consistency_audit` focuses on **design/system
>   consistency** (tokens, spacing, patterns, themes, naming, AI UI JSON
>   quality).
> - `/smartspec_ui_validation` focuses on **correctness & coverage**
>   (behavior, a11y, i18n, test coverage).
> - They are complementary and often used together.

Use this workflow when you want a **structured view of how consistently
(and safely) your UI adheres to the design system and brand standards**,
including how much you can trust AI-generated `ui.json` for each UI
unit.

### 1.1 Why you need this workflow

Without a dedicated UI consistency governance layer, teams often face:

- a design system exists, but each team uses it differently → the
  product looks like multiple brands in one
- design tokens exist, but code is still full of hard-coded colors,
  spacing, and shadows
- dark mode or multi-brand theming is only correct on some screens
- AI generates UI JSON with different style presets or misaligned
  layouts, but nobody sees the full picture
- naming conventions drift, making it harder for both humans and AI to
  reason about components and patterns

`/smartspec_ui_consistency_audit` helps you answer:

> "How well does our UI, across flows/screens, actually follow the
> design system?"  
> "Where is AI-generated `ui.json` aligned with the system — and where
> is it drifting?"

### 1.2 Risks if you don’t use it (or equivalent governance)

- Your design system becomes a document, not a practice.
- AI continues to generate inconsistent `ui.json` that leaks into
  production.
- Dark mode and branding are broken or inconsistent only on some flows.
- Future redesigns or theme changes become extremely hard and risky
  because the current UI is not aligned with tokens/patterns.

---

## 2. What’s New in v5.6

### 2.1 Per-UI-unit status model

Each UI unit (screen/route/flow/component group) receives a status
record with fields such as:

- `unit_id`
- `criticality = CRITICAL | HIGH | MEDIUM | LOW | UNKNOWN`
- `ui_spec_origin = AI | HUMAN | MIXED | UNKNOWN`
- `ui_spec_review_status = UNREVIEWED | DESIGNER_APPROVED | OVERRIDDEN | UNKNOWN`
- `ui_json_quality_status = STRONG | OK | WEAK | BROKEN | UNKNOWN`
- `design_system_alignment_status = GOOD | MINOR_DRIFT | MAJOR_DRIFT | UNKNOWN`
- `token_usage_status = CONSISTENT | MIXED | HARD_CODED | UNKNOWN`
- `spacing_consistency_status = CONSISTENT | MINOR_ISSUES | MAJOR_ISSUES | UNKNOWN`
- `typography_consistency_status = CONSISTENT | MINOR_ISSUES | MAJOR_ISSUES | UNKNOWN`
- `component_pattern_consistency_status = CONSISTENT | PARTIAL | FRAGMENTED | UNKNOWN`
- `state_handling_consistency_status = GOOD | MINOR_ISSUES | MAJOR_ISSUES | UNKNOWN`
- `dark_mode_consistency_status = NOT_APPLICABLE | CONSISTENT | PARTIAL | BROKEN | UNKNOWN`
- `naming_consistency_status = GOOD | MINOR_ISSUES | MAJOR_ISSUES | UNKNOWN`
- `risk_level = LOW | MEDIUM | HIGH | CRITICAL`
- `blocking_for_release = true | false`
- `notes`

### 2.2 AI-generated `ui.json` as a first-class signal

From v5.6.2 onwards:

- the workflow expects (but does not strictly require) a `meta` block in
  `ui.json`, e.g.:

  ```jsonc
  {
    "meta": {
      "source": "ai",              // ai | human | mixed | unknown
      "generator": "kilo-code-vX", // or workflow/agent id
      "design_system_version": "ds-v3.1",
      "style_preset": "modern-dashboard-v2",
      "review_status": "unreviewed" // unreviewed | designer_approved | overridden
    },
    "screens": [ /* ... */ ]
  }
  ```

- meta is used to derive:
  - `ui_spec_origin`
  - `ui_spec_review_status`
  - `ui_json_quality_status`

A new flag is introduced:

- `--ui-json-ai-strict`
  - enforces stricter rules for AI-generated UI JSON:
    - missing/inconsistent `design_system_version` or `style_preset`
      are treated as gaps.
    - `ui_spec_origin=AI` and `ui_spec_review_status=UNREVIEWED` for
      critical/high units raise risk.

### 2.3 Strict mode with design & AI awareness

In `--safety-mode=strict`, especially for units with
`criticality in {CRITICAL, HIGH}`:

- `design_system_alignment_status=MAJOR_DRIFT` → often blocking.
- `token_usage_status=HARD_CODED` on core surfaces → high risk.
- `dark_mode_consistency_status=BROKEN` where dark mode is required →
  blocking.
- `ui_spec_origin=AI` and `ui_spec_review_status=UNREVIEWED`, or
  `ui_json_quality_status=WEAK/BROKEN` → considered high risk and may
  be `blocking_for_release`.
- business-logic-like constructs found in `ui.json` (e.g., full `if`
  conditions, role checks) are treated as severe governance issues.

---

## 3. Backward Compatibility Notes

- This v5.6 manual targets `/smartspec_ui_consistency_audit` from
  **v5.6.2 onwards** (5.6.x series).
- Existing flags are preserved; new flags such as `--ui-json-ai-strict`
  are **additive**.
- Status model and strict-mode rules are extended, not changed
  incompatibly.

---

## 4. Core Concepts

### 4.1 UI unit

A UI unit can be:

- a route (e.g., `/checkout`, `/login`)
- a screen (e.g., "Profile Screen")
- a flow (e.g., "Checkout Flow", "Onboarding Wizard")
- a component group (e.g., "Form Controls", "Primary Buttons")

### 4.2 Criticality

Criticality reflects how important the unit is, based on:

- central registries (e.g., `.spec/registry/` entries for critical
  flows)
- tags in specs/UI JSON
- optional overrides (e.g., from upstream workflows that mark UI
  critical targets)

Levels:

- CRITICAL: login, checkout, payment, consent, account recovery, etc.
- HIGH: major business-impact surfaces.
- MEDIUM/LOW: secondary surfaces.

### 4.3 Design system alignment

The audit checks whether UI uses the design system correctly, focusing
on:

- colors / tokens / contrast
- spacing scale and layout rhythm
- typography scale and styles
- component reuse vs custom one-off components
- state handling (hover, focus, disabled, loading)
- themes (light/dark, brand variations)

### 4.4 AI-generated `ui.json`

When `ui.json` is primarily AI-generated:

- `ui_spec_origin = AI`
- `ui_spec_review_status` is taken from `meta.review_status` where
  available
- `ui_json_quality_status` summarizes whether the structure of
  `ui.json` looks coherent and aligned with the design system

For critical/high flows, combinations like `origin=AI + UNREVIEWED` or
`quality=WEAK/BROKEN` are strong signals of design governance risk.

---

## 5. Quick Start Examples

### 5.1 Audit consistency for a web portal

```bash
smartspec_ui_consistency_audit \
  --spec-ids=web_portal \
  --run-label=web-portal-ui-consistency \
  --ui-spec-paths=".spec/ui/**/*.json" \
  --ui-impl-paths="apps/web/src/**/*.{tsx,jsx,vue}" \
  --design-tokens-paths="design-system/tokens/**/*.json" \
  --design-system-doc-paths="design-system/docs/**/*.md" \
  --theme-config-paths="design-system/themes/**/*.json" \
  --target-envs=web \
  --target-brands=default \
  --report-format=md \
  --stdout-summary
```

### 5.2 Strict for AI-generated checkout UI JSON

```bash
smartspec_ui_consistency_audit \
  --spec-ids=checkout_service \
  --run-label=checkout-ui-consistency-ai-strict \
  --ui-spec-paths=".spec/ui/**/*.json" \
  --ui-impl-paths="apps/checkout/src/**/*.{tsx,jsx}" \
  --design-tokens-paths="design-system/tokens/**/*.json" \
  --design-system-doc-paths="design-system/docs/**/*.md" \
  --theme-config-paths="design-system/themes/**/*.json" \
  --target-envs=web \
  --ui-json-ai-strict \
  --safety-mode=strict \
  --report-format=json \
  --stdout-summary
```

### 5.3 Legacy project without UI JSON

```bash
smartspec_ui_consistency_audit \
  --spec-ids=legacy_portal \
  --run-label=legacy-ui-consistency \
  --ui-json-mode=disabled \
  --ui-spec-paths="specs/ui/**/*.md" \
  --ui-impl-paths="src/**/*.tsx" \
  --design-tokens-paths="design-system/tokens/**/*.json" \
  --report-format=md
```

---

## 6. CLI / Flags Cheat Sheet

- Scope & label
  - `--spec-ids`
  - `--ui-targets`
  - `--include-dependencies`
  - `--run-label`
- UI spec & implementation
  - `--ui-spec-paths`
  - `--ui-impl-paths`
  - `--ui-json-mode=auto|required|disabled`
  - `--ui-json-ai-strict`
- Design system & tokens
  - `--design-tokens-paths`
  - `--design-system-doc-paths`
  - `--theme-config-paths`
- Environment & brand
  - `--target-envs`
  - `--target-brands`
- Multi-repo & safety
  - `--workspace-roots`
  - `--repos-config`
  - `--registry-dir`, `--registry-roots`
  - `--index`, `--specindex`
  - `--safety-mode=normal|strict` (`--strict`)
- Output & KiloCode
  - `--report-format=md|json`
  - `--report-dir`
  - `--stdout-summary`
  - `--kilocode`, `--nosubtasks`

---

## 7. Reading the UI Consistency Audit Report

A typical report contains:

1. **Scope overview**
   - spec-ids, environments, brands
   - run-label, timestamp

2. **Per-UI-unit table**
   - for each `unit_id`, you see fields like:
     - `criticality`
     - `ui_spec_origin`
     - `ui_spec_review_status`
     - `ui_json_quality_status`
     - `design_system_alignment_status`
     - `token_usage_status`
     - `spacing_consistency_status`
     - `typography_consistency_status`
     - `component_pattern_consistency_status`
     - `state_handling_consistency_status`
     - `dark_mode_consistency_status`
     - `naming_consistency_status`
     - `risk_level`
     - `blocking_for_release`
     - `notes`

3. **Gaps & risks**
   - highlight units where:
     - `risk_level=HIGH/CRITICAL`
     - `blocking_for_release=true`
     - `ui_spec_origin=AI` and `ui_spec_review_status=UNREVIEWED`
     - `ui_json_quality_status=WEAK/BROKEN`
     - `design_system_alignment_status=MAJOR_DRIFT`
     - `token_usage_status=HARD_CODED` on important surfaces

4. **Summary**
   - counts by risk level
   - counts by blocking vs non-blocking

When `--report-format=json` is used, the JSON representation is
canonical; the markdown should mirror the same fields.

---

## 8. KiloCode Usage Examples

### 8.1 Kilo with multiple apps

```bash
smartspec_ui_consistency_audit \
  --spec-ids=web_portal,admin_portal \
  --include-dependencies \
  --run-label=portal-ui-consistency \
  --ui-spec-paths=".spec/ui/**/*.json" \
  --ui-impl-paths="apps/**/src/**/*.{tsx,jsx}" \
  --design-tokens-paths="design-system/tokens/**/*.json" \
  --design-system-doc-paths="design-system/docs/**/*.md" \
  --kilocode \
  --stdout-summary
```

On Kilo:

- Orchestrator decomposes work per spec-id/UI group.
- Code mode reads artifacts read-only.
- Results are aggregated as per-unit statuses and a summary section.

### 8.2 Disabling subtasks for small scope

```bash
smartspec_ui_consistency_audit \
  --spec-ids=small_widget_service \
  --run-label=small-widget-ui-consistency \
  --ui-spec-paths=".spec/ui/small_widget/*.json" \
  --ui-impl-paths="apps/small_widget/src/**/*.{tsx,jsx}" \
  --kilocode \
  --nosubtasks
```

---

## 9. Multi-repo / Multi-registry Examples

### 9.1 Monorepo with multiple apps

```bash
smartspec_ui_consistency_audit \
  --spec-ids=web_portal,admin_portal \
  --run-label=portal-ui-consistency \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --ui-spec-paths=".spec/ui/**/*.json" \
  --ui-impl-paths="apps/**/src/**/*.{tsx,jsx}" \
  --report-format=md
```

### 9.2 Multi-repo, multi-team

```bash
smartspec_ui_consistency_audit \
  --spec-ids=teamA_web,teamB_mobile \
  --run-label=web-mobile-ui-consistency \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --ui-spec-paths="../teamA/.spec/ui/**/*.json;../teamB/.spec/ui/**/*.json" \
  --ui-impl-paths="../teamA/apps/web/src/**/*.{tsx,jsx};../teamB/apps/mobile/src/**/*.{tsx,jsx}" \
  --report-format=json
```

---

## 10. UI JSON vs Inline UI

### 10.1 JSON-first UI

- UI structure and flows are defined in files such as:
  - `.spec/ui/<app>.ui.json`, or similar.
- The workflow treats UI JSON as the **primary source of truth**.
- When `--ui-json-mode=required` and UI JSON is missing:
  - this is treated as a gap and affects `ui_json_quality_status` and
    `risk_level`.
- For AI-generated UI JSON it is strongly recommended to always
  populate meta fields:
  - `source`, `generator`, `design_system_version`, `style_preset`,
    `review_status`.

### 10.2 Inline UI / opt-out

- If the project does not use dedicated UI JSON files:
  - use `--ui-json-mode=disabled`.
  - specs remain in markdown/docs.
- The workflow still builds a report based on specs + design system
  docs; some statuses may be `UNKNOWN` more frequently.

---

## 11. Benefits vs Risks of Not Using

### 11.1 Benefits of using

- Clear visibility into how consistently your UI uses the design system.
- Explicit view of AI-generated `ui.json` quality and review status.
- Reduced risk of “off-brand” or outdated-looking UI appearing only in
  some flows.
- Easier redesigns and theme changes, because the current system is more
  tightly aligned with tokens and patterns.

### 11.2 Risks if you don’t use it

- The design system remains theoretical; implementation drifts.
- AI-generated UI diverges from brand/look-and-feel without detection.
- Dark mode / multi-brand issues appear randomly in production.
- Large-scale UI changes or rebranding become extremely painful.

---

## 12. FAQ / Troubleshooting

**Q1: Can we use this workflow if we don’t have a full design system yet?**  
Yes, but the value is lower. The audit will focus more on structural and
naming consistency rather than specific tokens. As your design system
matures, the audit becomes more powerful.

**Q2: Will this workflow design a new design system for us?**  
No. It only checks how well you use the existing system. Designing a new
system is a separate process.

**Q3: Which workflows should we combine it with?**  
Common combinations:

- `/smartspec_ui_validation` – for behavior & validation coverage.
- `/smartspec_release_readiness` – for overall release gates.

---

End of `/smartspec_ui_consistency_audit v5.6.2+` manual (English).
If future versions significantly change the status model or strict-mode
semantics, issue a new manual (e.g., v5.7) and clearly document the
compatible workflow versions.

