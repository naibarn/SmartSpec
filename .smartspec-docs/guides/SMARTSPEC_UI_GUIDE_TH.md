# SmartSpec UI Guide (Penpot JSON-First)
Version: 1.0  
Last updated: 2025-12-07

เอกสารนี้เป็นคู่มือการออกแบบ/พัฒนา **SPEC ประเภท UI** ในระบบ SmartSpec  
โดยยึดแนวคิด **centralization** และรองรับการทำงานร่วมกันของทีม UI + ทีม dev แบบไม่ชนกัน

โครงเอกสารและแนวการใช้ตัวอย่าง/Best practices ตั้งใจให้ใกล้เคียง guide แบบ “อธิบายภาพรวม → ใช้เมื่อไร → ทำอย่างไร → ตัวอย่าง → ข้อควรระวัง” ตามรูปแบบคู่มือเดิมของทีม เพื่อให้ทีมอ่านต่อได้ลื่นและคุ้นโทนเอกสาร

---

## 1) เป้าหมายของ UI Spec

UI Spec มีหน้าที่:
1) กำหนด UX/UI scope ของฟีเจอร์ให้ชัด  
2) ทำให้ทีม UI สามารถ **แก้ไขดีไซน์ผ่าน Penpot ได้โดยตรง**  
3) ทำให้ทีม dev implement ได้โดยไม่เดา component/ชื่อ/โครงสร้างใหม่เอง  
4) ลด drift ระหว่าง:
   - Design (Penpot)
   - Spec narrative
   - Code components
   - Shared registries

---

## 2) นิยามสำคัญ

### 2.1 UI JSON = Design Source of Truth

สำหรับ SPEC ประเภท UI ให้ถือว่าไฟล์ **UI JSON** เป็น “ความจริงเชิงดีไซน์”  
เพื่อให้ Penpot อ่าน/เขียนได้โดยตรง

### 2.2 spec.md = Narrative & Rules

`spec.md` ใช้สำหรับ:
- ภาพรวมปัญหา/เป้าหมาย
- Scope / Non-goals
- UX rules
- Accessibility
- Performance UX targets
- ข้อจำกัดด้าน security ที่สะท้อนออกมาใน UI (เช่น flow เชิง permission)

**แต่ไม่ใช่ที่เก็บ layout รายละเอียดระดับ design tool**

---

## 3) โครงสร้างไฟล์มาตรฐาน

ภายใต้โฟลเดอร์ของ UI spec:

```
specs/ui/<spec-id>/
  spec.md
  tasks.md (optional แต่แนะนำ)
  ui.json
  assets/ (optional)
```

> ชื่อ `ui.json` สามารถเปลี่ยนได้ผ่าน config  
> แต่ต้อง “มีไฟล์เดียวที่เป็น design source of truth” เสมอ

---

## 4) Separation of Concerns (กติกาห้ามพลาด)

**หลักการทองคำ:**
- `ui.json` = design + structure + bindings + token references
- business logic / data fetching / permissions / validation rules  
  ต้องอยู่ที่:
  - code components
  - hooks / store
  - services / API clients
  - หรือระบุเชิง narrative ใน `spec.md`

### 4.1 ยกตัวอย่างสิ่งที่ “ไม่ควรอยู่ใน ui.json”

- เงื่อนไข business rules แบบ if/else เชิงโดเมน
- API behaviour ที่มี side effects
- permission logic แบบละเอียด
- การคำนวณราคาหรือเครดิต

### 4.2 สิ่งที่ “อยู่ได้”

- mapping กว้าง ๆ เช่น
  - หน้าจอ/section นี้ bind กับ component ชื่อ X
  - ใช้ design token ชื่อ Y
  - state slot ระดับ UI เช่น loading/empty/error **ในเชิง layout**

---

## 5) Registry สำหรับ UI (แนะนำให้ใช้)

เพื่อให้ชื่อ component ไม่แตกเป็นหลายแบบข้าม spec  
แนะนำ registry เพิ่ม:

