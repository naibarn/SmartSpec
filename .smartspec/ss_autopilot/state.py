from __future__ import annotations

import os, json
from typing import TypedDict, Optional, Dict, Any
from pathlib import Path

from .report_parser import latest_summary_for, extract_coverage_total


class AutopilotState(TypedDict, total=False):
    category: str
    spec_id: str
    spec_path: str
    plan_path: str
    tasks_path: str

    mode: str
    platform: str
    runner_type: str

    has_spec: bool
    has_plan: bool
    has_tasks: bool
    coverage: Optional[int]
    min_coverage: int

    step: str
    message: str
    next_commands: list[str]


def _exists(p: str) -> bool:
    return bool(p) and os.path.exists(p)


def load_state_from_files(*, ai_specs_dir: str, specs_root: str, category: str, spec_id: str, reports_dir: str,
                          min_coverage: int, platform: str, runner_type: str) -> AutopilotState:
    spec_path = str(Path(specs_root) / category / spec_id / "spec.md")
    plan_path = str(Path(specs_root) / category / spec_id / "plan.md")
    tasks_path = str(Path(specs_root) / category / spec_id / "tasks.md")

    has_spec = _exists(spec_path)
    has_plan = _exists(plan_path)
    has_tasks = _exists(tasks_path)

    summary = latest_summary_for(reports_dir, spec_id)
    cov = extract_coverage_total(summary) if summary else None

    return AutopilotState(
        category=category,
        spec_id=spec_id,
        spec_path=spec_path,
        plan_path=plan_path,
        tasks_path=tasks_path,
        has_spec=has_spec,
        has_plan=has_plan,
        has_tasks=has_tasks,
        coverage=cov,
        min_coverage=min_coverage,
        mode="auto",
        platform=platform,
        runner_type=runner_type,
        step="LOAD",
        message="Loaded state",
        next_commands=[],
    )


def save_state(ai_specs_dir: str, state: AutopilotState) -> None:
    path = os.path.join(ai_specs_dir, "state.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
