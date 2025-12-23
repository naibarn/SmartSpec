#!/usr/bin/env python3

import json
import argparse
import sys
import os
from collections.abc import MutableMapping

def deep_merge(destination, source):
    """Recursively merges source dict into destination dict."""
    for key, value in source.items():
        if isinstance(value, MutableMapping) and key in destination and isinstance(destination[key], MutableMapping):
            destination[key] = deep_merge(destination[key], value)
        else:
            destination[key] = value
    return destination

def main():
    parser = argparse.ArgumentParser(description="Merges multiple theme files into a single, resolved theme based on a specified hierarchy.")
    parser.add_argument("--base-theme", required=True, help="Path to the base or system-level theme file.")
    parser.add_argument("--override-themes", required=True, help="A JSON string representing an ordered list of paths to theme files.")
    parser.add_argument("--output-file", required=True, help="Path to save the final, merged theme file.")

    args = parser.parse_args()

    # Load base theme
    try:
        with open(args.base_theme, 'r') as f:
            resolved_theme = json.load(f)
    except FileNotFoundError:
        print(f"Error: Base theme file not found at {args.base_theme}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in base theme file: {args.base_theme}", file=sys.stderr)
        sys.exit(1)

    # Parse and process override themes
    try:
        override_paths = json.loads(args.override_themes)
        if not isinstance(override_paths, list):
            raise TypeError("Override themes must be a list of strings.")
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error: --override-themes must be a valid JSON array of strings. {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Starting with base theme: {args.base_theme}")
    for theme_path in override_paths:
        try:
            with open(theme_path, 'r') as f:
                override_theme = json.load(f)
            resolved_theme = deep_merge(resolved_theme, override_theme)
            print(f"✅ Merged override theme: {theme_path}")
        except FileNotFoundError:
            print(f"Warning: Override theme file not found, skipping: {theme_path}", file=sys.stderr)
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in override theme file, skipping: {theme_path}", file=sys.stderr)

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Write the final resolved theme
    try:
        with open(args.output_file, 'w') as f:
            json.dump(resolved_theme, f, indent=2)
        print(f"🎉 Successfully wrote resolved theme to: {args.output_file}")
    except IOError as e:
        print(f"Error: Failed to write output file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
