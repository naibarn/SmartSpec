from __future__ import annotations

import os

def _status_path(ai_specs_dir: str) -> str:
    return os.path.join(ai_specs_dir, "status.md")

def write_status(ai_specs_dir: str, content: str) -> None:
    os.makedirs(ai_specs_dir, exist_ok=True)
    with open(_status_path(ai_specs_dir), "w", encoding="utf-8") as f:
        f.write(content)

def append_status(ai_specs_dir: str, content: str) -> None:
    with open(_status_path(ai_specs_dir), "a", encoding="utf-8") as f:
        f.write(content)
