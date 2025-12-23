#!/usr/bin/env python3
import os
import re
from pathlib import Path

workflow_dir = Path(".smartspec/workflows")
output_file = Path(".smartspec/WORKFLOW_PARAMETERS_REFERENCE.md")

def extract_workflow_info(filepath):
    """Extract key information from a workflow file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    info = {
        'name': filepath.stem,
        'description': '',
        'version': '',
        'parameters': [],
        'universal_flags': [],
        'examples': []
    }
    
    desc_match = re.search(r'description:\s*(.+)', content)
    if desc_match:
        info['description'] = desc_match.group(1).strip()
    
    version_match = re.search(r'version:\s*([0-9.]+)', content)
    if version_match:
        info['version'] = version_match.group(1)

    # Process both Inputs and Flags sections
    for section_name in ["Inputs", "Flags"]:
        section_pattern = re.compile(r"##\s+" + section_name + r".*?(?=##|\Z)", re.DOTALL | re.IGNORECASE)
        section_match = section_pattern.search(content)
        if not section_match:
            continue

        section_content = section_match.group(0)
        
        # Find parameters within subsections like ### Required, ### Optional, ### Workflow-specific flags
        param_lines = re.findall(r"-\s+`(--[a-z0-9_-]+)[^`]*`\s*(?:\((required|optional)\))?:?\s*(.*)", section_content, re.IGNORECASE)
        for param_name, status, description in param_lines:
            # Avoid duplicates
            if any(p['name'] == param_name for p in info['parameters']):
                continue

            info['parameters'].append({
                'name': param_name.strip(),
                'status': status.strip().capitalize() if status else 'Optional',
                'description': description.strip().lstrip(': ')
            })

    # Extract universal flags
    universal_section = re.search(r'###\s+Universal flags.*?(?=###|\Z)', content, re.DOTALL)
    if universal_section:
        universal_flags = re.findall(r'`(--[a-z0-9_-]+)`', universal_section.group(0))
        info['universal_flags'] = list(set(universal_flags))
    
    # Extract code examples
    code_blocks = re.findall(r'```bash\n(.+?)```', content, re.DOTALL)
    info['examples'] = [block.strip() for block in code_blocks if 'smartspec' in block][:2]
    
    return info

def main():
    workflows = sorted(workflow_dir.glob("*.md"))
    
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("# SmartSpec Workflow Parameters Reference (v6.2.0)\n\n")
        out.write("This document provides a comprehensive reference for all parameters used in the 40 SmartSpec workflows. Each entry includes a description, version, parameter details, and usage examples.\n\n")
        out.write("---\n\n")
        
        for wf_path in workflows:
            print(f"Processing {wf_path.name}...")
            info = extract_workflow_info(wf_path)
            
            out.write(f"## {info['name']}\n\n")
            
            if info['description']:
                out.write(f"**Description:** {info['description']}\n\n")
            
            if info['version']:
                out.write(f"**Version:** {info['version']}\n\n")

            if info['parameters']:
                out.write("### Parameters\n\n")
                out.write("| Parameter | Status | Description |\n")
                out.write("|---|---|---|\n")
                for param in sorted(info['parameters'], key=lambda x: x['name']):
                    out.write(f"| `{param['name']}` | {param['status']} | {param['description']} |\n")
                out.write("\n")

            if info['universal_flags']:
                out.write("### Universal Flags (Supported)\n\n")
                out.write("These flags are supported by this workflow:\n")
                flags_list = ", ".join([f"`{f}`" for f in sorted(info['universal_flags'])])
                out.write(f"{flags_list}\n\n")

            if info['examples']:
                out.write("### Usage Examples\n\n")
                for i, example in enumerate(info['examples'], 1):
                    # Determine if this is CLI or Kilo Code
                    # Kilo Code has .md extension in workflow name (e.g., /smartspec_xxx.md)
                    is_kilo = re.search(r'/smartspec_\w+\.md', example) is not None
                    label = "Kilo Code" if is_kilo else "CLI"
                    
                    # Add --platform kilo if it's Kilo Code and doesn't have it
                    if is_kilo and '--platform kilo' not in example:
                        example = example.rstrip() + ' \\\n  --platform kilo'
                    
                    out.write(f"**{label}:**\n```bash\n{example}\n```\n\n")
            
            out.write("---\n\n")
    
    print(f"\nParameter reference created: {output_file}")
    print(f"Total workflows processed: {len(workflows)}")

if __name__ == "__main__":
    main()
