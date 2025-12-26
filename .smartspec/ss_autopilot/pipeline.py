from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Any

import yaml

from .state import load_state_from_files, save_state
from .status import write_status, append_status
from .graph import build_graph
from .context import decide_mode


@dataclass
class Settings:
    config: Dict[str, Any]

    @property
    def ai_specs_dir(self) -> str:
        return self.config["paths"]["ai_specs_dir"]

    @property
    def reports_dir(self) -> str:
        return self.config["paths"]["reports_dir"]


def load_settings() -> Settings:
    with open(os.path.join("config", "autopilot.yaml"), "r", encoding="utf-8") as f:
        return Settings(config=yaml.safe_load(f))


def run_autopilot(*, spec_id: str, category: str, mode: str, min_coverage: int, platform: str) -> None:
    settings = load_settings()
    os.makedirs(settings.ai_specs_dir, exist_ok=True)

    decided_mode = decide_mode(mode)
    write_status(
        settings.ai_specs_dir,
        f"# Autopilot run\n\n"
        f"- spec: {category}/{spec_id}\n"
        f"- mode: {decided_mode}\n"
        f"- platform: {platform}\n"
        f"- min_coverage: {min_coverage}\n"
    )

    state = load_state_from_files(
        ai_specs_dir=settings.ai_specs_dir,
        specs_root="specs",
        category=category,
        spec_id=spec_id,
        reports_dir=settings.reports_dir,
        min_coverage=min_coverage,
        platform=platform,
        runner_type=settings.config["runner"]["type"],
    )
    state["mode"] = decided_mode
    save_state(settings.ai_specs_dir, state)

    graph = build_graph(settings.config)
    result = graph.invoke(state)

    append_status(settings.ai_specs_dir, "\n## Result\n")
    append_status(settings.ai_specs_dir, f"- step: {result.get('step')}\n")
    append_status(settings.ai_specs_dir, f"- message: {result.get('message')}\n")

    save_state(settings.ai_specs_dir, result)
