---
description: SmartSpec v5.1.2 - FIXED: Header Metadata, Clean Templates, Section Separators - Back to v4.0 Readability
version: 5.1.2
changes: |
  v5.1.2 (Latest - CRITICAL FIXES):
  - ✅ FIXED: Header metadata NOW ALWAYS preserved (Status, Version, Author, Created, Last Updated)
  - ✅ FIXED: NO visible meta tags in generated specs (clean like v4.0)
  - ✅ FIXED: Section separators (---) restored between all major sections
  - ✅ FIXED: Technology Stack back to simple, readable format
  - ✅ Added Step 1.3: Header Metadata Management with validation
  - ✅ Added Step 13.2: Clean Section Templates (NO meta tags clutter)
  - ✅ Updated Step 13.3: Assembly with separators and clean format
  - ✅ Meta tags moved to internal registry only (not in spec.md)
  
  v5.1.1:
  - Added Step 1.2: Output Directory Initialization with validation
  - Implemented --output-dir flag with full path validation
  - Organized backups per SPEC (e.g., .smartspec/backups/spec-004/)
  - Organized reports per SPEC
  - Enhanced final report with explicit file locations
  
  v5.1.0:
  - Added content preservation, quality verification, merge strategy
  - Smart merging for STRIDE, Performance, API, Data models
---

## User Input

```text
$ARGUMENTS
```

**Patterns:**
- NEW: "Create SPEC for payment system..."
- EDIT: `specs/feature/spec-004/spec.md`
- With profile: `--profile=financial`
- With mode: `--mode=compact`
- With flags: `--no-di --security=stride-basic`

---

## 0. Parse Command-Line Flags

### 0.1 Profile Selection

```
--profile=<type>

Options:
  basic           - Minimal SPEC (Overview, Architecture, API/Data)
  backend-service - Standard backend (DI, testing, monitoring)
  financial       - Full security + performance (STRIDE, SLA, metrics)
  full            - All sections (default - v4.0 compatibility)
```

### 0.2 Mode Selection

```
--mode=<type>

Options:
  standard - Full SPEC with all details (default)
  compact  - Condensed 5-section SPEC for simple projects
```

### 0.3 Security Level

```
--security=<level>

Options:
  none         - No security section
  basic        - Basic security considerations
  stride-basic - STRIDE table (5-10 lines, key threats only)
  stride-full  - Complete STRIDE model (100+ lines, detailed)
  auto         - Auto-detect based on profile (default)
```

### 0.4 DI Pattern Control

```
--di=<level>

Options:
  full    - Complete DI pattern documentation (default for backend)
  minimal - Brief DI pattern mention
  none    - No DI pattern section
  auto    - Auto-detect based on project type (default)

Shorthand:
  --no-di  - Same as --di=none
```

### 0.5 Performance Requirements Control

```
--performance=<level>

Options:
  full    - Complete performance requirements
  basic   - Key metrics only (P99, TPS, uptime)
  none    - No performance section
  auto    - Auto-detect based on profile/domain (default)
```

### 0.6 Force Update Critical Sections

```
--force-update=<sections>

Options:
  all                          - Allow update all critical sections
  stride,config,di            - Allow specific sections
  none                        - Preserve all critical sections (default)
```

### 0.7 Content Preservation Strategy (NEW v5.1)

```
--preserve-strategy=<strategy>

Options:
  conservative - Preserve all existing detailed content, only add missing sections (default)
  balanced     - Merge existing with new, prefer existing for critical sections
  aggressive   - Regenerate all, only preserve critical sections marked with meta tags
  
--preserve-sections=<sections>

Specify sections to always preserve (comma-separated):
  --preserve-sections=stride,performance,di,api-spec,data-model
```

### 0.8 Output Organization

```
--no-backup        - Don't create backup files
--no-report        - Don't generate reports
--no-diff          - Don't generate diff report (NEW v5.1)
--output-dir=<dir> - Custom output directory (default: .smartspec/)
```

### 0.9 Validation

```
--validate-consistency  - Check consistency between sections
--validate-quality      - Check content quality (NEW v5.1)
--no-validation        - Skip validation checks
```

### 0.10 Domain Hints

```
--domain=<type>

Options:
  healthcare - Real-time + privacy critical
  iot        - High throughput, telemetry
  logistics  - High SLA requirements
  ai         - Latency sensitive
  fintech    - Security + performance critical
  saas       - Scalability focused
  internal   - Lower requirements
```

---

## 1. Load SmartSpec Context

Read configuration in priority order:
1. `.smartspec/smartspec.config.json` (if exists - organization-wide)
2. `SPEC_INDEX.json` (if exists - for dependency resolution)
3. Built-in defaults

Parse flags from $ARGUMENTS and merge with config.

### 1.1 Load or Create SPEC_INDEX.json

**Step 1: Check if SPEC_INDEX.json exists**

Check for `SPEC_INDEX.json`:
```bash
test -f SPEC_INDEX.json && echo "EXISTS" || echo "NOT_EXISTS"
```

**Step 2: If NOT exists, create it (Auto-Creation)**

If NOT_EXISTS:
```
1. Create SPEC_INDEX.json with initial structure (in project root):
   {
     "version": "5.1",
     "created": "<current_timestamp>",
     "last_updated": "<current_timestamp>",
     "specs": [],
     "metadata": {
       "total_specs": 0,
       "by_status": {
         "draft": 0,
         "active": 0,
         "deprecated": 0,
         "placeholder": 0
       },
       "by_repo": {},
       "validation": {
         "last_validated": "<current_timestamp>",
         "status": "valid",
         "errors": [],
         "warnings": [],
         "health_score": 100
       }
     }
   }

2. Log: "✅ Created SPEC_INDEX.json in project root"
```

**Step 3: Load SPEC_INDEX.json into memory**

If EXISTS (or just created):
- Read `SPEC_INDEX.json`
- Parse JSON structure
- Store in SPEC_REGISTRY for lookup

---

## 1.2 Output Directory Initialization (NEW v5.1)

**Purpose:** Validate and initialize output directory structure based on `--output-dir` flag

### 1.2.1 Resolve Output Directory

```typescript
// Get output directory from flags or use default
const OUTPUT_DIR = FLAGS.output_dir || '.smartspec';

console.log(`📁 Output directory: ${OUTPUT_DIR}`);
```

### 1.2.2 Validate Output Directory Path

```typescript
function validateOutputPath(dirPath: string): { valid: boolean; error?: string } {
  // Check for invalid characters
  const invalidChars = /[<>:"|?*\x00-\x1F]/;
  if (invalidChars.test(dirPath)) {
    return {
      valid: false,
      error: `Invalid characters in path: ${dirPath}`
    };
  }
  
  // Check for path traversal attempts
  const normalized = path.normalize(dirPath);
  if (normalized.includes('..')) {
    return {
      valid: false,
      error: `Path traversal not allowed: ${dirPath}`
    };
  }
  
  // Check path length (Windows: 260 chars, Unix: 4096 chars)
  const maxLength = process.platform === 'win32' ? 260 : 4096;
  if (path.resolve(dirPath).length > maxLength) {
    return {
      valid: false,
      error: `Path too long (max ${maxLength} chars): ${dirPath}`
    };
  }
  
  // Check if parent directory is writable (if exists)
  const parentDir = path.dirname(path.resolve(dirPath));
  if (fs.existsSync(parentDir)) {
    try {
      fs.accessSync(parentDir, fs.constants.W_OK);
    } catch (error) {
      return {
        valid: false,
        error: `Parent directory not writable: ${parentDir}`
      };
    }
  }
  
  return { valid: true };
}

// Validate the output directory
const validation = validateOutputPath(OUTPUT_DIR);
if (!validation.valid) {
  console.error(`❌ Invalid output directory: ${validation.error}`);
  throw new Error(validation.error);
}

console.log(`✅ Output directory validated: ${OUTPUT_DIR}`);
```

### 1.2.3 Extract SPEC ID from Path or Arguments

```typescript
function extractSpecId(args: string, specPath?: string): string {
  // Method 1: Extract from spec path (EDIT mode)
  // Example: specs/feature/spec-004-financial-system/spec.md -> spec-004
  if (specPath) {
    const match = specPath.match(/spec-([a-zA-Z0-9-]+)/);
    if (match) {
      return match[0]; // e.g., "spec-004" or "spec-core-001"
    }
  }
  
  // Method 2: Extract from arguments (NEW mode)
  // Example: "Create spec-005 for promo system" -> spec-005
  const argMatch = args.match(/spec-([a-zA-Z0-9-]+)/i);
  if (argMatch) {
    return argMatch[0].toLowerCase();
  }
  
  // Method 3: Generate from title
  // Example: "payment system" -> spec-payment-system
  const titleMatch = args.match(/(?:for|create|new)\s+([a-zA-Z0-9\s-]+)/i);
  if (titleMatch) {
    const title = titleMatch[1].trim()
      .toLowerCase()
      .replace(/\s+/g, '-')
      .replace(/[^a-z0-9-]/g, '');
    return `spec-${title}`;
  }
  
  // Fallback: use timestamp
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
  return `spec-${timestamp}`;
}

// Extract SPEC ID
const SPEC_ID = extractSpecId($ARGUMENTS, existingSpecPath);
console.log(`🆔 SPEC ID: ${SPEC_ID}`);
```

### 1.2.4 Create Output Directory Structure

```typescript
function initializeOutputDirectory(baseDir: string, specId: string): void {
  console.log(`\n📁 Initializing output directory structure...`);
  
  // Define directory structure
  const directories = {
    root: baseDir,
    backups: path.join(baseDir, 'backups'),
    backupsSpec: path.join(baseDir, 'backups', specId), // 👈 Separate folder per spec
    reports: path.join(baseDir, 'reports'),
    reportsSpec: path.join(baseDir, 'reports', specId), // 👈 Separate folder per spec
    registry: path.join(baseDir, 'registry'),
    logs: path.join(baseDir, 'logs')
  };
  
  // Create all directories
  for (const [name, dirPath] of Object.entries(directories)) {
    try {
      if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
        console.log(`  ✅ Created: ${dirPath}`);
      } else {
        console.log(`  📂 Exists: ${dirPath}`);
      }
    } catch (error) {
      console.error(`  ❌ Failed to create ${dirPath}: ${error.message}`);
      throw new Error(`Cannot create directory: ${dirPath}`);
    }
  }
  
  console.log(`✅ Output directory structure initialized`);
  
  // Store paths for later use
  global.OUTPUT_PATHS = directories;
}

// Initialize output directory
initializeOutputDirectory(OUTPUT_DIR, SPEC_ID);
```

### 1.2.5 Verify Write Permissions

```typescript
function verifyWritePermissions(paths: typeof OUTPUT_PATHS): void {
  console.log(`\n🔐 Verifying write permissions...`);
  
  const testFile = path.join(paths.root, '.write-test');
  
  try {
    // Try to write a test file
    fs.writeFileSync(testFile, 'test', 'utf-8');
    fs.unlinkSync(testFile);
    console.log(`✅ Write permissions verified`);
  } catch (error) {
    console.error(`❌ No write permission to ${paths.root}`);
    throw new Error(`Cannot write to output directory: ${paths.root}`);
  }
}

// Verify permissions
verifyWritePermissions(OUTPUT_PATHS);
```

### 1.2.6 Summary

```typescript
console.log(`\n📊 Output Directory Configuration:`);
console.log(`  Root: ${OUTPUT_PATHS.root}`);
console.log(`  Backups (this SPEC): ${OUTPUT_PATHS.backupsSpec}`);
console.log(`  Reports (this SPEC): ${OUTPUT_PATHS.reportsSpec}`);
console.log(`  Registry: ${OUTPUT_PATHS.registry}`);
console.log(`  Logs: ${OUTPUT_PATHS.logs}`);
```

**Output Paths Structure:**
```
<OUTPUT_DIR>/
├── backups/
│   ├── spec-004/              👈 Backups for spec-004 only
│   │   ├── spec.backup-20251206-143059.md
│   │   └── spec.backup-20251206-150231.md
│   ├── spec-005/              👈 Backups for spec-005 only
│   │   └── spec.backup-20251206-153012.md
│   └── spec-core-001/         👈 Backups for spec-core-001 only
│       └── spec.backup-20251205-120000.md
├── reports/
│   ├── spec-004/              👈 Reports for spec-004 only
│   │   ├── generation-report-20251206.md
│   │   └── diff-report-20251206.md
│   ├── spec-005/              👈 Reports for spec-005 only
│   │   └── generation-report-20251206.md
│   └── spec-core-001/
│       └── generation-report-20251205.md
├── registry/
│   └── critical-sections-registry.json
└── logs/
    └── smartspec.log
```

---

## 1.3 Header Metadata Management (CRITICAL - NEW v5.1.1)

**Purpose:** Ensure SPEC header metadata is always preserved and properly formatted

### 1.3.1 Header Metadata Structure

**MANDATORY Header Format:**
```markdown
# SPEC-{ID}: {Title}

**Status:** {DRAFT|ACTIVE|DEPRECATED}
**Version:** {X.Y.Z}
**Author:** {Author Name}
**Created:** {YYYY-MM-DD}
**Last Updated:** {YYYY-MM-DD}

**Update Reason:** {Brief description of changes}

---
```

**Example:**
```markdown
# SPEC-005: Promo System

**Status:** DRAFT
**Version:** 4.0.0
**Author:** SmartSpec Architect v4.0
**Created:** 2025-01-15
**Last Updated:** 2025-12-03

**Update Reason:** Updated to SmartSpec v4.0 format with enhanced structure and critical section preservation

---
```

