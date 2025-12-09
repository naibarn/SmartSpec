---
 title: SmartSpec Installation Manual (TH)
 version: 5.6
 audience: Dev / DevOps / Platform team
 scope: Project-local installation of SmartSpec core (.smartspec, .smartspec-docs)
---

# 1. ภาพรวม

คู่มือนี้อธิบายวิธีติดตั้ง **SmartSpec** แบบ *project-local* โดยใช้สคริปต์:

- `install.sh` (Linux / macOS)
- `install.ps1` (Windows / PowerShell)

หลังติดตั้งแล้ว โปรเจกต์จะมีสิ่งสำคัญดังนี้:

- โฟลเดอร์ **`.smartspec/`**
  - `system_prompt_smartspec.md`  → system prompt กลางของ SmartSpec
  - `knowledge_base_smartspec.md` → knowledge base กลาง (กติกาเวอร์ชัน 5.6+)
  - `workflows/` → ไฟล์ workflow `/smartspec_*` ทั้งหมด (รวมถึง `/smartspec_project_copilot`)
- โฟลเดอร์ **`.smartspec-docs/`**
  - `workflows/` → คู่มือและเอกสารประกอบของแต่ละ workflow (TH/EN, examples ฯลฯ)
- โฟลเดอร์คำสั่งของเครื่องมือต่าง ๆ (สร้าง/อัปเดตอัตโนมัติเมื่อมี)
  - `.kilocode/workflows`
  - `.roo/commands`
  - `.claude/commands`
  - `.agent/workflows`
  - `.gemini/commands`

> จุดสำคัญ: **ชื่อไฟล์ system prompt และ knowledge base เป็นชื่อคงที่**
> (`system_prompt_smartspec.md`, `knowledge_base_smartspec.md`) ทำให้เวลา
> อัปเดตเวอร์ชันในอนาคตไม่ต้องแก้สคริปต์หรือ workflow ใด ๆ

---

# 2. สิ่งที่ติดตั้งโดยรวม

เมื่อติดตั้งเสร็จ สคริปต์จะทำงานโดยสรุปดังนี้:

1. ดาวน์โหลด **SmartSpec distribution repo** ตาม URL/branch ที่กำหนด
2. คัดลอกโฟลเดอร์ต่อไปนี้เข้ามาในโปรเจกต์ปัจจุบัน:
   - `.smartspec/`
   - `.smartspec-docs/` (ถ้ามีใน repo)
3. ตรวจสอบว่าไฟล์ core มีอยู่:
   - `.smartspec/system_prompt_smartspec.md`
   - `.smartspec/knowledge_base_smartspec.md`
4. คัดลอก `./.smartspec/workflows` ไปยังโฟลเดอร์ของเครื่องมืออื่น ๆ ในโปรเจกต์
   - `.kilocode/workflows`
   - `.roo/commands`
   - `.claude/commands`
   - `.agent/workflows`
   - `.gemini/commands`

สคริปต์จะ **ไม่แตะโฟลเดอร์ `.spec/`** (index/registry/reports) เพราะถือว่าเป็นของโปรเจกต์และเวิร์กโฟลว์เอง

---

# 3. ข้อกำหนดเบื้องต้น

## 3.1 Linux / macOS (`install.sh`)

ต้องมีอย่างน้อยหนึ่งชุดต่อไปนี้:

- `git` (แนะนำที่สุด) **หรือ**
- `curl` หรือ `wget` + `unzip`

และต้องรันบน shell ที่รองรับ `bash`/`sh` เช่น:

- Bash บน Linux
- Bash/Zsh บน macOS

## 3.2 Windows (`install.ps1`)

- ใช้ PowerShell เวอร์ชันที่รองรับคำสั่ง:
  - `git` (ถ้ามี) **หรือ** `Invoke-WebRequest` + `Expand-Archive`
- แนะนำรันใน PowerShell ที่มีสิทธิ์อ่าน/เขียนไฟล์ในโปรเจกต์ได้ครบ

> หมายเหตุ: ในทุกแพลตฟอร์มควรมีสิทธิ์เขียนไฟล์ในโฟลเดอร์โปรเจกต์ปัจจุบัน

---

# 4. การตั้งค่า Repo ก่อนติดตั้ง

โดยค่าเริ่มต้น สคริปต์ใช้ค่า:

