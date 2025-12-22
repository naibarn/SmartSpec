#!/usr/bin/env python3
"""
SmartSpec Theme Manager
Manages design system themes for A2UI applications
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class ThemeManager:
    """Manages theme.json operations"""
    
    def __init__(self, theme_file: str = ".spec/theme.json"):
        self.theme_file = Path(theme_file)
        self.theme: Dict[str, Any] = {}
        
    def load_theme(self) -> Dict[str, Any]:
        """Load theme from file"""
        if not self.theme_file.exists():
            raise FileNotFoundError(f"Theme file not found: {self.theme_file}")
        
        with open(self.theme_file, 'r', encoding='utf-8') as f:
            self.theme = json.load(f)
        
        return self.theme
    
    def save_theme(self) -> None:
        """Save theme to file"""
        self.theme_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.theme_file, 'w', encoding='utf-8') as f:
            json.dump(self.theme, f, indent=2, ensure_ascii=False)
    
    def init_theme(self) -> Dict[str, Any]:
        """Initialize a new theme with default values"""
        default_theme = {
            "$schema": "https://smartspec.dev/schemas/theme-v1.json",
            "version": "1.0.0",
            "name": "SmartSpec Default Theme",
            "description": "Default design system theme for SmartSpec A2UI applications",
            "tokens": {
                "colors": {
                    "primary": {
                        "50": "#f0f9ff",
                        "500": "#0ea5e9",
                        "900": "#0c4a6e"
                    },
                    "neutral": {
                        "50": "#fafafa",
                        "500": "#737373",
                        "900": "#171717"
                    }
                },
                "typography": {
                    "fontFamily": {
                        "sans": "Inter, system-ui, sans-serif"
                    },
                    "fontSize": {
                        "base": "1rem",
                        "lg": "1.125rem",
                        "xl": "1.25rem"
                    }
                },
                "spacing": {
                    "0": "0",
                    "1": "0.25rem",
                    "2": "0.5rem",
                    "4": "1rem",
                    "8": "2rem"
                }
            },
            "components": {},
            "metadata": {
                "createdAt": "2025-12-22T00:00:00Z",
                "author": "SmartSpec",
                "source": "manual"
            }
        }
        
        self.theme = default_theme
        self.save_theme()
        
        return self.theme
    
    def get_token_by_path(self, path: str) -> Any:
        """Get token value by dot-notation path"""
        parts = path.split('.')
        value = self.theme.get('tokens', {})
        
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return None
        
        return value
    
    def set_token_by_path(self, path: str, value: Any) -> None:
        """Set token value by dot-notation path"""
        parts = path.split('.')
        
        # Ensure tokens section exists
        if 'tokens' not in self.theme:
            self.theme['tokens'] = {}
        
        # Navigate to parent
        current = self.theme['tokens']
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Set value
        current[parts[-1]] = value
    
    def update_token(self, token_path: str, token_value: str) -> Tuple[bool, str]:
        """Update a token value"""
        try:
            self.load_theme()
            
            # Validate path exists
            old_value = self.get_token_by_path(token_path)
            
            # Set new value
            self.set_token_by_path(token_path, token_value)
            
            # Validate theme
            is_valid, errors = self.validate_theme()
            if not is_valid:
                return False, f"Validation failed: {', '.join(errors)}"
            
            self.save_theme()
            
            return True, f"Updated {token_path}: {old_value} → {token_value}"
        
        except Exception as e:
            return False, str(e)
    
    def add_variant(self, component: str, variant_name: str, variant_spec: Dict[str, Any]) -> Tuple[bool, str]:
        """Add a component variant"""
        try:
            self.load_theme()
            
            # Ensure components section exists
            if 'components' not in self.theme:
                self.theme['components'] = {}
            
            # Ensure component exists
            if component not in self.theme['components']:
                self.theme['components'][component] = {"variants": {}}
            
            # Ensure variants section exists
            if 'variants' not in self.theme['components'][component]:
                self.theme['components'][component]['variants'] = {}
            
            # Check if variant already exists
            if variant_name in self.theme['components'][component]['variants']:
                return False, f"Variant '{variant_name}' already exists for component '{component}'"
            
            # Add variant
            self.theme['components'][component]['variants'][variant_name] = variant_spec
            
            # Validate theme
            is_valid, errors = self.validate_theme()
            if not is_valid:
                return False, f"Validation failed: {', '.join(errors)}"
            
            self.save_theme()
            
            return True, f"Added variant '{variant_name}' to component '{component}'"
        
        except Exception as e:
            return False, str(e)
    
    def remove_variant(self, component: str, variant_name: str) -> Tuple[bool, str]:
        """Remove a component variant"""
        try:
            self.load_theme()
            
            # Check if component exists
            if component not in self.theme.get('components', {}):
                return False, f"Component '{component}' not found"
            
            # Check if variant exists
            if variant_name not in self.theme['components'][component].get('variants', {}):
                return False, f"Variant '{variant_name}' not found in component '{component}'"
            
            # Remove variant
            del self.theme['components'][component]['variants'][variant_name]
            
            self.save_theme()
            
            return True, f"Removed variant '{variant_name}' from component '{component}'"
        
        except Exception as e:
            return False, str(e)
    
    def validate_theme(self) -> Tuple[bool, List[str]]:
        """Validate theme structure and token references"""
        errors = []
        
        # Check required fields
        required_fields = ['version', 'name', 'tokens']
        for field in required_fields:
            if field not in self.theme:
                errors.append(f"Missing required field: {field}")
        
        # Validate token references in components
        if 'components' in self.theme:
            errors.extend(self._validate_token_references(self.theme['components']))
        
        return len(errors) == 0, errors
    
    def _validate_token_references(self, obj: Any, path: str = "") -> List[str]:
        """Recursively validate token references"""
        errors = []
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_path = f"{path}.{key}" if path else key
                errors.extend(self._validate_token_references(value, current_path))
        
        elif isinstance(obj, str):
            # Check for token references like {colors.primary.500}
            token_refs = re.findall(r'\{([^}]+)\}', obj)
            for ref in token_refs:
                token_value = self.get_token_by_path(ref)
                if token_value is None:
                    errors.append(f"Invalid token reference at {path}: {{{ref}}}")
        
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                errors.extend(self._validate_token_references(item, f"{path}[{i}]"))
        
        return errors
    
    def export_css(self, output_file: str) -> Tuple[bool, str]:
        """Export theme as CSS custom properties"""
        try:
            self.load_theme()
            
            css_lines = [":root {"]
            
            # Export color tokens
            if 'colors' in self.theme.get('tokens', {}):
                css_lines.append("  /* Colors */")
                css_lines.extend(self._export_tokens_to_css(self.theme['tokens']['colors'], 'color'))
            
            # Export typography tokens
            if 'typography' in self.theme.get('tokens', {}):
                css_lines.append("\n  /* Typography */")
                css_lines.extend(self._export_tokens_to_css(self.theme['tokens']['typography'], 'typography'))
            
            # Export spacing tokens
            if 'spacing' in self.theme.get('tokens', {}):
                css_lines.append("\n  /* Spacing */")
                css_lines.extend(self._export_tokens_to_css(self.theme['tokens']['spacing'], 'spacing'))
            
            css_lines.append("}")
            
            # Write to file
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(css_lines))
            
            return True, f"Exported theme to {output_file}"
        
        except Exception as e:
            return False, str(e)
    
    def _export_tokens_to_css(self, tokens: Dict[str, Any], prefix: str, parent_key: str = "") -> List[str]:
        """Recursively export tokens to CSS variables"""
        lines = []
        
        for key, value in tokens.items():
            css_var_name = f"--{prefix}-{parent_key}-{key}" if parent_key else f"--{prefix}-{key}"
            css_var_name = css_var_name.replace('_', '-')
            
            if isinstance(value, dict):
                lines.extend(self._export_tokens_to_css(value, prefix, f"{parent_key}-{key}" if parent_key else key))
            else:
                lines.append(f"  {css_var_name}: {value};")
        
        return lines
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get theme statistics"""
        self.load_theme()
        
        stats = {
            "version": self.theme.get("version", "unknown"),
            "name": self.theme.get("name", "unknown"),
            "token_count": self._count_tokens(self.theme.get("tokens", {})),
            "component_count": len(self.theme.get("components", {})),
            "variant_count": sum(
                len(comp.get("variants", {}))
                for comp in self.theme.get("components", {}).values()
            )
        }
        
        return stats
    
    def _count_tokens(self, obj: Any) -> int:
        """Recursively count leaf tokens"""
        if isinstance(obj, dict):
            return sum(self._count_tokens(v) for v in obj.values())
        else:
            return 1


