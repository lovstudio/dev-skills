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

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = ROOT / "skills.yaml"
SKILLPAY_PRODUCT_ID_RE = re.compile(r"P\d{16}")
SKILLPAY_PURCHASE_URL_RE = re.compile(
    r"https://aipayapi\.alipay\.com/skillpay/ct\?c=[A-Za-z0-9_-]+"
)


def load_skills() -> list[dict]:
    with YAML_PATH.open() as f:
        return yaml.safe_load(f)["skills"]


def validate(skills: list[dict]) -> list[str]:
    errors: list[str] = []
    by_name = {s["name"]: s for s in skills}
    skillpay_ids: dict[str, str] = {}

    for s in skills:
        name = s["name"]
        product_id = s.get("skillpay_product_id")
        purchase_url = s.get("skillpay_purchase_url")
        distribution = s.get("distribution")
        skillpay_status = distribution.get("skillpay") if isinstance(distribution, dict) else None
        if product_id is not None:
            if not isinstance(product_id, str) or not SKILLPAY_PRODUCT_ID_RE.fullmatch(product_id):
                errors.append(f"{name}.skillpay_product_id: invalid product id")
            elif product_id in skillpay_ids:
                errors.append(
                    f"{name}.skillpay_product_id: duplicates {skillpay_ids[product_id]}"
                )
            else:
                skillpay_ids[product_id] = name
        if purchase_url is not None:
            if not isinstance(purchase_url, str) or not SKILLPAY_PURCHASE_URL_RE.fullmatch(purchase_url):
                errors.append(f"{name}.skillpay_purchase_url: invalid purchase URL")
            if not product_id:
                errors.append(f"{name}.skillpay_purchase_url: requires skillpay_product_id")
        if skillpay_status == "live" and (not product_id or not purchase_url):
            errors.append(f"{name}.distribution.skillpay: live requires product id and purchase URL")
        if skillpay_status == "rejected":
            if not product_id:
                errors.append(f"{name}.distribution.skillpay: rejected requires product id")
            if purchase_url:
                errors.append(f"{name}.distribution.skillpay: rejected must not expose a purchase URL")

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
