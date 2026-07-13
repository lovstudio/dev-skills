#!/usr/bin/env python3
"""Sync released independent skill repositories into the dev-skills bundle."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tarfile
import tempfile
from typing import Dict, Iterable, List, Tuple
import urllib.error
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "independent-skills.json"
IGNORED_NAMES = {".git", ".github", "__pycache__", ".DS_Store"}


def request_json(url: str) -> Dict[str, object]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "lovstudio-dev-skills-sync"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"GitHub API failed for {url}: HTTP {exc.code}") from exc


def download(url: str) -> bytes:
    headers = {"User-Agent": "lovstudio-dev-skills-sync"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def safe_extract(payload: bytes, destination: Path) -> Path:
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        members = archive.getmembers()
        for member in members:
            parts = PurePosixPath(member.name).parts
            if not parts or ".." in parts or member.issym() or member.islnk():
                raise RuntimeError(f"Unsafe release archive member: {member.name}")
        archive.extractall(destination)
    roots = [path for path in destination.iterdir() if path.is_dir()]
    if len(roots) != 1:
        raise RuntimeError("Expected exactly one root directory in release archive")
    return roots[0]


def included(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return not any(part in IGNORED_NAMES for part in relative.parts)


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.exists():
        return "missing"
    for path in sorted(p for p in root.rglob("*") if p.is_file() and included(p, root)):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def copy_mirror(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for path in source.iterdir():
        if path.name in IGNORED_NAMES:
            continue
        target = destination / path.name
        if path.is_dir():
            shutil.copytree(path, target, ignore=shutil.ignore_patterns(*IGNORED_NAMES))
        elif path.is_file():
            shutil.copy2(path, target)


def update_catalog(name: str, repo: str, version: str) -> None:
    path = ROOT / "skills.yaml"
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(rf"(?ms)(^- name:\s*{re.escape(name)}\s*$\n)(?P<body>.*?)(?=^- name:|\Z)")
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f"Missing skills.yaml entry for {name}")
    body = match.group("body")
    body = re.sub(r"(?m)^\s+repo:\s*.*$", f"  repo: {repo}", body, count=1)
    body = re.sub(r"(?m)^\s+skill_path:\s*.*\n", "", body, count=1)
    body = re.sub(r"(?m)^\s+version:\s*.*$", f"  version: {version}", body, count=1)
    updated = text[: match.start()] + match.group(1) + body + text[match.end() :]
    path.write_text(updated, encoding="utf-8")


def latest_release(repo: str) -> Tuple[str, str]:
    payload = request_json(f"https://api.github.com/repos/{repo}/releases/latest")
    tag = str(payload.get("tag_name") or "")
    tarball = str(payload.get("tarball_url") or "")
    if not tag or not tarball:
        raise RuntimeError(f"{repo} has no usable latest release")
    return tag, tarball


def manifest_entries() -> List[Dict[str, str]]:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return list(payload["skills"])


def sync(check: bool) -> int:
    drift: List[str] = []
    for entry in manifest_entries():
        name, repo = entry["name"], entry["repo"]
        tag, tarball_url = latest_release(repo)
        version = tag[1:] if tag.startswith("v") else tag
        with tempfile.TemporaryDirectory(prefix=f"sync-{name}-") as tmp:
            source = safe_extract(download(tarball_url), Path(tmp))
            destination = ROOT / "skills" / name
            before = tree_digest(destination)
            after = tree_digest(source)
            if before != after:
                drift.append(name)
                if not check:
                    copy_mirror(source, destination)
        if not check:
            update_catalog(name, repo, version)
        print(f"{name}: {tag}{' (drift)' if name in drift else ''}")
    if check and drift:
        print("Out-of-date mirrors: " + ", ".join(drift))
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("sync", "check"))
    args = parser.parse_args()
    return sync(check=args.command == "check")


if __name__ == "__main__":
    raise SystemExit(main())
