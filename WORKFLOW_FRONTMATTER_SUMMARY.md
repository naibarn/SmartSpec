# สรุปการเพิ่ม YAML Frontmatter ให้ Workflow Files

## ภาพรวม

เพิ่ม YAML frontmatter ให้กับไฟล์ workflow ทั้งหมด 33 ไฟล์ใน `.smartspec/workflows/` เพื่อรองรับ **antigravity**

## ความต้องการของ Antigravity

Workflow files ต้องมี:

1. **YAML Block ที่บรรทัดแรก**
   - เริ่มด้วย `---`
   - ปิดด้วย `---`

2. **Field `description`**
   - บอกว่า workflow นี้ทำอะไร
   - ใช้สำหรับแสดงผลใน UI

## ตัวอย่าง YAML Frontmatter

```yaml
---
description: Refine spec.md (SPEC-first) with deterministic preview/diff + completeness/reuse checks
version: 6.0.0
workflow: /smartspec_generate_spec
---
```

## การเปลี่ยนแปลง

### Before

**ปัญหาที่พบ:**
- ❌ ไม่มี YAML frontmatter: 23 ไฟล์
- ❌ มี YAML แต่ขาด description: 10 ไฟล์
- ❌ รวม: **33/33 ไฟล์มีปัญหา**

### After

**แก้ไขแล้ว:**
- ✅ เพิ่ม frontmatter ใหม่: 23 ไฟล์
- ✅ เพิ่ม description ใน frontmatter เดิม: 10 ไฟล์
- ✅ รวม: **33/33 ไฟล์ผ่านการตรวจสอบ**

## รายการไฟล์ที่แก้ไข

### กลุ่มที่ 1: เพิ่ม Frontmatter ใหม่ (23 ไฟล์)

1. smartspec_api_contract_validator.md
2. smartspec_code_assistant.md
3. smartspec_data_migration_generator.md
4. smartspec_data_model_validator.md
5. smartspec_design_system_migration_assistant.md
6. smartspec_generate_spec.md
7. smartspec_generate_spec_from_prompt.md
8. smartspec_generate_tasks.md
9. smartspec_implement_tasks.md
10. smartspec_quality_gate.md
11. smartspec_reindex_specs.md
12. smartspec_reindex_workflows.md
13. smartspec_report_implement_prompter.md
14. smartspec_security_audit_reporter.md
15. smartspec_security_threat_modeler.md
16. smartspec_sync_tasks_checkboxes.md
17. smartspec_test_report_analyzer.md
18. smartspec_test_suite_runner.md
19. smartspec_ui_component_audit.md
20. smartspec_ui_validation.md
21. smartspec_validate_index.md
22. smartspec_verify_tasks_progress_strict.md
23. (และอื่นๆ)

### กลุ่มที่ 2: เพิ่ม Description ใน Frontmatter เดิม (10 ไฟล์)

1. smartspec_deployment_planner.md
2. smartspec_docs_generator.md
3. smartspec_docs_publisher.md
4. smartspec_generate_plan.md
5. smartspec_generate_tests.md
6. smartspec_hotfix_assistant.md
7. smartspec_nfr_perf_planner.md
8. smartspec_nfr_perf_verifier.md
9. smartspec_observability_configurator.md
10. smartspec_project_copilot.md
11. smartspec_release_tagger.md

## วิธีการแก้ไข

### 1. ดึงข้อมูล Description

ดึงข้อมูล `purpose` จาก `.spec/WORKFLOWS_INDEX.yaml`:

```python
descriptions = {}
for wf in workflows:
    name = wf['name'].replace('/smartspec_', '')
    purpose = wf.get('purpose', 'SmartSpec workflow')
    descriptions[name] = purpose
```

### 2. สร้าง YAML Frontmatter

```python
data = {
    'description': description,
    'version': '6.0.0',
    'workflow': f'/smartspec_{workflow_name}'
}
yaml_str = yaml.dump(data)
frontmatter = f"---\n{yaml_str}---\n\n"
```

### 3. เพิ่มเข้าไฟล์

- **ไฟล์ที่ไม่มี frontmatter:** เพิ่มที่บรรทัดแรก
- **ไฟล์ที่มี frontmatter:** แก้ไขเพิ่ม description

## การตรวจสอบ

### Script ตรวจสอบ

```bash
python3 check_workflow_frontmatter.py
```

**ผลลัพธ์:**
```
Summary: 33 valid, 0 issues
✅ All workflow files have proper YAML frontmatter!
```

### ตรวจสอบด้วยตนเอง

```bash
# ตรวจสอบไฟล์ใดๆ
head -n 5 .smartspec/workflows/smartspec_generate_spec.md
```

**ผลลัพธ์ที่คาดหวัง:**
```yaml
---
description: Refine spec.md (SPEC-first) with deterministic preview/diff + completeness/reuse checks
version: 6.0.0
workflow: /smartspec_generate_spec
---
```

