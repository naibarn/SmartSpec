# Multi-Platform Installation Design
## Single Source, Easy Install, Auto-Sync

**Date:** 2025-01-04  
**Purpose:** Design installation system for 3 platforms with single source of truth

---

## 🔍 Problem Analysis

### **Current State** ❌

**3 Platforms = 3 Locations:**
```
Project/
├── .kilocode/
│   └── workflows/
│       ├── smartspec_generate_spec.md
│       ├── smartspec_generate_tasks.md
│       └── ... (9 workflows)
│
├── .roo/
│   └── commands/
│       ├── smartspec_generate_spec.md
│       ├── smartspec_generate_tasks.md
│       └── ... (9 workflows)
│
└── .claude/
    └── commands/
        ├── smartspec_generate_spec.md
        ├── smartspec_generate_tasks.md
        └── ... (9 workflows)
```

**Problems:**

1. **❌ Maintenance Nightmare**
   - Update 1 workflow = update 3 files
   - High chance of missing updates
   - Inconsistent versions across platforms

2. **❌ Complex Installation**
   - User must copy to 3 locations
   - Error-prone manual process
   - Hard for beginners

3. **❌ Version Control Issues**
   - 3x files in git (bloat)
   - Merge conflicts 3x more likely
   - Hard to track changes

4. **❌ User Experience**
   - Confusing for users
   - "Which one should I use?"
   - "Did I install all of them?"

---

## 🎯 Requirements

### **Must Have:**
1. ✅ Single source of truth
2. ✅ One-command installation
3. ✅ Support all 3 platforms
4. ✅ Auto-sync on update
5. ✅ Easy for beginners
6. ✅ No manual copying

### **Nice to Have:**
1. ✅ Auto-detect platforms
2. ✅ Selective installation
3. ✅ Uninstall support
4. ✅ Version checking
5. ✅ Update notifications

---

## 💡 Solution Design

### **Architecture Overview**

```
SmartSpec Repository (GitHub)
│
├── .kilocode/
│   └── workflows/          ← SINGLE SOURCE OF TRUTH
│       ├── smartspec_generate_spec.md
│       ├── smartspec_generate_tasks.md
│       └── ... (9 workflows)
│
├── scripts/
│   ├── install.sh          ← Installation script (Unix/Mac)
│   ├── install.ps1         ← Installation script (Windows)
│   ├── sync.sh             ← Sync script (Unix/Mac)
│   ├── sync.ps1            ← Sync script (Windows)
│   └── uninstall.sh        ← Uninstall script
│
└── README.md               ← Installation instructions
```

**User's Project (After Installation):**
```
User's Project/
│
├── .smartspec/
│   ├── config.json         ← SmartSpec config
│   ├── version.txt         ← Installed version
│   └── platforms.json      ← Installed platforms
│
├── .kilocode/
│   └── workflows/          ← Symlink or copy
│       └── smartspec_*.md
│
├── .roo/
│   └── commands/           ← Symlink or copy
│       └── smartspec_*.md
│
└── .claude/
    └── commands/           ← Symlink or copy
        └── smartspec_*.md
```

---

## 🔧 Solution Options

### **Option 1: Symlinks** ✅ **RECOMMENDED**

**Approach:**
- Keep workflows in `.smartspec/workflows/`
- Create symlinks to platform directories
- Single source, multiple access points

**Structure:**
```
User's Project/
│
├── .smartspec/
│   └── workflows/          ← ACTUAL FILES (single source)
│       ├── smartspec_generate_spec.md
│       └── ...
│
├── .kilocode/
│   └── workflows/          ← SYMLINK to .smartspec/workflows/
│
├── .roo/
│   └── commands/           ← SYMLINK to .smartspec/workflows/
│
└── .claude/
    └── commands/           ← SYMLINK to .smartspec/workflows/
```

**Pros:**
- ✅ Single source of truth
- ✅ Auto-sync (changes reflect immediately)
- ✅ No duplication
- ✅ Easy to update