### 1.3.2 Extract Header Metadata from Existing SPEC (EDIT Mode)

```typescript
interface HeaderMetadata {
  specId: string;
  title: string;
  status: 'DRAFT' | 'ACTIVE' | 'DEPRECATED';
  version: string;
  author: string;
  created: string;
  lastUpdated: string;
  updateReason: string;
}

function extractHeaderMetadata(existingSpec: string): HeaderMetadata | null {
  if (!existingSpec) return null;
  
  const lines = existingSpec.split('\n');
  const metadata: Partial<HeaderMetadata> = {};
  
  // Extract title and ID
  const titleMatch = existingSpec.match(/^#\s+(SPEC-[^:]+):\s+(.+)$/m);
  if (titleMatch) {
    metadata.specId = titleMatch[1];
    metadata.title = titleMatch[2];
  }
  
  // Extract status
  const statusMatch = existingSpec.match(/\*\*Status:\*\*\s+(\w+)/);
  if (statusMatch) {
    metadata.status = statusMatch[1] as HeaderMetadata['status'];
  }
  
  // Extract version
  const versionMatch = existingSpec.match(/\*\*Version:\*\*\s+([\d.]+)/);
  if (versionMatch) {
    metadata.version = versionMatch[1];
  }
  
  // Extract author
  const authorMatch = existingSpec.match(/\*\*Author:\*\*\s+(.+)$/m);
  if (authorMatch) {
    metadata.author = authorMatch[1];
  }
  
  // Extract created date
  const createdMatch = existingSpec.match(/\*\*Created:\*\*\s+([\d-]+)/);
  if (createdMatch) {
    metadata.created = createdMatch[1];
  }
  
  // Extract last updated date
  const updatedMatch = existingSpec.match(/\*\*Last Updated:\*\*\s+([\d-]+)/);
  if (updatedMatch) {
    metadata.lastUpdated = updatedMatch[1];
  }
  
  // Extract update reason
  const reasonMatch = existingSpec.match(/\*\*Update Reason:\*\*\s+(.+?)(?:\n\n|---)/s);
  if (reasonMatch) {
    metadata.updateReason = reasonMatch[1].trim();
  }
  
  return metadata as HeaderMetadata;
}

// Extract metadata if in EDIT mode
let EXISTING_METADATA: HeaderMetadata | null = null;
if (MODE === 'EDIT' && existingSpec) {
  EXISTING_METADATA = extractHeaderMetadata(existingSpec);
  console.log('\n📋 Extracted Header Metadata:');
  console.log(`  SPEC ID: ${EXISTING_METADATA?.specId}`);
  console.log(`  Title: ${EXISTING_METADATA?.title}`);
  console.log(`  Status: ${EXISTING_METADATA?.status}`);
  console.log(`  Version: ${EXISTING_METADATA?.version}`);
  console.log(`  Created: ${EXISTING_METADATA?.created}`);
}
```

### 1.3.3 Generate Header Metadata (NEW Mode or Missing)

```typescript
function generateHeaderMetadata(
  specId: string,
  title: string,
  existingMetadata?: HeaderMetadata | null
): HeaderMetadata {
  const now = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
  
  if (existingMetadata) {
    // EDIT mode - preserve and update
    return {
      specId: existingMetadata.specId,
      title: existingMetadata.title,
      status: existingMetadata.status,
      version: incrementVersion(existingMetadata.version), // e.g., 4.0.0 -> 4.1.0
      author: `SmartSpec Architect v${WORKFLOW_VERSION}`, // Update to current workflow version
      created: existingMetadata.created, // NEVER change
      lastUpdated: now, // Always update
      updateReason: `Updated to SmartSpec v${WORKFLOW_VERSION} format with enhanced features`
    };
  } else {
    // NEW mode - create fresh
    return {
      specId,
      title,
      status: 'DRAFT',
      version: '1.0.0',
      author: `SmartSpec Architect v${WORKFLOW_VERSION}`,
      created: now,
      lastUpdated: now,
      updateReason: 'Initial creation'
    };
  }
}

function incrementVersion(version: string): string {
  const parts = version.split('.').map(Number);
  parts[1]++; // Increment minor version (X.Y.Z -> X.(Y+1).0)
  parts[2] = 0; // Reset patch version
  return parts.join('.');
}

// Generate metadata
const HEADER_METADATA = generateHeaderMetadata(
  SPEC_ID,
  SPEC_TITLE,
  EXISTING_METADATA
);

console.log('\n📋 Header Metadata:');
console.log(`  SPEC ID: ${HEADER_METADATA.specId}`);
console.log(`  Title: ${HEADER_METADATA.title}`);
console.log(`  Status: ${HEADER_METADATA.status}`);
console.log(`  Version: ${HEADER_METADATA.version}`);
console.log(`  Author: ${HEADER_METADATA.author}`);
console.log(`  Created: ${HEADER_METADATA.created}`);
console.log(`  Last Updated: ${HEADER_METADATA.lastUpdated}`);
```

### 1.3.4 Format Header Section

```typescript
function formatHeader(metadata: HeaderMetadata): string {
  return `# ${metadata.specId}: ${metadata.title}

**Status:** ${metadata.status}
**Version:** ${metadata.version}
**Author:** ${metadata.author}
**Created:** ${metadata.created}
**Last Updated:** ${metadata.lastUpdated}

**Update Reason:** ${metadata.updateReason}

---
`;
}

// Store formatted header for later use
const FORMATTED_HEADER = formatHeader(HEADER_METADATA);
```

### 1.3.5 Validation

```typescript
function validateHeaderMetadata(metadata: HeaderMetadata): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  
  // Validate SPEC ID format
  if (!/^SPEC-[a-zA-Z0-9-]+$/.test(metadata.specId)) {
    errors.push(`Invalid SPEC ID format: ${metadata.specId}`);
  }
  
  // Validate status
  if (!['DRAFT', 'ACTIVE', 'DEPRECATED'].includes(metadata.status)) {
    errors.push(`Invalid status: ${metadata.status}`);
  }
  
  // Validate version format (X.Y.Z)
  if (!/^\d+\.\d+\.\d+$/.test(metadata.version)) {
    errors.push(`Invalid version format: ${metadata.version}`);
  }
  
  // Validate dates (YYYY-MM-DD)
  const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
  if (!dateRegex.test(metadata.created)) {
    errors.push(`Invalid created date: ${metadata.created}`);
  }
  if (!dateRegex.test(metadata.lastUpdated)) {
    errors.push(`Invalid last updated date: ${metadata.lastUpdated}`);
  }
  
  // Validate created <= lastUpdated
  if (new Date(metadata.created) > new Date(metadata.lastUpdated)) {
    errors.push('Created date cannot be after last updated date');
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}

// Validate
const validation = validateHeaderMetadata(HEADER_METADATA);
if (!validation.valid) {
  console.error('❌ Header metadata validation failed:');
  validation.errors.forEach(err => console.error(`  - ${err}`));
  throw new Error('Invalid header metadata');
}

console.log('✅ Header metadata validated');
```

---

## 2. Determine SPEC Structure (Profile-Based)

### 2.1 Profile: basic

**Sections:**
1. Header (minimal)
2. Overview (Purpose, Scope, Features)
3. Architecture Summary (high-level only)
4. API Specification OR Data Model (choose one)
5. Acceptance Criteria

**Excludes:**
- When to Use
- Detailed Implementation Guide
- Testing Strategy
- Monitoring
- Security (unless --security specified)
- Performance Requirements
- DI Pattern

---

### 2.2 Profile: backend-service

**Sections:**
1. Header
2. Technology Stack
3. Dependency Injection Pattern (if --di≠none)
4. Overview
5. When to Use
6. Architecture
7. Implementation Guide (core steps)
8. Testing Requirements
9. Monitoring (basic metrics)
10. Examples

**Includes if detected:**
- Configuration Schema (if config mentioned)
- API Documentation (if REST/GraphQL)
- Database Schema (if DB mentioned)

---

### 2.3 Profile: financial

**Sections (Full Critical System):**
1. Header
2. Technology Stack
3. Dependency Injection Pattern (MANDATORY)
4. Overview
5. When to Use / When NOT to Use
6. Architecture (detailed)
7. Business Rules & Logic
8. Data Model & Schema
9. API Specification
10. External Integration Contracts
11. Security Threat Model (STRIDE-Full)
12. Performance Requirements
13. Idempotency Requirements
14. Configuration Schema
15. Environment Configuration
16. Operational Requirements
17. Implementation Guide
18. Testing Strategy (comprehensive)
19. Monitoring & Observability (detailed)
20. Examples (multiple scenarios)
21. Related Specs

---

### 2.4 Profile: full (default)

**All v4.0 sections** - backward compatible

---

## 3-7. [Same as original workflow]

[Content skipped for brevity - includes Mode Handling, Flag Resolution, Security Templates, Performance Templates, Domain-Based Enhancement]

---

## 8. Detect Mode: NEW vs EDIT (Enhanced with Content Analysis - v5.1)

### 8.1 Check for Existing SPEC

```bash
test -f spec.md && echo "EDIT" || echo "NEW"
```

### 8.2 If EDIT Mode: Load Existing SPEC

```typescript
const existingSpec = fs.readFileSync('spec.md', 'utf-8');
const sections = parseSpecIntoSections(existingSpec);
```

### 8.3 Extract Critical Sections (Enhanced)

**Detect sections with meta tags:**
```markdown
<!-- @critical security -->
## Security Threat Model (STRIDE)
...
<!-- @end-critical -->
```

**Auto-detect critical sections (no meta tags):**
- Security Threat Model (STRIDE)
- Performance Requirements
- Dependency Injection Pattern
- Configuration Schema
- Data Model & Schema
- API Specification
- Business Rules & Logic
- Idempotency Requirements

### 8.4 Check Force Update Flags

If `--force-update=all`: Allow updating all sections
If `--force-update=stride,config`: Allow only specified sections
If `--force-update=none` (default): Preserve all critical sections

### 8.5 Content Analysis & Fingerprinting (NEW v5.1)

**Purpose:** Analyze existing content to understand what needs to be preserved

```typescript
interface ContentFingerprint {
  sectionName: string;
  
  // Basic metrics
  lineCount: number;
  wordCount: number;
  codeBlockCount: number;
  tableCount: number;
  
  // Content types
  hasTables: boolean;
  hasCodeExamples: boolean;
  hasDiagrams: boolean;
  hasMermaid: boolean;
  
  // Quality indicators
  isDetailed: boolean; // wordCount > 200
  isWellStructured: boolean; // has subsections
  hasSpecificExamples: boolean; // has code/tables
  
  // STRIDE-specific
  strideCategories?: string[]; // [Spoofing, Tampering, ...]
  strideEntryCount?: number;
  
  // Performance-specific
  performanceMetrics?: string[]; // [P50, P99, TPS, ...]
  
  // API-specific
  apiEndpoints?: string[]; // [GET /api/users, POST /api/auth, ...]
  
  // Data Model-specific
  tableNames?: string[]; // [users, transactions, ...]
  hasErDiagram?: boolean;
  
  // Hash for change detection
  contentHash: string;
}

function analyzeSection(sectionContent: string, sectionName: string): ContentFingerprint {
  const lines = sectionContent.split('\n');
  const words = sectionContent.split(/\s+/).length;
  const codeBlocks = (sectionContent.match(/```/g) || []).length / 2;
  const tables = (sectionContent.match(/\|.*\|/g) || []).length;
  
  const fingerprint: ContentFingerprint = {
    sectionName,
    lineCount: lines.length,
    wordCount: words,
    codeBlockCount: codeBlocks,
    tableCount: tables,
    hasTables: tables > 0,
    hasCodeExamples: codeBlocks > 0,
    hasDiagrams: sectionContent.includes('```mermaid') || sectionContent.includes('```diagram'),
    hasMermaid: sectionContent.includes('```mermaid'),
    isDetailed: words > 200,
    isWellStructured: lines.filter(l => l.startsWith('###')).length > 2,
    hasSpecificExamples: codeBlocks > 0 || tables > 0,
    contentHash: crypto.createHash('sha256').update(sectionContent).digest('hex').substring(0, 16)
  };
  
  // STRIDE-specific analysis
  if (sectionName.toLowerCase().includes('stride') || sectionName.toLowerCase().includes('security threat')) {
    const strideCategories = extractStrideCategories(sectionContent);
    fingerprint.strideCategories = strideCategories;
    fingerprint.strideEntryCount = countStrideEntries(sectionContent);
  }
  
  // Performance-specific analysis
  if (sectionName.toLowerCase().includes('performance')) {
    fingerprint.performanceMetrics = extractPerformanceMetrics(sectionContent);
  }
  
  // API-specific analysis
  if (sectionName.toLowerCase().includes('api')) {
    fingerprint.apiEndpoints = extractApiEndpoints(sectionContent);
  }
  
  // Data Model-specific analysis
  if (sectionName.toLowerCase().includes('data model') || sectionName.toLowerCase().includes('schema')) {
    fingerprint.tableNames = extractTableNames(sectionContent);
    fingerprint.hasErDiagram = sectionContent.includes('erDiagram');
  }
  
  return fingerprint;
}

function extractStrideCategories(content: string): string[] {
  const categories = ['Spoofing', 'Tampering', 'Repudiation', 'Information Disclosure', 'Denial of Service', 'Elevation of Privilege'];
  return categories.filter(cat => 
    content.toLowerCase().includes(cat.toLowerCase())
  );
}

