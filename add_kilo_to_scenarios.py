#!/usr/bin/env python3
"""
Add Kilo Code examples to all scenarios in WORKFLOW_SCENARIOS_GUIDE.md
that currently only have CLI examples.

For each CLI command block, generate a corresponding Kilo Code block with:
1. .md extension added to workflow name
2. --platform kilo flag added at the end
"""

import re
from pathlib import Path

def convert_cli_to_kilo(cli_command):
    """Convert a CLI command to Kilo Code syntax."""
    # Add .md extension to workflow name
    kilo_command = re.sub(r'(/smartspec_\w+)(\s|\\)', r'\1.md\2', cli_command)
    
    # Add --platform kilo at the end (before closing)
    lines = kilo_command.rstrip().split('\n')
    if lines:
        # Add to last line
        lines[-1] = lines[-1].rstrip().rstrip('\\').rstrip() + ' \\\n  --platform kilo'
    
    return '\n'.join(lines)

def process_scenarios_guide(input_path, output_path):
    """Process the scenarios guide and add Kilo Code examples."""
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all CLI code blocks that are followed by "**Parameter Explanation:**" or "**Best Practices**"
    # This indicates they are workflow commands without Kilo Code counterparts
    
    # Pattern: **CLI:** followed by ```bash...``` then NOT followed by **Kilo Code:**
    # Use lookahead to ensure no Kilo Code block follows within next 20 characters
    pattern = r'(\*\*CLI:\*\*\s*\n```bash\n)(.*?)(```\n)(?!\s*\*\*Kilo Code:\*\*)'
    
    def add_kilo_block(match):
        """Add Kilo Code block after CLI block."""
        prefix = match.group(1)
        cli_command = match.group(2)
        suffix = match.group(3)
        
        # Generate Kilo Code version
        kilo_command = convert_cli_to_kilo(cli_command)
        
        # Return CLI block + Kilo block
        return (f"{prefix}{cli_command}{suffix}\n"
                f"**Kilo Code:**\n```bash\n{kilo_command}\n```\n")
    
    # Apply the transformation
    new_content = re.sub(pattern, add_kilo_block, content, flags=re.DOTALL)
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # Count how many Kilo Code blocks were added
    cli_count = len(re.findall(r'\*\*CLI:\*\*', content))
    kilo_count_before = len(re.findall(r'\*\*Kilo Code:\*\*', content))
    kilo_count_after = len(re.findall(r'\*\*Kilo Code:\*\*', new_content))
    added = kilo_count_after - kilo_count_before
    
    # Verify no duplicates were created
    if kilo_count_after > cli_count:
        print(f"⚠️  Warning: More Kilo Code blocks ({kilo_count_after}) than CLI blocks ({cli_count})")
        print(f"   This may indicate duplicates were created.")
        return 1
    
    print(f"CLI blocks found: {cli_count}")
    print(f"Kilo Code blocks before: {kilo_count_before}")
    print(f"Kilo Code blocks after: {kilo_count_after}")
    print(f"Kilo Code blocks added: {added}")

def main():
    input_path = Path(".smartspec/WORKFLOW_SCENARIOS_GUIDE.md")
    output_path = Path(".smartspec/WORKFLOW_SCENARIOS_GUIDE.md")
    
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        return 1
    
    print(f"Processing {input_path}...")
    process_scenarios_guide(input_path, output_path)
    print(f"✅ Updated {output_path}")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
