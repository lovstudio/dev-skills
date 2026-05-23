# lovstudio-app-generator

![Version](https://img.shields.io/badge/version-0.1.0-CC785C)

Generate or standardize Lovstudio cross-platform apps with Tauri, React,
shadcn/ui, TanStack Query, Lovstudio branding, CI/CD, auto update, and lovinsp.

Part of [lovstudio dev-skills](https://github.com/lovstudio/dev-skills) — by [lovstudio.ai](https://lovstudio.ai)

## Install

```bash
npx skills add lovstudio/dev-skills
```

Or through Claude Code plugin marketplace:

```text
/plugin marketplace add lovstudio/dev-skills
/plugin install dev-tools@lovstudio-dev
```

Requires: Python 3.8+ for the audit helper. No Python packages are required.

## Usage

```bash
# Ask the assistant:
生成一个 Lovstudio Tauri App，品牌用 Lovstudio，包含 shadcn、TanStack Query、CI/CD、自动更新和 lovinsp

# Or audit an existing app:
python3 ~/.claude/skills/lovstudio-app-generator/scripts/audit_app_project.py --root . --format markdown
```

## What It Does

1. Collects the app brief: name, slug, platform, screens, backend, and release channel.
2. Audits the target project for Lovstudio app requirements.
3. Guides new app scaffolding or incremental upgrade.
4. Applies the Warm Academic UI system and Lovstudio brand asset paths.
5. Coordinates related Lovstudio skills:
   `install-shadcn-ui`, `install-tanstack-query`, `install-tauri-logo`,
   `install-lovinsp`, and `project-port`.
6. Adds or checks CI/CD and Tauri updater wiring.
7. Runs the lightest reliable verification commands available in the project.

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--root` | `.` | Target app root to inspect |
| `--format` | `markdown` | Output format: `markdown` or `json` |
| `--output` | stdout | Optional path to write the audit report |

## Brand Defaults

| Asset | Path |
|---|---|
| Lovstudio square logo folder | `/Users/mark/lovstudio/brand/Lovstudio - logo - square` |
| Lovstudio logo PNG | `/Users/mark/lovstudio/brand/Lovstudio - logo - square/Lovstudio-logo.png` |
| Lovstudio logo SVG | `/Users/mark/lovstudio/brand/Lovstudio - logo - square/Lovstudio-logo.svg` |
| Warm Academic design guide | `/Users/mark/lovstudio/design/design-guide.md` |

## Audit Helper

```bash
python3 ~/.claude/skills/lovstudio-app-generator/scripts/audit_app_project.py --root /path/to/app
python3 ~/.claude/skills/lovstudio-app-generator/scripts/audit_app_project.py --root /path/to/app --format json
```

## License

MIT