- Linux/macOS: ตัวแปร environment (ตั้งค่าก่อนรันได้)
  - `SMARTSPEC_REPO_URL` (ค่า default: `https://github.com/your-org/SmartSpec.git`)
  - `SMARTSPEC_REPO_BRANCH` (ค่า default: `main`)
- Windows (PowerShell): ใช้ `$env:SMARTSPEC_REPO_URL`, `$env:SMARTSPEC_REPO_BRANCH`

แนะนำให้ทีม Platform/Architecture กำหนดให้ชัดเจนว่า:

- ควรดึง SmartSpec จาก repo ไหน (เช่น internal Git server)
- ใช้ branch/tag ไหนเป็น **distribution branch** สำหรับการติดตั้งในแต่ละ environment

ตัวอย่าง (Linux/macOS):

```bash
export SMARTSPEC_REPO_URL="https://git.company.local/platform/SmartSpec.git"
export SMARTSPEC_REPO_BRANCH="release-5.6"
./install.sh
```

ตัวอย่าง (Windows/PowerShell):

```powershell
$env:SMARTSPEC_REPO_URL    = 'https://git.company.local/platform/SmartSpec.git'
$env:SMARTSPEC_REPO_BRANCH = 'release-5.6'
./install.ps1
```

---

# 5. ขั้นตอนติดตั้งบน Linux / macOS

1. เปิดเทอร์มินัลและ `cd` เข้ามาที่ root ของโปรเจกต์
2. วางไฟล์ `install.sh` ไว้ใน root โปรเจกต์
3. (ทางเลือก) ตั้งค่า `SMARTSPEC_REPO_URL` / `SMARTSPEC_REPO_BRANCH` ให้ตรงกับ environment
4. ทำให้ไฟล์รันได้:

   ```bash
   chmod +x install.sh
   ```

5. รันสคริปต์:

   ```bash
   ./install.sh
   ```

6. เมื่อสำเร็จ คุณจะเห็นข้อความคล้าย:

   ```
   ✅ SmartSpec installation/update complete.
      - Core:   .smartspec
      - Docs:   .smartspec-docs (if present in repo)
      - Tools:  .kilocode/workflows, .roo/commands, ...
   ```

---

# 6. ขั้นตอนติดตั้งบน Windows (PowerShell)

1. เปิด PowerShell และ `cd` เข้ามาที่ root ของโปรเจกต์
2. วางไฟล์ `install.ps1` ไว้ใน root โปรเจกต์
3. (ทางเลือก) ตั้งค่า `$env:SMARTSPEC_REPO_URL` / `$env:SMARTSPEC_REPO_BRANCH`
4. หาก Execution Policy จำกัด ให้เปิดใช้ชั่วคราว:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

5. รันสคริปต์:

   ```powershell
   ./install.ps1
   ```

6. เมื่อสำเร็จ จะเห็นข้อความสรุปเหมือนฝั่ง Linux/macOS

---

# 7. โครงสร้างโฟลเดอร์หลังติดตั้ง

หลังรัน installer สำเร็จ โปรเจกต์ควรมีโครงสร้างสำคัญประมาณนี้:

```text
.
├─ .smartspec/
│  ├─ system_prompt_smartspec.md
│  ├─ knowledge_base_smartspec.md
│  └─ workflows/
│     ├─ smartspec_generate_spec.md
│     ├─ smartspec_generate_plan.md
│     ├─ smartspec_project_copilot.md
│     └─ ...
├─ .smartspec-docs/
│  └─ workflows/
│     ├─ smartspec_generate_spec/
│     │  ├─ manual_th.md
│     │  ├─ manual_en.md
│     │  └─ examples.md
│     ├─ smartspec_project_copilot/
│     │  ├─ manual_th.md
│     │  ├─ manual_en.md
│     │  └─ ...
│     └─ ...
├─ .kilocode/workflows/
├─ .roo/commands/
├─ .claude/commands/
├─ .agent/workflows/
└─ .gemini/commands/
```

> หมายเหตุ: โฟลเดอร์ `.spec/` (index, registry, reports) เป็นของโปรเจกต์
> และไม่ได้ถูกสร้าง/แก้ไขโดย installer โดยตรง

---

# 8. การอัปเดตเวอร์ชัน SmartSpec