**Cons:**
- ⚠️ Requires symlink support (not all Windows versions)
- ⚠️ May not work on some filesystems

**Compatibility:**
- ✅ Linux: Full support
- ✅ macOS: Full support
- ⚠️ Windows: Requires Developer Mode or Admin (Windows 10+)
- ❌ Windows (old): May not work

---

### **Option 2: Hard Copies with Sync Script** ✅ **FALLBACK**

**Approach:**
- Keep workflows in `.smartspec/workflows/`
- Copy to platform directories
- Run sync script after updates

**Structure:**
```
User's Project/
│
├── .smartspec/
│   ├── workflows/          ← MASTER COPY
│   │   ├── smartspec_generate_spec.md
│   │   └── ...
│   └── sync.sh             ← Sync script
│
├── .kilocode/
│   └── workflows/          ← COPY (synced)
│
├── .roo/
│   └── commands/           ← COPY (synced)
│
└── .claude/
    └── commands/           ← COPY (synced)
```

**Pros:**
- ✅ Works on all platforms
- ✅ No special permissions needed
- ✅ Compatible with all filesystems

**Cons:**
- ⚠️ Requires manual sync (run script)
- ⚠️ Duplication (3x disk space)
- ⚠️ Can get out of sync

**Mitigation:**
- ✅ Git hook to auto-sync on pull
- ✅ Periodic sync check
- ✅ Warning if out of sync

---

### **Option 3: Hybrid (Symlink + Fallback)** ✅ **BEST**

**Approach:**
- Try symlinks first
- Fall back to copies if symlinks fail
- Auto-detect best method

**Installation Flow:**
```
1. Detect OS and capabilities
2. Try to create symlinks
3. If symlinks work:
   - Use symlinks (Option 1)
4. If symlinks fail:
   - Use copies (Option 2)
   - Set up sync script
5. Save method to .smartspec/config.json
```

**Pros:**
- ✅ Best of both worlds
- ✅ Works on all platforms
- ✅ Optimal performance when possible
- ✅ Graceful fallback

**Cons:**
- ⚠️ Slightly more complex
- ⚠️ Need to handle both methods

**Verdict:** ✅ **BEST SOLUTION**

---

## 📦 Installation Script Design

### **install.sh (Unix/Mac/Linux)**

