# Autopilot Ask - Natural Language Query

Ask questions in natural language and get routed to the appropriate agent automatically.

## Purpose

This workflow provides a natural language interface to the Multi-Agent System. Just ask your question in plain language (Thai or English), and the Intent Parser Agent will:
- Understand what you're asking
- Route to the appropriate agent
- Get the answer
- Return formatted result

**No need to remember specific commands!**

## Usage

```bash
/autopilot_ask.md "<your question>" --platform <kilo|antigravity|claude>
```

## Parameters

| Parameter | Required | Description | Example |
|:---|:---:|:---|:---|
| `"<question>"` | Yes | Your question in natural language | `"spec-core-001 งานถึงไหนแล้ว?"` |
| `--platform` | Yes | Platform (kilo/antigravity/claude) | `kilo` |

## Examples

### Example 1: Check progress

```bash
/autopilot_ask.md "spec-core-001 งานถึงไหนแล้ว?" --platform kilo
```

**Output:**
```
💬 Intent Parser Agent

**Type:** status_query  
**Target Agent:** status  
**Confidence:** 60%  
**Spec ID:** spec-core-001

🔀 Routing to: status

📊 Status Agent

**Tasks ที่เสร็จแล้ว:** 5 / 12 (42%)

```
████████░░░░░░░░░░░░ 42%
```
```

### Example 2: What's left?

```bash
/autopilot_ask.md "เหลืออะไรบ้างใน spec-core-001?" --platform kilo
```

**Output:**
```
💬 Intent Parser Agent

**Type:** status_query  
**Target Agent:** status

🔀 Routing to: status

📊 Status Agent

## Tasks ที่เหลือ

- Task 6: Implement logout API
- Task 7: Add password reset
- Task 8: Implement token refresh
- Task 9: Add rate limiting
- Task 10: Write API tests
- Task 11: Update documentation
- Task 12: Deploy to staging

**รวม:** 7 tasks
```

### Example 3: Start development

```bash
/autopilot_ask.md "เริ่มพัฒนา spec-core-002" --platform kilo
```

**Output:**
```
💬 Intent Parser Agent

**Type:** orchestration  
**Target Agent:** orchestrator

🔀 Routing to: orchestrator

🤖 Orchestrator Agent

**Workflow:** smartspec_generate_spec  
**Reason:** No spec.md found

**Command:**
/smartspec_generate_spec.md \
  "spec-core-002" \
  --out specs/spec-core-002/spec.md \
  --platform kilo
```

### Example 4: Fix bug

```bash
/autopilot_ask.md "แก้ bug ใน spec-core-001 error: undefined variable 'user_id'" --platform kilo
```

**Output:**
```
💬 Intent Parser Agent

**Type:** bug_fix  
**Target Agent:** bug_fixer  
**Confidence:** 95%

🔀 Routing to: bug_fixer

⚠️  Bug Fixer Agent not yet implemented (Phase 2)

**For now, please:**
1. Check error message: "undefined variable 'user_id'"
2. Search in code: `grep -r "user_id" specs/spec-core-001/`
3. Fix manually
4. Run tests

**Coming in Phase 2:**
- Automatic bug analysis
- Root cause detection
- Fix generation
- Test verification
```

### Example 5: Validate implementation

```bash
/autopilot_ask.md "ตรวจสอบ implementation ของ spec-core-001" --platform kilo
```

**Output:**
```
💬 Intent Parser Agent

**Type:** validation  
**Target Agent:** validation

🔀 Routing to: validation

⚠️  Validation Agent not yet implemented (Phase 2)

**For now, please run:**
/smartspec_verify_implementation.md \
  specs/spec-core-001/spec.md \
  --platform kilo

**Coming in Phase 2:**
- Automatic validation
- Contract checking
- Quality gates
- Detailed reports
```

### Example 6: Modify spec

```bash
/autopilot_ask.md "เพิ่มฟังก์ชัน password reset ใน spec-core-001" --platform kilo
```

