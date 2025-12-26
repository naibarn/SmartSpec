from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from .status import append_status


@dataclass
class RunResult:
    ok: bool
    returncode: int
    stdout: str
    stderr: str


class WorkflowRunner:
    def __init__(self, cfg: Dict[str, Any], ai_specs_dir: str):
        self.cfg = cfg
        self.ai_specs_dir = ai_specs_dir

    def run(self, *, runner_type: str, cmd_for_human: str, shell_cmd: Optional[List[str]] = None, cwd: Optional[str] = None) -> RunResult:
        if runner_type == "ide":
            append_status(self.ai_specs_dir, f"\n### Next command\n```bash\n{cmd_for_human}\n```\n")
            return RunResult(True, 0, "", "")

        if runner_type != "shell":
            return RunResult(False, 2, "", f"Unknown runner_type: {runner_type}")

        if not shell_cmd:
            return RunResult(False, 2, "", "shell_cmd missing for shell runner (configure workflow_entrypoints)")

        prefix = self.cfg["runner"].get("shell_prefix", []) or []
        full = prefix + shell_cmd
        try:
            p = subprocess.run(full, cwd=cwd, capture_output=True, text=True, check=False, timeout=3600)
            return RunResult(p.returncode == 0, p.returncode, p.stdout or "", p.stderr or "")
        except Exception as e:
            return RunResult(False, 1, "", str(e))
