---
name: sgc-electron-app-relaunch
description: >
  这个 Skill 应在用户提出“重启 App”“菜单栏重启 Electron”“第一次重启很慢”“Cmd+Q 后自动重启”“开发态重启白屏”，或 “restart/relaunch an Electron app” 等请求时使用；用于区分刷新、完整重启和更新安装，并验证真实替换进程。
license: MIT
metadata:
  author: lovstudio
  version: "0.2.0"
  tags:
    - electron
    - relaunch
    - lifecycle
    - desktop
    - performance
  compatibility: "Electron main-process applications in development or packaged production mode."
  dependencies: []
---

# Electron 应用重启

为 Electron 桌面应用建立语义清晰、生命周期正确且首轮性能稳定的完整重启机制。把 renderer 重新加载、用户主动退出、完整重启和更新安装视为四种独立意图。

## Triggers

### Activate when

- 用户说“在菜单里增加重启 App”“第一次重启很慢”“Cmd+Q 后又自动启动”或“开发态重启后白屏”。
- 用户把 `Cmd+R`、reload、relaunch、退出再打开混在一起，需要修复真实行为。
- User asks to “restart the app from a menu”, “use app.relaunch”, or “make the first Electron dev relaunch fast and reliable”.

### Do not activate when

- 用户只需要刷新页面或恢复某个 renderer 错误边界；使用 renderer reload。
- 用户要重启某一条 Agent、终端或 PTY 会话；使用会话生命周期工作流。
- 用户只要求安装更新；使用 updater 的 staging、cleanup 和 installation handoff。

## Workflow (MANDATORY)

按顺序执行以下步骤。

### Step 0：先定义动作和成功标准

- 把每个入口映射到唯一意图：renderer reload、full app relaunch、user quit 或 update installation handoff。
- 保留 `Cmd+R` / `Ctrl+R` 给“重新加载”，不要意外绑定到完整重启。
- 把 `Cmd+Q` 定义为用户退出；不得让重启助手、watcher 或守护进程再次拉起 App。
- 在实现前完整读取 [references/relaunch-contract.md](references/relaunch-contract.md)。遇到首轮慢、冷/热差异、白屏或端口冲突时，再读取 [references/first-relaunch-performance.md](references/first-relaunch-performance.md)。

### Step 1：识别开发态启动拓扑

- 记录实际 Electron main PID、`process.execPath`、`process.argv.slice(1)`、工作目录、父进程、启动时间、renderer/dev-server 端口和启动命令。wrapper 的 executable/args 必须从 wrapper 启动契约单独保存，不要从 Electron argv 猜测。
- 判断当前属于哪一种拓扑：自包含 Electron 进程、外部且持续存活的 dev server，或由 `electron-vite`、Vite、`concurrently`、pnpm 等 wrapper 共同拥有的进程树。
- 仅在 Electron 子进程本身足以恢复完整开发环境时，使用显式 `execPath` 和 `args` 的 `app.relaunch()`。
- 当 wrapper 同时拥有 dev server、main 构建或 watcher 时，先验证旧 owner 是否会随 Electron 收束。会收束时使用一次性 helper 复用真实开发命令；不会收束时向既有 owner 发送 relaunch intent，或让外部 supervisor 替换整棵进程树，避免重复工具链。

### Step 2：集中完整重启路径

- 在 main process 中建立一个完整重启函数，由原生菜单或 typed IPC 统一调用。
- 在 packaged production 中调用 `app.relaunch()`，随后调用 `app.quit()`，让 `before-quit` / `will-quit` 清理正常完成。
- 在安排 `app.relaunch()` 前完成未保存内容确认和所有可能取消退出的检查。若窗口的 `beforeunload` 仍可阻止 `app.quit()`，不要预先留下一个迟发的后继实例。
- 在 development 中于 App 启动时保存不可变的 relaunch plan：可执行文件、参数、cwd、稳定环境和进程所有权；不要等到点击菜单后再从已变化的运行环境猜测。
- 保持 renderer reload 独立，并在 UI 中分别使用“重新加载”和“重启 {App 名称}”。
- 保持 updater handoff 独立；普通重启函数不得抢占“安装并重启”。

### Step 3：稳定第一次重启性能

- 分别测量第一次、第二次和第三次重启；不要用后两次的热缓存掩盖首轮问题。
- 将启动环境分为稳定配置和运行时注入变量。helper 继承启动时保存的稳定环境，并只移除已确认会污染下一次启动的临时 PID、socket、inspector、child-channel 或构建输出变量。
- 避免通过 login shell、`shell: true` 或另一套 package-manager wrapper 改写 PATH、编译器、runtime 或缓存指纹；优先使用参数数组直接 spawn。
- 用旧 PID 已退出、端口已释放、single-instance lock 可获得和 dev server ready 等真实条件推进流程；避免固定秒数的 `sleep`。
- 在安全的前提下并行启动 renderer server 与 main build。源代码未变化时，完整重启不得触发依赖安装、原生模块重建或整套 main bundle 重编译。
- 若首轮仍明显慢，按 performance reference 区分构建指纹变化、旧进程树收束、端口等待、Chromium 冷启动和业务初始化，再优化占时最长的一段。

### Step 4：保护进程所有权与退出语义

- 为 shutdown intent 建立显式状态：`user-quit`、`relaunch`、`install-update`。只允许后两者安排后继进程。
- 明确 PTY、child process、local server、watcher 和 tray 的策略：关闭、保留、等待还是由新实例重新连接。
- 先走产品要求的 graceful cleanup，再退出旧 main process；为卡住的子进程设置有界超时和可诊断日志。
- 等待旧实例释放 single-instance lock 后再启动替代实例，避免新实例被 `second-instance` 路径吞掉。
- 防止一次菜单点击安排多个 helper；使用 main-process guard，并在安排失败或退出被取消时撤销状态、保留当前 App 可用。

### Step 5：验证真实替换实例

- 为生产态 relaunch、开发态命令构造、环境归一化、shutdown intent 和重复点击 guard 添加聚焦测试。
- 运行真实 App，记录旧实例 PID、可执行路径、cwd 和启动时间；点击一次原生“重启”菜单。
- 验证新 PID、更新后的启动时间、预期可执行路径、正确 cwd、单一 renderer server、单一 main process，以及可交互窗口。以 load Promise/`did-finish-load`、显示/聚焦状态和应用级 health signal 组合定义 readiness，并记录 `did-fail-load`；只把 `ready-to-show` 当可选信号。
- 连续测量至少三次完整重启。若第一次比后两次中位数多 1 秒且达到其 2 倍，继续调查，不把它归结为“正常冷启动”。
- 再执行一次 `Cmd+Q`，确认没有 helper、watcher 或 launch agent 自动拉起 App，端口也已释放。
- 不把菜单文案存在、bundle 中出现字符串、renderer reload、编译成功或 HTTP 200 当作完整重启证据。

## Deliverable

交付时报告：动作映射、开发态启动拓扑、进程所有权、第一次与热重启耗时、真实 PID 替换证据、退出后残留检查，以及仍存在的冷启动成本。

## Dependencies

- Electron main-process access。
- 目标项目的真实 development command 与进程所有权信息。
