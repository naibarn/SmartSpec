# Autopilot Status Query

Query spec development status using Multi-Agent System Status Agent.

## Purpose

This workflow provides quick status queries for any spec, showing:
- Progress percentage and visual progress bar
- Completed and pending tasks
- Next steps recommendations
- Estimated time to completion
- Warnings and issues

## Usage

```bash
/autopilot_status.md <spec-id> [--query <question>] --platform <kilo|antigravity|claude>
```

## Parameters

| Parameter | Required | Description | Example |
|:---|:---:|:---|:---|
| `<spec-id>` | Yes | Spec ID to query | `spec-core-001-authentication` |
| `--query` | No | Specific question to ask | `"เหลืออะไรบ้าง?"` |
| `--platform` | Yes | Platform (kilo/antigravity/claude) | `kilo` |

## Examples

### Example 1: Full status report

```bash
/autopilot_status.md spec-core-001-authentication --platform kilo
```

**Output:**
```
📊 Status Agent

## ความคืบหน้า

**Tasks ที่เสร็จแล้ว:** 5 / 12 (42%)

```
████████░░░░░░░░░░░░ 42%
```

## Tasks ที่เหลือ

- Task 6: Implement logout API
- Task 7: Add password reset functionality
- Task 8: Implement token refresh
- Task 9: Add rate limiting
- Task 10: Write API tests
- Task 11: Update documentation
- Task 12: Deploy to staging

## ขั้นตอนถัดไป

1. ทำ tasks ที่เหลืออีก 7 tasks
2. แนะนำให้ sync checkboxes ก่อนทำต่อ (เพื่อความแม่นยำ)

## เวลาโดยประมาณ

140 นาที (~2.3 ชั่วโมง)
```

### Example 2: Specific question

```bash
/autopilot_status.md spec-core-001-authentication --query "เหลืออะไรบ้าง?" --platform kilo
```

**Output:**
```
📊 Status Agent

## Tasks ที่เหลือ

- Task 6: Implement logout API
- Task 7: Add password reset functionality
- Task 8: Implement token refresh
- Task 9: Add rate limiting
- Task 10: Write API tests
- Task 11: Update documentation
- Task 12: Deploy to staging

**รวม:** 7 tasks
```

### Example 3: Progress query

```bash
/autopilot_status.md spec-core-001-authentication --query "งานถึงไหนแล้ว?" --platform kilo
```

**Output:**
```
📊 Status Agent

**คำตอบ:** 5 / 12 tasks เสร็จแล้ว (42%)

```
████████░░░░░░░░░░░░ 42%
```
```

### Example 4: Time estimate

```bash
/autopilot_status.md spec-core-001-authentication --query "เมื่อไหร่เสร็จ?" --platform kilo
```

**Output:**
```
📊 Status Agent

**คำตอบ:** ประมาณ 140 นาที (~2.3 ชั่วโมง)

**สมมติฐาน:** 20 นาที/task × 7 tasks ที่เหลือ
```

## Implementation

This workflow is a wrapper that calls the Multi-Agent System Status Agent.

### Internal Process

1. **Parse arguments**
   - Extract spec ID
   - Extract optional query
   - Validate inputs

2. **Call Status Agent**
   ```bash
   python3 ${SMARTSPEC_ROOT}/.smartspec/ss_autopilot/cli_multi_agent.py \
     status \
     --spec-id <spec-id> \
     [--query <question>]
   ```

3. **Format output**
   - Markdown formatting for IDE display
   - Emojis for visual cues
   - Progress bars for quick understanding

4. **Return result**
   - Display in IDE chat
   - Save to `.spec/reports/autopilot/` (optional)

### File Paths

**Input files (read):**
- `specs/<spec-id>/tasks.md` - Task list with checkboxes
- `.spec/reports/implement-tasks/<spec-id>/` - Implementation reports (if exists)

**Output files (write):**
- None (output to stdout/IDE chat only)

### Error Handling

**If spec ID not found:**
```
❌ Error: Spec 'spec-core-001' not found

**Available specs:**
- spec-core-001-authentication
- spec-core-002-authorization
- ...

**Tip:** Check spelling or list all specs with:
/smartspec_list_specs.md --platform kilo
```

**If tasks.md not found:**
```
⚠️  Warning: tasks.md not found for spec-core-001

**Next step:** Generate tasks first:

/smartspec_generate_tasks.md \
  specs/spec-core-001/spec.md \
  --out specs/spec-core-001/tasks.md \
  --platform kilo
```

## Question Types Supported

The Status Agent can answer 6 types of questions:

1. **"งานถึงไหนแล้ว?"** / **"progress"**
   - Shows completion percentage and progress bar

2. **"เหลืออะไรบ้าง?"** / **"what's left"**
   - Lists all pending tasks

3. **"ต้องทำอะไรต่อ?"** / **"next step"**
   - Shows recommended next steps

4. **"มีปัญหาไหม?"** / **"issues"**
   - Lists warnings and issues

5. **"เมื่อไหร่เสร็จ?"** / **"eta"**
   - Estimates time to completion

6. **Default** (no specific question)
   - Shows full status report (all of the above)

## Notes

### Requirements

- **Python 3.11+** required
- **Multi-Agent System** must be installed in `.smartspec/ss_autopilot/`
- **No external dependencies** (pure Python)

### Performance

- **Response time:** < 1 second (typical)
- **File reads:** 1-2 files (tasks.md, optional reports)
- **No network calls**

### Limitations

- Only reads `tasks.md` checkboxes (doesn't verify actual code)
- Time estimates assume 20 minutes per task (may not be accurate)
- No test results integration (Phase 2)
- No quality gate status (Phase 2)

### Tips

- Run this frequently to track progress
- Use specific questions to get quick answers
- Combine with `/autopilot_run.md` to get next workflow recommendation
- If checkboxes seem wrong, run `/smartspec_sync_tasks_checkboxes.md` first

## Related Workflows

- `/autopilot_run.md` - Get next workflow recommendation
- `/autopilot_ask.md` - Natural language query (more flexible)
- `/smartspec_sync_tasks_checkboxes.md` - Sync checkboxes with actual code
- `/smartspec_implement_tasks.md` - Implement tasks

## Troubleshooting

### Issue: "Spec not found"

**Solution:** Check spec ID spelling or list all specs:
```bash
/smartspec_list_specs.md --platform kilo
```

### Issue: "tasks.md not found"

**Solution:** Generate tasks first:
```bash
/smartspec_generate_tasks.md \
  specs/<spec-id>/spec.md \
  --out specs/<spec-id>/tasks.md \
  --platform kilo
```

### Issue: "Progress seems wrong"

**Solution:** Sync checkboxes with actual code:
```bash
/smartspec_sync_tasks_checkboxes.md \
  specs/<spec-id>/tasks.md \
  --apply \
  --platform kilo
```

## Version History

- **v2.0** (2025-12-25) - Initial release with Multi-Agent System