## ประโยชน์

### 1. Antigravity Support

✅ Workflow files พร้อมใช้งานกับ antigravity system  
✅ แสดง description ใน UI ได้ถูกต้อง  
✅ รองรับ metadata เพิ่มเติมในอนาคต

### 2. Consistency

✅ ทุกไฟล์มีโครงสร้างเหมือนกัน  
✅ ง่ายต่อการบำรุงรักษา  
✅ ง่ายต่อการเพิ่ม workflows ใหม่

### 3. Documentation

✅ Description อธิบายหน้าที่ของ workflow ชัดเจน  
✅ Version tracking สำหรับ workflow  
✅ Workflow name เป็น canonical reference

## โครงสร้าง YAML Frontmatter

### Required Fields

```yaml
description: string  # คำอธิบาย workflow (required)
```

### Recommended Fields

```yaml
version: string      # เวอร์ชันของ workflow (e.g., "6.0.0")
workflow: string     # ชื่อ canonical (e.g., "/smartspec_generate_spec")
```

### Optional Fields (เพิ่มได้ในอนาคต)

```yaml
author: string       # ผู้สร้าง workflow
tags: array         # tags สำหรับจัดหมวดหมู่
platform: array     # platforms ที่รองรับ (cli, kilo, ci)
deprecated: boolean # ระบุว่า workflow เลิกใช้แล้ว
```

## Commit

**Commit Hash:** 9cffd04  
**Commit Message:** Add YAML frontmatter to all workflow files for antigravity support  
**Branch:** main  
**Link:** https://github.com/naibarn/SmartSpec/commit/9cffd04

**Changes:**
- 33 files changed
- +247 insertions
- -20 deletions

## Scripts ที่ใช้

### 1. check_workflow_frontmatter.py

ตรวจสอบว่าไฟล์ workflow มี YAML frontmatter ที่ถูกต้อง

**การใช้งาน:**
```bash
python3 check_workflow_frontmatter.py
```

**ตรวจสอบ:**
- ✅ File starts with `---`
- ✅ YAML block closed with `---`
- ✅ Has `description` field

### 2. fix_workflow_frontmatter.py

แก้ไขไฟล์ workflow โดยเพิ่ม/แก้ไข YAML frontmatter

**การใช้งาน:**
```bash
python3 fix_workflow_frontmatter.py
```

**ทำงาน:**
1. Load descriptions from WORKFLOWS_INDEX.yaml
2. Check each workflow file
3. Add/fix YAML frontmatter
4. Write back to file

## Best Practices

### เมื่อสร้าง Workflow ใหม่

1. **เพิ่มใน WORKFLOWS_INDEX.yaml ก่อน**
   ```yaml
   - name: /smartspec_new_workflow
     purpose: "Description of what this workflow does"
     category: utility
     platform_support: [cli, kilo]
   ```

2. **สร้างไฟล์ workflow พร้อม frontmatter**
   ```yaml
   ---
   description: Description of what this workflow does
   version: 6.0.0
   workflow: /smartspec_new_workflow
   ---
   
   # Workflow content here...
   ```

3. **ตรวจสอบด้วย script**
   ```bash
   python3 check_workflow_frontmatter.py
   ```

### เมื่ออัปเดต Workflow

1. อัปเดต description ใน WORKFLOWS_INDEX.yaml
2. อัปเดต description ใน YAML frontmatter
3. ตรวจสอบความสอดคล้องกัน

## Validation Checklist

เมื่อ commit workflow files ใหม่:

- [ ] ไฟล์เริ่มด้วย `---`
- [ ] มี field `description`
- [ ] มี field `version`
- [ ] มี field `workflow`
- [ ] YAML block ปิดด้วย `---`
- [ ] Description ตรงกับ WORKFLOWS_INDEX.yaml
- [ ] ผ่านการตรวจสอบด้วย `check_workflow_frontmatter.py`

## Next Steps

### 1. Monitor Compliance

ตรวจสอบ workflows ใหม่ให้มี frontmatter:

```bash
# Run in CI/CD
python3 check_workflow_frontmatter.py
if [ $? -ne 0 ]; then
  echo "❌ Workflow frontmatter validation failed"
  exit 1
fi
```

### 2. Add More Metadata

พิจารณาเพิ่ม fields อื่นๆ:
- `tags` - สำหรับจัดหมวดหมู่
- `platform` - รองรับ platforms ใดบ้าง
- `examples` - ตัวอย่างการใช้งาน

### 3. Documentation

อัปเดตเอกสารให้ระบุ:
- ความต้องการของ YAML frontmatter
- วิธีสร้าง workflow ใหม่
- Best practices

---

**สร้างเมื่อ:** 13 ธันวาคม 2025  
**เวอร์ชัน:** 1.0