function countStrideEntries(content: string): number {
  // Count table rows or threat entries
  const tableRows = content.match(/\|[^|]+\|[^|]+\|[^|]+\|/g);
  return tableRows ? tableRows.length - 1 : 0; // -1 for header
}

function extractPerformanceMetrics(content: string): string[] {
  const metrics = ['P50', 'P95', 'P99', 'P999', 'TPS', 'RPS', 'Latency', 'Throughput', 'Uptime', 'SLA'];
  return metrics.filter(metric => 
    content.includes(metric)
  );
}

function extractApiEndpoints(content: string): string[] {
  const endpoints: string[] = [];
  const regex = /(GET|POST|PUT|DELETE|PATCH)\s+\/[^\s\n]+/g;
  const matches = content.match(regex);
  return matches || [];
}

function extractTableNames(content: string): string[] {
  const tableNames: string[] = [];
  const createTableRegex = /CREATE TABLE\s+(\w+)/gi;
  const matches = content.matchAll(createTableRegex);
  for (const match of matches) {
    tableNames.push(match[1]);
  }
  return tableNames;
}

// Analyze all sections
const sectionFingerprints = new Map<string, ContentFingerprint>();
for (const [sectionName, sectionContent] of sections.entries()) {
  sectionFingerprints.set(sectionName, analyzeSection(sectionContent, sectionName));
}

console.log('\n📊 Existing Content Analysis:');
for (const [name, fp] of sectionFingerprints.entries()) {
  console.log(`\n📄 ${name}:`);
  console.log(`  Lines: ${fp.lineCount}, Words: ${fp.wordCount}`);
  console.log(`  Detailed: ${fp.isDetailed ? '✅' : '❌'}, Has Examples: ${fp.hasSpecificExamples ? '✅' : '❌'}`);
  
  if (fp.strideCategories) {
    console.log(`  STRIDE Categories: ${fp.strideCategories.length}/6 (${fp.strideCategories.join(', ')})`);
    console.log(`  STRIDE Entries: ${fp.strideEntryCount}`);
  }
  
  if (fp.performanceMetrics) {
    console.log(`  Performance Metrics: ${fp.performanceMetrics.join(', ')}`);
  }
  
  if (fp.apiEndpoints && fp.apiEndpoints.length > 0) {
    console.log(`  API Endpoints: ${fp.apiEndpoints.length} (${fp.apiEndpoints.slice(0, 3).join(', ')}...)`);
  }
  
  if (fp.tableNames && fp.tableNames.length > 0) {
    console.log(`  Database Tables: ${fp.tableNames.length} (${fp.tableNames.join(', ')})`);
    console.log(`  ER Diagram: ${fp.hasErDiagram ? '✅' : '❌'}`);
  }
}
```

**Store fingerprints for later comparison:**
```typescript
const EXISTING_FINGERPRINTS = sectionFingerprints;
```

---

## 9. Critical Section Preservation Strategy

### 9.1 Default Strategy: Preserve All Critical Sections

By default, critical sections are **preserved** unless:
1. User specifies `--force-update`
2. Section has meta tag `<!-- @critical allow-update -->`

### 9.2 Critical Section Registry

```json
{
  "Security Threat Model (STRIDE)": {
    "preserve": true,
    "reason": "Contains detailed threat analysis",
    "allowUpdate": false
  },
  "Performance Requirements": {
    "preserve": true,
    "reason": "Contains validated SLA targets",
    "allowUpdate": false
  },
  "Dependency Injection Pattern": {
    "preserve": true,
    "reason": "Contains specific implementation patterns",
    "allowUpdate": false
  },
  "Configuration Schema": {
    "preserve": true,
    "reason": "Contains production config structure",
    "allowUpdate": false
  }
}
```

### 9.3 Handle --force-update Flag

```typescript
if (FLAGS.force_update === 'all') {
  // Allow all updates
  for (const section of criticalSections) {
    section.allowUpdate = true;
  }
} else if (FLAGS.force_update) {
  // Allow specific sections
  const allowList = FLAGS.force_update.split(',');
  for (const section of criticalSections) {
    if (allowList.some(s => section.name.toLowerCase().includes(s.toLowerCase()))) {
      section.allowUpdate = true;
    }
  }
}
```

### 9.4 Meta Tag Override

```markdown
<!-- @critical security allow-update -->
## Security Threat Model
...
<!-- @end-critical -->
```

This section can be updated even without --force-update flag.

---

## 10. Consistency Validation

### 10.1-10.4 [Same as original workflow]

[Content skipped for brevity]

### 10.5 Quality Validation (NEW v5.1)

**Purpose:** Validate that generated content meets quality standards

```typescript
interface QualityCheck {
  sectionName: string;
  passed: boolean;
  errors: string[];
  warnings: string[];
  score: number; // 0-100
}

function validateQuality(generatedContent: string, profile: string): QualityCheck[] {
  const checks: QualityCheck[] = [];
  const sections = parseSpecIntoSections(generatedContent);
  
  // Check 1: STRIDE Model Completeness (for financial/backend profiles)
  if (profile === 'financial' || profile === 'backend-service') {
    const strideCheck = validateStrideModel(sections.get('Security Threat Model (STRIDE)'));
    checks.push(strideCheck);
  }
  
  // Check 2: Performance Requirements Completeness
  if (profile === 'financial' || (profile === 'backend-service' && FLAGS.performance !== 'none')) {
    const perfCheck = validatePerformanceRequirements(sections.get('Performance Requirements'));
    checks.push(perfCheck);
  }
  
  // Check 3: API Specification Completeness
  if (sections.has('API Specification')) {
    const apiCheck = validateApiSpecification(sections.get('API Specification'));
    checks.push(apiCheck);
  }
  
  // Check 4: Data Model Completeness
  if (sections.has('Data Model & Schema') || sections.has('Data Model')) {
    const dataCheck = validateDataModel(sections.get('Data Model & Schema') || sections.get('Data Model'));
    checks.push(dataCheck);
  }
  
  // Check 5: DI Pattern Completeness (if included)
  if (sections.has('Dependency Injection Pattern')) {
    const diCheck = validateDIPattern(sections.get('Dependency Injection Pattern'));
    checks.push(diCheck);
  }
  
  return checks;
}

function validateStrideModel(content: string | undefined): QualityCheck {
  if (!content) {
    return {
      sectionName: 'Security Threat Model (STRIDE)',
      passed: false,
      errors: ['STRIDE section is missing'],
      warnings: [],
      score: 0
    };
  }
  
  const requiredCategories = ['Spoofing', 'Tampering', 'Repudiation', 'Information Disclosure', 'Denial of Service', 'Elevation of Privilege'];
  const foundCategories = requiredCategories.filter(cat => 
    content.toLowerCase().includes(cat.toLowerCase())
  );
  
  const errors: string[] = [];
  const warnings: string[] = [];
  
  // Must have all 6 categories
  if (foundCategories.length < 6) {
    errors.push(`STRIDE model incomplete: Only ${foundCategories.length}/6 categories found`);
    errors.push(`Missing: ${requiredCategories.filter(c => !foundCategories.includes(c)).join(', ')}`);
  }
  
  // Should have threat entries
  const hasTable = content.includes('|') && content.includes('Threat');
  if (!hasTable) {
    warnings.push('STRIDE model should include a threat table');
  }
  
  // Should have mitigations
  if (!content.toLowerCase().includes('mitigation')) {
    warnings.push('STRIDE model should include mitigations for each threat');
  }
  
  const score = (foundCategories.length / 6) * 100;
  
  return {
    sectionName: 'Security Threat Model (STRIDE)',
    passed: errors.length === 0,
    errors,
    warnings,
    score
  };
}

function validatePerformanceRequirements(content: string | undefined): QualityCheck {
  if (!content) {
    return {
      sectionName: 'Performance Requirements',
      passed: false,
      errors: ['Performance Requirements section is missing'],
      warnings: [],
      score: 0
    };
  }
  
  const requiredMetrics = ['P99', 'TPS', 'Uptime', 'SLA'];
  const foundMetrics = requiredMetrics.filter(metric => 
    content.includes(metric)
  );
  
  const errors: string[] = [];
  const warnings: string[] = [];
  
  // Must have key metrics
  if (foundMetrics.length < 3) {
    errors.push(`Performance metrics incomplete: Only ${foundMetrics.length}/4 key metrics found`);
  }
  
  // Should have specific values
  const hasNumericTargets = /\d+\s*(ms|s|%|TPS|RPS)/.test(content);
  if (!hasNumericTargets) {
    warnings.push('Performance metrics should include specific numeric targets');
  }
  
  // Should have monitoring section
  if (!content.toLowerCase().includes('monitor')) {
    warnings.push('Performance requirements should include monitoring strategy');
  }
  
  const score = (foundMetrics.length / 4) * 100;
  
  return {
    sectionName: 'Performance Requirements',
    passed: errors.length === 0,
    errors,
    warnings,
    score
  };
}

function validateApiSpecification(content: string | undefined): QualityCheck {
  if (!content) {
    return {
      sectionName: 'API Specification',
      passed: false,
      errors: ['API Specification section is missing'],
      warnings: [],
      score: 0
    };
  }
  
  const errors: string[] = [];
  const warnings: string[] = [];
  
  // Must have endpoints
  const endpoints = extractApiEndpoints(content);
  if (endpoints.length === 0) {
    errors.push('No API endpoints defined');
  }
  
  // Should have request/response schemas
  if (!content.toLowerCase().includes('request') || !content.toLowerCase().includes('response')) {
    warnings.push('API spec should include request/response schemas');
  }
  
  // Should have authentication info
  if (!content.toLowerCase().includes('auth')) {
    warnings.push('API spec should include authentication information');
  }
  
  // Should have error handling
  if (!content.toLowerCase().includes('error')) {
    warnings.push('API spec should include error response formats');
  }
  
  const score = endpoints.length > 0 ? 100 : 0;
  
  return {
    sectionName: 'API Specification',
    passed: errors.length === 0,
    errors,
    warnings,
    score
  };
}

function validateDataModel(content: string | undefined): QualityCheck {
  if (!content) {
    return {
      sectionName: 'Data Model & Schema',
      passed: false,
      errors: ['Data Model section is missing'],
      warnings: [],
      score: 0
    };
  }
  
  const errors: string[] = [];
  const warnings: string[] = [];
  
  // Must have table definitions
  const tables = extractTableNames(content);
  if (tables.length === 0) {
    errors.push('No database tables defined');
  }
  
  // Should have ER diagram
  if (!content.includes('erDiagram') && !content.includes('```mermaid')) {
    warnings.push('Data model should include ER diagram');
  }
  
  // Should have indexes
  if (!content.toLowerCase().includes('index')) {
    warnings.push('Schema should define indexes for performance');
  }
  
  // Should have constraints
  if (!content.toLowerCase().includes('constraint') && !content.toLowerCase().includes('foreign key')) {
    warnings.push('Schema should define constraints and relationships');
  }
  
  const score = tables.length > 0 ? 100 : 0;
  
  return {
    sectionName: 'Data Model & Schema',
    passed: errors.length === 0,
    errors,
    warnings,
    score
  };
}

function validateDIPattern(content: string | undefined): QualityCheck {
  if (!content) {
    return {
      sectionName: 'Dependency Injection Pattern',
      passed: false,
      errors: ['DI Pattern section is missing'],
      warnings: [],
      score: 0
    };
  }
  
  const errors: string[] = [];
  const warnings: string[] = [];
  
  // Must have constructor injection example
  if (!content.includes('constructor')) {
    errors.push('DI pattern must include constructor injection example');
  }
  
  // Should have interface definitions
  if (!content.includes('interface') && !content.includes('IDatabase')) {
    warnings.push('DI pattern should define interfaces for dependencies');
  }
  
  // Should mention backward compatibility
  if (!content.toLowerCase().includes('backward') && !content.toLowerCase().includes('optional')) {
    warnings.push('DI pattern should support backward compatibility with optional parameters');
  }
  
  const score = content.includes('constructor') ? 100 : 50;
  
  return {
    sectionName: 'Dependency Injection Pattern',
    passed: errors.length === 0,
    errors,
    warnings,
    score
  };
}

// Execute quality validation
console.log('\n🔍 Quality Validation:');
const qualityChecks = validateQuality(generatedContent, PROFILE);

for (const check of qualityChecks) {
  console.log(`\n📋 ${check.sectionName}:`);
  console.log(`  Score: ${check.score.toFixed(0)}%`);
  console.log(`  Status: ${check.passed ? '✅ PASS' : '❌ FAIL'}`);
  
  if (check.errors.length > 0) {
    console.log(`  ❌ Errors:`);
    check.errors.forEach(e => console.log(`    - ${e}`));
  }
  
  if (check.warnings.length > 0) {
    console.log(`  ⚠️ Warnings:`);
    check.warnings.forEach(w => console.log(`    - ${w}`));
  }
}

// Calculate overall quality score
const overallScore = qualityChecks.reduce((sum, c) => sum + c.score, 0) / qualityChecks.length;
console.log(`\n📊 Overall Quality Score: ${overallScore.toFixed(0)}%`);

