from __future__ import annotations

import os

def decide_mode(requested: str) -> str:
    if requested in ("ide", "headless"):
        return requested

    # auto: prefer IDE mode when run under VS Code/Kilo/Antigravity
    if os.getenv("VSCODE_PID") or os.getenv("TERM_PROGRAM") == "vscode":
        return "ide"
    if os.getenv("KILO") == "1" or os.getenv("KILO_CODE") == "1":
        return "ide"
    if os.getenv("ANTIGRAVITY") == "1":
        return "ide"

    return "headless"
