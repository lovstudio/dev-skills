#!/usr/bin/env python3
"""Diagnose and reversibly repair Clash Verge Rev TUN application failures."""

from __future__ import annotations

import argparse
import datetime as dt
import http.client
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import time
from typing import Any, Dict, Iterable, List, Optional, Tuple


APP_BUNDLE = "Clash Verge"
DEFAULT_SOCKET = Path("/tmp/verge/verge-mihomo.sock")
WECHAT_RULES = [
    "PROCESS-NAME,WeChat,DIRECT",
    "PROCESS-NAME,WeChatAppEx,DIRECT",
    "PROCESS-NAME,WeChatAppEx Helper,DIRECT",
    "DOMAIN-SUFFIX,weixin.qq.com,DIRECT",
    "DOMAIN-SUFFIX,wechat.com,DIRECT",
    "DOMAIN-SUFFIX,servicewechat.com,DIRECT",
    "DOMAIN-SUFFIX,qpic.cn,DIRECT",
    "DOMAIN-SUFFIX,qlogo.cn,DIRECT",
]


class UnixHTTPConnection(http.client.HTTPConnection):
    def __init__(self, socket_path: Path, timeout: float = 3.0) -> None:
        super().__init__("localhost", timeout=timeout)
        self.socket_path = str(socket_path)

    def connect(self) -> None:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect(self.socket_path)
        self.sock = sock


def api_json(socket_path: Path, path: str, method: str = "GET") -> Optional[Dict[str, Any]]:
    if not socket_path.exists():
        return None
    connection = UnixHTTPConnection(socket_path)
    try:
        connection.request(method, path)
        response = connection.getresponse()
        payload = response.read()
        if not 200 <= response.status < 300:
            return None
        return json.loads(payload.decode("utf-8")) if payload else {}
    except (OSError, ValueError, json.JSONDecodeError):
        return None
    finally:
        connection.close()


def resolve_data_dir(cli_value: Optional[str]) -> Path:
    raw = cli_value or os.environ.get("LOVSTUDIO_CLASH_TUN_DOCTOR_DATA_DIR")
    if raw:
        return Path(os.path.expandvars(os.path.expanduser(raw))).resolve()
    if sys.platform == "darwin":
        return Path.home() / "Library/Application Support/io.github.clash-verge-rev.clash-verge-rev"
    raise SystemExit("Cannot auto-detect Clash Verge Rev data directory; pass --data-dir.")


def resolve_socket(data_dir: Path, cli_value: Optional[str]) -> Path:
    if cli_value:
        return Path(os.path.expandvars(os.path.expanduser(cli_value))).resolve()
    if DEFAULT_SOCKET.exists():
        return DEFAULT_SOCKET
    return data_dir / "mihomo.sock"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def yaml_bool(text: str, key: str, indent: int = 0) -> Optional[bool]:
    prefix = " " * indent
    match = re.search(rf"(?m)^{re.escape(prefix + key)}:\s*(true|false)\s*$", text)
    return None if not match else match.group(1) == "true"


def generated_ipv6(text: str) -> Dict[str, Optional[bool]]:
    top = yaml_bool(text, "ipv6", 0)
    dns_value: Optional[bool] = None
    dns_match = re.search(r"(?ms)^dns:\s*\n(?P<body>(?:^[ \t]+.*\n?)*)", text)
    if dns_match:
        dns_value = yaml_bool(dns_match.group("body"), "ipv6", 2)
    return {"top_level": top, "dns": dns_value}


def current_rules_file(data_dir: Path) -> Optional[Path]:
    profile_text = read_text(data_dir / "profiles.yaml")
    current_match = re.search(r"(?m)^current:\s*([^\s#]+)", profile_text)
    if not current_match:
        return None
    current = re.escape(current_match.group(1))
    block_match = re.search(
        rf"(?ms)^- uid:\s*{current}\s*$\n(?P<body>.*?)(?=^- uid:|\Z)", profile_text
    )
    if not block_match:
        return None
    rules_match = re.search(r"(?m)^\s+rules:\s*([^\s#]+)", block_match.group("body"))
    if not rules_match:
        return None
    candidate = data_dir / "profiles" / f"{rules_match.group(1)}.yaml"
    return candidate if candidate.exists() else None


