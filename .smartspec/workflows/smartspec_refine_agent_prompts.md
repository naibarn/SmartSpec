# smartspec_refine_agent_prompts

## Overview
Analyzes UI analytics data and suggests improvements to AI agent prompts for better A2UI output quality.

## Version
1.0.0

## Category
ai_feedback_and_optimization

## Description
This workflow implements an **AI feedback loop** that analyzes UI analytics data (from `smartspec_ui_analytics_reporter`) and automatically suggests improvements to AI agent prompts. By learning from actual UI performance metrics, interaction patterns, and user behavior, this workflow helps refine prompts to generate higher-quality A2UI specifications.

The workflow:
- **Analyzes analytics data** to identify patterns and issues
- **Detects common problems** (e.g., low engagement, accessibility issues, performance bottlenecks)
- **Suggests prompt refinements** to address identified issues
- **Generates optimized prompts** for better A2UI output
- **Tracks improvement metrics** over time

## Parameters

### Required Parameters

#### `--analytics-file`
- **Type:** string
- **Required:** Yes
- **Description:** Path to the analytics JSON file (output from `smartspec_ui_analytics_reporter`)
- **Example:** `.spec/analytics/ui_analytics_2025-12-22.json`

### Optional Parameters

#### `--focus-area`
- **Type:** string
- **Required:** No
- **Description:** Specific area to focus refinement on
- **Allowed Values:**
  - `all`: Analyze all aspects (default)
  - `accessibility`: Focus on accessibility improvements
  - `performance`: Focus on performance optimization
  - `engagement`: Focus on user engagement
  - `usability`: Focus on usability issues
- **Default:** `all`

#### `--output-format`
- **Type:** string
- **Required:** No
- **Default:** `markdown`
- **Description:** Output format for refinement suggestions
- **Allowed Values:**
  - `markdown`: Markdown report with suggestions
  - `json`: Structured JSON with prompt templates
  - `both`: Both markdown and JSON

#### `--output-file`
- **Type:** string
- **Required:** No
- **Default:** `.spec/prompt_refinements.md`
- **Description:** Output file path for refinement suggestions

#### `--threshold`
- **Type:** number
- **Required:** No
- **Default:** `0.7`
- **Description:** Confidence threshold for suggestions (0.0-1.0)
- **Example:** `0.8`

#### `--include-examples`
- **Type:** boolean
- **Required:** No
- **Default:** `true`
- **Description:** Include before/after examples in suggestions

#### `--auto-apply`
- **Type:** boolean
- **Required:** No
- **Default:** `false`
- **Description:** Automatically apply high-confidence refinements to prompt templates

## Behavior

### Analysis Process
1. **Load Analytics Data:** Reads the analytics JSON file
2. **Identify Patterns:** Detects recurring issues and patterns
3. **Calculate Metrics:** Computes engagement rates, accessibility scores, performance metrics
4. **Detect Issues:** Identifies problems based on thresholds
5. **Generate Suggestions:** Creates specific prompt refinements for each issue
6. **Rank Suggestions:** Orders suggestions by impact and confidence
7. **Output Report:** Generates markdown or JSON report

### Issue Detection
The workflow detects various issues:

| Issue Type | Detection Criteria | Suggested Refinement |
|------------|-------------------|---------------------|
| Low Engagement | Click rate < 30% | Add more interactive elements, clearer CTAs |
| Accessibility | Missing alt text, low contrast | Emphasize WCAG compliance in prompts |
| Performance | Load time > 3s | Optimize component complexity, lazy loading |
| Usability | High error rate | Simplify forms, add validation hints |
| Consistency | Variant misuse | Reinforce theme token usage |

### Suggestion Format
Each suggestion includes:
- **Issue Description:** What problem was detected
- **Current Prompt Pattern:** The prompt pattern causing the issue
- **Refined Prompt:** Improved prompt to address the issue
- **Expected Impact:** Predicted improvement
- **Confidence Score:** How confident the analysis is (0.0-1.0)
- **Examples:** Before/after examples (if enabled)

## Output
- **Refinement Report:** Markdown or JSON file with suggestions
- **Prompt Templates:** Optimized prompt templates (if `--auto-apply`)
- **Metrics Summary:** Analytics summary and improvement predictions

