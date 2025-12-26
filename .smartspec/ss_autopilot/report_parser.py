from __future__ import annotations

import os, json, glob, re
from typing import Optional, Dict, Any

def latest_summary_for(reports_dir: str, spec_id: str) -> Optional[Dict[str, Any]]:
    patterns = [
        os.path.join(reports_dir, "**", f"*{spec_id}*", "summary.json"),
        os.path.join(".smartspec", "reports", "**", f"*{spec_id}*", "summary.json"),
    ]
    candidates = []
    for pat in patterns:
        candidates.extend(glob.glob(pat, recursive=True))
    if not candidates:
        return None
    newest = max(candidates, key=lambda p: os.path.getmtime(p))
    try:
        with open(newest, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def extract_coverage_total(summary: Dict[str, Any]) -> Optional[int]:
    for key in ("coverage_total", "coverage", "total_coverage"):
        v = summary.get(key)
        if isinstance(v, int):
            return v
    text = json.dumps(summary)
    m = re.search(r"(\d{1,3})%\s*coverage", text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return None