// Fail if critical errors
const criticalErrors = qualityChecks.filter(c => !c.passed && c.errors.length > 0);
if (criticalErrors.length > 0 && FLAGS.validate_quality) {
  console.error(`\n❌ Quality validation failed with ${criticalErrors.length} critical errors`);
  throw new Error('Quality validation failed');
}
```

---

## 11. Output Organization

[Same as original workflow]

---

## 12. Configuration File Support

[Same as original workflow]

---

## 13. Generate SPEC Based on Profile & Flags

### 13.1 Assemble Sections

Based on:
- Selected profile
- Flags (--security, --di, --performance)
- Domain hints
- Config file settings

### 13.1.1 Resolve Spec Dependencies

[Same as original workflow]

---

### 13.2 Section Templates & Formatting (NEW v5.1.1)

**Purpose:** Define clean, readable templates for each section WITHOUT visible meta tags

#### 13.2.1 Core Principles

1. **Clean Format:** No visible `<!-- @critical -->` tags in generated output
2. **Clear Separators:** Use `---` between major sections
3. **Consistent Structure:** Follow simple, readable markdown
4. **Preserve Readability:** Avoid clutter, keep it simple

#### 13.2.2 Technology Stack Template

**Template:**
```markdown
## Technology Stack

**Stack A:** {Primary Stack Description}

**Core Technologies:**
- **Runtime:** {Runtime details}
- **Framework:** {Framework details}
- **Database:** {Database details}
- **Queue System:** {Queue details}
- **Validation:** {Validation details}
- **Language:** {Language details}

---
```

**Example:**
```markdown
## Technology Stack

**Stack A:** Node.js with TypeScript

**Core Technologies:**
- **Runtime:** Node.js 22.x with TypeScript strict mode
- **Framework:** Fastify 5.x (^5.6.0)
- **Database:** PostgreSQL 16+ with Prisma 6.x (^6.0.0)
- **Queue System:** BullMQ on Redis 7+
- **Validation:** Zod 3.x
- **Language:** TypeScript 5.x

---
```

**❌ BAD (Too Complex):**
```markdown
## Technology Stack

<!-- @critical tech-stack -->
**Runtime:** Node.js 22.x with TypeScript strict mode  
**Framework:** Fastify 5.x for high-performance REST API  
**Database:** PostgreSQL 16+ with Redis 7+ for hierarchical caching  
...
<!-- @end-critical -->
```

#### 13.2.3 Dependency Injection Pattern Template

**Template:**
```markdown
## Dependency Injection Pattern (MANDATORY)

**Pattern Compliance:** All services in this specification **MUST** implement the Dependency Injection (DI) Pattern as defined in [DEPENDENCY-INJECTION-PATTERN.md](../../patterns/DEPENDENCY-INJECTION-PATTERN.md).

### Core Requirements

All service classes MUST:

1. **Constructor-Based Injection**
   - Accept all dependencies through constructor parameters
   - All parameters MUST be optional with sensible defaults
   - Support both production and testing scenarios

2. **Interface-Based Dependencies**
   - Define interfaces for all dependencies (IDatabase, ILogger, ICache, etc.)
   - Depend on abstractions, not concrete implementations
   - Use standard platform interfaces where available

3. **Backward Compatibility**
   - Service MUST work without any constructor parameters (production mode)
   - Service MUST accept injected dependencies (testing mode)
   - No breaking changes to existing code

### Standard Service Structure

```typescript
/**
 * Service description
 * 
 * @implements DI Pattern (Mandatory)
 */
export class ServiceName {
  private database: IDatabase;
  private logger: ILogger;
  private cache: ICache;
  private config: ServiceConfig;

  /**
   * Constructor with Dependency Injection
   * 
   * @param database - Database connection (optional, defaults to production DB)
   * @param logger - Logger instance (optional, defaults to production logger)
   * @param cache - Cache connection (optional, defaults to production cache)
   * @param config - Service configuration (optional, defaults to env config)
   */
  constructor(
    database?: IDatabase,
    logger?: ILogger,
    cache?: ICache,
    config?: ServiceConfig
  ) {
    this.database = database || createDatabaseConnection();
    this.logger = logger || initializeLogger();
    this.cache = cache || createCacheConnection();
    this.config = config || loadConfigFromEnv();
  }

  // Business logic methods...
}
```

---
```

#### 13.2.4 Section Separator Rules

**Apply `---` after these sections:**
1. Header (after Update Reason)
2. Technology Stack
3. Dependency Injection Pattern
4. Overview
5. When to Use This Specification
6. Architecture
7. All major sections before next major section

**Example Flow:**
```markdown
# SPEC-005: Promo System

**Status:** DRAFT
...

---                         👈 After header

## Technology Stack
...

---                         👈 After tech stack

## Dependency Injection Pattern
...

---                         👈 After DI

## Overview
...

---                         👈 After overview
```

#### 13.2.5 Overview Template

**Template:**
```markdown
## Overview

**Purpose:** {One-sentence purpose}

**Scope:**
- {Scope item 1}
- {Scope item 2}
- {Scope item 3}

**Non-Goals:**
- {Non-goal 1}
- {Non-goal 2}
- {Non-goal 3}

**Key Features:**
- **{Feature 1}:** {Description}
- **{Feature 2}:** {Description}
- **{Feature 3}:** {Description}

---
```

#### 13.2.6 When to Use Template

**Template:**
```markdown
## When to Use This Specification

**Use this spec when:**
- {Use case 1}
- {Use case 2}
- {Use case 3}

**Do NOT use this spec for:**
- {Anti-pattern 1}
- {Anti-pattern 2}
- {Anti-pattern 3}

---
```

#### 13.2.7 Architecture Template

**Template:**
```markdown
## Architecture

### High-Level Architecture

{High-level description paragraph}

### Components

**{Component 1 Name}:**
- Responsibility: {Responsibility}
- Technology: {Technology}
- Interactions: {Interactions}

**{Component 2 Name}:**
- Responsibility: {Responsibility}
- Technology: {Technology}
- Interactions: {Interactions}

### Data Flow

1. **{Flow 1 Name}:** {Steps}
2. **{Flow 2 Name}:** {Steps}
3. **{Flow 3 Name}:** {Steps}

---
```

#### 13.2.8 Meta Tags Strategy (INTERNAL USE ONLY)

**DO NOT include visible meta tags in generated spec.md**

Meta tags are for **internal tracking only** and should be:
1. Stored in separate `.smartspec/registry/critical-sections-registry.json`
2. Used during editing to identify critical sections
3. **NEVER** included in the actual spec.md file

**Internal Registry Format:**
```json
{
  "spec-005": {
    "critical_sections": {
      "Technology Stack": {
        "startLine": 13,
        "endLine": 24,
        "hash": "a1b2c3d4",
        "preserve": true
      },
      "Dependency Injection Pattern": {
        "startLine": 26,
        "endLine": 150,
        "hash": "e5f6g7h8",
        "preserve": true
      }
    }
  }
}
```

---

### 13.3 Apply Templates & Format Sections

**Implementation:**

```typescript
function assembleSPEC(
  headerMetadata: HeaderMetadata,
  profile: string,
  sections: Map<string, string>
): string {
  let spec = '';
  
  // 1. Header (ALWAYS first, ALWAYS preserved)
  spec += formatHeader(headerMetadata);
  spec += '\n';
  
  // 2. Technology Stack (if included in profile)
  if (sections.has('Technology Stack')) {
    spec += formatTechnologyStack(sections.get('Technology Stack')!);
    spec += '\n---\n\n';
  }
  
  // 3. Dependency Injection Pattern (if included in profile)
  if (sections.has('Dependency Injection Pattern')) {
    spec += sections.get('Dependency Injection Pattern')!;
    spec += '\n---\n\n';
  }
  
  // 4. Overview (ALWAYS included)
  if (sections.has('Overview')) {
    spec += sections.get('Overview')!;
    spec += '\n---\n\n';
  }
  
  // 5. When to Use (if included in profile)
  if (sections.has('When to Use This Specification')) {
    spec += sections.get('When to Use This Specification')!;
    spec += '\n---\n\n';
  }
  
  // 6. Architecture (ALWAYS included)
  if (sections.has('Architecture')) {
    spec += sections.get('Architecture')!;
    spec += '\n---\n\n';
  }
  
  // 7-21. Other sections with separators...
  // (Implementation continues for all sections)
  
  return spec;
}

function formatTechnologyStack(content: string): string {
  // Ensure clean format without meta tags
  let formatted = content;
  
  // Remove any meta tags if present
  formatted = formatted.replace(/<!-- @critical[^>]*-->\n?/g, '');
  formatted = formatted.replace(/<!-- @end-critical -->\n?/g, '');
  
  // Ensure proper structure
  if (!formatted.includes('**Stack A:**')) {
    // Convert to simple format if needed
    formatted = `## Technology Stack\n\n**Stack A:** Node.js with TypeScript\n\n**Core Technologies:**\n${formatted}`;
  }
  
  return formatted;
}

// Assemble the final SPEC
const ASSEMBLED_SPEC = assembleSPEC(
  HEADER_METADATA,
  PROFILE,
  GENERATED_SECTIONS
);

console.log('\n📝 SPEC Assembled:');
console.log(`  Total length: ${ASSEMBLED_SPEC.length} characters`);
console.log(`  Sections: ${GENERATED_SECTIONS.size}`);
console.log(`  Has header metadata: ${ASSEMBLED_SPEC.includes('**Status:**') ? '✅' : '❌'}`);
console.log(`  Has section separators: ${ASSEMBLED_SPEC.includes('\n---\n') ? '✅' : '❌'}`);
console.log(`  Has meta tags: ${ASSEMBLED_SPEC.includes('<!-- @critical') ? '❌ WARNING' : '✅ Clean'}`);
```

---

### 13.4 Run Validation

If --validate-consistency: check rules.
If --validate-quality: check content quality (NEW v5.1).

### 13.5 Write Output

#### 13.5.1 Backup Existing SPEC (MANDATORY - WITH PROOF)

🚨 **CRITICAL: This step MUST be executed before writing new spec.md** 🚨

🔍 **PROOF REQUIRED: You MUST show actual command outputs, not just say "done"** 🔍

---

**INSTRUCTION FOR AI:**

You MUST perform the following backup steps using `bash_tool`.

**⚠️ CRITICAL RULE: You MUST show the actual output from EVERY command below.**

**❌ DO NOT just say "Backup created" without showing proof.**
**❌ DO NOT just write "✅ Backup verified" without showing actual output.**
**✅ DO show the exact commands and their outputs.

---

**Step 1: Check if spec.md exists**

Execute using `bash_tool`:
```bash
test -f spec.md && echo "EXISTS" || echo "NOT_EXISTS"
```

**👉 SHOW THE OUTPUT HERE in your response.**

If output is "NOT_EXISTS", skip to section 13.5.2.
If output is "EXISTS", proceed to Step 2.

---

**Step 2: Create backup directory structure using OUTPUT_PATHS**

Execute using `bash_tool`:
```bash
# Use the spec-specific backup directory
BACKUP_DIR="${OUTPUT_PATHS.backupsSpec}"
mkdir -p "${BACKUP_DIR}"
ls -la "${BACKUP_DIR}/" 2>/dev/null || echo "📁 Created: ${BACKUP_DIR}"
```

**👉 SHOW THE OUTPUT HERE in your response.**

Example output:
```
📁 Created: .smartspec/backups/spec-004
```
or
```
drwxr-xr-x  2 user  group  64 Dec  6 14:30 .
drwxr-xr-x  5 user  group 160 Dec  6 14:30 ..
-rw-r--r--  1 user  group 24K Dec  6 14:25 spec.backup-20251206-142530.md
```

---

**Step 3: Create backup with timestamp**

Execute using `bash_tool`:
```bash
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
BACKUP_DIR="${OUTPUT_PATHS.backupsSpec}"
BACKUP_FILE="spec.backup-${TIMESTAMP}.md"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILE}"

cp spec.md "${BACKUP_PATH}"
echo "📁 Backup created: ${BACKUP_PATH}"
echo "📅 Timestamp: ${TIMESTAMP}"
```

**👉 SHOW THE OUTPUT HERE in your response.**

You should see:
```
📁 Backup created: .smartspec/backups/spec-004/spec.backup-20251206-143059.md
📅 Timestamp: 20251206-143059
```

---

**Step 4: Verify backup was created (MANDATORY PROOF)**

🚨 **THIS IS THE MOST CRITICAL STEP** 🚨

Execute ALL of these commands using `bash_tool` and show ALL outputs:

```bash
BACKUP_DIR="${OUTPUT_PATHS.backupsSpec}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILE}"

# Command 1: List all backup files with details
echo "=== Backup files in ${BACKUP_DIR} ==="
ls -lh "${BACKUP_DIR}/"

# Command 2: Verify specific backup exists
echo ""
echo "=== Verification ==="
test -f "${BACKUP_PATH}" && echo "✅ BACKUP FILE EXISTS: ${BACKUP_FILE}" || echo "❌ BACKUP FILE NOT FOUND"

# Command 3: Show file size
echo ""
echo "=== File size ==="
du -h "${BACKUP_PATH}"

# Command 4: Show first 5 lines to prove it's the correct file
echo ""
echo "=== First 5 lines of backup ==="
head -n 5 "${BACKUP_PATH}"