def main():
    """Main CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SmartSpec Theme Manager")
    parser.add_argument("--action", required=True, choices=[
        "init", "update-token", "add-variant", "remove-variant",
        "validate", "export-css", "export-scss"
    ])
    parser.add_argument("--theme-file", default=".spec/theme.json")
    parser.add_argument("--token-path")
    parser.add_argument("--token-value")
    parser.add_argument("--component")
    parser.add_argument("--variant-name")
    parser.add_argument("--variant-spec")
    parser.add_argument("--output-file")
    
    args = parser.parse_args()
    
    manager = ThemeManager(args.theme_file)
    
    try:
        if args.action == "init":
            theme = manager.init_theme()
            print(f"✅ Initialized theme: {theme['name']}")
            stats = manager.get_statistics()
            print(f"📊 Tokens: {stats['token_count']}, Components: {stats['component_count']}")
        
        elif args.action == "update-token":
            if not args.token_path or not args.token_value:
                print("❌ Error: --token-path and --token-value are required")
                sys.exit(1)
            
            success, message = manager.update_token(args.token_path, args.token_value)
            if success:
                print(f"✅ {message}")
            else:
                print(f"❌ Error: {message}")
                sys.exit(1)
        
        elif args.action == "add-variant":
            if not args.component or not args.variant_name or not args.variant_spec:
                print("❌ Error: --component, --variant-name, and --variant-spec are required")
                sys.exit(1)
            
            variant_spec = json.loads(args.variant_spec)
            success, message = manager.add_variant(args.component, args.variant_name, variant_spec)
            if success:
                print(f"✅ {message}")
            else:
                print(f"❌ Error: {message}")
                sys.exit(1)
        
        elif args.action == "remove-variant":
            if not args.component or not args.variant_name:
                print("❌ Error: --component and --variant-name are required")
                sys.exit(1)
            
            success, message = manager.remove_variant(args.component, args.variant_name)
            if success:
                print(f"✅ {message}")
            else:
                print(f"❌ Error: {message}")
                sys.exit(1)
        
        elif args.action == "validate":
            manager.load_theme()
            is_valid, errors = manager.validate_theme()
            
            if is_valid:
                print("✅ Theme is valid")
                stats = manager.get_statistics()
                print(f"📊 Tokens: {stats['token_count']}, Components: {stats['component_count']}, Variants: {stats['variant_count']}")
            else:
                print("❌ Theme validation failed:")
                for error in errors:
                    print(f"  - {error}")
                sys.exit(1)
        
        elif args.action == "export-css":
            if not args.output_file:
                print("❌ Error: --output-file is required")
                sys.exit(1)
            
            success, message = manager.export_css(args.output_file)
            if success:
                print(f"✅ {message}")
            else:
                print(f"❌ Error: {message}")
                sys.exit(1)
        
        elif args.action == "export-scss":
            print("❌ SCSS export not yet implemented")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
