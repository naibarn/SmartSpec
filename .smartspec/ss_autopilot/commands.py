from __future__ import annotations

from typing import Dict, Any

def build_slash_command(cfg: Dict[str, Any], platform: str, workflow_key: str, *args: str) -> str:
    cmd_base = cfg["commands"][platform][workflow_key]
    parts = [cmd_base] + list(args)
    return " ".join(parts)

def default_out_dir(workflow: str, spec_id: str) -> str:
    safe = spec_id.replace("spec-", "")
    return f".spec/reports/{workflow}/{safe}"