`.spec/registry/ui-component-registry.json`

โครงสร้างขั้นต่ำ:

```json
{
  "version": "1.0.0",
  "last_updated": "2025-12-07T00:00:00Z",
  "components": [
    {
      "canonical_name": "UserAvatar",
      "penpot_component_id": "penpot:component:xxx",
      "code_component_path": "src/components/user/UserAvatar.tsx",
      "owned_by_spec": "spec-ui-xxx",
      "aliases": []
    }
  ]
}
```

**กติกาใช้งาน**
- generate-spec / generate-tasks สามารถเพิ่ม entry ใหม่ได้
- implement / verify / refactor ต้อง **อ่านอย่างเดียว**
- หากพบชื่อใหม่ใน spec/tasks ที่ไม่มีใน registry:
  - ให้สร้าง “registration task” เพิ่ม

---

## 6) การตั้งชื่อ (Naming Conventions)

### 6.1 หน้าจอ/ฟีเจอร์

- ใช้คำจาก glossary เป็นหลัก
- ตั้งชื่อให้สะท้อน behavior ของผู้ใช้ ไม่ใช่ชื่อเทคนิค

### 6.2 Component

- ใช้ `PascalCase`
- ถ้าเป็น shared component ระดับระบบ:
  - ต้องลงทะเบียนใน UI component registry

---

## 7) การใช้ SPEC_INDEX กับ UI

ใน `SPEC_INDEX.json` จะมี spec ประเภท UI อยู่แล้วหลายตัว  
โดยใช้ `category: "ui"` และมักมี dependency ไปยัง core เช่น authentication/audit logging

บนหลักการนี้:
- UI spec ควรพึ่ง **contract ของ core**  
  ไม่ควรพยายามแก้ logic ของ core ผ่าน tasks ฝั่ง UI
- ถ้า UI flow ต้องเปลี่ยน core contract:
  - ให้สร้าง/อัปเดต spec ฝั่ง core ก่อน

---

## 8) Workflow ที่เกี่ยวกับ UI (ภาพใหญ่)

ลำดับที่แนะนำสำหรับ UI spec:

1) **generate-spec**
   - สร้าง `spec.md` + `ui.json` template ขั้นต่ำ
   - ลงทะเบียนใน SPEC_INDEX

2) **generate-plan**
   - กำหนด milestone:
     - design milestone
     - component binding milestone
     - logic milestone

3) **generate-tasks**
   - แตกงานเป็น 3 track ชัดเจน:
     1) Design tasks (ทีม UI / Penpot)
     2) Binding tasks (map Penpot → code)
     3) Logic tasks (ทีม dev)

4) **generate-implement-prompt / cursor-prompt**
   - ใส่ canonical constraints:
     - component names
     - screen names
     - shared glossary terms

5) **implement-tasks**
   - Treat `ui.json` เป็น design-owned
   - แก้ได้เฉพาะ tasks ระบุ

6) **generate-tests**
   - เน้น:
     - component tests
     - accessibility checks
     - (ถ้ามีระบบ) visual regression

7) **verify-tasks-progress**
   - ตรวจ 2 มิติ:
     - ความคืบหน้าใน tasks
     - ความสอดคล้องกับ registry + ui.json

8) **refactor-code**
   - ย้าย logic ที่เผลอฝังใน UI layer ออก
   - ไม่แตะ `ui.json` ถ้าไม่จำเป็น

9) **sync_spec_tasks / fix_errors**
   - กัน drift ระหว่าง spec ↔ tasks ↔ design artifacts

10) **validate-index / reindex-specs**
   - ตรวจว่า UI spec มี `ui.json`

---

## 9) Template แนะนำ

### 9.1 ส่วนสำคัญใน spec.md ของ UI

- Overview
- User personas / scenarios (ถ้ามี)
- Scope / Non-goals
- UX rules
- Accessibility baseline
- Performance UX targets
- Dependencies (อ้างอิง id ใน SPEC_INDEX)
- Design artifacts
  - ระบุ path ของ `ui.json`

