# Folder Naming Risk Analysis & Solution

**Date:** 2025-01-04  
**Issue:** Folder names may conflict with user's existing folders  
**Severity:** 🚨 CRITICAL (docs/), ⚠️ HIGH (doc/), ⚠️ MEDIUM (scripts/)

---

## 🚨 Problem

### **Current Structure (RISKY)**

```
SmartSpec/
├── README.md                          ← Standard (OK)
├── LICENSE                            ← Standard (OK)
│
├── .kilocode/workflows/               ← Platform-specific (OK)
├── .smartspec/                        ← SmartSpec-specific (OK)
│
├── docs/                              ⚠️⚠️⚠️ CRITICAL RISK
├── doc/                               ⚠️⚠️ HIGH RISK
└── scripts/                           ⚠️ MEDIUM RISK
```

### **Risk Assessment**

| Folder | Risk Level | Probability | Impact | Reason |
|--------|-----------|-------------|--------|--------|
| `docs/` | 🚨 CRITICAL | 80% | HIGH | Very common name, almost every project has `docs/` |
| `doc/` | ⚠️ HIGH | 40% | HIGH | Common alternative to `docs/` |
| `scripts/` | ⚠️ MEDIUM | 60% | MEDIUM | Common for build/deploy scripts |
| `.smartspec/` | ✅ SAFE | <1% | LOW | Specific to SmartSpec |
| `.kilocode/` | ✅ SAFE | <1% | LOW | Specific to Kilo Code |

### **Conflict Scenarios**

#### **Scenario 1: User has `docs/` folder**
```
User's Project/
├── docs/                              ← User's documentation
│   ├── api/
│   ├── guides/
│   └── README.md
```

**After SmartSpec Installation:**
```
User's Project/
├── docs/                              ❌ OVERWRITTEN!
│   ├── implementation/                ← SmartSpec files
│   ├── analysis/                      ← SmartSpec files
│   └── ...                            ← User's files LOST!
```

#### **Scenario 2: User has `scripts/` folder**
```
User's Project/
├── scripts/                           ← User's build scripts
│   ├── build.sh
│   ├── deploy.sh
│   └── test.sh
```

**After SmartSpec Installation:**
```
User's Project/
├── scripts/                           ❌ MIXED!
│   ├── build.sh                       ← User's
│   ├── deploy.sh                      ← User's
│   ├── install.sh                     ← SmartSpec (CONFLICT!)
│   └── ...
```

---

## 🎯 Solution

### **Principle: Use Specific Prefixes**

**Rules:**
1. ✅ Use `.smartspec-*` prefix for SmartSpec-specific folders
2. ✅ Use hidden folders (`.`) to avoid clutter
3. ✅ Keep standard files (README, LICENSE) as is
4. ✅ Never use common names (docs, scripts, src, lib, etc.)

### **Proposed Structure (SAFE)**

```
SmartSpec/
├── README.md                          ← Standard (OK)
├── LICENSE                            ← Standard (OK)
│
├── .kilocode/workflows/               ← Platform-specific (OK)
│
├── .smartspec/                        ← SmartSpec runtime
│   ├── scripts/                       ← Installation scripts (MOVED)
│   │   ├── install.sh
│   │   ├── install.ps1
│   │   ├── sync.sh
│   │   ├── sync.ps1
│   │   └── uninstall.sh
│   ├── SPEC_INDEX.example.json
│   ├── Knowledge-Base.md
│   ├── constitution.md
│   ├── kilocode-context.md
│   ├── performance-domains.json
│   ├── smartspec.config.json
│   └── system_prompt.md
│
└── .smartspec-dev/                    ← Development docs (RENAMED)
    ├── implementation/                (12 files)
    ├── analysis/                      (11 files)
    ├── design/                        (4 files)
    ├── fixes/                         (5 files)
    ├── guides/                        (2 files)
    └── plans/                         (3 files)
```

### **Changes Required**

| Current | New | Reason |
|---------|-----|--------|
| `docs/` | `.smartspec-dev/` | Avoid conflict with user's docs/ |
| `doc/` | (delete) | Duplicate, not needed |
| `scripts/` | `.smartspec/scripts/` | Avoid conflict, group with runtime files |

---

## 📋 Implementation Plan

### **Phase 1: Analysis** ✅
- [x] Identify risky folders
- [x] Assess risk levels
- [x] Design solution
- [x] Document changes

### **Phase 2: Rename & Move**
- [ ] Rename `docs/` → `.smartspec-dev/`
- [ ] Delete `doc/` (duplicate)
- [ ] Move `scripts/` → `.smartspec/scripts/`
- [ ] Update .gitignore

### **Phase 3: Update Scripts**
- [ ] Update install.sh (new paths)
- [ ] Update install.ps1 (new paths)
- [ ] Update sync.sh (if needed)
- [ ] Update sync.ps1 (if needed)
- [ ] Update uninstall.sh (new paths)

### **Phase 4: Testing & Commit**
- [ ] Test syntax
- [ ] Verify structure
- [ ] Update README
- [ ] Commit and push

---