# Command 5: Count total backups for this spec
echo ""
echo "=== Total backups for ${SPEC_ID} ==="
ls -1 "${BACKUP_DIR}/"*.md 2>/dev/null | wc -l
```

**👉 SHOW THE OUTPUT FROM ALL 5 COMMANDS HERE in your response.**

**CRITICAL VALIDATION:**

You MUST see:
1. ✅ List of backup files (from `ls -lh`)
2. ✅ Message "✅ BACKUP FILE EXISTS: spec.backup-..." (NOT "❌ BACKUP FILE NOT FOUND")
3. ✅ File size (e.g., "24K")
4. ✅ First 5 lines of the backup file (should match original spec.md header)
5. ✅ Total backup count (e.g., "3" if this is the 3rd backup)

If you see "❌ BACKUP FILE NOT FOUND" or any command fails:
1. ❌ STOP immediately
2. ❌ DO NOT proceed to section 13.5.2
3. ❌ DO NOT write new spec.md
4. ❌ Report error to user: "Backup failed. Cannot proceed."
5. ❌ Exit with error

---

**Step 5: Cleanup old backups (keep last 10 for this spec)**

Optional but recommended:
```bash
BACKUP_DIR="${OUTPUT_PATHS.backupsSpec}"
cd "${BACKUP_DIR}"
BACKUP_COUNT=$(ls -1 spec.backup-*.md 2>/dev/null | wc -l)

if [ $BACKUP_COUNT -gt 10 ]; then
  echo "🗑️  Cleanup: Found ${BACKUP_COUNT} backups, keeping last 10"
  ls -t spec.backup-*.md | tail -n +11 | xargs -r rm 2>/dev/null
  echo "✅ Cleanup complete"
  ls -lh
else
  echo "📦 Keeping all ${BACKUP_COUNT} backups (limit: 10)"
fi
cd - > /dev/null
```

**👉 You may show the output if you execute this step.**

Example output:
```
📦 Keeping all 3 backups (limit: 10)
```
or
```
🗑️  Cleanup: Found 12 backups, keeping last 10
✅ Cleanup complete
-rw-r--r-- 1 user group 24K Dec 6 14:30 spec.backup-20251206-143059.md
-rw-r--r-- 1 user group 23K Dec 6 14:15 spec.backup-20251206-141530.md
...
```

---

**Step 6: Store backup location for report**

```typescript
// Store backup info for later use in report
global.BACKUP_INFO = {
  path: BACKUP_PATH,
  filename: BACKUP_FILE,
  directory: BACKUP_DIR,
  timestamp: TIMESTAMP,
  specId: SPEC_ID,
  totalBackups: backupCount
};

console.log(`\n💾 Backup Information:`);
console.log(`  Location: ${BACKUP_INFO.path}`);
console.log(`  SPEC ID: ${BACKUP_INFO.specId}`);
console.log(`  Total backups for this SPEC: ${BACKUP_INFO.totalBackups}`);
```

---

**✅ PROOF CHECKLIST (MUST COMPLETE BEFORE PROCEEDING):**

Before you proceed to section 13.5.2, verify you have shown:

- [ ] ✅ Output from Step 1: "EXISTS" or "NOT_EXISTS"
- [ ] ✅ Output from Step 2: Directory creation confirmation
- [ ] ✅ Output from Step 3: Backup filename with full path
- [ ] ✅ Output from Step 4 Command 1: List of backup files in spec-specific folder
- [ ] ✅ Output from Step 4 Command 2: "✅ BACKUP FILE EXISTS"
- [ ] ✅ Output from Step 4 Command 3: File size
- [ ] ✅ Output from Step 4 Command 4: First 5 lines of backup
- [ ] ✅ Output from Step 4 Command 5: Total backup count

**If you cannot check ALL boxes above, GO BACK and execute the commands properly.**

---

**⚠️ CRITICAL REMINDERS:**

1. ✅ ALWAYS use `bash_tool` to execute commands
2. ✅ ALWAYS use OUTPUT_PATHS.backupsSpec (spec-specific backup folder)
3. ✅ ALWAYS show actual output from commands
4. ✅ NEVER just say "done" without showing proof
5. ✅ NEVER proceed if "❌ BACKUP FILE NOT FOUND"
6. ✅ NEVER skip backup unless user provides --no-backup flag
7. ❌ DO NOT write new spec.md if backup fails

---

**🔍 SELF-CHECK BEFORE PROCEEDING:**

Ask yourself:
1. Did I execute commands using `bash_tool`? (Not just read the instructions)
2. Did I show actual output? (Not just say "Backup created")
3. Did I see "✅ BACKUP FILE EXISTS"? (Not "❌ BACKUP FILE NOT FOUND")
4. Did I show first 5 lines of backup file? (Proof it's the correct file)
5. Is the backup in the correct spec-specific folder? (e.g., .smartspec/backups/spec-004/)

If answer is NO to ANY question:
- ❌ STOP
- ❌ GO BACK
- ❌ Execute properly
- ❌ DO NOT proceed to section 13.5.2

---

**Skip backup (only if user explicitly requests):**

If user provides `--no-backup` flag, you may skip this entire section.
Otherwise, backup is MANDATORY.

---

#### 13.5.2 Write New SPEC

Write generated content to spec.md:
```typescript
fs.writeFileSync(specPath, generatedContent, 'utf-8');
console.log(`✅ SPEC written: ${specPath}`);
```

---

#### 13.5.3 Generate Report (optional)

If `--no-report` not specified:
```typescript
// Use spec-specific reports directory
const reportDir = OUTPUT_PATHS.reportsSpec;
fs.mkdirSync(reportDir, { recursive: true });

// Generate generation report
const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
const reportPath = path.join(reportDir, `generation-report-${timestamp}.md`);
fs.writeFileSync(reportPath, reportContent, 'utf-8');

console.log(`📄 Report saved: ${reportPath}`);

// Store report info for final summary
global.REPORT_INFO = {
  path: reportPath,
  directory: reportDir,
  timestamp
};
```

---

#### 13.6 Content Comparison & Verification (NEW v5.1)

**Purpose:** Compare new content with existing to ensure no critical data is lost

```typescript
interface ContentComparison {
  sectionName: string;
  status: 'added' | 'modified' | 'preserved' | 'removed';
  oldFingerprint?: ContentFingerprint;
  newFingerprint?: ContentFingerprint;
  changes: Change[];
  concerns: string[];
}

interface Change {
  type: 'content_added' | 'content_removed' | 'content_modified';
  description: string;
  severity: 'info' | 'warning' | 'critical';
}

function compareContent(
  oldSections: Map<string, string>,
  newSections: Map<string, string>,
  oldFingerprints: Map<string, ContentFingerprint>
): ContentComparison[] {
  const comparisons: ContentComparison[] = [];
  
  // Check all sections in old spec
  for (const [sectionName, oldContent] of oldSections.entries()) {
    const newContent = newSections.get(sectionName);
    const oldFp = oldFingerprints.get(sectionName);
    
    if (!newContent) {
      // Section removed
      comparisons.push({
        sectionName,
        status: 'removed',
        oldFingerprint: oldFp,
        changes: [{
          type: 'content_removed',
          description: `Section "${sectionName}" was removed`,
          severity: 'critical'
        }],
        concerns: ['Critical section removed - data loss!']
      });
      continue;
    }
    
    const newFp = analyzeSection(newContent, sectionName);
    
    // Check if content changed
    if (oldFp!.contentHash === newFp.contentHash) {
      // Identical content
      comparisons.push({
        sectionName,
        status: 'preserved',
        oldFingerprint: oldFp,
        newFingerprint: newFp,
        changes: [],
        concerns: []
      });
      continue;
    }
    
    // Content modified - analyze changes
    const changes: Change[] = [];
    const concerns: string[] = [];
    
    // Check for significant content reduction
    if (newFp.wordCount < oldFp!.wordCount * 0.7) {
      changes.push({
        type: 'content_modified',
        description: `Content reduced by ${Math.round((1 - newFp.wordCount / oldFp!.wordCount) * 100)}% (${oldFp!.wordCount} → ${newFp.wordCount} words)`,
        severity: 'warning'
      });
      concerns.push('Significant content reduction detected');
    }
    
    // Check STRIDE-specific changes
    if (oldFp!.strideCategories && newFp.strideCategories) {
      const lostCategories = oldFp!.strideCategories.filter(c => !newFp.strideCategories!.includes(c));
      if (lostCategories.length > 0) {
        changes.push({
          type: 'content_removed',
          description: `Lost STRIDE categories: ${lostCategories.join(', ')}`,
          severity: 'critical'
        });
        concerns.push(`STRIDE model incomplete: missing ${lostCategories.join(', ')}`);
      }
      
      if (newFp.strideEntryCount! < oldFp!.strideEntryCount! * 0.8) {
        changes.push({
          type: 'content_modified',
          description: `STRIDE entries reduced: ${oldFp!.strideEntryCount} → ${newFp.strideEntryCount}`,
          severity: 'warning'
        });
        concerns.push('STRIDE threat entries significantly reduced');
      }
    }
    
    // Check Performance metrics changes
    if (oldFp!.performanceMetrics && newFp.performanceMetrics) {
      const lostMetrics = oldFp!.performanceMetrics.filter(m => !newFp.performanceMetrics!.includes(m));
      if (lostMetrics.length > 0) {
        changes.push({
          type: 'content_removed',
          description: `Lost performance metrics: ${lostMetrics.join(', ')}`,
          severity: 'critical'
        });
        concerns.push(`Performance metrics incomplete: missing ${lostMetrics.join(', ')}`);
      }
    }
    
    // Check API endpoints changes
    if (oldFp!.apiEndpoints && newFp.apiEndpoints) {
      const lostEndpoints = oldFp!.apiEndpoints.filter(e => !newFp.apiEndpoints!.includes(e));
      if (lostEndpoints.length > 0) {
        changes.push({
          type: 'content_removed',
          description: `Lost API endpoints: ${lostEndpoints.length}`,
          severity: 'critical'
        });
        concerns.push(`${lostEndpoints.length} API endpoints missing from new spec`);
      }
    }
    
    // Check database tables changes
    if (oldFp!.tableNames && newFp.tableNames) {
      const lostTables = oldFp!.tableNames.filter(t => !newFp.tableNames!.includes(t));
      if (lostTables.length > 0) {
        changes.push({
          type: 'content_removed',
          description: `Lost database tables: ${lostTables.join(', ')}`,
          severity: 'critical'
        });
        concerns.push(`Database tables missing: ${lostTables.join(', ')}`);
      }
      
      // Check ER diagram
      if (oldFp!.hasErDiagram && !newFp.hasErDiagram) {
        changes.push({
          type: 'content_removed',
          description: 'ER diagram removed',
          severity: 'warning'
        });
        concerns.push('ER diagram was removed from Data Model');
      }
    }
    
    // Check for lost code examples
    if (oldFp!.codeBlockCount > newFp.codeBlockCount) {
      changes.push({
        type: 'content_modified',
        description: `Code examples reduced: ${oldFp!.codeBlockCount} → ${newFp.codeBlockCount}`,
        severity: 'warning'
      });
      concerns.push('Some code examples were removed');
    }
    
    // Check for lost tables
    if (oldFp!.tableCount > newFp.tableCount) {
      changes.push({
        type: 'content_modified',
        description: `Tables reduced: ${oldFp!.tableCount} → ${newFp.tableCount}`,
        severity: 'warning'
      });
      concerns.push('Some tables were removed');
    }
    
    comparisons.push({
      sectionName,
      status: 'modified',
      oldFingerprint: oldFp,
      newFingerprint: newFp,
      changes,
      concerns
    });
  }
  
  // Check for new sections
  for (const [sectionName, newContent] of newSections.entries()) {
    if (!oldSections.has(sectionName)) {
      const newFp = analyzeSection(newContent, sectionName);
      comparisons.push({
        sectionName,
        status: 'added',
        newFingerprint: newFp,
        changes: [{
          type: 'content_added',
          description: `New section "${sectionName}" added`,
          severity: 'info'
        }],
        concerns: []
      });
    }
  }
  
  return comparisons;
}

