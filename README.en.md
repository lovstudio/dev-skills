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

## Skills

<!-- COUNT:START -->
> **12 skills** — 12 Free + 0 Paid.
<!-- COUNT:END -->

<!-- SKILLS:START -->
| | Skill | Description |
|---|---|---|
| **Meta** | | |
| ![Free](https://img.shields.io/badge/Free-green) | [`skill-creator`](https://github.com/lovstudio/skill-creator-skill) | Scaffold a new Claude Code skill as an independent repo or dev-skills bundle entry. |
| ![Free](https://img.shields.io/badge/Free-green) | [`skill-optimizer`](https://github.com/lovstudio/skill-optimizer-skill) | Audit an existing skill, auto-fix issues, and bump its version in one pass. |
| **Dev Tools** | | |
| ![Free](https://img.shields.io/badge/Free-green) | [`auto-context`](https://github.com/lovstudio/auto-context-skill) | Watch your Claude Code context for pollution and suggest when to fork or reset. |
| ![Free](https://img.shields.io/badge/Free-green) | [`cc-migrate-session`](https://github.com/lovstudio/cc-migrate-session/tree/main/skill/lovstudio-cc-mv) | Keep your Claude Code session history working after you move a project folder. |
| ![Free](https://img.shields.io/badge/Free-green) | [`deploy-to-vercel`](https://github.com/lovstudio/deploy-to-vercel-skill) | Ship a frontend to Vercel with custom domain and Cloudflare DNS wired up automatically. |
| ![Free](https://img.shields.io/badge/Free-green) | [`finder-action`](https://github.com/lovstudio/finder-action-skill) | Add a custom right-click action to macOS Finder in minutes. |
| ![Free](https://img.shields.io/badge/Free-green) | [`gh-access`](https://github.com/lovstudio/gh-access-skill) | Grant, revoke, or audit collaborator access on private GitHub repos in one command. |
| ![Free](https://img.shields.io/badge/Free-green) | [`gh-contribute`](https://github.com/lovstudio/gh-contribute-skill) | Ship a clean PR to any upstream GitHub repo — fork, branch, push, and open PR for you. |
| ![Free](https://img.shields.io/badge/Free-green) | [`gh-tidy`](https://github.com/lovstudio/gh-tidy-skill) | Triage and clean up GitHub issues, PRs, branches, and labels in a single pass. |
| ![Free](https://img.shields.io/badge/Free-green) | [`install-tanstack-query`](https://github.com/lovstudio/dev-skills/tree/main/skills/install-tanstack-query) | Initialize TanStack Query and migrate request state into shared query keys and hooks. |
| ![Free](https://img.shields.io/badge/Free-green) | [`obsidian-reset-cache`](https://github.com/lovstudio/obsidian-reset-cache-skill) | Reset Obsidian's cache when it gets stuck on "Loading cache". |
| ![Free](https://img.shields.io/badge/Free-green) | [`project-port`](https://github.com/lovstudio/project-port-skill) | Assign each project a stable, unique dev port so services stop colliding. |
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