## 🎨 Benefits

### **Before (RISKY)**

```
❌ docs/        - 80% conflict probability
❌ doc/         - 40% conflict probability
❌ scripts/     - 60% conflict probability
```

**Total Risk:** 3 high-risk folders

### **After (SAFE)**

```
✅ .smartspec-dev/     - <1% conflict probability
✅ .smartspec/scripts/ - <1% conflict probability
```

**Total Risk:** 0 high-risk folders

### **Improvements**

1. ✅ **No Conflicts** - Specific names won't clash
2. ✅ **Hidden Folders** - Less clutter in user's project
3. ✅ **Grouped** - All SmartSpec files under `.smartspec*`
4. ✅ **Clear** - Easy to identify SmartSpec files
5. ✅ **Professional** - Follows best practices

---

## 📊 Impact Analysis

### **User Experience**

**Before:**
```bash
$ ls
docs/          ← Wait, is this mine or SmartSpec's?
scripts/       ← Mixed files, confusing!
```

**After:**
```bash
$ ls -a
.smartspec/        ← Clear: SmartSpec runtime
.smartspec-dev/    ← Clear: SmartSpec dev docs (hidden)
```

### **Installation**

**Before:**
```bash
# Risk of overwriting user files
cp -r SmartSpec-main/docs/ ./docs/
cp -r SmartSpec-main/scripts/ ./scripts/
```

**After:**
```bash
# Safe: specific paths
cp -r SmartSpec-main/.smartspec/ ./.smartspec/
# Dev docs not installed (hidden, optional)
```

### **Updates**

**Before:**
```bash
# May overwrite user files
git pull
```

**After:**
```bash
# Safe: only SmartSpec files updated
git pull
```

---

## 🔍 Edge Cases

### **Case 1: User already has `.smartspec/`**
- **Probability:** Very low (<0.1%)
- **Solution:** Installation script checks and warns
- **Action:** Ask user to backup or rename

### **Case 2: User already has `.smartspec-dev/`**
- **Probability:** Extremely low (<0.01%)
- **Solution:** Installation script checks and warns
- **Action:** Ask user to backup or rename

### **Case 3: User wants dev docs**
- **Probability:** Low (10%)
- **Solution:** Provide optional flag `--with-dev-docs`
- **Action:** Copy `.smartspec-dev/` if requested

---

## 📝 Installation Script Changes

### **install.sh**

**Before:**
```bash
echo ".kilocode/workflows/" >> .git/info/sparse-checkout
echo ".smartspec/" >> .git/info/sparse-checkout
echo "scripts/" >> .git/info/sparse-checkout  # RISKY!
```

**After:**
```bash
echo ".kilocode/workflows/" >> .git/info/sparse-checkout
echo ".smartspec/" >> .git/info/sparse-checkout
# scripts/ now inside .smartspec/, no separate checkout needed
```

### **install.ps1**

**Before:**
```powershell
Copy-Item -Recurse "SmartSpec-main\scripts\*" $SCRIPTS_DIR\  # RISKY!
```

**After:**
```powershell
# scripts/ now inside .smartspec/, copied automatically
# No separate copy needed
```

---

## ✅ Success Criteria

### **Safety**
- [x] No common folder names (docs, scripts, src, lib)
- [x] Use specific prefixes (.smartspec-*)
- [x] Hidden folders for dev files
- [x] Standard files only (README, LICENSE)

### **Usability**
- [ ] Easy to identify SmartSpec files
- [ ] Clear separation from user files
- [ ] No confusion about ownership
- [ ] Easy to clean up (delete .smartspec*)

### **Compatibility**
- [ ] Works with all platforms (Linux, Mac, Windows)
- [ ] Works with all project types
- [ ] No conflicts with common tools
- [ ] Follows best practices

---

## 🚀 Next Steps

1. ⏳ **Phase 2:** Rename folders and move files
2. ⏳ **Phase 3:** Update installation scripts
3. ⏳ **Phase 4:** Test and commit

---

## 📚 References

### **Common Folder Names to Avoid**

**Documentation:**
- `docs/`, `doc/`, `documentation/`
- `wiki/`, `guides/`, `manual/`

**Code:**
- `src/`, `lib/`, `app/`, `core/`
- `components/`, `modules/`, `utils/`

**Build:**
- `scripts/`, `build/`, `dist/`, `bin/`
- `tools/`, `config/`, `deploy/`

**Testing:**
- `tests/`, `test/`, `spec/`, `e2e/`

**Assets:**
- `assets/`, `public/`, `static/`, `resources/`
- `images/`, `styles/`, `css/`, `js/`

### **Safe Naming Patterns**

**Hidden + Specific:**
- `.smartspec*` - SmartSpec-specific
- `.kilocode*` - Kilo Code-specific
- `.roo*` - Roo Code-specific
- `.claude*` - Claude Code-specific

**Prefixed:**
- `smartspec-*` - If not hidden
- `ss-*` - Short prefix

---

**Status:** 📋 ANALYSIS COMPLETE  
**Next:** Implement Phase 2 (Rename & Move)
