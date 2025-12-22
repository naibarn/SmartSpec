#!/usr/bin/env python3
"""
Add Flags/Inputs sections to SmartSpec workflow files that are missing them.

This script:
1. Reads each workflow file
2. Extracts metadata (name, version, parameters from Invocation examples)
3. Generates a comprehensive Flags section
4. Inserts it at the appropriate location (after Invocation, before Output/Behavior)
5. Preserves all existing content
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Universal flags that all workflows support
UNIVERSAL_FLAGS = {
    "--config": {
        "required": False,
        "description": "Path to custom config file (default: `.spec/smartspec.config.yaml`)"
    },
    "--lang": {
        "required": False,
        "description": "Output language (`th` for Thai, `en` for English, `auto` for automatic detection)"
    },
    "--platform": {
        "required": False,
        "description": "Platform mode (`cli` for CLI, `kilo` for Kilo Code, `ci` for CI/CD, `other` for custom integrations)"
    },
    "--out": {
        "required": False,
        "description": "Base output directory for reports and generated files (must pass safety checks)"
    },
    "--json": {
        "required": False,
        "description": "Output results in JSON format for machine parsing and automation"
    },
    "--quiet": {
        "required": False,
        "description": "Suppress non-essential output, showing only errors and critical information"
    }
}

def extract_workflow_info(content: str) -> Dict:
    """Extract workflow metadata from content."""
    info = {
        "name": "",
        "version": "",
        "parameters": {}
    }
    
    # Extract name from frontmatter
    name_match = re.search(r'^name:\s*(/smartspec_\w+)', content, re.MULTILINE)
    if name_match:
        info["name"] = name_match.group(1)
    
    # Extract version from frontmatter
    version_match = re.search(r'^version:\s*([\d.]+)', content, re.MULTILINE)
    if version_match:
        info["version"] = version_match.group(1)
    
    return info

def extract_parameters_from_invocation(content: str) -> Dict[str, Dict]:
    """Extract parameters from Invocation section examples."""
    parameters = {}
    
    # Find Invocation section
    invocation_match = re.search(r'## Invocation.*?(?=^##|\Z)', content, re.DOTALL | re.MULTILINE)
    if not invocation_match:
        return parameters
    
    invocation_section = invocation_match.group(0)
    
    # Extract all flags from code blocks
    code_blocks = re.findall(r'```(?:bash)?\n(.*?)```', invocation_section, re.DOTALL)
    
    for block in code_blocks:
        # Find all --flag patterns
        flag_matches = re.findall(r'(--[\w-]+)(?:\s+<([^>]+)>|\s+(\w+))?', block)
        
        for match in flag_matches:
            flag = match[0]
            param_type = match[1] or match[2] or ""
            
            # Determine if required (flags in square brackets are optional)
            is_optional = f'[{flag}' in block or f'[ {flag}' in block
            
            if flag not in parameters:
                parameters[flag] = {
                    "required": not is_optional,
                    "type": param_type,
                    "description": ""
                }
    
    return parameters

def generate_flags_section(workflow_name: str, parameters: Dict[str, Dict]) -> str:
    """Generate a comprehensive Flags section."""
    
    # Separate workflow-specific and universal flags
    workflow_flags = {k: v for k, v in parameters.items() if k not in UNIVERSAL_FLAGS}
    
    section = []
    section.append("---")
    section.append("")
    section.append("## Flags")
    section.append("")
    
    # Universal flags subsection
    section.append("### Universal flags (must support)")
    section.append("")
    section.append("All SmartSpec workflows support these universal flags:")
    section.append("")
    section.append("| Flag | Required | Description |")
    section.append("|---|---|---|")
    
    for flag, info in UNIVERSAL_FLAGS.items():
        req = "No" if not info["required"] else "Yes"
        desc = info["description"]
        section.append(f"| `{flag}` | {req} | {desc} |")
    
    section.append("")
    
    # Workflow-specific flags subsection
    if workflow_flags:
        section.append("### Workflow-specific flags")
        section.append("")
        section.append(f"Flags specific to `{workflow_name}`:")
        section.append("")
        section.append("| Flag | Required | Description |")
        section.append("|---|---|---|")
        
        for flag, info in sorted(workflow_flags.items()):
            req = "Yes" if info["required"] else "No"
            desc = info.get("description", "")
            if not desc:
                # Generate basic description from flag name
                flag_name = flag.replace("--", "").replace("-", " ").title()
                if info.get("type"):
                    desc = f"{flag_name} parameter (type: {info['type']})"
                else:
                    desc = f"{flag_name} parameter"
            section.append(f"| `{flag}` | {req} | {desc} |")
        
        section.append("")
    
    # Notes subsection
    section.append("### Flag usage notes")
    section.append("")
    section.append("- **Config-first approach:** Prefer setting defaults in `.spec/smartspec.config.yaml` to minimize command-line flags")
    section.append("- **Positional arguments:** When supported, use positional arguments for primary inputs (e.g., spec path) instead of flags")
    section.append("- **Boolean flags:** Flags without values are boolean (presence = true, absence = false)")
    section.append("- **Path safety:** All path arguments must pass safety validation (no directory traversal, symlink escape, or absolute paths outside project)")
    section.append("- **Secret handling:** Never pass secrets as flag values; use `env:VAR_NAME` references or config file")
    section.append("")
    
    return "\n".join(section)

def find_insertion_point(content: str) -> int:
    """Find the best location to insert Flags section."""
    
    # Try to find Invocation section end
    invocation_match = re.search(r'## Invocation.*?(?=^---)', content, re.DOTALL | re.MULTILINE)
    if invocation_match:
        # Insert after the --- that follows Invocation
        end_pos = invocation_match.end()
        # Find the next --- after Invocation
        next_section = re.search(r'^---', content[end_pos:], re.MULTILINE)
        if next_section:
            return end_pos + next_section.end()
    
    # Fallback: insert before Output section
    output_match = re.search(r'^## Output', content, re.MULTILINE)
    if output_match:
        return output_match.start()
    
    # Fallback: insert before Behavior section
    behavior_match = re.search(r'^## (?:\d+\))?\s*Behavior', content, re.MULTILINE)
    if behavior_match:
        return behavior_match.start()
    
    # Last resort: insert before "End of workflow doc"
    end_match = re.search(r'^# End of workflow doc', content, re.MULTILINE)
    if end_match:
        return end_match.start()
    
    # If nothing found, insert at end
    return len(content)

def add_flags_section(filepath: Path) -> bool:
    """Add Flags section to a workflow file."""
    
    print(f"\nProcessing: {filepath.name}")
    
    # Read file
    content = filepath.read_text(encoding='utf-8')
    
    # Check if already has Flags or Inputs section
    if re.search(r'^## (?:Flags|Inputs)', content, re.MULTILINE):
        print(f"  ✅ Already has Flags/Inputs section, skipping")
        return False
    
    # Extract workflow info
    info = extract_workflow_info(content)
    if not info["name"]:
        print(f"  ⚠️  Could not extract workflow name, skipping")
        return False
    
    print(f"  📝 Workflow: {info['name']} (v{info['version']})")
    
    # Extract parameters from Invocation section
    parameters = extract_parameters_from_invocation(content)
    print(f"  🔍 Found {len(parameters)} parameters in Invocation section")
    
    # Generate Flags section
    flags_section = generate_flags_section(info["name"], parameters)
    
    # Find insertion point
    insert_pos = find_insertion_point(content)
    
    # Insert Flags section
    new_content = content[:insert_pos] + "\n" + flags_section + "\n" + content[insert_pos:]
    
    # Write back
    filepath.write_text(new_content, encoding='utf-8')
    
    print(f"  ✅ Added Flags section at position {insert_pos}")
    return True

def main():
    """Main function."""
    
    # Read list of files to process
    missing_files_path = Path("/home/ubuntu/SmartSpec/missing_flags_sections.txt")
    if not missing_files_path.exists():
        print("❌ missing_flags_sections.txt not found")
        return 1
    
    missing_files = missing_files_path.read_text().strip().split("\n")
    
    print(f"📋 Processing {len(missing_files)} workflow files...")
    
    workflows_dir = Path("/home/ubuntu/SmartSpec/.smartspec/workflows")
    
    updated_count = 0
    skipped_count = 0
    
    for filename in missing_files:
        filepath = workflows_dir / filename.strip()
        
        if not filepath.exists():
            print(f"\n⚠️  File not found: {filename}")
            skipped_count += 1
            continue
        
        if add_flags_section(filepath):
            updated_count += 1
        else:
            skipped_count += 1
    
    print(f"\n" + "="*60)
    print(f"✅ Updated: {updated_count} workflows")
    print(f"⏭️  Skipped: {skipped_count} workflows")
    print(f"📊 Total: {len(missing_files)} workflows")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
