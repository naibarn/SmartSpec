---
description: Generate comprehensive project plan (plan.md) from SPEC with milestones, resource allocation, and timeline estimation. Supports --specindex and --nogenerate.
handoffs:
  - label: Generate Tasks
    agent: smartspec.tasks
    prompt: Generate tasks.md from this plan
---

## User Input
```text
$ARGUMENTS
```

**Patterns:** 
- `specs/feature/spec-004/spec.md`
- `--specindex="path/index.json"` 
- `--nogenerate` (dry run)
- `--output=roadmap.md` (custom name)

## 0. Load SmartSpec Context

Read: `.smartspec/system_prompt.md`, `Knowledge-Base.md`, `constitution.md`, SPEC_INDEX

Parse flags:
- `--specindex` → Custom SPEC_INDEX path
- `--nogenerate` → DRY_RUN_MODE = true
- `--output` → Custom output name (default: plan.md)

## 1. Resolve Paths

Extract SPEC path, determine SPEC_INDEX path, set output: `SPEC_DIR/[output or plan.md]`

## 2. Analyze SPEC

Parse sections: metadata, overview, architecture, implementation, testing, dependencies

Extract: complexity, risks, external deps, team needs, timeline constraints

## 3. Generate Plan Structure

### Header
```markdown
# Project Plan - [Name]

**Generated:** YYYY-MM-DD HH:mm
**Author:** SmartSpec Architect v4.0
**Source:** [SPEC-ID] v[X.Y.Z]
**Status:** PLANNING

## Executive Summary
- Duration: X weeks
- Team: Y developers
- Complexity: [LEVEL]
- Risk: [LEVEL]

Success Criteria: [from SPEC]
```

### Milestones
```markdown
## 🎯 Milestones

### M1: Foundation (Week X)
Deliverables: Database, auth, models
Success: [ ] Foundation complete, tests pass

### M2: Core Features (Week Y)
Deliverables: [Key features]

### M3: Integration (Week Z)
### M4: Production Ready (Week W)
```

### Phases
```markdown
## 📋 Phases

### Phase 1: Setup (Weeks 1-2)
Duration: 2 weeks | Team: 2-3 devs | Risk: LOW

Objectives:
- Initialize project
- Setup database
- Implement auth

Dependencies: Dev env, database access
Deliverables: Working dev env, auth functional

[Continue for all phases...]
```

### Resources
```markdown
## 👥 Resources

Required Roles:
- Backend: X devs
- Frontend: Y devs (if needed)
- DevOps: Z
- QA: W

Skills: [Tech stack from SPEC]

Time Allocation:
| Phase | Duration | Dev-Weeks | Calendar |
|-------|----------|-----------|----------|
| P1    | X weeks  | Y dev-wks | Z weeks  |
```

### Risks
```markdown
## ⚠️ Risks

HIGH:
- [Risk 1]: Impact [H/M/L], Prob [H/M/L]
  Mitigation: [Strategy]

MEDIUM:
- [Risk 2]: [Assessment]

Schedule Risks: [Dependencies, resources]
```

### Dependencies
```markdown
## 🔗 Dependencies

Internal (from SPEC_INDEX):
- **spec-core-001** (`path`, repo: private)
  Required: Phase X | Risk if delayed: [assessment]

External:
- Services: [List]
- Infrastructure: Database, cloud, CI/CD
```

### Timeline
```markdown
## 📅 Timeline

Week 1-2:  ████ Phase 1
Week 3-4:  ████ Phase 2
Week 5-6:  ████ Phase 3
...

Key Dates:
- Start: [Date]
- M1: [Date]
- M2: [Date]
- Launch: [Date]

Critical Path: [Tasks that cannot delay]
```

### Quality Gates
```markdown
## ✅ Quality Gates

Phase Completion:
- [ ] Code reviewed
- [ ] Tests >80% coverage
- [ ] No critical bugs
- [ ] Docs updated
- [ ] Performance met

Release Criteria:
- [ ] All features per SPEC
- [ ] Security audit passed
- [ ] Load testing done
- [ ] DR tested
- [ ] User docs complete
```

### Communication
```markdown
## 📢 Communication

Daily: Standup (15m), Slack updates
Weekly: Progress report, risk review
Bi-weekly: Demo, retrospective

Metrics: Tasks completed, velocity, bugs, coverage, performance
```

## 4. Dry Run

If `--nogenerate`:
```markdown
# Plan Preview (DRY RUN)

Would generate: [PATH]
- Milestones: X
- Phases: Y  
- Duration: Z weeks
- Team: W devs
- Risk: [LEVEL]

To proceed: Remove --nogenerate
```
STOP if dry run

## 5. Write File

Write plan.md to output path

## 6. Report (Thai)

```
✅ สร้าง Project Plan เรียบร้อย

📁 ไฟล์: [PATH]
📊 Milestones: X | Phases: Y | Duration: Z weeks
👥 ทีม: W developers | Risk: [LEVEL]

🎯 Milestones:
- M1: Week X - Foundation
- M2: Week Y - Core
- M3: Week Z - Integration

⚠️ Risks: X HIGH, Y MEDIUM
💡 ระวัง: [Key risks]

🔄 ต่อไป:
1. Review plan.md
2. สร้าง tasks.md
3. Align ทีม
4. เริ่ม Phase 1
```

Context: $ARGUMENTS
