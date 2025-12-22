#!/usr/bin/env python3
"""
SmartSpec Penpot Token Importer
Imports design tokens from Penpot into SmartSpec theme
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class PenpotTokenImporter:
    """Imports design tokens from Penpot"""
    
    def __init__(self, theme_file: str = ".spec/theme.json"):
        self.theme_file = Path(theme_file)
        self.theme: Dict[str, Any] = {}
        
    def load_theme(self) -> Dict[str, Any]:
        """Load existing theme or create new one"""
        if self.theme_file.exists():
            with open(self.theme_file, 'r', encoding='utf-8') as f:
                self.theme = json.load(f)
        else:
            self.theme = {
                "$schema": "https://smartspec.dev/schemas/theme-v1.json",
                "version": "1.0.0",
                "name": "Imported from Penpot",
                "description": "Design tokens imported from Penpot",
                "tokens": {},
                "components": {},
                "metadata": {
                    "source": "penpot",
                    "createdAt": "2025-12-22T00:00:00Z"
                }
            }
        
        return self.theme
    
    def save_theme(self) -> None:
        """Save theme to file"""
        self.theme_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.theme_file, 'w', encoding='utf-8') as f:
            json.dump(self.theme, f, indent=2, ensure_ascii=False)
    
    def import_from_file(self, input_file: str, merge_strategy: str = "merge") -> Tuple[bool, Dict[str, Any]]:
        """Import tokens from Penpot export file"""
        try:
            # Load Penpot export
            with open(input_file, 'r', encoding='utf-8') as f:
                penpot_data = json.load(f)
            
            # Load existing theme
            self.load_theme()
            
            # Extract and import tokens
            report = {
                "colors_imported": 0,
                "typography_imported": 0,
                "components_imported": 0,
                "errors": []
            }
            
            # Import colors
            if "colors" in penpot_data or "color-libraries" in penpot_data:
                colors = penpot_data.get("colors", penpot_data.get("color-libraries", {}))
                report["colors_imported"] = self._import_colors(colors, merge_strategy)
            
            # Import typography
            if "text-styles" in penpot_data or "typography" in penpot_data:
                text_styles = penpot_data.get("text-styles", penpot_data.get("typography", {}))
                report["typography_imported"] = self._import_typography(text_styles, merge_strategy)
            
            # Import components
            if "components" in penpot_data:
                report["components_imported"] = self._import_components(penpot_data["components"], merge_strategy)
            
            # Save theme
            self.save_theme()
            
            return True, report
        
        except Exception as e:
            return False, {"error": str(e)}
    
    def _import_colors(self, colors: Dict[str, Any], merge_strategy: str) -> int:
        """Import color tokens from Penpot"""
        count = 0
        
        # Ensure tokens.colors exists
        if "tokens" not in self.theme:
            self.theme["tokens"] = {}
        if "colors" not in self.theme["tokens"]:
            self.theme["tokens"]["colors"] = {}
        
        # Process color libraries
        for library_name, library_data in colors.items():
            # Normalize library name (e.g., "Primary Colors" → "primary")
            normalized_name = library_name.lower().replace(" colors", "").replace(" ", "_")
            
            if merge_strategy == "overwrite" or normalized_name not in self.theme["tokens"]["colors"]:
                self.theme["tokens"]["colors"][normalized_name] = {}
            
            # Import colors from library
            if isinstance(library_data, dict):
                for color_name, color_value in library_data.items():
                    # Try to extract shade number (e.g., "Primary 500" → "500")
                    shade = self._extract_shade(color_name)
                    
                    if shade:
                        self.theme["tokens"]["colors"][normalized_name][shade] = color_value
                        count += 1
                    else:
                        # No shade, use color name directly
                        self.theme["tokens"]["colors"][normalized_name][color_name.lower()] = color_value
                        count += 1
            elif isinstance(library_data, str):
                # Single color value
                self.theme["tokens"]["colors"][normalized_name] = {"500": library_data}
                count += 1
        
        return count
    
    def _extract_shade(self, color_name: str) -> Optional[str]:
        """Extract shade number from color name"""
        import re
        
        # Look for patterns like "500", "Primary 500", "Blue-500"
        match = re.search(r'(\d{2,3})$', color_name.replace("-", " ").replace("_", " "))
        if match:
            return match.group(1)
        
        return None
    
    def _import_typography(self, text_styles: Dict[str, Any], merge_strategy: str) -> int:
        """Import typography tokens from Penpot"""
        count = 0
        
        # Ensure tokens.typography exists
        if "tokens" not in self.theme:
            self.theme["tokens"] = {}
        if "typography" not in self.theme["tokens"]:
            self.theme["tokens"]["typography"] = {
                "fontFamily": {},
                "fontSize": {},
                "fontWeight": {},
                "lineHeight": {}
            }
        
        # Process text styles
        for style_name, style_data in text_styles.items():
            # Normalize style name
            normalized_name = style_name.lower().replace(" ", "_")
            
            # Import font family
            if "font-family" in style_data or "fontFamily" in style_data:
                font_family = style_data.get("font-family", style_data.get("fontFamily"))
                if merge_strategy == "overwrite" or normalized_name not in self.theme["tokens"]["typography"]["fontFamily"]:
                    self.theme["tokens"]["typography"]["fontFamily"][normalized_name] = font_family
                    count += 1
            
            # Import font size
            if "font-size" in style_data or "fontSize" in style_data:
                font_size = style_data.get("font-size", style_data.get("fontSize"))
                if merge_strategy == "overwrite" or normalized_name not in self.theme["tokens"]["typography"]["fontSize"]:
                    self.theme["tokens"]["typography"]["fontSize"][normalized_name] = font_size
                    count += 1
            
            # Import font weight
            if "font-weight" in style_data or "fontWeight" in style_data:
                font_weight = style_data.get("font-weight", style_data.get("fontWeight"))
                if merge_strategy == "overwrite" or normalized_name not in self.theme["tokens"]["typography"]["fontWeight"]:
                    self.theme["tokens"]["typography"]["fontWeight"][normalized_name] = str(font_weight)
                    count += 1
            
            # Import line height
            if "line-height" in style_data or "lineHeight" in style_data:
                line_height = style_data.get("line-height", style_data.get("lineHeight"))
                if merge_strategy == "overwrite" or normalized_name not in self.theme["tokens"]["typography"]["lineHeight"]:
                    self.theme["tokens"]["typography"]["lineHeight"][normalized_name] = str(line_height)
                    count += 1
        
        return count
    
    def _import_components(self, components: Dict[str, Any], merge_strategy: str) -> int:
        """Import component variants from Penpot"""
        count = 0
        
        # Ensure components section exists
        if "components" not in self.theme:
            self.theme["components"] = {}
        
        # Process components
        for component_name, component_data in components.items():
            # Normalize component name
            normalized_name = component_name.lower().replace(" ", "_")
            
            if merge_strategy == "overwrite" or normalized_name not in self.theme["components"]:
                self.theme["components"][normalized_name] = {"variants": {}}
            
            # Import variants
            if "variants" in component_data:
                for variant_name, variant_data in component_data["variants"].items():
                    normalized_variant = variant_name.lower().replace(" ", "_")
                    
                    if merge_strategy == "overwrite" or normalized_variant not in self.theme["components"][normalized_name]["variants"]:
                        self.theme["components"][normalized_name]["variants"][normalized_variant] = variant_data
                        count += 1
        
        return count
    
    def import_from_api(self, penpot_url: str, project_id: str, file_id: str, 
                       access_token: str, merge_strategy: str = "merge") -> Tuple[bool, Dict[str, Any]]:
        """Import tokens from Penpot API"""
        try:
            import requests
            
            # Construct API URL
            api_url = f"{penpot_url}/api/rpc/command/get-file"
            
            # Make API request
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "file-id": file_id
            }
            
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            
            penpot_data = response.json()
            
            # Load existing theme
            self.load_theme()
            
            # Extract and import tokens (similar to file import)
            report = {
                "colors_imported": 0,
                "typography_imported": 0,
                "components_imported": 0,
                "errors": []
            }
            
            # Import colors
            if "colors" in penpot_data:
                report["colors_imported"] = self._import_colors(penpot_data["colors"], merge_strategy)
            
            # Import typography
            if "text-styles" in penpot_data:
                report["typography_imported"] = self._import_typography(penpot_data["text-styles"], merge_strategy)
            
            # Import components
            if "components" in penpot_data:
                report["components_imported"] = self._import_components(penpot_data["components"], merge_strategy)
            
            # Save theme
            self.save_theme()
            
            return True, report
        
        except Exception as e:
            return False, {"error": str(e)}


def main():
    """Main CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SmartSpec Penpot Token Importer")
    parser.add_argument("--source", required=True, choices=["file", "api"])
    parser.add_argument("--input-file")
    parser.add_argument("--penpot-url", default="https://design.penpot.app")
    parser.add_argument("--project-id")
    parser.add_argument("--file-id")
    parser.add_argument("--access-token")
    parser.add_argument("--merge-strategy", default="merge", choices=["merge", "overwrite", "append"])
    parser.add_argument("--theme-file", default=".spec/theme.json")
    
    args = parser.parse_args()
    
    importer = PenpotTokenImporter(args.theme_file)
    
    try:
        if args.source == "file":
            if not args.input_file:
                print("❌ Error: --input-file is required for file source")
                sys.exit(1)
            
            success, report = importer.import_from_file(args.input_file, args.merge_strategy)
            
            if success:
                print("✅ Successfully imported tokens from Penpot file")
                print(f"📊 Colors: {report['colors_imported']}, Typography: {report['typography_imported']}, Components: {report['components_imported']}")
            else:
                print(f"❌ Error: {report.get('error', 'Unknown error')}")
                sys.exit(1)
        
        elif args.source == "api":
            if not args.project_id or not args.file_id or not args.access_token:
                print("❌ Error: --project-id, --file-id, and --access-token are required for API source")
                sys.exit(1)
            
            success, report = importer.import_from_api(
                args.penpot_url, args.project_id, args.file_id, 
                args.access_token, args.merge_strategy
            )
            
            if success:
                print("✅ Successfully imported tokens from Penpot API")
                print(f"📊 Colors: {report['colors_imported']}, Typography: {report['typography_imported']}, Components: {report['components_imported']}")
            else:
                print(f"❌ Error: {report.get('error', 'Unknown error')}")
                sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
