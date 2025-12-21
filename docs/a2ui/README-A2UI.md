# SmartSpec A2UI Integration (Optional)

## Overview

This directory contains **optional** dependencies for SmartSpec's A2UI (Agent-to-User Interface) integration. A2UI enables AI-driven generation of rich, interactive user interfaces using a declarative JSON format.

**Important:** A2UI features are **completely optional**. If you don't need UI generation workflows, you can safely ignore this directory. All existing SmartSpec workflows will continue to work without any A2UI dependencies installed.

---

## When to Install A2UI Dependencies

Install A2UI dependencies only if you plan to use these workflows:

- `smartspec_generate_ui_spec` - Generate UI specifications from requirements
- `smartspec_implement_ui_from_spec` - Generate platform-specific UI code
- `smartspec_verify_ui_implementation` - Verify UI implementation compliance
- `smartspec_manage_ui_catalog` - Manage UI component catalogs
- `smartspec_generate_multiplatform_ui` - Generate cross-platform UIs
- `smartspec_ui_agent` - Interactive UI design agent

---

## Installation

### Option 1: Using the Provided Package File

```bash
# From the SmartSpec root directory
cd /path/to/SmartSpec
npm install --prefix . --package-lock-only a2ui-package.json
```

### Option 2: Manual Installation

```bash
# Install required dependencies
npm install @a2ui/core@^0.8.0 lit@^3.0.0

# Install optional dependencies (as needed)
npm install --save-dev @a2ui/lit-renderer@^0.8.0
npm install --save-dev @a2ui/flutter-renderer@^0.8.0
npm install --save-dev @a2ui/testing@^0.8.0
```

### Option 3: Copy and Rename

```bash
# Copy the package file to package.json (if you don't have one)
cp a2ui-package.json package.json
npm install
```

---

## Enabling A2UI Features

After installing dependencies, enable A2UI in your SmartSpec configuration:

**File:** `.spec/smartspec.config.yaml`

```yaml
a2ui:
  enabled: true  # Change from false to true
  version: "0.8"
  # ... other settings
```

---

## Verification

Check that A2UI dependencies are installed correctly:

```bash
npm list @a2ui/core lit
```

Expected output:
```
smartspec-a2ui@1.0.0
├── @a2ui/core@0.8.0
└── lit@3.0.0
```

---

## Uninstallation

If you decide you don't need A2UI features:

1. **Remove dependencies:**
   ```bash
   npm uninstall @a2ui/core lit @a2ui/lit-renderer @a2ui/flutter-renderer @a2ui/testing
   ```

2. **Disable in config:**
   ```yaml
   a2ui:
     enabled: false
   ```

3. **Delete files (optional):**
   ```bash
   rm -f a2ui-package.json README-A2UI.md
   rm -f .spec/ui-catalog.json
   ```

---

## Zero-Impact Guarantee

**SmartSpec's A2UI integration is designed with zero impact on existing workflows:**

✅ **Opt-in only** - A2UI features are disabled by default  
✅ **No breaking changes** - All existing workflows work unchanged  
✅ **Graceful degradation** - If dependencies are missing, A2UI workflows will fail gracefully with clear error messages  
✅ **Independent** - A2UI workflows don't interfere with non-UI workflows  

---

## Documentation

- **A2UI Official Docs:** https://a2ui.org
- **A2UI GitHub:** https://github.com/google/A2UI
- **SmartSpec A2UI Integration Report:** `A2UI_SmartSpec_Integration_Report.md`
- **A2UI Workflow Specifications:** `a2ui_workflow_specifications.md`

---

## Support

For questions or issues related to A2UI integration:

1. Check the SmartSpec documentation
2. Review A2UI official documentation
3. Open an issue on GitHub: https://github.com/naibarn/SmartSpec/issues

---

## License

Apache-2.0 (same as SmartSpec and A2UI)

---

**Last Updated:** December 22, 2025  
**SmartSpec Version:** v6.3.3  
**A2UI Version:** v0.8