// Execute comparison
if (MODE === 'EDIT') {
  console.log('\n📊 Content Comparison:');
  
  const oldSections = parseSpecIntoSections(existingSpec);
  const newSections = parseSpecIntoSections(generatedContent);
  const comparisons = compareContent(oldSections, newSections, EXISTING_FINGERPRINTS);
  
  for (const comp of comparisons) {
    console.log(`\n📄 ${comp.sectionName}:`);
    console.log(`  Status: ${comp.status.toUpperCase()}`);
    
    if (comp.changes.length > 0) {
      console.log(`  Changes:`);
      for (const change of comp.changes) {
        const icon = change.severity === 'critical' ? '❌' : change.severity === 'warning' ? '⚠️' : 'ℹ️';
        console.log(`    ${icon} ${change.description}`);
      }
    }
    
    if (comp.concerns.length > 0) {
      console.log(`  ⚠️ Concerns:`);
      comp.concerns.forEach(c => console.log(`    - ${c}`));
    }
  }
  
  // Check for critical losses
  const criticalChanges = comparisons.flatMap(c => 
    c.changes.filter(ch => ch.severity === 'critical')
  );
  
  if (criticalChanges.length > 0) {
    console.error(`\n❌ CRITICAL: ${criticalChanges.length} critical data losses detected!`);
    console.error('The following critical content was lost:');
    criticalChanges.forEach(ch => console.error(`  - ${ch.description}`));
    
    if (!FLAGS.force_update) {
      console.error('\n⚠️ STOPPING: Use --force-update to override, or review and fix the issues');
      throw new Error('Critical content loss detected');
    } else {
      console.warn('\n⚠️ WARNING: Proceeding with --force-update despite critical losses');
    }
  }
}
```

---

#### 13.7 Generate Diff Report (NEW v5.1)

**Purpose:** Generate a detailed diff report showing what changed

```typescript
function generateDiffReport(comparisons: ContentComparison[]): string {
  const timestamp = new Date().toISOString();
  
  let report = `# SPEC Update Diff Report

**Generated:** ${timestamp}
**Mode:** ${MODE}
**Profile:** ${PROFILE}

---

## Summary

`;
  
  const added = comparisons.filter(c => c.status === 'added');
  const modified = comparisons.filter(c => c.status === 'modified');
  const preserved = comparisons.filter(c => c.status === 'preserved');
  const removed = comparisons.filter(c => c.status === 'removed');
  
  report += `- ✅ Sections Preserved: ${preserved.length}\n`;
  report += `- 📝 Sections Modified: ${modified.length}\n`;
  report += `- ➕ Sections Added: ${added.length}\n`;
  report += `- ❌ Sections Removed: ${removed.length}\n`;
  report += `\n---\n\n`;
  
  // Detailed changes
  if (modified.length > 0) {
    report += `## Modified Sections\n\n`;
    
    for (const comp of modified) {
      report += `### ${comp.sectionName}\n\n`;
      
      if (comp.oldFingerprint && comp.newFingerprint) {
        report += `**Content Metrics:**\n`;
        report += `- Words: ${comp.oldFingerprint.wordCount} → ${comp.newFingerprint.wordCount}`;
        const wordChange = ((comp.newFingerprint.wordCount - comp.oldFingerprint.wordCount) / comp.oldFingerprint.wordCount * 100).toFixed(1);
        report += ` (${wordChange > 0 ? '+' : ''}${wordChange}%)\n`;
        
        report += `- Code Blocks: ${comp.oldFingerprint.codeBlockCount} → ${comp.newFingerprint.codeBlockCount}\n`;
        report += `- Tables: ${comp.oldFingerprint.tableCount} → ${comp.newFingerprint.tableCount}\n`;
        report += `\n`;
      }
      
      if (comp.changes.length > 0) {
        report += `**Changes:**\n`;
        for (const change of comp.changes) {
          const icon = change.severity === 'critical' ? '❌' : change.severity === 'warning' ? '⚠️' : 'ℹ️';
          report += `- ${icon} ${change.description}\n`;
        }
        report += `\n`;
      }
      
      if (comp.concerns.length > 0) {
        report += `**Concerns:**\n`;
        for (const concern of comp.concerns) {
          report += `- ⚠️ ${concern}\n`;
        }
        report += `\n`;
      }
      
      report += `---\n\n`;
    }
  }
  
  if (added.length > 0) {
    report += `## Added Sections\n\n`;
    for (const comp of added) {
      report += `- ✅ ${comp.sectionName}\n`;
    }
    report += `\n---\n\n`;
  }
  
  if (removed.length > 0) {
    report += `## Removed Sections\n\n`;
    for (const comp of removed) {
      report += `- ❌ ${comp.sectionName}\n`;
    }
    report += `\n---\n\n`;
  }
  
  // Quality assessment
  report += `## Quality Assessment\n\n`;
  const criticalIssues = comparisons.flatMap(c => c.changes).filter(ch => ch.severity === 'critical').length;
  const warnings = comparisons.flatMap(c => c.changes).filter(ch => ch.severity === 'warning').length;
  
  report += `- ❌ Critical Issues: ${criticalIssues}\n`;
  report += `- ⚠️ Warnings: ${warnings}\n`;
  report += `- ℹ️ Info: ${added.length}\n`;
  report += `\n`;
  
  if (criticalIssues === 0 && warnings === 0) {
    report += `✅ **Overall Assessment:** EXCELLENT - No issues detected\n`;
  } else if (criticalIssues === 0) {
    report += `⚠️ **Overall Assessment:** GOOD - Only minor warnings\n`;
  } else {
    report += `❌ **Overall Assessment:** NEEDS REVIEW - Critical issues detected\n`;
  }
  
  return report;
}

// Generate and save diff report
if (MODE === 'EDIT' && !FLAGS.no_diff) {
  const diffReport = generateDiffReport(comparisons);
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
  
  // Use spec-specific reports directory
  const diffPath = path.join(OUTPUT_PATHS.reportsSpec, `diff-report-${timestamp}.md`);
  fs.writeFileSync(diffPath, diffReport, 'utf-8');
  
  console.log(`\n📊 Diff report saved: ${diffPath}`);
  
  // Store diff report info for final summary
  global.DIFF_REPORT_INFO = {
    path: diffPath,
    timestamp
  };
}
```

---

#### 13.8 Section-Specific Merge Strategy (NEW v5.1)

**Purpose:** Smart merging of specific sections to preserve detailed content

```typescript
interface MergeStrategy {
  sectionName: string;
  strategy: 'preserve' | 'merge' | 'replace';
  mergeFunction?: (old: string, new: string) => string;
}

const MERGE_STRATEGIES: MergeStrategy[] = [
  {
    sectionName: 'Security Threat Model (STRIDE)',
    strategy: 'merge',
    mergeFunction: mergeStrideTable
  },
  {
    sectionName: 'Performance Requirements',
    strategy: 'merge',
    mergeFunction: mergePerformanceMetrics
  },
  {
    sectionName: 'API Specification',
    strategy: 'merge',
    mergeFunction: mergeApiEndpoints
  },
  {
    sectionName: 'Data Model & Schema',
    strategy: 'merge',
    mergeFunction: mergeDataModel
  },
  {
    sectionName: 'Configuration Schema',
    strategy: 'preserve' // Always preserve exact config
  },
  {
    sectionName: 'Dependency Injection Pattern',
    strategy: 'preserve' // Always preserve implementation details
  }
];

function mergeStrideTable(oldContent: string, newContent: string): string {
  // Parse STRIDE table from both old and new
  const oldThreats = parseStrideThreats(oldContent);
  const newThreats = parseStrideThreats(newContent);
  
  // Merge: keep all old threats, add new ones that don't exist
  const mergedThreats = [...oldThreats];
  
  for (const newThreat of newThreats) {
    const exists = oldThreats.some(old => 
      old.category === newThreat.category && 
      old.threat.toLowerCase().includes(newThreat.threat.toLowerCase().substring(0, 20))
    );
    
    if (!exists) {
      mergedThreats.push(newThreat);
    }
  }
  
  // Rebuild STRIDE table with merged content
  return rebuildStrideSection(mergedThreats);
}

function mergePerformanceMetrics(oldContent: string, newContent: string): string {
  // Extract metrics from both
  const oldMetrics = parsePerformanceMetrics(oldContent);
  const newMetrics = parsePerformanceMetrics(newContent);
  
  // Merge strategy: prefer old values (already validated), add new metrics
  const mergedMetrics = { ...newMetrics, ...oldMetrics };
  
  // Rebuild performance section
  return rebuildPerformanceSection(mergedMetrics);
}

function mergeApiEndpoints(oldContent: string, newContent: string): string {
  // Extract endpoints from both
  const oldEndpoints = parseApiEndpoints(oldContent);
  const newEndpoints = parseApiEndpoints(newContent);
  
  // Merge: keep all old endpoints, add new ones
  const mergedEndpoints = [...oldEndpoints];
  
  for (const newEp of newEndpoints) {
    const exists = oldEndpoints.some(old => 
      old.method === newEp.method && old.path === newEp.path
    );
    
    if (!exists) {
      mergedEndpoints.push(newEp);
    }
  }
  
  // Rebuild API section
  return rebuildApiSection(mergedEndpoints);
}

function mergeDataModel(oldContent: string, newContent: string): string {
  // Extract table definitions
  const oldTables = parseTableDefinitions(oldContent);
  const newTables = parseTableDefinitions(newContent);
  
  // Merge: prefer old table definitions, add new tables
  const mergedTables = { ...newTables, ...oldTables };
  
  // Preserve ER diagram if exists
  const oldErDiagram = extractErDiagram(oldContent);
  const newErDiagram = extractErDiagram(newContent);
  const erDiagram = oldErDiagram || newErDiagram;
  
  // Rebuild data model section
  return rebuildDataModelSection(mergedTables, erDiagram);
}

// Apply merge strategies
function applyMergeStrategies(
  oldSections: Map<string, string>,
  newSections: Map<string, string>
): Map<string, string> {
  const finalSections = new Map(newSections);
  
  for (const strategy of MERGE_STRATEGIES) {
    const oldContent = oldSections.get(strategy.sectionName);
    const newContent = newSections.get(strategy.sectionName);
    
    if (!oldContent || !newContent) continue;
    
    if (strategy.strategy === 'preserve') {
      // Use old content entirely
      finalSections.set(strategy.sectionName, oldContent);
      console.log(`✅ Preserved: ${strategy.sectionName}`);
      
    } else if (strategy.strategy === 'merge' && strategy.mergeFunction) {
      // Smart merge
      const merged = strategy.mergeFunction(oldContent, newContent);
      finalSections.set(strategy.sectionName, merged);
      console.log(`🔀 Merged: ${strategy.sectionName}`);
    }
  }
  
  return finalSections;
}

// Execute merge if in EDIT mode and preserve strategy is not aggressive
if (MODE === 'EDIT' && FLAGS.preserve_strategy !== 'aggressive') {
  console.log('\n🔀 Applying merge strategies...');
  const oldSections = parseSpecIntoSections(existingSpec);
  const newSections = parseSpecIntoSections(generatedContent);
  const mergedSections = applyMergeStrategies(oldSections, newSections);
  
  // Rebuild spec from merged sections
  generatedContent = rebuildSpecFromSections(mergedSections);
  console.log('✅ Merge complete');
}
```

---

#### 13.9 Final Quality Gate (NEW v5.1)

**Purpose:** Final check before writing to disk

```typescript
function finalQualityGate(content: string, profile: string): boolean {
  console.log('\n🚪 Final Quality Gate:');
  
  // Re-run quality validation
  const qualityChecks = validateQuality(content, profile);
  const failed = qualityChecks.filter(c => !c.passed);
  
  if (failed.length > 0) {
    console.error(`❌ Quality gate FAILED: ${failed.length} sections failed validation`);
    failed.forEach(f => {
      console.error(`  - ${f.sectionName}: ${f.errors.join(', ')}`);
    });
    return false;
  }
  
  // Check critical sections present
  const criticalSections = [
    'Overview',
    'Architecture',
    'Technology Stack'
  ];
  
  if (profile === 'financial') {
    criticalSections.push(
      'Security Threat Model (STRIDE)',
      'Performance Requirements',
      'Data Model & Schema',
      'API Specification'
    );
  }
  
  const sections = parseSpecIntoSections(content);
  const missingSections = criticalSections.filter(s => !sections.has(s));
  
  if (missingSections.length > 0) {
    console.error(`❌ Quality gate FAILED: Missing critical sections: ${missingSections.join(', ')}`);
    return false;
  }
  
  console.log('✅ Quality gate PASSED');
  return true;
}

// Execute final quality gate
if (FLAGS.validate_quality) {
  const passed = finalQualityGate(generatedContent, PROFILE);
  if (!passed) {
    throw new Error('Final quality gate failed');
  }
}
```

---

## 14. Update SPEC_INDEX.json (Auto-Update)

[Same as original workflow]

---

## 15. Report Output

### 15.1 Enhanced Report (Thai) - with File Locations (NEW v5.1)

**Implementation:**

```typescript
function generateFinalReport(options: {
  specPath: string;
  profile: string;
  mode: string;
  sectionsCount: number;
  qualityScore: number;
  contentComparison?: ContentComparison[];
  qualityChecks?: QualityCheck[];
  backupInfo?: typeof BACKUP_INFO;
  reportInfo?: typeof REPORT_INFO;
  diffReportInfo?: typeof DIFF_REPORT_INFO;
  outputPaths: typeof OUTPUT_PATHS;
}): string {
  const {
    specPath,
    profile,
    mode,
    sectionsCount,
    qualityScore,
    contentComparison,
    qualityChecks,
    backupInfo,
    reportInfo,
    diffReportInfo,
    outputPaths
  } = options;
  
  // Build report
  let report = `
✅ สร้าง/อัพเดท SPEC เรียบร้อยแล้ว

📁 ไฟล์: ${specPath}
📊 Profile: ${profile}
🎛️ Mode: ${mode}
✍️ Author: SmartSpec Architect v5.1

📚 Sections Generated: ${sectionsCount}
`;

  // Add section details if available
  if (contentComparison) {
    const preserved = contentComparison.filter(c => c.status === 'preserved').length;
    const modified = contentComparison.filter(c => c.status === 'modified').length;
    const added = contentComparison.filter(c => c.status === 'added').length;
    const removed = contentComparison.filter(c => c.status === 'removed').length;
    
    report += `
📊 Content Comparison:
  - ✅ Preserved: ${preserved} sections
  - 📝 Modified: ${modified} sections (merged)
  - ➕ Added: ${added} sections
  - ❌ Removed: ${removed} sections
`;
  }
  
  // Add quality information
  if (qualityChecks) {
    const warnings = qualityChecks.flatMap(c => c.warnings).length;
    const errors = qualityChecks.flatMap(c => c.errors).length;
    
    report += `
🔍 Quality Check: ${qualityChecks.filter(c => c.passed).length}/${qualityChecks.length} passed (Score: ${qualityScore.toFixed(0)}%)
`;
    
    if (warnings > 0 || errors > 0) {
      report += `⚠️ Issues: ${errors} errors, ${warnings} warnings\n`;
    }
  }
  
  // **CRITICAL: File Locations Section**
  report += `
📂 ไฟล์ที่สร้างขึ้น:
`;

  // Backup location (ALWAYS show full path)
  if (backupInfo) {
    report += `  💾 Backup:
     📁 Location: ${backupInfo.path}
     📦 Directory: ${backupInfo.directory}
     🆔 SPEC ID: ${backupInfo.specId}
     📊 Total backups: ${backupInfo.totalBackups}
     ⏰ Timestamp: ${backupInfo.timestamp}
`;
  } else {
    report += `  💾 Backup: Skipped (--no-backup)\n`;
  }
  
  // Report location
  if (reportInfo) {
    report += `
  📄 Generation Report:
     📁 Location: ${reportInfo.path}
     📂 Directory: ${reportInfo.directory}
`;
  }
  
  // Diff report location (EDIT mode only)
  if (diffReportInfo) {
    report += `
  📊 Diff Report:
     📁 Location: ${diffReportInfo.path}
     ⚠️ Review this file to see what changed
`;
  }
  
  // Output directory summary
  report += `
📁 Output Directory Structure:
   Root: ${outputPaths.root}
   ├─ backups/${backupInfo?.specId}/ (backups for this SPEC only)
   ├─ reports/${backupInfo?.specId}/ (reports for this SPEC only)
   ├─ registry/ (shared across all SPECs)
   └─ logs/ (shared across all SPECs)
`;

  // Quality details
  if (qualityChecks) {
    report += `
⚡ Quality Breakdown:
`;
    for (const check of qualityChecks) {
      const status = check.passed ? '✅' : '❌';
      report += `  ${status} ${check.sectionName}: ${check.score.toFixed(0)}%\n`;
    }
  }
  
  // Next steps
  report += `
🔄 Next steps:
`;

  if (diffReportInfo) {
    report += `1. 📊 Review diff report: ${diffReportInfo.path}\n`;
    report += `2. ✅ Verify merged sections (STRIDE, Performance, API)\n`;
  }
  
  if (backupInfo) {
    report += `${diffReportInfo ? '3' : '1'}. 💾 Backup available at: ${backupInfo.path}\n`;
  }
  
  report += `${diffReportInfo ? '4' : backupInfo ? '2' : '1'}. 🚀 Generate implementation plan: smartspec generate-plan spec.md\n`;
  report += `${diffReportInfo ? '5' : backupInfo ? '3' : '2'}. 📋 Generate tasks: smartspec generate-tasks spec.md\n`;
  
  return report;
}