### 9.2 ui.json (ขั้นต่ำ)

> รูปแบบจริงขึ้นกับมาตรฐานที่ทีม UI ใช้กับ Penpot  
> แต่แนะนำให้มีฟิลด์ “anchor” เพื่อให้ tooling ผูกง่าย

```json
{
  "ui_spec_id": "spec-ui-xxx",
  "version": "0.1.0",
  "penpot": {
    "project_id": "optional",
    "file_id": "optional"
  },
  "screens": [
    {
      "name": "User Profile",
      "screen_id": "penpot:frame:xxx",
      "components": [
        {
          "canonical_name": "UserAvatar",
          "penpot_component_id": "penpot:component:yyy"
        }
      ]
    }
  ],
  "tokens": {
    "ref": "design-tokens-v1"
  }
}
```

---

## 10) แนวทาง Migration (สำหรับทีมที่ยังไม่ใช้ ui.json)

เพื่อไม่ให้กระทบโปรเจกต์เก่า:

### 10.1 Legacy UI Mode

เมื่อ spec มี `category=ui` แต่ยังไม่มี `ui.json`:
- เครื่องมือควรทำงานในโหมด legacy
- ให้ผลเป็น:
  - **WARN** ไม่ใช่ FAIL
  - สร้าง migration tasks แบบ optional

### 10.2 Migration Steps

1) สร้าง `ui.json` ด้วย template ขั้นต่ำ  
2) map หน้าจอหลัก 1-2 หน้าก่อน  
3) เพิ่ม component registry เฉพาะส่วนที่ใช้จริง  
4) ค่อย ๆ ย้ายรายละเอียด design เพิ่ม

---

## 11) ข้อผิดพลาดที่พบบ่อย

1) **UI JSON ถูกแก้โดย dev แบบไม่ผ่าน tasks**  
   → ทำให้ทีม UI เจอ conflict ใน Penpot

2) **ชื่อ component แตกหลายแบบ**  
   → ไม่มี registry หรือไม่บังคับ registration tasks

3) **UI spec พยายามแก้ core private โดยตรง**  
   → ต้องแยกงานไปยัง core spec

4) **tasks UI ไม่แยก design/binding/logic**  
   → ทำให้ประมาณ effort และ ownership ผิด

---

## 12) Checklist สำหรับ Review ก่อน merge

- [ ] UI spec มี `spec.md` + `ui.json`
- [ ] `ui.json` ไม่มี business logic
- [ ] Component ที่อ้างใน spec/tasks:
      - อยู่ใน UI component registry หรือมี registration task
- [ ] Dependencies ใน spec ตรงกับ SPEC_INDEX
- [ ] งานที่แตะ core ทำผ่าน core spec ไม่ใช่ UI spec
- [ ] มี acceptance criteria ที่ครอบคลุม accessibility

---

## 13) ตัวอย่างการเขียน tasks สำหรับ UI

**Design track**
- [ ] D001: Update layout & flow in `ui.json` via Penpot export sync
- [ ] D002: Confirm accessibility contrast + typography tokens

**Binding track**
- [ ] B001: Map Penpot component `UserAvatar` → `src/components/user/UserAvatar.tsx`
- [ ] B002: Register component in `ui-component-registry.json`

**Logic track**
- [ ] L001: Implement `useUserProfile()` hook
- [ ] L002: Wire API client + error states
- [ ] L003: Add permission guard for profile edit

---

## 14) สรุป

UI Spec แบบ Penpot JSON-first ทำให้:
- ทีม UI และ dev ทำงานคู่ขนานได้จริง
- ลดการชนกันของชื่อ/โครงสร้าง
- ลด drift ระหว่าง design ↔ spec ↔ code

หัวใจคือ:
1) `ui.json` เป็น design source of truth  
2) logic อยู่ในโค้ด/เอกสาร narrative  
3) registry-first สำหรับชื่อ component  
4) workflow ต้องแยก track งานให้ชัด
