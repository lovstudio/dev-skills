<h1 align="center">Lovstudio Dev Skills</h1>

<p align="center">
  <strong>Lovstudio skills for developers and skill authors on Claude Code.</strong><br>
  <sub>By <a href="https://lovstudio.ai">Lovstudio</a> · <a href="https://agentskills.io">agentskills.io</a></sub>
</p>

<p align="center">
  <a href="README.md">简体中文</a> · <b>English</b>
</p>

<p align="center">
  <a href="#skills">Skills</a> ·
  <a href="#install">Install</a> ·
  <a href="#related-indexes">Related indexes</a> ·
  <a href="#license">License</a>
</p>

---

## What Is This

This repo is the **developer-focused sub-index** of the Lovstudio skill catalog — a thematic slice of the main [`lovstudio/skills`](https://github.com/lovstudio/skills) index.

- **Meta** — meta-skills for creating, auditing, and optimizing Claude Code skills themselves
- **Dev Tools** — everyday developer utilities (GitHub, Vercel, macOS, Claude Code session management)

Each skill still lives in its own `github.com/lovstudio/{name}-skill` repo. This repo only maintains the index + mirror.

- [`pricing-cards/`](pricing-cards) — one Pricing Card per Skill, covering the deliverable, public price, value anchor, usage boundary, maintenance trigger, and evidence gaps; the website consumes only the curated public fields.

## Skills

Each Skill uses `lovstudio/{name}-skill` as its independent source of truth.
The `skills/` directory here is an installable mirror synced from the latest
GitHub Release of each source repository.

<!-- COUNT:START -->
> **22 skills** — 22 Free + 0 Paid.
<!-- COUNT:END -->

<!-- SKILLS:START -->
| | Skill | Description |
|---|---|---|
| **Meta** | | |
| ![Free](https://img.shields.io/badge/Free-green) | [`skill-creator`](https://github.com/lovstudio/skill-creator-skill) | Scaffold a new skill as an independent source repo with release-driven aggregate distribution. |
| ![Free](https://img.shields.io/badge/Free-green) | [`skill-optimizer`](https://github.com/lovstudio/skill-optimizer-skill) | Audit an existing skill, auto-fix issues, and bump its version in one pass. |
| **Dev Tools** | | |
| ![Free](https://img.shields.io/badge/Free-green) | [`app-generator`](https://github.com/lovstudio/app-generator-skill) | Generate Lovstudio-grade web, PWA, or Tauri apps with brand, UI, data, deploy/release, and developer tooling wired in. |
| ![Free](https://img.shields.io/badge/Free-green) | [`auto-context`](https://github.com/lovstudio/auto-context-skill) | Watch your Claude Code context for pollution and suggest when to fork or reset. |
| ![Free](https://img.shields.io/badge/Free-green) | [`cc-migrate-session`](https://github.com/lovstudio/cc-migrate-session/tree/main/skill/sgc-cc-mv) | Keep your Claude Code session history working after you move a project folder. |
| ![Free](https://img.shields.io/badge/Free-green) | [`clash-tun-doctor`](https://github.com/lovstudio/clash-tun-doctor-skill) | Diagnose Clash TUN failures from runtime evidence, apply reversible fixes, and verify the real application path. |
| ![Free](https://img.shields.io/badge/Free-green) | [`deploy-to-vercel`](https://github.com/lovstudio/deploy-to-vercel-skill) | Ship a frontend to Vercel with custom domain and Cloudflare DNS wired up automatically. |
| ![Free](https://img.shields.io/badge/Free-green) | [`electron-app-relaunch`](https://github.com/lovstudio/electron-app-relaunch-skill) | Add a real Electron relaunch while keeping renderer reload and update handoff separate. |
| ![Free](https://img.shields.io/badge/Free-green) | [`electron-delta-updater`](https://github.com/lovstudio/electron-delta-updater-skill) | Build verified Electron delta updates with Sparkle, appcasts, signing, and installation proof. |
| ![Free](https://img.shields.io/badge/Free-green) | [`finder-action`](https://github.com/lovstudio/finder-action-skill) | Add a custom right-click action to macOS Finder in minutes. |
| ![Free](https://img.shields.io/badge/Free-green) | [`gh-access`](https://github.com/lovstudio/gh-access-skill) | Grant, revoke, or audit collaborator access on private GitHub repos in one command. |
| ![Free](https://img.shields.io/badge/Free-green) | [`gh-contribute`](https://github.com/lovstudio/gh-contribute-skill) | Ship a clean PR to any upstream GitHub repo — fork, branch, push, and open PR for you. |
| ![Free](https://img.shields.io/badge/Free-green) | [`gh-tidy`](https://github.com/lovstudio/gh-tidy-skill) | Triage and clean up GitHub issues, PRs, branches, and labels in a single pass. |
| ![Free](https://img.shields.io/badge/Free-green) | [`install-ai`](https://github.com/lovstudio/install-ai-skill) | Add an App AI feature with Agent Client, MaaS routing, model intent, and optional UI. |
| ![Free](https://img.shields.io/badge/Free-green) | [`install-tanstack-query`](https://github.com/lovstudio/install-tanstack-query-skill) | Initialize TanStack Query and migrate request state into shared query keys and hooks. |
| ![Free](https://img.shields.io/badge/Free-green) | [`mobile-adapt`](https://github.com/lovstudio/mobile-adapt-skill) | Scan a web project for mobile issues and fix them — overflow, safe area, viewport units, responsive layouts, and page navigation. |
| ![Free](https://img.shields.io/badge/Free-green) | [`obsidian-reset-cache`](https://github.com/lovstudio/obsidian-reset-cache-skill) | Reset Obsidian's cache when it gets stuck on "Loading cache". |
| ![Free](https://img.shields.io/badge/Free-green) | [`optimize-tauri-backend`](https://github.com/lovstudio/optimize-tauri-backend-skill) | Reduce Tauri Rust restart pain by modularizing the backend, shrinking command surfaces, and hardening long IPC streams. |
| ![Free](https://img.shields.io/badge/Free-green) | [`project-port`](https://github.com/lovstudio/project-port-skill) | Assign each project a stable, unique dev port so services stop colliding. |
| ![Free](https://img.shields.io/badge/Free-green) | [`release-via-cicd`](https://github.com/lovstudio/release-via-cicd-skill) | Configure release workflows, publish versions, and verify signed Tauri app artifacts. |
| ![Free](https://img.shields.io/badge/Free-green) | [`skill-distiller`](https://github.com/lovstudio/skill-distiller-skill) | Turn delivery history into a clear, reusable Skill blueprint with boundaries and acceptance checks. |
| ![Free](https://img.shields.io/badge/Free-green) | [`skill-publisher`](https://github.com/lovstudio/skill-publisher-skill) | Publish a validated Skill across channels while keeping each release state independently verifiable. |
<!-- SKILLS:END -->

<sub>The table above is auto-generated from [`skills.yaml`](skills.yaml) by [`scripts/render-readme.py`](scripts/render-readme.py). Edit `skills.yaml`, not this table.</sub>

## Install

**Via `npx skills`** (vercel-labs CLI, cross-agent):

```bash
npx skills add lovstudio/dev-skills
```

**Via Claude Code native marketplace**:

```
/plugin marketplace add lovstudio/dev-skills
/plugin install dev-tools@lovstudio-dev
/plugin install meta@lovstudio-dev
```

Or install any single skill directly from its own repo — see each skill's README.

## Related indexes

- [`lovstudio/skills`](https://github.com/lovstudio/skills) — Lovstudio main skill index
- [`lovstudio/xbti-skills`](https://github.com/lovstudio/xbti-skills) — xBTI personality-test skills

## License

- **This index repo**: MIT
- **Free skills**: MIT (see each repo's LICENSE)

---

<p align="center">
  <sub>Built with <a href="https://claude.com/claude-code">Claude Code</a> · by <a href="https://lovstudio.ai">Lovstudio</a></sub>
</p>