```bash
#!/bin/bash
# SmartSpec Multi-Platform Installer

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SMARTSPEC_REPO="https://github.com/naibarn/SmartSpec.git"
SMARTSPEC_VERSION="v5.0"
SMARTSPEC_DIR=".smartspec"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"

# Platform directories
KILOCODE_DIR=".kilocode/workflows"
ROO_DIR=".roo/commands"
CLAUDE_DIR=".claude/commands"

echo "🚀 SmartSpec Multi-Platform Installer"
echo "======================================"
echo ""

# Check if already installed
if [ -d "$SMARTSPEC_DIR" ]; then
    echo -e "${YELLOW}⚠️  SmartSpec is already installed${NC}"
    read -p "Do you want to reinstall? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
    echo "🗑️  Removing existing installation..."
    rm -rf "$SMARTSPEC_DIR"
fi

# Step 1: Clone or download workflows
echo "📥 Downloading SmartSpec workflows..."
if command -v git &> /dev/null; then
    # Use git sparse checkout (only .kilocode/workflows/)
    mkdir -p "$SMARTSPEC_DIR"
    cd "$SMARTSPEC_DIR"
    git init
    git remote add origin "$SMARTSPEC_REPO"
    git config core.sparseCheckout true
    echo ".kilocode/workflows/" >> .git/info/sparse-checkout
    git pull origin main
    mv .kilocode/workflows ./workflows
    rm -rf .kilocode .git
    cd ..
else
    # Download as zip
    curl -L "$SMARTSPEC_REPO/archive/refs/heads/main.zip" -o smartspec.zip
    unzip -q smartspec.zip
    mkdir -p "$WORKFLOWS_DIR"
    mv SmartSpec-main/.kilocode/workflows/* "$WORKFLOWS_DIR/"
    rm -rf SmartSpec-main smartspec.zip
fi

echo -e "${GREEN}✅ Downloaded workflows${NC}"

# Step 2: Detect platforms
echo ""
echo "🔍 Detecting platforms..."
PLATFORMS=()

if [ -d ".kilocode" ]; then
    PLATFORMS+=("kilocode")
    echo "  ✅ Kilo Code detected"
fi

if [ -d ".roo" ]; then
    PLATFORMS+=("roo")
    echo "  ✅ Roo Code detected"
fi

if [ -d ".claude" ]; then
    PLATFORMS+=("claude")
    echo "  ✅ Claude Code detected"
fi

if [ ${#PLATFORMS[@]} -eq 0 ]; then
    echo -e "${YELLOW}⚠️  No platforms detected${NC}"
    echo ""
    echo "Which platforms do you want to install?"
    echo "  1) Kilo Code"
    echo "  2) Roo Code"
    echo "  3) Claude Code"
    echo "  4) All of the above"
    read -p "Enter choice [1-4]: " choice
    
    case $choice in
        1) PLATFORMS=("kilocode") ;;
        2) PLATFORMS=("roo") ;;
        3) PLATFORMS=("claude") ;;
        4) PLATFORMS=("kilocode" "roo" "claude") ;;
        *) echo "Invalid choice"; exit 1 ;;
    esac
fi

# Step 3: Try symlinks first
echo ""
echo "🔗 Setting up platform integrations..."

USE_SYMLINKS=true

# Test if symlinks work
test_symlink() {
    local test_dir=".smartspec_test"
    mkdir -p "$test_dir"
    if ln -s "$test_dir" "$test_dir/link" 2>/dev/null; then
        rm -rf "$test_dir"
        return 0
    else
        rm -rf "$test_dir"
        return 1
    fi
}

if test_symlink; then
    echo "  ✅ Symlinks supported - using symlinks"
    USE_SYMLINKS=true
else
    echo "  ⚠️  Symlinks not supported - using copies"
    USE_SYMLINKS=false
fi

# Step 4: Install for each platform
for platform in "${PLATFORMS[@]}"; do
    case $platform in
        kilocode)
            TARGET_DIR="$KILOCODE_DIR"
            ;;
        roo)
            TARGET_DIR="$ROO_DIR"
            ;;
        claude)
            TARGET_DIR="$CLAUDE_DIR"
            ;;
    esac
    
    # Create parent directory
    mkdir -p "$(dirname "$TARGET_DIR")"
    
    # Remove existing
    if [ -e "$TARGET_DIR" ]; then
        rm -rf "$TARGET_DIR"
    fi
    
    # Install
    if [ "$USE_SYMLINKS" = true ]; then
        # Create symlink
        ln -s "../../$WORKFLOWS_DIR" "$TARGET_DIR"
        echo "  ✅ $platform: Symlink created"
    else
        # Copy files
        cp -r "$WORKFLOWS_DIR" "$TARGET_DIR"
        echo "  ✅ $platform: Files copied"
    fi
done

# Step 5: Save configuration
echo ""
echo "💾 Saving configuration..."

cat > "$SMARTSPEC_DIR/config.json" <<EOF
{
  "version": "$SMARTSPEC_VERSION",
  "installed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "platforms": $(printf '%s\n' "${PLATFORMS[@]}" | jq -R . | jq -s .),
  "use_symlinks": $USE_SYMLINKS,
  "repo": "$SMARTSPEC_REPO"
}
EOF

echo "$SMARTSPEC_VERSION" > "$SMARTSPEC_DIR/version.txt"

# Step 6: Create sync script (if using copies)
if [ "$USE_SYMLINKS" = false ]; then
    cat > "$SMARTSPEC_DIR/sync.sh" <<'SYNCEOF'
#!/bin/bash
# SmartSpec Sync Script

SMARTSPEC_DIR=".smartspec"
WORKFLOWS_DIR="$SMARTSPEC_DIR/workflows"

# Read config
PLATFORMS=$(jq -r '.platforms[]' "$SMARTSPEC_DIR/config.json")

echo "🔄 Syncing SmartSpec workflows..."

for platform in $PLATFORMS; do
    case $platform in
        kilocode) TARGET_DIR=".kilocode/workflows" ;;
        roo) TARGET_DIR=".roo/commands" ;;
        claude) TARGET_DIR=".claude/commands" ;;
    esac
    
    # Sync
    rsync -a --delete "$WORKFLOWS_DIR/" "$TARGET_DIR/"
    echo "  ✅ $platform synced"
done

echo "✅ Sync complete"
SYNCEOF
    
    chmod +x "$SMARTSPEC_DIR/sync.sh"
    
    # Create git hook
    if [ -d ".git" ]; then
        mkdir -p ".git/hooks"
        cat > ".git/hooks/post-merge" <<'HOOKEOF'
#!/bin/bash
# Auto-sync SmartSpec after git pull

if [ -f ".smartspec/sync.sh" ]; then
    echo "🔄 Auto-syncing SmartSpec..."
    .smartspec/sync.sh
fi
HOOKEOF
        chmod +x ".git/hooks/post-merge"
        echo "  ✅ Git hook installed (auto-sync on pull)"
    fi
fi

# Step 7: Success message
echo ""
echo -e "${GREEN}✅ SmartSpec installed successfully!${NC}"
echo ""
echo "📍 Installation details:"
echo "  - Version: $SMARTSPEC_VERSION"
echo "  - Location: $SMARTSPEC_DIR"
echo "  - Method: $([ "$USE_SYMLINKS" = true ] && echo "Symlinks" || echo "Copies")"
echo "  - Platforms: ${PLATFORMS[*]}"
echo ""

if [ "$USE_SYMLINKS" = false ]; then
    echo "📝 Note: You're using copies (not symlinks)"
    echo "   Run '.smartspec/sync.sh' after updating workflows"
    echo ""
fi

echo "🎉 You can now use SmartSpec workflows in:"
for platform in "${PLATFORMS[@]}"; do
    case $platform in
        kilocode) echo "  - Kilo Code: /smartspec_*" ;;
        roo) echo "  - Roo Code: /smartspec_*" ;;
        claude) echo "  - Claude Code: /smartspec_*" ;;
    esac
done

echo ""
echo "📚 Documentation: https://github.com/naibarn/SmartSpec"
```

