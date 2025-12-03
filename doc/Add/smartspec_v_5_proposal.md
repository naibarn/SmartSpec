# SmartSpec v5.0 – Proposal for Improvements

This documentสรุปข้อเสนอในการปรับปรุง SmartSpec เพื่อให้เวอร์ชัน 5.0 ใช้งานง่ายขึ้น มีความยืดหยุ่น และปรับให้เหมาะกับงานจริงหลากหลายประเภท ทั้งระบบใหญ่ (mission‑critical) และงานทั่วไป

---

# 1. ลดความซับซ้อนด้วย **Profiles System**
SmartSpec เวอร์ชันปัจจุบันถูกออกแบบให้รองรับระบบ critical แต่หลายโปรเจ็กต์ต้องการเพียงโครงสร้างพื้นฐานที่ง่ายกว่า ดังนั้นจึงเสนอให้มี **profiles** ให้เลือก:

## 1.1 ประเภทของ Profiles
- **basic** – สร้างเฉพาะส่วนสำคัญ (Overview, Architecture, API/Data Model)
- **backend-service** – สำหรับ microservice ทั่วไป (DI, config, testing)
- **financial** – เปิด performance+security เต็มรูปแบบ
- **full (default)** – ทุก module ครบตาม SmartSpec v4

## 1.2 ตัวอย่างการใช้งาน
```bash
smartspec new payment-service --profile=financial
```

## 1.3 ประโยชน์
- ลดความยาว spec
- ไม่ต้องลบบทที่ไม่จำเป็นด้วยตัวเอง
- เหมาะกับทีมหลาย maturity level

---

# 2. Critical Sections ด้วย **Meta Tags** (ลด false-positive)
ปัจจุบัน SmartSpec ตรวจจับ critical section จาก keyword เช่น STRIDE, Zod, metrics ซึ่งอาจทำให้ detect ผิดพลาด

## 2.1 เสนอให้เพิ่ม meta tag
```markdown
<!-- @critical security -->
<!-- @critical config -->
<!-- @critical di -->
<!-- @critical monitoring -->
```

## 2.2 ประโยชน์
- ระบุตรงจุด ไม่ต้องอาศัยการค้นหา keyword
- ลดโอกาส restore ผิดตำแหน่ง
- ช่วยให้ SPEC ปรับแต่งได้ชัดเจน

---

# 3. สร้าง **Compact Technical Spec Mode**
Spec ปัจจุบันมีความยาวมาก (20–40 หน้าในบางระบบ) ซึ่งหนักเกินไปสำหรับงานทั่วไป เช่น CRUD หรือ internal tools

## 3.1 โหมดใหม่: `--mode=compact`
สร้างเฉพาะ 5 ส่วน:
1. Overview
2. Architecture Summary
3. API / Data Model
4. Constraints & Risk Notes
5. Acceptance Tests

## 3.2 ใช้งาน
```bash
smartspec new report-exporter --mode=compact
```

---

# 4. ปรับปรุง Performance Detection ให้ฉลาดขึ้น
ระบบปัจจุบัน detect จาก keyword เท่านั้น เช่น credit, TPS, saga แต่ควร detect จาก **domain** ด้วย

## 4.1 เพิ่ม domain-based rules เช่น
- Healthcare → เข้าข่าย real-time + privacy critical
- IoT / telemetry → throughput สูง
- Logistics → SLA สูง
- AI inference → latency sensitive

## 4.2 เสนอให้เพิ่มไฟล์ config
```
.smartspec/performance-domains.json
```
เพื่อให้ทีม custom ได้เอง

---

# 5. DI Pattern แบบเลือกได้ (ไม่บังคับทุกระบบ)
SmartSpec v4 บังคับ DI pattern สำหรับ backend service ทั้งหมด แต่บางประเภทไม่จำเป็น:
- front-end
- batch job
- cron job
- data pipeline
- ML training

## 5.1 เพิ่มตัวเลือก
```
--no-di
```
หรือ
```
--di=minimal
```
---

# 6. STRIDE Model แบบสองระดับ (Full / Basic)
ปัจจุบัน STRIDE มีความยาวมาก (>100 บรรทัด)

## 6.1 เพิ่มตัวเลือก
```
--security=stride-basic
--security=stride-full
```

## 6.2 STRIDE-Basic
- ตารางย่อ 5–10 บรรทัด
- ระบุ threat หลัก ๆ เท่านั้น

---

# 7. ปรับปรุงการ Restore Critical Sections
ปัจจุบัน SmartSpec จะ restore critical section หากถูกแก้ไขจนผิดเงื่อนไข (เช่น ยาวน้อยลงกว่า 80%) แต่บางครั้งผู้ใช้ต้องการแก้จริง ๆ

## 7.1 เสนอ flag
```
--force-update=stride,config-schema
```

## 7.2 หรือ meta tag override
```markdown
<!-- @critical allow-update -->
```

---

# 8. รวมไฟล์ Output ให้อยู่ในโฟลเดอร์เดียว
ตอนนี้ SmartSpec กระจายไฟล์หลายที่ เช่น backup, report, registry ซึ่งอาจทำให้ workspace รก

## 8.1 เสนอโฟลเดอร์รวม
```
.smartspec/
   backups/
   reports/
   registry.json
   trace.log
```
และเปิด/ปิดด้วย flag:
```
--no-backup
--no-report
```

---

# 9. เพิ่ม **Consistency Validator** ระหว่าง sections
SmartSpec v4 ตรวจเฉพาะ critical sections แต่ยังไม่ตรวจความสอดคล้องของเนื้อหา

## 9.1 ตัวอย่าง consistency rules
- API ที่เขียนใน Architecture ต้องปรากฏใน Examples
- ถ้ามี Queue → ต้องมี Queue ใน Performance Requirements
- ถ้ามี database transactions → ต้องมี Integration Tests
- ถ้ามี external API → ต้องมี Retry/Backoff Policy

## 9.2 Flag
```
--validate-consistency
```

---

# 10. Summary: สิ่งที่ SmartSpec v5 จะดีขึ้น
## 10.1 สิ่งที่ถูกเพิ่ม
- Profiles system
- Meta-tag critical
- Compact mode
- Domain-based performance detection
- Consistency validator

## 10.2 สิ่งที่ถูกลดความเข้มงวด
- DI pattern
- STRIDE model
- Restore critical behavior
- การตรวจ keyword

## 10.3 ผลลัพธ์โดยรวม
- SmartSpec จะใช้งานง่ายขึ้น 30–50%
- ยืดหยุ่นกับระบบหลากหลายประเภท
- ลดความยาว spec โดยเฉพาะระบบทั่วไป
- ยังคงความเข้มของการจัดการระบบสำคัญ

---

# 11. ข้อเสนอถัดไป
- สร้าง SmartSpec v5 configuration file (`smartspec.config.json`)
- รองรับ plugin สำหรับทีม/องค์กร
- รองรับการ generate diagram อัตโนมัติ

---

**Document Version:** Draft 1.0
**Author:** ChatGPT

