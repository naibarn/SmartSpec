"""
Platform detection for Kilo Code, AntiGravity, and Claude Code.

This module auto-detects which AI coding platform is currently running
and provides platform-specific command formatting.
"""

from __future__ import annotations

import os
from typing import Literal

Platform = Literal["kilo", "antigravity", "claude", "unknown"]


def detect_platform() -> Platform:
    """
    Auto-detect which platform is running.
    
    Detection order:
    1. Environment variables (most reliable)
    2. Platform-specific files
    3. Config hints
    4. Default to kilo
    
    Returns:
        Platform name: "kilo", "antigravity", "claude", or "unknown"
    """
    # Check environment variables
    if os.getenv("KILO_CODE") or os.getenv("KILO"):
        return "kilo"
    if os.getenv("ANTIGRAVITY"):
        return "antigravity"
    if os.getenv("CLAUDE_CODE") or os.getenv("CLAUDE"):
        return "claude"
    
    # Check for platform-specific marker files
    if os.path.exists(".kilo"):
        return "kilo"
    if os.path.exists(".antigravity"):
        return "antigravity"
    if os.path.exists(".claude"):
        return "claude"
    
    # Check for platform-specific directories
    if os.path.exists(".kilo-workspace"):
        return "kilo"
    if os.path.exists(".antigravity-workspace"):
        return "antigravity"
    
    # Default to kilo (most common)
    return "kilo"


def get_platform_flag(platform: Platform) -> str:
    """
    Get platform-specific flag to append to commands.
    
    Args:
        platform: Platform name
        
    Returns:
        Platform flag string (e.g., "--platform kilo")
    """
    if platform == "kilo":
        return "--platform kilo"
    elif platform == "antigravity":
        return "--platform antigravity"
    elif platform == "claude":
        # Claude Code may not need platform flag
        return ""
    else:
        return ""


def format_workflow_command(platform: Platform, workflow: str) -> str:
    """
    Format workflow name for platform-specific slash commands.
    
    Args:
        platform: Platform name
        workflow: Workflow name (e.g., "smartspec_generate_spec")
        
    Returns:
        Formatted command (e.g., "/smartspec_generate_spec.md")
    """
    if platform == "kilo":
        # Kilo Code uses .md extension
        return f"/{workflow}.md"
    elif platform == "antigravity":
        # AntiGravity may not need .md extension
        return f"/{workflow}"
    elif platform == "claude":
        # Claude Code format (TBD - may be similar to Kilo)
        return f"/{workflow}.md"
    else:
        # Default format
        return f"/{workflow}.md"


def get_platform_info(platform: Platform) -> dict:
    """
    Get detailed information about a platform.
    
    Args:
        platform: Platform name
        
    Returns:
        Dict with platform information
    """
    info = {
        "kilo": {
            "name": "Kilo Code",
            "command_format": "/{workflow}.md",
            "needs_platform_flag": True,
            "platform_flag": "--platform kilo",
            "supports_slash_commands": True,
            "supports_json_output": True,
        },
        "antigravity": {
            "name": "AntiGravity",
            "command_format": "/{workflow}",
            "needs_platform_flag": True,
            "platform_flag": "--platform antigravity",
            "supports_slash_commands": True,
            "supports_json_output": True,
        },
        "claude": {
            "name": "Claude Code",
            "command_format": "/{workflow}.md",
            "needs_platform_flag": False,
            "platform_flag": "",
            "supports_slash_commands": True,
            "supports_json_output": True,
        },
        "unknown": {
            "name": "Unknown Platform",
            "command_format": "/{workflow}.md",
            "needs_platform_flag": False,
            "platform_flag": "",
            "supports_slash_commands": True,
            "supports_json_output": True,
        }
    }
    return info.get(platform, info["unknown"])