def service_log(data_dir: Path) -> Path:
    return data_dir / "logs/service/service_latest.log"


def filtered_connections(payload: Optional[Dict[str, Any]], app: str) -> List[Dict[str, Any]]:
    if not payload:
        return []
    pattern = re.compile(app, re.IGNORECASE)
    output = []
    for connection in payload.get("connections", []):
        metadata = connection.get("metadata", {})
        haystack = " ".join(
            str(metadata.get(field) or "")
            for field in ("process", "host", "destinationIP")
        )
        if pattern.search(haystack):
            output.append(
                {
                    "network": metadata.get("network"),
                    "process": metadata.get("process"),
                    "host": metadata.get("host"),
                    "destination_ip": metadata.get("destinationIP"),
                    "destination_port": metadata.get("destinationPort"),
                    "rule": connection.get("rule"),
                    "rule_payload": connection.get("rulePayload"),
                    "chains": connection.get("chains", []),
                    "upload": connection.get("upload", 0),
                    "download": connection.get("download", 0),
                }
            )
    return output


def filtered_rules(payload: Optional[Dict[str, Any]], app: str) -> List[Dict[str, Any]]:
    if not payload:
        return []
    terms = [app]
    if app.lower() == "wechat":
        terms += ["weixin", "qpic", "qlogo", "servicewechat"]
    pattern = re.compile("|".join(map(re.escape, terms)), re.IGNORECASE)
    return [
        {"type": item.get("type"), "payload": item.get("payload"), "proxy": item.get("proxy")}
        for item in payload.get("rules", [])
        if pattern.search(str(item.get("payload") or ""))
    ]


def recent_log_findings(log_text: str, app: str, limit: int = 4000) -> Dict[str, Any]:
    lines = log_text.splitlines()[-limit:]
    app_pattern = re.compile(app, re.IGNORECASE)
    relevant = [line for line in lines if app_pattern.search(line)]
    no_route = [line for line in relevant if "no route to host" in line.lower()]
    timeouts = [line for line in relevant if "deadline exceeded" in line.lower() or "i/o timeout" in line.lower()]
    ipv6 = [line for line in relevant if re.search(r"\[[0-9a-f:]{3,}\]", line, re.IGNORECASE)]
    return {
        "matched_lines": len(relevant),
        "no_route_to_host": len(no_route),
        "timeouts": len(timeouts),
        "ipv6_lines": len(ipv6),
        "samples": (no_route + timeouts)[:5],
    }


def diagnose(data_dir: Path, socket_path: Path, app: str) -> Dict[str, Any]:
    app_config = read_text(data_dir / "config.yaml")
    generated = read_text(data_dir / "clash-verge.yaml")
    runtime = api_json(socket_path, "/configs")
    connections = filtered_connections(api_json(socket_path, "/connections"), app)
    ipv6_destinations = sum(1 for item in connections if ":" in str(item.get("destination_ip") or ""))
    return {
        "data_dir": str(data_dir),
        "socket": str(socket_path),
        "app_config_ipv6": yaml_bool(app_config, "ipv6"),
        "generated_ipv6": generated_ipv6(generated),
        "runtime_ipv6": None if runtime is None else runtime.get("ipv6"),
        "rules": filtered_rules(api_json(socket_path, "/rules"), app),
        "connections": connections,
        "ipv6_destinations": ipv6_destinations,
        "logs": recent_log_findings(read_text(service_log(data_dir)), app),
    }