**Output:**
```
💬 Intent Parser Agent

**Type:** modification  
**Target Agent:** spec_modifier  
**Confidence:** 80%

🔀 Routing to: spec_modifier

⚠️  Spec Modifier Agent not yet implemented (Phase 3)

**For now, please:**
1. Edit specs/spec-core-001/spec.md manually
2. Add "password reset" feature
3. Regenerate plan: /smartspec_generate_plan.md
4. Regenerate tasks: /smartspec_generate_tasks.md
5. Implement: /smartspec_implement_tasks.md

**Coming in Phase 3:**
- Automatic spec modification
- Plan/tasks regeneration
- Impact analysis
- Guided re-implementation
```

## Implementation

This workflow calls the Intent Parser Agent which understands natural language and routes to appropriate agents.

### Internal Process

1. **Parse intent**
   ```python
   intent = intent_parser.parse(user_question)
   # Returns: {
   #   "type": "status_query|orchestration|bug_fix|validation|modification",
   #   "spec_id": "spec-core-001",
   #   "target_agent": "status|orchestrator|bug_fixer|validation|spec_modifier",
   #   "context": {...},
   #   "confidence": 0.60
   # }
   ```

2. **Route to agent**
   ```python
   if intent.target_agent == "status":
       result = status_agent.query(intent.spec_id, intent.context["question"])
   elif intent.target_agent == "orchestrator":
       result = orchestrator_agent.recommend_next_workflow(intent.spec_id)
   elif intent.target_agent == "bug_fixer":
       result = bug_fixer_agent.fix(intent.spec_id, intent.context["error_message"])
   elif intent.target_agent == "validation":
       result = validation_agent.validate(intent.spec_id, intent.context["target"])
   elif intent.target_agent == "spec_modifier":
       result = spec_modifier_agent.modify(intent.spec_id, intent.context["change_description"])
   ```

3. **Format output**
   - Show intent parsing result
   - Show routing decision
   - Show agent response
   - Format for IDE display

### Intent Types Recognized

The Intent Parser recognizes **5 types of intents**:

#### 1. Status Query

**Keywords:** งานถึงไหน, เหลืออะไร, ต้องทำอะไรต่อ, มีปัญหาไหม, เมื่อไหร่เสร็จ, progress, status, remaining, next step, eta

**Routes to:** Status Agent

**Examples:**
- "spec-core-001 งานถึงไหนแล้ว?"
- "เหลืออะไรบ้าง?"
- "What's the progress?"
- "เมื่อไหร่เสร็จ?"

#### 2. Orchestration

**Keywords:** ทำต่อ, เริ่ม, run, start, continue, next, พัฒนา, ดำเนินการ

**Routes to:** Orchestrator Agent

**Examples:**
- "เริ่มพัฒนา spec-core-002"
- "ทำต่อ"
- "run spec-core-001"
- "What should I do next?"

#### 3. Bug Fix

**Keywords:** แก้, bug, error, fix, ผิดพลาด, ไม่ทำงาน, broken, issue

**Routes to:** Bug Fixer Agent (Phase 2)

**Examples:**
- "แก้ bug ใน spec-core-001"
- "error: undefined variable"
- "Fix the broken test"
- "มี bug ที่ login"

#### 4. Validation

**Keywords:** ตรวจสอบ, validate, check, verify, ผิด, ถูกต้อง, correct

**Routes to:** Validation Agent (Phase 2)

**Examples:**
- "ตรวจสอบ implementation ของ spec-core-001"
- "Validate the API"
- "Check if tests pass"
- "Verify the deployment"

#### 5. Modification

**Keywords:** เปลี่ยน, เพิ่ม, ลบ, แก้ไข, ปรับปรุง, change, add, remove, modify, update, refactor

**Routes to:** Spec Modifier Agent (Phase 3)

**Examples:**
- "เพิ่มฟังก์ชัน password reset"
- "เปลี่ยนจาก JWT เป็น OAuth"
- "ลบ feature X"
- "Refactor authentication"

### Entity Extraction

The Intent Parser extracts:

- **Spec ID:** `spec-xxx-yyy-zzz` or `xxx-yyy`
- **Error message:** After "error:", "bug:", etc.
- **Target:** implementation, api, ui, tests, etc.
- **Change description:** Full text for modifications

### Confidence Scores

