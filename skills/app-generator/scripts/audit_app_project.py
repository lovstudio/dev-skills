#!/usr/bin/env python3
"""Audit a project against the Lovstudio app baseline."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


TEXT_EXTENSIONS = {
    ".json",
    ".json5",
    ".toml",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".css",
    ".md",
    ".yml",
    ".yaml",
}


@dataclass
class Check:
    id: str
    title: str
    status: str
    detail: str
    recommendation: str


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def load_package_json(root: Path) -> dict:
    package_path = root / "package.json"
    if not package_path.exists():
        return {}
    try:
        return json.loads(read_text(package_path))
    except json.JSONDecodeError:
        return {}


def dependencies(package: dict) -> dict:
    merged = {}
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        value = package.get(key)
        if isinstance(value, dict):
            merged.update(value)
    return merged


def file_exists(root: Path, patterns: Iterable[str]) -> bool:
    for pattern in patterns:
        if any(root.glob(pattern)):
            return True
    return False


def find_files(root: Path, patterns: Iterable[str]) -> list[Path]:
    files: list[Path] = []
    for pattern in patterns:
        files.extend(root.glob(pattern))
    return sorted({p.resolve() for p in files if p.is_file()})


def contains_text(paths: Iterable[Path], needles: Iterable[str]) -> bool:
    lower_needles = [needle.lower() for needle in needles]
    for path in paths:
        text = read_text(path).lower()
        if any(needle in text for needle in lower_needles):
            return True
    return False


def search_text(root: Path, needles: Iterable[str], max_files: int = 300) -> bool:
    lower_needles = [needle.lower() for needle in needles]
    count = 0
    for path in root.rglob("*"):
        if count >= max_files:
            break
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        parts = set(path.parts)
        if {"node_modules", "target", "dist", "build"} & parts:
            continue
        count += 1
        text = read_text(path).lower()
        if any(needle in text for needle in lower_needles):
            return True
    return False


def status(ok: bool) -> str:
    return "ok" if ok else "missing"


def audit(root: Path) -> dict:
    root = root.resolve()
    package = load_package_json(root)
    deps = dependencies(package)
    src_tauri = root / "src-tauri"

    tauri_conf = find_files(
        root,
        [
            "src-tauri/tauri.conf.json",
            "src-tauri/tauri.conf.json5",
            "src-tauri/Tauri.toml",
        ],
    )
    workflows = find_files(root, [".github/workflows/*.yml", ".github/workflows/*.yaml"])
    css_files = find_files(root, ["src/index.css", "src/App.css", "app/globals.css", "src/styles/*.css"])
    build_config_files = find_files(
        root,
        [
            "vite.config.ts",
            "vite.config.js",
            "vite.config.mts",
            "webpack.config.ts",
            "webpack.config.js",
            "next.config.ts",
            "next.config.js",
            "nuxt.config.ts",
            "nuxt.config.js",
        ],
    )
    local_instruction_files = find_files(root, ["AGENTS.md", "CLAUDE.md", "tailwind.config.ts", "tailwind.config.js"])

    has_tauri = src_tauri.exists() or "@tauri-apps/api" in deps or "@tauri-apps/cli" in deps
    has_react = "react" in deps
    has_vite = file_exists(root, ["vite.config.ts", "vite.config.js", "vite.config.mts"]) or "vite" in deps
    has_shadcn = (root / "components.json").exists()
    has_tanstack = "@tanstack/react-query" in deps
    has_lucin = "lucide-react" in deps
    has_lovinsp = "lovinsp" in deps or contains_text(build_config_files, ["lovinspplugin", "@lovinsp/", "lovinsp"])
    has_logo = file_exists(root, ["assets/logo.png", "assets/logo.svg", "public/logo.png", "public/logo.svg"])
    has_icons = file_exists(root, ["src-tauri/icons/icon.icns", "src-tauri/icons/icon.ico"])
    has_ci = any(re.search(r"(check|ci|test|build)", p.name, re.I) for p in workflows)
    has_release = any(re.search(r"(release|tauri)", p.name, re.I) for p in workflows)
    has_updater = (
        "@tauri-apps/plugin-updater" in deps
        or (src_tauri.exists() and search_text(src_tauri, ["plugin-updater", "tauri_plugin_updater", "updater"]))
    )
    frontend_roots = [path for path in (root / "src", root / "app", root / "pages") if path.exists()]
    has_query_provider = has_tanstack and any(search_text(path, ["queryclientprovider"]) for path in frontend_roots)
    has_warm_academic = any(
        "--primary" in read_text(path)
        and ("--background" in read_text(path) or "bg-background" in read_text(path))
        for path in css_files
    ) or contains_text(local_instruction_files, ["warm academic", "cc785c", "lovstudio"])

    checks = [
        Check(
            "package",
            "Package manifest",
            status(bool(package)),
            "package.json found" if package else "package.json not found",
            "Create a React/Vite package before app-layer setup.",
        ),
        Check(
            "react-vite",
            "React + Vite baseline",
            status(has_react and has_vite),
            f"react={has_react}, vite={has_vite}",
            "Use a React TypeScript Vite app unless the target project already has a stronger local convention.",
        ),
        Check(
            "tauri",
            "Tauri baseline",
            status(has_tauri and bool(tauri_conf)),
            f"src-tauri={src_tauri.exists()}, config_files={len(tauri_conf)}",
            "Run Tauri init and configure title, identifier, windows, bundle metadata, and capabilities.",
        ),
        Check(
            "shadcn",
            "shadcn/ui",
            status(has_shadcn),
            "components.json found" if has_shadcn else "components.json missing",
            "Initialize shadcn/ui and map tokens to the Lovstudio Warm Academic theme.",
        ),
        Check(
            "warm-academic",
            "Lovstudio Warm Academic UI",
            status(has_warm_academic),
            "theme tokens or Lovstudio references detected" if has_warm_academic else "theme tokens not detected",
            "Read /Users/mark/lovstudio/design/design-guide.md and use semantic Tailwind classes.",
        ),
        Check(
            "tanstack-query",
            "TanStack Query",
            status(has_tanstack and has_query_provider),
            f"dependency={has_tanstack}, provider={has_query_provider}",
            "Add QueryClientProvider, stable query keys, and invoke/query wrappers for server state.",
        ),
        Check(
            "icons",
            "Target-specific app logo and Tauri icons",
            status(has_logo and (has_icons or not has_tauri)),
            f"source_logo={has_logo}, tauri_icons={has_icons}",
            "For new apps, run lovstudio:gen-logo to create assets/logo* and public/logo*, then generate Tauri icons from that target-specific logo.",
        ),
        Check(
            "lucide",
            "Lucide icons",
            status(has_lucin),
            "lucide-react dependency found" if has_lucin else "lucide-react missing",
            "Use lucide-react for toolbar and action icons.",
        ),
        Check(
            "lovinsp",
            "Lovinsp click-to-code",
            status(has_lovinsp),
            "lovinsp detected" if has_lovinsp else "lovinsp missing",
            "Install lovinsp idempotently so designers/developers can jump from DOM to source.",
        ),
        Check(
            "ci",
            "CI workflow",
            status(has_ci),
            f"workflow_files={len(workflows)}",
            "Add a GitHub Actions check workflow for install, typecheck, lint/build where available.",
        ),
        Check(
            "release",
            "Tauri release workflow",
            status(has_release),
            f"workflow_files={len(workflows)}",
            "Add a Tauri release workflow that builds artifacts and attaches them to GitHub Releases.",
        ),
        Check(
            "updater",
            "Auto update",
            status(has_updater),
            "updater detected" if has_updater else "updater not detected",
            "Wire @tauri-apps/plugin-updater / tauri_plugin_updater and signing env placeholders.",
        ),
    ]

    return {
        "root": str(root),
        "summary": {
            "ok": sum(1 for check in checks if check.status == "ok"),
            "missing": sum(1 for check in checks if check.status != "ok"),
        },
        "checks": [asdict(check) for check in checks],
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Lovstudio App Audit",
        "",
        f"Root: `{report['root']}`",
        "",
        f"Checks: {report['summary']['ok']} ok, {report['summary']['missing']} missing",
        "",
        "| Status | Area | Detail | Recommendation |",
        "|---|---|---|---|",
    ]
    marker = {"ok": "OK", "missing": "MISSING"}
    for check in report["checks"]:
        lines.append(
            "| {status} | {title} | {detail} | {recommendation} |".format(
                status=marker.get(check["status"], check["status"].upper()),
                title=check["title"].replace("|", "\\|"),
                detail=check["detail"].replace("|", "\\|"),
                recommendation=check["recommendation"].replace("|", "\\|"),
            )
        )
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit a project against the Lovstudio app baseline.")
    parser.add_argument("--root", default=".", help="Target app root to inspect.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Output format.")
    parser.add_argument("--output", help="Optional path to write the report.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = Path(args.root)
    if not root.exists():
        print(f"error: root does not exist: {root}", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"error: root is not a directory: {root}", file=sys.stderr)
        return 2

    report = audit(root)
    if args.format == "json":
        output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    else:
        output = render_markdown(report)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
