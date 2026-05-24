---
name: lovstudio-app-generator
description: >
  Generate or standardize Lovstudio cross-platform apps, especially Tauri +
  React + shadcn/ui + TanStack Query projects with Lovstudio branding, CI/CD,
  auto update, and lovinsp. Use when the user asks to create a Lovstudio app,
  scaffold a Tauri app, initialize an app shell, apply Lovstudio app standards,
  or mentions "App生成器", "新建 Lovstudio App", "生成跨端 App",
  "create Lovstudio app", "scaffold Tauri app", or "Lovstudio app generator".
license: MIT
compatibility: >
  Requires Python 3.8+ for the project audit helper. Designed for React,
  TypeScript, Vite, Tauri, shadcn/ui, TanStack Query, GitHub Actions, and
  Lovstudio Warm Academic branded apps. New apps must generate a
  target-specific logo through `lovstudio:gen-logo` before the Tauri icon
  pipeline is run.
metadata:
  author: lovstudio
  version: "0.2.0"
  tags: lovstudio app-generator tauri react shadcn tanstack-query cicd updater lovinsp
---

# app-generator — Lovstudio App 生成器

Use this skill to create or upgrade a Lovstudio-grade cross-platform app. The
default architecture is Tauri + React + TypeScript + shadcn/ui + TanStack
Query, with Lovstudio brand assets, Warm Academic UI, CI/CD, auto update, and
lovinsp click-to-code support.

## When to Use

- The user asks to generate a new Lovstudio app or cross-platform app.
- The user has an existing frontend/Tauri project and wants it brought up to
  Lovstudio app standards.
- The user mentions Tauri, shadcn, React Query / TanStack Query, auto update,
  CI/CD, app logo, Lovstudio logo, Warm Academic UI, or lovinsp as part of app
  setup.
- The project is a LovStudio, Lovpen, Lovcode, Lovmind, Lovshot, Lovsider,
  Lovsigil, or Lovtarot app.

## Workflow (MANDATORY)

**You MUST follow these steps in order:**

### Step 1: Clarify the App Brief

Collect only the missing fields. Use conversation context first. Prefer
`AskUserQuestion` for interactive choices; if that tool is unavailable, ask
short direct questions and continue once the answer is clear.

Required fields:

| Field | Default | Notes |
|---|---|---|
| App name | Ask user | Product/display name, e.g. `Lovshot` |
| Project slug | Derived from app name | Lowercase kebab-case |
| Brand scope | `Lovstudio` | Ask if ambiguous between Lovstudio / LovPen / personal brand |
| Target mode | `new app` | `new app` or `upgrade existing app` |
| Platforms | `macOS first, Windows/Linux ready` | Tauri desktop unless user says web-only |
| Core screens | Ask user | 2-5 concrete screens or workflows |
| Backend/API | Ask user if needed | Tauri commands, REST, Supabase, local files, etc. |
| Distribution | `GitHub Releases + Tauri updater` | Ask if using a different channel |

If the user asks for a real implementation and enough information is present,
make conservative assumptions and proceed.

Suggested options to collect interactively:

| Question | Recommended choice |
|---|---|
| Target mode | `New Tauri app` |
| Brand scope | `Lovstudio` |
| UI baseline | `Warm Academic + shadcn/ui` |
| Data layer | `TanStack Query` |
| Release channel | `GitHub Releases + Tauri updater` |

### Step 2: Read Local Context

Before changing files, inspect the target project:

```bash
pwd
find .. -name AGENTS.md -print
find .. -name CLAUDE.md -print
ls
find . -maxdepth 2 -type f \( -name package.json -o -name vite.config.ts -o -name tauri.conf.json -o -name tauri.conf.json5 -o -name Cargo.toml \) -print
```

Honor any project-level instructions. If the target lives under a symlinked
workspace, follow that project's own AGENTS.md / CLAUDE.md.

### Step 3: Run the Lovstudio App Audit

Run the helper from the target project root:

```bash
python3 ~/.claude/skills/lovstudio-app-generator/scripts/audit_app_project.py --root . --format markdown
```