---

### **install.ps1 (Windows)**

```powershell
# SmartSpec Multi-Platform Installer (Windows)

$ErrorActionPreference = "Stop"

# Configuration
$SMARTSPEC_REPO = "https://github.com/naibarn/SmartSpec.git"
$SMARTSPEC_VERSION = "v5.0"
$SMARTSPEC_DIR = ".smartspec"
$WORKFLOWS_DIR = "$SMARTSPEC_DIR\workflows"

Write-Host "🚀 SmartSpec Multi-Platform Installer" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if already installed
if (Test-Path $SMARTSPEC_DIR) {
    Write-Host "⚠️  SmartSpec is already installed" -ForegroundColor Yellow
    $reply = Read-Host "Do you want to reinstall? [y/N]"
    if ($reply -notmatch "^[Yy]$") {
        exit 0
    }
    Write-Host "🗑️  Removing existing installation..."
    Remove-Item -Recurse -Force $SMARTSPEC_DIR
}

# Step 1: Download workflows
Write-Host "📥 Downloading SmartSpec workflows..."

if (Get-Command git -ErrorAction SilentlyContinue) {
    # Use git sparse checkout
    New-Item -ItemType Directory -Force -Path $SMARTSPEC_DIR | Out-Null
    Set-Location $SMARTSPEC_DIR
    git init
    git remote add origin $SMARTSPEC_REPO
    git config core.sparseCheckout true
    ".kilocode/workflows/" | Out-File -Encoding ASCII .git\info\sparse-checkout
    git pull origin main
    Move-Item .kilocode\workflows .\workflows
    Remove-Item -Recurse -Force .kilocode, .git
    Set-Location ..
} else {
    # Download as zip
    $zipPath = "smartspec.zip"
    Invoke-WebRequest -Uri "$SMARTSPEC_REPO/archive/refs/heads/main.zip" -OutFile $zipPath
    Expand-Archive -Path $zipPath -DestinationPath .
    New-Item -ItemType Directory -Force -Path $WORKFLOWS_DIR | Out-Null
    Copy-Item -Recurse "SmartSpec-main\.kilocode\workflows\*" $WORKFLOWS_DIR\
    Remove-Item -Recurse -Force SmartSpec-main, $zipPath
}

Write-Host "✅ Downloaded workflows" -ForegroundColor Green

# Step 2: Detect platforms
Write-Host ""
Write-Host "🔍 Detecting platforms..."
$PLATFORMS = @()

if (Test-Path ".kilocode") {
    $PLATFORMS += "kilocode"
    Write-Host "  ✅ Kilo Code detected" -ForegroundColor Green
}

if (Test-Path ".roo") {
    $PLATFORMS += "roo"
    Write-Host "  ✅ Roo Code detected" -ForegroundColor Green
}

if (Test-Path ".claude") {
    $PLATFORMS += "claude"
    Write-Host "  ✅ Claude Code detected" -ForegroundColor Green
}

if ($PLATFORMS.Count -eq 0) {
    Write-Host "⚠️  No platforms detected" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Which platforms do you want to install?"
    Write-Host "  1) Kilo Code"
    Write-Host "  2) Roo Code"
    Write-Host "  3) Claude Code"
    Write-Host "  4) All of the above"
    $choice = Read-Host "Enter choice [1-4]"
    
    switch ($choice) {
        1 { $PLATFORMS = @("kilocode") }
        2 { $PLATFORMS = @("roo") }
        3 { $PLATFORMS = @("claude") }
        4 { $PLATFORMS = @("kilocode", "roo", "claude") }
        default { Write-Host "Invalid choice"; exit 1 }
    }
}

# Step 3: Try symlinks first (Windows 10+ with Developer Mode)
Write-Host ""
Write-Host "🔗 Setting up platform integrations..."

$USE_SYMLINKS = $false

# Test if symlinks work
try {
    $testDir = ".smartspec_test"
    New-Item -ItemType Directory -Force -Path $testDir | Out-Null
    New-Item -ItemType SymbolicLink -Path "$testDir\link" -Target $testDir -ErrorAction Stop | Out-Null
    Remove-Item -Recurse -Force $testDir
    $USE_SYMLINKS = $true
    Write-Host "  ✅ Symlinks supported - using symlinks" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Symlinks not supported - using copies" -ForegroundColor Yellow
    Write-Host "     (Enable Developer Mode in Windows Settings for symlinks)" -ForegroundColor Gray
    $USE_SYMLINKS = $false
}

# Step 4: Install for each platform
foreach ($platform in $PLATFORMS) {
    switch ($platform) {
        "kilocode" { $TARGET_DIR = ".kilocode\workflows" }
        "roo" { $TARGET_DIR = ".roo\commands" }
        "claude" { $TARGET_DIR = ".claude\commands" }
    }
    
    # Create parent directory
    $parentDir = Split-Path -Parent $TARGET_DIR
    New-Item -ItemType Directory -Force -Path $parentDir | Out-Null
    
    # Remove existing
    if (Test-Path $TARGET_DIR) {
        Remove-Item -Recurse -Force $TARGET_DIR
    }
    
    # Install
    if ($USE_SYMLINKS) {
        # Create symlink
        $sourcePath = (Resolve-Path $WORKFLOWS_DIR).Path
        New-Item -ItemType SymbolicLink -Path $TARGET_DIR -Target $sourcePath | Out-Null
        Write-Host "  ✅ $platform`: Symlink created" -ForegroundColor Green
    } else {
        # Copy files
        Copy-Item -Recurse $WORKFLOWS_DIR $TARGET_DIR
        Write-Host "  ✅ $platform`: Files copied" -ForegroundColor Green
    }
}