// Generate and display final report
const finalReport = generateFinalReport({
  specPath: SPEC_PATH,
  profile: PROFILE,
  mode: MODE,
  sectionsCount: GENERATED_SECTIONS_COUNT,
  qualityScore: OVERALL_QUALITY_SCORE,
  contentComparison: MODE === 'EDIT' ? comparisons : undefined,
  qualityChecks: FLAGS.validate_quality ? qualityChecks : undefined,
  backupInfo: FLAGS.no_backup ? undefined : BACKUP_INFO,
  reportInfo: FLAGS.no_report ? undefined : REPORT_INFO,
  diffReportInfo: (MODE === 'EDIT' && !FLAGS.no_diff) ? DIFF_REPORT_INFO : undefined,
  outputPaths: OUTPUT_PATHS
});

console.log(finalReport);
```

**Example Output:**

```
✅ สร้าง/อัพเดท SPEC เรียบร้อยแล้ว

📁 ไฟล์: specs/feature/spec-004-financial-system/spec.md
📊 Profile: financial
🎛️ Mode: standard
✍️ Author: SmartSpec Architect v5.1

📚 Sections Generated: 21

📊 Content Comparison:
  - ✅ Preserved: 8 sections
  - 📝 Modified: 5 sections (merged)
  - ➕ Added: 3 sections
  - ❌ Removed: 0 sections

🔍 Quality Check: 10/10 passed (Score: 95%)

📂 ไฟล์ที่สร้างขึ้น:
  💾 Backup:
     📁 Location: .smartspec/backups/spec-004/spec.backup-20251206-143059.md
     📦 Directory: .smartspec/backups/spec-004
     🆔 SPEC ID: spec-004
     📊 Total backups: 3
     ⏰ Timestamp: 20251206-143059

  📄 Generation Report:
     📁 Location: .smartspec/reports/spec-004/generation-report-20251206-143102.md
     📂 Directory: .smartspec/reports/spec-004

  📊 Diff Report:
     📁 Location: .smartspec/reports/spec-004/diff-report-20251206-143102.md
     ⚠️ Review this file to see what changed

📁 Output Directory Structure:
   Root: .smartspec
   ├─ backups/spec-004/ (backups for this SPEC only)
   ├─ reports/spec-004/ (reports for this SPEC only)
   ├─ registry/ (shared across all SPECs)
   └─ logs/ (shared across all SPECs)

⚡ Quality Breakdown:
  ✅ Security Threat Model (STRIDE): 100%
  ✅ Performance Requirements: 100%
  ✅ API Specification: 90%
  ✅ Data Model & Schema: 100%
  ✅ Dependency Injection Pattern: 100%

🔄 Next steps:
1. 📊 Review diff report: .smartspec/reports/spec-004/diff-report-20251206-143102.md
2. ✅ Verify merged sections (STRIDE, Performance, API)
3. 💾 Backup available at: .smartspec/backups/spec-004/spec.backup-20251206-143059.md
4. 🚀 Generate implementation plan: smartspec generate-plan spec.md
5. 📋 Generate tasks: smartspec generate-tasks spec.md
```

**Example Output (with custom output dir):**

```bash
smartspec edit spec.md --output-dir=/custom/path
```

```
✅ สร้าง/อัพเดท SPEC เรียบร้อยแล้ว

📁 ไฟล์: specs/feature/spec-005-promo-system/spec.md
📊 Profile: backend-service
🎛️ Mode: standard
✍️ Author: SmartSpec Architect v5.1

📚 Sections Generated: 15

📊 Content Comparison:
  - ✅ Preserved: 10 sections
  - 📝 Modified: 2 sections (merged)
  - ➕ Added: 3 sections
  - ❌ Removed: 0 sections

🔍 Quality Check: 8/8 passed (Score: 92%)

📂 ไฟล์ที่สร้างขึ้น:
  💾 Backup:
     📁 Location: /custom/path/backups/spec-005/spec.backup-20251206-150530.md
     📦 Directory: /custom/path/backups/spec-005
     🆔 SPEC ID: spec-005
     📊 Total backups: 1
     ⏰ Timestamp: 20251206-150530

  📄 Generation Report:
     📁 Location: /custom/path/reports/spec-005/generation-report-20251206-150532.md
     📂 Directory: /custom/path/reports/spec-005

  📊 Diff Report:
     📁 Location: /custom/path/reports/spec-005/diff-report-20251206-150532.md
     ⚠️ Review this file to see what changed

📁 Output Directory Structure:
   Root: /custom/path
   ├─ backups/spec-005/ (backups for this SPEC only)
   ├─ reports/spec-005/ (reports for this SPEC only)
   ├─ registry/ (shared across all SPECs)
   └─ logs/ (shared across all SPECs)

⚡ Quality Breakdown:
  ✅ Security Threat Model (STRIDE): 95%
  ✅ Performance Requirements: 90%
  ✅ API Specification: 92%
  ✅ Data Model & Schema: 90%

🔄 Next steps:
1. 📊 Review diff report: /custom/path/reports/spec-005/diff-report-20251206-150532.md
2. ✅ Verify merged sections (STRIDE, Performance, API)
3. 💾 Backup available at: /custom/path/backups/spec-005/spec.backup-20251206-150530.md
4. 🚀 Generate implementation plan: smartspec generate-plan spec.md
5. 📋 Generate tasks: smartspec generate-tasks spec.md
```

---

## Appendix A: Flag Reference

```
Profiles:
  --profile=basic|backend-service|financial|full

Modes:
  --mode=standard|compact

Security:
  --security=none|basic|stride-basic|stride-full|auto

DI Pattern:
  --di=none|minimal|full|auto
  --no-di (shorthand for --di=none)

Performance:
  --performance=none|basic|full|auto

Domain Hints:
  --domain=healthcare|iot|logistics|ai|fintech|saas|internal

Force Update:
  --force-update=all|stride,config,di,monitoring

Content Preservation (NEW v5.1):
  --preserve-strategy=conservative|balanced|aggressive
  --preserve-sections=stride,performance,di,api-spec,data-model

Output Control:
  --no-backup
  --no-report
  --no-diff (NEW v5.1)
  --output-dir=<path>

Validation:
  --validate-consistency
  --validate-quality (NEW v5.1)
  --no-validation

Other:
  --specindex=<path>
  --nogenerate (dry run)
```

---

## Appendix B: Version History

### v5.1.2 (Latest - December 2025)

**CRITICAL FIXES:**
1. **Header Metadata Management (Step 1.3) - FIXED**
   - ✅ Header metadata NOW ALWAYS preserved (Status, Version, Author, Created, Last Updated)
   - ✅ Automatic version incrementing on updates
   - ✅ Validation for all header fields
   - ✅ Created date NEVER changes, Last Updated always updates

2. **Clean Section Templates (Step 13.2) - FIXED**
   - ✅ NO visible `<!-- @critical -->` tags in generated specs
   - ✅ Meta tags moved to internal registry only
   - ✅ Clean, readable format like v4.0
   - ✅ Simple Technology Stack format restored

3. **Section Separators (Step 13.3) - FIXED**
   - ✅ `---` separators between all major sections
   - ✅ Consistent spacing and formatting
   - ✅ Professional, readable output

4. **Technology Stack Template - FIXED**
   - ✅ Returns to simple, clean format:
     ```markdown
     ## Technology Stack
     
     **Stack A:** Node.js with TypeScript
     
     **Core Technologies:**
     - **Runtime:** Node.js 22.x...
     ```
   - ❌ NO MORE complex multi-line format
   - ❌ NO MORE meta tags cluttering the output

**Quality Improvements:**
- Header metadata validation
- Format consistency checks
- Meta tag removal verification
- Readability score tracking

**Breaking Changes:**
- None - fully backward compatible with v4.0 format

### v5.1.1 (December 2025)

**New Features:**
1. **Output Directory Initialization (Step 1.2)**
   - Complete path validation with security checks
   - Automatic SPEC ID extraction
   - Per-SPEC directory organization
   - Write permission verification

2. **Per-SPEC Backup Organization**
   - Backups separated by SPEC ID
   - No more mixed backups
   - Automatic cleanup keeps last 10 backups per SPEC

3. **Per-SPEC Report Organization**
   - Reports separated by SPEC ID
   - Easy to find all artifacts

4. **Enhanced Final Report**
   - Shows exact backup locations
   - Displays total backup count
   - Clear directory structure

**Improvements:**
- Full `--output-dir` implementation
- Better error messages
- Automatic directory creation
- Backup verification

### v5.1.0 (December 2025)

**New Features:**
1. Content Fingerprinting (Step 8.5)
2. Quality Validation (Step 10.5)
3. Content Comparison & Verification (Step 13.6)
4. Diff Report Generation (Step 13.7)
5. Section-Specific Merge Strategy (Step 13.8)
6. Final Quality Gate (Step 13.9)

**Improvements:**
- Smart merging for STRIDE tables
- Performance metrics preservation
- API endpoint merging
- Data model preservation

### v5.0.0

- Initial release with profiles

---

## Appendix C: Output Directory Organization (NEW v5.1.1)

### Directory Structure

**Default Structure (`--output-dir` not specified):**
```
.smartspec/
├── backups/
│   ├── spec-004/              # Backups for SPEC-004 only
│   │   ├── spec.backup-20251206-143059.md
│   │   ├── spec.backup-20251206-141530.md
│   │   └── spec.backup-20251205-103045.md
│   ├── spec-005/              # Backups for SPEC-005 only
│   │   ├── spec.backup-20251206-150530.md
│   │   └── spec.backup-20251206-120000.md
│   └── spec-core-001/         # Backups for SPEC-CORE-001 only
│       └── spec.backup-20251205-120000.md
├── reports/
│   ├── spec-004/              # Reports for SPEC-004 only
│   │   ├── generation-report-20251206-143102.md
│   │   └── diff-report-20251206-143102.md
│   ├── spec-005/              # Reports for SPEC-005 only
│   │   ├── generation-report-20251206-150532.md
│   │   └── diff-report-20251206-150532.md
│   └── spec-core-001/
│       └── generation-report-20251205-120005.md
├── registry/
│   └── critical-sections-registry.json  # Shared across all SPECs
└── logs/
    └── smartspec.log                    # Shared across all SPECs
```

**Custom Structure (`--output-dir=/custom/path`):**
```
/custom/path/
├── backups/
│   ├── spec-004/
│   │   └── spec.backup-20251206-143059.md
│   └── spec-005/
│       └── spec.backup-20251206-150530.md
├── reports/
│   ├── spec-004/
│   │   ├── generation-report-20251206-143102.md
│   │   └── diff-report-20251206-143102.md
│   └── spec-005/
│       ├── generation-report-20251206-150532.md
│       └── diff-report-20251206-150532.md
├── registry/
│   └── critical-sections-registry.json
└── logs/
    └── smartspec.log
```

### Benefits of Per-SPEC Organization

**Before (v5.0):**
```
.smartspec/backups/
├── spec.backup-20251206-143059.md  # Which SPEC is this? 🤔
├── spec.backup-20251206-141530.md  # Which SPEC is this? 🤔
├── spec.backup-20251206-120000.md  # Which SPEC is this? 🤔
└── spec.backup-20251205-103045.md  # Which SPEC is this? 🤔
```
**Problem:** All backups mixed together, hard to find backups for specific SPEC

**After (v5.1.1):**
```
.smartspec/backups/
├── spec-004/
│   ├── spec.backup-20251206-143059.md  # ✅ SPEC-004 backup
│   └── spec.backup-20251206-141530.md  # ✅ SPEC-004 backup
├── spec-005/
│   └── spec.backup-20251206-120000.md  # ✅ SPEC-005 backup
└── spec-core-001/
    └── spec.backup-20251205-103045.md  # ✅ SPEC-CORE-001 backup