เมื่อต้องการอัปเดต SmartSpec (เช่น จาก 5.6.0 → 5.6.1 หรือ update KB ใหม่):

1. ให้ทีม Platform อัปเดต distribution repo (แก้เนื้อใน `.smartspec/*` และ `.smartspec-docs/*`)
2. ในแต่ละโปรเจกต์ ให้รัน `install.sh` หรือ `install.ps1` ซ้ำอีกครั้ง
3. สคริปต์จะ:
   - สำรอง (backup) โฟลเดอร์เดิมบางส่วน เช่น:
     - `.smartspec/` → `.smartspec.backup.<timestamp>`
     - `.smartspec-docs/` → `.smartspec-docs.backup.<timestamp>`
   - คัดลอกเวอร์ชันล่าสุดจาก repo มาทับ

> แนะนำ: อย่าแก้ไฟล์ใน `.smartspec/workflows` โดยตรงในโปรเจกต์
> หากต้องการ custom ให้ใช้วิธีเพิ่มไฟล์ overlay หรือ config ฝั่งโปรเจกต์
> เพื่อหลีกเลี่ยง conflict เวลาติดตั้งเวอร์ชันใหม่

---

# 9. การใช้งานร่วมกับ `/smartspec_project_copilot`

หลังติดตั้ง SmartSpec แล้ว คุณสามารถใช้ workflow `/smartspec_project_copilot` เป็น
"เลขา/ที่ปรึกษา" ระดับโปรเจกต์ได้ทันที (ผ่าน Kilo/Roo/Claude/ฯลฯ):

ตัวอย่าง (แนวคิด):

- รันคำสั่ง copilot พร้อมกำหนด root ของโปรเจกต์
- ให้ copilot อ่าน:
  - `.spec/` (index, registry, reports)
  - `.smartspec/system_prompt_smartspec.md`
  - `.smartspec/knowledge_base_smartspec.md`
  - `.smartspec-docs/workflows/**`
- แล้วถามเป็นภาษาคน เช่น:
  - "ตอนนี้โปรเจกต์พร้อมปล่อย production หรือยัง?"
  - "ควรรัน workflow ตัวไหนต่อสำหรับเช็ก security/perf/UI?"

> รายละเอียดวิธีใช้ `/smartspec_project_copilot` ดูได้จากคู่มือของ workflow นั้นใน
> `.smartspec-docs/workflows/smartspec_project_copilot/`

---

# 10. ข้อควรระวังด้านความปลอดภัย

- ใช้ `SMARTSPEC_REPO_URL` ชี้ไปยัง **repo ที่เชื่อถือได้** เท่านั้น
- อย่าแก้ไข `system_prompt_smartspec.md` หรือ `knowledge_base_smartspec.md`
  ในโปรเจกต์แบบสุ่ม เพราะเป็นไฟล์ที่ควบคุมพฤติกรรมทั้งหมดของ SmartSpec
- เมื่อมีการเปลี่ยน policy สำคัญ (เช่น tool-version-registry, security rules,
  design-system) ให้ทีม Platform อัปเดตไฟล์ใน repo กลาง แล้วให้แต่ละโปรเจกต์รัน
  installer ใหม่

---

# 11. Troubleshooting พื้นฐาน

- **รันแล้วขึ้น error เรื่อง git/curl/wget/unzip**
  - ติดตั้งเครื่องมือเหล่านั้นตามแพลตฟอร์มที่ใช้
- **หลังรันแล้วไม่เห็นโฟลเดอร์ `.smartspec/`**
  - ตรวจสอบว่า repo ที่ตั้งค่าไว้มีโฟลเดอร์ `.smartspec/` อยู่จริง
- **ไม่พบไฟล์ `system_prompt_smartspec.md` หรือ `knowledge_base_smartspec.md`**
  - ตรวจสอบ path ใน repo และติดตั้งใหม่
- **workflow ไม่เห็น docs ใน `.smartspec-docs/`**
  - ตรวจสอบว่า installer ดึง `.smartspec-docs/` มาด้วยหรือไม่

หากมีปัญหาที่ซับซ้อนกว่านี้ แนะนำเก็บ log การรัน installer และปรึกษาทีม Platform
หรืออัปเดต SmartSpec distribution repo ให้ถูกต้องก่อนติดตั้งใหม่อีกครั้ง