Use the output as the implementation checklist. For new projects, the audit
will mostly report missing pieces; that is expected.

### Step 4: Choose the Implementation Path

#### New Tauri App

Default stack:

```bash
pnpm create vite@latest <project-slug> -- --template react-ts
cd <project-slug>
pnpm add @tauri-apps/api @tanstack/react-query lucide-react
pnpm add -D @tauri-apps/cli typescript
pnpm tauri init
```

Then apply the Lovstudio layers in this order:

1. Project identity: package name, app title, bundle identifier, README, and
   app-specific CLAUDE.md.
2. Warm Academic UI: shadcn/ui, semantic tokens, typography, and layout.
3. Server state: TanStack Query provider, query keys, and Tauri invoke wrappers.
4. Brand assets: generate a target-specific app logo with
   `lovstudio:gen-logo`, publish the chosen version into `assets/` and
   `public/`, prepare a macOS-safe padded icon source, then run the Tauri icon
   pipeline from that generated logo.
5. Lovinsp: click-to-code integration.
6. CI/CD: typecheck, lint/build where available, Tauri release workflow.
7. Auto update: Tauri updater plugin, signing keys/env placeholders, release
   endpoint wiring.
8. Verification: typecheck, build, and app launch where practical.

#### Upgrade Existing App

Do not rebuild the project from scratch. Patch the smallest surface needed:

1. Keep the existing package manager, router, folder layout, aliases, and style
   conventions unless they conflict with Lovstudio requirements.
2. Add missing Lovstudio layers from the audit.
3. Preserve user code and unrelated changes.
4. Prefer incremental commits/checkpoints when the app is already substantial.

### Step 5: Apply Brand and UI Standards

New apps must not use the canonical Lovstudio logo as the app/product icon.
After the project identity and README describe the target clearly, invoke the
`lovstudio:gen-logo` workflow from the new app root:

1. Generate `assets/logo-drafts/v1-*.png` and `.svg` based on what the app does,
   not a literal reading of its name.
2. Publish the chosen draft to `assets/logo.png`, `assets/logo.svg`,
   `public/logo.png`, and `public/logo.svg`.
3. Before feeding the generated logo into the Tauri icon pipeline, ensure the
   icon source has transparent safe area. Do not use a 512x512 edge-to-edge
   filled icon as the macOS app icon source; it appears oversized in Dock,
   Launchpad, and Finder. Prefer roughly 40-56px transparent padding on a
   512x512 canvas, or a content bounding box around 80-85% of the canvas.
4. Use that padded generated logo as the source for
   `lovstudio:install-tauri-logo` and any favicon/tray-icon generation.

For upgrades, keep an existing product logo unless the user asks to refresh it;
if the app has no logo, use `lovstudio:gen-logo` before generating icons.

Canonical assets:

| Asset | Path |
|---|---|
| Lovstudio square logo folder | `/Users/mark/lovstudio/brand/Lovstudio - logo - square` |
| Lovstudio PNG logo | `/Users/mark/lovstudio/brand/Lovstudio - logo - square/Lovstudio-logo.png` |
| Lovstudio SVG logo | `/Users/mark/lovstudio/brand/Lovstudio - logo - square/Lovstudio-logo.svg` |
| Warm Academic guide | `/Users/mark/lovstudio/design/design-guide.md` |

Rules:

- Treat the canonical Lovstudio logo as brand reference or fallback only, not as
  the default app icon for new apps.
- For Tauri/macOS icons, verify the generated app icon is visually aligned with
  normal macOS app icons. If ImageMagick is available, a quick sanity check is:
  `magick src-tauri/icons/icon.png -alpha extract -trim -format '%wx%h%O\n' info:`;
  for a 512x512 source, content around `400x400` to `440x440` with positive
  offsets is usually safer than `512x512+0+0`.
- Use semantic Tailwind classes such as `bg-background`, `text-foreground`,
  `bg-primary`, `border-border`; do not hard-code brand hex values in UI
  components.
- Keep the UI operational and app-like. Do not create a marketing landing page
  when the user asked for an app.