## Example Usage

### CLI

```bash
# Analyze analytics and generate refinement suggestions
/smartspec_refine_agent_prompts \
  --analytics-file .spec/analytics/ui_analytics_2025-12-22.json

# Focus on accessibility improvements
/smartspec_refine_agent_prompts \
  --analytics-file .spec/analytics/ui_analytics_2025-12-22.json \
  --focus-area accessibility \
  --threshold 0.8

# Generate JSON output with auto-apply
/smartspec_refine_agent_prompts \
  --analytics-file .spec/analytics/ui_analytics_2025-12-22.json \
  --output-format json \
  --output-file .spec/prompt_refinements.json \
  --auto-apply true

# Full analysis with examples
/smartspec_refine_agent_prompts \
  --analytics-file .spec/analytics/ui_analytics_2025-12-22.json \
  --focus-area all \
  --include-examples true \
  --output-format both
```

### Kilo Code

```kilo
# Basic refinement analysis
smartspec_refine_agent_prompts(
  analytics_file=".spec/analytics/ui_analytics_2025-12-22.json"
)

# Focus on performance
smartspec_refine_agent_prompts(
  analytics_file=".spec/analytics/ui_analytics_2025-12-22.json",
  focus_area="performance",
  threshold=0.8
)

# Auto-apply high-confidence refinements
smartspec_refine_agent_prompts(
  analytics_file=".spec/analytics/ui_analytics_2025-12-22.json",
  output_format="json",
  auto_apply=true
)
```

## Use Cases

### Use Case 1: Improve Accessibility Based on Analytics
**Scenario:** Analytics show that 40% of components are missing alt text.

**Command:**
```bash
/smartspec_refine_agent_prompts \
  --analytics-file .spec/analytics/ui_analytics.json \
  --focus-area accessibility
```

**Result:** 
```markdown
## Accessibility Refinement Suggestions

### Issue: Missing Alt Text (40% of images)
**Current Prompt Pattern:**
"Generate a product card with image"

**Refined Prompt:**
"Generate a product card with image. IMPORTANT: Include descriptive alt text for accessibility (WCAG 2.1 Level AA)."

**Expected Impact:** +40% accessibility score
**Confidence:** 0.95
```

---

### Use Case 2: Optimize Performance Based on Metrics
**Scenario:** Analytics show average load time is 4.2s, above the 3s threshold.

**Command:**
```bash
/smartspec_refine_agent_prompts \
  --analytics-file .spec/analytics/ui_analytics.json \
  --focus-area performance
```

**Result:**
```markdown
## Performance Refinement Suggestions

### Issue: High Component Complexity (avg load time 4.2s)
**Current Prompt Pattern:**
"Generate a dashboard with all features"

**Refined Prompt:**
"Generate a dashboard with progressive loading. Use lazy loading for below-fold components. Limit initial render to 10 components max."

**Expected Impact:** -30% load time
**Confidence:** 0.88
```

---

### Use Case 3: Continuous Improvement Loop
**Scenario:** Weekly analysis to continuously improve prompt quality.

**Command:**
```bash
# Run weekly via cron
/smartspec_refine_agent_prompts \
  --analytics-file .spec/analytics/ui_analytics_weekly.json \
  --auto-apply true \
  --threshold 0.9
```

**Result:** High-confidence refinements are automatically applied to prompt templates.

## Related Workflows
- `smartspec_ui_analytics_reporter`: Generate analytics data for analysis
- `smartspec_ui_performance_test`: Test performance metrics
- `smartspec_ui_accessibility_audit`: Audit accessibility compliance
- `smartspec_generate_ui_spec`: Generate UI specs with refined prompts

## Implementation
Implemented in: `.smartspec/scripts/refine_agent_prompts.py`

## Notes
- This workflow implements a **closed feedback loop** for continuous improvement
- Refinement suggestions are based on statistical analysis, not manual review
- High confidence threshold (>0.9) is recommended for auto-apply
- The workflow learns from aggregate patterns, not individual cases
- Prompt refinements are additive; they don't replace existing prompts
- Regular analysis (weekly/monthly) helps track improvement trends