# Step 5: Save configuration
Write-Host ""
Write-Host "💾 Saving configuration..."

$config = @{
    version = $SMARTSPEC_VERSION
    installed_at = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    platforms = $PLATFORMS
    use_symlinks = $USE_SYMLINKS
    repo = $SMARTSPEC_REPO
}

$config | ConvertTo-Json | Out-File -Encoding UTF8 "$SMARTSPEC_DIR\config.json"
$SMARTSPEC_VERSION | Out-File -Encoding UTF8 "$SMARTSPEC_DIR\version.txt"

# Step 6: Create sync script (if using copies)
if (-not $USE_SYMLINKS) {
    $syncScript = @'
# SmartSpec Sync Script (Windows)

$SMARTSPEC_DIR = ".smartspec"
$WORKFLOWS_DIR = "$SMARTSPEC_DIR\workflows"

# Read config
$config = Get-Content "$SMARTSPEC_DIR\config.json" | ConvertFrom-Json
$PLATFORMS = $config.platforms

Write-Host "🔄 Syncing SmartSpec workflows..."

foreach ($platform in $PLATFORMS) {
    switch ($platform) {
        "kilocode" { $TARGET_DIR = ".kilocode\workflows" }
        "roo" { $TARGET_DIR = ".roo\commands" }
        "claude" { $TARGET_DIR = ".claude\commands" }
    }
    
    # Sync
    Remove-Item -Recurse -Force $TARGET_DIR -ErrorAction SilentlyContinue
    Copy-Item -Recurse $WORKFLOWS_DIR $TARGET_DIR
    Write-Host "  ✅ $platform synced" -ForegroundColor Green
}

Write-Host "✅ Sync complete" -ForegroundColor Green
'@
    
    $syncScript | Out-File -Encoding UTF8 "$SMARTSPEC_DIR\sync.ps1"
    
    Write-Host "  ✅ Sync script created" -ForegroundColor Green
}

