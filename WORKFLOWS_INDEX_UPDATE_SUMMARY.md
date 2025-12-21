# สรุปการอัปเดต WORKFLOWS_INDEX.yaml

## ภาพรวม

อัปเดต `.spec/WORKFLOWS_INDEX.yaml` ให้ครอบคลุม workflows ทั้งหมดที่มีคู่มือเอกสาร รวมถึงแก้ไข YAML syntax error

## การเปลี่ยนแปลง

### 1. ✅ เพิ่ม Workflows ใหม่ (16 workflows)

เพิ่ม workflow entries สำหรับคู่มือที่มีอยู่แต่ยังไม่ได้ลงทะเบียนใน INDEX:

| ลำดับ | Workflow Name | Category | Platform Support |
|------|---------------|----------|------------------|
| 1 | ci_quality_gate | quality | cli, kilo, ci |
| 2 | fix_errors | implement | cli, kilo |
| 3 | generate_cursor_prompt | core | cli, kilo |
| 4 | generate_implement_prompt | core | cli, kilo |
| 5 | global_registry_audit | index | cli, kilo |
| 6 | project_copilot_manual | documentation | cli, kilo |
| 7 | refactor_code | implement | cli, kilo |
| 8 | release_readiness | deployment | cli, kilo |
| 9 | smart_spec_install_manual | documentation | cli, kilo |
| 10 | smart_spec_manuals_aligned_workflows | documentation | cli, kilo |
| 11 | smartspec_reindex_workflows | index | cli, kilo |
| 12 | smartspec_workflow_overview_guide | utility | cli, kilo |
| 13 | tasks_checkboxes | utility | cli, kilo |
| 14 | ui_consistency_audit_manual | documentation | cli, kilo |
| 15 | ui_validation_manual | documentation | cli, kilo |
| 16 | verify_tasks_progress | verify | cli, kilo |

### 2. ✅ แก้ไข YAML Syntax Error

**ปัญหา:** บรรทัด 92 มี colon (`:`) ใน purpose string ที่ไม่ได้ escape

**Before:**
```yaml
purpose: Strict evidence-only verification using parseable evidence hooks (evidence: type key=value...).
```

**After:**
```yaml
purpose: "Strict evidence-only verification using parseable evidence hooks (evidence: type key=value...)."
```

### 3. ✅ Validation

- ✅ YAML syntax ถูกต้อง (ผ่าน `yaml.safe_load()`)
- ✅ ทุก workflow ที่มีคู่มือมี entry ใน INDEX
- ✅ Structure สอดคล้องกับ workflows อื่นๆ

## สถิติ

### Before Update

- **Workflows ใน INDEX:** 40
- **คู่มือที่มี:** 51
- **ขาดหายไป:** 16 workflows
- **YAML Errors:** 1

### After Update

- **Workflows ใน INDEX:** 56
- **คู่มือที่มี:** 51
- **ครอบคลุม:** ✅ ทุกคู่มือมี entry
- **YAML Errors:** 0

### เพิ่มเติม

INDEX มี 56 workflows (มากกว่าคู่มือ 51 ตัว) เพราะมี workflows บางตัวที่อยู่ใน INDEX แต่ยังไม่มีคู่มือ:

- reverse_to_spec
- spec_lifecycle_manager
- sync_spec_tasks
- data_migration_governance
- observability_runbook_generator

## โครงสร้าง YAML Entry

แต่ละ workflow entry มีโครงสร้างดังนี้:

```yaml
- name: /smartspec_<workflow_name>
  aliases: [/smartspec_<workflow_name>.md]
  purpose: "<brief description>"
  category: <category>
  positional_args: []
  extra_flags: []
  reads: []
  writes: []
  write_scope: [reports]
  apply_required_for: []
  platform_support: [cli, kilo]
```

## Categories

Workflows ถูกจัดหมวดหมู่ตาม:

- **core** - Core workflows (generate_spec, generate_plan, etc.)
- **verify** - Verification workflows
- **implement** - Implementation workflows (fix, refactor)
- **quality** - Quality assurance workflows
- **security** - Security-related workflows
- **deployment** - Deployment workflows
- **documentation** - Documentation workflows
- **index** - Index maintenance workflows
- **utility** - Utility workflows

## Platform Support

- **cli** - Command-line interface
- **kilo** - Kilo Code platform
- **ci** - CI/CD environments

## ไฟล์ที่เกี่ยวข้อง

- `.spec/WORKFLOWS_INDEX.yaml` - Main index file (อัปเดตแล้ว)
- `.smartspec-docs/workflows/*.md` - Workflow manuals (51 ไฟล์)
- `new_workflow_entries.yaml` - Generated entries (temporary)
- `generate_workflow_entries.py` - Generation script

## Commit

**Commit Hash:** d532068  
**Commit Message:** Update WORKFLOWS_INDEX.yaml to include all documented workflows  
**Branch:** main  
**Link:** https://github.com/naibarn/SmartSpec/commit/d532068

## การตรวจสอบ

### ตรวจสอบ YAML syntax

```bash
python3 -c "import yaml; yaml.safe_load(open('.spec/WORKFLOWS_INDEX.yaml'))"
```

### นับจำนวน workflows

```bash
grep -c "^  - name: /smartspec_" .spec/WORKFLOWS_INDEX.yaml
# Output: 56
```

### ดูรายชื่อทั้งหมด

```bash
grep "^  - name: /smartspec_" .spec/WORKFLOWS_INDEX.yaml | sed 's/.*\/smartspec_//' | sort
```

## Next Steps

### สำหรับ Workflows ที่ยังไม่มีคู่มือ

Workflows 5 ตัวต่อไปนี้มี entry ใน INDEX แต่ยังไม่มีคู่มือ:

1. reverse_to_spec
2. spec_lifecycle_manager
3. sync_spec_tasks
4. data_migration_governance
5. observability_runbook_generator

**แนะนำ:** สร้างคู่มือสำหรับ workflows เหล่านี้เพื่อให้เอกสารครบถ้วน

### การบำรุงรักษา

เมื่อเพิ่ม workflow ใหม่:

1. สร้างไฟล์คู่มือ `.smartspec-docs/workflows/<workflow_name>.md`
2. เพิ่ม entry ใน `.spec/WORKFLOWS_INDEX.yaml`
3. ตรวจสอบ YAML syntax
4. Commit และ push

---

**สร้างเมื่อ:** 13 ธันวาคม 2025  
**เวอร์ชัน:** 1.0