- **95%:** 3+ keyword matches
- **80%:** 2 keyword matches
- **60%:** 1 keyword match
- **30%:** No clear match (low confidence)

## File Paths

**Input files (depends on routed agent):**
- Status Agent: `specs/<spec-id>/tasks.md`
- Orchestrator: `specs/<spec-id>/{spec,plan,tasks}.md`
- Bug Fixer: Source code files
- Validation: Implementation files
- Spec Modifier: `specs/<spec-id>/spec.md`

**Output files (write):**
- None (output to stdout/IDE chat only)

## Error Handling

**If question is unclear:**
```
⚠️  Low confidence (30%)

**Your question:** "ทำอะไรดี?"

**Suggestions:**
- Be more specific: "spec-core-001 งานถึงไหนแล้ว?"
- Include spec ID: "spec-core-001 ..."
- Use keywords: "เหลืออะไร", "ทำต่อ", "แก้ bug"

**Or use specific commands:**
- /autopilot_status.md <spec-id> --platform kilo
- /autopilot_run.md <spec-id> --platform kilo
```

**If spec ID not found:**
```
⚠️  Spec ID not found in question

**Please include spec ID:**
- "spec-core-001 งานถึงไหนแล้ว?"
- "เริ่มพัฒนา spec-core-002"

**Or list all specs:**
/smartspec_list_specs.md --platform kilo
```

## Notes

### Requirements

- **Python 3.11+** required
- **Multi-Agent System** installed
- **Intent Parser Agent** (Phase 1)
- **Status Agent** (Phase 1)
- **Orchestrator Agent** (Phase 1)

### Performance

- **Response time:** < 1 second (parsing) + agent time
- **Intent parsing:** < 0.1 second
- **Agent routing:** < 0.1 second

### Limitations (Phase 1)

- **Keyword-based parsing** (will add LLM in Phase 2)
- **No context awareness** (doesn't remember previous questions)
- **No entity disambiguation** (may extract wrong spec ID)
- **3 agents only** (Bug Fixer, Validation, Spec Modifier in Phase 2-3)

### Tips

- **Be specific:** Include spec ID in your question
- **Use keywords:** "งานถึงไหน", "เหลืออะไร", "แก้ bug", etc.
- **One question at a time:** Don't combine multiple questions
- **Check confidence:** Low confidence? Rephrase your question
- **Fallback:** Use specific commands if parsing fails

## Related Workflows

- `/autopilot_status.md` - Direct status query (no parsing)
- `/autopilot_run.md` - Direct orchestrator (no parsing)
- All 59 SmartSpec workflows (can be recommended)

## Supported Languages

- **Thai:** งานถึงไหน, เหลืออะไร, แก้ bug, ตรวจสอบ, เพิ่ม, etc.
- **English:** progress, remaining, fix, validate, add, etc.
- **Mixed:** "spec-core-001 งานถึงไหนแล้ว?" (recommended)

## Troubleshooting

### Issue: "Low confidence"

**Solution:** Be more specific:
```bash
# ❌ Unclear
/autopilot_ask.md "ทำอะไรดี?" --platform kilo

# ✅ Clear
/autopilot_ask.md "spec-core-001 งานถึงไหนแล้ว?" --platform kilo
```

### Issue: "Spec ID not found"

**Solution:** Include spec ID:
```bash
# ❌ No spec ID
/autopilot_ask.md "เหลืออะไรบ้าง?" --platform kilo

# ✅ With spec ID
/autopilot_ask.md "spec-core-001 เหลืออะไรบ้าง?" --platform kilo
```

### Issue: "Wrong agent"

**Solution:** Use more specific keywords:
```bash
# If routed to wrong agent, use specific command:
/autopilot_status.md spec-core-001 --platform kilo
/autopilot_run.md spec-core-001 --platform kilo
```

### Issue: "Agent not implemented"

**Solution:** Some agents are coming in Phase 2-3:
- **Bug Fixer:** Phase 2 (Week 2)
- **Validation:** Phase 2 (Week 2)
- **Spec Modifier:** Phase 3 (Week 3)

Use manual workflows for now.

## Version History

- **v2.0** (2025-12-25) - Initial release with Intent Parser Agent
