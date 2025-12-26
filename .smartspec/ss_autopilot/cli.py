from __future__ import annotations

import typer
from .pipeline import run_autopilot

app = typer.Typer(help="SmartSpec Autopilot (LangGraph, no-LLM routing)")

@app.command()
def run(
    spec_id: str = typer.Option(..., help="Spec folder name, e.g. spec-core-001-authentication"),
    category: str = typer.Option("core", help="Spec category: core|feature|ui"),
    mode: str = typer.Option("auto", help="auto|ide|headless"),
    min_coverage: int = typer.Option(80, help="Minimum coverage percent"),
    platform: str = typer.Option("kilo", help="kilo|antigravity (affects slash command formatting)"),
):
    """Run autopilot for one spec.

    IDE mode: writes next commands to ai_specs/status.md and stops.
    Headless mode: executes workflows via shell if configured.
    """
    run_autopilot(spec_id=spec_id, category=category, mode=mode, min_coverage=min_coverage, platform=platform)