- Use shadcn/ui controls, lucide icons, compact panels, predictable navigation,
  and no nested cards.
- First screen should be the real product workflow.

When shadcn/ui is needed, use the existing `lovstudio:install-shadcn-ui` skill
as the detailed reference. When TanStack Query is needed, use
`lovstudio:install-tanstack-query`. When app icons are needed, use
`lovstudio:install-tauri-logo`; for new apps, run `lovstudio:gen-logo` first
and feed the generated logo into the icon pipeline.

### Step 6: Tauri App Baseline

For Tauri apps, check these areas:

| Area | Expected |
|---|---|
| `src-tauri/tauri.conf.*` | app title, identifier, windows, bundle metadata |
| `src-tauri/Cargo.toml` | Tauri plugins, app metadata, updater if enabled |
| Rust commands | typed command boundary, no broad stringly APIs where avoidable |
| Frontend API | `invoke()` wrapped through query/mutation helpers for server state |
| Filesystem/native APIs | least permission needed in Tauri capabilities |
| Icons | generated through Tauri icon pipeline from the target-specific logo produced by `lovstudio:gen-logo` |
| Dev server | stable project port, preferably via `lovstudio-project-port` |

### Step 7: CI/CD and Auto Update

Default GitHub Actions surface:

- `check.yml`: install, typecheck, lint/build if present.
- `release.yml`: Tauri build for target platforms, draft or publish GitHub
  Release, attach artifacts.
- Tauri updater wiring: plugin dependency, updater config, signing key env
  placeholders, and documented release process.
- For Tauri v2, `plugins.updater.pubkey` is required at runtime. Do not leave
  it out even during early scaffolding: a missing `pubkey` causes the app to
  panic during updater plugin initialization. Use a clear placeholder such as
  `PLACEHOLDER_REPLACE_WITH_TAURI_SIGNER_PUBLIC_KEY` until the real public key
  is generated with `pnpm tauri signer generate`.

Do not invent secrets. Use placeholder names and document where the user must
set them:

- `TAURI_SIGNING_PRIVATE_KEY`
- `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`
- platform signing/notarization secrets as required by the target app

### Step 8: Lovinsp

Integrate lovinsp for frontend development unless the project is not browser/UI
based. Prefer the existing `lovstudio:install-lovinsp` workflow and keep it
idempotent.

For Vite apps, confirm the Vite config imports and registers
`lovinspPlugin({ bundler: "vite" })` before the framework plugin, not merely
that the package is installed. In dev mode, verify the served module contains
`lovinsp-component` or `[lovinsp v...]`:

```bash
curl -s http://127.0.0.1:<port>/src/main.tsx | rg "lovinsp-component|lovinsp v"
```

For Tauri apps, prefer launching dev mode through a persistent session when the
user wants to keep it running after the turn:

```bash
tmux new-session -d -s <slug>-dev -c "$PWD" 'pnpm tauri dev'
tmux capture-pane -pt <slug>-dev -S -120
```

### Step 9: Verification

Run the lightest reliable checks that the target repo supports:

```bash
pnpm exec tsc --noEmit --pretty false
pnpm build
pnpm tauri build --debug
```

Adjust for npm/yarn/bun and local instructions. If a dev server is needed to
verify frontend behavior, start it and give the user the local URL.

For UI changes, use browser or screenshot verification when practical. For
Tauri-native behavior, report what was and was not verified.

## CLI Reference

| Argument | Default | Description |
|----------|---------|-------------|
| `--root` | `.` | Target app root to inspect |
| `--format` | `markdown` | `markdown` or `json` |
| `--output` | stdout | Optional path to write the report |

## Dependencies

```bash
python3 ~/.claude/skills/lovstudio-app-generator/scripts/audit_app_project.py --help
```

No Python packages are required.

## Final Response Checklist

Report:

- App path and stack chosen.
- Lovstudio layers added or confirmed: brand, UI, Tauri, TanStack Query,
  lovinsp, CI/CD, updater.
- Commands/checks run and their result.
- Any remaining secrets, signing steps, or manual app-store/release actions.