# Step 7: Success message
Write-Host ""
Write-Host "✅ SmartSpec installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Installation details:"
Write-Host "  - Version: $SMARTSPEC_VERSION"
Write-Host "  - Location: $SMARTSPEC_DIR"
Write-Host "  - Method: $(if ($USE_SYMLINKS) { 'Symlinks' } else { 'Copies' })"
Write-Host "  - Platforms: $($PLATFORMS -join ', ')"
Write-Host ""

if (-not $USE_SYMLINKS) {
    Write-Host "📝 Note: You're using copies (not symlinks)"
    Write-Host "   Run '.smartspec\sync.ps1' after updating workflows"
    Write-Host ""
}

Write-Host "🎉 You can now use SmartSpec workflows in:"
foreach ($platform in $PLATFORMS) {
    switch ($platform) {
        "kilocode" { Write-Host "  - Kilo Code: /smartspec_*" }
        "roo" { Write-Host "  - Roo Code: /smartspec_*" }
        "claude" { Write-Host "  - Claude Code: /smartspec_*" }
    }
}

Write-Host ""
Write-Host "📚 Documentation: https://github.com/naibarn/SmartSpec"
```

---

## 📚 Usage Instructions

### **Installation**

**Unix/Mac/Linux:**
```bash
# Navigate to your project
cd /path/to/your/project

# Download and run installer
curl -fsSL https://raw.githubusercontent.com/naibarn/SmartSpec/main/scripts/install.sh | bash

# Or download first, then run
curl -O https://raw.githubusercontent.com/naibarn/SmartSpec/main/scripts/install.sh
chmod +x install.sh
./install.sh
```

**Windows (PowerShell):**
```powershell
# Navigate to your project
cd C:\path\to\your\project