def replace_top_level_ipv6(text: str) -> str:
    pattern = re.compile(r"(?m)^ipv6:\s*(?:true|false)\s*$")
    if pattern.search(text):
        return pattern.sub("ipv6: false", text, count=1)
    suffix = "" if text.endswith("\n") else "\n"
    return text + suffix + "ipv6: false\n"


def replace_prepend(text: str, rules: Iterable[str]) -> str:
    block = ["prepend:\n"] + [
        f'  - {json.dumps(rule, ensure_ascii=False)}\n' for rule in rules
    ]
    lines = text.splitlines(keepends=True)
    start = next((index for index, line in enumerate(lines) if line.startswith("prepend:")), None)
    if start is None:
        return "".join(block) + text.lstrip("\n")
    end = start + 1
    while end < len(lines):
        line = lines[end]
        if line.strip() and not line.startswith((" ", "\t", "#")):
            break
        end += 1
    suffix = lines[end:]
    if suffix and block[-1].endswith("\n"):
        block.append("\n")
    return "".join(lines[:start] + block + suffix)


def stop_clash() -> None:
    if sys.platform != "darwin":
        return
    subprocess.run(
        ["osascript", "-e", f'tell application "{APP_BUNDLE}" to quit'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    for _ in range(30):
        result = subprocess.run(["pgrep", "-x", "clash-verge"], stdout=subprocess.DEVNULL, check=False)
        if result.returncode != 0:
            break
        time.sleep(0.2)


def start_clash() -> None:
    if sys.platform == "darwin":
        subprocess.run(["open", "-a", APP_BUNDLE], check=True)


def backup_files(data_dir: Path, files: Iterable[Path]) -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    root = data_dir / "backups/clash-tun-doctor" / stamp
    root.mkdir(parents=True, exist_ok=False)
    mappings = []
    for index, source in enumerate(files):
        target = root / f"{index:02d}-{source.name}"
        shutil.copy2(source, target)
        mappings.append({"source": str(source), "backup": str(target)})
    (root / "manifest.json").write_text(json.dumps({"files": mappings}, indent=2), encoding="utf-8")
    return root


def wait_for_runtime(socket_path: Path, timeout: float = 15.0) -> Optional[Dict[str, Any]]:
    deadline = time.time() + timeout
    while time.time() < deadline:
        payload = api_json(socket_path, "/configs")
        if payload is not None:
            return payload
        time.sleep(0.25)
    return None


def repair_plan(data_dir: Path) -> Tuple[Path, Path, str, str]:
    config_path = data_dir / "config.yaml"
    rules_path = current_rules_file(data_dir)
    if not config_path.exists():
        raise SystemExit(f"Missing Clash Verge config: {config_path}")
    if rules_path is None:
        raise SystemExit("Cannot resolve current profile rule file from profiles.yaml.")
    return (
        config_path,
        rules_path,
        replace_top_level_ipv6(read_text(config_path)),
        replace_prepend(read_text(rules_path), WECHAT_RULES),
    )


def fix_wechat(data_dir: Path, socket_path: Path, apply: bool, restart: bool) -> int:
    config_path, rules_path, config_new, rules_new = repair_plan(data_dir)
    changes = [
        {"path": str(config_path), "changed": config_new != read_text(config_path), "action": "set global ipv6=false"},
        {"path": str(rules_path), "changed": rules_new != read_text(rules_path), "action": "prepend WeChat DIRECT rules"},
    ]
    if not apply:
        print(json.dumps({"dry_run": True, "changes": changes, "rules": WECHAT_RULES}, ensure_ascii=False, indent=2))
        return 0

    stop_clash()
    backup = backup_files(data_dir, [config_path, rules_path])
    config_path.write_text(config_new, encoding="utf-8")
    rules_path.write_text(rules_new, encoding="utf-8")
    if restart:
        start_clash()
        wait_for_runtime(socket_path)
    result = diagnose(data_dir, socket_path, "wechat")
    verified = result.get("runtime_ipv6") is False and all(
        rule.get("proxy") == "DIRECT" for rule in result.get("rules", [])[: len(WECHAT_RULES)]
    )
    print(json.dumps({"ok": verified, "backup": str(backup), "diagnosis": result}, ensure_ascii=False, indent=2))
    return 0 if verified else 2


def latest_backup(data_dir: Path) -> Optional[Path]:
    root = data_dir / "backups/clash-tun-doctor"
    candidates = sorted((p for p in root.glob("*") if (p / "manifest.json").exists()), reverse=True)
    return candidates[0] if candidates else None


def rollback(data_dir: Path, apply: bool, restart: bool, backup_arg: Optional[str]) -> int:
    root = Path(backup_arg).resolve() if backup_arg else latest_backup(data_dir)
    if root is None:
        raise SystemExit("No clash-tun-doctor backup found.")
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    if not apply:
        print(json.dumps({"dry_run": True, "backup": str(root), "restore": manifest["files"]}, indent=2))
        return 0
    stop_clash()
    for item in manifest["files"]:
        shutil.copy2(item["backup"], item["source"])
    if restart:
        start_clash()
        wait_for_runtime(resolve_socket(data_dir, None))
    print(json.dumps({"ok": True, "restored": str(root)}, indent=2))
    return 0


def print_human(result: Dict[str, Any]) -> None:
    print(f"Data dir: {result['data_dir']}")
    print(
        "IPv6: app-config={app} generated={generated} dns={dns} runtime={runtime}".format(
            app=result["app_config_ipv6"],
            generated=result["generated_ipv6"]["top_level"],
            dns=result["generated_ipv6"]["dns"],
            runtime=result["runtime_ipv6"],
        )
    )
    print(f"Connections: {len(result['connections'])}; IPv6 destinations: {result['ipv6_destinations']}")
    print(
        "Recent logs: no-route={no_route_to_host} timeouts={timeouts} IPv6-lines={ipv6_lines}".format(
            **result["logs"]
        )
    )
    for rule in result["rules"][:12]:
        print(f"Rule: {rule['type']},{rule['payload']} => {rule['proxy']}")
    for sample in result["logs"]["samples"]:
        print(f"Log: {sample}")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--data-dir", help="Clash Verge Rev application data directory")
    root.add_argument("--socket", help="Mihomo controller Unix socket")
    subparsers = root.add_subparsers(dest="command", required=True)

    diagnose_parser = subparsers.add_parser("diagnose", help="Read-only evidence collection")
    diagnose_parser.add_argument("--app", default="wechat", help="Application/process/host filter")
    diagnose_parser.add_argument("--json", action="store_true", help="Emit JSON")

    fix_parser = subparsers.add_parser("fix-wechat", help="Preview or apply WeChat direct/IPv4 repair")
    fix_parser.add_argument("--apply", action="store_true", help="Apply changes")
    fix_parser.add_argument("--no-restart", action="store_true", help="Do not restart Clash Verge")

    rollback_parser = subparsers.add_parser("rollback", help="Preview or restore a repair backup")
    rollback_parser.add_argument("--backup", help="Specific backup directory; newest is default")
    rollback_parser.add_argument("--apply", action="store_true", help="Restore files")
    rollback_parser.add_argument("--no-restart", action="store_true", help="Do not restart Clash Verge")
    return root


def main() -> int:
    args = parser().parse_args()
    data_dir = resolve_data_dir(args.data_dir)
    socket_path = resolve_socket(data_dir, args.socket)
    if args.command == "diagnose":
        result = diagnose(data_dir, socket_path, args.app)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_human(result)
        return 0
    if args.command == "fix-wechat":
        return fix_wechat(data_dir, socket_path, args.apply, not args.no_restart)
    return rollback(data_dir, args.apply, not args.no_restart, args.backup)


if __name__ == "__main__":
    raise SystemExit(main())