```
**Benefits:**
- ✅ Easy to find all backups for a specific SPEC
- ✅ Clean separation between SPECs
- ✅ Backup cleanup per SPEC (keeps last 10 for each SPEC)
- ✅ No confusion about which backup belongs to which SPEC

### SPEC ID Extraction

**Method 1: From spec path (EDIT mode)**
```
Input: specs/feature/spec-004-financial-system/spec.md
SPEC ID: spec-004
```

**Method 2: From arguments (NEW mode)**
```
Input: "Create spec-005 for promo system"
SPEC ID: spec-005
```

**Method 3: From title**
```
Input: "Create SPEC for payment system"
SPEC ID: spec-payment-system
```

**Method 4: Fallback (timestamp)**
```
Input: "Create SPEC"
SPEC ID: spec-2025-12-06T14-30-59
```

### Output Directory Validation

**Valid Paths:**
- ✅ `.smartspec`
- ✅ `/home/user/project/.smartspec`
- ✅ `/custom/path`
- ✅ `../shared/.smartspec`

**Invalid Paths:**
- ❌ `../../etc/passwd` (path traversal)
- ❌ `/root/.smartspec` (no write permission)
- ❌ `output<>:dir` (invalid characters)
- ❌ Very long paths (>260 chars on Windows, >4096 on Unix)

### Cleanup Policy

**Per-SPEC Backup Cleanup:**
- Keeps last **10 backups** for each SPEC
- Deletes oldest backups when count > 10
- Each SPEC has independent cleanup

**Example:**
```
spec-004 has 12 backups → Keep last 10, delete 2 oldest
spec-005 has 3 backups → Keep all 3
spec-core-001 has 1 backup → Keep it
```

---

## Appendix D: Quality Metrics

### STRIDE Model Quality
- ✅ Must have all 6 categories (S,T,R,I,D,E)
- ✅ Minimum 5 threat entries per category
- ✅ Mitigations defined for each threat

### Performance Requirements Quality
- ✅ Must define P99 latency target
- ✅ Must define TPS/RPS target
- ✅ Must define uptime/SLA target
- ✅ Should include monitoring strategy

### API Specification Quality
- ✅ Must document all endpoints (method + path)
- ✅ Should include request/response schemas
- ✅ Should include authentication details
- ✅ Should include error responses

### Data Model Quality
- ✅ Must define all tables with schema
- ✅ Should include ER diagram
- ✅ Should define indexes
- ✅ Should define constraints and relationships

---

## Appendix E: Format Guidelines (NEW v5.1.2)

### SPEC Format Requirements

**✅ MUST HAVE:**

1. **Header Metadata** (ALWAYS first)
   ```markdown
   # SPEC-{ID}: {Title}
   
   **Status:** {DRAFT|ACTIVE|DEPRECATED}
   **Version:** {X.Y.Z}
   **Author:** {Author Name}
   **Created:** {YYYY-MM-DD}
   **Last Updated:** {YYYY-MM-DD}
   
   **Update Reason:** {Description}
   
   ---
   ```

2. **Section Separators** (between major sections)
   ```markdown
   ## Section Name
   
   Content...
   
   ---
   
   ## Next Section
   ```

3. **Clean Technology Stack**
   ```markdown
   ## Technology Stack
   
   **Stack A:** {Stack Description}
   
   **Core Technologies:**
   - **Runtime:** {Runtime}
   - **Framework:** {Framework}
   - **Database:** {Database}
   
   ---
   ```

**❌ MUST NOT HAVE:**

1. **Visible Meta Tags**
   ```markdown
   ❌ <!-- @critical tech-stack -->
   ❌ **Runtime:** Node.js...
   ❌ <!-- @end-critical -->
   ```

2. **Complex Multi-line Format**
   ```markdown
   ❌ **Runtime:** Node.js 22.x with TypeScript strict mode  
   ❌ **Framework:** Fastify 5.x for high-performance REST API  
   ```

3. **Missing Header Metadata**
   ```markdown
   ❌ # SPEC-005: Promo System
   
   ## Technology Stack    👈 Missing header metadata!
   ```

### Good vs Bad Examples

**✅ GOOD (v5.1.2 - Clean & Readable):**
```markdown
# SPEC-005: Promo System

**Status:** DRAFT
**Version:** 4.0.0
**Author:** SmartSpec Architect v4.0
**Created:** 2025-01-15
**Last Updated:** 2025-12-03

**Update Reason:** Updated to SmartSpec v4.0 format

---

## Technology Stack

**Stack A:** Node.js with TypeScript

**Core Technologies:**
- **Runtime:** Node.js 22.x with TypeScript strict mode
- **Framework:** Fastify 5.x (^5.6.0)
- **Database:** PostgreSQL 16+ with Prisma 6.x (^6.0.0)
- **Queue System:** BullMQ on Redis 7+
- **Validation:** Zod 3.x
- **Language:** TypeScript 5.x

---

## Overview

**Purpose:** A service responsible for creating, managing, and redeeming promotional codes.

**Scope:**
- Promo code creation and management
- Secure redemption process
- Audit logging and fraud detection

---
```

**❌ BAD (v5.1.0 - Cluttered with Meta Tags):**
```markdown
# SPEC-005: Promo System

## Technology Stack

<!-- @critical tech-stack -->
**Runtime:** Node.js 22.x with TypeScript strict mode  
**Framework:** Fastify 5.x for high-performance REST API  
**Database:** PostgreSQL 16+ with Redis 7+ for hierarchical caching  
**ORM:** Prisma 6.x with type-safe database operations  
<!-- @end-critical -->

## Dependency Injection Pattern

<!-- @critical di -->
### Requirements
...
<!-- @end-critical -->
```

**Problems with BAD format:**
1. ❌ No header metadata (Status, Version, Author, etc.)
2. ❌ Visible meta tags clutter the output
3. ❌ No section separators (`---`)
4. ❌ Complex multi-line format hard to read
5. ❌ Not consistent with v4.0 format

### Format Validation Checklist

Before saving spec.md, verify:

- [ ] ✅ Header metadata present (Status, Version, Author, Created, Last Updated)
- [ ] ✅ Section separators (`---`) between major sections
- [ ] ✅ Technology Stack in simple format with `**Stack A:**`
- [ ] ✅ NO visible `<!-- @critical -->` tags
- [ ] ✅ NO complex multi-line format with `  ` (double space) line breaks
- [ ] ✅ Clean, readable markdown like v4.0

### Internal Registry (Meta Tags Storage)

Meta tags are stored separately in `.smartspec/registry/critical-sections-registry.json`:

```json
{
  "spec-005": {
    "version": "5.1.2",
    "last_updated": "2025-12-06T15:30:00Z",
    "critical_sections": {
      "Technology Stack": {
        "start_line": 13,
        "end_line": 24,
        "hash": "a1b2c3d4e5f6",
        "preserve": true,
        "last_modified": "2025-12-03"
      },
      "Dependency Injection Pattern": {
        "start_line": 26,
        "end_line": 150,
        "hash": "g7h8i9j0k1l2",
        "preserve": true,
        "last_modified": "2025-12-03"
      }
    }
  }
}
```

**Benefits:**
- ✅ Tracking critical sections without cluttering spec.md
- ✅ Change detection via content hash
- ✅ Preservation rules stored separately
- ✅ Clean spec.md for human reading

---

Context: $ARGUMENTS

---

# UI Centralization Addendum (Penpot-first)

เอกสารนี้เป็นส่วนเสริมของ **SmartSpec Centralization Contract**  
เพื่อรองรับ **SPEC ประเภท UI** ที่มีข้อกำหนดพิเศษ:

- **UI design source of truth เป็น JSON** (เพื่อใช้กับ Penpot)
- ทีม UI ต้องสามารถแก้ UI ได้ตรงจากไฟล์นี้
- งานของทีม dev ต้องผูกกับ component/logic โดยไม่ทำให้ไฟล์ UI JSON ปน logic

ใช้ addendum นี้วางต่อท้าย contract ในทุก workflow ที่แตะ UI:
- generate-spec
- generate-plan
- generate-tasks
- implement-tasks
- verify-tasks-progress
- generate-tests
- refactor-code
- reverse-to-spec
- reindex-specs
- validate-index
- sync-spec-tasks
- fix-errors
- generate-implement-prompt / generate-cursor-prompt (ในส่วน canonical constraints)

---

## 1) UI File Model

สำหรับ UI spec ให้ถือว่าในโฟลเดอร์ spec มีไฟล์หลัก 2 ชั้น:

1) `spec.md`  
   - narrative, scope, non-goals, UX rules, accessibility, performance targets  
   - อ้างอิงไฟล์ UI JSON เป็น design artifact

2) `ui.json` (หรือชื่อที่ทีมกำหนดใน config)  
   - **Penpot-editable**  
   - เก็บ layout, components mapping, design tokens references  
   - **ห้าม** ใส่ business logic หรือ API behaviour ในไฟล์นี้

> ถ้าทีมต้องการชื่อไฟล์เฉพาะ ให้กำหนดใน config:
```json
{
  "ui_spec": {
    "ui_json_name": "ui.json",
    "component_registry": "ui-component-registry.json"
  }
}
```

---

## 2) Registry เพิ่มเติมสำหรับ UI (แนะนำ)

เพิ่มไฟล์ registry ใหม่แบบ optional:

- `.spec/registry/ui-component-registry.json`

โครงสร้างขั้นต่ำแนะนำ:
```json
{
  "version": "1.0.0",
  "last_updated": "ISO-8601",
  "components": [
    {
      "canonical_name": "UserAvatar",
      "penpot_component_id": "penpot:component:xxx",
      "code_component_path": "src/components/user/UserAvatar.tsx",
      "owned_by_spec": "spec-XXX",
      "aliases": []
    }
  ]
}
```

**กติกา:**
- ชื่อ component ใน tasks/implementation ต้องอ้าง `canonical_name` เป็นค่า default
- ถ้าพบชื่อใหม่:
  - generate-spec / generate-tasks สามารถเพิ่ม entry ใหม่ได้
  - implement / verify ต้องอ่านอย่างเดียว

---

## 3) UI Naming & Separation Rules (MUST)

### 3.1 Separation of Concerns

- `ui.json` = design + structure + bindings
- business logic / data fetching / permissions  
  ต้องอยู่ใน:
  - code components
  - service layer
  - hooks/store
  - หรือ spec.md ในส่วน logic description

### 3.2 Canonical-first

เมื่อ workflow ต้องเสนอชื่อ component:
1) เช็ค `ui-component-registry.json` (ถ้ามี)
2) เช็ค glossary (คำเรียกหน้าจอ/ฟีเจอร์)
3) ถ้ายังไม่มี:
   - เสนอชื่อใหม่แบบ `Proposed`
   - สร้าง task ให้ลงทะเบียน

---

## 4) Workflow-specific Enforcement

### 4.1 generate-spec (UI category)

ต้อง:
- ตรวจ/สร้าง `ui.json` template ขั้นต่ำ (ถ้ายังไม่มี)
- เพิ่ม `ui.json` ลงใน SPEC_INDEX `files` (ถ้าสคีมารองรับ)
- ระบุใน spec.md ว่า:
  - design source-of-truth = ui.json
  - logic อยู่ที่ code layer

### 4.2 generate-tasks

สำหรับ UI spec:
- สร้าง 3 กลุ่มงานแยกกันชัดเจน:

1) **Design tasks (UI team)**
   - ปรับ layout/flow ใน `ui.json` ผ่าน Penpot

2) **Component binding tasks**
   - map Penpot component → code component
   - อัปเดต `ui-component-registry.json` (ถ้าจำเป็น)

3) **Logic tasks (Dev team)**
   - สร้าง/แก้ hooks/services/state
   - ห้ามใส่ logic ใหม่ใน `ui.json`

### 4.3 implement-tasks / refactor-code

- Treat `ui.json` เป็น **design-owned**
- แก้ไขได้เฉพาะเมื่อ tasks ระบุชัดเจน
- ถ้าพบว่า logic ถูกฝังใน ui.json:
  - สร้าง refactor task เพื่อย้าย logic ออก

### 4.4 generate-tests

- อ้าง component canonical names
- สนับสนุนแนวทาง:
  - component tests
  - accessibility checks
  - visual regression (ถ้าทีมใช้)

---

## 5) Index & Validation Rules

### 5.1 SPEC_INDEX

สำหรับ UI spec:
- แนะนำให้มี field เสริมใน entry (ถ้าทีมอนุญาตแบบ additive):
```json
{
  "ui_artifacts": {
    "ui_json_path": "specs/ui/spec-123/ui.json",
    "penpot_project": "optional-string"
  }
}
```

ถ้าไม่เพิ่ม schema:
- ให้ใช้ `files` list แทน

### 5.2 validate-index / global-registry-audit

ต้องตรวจอย่างน้อย:
- UI spec ที่ category=ui ต้องมี `ui.json`
- ชื่อ component ที่ spec/tasks อ้าง ต้องสอดคล้องกับ registry

---

## 6) ผลลัพธ์ที่ต้องการ

- ทีม UI แก้ UI ได้โดยไม่ชนกับ dev logic
- ลดการแตกชื่อ component ซ้ำซ้อน
- UI specs กลายเป็นส่วนหนึ่งของ centralization ไม่ใช่โลกคู่ขนาน
