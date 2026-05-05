<h1 align="center">Lovstudio Dev Skills</h1>

<p align="center">
  <strong>Lovstudio 面向开发者与技能作者的 Claude Code 技能子索引。</strong><br>
  <sub>由 <a href="https://lovstudio.ai">Lovstudio</a> 出品 · <a href="https://agentskills.io">agentskills.io</a></sub>
</p>

<p align="center">
  <b>简体中文</b> · <a href="README.en.md">English</a>
</p>

<p align="center">
  <a href="#技能列表">技能</a> ·
  <a href="#安装">安装</a> ·
  <a href="#相关索引">相关索引</a> ·
  <a href="#许可证">许可证</a>
</p>

---

## 这是什么

本仓库是 Lovstudio 技能体系中**面向开发者与技能作者**的子索引，是 [`lovstudio/skills`](https://github.com/lovstudio/skills) 主索引的专题分支。

- **Meta** — 创建 / 体检 / 优化 Claude Code skill 自身的元技能
- **Dev Tools** — 日常开发流程中用得上的工具类技能（GitHub、Vercel、macOS、Claude Code session 等）

每个技能仍然在自己的独立仓库 `github.com/lovstudio/{name}-skill` 里。本仓库只维护索引与镜像。

## 技能列表

<!-- COUNT:START -->
> **12 个技能** — 12 个免费 + 0 个付费。
<!-- COUNT:END -->

<!-- SKILLS:START -->
| | 技能 | 描述 |
|---|---|---|
| **元技能** | | |
| ![Free](https://img.shields.io/badge/Free-green) | [技能脚手架 · `skill-creator`](https://github.com/lovstudio/skill-creator-skill) | 一条命令生成规范的 Claude Code 技能骨架，支持独立仓库或 dev-skills 聚合分发。 |
| ![Free](https://img.shields.io/badge/Free-green) | [技能优化器 · `skill-optimizer`](https://github.com/lovstudio/skill-optimizer-skill) | 一键体检并修复现有技能，自动升版本号并追加 CHANGELOG。 |
| **开发工具** | | |
| ![Free](https://img.shields.io/badge/Free-green) | [上下文体检 · `auto-context`](https://github.com/lovstudio/auto-context-skill) | 监测 Claude Code 上下文是否被污染，适时提示你 /fork 或 /btw。 |
| ![Free](https://img.shields.io/badge/Free-green) | [会话迁移 · `cc-migrate-session`](https://github.com/lovstudio/cc-migrate-session/tree/main/skill/lovstudio-cc-mv) | 项目目录搬家后，让 Claude Code 的历史会话还能正常 `--resume`。 |
| ![Free](https://img.shields.io/badge/Free-green) | [部署到 Vercel · `deploy-to-vercel`](https://github.com/lovstudio/deploy-to-vercel-skill) | 一键把前端部署到 Vercel，自动配好 Cloudflare DNS 和自定义域名。 |
| ![Free](https://img.shields.io/badge/Free-green) | [访达右键动作 · `finder-action`](https://github.com/lovstudio/finder-action-skill) | 几分钟给 macOS 访达右键菜单加一个你自己的动作。 |
| ![Free](https://img.shields.io/badge/Free-green) | [GitHub 协作者管理 · `gh-access`](https://github.com/lovstudio/gh-access-skill) | 一条命令给私有 GitHub 仓库加减协作者权限，或盘点现有访问清单。 |
| ![Free](https://img.shields.io/badge/Free-green) | [GitHub 投稿 PR · `gh-contribute`](https://github.com/lovstudio/gh-contribute-skill) | 给任意上游 GitHub 仓库提一份干净的 PR——fork、分支、推送、开 PR 一站搞定。 |
| ![Free](https://img.shields.io/badge/Free-green) | [GitHub 仓库整理 · `gh-tidy`](https://github.com/lovstudio/gh-tidy-skill) | 一次过清理 GitHub 上的 issue、PR、分支和标签，让仓库重新整洁。 |
| ![Free](https://img.shields.io/badge/Free-green) | [TanStack Query 初始化 · `install-tanstack-query`](https://github.com/lovstudio/dev-skills/tree/main/skills/install-tanstack-query) | 初始化 TanStack Query，并把分散的请求状态收敛到统一 query keys 和 hooks。 |
| ![Free](https://img.shields.io/badge/Free-green) | [重置 Obsidian 缓存 · `obsidian-reset-cache`](https://github.com/lovstudio/obsidian-reset-cache-skill) | Obsidian 卡在 Loading cache 时，一键重置缓存救场。 |
| ![Free](https://img.shields.io/badge/Free-green) | [项目端口分配 · `project-port`](https://github.com/lovstudio/project-port-skill) | 给每个项目分配一个稳定且唯一的开发端口，彻底告别端口撞车。 |
<!-- SKILLS:END -->

<sub>上表由 [`scripts/render-readme.py`](scripts/render-readme.py) 从 [`skills.yaml`](skills.yaml) 自动生成。请编辑 `skills.yaml`，不要手动改表格。</sub>

## 安装

**通过 `npx skills`**（vercel-labs CLI，跨 agent 通用）：

```bash
npx skills add lovstudio/dev-skills
```

**通过 Claude Code 原生 marketplace**：

```
/plugin marketplace add lovstudio/dev-skills
/plugin install dev-tools@lovstudio-dev
/plugin install meta@lovstudio-dev
```

也可以从各自独立仓库单独安装，详见各 skill 的 README。

## 相关索引

- [`lovstudio/skills`](https://github.com/lovstudio/skills) — Lovstudio 所有技能的主索引
- [`lovstudio/xbti-skills`](https://github.com/lovstudio/xbti-skills) — xBTI 人格测试相关技能

## 许可证

- **本索引仓库**：MIT
- **免费技能**：MIT（详见各仓库的 LICENSE）

---

<p align="center">
  <sub>使用 <a href="https://claude.com/claude-code">Claude Code</a> 构建 · 由 <a href="https://lovstudio.ai">Lovstudio</a> 出品</sub>
</p>
