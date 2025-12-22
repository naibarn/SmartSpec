#!/usr/bin/env python3
"""
SmartSpec Catalog to A2UI v0.8 Export Utility

This script converts a SmartSpec-managed UI catalog to a standard A2UI v0.8
Catalog Definition Document, enabling interoperability with external A2UI renderers.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


class CatalogExporter:
    """Handles the conversion from SmartSpec catalog to A2UI v0.8 format."""
    
    # Mapping from SmartSpec component types to A2UI component types
    TYPE_MAPPING = {
        "input-text": "TextInput",
        "input-email": "EmailInput",
        "input-password": "PasswordInput",
        "input-search": "SearchInput",
        "textarea": "TextArea",
        "button-primary": "Button",
        "button-secondary": "Button",
        "checkbox": "Checkbox",
        "radio": "Radio",
        "select": "Select",
        "data-table": "Table",
        "pagination": "Pagination",
        "image": "Image",
        "text-heading": "Heading",
        "text-body": "Text",
        "link": "Link",
        "card": "Card",
        "modal": "Modal",
        "navigation-menu": "Navigation",
        "metric-card": "MetricCard",
        "chart-line": "LineChart",
        "chart-bar": "BarChart",
        "timeline": "Timeline",
        "progress-stepper": "Stepper",
        "toast": "Toast",
    }
    
    def __init__(self, catalog_id: str, include_metadata: bool = False):
        self.catalog_id = catalog_id
        self.include_metadata = include_metadata
        self.stats = {
            "components_exported": 0,
            "properties_mapped": 0,
            "warnings": []
        }
    
    def export(self, smartspec_catalog: Dict[str, Any], platform: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert SmartSpec catalog to A2UI v0.8 format.
        
        Args:
            smartspec_catalog: The SmartSpec catalog dictionary
            platform: Optional platform filter
            
        Returns:
            A2UI v0.8 Catalog Definition Document
        """
        a2ui_catalog = {
            "catalogId": self.catalog_id,
            "version": "0.8",
            "components": []
        }
        
        # Add metadata if requested
        if self.include_metadata and "description" in smartspec_catalog:
            a2ui_catalog["_metadata"] = {
                "source": "SmartSpec",
                "description": smartspec_catalog["description"]
            }
        
        # Process patterns (which contain components)
        if "patterns" in smartspec_catalog:
            for pattern in smartspec_catalog["patterns"]:
                if "components" in pattern:
                    for component in pattern["components"]:
                        # Filter by platform if specified
                        if platform and "platforms" in component:
                            if platform not in component["platforms"]:
                                continue
                        
                        a2ui_component = self._convert_component(component, platform)
                        if a2ui_component:
                            a2ui_catalog["components"].append(a2ui_component)
                            self.stats["components_exported"] += 1
        
        return a2ui_catalog
    
    def _convert_component(self, smartspec_component: Dict[str, Any], platform: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Convert a single SmartSpec component to A2UI format.
        
        Args:
            smartspec_component: SmartSpec component definition
            platform: Optional platform for platform-specific properties
            
        Returns:
            A2UI component definition or None if conversion fails
        """
        component_id = smartspec_component.get("id")
        component_type = smartspec_component.get("type")
        
        if not component_id or not component_type:
            self.stats["warnings"].append(f"Skipping component without id or type: {smartspec_component}")
            return None
        
        # Map SmartSpec type to A2UI type
        a2ui_type = self.TYPE_MAPPING.get(component_type, component_type)
        
        a2ui_component = {
            "id": component_id,
            "type": a2ui_type,
            "properties": {}
        }
        
        # Convert common properties
        if "label" in smartspec_component:
            a2ui_component["properties"]["label"] = {
                "type": "string",
                "description": "The text label for the component.",
                "default": smartspec_component["label"]
            }
            self.stats["properties_mapped"] += 1
        
        if "required" in smartspec_component:
            a2ui_component["properties"]["required"] = {
                "type": "boolean",
                "description": "Whether the input is required.",
                "default": smartspec_component["required"]
            }
            self.stats["properties_mapped"] += 1
        
        if "placeholder" in smartspec_component:
            a2ui_component["properties"]["placeholder"] = {
                "type": "string",
                "description": "Placeholder text for the input.",
                "default": smartspec_component["placeholder"]
            }
            self.stats["properties_mapped"] += 1
        
        if "disabled" in smartspec_component:
            a2ui_component["properties"]["disabled"] = {
                "type": "boolean",
                "description": "Whether the component is disabled.",
                "default": smartspec_component["disabled"]
            }
            self.stats["properties_mapped"] += 1
        
        # Handle platform-specific properties
        if platform and "platforms" in smartspec_component:
            platform_props = smartspec_component["platforms"].get(platform, {})
            for key, value in platform_props.items():
                a2ui_component["properties"][key] = {
                    "type": self._infer_type(value),
                    "description": f"Platform-specific property: {key}",
                    "default": value
                }
                self.stats["properties_mapped"] += 1
        
        return a2ui_component
    
    def _infer_type(self, value: Any) -> str:
        """Infer JSON schema type from Python value."""
        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return "string"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get export statistics."""
        return self.stats


def main():
    """Main entry point for the export script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Export SmartSpec catalog to A2UI v0.8 format"
    )
    parser.add_argument(
        "--input-catalog",
        default=".spec/ui-catalog.json",
        help="Path to SmartSpec catalog file"
    )
    parser.add_argument(
        "--output-file",
        required=True,
        help="Path to write A2UI catalog file"
    )
    parser.add_argument(
        "--catalog-id",
        required=True,
        help="Unique catalog ID (typically a URL)"
    )
    parser.add_argument(
        "--output-format",
        default="a2ui-v0.8",
        choices=["a2ui-v0.8"],
        help="Target format"
    )
    parser.add_argument(
        "--platform",
        help="Platform filter (e.g., web, flutter)"
    )
    parser.add_argument(
        "--include-metadata",
        action="store_true",
        help="Include SmartSpec metadata in output"
    )
    
    args = parser.parse_args()
    
    # Read SmartSpec catalog
    input_path = Path(args.input_catalog)
    if not input_path.exists():
        print(f"Error: Input catalog not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            smartspec_catalog = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input catalog: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Export to A2UI format
    exporter = CatalogExporter(
        catalog_id=args.catalog_id,
        include_metadata=args.include_metadata
    )
    
    a2ui_catalog = exporter.export(smartspec_catalog, platform=args.platform)
    
    # Write output
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(a2ui_catalog, f, indent=2, ensure_ascii=False)
    
    # Print statistics
    stats = exporter.get_stats()
    print(f"✅ Export complete!")
    print(f"   Components exported: {stats['components_exported']}")
    print(f"   Properties mapped: {stats['properties_mapped']}")
    print(f"   Output file: {output_path}")
    
    if stats["warnings"]:
        print(f"\n⚠️  Warnings:")
        for warning in stats["warnings"]:
            print(f"   - {warning}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
