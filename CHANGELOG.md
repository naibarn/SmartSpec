# Changelog

All notable changes to SmartSpec will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.2.0] - 2024-12-05

### Added
- **Google Antigravity Support**: Full support for Google's agentic IDE platform
  - Workflows installed to `.agent/workflows/`
  - Markdown format (same as Kilo/Roo/Claude)
  - Auto-detection during installation
- **Gemini CLI Support**: Full support for Google's terminal-based AI coding assistant
  - Commands installed to `.gemini/commands/`
  - Automatic Markdown to TOML conversion
  - Auto-detection during installation
- **Markdown to TOML Converter**: New utility script for converting workflows
  - Located at `.smartspec/scripts/convert-md-to-toml.sh`
  - Automatically used during Gemini CLI installation
  - Can be used standalone for manual conversions

### Changed
- **Installation Menu**: Updated to include 6 platform options
  - Added option 4: Google Antigravity
  - Added option 5: Gemini CLI
  - Updated option 6: All platforms (now includes all 5 platforms)
- **Sync Script**: Enhanced to support new platforms
  - Antigravity: Direct Markdown copy
  - Gemini CLI: Automatic TOML conversion during sync
- **Version**: Bumped from v5.0 to v5.2

### Fixed
- None

### Documentation
- Updated README.md with new platform information
- Added platform-specific installation notes
- Created comprehensive platform expansion plan document

## [5.1.0] - 2024-12-05

### Added
- **Complete Kilo Code Integration**: All 5 modes integrated
  - Ask Mode
  - Architect Mode
  - Code Mode
  - Debug Mode
  - Orchestrator Mode
- **Enhanced README Documentation**: Added "What SmartSpec Does" section
  - Clear explanation of 6 core capabilities
  - Better onboarding for new users
- **Comprehensive Documentation**:
  - ASK_MODE_GUIDE.md
  - KILO_CODE_COMPLETE_GUIDE.md
  - Cross-references between all guides

### Changed
- **Workflows Enhanced**: Added `--kilocode` flag support to 4 workflows
  - smartspec_implement_tasks
  - smartspec_fix_errors
  - smartspec_refactor_code
  - smartspec_generate_tests

## [5.0.0] - 2024-12-03

### Added
- Initial SmartSpec V5 release
- Multi-platform support (Kilo Code, Roo Code, Claude Code)
- Core workflow system
- SPEC → PLAN → TASKS → IMPLEMENT process
- Profile system (standard, financial, healthcare, ecommerce, iot)
- Domain-specific optimizations
- Comprehensive documentation

### Changed
- Complete rewrite from V4
- New installation system
- Enhanced workflow structure

## Links

- [5.2.0]: https://github.com/naibarn/SmartSpec/releases/tag/v5.2.0
- [5.1.0]: https://github.com/naibarn/SmartSpec/releases/tag/smartspec%2Cvibecoding%2Ccodingbyai
- [5.0.0]: https://github.com/naibarn/SmartSpec/releases/tag/v5.0.0