# Download and run installer
iwr -useb https://raw.githubusercontent.com/naibarn/SmartSpec/main/scripts/install.ps1 | iex

# Or download first, then run
iwr -OutFile install.ps1 https://raw.githubusercontent.com/naibarn/SmartSpec/main/scripts/install.ps1
.\install.ps1
```

---

### **Updating**

**If using symlinks (automatic):**
```bash
# Just update the workflows
cd .smartspec/workflows
git pull

# Changes reflect immediately in all platforms
```

**If using copies (manual sync):**
```bash
# Update workflows
cd .smartspec/workflows
git pull

# Sync to platforms
cd ../..
.smartspec/sync.sh      # Unix/Mac/Linux
.smartspec/sync.ps1     # Windows
```

---

### **Uninstalling**

```bash
# Remove SmartSpec from all platforms
rm -rf .smartspec
rm -rf .kilocode/workflows/smartspec_*
rm -rf .roo/commands/smartspec_*
rm -rf .claude/commands/smartspec_*
```

---

## ✅ Benefits

### **For Users:**
1. ✅ **One-command install** - curl | bash
2. ✅ **Auto-detect platforms** - no manual selection
3. ✅ **Works everywhere** - Linux, Mac, Windows
4. ✅ **Auto-sync** - symlinks or git hooks
5. ✅ **Easy updates** - git pull + sync
6. ✅ **Clean uninstall** - rm -rf .smartspec

### **For Maintainers:**
1. ✅ **Single source** - only update .kilocode/workflows/
2. ✅ **No duplication** - workflows stored once
3. ✅ **Version control** - track changes easily
4. ✅ **Consistent** - all platforms get same version

### **For System:**
1. ✅ **Efficient** - symlinks use no extra space
2. ✅ **Fast** - no copying needed
3. ✅ **Reliable** - fallback to copies if needed
4. ✅ **Compatible** - works on all platforms

---

## 📊 Comparison

### **Before (Manual Installation)**

**Steps:**
1. Clone SmartSpec repo
2. Copy workflows to .kilocode/workflows/
3. Copy workflows to .roo/commands/
4. Copy workflows to .claude/commands/
5. Remember to update all 3 when upgrading

**Problems:**
- ❌ 5 steps (complex)
- ❌ Error-prone
- ❌ Easy to forget platforms
- ❌ Hard to update

---

### **After (Automated Installation)**

**Steps:**
1. Run: `curl -fsSL https://...install.sh | bash`

**Benefits:**
- ✅ 1 step (simple)
- ✅ Automatic
- ✅ All platforms installed
- ✅ Easy to update

---

## 🎯 Implementation Plan

### **Phase 1: Core Scripts** (2 hours)
1. ✅ Create install.sh
2. ✅ Create install.ps1
3. ✅ Create sync.sh
4. ✅ Create sync.ps1
5. ✅ Test on Linux, Mac, Windows

### **Phase 2: Documentation** (1 hour)
1. ✅ Update README with installation instructions
2. ✅ Add troubleshooting guide
3. ✅ Add examples

### **Phase 3: Testing** (1 hour)
1. ✅ Test on different platforms
2. ✅ Test with/without git
3. ✅ Test symlinks vs copies
4. ✅ Test updates

### **Phase 4: Deployment** (0.5 hour)
1. ✅ Commit scripts to repo
2. ✅ Update README
3. ✅ Announce to users

**Total: 4.5 hours**

---

## 🚀 Next Steps

1. ⏳ Review this design
2. ⏳ Approve approach
3. ⏳ Implement scripts
4. ⏳ Test thoroughly
5. ⏳ Deploy to GitHub
6. ⏳ Update documentation

---

**Status:** 📋 DESIGN COMPLETE  
**Recommendation:** ✅ Implement hybrid approach (symlinks + fallback)  
**Estimated Time:** 4.5 hours
