# การอัพเดท README.md - ปรับปรุงคำสั่งให้ตรงกับ Workflow จริง

## วันที่: 3 ธันวาคม 2025

## สรุปการเปลี่ยนแปลง

ได้ทำการปรับปรุงคำสั่งใช้งานใน README.md ให้ตรงกับชื่อไฟล์ workflow ที่มีอยู่จริงใน folder `.kilocode/workflows/`

## ไฟล์ Workflow ที่มีอยู่จริง

1. `smartspec_generate_spec.md` - สร้าง SPEC
2. `smartspec_generate_plan.md` - สร้าง Plan
3. `smartspec_generate_tasks.md` - สร้าง Tasks
4. `smartspec_generate_kilo_prompt.md` - สร้าง Kilo Prompt
5. `smartspec_sync_spec_tasks.md` - ซิงค์ SPEC กับ Tasks
6. `smartspec_verify_tasks_progress.md` - ตรวจสอบความคืบหน้า

## รายละเอียดการแก้ไข

### 1. Section 4: Profiles System
**เดิม:**
```
/spec create financial
/spec update financial
```

**ใหม่:**
```
/smartspec_generate_spec.md
```
จากนั้นเลือก profile ที่ต้องการเมื่อถูกถาม

### 2. Section 5: Domains
**เดิม:**
```
/spec create financial --domain=fintech
```

**ใหม่:**
```
/smartspec_generate_spec.md
```
จากนั้นระบุ domain ที่ต้องการเมื่อถูกถาม

### 3. Section 7: Dependency Injection Control Modes
**เดิม:**
```
/spec update full --di=auto
```

**ใหม่:**
รัน `/smartspec_generate_spec.md` และระบุ DI mode เมื่อถูกถาม

### 4. Section 8: Security Modes
**เดิม:**
```
--security=stride-basic
--security=stride-full
```

**ใหม่:**
รัน `/smartspec_generate_spec.md` และระบุ security mode เมื่อถูกถาม

### 5. Section 9: Performance Modes
**เดิม:**
```
--performance=basic
--performance=full
```

**ใหม่:**
รัน `/smartspec_generate_spec.md` และระบุ performance mode เมื่อถูกถาม

### 6. Section 11: Compact Mode
**เดิม:**
```
/spec create financial --mode=compact
```

**ใหม่:**
รัน `/smartspec_generate_spec.md` และระบุ compact mode เมื่อถูกถาม

### 7. Section 12: Force Update System
**เดิม:**
```
/spec update full --force-update=stride
/spec update financial --force-update=performance,config
/spec update full --force-update=all
```

**ใหม่:**
1. รัน `/smartspec_generate_spec.md`
2. ระบุ force-update options เมื่อถูกถาม

### 8. Section 14: Migration Guide
**เดิม:**
```
/spec upgrade v5
```

**ใหม่:**
รัน `/smartspec_generate_spec.md` กับ SPEC เดิมเพื่ออัพเกรดเป็น V5

### 9. Section 15: Workflow Summary
**เดิม:** แสดง 3 workflows
- `/spec create <profile> --domain=<domain>`
- `/spec tasks <path>`
- `/spec kilo <path>`

**ใหม่:** แสดง 6 workflows ทั้งหมด
1. `/smartspec_generate_spec.md` - สร้าง SPEC
2. `/smartspec_generate_plan.md` - สร้าง Plan
3. `/smartspec_generate_tasks.md` - สร้าง Tasks
4. `/smartspec_generate_kilo_prompt.md` - สร้าง Kilo Prompt
5. `/smartspec_sync_spec_tasks.md` - ซิงค์ SPEC กับ Tasks
6. `/smartspec_verify_tasks_progress.md` - ตรวจสอบความคืบหน้า

### 10. Section 17: Example Usage
ปรับปรุงตัวอย่างทั้งหมดให้ใช้ชื่อไฟล์ workflow จริง และเพิ่มตัวอย่างใหม่:
- Generate project plan
- Sync SPEC with tasks
- Verify implementation progress

### 11. Section 18: Troubleshooting
**เพิ่มเติม:**
- Tasks out of sync → run `/smartspec_sync_spec_tasks.md`

**ปรับปรุง:**
- SPEC missing sections → run `/smartspec_generate_spec.md`
- Kilo prompt missing tasks → re-run `/smartspec_generate_tasks.md`

## ผลกระทบ

การเปลี่ยนแปลงนี้ทำให้:
1. ✅ คำสั่งใน README ตรงกับชื่อไฟล์ workflow จริงที่มีใน `.kilocode/workflows/`
2. ✅ ผู้ใช้สามารถใช้งานได้ถูกต้องตามที่แสดงใน UI
3. ✅ เพิ่มความชัดเจนในการใช้งาน workflows ทั้ง 6 แบบ
4. ✅ ลดความสับสนจากคำสั่งแบบเก่าที่ใช้ไม่ได้

## การทดสอบ

ควรทดสอบว่า:
- [ ] ไฟล์ workflow ทั้ง 6 ไฟล์ทำงานได้ถูกต้อง
- [ ] คำสั่งที่แสดงใน README สามารถเรียกใช้งานได้จริง
- [ ] เอกสารอื่นๆ ใน `doc/` folder ยังคงสอดคล้องกัน
