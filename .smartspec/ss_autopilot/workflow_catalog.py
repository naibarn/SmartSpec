from __future__ import annotations

import os, re
from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class WorkflowMeta:
    name: str                 # e.g. smartspec_generate_plan
    slash: str                # e.g. /smartspec_generate_plan
    version: Optional[str]
    category: Optional[str]
    description: Optional[str]
    path: str

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

def _parse_frontmatter(text: str) -> Dict[str, str]:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    body = m.group(1)
    out: Dict[str, str] = {}
    # super-light YAML-ish parsing: key: value lines only
    for line in body.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out

def discover_workflows(workflows_dir: str = ".smartspec/workflows") -> List[WorkflowMeta]:
    metas: List[WorkflowMeta] = []
    if not os.path.isdir(workflows_dir):
        return metas
    for fn in os.listdir(workflows_dir):
        if not fn.endswith(".md"):
            continue
        path = os.path.join(workflows_dir, fn)
        try:
            text = open(path, "r", encoding="utf-8").read()
        except Exception:
            continue
        fm = _parse_frontmatter(text)
        slash = fm.get("workflow") or ""
        name = fn.replace(".md", "")
        metas.append(WorkflowMeta(
            name=name,
            slash=slash,
            version=fm.get("version"),
            category=fm.get("category"),
            description=fm.get("description"),
            path=path,
        ))
    return sorted(metas, key=lambda m: m.name)
