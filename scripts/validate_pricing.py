#!/usr/bin/env python3
"""Validate the catalog Pricing Card contract."""
from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    catalog = yaml.safe_load((ROOT / "skills.yaml").read_text(encoding="utf-8"))
    index = yaml.safe_load((ROOT / "pricing-cards/index.yaml").read_text(encoding="utf-8"))
    entries = catalog.get("skills", [])
    cards = {card["id"]: card for card in index.get("cards", [])}
    names = {entry["name"] for entry in entries}
    if names != set(cards):
        raise SystemExit(f"Pricing Card IDs do not match catalog: {sorted(names ^ set(cards))}")
    for entry in entries:
        name = entry["name"]
        pricing = entry.get("pricing")
        if not pricing:
            raise SystemExit(f"Missing public pricing metadata: {name}")
        path = ROOT / pricing["card_path"]
        if not path.exists() or not path.read_text(encoding="utf-8").startswith(f"# Skill Pricing Card：{name}"):
            raise SystemExit(f"Missing or mismatched card file: {name}")
        card = cards[name]
        if pricing["list_price_cny"] != card["list_price_cny"]:
            raise SystemExit(f"Price mismatch: {name}")
        if entry.get("paid") and not entry.get("test"):
            if not isinstance(entry.get("price_cny"), (int, float)) or entry["price_cny"] <= 0:
                raise SystemExit(f"Paid Skill needs a public CNY price: {name}")
            if entry["price_cny"] != pricing["list_price_cny"]:
                raise SystemExit(f"Catalog price mismatch: {name}")
    print(f"validated {len(entries)} catalog Pricing Cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
