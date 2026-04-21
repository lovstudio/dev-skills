#!/usr/bin/env python3
"""Validate depends_on / related fields in skills.yaml.

Rules:
  - Every name in depends_on / related must exist in skills.yaml.
  - related must be symmetric: if A lists B, B must list A.
  - depends_on graph must be acyclic.

Run standalone; both render-marketplace.py and render-readme.py import
validate() so CI rejects bad states before regenerating outputs.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = ROOT / "skills.yaml"


def load_skills() -> list[dict]:
    with YAML_PATH.open() as f:
        return yaml.safe_load(f)["skills"]


def validate(skills: list[dict]) -> list[str]:
    errors: list[str] = []
    by_name = {s["name"]: s for s in skills}

    for s in skills:
        name = s["name"]
        for field in ("depends_on", "related"):
            for ref in s.get(field) or []:
                if ref not in by_name:
                    errors.append(f"{name}.{field}: unknown skill '{ref}'")
                if ref == name:
                    errors.append(f"{name}.{field}: self-reference")

        for ref in s.get("related") or []:
            if ref in by_name:
                back = by_name[ref].get("related") or []
                if name not in back:
                    errors.append(
                        f"related asymmetry: {name} → {ref} but {ref} does not list {name}"
                    )

    # DFS cycle detection on depends_on graph.
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {s["name"]: WHITE for s in skills}

    def visit(n: str, path: list[str]) -> None:
        if color[n] == GRAY:
            cycle = path[path.index(n):] + [n]
            errors.append(f"depends_on cycle: {' → '.join(cycle)}")
            return
        if color[n] == BLACK:
            return
        color[n] = GRAY
        for dep in by_name[n].get("depends_on") or []:
            if dep in by_name:
                visit(dep, path + [n])
        color[n] = BLACK

    for s in skills:
        if color[s["name"]] == WHITE:
            visit(s["name"], [])

    return errors


def main() -> int:
    errors = validate(load_skills())
    if errors:
        print("Dependency validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("Dependency validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
